"""
Handles downloading the search results page over HTTP.

This is the only file that talks to the network. Keeping the network
call separate from the HTML parsing (parser.py) means:
  - we can test parser.py offline using a saved HTML file
  - if the website changes its transport (e.g. adds a required cookie),
    only this file needs to change
"""

import requests
import cloudscraper

# A realistic browser User-Agent. Without this, many sites (including
# mdcomputers.in) reject the request before it even reaches their
# application code, because it looks like a script instead of a browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

REQUEST_TIMEOUT_SECONDS = 15


class ScraperError(Exception):
    """Raised when the search results page could not be downloaded."""


def fetch_html(url: str) -> str:
    """
    Download the HTML content at `url` and return it as a string.

    mdcomputers.in sits behind Cloudflare's bot-protection, which blocks a
    plain `requests.get()` with an HTTP 403 before the request even reaches
    the site's own server. We first try the plain, simple request (fast,
    no extra dependency needed for sites that don't block us); only if
    that comes back 403 do we retry once with `cloudscraper`, a
    requests-compatible library that solves Cloudflare's basic JS
    challenge itself - no headless browser (Selenium/Playwright) involved.

    Raises ScraperError with a human-readable message if neither attempt
    succeeds: no internet, timeout, or a non-200 HTTP response.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.exceptions.Timeout as exc:
        raise ScraperError(f"Request timed out after {REQUEST_TIMEOUT_SECONDS}s: {url}") from exc
    except requests.exceptions.ConnectionError as exc:
        raise ScraperError(
            "Could not connect to the website. Check your internet connection."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ScraperError(f"Unexpected network error: {exc}") from exc

    if response.status_code == 403:
        return _fetch_html_via_cloudscraper(url)
    if response.status_code != 200:
        raise ScraperError(f"Server returned HTTP {response.status_code} for {url}")

    return response.text


def _fetch_html_via_cloudscraper(url: str) -> str:
    """Retry the request through cloudscraper after a plain 403, and raise a clear error if that also fails."""
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.exceptions.RequestException as exc:
        raise ScraperError(
            "Server returned 403 Forbidden, and the cloudscraper fallback also "
            f"failed ({exc}). Use --input-file with a saved HTML page instead "
            "(see sample_data/sample_search_results.html)."
        ) from exc

    if response.status_code != 200:
        raise ScraperError(
            f"Server returned 403 Forbidden, and the cloudscraper fallback got "
            f"HTTP {response.status_code} instead of 200. Cloudflare's "
            "protection may have been tightened since this was last tested - "
            "use --input-file with a saved HTML page instead "
            "(see sample_data/sample_search_results.html)."
        )

    return response.text

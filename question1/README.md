# Question 1 - mdcomputers.in Product Scraper

A small, modular Python CLI that searches [mdcomputers.in](https://mdcomputers.in)
for a given term and extracts the listed products (name, price, URL, image),
printing them to the terminal and saving them as JSON and CSV.

## Files

| File | Responsibility |
|---|---|
| `main.py` | CLI entry point - wires everything together |
| `scraper.py` | Downloads the search results HTML (the only file that touches the network) |
| `parser.py` | Turns HTML into `Product` objects (the only file that knows CSS selectors) |
| `models.py` | The `Product` dataclass - the shared "shape" of a product |
| `utils.py` | Small pure helpers: build URL, clean price text, save JSON/CSV, print table |
| `sample_data/sample_search_results.html` | Real, offline copy of a search results page (see "A note on Cloudflare" below) |
| `output/` | Where `products.json` / `products.csv` are written |

## How to run

```bash
pip install -r ../requirements.txt

python3 -m pip install -r ../requirements.txt

# Live mode - downloads the real search page
python3 main.py "external hard drive"

# Offline mode - parses a saved HTML file (see note below on why this exists)
python3 main.py --input-file sample_data/sample_search_results.html
```

Output is printed as a table and also saved to `output/products.json` and
`output/products.csv`.

## A note on Cloudflare

`mdcomputers.in` is protected by **Cloudflare bot-detection**. A plain
`requests.get()` - even with a realistic browser `User-Agent` header - is
often answered with an HTTP 403 "Attention Required! | Cloudflare" page
instead of real search results, because Cloudflare inserts a small
JavaScript/cookie challenge in front of the site that a plain HTTP client
can't solve.

`scraper.py` handles this automatically and in two stages:

1. It first tries a plain `requests.get()` (fast, no extra moving parts).
2. If - and only if - that comes back `403`, it retries once using
   [`cloudscraper`](https://github.com/VeNoMouS/cloudscraper), a
   requests-compatible library purpose-built to solve Cloudflare's basic
   JS challenge itself. This is **not** browser automation (no
   Selenium/Playwright, no real browser is launched) - it's still a plain
   HTTP client, just one that knows how to answer Cloudflare's challenge.

This means `python3 main.py "<search term>"` works against the live site
in the normal case. If Cloudflare ever tightens its protection further and
both attempts fail, `scraper.py` still reports a clear error rather than
crashing:

```
Error: Server returned 403 Forbidden, and the cloudscraper fallback also
failed (...). Use --input-file with a saved HTML page instead...
```

`--input-file` exists as a safety net for exactly that scenario, and to
make the parsing logic demonstrable offline / without a network call at
all. The file in `sample_data/` was captured from a real mdcomputers.in
"cpu cooler" search - the CSS classes and markup are unmodified.

## How the flow works

```
search term
   |
   v
build_search_url()          (utils.py)   -> https://mdcomputers.in/?route=product/search&search=...
   |
   v
fetch_html()                (scraper.py) -> raw HTML string
   |
   v
parse_products()            (parser.py)  -> list[Product]
   |
   v
print_products_table()      (utils.py)   -> printed to terminal
   |
   v
save_json() / save_csv()    (utils.py)   -> output/products.json, output/products.csv
```

## What gets extracted

Each product tile on the results page (`div.product-grid-item`) yields:

| Field | Source | Notes |
|---|---|---|
| `name` | `h3.product-entities-title a` text | |
| `url` | same `<a>` tag's `href` | |
| `price` | `span.price .ins .amount` (or plain `.amount` if no discount) | current selling price |
| `original_price` | `span.price .del .amount` | only present when the item is discounted |
| `image_url` | `img` tag `src` | |
| `brand` | - | not shown on the listing page for this site; kept as `None` rather than guessed |
| `availability` | - | same - only shown on the individual product page, not the search results grid |

**Design decision:** rather than inventing a brand/availability value from
the product title with regex guesswork, both fields are left as `None`
when the source page genuinely does not provide them. A `None` that is
honestly missing is more useful downstream than a wrong guess.

## Error handling

`scraper.py` raises a single custom `ScraperError` for all three cases the
assignment calls out, with a message describing what happened:

- **No internet** -> `requests.exceptions.ConnectionError` is caught
- **Timeout** -> `requests.exceptions.Timeout` (10s timeout) is caught
- **No search results** -> not an exception; `parse_products()` simply
  returns an empty list, and `main.py` prints "No products found" instead
  of crashing or writing empty output files

## Output format choices

- **JSON** - preserves types (e.g. `price` stays a number, not a string),
  and is the natural format if this output were ever consumed by another
  program or web frontend.
- **CSV** - opens directly in Excel/Google Sheets, which is the more likely
  format a non-technical reviewer would want to skim.

Both are generated on every run so neither use case is left out.





User
  │
  │ python3 main.py "external hard drive"
  ▼
main.py
  │
  ├── Parse CLI arguments
  │
  ▼
utils.py
  │
  ├── Build search URL
  │
  ▼
scraper.py
  │
  ├── requests.get()
  ├── headers
  ├── timeout
  ├── HTTP status handling
  └── cloudscraper fallback
  │
  ▼
HTML
  │
  ▼
parser.py
  │
  ├── BeautifulSoup
  ├── CSS selectors
  ├── Extract name
  ├── Extract URL
  └── Extract price
  │
  ▼
models.py
  │
  └── Product objects
  │
  ▼
main.py
  │
  ├── Print table
  ├── Save JSON
  └── Save CSV
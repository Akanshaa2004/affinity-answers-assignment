"""
CLI entry point.

Flow:
    user gives a search term (or --input-file for offline mode)
        -> download HTML (scraper.py)
        -> parse HTML into Product objects (parser.py)
        -> print a table (utils.py)
        -> save output/products.json and output/products.csv (utils.py)

Run:
    python3 main.py "external hard drive"
    python3 main.py --input-file sample_data/sample_search_results.html
"""

import argparse
import os
import sys

from parser import parse_products
from scraper import ScraperError, fetch_html
from utils import build_search_url, print_products_table, save_csv, save_json

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        description="Extract product listings from mdcomputers.in for a given search term."
    )
    arg_parser.add_argument(
        "search_term",
        nargs="+",
        help="Product search term, e.g. \"external hard drive\"",
    )
    arg_parser.add_argument(
        "--input-file",
        help=(
            "Parse a locally saved HTML file instead of downloading it. "
            "Useful when the live site is unreachable or blocking automated "
            "requests (see sample_data/sample_search_results.html)."
        ),
    )
    return arg_parser.parse_args()


def get_html(args: argparse.Namespace) -> str:
    """Return HTML either from a local file or by downloading it."""
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            return f.read()

    url = build_search_url(args.search_term)
    print(f"Fetching: {url}")
    return fetch_html(url)


def main() -> int:
    args = parse_args()

    if not args.search_term and not args.input_file:
        print("Please provide a search term, e.g.: python3 main.py \"external hard drive\"")
        return 1

    try:
        html = get_html(args)
    except ScraperError as exc:
        print(f"Error: {exc}")
        return 1
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input_file}")
        return 1

    products = parse_products(html)

    if not products:
        print("No products found for this search term.")
        return 0

    print_products_table(products)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "products.json")
    csv_path = os.path.join(OUTPUT_DIR, "products.csv")
    save_json(products, json_path)
    save_csv(products, csv_path)
    print(f"Saved {len(products)} product(s) to:")
    print(f"  {json_path}")
    print(f"  {csv_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

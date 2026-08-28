"""
Small, independent helper functions.

Nothing in this file knows about requests/BeautifulSoup or about the CLI.
Keeping it "pure" makes each function trivial to unit test on its own.
"""

import json
import re
from typing import List, Optional
from urllib.parse import urlencode

import pandas as pd

from models import Product

SEARCH_URL = "https://mdcomputers.in/"


def build_search_url(search_term: str) -> str:
    """
    Build the mdcomputers.in search URL for a given term.

    Example:
        build_search_url("external hard drive")
        -> "https://mdcomputers.in/?route=product/search&search=external+hard+drive"

    urlencode() takes care of turning spaces and special characters into
    a URL-safe form, so we never have to manually replace " " with "%20".
    """
    query = {"route": "product/search", "search": search_term}
    return f"{SEARCH_URL}?{urlencode(query)}"


def clean_price(raw_text: Optional[str]) -> Optional[float]:
    """
    Convert a price string like '₹23,390' or 'Rs. 1,299.00' into a float (23390.0).

    Returns None if no digits are found, instead of raising an exception -
    a missing/blank price should not crash the whole program.
    """
    if not raw_text:
        return None

    digits_and_dot = re.sub(r"[^\d.]", "", raw_text)
    if not digits_and_dot:
        return None

    try:
        return float(digits_and_dot)
    except ValueError:
        return None


def save_json(products: List[Product], file_path: str) -> None:
    """Save the list of products as a pretty-printed JSON array."""
    data = [product.to_dict() for product in products]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(products: List[Product], file_path: str) -> None:
    """Save the list of products as a CSV file with a header row, using pandas."""
    df = pd.DataFrame([product.to_dict() for product in products])
    df.to_csv(file_path, index=False)


def print_products_table(products: List[Product]) -> None:
    """Print a simple, readable table of products to the terminal."""
    if not products:
        print("No products to display.")
        return

    print(f"\nFound {len(products)} product(s):\n")
    for index, product in enumerate(products, start=1):
        price_text = f"Rs. {product.price:,.2f}" if product.price is not None else "N/A"
        print(f"{index}. {product.name}")
        print(f"   Price : {price_text}")
        print(f"   URL   : {product.url}")
        print()

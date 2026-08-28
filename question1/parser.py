"""
Turns raw HTML into a list of Product objects.

All BeautifulSoup / CSS-selector knowledge lives here. If mdcomputers.in
changes its HTML markup in the future, this is the only file that needs
to change - scraper.py, models.py and main.py are unaffected.
"""

from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from models import Product
from utils import clean_price

# Each product on the search results page sits inside a
# <div class="product-grid-item"> ... </div> block. This was confirmed
# by inspecting a real mdcomputers.in search results page (see
# sample_data/sample_search_results.html for an offline copy).
PRODUCT_TILE_SELECTOR = "div.product-grid-item"
TITLE_SELECTOR = "h3.product-entities-title a"
IMAGE_SELECTOR = "img"


def parse_products(html: str) -> List[Product]:
    """Parse a search results HTML page and return a list of Product objects."""
    soup = BeautifulSoup(html, "lxml")
    tiles = soup.select(PRODUCT_TILE_SELECTOR)

    products = []
    for tile in tiles:
        product = _parse_single_tile(tile)
        if product is not None:
            products.append(product)

    return products


def _parse_single_tile(tile: Tag) -> Optional[Product]:
    """Extract one Product from a single product tile. Returns None if unparsable."""
    title_tag = tile.select_one(TITLE_SELECTOR)
    if title_tag is None or not title_tag.get("href"):
        # Without a name and a URL the row is useless, so skip it instead
        # of adding a half-empty entry.
        return None

    name = title_tag.get_text(strip=True)
    url = title_tag["href"]

    image_tag = tile.select_one(IMAGE_SELECTOR)
    image_url = image_tag["src"] if image_tag and image_tag.get("src") else None

    price, original_price = _extract_prices(tile)

    return Product(
        name=name,
        url=url,
        price=price,
        original_price=original_price,
        image_url=image_url,
        # Brand and availability are not shown on the search results page
        # for this site - only on the individual product page - so they
        # are left as None rather than guessed.
        brand=None,
        availability=None,
    )


def _extract_prices(tile: Tag):
    """
    Return (current_price, original_price) as floats.

    A product on sale is marked up as:
        <span class="price">
          <span class="del"><span class="amount">OLD PRICE</span></span>
          <span class="ins"><span class="amount">NEW PRICE</span></span>
        </span>
    A product with no discount only has the "ins" (or a bare) amount.
    """
    price_tag = tile.select_one("span.price")
    if price_tag is None:
        return None, None

    sale_price_tag = price_tag.select_one("span.ins .amount")
    original_price_tag = price_tag.select_one("span.del .amount")

    if sale_price_tag is not None:
        current = clean_price(sale_price_tag.get_text())
        original = clean_price(original_price_tag.get_text()) if original_price_tag else None
        return current, original

    # No sale - just a plain amount element.
    plain_amount_tag = price_tag.select_one(".amount")
    current = clean_price(plain_amount_tag.get_text()) if plain_amount_tag else None
    return current, None

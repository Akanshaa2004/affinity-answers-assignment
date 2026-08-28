"""
Data model for a single scraped product.

Using a single dataclass keeps the "shape" of a product in one place.
Every other file (parser, utils, main) imports this class instead of
passing around loose dictionaries, so a typo in a field name is caught
by the IDE / type checker instead of silently producing bad output.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Product:
    """One product row extracted from the search results page."""

    name: str
    url: str
    price: Optional[float] = None          # current selling price (None if not shown)
    original_price: Optional[float] = None  # MRP before discount, if the item is on sale
    image_url: Optional[str] = None
    brand: Optional[str] = None            # not shown on the listing page, kept for completeness
    availability: Optional[str] = None     # not shown on the listing page, kept for completeness

    def to_dict(self) -> dict:
        """Convert to a plain dict, used by the JSON/CSV writers in utils.py."""
        return asdict(self)

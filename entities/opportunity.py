from dataclasses import dataclass

from entities.product import Product


@dataclass
class Opportunity:
    product: Product
    score: int
    should_notify: bool
    reasons: list[str]

    opportunity_type: str = "normal"
    confidence: str = "baixa"
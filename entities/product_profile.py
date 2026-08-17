from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProductProfile:
    product_id: str

    brand: str | None
    model: str | None
    memory_gb: int | None
    variant: str | None

    broad_key: str | None
    tier_key: str | None
    strict_key: str | None

    category: str | None = None

    attributes: dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )
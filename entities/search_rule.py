from dataclasses import dataclass


@dataclass(frozen=True)
class SearchRule:
    required_terms: tuple[str, ...] = ()
    excluded_terms: tuple[str, ...] = ()

    minimum_price: float | None = None
    maximum_price: float | None = None

    require_official_store: bool = False
    require_full: bool = False
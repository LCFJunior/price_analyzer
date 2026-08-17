from typing import Protocol

from entities.product import Product


class MarketplaceCollector(Protocol):
    """
    Contrato comum para todos os coletores.

    Qualquer collector de marketplace deve possuir um método search()
    que recebe uma pesquisa e devolve uma lista normalizada de Product.
    """

    def search(
        self,
        query: str,
    ) -> list[Product]:
        ...
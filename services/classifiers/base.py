from typing import Protocol

from entities.product import Product
from entities.product_profile import ProductProfile


class ProductCategoryClassifier(Protocol):
    """
    Contrato comum para classificadores de categorias.

    Cada classificador deve informar se consegue reconhecer
    determinado produto e, em caso positivo, gerar um
    ProductProfile normalizado.
    """

    def can_classify(
        self,
        product: Product,
    ) -> bool:
        ...

    def classify(
        self,
        product: Product,
    ) -> ProductProfile:
        ...
from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)


class CandidateSelector:
    """
    Seleciona quais produtos válidos serão analisados
    pelo OpportunityEngine.

    Esta camada NÃO decide se um preço é bom.

    Ela apenas verifica se existe informação mínima
    para que os motores de promoção/bug possam analisar
    o produto.

    Com isso eliminamos regras rígidas como:

        RTX 5070 abaixo de R$ 5.500
        Ryzen 5700X abaixo de R$ 1.100
        SSD abaixo de R$ 450

    O preço passa a ser julgado dinamicamente por:

    - histórico;
    - produtos equivalentes;
    - identidade;
    - desconto anunciado;
    - sinais de confiança.
    """

    def select(
        self,
        *,
        products: list[Product],
        profiles: dict[
            str,
            ProductProfile,
        ],
    ) -> list[Product]:
        candidates: list[Product] = []

        for product in products:
            if not self._has_valid_price(
                product
            ):
                continue

            profile = profiles.get(
                product.id
            )

            if profile is None:
                continue

            # Precisamos pelo menos de um grupo geral.
            #
            # Produtos sem broad_key ainda podem ser
            # armazenados para diagnóstico, mas não são
            # bons candidatos para comparação automática.
            if not profile.broad_key:
                continue

            candidates.append(
                product
            )

        return candidates

    @staticmethod
    def _has_valid_price(
        product: Product,
    ) -> bool:
        return (
            product.price is not None
            and product.price > 0
        )
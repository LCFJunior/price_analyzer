from dataclasses import dataclass
import unicodedata

from entities.product import Product


@dataclass(frozen=True)
class ListingValidationResult:
    is_valid: bool
    reasons: tuple[str, ...]


class ListingValidator:
    """
    Valida se o anúncio aparenta conter o produto principal.

    Esta primeira versão usa o título. Futuramente, candidatos
    suspeitos também poderão ser validados pela descrição e pelas
    características da página do produto.
    """

    INVALID_PHRASES = (
        "caixa vazia",
        "caixa sem produto",
        "somente caixa",
        "apenas caixa",
        "só a caixa",
        "so a caixa",
        "embalagem vazia",
        "somente embalagem",
        "apenas embalagem",
        "manual",
        "adesivo",
        "blister",
        "sem processador",
        "não acompanha processador",
        "nao acompanha processador",
        "sem placa de vídeo",
        "sem placa de video",
        "não acompanha placa",
        "nao acompanha placa",
        "para retirada de peças",
        "retirada de peças",
        "com defeito",
        "não funciona",
        "nao funciona",
        "sucata",
        "peças",
        "pecas",
    )

    def validate(
        self,
        product: Product,
    ) -> ListingValidationResult:
        normalized_title = self._normalize(
            product.title
        )

        reasons: list[str] = []

        for phrase in self.INVALID_PHRASES:
            normalized_phrase = self._normalize(
                phrase
            )

            if normalized_phrase in normalized_title:
                reasons.append(
                    f"Termo inválido encontrado: {phrase}"
                )

        return ListingValidationResult(
            is_valid=not reasons,
            reasons=tuple(reasons),
        )

    def filter_valid(
        self,
        products: list[Product],
    ) -> tuple[
        list[Product],
        dict[str, ListingValidationResult],
    ]:
        valid_products: list[Product] = []
        rejected_products: dict[
            str,
            ListingValidationResult,
        ] = {}

        for product in products:
            result = self.validate(product)

            if result.is_valid:
                valid_products.append(product)
                continue

            rejected_products[product.id] = result

        return valid_products, rejected_products

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:
        normalized = unicodedata.normalize(
            "NFKD",
            value.lower().strip(),
        )

        normalized = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )

        return " ".join(
            normalized.split()
        )
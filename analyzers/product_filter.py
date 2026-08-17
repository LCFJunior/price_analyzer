import unicodedata

from entities.product import Product
from entities.search_rule import SearchRule


class ProductFilter:
    """
    Aplica regras objetivas antes de o produto chegar ao PriceAnalyzer.

    Exemplos:
    - exigir palavras no título;
    - excluir versões diferentes;
    - aplicar preço mínimo e máximo;
    - exigir loja oficial ou entrega FULL.
    """

    def filter(
        self,
        products: list[Product],
        rule: SearchRule,
    ) -> list[Product]:
        return [
            product
            for product in products
            if self.matches(product, rule)
        ]

    def matches(
        self,
        product: Product,
        rule: SearchRule,
    ) -> bool:
        normalized_title = self._normalize(product.title)

        if not self._contains_required_terms(
            normalized_title,
            rule.required_terms,
        ):
            return False

        if self._contains_excluded_terms(
            normalized_title,
            rule.excluded_terms,
        ):
            return False

        if not self._matches_price_range(product, rule):
            return False

        if rule.require_official_store and not product.official_store:
            return False

        if rule.require_full and not product.full:
            return False

        return True

    def explain_rejection(
        self,
        product: Product,
        rule: SearchRule,
    ) -> list[str]:
        reasons: list[str] = []
        normalized_title = self._normalize(product.title)

        missing_terms = [
            term
            for term in rule.required_terms
            if self._normalize(term) not in normalized_title
        ]

        if missing_terms:
            reasons.append(
                "Termos obrigatórios ausentes: "
                + ", ".join(missing_terms)
            )

        excluded_terms_found = [
            term
            for term in rule.excluded_terms
            if self._normalize(term) in normalized_title
        ]

        if excluded_terms_found:
            reasons.append(
                "Termos excluídos encontrados: "
                + ", ".join(excluded_terms_found)
            )

        if product.price is None:
            reasons.append("Produto sem preço válido")
        else:
            if (
                rule.minimum_price is not None
                and product.price < rule.minimum_price
            ):
                reasons.append(
                    f"Preço abaixo do mínimo: R$ {product.price:.2f}"
                )

            if (
                rule.maximum_price is not None
                and product.price > rule.maximum_price
            ):
                reasons.append(
                    f"Preço acima do máximo: R$ {product.price:.2f}"
                )

        if rule.require_official_store and not product.official_store:
            reasons.append("Não é loja oficial")

        if rule.require_full and not product.full:
            reasons.append("Não possui envio FULL")

        return reasons

    @staticmethod
    def _contains_required_terms(
        normalized_title: str,
        required_terms: tuple[str, ...],
    ) -> bool:
        return all(
            ProductFilter._normalize(term) in normalized_title
            for term in required_terms
        )

    @staticmethod
    def _contains_excluded_terms(
        normalized_title: str,
        excluded_terms: tuple[str, ...],
    ) -> bool:
        return any(
            ProductFilter._normalize(term) in normalized_title
            for term in excluded_terms
        )

    @staticmethod
    def _matches_price_range(
        product: Product,
        rule: SearchRule,
    ) -> bool:
        if product.price is None or product.price <= 0:
            return False

        if (
            rule.minimum_price is not None
            and product.price < rule.minimum_price
        ):
            return False

        if (
            rule.maximum_price is not None
            and product.price > rule.maximum_price
        ):
            return False

        return True

    @staticmethod
    def _normalize(value: str) -> str:
        value = value.lower().strip()

        normalized = unicodedata.normalize("NFKD", value)

        normalized = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )

        return " ".join(normalized.split())
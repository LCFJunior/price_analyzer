import re
import unicodedata

from playwright.sync_api import Locator, Page

from entities.product import Product
from services.product_factory import ProductFactory


class MercadoLivreCollector:
    CARD_SELECTOR = "li.ui-search-layout__item"

    INTERNATIONAL_TERMS = (
        "internacional",
        "compra internacional",
        "produto internacional",
        "envio internacional",
    )

    def __init__(
        self,
        page: Page,
    ):
        self.page = page

    def search(
        self,
        query: str,
    ) -> list[Product]:
        url = self._build_search_url(
            query
        )

        print(
            f"\nAbrindo:\n{url}\n"
        )

        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60_000,
        )

        self.page.wait_for_selector(
            self.CARD_SELECTOR,
            timeout=30_000,
        )

        cards = self.page.locator(
            self.CARD_SELECTOR
        )

        total = cards.count()

        print(
            f"{total} produtos encontrados.\n"
        )

        products: list[Product] = []

        international_count = 0

        for index in range(total):
            card = cards.nth(index)

            try:
                product = self._parse_card(
                    card
                )

                if (
                    product.title
                    and product.link
                    and product.price is not None
                ):
                    products.append(
                        product
                    )

                    if product.international:
                        international_count += 1

            except Exception as error:
                print(
                    "Falha ao processar "
                    f"o card {index + 1}: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

        if international_count > 0:
            print(
                "Anúncios internacionais "
                "identificados: "
                f"{international_count}\n"
            )

        return products

    def _parse_card(
        self,
        card: Locator,
    ) -> Product:
        title = self._safe_text(
            card,
            ".poly-component__title",
        )

        link = self._safe_attribute(
            card,
            ".poly-component__title",
            "href",
        )

        image_url = self._safe_attribute(
            card,
            ".poly-component__picture",
            "src",
        )

        if not image_url:
            image_url = (
                self._safe_attribute(
                    card,
                    "img[data-testid='picture']",
                    "src",
                )
            )

        current_price = self._safe_text(
            card,
            ".poly-price__amount",
        )

        old_price = self._safe_text(
            card,
            ".andes-money-amount--previous",
        )

        discount = self._safe_text(
            card,
            ".poly-price__discount-polylabel",
        )

        installments = self._safe_text(
            card,
            ".poly-price__installments",
        )

        seller = self._safe_text(
            card,
            ".poly-component__seller",
        )

        shipping = self._safe_text(
            card,
            ".poly-component__shipping-v2",
        )

        official_store = (
            card.locator(
                ".poly-component__seller "
                "svg[aria-label='Loja oficial']"
            ).count()
            > 0
        )

        full = (
            card.locator(
                "svg[aria-label='Enviado pelo FULL']"
            ).count()
            > 0
        )

        international = (
            self._is_international(
                card
            )
        )

        product_id = (
            self._extract_product_id(
                link
            )
        )

        product = ProductFactory.create(
            marketplace="Mercado Livre",
            title=title,
            price=current_price,
            old_price=old_price,
            discount=discount,
            installments=installments,
            seller=seller,
            official_store=official_store,
            full=full,
            shipping=shipping,
            link=link or "",
            image_url=image_url,
            product_id=product_id,
        )

        # Não precisamos alterar ProductFactory agora.
        product.international = (
            international
        )

        return product

    def _is_international(
        self,
        card: Locator,
    ) -> bool:
        """
        Detecta se o próprio card do produto contém
        indicação de compra internacional.

        Usamos somente o conteúdo daquele card,
        nunca o texto da página inteira.
        """

        try:
            card_text = card.inner_text(
                timeout=2_000
            )
        except Exception:
            card_text = ""

        normalized_text = (
            self._normalize_text(
                card_text
            )
        )

        for term in (
            self.INTERNATIONAL_TERMS
        ):
            normalized_term = (
                self._normalize_text(
                    term
                )
            )

            if (
                normalized_term
                in normalized_text
            ):
                return True

        # ------------------------------------------------------
        # Tentativas adicionais usando elementos com atributos
        # acessíveis.
        # ------------------------------------------------------

        possible_selectors = (
            "[aria-label*='Internacional']",
            "[aria-label*='internacional']",
            "[title*='Internacional']",
            "[title*='internacional']",
        )

        for selector in possible_selectors:
            try:
                if (
                    card.locator(
                        selector
                    ).count()
                    > 0
                ):
                    return True

            except Exception:
                continue

        return False

    @staticmethod
    def _normalize_text(
        value: str | None,
    ) -> str:
        if not value:
            return ""

        normalized = (
            unicodedata.normalize(
                "NFKD",
                value.lower(),
            )
        )

        normalized = "".join(
            character
            for character in normalized
            if not unicodedata.combining(
                character
            )
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()

    @staticmethod
    def _safe_text(
        container: Locator,
        selector: str,
    ) -> str | None:
        locator = container.locator(
            selector
        )

        if locator.count() == 0:
            return None

        try:
            return (
                locator.first.inner_text(
                    timeout=2_000
                )
            )

        except Exception:
            return None

    @staticmethod
    def _safe_attribute(
        container: Locator,
        selector: str,
        attribute: str,
    ) -> str | None:
        locator = container.locator(
            selector
        )

        if locator.count() == 0:
            return None

        try:
            return (
                locator.first.get_attribute(
                    attribute,
                    timeout=2_000,
                )
            )

        except Exception:
            return None

    @staticmethod
    def _extract_product_id(
        link: str | None,
    ) -> str:
        if not link:
            return ""

        matches = re.findall(
            r"MLB\d+",
            link,
        )

        if not matches:
            return ""

        return matches[-1]

    @staticmethod
    def _build_search_url(
        query: str,
    ) -> str:
        normalized_query = (
            query.strip()
            .replace(
                " ",
                "-",
            )
        )

        return (
            "https://lista.mercadolivre.com.br/"
            f"{normalized_query}"
        )
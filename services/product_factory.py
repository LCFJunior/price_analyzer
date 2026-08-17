from entities.product import Product
from utils.money import Money
from utils.text import Text


class ProductFactory:
    @staticmethod
    def create(
        *,
        marketplace: str,
        title: str | None,
        price: str | None,
        old_price: str | None,
        discount: str | None,
        installments: str | None,
        seller: str | None,
        official_store: bool,
        full: bool,
        shipping: str | None,
        link: str,
        image_url: str | None = None,
        product_id: str = "",
    ) -> Product:
        return Product(
            id=product_id,
            marketplace=marketplace,
            title=Text.clean(title) or "",
            price=Money.parse(price),
            old_price=Money.parse(old_price),
            discount=Text.clean(discount),
            installments=Text.clean(installments),
            seller=Text.clean(seller),
            official_store=official_store,
            full=full,
            shipping=Text.clean(shipping),
            link=link,
            image_url=image_url,
        )
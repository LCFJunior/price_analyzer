from dataclasses import dataclass


@dataclass
class Product:
    id: str

    marketplace: str

    title: str

    price: float | None

    old_price: float | None

    discount: str | None

    installments: str | None

    seller: str | None

    official_store: bool

    full: bool

    shipping: str | None

    link: str

    image_url: str | None

    # ==========================================================
    # ORIGEM DO ANÚNCIO
    # ==========================================================

    # True quando o marketplace indica que o produto
    # é uma compra internacional/importada.
    international: bool = False
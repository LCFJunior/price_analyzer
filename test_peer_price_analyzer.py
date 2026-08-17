from analyzers.peer_price_analyzer import (
    PeerPriceAnalyzer,
)
from entities.product import Product
from services.product_classifier import (
    ProductClassifier,
)


def create_product(
    product_id: str,
    title: str,
    price: float,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=None,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=True,
        full=True,
        shipping="Frete grátis",
        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),
    )


products = [
    create_product(
        "MLB001",
        "RTX 5070 MSI Ventus 12GB",
        5000.0,
    ),
    create_product(
        "MLB002",
        "RTX 5070 MSI Shadow 12GB",
        5100.0,
    ),
    create_product(
        "MLB003",
        "RTX 5070 MSI Gaming 12GB",
        4950.0,
    ),
    create_product(
        "MLB004",
        "RTX 5070 Asus Dual 12GB",
        5200.0,
    ),
    create_product(
        "MLB005",
        "RTX 5070 Gigabyte 12GB",
        4900.0,
    ),
    create_product(
        "MLB_BUG",
        "RTX 5070 MSI Ventus 12GB",
        1999.0,
    ),
]

classifier = ProductClassifier()

profiles = classifier.classify_many(
    products
)

peer_analyzer = PeerPriceAnalyzer(
    minimum_strict_peers=2,
    minimum_broad_peers=4,
)

bug_product = products[-1]

statistics = (
    peer_analyzer.get_product_statistics(
        product=bug_product,
        products=products,
        profiles=profiles,
    )
)

drop = (
    peer_analyzer.calculate_drop_percentage(
        current_price=bug_product.price,
        statistics=statistics,
    )
)

print(
    f"Produto: {bug_product.title}"
)
print(
    f"Preço atual: {bug_product.price}"
)
print(
    f"Escopo utilizado: "
    f"{statistics.comparison_scope if statistics else None}"
)
print(
    f"Chave: "
    f"{statistics.comparison_key if statistics else None}"
)
print(
    f"Estatísticas: {statistics}"
)
print(
    "Queda contra equivalentes: "
    f"{drop}%"
)
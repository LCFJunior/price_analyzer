from analyzers.product_filter import ProductFilter
from entities.product import Product
from entities.search_rule import SearchRule


def create_product(
    *,
    title: str,
    price: float,
    official_store: bool = True,
    full: bool = True,
) -> Product:
    return Product(
        id="MLB123",
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=None,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=official_store,
        full=full,
        shipping="Frete grátis",
        link="https://teste",
    )


rule = SearchRule(
    required_terms=("rtx", "5070"),
    excluded_terms=("5070 ti", "5070ti"),
    maximum_price=5500.0,
)

products = [
    create_product(
        title="Placa de vídeo RTX 5070 12GB",
        price=4999.0,
    ),
    create_product(
        title="Placa de vídeo RTX 5070 Ti 16GB",
        price=5200.0,
    ),
    create_product(
        title="Placa de vídeo RTX 5070 12GB",
        price=6200.0,
    ),
    create_product(
        title="Placa de vídeo RX 9070 XT",
        price=4999.0,
    ),
]

product_filter = ProductFilter()
filtered_products = product_filter.filter(products, rule)

print(f"Produtos recebidos: {len(products)}")
print(f"Produtos aprovados: {len(filtered_products)}")

for product in filtered_products:
    print(product)
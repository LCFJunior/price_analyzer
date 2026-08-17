from entities.product import Product
from services.listing_validator import (
    ListingValidator,
)


def create_product(
    product_id: str,
    title: str,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=100.0,
        old_price=None,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=False,
        full=False,
        shipping=None,
        link=f"https://teste.com/{product_id}",
        image_url=None,
    )


products = [
    create_product(
        "VALID_001",
        "Processador AMD Ryzen 7 5700X OEM Sem Cooler",
    ),
    create_product(
        "INVALID_001",
        "Caixa Vazia AMD CPU Ryzen 7 5700X "
        "Adesivo Blister Manual",
    ),
    create_product(
        "INVALID_002",
        "Somente Caixa RTX 5070 ASUS",
    ),
    create_product(
        "INVALID_003",
        "Ryzen 7 5700X com defeito para peças",
    ),
]

validator = ListingValidator()

valid_products, rejected_products = (
    validator.filter_valid(products)
)

print("=" * 80)
print("PRODUTOS VÁLIDOS")

for product in valid_products:
    print(f"- {product.title}")

print("=" * 80)
print("PRODUTOS REJEITADOS")

for product_id, result in rejected_products.items():
    print(f"ID: {product_id}")

    for reason in result.reasons:
        print(f"- {reason}")
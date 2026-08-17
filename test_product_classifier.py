from entities.product import Product
from services.product_classifier import (
    ProductClassifier,
)


def create_product(
    product_id: str,
    title: str,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=5000.0,
        old_price=None,
        discount=None,
        installments=None,
        seller=None,
        official_store=False,
        full=False,
        shipping=None,
        link="https://teste.com",
    )


products = [
    create_product(
        "MLB001",
        (
            "Placa De Vídeo Msi Geforce "
            "RTX 5070 Ventus 3X OC "
            "12GB GDDR7"
        ),
    ),
    create_product(
        "MLB002",
        (
            "Placa De Vídeo Asus "
            "RTX 5070 Ti Prime OC "
            "16GB GDDR7"
        ),
    ),
    create_product(
        "MLB003",
        (
            "Placa De Vídeo Gigabyte "
            "RTX5070 Windforce 12 GB"
        ),
    ),
    create_product(
        "MLB004",
        (
            "Placa de vídeo Gigabyte "
            "Geforce RTX 5070 Gaming "
            "OC 12G"
        ),
    ),
    create_product(
        "MLB005",
        (
            "Placa de vídeo sem modelo "
            "identificado"
        ),
    ),
]

classifier = ProductClassifier()

for product in products:
    profile = classifier.classify(
        product
    )

    print("=" * 80)
    print(
        f"Título: {product.title}"
    )
    print(
        f"Marca: {profile.brand}"
    )
    print(
        f"Modelo: {profile.model}"
    )
    print(
        f"Memória: {profile.memory_gb}"
    )
    print(
        f"Variante: {profile.variant}"
    )
    print(
        f"Chave geral: "
        f"{profile.broad_key}"
    )
    print(
        f"Chave específica: "
        f"{profile.strict_key}"
    )
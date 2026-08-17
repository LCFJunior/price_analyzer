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
        price=1000.0,
        old_price=None,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=False,
        full=False,
        shipping=None,
        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),
        image_url=None,
    )


def main() -> None:
    products = [
        # GPU tradicional
        create_product(
            "GPU001",
            (
                "Placa de Vídeo ASUS "
                "GeForce RTX 5070 "
                "Prime OC 12GB GDDR7"
            ),
        ),

        # GPU AMD
        create_product(
            "GPU002",
            (
                "Placa de Vídeo Sapphire "
                "Radeon RX 9070 XT 16GB"
            ),
        ),

        # Ryzen tradicional
        create_product(
            "CPU001",
            (
                "Processador AMD "
                "Ryzen 7 5700X AM4"
            ),
        ),

        # Ryzen X3D
        create_product(
            "CPU002",
            (
                "Processador AMD "
                "Ryzen 7 5700X3D AM4"
            ),
        ),

        # Intel
        create_product(
            "CPU003",
            (
                "Processador Intel Core "
                "i9-11900KF LGA1200"
            ),
        ),

        # Caso real encontrado no ML:
        # modelo concatenado ao código AMD
        create_product(
            "CPU004",
            (
                "Processador Amd Ryzen 7 "
                "5700x100-100000926wof "
                "8 Núcleos Top1"
            ),
        ),

        # Caso real encontrado no ML:
        # palavras extras entre a família
        # e o modelo
        create_product(
            "CPU005",
            (
                "Processadores De Cpu "
                "Amd Ryzen 7 Série "
                "R7 5700x"
            ),
        ),

        # Outro formato possível
        create_product(
            "CPU006",
            (
                "Processador AMD R7 "
                "5700X AM4 8 Core"
            ),
        ),

        # Genérico proposital
        create_product(
            "GENERIC001",
            (
                "Mouse Gamer Sem Fio "
                "Modelo Teste"
            ),
        ),
    ]

    classifier = (
        ProductClassifier()
    )

    for product in products:
        profile = (
            classifier.classify(
                product
            )
        )

        print("=" * 80)

        print(
            f"Título: "
            f"{product.title}"
        )

        print(
            f"Marca: "
            f"{profile.brand}"
        )

        print(
            f"Modelo: "
            f"{profile.model}"
        )

        print(
            f"Memória: "
            f"{profile.memory_gb}"
        )

        print(
            f"Variante: "
            f"{profile.variant}"
        )

        print(
            "Chave geral: "
            f"{profile.broad_key}"
        )

        print(
            "Chave específica: "
            f"{profile.strict_key}"
        )


if __name__ == "__main__":
    main()
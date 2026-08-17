from analyzers.peer_price_analyzer import (
    PeerPriceAnalyzer,
)

from entities.product import Product

from entities.product_profile import (
    ProductProfile,
)


def create_product(
    *,
    product_id: str,
    price: float,
    international: bool,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=(
            "SSD Kingston NV3 "
            "1TB NVMe"
        ),
        price=price,
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
        international=(
            international
        ),
    )


def create_profile(
    product_id: str,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,
        brand="KINGSTON",
        model="NV3",
        memory_gb=None,
        variant=None,

        broad_key=(
            "ssd_nvme_1tb"
        ),

        strict_key=(
            "kingston_nv3_1tb_nvme"
        ),

        category="ssd",

        attributes={
            "capacity_gb": 1000,
            "capacity_label": "1tb",
            "interface": "nvme",
            "identity_confidence": "alta",
        },
    )


def main() -> None:
    products = [
        # ======================================================
        # NACIONAIS
        # ======================================================

        create_product(
            product_id="BR001",
            price=399.0,
            international=False,
        ),

        create_product(
            product_id="BR002",
            price=379.0,
            international=False,
        ),

        create_product(
            product_id="BR003",
            price=409.0,
            international=False,
        ),

        create_product(
            product_id="BR004",
            price=389.0,
            international=False,
        ),

        create_product(
            product_id="BR005",
            price=419.0,
            international=False,
        ),

        # ======================================================
        # INTERNACIONAIS
        # ======================================================

        create_product(
            product_id="INT001",
            price=175.0,
            international=True,
        ),

        create_product(
            product_id="INT002",
            price=185.0,
            international=True,
        ),

        create_product(
            product_id="INT003",
            price=169.0,
            international=True,
        ),

        create_product(
            product_id="INT004",
            price=199.0,
            international=True,
        ),

        create_product(
            product_id="INT005",
            price=179.0,
            international=True,
        ),
    ]

    profiles = {
        product.id: (
            create_profile(
                product.id
            )
        )
        for product in products
    }

    analyzer = PeerPriceAnalyzer(
        minimum_strict_peers=4,
        minimum_broad_peers=4,
    )

    # ==========================================================
    # PRODUTO NACIONAL
    # ==========================================================

    national_product = (
        products[0]
    )

    national_statistics = (
        analyzer.get_product_statistics(
            product=national_product,
            products=products,
            profiles=profiles,
        )
    )

    # ==========================================================
    # PRODUTO INTERNACIONAL
    # ==========================================================

    international_product = (
        products[5]
    )

    international_statistics = (
        analyzer.get_product_statistics(
            product=international_product,
            products=products,
            profiles=profiles,
        )
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "REFERÊNCIA NACIONAL"
    )

    print(
        "=" * 80
    )

    if national_statistics:
        print(
            "Escopo: "
            f"{national_statistics.comparison_scope}"
        )

        print(
            "Observações: "
            f"{national_statistics.observations}"
        )

        print(
            "Menor: "
            f"R$ {national_statistics.minimum_price:.2f}"
        )

        print(
            "Maior: "
            f"R$ {national_statistics.maximum_price:.2f}"
        )

        print(
            "Média: "
            f"R$ {national_statistics.average_price:.2f}"
        )

        print(
            "Mediana: "
            f"R$ {national_statistics.median_price:.2f}"
        )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "REFERÊNCIA INTERNACIONAL"
    )

    print(
        "=" * 80
    )

    if international_statistics:
        print(
            "Escopo: "
            f"{international_statistics.comparison_scope}"
        )

        print(
            "Observações: "
            f"{international_statistics.observations}"
        )

        print(
            "Menor: "
            f"R$ {international_statistics.minimum_price:.2f}"
        )

        print(
            "Maior: "
            f"R$ {international_statistics.maximum_price:.2f}"
        )

        print(
            "Média: "
            f"R$ {international_statistics.average_price:.2f}"
        )

        print(
            "Mediana: "
            f"R$ {international_statistics.median_price:.2f}"
        )

    # ==========================================================
    # VERIFICAÇÕES AUTOMÁTICAS
    # ==========================================================

    print(
        "\n"
        + "=" * 80
    )

    print(
        "VERIFICAÇÕES AUTOMÁTICAS"
    )

    print(
        "=" * 80
    )

    assert (
        national_statistics
        is not None
    )

    assert (
        international_statistics
        is not None
    )

    assert (
        national_statistics
        .comparison_scope
        == "mesma_marca_nacional"
    )

    assert (
        international_statistics
        .comparison_scope
        == "mesma_marca_internacional"
    )

    # Internacional barato não pode
    # derrubar a mediana nacional.
    assert (
        national_statistics
        .median_price
        > 350
    )

    # Nacional caro não pode elevar
    # a mediana internacional.
    assert (
        international_statistics
        .median_price
        < 220
    )

    assert (
        national_statistics
        .minimum_price
        >= 379
    )

    assert (
        international_statistics
        .maximum_price
        <= 199
    )

    print(
        "✓ Nacional comparou apenas "
        "com nacionais"
    )

    print(
        "✓ Internacional comparou apenas "
        "com internacionais"
    )

    print(
        "✓ Internacional barato não "
        "contaminou a referência nacional"
    )

    print(
        "✓ Nacional caro não contaminou "
        "a referência internacional"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
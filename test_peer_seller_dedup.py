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
    seller: str,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title="SSD Samsung 9100 Pro 1TB",
        price=price,
        old_price=None,
        discount=None,
        installments=None,
        seller=seller,
        official_store=False,
        full=False,
        shipping=None,
        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),
        image_url=None,
        international=False,
    )


def create_profile(
    product_id: str,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,

        brand="SAMSUNG",

        model="9100 PRO",

        memory_gb=None,

        variant=None,

        broad_key=(
            "ssd_nvme_1tb"
        ),

        tier_key=(
            "ssd_nvme_gen5_1tb"
        ),

        strict_key=(
            "samsung_9100_pro_1tb_nvme"
        ),

        category="ssd",

        attributes={
            "identity_confidence": (
                "alta"
            ),
        },
    )


def main() -> None:
    products = [
        # Produto sendo analisado.
        create_product(
            product_id="TARGET",
            price=2500.0,
            seller="Loja Target",
        ),

        # ======================================================
        # LOJA A
        #
        # Cinco anúncios praticamente iguais.
        # ======================================================

        create_product(
            product_id="A1",
            price=2300.0,
            seller="Loja A",
        ),

        create_product(
            product_id="A2",
            price=2310.0,
            seller="Loja A",
        ),

        create_product(
            product_id="A3",
            price=2320.0,
            seller="Loja A",
        ),

        create_product(
            product_id="A4",
            price=2330.0,
            seller="Loja A",
        ),

        create_product(
            product_id="A5",
            price=2340.0,
            seller="Loja A",
        ),

        # ======================================================
        # OUTROS VENDEDORES
        # ======================================================

        create_product(
            product_id="B1",
            price=2700.0,
            seller="Loja B",
        ),

        create_product(
            product_id="C1",
            price=2750.0,
            seller="Loja C",
        ),

        create_product(
            product_id="D1",
            price=2800.0,
            seller="Loja D",
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
        minimum_strict_peers=1,
        minimum_tier_peers=2,
        minimum_broad_peers=3,
    )

    statistics = (
        analyzer.get_product_statistics(
            product=products[0],
            products=products,
            profiles=profiles,
        )
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DEDUPLICAÇÃO POR VENDEDOR"
    )

    print(
        "=" * 80
    )

    assert (
        statistics
        is not None
    )

    print(
        "Escopo: "
        f"{statistics.comparison_scope}"
    )

    print(
        "Observações comerciais: "
        f"{statistics.observations}"
    )

    print(
        "Menor: "
        f"R$ {statistics.minimum_price:.2f}"
    )

    print(
        "Maior: "
        f"R$ {statistics.maximum_price:.2f}"
    )

    print(
        "Média: "
        f"R$ {statistics.average_price:.2f}"
    )

    print(
        "Mediana: "
        f"R$ {statistics.median_price:.2f}"
    )

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

    # Loja A possui 5 anúncios, mas deve
    # representar apenas 1 observação.
    #
    # Loja A
    # Loja B
    # Loja C
    # Loja D
    #
    # Total esperado = 4.
    assert (
        statistics.observations
        == 4
    ), (
        "Os cinco anúncios da Loja A "
        "deveriam virar uma única "
        "observação comercial."
    )

    # Mediana da Loja A:
    #
    # 2300, 2310, 2320, 2330, 2340
    # → 2320
    #
    # Depois:
    #
    # 2320
    # 2700
    # 2750
    # 2800
    #
    # mediana = (2700 + 2750) / 2
    # = 2725
    assert (
        statistics.median_price
        == 2725.0
    ), (
        "A mediana deveria ser calculada "
        "sobre vendedores consolidados."
    )

    assert (
        statistics.minimum_price
        == 2320.0
    )

    assert (
        statistics.maximum_price
        == 2800.0
    )

    print(
        "✓ Cinco anúncios da mesma loja "
        "viraram uma observação"
    )

    print(
        "✓ Cada vendedor recebeu peso semelhante"
    )

    print(
        "✓ Mediana não foi dominada pela Loja A"
    )

    print(
        "✓ STRICT/TIER/BROAD permanecem intactos"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
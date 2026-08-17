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
        official_store=False,
        full=False,
        shipping="Frete grátis",
        link=f"https://teste.com/{product_id}",
        image_url=None,
        international=False,
    )


def create_profile(
    *,
    product_id: str,
    brand: str,
    model: str,
    strict_key: str,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,
        brand=brand,
        model=model,
        memory_gb=None,
        variant=None,

        broad_key="ssd_nvme_1tb",

        tier_key="ssd_nvme_gen5_1tb",

        strict_key=strict_key,

        category="ssd",

        attributes={
            "capacity_gb": 1000,
            "capacity_label": "1tb",
            "interface": "nvme",
            "pcie_generation": "5.0",
            "identity_confidence": "alta",
        },
    )


def print_statistics(
    *,
    product: Product,
    statistics,
) -> None:
    print(
        "\n"
        + "=" * 80
    )

    print(
        f"Produto: {product.title}"
    )

    if statistics is None:
        print(
            "Nenhuma referência encontrada."
        )

        return

    print(
        "Escopo: "
        f"{statistics.comparison_scope}"
    )

    print(
        "Chave: "
        f"{statistics.comparison_key}"
    )

    print(
        "Observações: "
        f"{statistics.observations}"
    )

    print(
        "Mediana: "
        f"R$ {statistics.median_price:.2f}"
    )

    print(
        "Menor: "
        f"R$ {statistics.minimum_price:.2f}"
    )

    print(
        "Maior: "
        f"R$ {statistics.maximum_price:.2f}"
    )


def main() -> None:
    products = [
        create_product(
            product_id="SAM001",
            title="Samsung 9100 Pro 1TB Gen5",
            price=2550.0,
        ),

        create_product(
            product_id="SAM002",
            title="Samsung 9100 Pro 1TB Gen5",
            price=2690.0,
        ),

        create_product(
            product_id="WD001",
            title="WD SN8100 1TB Gen5",
            price=2459.0,
        ),

        create_product(
            product_id="CRU001",
            title="Crucial T705 1TB Gen5",
            price=2399.0,
        ),

        # Grupo amplo Gen4/básico.
        create_product(
            product_id="BROAD001",
            title="Kingston NV3 1TB Gen4",
            price=799.0,
        ),

        create_product(
            product_id="BROAD002",
            title="Lexar NM790 1TB Gen4",
            price=899.0,
        ),

        create_product(
            product_id="BROAD003",
            title="ADATA Legend 1TB Gen4",
            price=849.0,
        ),

        create_product(
            product_id="BROAD004",
            title="SSD NVMe 1TB Gen4",
            price=829.0,
        ),

        create_product(
            product_id="BROAD005",
            title="SSD NVMe 1TB Gen4",
            price=879.0,
        ),

        create_product(
            product_id="BROAD006",
            title="SSD NVMe 1TB Gen4",
            price=819.0,
        ),
    ]

    profiles = {
        "SAM001": create_profile(
            product_id="SAM001",
            brand="SAMSUNG",
            model="9100 PRO",
            strict_key=(
                "samsung_9100_pro_1tb_nvme"
            ),
        ),

        "SAM002": create_profile(
            product_id="SAM002",
            brand="SAMSUNG",
            model="9100 PRO",
            strict_key=(
                "samsung_9100_pro_1tb_nvme"
            ),
        ),

        "WD001": create_profile(
            product_id="WD001",
            brand="WESTERN DIGITAL",
            model="SN8100",
            strict_key=(
                "western_digital_sn8100_1tb_nvme"
            ),
        ),

        "CRU001": create_profile(
            product_id="CRU001",
            brand="CRUCIAL",
            model="T705",
            strict_key=(
                "crucial_t705_1tb_nvme"
            ),
        ),
    }

    # Produtos broad propositalmente não têm
    # tier Gen5.
    for product in products[4:]:
        profiles[
            product.id
        ] = ProductProfile(
            product_id=product.id,
            brand=None,
            model=None,
            memory_gb=None,
            variant=None,

            broad_key="ssd_nvme_1tb",

            tier_key=(
                "ssd_nvme_gen4_1tb"
            ),

            strict_key=None,

            category="ssd",

            attributes={
                "capacity_gb": 1000,
                "capacity_label": "1tb",
                "interface": "nvme",
                "pcie_generation": "4.0",
                "identity_confidence": "baixa",
            },
        )

    analyzer = PeerPriceAnalyzer(
        minimum_strict_peers=1,
        minimum_tier_peers=2,
        minimum_broad_peers=6,
    )

    # ==========================================================
    # SAMSUNG
    #
    # Existe outro Samsung 9100 Pro.
    # Deve usar STRICT.
    # ==========================================================

    samsung_statistics = (
        analyzer.get_product_statistics(
            product=products[0],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[0],
        statistics=samsung_statistics,
    )

    # ==========================================================
    # WD
    #
    # Não existe outro SN8100.
    # Existem pelo menos dois outros Gen5.
    # Deve usar TIER.
    # ==========================================================

    wd_statistics = (
        analyzer.get_product_statistics(
            product=products[2],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[2],
        statistics=wd_statistics,
    )

    # ==========================================================
    # VERIFICAÇÕES
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
        samsung_statistics
        is not None
    )

    assert (
        samsung_statistics
        .comparison_scope
        == "modelo_exato_nacional"
    )

    assert (
        samsung_statistics
        .comparison_key
        == "samsung_9100_pro_1tb_nvme"
    )

    assert (
        samsung_statistics.observations
        == 1
    )

    assert (
        wd_statistics
        is not None
    )

    assert (
        wd_statistics
        .comparison_scope
        == "mesmo_tier_nacional"
    )

    assert (
        wd_statistics
        .comparison_key
        == "ssd_nvme_gen5_1tb"
    )

    assert (
        wd_statistics.observations
        >= 2
    )

    # O WD não pode estar usando os SSDs
    # baratos do grupo geral.
    assert (
        wd_statistics.median_price
        > 2000
    )

    print(
        "✓ Mesmo modelo prioriza STRICT"
    )

    print(
        "✓ Falta de modelo exato usa TIER"
    )

    print(
        "✓ Gen5 não foi misturado "
        "com SSDs Gen4 básicos"
    )

    print(
        "✓ BROAD continua disponível "
        "como último fallback"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
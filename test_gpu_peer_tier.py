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
    seller: str,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=None,
        discount=None,
        installments=None,
        seller=seller,
        official_store=False,
        full=False,
        shipping="Frete grátis",
        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),
        image_url=None,
        international=False,
    )


def create_gpu_profile(
    *,
    product_id: str,
    brand: str | None,
    model: str,
    memory_gb: int,
    broad_key: str,
    tier_key: str,
    strict_key: str | None,
    variant: str | None,
    gpu_vendor: str,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,
        brand=brand,
        model=model,
        memory_gb=memory_gb,
        variant=variant,
        broad_key=broad_key,
        tier_key=tier_key,
        strict_key=strict_key,
        category="gpu",
        attributes={
            "gpu_vendor": gpu_vendor,
            "vram_gb": memory_gb,
            "variant": variant,
            "identity_confidence": (
                "alta"
                if strict_key is not None
                else "media"
            ),
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
        "Média: "
        f"R$ {statistics.average_price:.2f}"
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
        # ======================================================
        # RTX 5060 8GB
        # ======================================================

        create_product(
            product_id="VENTUS001",
            title=(
                "MSI RTX 5060 "
                "Ventus 2X 8GB"
            ),
            price=2499.0,
            seller="Loja A",
        ),

        create_product(
            product_id="VENTUS002",
            title=(
                "MSI RTX 5060 "
                "Ventus 2X 8GB"
            ),
            price=2599.0,
            seller="Loja B",
        ),

        create_product(
            product_id="VENTUS003",
            title=(
                "MSI RTX 5060 "
                "Ventus 2X OC 8GB"
            ),
            price=2450.0,
            seller="Loja A",
        ),

        create_product(
            product_id="SHADOW001",
            title=(
                "MSI RTX 5060 "
                "Shadow 2X 8GB"
            ),
            price=2399.0,
            seller="Loja C",
        ),

        create_product(
            product_id="TRIO001",
            title=(
                "MSI RTX 5060 "
                "Gaming Trio 8GB"
            ),
            price=3299.0,
            seller="Loja D",
        ),

        create_product(
            product_id="EAGLE001",
            title=(
                "Gigabyte RTX 5060 "
                "Eagle OC 8GB"
            ),
            price=2449.0,
            seller="Loja E",
        ),

        create_product(
            product_id="PNY001",
            title=(
                "PNY RTX 5060 "
                "Dual Fan 8GB"
            ),
            price=2429.0,
            seller="Loja F",
        ),

        # ======================================================
        # RTX 5060 TI 8GB
        # ======================================================

        create_product(
            product_id="5060TI001",
            title=(
                "MSI RTX 5060 Ti "
                "Ventus 2X 8GB"
            ),
            price=3099.0,
            seller="Loja G",
        ),

        create_product(
            product_id="5060TI002",
            title=(
                "Gigabyte RTX 5060 Ti "
                "Eagle 8GB"
            ),
            price=3199.0,
            seller="Loja H",
        ),

        # ======================================================
        # RTX 3050 6GB
        # ======================================================

        create_product(
            product_id="3050_6_A",
            title="MSI RTX 3050 6GB",
            price=1300.0,
            seller="Loja I",
        ),

        create_product(
            product_id="3050_6_B",
            title="Palit RTX 3050 6GB",
            price=1350.0,
            seller="Loja J",
        ),

        # ======================================================
        # RTX 3050 8GB
        # ======================================================

        create_product(
            product_id="3050_8_A",
            title="PCYes RTX 3050 8GB",
            price=1750.0,
            seller="Loja K",
        ),

        create_product(
            product_id="3050_8_B",
            title="ASUS RTX 3050 8GB",
            price=1850.0,
            seller="Loja L",
        ),
    ]

    profiles = {
        "VENTUS001": create_gpu_profile(
            product_id="VENTUS001",
            brand="MSI",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_"
                "ventus_2x_8gb"
            ),
            variant="ventus 2x",
            gpu_vendor="NVIDIA",
        ),

        "VENTUS002": create_gpu_profile(
            product_id="VENTUS002",
            brand="MSI",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_"
                "ventus_2x_8gb"
            ),
            variant="ventus 2x",
            gpu_vendor="NVIDIA",
        ),

        "VENTUS003": create_gpu_profile(
            product_id="VENTUS003",
            brand="MSI",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_"
                "ventus_2x_8gb"
            ),
            variant="ventus 2x",
            gpu_vendor="NVIDIA",
        ),

        "SHADOW001": create_gpu_profile(
            product_id="SHADOW001",
            brand="MSI",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_"
                "shadow_2x_8gb"
            ),
            variant="shadow 2x",
            gpu_vendor="NVIDIA",
        ),

        "TRIO001": create_gpu_profile(
            product_id="TRIO001",
            brand="MSI",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_"
                "gaming_trio_8gb"
            ),
            variant="gaming trio",
            gpu_vendor="NVIDIA",
        ),

        "EAGLE001": create_gpu_profile(
            product_id="EAGLE001",
            brand="GIGABYTE",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "gigabyte_rtx_5060_"
                "eagle_oc_8gb"
            ),
            variant="eagle oc",
            gpu_vendor="NVIDIA",
        ),

        "PNY001": create_gpu_profile(
            product_id="PNY001",
            brand="PNY",
            model="RTX 5060",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_8gb"
            ),
            strict_key=(
                "pny_rtx_5060_"
                "dual_fan_8gb"
            ),
            variant="dual fan",
            gpu_vendor="NVIDIA",
        ),

        "5060TI001": create_gpu_profile(
            product_id="5060TI001",
            brand="MSI",
            model="RTX 5060 Ti",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_ti_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_ti_8gb"
            ),
            strict_key=(
                "msi_rtx_5060_ti_"
                "ventus_2x_8gb"
            ),
            variant="ventus 2x",
            gpu_vendor="NVIDIA",
        ),

        "5060TI002": create_gpu_profile(
            product_id="5060TI002",
            brand="GIGABYTE",
            model="RTX 5060 Ti",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "50_60_ti_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_5060_ti_8gb"
            ),
            strict_key=None,
            variant=None,
            gpu_vendor="NVIDIA",
        ),

        "3050_6_A": create_gpu_profile(
            product_id="3050_6_A",
            brand="MSI",
            model="RTX 3050",
            memory_gb=6,
            broad_key=(
                "gpu_nvidia_"
                "30_50_standard_6gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_3050_6gb"
            ),
            strict_key=None,
            variant=None,
            gpu_vendor="NVIDIA",
        ),

        "3050_6_B": create_gpu_profile(
            product_id="3050_6_B",
            brand="PALIT",
            model="RTX 3050",
            memory_gb=6,
            broad_key=(
                "gpu_nvidia_"
                "30_50_standard_6gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_3050_6gb"
            ),
            strict_key=None,
            variant=None,
            gpu_vendor="NVIDIA",
        ),

        "3050_8_A": create_gpu_profile(
            product_id="3050_8_A",
            brand="PCYES",
            model="RTX 3050",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "30_50_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_3050_8gb"
            ),
            strict_key=None,
            variant=None,
            gpu_vendor="NVIDIA",
        ),

        "3050_8_B": create_gpu_profile(
            product_id="3050_8_B",
            brand="ASUS",
            model="RTX 3050",
            memory_gb=8,
            broad_key=(
                "gpu_nvidia_"
                "30_50_standard_8gb"
            ),
            tier_key=(
                "gpu_nvidia_"
                "rtx_3050_8gb"
            ),
            strict_key=None,
            variant=None,
            gpu_vendor="NVIDIA",
        ),
    }

    analyzer = PeerPriceAnalyzer(
        minimum_strict_peers=1,
        minimum_tier_peers=2,
        minimum_broad_peers=4,
    )

    # ==========================================================
    # VENTUS
    # ==========================================================

    ventus_statistics = (
        analyzer.get_product_statistics(
            product=products[0],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[0],
        statistics=ventus_statistics,
    )

    # ==========================================================
    # SHADOW
    # ==========================================================

    shadow_statistics = (
        analyzer.get_product_statistics(
            product=products[3],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[3],
        statistics=shadow_statistics,
    )

    # ==========================================================
    # RTX 5060 TI
    # ==========================================================

    ti_statistics = (
        analyzer.get_product_statistics(
            product=products[7],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[7],
        statistics=ti_statistics,
    )

    # ==========================================================
    # RTX 3050 6GB
    #
    # Só existe 1 peer, portanto não haverá referência.
    # Mais importante: 8GB NÃO pode ser usado.
    # ==========================================================

    rtx3050_6_statistics = (
        analyzer.get_product_statistics(
            product=products[9],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[9],
        statistics=rtx3050_6_statistics,
    )

    # ==========================================================
    # RTX 3050 8GB
    # ==========================================================

    rtx3050_8_statistics = (
        analyzer.get_product_statistics(
            product=products[11],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[11],
        statistics=rtx3050_8_statistics,
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

    # ======================================================
    # STRICT
    # ======================================================

    assert (
        ventus_statistics
        is not None
    )

    assert (
        ventus_statistics
        .comparison_scope
        == "modelo_exato_nacional"
    )

    assert (
        ventus_statistics
        .comparison_key
        == (
            "msi_rtx_5060_"
            "ventus_2x_8gb"
        )
    )

    # ======================================================
    # TIER
    # ======================================================

    assert (
        shadow_statistics
        is not None
    )

    assert (
        shadow_statistics
        .comparison_scope
        == "mesmo_tier_nacional"
    )

    assert (
        shadow_statistics
        .comparison_key
        == (
            "gpu_nvidia_"
            "rtx_5060_8gb"
        )
    )

    # ======================================================
    # 5060 TI
    # ======================================================

    assert (
        ti_statistics
        is None
    )

    # ======================================================
    # 3050 6GB VS 8GB
    # ======================================================

    assert (
        profiles["3050_6_A"].tier_key
        != profiles["3050_8_A"].tier_key
    )

    assert (
        profiles["3050_6_A"].broad_key
        != profiles["3050_8_A"].broad_key
    )

    assert (
        profiles["3050_6_A"].broad_key
        == (
            "gpu_nvidia_"
            "30_50_standard_6gb"
        )
    )

    assert (
        profiles["3050_8_A"].broad_key
        == (
            "gpu_nvidia_"
            "30_50_standard_8gb"
        )
    )

    # Como há apenas um outro anúncio de cada capacidade,
    # minimum_tier_peers=2 e minimum_broad_peers=4
    # não são atingidos.
    #
    # Isso também prova que 6GB e 8GB não foram somados.
    assert (
        rtx3050_6_statistics
        is None
    )

    assert (
        rtx3050_8_statistics
        is None
    )

    print(
        "✓ Ventus continua usando STRICT"
    )

    print(
        "✓ Shadow continua usando TIER"
    )

    print(
        "✓ RTX 5060 Ti continua isolada"
    )

    print(
        "✓ BROAD agora considera VRAM"
    )

    print(
        "✓ RTX 3050 6GB não mistura com 8GB"
    )

    print(
        "✓ RTX 3050 8GB não mistura com 6GB"
    )

    print(
        "✓ Poucos peers não forçam fallback inseguro"
    )

    print(
        "✓ STRICT/TIER/BROAD permanecem hierárquicos"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
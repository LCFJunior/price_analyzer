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


def create_cpu_profile(
    *,
    product_id: str,
    brand: str,
    model: str,
    broad_key: str,
    tier_key: str,
    strict_key: str,
    variant: str | None = None,
    variant_class: str = "standard",
    mobile: bool = False,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,
        brand=brand,
        model=model,
        memory_gb=None,
        variant=variant,

        broad_key=broad_key,
        tier_key=tier_key,
        strict_key=strict_key,

        category="cpu",

        attributes={
            "variant": variant,
            "variant_class": (
                variant_class
            ),
            "mobile": mobile,
            "identity_confidence": (
                "alta"
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
    # ==========================================================
    # PRODUTOS
    # ==========================================================

    products = [
        # ------------------------------------------------------
        # RYZEN 7 5700X
        # ------------------------------------------------------

        create_product(
            product_id="5700X_A",
            title=(
                "AMD Ryzen 7 5700X"
            ),
            price=1180.0,
            seller="Loja A",
        ),

        create_product(
            product_id="5700X_B",
            title=(
                "AMD Ryzen 7 5700X"
            ),
            price=1210.0,
            seller="Loja B",
        ),

        # ------------------------------------------------------
        # RYZEN 7 5800X
        # ------------------------------------------------------

        create_product(
            product_id="5800X_A",
            title=(
                "AMD Ryzen 7 5800X"
            ),
            price=1450.0,
            seller="Loja C",
        ),

        create_product(
            product_id="5800X_B",
            title=(
                "AMD Ryzen 7 5800X"
            ),
            price=1490.0,
            seller="Loja D",
        ),

        # ------------------------------------------------------
        # X3D
        # ------------------------------------------------------

        create_product(
            product_id="5700X3D_A",
            title=(
                "AMD Ryzen 7 5700X3D"
            ),
            price=1650.0,
            seller="Loja E",
        ),

        create_product(
            product_id="5700X3D_B",
            title=(
                "AMD Ryzen 7 5700X3D"
            ),
            price=1700.0,
            seller="Loja F",
        ),

        # ------------------------------------------------------
        # AMD APU
        # ------------------------------------------------------

        create_product(
            product_id="5600G_A",
            title=(
                "AMD Ryzen 5 5600G"
            ),
            price=820.0,
            seller="Loja G",
        ),

        create_product(
            product_id="5600GT_A",
            title=(
                "AMD Ryzen 5 5600GT"
            ),
            price=880.0,
            seller="Loja H",
        ),

        create_product(
            product_id="5600GT_B",
            title=(
                "AMD Ryzen 5 5600GT"
            ),
            price=900.0,
            seller="Loja I",
        ),

        # ------------------------------------------------------
        # AMD STANDARD
        # ------------------------------------------------------

        create_product(
            product_id="5600_A",
            title=(
                "AMD Ryzen 5 5600"
            ),
            price=700.0,
            seller="Loja J",
        ),

        create_product(
            product_id="5500_A",
            title=(
                "AMD Ryzen 5 5500"
            ),
            price=620.0,
            seller="Loja K",
        ),

        # ------------------------------------------------------
        # INTEL PERFORMANCE
        # ------------------------------------------------------

        create_product(
            product_id="13600K_A",
            title=(
                "Intel Core i5-13600K"
            ),
            price=1850.0,
            seller="Loja L",
        ),

        create_product(
            product_id="13600KF_A",
            title=(
                "Intel Core i5-13600KF"
            ),
            price=1750.0,
            seller="Loja M",
        ),

        create_product(
            product_id="13700K_A",
            title=(
                "Intel Core i7-13700K"
            ),
            price=2400.0,
            seller="Loja N",
        ),

        # ------------------------------------------------------
        # INTEL STANDARD / F
        # ------------------------------------------------------

        create_product(
            product_id="13400F_A",
            title=(
                "Intel Core i5-13400F"
            ),
            price=1150.0,
            seller="Loja O",
        ),

        create_product(
            product_id="13400_A",
            title=(
                "Intel Core i5-13400"
            ),
            price=1250.0,
            seller="Loja P",
        ),

        # ------------------------------------------------------
        # INTEL MOBILE
        # ------------------------------------------------------

        create_product(
            product_id="460M_A",
            title=(
                "Intel Core i5-460M"
            ),
            price=120.0,
            seller="Loja Q",
        ),

        create_product(
            product_id="520M_A",
            title=(
                "Intel Core i5-520M"
            ),
            price=140.0,
            seller="Loja R",
        ),
    ]

    # ==========================================================
    # PERFIS
    # ==========================================================

    profiles = {
        # ======================================================
        # AMD RYZEN 7 X
        # ======================================================

        "5700X_A": create_cpu_profile(
            product_id="5700X_A",
            brand="AMD",
            model="Ryzen 7 5700X",
            broad_key=(
                "cpu_amd_ryzen_7"
            ),
            tier_key=(
                "cpu_amd_ryzen_7_"
                "5000_x"
            ),
            strict_key=(
                "amd_ryzen_7_5700x"
            ),
            variant="X",
            variant_class="x",
        ),

        "5700X_B": create_cpu_profile(
            product_id="5700X_B",
            brand="AMD",
            model="Ryzen 7 5700X",
            broad_key=(
                "cpu_amd_ryzen_7"
            ),
            tier_key=(
                "cpu_amd_ryzen_7_"
                "5000_x"
            ),
            strict_key=(
                "amd_ryzen_7_5700x"
            ),
            variant="X",
            variant_class="x",
        ),

        "5800X_A": create_cpu_profile(
            product_id="5800X_A",
            brand="AMD",
            model="Ryzen 7 5800X",
            broad_key=(
                "cpu_amd_ryzen_7"
            ),
            tier_key=(
                "cpu_amd_ryzen_7_"
                "5000_x"
            ),
            strict_key=(
                "amd_ryzen_7_5800x"
            ),
            variant="X",
            variant_class="x",
        ),

        "5800X_B": create_cpu_profile(
            product_id="5800X_B",
            brand="AMD",
            model="Ryzen 7 5800X",
            broad_key=(
                "cpu_amd_ryzen_7"
            ),
            tier_key=(
                "cpu_amd_ryzen_7_"
                "5000_x"
            ),
            strict_key=(
                "amd_ryzen_7_5800x"
            ),
            variant="X",
            variant_class="x",
        ),

        # ======================================================
        # AMD X3D
        # ======================================================

        "5700X3D_A": (
            create_cpu_profile(
                product_id="5700X3D_A",
                brand="AMD",
                model="Ryzen 7 5700X3D",
                broad_key=(
                    "cpu_amd_ryzen_7"
                ),
                tier_key=(
                    "cpu_amd_ryzen_7_"
                    "5000_x3d"
                ),
                strict_key=(
                    "amd_ryzen_7_"
                    "5700x3d"
                ),
                variant="X3D",
                variant_class="x3d",
            )
        ),

        "5700X3D_B": (
            create_cpu_profile(
                product_id="5700X3D_B",
                brand="AMD",
                model="Ryzen 7 5700X3D",
                broad_key=(
                    "cpu_amd_ryzen_7"
                ),
                tier_key=(
                    "cpu_amd_ryzen_7_"
                    "5000_x3d"
                ),
                strict_key=(
                    "amd_ryzen_7_"
                    "5700x3d"
                ),
                variant="X3D",
                variant_class="x3d",
            )
        ),

        # ======================================================
        # AMD APU
        # ======================================================

        "5600G_A": create_cpu_profile(
            product_id="5600G_A",
            brand="AMD",
            model="Ryzen 5 5600G",
            broad_key=(
                "cpu_amd_ryzen_5"
            ),
            tier_key=(
                "cpu_amd_ryzen_5_"
                "5000_apu"
            ),
            strict_key=(
                "amd_ryzen_5_5600g"
            ),
            variant="G",
            variant_class="apu",
        ),

        "5600GT_A": create_cpu_profile(
            product_id="5600GT_A",
            brand="AMD",
            model="Ryzen 5 5600GT",
            broad_key=(
                "cpu_amd_ryzen_5"
            ),
            tier_key=(
                "cpu_amd_ryzen_5_"
                "5000_apu"
            ),
            strict_key=(
                "amd_ryzen_5_5600gt"
            ),
            variant="GT",
            variant_class="apu",
        ),

        "5600GT_B": create_cpu_profile(
            product_id="5600GT_B",
            brand="AMD",
            model="Ryzen 5 5600GT",
            broad_key=(
                "cpu_amd_ryzen_5"
            ),
            tier_key=(
                "cpu_amd_ryzen_5_"
                "5000_apu"
            ),
            strict_key=(
                "amd_ryzen_5_5600gt"
            ),
            variant="GT",
            variant_class="apu",
        ),

        # ======================================================
        # AMD STANDARD
        # ======================================================

        "5600_A": create_cpu_profile(
            product_id="5600_A",
            brand="AMD",
            model="Ryzen 5 5600",
            broad_key=(
                "cpu_amd_ryzen_5"
            ),
            tier_key=(
                "cpu_amd_ryzen_5_"
                "5000_standard"
            ),
            strict_key=(
                "amd_ryzen_5_5600"
            ),
            variant=None,
            variant_class="standard",
        ),

        "5500_A": create_cpu_profile(
            product_id="5500_A",
            brand="AMD",
            model="Ryzen 5 5500",
            broad_key=(
                "cpu_amd_ryzen_5"
            ),
            tier_key=(
                "cpu_amd_ryzen_5_"
                "5000_standard"
            ),
            strict_key=(
                "amd_ryzen_5_5500"
            ),
            variant=None,
            variant_class="standard",
        ),

        # ======================================================
        # INTEL DESKTOP PERFORMANCE
        # ======================================================

        "13600K_A": create_cpu_profile(
            product_id="13600K_A",
            brand="INTEL",
            model="Core I5-13600K",
            broad_key=(
                "cpu_intel_core_"
                "i5_desktop"
            ),
            tier_key=(
                "cpu_intel_core_i5_"
                "gen13_performance"
            ),
            strict_key=(
                "intel_core_i5_13600k"
            ),
            variant="K",
            variant_class=(
                "performance"
            ),
            mobile=False,
        ),

        "13600KF_A": (
            create_cpu_profile(
                product_id="13600KF_A",
                brand="INTEL",
                model="Core I5-13600KF",
                broad_key=(
                    "cpu_intel_core_"
                    "i5_desktop"
                ),
                tier_key=(
                    "cpu_intel_core_i5_"
                    "gen13_performance"
                ),
                strict_key=(
                    "intel_core_i5_"
                    "13600kf"
                ),
                variant="KF",
                variant_class=(
                    "performance"
                ),
                mobile=False,
            )
        ),

        "13700K_A": create_cpu_profile(
            product_id="13700K_A",
            brand="INTEL",
            model="Core I7-13700K",
            broad_key=(
                "cpu_intel_core_"
                "i7_desktop"
            ),
            tier_key=(
                "cpu_intel_core_i7_"
                "gen13_performance"
            ),
            strict_key=(
                "intel_core_i7_13700k"
            ),
            variant="K",
            variant_class=(
                "performance"
            ),
            mobile=False,
        ),

        # ======================================================
        # INTEL DESKTOP STANDARD / F
        # ======================================================

        "13400F_A": create_cpu_profile(
            product_id="13400F_A",
            brand="INTEL",
            model="Core I5-13400F",
            broad_key=(
                "cpu_intel_core_"
                "i5_desktop"
            ),
            tier_key=(
                "cpu_intel_core_i5_"
                "gen13_standard_f"
            ),
            strict_key=(
                "intel_core_i5_13400f"
            ),
            variant="F",
            variant_class=(
                "standard_f"
            ),
            mobile=False,
        ),

        "13400_A": create_cpu_profile(
            product_id="13400_A",
            brand="INTEL",
            model="Core I5-13400",
            broad_key=(
                "cpu_intel_core_"
                "i5_desktop"
            ),
            tier_key=(
                "cpu_intel_core_i5_"
                "gen13_standard"
            ),
            strict_key=(
                "intel_core_i5_13400"
            ),
            variant=None,
            variant_class=(
                "standard"
            ),
            mobile=False,
        ),

        # ======================================================
        # INTEL MOBILE
        # ======================================================

        "460M_A": create_cpu_profile(
            product_id="460M_A",
            brand="INTEL",
            model="Core I5-460M",
            broad_key=(
                "cpu_intel_core_"
                "i5_mobile"
            ),
            tier_key=(
                "cpu_intel_core_i5_"
                "gen1_mobile"
            ),
            strict_key=(
                "intel_core_i5_460m"
            ),
            variant="M",
            variant_class="mobile",
            mobile=True,
        ),

        "520M_A": create_cpu_profile(
            product_id="520M_A",
            brand="INTEL",
            model="Core I5-520M",
            broad_key=(
                "cpu_intel_core_"
                "i5_mobile"
            ),
            tier_key=(
                "cpu_intel_core_i5_"
                "gen1_mobile"
            ),
            strict_key=(
                "intel_core_i5_520m"
            ),
            variant="M",
            variant_class="mobile",
            mobile=True,
        ),
    }

    # ==========================================================
    # ANALYZER
    # ==========================================================

    analyzer = PeerPriceAnalyzer(
        minimum_strict_peers=1,
        minimum_tier_peers=2,
        minimum_broad_peers=4,
    )

    # ==========================================================
    # TESTE 1
    #
    # 5700X possui outro 5700X.
    # STRICT deve vencer.
    # ==========================================================

    strict_5700x = (
        analyzer.get_product_statistics(
            product=products[0],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[0],
        statistics=strict_5700x,
    )

    # ==========================================================
    # TESTE 2
    #
    # 5800X possui outro 5800X.
    # STRICT também deve vencer.
    # ==========================================================

    strict_5800x = (
        analyzer.get_product_statistics(
            product=products[2],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[2],
        statistics=strict_5800x,
    )

    # ==========================================================
    # TESTE 3
    #
    # 5900X fictício não possui STRICT.
    #
    # Deve usar o TIER:
    #
    # cpu_amd_ryzen_7_5000_x
    #
    # X3D não pode entrar.
    # ==========================================================

    target_5900x = (
        create_product(
            product_id="5900X_TARGET",
            title="AMD Ryzen 7 5900X",
            price=1350.0,
            seller="Loja Target",
        )
    )

    products_with_target = (
        products
        + [
            target_5900x,
        ]
    )

    profiles_with_target = (
        profiles.copy()
    )

    profiles_with_target[
        "5900X_TARGET"
    ] = create_cpu_profile(
        product_id="5900X_TARGET",
        brand="AMD",
        model="Ryzen 7 5900X",
        broad_key=(
            "cpu_amd_ryzen_7"
        ),
        tier_key=(
            "cpu_amd_ryzen_7_"
            "5000_x"
        ),
        strict_key=(
            "amd_ryzen_7_5900x"
        ),
        variant="X",
        variant_class="x",
    )

    tier_5900x = (
        analyzer.get_product_statistics(
            product=target_5900x,
            products=products_with_target,
            profiles=profiles_with_target,
        )
    )

    print_statistics(
        product=target_5900x,
        statistics=tier_5900x,
    )

    # ==========================================================
    # TESTE 4
    #
    # 5600G não possui outro 5600G.
    #
    # Existem dois 5600GT no tier APU.
    # Deve usar TIER.
    # ==========================================================

    apu_statistics = (
        analyzer.get_product_statistics(
            product=products[6],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[6],
        statistics=apu_statistics,
    )

    # ==========================================================
    # TESTE 5
    #
    # Intel 13600K.
    #
    # STRICT:
    # nenhum outro 13600K.
    #
    # TIER performance:
    # somente 13600KF.
    #
    # 1 peer < mínimo 2.
    #
    # BROAD desktop:
    #
    # 13600KF
    # 13400F
    # 13400
    #
    # Total = 3.
    #
    # 3 < minimum_broad_peers=4.
    #
    # Portanto não deve existir referência.
    #
    # Os CPUs mobile NÃO podem entrar.
    # ==========================================================

    intel_performance = (
        analyzer.get_product_statistics(
            product=products[11],
            products=products,
            profiles=profiles,
        )
    )

    print_statistics(
        product=products[11],
        statistics=intel_performance,
    )

    # ==========================================================
    # TESTE 6
    #
    # Verificação específica de isolamento.
    #
    # Mobile deve possuir BROAD diferente
    # de desktop.
    # ==========================================================

    assert (
        profiles["460M_A"].broad_key
        == "cpu_intel_core_i5_mobile"
    )

    assert (
        profiles["13600K_A"].broad_key
        == "cpu_intel_core_i5_desktop"
    )

    assert (
        profiles["460M_A"].broad_key
        != profiles["13600K_A"].broad_key
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

    # ======================================================
    # STRICT 5700X
    # ======================================================

    assert (
        strict_5700x
        is not None
    )

    assert (
        strict_5700x
        .comparison_scope
        == "modelo_exato_nacional"
    )

    assert (
        strict_5700x
        .comparison_key
        == "amd_ryzen_7_5700x"
    )

    assert (
        strict_5700x.observations
        == 1
    )

    assert (
        strict_5700x.median_price
        == 1210.0
    )

    # ======================================================
    # STRICT 5800X
    # ======================================================

    assert (
        strict_5800x
        is not None
    )

    assert (
        strict_5800x
        .comparison_scope
        == "modelo_exato_nacional"
    )

    assert (
        strict_5800x
        .comparison_key
        == "amd_ryzen_7_5800x"
    )

    assert (
        strict_5800x.observations
        == 1
    )

    # ======================================================
    # TIER RYZEN X
    # ======================================================

    assert (
        tier_5900x
        is not None
    )

    assert (
        tier_5900x
        .comparison_scope
        == "mesmo_tier_nacional"
    )

    assert (
        tier_5900x
        .comparison_key
        == (
            "cpu_amd_ryzen_7_"
            "5000_x"
        )
    )

    assert (
        tier_5900x.observations
        == 4
    )

    # Peers usados:
    #
    # 5700X 1180
    # 5700X 1210
    # 5800X 1450
    # 5800X 1490
    #
    # Mediana:
    #
    # (1210 + 1450) / 2 = 1330
    assert (
        tier_5900x.median_price
        == 1330.0
    )

    # X3D não entrou.
    assert (
        tier_5900x.maximum_price
        == 1490.0
    )

    # ======================================================
    # TIER APU
    # ======================================================

    assert (
        apu_statistics
        is not None
    )

    assert (
        apu_statistics
        .comparison_scope
        == "mesmo_tier_nacional"
    )

    assert (
        apu_statistics
        .comparison_key
        == (
            "cpu_amd_ryzen_5_"
            "5000_apu"
        )
    )

    assert (
        apu_statistics.observations
        == 2
    )

    assert (
        apu_statistics.minimum_price
        == 880.0
    )

    assert (
        apu_statistics.maximum_price
        == 900.0
    )

    assert (
        apu_statistics.median_price
        == 890.0
    )

    # Modelos standard:
    #
    # 5600 = 700
    # 5500 = 620
    #
    # Não podem entrar.
    assert (
        apu_statistics.minimum_price
        > 700.0
    )

    # ======================================================
    # INTEL
    # ======================================================

    assert (
        intel_performance
        is None
    )

    # ======================================================
    # BROAD INTEL
    # ======================================================

    assert (
        profiles["13600K_A"].broad_key
        == "cpu_intel_core_i5_desktop"
    )

    assert (
        profiles["13600KF_A"].broad_key
        == "cpu_intel_core_i5_desktop"
    )

    assert (
        profiles["13400F_A"].broad_key
        == "cpu_intel_core_i5_desktop"
    )

    assert (
        profiles["13400_A"].broad_key
        == "cpu_intel_core_i5_desktop"
    )

    assert (
        profiles["460M_A"].broad_key
        == "cpu_intel_core_i5_mobile"
    )

    assert (
        profiles["520M_A"].broad_key
        == "cpu_intel_core_i5_mobile"
    )

    assert (
        profiles["460M_A"].broad_key
        != profiles["13600K_A"].broad_key
    )

    # ======================================================
    # RESULTADOS
    # ======================================================

    print(
        "✓ STRICT continua com prioridade"
    )

    print(
        "✓ Ryzen 5700X usa modelo exato"
    )

    print(
        "✓ Ryzen 5800X usa modelo exato"
    )

    print(
        "✓ TIER é usado quando "
        "STRICT não possui peers"
    )

    print(
        "✓ Ryzen X separado de X3D"
    )

    print(
        "✓ Ryzen APU separado "
        "de modelos standard"
    )

    print(
        "✓ 5600G e 5600GT "
        "compartilham tier APU"
    )

    print(
        "✓ Intel performance não usa "
        "um único peer como referência"
    )

    print(
        "✓ Intel desktop separado "
        "de Intel mobile"
    )

    print(
        "✓ CPU mobile antiga não "
        "contamina BROAD desktop"
    )

    print(
        "✓ Minimum tier peers "
        "continua protegendo o sistema"
    )

    print(
        "✓ Minimum broad peers "
        "continua protegendo o sistema"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
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
        price=3000.0,
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
        # ==================================================
        # RTX 5060 - VARIANTES
        # ==================================================

        create_product(
            "MSI001",
            (
                "Placa De Video MSI "
                "GeForce RTX 5060 "
                "8GB Ventus 2X OC Edition"
            ),
        ),

        create_product(
            "MSI002",
            (
                "Placa De Video MSI "
                "GeForce RTX5060 "
                "Shadow 2X OC 8GB"
            ),
        ),

        create_product(
            "MSI003",
            (
                "Placa De Video MSI "
                "RTX5060 Gaming Trio "
                "OC 8GB"
            ),
        ),

        # ==================================================
        # RTX 5070 TI - CASO REAL
        # ==================================================

        create_product(
            "REAL_RTX5070TI",
            (
                "Placa De Video Nv "
                "Rtx5070ti Shadow MSI"
            ),
        ),

        create_product(
            "RTX5070TI_WITH_VRAM",
            (
                "MSI RTX5070Ti "
                "Shadow 3X 16GB"
            ),
        ),

        # ==================================================
        # RTX COM HÍFEN
        # ==================================================

        create_product(
            "RTX_HYPHEN",
            (
                "Gigabyte GeForce "
                "RTX-5070-12GB "
                "Gaming OC"
            ),
        ),

        # ==================================================
        # RTX 3050 6GB / 8GB
        # ==================================================

        create_product(
            "3050_6GB",
            (
                "MSI RTX3050 "
                "Ventus 2X 6GB"
            ),
        ),

        create_product(
            "3050_8GB",
            (
                "Pcyes RTX 3050 "
                "Black Edition 8GB"
            ),
        ),

        # ==================================================
        # GT210 / G210
        # ==================================================

        create_product(
            "GT210_REAL",
            (
                "Placa De Vídeo "
                "Gt210 Ddr3 Vga "
                "Hdmi 1gb 500mhz"
            ),
        ),

        create_product(
            "G210_STANDARD",
            (
                "Vinik GeForce "
                "G210 1GB DDR3"
            ),
        ),

        create_product(
            "GT210_COMPACT",
            (
                "VXpro Geforce "
                "GT210 1GB DDR3"
            ),
        ),

        # ==================================================
        # GT 730
        # ==================================================

        create_product(
            "GT730",
            (
                "Placa De Video "
                "Clanm Geforce Nvidia "
                "Gt730 4gb Ddr3"
            ),
        ),

        # ==================================================
        # RX 500 - CASOS REAIS
        # ==================================================

        create_product(
            "RX580_REVENGER",
            (
                "Placa De Video "
                "Amd Radeon Rx580 "
                "8gb Gddr5 256 Bits "
                "Revenger"
            ),
        ),

        create_product(
            "RX580_SOYO",
            (
                "Placa De Vídeo "
                "Soyo Radeon Rx580 "
                "8gb 256bit Gddr5 "
                "Hdmi Gamer"
            ),
        ),

        create_product(
            "RX570",
            (
                "XFX Radeon "
                "RX 570 8GB GDDR5"
            ),
        ),

        create_product(
            "RX560",
            (
                "PowerColor Radeon "
                "RX560 4GB GDDR5"
            ),
        ),

        create_product(
            "RX550",
            (
                "Sapphire Radeon "
                "RX 550 4GB"
            ),
        ),

        # ==================================================
        # AMD MAIS NOVAS
        # ==================================================

        create_product(
            "RX7600",
            (
                "PowerColor RX7600 "
                "8GB Fighter"
            ),
        ),

        create_product(
            "RX7800XT",
            (
                "Sapphire RX7800XT "
                "16GB Nitro Plus"
            ),
        ),

        create_product(
            "RX7900XTX",
            (
                "XFX RX7900XTX "
                "24GB Merc 310"
            ),
        ),

        # ==================================================
        # MARCAS
        # ==================================================

        create_product(
            "PCYES",
            (
                "Pcyes RTX3050 "
                "6GB Dual Fan"
            ),
        ),

        create_product(
            "PELADN",
            (
                "Peladn GTX1660Super "
                "6GB GDDR6"
            ),
        ),

        create_product(
            "SOYO",
            (
                "Soyo RX580 "
                "8GB GDDR5"
            ),
        ),

        create_product(
            "VXPRO",
            (
                "VXpro GT210 "
                "1GB DDR3"
            ),
        ),

        # ==================================================
        # SEM VRAM
        # ==================================================

        create_product(
            "NO_VRAM",
            (
                "Gigabyte "
                "RTX5070 Windforce OC"
            ),
        ),

        # ==================================================
        # PRODUTO SEM MARCA
        # ==================================================

        create_product(
            "NO_BRAND",
            (
                "Placa de Video "
                "GeForce RTX3060 "
                "12GB GDDR6"
            ),
        ),

        # ==================================================
        # INVÁLIDOS
        # ==================================================

        create_product(
            "INVALID001",
            (
                "Notebook Gamer ASUS "
                "RTX5070 12GB"
            ),
        ),

        create_product(
            "INVALID002",
            (
                "PC Gamer Ryzen 7 "
                "RTX5070 12GB"
            ),
        ),

        create_product(
            "INVALID003",
            (
                "Waterblock para "
                "RTX5070 ASUS"
            ),
        ),

        create_product(
            "INVALID004",
            (
                "Suporte Vertical "
                "para RTX5070"
            ),
        ),

        create_product(
            "INVALID005",
            (
                "Caixa Vazia "
                "RTX5070 MSI"
            ),
        ),
    ]

    classifier = (
        ProductClassifier()
    )

    profiles = {}

    for product in products:
        profile = (
            classifier.classify(
                product
            )
        )

        profiles[
            product.id
        ] = profile

        print(
            "\n"
            + "=" * 80
        )

        print(
            f"Título: {product.title}"
        )

        print(
            f"Categoria: {profile.category}"
        )

        print(
            f"Marca: {profile.brand}"
        )

        print(
            f"Modelo: {profile.model}"
        )

        print(
            f"VRAM: {profile.memory_gb}"
        )

        print(
            f"Variante: {profile.variant}"
        )

        print(
            f"BROAD: {profile.broad_key}"
        )

        print(
            f"TIER: {profile.tier_key}"
        )

        print(
            f"STRICT: {profile.strict_key}"
        )

        print(
            "Atributos:"
        )

        for (
            key,
            value,
        ) in profile.attributes.items():
            print(
                f"- {key}: {value}"
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
    # RTX 5060
    # ======================================================

    assert (
        profiles["MSI001"].model
        == "RTX 5060"
    )

    assert (
        profiles["MSI001"].strict_key
        == (
            "msi_rtx_5060_"
            "ventus_2x_8gb"
        )
    )

    assert (
        profiles["MSI002"].strict_key
        == (
            "msi_rtx_5060_"
            "shadow_2x_8gb"
        )
    )

    assert (
        profiles["MSI003"].strict_key
        == (
            "msi_rtx_5060_"
            "gaming_trio_8gb"
        )
    )

    # ======================================================
    # RTX5070TI COMPACTA
    # ======================================================

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].category
        == "gpu"
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].brand
        == "MSI"
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].model
        == "RTX 5070 Ti"
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].variant
        == "shadow"
    )

    # Sem VRAM, não cria BROAD
    # nem STRICT.
    assert (
        profiles[
            "REAL_RTX5070TI"
        ].memory_gb
        is None
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].broad_key
        is None
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].strict_key
        is None
    )

    assert (
        profiles[
            "REAL_RTX5070TI"
        ].tier_key
        == (
            "gpu_nvidia_"
            "rtx_5070_ti"
        )
    )

    # Com VRAM já pode criar BROAD/STRICT.
    assert (
        profiles[
            "RTX5070TI_WITH_VRAM"
        ].broad_key
        == (
            "gpu_nvidia_"
            "50_70_ti_16gb"
        )
    )

    assert (
        profiles[
            "RTX5070TI_WITH_VRAM"
        ].strict_key
        == (
            "msi_rtx_5070_ti_"
            "shadow_3x_16gb"
        )
    )

    # ======================================================
    # RTX COM HÍFEN
    # ======================================================

    assert (
        profiles["RTX_HYPHEN"].model
        == "RTX 5070"
    )

    assert (
        profiles["RTX_HYPHEN"].memory_gb
        == 12
    )

    # ======================================================
    # VRAM NO BROAD
    # ======================================================

    assert (
        profiles["3050_6GB"].broad_key
        == (
            "gpu_nvidia_"
            "30_50_standard_6gb"
        )
    )

    assert (
        profiles["3050_8GB"].broad_key
        == (
            "gpu_nvidia_"
            "30_50_standard_8gb"
        )
    )

    assert (
        profiles["3050_6GB"].broad_key
        != profiles["3050_8GB"].broad_key
    )

    # ======================================================
    # GT210
    # ======================================================

    assert (
        profiles["GT210_REAL"].category
        == "gpu"
    )

    assert (
        profiles["GT210_REAL"].model
        == "G210"
    )

    assert (
        profiles["GT210_REAL"].memory_gb
        == 1
    )

    assert (
        profiles["GT210_REAL"].tier_key
        == "gpu_nvidia_g210_1gb"
    )

    assert (
        profiles["GT210_REAL"].broad_key
        == (
            "gpu_nvidia_"
            "200_10_standard_1gb"
        )
    )

    assert (
        profiles["G210_STANDARD"].model
        == "G210"
    )

    assert (
        profiles["GT210_COMPACT"].model
        == "G210"
    )

    assert (
        profiles["GT210_REAL"].tier_key
        == profiles["G210_STANDARD"].tier_key
        == profiles["GT210_COMPACT"].tier_key
    )

    # ======================================================
    # GT730
    # ======================================================

    assert (
        profiles["GT730"].model
        == "GT 730"
    )

    assert (
        profiles["GT730"].broad_key
        == (
            "gpu_nvidia_"
            "700_30_standard_4gb"
        )
    )

    # ======================================================
    # RX 580
    # ======================================================

    assert (
        profiles[
            "RX580_REVENGER"
        ].category
        == "gpu"
    )

    assert (
        profiles[
            "RX580_REVENGER"
        ].brand
        == "REVENGER"
    )

    assert (
        profiles[
            "RX580_REVENGER"
        ].model
        == "RX 580"
    )

    assert (
        profiles[
            "RX580_REVENGER"
        ].memory_gb
        == 8
    )

    assert (
        profiles[
            "RX580_REVENGER"
        ].broad_key
        == (
            "gpu_amd_"
            "500_80_standard_8gb"
        )
    )

    assert (
        profiles[
            "RX580_REVENGER"
        ].tier_key
        == (
            "gpu_amd_"
            "rx_580_8gb"
        )
    )

    assert (
        profiles[
            "RX580_SOYO"
        ].brand
        == "SOYO"
    )

    assert (
        profiles[
            "RX580_SOYO"
        ].model
        == "RX 580"
    )

    assert (
        profiles[
            "RX580_SOYO"
        ].tier_key
        == profiles[
            "RX580_REVENGER"
        ].tier_key
    )

    # ======================================================
    # OUTRAS RX 500
    # ======================================================

    assert (
        profiles["RX570"].broad_key
        == (
            "gpu_amd_"
            "500_70_standard_8gb"
        )
    )

    assert (
        profiles["RX560"].broad_key
        == (
            "gpu_amd_"
            "500_60_standard_4gb"
        )
    )

    assert (
        profiles["RX550"].broad_key
        == (
            "gpu_amd_"
            "500_50_standard_4gb"
        )
    )

    # ======================================================
    # AMD MODERNAS
    # ======================================================

    assert (
        profiles["RX7600"].broad_key
        == (
            "gpu_amd_"
            "7000_60_standard_8gb"
        )
    )

    assert (
        profiles["RX7800XT"].broad_key
        == (
            "gpu_amd_"
            "7000_80_xt_16gb"
        )
    )

    assert (
        profiles["RX7900XTX"].broad_key
        == (
            "gpu_amd_"
            "7000_90_xtx_24gb"
        )
    )

    # ======================================================
    # MARCAS
    # ======================================================

    assert (
        profiles["PCYES"].brand
        == "PCYES"
    )

    assert (
        profiles["PELADN"].brand
        == "PELADN"
    )

    assert (
        profiles["SOYO"].brand
        == "SOYO"
    )

    assert (
        profiles["VXPRO"].brand
        == "VXPRO"
    )

    # ======================================================
    # SEM VRAM
    # ======================================================

    assert (
        profiles["NO_VRAM"].model
        == "RTX 5070"
    )

    assert (
        profiles["NO_VRAM"].memory_gb
        is None
    )

    assert (
        profiles["NO_VRAM"].broad_key
        is None
    )

    assert (
        profiles["NO_VRAM"].strict_key
        is None
    )

    # ======================================================
    # SEM MARCA
    # ======================================================

    assert (
        profiles["NO_BRAND"].category
        == "gpu"
    )

    assert (
        profiles["NO_BRAND"].brand
        is None
    )

    assert (
        profiles["NO_BRAND"].model
        == "RTX 3060"
    )

    assert (
        profiles["NO_BRAND"].tier_key
        == (
            "gpu_nvidia_"
            "rtx_3060_12gb"
        )
    )

    assert (
        profiles["NO_BRAND"].strict_key
        is None
    )

    # ======================================================
    # INVÁLIDOS
    # ======================================================

    for product_id in (
        "INVALID001",
        "INVALID002",
        "INVALID003",
        "INVALID004",
        "INVALID005",
    ):
        assert (
            profiles[
                product_id
            ].category
            is None
        )

    print(
        "✓ RTX compacta reconhecida"
    )

    print(
        "✓ RTX5070Ti compacta reconhecida"
    )

    print(
        "✓ RTX com hífen reconhecida"
    )

    print(
        "✓ Shadow genérico reconhecido"
    )

    print(
        "✓ GT210 convertido para G210"
    )

    print(
        "✓ GT210/G210 compartilham TIER"
    )

    print(
        "✓ GT730 continua funcionando"
    )

    print(
        "✓ RX580 reconhecida"
    )

    print(
        "✓ RX580 Revenger reconhecida"
    )

    print(
        "✓ RX580 Soyo reconhecida"
    )

    print(
        "✓ RX570/RX560/RX550 reconhecidas"
    )

    print(
        "✓ RX modernas continuam funcionando"
    )

    print(
        "✓ BROAD continua separando VRAM"
    )

    print(
        "✓ Produto sem VRAM não recebe BROAD"
    )

    print(
        "✓ Produto sem marca não recebe STRICT"
    )

    print(
        "✓ Soyo reconhecida"
    )

    print(
        "✓ VXPRO reconhecida"
    )

    print(
        "✓ Inválidos continuam bloqueados"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
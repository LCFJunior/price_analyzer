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
        # ==================================================
        # AMD
        # ==================================================

        create_product(
            "AMD001",
            (
                "Processador AMD Ryzen 7 "
                "5700X OEM Sem Cooler"
            ),
        ),

        create_product(
            "AMD002",
            (
                "Processador AMD Ryzen 7 "
                "5700X Box"
            ),
        ),

        create_product(
            "AMD003",
            (
                "AMD Ryzen 7 5700X3D "
                "AM4"
            ),
        ),

        create_product(
            "AMD004",
            (
                "AMD Ryzen 5 5600 "
                "Processador"
            ),
        ),

        create_product(
            "AMD005",
            (
                "Processador Ryzen 5 "
                "5600G Radeon Graphics"
            ),
        ),

        create_product(
            "AMD006",
            (
                "AMD Ryzen 7 7800X3D "
                "Processador"
            ),
        ),

        create_product(
            "AMD007",
            (
                "AMD Ryzen 9 9950X "
                "Processador"
            ),
        ),

        create_product(
            "AMD008",
            (
                "AMD R7 5700X "
                "100-100000926WOF"
            ),
        ),

        # Caso real encontrado na coleta ampla.
        create_product(
            "AMD009",
            (
                "Processador AMD Ryzen 5 "
                "5600GT com Cooler, "
                "3.6GHz 6-Cores"
            ),
        ),

        # ==================================================
        # INTEL
        # ==================================================

        create_product(
            "INTEL001",
            (
                "Processador Intel "
                "Core i5-10400"
            ),
        ),

        create_product(
            "INTEL002",
            (
                "Intel Core i7-11700 "
                "Processador"
            ),
        ),

        create_product(
            "INTEL003",
            (
                "Intel Core i5-12400F "
                "LGA1700"
            ),
        ),

        create_product(
            "INTEL004",
            (
                "Processador Intel "
                "Core i5 13600KF"
            ),
        ),

        create_product(
            "INTEL005",
            (
                "Intel Core i7-14700K "
                "Processador"
            ),
        ),

        create_product(
            "INTEL006",
            (
                "Intel Core i9-14900KS"
            ),
        ),

        create_product(
            "INTEL007",
            (
                "Intel Core i9-9900K"
            ),
        ),

        # Casos reais antigos.
        create_product(
            "INTEL008",
            (
                "Processador Intel Core "
                "i5-3570"
            ),
        ),

        create_product(
            "INTEL009",
            (
                "Processador Intel Core "
                "i7-3770"
            ),
        ),

        create_product(
            "INTEL010",
            (
                "Processador Intel Core "
                "I5 - 460m 2.53GHz"
            ),
        ),

        # ==================================================
        # PRODUTOS INVÁLIDOS
        # ==================================================

        create_product(
            "INVALID001",
            (
                "Caixa Vazia AMD CPU "
                "Ryzen 7 5700X "
                "Adesivo Blister Manual"
            ),
        ),

        create_product(
            "INVALID002",
            (
                "Kit Upgrade Ryzen 7 "
                "5700X Placa Mae B550"
            ),
        ),

        create_product(
            "INVALID003",
            (
                "Cooler Para Ryzen 7 "
                "5700X AM4"
            ),
        ),

        create_product(
            "INVALID004",
            (
                "Placa Mae B550 Para "
                "Ryzen 7 5700X"
            ),
        ),

        create_product(
            "INVALID005",
            (
                "Processador de Alimentos "
                "500ml 3 Lâminas"
            ),
        ),

        create_product(
            "INVALID006",
            (
                "Processador de Audio "
                "Automotivo Crossover"
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
            "Categoria: "
            f"{profile.category}"
        )

        print(
            "Marca: "
            f"{profile.brand}"
        )

        print(
            "Modelo: "
            f"{profile.model}"
        )

        print(
            "Variante: "
            f"{profile.variant}"
        )

        print(
            "Chave geral: "
            f"{profile.broad_key}"
        )

        print(
            "Chave tier: "
            f"{profile.tier_key}"
        )

        print(
            "Chave específica: "
            f"{profile.strict_key}"
        )

        print(
            "Atributos:"
        )

        for (
            key,
            value,
        ) in (
            profile.attributes.items()
        ):
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
    # AMD 5700X
    # ======================================================

    assert (
        profiles["AMD001"].category
        == "cpu"
    )

    assert (
        profiles["AMD001"].brand
        == "AMD"
    )

    assert (
        profiles["AMD001"].model
        == "Ryzen 7 5700X"
    )

    assert (
        profiles["AMD001"].variant
        == "X"
    )

    assert (
        profiles["AMD001"].strict_key
        == "amd_ryzen_7_5700x"
    )

    assert (
        profiles["AMD001"].broad_key
        == "cpu_amd_ryzen_7"
    )

    assert (
        profiles["AMD001"].tier_key
        == "cpu_amd_ryzen_7_5000_x"
    )

    assert (
        profiles["AMD001"]
        .attributes["variant_class"]
        == "x"
    )

    # OEM e BOX do mesmo processador
    # precisam gerar a mesma identidade.
    assert (
        profiles["AMD001"].strict_key
        == profiles["AMD002"].strict_key
    )

    assert (
        profiles["AMD001"].tier_key
        == profiles["AMD002"].tier_key
    )

    # ======================================================
    # AMD X3D
    # ======================================================

    assert (
        profiles["AMD003"].model
        == "Ryzen 7 5700X3D"
    )

    assert (
        profiles["AMD003"].variant
        == "X3D"
    )

    assert (
        profiles["AMD003"].strict_key
        == "amd_ryzen_7_5700x3d"
    )

    assert (
        profiles["AMD003"].tier_key
        == "cpu_amd_ryzen_7_5000_x3d"
    )

    assert (
        profiles["AMD003"]
        .attributes["variant_class"]
        == "x3d"
    )

    # X e X3D não devem compartilhar tier.
    assert (
        profiles["AMD003"].tier_key
        != profiles["AMD001"].tier_key
    )

    # ======================================================
    # AMD STANDARD
    # ======================================================

    assert (
        profiles["AMD004"].model
        == "Ryzen 5 5600"
    )

    assert (
        profiles["AMD004"].broad_key
        == "cpu_amd_ryzen_5"
    )

    assert (
        profiles["AMD004"].tier_key
        == (
            "cpu_amd_ryzen_5_"
            "5000_standard"
        )
    )

    assert (
        profiles["AMD004"]
        .attributes["variant_class"]
        == "standard"
    )

    # ======================================================
    # AMD APU
    # ======================================================

    assert (
        profiles["AMD005"].model
        == "Ryzen 5 5600G"
    )

    assert (
        profiles["AMD005"].variant
        == "G"
    )

    assert (
        profiles["AMD005"].tier_key
        == "cpu_amd_ryzen_5_5000_apu"
    )

    assert (
        profiles["AMD005"]
        .attributes["variant_class"]
        == "apu"
    )

    # ======================================================
    # AMD 7000 X3D
    # ======================================================

    assert (
        profiles["AMD006"].tier_key
        == "cpu_amd_ryzen_7_7000_x3d"
    )

    # ======================================================
    # AMD 9000 X
    # ======================================================

    assert (
        profiles["AMD007"].tier_key
        == "cpu_amd_ryzen_9_9000_x"
    )

    # ======================================================
    # AMD R7
    # ======================================================

    assert (
        profiles["AMD008"].strict_key
        == "amd_ryzen_7_5700x"
    )

    # ======================================================
    # AMD 5600GT - CASO REAL
    # ======================================================

    assert (
        profiles["AMD009"].model
        == "Ryzen 5 5600GT"
    )

    assert (
        profiles["AMD009"].variant
        == "GT"
    )

    assert (
        profiles["AMD009"].strict_key
        == "amd_ryzen_5_5600gt"
    )

    assert (
        profiles["AMD009"].tier_key
        == "cpu_amd_ryzen_5_5000_apu"
    )

    # 5600GT e 5600G pertencem
    # à mesma classe comercial.
    assert (
        profiles["AMD009"].tier_key
        == profiles["AMD005"].tier_key
    )

    # Mas 5600 sem iGPU não.
    assert (
        profiles["AMD009"].tier_key
        != profiles["AMD004"].tier_key
    )

    # ======================================================
    # INTEL 10ª STANDARD
    # ======================================================

    assert (
        profiles["INTEL001"].category
        == "cpu"
    )

    assert (
        profiles["INTEL001"].brand
        == "INTEL"
    )

    assert (
        profiles["INTEL001"].model
        == "Core I5-10400"
    )

    assert (
        profiles["INTEL001"].broad_key
        == "cpu_intel_core_i5"
    )

    assert (
        profiles["INTEL001"].tier_key
        == (
            "cpu_intel_core_i5_"
            "gen10_standard"
        )
    )

    assert (
        profiles["INTEL001"].strict_key
        == "intel_core_i5_10400"
    )

    # ======================================================
    # INTEL 11ª STANDARD
    # ======================================================

    assert (
        profiles["INTEL002"].tier_key
        == (
            "cpu_intel_core_i7_"
            "gen11_standard"
        )
    )

    # ======================================================
    # INTEL F
    # ======================================================

    assert (
        profiles["INTEL003"].model
        == "Core I5-12400F"
    )

    assert (
        profiles["INTEL003"].variant
        == "F"
    )

    assert (
        profiles["INTEL003"].tier_key
        == (
            "cpu_intel_core_i5_"
            "gen12_standard_f"
        )
    )

    assert (
        profiles["INTEL003"]
        .attributes["variant_class"]
        == "standard_f"
    )

    # ======================================================
    # INTEL KF
    # ======================================================

    assert (
        profiles["INTEL004"].model
        == "Core I5-13600KF"
    )

    assert (
        profiles["INTEL004"].variant
        == "KF"
    )

    assert (
        profiles["INTEL004"].tier_key
        == (
            "cpu_intel_core_i5_"
            "gen13_performance"
        )
    )

    # ======================================================
    # INTEL K
    # ======================================================

    assert (
        profiles["INTEL005"].tier_key
        == (
            "cpu_intel_core_i7_"
            "gen14_performance"
        )
    )

    # ======================================================
    # INTEL KS
    # ======================================================

    assert (
        profiles["INTEL006"].model
        == "Core I9-14900KS"
    )

    assert (
        profiles["INTEL006"].variant
        == "KS"
    )

    assert (
        profiles["INTEL006"].tier_key
        == (
            "cpu_intel_core_i9_"
            "gen14_performance"
        )
    )

    # ======================================================
    # INTEL 9ª
    # ======================================================

    assert (
        profiles["INTEL007"].tier_key
        == (
            "cpu_intel_core_i9_"
            "gen9_performance"
        )
    )

    # ======================================================
    # INTEL 3ª GERAÇÃO
    # ======================================================

    assert (
        profiles["INTEL008"].tier_key
        == (
            "cpu_intel_core_i5_"
            "gen3_standard"
        )
    )

    assert (
        profiles["INTEL009"].tier_key
        == (
            "cpu_intel_core_i7_"
            "gen3_standard"
        )
    )

    # ======================================================
    # INTEL MÓVEL LEGADO
    # ======================================================

    assert (
        profiles["INTEL010"].model
        == "Core I5-460M"
    )

    assert (
        profiles["INTEL010"].variant
        == "M"
    )

    assert (
        profiles["INTEL010"].strict_key
        == "intel_core_i5_460m"
    )

    assert (
        profiles["INTEL010"].tier_key
        == (
            "cpu_intel_core_i5_"
            "gen1_mobile"
        )
    )

    assert (
        profiles["INTEL010"]
        .attributes["mobile"]
        is True
    )

    # ======================================================
    # PRODUTOS INVÁLIDOS
    # ======================================================

    for product_id in (
        "INVALID001",
        "INVALID002",
        "INVALID003",
        "INVALID004",
        "INVALID005",
        "INVALID006",
    ):
        assert (
            profiles[
                product_id
            ].category
            is None
        )

    print(
        "✓ Ryzen 5700X identificado"
    )

    print(
        "✓ OEM e BOX geraram "
        "a mesma identidade"
    )

    print(
        "✓ X e X3D receberam "
        "tiers diferentes"
    )

    print(
        "✓ Ryzen padrão separado "
        "de APU"
    )

    print(
        "✓ Ryzen G e GT "
        "agrupados como APU"
    )

    print(
        "✓ Ryzen X3D recebeu "
        "tier próprio"
    )

    print(
        "✓ Séries AMD preservadas"
    )

    print(
        "✓ Intel STANDARD separado"
    )

    print(
        "✓ Intel F separado"
    )

    print(
        "✓ Intel K/KF/KS agrupados "
        "como performance"
    )

    print(
        "✓ Intel móvel separado "
        "de desktop"
    )

    print(
        "✓ Intel antigo recebeu geração"
    )

    print(
        "✓ STRICT continua por "
        "modelo exato"
    )

    print(
        "✓ TIER agora considera "
        "classe de variante"
    )

    print(
        "✓ BROAD continua por família"
    )

    print(
        "✓ Caixa vazia bloqueada"
    )

    print(
        "✓ Kit upgrade bloqueado"
    )

    print(
        "✓ Cooler separado bloqueado"
    )

    print(
        "✓ Placa-mãe bloqueada"
    )

    print(
        "✓ Processador de alimentos "
        "bloqueado"
    )

    print(
        "✓ Processador de áudio "
        "bloqueado"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
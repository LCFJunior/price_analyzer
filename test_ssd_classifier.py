from entities.product import Product
from services.product_classifier import ProductClassifier


def create_product(
    product_id: str,
    title: str,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=300.0,
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
        create_product(
            "SSD001",
            (
                "SSD Kingston NV3 1TB "
                "NVMe M.2 PCIe 4.0"
            ),
        ),

        create_product(
            "SSD002",
            (
                "SSD Kingston NV3 2TB "
                "NVMe PCIe 4.0"
            ),
        ),

        create_product(
            "SSD003",
            (
                "SSD WD Black SN850X "
                "1TB NVMe M2"
            ),
        ),

        create_product(
            "SSD004",
            (
                "SSD Samsung 990 Pro "
                "2TB NVMe PCIe 4.0"
            ),
        ),

        create_product(
            "SSD005",
            (
                "SSD Crucial P3 Plus "
                "1TB NVMe M.2"
            ),
        ),

        create_product(
            "SSD006",
            (
                "SSD Kingston A400 "
                "480GB SATA"
            ),
        ),

        create_product(
            "SSD007",
            (
                "SSD Lexar NM790 "
                "1TB PCIe Gen4 NVMe"
            ),
        ),

        create_product(
            "SSD008",
            (
                "SSD ADATA Legend 800 "
                "1TB NVMe"
            ),
        ),

        create_product(
            "SSD009",
            (
                "Unidade SSD NVMe "
                "Kingston 1TB NV3 "
                "M2 2280"
            ),
        ),

        create_product(
            "OTHER001",
            (
                "Case Externo USB "
                "para SSD NVMe"
            ),
        ),

        # ==================================================
        # CASOS REAIS DO MERCADO LIVRE
        # ==================================================

        create_product(
            "REAL001",
            (
                "Bh 1tb M.2 Sata Ssd "
                "Armazenamento De "
                "Alta Velocidade"
            ),
        ),

        create_product(
            "REAL002",
            (
                "interno Crucial "
                "CT1000P2SSD8 1TB"
            ),
        ),

        create_product(
            "REAL003",
            (
                "Disco Sólido Interno "
                "Ssd Plus "
                "Sa400s37480g "
                "Kingston Cinza-escuro"
            ),
        ),

        create_product(
            "REAL004",
            (
                "SSD Externo Portátil "
                "1TB Interface USB 3.2 "
                "SanDisk SDSSDE30-1T00 "
                "Velocidade de Leitura "
                "Até 800MB/s Preto"
            ),
        ),

        create_product(
            "REAL005",
            (
                "SSD Samsung 9100 Pro "
                "1TB NVMe Gen5 X4"
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
            f"Título: "
            f"{product.title}"
        )

        print(
            f"Categoria: "
            f"{profile.category}"
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
    # KINGSTON NV3
    # ======================================================

    assert (
        profiles["SSD001"].model
        == "NV3"
    )

    assert (
        profiles["SSD001"].broad_key
        == "ssd_interno_nvme_1tb"
    )

    assert (
        profiles["SSD001"].tier_key
        == "ssd_interno_nvme_gen4_1tb"
    )

    assert (
        profiles["SSD001"].strict_key
        == "kingston_nv3_1tb_nvme"
    )

    assert (
        profiles["SSD001"]
        .attributes["external"]
        is False
    )

    assert (
        profiles["SSD001"]
        .attributes["form_factor"]
        == "m2"
    )

    # ======================================================
    # CAPACIDADE DIFERENTE
    # ======================================================

    assert (
        profiles["SSD002"].strict_key
        == "kingston_nv3_2tb_nvme"
    )

    assert (
        profiles["SSD002"].broad_key
        == "ssd_interno_nvme_2tb"
    )

    # ======================================================
    # WD SN850X
    # ======================================================

    assert (
        profiles["SSD003"].model
        == "SN850X"
    )

    assert (
        profiles["SSD003"].tier_key
        == "ssd_interno_nvme_gen4_1tb"
    )

    # ======================================================
    # SAMSUNG 990 PRO
    # ======================================================

    assert (
        profiles["SSD004"].model
        == "990 PRO"
    )

    assert (
        profiles["SSD004"].tier_key
        == "ssd_interno_nvme_gen4_2tb"
    )

    # ======================================================
    # CRUCIAL P3 PLUS
    # ======================================================

    assert (
        profiles["SSD005"].model
        == "P3 PLUS"
    )

    assert (
        profiles["SSD005"].tier_key
        == "ssd_interno_nvme_gen4_1tb"
    )

    # ======================================================
    # KINGSTON A400
    # ======================================================

    assert (
        profiles["SSD006"].model
        == "A400"
    )

    assert (
        profiles["SSD006"].broad_key
        == "ssd_interno_sata_480gb"
    )

    assert (
        profiles["SSD006"].tier_key
        == "ssd_interno_sata_480gb"
    )

    assert (
        profiles["SSD006"].strict_key
        == "kingston_a400_480gb_sata"
    )

    assert (
        profiles["SSD006"]
        .attributes["form_factor"]
        == "2.5"
    )

    # ======================================================
    # LEXAR NM790
    # ======================================================

    assert (
        profiles["SSD007"].model
        == "NM790"
    )

    assert (
        profiles["SSD007"].tier_key
        == "ssd_interno_nvme_gen4_1tb"
    )

    # ======================================================
    # ADATA LEGEND 800
    # ======================================================

    assert (
        profiles["SSD008"].model
        == "LEGEND 800"
    )

    assert (
        profiles["SSD008"].broad_key
        == "ssd_interno_nvme_1tb"
    )

    # Como ainda não temos a geração conhecida,
    # tier pode permanecer None.
    assert (
        profiles["SSD008"].tier_key
        is None
    )

    # ======================================================
    # MESMO NV3 COM TÍTULO DIFERENTE
    # ======================================================

    assert (
        profiles["SSD009"].strict_key
        == profiles["SSD001"].strict_key
    )

    assert (
        profiles["SSD009"].tier_key
        == profiles["SSD001"].tier_key
    )

    # ======================================================
    # CASE NÃO É SSD
    # ======================================================

    assert (
        profiles["OTHER001"].category
        is None
    )

    # ======================================================
    # BH M.2 SATA
    # ======================================================

    assert (
        profiles["REAL001"]
        .attributes["interface"]
        == "sata"
    )

    assert (
        profiles["REAL001"].broad_key
        == "ssd_interno_sata_1tb"
    )

    assert (
        profiles["REAL001"].tier_key
        == "ssd_interno_sata_1tb"
    )

    # Produto genérico não deve receber
    # identidade comercial inventada.
    assert (
        profiles["REAL001"].strict_key
        is None
    )

    assert (
        profiles["REAL001"]
        .attributes[
            "identity_confidence"
        ]
        == "muito_baixa"
    )

    # ======================================================
    # CRUCIAL CT1000P2SSD8
    # ======================================================

    assert (
        profiles["REAL002"].category
        == "ssd"
    )

    assert (
        profiles["REAL002"].brand
        == "CRUCIAL"
    )

    assert (
        profiles["REAL002"].model
        == "CT1000P2SSD8"
    )

    assert (
        profiles["REAL002"].broad_key
        == (
            "ssd_interno_"
            "interface_desconhecida_1tb"
        )
    )

    # ======================================================
    # A400 POR SKU
    # ======================================================

    assert (
        profiles["REAL003"].category
        == "ssd"
    )

    assert (
        profiles["REAL003"].brand
        == "KINGSTON"
    )

    assert (
        profiles["REAL003"].model
        == "A400"
    )

    assert (
        profiles["REAL003"].strict_key
        == "kingston_a400_480gb_sata"
    )

    assert (
        profiles["REAL003"].broad_key
        == "ssd_interno_sata_480gb"
    )

    assert (
        profiles["REAL003"]
        .attributes["interface"]
        == "sata"
    )

    # ======================================================
    # SSD EXTERNO SANDISK
    # ======================================================

    assert (
        profiles["REAL004"].category
        == "ssd"
    )

    assert (
        profiles["REAL004"].brand
        == "SANDISK"
    )

    assert (
        profiles["REAL004"].model
        == "SDSSDE30"
    )

    assert (
        profiles["REAL004"]
        .attributes["external"]
        is True
    )

    assert (
        profiles["REAL004"]
        .attributes["interface"]
        == "usb"
    )

    assert (
        profiles["REAL004"].broad_key
        == "ssd_externo_usb_1tb"
    )

    assert (
        profiles["REAL004"].tier_key
        == "ssd_externo_usb_1tb"
    )

    assert (
        profiles["REAL004"].strict_key
        == (
            "sandisk_sdssde30_"
            "1tb_externo_usb"
        )
    )

    # ======================================================
    # SAMSUNG 9100 PRO
    # ======================================================

    assert (
        profiles["REAL005"].model
        == "9100 PRO"
    )

    assert (
        profiles["REAL005"]
        .attributes["pcie_generation"]
        == "5.0"
    )

    assert (
        profiles["REAL005"].tier_key
        == "ssd_interno_nvme_gen5_1tb"
    )

    assert (
        profiles["REAL005"].strict_key
        == "samsung_9100_pro_1tb_nvme"
    )

    print(
        "✓ SSDs internos separados "
        "de SSDs externos"
    )

    print(
        "✓ Modelos conhecidos "
        "receberam especificações"
    )

    print(
        "✓ NV3 recebeu NVMe Gen4"
    )

    print(
        "✓ SN850X recebeu NVMe Gen4"
    )

    print(
        "✓ Samsung 990 PRO "
        "recebeu NVMe Gen4"
    )

    print(
        "✓ Samsung 9100 PRO "
        "recebeu NVMe Gen5"
    )

    print(
        "✓ A400 recebeu SATA"
    )

    print(
        "✓ A400 por SKU foi normalizado"
    )

    print(
        "✓ Capacidades continuam separadas"
    )

    print(
        "✓ M.2 SATA continua sendo SATA"
    )

    print(
        "✓ SSD externo USB ganhou "
        "mercado próprio"
    )

    print(
        "✓ Produto genérico não recebeu "
        "identidade falsa"
    )

    print(
        "✓ Case de SSD continua "
        "não classificado"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
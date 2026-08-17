from dataclasses import dataclass


@dataclass(frozen=True)
class SSDSpecification:
    interface: str | None = None
    pcie_generation: str | None = None
    form_factor: str | None = None
    external: bool = False


class SSDSpecifications:
    """
    Pequena base de especificações confiáveis.

    Esta classe NÃO identifica SSDs.

    Ela apenas complementa informações quando o
    SSDClassifier já reconheceu com segurança:

        marca + modelo

    Exemplos:

        KINGSTON + A400
            -> SATA

        KINGSTON + NV3
            -> NVMe Gen4

        SAMSUNG + 9100 PRO
            -> NVMe Gen5
    """

    SPECS: dict[
        tuple[str, str],
        SSDSpecification,
    ] = {
        (
            "KINGSTON",
            "A400",
        ): SSDSpecification(
            interface="sata",
            form_factor="2.5",
        ),

        (
            "KINGSTON",
            "NV3",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="4.0",
            form_factor="m2",
        ),

        (
            "CRUCIAL",
            "BX500",
        ): SSDSpecification(
            interface="sata",
            form_factor="2.5",
        ),

        (
            "CRUCIAL",
            "P3 PLUS",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="4.0",
            form_factor="m2",
        ),

        (
            "SAMSUNG",
            "990 PRO",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="4.0",
            form_factor="m2",
        ),

        (
            "SAMSUNG",
            "9100 PRO",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="5.0",
            form_factor="m2",
        ),

        (
            "WD",
            "SN850X",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="4.0",
            form_factor="m2",
        ),

        (
            "WESTERN DIGITAL",
            "SN8100",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="5.0",
            form_factor="m2",
        ),

        (
            "WD",
            "SN8100",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="5.0",
            form_factor="m2",
        ),

        (
            "LEXAR",
            "NM790",
        ): SSDSpecification(
            interface="nvme",
            pcie_generation="4.0",
            form_factor="m2",
        ),

        (
            "SANDISK",
            "SDSSDE30",
        ): SSDSpecification(
            interface="usb",
            external=True,
        ),
    }

    @classmethod
    def get(
        cls,
        *,
        brand: str | None,
        model: str | None,
    ) -> SSDSpecification | None:
        if (
            brand is None
            or model is None
        ):
            return None

        return cls.SPECS.get(
            (
                brand,
                model,
            )
        )
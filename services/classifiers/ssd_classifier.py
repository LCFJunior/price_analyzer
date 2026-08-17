import re

from entities.product import Product
from entities.product_profile import ProductProfile

from services.classifiers.ssd_specs import (
    SSDSpecifications,
)
from services.classifiers.text_utils import (
    ClassifierTextUtils,
)


class SSDClassifier:
    """
    Classificador de SSDs.

    Responsabilidades:

    - identificar marca;
    - identificar modelo;
    - identificar capacidade;
    - identificar interface;
    - identificar geração PCIe;
    - identificar SSD interno ou externo;
    - complementar especificações conhecidas;
    - criar broad_key;
    - criar tier_key;
    - criar strict_key;
    - estimar confiança da identidade.

    O comportamento é propositalmente conservador.

    Se não conseguimos identificar a capacidade,
    o produto não é classificado como SSD para
    comparação de preços.
    """

    KNOWN_BRANDS = (
        (
            "western digital",
            "WESTERN DIGITAL",
        ),
        (
            "wd black",
            "WD",
        ),
        (
            "wd green",
            "WD",
        ),
        (
            "wd blue",
            "WD",
        ),
        (
            "kingston",
            "KINGSTON",
        ),
        (
            "samsung",
            "SAMSUNG",
        ),
        (
            "crucial",
            "CRUCIAL",
        ),
        (
            "sandisk",
            "SANDISK",
        ),
        (
            "adata",
            "ADATA",
        ),
        (
            "xpg",
            "XPG",
        ),
        (
            "lexar",
            "LEXAR",
        ),
        (
            "corsair",
            "CORSAIR",
        ),
        (
            "seagate",
            "SEAGATE",
        ),
        (
            "teamgroup",
            "TEAMGROUP",
        ),
        (
            "team group",
            "TEAMGROUP",
        ),
        (
            "pny",
            "PNY",
        ),
        (
            "patriot",
            "PATRIOT",
        ),
        (
            "netac",
            "NETAC",
        ),
        (
            "hiksemi",
            "HIKSEMI",
        ),
        (
            "hikvision",
            "HIKVISION",
        ),
        (
            "kingspec",
            "KINGSPEC",
        ),
        (
            "mancer",
            "MANCER",
        ),
        (
            "rise mode",
            "RISE MODE",
        ),
        (
            "goldenfir",
            "GOLDENFIR",
        ),
        (
            "umemory",
            "UMEMORY",
        ),
    )

    BRAND_TERMS_TO_REMOVE = tuple(
        item[0]
        for item in KNOWN_BRANDS
    )

    GENERIC_WORDS = {
        "ssd",
        "disco",
        "estado",
        "solido",
        "interno",
        "externo",
        "armazenamento",
        "drive",
        "unidade",
        "para",
        "desktop",
        "notebook",
        "computador",
        "pc",
        "novo",
        "nova",
        "original",
        "gamer",
        "alta",
        "velocidade",
        "modelo",
        "cor",
        "negro",
        "preto",
        "cinza",
        "escuro",
        "rapido",
        "desempenho",
        "jogos",
        "facil",
        "instalacao",
        "edicao",
        "video",
        "portatil",
        "portable",
    }

    INTERFACE_WORDS = {
        "nvme",
        "sata",
        "sata2",
        "sata3",
        "pcie",
        "pci",
        "express",
        "usb",
        "usb3",
    }

    MODEL_SUFFIXES = {
        "pro",
        "plus",
        "evo",
        "qvo",
        "max",
        "elite",
        "premium",
        "ultra",
    }

    CAPACITY_PATTERN = re.compile(
        r"\b"
        r"(\d+(?:[\.,]\d+)?)"
        r"\s*"
        r"(tb|gb)"
        r"\b"
    )

    KINGSTON_A400_CAPACITY_PATTERN = (
        re.compile(
            r"\b"
            r"sa400s37"
            r"(?:[/\-\s]?)"
            r"(\d{3,4})"
            r"g"
            r"\b"
        )
    )

    PCIE_PATTERN = re.compile(
        r"\b"
        r"(?:pcie|pci\s*e|pci express)"
        r"\s*"
        r"(?:gen\s*)?"
        r"([345])"
        r"(?:[\.,]0)?"
        r"\b"
    )

    ALPHA_NUMERIC_PATTERN = re.compile(
        r"^(?=.*[a-z])(?=.*\d)"
        r"[a-z0-9\-]+$"
    )

    def can_classify(
        self,
        product: Product,
    ) -> bool:
        normalized_title = (
            ClassifierTextUtils.normalize(
                product.title
            )
        )

        capacity = (
            self._extract_capacity(
                normalized_title
            )
        )

        # Sem capacidade, não há comparação segura.
        if capacity is None:
            return False

        if re.search(
            r"\bssd\b",
            normalized_title,
        ):
            return True

        brand = self._extract_brand(
            normalized_title
        )

        if (
            brand is not None
            and re.search(
                r"\b"
                r"[a-z0-9\-]*"
                r"ssd"
                r"[a-z0-9\-]*"
                r"\b",
                normalized_title,
            )
        ):
            return True

        return False

    def classify(
        self,
        product: Product,
    ) -> ProductProfile:
        normalized_title = (
            ClassifierTextUtils.normalize(
                product.title
            )
        )

        brand = self._extract_brand(
            normalized_title
        )

        capacity_data = (
            self._extract_capacity(
                normalized_title
            )
        )

        capacity_gb = None
        capacity_label = None

        if capacity_data is not None:
            (
                capacity_gb,
                capacity_label,
            ) = capacity_data

        # ======================================================
        # EXTRAÇÃO DIRETA DO TÍTULO
        # ======================================================

        interface = (
            self._extract_interface(
                normalized_title
            )
        )

        pcie_generation = (
            self._extract_pcie_generation(
                normalized_title
            )
        )

        model = self._extract_model(
            normalized_title=(
                normalized_title
            ),
            brand=brand,
        )

        external = self._is_external(
            normalized_title
        )

        # ======================================================
        # ESPECIFICAÇÕES CONHECIDAS
        #
        # Só complementa dados que não vieram no título.
        # ======================================================

        known_specification = (
            SSDSpecifications.get(
                brand=brand,
                model=model,
            )
        )

        if (
            known_specification
            is not None
        ):
            if interface is None:
                interface = (
                    known_specification
                    .interface
                )

            if pcie_generation is None:
                pcie_generation = (
                    known_specification
                    .pcie_generation
                )

            if (
                known_specification
                .external
            ):
                external = True

        # ======================================================
        # CHAVES
        # ======================================================

        broad_key = (
            self._build_broad_key(
                interface=interface,
                capacity_label=(
                    capacity_label
                ),
                external=external,
            )
        )

        tier_key = (
            self._build_tier_key(
                interface=interface,
                pcie_generation=(
                    pcie_generation
                ),
                capacity_label=(
                    capacity_label
                ),
                external=external,
            )
        )

        strict_key = (
            self._build_strict_key(
                brand=brand,
                model=model,
                capacity_label=(
                    capacity_label
                ),
                interface=interface,
                external=external,
            )
        )

        identity_confidence = (
            self._get_identity_confidence(
                brand=brand,
                model=model,
                interface=interface,
            )
        )

        form_factor = None

        if (
            known_specification
            is not None
        ):
            form_factor = (
                known_specification
                .form_factor
            )

        return ProductProfile(
            product_id=product.id,
            brand=brand,
            model=model,
            memory_gb=None,
            variant=None,
            broad_key=broad_key,
            tier_key=tier_key,
            strict_key=strict_key,
            category="ssd",
            attributes={
                "capacity_gb": (
                    capacity_gb
                ),
                "capacity_label": (
                    capacity_label
                ),
                "interface": interface,
                "pcie_generation": (
                    pcie_generation
                ),
                "external": external,
                "form_factor": (
                    form_factor
                ),
                "identity_confidence": (
                    identity_confidence
                ),
            },
        )

    # ==========================================================
    # MARCA
    # ==========================================================

    def _extract_brand(
        self,
        normalized_title: str,
    ) -> str | None:
        for (
            search_term,
            normalized_brand,
        ) in self.KNOWN_BRANDS:
            if re.search(
                rf"\b"
                rf"{re.escape(search_term)}"
                rf"\b",
                normalized_title,
            ):
                return (
                    normalized_brand
                )

        return None

    # ==========================================================
    # CAPACIDADE
    # ==========================================================

    def _extract_capacity(
        self,
        normalized_title: str,
    ) -> tuple[
        int,
        str,
    ] | None:
        match = (
            self.CAPACITY_PATTERN.search(
                normalized_title
            )
        )

        if match is not None:
            raw_value = (
                match.group(1)
                .replace(
                    ",",
                    ".",
                )
            )

            unit = (
                match.group(2)
            )

            try:
                numeric_value = float(
                    raw_value
                )
            except ValueError:
                numeric_value = 0

            if numeric_value > 0:
                if unit == "tb":
                    capacity_gb = int(
                        numeric_value
                        * 1000
                    )

                    if (
                        numeric_value
                        .is_integer()
                    ):
                        capacity_label = (
                            f"{int(numeric_value)}tb"
                        )
                    else:
                        capacity_label = (
                            str(
                                numeric_value
                            )
                            .replace(
                                ".",
                                "_",
                            )
                            + "tb"
                        )

                else:
                    capacity_gb = int(
                        numeric_value
                    )

                    capacity_label = (
                        f"{capacity_gb}gb"
                    )

                if (
                    64
                    <= capacity_gb
                    <= 16000
                ):
                    return (
                        capacity_gb,
                        capacity_label,
                    )

        # Kingston A400 via SKU.
        a400_match = (
            self.KINGSTON_A400_CAPACITY_PATTERN
            .search(
                normalized_title
            )
        )

        if a400_match is not None:
            try:
                capacity_gb = int(
                    a400_match.group(1)
                )
            except ValueError:
                return None

            if (
                64
                <= capacity_gb
                <= 4000
            ):
                return (
                    capacity_gb,
                    f"{capacity_gb}gb",
                )

        return None

    # ==========================================================
    # INTERFACE
    # ==========================================================

    @staticmethod
    def _extract_interface(
        normalized_title: str,
    ) -> str | None:
        sata_patterns = (
            r"\bsata\b",
            r"\bsata\s*ii\b",
            r"\bsata\s*iii\b",
            r"\bsata\s*2\b",
            r"\bsata\s*3\b",
            r"\bsata2\b",
            r"\bsata3\b",
        )

        for pattern in (
            sata_patterns
        ):
            if re.search(
                pattern,
                normalized_title,
            ):
                return "sata"

        if re.search(
            r"\bnvme\b",
            normalized_title,
        ):
            return "nvme"

        if re.search(
            r"\bpcie\b",
            normalized_title,
        ):
            return "nvme"

        if re.search(
            r"\bpci\s*e\b",
            normalized_title,
        ):
            return "nvme"

        if re.search(
            r"\bpci express\b",
            normalized_title,
        ):
            return "nvme"

        # SSD externo USB.
        usb_patterns = (
            r"\busb\b",
            r"\busb\s*3(?:\.\d)?\b",
            r"\busb3\b",
            r"\busb-c\b",
            r"\btype c\b",
        )

        for pattern in (
            usb_patterns
        ):
            if re.search(
                pattern,
                normalized_title,
            ):
                return "usb"

        return None

    # ==========================================================
    # EXTERNO / INTERNO
    # ==========================================================

    @staticmethod
    def _is_external(
        normalized_title: str,
    ) -> bool:
        external_patterns = (
            r"\bssd externo\b",
            r"\bexterno portatil\b",
            r"\bexterno portátil\b",
            r"\bportatil\b",
            r"\bportable\b",
            r"\busb 3\b",
            r"\busb3\b",
            r"\busb-c\b",
            r"\btype c\b",
        )

        for pattern in (
            external_patterns
        ):
            if re.search(
                pattern,
                normalized_title,
            ):
                return True

        return False

    # ==========================================================
    # GERAÇÃO PCIe
    # ==========================================================

    def _extract_pcie_generation(
        self,
        normalized_title: str,
    ) -> str | None:
        if re.search(
            r"\b"
            r"(?:pcie\s*)?"
            r"gen\s*5"
            r"(?:x4)?"
            r"\b",
            normalized_title,
        ):
            return "5.0"

        if re.search(
            r"\b"
            r"(?:pcie\s*)?"
            r"gen\s*4"
            r"(?:x4)?"
            r"\b",
            normalized_title,
        ):
            return "4.0"

        if re.search(
            r"\b"
            r"(?:pcie\s*)?"
            r"gen\s*3"
            r"(?:x4)?"
            r"\b",
            normalized_title,
        ):
            return "3.0"

        match = (
            self.PCIE_PATTERN.search(
                normalized_title
            )
        )

        if match is not None:
            return (
                f"{match.group(1)}.0"
            )

        return None

    # ==========================================================
    # MODELO
    # ==========================================================

    def _extract_model(
        self,
        *,
        normalized_title: str,
        brand: str | None,
    ) -> str | None:
        known_model = (
            self._extract_known_model(
                normalized_title
            )
        )

        if known_model is not None:
            return known_model

        model_patterns = (
            (
                r"\b"
                r"(\d{3,4})"
                r"\s+"
                r"(pro|evo|qvo)"
                r"\b"
            ),
            (
                r"\b"
                r"([a-z]\d+)"
                r"\s+"
                r"(plus|pro|max)"
                r"\b"
            ),
            (
                r"\b"
                r"(legend)"
                r"\s+"
                r"(\d{3,4})"
                r"\b"
            ),
        )

        for pattern in (
            model_patterns
        ):
            match = re.search(
                pattern,
                normalized_title,
            )

            if match:
                return (
                    " ".join(
                        match.groups()
                    )
                    .upper()
                )

        embedded_model_match = (
            re.search(
                r"\b"
                r"([a-z0-9\-]*"
                r"ssd"
                r"[a-z0-9\-]*)"
                r"\b",
                normalized_title,
            )
        )

        if embedded_model_match:
            embedded_model = (
                embedded_model_match
                .group(1)
            )

            if (
                embedded_model
                != "ssd"
            ):
                return (
                    embedded_model.upper()
                )

        working_title = (
            normalized_title
        )

        for brand_term in (
            self.BRAND_TERMS_TO_REMOVE
        ):
            working_title = re.sub(
                rf"\b"
                rf"{re.escape(brand_term)}"
                rf"\b",
                " ",
                working_title,
            )

        working_title = (
            self.CAPACITY_PATTERN.sub(
                " ",
                working_title,
            )
        )

        working_title = (
            self.KINGSTON_A400_CAPACITY_PATTERN
            .sub(
                " ",
                working_title,
            )
        )

        working_title = re.sub(
            r"\bssd\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bm[\s\-\.]?2\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bpcie\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bpci\s*e\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bpci express\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bsata\s*(?:ii|iii|2|3)?\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bsata[23]\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bnvme\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\busb(?:\s*3(?:\.\d)?)?\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\busb-c\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\btype c\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bgen\s*[345](?:x4)?\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\b[345](?:[\.,]0)?x4\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\bx4\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\b\d+\s*"
            r"(?:mbs|mbps|gbs|gbps)"
            r"\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\b\d+/\d+\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\b"
            r"22(?:30|42|60|80)"
            r"\b",
            " ",
            working_title,
        )

        working_title = re.sub(
            r"\s+",
            " ",
            working_title,
        ).strip()

        valid_tokens: list[
            str
        ] = []

        for token in (
            working_title.split()
        ):
            token = token.strip(
                "-_"
            )

            if not token:
                continue

            if (
                token
                in self.GENERIC_WORDS
            ):
                continue

            if (
                token
                in self.INTERFACE_WORDS
            ):
                continue

            if re.fullmatch(
                r"22(?:30|42|60|80)",
                token,
            ):
                continue

            if re.fullmatch(
                r"gen[345]x4",
                token,
            ):
                continue

            if re.fullmatch(
                r"[345](?:0)?x4",
                token,
            ):
                continue

            if re.fullmatch(
                r"x\d+",
                token,
            ):
                continue

            if re.fullmatch(
                r"\d+"
                r"(?:mbs|mbps|gbs|gbps)",
                token,
            ):
                continue

            if self._is_technical_token(
                token
            ):
                continue

            valid_tokens.append(
                token
            )

        for index, token in enumerate(
            valid_tokens
        ):
            if not (
                self.ALPHA_NUMERIC_PATTERN
                .match(
                    token
                )
            ):
                continue

            model_parts = [
                token
            ]

            next_index = (
                index + 1
            )

            if (
                next_index
                < len(
                    valid_tokens
                )
            ):
                next_token = (
                    valid_tokens[
                        next_index
                    ]
                )

                if (
                    next_token
                    in self.MODEL_SUFFIXES
                ):
                    model_parts.append(
                        next_token
                    )

            return (
                " ".join(
                    model_parts
                )
                .upper()
            )

        return None

    # ==========================================================
    # MODELOS CONHECIDOS
    # ==========================================================

    @staticmethod
    def _extract_known_model(
        normalized_title: str,
    ) -> str | None:
        if re.search(
            r"\ba400\b",
            normalized_title,
        ):
            return "A400"

        if re.search(
            r"\b"
            r"sa400s37"
            r"(?:[/\-\s]?"
            r"\d{3,4}g)?"
            r"\b",
            normalized_title,
        ):
            return "A400"

        if re.search(
            r"\bnv3\b",
            normalized_title,
        ):
            return "NV3"

        if re.search(
            r"\bbx500\b",
            normalized_title,
        ):
            return "BX500"

        if re.search(
            r"\bp3\s+plus\b",
            normalized_title,
        ):
            return "P3 PLUS"

        if re.search(
            r"\bsn850x\b",
            normalized_title,
        ):
            return "SN850X"

        if re.search(
            r"\bsn8100\b",
            normalized_title,
        ):
            return "SN8100"

        if re.search(
            r"\bnm790\b",
            normalized_title,
        ):
            return "NM790"

        return None

    # ==========================================================
    # TOKENS TÉCNICOS
    # ==========================================================

    @staticmethod
    def _is_technical_token(
        token: str,
    ) -> bool:
        patterns = (
            r"x\d+",
            r"gen[345]x\d+",
            r"sata[23]",
            r"[345]x\d+",
            r"[345]0x\d+",
            r"usb\d+",
        )

        for pattern in (
            patterns
        ):
            if re.fullmatch(
                pattern,
                token,
            ):
                return True

        return False

    # ==========================================================
    # CONFIANÇA
    # ==========================================================

    @staticmethod
    def _get_identity_confidence(
        *,
        brand: str | None,
        model: str | None,
        interface: str | None,
    ) -> str:
        if (
            brand is not None
            and model is not None
            and interface is not None
        ):
            return "alta"

        if (
            brand is not None
            and model is not None
        ):
            return "media"

        if brand is not None:
            return "baixa"

        return "muito_baixa"

    # ==========================================================
    # BROAD KEY
    # ==========================================================

    @staticmethod
    def _build_broad_key(
        *,
        interface: str | None,
        capacity_label: str | None,
        external: bool,
    ) -> str | None:
        if capacity_label is None:
            return None

        parts = [
            "ssd",
        ]

        if external:
            parts.append(
                "externo"
            )
        else:
            parts.append(
                "interno"
            )

        if interface is not None:
            parts.append(
                interface
            )
        else:
            parts.append(
                "interface_desconhecida"
            )

        parts.append(
            capacity_label
        )

        return "_".join(
            parts
        )

    # ==========================================================
    # TIER KEY
    # ==========================================================

    @staticmethod
    def _build_tier_key(
        *,
        interface: str | None,
        pcie_generation: str | None,
        capacity_label: str | None,
        external: bool,
    ) -> str | None:
        if (
            capacity_label is None
            or interface is None
        ):
            return None

        prefix = (
            "ssd_externo"
            if external
            else "ssd_interno"
        )

        if interface == "nvme":
            if (
                pcie_generation
                is None
            ):
                return None

            generation_number = (
                pcie_generation
                .split(".")[0]
            )

            return (
                f"{prefix}_"
                f"nvme_"
                f"gen{generation_number}_"
                f"{capacity_label}"
            )

        if interface == "sata":
            return (
                f"{prefix}_"
                f"sata_"
                f"{capacity_label}"
            )

        if interface == "usb":
            return (
                f"{prefix}_"
                f"usb_"
                f"{capacity_label}"
            )

        return None

    # ==========================================================
    # STRICT KEY
    # ==========================================================

    @staticmethod
    def _build_strict_key(
        *,
        brand: str | None,
        model: str | None,
        capacity_label: str | None,
        interface: str | None,
        external: bool,
    ) -> str | None:
        if (
            brand is None
            or model is None
            or capacity_label is None
        ):
            return None

        parts = [
            ClassifierTextUtils.slug(
                brand
            ),

            ClassifierTextUtils.slug(
                model
            ),

            capacity_label,
        ]

        if external:
            parts.append(
                "externo"
            )

        if interface is not None:
            parts.append(
                interface
            )

        return "_".join(
            parts
        )
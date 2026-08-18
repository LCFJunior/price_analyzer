import re

from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)
from services.classifiers.text_utils import (
    ClassifierTextUtils,
)


class GPUClassifier:
    """
    Classificador de placas de vídeo.

    Hierarquia de comparação:

        STRICT
        fabricante + GPU + variante + VRAM

            ↓

        TIER
        GPU + VRAM

            ↓

        BROAD
        fabricante do chip
        + geração
        + segmento
        + classe
        + VRAM

    Exemplos:

        MSI RTX 5060 Ventus 2X 8GB

        STRICT:
        msi_rtx_5060_ventus_2x_8gb

        TIER:
        gpu_nvidia_rtx_5060_8gb

        BROAD:
        gpu_nvidia_50_60_standard_8gb

    Regras importantes:

    - NVIDIA/AMD representam o fabricante do chip;
    - MSI/ASUS/Gigabyte/etc. representam a marca da placa;
    - BROAD exige VRAM conhecida;
    - STRICT exige marca + modelo + VRAM + variante;
    - acessórios, notebooks e PCs completos são bloqueados.
    """

    # ==========================================================
    # MARCAS / FABRICANTES DA PLACA
    # ==========================================================

    KNOWN_BRANDS = (
        ("powercolor", "POWERCOLOR"),
        ("gainward", "GAINWARD"),
        ("colorful", "COLORFUL"),
        ("sapphire", "SAPPHIRE"),
        ("gigabyte", "GIGABYTE"),
        ("inno3d", "INNO3D"),
        ("revenger", "REVENGER"),
        ("peladn", "PELADN"),
        ("pcyes", "PCYES"),
        ("clanm", "CLANM"),
        ("arvex", "ARVEX"),
        ("vinik", "VINIK"),
        ("vxpro", "VXPRO"),
        ("asrock", "ASROCK"),
        ("zotac", "ZOTAC"),
        ("galax", "GALAX"),
        ("palit", "PALIT"),
        ("soyo", "SOYO"),
        ("maxsun", "MAXSUN"),
        ("mllse", "MLLSE"),
        ("51risc", "51RISC"),
        ("veineda", "VEINEDA"),
        ("yeston", "YESTON"),
        ("asus", "ASUS"),
        ("msi", "MSI"),
        ("pny", "PNY"),
        ("xfx", "XFX"),
    )

    # ==========================================================
    # VARIANTES / LINHAS
    #
    # Específicas primeiro.
    # ==========================================================

    KNOWN_VARIANTS = (
        # MSI
        "ventus 3x",
        "ventus 2x",
        "shadow 3x",
        "shadow 2x",
        "gaming trio",
        "gaming x trio",
        "gaming x",
        "suprim x",
        "suprim",

        # ASUS
        "rog strix",
        "tuf gaming",
        "prime oc",
        "dual oc",
        "dual evo",
        "proart",

        # Gigabyte
        "aorus master",
        "aorus elite",
        "gaming oc",
        "eagle oc",
        "windforce",

        # Zotac
        "amp extreme",
        "twin edge",
        "solid oc",
        "trinity",

        # Galax
        "1 click oc",
        "ex gamer",

        # Gainward
        "phoenix gs",
        "phoenix",
        "pegasus",

        # Palit
        "stormx",

        # Inno3D
        "ichill",
        "twin x2",

        # AMD AIB
        "red devil",
        "hellhound",
        "nitro plus",
        "nitro+",
        "pulse",
        "merc 319",
        "merc 310",
        "qick 319",
        "qick",
        "speedster",
        "fighter",
        "steel legend",
        "challenger",

        # PCYes / outros
        "projeto edge",
        "black edition",

        # Fallbacks comerciais
        "triple fan",
        "dual fan",
        "dual-fan",

        # Variantes curtas.
        # Devem vir DEPOIS das específicas.
        "shadow",
        "dual",
    )

    # ==========================================================
    # NVIDIA RTX
    #
    # Regexes toleram:
    #
    # RTX 5070 Ti
    # RTX5070Ti
    # RTX-5070-Ti
    # RTX 5070Ti
    # ==========================================================

    NVIDIA_RTX_PATTERNS = (
        (
            r"\brtx[\s-]*5090\b",
            "RTX 5090",
        ),
        (
            r"\brtx[\s-]*5080\b",
            "RTX 5080",
        ),

        (
            r"\brtx[\s-]*5070[\s-]*ti\b",
            "RTX 5070 Ti",
        ),
        (
            r"\brtx[\s-]*5070\b",
            "RTX 5070",
        ),

        (
            r"\brtx[\s-]*5060[\s-]*ti\b",
            "RTX 5060 Ti",
        ),
        (
            r"\brtx[\s-]*5060\b",
            "RTX 5060",
        ),

        # RTX 40
        (
            r"\brtx[\s-]*4090\b",
            "RTX 4090",
        ),

        (
            r"\brtx[\s-]*4080[\s-]*super\b",
            "RTX 4080 Super",
        ),
        (
            r"\brtx[\s-]*4080\b",
            "RTX 4080",
        ),

        (
            r"\brtx[\s-]*4070[\s-]*ti[\s-]*super\b",
            "RTX 4070 Ti Super",
        ),
        (
            r"\brtx[\s-]*4070[\s-]*ti\b",
            "RTX 4070 Ti",
        ),
        (
            r"\brtx[\s-]*4070[\s-]*super\b",
            "RTX 4070 Super",
        ),
        (
            r"\brtx[\s-]*4070\b",
            "RTX 4070",
        ),

        (
            r"\brtx[\s-]*4060[\s-]*ti\b",
            "RTX 4060 Ti",
        ),
        (
            r"\brtx[\s-]*4060\b",
            "RTX 4060",
        ),

        # RTX 30
        (
            r"\brtx[\s-]*3090[\s-]*ti\b",
            "RTX 3090 Ti",
        ),
        (
            r"\brtx[\s-]*3090\b",
            "RTX 3090",
        ),

        (
            r"\brtx[\s-]*3080[\s-]*ti\b",
            "RTX 3080 Ti",
        ),
        (
            r"\brtx[\s-]*3080\b",
            "RTX 3080",
        ),

        (
            r"\brtx[\s-]*3070[\s-]*ti\b",
            "RTX 3070 Ti",
        ),
        (
            r"\brtx[\s-]*3070\b",
            "RTX 3070",
        ),

        (
            r"\brtx[\s-]*3060[\s-]*ti\b",
            "RTX 3060 Ti",
        ),
        (
            r"\brtx[\s-]*3060\b",
            "RTX 3060",
        ),

        (
            r"\brtx[\s-]*3050\b",
            "RTX 3050",
        ),

        # RTX 20
        (
            r"\brtx[\s-]*2080[\s-]*ti\b",
            "RTX 2080 Ti",
        ),
        (
            r"\brtx[\s-]*2080[\s-]*super\b",
            "RTX 2080 Super",
        ),
        (
            r"\brtx[\s-]*2080\b",
            "RTX 2080",
        ),

        (
            r"\brtx[\s-]*2070[\s-]*super\b",
            "RTX 2070 Super",
        ),
        (
            r"\brtx[\s-]*2070\b",
            "RTX 2070",
        ),

        (
            r"\brtx[\s-]*2060[\s-]*super\b",
            "RTX 2060 Super",
        ),
        (
            r"\brtx[\s-]*2060\b",
            "RTX 2060",
        ),
    )

    # ==========================================================
    # NVIDIA GTX / GT / G
    # ==========================================================

    NVIDIA_LEGACY_PATTERNS = (
        # GTX 16
        (
            r"\bgtx[\s-]*1660[\s-]*ti\b",
            "GTX 1660 Ti",
        ),
        (
            r"\bgtx[\s-]*1660[\s-]*super\b",
            "GTX 1660 Super",
        ),
        (
            r"\bgtx[\s-]*1660\b",
            "GTX 1660",
        ),

        (
            r"\bgtx[\s-]*1650[\s-]*super\b",
            "GTX 1650 Super",
        ),
        (
            r"\bgtx[\s-]*1650\b",
            "GTX 1650",
        ),

        # GTX 10
        (
            r"\bgtx[\s-]*1080[\s-]*ti\b",
            "GTX 1080 Ti",
        ),
        (
            r"\bgtx[\s-]*1080\b",
            "GTX 1080",
        ),

        (
            r"\bgtx[\s-]*1070[\s-]*ti\b",
            "GTX 1070 Ti",
        ),
        (
            r"\bgtx[\s-]*1070\b",
            "GTX 1070",
        ),

        (
            r"\bgtx[\s-]*1060\b",
            "GTX 1060",
        ),

        (
            r"\bgtx[\s-]*1050[\s-]*ti\b",
            "GTX 1050 Ti",
        ),
        (
            r"\bgtx[\s-]*1050\b",
            "GTX 1050",
        ),

        # GTX 900
        (
            r"\bgtx[\s-]*980[\s-]*ti\b",
            "GTX 980 Ti",
        ),
        (
            r"\bgtx[\s-]*980\b",
            "GTX 980",
        ),
        (
            r"\bgtx[\s-]*970\b",
            "GTX 970",
        ),
        (
            r"\bgtx[\s-]*960\b",
            "GTX 960",
        ),
        (
            r"\bgtx[\s-]*950\b",
            "GTX 950",
        ),

        # GT
        (
            r"\bgt[\s-]*1030\b",
            "GT 1030",
        ),
        (
            r"\bgt[\s-]*730\b",
            "GT 730",
        ),
        (
            r"\bgt[\s-]*710\b",
            "GT 710",
        ),

        # G210 / GT210
        #
        # Mercado Livre contém ambos os formatos.
        (
            r"\b(?:geforce[\s-]*)?gt[\s-]*210\b",
            "G210",
        ),
        (
            r"\b(?:geforce[\s-]*)?g[\s-]*210\b",
            "G210",
        ),
    )

    # ==========================================================
    # AMD RADEON
    # ==========================================================

    AMD_MODEL_PATTERNS = (
        # RX 9000
        (
            r"\brx[\s-]*9070[\s-]*xt\b",
            "RX 9070 XT",
        ),
        (
            r"\brx[\s-]*9070\b",
            "RX 9070",
        ),

        # RX 7000
        (
            r"\brx[\s-]*7900[\s-]*xtx\b",
            "RX 7900 XTX",
        ),
        (
            r"\brx[\s-]*7900[\s-]*xt\b",
            "RX 7900 XT",
        ),

        (
            r"\brx[\s-]*7800[\s-]*xt\b",
            "RX 7800 XT",
        ),

        (
            r"\brx[\s-]*7700[\s-]*xt\b",
            "RX 7700 XT",
        ),

        (
            r"\brx[\s-]*7600[\s-]*xt\b",
            "RX 7600 XT",
        ),
        (
            r"\brx[\s-]*7600\b",
            "RX 7600",
        ),

        # RX 6000
        (
            r"\brx[\s-]*6950[\s-]*xt\b",
            "RX 6950 XT",
        ),
        (
            r"\brx[\s-]*6900[\s-]*xt\b",
            "RX 6900 XT",
        ),

        (
            r"\brx[\s-]*6800[\s-]*xt\b",
            "RX 6800 XT",
        ),
        (
            r"\brx[\s-]*6800\b",
            "RX 6800",
        ),

        (
            r"\brx[\s-]*6750[\s-]*xt\b",
            "RX 6750 XT",
        ),
        (
            r"\brx[\s-]*6700[\s-]*xt\b",
            "RX 6700 XT",
        ),

        (
            r"\brx[\s-]*6650[\s-]*xt\b",
            "RX 6650 XT",
        ),
        (
            r"\brx[\s-]*6600[\s-]*xt\b",
            "RX 6600 XT",
        ),
        (
            r"\brx[\s-]*6600\b",
            "RX 6600",
        ),

        (
            r"\brx[\s-]*6500[\s-]*xt\b",
            "RX 6500 XT",
        ),

        # RX 5000
        (
            r"\brx[\s-]*5700[\s-]*xt\b",
            "RX 5700 XT",
        ),
        (
            r"\brx[\s-]*5700\b",
            "RX 5700",
        ),
        (
            r"\brx[\s-]*5600[\s-]*xt\b",
            "RX 5600 XT",
        ),
        (
            r"\brx[\s-]*5500[\s-]*xt\b",
            "RX 5500 XT",
        ),

        # RX 500
        (
            r"\brx[\s-]*590\b",
            "RX 590",
        ),
        (
            r"\brx[\s-]*580\b",
            "RX 580",
        ),
        (
            r"\brx[\s-]*570\b",
            "RX 570",
        ),
        (
            r"\brx[\s-]*560\b",
            "RX 560",
        ),
        (
            r"\brx[\s-]*550\b",
            "RX 550",
        ),
    )

    # ==========================================================
    # PRODUTOS QUE NÃO SÃO GPU
    # ==========================================================

    EXCLUDED_PATTERNS = (
        # Notebook
        r"\bnotebook\b",
        r"\blaptop\b",

        # Computadores completos
        r"\bpc\s+gamer\b",
        r"\bcomputador\s+gamer\b",
        r"\bcomputador\s+completo\b",
        r"\bdesktop\s+gamer\b",
        r"\bmini\s*pc\b",

        # Placa-mãe / kits
        r"\bplaca\s+mae\b",
        r"\bmotherboard\b",
        r"\bkit\s+upgrade\b",

        # Refrigeração
        r"\bwater\s*block\b",
        r"\bwaterblock\b",
        r"\bbloco\s+de\s+agua\b",
        r"\bcooler\s+para\b",
        r"\bventoinha\s+para\b",
        r"\bfan\s+para\b",

        # Acessórios
        r"\bbackplate\b",
        r"\bsuporte\s+para\b",
        r"\bsuporte\s+vertical\b",
        r"\briser\b",
        r"\bcabo\s+riser\b",
        r"\bextensor\s+pcie\b",
        r"\badaptador\s+pcie\b",

        # Embalagens / itens decorativos
        r"\bcaixa\s+vazia\b",
        r"\bcaixa\s+da\s+placa\b",
        r"\bembalagem\s+vazia\b",
        r"\badesivo\b",
        r"\bsticker\b",
        r"\bchaveiro\b",

        # Reparos
        r"\bcarcaca\b",
        r"\bdissipador\s+para\b",
        r"\bthermal\s+pad\b",
    )

    # ==========================================================
    # API
    # ==========================================================

    def can_classify(
        self,
        product: Product,
    ) -> bool:
        normalized_title = (
            ClassifierTextUtils.normalize(
                product.title
            )
        )

        if self._looks_like_non_gpu(
            normalized_title
        ):
            return False

        return (
            self._extract_model(
                normalized_title
            )
            is not None
        )

    def classify(
        self,
        product: Product,
    ) -> ProductProfile:
        normalized_title = (
            ClassifierTextUtils.normalize(
                product.title
            )
        )

        if self._looks_like_non_gpu(
            normalized_title
        ):
            return self._empty_profile(
                product
            )

        model = self._extract_model(
            normalized_title
        )

        if model is None:
            return self._empty_profile(
                product
            )

        gpu_vendor = (
            self._extract_gpu_vendor(
                model
            )
        )

        brand = (
            self._extract_brand(
                normalized_title
            )
        )

        memory_gb = (
            self._extract_memory(
                normalized_title
            )
        )

        variant = (
            self._extract_variant(
                normalized_title
            )
        )

        generation = (
            self._extract_generation(
                model
            )
        )

        segment = (
            self._extract_segment(
                model
            )
        )

        variant_class = (
            self._extract_model_variant_class(
                model
            )
        )

        broad_key = (
            self._build_broad_key(
                gpu_vendor=gpu_vendor,
                generation=generation,
                segment=segment,
                variant_class=variant_class,
                memory_gb=memory_gb,
            )
        )

        tier_key = (
            self._build_tier_key(
                gpu_vendor=gpu_vendor,
                model=model,
                memory_gb=memory_gb,
            )
        )

        strict_key = (
            self._build_strict_key(
                brand=brand,
                model=model,
                memory_gb=memory_gb,
                variant=variant,
            )
        )

        identity_confidence = (
            self._get_identity_confidence(
                model=model,
                memory_gb=memory_gb,
                brand=brand,
                variant=variant,
            )
        )

        return ProductProfile(
            product_id=product.id,
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
                "manufacturer": brand,
                "generation": generation,
                "segment": segment,
                "vram_gb": memory_gb,
                "variant": variant,
                "variant_class": variant_class,
                "identity_confidence": (
                    identity_confidence
                ),
            },
        )

    # ==========================================================
    # FILTROS
    # ==========================================================

    @classmethod
    def _looks_like_non_gpu(
        cls,
        normalized_title: str,
    ) -> bool:
        for pattern in (
            cls.EXCLUDED_PATTERNS
        ):
            if re.search(
                pattern,
                normalized_title,
            ):
                return True

        return False

    # ==========================================================
    # MARCA DA PLACA
    # ==========================================================

    def _extract_brand(
        self,
        normalized_title: str,
    ) -> str | None:
        for (
            search_term,
            brand,
        ) in self.KNOWN_BRANDS:
            if re.search(
                rf"\b"
                rf"{re.escape(search_term)}"
                rf"\b",
                normalized_title,
            ):
                return brand

        return None

    # ==========================================================
    # MODELO
    # ==========================================================

    def _extract_model(
        self,
        normalized_title: str,
    ) -> str | None:
        pattern_groups = (
            self.NVIDIA_RTX_PATTERNS,
            self.NVIDIA_LEGACY_PATTERNS,
            self.AMD_MODEL_PATTERNS,
        )

        for patterns in pattern_groups:
            for (
                pattern,
                model,
            ) in patterns:
                if re.search(
                    pattern,
                    normalized_title,
                ):
                    return model

        return None

    # ==========================================================
    # GPU VENDOR
    # ==========================================================

    @staticmethod
    def _extract_gpu_vendor(
        model: str,
    ) -> str | None:
        if (
            model.startswith("RTX")
            or model.startswith("GTX")
            or model.startswith("GT ")
            or model == "G210"
        ):
            return "NVIDIA"

        if model.startswith("RX"):
            return "AMD"

        return None

    # ==========================================================
    # VRAM
    # ==========================================================

    @staticmethod
    def _extract_memory(
        normalized_title: str,
    ) -> int | None:
        patterns = (
            r"\b(\d{1,2})\s*(?:gb|g)\b",
            r"\b(\d{1,2})\s*gigas?\b",
            r"\bmemoria\s+(?:de\s+)?(\d{1,2})\b",
            r"\bvram\s*(\d{1,2})\s*(?:gb)?\b",
        )

        for pattern in patterns:
            match = re.search(
                pattern,
                normalized_title,
            )

            if match is None:
                continue

            memory = int(
                match.group(1)
            )

            if (
                1
                <= memory
                <= 64
            ):
                return memory

        return None

    # ==========================================================
    # VARIANTE
    # ==========================================================

    def _extract_variant(
        self,
        normalized_title: str,
    ) -> str | None:
        ordered_variants = sorted(
            self.KNOWN_VARIANTS,
            key=len,
            reverse=True,
        )

        for variant in (
            ordered_variants
        ):
            normalized_variant = (
                ClassifierTextUtils.normalize(
                    variant
                )
            )

            if self._contains_phrase(
                normalized_title=normalized_title,
                phrase=normalized_variant,
            ):
                return normalized_variant

        return None

    @staticmethod
    def _contains_phrase(
        *,
        normalized_title: str,
        phrase: str,
    ) -> bool:
        return bool(
            re.search(
                rf"\b"
                rf"{re.escape(phrase)}"
                rf"\b",
                normalized_title,
            )
        )

    # ==========================================================
    # GERAÇÃO
    # ==========================================================

    @staticmethod
    def _extract_generation(
        model: str,
    ) -> str | None:
        # RTX 5060 -> 50
        # RTX 4070 -> 40
        if model.startswith("RTX"):
            match = re.search(
                r"RTX\s+(\d{2})\d{2}",
                model,
            )

            if match is not None:
                return match.group(1)

        # GTX 1660 -> 16
        # GTX 1080 -> 10
        if model.startswith("GTX"):
            match = re.search(
                r"GTX\s+(\d{2})\d{2}",
                model,
            )

            if match is not None:
                return match.group(1)

            # GTX 980 -> 900
            match = re.search(
                r"GTX\s+(\d)\d{2}",
                model,
            )

            if match is not None:
                return (
                    f"{match.group(1)}00"
                )

        # GT 1030 -> 10
        if model.startswith("GT "):
            match = re.search(
                r"GT\s+(\d{2})\d{2}",
                model,
            )

            if match is not None:
                return match.group(1)

            # GT 730 -> 700
            match = re.search(
                r"GT\s+(\d)\d{2}",
                model,
            )

            if match is not None:
                return (
                    f"{match.group(1)}00"
                )

        if model == "G210":
            return "200"

        if model.startswith("RX"):
            # RX 9070 -> 9000
            # RX 7900 -> 7000
            match = re.search(
                r"RX\s+(\d)(\d{3})",
                model,
            )

            if match is not None:
                return (
                    f"{match.group(1)}000"
                )

            # RX 580 -> 500
            # RX 570 -> 500
            match = re.search(
                r"RX\s+(\d)(\d{2})",
                model,
            )

            if match is not None:
                return (
                    f"{match.group(1)}00"
                )

        return None

    # ==========================================================
    # SEGMENTO
    # ==========================================================

    @staticmethod
    def _extract_segment(
        model: str,
    ) -> str | None:
        # RTX / GTX com 4 dígitos.
        #
        # RTX 5060 -> 60
        # GTX 1660 -> 60
        nvidia_four_digit = re.search(
            r"\b"
            r"(?:RTX|GTX)"
            r"\s+"
            r"\d{2}"
            r"(\d{2})"
            r"\b",
            model,
        )

        if nvidia_four_digit is not None:
            return (
                nvidia_four_digit.group(1)
            )

        # GTX 980 -> 80
        nvidia_three_digit = re.search(
            r"\bGTX\s+\d(\d{2})\b",
            model,
        )

        if nvidia_three_digit is not None:
            return (
                nvidia_three_digit.group(1)
            )

        # GT 1030 -> 30
        gt_four_digit = re.search(
            r"\bGT\s+\d{2}(\d{2})\b",
            model,
        )

        if gt_four_digit is not None:
            return (
                gt_four_digit.group(1)
            )

        # GT 730 -> 30
        gt_three_digit = re.search(
            r"\bGT\s+\d(\d{2})\b",
            model,
        )

        if gt_three_digit is not None:
            return (
                gt_three_digit.group(1)
            )

        if model == "G210":
            return "10"

        # RX 7900 -> 90
        # RX 7800 -> 80
        # RX 6700 -> 70
        amd_four_digit = re.search(
            r"\bRX\s+(\d{4})\b",
            model,
        )

        if amd_four_digit is not None:
            number = (
                amd_four_digit.group(1)
            )

            if number.startswith("9"):
                return number[2:4]

            return number[1:3]

        # RX 580 -> 80
        # RX 570 -> 70
        amd_three_digit = re.search(
            r"\bRX\s+(\d{3})\b",
            model,
        )

        if amd_three_digit is not None:
            number = (
                amd_three_digit.group(1)
            )

            return number[1:3]

        return None

    # ==========================================================
    # CLASSE DO CHIP
    # ==========================================================

    @staticmethod
    def _extract_model_variant_class(
        model: str,
    ) -> str:
        normalized_model = (
            model.lower()
        )

        if "xtx" in normalized_model:
            return "xtx"

        if "ti super" in normalized_model:
            return "ti_super"

        if "super" in normalized_model:
            return "super"

        if re.search(
            r"\bti\b",
            normalized_model,
        ):
            return "ti"

        if re.search(
            r"\bxt\b",
            normalized_model,
        ):
            return "xt"

        return "standard"

    # ==========================================================
    # CONFIANÇA
    # ==========================================================

    @staticmethod
    def _get_identity_confidence(
        *,
        model: str | None,
        memory_gb: int | None,
        brand: str | None,
        variant: str | None,
    ) -> str:
        if (
            model is not None
            and memory_gb is not None
            and brand is not None
            and variant is not None
        ):
            return "alta"

        if (
            model is not None
            and memory_gb is not None
            and brand is not None
        ):
            return "media"

        if (
            model is not None
            and memory_gb is not None
        ):
            return "media"

        if model is not None:
            return "baixa"

        return "muito_baixa"

    # ==========================================================
    # BROAD
    # ==========================================================

    @staticmethod
    def _build_broad_key(
        *,
        gpu_vendor: str | None,
        generation: str | None,
        segment: str | None,
        variant_class: str,
        memory_gb: int | None,
    ) -> str | None:
        if (
            gpu_vendor is None
            or generation is None
            or segment is None
            or memory_gb is None
        ):
            return None

        return (
            "gpu_"
            f"{gpu_vendor.lower()}_"
            f"{ClassifierTextUtils.slug(generation)}_"
            f"{segment}_"
            f"{variant_class}_"
            f"{memory_gb}gb"
        )

    # ==========================================================
    # TIER
    # ==========================================================

    @staticmethod
    def _build_tier_key(
        *,
        gpu_vendor: str | None,
        model: str | None,
        memory_gb: int | None,
    ) -> str | None:
        if (
            gpu_vendor is None
            or model is None
        ):
            return None

        parts = [
            "gpu",
            gpu_vendor.lower(),
            ClassifierTextUtils.slug(
                model
            ),
        ]

        if memory_gb is not None:
            parts.append(
                f"{memory_gb}gb"
            )

        return "_".join(
            parts
        )

    # ==========================================================
    # STRICT
    # ==========================================================

    @staticmethod
    def _build_strict_key(
        *,
        brand: str | None,
        model: str | None,
        memory_gb: int | None,
        variant: str | None,
    ) -> str | None:
        if (
            brand is None
            or model is None
            or memory_gb is None
            or variant is None
        ):
            return None

        return "_".join(
            (
                ClassifierTextUtils.slug(
                    brand
                ),
                ClassifierTextUtils.slug(
                    model
                ),
                ClassifierTextUtils.slug(
                    variant
                ),
                f"{memory_gb}gb",
            )
        )

    # ==========================================================
    # PERFIL VAZIO
    # ==========================================================

    @staticmethod
    def _empty_profile(
        product: Product,
    ) -> ProductProfile:
        return ProductProfile(
            product_id=product.id,
            brand=None,
            model=None,
            memory_gb=None,
            variant=None,
            broad_key=None,
            tier_key=None,
            strict_key=None,
            category=None,
            attributes={
                "identity_confidence": (
                    "muito_baixa"
                ),
            },
        )
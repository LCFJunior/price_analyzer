import re

from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)
from services.classifiers.text_utils import (
    ClassifierTextUtils,
)


class CPUClassifier:
    """
    Classificador de processadores AMD Ryzen
    e Intel Core.

    Hierarquia:

        STRICT
        mesmo modelo exato

            ↓

        TIER
        mesma família + geração/série
        + classe de variante

            ↓

        BROAD
        mesma família geral
    """

    # ==========================================================
    # AMD
    # ==========================================================

    AMD_FAMILY_PATTERNS = (
        re.compile(
            r"\b"
            r"ryzen\s+"
            r"([3579])"
            r"\b"
        ),

        re.compile(
            r"\b"
            r"amd\s+"
            r"r([3579])"
            r"\b"
        ),

        re.compile(
            r"\b"
            r"r([3579])"
            r"\s+"
            r"\d{4}"
        ),
    )

    AMD_MODEL_PATTERN = re.compile(
        r"\b"
        r"(\d{4})"
        r"(x3d|xt|gt|x|ge|g|f)?"
        r"(?=[^a-z]|$)"
    )

    AMD_VARIANTS = {
        "x3d": "X3D",
        "xt": "XT",
        "gt": "GT",
        "x": "X",
        "ge": "GE",
        "g": "G",
        "f": "F",
    }

    # ==========================================================
    # INTEL
    # ==========================================================

    INTEL_MODEL_PATTERN = re.compile(
        r"\b"
        r"(?:intel\s+)?"
        r"(?:core\s+)?"
        r"(i[3579])"
        r"[\s\-]*"
        r"(\d{4,5})"
        r"(ks|kf|k|f|t|m|u|h|hq)?"
        r"\b"
    )

    INTEL_LEGACY_MOBILE_PATTERN = re.compile(
        r"\b"
        r"(?:intel\s+)?"
        r"(?:core\s+)?"
        r"(i[3579])"
        r"[\s\-]*"
        r"(\d{3})"
        r"(m|um|lm)"
        r"\b"
    )

    INTEL_VARIANTS = {
        "ks": "KS",
        "kf": "KF",
        "k": "K",
        "f": "F",
        "t": "T",
        "m": "M",
        "um": "UM",
        "lm": "LM",
        "u": "U",
        "h": "H",
        "hq": "HQ",
    }

    # ==========================================================
    # PRODUTOS QUE NÃO SÃO CPU
    # ==========================================================

    EXCLUDED_PATTERNS = (
        r"\bkit\s+upgrade\b",
        r"\bkit\s+processador\b",
        r"\bkit\s+ryzen\b",
        r"\bkit\s+intel\b",

        r"\bplaca\s+mae\b",
        r"\bmotherboard\b",

        r"\bcaixa\s+vazia\b",
        r"\bcaixa\s+do\s+processador\b",
        r"\bembalagem\s+vazia\b",

        r"\badesivo\b",
        r"\bsticker\b",
        r"\bblister\b",
        r"\bmanual\b",
        r"\bchaveiro\b",

        r"\bsuporte\s+para\b",
        r"\bcooler\s+para\b",
        r"\bwater\s*cooler\s+para\b",

        r"\bprocessador\s+de\s+audio\b",
        r"\bprocessador\s+audio\b",
        r"\bprocessador\s+de\s+alimentos\b",

        r"\bmini\s+processador\b",
        r"\bmultiprocessador\b",

        r"\bmixer\b",
        r"\bcrossover\b",
        r"\bequalizador\b",
        r"\bsom\s+automotivo\b",

        r"\bpasta\s+termica\b",

        r"\blaminas?\b",

        r"\b250ml\b",
        r"\b500ml\b",
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

        if self._looks_like_non_cpu(
            normalized_title
        ):
            return False

        if (
            self._extract_amd_data(
                normalized_title
            )
            is not None
        ):
            return True

        if (
            self._extract_intel_match(
                normalized_title
            )
            is not None
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

        if self._looks_like_non_cpu(
            normalized_title
        ):
            return self._empty_profile(
                product
            )

        amd_data = (
            self._extract_amd_data(
                normalized_title
            )
        )

        if amd_data is not None:
            (
                family_number,
                model_number,
                suffix,
            ) = amd_data

            return self._classify_amd(
                product=product,
                family_number=(
                    family_number
                ),
                model_number=(
                    model_number
                ),
                suffix=suffix,
            )

        intel_data = (
            self._extract_intel_match(
                normalized_title
            )
        )

        if intel_data is not None:
            return self._classify_intel(
                product=product,
                family_raw=(
                    intel_data[0]
                ),
                model_number=(
                    intel_data[1]
                ),
                suffix=(
                    intel_data[2]
                ),
                legacy_mobile=(
                    intel_data[3]
                ),
            )

        return self._empty_profile(
            product
        )

    # ==========================================================
    # FILTRO
    # ==========================================================

    @classmethod
    def _looks_like_non_cpu(
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
    # AMD
    # ==========================================================

    def _extract_amd_data(
        self,
        normalized_title: str,
    ) -> tuple[
        str,
        str,
        str,
    ] | None:
        family_number = (
            self._extract_amd_family(
                normalized_title
            )
        )

        if family_number is None:
            return None

        model_match = (
            self.AMD_MODEL_PATTERN.search(
                normalized_title
            )
        )

        if model_match is None:
            return None

        model_number = (
            model_match.group(1)
        )

        suffix = (
            model_match.group(2)
            or ""
        ).lower()

        model_value = int(
            model_number
        )

        if not (
            1000
            <= model_value
            <= 9999
        ):
            return None

        return (
            family_number,
            model_number,
            suffix,
        )

    def _extract_amd_family(
        self,
        normalized_title: str,
    ) -> str | None:
        for pattern in (
            self.AMD_FAMILY_PATTERNS
        ):
            match = pattern.search(
                normalized_title
            )

            if match is not None:
                return (
                    match.group(1)
                )

        return None

    def _classify_amd(
        self,
        *,
        product: Product,
        family_number: str,
        model_number: str,
        suffix: str,
    ) -> ProductProfile:
        family = (
            f"Ryzen {family_number}"
        )

        variant = (
            self.AMD_VARIANTS.get(
                suffix
            )
        )

        model = (
            f"{family} "
            f"{model_number}"
            f"{variant or ''}"
        )

        series = (
            self._get_amd_series(
                model_number
            )
        )

        variant_class = (
            self._get_amd_variant_class(
                suffix
            )
        )

        broad_key = (
            "cpu_amd_"
            f"ryzen_{family_number}"
        )

        tier_key = (
            self._build_amd_tier_key(
                family_number=(
                    family_number
                ),
                series=series,
                variant_class=(
                    variant_class
                ),
            )
        )

        strict_key = (
            "amd_"
            f"{ClassifierTextUtils.slug(model)}"
        )

        return ProductProfile(
            product_id=product.id,
            brand="AMD",
            model=model,
            memory_gb=None,
            variant=variant,
            broad_key=broad_key,
            tier_key=tier_key,
            strict_key=strict_key,
            category="cpu",
            attributes={
                "manufacturer": "AMD",
                "family": family,
                "family_number": (
                    family_number
                ),
                "series": series,
                "model_number": (
                    model_number
                ),
                "variant": variant,
                "variant_class": (
                    variant_class
                ),
                "mobile": False,
                "identity_confidence": (
                    "alta"
                ),
            },
        )

    @staticmethod
    def _get_amd_series(
        model_number: str,
    ) -> str | None:
        if len(model_number) != 4:
            return None

        first_digit = (
            model_number[0]
        )

        if not first_digit.isdigit():
            return None

        return (
            f"{first_digit}000"
        )

    @staticmethod
    def _get_amd_variant_class(
        suffix: str,
    ) -> str:
        """
        Agrupa variantes AMD por comportamento
        comercial/técnico parecido.

        Exemplos:

        5600
            -> standard

        5600X
            -> x

        5600G / 5600GT / 5600GE
            -> apu

        5700X3D
            -> x3d

        3600XT
            -> xt
        """

        suffix = (
            suffix
            or ""
        ).lower()

        if suffix == "x3d":
            return "x3d"

        if suffix in {
            "g",
            "gt",
            "ge",
        }:
            return "apu"

        if suffix == "x":
            return "x"

        if suffix == "xt":
            return "xt"

        if suffix == "f":
            return "f"

        return "standard"

    @staticmethod
    def _build_amd_tier_key(
        *,
        family_number: str,
        series: str | None,
        variant_class: str,
    ) -> str | None:
        if series is None:
            return None

        return (
            "cpu_amd_"
            f"ryzen_{family_number}_"
            f"{series}_"
            f"{variant_class}"
        )

    # ==========================================================
    # INTEL
    # ==========================================================

    def _extract_intel_match(
        self,
        normalized_title: str,
    ) -> tuple[
        str,
        str,
        str,
        bool,
    ] | None:
        modern_match = (
            self.INTEL_MODEL_PATTERN.search(
                normalized_title
            )
        )

        if modern_match is not None:
            return (
                modern_match.group(1),
                modern_match.group(2),
                (
                    modern_match.group(3)
                    or ""
                ).lower(),
                False,
            )

        legacy_match = (
            self.INTEL_LEGACY_MOBILE_PATTERN
            .search(
                normalized_title
            )
        )

        if legacy_match is not None:
            return (
                legacy_match.group(1),
                legacy_match.group(2),
                (
                    legacy_match.group(3)
                    or ""
                ).lower(),
                True,
            )

        return None

    def _classify_intel(
        self,
        *,
        product: Product,
        family_raw: str,
        model_number: str,
        suffix: str,
        legacy_mobile: bool,
    ) -> ProductProfile:
        family_raw = (
            family_raw.lower()
        )

        family_display = (
            family_raw.upper()
        )

        variant = (
            self.INTEL_VARIANTS.get(
                suffix
            )
        )

        model = (
            f"Core "
            f"{family_display}-"
            f"{model_number}"
            f"{variant or ''}"
        )

        generation = (
            self._get_intel_generation(
                model_number=(
                    model_number
                ),
                legacy_mobile=(
                    legacy_mobile
                ),
            )
        )

        variant_class = (
            self._get_intel_variant_class(
                suffix=suffix,
                legacy_mobile=(
                    legacy_mobile
                ),
            )
        )

        broad_key = (
            "cpu_intel_core_"
            f"{family_raw}"
        )

        tier_key = (
            self._build_intel_tier_key(
                family=(
                    family_raw
                ),
                generation=(
                    generation
                ),
                variant_class=(
                    variant_class
                ),
            )
        )

        strict_key = (
            "intel_"
            f"{ClassifierTextUtils.slug(model)}"
        )

        return ProductProfile(
            product_id=product.id,
            brand="INTEL",
            model=model,
            memory_gb=None,
            variant=variant,
            broad_key=broad_key,
            tier_key=tier_key,
            strict_key=strict_key,
            category="cpu",
            attributes={
                "manufacturer": (
                    "INTEL"
                ),
                "family": (
                    family_display
                ),
                "generation": (
                    generation
                ),
                "model_number": (
                    model_number
                ),
                "variant": variant,
                "variant_class": (
                    variant_class
                ),
                "mobile": (
                    legacy_mobile
                    or variant_class
                    == "mobile"
                ),
                "identity_confidence": (
                    "alta"
                ),
            },
        )

    @staticmethod
    def _get_intel_generation(
        *,
        model_number: str,
        legacy_mobile: bool,
    ) -> int | None:
        if not model_number.isdigit():
            return None

        if (
            legacy_mobile
            and len(model_number) == 3
        ):
            return 1

        if len(model_number) == 4:
            first_digit = int(
                model_number[0]
            )

            if (
                2
                <= first_digit
                <= 9
            ):
                return first_digit

            return None

        if len(model_number) == 5:
            generation = int(
                model_number[:2]
            )

            if (
                10
                <= generation
                <= 19
            ):
                return generation

        return None

    @staticmethod
    def _get_intel_variant_class(
        *,
        suffix: str,
        legacy_mobile: bool,
    ) -> str:
        suffix = (
            suffix
            or ""
        ).lower()

        if legacy_mobile:
            return "mobile"

        if suffix in {
            "m",
            "um",
            "lm",
            "u",
            "h",
            "hq",
        }:
            return "mobile"

        if suffix in {
            "k",
            "kf",
            "ks",
        }:
            return "performance"

        if suffix == "f":
            return "standard_f"

        if suffix == "t":
            return "low_power"

        return "standard"

    @staticmethod
    def _build_intel_tier_key(
        *,
        family: str,
        generation: int | None,
        variant_class: str,
    ) -> str | None:
        if generation is None:
            return None

        return (
            "cpu_intel_core_"
            f"{family}_"
            f"gen{generation}_"
            f"{variant_class}"
        )

    # ==========================================================
    # EMPTY
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
import re

from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)
from services.classifiers.text_utils import (
    ClassifierTextUtils,
)


class GPUClassifier:
    KNOWN_BRANDS = (
        "asus",
        "msi",
        "gigabyte",
        "zotac",
        "galax",
        "gainward",
        "palit",
        "pny",
        "inno3d",
        "colorful",
        "nvidia",
        "sapphire",
        "powercolor",
        "xfx",
        "asrock",
    )

    KNOWN_VARIANTS = (
        "ventus 3x",
        "ventus 2x",
        "shadow 3x",
        "shadow 2x",
        "windforce",
        "gaming oc",
        "prime oc",
        "dual oc",
        "solid oc",
        "phoenix gs",
        "phoenix",
        "infinity 3",
        "twin x2",
        "dual fan",
        "dual-fan",
        "slim dualfan",
        "tuf gaming",
        "rog strix",
        "aero oc",
        "eagle oc",
        "hellhound",
        "red devil",
        "nitro plus",
        "pulse",
        "merc",
        "quick",
    )

    MODEL_PATTERNS = (
        (
            r"\brtx\s*5090\b",
            "RTX 5090",
        ),
        (
            r"\brtx\s*5080\b",
            "RTX 5080",
        ),
        (
            r"\brtx\s*5070\s*ti\b",
            "RTX 5070 Ti",
        ),
        (
            r"\brtx\s*5070ti\b",
            "RTX 5070 Ti",
        ),
        (
            r"\brtx\s*5070\b",
            "RTX 5070",
        ),
        (
            r"\brtx\s*5060\s*ti\b",
            "RTX 5060 Ti",
        ),
        (
            r"\brtx\s*5060ti\b",
            "RTX 5060 Ti",
        ),
        (
            r"\brtx\s*5060\b",
            "RTX 5060",
        ),
        (
            r"\brtx\s*4090\b",
            "RTX 4090",
        ),
        (
            r"\brtx\s*4080\s*super\b",
            "RTX 4080 Super",
        ),
        (
            r"\brtx\s*4080\b",
            "RTX 4080",
        ),
        (
            r"\brtx\s*4070\s*ti\s*super\b",
            "RTX 4070 Ti Super",
        ),
        (
            r"\brtx\s*4070\s*ti\b",
            "RTX 4070 Ti",
        ),
        (
            r"\brtx\s*4070\s*super\b",
            "RTX 4070 Super",
        ),
        (
            r"\brtx\s*4070\b",
            "RTX 4070",
        ),
        (
            r"\brx\s*9070\s*xt\b",
            "RX 9070 XT",
        ),
        (
            r"\brx\s*9070\b",
            "RX 9070",
        ),
        (
            r"\brx\s*7900\s*xtx\b",
            "RX 7900 XTX",
        ),
        (
            r"\brx\s*7900\s*xt\b",
            "RX 7900 XT",
        ),
        (
            r"\brx\s*7800\s*xt\b",
            "RX 7800 XT",
        ),
        (
            r"\brx\s*7700\s*xt\b",
            "RX 7700 XT",
        ),
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

        brand = self._extract_brand(
            normalized_title
        )

        model = self._extract_model(
            normalized_title
        )

        memory_gb = self._extract_memory(
            normalized_title
        )

        variant = self._extract_variant(
            normalized_title
        )

        broad_key = (
            self._build_broad_key(
                model=model,
                memory_gb=memory_gb,
            )
        )

        strict_key = (
            self._build_strict_key(
                brand=brand,
                model=model,
                memory_gb=memory_gb,
            )
        )

        return ProductProfile(
            product_id=product.id,
            brand=brand,
            model=model,
            memory_gb=memory_gb,
            variant=variant,
            broad_key=broad_key,
            tier_key=None,
            strict_key=strict_key,
            category="gpu",
            attributes={
                "vram_gb": memory_gb,
                "variant": variant,
                "identity_confidence": (
                    "alta"
                    if strict_key is not None
                    else "media"
                ),
            },
        )

    def _extract_brand(
        self,
        normalized_title: str,
    ) -> str | None:
        for brand in self.KNOWN_BRANDS:
            if re.search(
                rf"\b{re.escape(brand)}\b",
                normalized_title,
            ):
                return brand.upper()

        return None

    def _extract_model(
        self,
        normalized_title: str,
    ) -> str | None:
        for (
            pattern,
            model,
        ) in self.MODEL_PATTERNS:
            if re.search(
                pattern,
                normalized_title,
            ):
                return model

        return None

    @staticmethod
    def _extract_memory(
        normalized_title: str,
    ) -> int | None:
        patterns = (
            r"\b(\d{1,2})\s*(?:gb|g)\b",
            r"\b(\d{1,2})\s*gigas?\b",
            r"\bmemoria\s+(?:de\s+)?(\d{1,2})\b",
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

            if 1 <= memory <= 64:
                return memory

        return None

    def _extract_variant(
        self,
        normalized_title: str,
    ) -> str | None:
        for variant in (
            self.KNOWN_VARIANTS
        ):
            normalized_variant = (
                ClassifierTextUtils.normalize(
                    variant
                )
            )

            if (
                normalized_variant
                in normalized_title
            ):
                return variant.title()

        return None

    @staticmethod
    def _build_broad_key(
        model: str | None,
        memory_gb: int | None,
    ) -> str | None:
        if model is None:
            return None

        parts = [
            ClassifierTextUtils.slug(
                model
            )
        ]

        if memory_gb is not None:
            parts.append(
                f"{memory_gb}gb"
            )

        return "_".join(
            parts
        )

    @staticmethod
    def _build_strict_key(
        brand: str | None,
        model: str | None,
        memory_gb: int | None,
    ) -> str | None:
        if (
            brand is None
            or model is None
        ):
            return None

        parts = [
            ClassifierTextUtils.slug(
                brand
            ),
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
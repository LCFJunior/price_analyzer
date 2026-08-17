from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)

from services.classifiers.base import (
    ProductCategoryClassifier,
)

from services.classifiers.cpu_classifier import (
    CPUClassifier,
)

from services.classifiers.generic_classifier import (
    GenericClassifier,
)

from services.classifiers.gpu_classifier import (
    GPUClassifier,
)

from services.classifiers.ssd_classifier import (
    SSDClassifier,
)


class ProductClassifier:
    """
    Coordenador central dos classificadores.

    A ordem dos classificadores é importante.

    Classificadores específicos devem sempre aparecer
    antes do GenericClassifier.

    Fluxo atual:

        GPU
        ↓
        CPU
        ↓
        SSD
        ↓
        Generic
    """

    SUPPORTED_CATEGORIES = {
        "gpu",
        "cpu",
        "ssd",
    }

    def __init__(
        self,
        classifiers: list[
            ProductCategoryClassifier
        ] | None = None,
    ):
        self.classifiers = (
            classifiers
            if classifiers is not None
            else [
                GPUClassifier(),
                CPUClassifier(),
                SSDClassifier(),
                GenericClassifier(),
            ]
        )

    def classify(
        self,
        product: Product,
    ) -> ProductProfile:
        for classifier in (
            self.classifiers
        ):
            if classifier.can_classify(
                product
            ):
                return classifier.classify(
                    product
                )

        return (
            GenericClassifier()
            .classify(
                product
            )
        )

    def classify_many(
        self,
        products: list[Product],
    ) -> dict[
        str,
        ProductProfile,
    ]:
        profiles: dict[
            str,
            ProductProfile,
        ] = {}

        for product in products:
            if not product.id:
                continue

            profiles[
                product.id
            ] = self.classify(
                product
            )

        return profiles

    @classmethod
    def is_supported_category(
        cls,
        profile: ProductProfile | None,
    ) -> bool:
        if profile is None:
            return False

        return (
            profile.category
            in cls.SUPPORTED_CATEGORIES
        )
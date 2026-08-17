from entities.product import Product
from entities.product_profile import ProductProfile


class GenericClassifier:
    def can_classify(
        self,
        product: Product,
    ) -> bool:
        return True

    def classify(
        self,
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
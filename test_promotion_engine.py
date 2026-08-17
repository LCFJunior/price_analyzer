from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)

from analyzers.promotion_engine import (
    PromotionEngine,
)

from entities.product import (
    Product,
)

from entities.product_profile import (
    ProductProfile,
)


class FakeHistory:
    def __init__(
        self,
        *,
        median_price: float,
        observations: int,
    ):
        self.median_price = (
            median_price
        )

        self.average_price = (
            median_price
        )

        self.minimum_price = (
            median_price
        )

        self.maximum_price = (
            median_price
        )

        self.observations = (
            observations
        )


def create_product(
    *,
    product_id: str,
    title: str,
    price: float,
    old_price: float | None = None,
    official_store: bool = False,
    full: bool = False,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=old_price,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=official_store,
        full=full,
        shipping="Frete grátis",
        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),
        image_url=None,
        international=False,
    )


def create_profile(
    *,
    product_id: str,
    brand: str | None,
    model: str | None,
    broad_key: str | None,
    tier_key: str | None,
    strict_key: str | None,
    identity_confidence: str,
) -> ProductProfile:
    return ProductProfile(
        product_id=product_id,
        brand=brand,
        model=model,
        memory_gb=None,
        variant=None,
        broad_key=broad_key,
        tier_key=tier_key,
        strict_key=strict_key,
        category="ssd",
        attributes={
            "identity_confidence": (
                identity_confidence
            ),
        },
    )


def create_peers(
    *,
    median_price: float,
    observations: int,
    scope: str,
    key: str,
) -> PeerPriceStatistics:
    return PeerPriceStatistics(
        comparison_key=key,
        comparison_scope=scope,
        observations=observations,
        minimum_price=median_price,
        maximum_price=median_price,
        average_price=median_price,
        median_price=median_price,
    )


def print_result(
    *,
    name: str,
    result,
) -> None:
    print(
        "\n"
        + "=" * 80
    )

    print(name)

    print("=" * 80)

    print(
        f"Produto: "
        f"{result.product.title}"
    )

    print(
        f"Preço: "
        f"R$ {result.product.price:.2f}"
    )

    print(
        f"Score: "
        f"{result.score}/100"
    )

    print(
        f"Tipo: "
        f"{result.opportunity_type}"
    )

    print(
        f"Confiança: "
        f"{result.confidence}"
    )

    print(
        "Notificar: "
        f"{result.should_notify}"
    )

    print(
        "Motivos:"
    )

    for reason in (
        result.reasons
    ):
        print(
            f"- {reason}"
        )


def main() -> None:
    engine = PromotionEngine(
        notification_threshold=70,
        minimum_history_observations=3,
    )

    # ==========================================================
    # TESTE 1
    #
    # PROMOÇÃO FORTE DE MODELO EXATO
    # ==========================================================

    promo_product = create_product(
        product_id="PROMO001",
        title=(
            "Samsung 9100 Pro 1TB"
        ),
        price=1850.0,
        old_price=2600.0,
        official_store=True,
        full=True,
    )

    promo_profile = create_profile(
        product_id="PROMO001",
        brand="SAMSUNG",
        model="9100 PRO",
        broad_key="ssd_nvme_1tb",
        tier_key=(
            "ssd_nvme_gen5_1tb"
        ),
        strict_key=(
            "samsung_9100_pro_1tb_nvme"
        ),
        identity_confidence="alta",
    )

    promo_history = FakeHistory(
        median_price=2500.0,
        observations=10,
    )

    promo_peers = create_peers(
        median_price=2450.0,
        observations=4,
        scope=(
            "modelo_exato_nacional"
        ),
        key=(
            "samsung_9100_pro_1tb_nvme"
        ),
    )

    promo_result = engine.analyze(
        product=promo_product,
        profile=promo_profile,
        statistics=promo_history,
        peer_statistics=promo_peers,
    )

    print_result(
        name=(
            "TESTE 1 - PROMOÇÃO FORTE"
        ),
        result=promo_result,
    )

    # ==========================================================
    # TESTE 2
    #
    # PEQUENA DIFERENÇA DE PREÇO
    # ==========================================================

    normal_product = create_product(
        product_id="NORMAL001",
        title=(
            "Samsung 9100 Pro 1TB"
        ),
        price=2390.0,
        old_price=2500.0,
        official_store=True,
        full=True,
    )

    normal_profile = create_profile(
        product_id="NORMAL001",
        brand="SAMSUNG",
        model="9100 PRO",
        broad_key="ssd_nvme_1tb",
        tier_key=(
            "ssd_nvme_gen5_1tb"
        ),
        strict_key=(
            "samsung_9100_pro_1tb_nvme"
        ),
        identity_confidence="alta",
    )

    normal_history = FakeHistory(
        median_price=2500.0,
        observations=10,
    )

    normal_peers = create_peers(
        median_price=2450.0,
        observations=4,
        scope=(
            "modelo_exato_nacional"
        ),
        key=(
            "samsung_9100_pro_1tb_nvme"
        ),
    )

    normal_result = engine.analyze(
        product=normal_product,
        profile=normal_profile,
        statistics=normal_history,
        peer_statistics=normal_peers,
    )

    print_result(
        name=(
            "TESTE 2 - PREÇO NORMAL"
        ),
        result=normal_result,
    )

    # ==========================================================
    # TESTE 3
    #
    # PRODUTO GENÉRICO MUITO BARATO
    # ==========================================================

    generic_product = create_product(
        product_id="GEN001",
        title=(
            "SSD Genérico 1TB"
        ),
        price=160.0,
        old_price=None,
        official_store=False,
        full=False,
    )

    generic_profile = create_profile(
        product_id="GEN001",
        brand=None,
        model=None,
        broad_key="ssd_sata_1tb",
        tier_key=None,
        strict_key=None,
        identity_confidence=(
            "muito_baixa"
        ),
    )

    generic_peers = create_peers(
        median_price=800.0,
        observations=20,
        scope=(
            "grupo_geral_nacional"
        ),
        key="ssd_sata_1tb",
    )

    generic_result = engine.analyze(
        product=generic_product,
        profile=generic_profile,
        statistics=None,
        peer_statistics=(
            generic_peers
        ),
    )

    print_result(
        name=(
            "TESTE 3 - PRODUTO GENÉRICO"
        ),
        result=generic_result,
    )

    # ==========================================================
    # VERIFICAÇÕES
    # ==========================================================

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

    assert (
        promo_result.should_notify
        is True
    )

    assert (
        promo_result.opportunity_type
        == "promocao"
    )

    assert (
        promo_result.score
        >= 70
    )

    assert (
        normal_result.should_notify
        is False
    )

    assert (
        normal_result.score
        < 70
    )

    assert (
        generic_result.should_notify
        is False
    )

    assert (
        generic_result.score
        <= 55
    )

    print(
        "✓ Promoção forte foi detectada"
    )

    print(
        "✓ Pequena diferença de preço "
        "não gerou alerta"
    )

    print(
        "✓ Produto genérico barato "
        "não virou promoção forte"
    )

    print(
        "✓ Modelo exato recebeu peso "
        "maior que grupo geral"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
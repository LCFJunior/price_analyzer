from analyzers.bug_engine import (
    BugEngine,
)
from analyzers.opportunity_engine import (
    OpportunityEngine,
)
from analyzers.promotion_engine import (
    PromotionEngine,
)

from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)


class FakePeerStatistics:
    def __init__(
        self,
        *,
        median_price: float,
        observations: int,
        comparison_scope: str = "grupo_geral",
    ):
        self.median_price = median_price
        self.average_price = median_price
        self.minimum_price = median_price
        self.maximum_price = median_price

        self.observations = observations

        self.comparison_scope = (
            comparison_scope
        )

        self.comparison_key = "teste"


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
    )


def create_profile(
    *,
    product_id: str,
    brand: str | None,
    model: str | None,
    broad_key: str | None,
    strict_key: str | None,
    identity_confidence: str,
    tier_key: str | None = None,
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
        category="teste",
        attributes={
            "identity_confidence": (
                identity_confidence
            )
        },
    )


def print_result(
    title: str,
    opportunity,
) -> None:
    print(
        "\n"
        + "=" * 80
    )

    print(title)

    print("=" * 80)

    print(
        "Produto: "
        f"{opportunity.product.title}"
    )

    print(
        "Preço: "
        f"R$ {opportunity.product.price:.2f}"
    )

    print(
        f"Score: "
        f"{opportunity.score}/100"
    )

    print(
        f"Tipo: "
        f"{opportunity.opportunity_type}"
    )

    print(
        f"Confiança: "
        f"{opportunity.confidence}"
    )

    print(
        "Notificar: "
        f"{opportunity.should_notify}"
    )

    print(
        "Motivos:"
    )

    for reason in (
        opportunity.reasons
    ):
        print(
            f"- {reason}"
        )


def main() -> None:
    engine = OpportunityEngine(
        bug_engine=BugEngine(
            notification_threshold=70,
            minimum_peer_observations=4,
        ),
        promotion_engine=(
            PromotionEngine(
                notification_threshold=70,
                minimum_history_observations=3,
            )
        ),
    )

    # ==========================================================
    # TESTE 1
    # BUG REAL COM IDENTIDADE ALTA
    # ==========================================================

    bug_product = create_product(
        product_id="BUG001",
        title=(
            "Mesa Controladora "
            "Rise Mode Vision 02"
        ),
        price=70.0,
        official_store=True,
        full=True,
    )

    bug_profile = create_profile(
        product_id="BUG001",
        brand="RISE MODE",
        model="VISION 02",
        broad_key=(
            "stream_controller"
        ),
        tier_key=None,
        strict_key=(
            "rise_mode_vision_02"
        ),
        identity_confidence="alta",
    )

    bug_peers = FakePeerStatistics(
        median_price=400.0,
        observations=10,
    )

    bug_result = engine.analyze(
        product=bug_product,
        profile=bug_profile,
        statistics=None,
        peer_statistics=bug_peers,
    )

    print_result(
        "TESTE 1 - BUG COM IDENTIDADE ALTA",
        bug_result,
    )

    # ==========================================================
    # TESTE 2
    # SSD GENÉRICO MUITO BARATO
    # ==========================================================

    generic_ssd = create_product(
        product_id="SSDGEN001",
        title=(
            "BH 1TB M.2 SATA SSD "
            "Armazenamento de Alta Velocidade"
        ),
        price=161.03,
    )

    generic_profile = create_profile(
        product_id="SSDGEN001",
        brand=None,
        model=None,
        broad_key="ssd_sata_1tb",
        tier_key="ssd_sata_sata_1tb",
        strict_key=None,
        identity_confidence=(
            "muito_baixa"
        ),
    )

    generic_peers = FakePeerStatistics(
        median_price=1299.0,
        observations=33,
    )

    generic_result = engine.analyze(
        product=generic_ssd,
        profile=generic_profile,
        statistics=None,
        peer_statistics=(
            generic_peers
        ),
    )

    print_result(
        "TESTE 2 - SSD GENÉRICO "
        "COM IDENTIDADE MUITO BAIXA",
        generic_result,
    )

    # ==========================================================
    # TESTE 3
    # PROMOÇÃO NORMAL
    # ==========================================================

    promo_product = create_product(
        product_id="PROMO001",
        title="SSD Kingston NV3 1TB",
        price=299.0,
        old_price=399.0,
        official_store=True,
        full=True,
    )

    promo_profile = create_profile(
        product_id="PROMO001",
        brand="KINGSTON",
        model="NV3",
        broad_key="ssd_nvme_1tb",
        tier_key="ssd_nvme_gen4_1tb",
        strict_key=(
            "kingston_nv3_1tb_nvme"
        ),
        identity_confidence="alta",
    )

    promo_peers = FakePeerStatistics(
        median_price=360.0,
        observations=12,
    )

    promo_result = engine.analyze(
        product=promo_product,
        profile=promo_profile,
        statistics=None,
        peer_statistics=promo_peers,
    )

    print_result(
        "TESTE 3 - PROMOÇÃO NORMAL",
        promo_result,
    )

    # ==========================================================
    # TESTE 4
    # PRODUTO NORMAL
    # ==========================================================

    normal_product = create_product(
        product_id="NORMAL001",
        title="RTX 5070 Produto Normal",
        price=5000.0,
        old_price=5200.0,
        official_store=True,
        full=True,
    )

    normal_profile = create_profile(
        product_id="NORMAL001",
        brand="ASUS",
        model="RTX 5070",
        broad_key="rtx_5070_12gb",
        tier_key=None,
        strict_key=(
            "asus_rtx_5070_12gb"
        ),
        identity_confidence="alta",
    )

    normal_peers = FakePeerStatistics(
        median_price=5100.0,
        observations=20,
    )

    normal_result = engine.analyze(
        product=normal_product,
        profile=normal_profile,
        statistics=None,
        peer_statistics=normal_peers,
    )

    print_result(
        "TESTE 4 - PREÇO NORMAL",
        normal_result,
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
        bug_result.should_notify
        is True
    )

    assert (
        bug_result.opportunity_type
        == "possivel_erro_preco"
    )

    assert (
        generic_result.should_notify
        is False
    )

    assert (
        generic_result.score
        < 70
    )

    assert (
        normal_result.should_notify
        is False
    )

    print(
        "✓ Produto bem identificado "
        "continua acionando FAST PATH"
    )

    print(
        "✓ Produto genérico muito barato "
        "não aciona FAST PATH sozinho"
    )

    print(
        "✓ Promoção comum continua "
        "sendo analisada normalmente"
    )

    print(
        "✓ Produto normal permanece normal"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
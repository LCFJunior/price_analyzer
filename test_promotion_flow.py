from pathlib import Path

from analyzers.bug_engine import (
    BugEngine,
)
from analyzers.opportunity_engine import (
    OpportunityEngine,
)
from analyzers.peer_price_analyzer import (
    PeerPriceAnalyzer,
)
from analyzers.product_filter import (
    ProductFilter,
)
from analyzers.promotion_engine import (
    PromotionEngine,
)

from database.database import (
    Database,
)
from database.notification_repository import (
    NotificationRepository,
)
from database.repository import (
    ProductRepository,
)

from entities.candidate_validation import (
    CandidateValidationResult,
)
from entities.product import (
    Product,
)
from entities.search_rule import (
    SearchRule,
)

from services.candidate_selector import (
    CandidateSelector,
)
from services.listing_validator import (
    ListingValidator,
)
from services.monitor_service import (
    MonitorService,
)
from services.product_classifier import (
    ProductClassifier,
)


class FakeCollector:
    """
    Simula uma coleta real.

    PROMO001 é o mesmo anúncio que possui
    histórico anterior no banco.

    Os outros produtos são anúncios do mesmo
    Samsung 9100 Pro e fornecem a referência
    de mercado por strict_key.
    """

    def search(
        self,
        query: str,
    ) -> list[Product]:
        print(
            f"Pesquisa simulada: {query}"
        )

        return [
            create_product(
                product_id="PROMO001",
                title=(
                    "SSD Samsung 9100 Pro "
                    "1TB NVMe Gen5 X4"
                ),
                price=1850.0,
                old_price=2600.0,
                official_store=True,
                full=True,
            ),

            create_product(
                product_id="PEER001",
                title=(
                    "SSD Samsung 9100 Pro "
                    "1TB NVMe PCIe Gen5"
                ),
                price=2450.0,
            ),

            create_product(
                product_id="PEER002",
                title=(
                    "SSD M.2 Samsung 9100 Pro "
                    "1TB NVMe Gen5x4"
                ),
                price=2500.0,
            ),

            create_product(
                product_id="PEER003",
                title=(
                    "SSD Samsung 9100 Pro "
                    "1TB NVMe Gen 5"
                ),
                price=2550.0,
            ),
        ]


class FakeCandidateValidator:
    def __init__(
        self,
    ) -> None:
        self.validations = 0

        self.validated_products: list[
            Product
        ] = []

    def validate(
        self,
        product: Product,
    ) -> CandidateValidationResult:
        self.validations += 1

        self.validated_products.append(
            product
        )

        print(
            "\nValidação profunda simulada:"
        )

        print(
            f"- {product.title}"
        )

        return CandidateValidationResult(
            status="valid",

            reasons=(
                "Produto validado no teste.",
            ),

            inspected_fields=(
                "titulo",
                "condicao",
                "descricao",
                "detalhes",
            ),
        )


class FakeNotifier:
    def __init__(
        self,
    ) -> None:
        self.messages_sent = 0

        self.received_opportunities = []

        self.received_products: list[
            Product
        ] = []

    def send_opportunity(
        self,
        opportunity,
    ) -> bool:
        self.messages_sent += 1

        self.received_opportunities.append(
            opportunity
        )

        self.received_products.append(
            opportunity.product
        )

        print(
            "\n"
            + "!" * 80
        )

        print(
            "FAKE TELEGRAM"
        )

        print(
            "!" * 80
        )

        print(
            "Produto: "
            f"{opportunity.product.title}"
        )

        print(
            "Preço: "
            f"R$ {opportunity.product.price:.2f}"
        )

        print(
            "Score: "
            f"{opportunity.score}/100"
        )

        print(
            "Tipo: "
            f"{opportunity.opportunity_type}"
        )

        print(
            "Confiança: "
            f"{opportunity.confidence}"
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

        return True


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

        official_store=(
            official_store
        ),

        full=full,

        shipping="Frete grátis",

        link=(
            f"https://teste.com/"
            f"{product_id}"
        ),

        image_url=None,

        international=False,
    )


def seed_promotion_history(
    repository: ProductRepository,
) -> None:
    """
    Cria três observações históricas anteriores
    à coleta promocional atual.

    Histórico:

    R$ 2.550
    R$ 2.500
    R$ 2.450

    Mediana esperada:
    R$ 2.500
    """

    historical_prices = (
        2550.0,
        2500.0,
        2450.0,
    )

    print(
        "\nPreparando histórico "
        "do PROMO001..."
    )

    for price in (
        historical_prices
    ):
        historical_product = (
            create_product(
                product_id="PROMO001",

                title=(
                    "SSD Samsung 9100 Pro "
                    "1TB NVMe Gen5 X4"
                ),

                price=price,

                old_price=None,

                official_store=True,

                full=True,
            )
        )

        repository.save_products(
            [
                historical_product
            ]
        )

        print(
            f"- R$ {price:.2f}"
        )

    print(
        "Histórico preparado."
    )


def main() -> None:
    database_path = Path(
        "database/test_promotion_flow.db"
    )

    if database_path.exists():
        database_path.unlink()

    database = Database(
        str(database_path)
    )

    product_repository = (
        ProductRepository(
            database
        )
    )

    notification_repository = (
        NotificationRepository(
            database
        )
    )

    # ==========================================================
    # PREPARA O HISTÓRICO
    # ==========================================================

    seed_promotion_history(
        product_repository
    )

    # Verificação de diagnóstico antes
    # da execução principal.
    baseline_before_run = (
        product_repository
        .get_baseline_statistics(
            product_id="PROMO001",
            marketplace="Mercado Livre",
        )
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "BASELINE ANTES DA COLETA"
    )

    print(
        "=" * 80
    )

    if baseline_before_run:
        print(
            "Observações consideradas: "
            f"{baseline_before_run.observations}"
        )

        print(
            "Mediana: "
            f"R$ {baseline_before_run.median_price:.2f}"
        )

        print(
            "Média: "
            f"R$ {baseline_before_run.average_price:.2f}"
        )

        print(
            "Menor: "
            f"R$ {baseline_before_run.minimum_price:.2f}"
        )

        print(
            "Maior: "
            f"R$ {baseline_before_run.maximum_price:.2f}"
        )

    # ==========================================================
    # SERVIÇOS FAKE
    # ==========================================================

    notifier = FakeNotifier()

    candidate_validator = (
        FakeCandidateValidator()
    )

    # ==========================================================
    # OPPORTUNITY ENGINE REAL
    # ==========================================================

    opportunity_engine = (
        OpportunityEngine(
            bug_engine=BugEngine(
                extreme_peer_drop_percent=60.0,

                strong_peer_drop_percent=45.0,

                extreme_history_drop_percent=55.0,

                # Temos somente 3 peers do
                # mesmo modelo neste teste.
                #
                # Dessa forma o BugEngine não
                # deve assumir que é BUG apenas
                # pela comparação.
                minimum_peer_observations=4,

                notification_threshold=70,
            ),

            promotion_engine=(
                PromotionEngine(
                    notification_threshold=70,

                    minimum_history_observations=3,
                )
            ),
        )
    )

    # ==========================================================
    # MONITOR SERVICE REAL
    # ==========================================================

    monitor_service = (
        MonitorService(
            collector=FakeCollector(),

            product_filter=(
                ProductFilter()
            ),

            listing_validator=(
                ListingValidator()
            ),

            candidate_validator=(
                candidate_validator
            ),

            classifier=(
                ProductClassifier()
            ),

            candidate_selector=(
                CandidateSelector()
            ),

            peer_analyzer=(
                PeerPriceAnalyzer(
                    minimum_strict_peers=1,

                    minimum_tier_peers=2,

                    minimum_broad_peers=4,
                )
            ),

            opportunity_engine=(
                opportunity_engine
            ),

            product_repository=(
                product_repository
            ),

            notification_repository=(
                notification_repository
            ),

            notifier=notifier,
        )
    )

    # ==========================================================
    # REGRA DE RELEVÂNCIA
    # ==========================================================

    rule = SearchRule(
        required_terms=(
            "samsung",
            "9100",
            "pro",
            "1tb",
        ),

        excluded_terms=(),

        minimum_price=None,

        maximum_price=None,

        require_official_store=False,

        require_full=False,
    )

    # ==========================================================
    # EXECUÇÃO
    # ==========================================================

    result = monitor_service.run(
        search_query=(
            "Samsung 9100 Pro 1TB"
        ),

        relevance_rule=rule,

        notifications_enabled=True,

        resend_after_hours=24,

        minimum_price_drop_percent=1.0,

        minimum_score_increase=15,
    )

    # ==========================================================
    # RESULTADO GERAL
    # ==========================================================

    print(
        "\n"
        + "=" * 80
    )

    print(
        "RESULTADO FINAL DO TESTE"
    )

    print(
        "=" * 80
    )

    print(
        "Produtos coletados: "
        f"{result.collected_count}"
    )

    print(
        "Produtos relevantes: "
        f"{result.relevant_count}"
    )

    print(
        "Produtos candidatos: "
        f"{result.candidate_count}"
    )

    print(
        "Produtos classificados: "
        f"{result.classified_count}"
    )

    print(
        "Oportunidades detectadas: "
        f"{result.detected_opportunities}"
    )

    print(
        "Validações profundas: "
        f"{result.deep_validations}"
    )

    print(
        "Bloqueados pela validação: "
        f"{result.validation_blocked}"
    )

    print(
        "Validações inconclusivas: "
        f"{result.validation_inconclusive}"
    )

    print(
        "Mensagens enviadas: "
        f"{result.sent_notifications}"
    )

    print(
        "Mensagens recebidas "
        "pelo FakeNotifier: "
        f"{notifier.messages_sent}"
    )

    print(
        "Notificações no banco: "
        f"{result.total_notifications_in_database}"
    )

    # ==========================================================
    # PRODUTOS
    # ==========================================================

    print(
        "\n"
        + "=" * 80
    )

    print(
        "PRODUTOS ANALISADOS"
    )

    print(
        "=" * 80
    )

    promo_analysis = None

    for analyzed in (
        result.analyzed_products
    ):
        opportunity = (
            analyzed.opportunity
        )

        product = (
            opportunity.product
        )

        print(
            "\n"
            + "-" * 80
        )

        print(
            "Produto: "
            f"{product.title}"
        )

        print(
            "ID: "
            f"{product.id}"
        )

        print(
            "Preço: "
            f"R$ {product.price:.2f}"
        )

        print(
            "Score: "
            f"{opportunity.score}/100"
        )

        print(
            "Tipo: "
            f"{opportunity.opportunity_type}"
        )

        print(
            "Confiança: "
            f"{opportunity.confidence}"
        )

        print(
            "Notificar: "
            f"{opportunity.should_notify}"
        )

        if (
            analyzed.profile
            is not None
        ):
            print(
                "Broad: "
                f"{analyzed.profile.broad_key}"
            )

            print(
                "Tier: "
                f"{analyzed.profile.tier_key}"
            )

            print(
                "Strict: "
                f"{analyzed.profile.strict_key}"
            )

        if (
            analyzed.historical_statistics
            is not None
        ):
            print(
                "Mediana histórica: "
                "R$ "
                f"{analyzed.historical_statistics.median_price:.2f}"
            )

            print(
                "Observações históricas: "
                f"{analyzed.historical_statistics.observations}"
            )

        if (
            analyzed.peer_statistics
            is not None
        ):
            print(
                "Escopo dos equivalentes: "
                f"{analyzed.peer_statistics.comparison_scope}"
            )

            print(
                "Mediana dos equivalentes: "
                "R$ "
                f"{analyzed.peer_statistics.median_price:.2f}"
            )

            print(
                "Anúncios equivalentes: "
                f"{analyzed.peer_statistics.observations}"
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

        if (
            analyzed.candidate_validation
            is not None
        ):
            print(
                "Validação profunda: "
                f"{analyzed.candidate_validation.status}"
            )

        print(
            "Telegram fake enviado: "
            f"{analyzed.notification_sent}"
        )

        if (
            analyzed.notification_reason
        ):
            print(
                "Decisão: "
                f"{analyzed.notification_reason}"
            )

        if (
            product.id
            == "PROMO001"
        ):
            promo_analysis = (
                analyzed
            )

    # ==========================================================
    # VERIFICAÇÕES AUTOMÁTICAS
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
        promo_analysis
        is not None
    ), (
        "PROMO001 deveria ter sido "
        "analisado."
    )

    assert (
        promo_analysis.opportunity
        .should_notify
        is True
    ), (
        "A promoção deveria gerar "
        "should_notify=True."
    )

    assert (
        promo_analysis.opportunity
        .opportunity_type
        == "promocao"
    ), (
        "PROMO001 deveria ser "
        "classificado como promocao."
    )

    assert (
        promo_analysis.opportunity.score
        >= 70
    ), (
        "A promoção deveria ter "
        "score >= 70."
    )

    assert (
        promo_analysis
        .historical_statistics
        is not None
    ), (
        "O histórico deveria ter "
        "sido recuperado."
    )

    assert (
        promo_analysis
        .historical_statistics
        .observations
        >= 3
    ), (
        "A promoção deveria possuir "
        "pelo menos 3 observações "
        "históricas utilizáveis."
    )

    assert (
        promo_analysis
        .peer_statistics
        is not None
    ), (
        "Deveria existir referência "
        "de produtos equivalentes."
    )

    assert (
        promo_analysis
        .peer_statistics
        .comparison_scope
        == "modelo_exato_nacional"
    ), (
        "A comparação deveria priorizar "
        "o mesmo modelo."
    )

    assert (
        result.detected_opportunities
        == 1
    ), (
        "Era esperada exatamente "
        "1 oportunidade."
    )

    assert (
        result.deep_validations
        == 1
    ), (
        "Era esperada exatamente "
        "1 validação profunda."
    )

    assert (
        candidate_validator.validations
        == 1
    ), (
        "FakeCandidateValidator deveria "
        "ser chamado uma única vez."
    )

    assert (
        result.validation_blocked
        == 0
    ), (
        "A promoção válida não deveria "
        "ser bloqueada."
    )

    assert (
        result.validation_inconclusive
        == 0
    ), (
        "A validação não deveria "
        "ser inconclusiva."
    )

    assert (
        result.sent_notifications
        == 1
    ), (
        "Era esperado exatamente "
        "1 envio."
    )

    assert (
        notifier.messages_sent
        == 1
    ), (
        "FakeNotifier deveria receber "
        "exatamente 1 mensagem."
    )

    assert (
        len(
            notifier.received_products
        )
        == 1
    )

    assert (
        notifier.received_products[
            0
        ].id
        == "PROMO001"
    ), (
        "O produto enviado deveria "
        "ser PROMO001."
    )

    assert (
        notifier.received_opportunities[
            0
        ].opportunity_type
        == "promocao"
    ), (
        "O FakeNotifier deveria receber "
        "uma promoção, não um bug."
    )

    assert (
        result.total_notifications_in_database
        == 1
    ), (
        "Deveria existir exatamente "
        "1 notificação registrada."
    )

    print(
        "✓ Histórico recuperado"
    )

    print(
        "✓ Comparação por modelo exato executada"
    )

    print(
        "✓ Promoção detectada"
    )

    print(
        "✓ PromotionEngine venceu o BugEngine"
    )

    print(
        "✓ Validação profunda executada"
    )

    print(
        "✓ Produto aprovado"
    )

    print(
        "✓ FakeNotifier acionado"
    )

    print(
        "✓ Somente a promoção foi enviada"
    )

    print(
        "✓ Notificação registrada no banco"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
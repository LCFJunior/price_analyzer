from pathlib import Path

from analyzers.bug_engine import BugEngine
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

from database.database import Database
from database.notification_repository import (
    NotificationRepository,
)
from database.repository import (
    ProductRepository,
)

from entities.candidate_validation import (
    CandidateValidationResult,
)
from entities.product import Product
from entities.search_rule import (
    SearchRule,
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
    def search(
        self,
        query: str,
    ) -> list[Product]:
        print(
            f"Pesquisa simulada: {query}"
        )

        return [
            create_product(
                product_id="NORMAL001",
                title=(
                    "Placa de Vídeo ASUS "
                    "RTX 5070 12GB"
                ),
                price=5200.0,
            ),

            create_product(
                product_id="NORMAL002",
                title=(
                    "Placa de Vídeo MSI "
                    "RTX 5070 12GB"
                ),
                price=5000.0,
            ),

            create_product(
                product_id="NORMAL003",
                title=(
                    "Placa de Vídeo Gigabyte "
                    "RTX 5070 12GB"
                ),
                price=5100.0,
            ),

            create_product(
                product_id="NORMAL004",
                title=(
                    "Placa de Vídeo Zotac "
                    "RTX 5070 12GB"
                ),
                price=4900.0,
            ),

            create_product(
                product_id="NORMAL005",
                title=(
                    "Placa de Vídeo Galax "
                    "RTX 5070 12GB"
                ),
                price=5300.0,
            ),

            create_product(
                product_id="BUG001",
                title=(
                    "Placa de Vídeo PNY "
                    "RTX 5070 12GB"
                ),
                price=900.0,
                official_store=True,
                full=True,
            ),
        ]


class FakeCandidateValidator:
    def validate(
        self,
        product: Product,
    ) -> CandidateValidationResult:
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
                "descricao",
                "detalhes",
            ),
        )


class FakeNotifier:
    def __init__(
        self,
    ) -> None:
        self.messages_sent = 0
        self.received_products = []

    def send_opportunity(
        self,
        opportunity,
    ) -> bool:
        self.messages_sent += 1

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
            f"Produto: "
            f"{opportunity.product.title}"
        )

        print(
            f"Preço: "
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
    official_store: bool = False,
    full: bool = False,
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=None,
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


def main() -> None:
    database_path = Path(
        "database/test_bug_flow.db"
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

    notifier = FakeNotifier()

    opportunity_engine = (
        OpportunityEngine(
            bug_engine=BugEngine(
                extreme_peer_drop_percent=60.0,
                strong_peer_drop_percent=45.0,
                extreme_history_drop_percent=55.0,
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
                FakeCandidateValidator()
            ),

            classifier=(
                ProductClassifier()
            ),

            peer_analyzer=(
                PeerPriceAnalyzer(
                    minimum_strict_peers=2,
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

    rule = SearchRule(
        required_terms=(
            "rtx",
            "5070",
        ),

        excluded_terms=(),

        minimum_price=None,

        maximum_price=None,

        require_official_store=False,

        require_full=False,
    )

    result = monitor_service.run(
        search_query="RTX 5070",

        relevance_rule=rule,

        candidate_rule=rule,

        resend_after_hours=24,

        minimum_price_drop_percent=1.0,

        minimum_score_increase=15,
    )

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

    for analyzed in (
        result.analyzed_products
    ):
        opportunity = (
            analyzed.opportunity
        )

        print(
            "\n"
            + "-" * 80
        )

        print(
            f"Produto: "
            f"{opportunity.product.title}"
        )

        print(
            f"Preço: "
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
            "Notificar: "
            f"{opportunity.should_notify}"
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

    # ==========================================================
    # ASSERTS
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
        result.validation_blocked
        == 0
    ), (
        "O produto válido não deveria "
        "ser bloqueado."
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
        "1 mensagem."
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
        == "BUG001"
    ), (
        "O produto enviado deveria "
        "ser BUG001."
    )

    print(
        "✓ Bug detectado"
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
        "✓ Notificação registrada "
        "no banco"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
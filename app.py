from analyzers.bug_engine import BugEngine
from analyzers.opportunity_engine import OpportunityEngine
from analyzers.peer_price_analyzer import PeerPriceAnalyzer
from analyzers.product_filter import ProductFilter
from analyzers.promotion_engine import PromotionEngine

from browser.browser import Browser

from config.monitoring_targets import get_monitoring_targets
from config.settings import Settings

from database.database import Database
from database.notification_repository import NotificationRepository
from database.repository import ProductRepository

from entities.batch_monitor_result import (
    BatchMonitorResult,
    TargetMonitorResult,
)
from entities.monitor_result import (
    AnalyzedProduct,
    MonitorResult,
)

from marketplaces.mercadolivre.collector import (
    MercadoLivreCollector,
)

from notifications.telegram import TelegramNotifier

from services.batch_monitor_service import BatchMonitorService
from services.candidate_selector import CandidateSelector
from services.listing_validator import ListingValidator
from services.monitor_service import MonitorService
from services.product_classifier import ProductClassifier

from validators.mercadolivre_candidate_validator import (
    MercadoLivreCandidateValidator,
)


def main() -> None:
    browser = Browser()
    settings = Settings.load()

    playwright = None
    context = None

    try:
        settings.validate_telegram()

        database = Database()

        product_repository = ProductRepository(
            database
        )

        notification_repository = NotificationRepository(
            database
        )

        notifier = TelegramNotifier(
            bot_token=settings.telegram_bot_token,
            chat_id=settings.telegram_chat_id,
            enabled=settings.telegram_enabled,
        )

        (
            playwright,
            context,
            page,
        ) = browser.open()

        collector = MercadoLivreCollector(
            page
        )

        candidate_validator = (
            MercadoLivreCandidateValidator(
                context
            )
        )

        opportunity_engine = OpportunityEngine(
            bug_engine=BugEngine(
                extreme_peer_drop_percent=60.0,
                strong_peer_drop_percent=45.0,
                extreme_history_drop_percent=55.0,
                minimum_peer_observations=4,
                notification_threshold=70,
            ),

            promotion_engine=PromotionEngine(
                notification_threshold=70,
                minimum_history_observations=3,
            ),
        )

        monitor_service = MonitorService(
            collector=collector,

            product_filter=ProductFilter(),

            listing_validator=ListingValidator(),

            candidate_validator=(
                candidate_validator
            ),

            classifier=ProductClassifier(),

            candidate_selector=CandidateSelector(),

            peer_analyzer=PeerPriceAnalyzer(
                minimum_strict_peers=1,
                minimum_tier_peers=2,
                minimum_broad_peers=6,
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

        batch_service = BatchMonitorService(
            monitor_service
        )

        targets = (
            get_monitoring_targets()
        )

        batch_result = batch_service.run(
            targets=targets,
            resend_after_hours=24,
            minimum_price_drop_percent=1.0,
            minimum_score_increase=15,
        )

        print_batch_result(
            batch_result
        )

        input(
            "\nPressione ENTER para finalizar..."
        )

    finally:
        if context is not None:
            context.close()

        if playwright is not None:
            playwright.stop()


def print_batch_result(
    batch_result: BatchMonitorResult,
) -> None:
    for target_result in (
        batch_result.target_results
    ):
        print_target_result(
            target_result
        )

    print("\n" + "=" * 80)
    print("RESUMO GERAL")
    print("=" * 80)

    print(
        "Monitoramentos executados: "
        f"{batch_result.executed_targets}"
    )

    print(
        "Monitoramentos concluídos: "
        f"{batch_result.successful_targets}"
    )

    print(
        "Monitoramentos com falha: "
        f"{batch_result.failed_targets}"
    )

    print(
        "Produtos coletados: "
        f"{batch_result.total_collected}"
    )

    print(
        "Produtos aprovados pelo filtro inicial: "
        f"{batch_result.total_filtered_relevant}"
    )

    print(
        "Anúncios rejeitados pelo validador: "
        f"{batch_result.total_rejected}"
    )

    print(
        "Produtos relevantes válidos: "
        f"{batch_result.total_relevant}"
    )

    print(
        "Produtos classificados: "
        f"{batch_result.total_classified}"
    )

    print(
        "Produtos não classificados: "
        f"{batch_result.total_unclassified}"
    )

    print(
        "Produtos candidatos: "
        f"{batch_result.total_candidates}"
    )

    print(
        "Observações salvas: "
        f"{batch_result.total_saved_observations}"
    )

    print(
        "Oportunidades detectadas: "
        f"{batch_result.total_detected_opportunities}"
    )

    print(
        "Validações profundas executadas: "
        f"{batch_result.total_deep_validations}"
    )

    print(
        "Bloqueados pela validação profunda: "
        f"{batch_result.total_validation_blocked}"
    )

    print(
        "Validações inconclusivas: "
        f"{batch_result.total_validation_inconclusive}"
    )

    print(
        "Alertas duplicados bloqueados: "
        f"{batch_result.total_blocked_notifications}"
    )

    print(
        "Mensagens enviadas: "
        f"{batch_result.total_sent_notifications}"
    )


def print_target_result(
    target_result: TargetMonitorResult,
) -> None:
    target = target_result.target

    print("\n" + "=" * 80)
    print(
        f"RESULTADO: {target.name}"
    )
    print("=" * 80)

    if not target_result.success:
        print(
            "Monitoramento não concluído."
        )

        print(
            "Erro: "
            f"{target_result.error_message}"
        )

        return

    if target_result.result is None:
        print(
            "Resultado não disponível."
        )

        return

    print_monitor_result(
        target_result.result
    )


def print_monitor_result(
    result: MonitorResult,
) -> None:
    for analyzed_product in (
        result.analyzed_products
    ):
        print_analyzed_product(
            analyzed_product
        )

    if result.unclassified_products:
        print(
            "\n"
            + "?" * 80
        )

        print(
            "PRODUTOS NÃO CLASSIFICADOS"
        )

        print(
            "?" * 80
        )

        for product in (
            result.unclassified_products
        ):
            print(
                f"\n- {product.title}"
            )

            print(
                "  Preço: "
                f"{format_price(
                    product.price
                )}"
            )

            print(
                f"  ID: {product.id}"
            )

            print(
                f"  Link: {product.link}"
            )

    print(
        "\n"
        + "-" * 80
    )

    print(
        "RESUMO DO MONITORAMENTO"
    )

    print("-" * 80)

    print(
        "Produtos encontrados: "
        f"{result.collected_count}"
    )

    print(
        "Aprovados pelo filtro inicial: "
        f"{result.filtered_relevant_count}"
    )

    print(
        "Rejeitados pelo validador: "
        f"{result.rejected_count}"
    )

    print(
        "Produtos relevantes válidos: "
        f"{result.relevant_count}"
    )

    print(
        "Produtos classificados: "
        f"{result.classified_count}"
    )

    print(
        "Produtos não classificados: "
        f"{result.unclassified_count}"
    )

    print(
        "Produtos candidatos: "
        f"{result.candidate_count}"
    )

    print(
        "Observações salvas: "
        f"{result.saved_observations}"
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
        "Alertas duplicados: "
        f"{result.blocked_notifications}"
    )

    print(
        "Mensagens enviadas: "
        f"{result.sent_notifications}"
    )

    print(
        "Notificações no banco: "
        f"{result.total_notifications_in_database}"
    )


def print_analyzed_product(
    analyzed: AnalyzedProduct,
) -> None:
    opportunity = (
        analyzed.opportunity
    )

    product = (
        opportunity.product
    )

    profile = (
        analyzed.profile
    )

    historical = (
        analyzed.historical_statistics
    )

    peers = (
        analyzed.peer_statistics
    )

    validation = (
        analyzed.candidate_validation
    )

    print("\n" + "-" * 80)

    print(
        f"Produto: {product.title}"
    )

    print(
        "Preço: "
        f"{format_price(product.price)}"
    )

    print(
        "Origem: "
        f"{'Internacional' if product.international else 'Nacional'}"
    )

    if profile is not None:
        print(
            "Classificação geral: "
            f"{profile.broad_key or 'Não identificada'}"
        )

        print(
            "Classificação específica: "
            f"{profile.strict_key or 'Não identificada'}"
        )

        print(
            "Marca: "
            f"{profile.brand or 'Não identificada'}"
        )

        print(
            "Modelo: "
            f"{profile.model or 'Não identificado'}"
        )

        print(
            "Memória: "
            f"{profile.memory_gb or 'Não identificada'}"
        )

        identity_confidence = (
            profile.attributes.get(
                "identity_confidence"
            )
        )

        if identity_confidence:
            print(
                "Confiança da identidade: "
                f"{identity_confidence}"
            )

    print(
        f"Score: {opportunity.score}/100"
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
        f"{'Sim' if opportunity.should_notify else 'Não'}"
    )

    if (
        opportunity.opportunity_type
        == "possivel_erro_preco"
    ):
        print(
            "FAST PATH: "
            "possível bug de preço"
        )

    if historical is not None:
        print(
            "Mediana histórica: "
            f"{format_price(
                historical.median_price
            )}"
        )

        print(
            "Média histórica: "
            f"{format_price(
                historical.average_price
            )}"
        )

        print(
            "Menor preço histórico: "
            f"{format_price(
                historical.minimum_price
            )}"
        )

        print(
            "Observações históricas: "
            f"{historical.observations}"
        )

    if peers is not None:
        print(
            "Escopo dos equivalentes: "
            f"{peers.comparison_scope}"
        )

        print(
            "Chave dos equivalentes: "
            f"{peers.comparison_key}"
        )

        print(
            "Mediana dos equivalentes: "
            f"{format_price(
                peers.median_price
            )}"
        )

        print(
            "Média dos equivalentes: "
            f"{format_price(
                peers.average_price
            )}"
        )

        print(
            "Menor preço equivalente: "
            f"{format_price(
                peers.minimum_price
            )}"
        )

        print(
            "Maior preço equivalente: "
            f"{format_price(
                peers.maximum_price
            )}"
        )

        print(
            "Anúncios equivalentes: "
            f"{peers.observations}"
        )

    if opportunity.reasons:
        print("Motivos:")

        for reason in (
            opportunity.reasons
        ):
            print(
                f"- {reason}"
            )

    if validation is not None:
        print(
            "Validação profunda: "
            f"{validation.status}"
        )

        if validation.inspected_fields:
            print(
                "Campos verificados: "
                + ", ".join(
                    validation.inspected_fields
                )
            )

        for reason in (
            validation.reasons
        ):
            print(
                f"- {reason}"
            )

    if analyzed.notification_reason:
        print(
            "Decisão de notificação: "
            f"{analyzed.notification_reason}"
        )

    if analyzed.notification_sent:
        print(
            "Telegram: mensagem enviada."
        )

    if analyzed.notification_blocked:
        print(
            "Telegram: envio bloqueado."
        )

    print(
        "Link: "
        f"{product.link or 'Não informado'}"
    )


def format_price(
    price: float | None,
) -> str:
    if price is None:
        return "Não informado"

    formatted = (
        f"{price:,.2f}"
    )

    formatted = (
        formatted.replace(
            ",",
            "_",
        )
    )

    formatted = (
        formatted.replace(
            ".",
            ",",
        )
    )

    formatted = (
        formatted.replace(
            "_",
            ".",
        )
    )

    return (
        f"R$ {formatted}"
    )


if __name__ == "__main__":
    main()
from analyzers.opportunity_engine import (
    OpportunityEngine,
)
from analyzers.peer_price_analyzer import (
    PeerPriceAnalyzer,
)
from analyzers.product_filter import (
    ProductFilter,
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
from entities.monitor_result import (
    AnalyzedProduct,
    MonitorResult,
)
from entities.search_rule import (
    SearchRule,
)

from marketplaces.base_collector import (
    MarketplaceCollector,
)

from notifications.telegram import (
    TelegramNotifier,
)

from services.candidate_selector import (
    CandidateSelector,
)
from services.listing_validator import (
    ListingValidator,
)
from services.product_classifier import (
    ProductClassifier,
)

from validators.base_candidate_validator import (
    CandidateValidator,
)


class MonitorService:
    def __init__(
        self,
        *,
        collector: MarketplaceCollector,
        product_filter: ProductFilter,
        listing_validator: ListingValidator,
        candidate_validator: CandidateValidator,
        classifier: ProductClassifier,
        candidate_selector: CandidateSelector,
        peer_analyzer: PeerPriceAnalyzer,
        opportunity_engine: OpportunityEngine,
        product_repository: ProductRepository,
        notification_repository: NotificationRepository,
        notifier: TelegramNotifier,
    ):
        self.collector = collector

        self.product_filter = (
            product_filter
        )

        self.listing_validator = (
            listing_validator
        )

        self.candidate_validator = (
            candidate_validator
        )

        self.classifier = classifier

        self.candidate_selector = (
            candidate_selector
        )

        self.peer_analyzer = (
            peer_analyzer
        )

        self.opportunity_engine = (
            opportunity_engine
        )

        self.product_repository = (
            product_repository
        )

        self.notification_repository = (
            notification_repository
        )

        self.notifier = notifier

    def run(
        self,
        *,
        search_query: str,
        relevance_rule: SearchRule,
        notifications_enabled: bool = True,
        resend_after_hours: int = 24,
        minimum_price_drop_percent: float = 1.0,
        minimum_score_increase: int = 15,
    ) -> MonitorResult:
        # ======================================================
        # COLETA
        # ======================================================

        collected_products = (
            self.collector.search(
                search_query
            )
        )

        # ======================================================
        # FILTRO DE RELEVÂNCIA
        # ======================================================

        filtered_relevant_products = (
            self.product_filter.filter(
                collected_products,
                relevance_rule,
            )
        )

        # ======================================================
        # VALIDAÇÃO SUPERFICIAL
        # ======================================================

        (
            relevant_products,
            rejected_products,
        ) = (
            self.listing_validator
            .filter_valid(
                filtered_relevant_products
            )
        )

        self._print_rejected_products(
            rejected_products
        )

        # ======================================================
        # CLASSIFICAÇÃO
        # ======================================================

        profiles = (
            self.classifier.classify_many(
                relevant_products
            )
        )

        (
            classified_products,
            unclassified_products,
        ) = self._split_classified_products(
            relevant_products=(
                relevant_products
            ),
            profiles=profiles,
        )

        # ======================================================
        # SELEÇÃO DINÂMICA DE CANDIDATOS
        #
        # Não existe mais maximum_price.
        # ======================================================

        candidate_products = (
            self.candidate_selector.select(
                products=(
                    relevant_products
                ),
                profiles=profiles,
            )
        )

        # ======================================================
        # HISTÓRICO ANTES DE SALVAR A OBSERVAÇÃO ATUAL
        # ======================================================

        historical_statistics_by_product = {}

        for product in candidate_products:
            historical_statistics_by_product[
                product.id
            ] = (
                self.product_repository
                .get_baseline_statistics(
                    product_id=(
                        product.id
                    ),
                    marketplace=(
                        product.marketplace
                    ),
                )
            )

        # ======================================================
        # SALVA OBSERVAÇÃO ATUAL
        # ======================================================

        saved_observations = (
            self.product_repository
            .save_products(
                relevant_products
            )
        )

        analyzed_products: list[
            AnalyzedProduct
        ] = []

        detected_opportunities = 0

        deep_validations = 0

        validation_blocked = 0

        validation_inconclusive = 0

        sent_notifications = 0

        blocked_notifications = 0

        # ======================================================
        # ANÁLISE DOS CANDIDATOS
        # ======================================================

        for product in candidate_products:
            historical_statistics = (
                historical_statistics_by_product
                .get(
                    product.id
                )
            )

            profile = profiles.get(
                product.id
            )

            peer_statistics = (
                self.peer_analyzer
                .get_product_statistics(
                    product=product,
                    products=(
                        relevant_products
                    ),
                    profiles=profiles,
                )
            )

            opportunity = (
                self.opportunity_engine
                .analyze(
                    product=product,
                    profile=profile,
                    statistics=(
                        historical_statistics
                    ),
                    peer_statistics=(
                        peer_statistics
                    ),
                )
            )

            candidate_validation: (
                CandidateValidationResult | None
            ) = None

            notification_sent = False

            notification_blocked = False

            notification_reason: (
                str | None
            ) = None

            # ==================================================
            # SOMENTE OPORTUNIDADES FORTES
            # VÃO PARA VALIDAÇÃO PROFUNDA
            # ==================================================

            if opportunity.should_notify:
                detected_opportunities += 1

                deep_validations += 1

                candidate_validation = (
                    self.candidate_validator
                    .validate(
                        product
                    )
                )

                if (
                    candidate_validation
                    .is_invalid
                ):
                    validation_blocked += 1

                    notification_blocked = (
                        True
                    )

                    notification_reason = (
                        "Bloqueado pela validação "
                        "profunda: "
                        + "; ".join(
                            candidate_validation
                            .reasons
                        )
                    )

                elif (
                    candidate_validation
                    .is_inconclusive
                ):
                    validation_inconclusive += 1

                    notification_blocked = (
                        True
                    )

                    notification_reason = (
                        "Validação profunda "
                        "inconclusiva: "
                        + "; ".join(
                            candidate_validation
                            .reasons
                        )
                    )

                elif not notifications_enabled:
                    notification_blocked = (
                        True
                    )

                    blocked_notifications += 1

                    notification_reason = (
                        "Target em modo observação: "
                        "notificações desativadas."
                    )

                else:
                    (
                        should_send,
                        notification_reason,
                    ) = (
                        self.notification_repository
                        .should_send(
                            opportunity=(
                                opportunity
                            ),
                            resend_after_hours=(
                                resend_after_hours
                            ),
                            minimum_price_drop_percent=(
                                minimum_price_drop_percent
                            ),
                            minimum_score_increase=(
                                minimum_score_increase
                            ),
                        )
                    )

                    if should_send:
                        try:
                            (
                                self.notifier
                                .send_opportunity(
                                    opportunity
                                )
                            )

                            (
                                self.notification_repository
                                .save_notification(
                                    opportunity
                                )
                            )

                            notification_sent = (
                                True
                            )

                            sent_notifications += 1

                        except Exception as error:
                            notification_reason = (
                                "Falha ao enviar "
                                "notificação: "
                                f"{type(error).__name__}: "
                                f"{error}"
                            )

                    else:
                        notification_blocked = (
                            True
                        )

                        blocked_notifications += 1

            analyzed_products.append(
                AnalyzedProduct(
                    opportunity=opportunity,

                    profile=profile,

                    historical_statistics=(
                        historical_statistics
                    ),

                    peer_statistics=(
                        peer_statistics
                    ),

                    candidate_validation=(
                        candidate_validation
                    ),

                    notification_sent=(
                        notification_sent
                    ),

                    notification_blocked=(
                        notification_blocked
                    ),

                    notification_reason=(
                        notification_reason
                    ),
                )
            )

        # ======================================================
        # ORDENA DIAGNÓSTICO
        # ======================================================

        analyzed_products.sort(
            key=lambda item: (
                item.opportunity
                .should_notify,

                item.opportunity.score,

                -(
                    item.opportunity
                    .product.price
                    or float("inf")
                ),
            ),
            reverse=True,
        )

        # ======================================================
        # RESULTADO
        # ======================================================

        return MonitorResult(
            collected_count=len(
                collected_products
            ),

            filtered_relevant_count=len(
                filtered_relevant_products
            ),

            rejected_count=len(
                rejected_products
            ),

            relevant_count=len(
                relevant_products
            ),

            candidate_count=len(
                candidate_products
            ),

            classified_count=len(
                classified_products
            ),

            unclassified_count=len(
                unclassified_products
            ),

            saved_observations=(
                saved_observations
            ),

            detected_opportunities=(
                detected_opportunities
            ),

            deep_validations=(
                deep_validations
            ),

            validation_blocked=(
                validation_blocked
            ),

            validation_inconclusive=(
                validation_inconclusive
            ),

            sent_notifications=(
                sent_notifications
            ),

            blocked_notifications=(
                blocked_notifications
            ),

            total_notifications_in_database=(
                self.notification_repository
                .count_notifications()
            ),

            unclassified_products=(
                unclassified_products
            ),

            analyzed_products=(
                analyzed_products
            ),
        )

    @staticmethod
    def _split_classified_products(
        *,
        relevant_products,
        profiles,
    ):
        classified_products = []

        unclassified_products = []

        for product in relevant_products:
            profile = profiles.get(
                product.id
            )

            if (
                profile is not None
                and profile.broad_key
            ):
                classified_products.append(
                    product
                )

                continue

            unclassified_products.append(
                product
            )

        return (
            classified_products,
            unclassified_products,
        )

    @staticmethod
    def _print_rejected_products(
        rejected_products,
    ) -> None:
        if not rejected_products:
            return

        print(
            "\n"
            + "!" * 80
        )

        print(
            "ANÚNCIOS DESCARTADOS "
            "PELO VALIDADOR"
        )

        print(
            "!" * 80
        )

        for (
            product_id,
            validation,
        ) in rejected_products.items():
            print(
                f"\nAnúncio: "
                f"{product_id}"
            )

            for reason in (
                validation.reasons
            ):
                print(
                    f"- {reason}"
                )
from entities.batch_monitor_result import (
    BatchMonitorResult,
    TargetMonitorResult,
)

from entities.monitoring_target import (
    MonitoringTarget,
)

from services.monitor_service import (
    MonitorService,
)


class BatchMonitorService:
    def __init__(
        self,
        monitor_service: MonitorService,
    ):
        self.monitor_service = (
            monitor_service
        )

    def run(
        self,
        *,
        targets: list[
            MonitoringTarget
        ],
        resend_after_hours: int = 24,
        minimum_price_drop_percent: float = 1.0,
        minimum_score_increase: int = 15,
    ) -> BatchMonitorResult:
        target_results: list[
            TargetMonitorResult
        ] = []

        executed_targets = 0
        successful_targets = 0
        failed_targets = 0

        total_collected = 0
        total_filtered_relevant = 0
        total_rejected = 0
        total_relevant = 0
        total_candidates = 0
        total_classified = 0
        total_unclassified = 0
        total_saved_observations = 0

        total_detected_opportunities = 0
        total_deep_validations = 0
        total_validation_blocked = 0
        total_validation_inconclusive = 0
        total_sent_notifications = 0
        total_blocked_notifications = 0

        for target in targets:
            if not target.enabled:
                continue

            executed_targets += 1

            print(
                "\n"
                + "#" * 80
            )

            print(
                "MONITORAMENTO: "
                f"{target.name}"
            )

            print(
                "BUSCA: "
                f"{target.search_query}"
            )

            print(
                "NOTIFICAÇÕES: "
                f"{'ATIVAS' if target.notifications_enabled else 'OBSERVAÇÃO'}"
            )

            print(
                "#" * 80
            )

            try:
                result = (
                    self.monitor_service
                    .run(
                        search_query=(
                            target.search_query
                        ),

                        relevance_rule=(
                            target.relevance_rule
                        ),

                        notifications_enabled=(
                            target.notifications_enabled
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

                successful_targets += 1

                total_collected += (
                    result.collected_count
                )

                total_filtered_relevant += (
                    result.filtered_relevant_count
                )

                total_rejected += (
                    result.rejected_count
                )

                total_relevant += (
                    result.relevant_count
                )

                total_candidates += (
                    result.candidate_count
                )

                total_classified += (
                    result.classified_count
                )

                total_unclassified += (
                    result.unclassified_count
                )

                total_saved_observations += (
                    result.saved_observations
                )

                total_detected_opportunities += (
                    result.detected_opportunities
                )

                total_deep_validations += (
                    result.deep_validations
                )

                total_validation_blocked += (
                    result.validation_blocked
                )

                total_validation_inconclusive += (
                    result.validation_inconclusive
                )

                total_sent_notifications += (
                    result.sent_notifications
                )

                total_blocked_notifications += (
                    result.blocked_notifications
                )

                target_results.append(
                    TargetMonitorResult(
                        target=target,
                        result=result,
                        success=True,
                    )
                )

            except Exception as error:
                failed_targets += 1

                error_message = (
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                print(
                    "\nFalha ao executar "
                    f"'{target.name}': "
                    f"{error_message}"
                )

                target_results.append(
                    TargetMonitorResult(
                        target=target,
                        result=None,
                        success=False,
                        error_message=(
                            error_message
                        ),
                    )
                )

        return BatchMonitorResult(
            executed_targets=(
                executed_targets
            ),

            successful_targets=(
                successful_targets
            ),

            failed_targets=(
                failed_targets
            ),

            total_collected=(
                total_collected
            ),

            total_filtered_relevant=(
                total_filtered_relevant
            ),

            total_rejected=(
                total_rejected
            ),

            total_relevant=(
                total_relevant
            ),

            total_candidates=(
                total_candidates
            ),

            total_classified=(
                total_classified
            ),

            total_unclassified=(
                total_unclassified
            ),

            total_saved_observations=(
                total_saved_observations
            ),

            total_detected_opportunities=(
                total_detected_opportunities
            ),

            total_deep_validations=(
                total_deep_validations
            ),

            total_validation_blocked=(
                total_validation_blocked
            ),

            total_validation_inconclusive=(
                total_validation_inconclusive
            ),

            total_sent_notifications=(
                total_sent_notifications
            ),

            total_blocked_notifications=(
                total_blocked_notifications
            ),

            target_results=(
                target_results
            ),
        )
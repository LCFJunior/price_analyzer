from dataclasses import dataclass, field

from entities.monitor_result import (
    MonitorResult,
)
from entities.monitoring_target import (
    MonitoringTarget,
)


@dataclass(frozen=True)
class TargetMonitorResult:
    target: MonitoringTarget

    result: MonitorResult | None

    success: bool

    error_message: str | None = None


@dataclass(frozen=True)
class BatchMonitorResult:
    executed_targets: int

    successful_targets: int

    failed_targets: int

    total_collected: int

    total_filtered_relevant: int

    total_rejected: int

    total_relevant: int

    total_candidates: int

    total_classified: int

    total_unclassified: int

    total_saved_observations: int

    total_detected_opportunities: int

    total_deep_validations: int

    total_validation_blocked: int

    total_validation_inconclusive: int

    total_sent_notifications: int

    total_blocked_notifications: int

    target_results: list[
        TargetMonitorResult
    ] = field(
        default_factory=list
    )
from dataclasses import dataclass, field

from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)
from database.repository import (
    PriceStatistics,
)
from entities.candidate_validation import (
    CandidateValidationResult,
)
from entities.opportunity import Opportunity
from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)


@dataclass(frozen=True)
class AnalyzedProduct:
    opportunity: Opportunity

    profile: ProductProfile | None

    historical_statistics: (
        PriceStatistics | None
    )

    peer_statistics: (
        PeerPriceStatistics | None
    )

    candidate_validation: (
        CandidateValidationResult | None
    ) = None

    notification_sent: bool = False

    notification_blocked: bool = False

    notification_reason: str | None = None


@dataclass(frozen=True)
class MonitorResult:
    collected_count: int

    filtered_relevant_count: int

    rejected_count: int

    relevant_count: int

    candidate_count: int

    classified_count: int

    unclassified_count: int

    saved_observations: int

    detected_opportunities: int

    deep_validations: int

    validation_blocked: int

    validation_inconclusive: int

    sent_notifications: int

    blocked_notifications: int

    total_notifications_in_database: int

    unclassified_products: list[
        Product
    ] = field(
        default_factory=list
    )

    analyzed_products: list[
        AnalyzedProduct
    ] = field(
        default_factory=list
    )
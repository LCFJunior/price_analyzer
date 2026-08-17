from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from database.database import Database
from entities.opportunity import Opportunity


@dataclass(frozen=True)
class NotificationRecord:
    product_id: str
    marketplace: str

    price: float
    score: int
    opportunity_type: str
    confidence: str

    sent_at: datetime


class NotificationRepository:
    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def should_send(
        self,
        opportunity: Opportunity,
        resend_after_hours: int = 24,
        minimum_price_drop_percent: float = 1.0,
        minimum_score_increase: int = 15,
    ) -> tuple[bool, str]:
        product = opportunity.product

        if (
            not product.id
            or not product.marketplace
            or product.price is None
            or product.price <= 0
        ):
            return (
                False,
                "Oportunidade sem dados válidos",
            )

        last_notification = self.get_last_notification(
            product_id=product.id,
            marketplace=product.marketplace,
        )

        if last_notification is None:
            return (
                True,
                "Primeiro alerta deste anúncio",
            )

        price_drop = self._calculate_price_drop(
            current_price=product.price,
            previous_price=last_notification.price,
        )

        if (
            price_drop is not None
            and price_drop
            >= minimum_price_drop_percent
        ):
            return (
                True,
                "Preço caiu desde o último alerta: "
                f"{price_drop:.1f}%",
            )

        score_increase = (
            opportunity.score
            - last_notification.score
        )

        if (
            score_increase
            >= minimum_score_increase
        ):
            return (
                True,
                "Score aumentou desde o último alerta: "
                f"+{score_increase}",
            )

        now = datetime.now(
            timezone.utc
        )

        elapsed = (
            now - last_notification.sent_at
        )

        if elapsed >= timedelta(
            hours=resend_after_hours
        ):
            return (
                True,
                "Período mínimo para reenvio atingido",
            )

        return (
            False,
            "Alerta duplicado: mesmo preço "
            "e score semelhante",
        )

    def save_notification(
        self,
        opportunity: Opportunity,
    ) -> None:
        product = opportunity.product

        if product.price is None:
            raise ValueError(
                "Não é possível salvar alerta "
                "sem preço."
            )

        with self.database.connect() as connection:
            connection.execute(
                """
                INSERT INTO notification_history (
                    product_id,
                    marketplace,
                    price,
                    score,
                    opportunity_type,
                    confidence
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    product.id,
                    product.marketplace,
                    product.price,
                    opportunity.score,
                    opportunity.opportunity_type,
                    opportunity.confidence,
                ),
            )

    def get_last_notification(
        self,
        product_id: str,
        marketplace: str,
    ) -> NotificationRecord | None:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    product_id,
                    marketplace,
                    price,
                    score,
                    opportunity_type,
                    confidence,
                    sent_at
                FROM notification_history
                WHERE product_id = ?
                  AND marketplace = ?
                ORDER BY
                    sent_at DESC,
                    notification_id DESC
                LIMIT 1
                """,
                (
                    product_id,
                    marketplace,
                ),
            ).fetchone()

        if row is None:
            return None

        sent_at = datetime.fromisoformat(
            row["sent_at"]
        )

        if sent_at.tzinfo is None:
            sent_at = sent_at.replace(
                tzinfo=timezone.utc
            )

        return NotificationRecord(
            product_id=row["product_id"],
            marketplace=row["marketplace"],
            price=float(row["price"]),
            score=int(row["score"]),
            opportunity_type=row[
                "opportunity_type"
            ],
            confidence=row["confidence"],
            sent_at=sent_at,
        )

    def count_notifications(self) -> int:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM notification_history
                """
            ).fetchone()

        return int(row["total"])

    @staticmethod
    def _calculate_price_drop(
        current_price: float,
        previous_price: float,
    ) -> float | None:
        if (
            current_price <= 0
            or previous_price <= 0
        ):
            return None

        if current_price >= previous_price:
            return 0.0

        return round(
            (
                (
                    previous_price
                    - current_price
                )
                / previous_price
            )
            * 100,
            2,
        )
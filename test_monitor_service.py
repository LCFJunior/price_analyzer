from pathlib import Path

from analyzers.peer_price_analyzer import (
    PeerPriceAnalyzer,
)
from analyzers.price_analyzer import PriceAnalyzer
from analyzers.product_filter import ProductFilter
from database.database import Database
from database.notification_repository import (
    NotificationRepository,
)
from database.repository import ProductRepository
from entities.product import Product
from entities.search_rule import SearchRule
from services.monitor_service import MonitorService
from services.product_classifier import ProductClassifier


class FakeCollector:
    def search(
        self,
        query: str,
    ) -> list[Product]:
        print(f"Pesquisa simulada: {query}")

        return [
            create_product(
                "MLB001",
                "RTX 5070 MSI Ventus 12GB",
                5000.0,
            ),
            create_product(
                "MLB002",
                "RTX 5070 MSI Shadow 12GB",
                5100.0,
            ),
            create_product(
                "MLB003",
                "RTX 5070 ASUS Dual 12GB",
                5200.0,
            ),
            create_product(
                "MLB004",
                "RTX 5070 Gigabyte Windforce 12GB",
                4900.0,
            ),
            create_product(
                "MLB005",
                "RTX 5070 Galax 12GB",
                5150.0,
            ),
            create_product(
                "MLB_BUG",
                "RTX 5070 Zotac 12GB",
                1999.0,
            ),
        ]


class FakeNotifier:
    def __init__(self):
        self.messages_sent = 0

    def send_opportunity(
        self,
        opportunity,
    ) -> bool:
        self.messages_sent += 1

        print(
            "Notificação simulada: "
            f"{opportunity.product.title}"
        )

        return True


def create_product(
    product_id: str,
    title: str,
    price: float,
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
        official_store=True,
        full=True,
        shipping="Frete grátis",
        link=f"https://teste.com/{product_id}",
        image_url=None,
    )


def main() -> None:
    database_path = Path(
        "database/test_monitor_service.db"
    )

    if database_path.exists():
        database_path.unlink()

    database = Database(
        str(database_path)
    )

    notifier = FakeNotifier()

    service = MonitorService(
        collector=FakeCollector(),
        product_filter=ProductFilter(),
        classifier=ProductClassifier(),
        peer_analyzer=PeerPriceAnalyzer(
            minimum_strict_peers=2,
            minimum_broad_peers=4,
        ),
        price_analyzer=PriceAnalyzer(
            notification_threshold=70,
            minimum_history_observations=3,
        ),
        product_repository=ProductRepository(
            database
        ),
        notification_repository=(
            NotificationRepository(
                database
            )
        ),
        notifier=notifier,
    )

    rule = SearchRule(
        required_terms=(
            "rtx",
            "5070",
        ),
        excluded_terms=(
            "5070 ti",
            "5070ti",
        ),
        minimum_price=None,
        maximum_price=None,
        require_official_store=False,
        require_full=False,
    )

    result = service.run(
        search_query="RTX 5070",
        relevance_rule=rule,
        candidate_rule=rule,
    )

    print("=" * 80)
    print(f"Coletados: {result.collected_count}")
    print(f"Relevantes: {result.relevant_count}")
    print(
        "Oportunidades: "
        f"{result.detected_opportunities}"
    )
    print(
        "Notificações enviadas: "
        f"{result.sent_notifications}"
    )

    for analyzed in result.analyzed_products:
        opportunity = analyzed.opportunity

        print("-" * 80)
        print(opportunity.product.title)
        print(f"Score: {opportunity.score}")
        print(
            f"Notificar: "
            f"{opportunity.should_notify}"
        )


if __name__ == "__main__":
    main()
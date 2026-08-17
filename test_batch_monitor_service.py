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
from entities.monitoring_target import (
    MonitoringTarget,
)
from entities.product import Product
from entities.search_rule import SearchRule
from services.batch_monitor_service import (
    BatchMonitorService,
)
from services.monitor_service import MonitorService
from services.product_classifier import (
    ProductClassifier,
)


class FakeCollector:
    def search(
        self,
        query: str,
    ) -> list[Product]:
        if query == "BUSCA COM ERRO":
            raise RuntimeError(
                "Erro simulado no collector"
            )

        return [
            create_product(
                product_id=f"{query}_001",
                title=f"{query} Produto 1",
                price=5000.0,
            ),
            create_product(
                product_id=f"{query}_002",
                title=f"{query} Produto 2",
                price=5100.0,
            ),
            create_product(
                product_id=f"{query}_003",
                title=f"{query} Produto 3",
                price=4900.0,
            ),
            create_product(
                product_id=f"{query}_004",
                title=f"{query} Produto 4",
                price=5200.0,
            ),
            create_product(
                product_id=f"{query}_005",
                title=f"{query} Produto 5",
                price=4950.0,
            ),
        ]


class FakeNotifier:
    def send_opportunity(
        self,
        opportunity,
    ) -> bool:
        print(
            "Notificação simulada: "
            f"{opportunity.product.title}"
        )

        return True


def create_product(
    *,
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
        "database/test_batch_monitor.db"
    )

    if database_path.exists():
        database_path.unlink()

    database = Database(
        str(database_path)
    )

    monitor_service = MonitorService(
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
        product_repository=(
            ProductRepository(database)
        ),
        notification_repository=(
            NotificationRepository(
                database
            )
        ),
        notifier=FakeNotifier(),
    )

    batch_service = BatchMonitorService(
        monitor_service
    )

    rtx_rule = SearchRule(
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

    targets = [
        MonitoringTarget(
            name="Teste RTX 5070",
            search_query="RTX 5070",
            relevance_rule=rtx_rule,
            candidate_rule=rtx_rule,
        ),
        MonitoringTarget(
            name="Monitoramento desativado",
            search_query="NÃO EXECUTAR",
            relevance_rule=rtx_rule,
            candidate_rule=rtx_rule,
            enabled=False,
        ),
        MonitoringTarget(
            name="Monitoramento com erro",
            search_query="BUSCA COM ERRO",
            relevance_rule=rtx_rule,
            candidate_rule=rtx_rule,
        ),
    ]

    result = batch_service.run(
        targets=targets
    )

    print("\n" + "=" * 80)
    print("RESULTADO DO TESTE")
    print("=" * 80)

    print(
        "Executados: "
        f"{result.executed_targets}"
    )

    print(
        "Sucessos: "
        f"{result.successful_targets}"
    )

    print(
        "Falhas: "
        f"{result.failed_targets}"
    )

    for target_result in (
        result.target_results
    ):
        print("-" * 80)
        print(
            f"Alvo: "
            f"{target_result.target.name}"
        )
        print(
            f"Sucesso: "
            f"{target_result.success}"
        )
        print(
            f"Erro: "
            f"{target_result.error_message}"
        )


if __name__ == "__main__":
    main()
import math
import statistics
from dataclasses import dataclass
from sqlite3 import Connection

from database.database import Database
from entities.product import Product


@dataclass(frozen=True)
class PriceStatistics:
    observations: int
    minimum_price: float
    maximum_price: float
    average_price: float
    median_price: float
    standard_deviation: float
    previous_price: float | None


class ProductRepository:
    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def save_products(
        self,
        products: list[Product],
    ) -> int:
        saved_count = 0

        with self.database.connect() as connection:
            for product in products:
                if not self._is_valid_product(
                    product
                ):
                    continue

                self._upsert_product(
                    connection,
                    product,
                )

                self._insert_price_history(
                    connection,
                    product,
                )

                saved_count += 1

        return saved_count

    def get_price_statistics(
        self,
        product_id: str,
        marketplace: str,
    ) -> PriceStatistics | None:
        """
        Retorna todas as observações atualmente
        armazenadas para o anúncio.
        """

        return self._get_statistics(
            product_id=product_id,
            marketplace=marketplace,
        )

    def get_baseline_statistics(
        self,
        product_id: str,
        marketplace: str,
    ) -> PriceStatistics | None:
        """
        Retorna o histórico disponível ANTES da coleta atual.

        Importante:

        O MonitorService chama este método antes de salvar
        a observação atual.

        Portanto, todas as observações que já estão no banco
        são histórico válido e devem ser consideradas.

        Não removemos mais artificialmente o registro mais
        recente.
        """

        return self._get_statistics(
            product_id=product_id,
            marketplace=marketplace,
        )

    def _get_statistics(
        self,
        product_id: str,
        marketplace: str,
    ) -> PriceStatistics | None:
        if (
            not product_id
            or not marketplace
        ):
            return None

        with self.database.connect() as connection:
            prices = self._get_prices(
                connection=connection,
                product_id=product_id,
                marketplace=marketplace,
            )

        if not prices:
            return None

        observations = len(
            prices
        )

        minimum_price = min(
            prices
        )

        maximum_price = max(
            prices
        )

        average_price = (
            statistics.fmean(
                prices
            )
        )

        median_price = (
            statistics.median(
                prices
            )
        )

        if observations >= 2:
            standard_deviation = (
                statistics.pstdev(
                    prices
                )
            )
        else:
            standard_deviation = 0.0

        # Como os preços vêm ordenados do
        # mais recente para o mais antigo,
        # prices[0] representa a última
        # observação disponível.
        previous_price = (
            prices[0]
        )

        return PriceStatistics(
            observations=observations,

            minimum_price=float(
                minimum_price
            ),

            maximum_price=float(
                maximum_price
            ),

            average_price=float(
                average_price
            ),

            median_price=float(
                median_price
            ),

            standard_deviation=float(
                standard_deviation
            ),

            previous_price=float(
                previous_price
            ),
        )

    @staticmethod
    def _get_prices(
        connection: Connection,
        product_id: str,
        marketplace: str,
    ) -> list[float]:
        rows = connection.execute(
            """
            SELECT price
            FROM price_history
            WHERE product_id = ?
              AND marketplace = ?
              AND price IS NOT NULL
              AND price > 0
            ORDER BY collected_at DESC, history_id DESC
            """,
            (
                product_id,
                marketplace,
            ),
        ).fetchall()

        prices: list[float] = []

        for row in rows:
            price = float(
                row["price"]
            )

            if (
                math.isfinite(
                    price
                )
                and price > 0
            ):
                prices.append(
                    price
                )

        return prices

    def count_products(
        self,
    ) -> int:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM products
                """
            ).fetchone()

            return int(
                row["total"]
            )

    def count_price_observations(
        self,
    ) -> int:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM price_history
                """
            ).fetchone()

            return int(
                row["total"]
            )

    @staticmethod
    def _upsert_product(
        connection: Connection,
        product: Product,
    ) -> None:
        connection.execute(
            """
            INSERT INTO products (
                id,
                marketplace,
                title,
                seller,
                official_store,
                full_shipping,
                link
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(id, marketplace)
            DO UPDATE SET
                title = excluded.title,
                seller = excluded.seller,
                official_store = excluded.official_store,
                full_shipping = excluded.full_shipping,
                link = excluded.link,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                product.id,
                product.marketplace,
                product.title,
                product.seller,
                int(
                    product.official_store
                ),
                int(
                    product.full
                ),
                product.link,
            ),
        )

    @staticmethod
    def _insert_price_history(
        connection: Connection,
        product: Product,
    ) -> None:
        connection.execute(
            """
            INSERT INTO price_history (
                product_id,
                marketplace,
                price,
                old_price,
                discount,
                installments,
                shipping
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product.id,
                product.marketplace,
                product.price,
                product.old_price,
                product.discount,
                product.installments,
                product.shipping,
            ),
        )

    @staticmethod
    def _is_valid_product(
        product: Product,
    ) -> bool:
        return bool(
            product.id
            and product.marketplace
            and product.title
            and product.link
            and product.price is not None
            and product.price > 0
        )
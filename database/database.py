import sqlite3
from pathlib import Path


class Database:
    def __init__(
        self,
        database_path: str = "database/price_monitor.db",
    ):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._create_tables()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    def _create_tables(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT NOT NULL,
                    marketplace TEXT NOT NULL,
                    title TEXT NOT NULL,
                    seller TEXT,
                    official_store INTEGER
                        NOT NULL DEFAULT 0,
                    full_shipping INTEGER
                        NOT NULL DEFAULT 0,
                    link TEXT NOT NULL,
                    created_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    PRIMARY KEY (
                        id,
                        marketplace
                    )
                );

                CREATE TABLE IF NOT EXISTS price_history (
                    history_id INTEGER
                        PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    marketplace TEXT NOT NULL,
                    price REAL NOT NULL,
                    old_price REAL,
                    discount TEXT,
                    installments TEXT,
                    shipping TEXT,
                    collected_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (
                        product_id,
                        marketplace
                    )
                    REFERENCES products (
                        id,
                        marketplace
                    )
                    ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS notification_history (
                    notification_id INTEGER
                        PRIMARY KEY AUTOINCREMENT,

                    product_id TEXT NOT NULL,
                    marketplace TEXT NOT NULL,

                    price REAL NOT NULL,
                    score INTEGER NOT NULL,
                    opportunity_type TEXT NOT NULL,
                    confidence TEXT NOT NULL,

                    sent_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (
                        product_id,
                        marketplace
                    )
                    REFERENCES products (
                        id,
                        marketplace
                    )
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS
                    idx_price_history_product
                ON price_history (
                    product_id,
                    marketplace,
                    collected_at
                );

                CREATE INDEX IF NOT EXISTS
                    idx_price_history_collected_at
                ON price_history (
                    collected_at
                );

                CREATE INDEX IF NOT EXISTS
                    idx_notification_history_product
                ON notification_history (
                    product_id,
                    marketplace,
                    sent_at
                );
                """
            )
import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_chat_id: str
    telegram_enabled: bool

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            telegram_bot_token=os.getenv(
                "TELEGRAM_BOT_TOKEN",
                "",
            ).strip(),
            telegram_chat_id=os.getenv(
                "TELEGRAM_CHAT_ID",
                "",
            ).strip(),
            telegram_enabled=cls._parse_boolean(
                os.getenv(
                    "TELEGRAM_ENABLED",
                    "false",
                )
            ),
        )

    def validate_telegram(self) -> None:
        if not self.telegram_enabled:
            return

        if not self.telegram_bot_token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN não foi configurado no .env."
            )

        if not self.telegram_chat_id:
            raise ValueError(
                "TELEGRAM_CHAT_ID não foi configurado no .env."
            )

    @staticmethod
    def _parse_boolean(value: str) -> bool:
        return value.strip().lower() in {
            "1",
            "true",
            "yes",
            "sim",
            "on",
        }
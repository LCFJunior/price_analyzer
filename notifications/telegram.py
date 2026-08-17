from html import escape

import requests

from entities.opportunity import Opportunity


class TelegramNotifier:
    API_BASE_URL = "https://api.telegram.org"

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        enabled: bool = True,
        timeout_seconds: int = 15,
    ):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = enabled
        self.timeout_seconds = timeout_seconds

    def send_opportunity(
        self,
        opportunity: Opportunity,
    ) -> bool:
        if not self.enabled:
            print(
                "Telegram desativado. "
                "Mensagem não enviada."
            )
            return False

        self._validate_configuration()

        product = opportunity.product

        caption = self.format_opportunity(
            opportunity
        )

        if product.image_url:
            try:
                return self._send_photo(
                    photo_url=product.image_url,
                    caption=caption,
                    product_url=product.link,
                )

            except Exception as error:
                print(
                    "Falha ao enviar a foto. "
                    "Tentando mensagem de texto: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

        return self._send_text(
            message=caption,
            product_url=product.link,
        )

    def send_message(
        self,
        message: str,
    ) -> bool:
        self._validate_configuration()

        return self._send_text(
            message=message,
            product_url=None,
        )

    def _send_photo(
        self,
        *,
        photo_url: str,
        caption: str,
        product_url: str,
    ) -> bool:
        url = (
            f"{self.API_BASE_URL}/bot"
            f"{self.bot_token}/sendPhoto"
        )

        response = requests.post(
            url,
            json={
                "chat_id": self.chat_id,
                "photo": photo_url,
                "caption": caption,
                "parse_mode": "HTML",
                "show_caption_above_media": False,
                "reply_markup": self._build_keyboard(
                    product_url
                ),
            },
            timeout=self.timeout_seconds,
        )

        self._validate_response(
            response=response,
            operation="enviar foto",
        )

        return True

    def _send_text(
        self,
        *,
        message: str,
        product_url: str | None,
    ) -> bool:
        url = (
            f"{self.API_BASE_URL}/bot"
            f"{self.bot_token}/sendMessage"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }

        if product_url:
            payload["reply_markup"] = (
                self._build_keyboard(
                    product_url
                )
            )

        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout_seconds,
        )

        self._validate_response(
            response=response,
            operation="enviar mensagem",
        )

        return True

    @staticmethod
    def format_opportunity(
        opportunity: Opportunity,
    ) -> str:
        product = opportunity.product

        alert_title = (
            TelegramNotifier._get_alert_title(
                opportunity.opportunity_type
            )
        )

        price = TelegramNotifier._format_price(
            product.price
        )

        old_price = TelegramNotifier._format_price(
            product.old_price
        )

        seller = escape(
            product.seller
            or "Não informado"
        )

        shipping = escape(
            product.shipping
            or "Não informado"
        )

        highlights = (
            TelegramNotifier._format_reasons(
                opportunity.reasons
            )
        )

        discount_line = ""

        if product.old_price is not None:
            discount_line = (
                f"❌ <b>Antes:</b> "
                f"<s>{old_price}</s>\n"
            )

        installments_line = ""

        if product.installments:
            installments_line = (
                "💳 <b>Pagamento:</b> "
                f"{escape(product.installments)}\n"
            )

        return (
            f"{alert_title}\n\n"
            f"<b>{escape(product.title)}</b>\n\n"
            f"💰 <b>{price}</b>\n"
            f"{discount_line}"
            f"{installments_line}"
            f"📊 <b>Score:</b> "
            f"{opportunity.score}/100\n"
            f"🔎 <b>Confiança:</b> "
            f"{escape(
                opportunity.confidence.upper()
            )}\n\n"
            f"🏪 <b>Vendedor:</b> "
            f"{seller}\n"
            f"✅ <b>Oficial:</b> "
            f"{'Sim' if product.official_store else 'Não'}\n"
            f"📦 <b>FULL:</b> "
            f"{'Sim' if product.full else 'Não'}\n"
            f"🚚 <b>Frete:</b> "
            f"{shipping}\n\n"
            f"📌 <b>Destaques</b>\n"
            f"{highlights}"
        )

    @staticmethod
    def _format_reasons(
        reasons: list[str],
    ) -> str:
        if not reasons:
            return "• Oferta detectada"

        important_reasons = reasons[:3]

        return "\n".join(
            f"• {escape(reason)}"
            for reason in important_reasons
        )

    @staticmethod
    def _build_keyboard(
        product_url: str,
    ) -> dict:
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "🛒 Abrir anúncio",
                        "url": product_url,
                    }
                ]
            ]
        }

    @staticmethod
    def _get_alert_title(
        opportunity_type: str,
    ) -> str:
        titles = {
            "possivel_erro_preco": (
                "💥 <b>POSSÍVEL BUG DE PREÇO</b>"
            ),
            "queda_historica": (
                "🚨 <b>QUEDA HISTÓRICA</b>"
            ),
            "promocao": (
                "🔥 <b>PROMOÇÃO ENCONTRADA</b>"
            ),
            "normal": (
                "🏷️ <b>OPORTUNIDADE</b>"
            ),
        }

        return titles.get(
            opportunity_type,
            titles["normal"],
        )

    def _validate_configuration(
        self,
    ) -> None:
        if not self.enabled:
            raise RuntimeError(
                "Telegram está desativado."
            )

        if not self.bot_token:
            raise ValueError(
                "Token do Telegram "
                "não configurado."
            )

        if not self.chat_id:
            raise ValueError(
                "Chat ID do Telegram "
                "não configurado."
            )

    @staticmethod
    def _validate_response(
        *,
        response: requests.Response,
        operation: str,
    ) -> None:
        if response.ok:
            return

        raise RuntimeError(
            f"Falha ao {operation} "
            "pelo Telegram. "
            f"Status: {response.status_code}. "
            f"Resposta: {response.text}"
        )

    @staticmethod
    def _format_price(
        price: float | None,
    ) -> str:
        if price is None:
            return "Não informado"

        formatted = f"{price:,.2f}"

        formatted = formatted.replace(
            ",",
            "_",
        )

        formatted = formatted.replace(
            ".",
            ",",
        )

        formatted = formatted.replace(
            "_",
            ".",
        )

        return f"R$ {formatted}"
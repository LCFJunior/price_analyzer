from config.settings import Settings
from entities.opportunity import Opportunity
from entities.product import Product
from notifications.telegram import TelegramNotifier


def main() -> None:
    settings = Settings.load()
    settings.validate_telegram()

    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
        enabled=settings.telegram_enabled,
    )

    product = Product(
        id="MLB_TEST_TELEGRAM_PHOTO",
        marketplace="Mercado Livre",
        title=(
            "Placa de Vídeo ASUS GeForce "
            "RTX 5070 Dual OC 12GB GDDR7"
        ),
        price=2999.90,
        old_price=5499.90,
        discount="45% OFF",
        installments="12x R$ 249,99",
        seller="Loja Oficial ASUS",
        official_store=True,
        full=True,
        shipping="Frete grátis",
        link="https://www.mercadolivre.com.br",
        image_url=(
            "https://http2.mlstatic.com/"
            "D_Q_NP_2X_711964-"
            "MLA106104908117_012026-E.webp"
        ),
    )

    opportunity = Opportunity(
        product=product,
        score=96,
        should_notify=True,
        reasons=[
            "Preço 45,5% abaixo da mediana histórica",
            "Novo menor preço observado",
            "Preço muito abaixo de anúncios equivalentes",
            "Produto vendido por loja oficial",
            "Produto enviado pelo FULL",
            "Frete grátis",
        ],
        opportunity_type="possivel_erro_preco",
        confidence="muito alta",
    )

    sent = notifier.send_opportunity(
        opportunity
    )

    if sent:
        print(
            "Mensagem compacta com foto "
            "enviada com sucesso."
        )
    else:
        print("Mensagem não enviada.")


if __name__ == "__main__":
    main()
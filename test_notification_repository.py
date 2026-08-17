from database.database import Database
from database.notification_repository import (
    NotificationRepository,
)
from database.repository import ProductRepository
from entities.opportunity import Opportunity
from entities.product import Product


database = Database(
    "database/test_notifications.db"
)

product_repository = ProductRepository(
    database
)

notification_repository = NotificationRepository(
    database
)

product = Product(
    id="MLB_NOTIFICATION_TEST",
    marketplace="Mercado Livre",
    title="RTX 5070 de teste",
    price=2999.0,
    old_price=4999.0,
    discount="40% OFF",
    installments=None,
    seller="Loja Teste",
    official_store=True,
    full=True,
    shipping="Frete grátis",
    link="https://teste.com",
)

# O produto precisa existir na tabela products antes
# de uma notificação poder referenciá-lo.
saved_products = product_repository.save_products(
    [product]
)

print("=" * 80)
print("PRODUTO DE TESTE")
print(f"Produtos salvos: {saved_products}")

opportunity = Opportunity(
    product=product,
    score=90,
    should_notify=True,
    reasons=[
        "Preço muito abaixo do mercado",
    ],
    opportunity_type="possivel_erro_preco",
    confidence="muito alta",
)

should_send, reason = (
    notification_repository.should_send(
        opportunity
    )
)

print("=" * 80)
print("PRIMEIRA VERIFICAÇÃO")
print(f"Enviar: {should_send}")
print(f"Motivo: {reason}")

if should_send:
    notification_repository.save_notification(
        opportunity
    )

should_send_again, reason_again = (
    notification_repository.should_send(
        opportunity
    )
)

print("=" * 80)
print("SEGUNDA VERIFICAÇÃO")
print(f"Enviar: {should_send_again}")
print(f"Motivo: {reason_again}")

product_with_lower_price = Product(
    id=product.id,
    marketplace=product.marketplace,
    title=product.title,
    price=2799.0,
    old_price=product.old_price,
    discount=product.discount,
    installments=product.installments,
    seller=product.seller,
    official_store=product.official_store,
    full=product.full,
    shipping=product.shipping,
    link=product.link,
)

lower_price_opportunity = Opportunity(
    product=product_with_lower_price,
    score=95,
    should_notify=True,
    reasons=[
        "Preço caiu novamente",
    ],
    opportunity_type="possivel_erro_preco",
    confidence="muito alta",
)

should_send_lower, reason_lower = (
    notification_repository.should_send(
        lower_price_opportunity
    )
)

print("=" * 80)
print("PREÇO MAIS BAIXO")
print(f"Enviar: {should_send_lower}")
print(f"Motivo: {reason_lower}")

print("=" * 80)
print(
    "Total de alertas salvos: "
    f"{notification_repository.count_notifications()}"
)
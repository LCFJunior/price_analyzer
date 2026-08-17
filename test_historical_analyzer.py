from analyzers.price_analyzer import PriceAnalyzer
from database.repository import PriceStatistics
from entities.product import Product


product = Product(
    id="MLB_TEST_HISTORY",
    marketplace="Mercado Livre",
    title="RTX 5070 em promoção",
    price=2500.0,
    old_price=5999.0,
    discount="58% OFF",
    installments="12x R$ 208,33",
    seller="Loja Teste",
    official_store=True,
    full=True,
    shipping="Frete grátis",
    link="https://produto-teste.com",
)

statistics = PriceStatistics(
    observations=10,
    minimum_price=4500.0,
    maximum_price=5500.0,
    average_price=5000.0,
    previous_price=5100.0,
)

analyzer = PriceAnalyzer(
    notification_threshold=70,
    minimum_history_observations=3,
)

opportunity = analyzer.analyze(
    product=product,
    statistics=statistics,
)

print(f"Produto: {opportunity.product.title}")
print(f"Score: {opportunity.score}/100")
print(f"Notificar: {opportunity.should_notify}")
print("Motivos:")

for reason in opportunity.reasons:
    print(f"- {reason}")
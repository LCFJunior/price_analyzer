from analyzers.price_analyzer import PriceAnalyzer
from database.repository import PriceStatistics
from entities.product import Product


product = Product(
    id="MLB_ANOMALY_TEST",
    marketplace="Mercado Livre",
    title="Produto com possível erro de preço",
    price=1999.0,
    old_price=None,
    discount=None,
    installments="12x R$ 166,58",
    seller="Loja Oficial Teste",
    official_store=True,
    full=True,
    shipping="Frete grátis",
    link="https://produto-teste.com",
)

statistics = PriceStatistics(
    observations=20,
    minimum_price=4700.0,
    maximum_price=5300.0,
    average_price=5000.0,
    median_price=5020.0,
    standard_deviation=120.0,
    previous_price=4990.0,
)

analyzer = PriceAnalyzer(
    notification_threshold=70,
    minimum_history_observations=3,
)

opportunity = analyzer.analyze(
    product=product,
    statistics=statistics,
)

print("=" * 80)
print(f"Produto: {product.title}")
print(f"Preço atual: R$ {product.price:.2f}")
print(f"Score: {opportunity.score}/100")
print(f"Tipo: {opportunity.opportunity_type}")
print(f"Confiança: {opportunity.confidence}")
print(f"Notificar: {opportunity.should_notify}")
print("Motivos:")

for reason in opportunity.reasons:
    print(f"- {reason}")
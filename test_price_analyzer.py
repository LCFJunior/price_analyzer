from analyzers.price_analyzer import PriceAnalyzer
from entities.product import Product


def create_product(
    *,
    product_id: str,
    title: str,
    price: float | None,
    old_price: float | None,
    official_store: bool,
    full: bool,
    shipping: str | None,
    link: str = "https://produto-teste.com",
) -> Product:
    return Product(
        id=product_id,
        marketplace="Mercado Livre",
        title=title,
        price=price,
        old_price=old_price,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=official_store,
        full=full,
        shipping=shipping,
        link=link,
    )


analyzer = PriceAnalyzer(notification_threshold=60)


excellent_product = create_product(
    product_id="MLB001",
    title="Produto com desconto excepcional",
    price=2000.0,
    old_price=8000.0,
    official_store=True,
    full=True,
    shipping="Frete grátis",
)

normal_product = create_product(
    product_id="MLB002",
    title="Produto com desconto moderado",
    price=4500.0,
    old_price=5000.0,
    official_store=False,
    full=False,
    shipping=None,
)

invalid_product = create_product(
    product_id="MLB003",
    title="Produto sem preço",
    price=None,
    old_price=None,
    official_store=True,
    full=True,
    shipping="Frete grátis",
)


opportunities = [
    analyzer.analyze(excellent_product),
    analyzer.analyze(normal_product),
    analyzer.analyze(invalid_product),
]


for opportunity in opportunities:
    print("=" * 80)
    print(f"Produto: {opportunity.product.title}")
    print(f"Score: {opportunity.score}/100")
    print(f"Notificar: {opportunity.should_notify}")
    print("Motivos:")

    for reason in opportunity.reasons:
        print(f"- {reason}")
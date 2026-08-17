from entities.product import Product
from entities.opportunity import Opportunity

produto = Product(
    id="MLB123",
    marketplace="Mercado Livre",
    title="RTX 5070",
    price=4999.0,
    old_price=7999.0,
    discount="38%",
    installments=None,
    seller="TNT Info",
    official_store=True,
    full=True,
    shipping="Frete grátis",
    link="https://teste"
)

oportunidade = Opportunity(
    product=produto,
    score=95,
    should_notify=True,
    reasons=[
        "Preço abaixo do esperado",
        "Loja Oficial",
        "FULL"
    ]
)

print(oportunidade)
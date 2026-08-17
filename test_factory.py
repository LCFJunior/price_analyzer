from services.product_factory import ProductFactory


produto = ProductFactory.create(

    marketplace="Mercado Livre",

    title=" RTX 5070 ASUS ",

    price="R$\n5.042",

    old_price="R$ 7.899",

    discount="36% OFF",

    installments="12x R$484,71",

    seller=" TNT Info ",

    official_store=True,

    full=True,

    shipping="Chegará amanhã",

    link="https://teste",

    product_id="MLB123"
)

print(produto)
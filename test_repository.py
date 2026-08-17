from database.database import Database
from database.repository import ProductRepository
from entities.product import Product


database = Database("database/test_price_monitor.db")

repository = ProductRepository(database)

product = Product(
    id="MLB_TEST_001",
    marketplace="Mercado Livre",
    title="RTX 5070 Produto de Teste",
    price=4999.0,
    old_price=5999.0,
    discount="16% OFF",
    installments="12x R$ 416,58",
    seller="Loja Teste",
    official_store=True,
    full=True,
    shipping="Frete grátis",
    link="https://produto-teste.com",
)

saved_count = repository.save_products([product])

statistics = repository.get_price_statistics(
    product_id=product.id,
    marketplace=product.marketplace,
)

print(f"Registros salvos: {saved_count}")
print(f"Produtos cadastrados: {repository.count_products()}")
print(
    "Observações de preço: "
    f"{repository.count_price_observations()}"
)
print(f"Estatísticas: {statistics}")
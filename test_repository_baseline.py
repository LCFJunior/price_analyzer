from pathlib import Path

from database.database import Database
from database.repository import (
    ProductRepository,
)

from entities.product import Product


def create_product(
    *,
    price: float,
) -> Product:
    return Product(
        id="TEST001",
        marketplace="Mercado Livre",
        title="Produto Teste",
        price=price,
        old_price=None,
        discount=None,
        installments=None,
        seller="Loja Teste",
        official_store=False,
        full=False,
        shipping=None,
        link="https://teste.com/TEST001",
        image_url=None,
        international=False,
    )


def main() -> None:
    database_path = Path(
        "database/test_repository_baseline.db"
    )

    if database_path.exists():
        database_path.unlink()

    database = Database(
        str(database_path)
    )

    repository = ProductRepository(
        database
    )

    historical_prices = (
    2550.0,
    2500.0,
    2450.0,
)

    print(
        "\nSalvando histórico..."
    )

    for price in historical_prices:
        repository.save_products(
            [
                create_product(
                    price=price
                )
            ]
        )

        print(
            f"- R$ {price:.2f}"
        )

    baseline = (
        repository
        .get_baseline_statistics(
            product_id="TEST001",
            marketplace="Mercado Livre",
        )
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "BASELINE"
    )

    print(
        "=" * 80
    )

    assert (
        baseline is not None
    )

    print(
        "Observações: "
        f"{baseline.observations}"
    )

    print(
        "Menor: "
        f"R$ {baseline.minimum_price:.2f}"
    )

    print(
        "Maior: "
        f"R$ {baseline.maximum_price:.2f}"
    )

    print(
        "Média: "
        f"R$ {baseline.average_price:.2f}"
    )

    print(
        "Mediana: "
        f"R$ {baseline.median_price:.2f}"
    )

    print(
        "Preço anterior/mais recente: "
        f"R$ {baseline.previous_price:.2f}"
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "VERIFICAÇÕES AUTOMÁTICAS"
    )

    print(
        "=" * 80
    )

    assert (
        baseline.observations
        == 3
    ), (
        "Todas as 3 observações históricas "
        "deveriam ser consideradas."
    )

    assert (
        baseline.minimum_price
        == 1000.0
    )

    assert (
        baseline.maximum_price
        == 1200.0
    )

    assert (
        baseline.average_price
        == 1100.0
    )

    assert (
        baseline.median_price
        == 1100.0
    )

    assert (
        baseline.previous_price
        == 1200.0
    ), (
        "previous_price deveria representar "
        "a observação mais recente."
    )

    print(
        "✓ Todas as observações foram consideradas"
    )

    print(
        "✓ Nenhuma observação válida foi descartada"
    )

    print(
        "✓ Mediana calculada corretamente"
    )

    print(
        "✓ Previous price representa "
        "a última observação"
    )

    print(
        "\nTESTE CONCLUÍDO COM SUCESSO."
    )


if __name__ == "__main__":
    main()
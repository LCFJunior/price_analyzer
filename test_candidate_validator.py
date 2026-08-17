from browser.browser import Browser
from entities.product import Product
from validators.mercadolivre_candidate_validator import (
    MercadoLivreCandidateValidator,
)


def main() -> None:
    browser = Browser()

    playwright = None
    context = None

    try:
        playwright, context, page = (
            browser.open()
        )

        validator = (
            MercadoLivreCandidateValidator(
                context
            )
        )

        product = Product(
            id="MLB_TEST_VALIDATOR",
            marketplace="Mercado Livre",
            title=(
                "Caixa Vazia AMD CPU Ryzen 7 "
                "5700X Adesivo Blister Manual"
            ),
            price=1096.0,
            old_price=None,
            discount=None,
            installments=None,
            seller="Loja Teste",
            official_store=False,
            full=False,
            shipping=None,

            # Cole aqui um anúncio REAL.
            link=(
                "https://www.mercadolivre.com.br/"
                "caixa-vazia-amd-cpu-ryzen-7-5700x-"
                "adesivo-blister-manual/"
                "up/MLBU3089713824"
            ),

            image_url=None,
        )

        print("=" * 80)
        print("VALIDAÇÃO PROFUNDA")
        print("=" * 80)

        print(
            f"Produto: {product.title}"
        )

        print(
            f"Link: {product.link}"
        )

        print(
            "\nAbrindo anúncio..."
        )

        result = validator.validate(
            product
        )

        print("\n" + "=" * 80)
        print("RESULTADO")
        print("=" * 80)

        print(
            f"Status: {result.status}"
        )

        print(
            "Válido: "
            f"{result.is_valid}"
        )

        print(
            "Inválido: "
            f"{result.is_invalid}"
        )

        print(
            "Inconclusivo: "
            f"{result.is_inconclusive}"
        )

        if result.inspected_fields:
            print(
                "\nCampos verificados:"
            )

            for field in (
                result.inspected_fields
            ):
                print(
                    f"- {field}"
                )

        if result.reasons:
            print(
                "\nMotivos:"
            )

            for reason in (
                result.reasons
            ):
                print(
                    f"- {reason}"
                )

        input(
            "\nPressione ENTER "
            "para finalizar..."
        )

    finally:
        if context is not None:
            context.close()

        if playwright is not None:
            playwright.stop()


if __name__ == "__main__":
    main()
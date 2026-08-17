import re
import unicodedata
from dataclasses import dataclass, field

from playwright.sync_api import BrowserContext

from entities.product import Product


@dataclass
class CandidateValidationResult:
    status: str
    reasons: list[str] = field(default_factory=list)
    inspected_fields: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == "valid"

    @property
    def is_invalid(self) -> bool:
        return self.status == "invalid"

    @property
    def is_inconclusive(self) -> bool:
        return self.status == "inconclusive"


class MercadoLivreCandidateValidator:
    """
    Faz uma validação profunda de um anúncio do Mercado Livre.

    Essa validação deve ser executada somente quando o anúncio
    já foi considerado uma possível oportunidade pelo analisador
    principal.

    O objetivo é impedir falsos positivos como:

    - caixa vazia;
    - embalagem;
    - acessórios;
    - peças;
    - produtos defeituosos;
    - sucata;
    - anúncios que explicitamente não acompanham o produto;
    - anúncios ambíguos.

    A página completa do produto é aberta pelo Playwright e alguns
    campos são analisados antes de permitir o envio da notificação.
    """

    INVALID_PHRASES = [
        # Caixa / embalagem
        "caixa vazia",
        "somente caixa",
        "apenas caixa",
        "só a caixa",
        "so a caixa",
        "caixa original vazia",
        "embalagem vazia",

        # Produto não incluso
        "não acompanha processador",
        "nao acompanha processador",
        "não acompanha placa",
        "nao acompanha placa",
        "não acompanha produto",
        "nao acompanha produto",
        "produto não incluso",
        "produto nao incluso",

        # Embalagens / itens relacionados
        "adesivo blister",
        "blister",
        "manual",
        "somente embalagem",
        "apenas embalagem",

        # Defeitos
        "com defeito",
        "defeituoso",
        "não funciona",
        "nao funciona",
        "para conserto",
        "para concerto",
        "para retirada de peças",
        "retirada de peças",
        "sucata",

        # Peças / partes
        "somente peças",
        "somente pecas",
        "apenas peças",
        "apenas pecas",
        "peças para reposição",
        "pecas para reposicao",
    ]

    def __init__(
        self,
        context: BrowserContext,
        timeout: int = 15000,
    ) -> None:
        self.context = context
        self.timeout = timeout

    def validate(
        self,
        product: Product,
    ) -> CandidateValidationResult:
        """
        Abre o anúncio e verifica seu conteúdo.

        Retorna:

        valid
            Página analisada e nenhum indício de produto
            incompleto/inválido foi encontrado.

        invalid
            Foi encontrada alguma expressão que indica que
            provavelmente não se trata do produto completo.

        inconclusive
            Não foi possível analisar a página com segurança.
        """

        if not product.link:
            return CandidateValidationResult(
                status="inconclusive",
                reasons=[
                    "Produto não possui link para validação."
                ],
            )

        page = None

        try:
            page = self.context.new_page()

            page.goto(
                product.link,
                wait_until="domcontentloaded",
                timeout=self.timeout,
            )

            # Aguarda um pequeno período para permitir que
            # conteúdos carregados via JavaScript apareçam.
            try:
                page.wait_for_load_state(
                    "networkidle",
                    timeout=5000,
                )
            except Exception:
                # O Mercado Livre pode manter requisições abertas.
                # Isso não deve invalidar toda a análise.
                pass

            title = self._extract_title(page)
            condition = self._extract_condition(page)
            description = self._extract_description(page)
            details = self._extract_details(page)

            inspected_fields = []

            if title:
                inspected_fields.append("titulo")

            if condition:
                inspected_fields.append("condicao")

            if description:
                inspected_fields.append("descricao")

            if details:
                inspected_fields.append("detalhes")

            # --------------------------------------------------
            # Segurança mínima
            # --------------------------------------------------

            if not title:
                return CandidateValidationResult(
                    status="inconclusive",
                    reasons=[
                        "Não foi possível identificar o título "
                        "do anúncio."
                    ],
                    inspected_fields=inspected_fields,
                )

            # --------------------------------------------------
            # Junta todo o conteúdo relevante
            # --------------------------------------------------

            combined_text = " ".join(
                [
                    title or "",
                    condition or "",
                    description or "",
                    details or "",
                ]
            )

            combined_text = self._normalize(
                combined_text
            )

            # --------------------------------------------------
            # Procura sinais de produto inválido
            # --------------------------------------------------

            suspicious_phrases: list[str] = []

            # Evita duplicidade causada por versões
            # acentuadas/não acentuadas da mesma expressão.
            seen_normalized_phrases: set[str] = set()

            for phrase in self.INVALID_PHRASES:
                normalized_phrase = self._normalize(
                    phrase
                )

                if (
                    normalized_phrase
                    and normalized_phrase in combined_text
                    and normalized_phrase
                    not in seen_normalized_phrases
                ):
                    suspicious_phrases.append(
                        phrase
                    )

                    seen_normalized_phrases.add(
                        normalized_phrase
                    )

            # --------------------------------------------------
            # Encontramos sinais claros de falso positivo
            # --------------------------------------------------

            if suspicious_phrases:
                reasons = [
                    (
                        "Conteúdo suspeito encontrado na página: "
                        f"{phrase}"
                    )
                    for phrase in suspicious_phrases
                ]

                return CandidateValidationResult(
                    status="invalid",
                    reasons=reasons,
                    inspected_fields=inspected_fields,
                )

            # --------------------------------------------------
            # Nenhum problema encontrado
            # --------------------------------------------------

            return CandidateValidationResult(
                status="valid",
                reasons=[
                    "Página do anúncio validada sem indícios "
                    "de produto incompleto."
                ],
                inspected_fields=inspected_fields,
            )

        except Exception as error:
            return CandidateValidationResult(
                status="inconclusive",
                reasons=[
                    (
                        "Não foi possível concluir a validação "
                        f"profunda: {error}"
                    )
                ],
            )

        finally:
            if page is not None:
                try:
                    page.close()
                except Exception:
                    pass

    # ==========================================================
    # EXTRAÇÃO
    # ==========================================================

    def _extract_title(
        self,
        page,
    ) -> str:
        """
        Tenta obter o título do anúncio utilizando mais de
        uma estratégia para reduzir dependência de um único
        seletor do Mercado Livre.
        """

        selectors = [
            "h1.ui-pdp-title",
            "h1",
        ]

        return self._first_text(
            page,
            selectors,
        )

    def _extract_condition(
        self,
        page,
    ) -> str:
        """
        Obtém informações como:

        Novo
        Usado
        Recondicionado
        """

        selectors = [
            ".ui-pdp-subtitle",
            ".ui-pdp-header__subtitle",
        ]

        return self._first_text(
            page,
            selectors,
        )

    def _extract_description(
        self,
        page,
    ) -> str:
        """
        Obtém a descrição principal do anúncio.
        """

        selectors = [
            ".ui-pdp-description__content",
            ".ui-pdp-description",
        ]

        return self._first_text(
            page,
            selectors,
        )

    def _extract_details(
        self,
        page,
    ) -> str:
        """
        Obtém informações adicionais/especificações.

        Como o HTML do Mercado Livre pode variar entre
        categorias, tentamos diferentes regiões.
        """

        selectors = [
            ".ui-pdp-specs",
            ".ui-vpp-highlighted-specs",
            ".ui-pdp-specs__table",
            ".andes-table",
        ]

        texts = []

        for selector in selectors:
            try:
                locator = page.locator(
                    selector
                )

                count = locator.count()

                for index in range(
                    min(count, 5)
                ):
                    text = locator.nth(
                        index
                    ).inner_text(
                        timeout=2000
                    )

                    text = self._clean_text(
                        text
                    )

                    if (
                        text
                        and text not in texts
                    ):
                        texts.append(
                            text
                        )

            except Exception:
                continue

        return " ".join(
            texts
        )

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _first_text(
        self,
        page,
        selectors: list[str],
    ) -> str:
        """
        Retorna o primeiro texto válido encontrado entre
        vários seletores.
        """

        for selector in selectors:
            try:
                locator = page.locator(
                    selector
                )

                if locator.count() == 0:
                    continue

                text = locator.first.inner_text(
                    timeout=3000
                )

                text = self._clean_text(
                    text
                )

                if text:
                    return text

            except Exception:
                continue

        return ""

    @staticmethod
    def _clean_text(
        text: str | None,
    ) -> str:
        if not text:
            return ""

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def _normalize(
        text: str | None,
    ) -> str:
        """
        Normaliza texto para comparação:

        - converte para minúsculas;
        - remove acentos;
        - normaliza espaços.

        Exemplo:

        "NÃO acompanha Processador"

        vira:

        "nao acompanha processador"
        """

        if not text:
            return ""

        text = text.lower()

        text = unicodedata.normalize(
            "NFKD",
            text,
        )

        text = "".join(
            character
            for character in text
            if not unicodedata.combining(
                character
            )
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()
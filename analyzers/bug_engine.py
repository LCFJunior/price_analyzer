from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)
from database.repository import (
    PriceStatistics,
)
from entities.opportunity import Opportunity
from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)


class BugEngine:
    """
    Detecta possíveis erros de preço.

    O histórico individual do anúncio NÃO é obrigatório.

    Porém, a força da comparação contra produtos equivalentes
    depende agora da confiança que temos na identidade do produto.

    Exemplos:

    KINGSTON / NV3 / 1TB / NVMe
    identity_confidence = alta

    → comparação com equivalentes pode gerar FAST PATH.

    Produto genérico / marca desconhecida / modelo desconhecido
    identity_confidence = muito_baixa

    → preço baixo sozinho NÃO pode gerar um bug de alta confiança.
    """

    def __init__(
        self,
        *,
        extreme_peer_drop_percent: float = 60.0,
        strong_peer_drop_percent: float = 45.0,
        extreme_history_drop_percent: float = 55.0,
        minimum_peer_observations: int = 4,
        notification_threshold: int = 70,
    ):
        self.extreme_peer_drop_percent = (
            extreme_peer_drop_percent
        )

        self.strong_peer_drop_percent = (
            strong_peer_drop_percent
        )

        self.extreme_history_drop_percent = (
            extreme_history_drop_percent
        )

        self.minimum_peer_observations = (
            minimum_peer_observations
        )

        self.notification_threshold = (
            notification_threshold
        )

    def analyze(
        self,
        *,
        product: Product,
        profile: ProductProfile | None,
        statistics: PriceStatistics | None,
        peer_statistics: PeerPriceStatistics | None,
    ) -> Opportunity:
        score = 0

        reasons: list[str] = []

        price = product.price

        if (
            price is None
            or price <= 0
        ):
            return self._normal_result(
                product=product,
                reasons=[
                    "Produto sem preço válido."
                ],
            )

        identity_confidence = (
            self._get_identity_confidence(
                profile
            )
        )

        # ======================================================
        # COMPARAÇÃO COM PRODUTOS EQUIVALENTES
        # ======================================================

        peer_score = (
            self._score_peer_price(
                product=product,
                peer_statistics=(
                    peer_statistics
                ),
                identity_confidence=(
                    identity_confidence
                ),
                reasons=reasons,
            )
        )

        score += peer_score

        # ======================================================
        # HISTÓRICO DO PRÓPRIO ANÚNCIO
        # ======================================================

        historical_score = (
            self._score_historical_price(
                price=price,
                statistics=statistics,
                reasons=reasons,
            )
        )

        score += historical_score

        # ======================================================
        # PREÇO ANTERIOR ANUNCIADO
        # ======================================================

        advertised_score = (
            self._score_advertised_price(
                product=product,
                reasons=reasons,
            )
        )

        score += advertised_score

        # ======================================================
        # SINAIS DE CONFIANÇA DO ANÚNCIO
        # ======================================================

        if product.official_store:
            score += 8

            reasons.append(
                "Produto vendido por loja oficial"
            )

        if product.full:
            score += 4

            reasons.append(
                "Produto enviado pela logística "
                "do marketplace"
            )

        score = min(
            score,
            100,
        )

        should_notify = (
            score
            >= self.notification_threshold
        )

        confidence = (
            self._get_opportunity_confidence(
                score
            )
        )

        opportunity_type = (
            "possivel_erro_preco"
            if should_notify
            else "normal"
        )

        return Opportunity(
            product=product,
            score=score,
            should_notify=should_notify,
            reasons=reasons,
            opportunity_type=(
                opportunity_type
            ),
            confidence=confidence,
        )

    def _score_peer_price(
        self,
        *,
        product: Product,
        peer_statistics: (
            PeerPriceStatistics | None
        ),
        identity_confidence: str,
        reasons: list[str],
    ) -> int:
        if (
            peer_statistics is None
            or product.price is None
            or peer_statistics.median_price is None
            or peer_statistics.median_price <= 0
            or (
                peer_statistics.observations
                < self.minimum_peer_observations
            )
        ):
            return 0

        peer_reference = (
            peer_statistics.median_price
        )

        peer_drop = (
            (
                peer_reference
                - product.price
            )
            / peer_reference
            * 100
        )

        if peer_drop < 35:
            return 0

        # ======================================================
        # IDENTIDADE ALTA
        #
        # Produto muito bem identificado.
        # Pode gerar FAST PATH somente com comparação de mercado.
        # ======================================================

        if identity_confidence == "alta":
            if (
                peer_drop
                >= self.extreme_peer_drop_percent
            ):
                reasons.append(
                    "Preço extremamente abaixo "
                    "do mercado: "
                    f"{peer_drop:.1f}% abaixo "
                    "da mediana dos equivalentes"
                )

                return 80

            if (
                peer_drop
                >= self.strong_peer_drop_percent
            ):
                reasons.append(
                    "Preço anormalmente abaixo "
                    "do mercado: "
                    f"{peer_drop:.1f}% abaixo "
                    "da mediana dos equivalentes"
                )

                return 55

            reasons.append(
                "Preço bastante abaixo "
                "dos equivalentes: "
                f"{peer_drop:.1f}%"
            )

            return 30

        # ======================================================
        # IDENTIDADE MÉDIA
        #
        # Ainda pode contribuir bastante, mas evitamos dar
        # 80 pontos somente com comparação ampla.
        # ======================================================

        if identity_confidence == "media":
            if (
                peer_drop
                >= self.extreme_peer_drop_percent
            ):
                reasons.append(
                    "Preço extremamente abaixo "
                    "dos equivalentes, mas com "
                    "identidade parcialmente confirmada: "
                    f"{peer_drop:.1f}%"
                )

                return 55

            if (
                peer_drop
                >= self.strong_peer_drop_percent
            ):
                reasons.append(
                    "Preço muito abaixo dos equivalentes "
                    "com identidade parcialmente confirmada: "
                    f"{peer_drop:.1f}%"
                )

                return 35

            reasons.append(
                "Preço abaixo dos equivalentes "
                "com identidade parcialmente confirmada: "
                f"{peer_drop:.1f}%"
            )

            return 20

        # ======================================================
        # IDENTIDADE BAIXA
        # ======================================================

        if identity_confidence == "baixa":
            if (
                peer_drop
                >= self.extreme_peer_drop_percent
            ):
                reasons.append(
                    "Preço muito abaixo do grupo, "
                    "mas a identidade do produto "
                    "possui baixa confiança: "
                    f"{peer_drop:.1f}%"
                )

                return 30

            if (
                peer_drop
                >= self.strong_peer_drop_percent
            ):
                reasons.append(
                    "Preço abaixo do grupo com "
                    "baixa confiança de identidade: "
                    f"{peer_drop:.1f}%"
                )

                return 20

            return 10

        # ======================================================
        # IDENTIDADE MUITO BAIXA
        #
        # Produto genérico/desconhecido.
        #
        # Comparação de mercado funciona somente como sinal
        # secundário e jamais deve, sozinha, disparar FAST PATH.
        # ======================================================

        if (
            peer_drop
            >= self.extreme_peer_drop_percent
        ):
            reasons.append(
                "Preço muito abaixo do grupo, "
                "mas o produto não possui identidade "
                "confiável: "
                f"{peer_drop:.1f}%"
            )

            return 15

        if (
            peer_drop
            >= self.strong_peer_drop_percent
        ):
            reasons.append(
                "Preço abaixo do grupo, porém "
                "com identidade muito incerta: "
                f"{peer_drop:.1f}%"
            )

            return 10

        return 5

    def _score_historical_price(
        self,
        *,
        price: float,
        statistics: PriceStatistics | None,
        reasons: list[str],
    ) -> int:
        if (
            statistics is None
            or statistics.median_price is None
            or statistics.median_price <= 0
            or statistics.observations < 3
        ):
            return 0

        historical_reference = (
            statistics.median_price
        )

        historical_drop = (
            (
                historical_reference
                - price
            )
            / historical_reference
            * 100
        )

        if (
            historical_drop
            >= self.extreme_history_drop_percent
        ):
            reasons.append(
                "Queda extrema em relação "
                "ao histórico do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 45

        if historical_drop >= 40:
            reasons.append(
                "Queda anormal em relação "
                "ao histórico do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 25

        if historical_drop >= 25:
            reasons.append(
                "Queda relevante em relação "
                "ao histórico do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 12

        return 0

    @staticmethod
    def _score_advertised_price(
        *,
        product: Product,
        reasons: list[str],
    ) -> int:
        if (
            product.price is None
            or product.old_price is None
            or product.old_price <= product.price
        ):
            return 0

        advertised_drop = (
            (
                product.old_price
                - product.price
            )
            / product.old_price
            * 100
        )

        if advertised_drop >= 70:
            reasons.append(
                "Desconto anunciado "
                "extremamente elevado: "
                f"{advertised_drop:.1f}%"
            )

            return 20

        if advertised_drop >= 50:
            reasons.append(
                "Desconto anunciado muito alto: "
                f"{advertised_drop:.1f}%"
            )

            return 10

        return 0

    @staticmethod
    def _get_identity_confidence(
        profile: ProductProfile | None,
    ) -> str:
        if profile is None:
            return "muito_baixa"

        explicit_confidence = (
            profile.attributes.get(
                "identity_confidence"
            )
        )

        if explicit_confidence in {
            "alta",
            "media",
            "baixa",
            "muito_baixa",
        }:
            return explicit_confidence

        # Compatibilidade com os classificadores
        # que ainda não possuem identity_confidence.
        #
        # Exemplo: GPU e CPU.
        if profile.strict_key:
            return "alta"

        if profile.broad_key:
            return "media"

        return "muito_baixa"

    @staticmethod
    def _get_opportunity_confidence(
        score: int,
    ) -> str:
        if score >= 85:
            return "muito alta"

        if score >= 70:
            return "alta"

        if score >= 45:
            return "media"

        return "baixa"

    @staticmethod
    def _normal_result(
        *,
        product: Product,
        reasons: list[str],
    ) -> Opportunity:
        return Opportunity(
            product=product,
            score=0,
            should_notify=False,
            reasons=reasons,
            opportunity_type="normal",
            confidence="baixa",
        )
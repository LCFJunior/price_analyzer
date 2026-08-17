from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)

from database.repository import (
    PriceStatistics,
)

from entities.opportunity import (
    Opportunity,
)

from entities.product import (
    Product,
)

from entities.product_profile import (
    ProductProfile,
)


class PromotionEngine:
    """
    Detecta promoções reais.

    Diferente do BugEngine, este motor procura
    descontos plausíveis e sustentados por:

    - histórico do próprio anúncio;
    - produtos equivalentes;
    - qualidade da comparação;
    - desconto anunciado;
    - confiança comercial do anúncio.

    Hierarquia de referência:

    modelo_exato
        ↓
    mesmo_tier
        ↓
    grupo_geral

    Quanto mais específica a comparação,
    maior o peso dela no score.
    """

    def __init__(
        self,
        *,
        notification_threshold: int = 70,
        minimum_history_observations: int = 3,
    ):
        self.notification_threshold = (
            notification_threshold
        )

        self.minimum_history_observations = (
            minimum_history_observations
        )

    def analyze(
        self,
        *,
        product: Product,
        profile: ProductProfile | None,
        statistics: PriceStatistics | None,
        peer_statistics: (
            PeerPriceStatistics | None
        ),
    ) -> Opportunity:
        score = 0

        reasons: list[str] = []

        if (
            product.price is None
            or product.price <= 0
        ):
            return self._normal_result(
                product=product,
                reasons=[
                    "Produto sem preço válido."
                ],
            )

        # ======================================================
        # HISTÓRICO DO PRÓPRIO ANÚNCIO
        # ======================================================

        score += self._score_history(
            product=product,
            statistics=statistics,
            reasons=reasons,
        )

        # ======================================================
        # PRODUTOS EQUIVALENTES
        # ======================================================

        score += self._score_peers(
            product=product,
            peer_statistics=(
                peer_statistics
            ),
            reasons=reasons,
        )

        # ======================================================
        # DESCONTO INFORMADO PELO MARKETPLACE
        # ======================================================

        score += (
            self._score_advertised_discount(
                product=product,
                reasons=reasons,
            )
        )

        # ======================================================
        # CONFIANÇA COMERCIAL
        # ======================================================

        if product.official_store:
            score += 5

            reasons.append(
                "Produto vendido por loja oficial"
            )

        if product.full:
            score += 3

            reasons.append(
                "Produto enviado pela logística "
                "do marketplace"
            )

        if self._has_free_shipping(
            product
        ):
            score += 2

            reasons.append(
                "Frete grátis"
            )

        # ======================================================
        # IDENTIDADE DO PRODUTO
        # ======================================================

        identity_confidence = (
            self._get_identity_confidence(
                profile
            )
        )

        if (
            identity_confidence
            == "muito_baixa"
        ):
            # Não zeramos a análise.
            #
            # Apenas limitamos a força de uma promoção
            # baseada em identidade muito incerta.
            score = min(
                score,
                55,
            )

            reasons.append(
                "Identidade do produto possui "
                "confiança muito baixa"
            )

        elif (
            identity_confidence
            == "baixa"
        ):
            score = min(
                score,
                65,
            )

        score = min(
            score,
            100,
        )

        should_notify = (
            score
            >= self.notification_threshold
        )

        if should_notify:
            opportunity_type = (
                "promocao"
            )

        elif score >= 40:
            # Interessante, mas ainda não forte
            # o suficiente para notificação.
            opportunity_type = (
                "promocao"
            )

        else:
            opportunity_type = (
                "normal"
            )

        confidence = (
            self._get_confidence(
                score
            )
        )

        return Opportunity(
            product=product,
            score=score,
            should_notify=(
                should_notify
            ),
            reasons=reasons,
            opportunity_type=(
                opportunity_type
            ),
            confidence=confidence,
        )

    def _score_history(
        self,
        *,
        product: Product,
        statistics: PriceStatistics | None,
        reasons: list[str],
    ) -> int:
        if statistics is None:
            reasons.append(
                "Produto ainda não possui "
                "histórico anterior"
            )

            return 0

        if (
            statistics.observations
            < self.minimum_history_observations
        ):
            reasons.append(
                "Histórico ainda insuficiente: "
                f"{statistics.observations}/"
                f"{self.minimum_history_observations} "
                "observações"
            )

            return 0

        if (
            statistics.median_price is None
            or statistics.median_price <= 0
            or product.price is None
        ):
            return 0

        historical_drop = (
            (
                statistics.median_price
                - product.price
            )
            / statistics.median_price
            * 100
        )

        if historical_drop >= 35:
            reasons.append(
                "Preço muito abaixo do histórico "
                "do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 40

        if historical_drop >= 25:
            reasons.append(
                "Preço bem abaixo do histórico "
                "do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 30

        if historical_drop >= 15:
            reasons.append(
                "Preço abaixo do histórico "
                "do próprio anúncio: "
                f"{historical_drop:.1f}%"
            )

            return 20

        if historical_drop >= 8:
            reasons.append(
                "Preço moderadamente abaixo "
                "do histórico: "
                f"{historical_drop:.1f}%"
            )

            return 10

        return 0

    def _score_peers(
        self,
        *,
        product: Product,
        peer_statistics: (
            PeerPriceStatistics | None
        ),
        reasons: list[str],
    ) -> int:
        if (
            peer_statistics is None
            or product.price is None
            or peer_statistics.median_price <= 0
        ):
            return 0

        if (
            product.price
            >= peer_statistics.median_price
        ):
            return 0

        peer_drop = (
            (
                peer_statistics.median_price
                - product.price
            )
            / peer_statistics.median_price
            * 100
        )

        scope = (
            peer_statistics.comparison_scope
        )

        # ======================================================
        # MODELO EXATO
        # ======================================================

        if scope.startswith(
            "modelo_exato"
        ):
            if peer_drop >= 20:
                reasons.append(
                    "Preço muito abaixo de anúncios "
                    "do mesmo modelo: "
                    f"{peer_drop:.1f}%"
                )

                return 30

            if peer_drop >= 12:
                reasons.append(
                    "Preço abaixo de anúncios "
                    "do mesmo modelo: "
                    f"{peer_drop:.1f}%"
                )

                return 20

            if peer_drop >= 7:
                reasons.append(
                    "Preço moderadamente abaixo "
                    "do mesmo modelo: "
                    f"{peer_drop:.1f}%"
                )

                return 10

            return 0

        # ======================================================
        # MESMO TIER
        # ======================================================

        if scope.startswith(
            "mesmo_tier"
        ):
            if peer_drop >= 25:
                reasons.append(
                    "Preço muito abaixo de produtos "
                    "da mesma classe técnica: "
                    f"{peer_drop:.1f}%"
                )

                return 24

            if peer_drop >= 15:
                reasons.append(
                    "Preço abaixo de produtos "
                    "da mesma classe técnica: "
                    f"{peer_drop:.1f}%"
                )

                return 16

            if peer_drop >= 8:
                reasons.append(
                    "Preço moderadamente abaixo "
                    "do mesmo tier: "
                    f"{peer_drop:.1f}%"
                )

                return 8

            return 0

        # ======================================================
        # GRUPO AMPLO
        #
        # É nossa referência menos precisa.
        # Portanto recebe peso menor.
        # ======================================================

        if peer_drop >= 35:
            reasons.append(
                "Preço bem abaixo do grupo geral "
                "de produtos equivalentes: "
                f"{peer_drop:.1f}%"
            )

            return 16

        if peer_drop >= 20:
            reasons.append(
                "Preço abaixo do grupo geral "
                "de produtos equivalentes: "
                f"{peer_drop:.1f}%"
            )

            return 10

        if peer_drop >= 10:
            reasons.append(
                "Preço moderadamente abaixo "
                "do grupo geral: "
                f"{peer_drop:.1f}%"
            )

            return 5

        return 0

    @staticmethod
    def _score_advertised_discount(
        *,
        product: Product,
        reasons: list[str],
    ) -> int:
        if (
            product.price is None
            or product.old_price is None
            or product.old_price <= 0
            or (
                product.old_price
                <= product.price
            )
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

        if advertised_drop >= 30:
            reasons.append(
                "Bom desconto anunciado: "
                f"{advertised_drop:.1f}%"
            )

            return 15

        if advertised_drop >= 20:
            reasons.append(
                "Desconto anunciado relevante: "
                f"{advertised_drop:.1f}%"
            )

            return 10

        if advertised_drop >= 10:
            reasons.append(
                "Desconto anunciado moderado: "
                f"{advertised_drop:.1f}%"
            )

            return 5

        return 0

    @staticmethod
    def _has_free_shipping(
        product: Product,
    ) -> bool:
        if not product.shipping:
            return False

        normalized = (
            product.shipping
            .lower()
            .strip()
        )

        return (
            "gratis" in normalized
            or "grátis" in normalized
        )

    @staticmethod
    def _get_identity_confidence(
        profile: ProductProfile | None,
    ) -> str:
        if profile is None:
            return "muito_baixa"

        confidence = (
            profile.attributes.get(
                "identity_confidence"
            )
        )

        if confidence in {
            "alta",
            "media",
            "baixa",
            "muito_baixa",
        }:
            return confidence

        if profile.strict_key:
            return "alta"

        if profile.tier_key:
            return "media"

        if profile.broad_key:
            return "baixa"

        return "muito_baixa"

    @staticmethod
    def _get_confidence(
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
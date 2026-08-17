from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)
from database.repository import PriceStatistics
from entities.opportunity import Opportunity
from entities.product import Product


class PriceAnalyzer:
    def __init__(
        self,
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
        product: Product,
        statistics: PriceStatistics | None = None,
        peer_statistics: PeerPriceStatistics | None = None,
    ) -> Opportunity:
        reasons: list[str] = []

        historical_score = (
            self._analyze_historical_price(
                product=product,
                statistics=statistics,
                reasons=reasons,
            )
        )

        peer_score = self._analyze_peer_price(
            product=product,
            peer_statistics=peer_statistics,
            reasons=reasons,
        )

        commercial_score = (
            self._analyze_advertised_discount(
                product=product,
                reasons=reasons,
            )
        )

        reliability_score = (
            self._analyze_reliability(
                product=product,
                reasons=reasons,
            )
        )

        data_score = self._analyze_product_data(
            product=product,
            reasons=reasons,
        )

        score = (
            historical_score
            + peer_score
            + commercial_score
            + reliability_score
            + data_score
        )

        score = max(0, min(score, 100))

        opportunity_type, confidence = (
            self._classify_opportunity(
                product=product,
                statistics=statistics,
                peer_statistics=peer_statistics,
                score=score,
            )
        )

        return Opportunity(
            product=product,
            score=score,
            should_notify=(
                score >= self.notification_threshold
            ),
            reasons=reasons,
            opportunity_type=opportunity_type,
            confidence=confidence,
        )

    def _analyze_historical_price(
        self,
        product: Product,
        statistics: PriceStatistics | None,
        reasons: list[str],
    ) -> int:
        if product.price is None:
            return 0

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

        median_drop = (
            self._calculate_drop_percentage(
                current_price=product.price,
                reference_price=(
                    statistics.median_price
                ),
            )
        )

        average_drop = (
            self._calculate_drop_percentage(
                current_price=product.price,
                reference_price=(
                    statistics.average_price
                ),
            )
        )

        minimum_drop = (
            self._calculate_drop_percentage(
                current_price=product.price,
                reference_price=(
                    statistics.minimum_price
                ),
            )
        )

        previous_drop = (
            self._calculate_drop_percentage(
                current_price=product.price,
                reference_price=(
                    statistics.previous_price
                ),
            )
        )

        score = self._score_drop(
            drop=median_drop,
            label="mediana histórica",
            reasons=reasons,
            maximum_score=80,
        )

        if (
            average_drop is not None
            and average_drop >= 15
        ):
            reasons.append(
                "Preço abaixo da média histórica: "
                f"{average_drop:.1f}%"
            )
            score += 5

        if (
            minimum_drop is not None
            and minimum_drop > 0
        ):
            reasons.append(
                "Novo menor preço observado: "
                f"{minimum_drop:.1f}% abaixo "
                "do mínimo anterior"
            )
            score += 10

        if (
            previous_drop is not None
            and previous_drop >= 10
        ):
            reasons.append(
                "Queda desde a última coleta: "
                f"{previous_drop:.1f}%"
            )
            score += 5

        return min(score, 85)

    @staticmethod
    def _analyze_peer_price(
        product: Product,
        peer_statistics: PeerPriceStatistics | None,
        reasons: list[str],
    ) -> int:
        if (
            product.price is None
            or peer_statistics is None
        ):
            return 0

        drop = (
            PriceAnalyzer
            ._calculate_drop_percentage(
                current_price=product.price,
                reference_price=(
                    peer_statistics.median_price
                ),
            )
        )

        if drop is None or drop < 10:
            return 0

        scope_label = (
            "da mesma marca"
            if (
                peer_statistics.comparison_scope
                == "mesma_marca"
            )
            else "do mesmo grupo"
        )

        if drop >= 60:
            reasons.append(
                "Preço extremamente abaixo "
                f"dos anúncios {scope_label}: "
                f"{drop:.1f}%"
            )
            return 80

        if drop >= 45:
            reasons.append(
                "Preço muito abaixo "
                f"dos anúncios {scope_label}: "
                f"{drop:.1f}%"
            )
            return 70

        if drop >= 35:
            reasons.append(
                "Preço fortemente abaixo "
                f"dos anúncios {scope_label}: "
                f"{drop:.1f}%"
            )
            return 55

        if drop >= 25:
            reasons.append(
                "Preço bem abaixo "
                f"dos anúncios {scope_label}: "
                f"{drop:.1f}%"
            )
            return 40

        if drop >= 15:
            reasons.append(
                "Preço abaixo "
                f"dos anúncios {scope_label}: "
                f"{drop:.1f}%"
            )
            return 20

        reasons.append(
            "Preço moderadamente abaixo "
            f"dos anúncios {scope_label}: "
            f"{drop:.1f}%"
        )

        return 8

    @staticmethod
    def _score_drop(
        drop: float | None,
        label: str,
        reasons: list[str],
        maximum_score: int,
    ) -> int:
        if drop is None:
            return 0

        if drop >= 60:
            reasons.append(
                f"Preço extremamente abaixo "
                f"da {label}: {drop:.1f}%"
            )
            return min(80, maximum_score)

        if drop >= 45:
            reasons.append(
                f"Preço muito abaixo da "
                f"{label}: {drop:.1f}%"
            )
            return min(70, maximum_score)

        if drop >= 35:
            reasons.append(
                f"Preço fortemente abaixo "
                f"da {label}: {drop:.1f}%"
            )
            return min(60, maximum_score)

        if drop >= 25:
            reasons.append(
                f"Preço bem abaixo da "
                f"{label}: {drop:.1f}%"
            )
            return min(50, maximum_score)

        if drop >= 15:
            reasons.append(
                f"Preço abaixo da "
                f"{label}: {drop:.1f}%"
            )
            return min(35, maximum_score)

        if drop >= 8:
            reasons.append(
                f"Queda moderada contra "
                f"a {label}: {drop:.1f}%"
            )
            return min(20, maximum_score)

        return 0

    @staticmethod
    def _analyze_advertised_discount(
        product: Product,
        reasons: list[str],
    ) -> int:
        discount = (
            PriceAnalyzer
            ._calculate_drop_percentage(
                current_price=product.price,
                reference_price=product.old_price,
            )
        )

        if discount is None:
            return 0

        if discount >= 60:
            reasons.append(
                "Desconto anunciado muito "
                f"elevado: {discount:.1f}%"
            )
            return 10

        if discount >= 40:
            reasons.append(
                "Desconto anunciado elevado: "
                f"{discount:.1f}%"
            )
            return 7

        if discount >= 25:
            reasons.append(
                "Bom desconto anunciado: "
                f"{discount:.1f}%"
            )
            return 4

        return 0

    @staticmethod
    def _analyze_reliability(
        product: Product,
        reasons: list[str],
    ) -> int:
        score = 0

        if product.official_store:
            reasons.append(
                "Produto vendido por loja oficial"
            )
            score += 5

        if product.full:
            reasons.append(
                "Produto enviado pelo FULL"
            )
            score += 3

        if product.shipping:
            shipping = product.shipping.lower()

            if (
                "grátis" in shipping
                or "gratis" in shipping
            ):
                reasons.append("Frete grátis")
                score += 2

        return score

    @staticmethod
    def _analyze_product_data(
        product: Product,
        reasons: list[str],
    ) -> int:
        penalty = 0

        if (
            product.price is None
            or product.price <= 0
        ):
            reasons.append(
                "Produto sem preço válido"
            )
            penalty -= 50

        if not product.id:
            reasons.append(
                "Produto sem identificador válido"
            )
            penalty -= 10

        if not product.link:
            reasons.append(
                "Produto sem link válido"
            )
            penalty -= 20

        return penalty

    def _classify_opportunity(
        self,
        product: Product,
        statistics: PriceStatistics | None,
        peer_statistics: PeerPriceStatistics | None,
        score: int,
    ) -> tuple[str, str]:
        historical_drop = None
        peer_drop = None

        if (
            statistics is not None
            and statistics.observations
            >= self.minimum_history_observations
        ):
            historical_drop = (
                self._calculate_drop_percentage(
                    current_price=product.price,
                    reference_price=(
                        statistics.median_price
                    ),
                )
            )

        if peer_statistics is not None:
            peer_drop = (
                self._calculate_drop_percentage(
                    current_price=product.price,
                    reference_price=(
                        peer_statistics.median_price
                    ),
                )
            )

        historical_drop = historical_drop or 0
        peer_drop = peer_drop or 0

        # Erro de preço pode ser identificado por histórico
        # ou por uma diferença extrema frente ao mercado.
        if (
            historical_drop >= 45
            or peer_drop >= 45
        ):
            return (
                "possivel_erro_preco",
                "muito alta",
            )

        # Só chamamos de queda histórica quando a queda
        # realmente veio do histórico do próprio anúncio.
        if historical_drop >= 25:
            return (
                "queda_historica",
                "alta",
            )

        # Diferenças relevantes contra o mercado são promoções,
        # não quedas históricas.
        if (
            peer_drop >= 15
            or historical_drop >= 10
            or score >= 70
        ):
            return (
                "promocao",
                "media",
            )

        return (
            "normal",
            "baixa",
        )

    @staticmethod
    def _calculate_drop_percentage(
        current_price: float | None,
        reference_price: float | None,
    ) -> float | None:
        if (
            current_price is None
            or reference_price is None
        ):
            return None

        if (
            current_price <= 0
            or reference_price <= 0
        ):
            return None

        if current_price >= reference_price:
            return 0.0

        return round(
            (
                (
                    reference_price
                    - current_price
                )
                / reference_price
            )
            * 100,
            2,
        )
import statistics
from dataclasses import dataclass

from entities.product import Product
from entities.product_profile import (
    ProductProfile,
)


@dataclass(frozen=True)
class PeerPriceStatistics:
    comparison_key: str
    comparison_scope: str

    observations: int

    minimum_price: float
    maximum_price: float
    average_price: float
    median_price: float


class PeerPriceAnalyzer:
    """
    Calcula referências de preço entre produtos equivalentes.

    Hierarquia:

    1. strict_key
       Mesmo modelo.

    2. tier_key
       Mesma classe técnica.

    3. broad_key
       Grupo geral.

    Além disso:

    - nacionais só com nacionais;
    - internacionais só com internacionais;
    - vários anúncios do mesmo vendedor são consolidados
      antes de calcular a referência.
    """

    def __init__(
        self,
        minimum_strict_peers: int = 1,
        minimum_tier_peers: int = 2,
        minimum_broad_peers: int = 6,
    ):
        self.minimum_strict_peers = (
            minimum_strict_peers
        )

        self.minimum_tier_peers = (
            minimum_tier_peers
        )

        self.minimum_broad_peers = (
            minimum_broad_peers
        )

    def get_product_statistics(
        self,
        product: Product,
        products: list[Product],
        profiles: dict[
            str,
            ProductProfile,
        ],
    ) -> PeerPriceStatistics | None:
        profile = profiles.get(
            product.id
        )

        if profile is None:
            return None

        # ======================================================
        # STRICT
        # ======================================================

        strict_statistics = (
            self._get_statistics_for_key(
                product=product,
                products=products,
                profiles=profiles,
                comparison_key=(
                    profile.strict_key
                ),
                key_type="strict",
                minimum_peers=(
                    self.minimum_strict_peers
                ),
                scope=(
                    self._build_scope_name(
                        base_scope=(
                            "modelo_exato"
                        ),
                        product=product,
                    )
                ),
            )
        )

        if strict_statistics is not None:
            return strict_statistics

        # ======================================================
        # TIER
        # ======================================================

        tier_statistics = (
            self._get_statistics_for_key(
                product=product,
                products=products,
                profiles=profiles,
                comparison_key=(
                    profile.tier_key
                ),
                key_type="tier",
                minimum_peers=(
                    self.minimum_tier_peers
                ),
                scope=(
                    self._build_scope_name(
                        base_scope=(
                            "mesmo_tier"
                        ),
                        product=product,
                    )
                ),
            )
        )

        if tier_statistics is not None:
            return tier_statistics

        # ======================================================
        # BROAD
        # ======================================================

        return self._get_statistics_for_key(
            product=product,
            products=products,
            profiles=profiles,
            comparison_key=(
                profile.broad_key
            ),
            key_type="broad",
            minimum_peers=(
                self.minimum_broad_peers
            ),
            scope=(
                self._build_scope_name(
                    base_scope=(
                        "grupo_geral"
                    ),
                    product=product,
                )
            ),
        )

    @staticmethod
    def calculate_drop_percentage(
        current_price: float | None,
        statistics: (
            PeerPriceStatistics | None
        ),
    ) -> float | None:
        if (
            current_price is None
            or current_price <= 0
            or statistics is None
            or statistics.median_price <= 0
        ):
            return None

        if (
            current_price
            >= statistics.median_price
        ):
            return 0.0

        return round(
            (
                (
                    statistics.median_price
                    - current_price
                )
                / statistics.median_price
            )
            * 100,
            2,
        )

    @staticmethod
    def _get_statistics_for_key(
        *,
        product: Product,
        products: list[Product],
        profiles: dict[
            str,
            ProductProfile,
        ],
        comparison_key: str | None,
        key_type: str,
        minimum_peers: int,
        scope: str,
    ) -> PeerPriceStatistics | None:
        if comparison_key is None:
            return None

        matching_peers: list[
            Product
        ] = []

        for peer in products:
            if (
                peer.id
                == product.id
            ):
                continue

            if (
                peer.price is None
                or peer.price <= 0
            ):
                continue

            if (
                peer.international
                != product.international
            ):
                continue

            peer_profile = (
                profiles.get(
                    peer.id
                )
            )

            if peer_profile is None:
                continue

            if key_type == "strict":
                peer_key = (
                    peer_profile.strict_key
                )

            elif key_type == "tier":
                peer_key = (
                    peer_profile.tier_key
                )

            else:
                peer_key = (
                    peer_profile.broad_key
                )

            if (
                peer_key
                != comparison_key
            ):
                continue

            matching_peers.append(
                peer
            )

        # ======================================================
        # DEDUPLICAÇÃO COMERCIAL
        #
        # Consolida vários anúncios do mesmo vendedor.
        # ======================================================

        peer_prices = (
            PeerPriceAnalyzer
            ._consolidate_by_seller(
                matching_peers
            )
        )

        if (
            len(peer_prices)
            < minimum_peers
        ):
            return None

        filtered_prices = (
            PeerPriceAnalyzer
            ._remove_extreme_outliers(
                peer_prices
            )
        )

        if (
            len(filtered_prices)
            < minimum_peers
        ):
            return None

        return PeerPriceStatistics(
            comparison_key=(
                comparison_key
            ),

            comparison_scope=scope,

            observations=len(
                filtered_prices
            ),

            minimum_price=min(
                filtered_prices
            ),

            maximum_price=max(
                filtered_prices
            ),

            average_price=(
                statistics.fmean(
                    filtered_prices
                )
            ),

            median_price=(
                statistics.median(
                    filtered_prices
                )
            ),
        )

    @staticmethod
    def _consolidate_by_seller(
        peers: list[Product],
    ) -> list[float]:
        """
        Consolida anúncios equivalentes por vendedor.

        Um vendedor pode possuir vários anúncios do mesmo
        produto ou da mesma classe.

        Sem consolidação:

            Loja A: 2300
            Loja A: 2310
            Loja A: 2320
            Loja B: 2700
            Loja C: 2750

        Loja A teria peso 3.

        Com consolidação:

            Loja A → mediana dos anúncios
            Loja B → mediana dos anúncios
            Loja C → mediana dos anúncios

        Cada vendedor passa a representar apenas uma
        observação comercial.
        """

        seller_prices: dict[
            str,
            list[float],
        ] = {}

        anonymous_prices: list[
            float
        ] = []

        for peer in peers:
            if (
                peer.price is None
                or peer.price <= 0
            ):
                continue

            seller = (
                peer.seller
                or ""
            ).strip().lower()

            # Se não conhecemos o vendedor,
            # não juntamos anúncios diferentes
            # artificialmente.
            if not seller:
                anonymous_prices.append(
                    peer.price
                )

                continue

            seller_prices.setdefault(
                seller,
                [],
            ).append(
                peer.price
            )

        consolidated_prices: list[
            float
        ] = []

        for prices in (
            seller_prices.values()
        ):
            consolidated_prices.append(
                float(
                    statistics.median(
                        prices
                    )
                )
            )

        consolidated_prices.extend(
            anonymous_prices
        )

        return consolidated_prices

    @staticmethod
    def _build_scope_name(
        *,
        base_scope: str,
        product: Product,
    ) -> str:
        origin = (
            "internacional"
            if product.international
            else "nacional"
        )

        return (
            f"{base_scope}_{origin}"
        )

    @staticmethod
    def _remove_extreme_outliers(
        prices: list[float],
    ) -> list[float]:
        """
        Remove valores extremos utilizando IQR.
        """

        if len(prices) < 6:
            return prices.copy()

        sorted_prices = sorted(
            prices
        )

        quartiles = (
            statistics.quantiles(
                sorted_prices,
                n=4,
                method="inclusive",
            )
        )

        first_quartile = (
            quartiles[0]
        )

        third_quartile = (
            quartiles[2]
        )

        interquartile_range = (
            third_quartile
            - first_quartile
        )

        if (
            interquartile_range
            <= 0
        ):
            return sorted_prices

        lower_limit = (
            first_quartile
            - 1.5
            * interquartile_range
        )

        upper_limit = (
            third_quartile
            + 1.5
            * interquartile_range
        )

        filtered = [
            price
            for price
            in sorted_prices
            if (
                lower_limit
                <= price
                <= upper_limit
            )
        ]

        return (
            filtered
            or sorted_prices
        )
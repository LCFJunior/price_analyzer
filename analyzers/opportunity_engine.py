from analyzers.bug_engine import (
    BugEngine,
)

from analyzers.peer_price_analyzer import (
    PeerPriceStatistics,
)

from analyzers.promotion_engine import (
    PromotionEngine,
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


class OpportunityEngine:
    """
    Coordenador dos motores de oportunidade.

    Fluxo:

    Produto
        ↓
    BugEngine
        ↓
    FAST PATH se bug extremo
        ↓
    PromotionEngine
        ↓
    melhor resultado
    """

    def __init__(
        self,
        *,
        bug_engine: BugEngine,
        promotion_engine: PromotionEngine,
    ):
        self.bug_engine = (
            bug_engine
        )

        self.promotion_engine = (
            promotion_engine
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
        # ======================================================
        # BUG ENGINE
        # ======================================================

        bug_opportunity = (
            self.bug_engine.analyze(
                product=product,
                profile=profile,
                statistics=statistics,
                peer_statistics=(
                    peer_statistics
                ),
            )
        )

        # ======================================================
        # FAST PATH
        #
        # Um possível erro de preço forte não precisa
        # esperar o PromotionEngine.
        # ======================================================

        if (
            bug_opportunity.should_notify
            and (
                bug_opportunity
                .opportunity_type
                == "possivel_erro_preco"
            )
        ):
            return bug_opportunity

        # ======================================================
        # PROMOTION ENGINE
        # ======================================================

        promotion_opportunity = (
            self.promotion_engine.analyze(
                product=product,
                profile=profile,
                statistics=statistics,
                peer_statistics=(
                    peer_statistics
                ),
            )
        )

        # ======================================================
        # PROMOÇÃO NOTIFICÁVEL
        # ======================================================

        if (
            promotion_opportunity
            .should_notify
        ):
            return (
                promotion_opportunity
            )

        # ======================================================
        # DIAGNÓSTICO
        #
        # Nenhum motor pediu notificação.
        # Retornamos o mais relevante.
        # ======================================================

        if (
            bug_opportunity.score
            > promotion_opportunity.score
        ):
            return bug_opportunity

        return promotion_opportunity
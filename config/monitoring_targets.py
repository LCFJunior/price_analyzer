from entities.monitoring_target import (
    MonitoringTarget,
)
from entities.search_rule import (
    SearchRule,
)


def get_monitoring_targets() -> list[
    MonitoringTarget
]:
    return [
        # ======================================================
        # GPU AMPLA
        #
        # Busca geral por placas de vídeo.
        #
        # O filtro inicial fica propositalmente mais aberto,
        # porque a triagem principal será feita pelo
        # GPUClassifier.
        #
        # Notificações ficam desligadas enquanto observamos
        # resultados reais do Mercado Livre.
        # ======================================================

        MonitoringTarget(
            name="Placas de Vídeo",

            search_query=(
                "Placa de Video"
            ),

            relevance_rule=SearchRule(
                required_terms=(
                    "placa",
                    "video",
                ),

                excluded_terms=(
                    "notebook",
                    "laptop",
                    "pc gamer",
                    "computador gamer",
                    "computador completo",
                    "kit upgrade",
                    "placa mae",
                    "placa-mãe",
                    "motherboard",
                    "waterblock",
                    "water block",
                    "suporte",
                    "riser",
                    "backplate",
                    "caixa vazia",
                    "ventoinha",
                    "fan para",
                    "cooler para",
                ),

                minimum_price=None,

                maximum_price=None,

                require_official_store=False,

                require_full=False,
            ),

            enabled=True,

            notifications_enabled=False,
        ),

        # ======================================================
        # CPU AMPLA
        # ======================================================

        MonitoringTarget(
            name="Processadores",

            search_query=(
                "Processador"
            ),

            relevance_rule=SearchRule(
                required_terms=(
                    "processador",
                ),

                excluded_terms=(
                    "processador de alimentos",
                    "processador alimentos",
                    "processador de audio",
                    "processador audio",
                    "processador digital de audio",
                    "processador digital audio",
                    "som automotivo",
                    "crossover",
                    "equalizador",
                    "mixer",
                    "mini processador",
                    "mini-processador",
                    "multiprocessador",
                    "pasta termica",
                    "pasta térmica",
                    "lamina",
                    "lâmina",
                    "laminas",
                    "lâminas",
                    "placa mae",
                    "placa-mãe",
                    "motherboard",
                    "kit upgrade",
                    "cooler para",
                    "caixa vazia",
                    "adesivo",
                    "blister",
                    "manual",
                ),

                minimum_price=None,

                maximum_price=None,

                require_official_store=False,

                require_full=False,
            ),

            enabled=True,

            notifications_enabled=False,
        ),

        # ======================================================
        # SSD AMPLA
        # ======================================================

        MonitoringTarget(
            name="SSD",

            search_query=(
                "SSD"
            ),

            relevance_rule=SearchRule(
                required_terms=(
                    "ssd",
                ),

                excluded_terms=(
                    "case",
                    "adaptador",
                    "gaveta",
                    "suporte",
                    "cabo",
                    "dock",
                    "docking",
                    "enclosure",
                ),

                minimum_price=None,

                maximum_price=None,

                require_official_store=False,

                require_full=False,
            ),

            enabled=True,

            notifications_enabled=False,
        ),
    ]
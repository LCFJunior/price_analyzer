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
        # GPU
        # ======================================================

        MonitoringTarget(
            name="NVIDIA RTX 5070 12GB",

            search_query="RTX 5070",

            relevance_rule=SearchRule(
                required_terms=(
                    "rtx",
                    "5070",
                ),

                excluded_terms=(
                    "5070 ti",
                    "5070ti",
                ),

                minimum_price=None,
                maximum_price=None,

                require_official_store=False,
                require_full=False,
            ),

            enabled=True,

            notifications_enabled=True,
        ),

        # ======================================================
        # PROCESSADORES
        # ======================================================

        MonitoringTarget(
            name="Processadores",

            search_query="Processador",

            relevance_rule=SearchRule(
                required_terms=(
                    "processador",
                ),

                excluded_terms=(
                    # ------------------------------------------
                    # Kits / acessórios de computador
                    # ------------------------------------------

                    "kit",
                    "kit upgrade",

                    "placa mae",
                    "placa-mãe",
                    "motherboard",

                    "caixa vazia",
                    "caixa do processador",
                    "embalagem vazia",

                    "adesivo",
                    "sticker",
                    "blister",
                    "manual",
                    "chaveiro",

                    "cooler para",
                    "water cooler para",
                    "suporte para",

                    "pasta termica",
                    "pasta térmica",

                    # ------------------------------------------
                    # Áudio automotivo
                    # ------------------------------------------

                    "processador de audio",
                    "processador de áudio",
                    "processador audio",
                    "processador áudio",

                    "som automotivo",

                    "crossover",
                    "equalizador",

                    "stetsom",
                    "taramps",

                    # ------------------------------------------
                    # Eletrodomésticos / alimentos
                    # ------------------------------------------

                    "processador de alimentos",
                    "mini processador",
                    "multiprocessador",

                    "mixer",

                    "walita",
                    "oster",
                    "kian",

                    "laminas",
                    "lâminas",

                    "250ml",
                    "500ml",
                ),

                minimum_price=None,
                maximum_price=None,

                require_official_store=False,
                require_full=False,
            ),

            enabled=True,

            # Mantemos observação até completar
            # esta rodada de validação.
            notifications_enabled=False,
        ),

        # ======================================================
        # SSD
        # ======================================================

        MonitoringTarget(
            name="SSDs",

            search_query="SSD",

            relevance_rule=SearchRule(
                required_terms=(
                    "ssd",
                ),

                excluded_terms=(
                    "case",
                    "case externo",
                    "adaptador",
                    "adaptador ssd",
                    "gaveta",
                    "caddy",
                    "suporte",
                    "cabo",
                    "enclosure",
                    "leitor",
                    "dock",
                    "docking",
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
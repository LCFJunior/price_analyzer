from dataclasses import dataclass

from entities.search_rule import (
    SearchRule,
)


@dataclass(frozen=True)
class MonitoringTarget:
    name: str

    search_query: str

    relevance_rule: SearchRule

    enabled: bool = True

    notifications_enabled: bool = True
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CandidateValidationResult:
    status: str

    reasons: tuple[str, ...] = field(
        default_factory=tuple
    )

    inspected_fields: tuple[str, ...] = field(
        default_factory=tuple
    )

    @property
    def is_valid(self) -> bool:
        return self.status == "valid"

    @property
    def is_invalid(self) -> bool:
        return self.status == "invalid"

    @property
    def is_inconclusive(self) -> bool:
        return self.status == "inconclusive"
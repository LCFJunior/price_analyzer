from typing import Protocol

from entities.candidate_validation import (
    CandidateValidationResult,
)
from entities.product import Product


class CandidateValidator(Protocol):
    def validate(
        self,
        product: Product,
    ) -> CandidateValidationResult:
        ...
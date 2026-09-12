from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


T = TypeVar("T")


class UnavailableReason(Enum):
    VALUE_ABSENT = "VALUE_ABSENT"
    CONCEPT_ABSENT = "CONCEPT_ABSENT"
    EVIDENCE_INDETERMINATE = "EVIDENCE_INDETERMINATE"
    TRANSFORMATION_NOT_APPLIED = "TRANSFORMATION_NOT_APPLIED"
    TRANSFORMATION_UNRESOLVED = "TRANSFORMATION_UNRESOLVED"


@dataclass(frozen=True)
class ObservedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class DerivedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class SimulatedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class UnavailableEvidence:
    reason: UnavailableReason


FieldEvidence = (
    ObservedEvidence[T]
    | DerivedEvidence[T]
    | SimulatedEvidence[T]
    | UnavailableEvidence
)

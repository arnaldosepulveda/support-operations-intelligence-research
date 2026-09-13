from collections.abc import Mapping
from dataclasses import dataclass

from support_operations_intelligence.case import Case
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)


@dataclass(frozen=True)
class CalgaryMappedCase:
    case: Case
    source_status: ObservedEvidence[str] | UnavailableEvidence


def map_calgary_source_status(
    record: Mapping[str, object],
) -> ObservedEvidence[str] | UnavailableEvidence:
    if "status_description" not in record:
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    value = record["status_description"]

    if value is None:
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    if not isinstance(value, str):
        return UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE)

    if value == "":
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    if value.isspace():
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    return ObservedEvidence(value)

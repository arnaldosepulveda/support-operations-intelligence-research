from collections.abc import Mapping
from dataclasses import dataclass

from support_operations_intelligence.case import Case
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import (
    RejectedIdentity,
    admit_calgary_source_identity,
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


CalgaryCaseMappingResult = CalgaryMappedCase | RejectedIdentity


def map_calgary_case(
    record: Mapping[str, object],
) -> CalgaryCaseMappingResult:
    identity_result = admit_calgary_source_identity(record)

    if isinstance(identity_result, RejectedIdentity):
        return identity_result

    case = Case(case_id=identity_result.case_id)
    source_status = map_calgary_source_status(record)

    return CalgaryMappedCase(
        case=case,
        source_status=source_status,
    )

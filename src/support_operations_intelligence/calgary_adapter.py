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


@dataclass(frozen=True)
class CalgarySourceNativeEvidence:
    source: ObservedEvidence[str] | UnavailableEvidence
    service_name: ObservedEvidence[str] | UnavailableEvidence
    agency_responsible: ObservedEvidence[str] | UnavailableEvidence
    updated_date: ObservedEvidence[str] | UnavailableEvidence
    closed_date: ObservedEvidence[str] | UnavailableEvidence


def _map_source_native_lexical_field(
    record: Mapping[str, object],
    field_name: str,
) -> ObservedEvidence[str] | UnavailableEvidence:
    if field_name not in record:
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    value = record[field_name]

    if value is None:
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    if not isinstance(value, str):
        return UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE)

    if value == "":
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    if value.isspace():
        return UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

    return ObservedEvidence(value)


def map_calgary_source_native_evidence(
    record: Mapping[str, object],
) -> CalgarySourceNativeEvidence:
    return CalgarySourceNativeEvidence(
        source=_map_source_native_lexical_field(record, "source"),
        service_name=_map_source_native_lexical_field(
            record, "service_name"
        ),
        agency_responsible=_map_source_native_lexical_field(
            record, "agency_responsible"
        ),
        updated_date=_map_source_native_lexical_field(
            record, "updated_date"
        ),
        closed_date=_map_source_native_lexical_field(
            record, "closed_date"
        ),
    )


@dataclass(frozen=True)
class CalgaryAdaptedCase:
    mapped_case: CalgaryMappedCase
    source_native: CalgarySourceNativeEvidence


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


CalgaryAdapterResult = CalgaryAdaptedCase | RejectedIdentity


def adapt_calgary_record(
    record: Mapping[str, object],
) -> CalgaryAdapterResult:
    mapped_result = map_calgary_case(record)

    if isinstance(mapped_result, RejectedIdentity):
        return mapped_result

    source_native = map_calgary_source_native_evidence(record)

    return CalgaryAdaptedCase(
        mapped_case=mapped_result,
        source_native=source_native,
    )

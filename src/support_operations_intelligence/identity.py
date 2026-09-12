from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class CaseId:
    source_system: str
    source_case_id: str


class IdentityRejectionReason(Enum):
    MISSING_SOURCE_CASE_ID = "MISSING_SOURCE_CASE_ID"
    NULL_SOURCE_CASE_ID = "NULL_SOURCE_CASE_ID"
    NON_STRING_SOURCE_CASE_ID = "NON_STRING_SOURCE_CASE_ID"
    EMPTY_SOURCE_CASE_ID = "EMPTY_SOURCE_CASE_ID"
    WHITESPACE_ONLY_SOURCE_CASE_ID = "WHITESPACE_ONLY_SOURCE_CASE_ID"


@dataclass(frozen=True)
class AcceptedIdentity:
    case_id: CaseId


@dataclass(frozen=True)
class RejectedIdentity:
    reason: IdentityRejectionReason


IdentityAdmissionResult = AcceptedIdentity | RejectedIdentity


def admit_calgary_source_identity(
    record: Mapping[str, object],
) -> IdentityAdmissionResult:
    if "service_request_id" not in record:
        return RejectedIdentity(
            reason=IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )

    value = record["service_request_id"]

    if value is None:
        return RejectedIdentity(
            reason=IdentityRejectionReason.NULL_SOURCE_CASE_ID,
        )

    if not isinstance(value, str):
        return RejectedIdentity(
            reason=IdentityRejectionReason.NON_STRING_SOURCE_CASE_ID,
        )

    if value == "":
        return RejectedIdentity(
            reason=IdentityRejectionReason.EMPTY_SOURCE_CASE_ID,
        )

    if value.isspace():
        return RejectedIdentity(
            reason=IdentityRejectionReason.WHITESPACE_ONLY_SOURCE_CASE_ID,
        )

    return AcceptedIdentity(
        case_id=CaseId(
            source_system="city_of_calgary_311",
            source_case_id=value,
        )
    )

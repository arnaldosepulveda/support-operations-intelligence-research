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

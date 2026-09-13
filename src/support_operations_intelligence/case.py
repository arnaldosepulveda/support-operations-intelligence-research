from dataclasses import dataclass

from support_operations_intelligence.identity import CaseId


@dataclass(frozen=True)
class Case:
    case_id: CaseId

from dataclasses import dataclass


@dataclass(frozen=True)
class CaseId:
    source_system: str
    source_case_id: str

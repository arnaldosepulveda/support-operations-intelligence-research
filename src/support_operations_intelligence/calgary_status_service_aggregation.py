from collections.abc import Iterable
from dataclasses import dataclass

from support_operations_intelligence.calgary_adapter import CalgaryAdapterResult
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
)
from support_operations_intelligence.identity import (
    IdentityRejectionReason,
    RejectedIdentity,
)


CalgaryGroupingEvidence = ObservedEvidence[str] | UnavailableEvidence
CalgaryStatusServiceKey = tuple[
    CalgaryGroupingEvidence,
    CalgaryGroupingEvidence,
]


@dataclass(frozen=True)
class CalgaryStatusServiceAggregation:
    total_logical_records_seen: int
    total_admitted_records: int
    total_rejected_identity_records: int
    rejection_counts_by_reason: dict[IdentityRejectionReason, int]
    aggregated_record_count: int
    aggregated_counts: dict[CalgaryStatusServiceKey, int]


def aggregate_calgary_status_by_service(
    results: Iterable[CalgaryAdapterResult],
) -> CalgaryStatusServiceAggregation:
    total_logical_records_seen = 0
    total_admitted_records = 0
    total_rejected_identity_records = 0
    rejection_counts_by_reason: dict[IdentityRejectionReason, int] = {}
    aggregated_counts: dict[CalgaryStatusServiceKey, int] = {}

    for result in results:
        total_logical_records_seen += 1

        if isinstance(result, RejectedIdentity):
            total_rejected_identity_records += 1
            rejection_counts_by_reason[result.reason] = (
                rejection_counts_by_reason.get(result.reason, 0) + 1
            )
            continue

        total_admitted_records += 1
        key = (
            result.mapped_case.source_status,
            result.source_native.service_name,
        )
        aggregated_counts[key] = aggregated_counts.get(key, 0) + 1

    return CalgaryStatusServiceAggregation(
        total_logical_records_seen=total_logical_records_seen,
        total_admitted_records=total_admitted_records,
        total_rejected_identity_records=total_rejected_identity_records,
        rejection_counts_by_reason=rejection_counts_by_reason,
        aggregated_record_count=total_admitted_records,
        aggregated_counts=aggregated_counts,
    )

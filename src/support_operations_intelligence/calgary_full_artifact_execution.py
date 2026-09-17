from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from support_operations_intelligence.calgary_adapter import (
    CalgaryAdaptedCase,
    CalgaryAdapterResult,
    adapt_calgary_record,
)
from support_operations_intelligence.calgary_csv import (
    iter_calgary_csv_records,
    verify_calgary_csv_artifact_sha256,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    CalgaryGroupingEvidence,
    CalgaryStatusServiceAggregation,
    aggregate_calgary_status_by_service,
)
from support_operations_intelligence.evidence import (
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import RejectedIdentity


class CalgaryFullArtifactAccountingError(Exception):
    pass


def _require_accounting(condition: bool, invariant: str) -> None:
    if not condition:
        raise CalgaryFullArtifactAccountingError(invariant)


@dataclass(frozen=True)
class CalgaryFullArtifactCounterSummary:
    rows_observed: int
    rows_structurally_accepted: int
    rows_structurally_rejected: int
    rows_identity_admitted: int
    rows_identity_rejected: int
    distinct_source_case_ids: int
    source_case_ids_appearing_more_than_once: int
    rows_involved_in_duplication: int
    blank_service_name: int
    blank_agency_responsible: int
    blank_status_description: int
    status_vocabulary: dict[CalgaryGroupingEvidence, int]
    service_name_vocabulary: dict[CalgaryGroupingEvidence, int]

    def __post_init__(self) -> None:
        _validate_counter_summary(self)


@dataclass(frozen=True)
class CalgaryFullArtifactExecutionResult:
    verified_sha256: str
    aggregation: CalgaryStatusServiceAggregation
    counter_summary: CalgaryFullArtifactCounterSummary

    def __post_init__(self) -> None:
        _validate_completed_result(
            self.counter_summary,
            self.aggregation,
        )


def _is_value_absent(evidence: CalgaryGroupingEvidence) -> bool:
    return (
        isinstance(evidence, UnavailableEvidence)
        and evidence.reason is UnavailableReason.VALUE_ABSENT
    )


@dataclass
class _CounterAccumulator:
    rows_observed: int = 0
    rows_structurally_accepted: int = 0
    rows_identity_admitted: int = 0
    rows_identity_rejected: int = 0
    seen_source_case_ids: set[str] = field(default_factory=set)
    duplicate_source_case_ids: set[str] = field(default_factory=set)
    rows_involved_in_duplication: int = 0
    blank_service_name: int = 0
    blank_agency_responsible: int = 0
    blank_status_description: int = 0
    status_vocabulary: dict[CalgaryGroupingEvidence, int] = field(
        default_factory=dict
    )
    service_name_vocabulary: dict[CalgaryGroupingEvidence, int] = field(
        default_factory=dict
    )

    def observe(self, result: CalgaryAdapterResult) -> None:
        self.rows_observed += 1
        self.rows_structurally_accepted += 1

        if isinstance(result, RejectedIdentity):
            self.rows_identity_rejected += 1
            return

        self.rows_identity_admitted += 1
        self._observe_admitted_identity(result)
        self._observe_admitted_evidence(result)

    def _observe_admitted_identity(self, result: CalgaryAdaptedCase) -> None:
        source_case_id = result.mapped_case.case.case_id.source_case_id

        if source_case_id not in self.seen_source_case_ids:
            self.seen_source_case_ids.add(source_case_id)
        elif source_case_id not in self.duplicate_source_case_ids:
            self.duplicate_source_case_ids.add(source_case_id)
            self.rows_involved_in_duplication += 2
        else:
            self.rows_involved_in_duplication += 1

    def _observe_admitted_evidence(self, result: CalgaryAdaptedCase) -> None:
        status = result.mapped_case.source_status
        service_name = result.source_native.service_name
        agency_responsible = result.source_native.agency_responsible

        self.status_vocabulary[status] = (
            self.status_vocabulary.get(status, 0) + 1
        )
        self.service_name_vocabulary[service_name] = (
            self.service_name_vocabulary.get(service_name, 0) + 1
        )

        if _is_value_absent(service_name):
            self.blank_service_name += 1
        if _is_value_absent(agency_responsible):
            self.blank_agency_responsible += 1
        if _is_value_absent(status):
            self.blank_status_description += 1

    def summary(self) -> CalgaryFullArtifactCounterSummary:
        return CalgaryFullArtifactCounterSummary(
            rows_observed=self.rows_observed,
            rows_structurally_accepted=self.rows_structurally_accepted,
            rows_structurally_rejected=0,
            rows_identity_admitted=self.rows_identity_admitted,
            rows_identity_rejected=self.rows_identity_rejected,
            distinct_source_case_ids=len(self.seen_source_case_ids),
            source_case_ids_appearing_more_than_once=len(
                self.duplicate_source_case_ids
            ),
            rows_involved_in_duplication=self.rows_involved_in_duplication,
            blank_service_name=self.blank_service_name,
            blank_agency_responsible=self.blank_agency_responsible,
            blank_status_description=self.blank_status_description,
            status_vocabulary=dict(self.status_vocabulary),
            service_name_vocabulary=dict(self.service_name_vocabulary),
        )


def _adapt_and_count_records(
    records: Iterator[Mapping[str, str]],
    accumulator: _CounterAccumulator,
) -> Iterator[CalgaryAdapterResult]:
    for record in records:
        result = adapt_calgary_record(record)
        accumulator.observe(result)
        yield result


def _validate_counter_summary(
    summary: CalgaryFullArtifactCounterSummary,
) -> None:
    _require_accounting(
        summary.rows_observed
        == summary.rows_structurally_accepted
        + summary.rows_structurally_rejected,
        "rows observed must equal structurally accepted plus rejected",
    )
    _require_accounting(
        summary.rows_structurally_accepted
        == summary.rows_identity_admitted + summary.rows_identity_rejected,
        "structurally accepted must equal identity admitted plus rejected",
    )
    _require_accounting(
        summary.rows_structurally_rejected == 0,
        "successful execution cannot contain structural rejections",
    )
    _require_accounting(
        summary.distinct_source_case_ids <= summary.rows_identity_admitted,
        "distinct source identifiers cannot exceed admitted rows",
    )
    _require_accounting(
        summary.source_case_ids_appearing_more_than_once
        <= summary.distinct_source_case_ids,
        "repeated source identifiers cannot exceed distinct identifiers",
    )
    _require_accounting(
        summary.rows_involved_in_duplication
        <= summary.rows_identity_admitted,
        "rows involved in duplication cannot exceed admitted rows",
    )
    _require_accounting(
        sum(summary.status_vocabulary.values())
        == summary.rows_identity_admitted,
        "status vocabulary must sum to admitted rows",
    )
    _require_accounting(
        sum(summary.service_name_vocabulary.values())
        == summary.rows_identity_admitted,
        "service vocabulary must sum to admitted rows",
    )


def _validate_completed_result(
    summary: CalgaryFullArtifactCounterSummary,
    aggregation: CalgaryStatusServiceAggregation,
) -> None:
    _require_accounting(
        aggregation.total_logical_records_seen
        == aggregation.total_admitted_records
        + aggregation.total_rejected_identity_records,
        "aggregation seen must equal admitted plus rejected",
    )
    _require_accounting(
        sum(aggregation.rejection_counts_by_reason.values())
        == aggregation.total_rejected_identity_records,
        "rejection reasons must sum to rejected records",
    )
    _require_accounting(
        sum(aggregation.aggregated_counts.values())
        == aggregation.aggregated_record_count,
        "aggregate counts must sum to aggregated records",
    )
    _require_accounting(
        aggregation.aggregated_record_count
        == summary.rows_identity_admitted,
        "aggregated records must equal admitted rows",
    )
    _require_accounting(
        aggregation.total_logical_records_seen
        == summary.rows_structurally_accepted,
        "aggregation seen must equal structurally accepted rows",
    )
    _require_accounting(
        aggregation.total_admitted_records == summary.rows_identity_admitted,
        "aggregation admitted must equal identity-admitted rows",
    )
    _require_accounting(
        aggregation.total_rejected_identity_records
        == summary.rows_identity_rejected,
        "aggregation rejected must equal identity-rejected rows",
    )


def execute_calgary_full_artifact(
    path: Path,
    expected_sha256: str,
) -> CalgaryFullArtifactExecutionResult:
    verified_sha256 = verify_calgary_csv_artifact_sha256(
        path,
        expected_sha256,
    )
    records = iter_calgary_csv_records(path)
    accumulator = _CounterAccumulator()
    aggregation = aggregate_calgary_status_by_service(
        _adapt_and_count_records(records, accumulator)
    )
    counter_summary = accumulator.summary()

    return CalgaryFullArtifactExecutionResult(
        verified_sha256=verified_sha256,
        aggregation=aggregation,
        counter_summary=counter_summary,
    )

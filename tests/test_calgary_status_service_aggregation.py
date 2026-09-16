import unittest

from support_operations_intelligence.calgary_adapter import (
    CalgaryAdaptedCase,
    adapt_calgary_record,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    aggregate_calgary_status_by_service,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import (
    IdentityRejectionReason,
    RejectedIdentity,
)


_MISSING = object()


def _synthetic_record(
    case_id="SYNTHETIC-001",
    status_description="Closed",
    service_name="Synthetic Service",
):
    record = {"service_request_id": case_id}

    if status_description is not _MISSING:
        record["status_description"] = status_description

    if service_name is not _MISSING:
        record["service_name"] = service_name

    return record


def _adapted_result(
    case_id="SYNTHETIC-001",
    status_description="Closed",
    service_name="Synthetic Service",
):
    result = adapt_calgary_record(
        _synthetic_record(
            case_id=case_id,
            status_description=status_description,
            service_name=service_name,
        )
    )
    if not isinstance(result, CalgaryAdaptedCase):
        raise AssertionError("synthetic admitted fixture was rejected")
    return result


def _aggregation_key(result):
    return (
        result.mapped_case.source_status,
        result.source_native.service_name,
    )


class CalgaryStatusServiceAggregationTests(unittest.TestCase):
    def test_identical_observed_pair_aggregates_to_one_key(self):
        first = _adapted_result(case_id="SYNTHETIC-001")
        second = _adapted_result(case_id="SYNTHETIC-002")

        result = aggregate_calgary_status_by_service([first, second])

        self.assertEqual(result.total_logical_records_seen, 2)
        self.assertEqual(result.total_admitted_records, 2)
        self.assertEqual(result.total_rejected_identity_records, 0)
        self.assertEqual(result.aggregated_record_count, 2)
        self.assertEqual(
            result.aggregated_counts,
            {_aggregation_key(first): 2},
        )

    def test_exact_status_values_remain_distinct(self):
        first = _adapted_result(
            case_id="SYNTHETIC-001",
            status_description="Closed",
        )
        second = _adapted_result(
            case_id="SYNTHETIC-002",
            status_description="Complete",
        )

        result = aggregate_calgary_status_by_service([first, second])

        self.assertEqual(
            result.aggregated_counts,
            {
                _aggregation_key(first): 1,
                _aggregation_key(second): 1,
            },
        )

    def test_exact_service_values_remain_distinct(self):
        first = _adapted_result(
            case_id="SYNTHETIC-001",
            service_name="Synthetic Roads",
        )
        second = _adapted_result(
            case_id="SYNTHETIC-002",
            service_name="Synthetic Waste",
        )

        result = aggregate_calgary_status_by_service([first, second])

        self.assertEqual(
            result.aggregated_counts,
            {
                _aggregation_key(first): 1,
                _aggregation_key(second): 1,
            },
        )

    def test_status_case_and_whitespace_are_not_normalized(self):
        admitted = [
            _adapted_result(
                case_id="SYNTHETIC-001",
                status_description="Closed",
            ),
            _adapted_result(
                case_id="SYNTHETIC-002",
                status_description="closed",
            ),
            _adapted_result(
                case_id="SYNTHETIC-003",
                status_description=" Closed ",
            ),
        ]

        result = aggregate_calgary_status_by_service(admitted)

        self.assertEqual(
            result.aggregated_counts,
            {_aggregation_key(item): 1 for item in admitted},
        )
        self.assertEqual(len(result.aggregated_counts), 3)

    def test_observed_unknown_remains_distinct_from_unavailable(self):
        observed = _adapted_result(
            case_id="SYNTHETIC-001",
            status_description="UNKNOWN",
        )
        unavailable = _adapted_result(
            case_id="SYNTHETIC-002",
            status_description=_MISSING,
        )

        self.assertEqual(
            observed.mapped_case.source_status,
            ObservedEvidence("UNKNOWN"),
        )
        self.assertEqual(
            unavailable.mapped_case.source_status,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

        result = aggregate_calgary_status_by_service(
            [observed, unavailable]
        )

        self.assertEqual(
            result.aggregated_counts,
            {
                _aggregation_key(observed): 1,
                _aggregation_key(unavailable): 1,
            },
        )
        self.assertEqual(len(result.aggregated_counts), 2)

    def test_unavailable_reasons_remain_distinct(self):
        absent = _adapted_result(
            case_id="SYNTHETIC-001",
            status_description=_MISSING,
        )
        indeterminate = _adapted_result(
            case_id="SYNTHETIC-002",
            status_description=123,
        )

        self.assertEqual(
            absent.mapped_case.source_status,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )
        self.assertEqual(
            indeterminate.mapped_case.source_status,
            UnavailableEvidence(
                UnavailableReason.EVIDENCE_INDETERMINATE
            ),
        )

        result = aggregate_calgary_status_by_service(
            [absent, indeterminate]
        )

        self.assertEqual(
            result.aggregated_counts,
            {
                _aggregation_key(absent): 1,
                _aggregation_key(indeterminate): 1,
            },
        )
        self.assertEqual(len(result.aggregated_counts), 2)

    def test_explained_identity_rejection_is_accounted(self):
        rejected = adapt_calgary_record(
            {
                "status_description": "Closed",
                "service_name": "Synthetic Service",
            }
        )
        self.assertIsInstance(rejected, RejectedIdentity)
        self.assertIs(
            rejected.reason,
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )

        result = aggregate_calgary_status_by_service([rejected])

        self.assertEqual(result.total_logical_records_seen, 1)
        self.assertEqual(result.total_admitted_records, 0)
        self.assertEqual(result.total_rejected_identity_records, 1)
        self.assertEqual(result.aggregated_record_count, 0)
        self.assertEqual(result.aggregated_counts, {})
        self.assertEqual(result.rejection_counts_by_reason[rejected.reason], 1)

    def test_multiple_rejection_reasons_remain_distinct(self):
        missing = adapt_calgary_record({})
        null = adapt_calgary_record({"service_request_id": None})
        self.assertIsInstance(missing, RejectedIdentity)
        self.assertIsInstance(null, RejectedIdentity)
        self.assertIs(
            missing.reason,
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )
        self.assertIs(
            null.reason,
            IdentityRejectionReason.NULL_SOURCE_CASE_ID,
        )

        result = aggregate_calgary_status_by_service([missing, null])

        self.assertEqual(
            result.rejection_counts_by_reason,
            {
                missing.reason: 1,
                null.reason: 1,
            },
        )
        self.assertEqual(
            sum(result.rejection_counts_by_reason.values()),
            result.total_rejected_identity_records,
        )

    def test_mixed_results_satisfy_seen_accounting_postcondition(self):
        results = [
            _adapted_result(case_id="SYNTHETIC-001"),
            adapt_calgary_record({}),
            _adapted_result(case_id="SYNTHETIC-002"),
            adapt_calgary_record({"service_request_id": ""}),
        ]

        result = aggregate_calgary_status_by_service(results)

        self.assertEqual(
            result.total_logical_records_seen,
            result.total_admitted_records
            + result.total_rejected_identity_records,
        )

    def test_mixed_results_satisfy_aggregation_accounting_postcondition(self):
        results = [
            _adapted_result(case_id="SYNTHETIC-001"),
            adapt_calgary_record({"service_request_id": None}),
            _adapted_result(
                case_id="SYNTHETIC-002",
                status_description="Open",
            ),
        ]

        result = aggregate_calgary_status_by_service(results)

        self.assertEqual(
            sum(result.aggregated_counts.values()),
            result.aggregated_record_count,
        )
        self.assertEqual(
            result.aggregated_record_count,
            result.total_admitted_records,
        )

    def test_iterable_runtime_error_propagates_unchanged(self):
        admitted = _adapted_result(case_id="SYNTHETIC-001")

        def failing_results():
            yield admitted
            raise RuntimeError("synthetic iterable failure")

        with self.assertRaisesRegex(
            RuntimeError,
            "^synthetic iterable failure$",
        ):
            aggregate_calgary_status_by_service(failing_results())


if __name__ == "__main__":
    unittest.main()

import csv
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from support_operations_intelligence import calgary_adapter
from support_operations_intelligence.calgary_csv import (
    EXPECTED_CALGARY_HEADER,
    CalgaryCsvStructureError,
    CalgaryCsvStructureErrorReason,
    iter_calgary_csv_records,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    aggregate_calgary_status_by_service,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import IdentityRejectionReason


def _write_synthetic_csv(path: Path, rows: list[tuple[str, ...]]) -> None:
    with path.open(mode="w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows([EXPECTED_CALGARY_HEADER, *rows])


def _synthetic_row(
    service_request_id: str,
    *,
    status_description: str = "Closed",
    service_name: str = "Pothole",
) -> tuple[str, ...]:
    return (
        service_request_id,
        "2026-01-01",
        "2026-01-02",
        "",
        status_description,
        "Synthetic Source",
        service_name,
        "Synthetic Agency",
        "123 Synthetic Street",
        "SYN",
        "Synthetic Community",
        "Synthetic Location",
        "-114.0000",
        "51.0000",
        "POINT (-114.0000 51.0000)",
    )


def _aggregate_synthetic_csv(path: Path):
    return aggregate_calgary_status_by_service(
        calgary_adapter.adapt_calgary_record(record)
        for record in iter_calgary_csv_records(path)
    )


class CalgaryCsvAdapterAggregationCompositionTests(unittest.TestCase):
    def test_mixed_stream_preserves_accounting_and_evidence(self):
        rows = [
            _synthetic_row("synthetic-001"),
            _synthetic_row("synthetic-002"),
            _synthetic_row(
                "synthetic-003",
                status_description="UNKNOWN",
                service_name=" Drainage ",
            ),
            _synthetic_row(
                "synthetic-004",
                status_description="",
                service_name=" Drainage ",
            ),
            _synthetic_row(""),
        ]

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "mixed-composition.csv"
            _write_synthetic_csv(path, rows)

            result = _aggregate_synthetic_csv(path)

        closed_pothole_key = (
            ObservedEvidence("Closed"),
            ObservedEvidence("Pothole"),
        )
        observed_unknown_key = (
            ObservedEvidence("UNKNOWN"),
            ObservedEvidence(" Drainage "),
        )
        unavailable_status_key = (
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
            ObservedEvidence(" Drainage "),
        )

        self.assertEqual(result.total_logical_records_seen, 5)
        self.assertEqual(result.total_admitted_records, 4)
        self.assertEqual(result.total_rejected_identity_records, 1)
        self.assertEqual(result.aggregated_record_count, 4)
        self.assertEqual(
            result.total_logical_records_seen,
            result.total_admitted_records
            + result.total_rejected_identity_records,
        )
        self.assertEqual(
            result.rejection_counts_by_reason,
            {IdentityRejectionReason.EMPTY_SOURCE_CASE_ID: 1},
        )
        self.assertEqual(
            sum(result.rejection_counts_by_reason.values()),
            result.total_rejected_identity_records,
        )
        self.assertEqual(
            result.aggregated_counts,
            {
                closed_pothole_key: 2,
                observed_unknown_key: 1,
                unavailable_status_key: 1,
            },
        )
        self.assertEqual(
            sum(result.aggregated_counts.values()),
            result.aggregated_record_count,
        )
        self.assertEqual(
            result.aggregated_record_count,
            result.total_admitted_records,
        )

    def test_later_structural_failure_propagates_without_summary(self):
        valid_row = _synthetic_row("synthetic-001")
        malformed_row = _synthetic_row("synthetic-002")[:-1]
        summary = None

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "malformed-composition.csv"
            _write_synthetic_csv(path, [valid_row, malformed_row])

            with self.assertRaises(CalgaryCsvStructureError) as captured:
                summary = _aggregate_synthetic_csv(path)

        self.assertIsNone(summary)
        self.assertIs(
            captured.exception.reason,
            CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
        )
        self.assertEqual(captured.exception.logical_data_record_number, 2)

    def test_unexpected_adapter_runtime_error_propagates(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "adapter-failure.csv"
            _write_synthetic_csv(path, [_synthetic_row("synthetic-001")])

            with patch.object(
                calgary_adapter,
                "adapt_calgary_record",
                side_effect=RuntimeError("synthetic adapter failure"),
            ) as adapter:
                with self.assertRaisesRegex(
                    RuntimeError,
                    "^synthetic adapter failure$",
                ):
                    _aggregate_synthetic_csv(path)

        adapter.assert_called_once()


if __name__ == "__main__":
    unittest.main()

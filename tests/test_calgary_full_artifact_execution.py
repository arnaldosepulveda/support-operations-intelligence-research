import csv
import unittest
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from support_operations_intelligence.calgary_csv import (
    EXPECTED_CALGARY_HEADER,
    CalgaryCsvArtifactDigestMismatch,
)
from support_operations_intelligence.calgary_full_artifact_execution import (
    CalgaryFullArtifactAccountingError,
    CalgaryFullArtifactExecutionResult,
    execute_calgary_full_artifact,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    aggregate_calgary_status_by_service,
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


def _artifact_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class CalgaryFullArtifactExecutionTests(unittest.TestCase):
    def test_successful_synthetic_artifact_returns_verified_digest_and_aggregation(
        self,
    ):
        rows = [
            _synthetic_row("synthetic-001"),
            _synthetic_row(
                "synthetic-002",
                status_description="Open",
                service_name="Drainage",
            ),
            _synthetic_row(""),
        ]

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "full-domain-execution.csv"
            _write_synthetic_csv(path, rows)
            expected_sha256 = _artifact_sha256(path)

            result = execute_calgary_full_artifact(path, expected_sha256)

        self.assertIsInstance(result, CalgaryFullArtifactExecutionResult)
        self.assertEqual(result.verified_sha256, expected_sha256)

        aggregation = result.aggregation
        self.assertEqual(aggregation.total_logical_records_seen, 3)
        self.assertEqual(aggregation.total_admitted_records, 2)
        self.assertEqual(aggregation.total_rejected_identity_records, 1)
        self.assertEqual(aggregation.aggregated_record_count, 2)
        self.assertEqual(
            aggregation.rejection_counts_by_reason,
            {IdentityRejectionReason.EMPTY_SOURCE_CASE_ID: 1},
        )
        self.assertEqual(
            aggregation.total_logical_records_seen,
            aggregation.total_admitted_records
            + aggregation.total_rejected_identity_records,
        )
        self.assertEqual(
            sum(aggregation.rejection_counts_by_reason.values()),
            aggregation.total_rejected_identity_records,
        )
        self.assertEqual(
            sum(aggregation.aggregated_counts.values()),
            aggregation.aggregated_record_count,
        )
        self.assertEqual(
            aggregation.aggregated_record_count,
            aggregation.total_admitted_records,
        )

    def test_digest_mismatch_prevents_csv_traversal(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "digest-mismatch.csv"
            _write_synthetic_csv(path, [_synthetic_row("synthetic-001")])
            incorrect_sha256 = "0" * 64
            self.assertNotEqual(_artifact_sha256(path), incorrect_sha256)

            with patch(
                "support_operations_intelligence."
                "calgary_full_artifact_execution.iter_calgary_csv_records"
            ) as record_stream:
                with self.assertRaises(CalgaryCsvArtifactDigestMismatch):
                    execute_calgary_full_artifact(path, incorrect_sha256)

        record_stream.assert_not_called()

    def test_digest_verification_completes_before_record_stream_is_constructed(
        self,
    ):
        events: list[str] = []
        verified_sha256 = "a" * 64

        def verify_digest(path: Path, expected_sha256: str) -> str:
            events.append("digest_complete")
            return verified_sha256

        def construct_stream(path: Path):
            events.append("stream_constructed")
            return iter(())

        with patch(
            "support_operations_intelligence."
            "calgary_full_artifact_execution."
            "verify_calgary_csv_artifact_sha256",
            side_effect=verify_digest,
        ), patch(
            "support_operations_intelligence."
            "calgary_full_artifact_execution.iter_calgary_csv_records",
            side_effect=construct_stream,
        ):
            result = execute_calgary_full_artifact(
                Path("synthetic-not-opened.csv"),
                "expected synthetic digest",
            )

        self.assertEqual(
            events,
            ["digest_complete", "stream_constructed"],
        )
        self.assertEqual(result.verified_sha256, verified_sha256)

    def test_completed_accounting_inconsistency_raises_accounting_error(self):
        valid_empty_summary = aggregate_calgary_status_by_service(())
        inconsistent_summary = replace(
            valid_empty_summary,
            total_logical_records_seen=1,
        )

        with patch(
            "support_operations_intelligence."
            "calgary_full_artifact_execution."
            "verify_calgary_csv_artifact_sha256",
            return_value="b" * 64,
        ), patch(
            "support_operations_intelligence."
            "calgary_full_artifact_execution.iter_calgary_csv_records",
            return_value=iter(()),
        ), patch(
            "support_operations_intelligence."
            "calgary_full_artifact_execution."
            "aggregate_calgary_status_by_service",
            return_value=inconsistent_summary,
        ):
            with self.assertRaises(CalgaryFullArtifactAccountingError):
                execute_calgary_full_artifact(
                    Path("synthetic-not-opened.csv"),
                    "expected synthetic digest",
                )


if __name__ == "__main__":
    unittest.main()

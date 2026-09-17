import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import support_operations_intelligence.calgary_full_artifact_run as calgary_full_artifact_run
from support_operations_intelligence.calgary_csv import (
    CalgaryCsvStructureError,
    CalgaryCsvStructureErrorReason,
)
from support_operations_intelligence.calgary_full_artifact_execution import (
    CalgaryFullArtifactCounterSummary,
    CalgaryFullArtifactExecutionResult,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    CalgaryStatusServiceAggregation,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import IdentityRejectionReason


EXPECTED_SHA256 = "a" * 64
EXPECTED_GIT_REVISION = "b" * 40
EXPECTED_RUN_DATE_UTC = "2026-09-17T03:30:00+00:00"
EXPECTED_PYTHON_VERSION = "3.12.3"
EXPECTED_CONTRACT_ID = (
    "007-full-artifact-execution-and-status-by-service-baseline"
)
ESTABLISHED_CLAIM = (
    "The current tested parser and adapter traversed the complete "
    "digest-verified artifact and produced source-native service_name x "
    "status_description counts under a declared denominator and declared "
    "exclusions."
)
NOT_ESTABLISHED_CLAIMS = [
    "operational finding",
    "diagnosis",
    "causal claim",
    "backlog interpretation",
    "duration interpretation",
    "closure finality",
    "comparability of status values across service categories",
    "comparability of service_name labels",
    "whether one row equals one independently managed unit of work",
    "representativeness of the artifact",
    "AI suitability",
]


def _synthetic_c1_result() -> CalgaryFullArtifactExecutionResult:
    observed_closed = ObservedEvidence("Closed")
    observed_spaced_closed = ObservedEvidence(" Closed ")
    unavailable_absent = UnavailableEvidence(
        UnavailableReason.VALUE_ABSENT
    )
    unavailable_indeterminate = UnavailableEvidence(
        UnavailableReason.EVIDENCE_INDETERMINATE
    )
    observed_roads = ObservedEvidence("Roads")
    observed_spaced_roads = ObservedEvidence(" Roads ")

    aggregation = CalgaryStatusServiceAggregation(
        total_logical_records_seen=6,
        total_admitted_records=5,
        total_rejected_identity_records=1,
        rejection_counts_by_reason={
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID: 1,
        },
        aggregated_record_count=5,
        aggregated_counts={
            (observed_closed, unavailable_indeterminate): 1,
            (unavailable_absent, observed_roads): 1,
            (unavailable_indeterminate, unavailable_absent): 1,
            (observed_closed, observed_roads): 1,
            (observed_spaced_closed, observed_spaced_roads): 1,
        },
    )
    counter_summary = CalgaryFullArtifactCounterSummary(
        rows_observed=6,
        rows_structurally_accepted=6,
        rows_structurally_rejected=0,
        rows_identity_admitted=5,
        rows_identity_rejected=1,
        distinct_source_case_ids=4,
        source_case_ids_appearing_more_than_once=1,
        rows_involved_in_duplication=2,
        blank_service_name=1,
        blank_agency_responsible=0,
        blank_status_description=1,
        status_vocabulary={
            unavailable_indeterminate: 1,
            observed_closed: 2,
            unavailable_absent: 1,
            observed_spaced_closed: 1,
        },
        service_name_vocabulary={
            unavailable_indeterminate: 1,
            observed_roads: 2,
            unavailable_absent: 1,
            observed_spaced_roads: 1,
        },
    )
    return CalgaryFullArtifactExecutionResult(
        verified_sha256=EXPECTED_SHA256,
        aggregation=aggregation,
        counter_summary=counter_summary,
    )


class CalgaryFullArtifactRunTests(unittest.TestCase):
    def _assert_json_object_keys_are_sorted(self, value: object) -> None:
        if isinstance(value, dict):
            self.assertEqual(list(value), sorted(value))
            for nested_value in value.values():
                self._assert_json_object_keys_are_sorted(nested_value)
        elif isinstance(value, list):
            for nested_value in value:
                self._assert_json_object_keys_are_sorted(nested_value)

    def _invoke_success(self, output_path: Path) -> int:
        with (
            patch.object(
                calgary_full_artifact_run,
                "execute_calgary_full_artifact",
                return_value=_synthetic_c1_result(),
            ) as execute,
            patch.object(
                calgary_full_artifact_run,
                "_capture_git_revision",
                return_value=EXPECTED_GIT_REVISION,
            ),
            patch.object(
                calgary_full_artifact_run,
                "_capture_run_date_utc",
                return_value=EXPECTED_RUN_DATE_UTC,
            ),
            patch.object(
                calgary_full_artifact_run,
                "_capture_python_version",
                return_value=EXPECTED_PYTHON_VERSION,
            ),
            patch.object(
                calgary_full_artifact_run,
                "_capture_peak_rss_bytes",
                return_value=12_345_344,
            ),
            patch.object(
                calgary_full_artifact_run,
                "_monotonic",
                side_effect=[100.0, 102.5],
            ),
        ):
            return_code = calgary_full_artifact_run.main(
                [
                    "--artifact",
                    "synthetic-artifact.csv",
                    "--expected-sha256",
                    EXPECTED_SHA256,
                    "--output",
                    str(output_path),
                ]
            )

        execute.assert_called_once_with(
            Path("synthetic-artifact.csv"),
            EXPECTED_SHA256,
        )
        return return_code

    def _read_success_json(self, output_path: Path) -> dict[str, object]:
        return_code = self._invoke_success(output_path)
        self.assertEqual(return_code, 0)
        self.assertTrue(output_path.is_file())
        output_bytes = output_path.read_bytes()
        self.assertTrue(output_bytes.endswith(b"\n"))
        result = json.loads(output_bytes)
        self._assert_json_object_keys_are_sorted(result)
        return result

    def test_successful_cli_writes_complete_bound_result(self):
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "baseline.json"
            result = self._read_success_json(output_path)

        self.assertEqual(result["artifact_sha256"], EXPECTED_SHA256)
        self.assertEqual(result["git_revision"], EXPECTED_GIT_REVISION)
        self.assertEqual(result["increment_version"], "007")
        self.assertEqual(result["contract_id"], EXPECTED_CONTRACT_ID)
        self.assertEqual(result["run_date_utc"], EXPECTED_RUN_DATE_UTC)
        self.assertEqual(result["python_version"], EXPECTED_PYTHON_VERSION)
        self.assertEqual(result["wall_clock_seconds"], 2.5)
        self.assertEqual(result["peak_rss_bytes"], 12_345_344)
        self.assertEqual(
            {
                key: value
                for key, value in result["counter_summary"].items()
                if key not in {"status_vocabulary", "service_name_vocabulary"}
            },
            {
                "rows_observed": 6,
                "rows_structurally_accepted": 6,
                "rows_structurally_rejected": 0,
                "rows_identity_admitted": 5,
                "rows_identity_rejected": 1,
                "distinct_source_case_ids": 4,
                "source_case_ids_appearing_more_than_once": 1,
                "rows_involved_in_duplication": 2,
                "blank_service_name": 1,
                "blank_agency_responsible": 0,
                "blank_status_description": 1,
            },
        )
        self.assertEqual(
            result["rejection_counts"],
            [{"reason": "MISSING_SOURCE_CASE_ID", "count": 1}],
        )

    def test_git_revision_capture_failure_prevents_c1_and_output(self):
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "baseline.json"
            with (
                patch.object(
                    calgary_full_artifact_run,
                    "_capture_git_revision",
                    side_effect=RuntimeError("synthetic git failure"),
                ),
                patch.object(
                    calgary_full_artifact_run,
                    "execute_calgary_full_artifact",
                ) as execute,
            ):
                return_code = calgary_full_artifact_run.main(
                    [
                        "--artifact",
                        "synthetic-artifact.csv",
                        "--expected-sha256",
                        EXPECTED_SHA256,
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertNotEqual(return_code, 0)
            execute.assert_not_called()
            self.assertFalse(output_path.exists())

    def test_typed_evidence_and_rows_have_deterministic_order(self):
        with TemporaryDirectory() as temporary_directory:
            result = self._read_success_json(
                Path(temporary_directory) / "baseline.json"
            )

        self.assertEqual(
            result["counter_summary"]["status_vocabulary"],
            [
                {"evidence": {"kind": "OBSERVED", "value": " Closed "}, "count": 1},
                {"evidence": {"kind": "OBSERVED", "value": "Closed"}, "count": 2},
                {
                    "evidence": {
                        "kind": "UNAVAILABLE",
                        "reason": "EVIDENCE_INDETERMINATE",
                    },
                    "count": 1,
                },
                {
                    "evidence": {
                        "kind": "UNAVAILABLE",
                        "reason": "VALUE_ABSENT",
                    },
                    "count": 1,
                },
            ],
        )
        service_rows = result["status_by_service"]
        self.assertEqual(
            [row["service_name"] for row in service_rows],
            [
                {"kind": "OBSERVED", "value": " Roads "},
                {"kind": "OBSERVED", "value": "Roads"},
                {"kind": "OBSERVED", "value": "Roads"},
                {
                    "kind": "UNAVAILABLE",
                    "reason": "EVIDENCE_INDETERMINATE",
                },
                {"kind": "UNAVAILABLE", "reason": "VALUE_ABSENT"},
            ],
        )

    def test_percentages_use_exact_declared_denominators(self):
        with TemporaryDirectory() as temporary_directory:
            result = self._read_success_json(
                Path(temporary_directory) / "baseline.json"
            )

        rows_by_evidence = {
            (
                json.dumps(row["service_name"], sort_keys=True),
                json.dumps(row["status_description"], sort_keys=True),
            ): row
            for row in result["status_by_service"]
        }
        observed_roads_closed = rows_by_evidence[
            (
                json.dumps(
                    {"kind": "OBSERVED", "value": "Roads"},
                    sort_keys=True,
                ),
                json.dumps(
                    {"kind": "OBSERVED", "value": "Closed"},
                    sort_keys=True,
                ),
            )
        ]
        unavailable_pair = rows_by_evidence[
            (
                json.dumps(
                    {"kind": "UNAVAILABLE", "reason": "VALUE_ABSENT"},
                    sort_keys=True,
                ),
                json.dumps(
                    {
                        "kind": "UNAVAILABLE",
                        "reason": "EVIDENCE_INDETERMINATE",
                    },
                    sort_keys=True,
                ),
            )
        ]
        self.assertEqual(
            observed_roads_closed["within_category_percentage"],
            "50.0000",
        )
        self.assertEqual(
            observed_roads_closed["portfolio_wide_percentage"],
            "20.0000",
        )
        self.assertEqual(
            unavailable_pair["within_category_percentage"],
            "100.0000",
        )
        self.assertEqual(
            unavailable_pair["portfolio_wide_percentage"],
            "20.0000",
        )

    def test_historical_comparison_preserves_arithmetic_difference(self):
        with TemporaryDirectory() as temporary_directory:
            result = self._read_success_json(
                Path(temporary_directory) / "baseline.json"
            )

        self.assertEqual(
            result["historical_comparison"],
            {
                "historical_rows_observed": 7_474_403,
                "current_rows_observed": 6,
                "difference": 6 - 7_474_403,
                "cause": "NOT_DETERMINED",
            },
        )

    def test_success_claims_are_static_and_bounded(self):
        with TemporaryDirectory() as temporary_directory:
            result = self._read_success_json(
                Path(temporary_directory) / "baseline.json"
            )

        self.assertEqual(result["claims"]["established"], [ESTABLISHED_CLAIM])
        self.assertEqual(
            result["claims"]["not_established"],
            NOT_ESTABLISHED_CLAIMS,
        )
        self.assertEqual(
            result["claims"]["duplicate_counter_scope"],
            "Exact source-identifier repetition only; does not establish "
            "that one row equals one independently managed real-world unit "
            "of work.",
        )
        self.assertEqual(
            result["claims"]["cross_tab_interpretation"],
            "NOT_INCLUDED",
        )

    def test_c1_failure_returns_nonzero_without_success_output(self):
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "baseline.json"
            with (
                patch.object(
                    calgary_full_artifact_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_GIT_REVISION,
                ),
                patch.object(
                    calgary_full_artifact_run,
                    "execute_calgary_full_artifact",
                    side_effect=RuntimeError("synthetic C1 failure"),
                ),
                patch.object(
                    calgary_full_artifact_run,
                    "_monotonic",
                    return_value=100.0,
                ),
            ):
                return_code = calgary_full_artifact_run.main(
                    [
                        "--artifact",
                        "synthetic-artifact.csv",
                        "--expected-sha256",
                        EXPECTED_SHA256,
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertNotEqual(return_code, 0)
            self.assertFalse(output_path.exists())

    def test_structural_diagnostic_is_not_serialized_as_success(self):
        structural_error = CalgaryCsvStructureError(
            reason=CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            logical_data_record_number=7,
            expected_column_count=15,
            actual_column_count=14,
            raw_logical_record='synthetic,"raw\r\nrecord"\r\n',
        )

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "baseline.json"
            with (
                patch.object(
                    calgary_full_artifact_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_GIT_REVISION,
                ),
                patch.object(
                    calgary_full_artifact_run,
                    "execute_calgary_full_artifact",
                    side_effect=structural_error,
                ),
                patch.object(
                    calgary_full_artifact_run,
                    "_monotonic",
                    return_value=100.0,
                ),
            ):
                return_code = calgary_full_artifact_run.main(
                    [
                        "--artifact",
                        "synthetic-artifact.csv",
                        "--expected-sha256",
                        EXPECTED_SHA256,
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertNotEqual(return_code, 0)
            self.assertFalse(output_path.exists())
            self.assertEqual(structural_error.logical_data_record_number, 7)
            self.assertEqual(
                structural_error.raw_logical_record,
                'synthetic,"raw\r\nrecord"\r\n',
            )


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import call, patch

import support_operations_intelligence.source_native_sentinel_audit_run as audit_run
from support_operations_intelligence.source_native_sentinel_audit import (
    Phase1Candidate,
    Phase1FieldAuditResult,
)


EXPECTED_ARTIFACT_SHA256 = (
    "9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f"
)
EXPECTED_INCREMENT_007_REVISION = (
    "f16c19fef3b3e6bae1c5653568b5e76cfece2f14"
)
EXPECTED_INCREMENT_007_CONTRACT = (
    "007-full-artifact-execution-and-status-by-service-baseline"
)
EXPECTED_AUDIT_REVISION = "a" * 40
EXPECTED_RUN_DATE_UTC = "2026-09-17T17:30:00+00:00"
EXPECTED_PYTHON_VERSION = "3.12.3"
AGENCY_NOT_EVALUABLE = (
    "NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES"
)
NO_CROSS_FIELD_UNION = (
    "NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES"
)


def _observed(value: str, count: int) -> dict[str, object]:
    return {
        "evidence": {"kind": "OBSERVED", "value": value},
        "count": count,
    }


def _synthetic_baseline() -> dict[str, object]:
    return {
        "artifact_sha256": EXPECTED_ARTIFACT_SHA256,
        "git_revision": EXPECTED_INCREMENT_007_REVISION,
        "increment_version": "007",
        "contract_id": EXPECTED_INCREMENT_007_CONTRACT,
        "counter_summary": {
            "rows_identity_admitted": 12,
            "service_name_vocabulary": [
                _observed("synthetic service", 12),
            ],
            "status_vocabulary": [
                _observed("synthetic status", 12),
            ],
        },
        "service_name_x_status": [
            {"synthetic_unrelated_content": "MUST_NOT_BE_AUDITED"},
        ],
        "status_by_service": [
            {"synthetic_unrelated_content": "MUST_NOT_BE_AUDITED"},
        ],
        "claims": {"synthetic": "MUST_NOT_BE_ANALYZED"},
        "historical_comparison": {"synthetic": "MUST_NOT_BE_ANALYZED"},
        "wall_clock_seconds": "MUST_NOT_BE_ANALYZED",
    }


def _candidate(
    field: str,
    value: str,
    matched_checks: tuple[str, ...],
    classification: str,
) -> Phase1Candidate:
    return Phase1Candidate(
        field=field,
        exact_lexical_value=value,
        phase="PHASE_1",
        matched_checks=matched_checks,
        classification=classification,
        row_count=1,
        row_percentage_exact=Decimal(100) / Decimal(12),
        row_percentage="8.333333",
        vocabulary_percentage_exact=Decimal(100) / Decimal(3),
        vocabulary_percentage="33.333333",
    )


def _field_result(
    field: str,
    candidates: tuple[Phase1Candidate, ...] = (),
) -> Phase1FieldAuditResult:
    return Phase1FieldAuditResult(
        field=field,
        evaluability_status=(
            "EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY"
        ),
        row_denominator=12,
        distinct_vocabulary_count=3,
        candidates=candidates,
        aggregate_sentinel_candidate_row_count=2 if candidates else 0,
        aggregate_sentinel_candidate_row_percentage_exact=(
            Decimal(100) * Decimal(2 if candidates else 0) / Decimal(12)
        ),
        aggregate_sentinel_candidate_row_percentage=(
            "16.666667" if candidates else "0.000000"
        ),
        aggregate_sentinel_candidate_vocabulary_count=2 if candidates else 0,
        aggregate_sentinel_candidate_vocabulary_percentage_exact=(
            Decimal(100) * Decimal(2 if candidates else 0) / Decimal(3)
        ),
        aggregate_sentinel_candidate_vocabulary_percentage=(
            "66.666667" if candidates else "0.000000"
        ),
        materiality_classification=(
            "RECORDED_BASELINE_DESCRIPTION_DECISION_REQUIRED_BEFORE_PUBLICATION"
            if candidates
            else "FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE"
        ),
        normalization_drift_candidate_count=1 if candidates else 0,
        normalization_drift_row_count=1 if candidates else 0,
        normalization_drift_row_percentage_exact=(
            Decimal(100) * Decimal(1 if candidates else 0) / Decimal(12)
        ),
        normalization_drift_row_percentage=(
            "8.333333" if candidates else "0.000000"
        ),
        standalone_control_character_candidate_count=0,
        standalone_control_character_row_count=0,
        standalone_control_character_row_percentage_exact=Decimal(0),
        standalone_control_character_row_percentage="0.000000",
    )


class SourceNativeSentinelAuditRunContractTests(unittest.TestCase):
    def _write_baseline(
        self,
        path: Path,
        payload: dict[str, object] | None = None,
    ) -> str:
        serialized = json.dumps(
            payload if payload is not None else _synthetic_baseline(),
            sort_keys=True,
        ) + "\n"
        path.write_text(serialized, encoding="utf-8", newline="")
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _audit_side_effect(
        self,
        field_name: str,
        vocabulary_rows: list[dict[str, object]],
        row_denominator: int,
    ) -> Phase1FieldAuditResult:
        self.assertIn(field_name, ("service_name", "status_description"))
        self.assertTrue(vocabulary_rows)
        self.assertEqual(row_denominator, 12)
        return _field_result(field_name)

    def _invoke(
        self,
        baseline_path: Path,
        baseline_sha256: str,
        output_path: Path,
    ) -> int:
        return audit_run.main(
            [
                "--baseline-result",
                str(baseline_path),
                "--expected-baseline-sha256",
                baseline_sha256,
                "--output",
                str(output_path),
            ]
        )

    def _assert_object_keys_are_sorted(self, value: object) -> None:
        if isinstance(value, dict):
            self.assertEqual(list(value), sorted(value))
            for nested_value in value.values():
                self._assert_object_keys_are_sorted(nested_value)
        elif isinstance(value, list):
            for nested_value in value:
                self._assert_object_keys_are_sorted(nested_value)

    def test_digest_mismatch_stops_before_json_parse_or_audit(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_path.write_text("not-json", encoding="utf-8")

            with (
                patch.object(audit_run, "_load_json") as load_json,
                patch.object(audit_run, "audit_phase1_field") as audit,
            ):
                return_code = self._invoke(
                    baseline_path,
                    "0" * 64,
                    output_path,
                )

            self.assertNotEqual(return_code, 0)
            load_json.assert_not_called()
            audit.assert_not_called()
            self.assertFalse(output_path.exists())

    def test_required_increment_007_binding_mismatches_fail_closed(self) -> None:
        mismatch_cases = (
            ("artifact_sha256", "0" * 64),
            ("git_revision", "0" * 40),
            ("increment_version", "999"),
            ("contract_id", "unexpected-contract"),
        )

        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for key, mismatched_value in mismatch_cases:
                with self.subTest(key=key):
                    payload = _synthetic_baseline()
                    payload[key] = mismatched_value
                    baseline_path = root / f"baseline-{key}.json"
                    output_path = root / f"output-{key}.json"
                    baseline_sha256 = self._write_baseline(
                        baseline_path,
                        payload,
                    )

                    with patch.object(
                        audit_run,
                        "audit_phase1_field",
                    ) as audit:
                        return_code = self._invoke(
                            baseline_path,
                            baseline_sha256,
                            output_path,
                        )

                    self.assertNotEqual(return_code, 0)
                    audit.assert_not_called()
                    self.assertFalse(output_path.exists())

    def test_only_service_and_status_are_audited_with_retained_denominator(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            payload = _synthetic_baseline()
            baseline_sha256 = self._write_baseline(baseline_path, payload)
            counter_summary = payload["counter_summary"]
            self.assertIsInstance(counter_summary, dict)

            with (
                patch.object(
                    audit_run,
                    "audit_phase1_field",
                    side_effect=self._audit_side_effect,
                ) as audit,
                patch.object(
                    audit_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_AUDIT_REVISION,
                ),
                patch.object(
                    audit_run,
                    "_capture_python_version",
                    return_value=EXPECTED_PYTHON_VERSION,
                ),
                patch.object(
                    audit_run,
                    "_capture_run_date_utc",
                    return_value=EXPECTED_RUN_DATE_UTC,
                ),
            ):
                return_code = self._invoke(
                    baseline_path,
                    baseline_sha256,
                    output_path,
                )

            self.assertEqual(return_code, 0)
            self.assertEqual(
                audit.call_args_list,
                [
                    call(
                        "service_name",
                        counter_summary["service_name_vocabulary"],
                        12,
                    ),
                    call(
                        "status_description",
                        counter_summary["status_vocabulary"],
                        12,
                    ),
                ],
            )

    def test_success_has_explicit_agency_summary_and_no_union_or_later_phases(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_sha256 = self._write_baseline(baseline_path)

            with (
                patch.object(
                    audit_run,
                    "audit_phase1_field",
                    side_effect=self._audit_side_effect,
                ),
                patch.object(
                    audit_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_AUDIT_REVISION,
                ),
                patch.object(
                    audit_run,
                    "_capture_python_version",
                    return_value=EXPECTED_PYTHON_VERSION,
                ),
                patch.object(
                    audit_run,
                    "_capture_run_date_utc",
                    return_value=EXPECTED_RUN_DATE_UTC,
                ),
            ):
                self.assertEqual(
                    self._invoke(baseline_path, baseline_sha256, output_path),
                    0,
                )

            result = json.loads(output_path.read_text(encoding="utf-8"))
            agency_field = result["fields"]["agency_responsible"]
            self.assertEqual(
                agency_field,
                {
                    "evaluable": False,
                    "field": "agency_responsible",
                    "reason": AGENCY_NOT_EVALUABLE,
                },
            )
            self.assertEqual(
                result["summary"]["agency_responsible"],
                {
                    "evaluable": False,
                    "reason": AGENCY_NOT_EVALUABLE,
                },
            )
            self.assertEqual(
                result["summary"]["cross_field_sentinel_union"],
                NO_CROSS_FIELD_UNION,
            )
            self.assertNotIn("phase_2", result)
            self.assertNotIn("phase_3", result)
            serialized = output_path.read_text(encoding="utf-8")
            self.assertNotIn("EXPLORATORY_SENTINEL_CANDIDATE", serialized)
            self.assertNotIn("LOW_INFORMATION_CANDIDATE", serialized)

    def test_result_binding_and_json_serialization_are_deterministic(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_sha256 = self._write_baseline(baseline_path)

            with (
                patch.object(
                    audit_run,
                    "audit_phase1_field",
                    side_effect=self._audit_side_effect,
                ),
                patch.object(
                    audit_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_AUDIT_REVISION,
                ),
                patch.object(
                    audit_run,
                    "_capture_python_version",
                    return_value=EXPECTED_PYTHON_VERSION,
                ),
                patch.object(
                    audit_run,
                    "_capture_run_date_utc",
                    return_value=EXPECTED_RUN_DATE_UTC,
                ),
            ):
                self.assertEqual(
                    self._invoke(baseline_path, baseline_sha256, output_path),
                    0,
                )

            output_bytes = output_path.read_bytes()
            self.assertTrue(output_bytes.endswith(b"\n"))
            result = json.loads(output_bytes.decode("utf-8"))
            self.assertEqual(
                result["binding"],
                {
                    "audit_code_git_revision": EXPECTED_AUDIT_REVISION,
                    "increment_008_contract": (
                        "008-source-native-sentinel-and-missingness-audit"
                    ),
                    "increment_008_version": "008",
                    "input_baseline_sha256": baseline_sha256,
                    "input_increment_007_git_revision": (
                        EXPECTED_INCREMENT_007_REVISION
                    ),
                    "phase": "PHASE_1",
                    "python_version": EXPECTED_PYTHON_VERSION,
                    "run_date_utc": EXPECTED_RUN_DATE_UTC,
                },
            )
            self._assert_object_keys_are_sorted(result)

    def test_candidate_values_and_field_results_serialize_without_reinterpretation(self) -> None:
        values = (" unknown ", "\t", "\u00a0")
        candidates = (
            _candidate(
                "service_name",
                values[0],
                ("PHASE_1D_LEADING_OR_TRAILING_WHITESPACE",),
                "NORMALIZATION_DRIFT_CANDIDATE",
            ),
            _candidate(
                "service_name",
                values[1],
                (
                    "PHASE_1B_WHITESPACE_ONLY",
                    "PHASE_1E_NON_PRINTABLE_OR_CONTROL",
                ),
                "SENTINEL_CANDIDATE",
            ),
            _candidate(
                "service_name",
                values[2],
                ("PHASE_1B_WHITESPACE_ONLY",),
                "SENTINEL_CANDIDATE",
            ),
        )

        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_sha256 = self._write_baseline(baseline_path)

            def audit_side_effect(
                field_name: str,
                vocabulary_rows: list[dict[str, object]],
                row_denominator: int,
            ) -> Phase1FieldAuditResult:
                self.assertTrue(vocabulary_rows)
                self.assertEqual(row_denominator, 12)
                if field_name == "service_name":
                    return _field_result(field_name, candidates)
                return _field_result(field_name)

            with (
                patch.object(
                    audit_run,
                    "audit_phase1_field",
                    side_effect=audit_side_effect,
                ),
                patch.object(
                    audit_run,
                    "_capture_git_revision",
                    return_value=EXPECTED_AUDIT_REVISION,
                ),
                patch.object(
                    audit_run,
                    "_capture_python_version",
                    return_value=EXPECTED_PYTHON_VERSION,
                ),
                patch.object(
                    audit_run,
                    "_capture_run_date_utc",
                    return_value=EXPECTED_RUN_DATE_UTC,
                ),
            ):
                self.assertEqual(
                    self._invoke(baseline_path, baseline_sha256, output_path),
                    0,
                )

            result = json.loads(output_path.read_text(encoding="utf-8"))
            service_result = result["fields"]["service_name"]
            self.assertTrue(service_result["evaluable"])
            self.assertEqual(service_result["field"], "service_name")
            self.assertEqual(service_result["row_denominator"], 12)
            self.assertEqual(service_result["distinct_vocabulary_count"], 3)
            self.assertEqual(service_result["candidate_count"], 3)
            self.assertEqual(
                [
                    candidate["exact_lexical_value"]
                    for candidate in service_result["candidates"]
                ],
                list(values),
            )
            for candidate in service_result["candidates"]:
                self.assertEqual(
                    set(candidate),
                    {
                        "classification",
                        "exact_lexical_value",
                        "field",
                        "matched_checks",
                        "phase",
                        "row_count",
                        "row_percentage",
                        "vocabulary_percentage",
                    },
                )
            self.assertIsInstance(
                service_result["aggregate_sentinel_candidate_row_percentage"],
                str,
            )
            self.assertIsInstance(
                service_result[
                    "aggregate_sentinel_candidate_vocabulary_percentage"
                ],
                str,
            )

    def test_invalid_json_fails_without_audit_or_success_result(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_path.write_text("{", encoding="utf-8")
            baseline_sha256 = hashlib.sha256(
                baseline_path.read_bytes()
            ).hexdigest()

            with patch.object(
                audit_run,
                "audit_phase1_field",
            ) as audit:
                return_code = self._invoke(
                    baseline_path,
                    baseline_sha256,
                    output_path,
                )

            self.assertNotEqual(return_code, 0)
            audit.assert_not_called()
            self.assertFalse(output_path.exists())

    def test_audit_failure_returns_nonzero_without_success_result(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline_path = root / "synthetic-baseline.json"
            output_path = root / "phase1-result.json"
            baseline_sha256 = self._write_baseline(baseline_path)

            with patch.object(
                audit_run,
                "audit_phase1_field",
                side_effect=ValueError("synthetic audit failure"),
            ):
                return_code = self._invoke(
                    baseline_path,
                    baseline_sha256,
                    output_path,
                )

            self.assertNotEqual(return_code, 0)
            self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import support_operations_intelligence.source_native_sentinel_stage_a_run as stage_a_run


EXPECTED_ARTIFACT_SHA256 = (
    "9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f"
)
EXPECTED_INCREMENT_007_REVISION = (
    "f16c19fef3b3e6bae1c5653568b5e76cfece2f14"
)
EXPECTED_INCREMENT_007_CONTRACT = (
    "007-full-artifact-execution-and-status-by-service-baseline"
)
EXPECTED_INCREMENT_008_CONTRACT = (
    "008-source-native-sentinel-and-missingness-audit"
)
EXPECTED_GENERATOR_REVISION = "a" * 40
EXPECTED_GENERATED_AT_UTC = "2026-09-18T15:00:00+00:00"
EXPECTED_PYTHON_VERSION = "3.12.3"
AGENCY_NOT_EVALUABLE = (
    "NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES"
)


def _observed(value: str, count: int) -> dict[str, object]:
    return {
        "evidence": {"kind": "OBSERVED", "value": value},
        "count": count,
    }


def _synthetic_baseline(
    service_rows: list[dict[str, object]] | None = None,
    status_rows: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    services = service_rows or [
        _observed("Alpha", 4),
        _observed("N/A", 3),
        _observed("Beta", 5),
    ]
    statuses = status_rows or [
        _observed("Closed", 7),
        _observed("Open", 5),
    ]
    return {
        "artifact_sha256": EXPECTED_ARTIFACT_SHA256,
        "git_revision": EXPECTED_INCREMENT_007_REVISION,
        "increment_version": "007",
        "contract_id": EXPECTED_INCREMENT_007_CONTRACT,
        "counter_summary": {
            "rows_identity_admitted": 12,
            "service_name_vocabulary": services,
            "status_vocabulary": statuses,
        },
        "status_by_service": [
            {"synthetic_unrelated_content": "MUST_NOT_BE_EXPORTED"},
        ],
    }


def _phase1_candidate(field: str, value: str) -> dict[str, object]:
    return {
        "classification": "SENTINEL_CANDIDATE",
        "exact_lexical_value": value,
        "field": field,
        "matched_checks": ["SYNTHETIC_PHASE_1_CHECK"],
        "phase": "PHASE_1",
        "row_count": 1,
        "row_percentage": "8.333333",
        "vocabulary_percentage": "33.333333",
    }


def _synthetic_phase1_result(
    baseline_sha256: str,
    service_candidates: tuple[str, ...] = ("N/A",),
    status_candidates: tuple[str, ...] = (),
) -> dict[str, object]:
    return {
        "binding": {
            "audit_code_git_revision": "b" * 40,
            "increment_008_contract": EXPECTED_INCREMENT_008_CONTRACT,
            "increment_008_version": "008",
            "input_baseline_sha256": baseline_sha256,
            "input_increment_007_git_revision": (
                EXPECTED_INCREMENT_007_REVISION
            ),
            "phase": "PHASE_1",
            "python_version": EXPECTED_PYTHON_VERSION,
            "run_date_utc": "2026-09-18T14:22:45+00:00",
        },
        "fields": {
            "agency_responsible": {
                "evaluable": False,
                "field": "agency_responsible",
                "reason": AGENCY_NOT_EVALUABLE,
            },
            "service_name": {
                "candidates": [
                    _phase1_candidate("service_name", value)
                    for value in service_candidates
                ],
                "evaluable": True,
                "field": "service_name",
            },
            "status_description": {
                "candidates": [
                    _phase1_candidate("status_description", value)
                    for value in status_candidates
                ],
                "evaluable": True,
                "field": "status_description",
            },
        },
        "summary": {
            "cross_field_sentinel_union": (
                "NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES"
            ),
        },
    }


class SourceNativeSentinelStageARunContractTests(unittest.TestCase):
    def _write_json(self, path: Path, payload: dict[str, object]) -> str:
        path.write_text(
            json.dumps(payload, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="",
        )
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _write_inputs(
        self,
        root: Path,
        *,
        baseline: dict[str, object] | None = None,
        service_candidates: tuple[str, ...] = ("N/A",),
        status_candidates: tuple[str, ...] = (),
    ) -> tuple[Path, str, Path, str]:
        baseline_path = root / "synthetic-baseline.json"
        baseline_sha256 = self._write_json(
            baseline_path,
            baseline or _synthetic_baseline(),
        )
        phase1_path = root / "synthetic-phase1.json"
        phase1_sha256 = self._write_json(
            phase1_path,
            _synthetic_phase1_result(
                baseline_sha256,
                service_candidates,
                status_candidates,
            ),
        )
        return baseline_path, baseline_sha256, phase1_path, phase1_sha256

    def _invoke(
        self,
        baseline_path: Path,
        baseline_sha256: str,
        phase1_path: Path,
        phase1_sha256: str,
        output_path: Path,
    ) -> int:
        return stage_a_run.main(
            [
                "--baseline-result",
                str(baseline_path),
                "--expected-baseline-sha256",
                baseline_sha256,
                "--phase1-result",
                str(phase1_path),
                "--expected-phase1-sha256",
                phase1_sha256,
                "--output",
                str(output_path),
            ]
        )

    def _invoke_with_deterministic_metadata(
        self,
        baseline_path: Path,
        baseline_sha256: str,
        phase1_path: Path,
        phase1_sha256: str,
        output_path: Path,
    ) -> int:
        with (
            patch.object(
                stage_a_run,
                "_capture_git_revision",
                return_value=EXPECTED_GENERATOR_REVISION,
            ),
            patch.object(
                stage_a_run,
                "_capture_python_version",
                return_value=EXPECTED_PYTHON_VERSION,
            ),
            patch.object(
                stage_a_run,
                "_capture_generated_at_utc",
                return_value=EXPECTED_GENERATED_AT_UTC,
            ),
        ):
            return self._invoke(
                baseline_path,
                baseline_sha256,
                phase1_path,
                phase1_sha256,
                output_path,
            )

    def _successful_result(
        self,
        root: Path,
        *,
        baseline: dict[str, object] | None = None,
        service_candidates: tuple[str, ...] = ("N/A",),
        status_candidates: tuple[str, ...] = (),
    ) -> dict[str, object]:
        inputs = self._write_inputs(
            root,
            baseline=baseline,
            service_candidates=service_candidates,
            status_candidates=status_candidates,
        )
        output_path = root / "stage-a-universe.json"
        return_code = self._invoke_with_deterministic_metadata(
            *inputs,
            output_path,
        )
        self.assertEqual(return_code, 0)
        return json.loads(output_path.read_text(encoding="utf-8"))

    def test_both_digests_are_verified_before_either_json_is_parsed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inputs = self._write_inputs(root)
            output_path = root / "stage-a-universe.json"

            for baseline_sha256, phase1_sha256 in (
                ("0" * 64, inputs[3]),
                (inputs[1], "0" * 64),
            ):
                with self.subTest(
                    baseline_sha256=baseline_sha256,
                    phase1_sha256=phase1_sha256,
                ):
                    with (
                        patch.object(stage_a_run, "_load_json") as load_json,
                        patch.object(
                            stage_a_run,
                            "_build_stage_a_review_universe",
                        ) as build,
                    ):
                        return_code = self._invoke(
                            inputs[0],
                            baseline_sha256,
                            inputs[2],
                            phase1_sha256,
                            output_path,
                        )

                    self.assertNotEqual(return_code, 0)
                    load_json.assert_not_called()
                    build.assert_not_called()
                    self.assertFalse(output_path.exists())

    def test_required_baseline_and_phase1_bindings_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline = _synthetic_baseline()
            baseline["contract_id"] = "unexpected-contract"
            inputs = self._write_inputs(root, baseline=baseline)
            output_path = root / "stage-a-universe.json"

            self.assertNotEqual(self._invoke(*inputs, output_path), 0)
            self.assertFalse(output_path.exists())

            inputs = self._write_inputs(root)
            phase1 = _synthetic_phase1_result(inputs[1])
            binding = phase1["binding"]
            self.assertIsInstance(binding, dict)
            binding["phase"] = "PHASE_2"
            phase1_sha256 = self._write_json(inputs[2], phase1)

            self.assertNotEqual(
                self._invoke(
                    inputs[0],
                    inputs[1],
                    inputs[2],
                    phase1_sha256,
                    output_path,
                ),
                0,
            )
            self.assertFalse(output_path.exists())

    def test_phase1_exclusions_are_derived_from_retained_candidates(self) -> None:
        for excluded, expected_services in (
            ("N/A", ["Alpha", "Beta"]),
            ("Beta", ["Alpha", "N/A"]),
        ):
            with self.subTest(excluded=excluded):
                with TemporaryDirectory() as temporary_directory:
                    result = self._successful_result(
                        Path(temporary_directory),
                        service_candidates=(excluded,),
                    )

                entries = result["entries"]
                self.assertEqual(
                    [
                        entry["value"]
                        for entry in entries
                        if entry["field"] == "service_name"
                    ],
                    expected_services,
                )
                self.assertNotIn(excluded, json.dumps(entries))

    def test_entries_are_count_blinded_and_contain_no_decisions(self) -> None:
        baseline = _synthetic_baseline(
            service_rows=[
                _observed("Alpha", 101),
                _observed("N/A", 203),
                _observed("Beta", 307),
            ],
            status_rows=[
                _observed("Closed", 400),
                _observed("Open", 211),
            ],
        )
        baseline["counter_summary"]["rows_identity_admitted"] = 611

        with TemporaryDirectory() as temporary_directory:
            result = self._successful_result(
                Path(temporary_directory),
                baseline=baseline,
            )

        entries = result["entries"]
        for entry in entries:
            self.assertEqual(set(entry), {"field", "value"})
        serialized_entries = json.dumps(entries)
        for forbidden in (
            "count",
            "percentage",
            "rank",
            "materiality",
            "decision",
            "rationale",
            "EXPLORATORY_SENTINEL_CANDIDATE",
            "NO_PHASE_2_FLAG",
            "LOW_INFORMATION",
        ):
            self.assertNotIn(forbidden, serialized_entries)
        for distinctive_count in (101, 203, 307, 400, 211):
            self.assertNotIn(str(distinctive_count), serialized_entries)

    def test_exact_lexical_values_survive_without_normalization(self) -> None:
        values = [" Leading", "Trailing ", "\tEmbedded", "é", "\u00a0Value"]
        baseline = _synthetic_baseline(
            service_rows=[_observed(value, 1) for value in reversed(values)],
            status_rows=[_observed("Closed", 5)],
        )
        baseline["counter_summary"]["rows_identity_admitted"] = 5

        with TemporaryDirectory() as temporary_directory:
            result = self._successful_result(
                Path(temporary_directory),
                baseline=baseline,
                service_candidates=(),
            )

        service_values = [
            entry["value"]
            for entry in result["entries"]
            if entry["field"] == "service_name"
        ]
        self.assertEqual(service_values, sorted(values))

    def test_entries_use_field_then_exact_python_string_order(self) -> None:
        baseline = _synthetic_baseline(
            service_rows=[_observed("Zulu", 6), _observed("Alpha", 6)],
            status_rows=[_observed("Open", 8), _observed("Closed", 4)],
        )

        with TemporaryDirectory() as temporary_directory:
            result = self._successful_result(
                Path(temporary_directory),
                baseline=baseline,
                service_candidates=(),
            )

        self.assertEqual(
            result["entries"],
            [
                {"field": "service_name", "value": "Alpha"},
                {"field": "service_name", "value": "Zulu"},
                {"field": "status_description", "value": "Closed"},
                {"field": "status_description", "value": "Open"},
            ],
        )

    def test_cardinality_accounting_reconciles_and_malformed_input_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            result = self._successful_result(Path(temporary_directory))

        self.assertEqual(
            result["summary"],
            {
                "service_phase1_excluded_count": 1,
                "service_source_vocabulary_count": 3,
                "service_stage_a_review_count": 2,
                "status_phase1_excluded_count": 0,
                "status_source_vocabulary_count": 2,
                "status_stage_a_review_count": 2,
                "total_stage_a_review_count": 4,
            },
        )

        malformed = _synthetic_baseline(
            service_rows=[_observed("Duplicate", 6), _observed("Duplicate", 6)],
        )
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inputs = self._write_inputs(root, baseline=malformed)
            output_path = root / "stage-a-universe.json"
            self.assertNotEqual(self._invoke(*inputs, output_path), 0)
            self.assertFalse(output_path.exists())

    def test_agency_is_not_evaluable_and_never_becomes_an_entry(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            result = self._successful_result(Path(temporary_directory))

        self.assertEqual(
            result["field_evaluability"],
            {
                "agency_responsible": AGENCY_NOT_EVALUABLE,
                "service_name": "EVALUABLE",
                "status_description": "EVALUABLE",
            },
        )
        self.assertNotIn(
            "agency_responsible",
            [entry["field"] for entry in result["entries"]],
        )

    def test_result_bindings_and_representation_are_deterministic(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inputs = self._write_inputs(root)
            output_path = root / "stage-a-universe.json"
            self.assertEqual(
                self._invoke_with_deterministic_metadata(*inputs, output_path),
                0,
            )
            output_bytes = output_path.read_bytes()
            result = json.loads(output_bytes.decode("utf-8"))

        self.assertTrue(output_bytes.endswith(b"\n"))
        self.assertEqual(
            result["binding"],
            {
                "generated_at_utc": EXPECTED_GENERATED_AT_UTC,
                "generator_git_revision": EXPECTED_GENERATOR_REVISION,
                "increment_008_contract": EXPECTED_INCREMENT_008_CONTRACT,
                "increment_008_version": "008",
                "input_baseline_sha256": inputs[1],
                "input_phase1_result_sha256": inputs[3],
                "phase": "PHASE_2",
                "python_version": EXPECTED_PYTHON_VERSION,
                "stage": "STAGE_A_REVIEW_UNIVERSE",
            },
        )
        self.assertEqual(output_bytes, json.dumps(result, sort_keys=True).encode() + b"\n")

    def test_failure_returns_nonzero_without_output_retry_or_fallback(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inputs = self._write_inputs(
                root,
                service_candidates=("not-present-in-baseline",),
            )
            output_path = root / "stage-a-universe.json"

            with patch.object(
                stage_a_run,
                "_build_stage_a_review_universe",
                side_effect=ValueError("synthetic reconciliation failure"),
            ) as build:
                return_code = self._invoke(*inputs, output_path)

            self.assertNotEqual(return_code, 0)
            self.assertEqual(build.call_count, 1)
            self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()

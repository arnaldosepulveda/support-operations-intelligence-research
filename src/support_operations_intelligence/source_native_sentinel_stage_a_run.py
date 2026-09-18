"""Export a count-blinded Phase 2 Stage A review universe."""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_EXPECTED_ARTIFACT_SHA256 = (
    "9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f"
)
_EXPECTED_INCREMENT_007_REVISION = (
    "f16c19fef3b3e6bae1c5653568b5e76cfece2f14"
)
_EXPECTED_INCREMENT_007_VERSION = "007"
_EXPECTED_INCREMENT_007_CONTRACT = (
    "007-full-artifact-execution-and-status-by-service-baseline"
)

_INCREMENT_008_VERSION = "008"
_INCREMENT_008_CONTRACT = (
    "008-source-native-sentinel-and-missingness-audit"
)
_PHASE_1 = "PHASE_1"
_PHASE_2 = "PHASE_2"
_STAGE = "STAGE_A_REVIEW_UNIVERSE"
_AGENCY_NOT_EVALUABLE = (
    "NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES"
)
_EVALUABLE_FIELDS = ("service_name", "status_description")


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-result", required=True, type=Path)
    parser.add_argument("--expected-baseline-sha256", required=True)
    parser.add_argument("--phase1-result", required=True, type=Path)
    parser.add_argument("--expected-phase1-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _capture_git_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=_repository_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    revision = completed.stdout.strip()
    if not revision:
        raise RuntimeError("git revision capture returned no revision")
    return revision


def _capture_python_version() -> str:
    return platform.python_version()


def _capture_generated_at_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open(mode="rb") as input_file:
        for block in iter(lambda: input_file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(mode="r", encoding="utf-8") as input_file:
        payload = json.load(input_file)
    if not isinstance(payload, dict):
        raise ValueError("retained result must be a JSON object")
    return payload


def _require_increment_007_binding(payload: Mapping[str, Any]) -> None:
    expected = {
        "artifact_sha256": _EXPECTED_ARTIFACT_SHA256,
        "git_revision": _EXPECTED_INCREMENT_007_REVISION,
        "increment_version": _EXPECTED_INCREMENT_007_VERSION,
        "contract_id": _EXPECTED_INCREMENT_007_CONTRACT,
    }
    for key, expected_value in expected.items():
        if payload.get(key) != expected_value:
            raise ValueError(f"Increment 007 binding mismatch: {key}")


def _require_phase1_binding(
    payload: Mapping[str, Any],
    baseline_sha256: str,
) -> None:
    binding = payload.get("binding")
    if not isinstance(binding, Mapping):
        raise ValueError("Phase 1 binding must be an object")

    expected = {
        "increment_008_contract": _INCREMENT_008_CONTRACT,
        "increment_008_version": _INCREMENT_008_VERSION,
        "input_baseline_sha256": baseline_sha256,
        "input_increment_007_git_revision": (
            _EXPECTED_INCREMENT_007_REVISION
        ),
        "phase": _PHASE_1,
    }
    for key, expected_value in expected.items():
        if binding.get(key) != expected_value:
            raise ValueError(f"Phase 1 binding mismatch: {key}")


def _authorized_vocabulary_inputs(
    payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], int]:
    counter_summary = payload.get("counter_summary")
    if not isinstance(counter_summary, Mapping):
        raise ValueError("counter_summary must be an object")

    row_denominator = counter_summary.get("rows_identity_admitted")
    if (
        not isinstance(row_denominator, int)
        or isinstance(row_denominator, bool)
        or row_denominator <= 0
    ):
        raise ValueError("rows_identity_admitted must be a positive integer")
    return counter_summary, row_denominator


def _validate_vocabulary(
    counter_summary: Mapping[str, Any],
    vocabulary_key: str,
    row_denominator: int,
) -> tuple[set[str], int]:
    vocabulary = counter_summary.get(vocabulary_key)
    if not isinstance(vocabulary, list) or not vocabulary:
        raise ValueError(f"{vocabulary_key} must be a non-empty list")

    observed_values: set[str] = set()
    total_count = 0
    for row in vocabulary:
        if not isinstance(row, Mapping):
            raise ValueError("each vocabulary row must be an object")
        count = row.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise ValueError("vocabulary row count must be a positive integer")
        evidence = row.get("evidence")
        if not isinstance(evidence, Mapping):
            raise ValueError("vocabulary row evidence must be an object")

        kind = evidence.get("kind")
        if kind == "OBSERVED":
            value = evidence.get("value")
            if not isinstance(value, str):
                raise ValueError("OBSERVED evidence must contain a string value")
            if value in observed_values:
                raise ValueError("duplicate exact OBSERVED lexical value")
            observed_values.add(value)
        elif kind == "UNAVAILABLE":
            reason = evidence.get("reason")
            if not isinstance(reason, str) or not reason:
                raise ValueError("UNAVAILABLE evidence must contain a reason")
        else:
            raise ValueError("unknown evidence kind")
        total_count += count

    if total_count != row_denominator:
        raise ValueError(f"{vocabulary_key} counts do not reconcile")
    return observed_values, len(observed_values)


def _phase1_exclusions(
    payload: Mapping[str, Any],
    field: str,
) -> set[str]:
    fields = payload.get("fields")
    if not isinstance(fields, Mapping):
        raise ValueError("Phase 1 fields must be an object")
    field_result = fields.get(field)
    if not isinstance(field_result, Mapping):
        raise ValueError(f"Phase 1 {field} result must be an object")
    if field_result.get("evaluable") is not True:
        raise ValueError(f"Phase 1 {field} must be evaluable")
    if field_result.get("field") != field:
        raise ValueError(f"Phase 1 {field} identity mismatch")

    candidates = field_result.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError(f"Phase 1 {field} candidates must be a list")
    exclusions: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            raise ValueError("each Phase 1 candidate must be an object")
        if candidate.get("field") != field:
            raise ValueError("Phase 1 candidate field mismatch")
        value = candidate.get("exact_lexical_value")
        if not isinstance(value, str):
            raise ValueError(
                "Phase 1 candidate exact_lexical_value must be a string"
            )
        if value in exclusions:
            raise ValueError("duplicate Phase 1 candidate identity")
        exclusions.add(value)
    return exclusions


def _require_agency_boundary(payload: Mapping[str, Any]) -> None:
    fields = payload.get("fields")
    if not isinstance(fields, Mapping):
        raise ValueError("Phase 1 fields must be an object")
    agency = fields.get("agency_responsible")
    if not isinstance(agency, Mapping):
        raise ValueError("Phase 1 agency result must be an object")
    expected = {
        "evaluable": False,
        "field": "agency_responsible",
        "reason": _AGENCY_NOT_EVALUABLE,
    }
    for key, expected_value in expected.items():
        if agency.get(key) != expected_value:
            raise ValueError(f"Phase 1 agency boundary mismatch: {key}")


def _build_stage_a_review_universe(
    *,
    baseline: Mapping[str, Any],
    phase1_result: Mapping[str, Any],
    input_baseline_sha256: str,
    input_phase1_result_sha256: str,
    generator_git_revision: str,
    python_version: str,
    generated_at_utc: str,
) -> dict[str, object]:
    counter_summary, row_denominator = _authorized_vocabulary_inputs(baseline)
    service_values, service_source_count = _validate_vocabulary(
        counter_summary,
        "service_name_vocabulary",
        row_denominator,
    )
    status_values, status_source_count = _validate_vocabulary(
        counter_summary,
        "status_vocabulary",
        row_denominator,
    )
    _require_agency_boundary(phase1_result)
    service_exclusions = _phase1_exclusions(phase1_result, "service_name")
    status_exclusions = _phase1_exclusions(
        phase1_result,
        "status_description",
    )

    if not service_exclusions.issubset(service_values):
        raise ValueError("Phase 1 service exclusions do not reconcile")
    if not status_exclusions.issubset(status_values):
        raise ValueError("Phase 1 status exclusions do not reconcile")

    service_review_values = service_values - service_exclusions
    status_review_values = status_values - status_exclusions
    entries = [
        {"field": field, "value": value}
        for field, values in (
            ("service_name", service_review_values),
            ("status_description", status_review_values),
        )
        for value in sorted(values)
    ]

    summary = {
        "service_phase1_excluded_count": len(service_exclusions),
        "service_source_vocabulary_count": service_source_count,
        "service_stage_a_review_count": len(service_review_values),
        "status_phase1_excluded_count": len(status_exclusions),
        "status_source_vocabulary_count": status_source_count,
        "status_stage_a_review_count": len(status_review_values),
        "total_stage_a_review_count": len(entries),
    }
    if (
        service_source_count
        != len(service_exclusions) + len(service_review_values)
        or status_source_count
        != len(status_exclusions) + len(status_review_values)
        or len(entries)
        != len(service_review_values) + len(status_review_values)
    ):
        raise ValueError("Stage A cardinality accounting does not reconcile")

    return {
        "binding": {
            "generated_at_utc": generated_at_utc,
            "generator_git_revision": generator_git_revision,
            "increment_008_contract": _INCREMENT_008_CONTRACT,
            "increment_008_version": _INCREMENT_008_VERSION,
            "input_baseline_sha256": input_baseline_sha256,
            "input_phase1_result_sha256": input_phase1_result_sha256,
            "phase": _PHASE_2,
            "python_version": python_version,
            "stage": _STAGE,
        },
        "entries": entries,
        "field_evaluability": {
            "agency_responsible": _AGENCY_NOT_EVALUABLE,
            "service_name": "EVALUABLE",
            "status_description": "EVALUABLE",
        },
        "summary": summary,
    }


def _report_failure(error: Exception) -> None:
    print(f"{type(error).__name__}: {error}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _argument_parser().parse_args(argv)

    try:
        baseline_sha256 = _sha256_file(arguments.baseline_result)
        if baseline_sha256 != arguments.expected_baseline_sha256:
            raise ValueError("baseline result SHA-256 mismatch")

        phase1_sha256 = _sha256_file(arguments.phase1_result)
        if phase1_sha256 != arguments.expected_phase1_sha256:
            raise ValueError("Phase 1 result SHA-256 mismatch")

        baseline = _load_json(arguments.baseline_result)
        phase1_result = _load_json(arguments.phase1_result)
        _require_increment_007_binding(baseline)
        _require_phase1_binding(phase1_result, baseline_sha256)

        result = _build_stage_a_review_universe(
            baseline=baseline,
            phase1_result=phase1_result,
            input_baseline_sha256=baseline_sha256,
            input_phase1_result_sha256=phase1_sha256,
            generator_git_revision=_capture_git_revision(),
            python_version=_capture_python_version(),
            generated_at_utc=_capture_generated_at_utc(),
        )
        serialized = json.dumps(result, sort_keys=True) + "\n"
        with arguments.output.open(
            mode="x",
            encoding="utf-8",
            newline="",
        ) as output_file:
            output_file.write(serialized)
    except Exception as error:
        _report_failure(error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

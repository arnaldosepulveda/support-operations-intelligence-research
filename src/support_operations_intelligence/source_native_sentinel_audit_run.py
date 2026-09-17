"""Synthetic-tested runner boundary for the retained Phase 1 audit."""

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

from support_operations_intelligence.source_native_sentinel_audit import (
    Phase1Candidate,
    Phase1FieldAuditResult,
    audit_phase1_field,
)


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
_PHASE = "PHASE_1"
_AGENCY_NOT_EVALUABLE = (
    "NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES"
)
_NO_CROSS_FIELD_UNION = (
    "NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES"
)


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-result", required=True, type=Path)
    parser.add_argument("--expected-baseline-sha256", required=True)
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


def _capture_run_date_utc() -> str:
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
        raise ValueError("baseline result must be a JSON object")
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


def _authorized_inputs(
    payload: Mapping[str, Any],
) -> tuple[list[dict[str, object]], list[dict[str, object]], int]:
    counter_summary = payload.get("counter_summary")
    if not isinstance(counter_summary, dict):
        raise ValueError("counter_summary must be an object")

    row_denominator = counter_summary.get("rows_identity_admitted")
    if (
        not isinstance(row_denominator, int)
        or isinstance(row_denominator, bool)
        or row_denominator <= 0
    ):
        raise ValueError("rows_identity_admitted must be a positive integer")

    service_vocabulary = counter_summary.get("service_name_vocabulary")
    if not isinstance(service_vocabulary, list):
        raise ValueError("service_name_vocabulary must be a list")

    status_vocabulary = counter_summary.get("status_vocabulary")
    if not isinstance(status_vocabulary, list):
        raise ValueError("status_vocabulary must be a list")

    return service_vocabulary, status_vocabulary, row_denominator


def _serialize_candidate(candidate: Phase1Candidate) -> dict[str, object]:
    return {
        "classification": candidate.classification,
        "exact_lexical_value": candidate.exact_lexical_value,
        "field": candidate.field,
        "matched_checks": list(candidate.matched_checks),
        "phase": candidate.phase,
        "row_count": candidate.row_count,
        "row_percentage": candidate.row_percentage,
        "vocabulary_percentage": candidate.vocabulary_percentage,
    }


def _serialize_field_result(
    result: Phase1FieldAuditResult,
) -> dict[str, object]:
    return {
        "aggregate_sentinel_candidate_row_count": (
            result.aggregate_sentinel_candidate_row_count
        ),
        "aggregate_sentinel_candidate_row_percentage": (
            result.aggregate_sentinel_candidate_row_percentage
        ),
        "aggregate_sentinel_candidate_vocabulary_count": (
            result.aggregate_sentinel_candidate_vocabulary_count
        ),
        "aggregate_sentinel_candidate_vocabulary_percentage": (
            result.aggregate_sentinel_candidate_vocabulary_percentage
        ),
        "candidate_count": len(result.candidates),
        "candidates": [
            _serialize_candidate(candidate) for candidate in result.candidates
        ],
        "distinct_vocabulary_count": result.distinct_vocabulary_count,
        "evaluable": True,
        "field": result.field,
        "materiality_classification": result.materiality_classification,
        "normalization_drift_candidate_count": (
            result.normalization_drift_candidate_count
        ),
        "normalization_drift_row_count": (
            result.normalization_drift_row_count
        ),
        "normalization_drift_row_percentage": (
            result.normalization_drift_row_percentage
        ),
        "row_denominator": result.row_denominator,
        "standalone_control_character_candidate_count": (
            result.standalone_control_character_candidate_count
        ),
        "standalone_control_character_row_count": (
            result.standalone_control_character_row_count
        ),
        "standalone_control_character_row_percentage": (
            result.standalone_control_character_row_percentage
        ),
    }


def _field_summary(result: Phase1FieldAuditResult) -> dict[str, object]:
    return {
        "aggregate_sentinel_candidate_row_count": (
            result.aggregate_sentinel_candidate_row_count
        ),
        "aggregate_sentinel_candidate_row_percentage": (
            result.aggregate_sentinel_candidate_row_percentage
        ),
        "evaluable": True,
        "materiality_classification": result.materiality_classification,
    }


def _build_result(
    *,
    input_baseline_sha256: str,
    audit_code_git_revision: str,
    python_version: str,
    run_date_utc: str,
    service_result: Phase1FieldAuditResult,
    status_result: Phase1FieldAuditResult,
) -> dict[str, object]:
    agency_field = {
        "evaluable": False,
        "field": "agency_responsible",
        "reason": _AGENCY_NOT_EVALUABLE,
    }
    agency_summary = {
        "evaluable": False,
        "reason": _AGENCY_NOT_EVALUABLE,
    }
    return {
        "binding": {
            "audit_code_git_revision": audit_code_git_revision,
            "increment_008_contract": _INCREMENT_008_CONTRACT,
            "increment_008_version": _INCREMENT_008_VERSION,
            "input_baseline_sha256": input_baseline_sha256,
            "input_increment_007_git_revision": (
                _EXPECTED_INCREMENT_007_REVISION
            ),
            "phase": _PHASE,
            "python_version": python_version,
            "run_date_utc": run_date_utc,
        },
        "fields": {
            "agency_responsible": agency_field,
            "service_name": _serialize_field_result(service_result),
            "status_description": _serialize_field_result(status_result),
        },
        "summary": {
            "agency_responsible": agency_summary,
            "cross_field_sentinel_union": _NO_CROSS_FIELD_UNION,
            "service_name": _field_summary(service_result),
            "status_description": _field_summary(status_result),
        },
    }


def _report_failure(error: Exception) -> None:
    print(f"{type(error).__name__}: {error}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _argument_parser().parse_args(argv)

    try:
        observed_sha256 = _sha256_file(arguments.baseline_result)
        if observed_sha256 != arguments.expected_baseline_sha256:
            raise ValueError("baseline result SHA-256 mismatch")

        baseline = _load_json(arguments.baseline_result)
        _require_increment_007_binding(baseline)
        (
            service_vocabulary,
            status_vocabulary,
            row_denominator,
        ) = _authorized_inputs(baseline)

        service_result = audit_phase1_field(
            "service_name",
            service_vocabulary,
            row_denominator,
        )
        status_result = audit_phase1_field(
            "status_description",
            status_vocabulary,
            row_denominator,
        )

        result = _build_result(
            input_baseline_sha256=observed_sha256,
            audit_code_git_revision=_capture_git_revision(),
            python_version=_capture_python_version(),
            run_date_utc=_capture_run_date_utc(),
            service_result=service_result,
            status_result=status_result,
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

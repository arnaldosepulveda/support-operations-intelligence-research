import argparse
import json
import platform
import resource
import subprocess
import sys
import time
from collections.abc import Sequence
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

from support_operations_intelligence.calgary_csv import (
    CalgaryCsvStructureError,
)
from support_operations_intelligence.calgary_full_artifact_execution import (
    CalgaryFullArtifactCounterSummary,
    CalgaryFullArtifactExecutionResult,
    execute_calgary_full_artifact,
)
from support_operations_intelligence.calgary_status_service_aggregation import (
    CalgaryGroupingEvidence,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
)


INCREMENT_VERSION = "007"
CONTRACT_ID = "007-full-artifact-execution-and-status-by-service-baseline"
HISTORICAL_ROWS_OBSERVED = 7_474_403
PERCENTAGE_QUANTUM = Decimal("0.0001")

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
DUPLICATE_COUNTER_SCOPE = (
    "Exact source-identifier repetition only; does not establish that one "
    "row equals one independently managed real-world unit of work."
)

_monotonic = time.monotonic


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


def _capture_run_date_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _capture_python_version() -> str:
    return platform.python_version()


def _capture_peak_rss_bytes() -> int:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def _evidence_sort_key(
    evidence: CalgaryGroupingEvidence,
) -> tuple[int, str]:
    if isinstance(evidence, ObservedEvidence):
        if not isinstance(evidence.value, str):
            raise TypeError("observed grouping evidence must contain a string")
        return (0, evidence.value)
    if isinstance(evidence, UnavailableEvidence):
        return (1, evidence.reason.value)
    raise TypeError(f"unsupported grouping evidence: {type(evidence).__name__}")


def _serialize_evidence(
    evidence: CalgaryGroupingEvidence,
) -> dict[str, str]:
    if isinstance(evidence, ObservedEvidence):
        if not isinstance(evidence.value, str):
            raise TypeError("observed grouping evidence must contain a string")
        return {
            "kind": "OBSERVED",
            "value": evidence.value,
        }
    if isinstance(evidence, UnavailableEvidence):
        return {
            "kind": "UNAVAILABLE",
            "reason": evidence.reason.value,
        }
    raise TypeError(f"unsupported grouping evidence: {type(evidence).__name__}")


def _serialize_vocabulary(
    vocabulary: dict[CalgaryGroupingEvidence, int],
) -> list[dict[str, object]]:
    return [
        {
            "evidence": _serialize_evidence(evidence),
            "count": count,
        }
        for evidence, count in sorted(
            vocabulary.items(),
            key=lambda item: _evidence_sort_key(item[0]),
        )
    ]


def _serialize_counter_summary(
    summary: CalgaryFullArtifactCounterSummary,
) -> dict[str, object]:
    return {
        "rows_observed": summary.rows_observed,
        "rows_structurally_accepted": summary.rows_structurally_accepted,
        "rows_structurally_rejected": summary.rows_structurally_rejected,
        "rows_identity_admitted": summary.rows_identity_admitted,
        "rows_identity_rejected": summary.rows_identity_rejected,
        "distinct_source_case_ids": summary.distinct_source_case_ids,
        "source_case_ids_appearing_more_than_once": (
            summary.source_case_ids_appearing_more_than_once
        ),
        "rows_involved_in_duplication": summary.rows_involved_in_duplication,
        "blank_service_name": summary.blank_service_name,
        "blank_agency_responsible": summary.blank_agency_responsible,
        "blank_status_description": summary.blank_status_description,
        "status_vocabulary": _serialize_vocabulary(summary.status_vocabulary),
        "service_name_vocabulary": _serialize_vocabulary(
            summary.service_name_vocabulary
        ),
    }


def _format_percentage(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        raise ValueError("percentage denominator must be positive")
    percentage = Decimal(numerator) * Decimal(100) / Decimal(denominator)
    return format(
        percentage.quantize(PERCENTAGE_QUANTUM, rounding=ROUND_HALF_EVEN),
        ".4f",
    )


def _serialize_status_by_service(
    result: CalgaryFullArtifactExecutionResult,
) -> list[dict[str, object]]:
    aggregation = result.aggregation
    service_totals: dict[CalgaryGroupingEvidence, int] = {}
    for (_, service_name), count in aggregation.aggregated_counts.items():
        service_totals[service_name] = service_totals.get(service_name, 0) + count

    ordered_cells = sorted(
        aggregation.aggregated_counts.items(),
        key=lambda item: (
            _evidence_sort_key(item[0][1]),
            _evidence_sort_key(item[0][0]),
        ),
    )
    return [
        {
            "service_name": _serialize_evidence(service_name),
            "status_description": _serialize_evidence(status_description),
            "count": count,
            "within_category_percentage": _format_percentage(
                count,
                service_totals[service_name],
            ),
            "portfolio_wide_percentage": _format_percentage(
                count,
                result.counter_summary.rows_identity_admitted,
            ),
        }
        for (status_description, service_name), count in ordered_cells
    ]


def _serialize_rejection_counts(
    result: CalgaryFullArtifactExecutionResult,
) -> list[dict[str, object]]:
    return [
        {
            "reason": reason.value,
            "count": count,
        }
        for reason, count in sorted(
            result.aggregation.rejection_counts_by_reason.items(),
            key=lambda item: item[0].value,
        )
    ]


def _build_baseline_result(
    result: CalgaryFullArtifactExecutionResult,
    *,
    git_revision: str,
    run_date_utc: str,
    python_version: str,
    peak_rss_bytes: int,
) -> dict[str, object]:
    current_rows_observed = result.counter_summary.rows_observed
    return {
        "artifact_sha256": result.verified_sha256,
        "git_revision": git_revision,
        "increment_version": INCREMENT_VERSION,
        "contract_id": CONTRACT_ID,
        "run_date_utc": run_date_utc,
        "python_version": python_version,
        "peak_rss_bytes": peak_rss_bytes,
        "counter_summary": _serialize_counter_summary(result.counter_summary),
        "rejection_counts": _serialize_rejection_counts(result),
        "status_by_service": _serialize_status_by_service(result),
        "historical_comparison": {
            "historical_rows_observed": HISTORICAL_ROWS_OBSERVED,
            "current_rows_observed": current_rows_observed,
            "difference": current_rows_observed - HISTORICAL_ROWS_OBSERVED,
            "cause": "NOT_DETERMINED",
        },
        "claims": {
            "established": [ESTABLISHED_CLAIM],
            "not_established": list(NOT_ESTABLISHED_CLAIMS),
            "duplicate_counter_scope": DUPLICATE_COUNTER_SCOPE,
            "cross_tab_interpretation": "NOT_INCLUDED",
        },
    }


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def _report_failure(error: Exception) -> None:
    if isinstance(error, CalgaryCsvStructureError):
        print(
            f"{type(error).__name__}: {error}; "
            f"logical_data_record_number={error.logical_data_record_number}; "
            f"raw_logical_record={error.raw_logical_record!r}",
            file=sys.stderr,
        )
        return
    print(f"{type(error).__name__}: {error}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _argument_parser().parse_args(argv)

    try:
        git_revision = _capture_git_revision()
        run_date_utc = _capture_run_date_utc()
        python_version = _capture_python_version()

        started_at = _monotonic()
        result = execute_calgary_full_artifact(
            arguments.artifact,
            arguments.expected_sha256,
        )
        payload = _build_baseline_result(
            result,
            git_revision=git_revision,
            run_date_utc=run_date_utc,
            python_version=python_version,
            peak_rss_bytes=_capture_peak_rss_bytes(),
        )
        wall_clock_seconds = _monotonic() - started_at
        payload["wall_clock_seconds"] = wall_clock_seconds

        serialized = json.dumps(payload, sort_keys=True) + "\n"
        with arguments.output.open(mode="w", encoding="utf-8", newline="") as output:
            output.write(serialized)
    except Exception as error:
        _report_failure(error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

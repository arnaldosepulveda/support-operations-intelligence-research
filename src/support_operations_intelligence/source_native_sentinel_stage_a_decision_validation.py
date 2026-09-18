"""Validate count-blinded Increment 008 Stage A decision evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Sequence


INCREMENT_008_CONTRACT = "008-source-native-sentinel-and-missingness-audit"
BATCH_SIZE = 100
REVIEWER_ROLE = "PROJECT_RESEARCHER"
NO_FLAG = "NO_PHASE_2_FLAG"
CANDIDATE = "EXPLORATORY_SENTINEL_CANDIDATE"
ALLOWED_DECISIONS = frozenset((NO_FLAG, CANDIDATE))
ALLOWED_STATUSES = frozenset(
    ("IN_PROGRESS", "COMPLETE_PENDING_RECONCILIATION")
)

_UNIVERSE_BINDING = {
    "increment_008_contract": INCREMENT_008_CONTRACT,
    "increment_008_version": "008",
    "phase": "PHASE_2",
    "stage": "STAGE_A_REVIEW_UNIVERSE",
}
_TOP_LEVEL_KEYS = frozenset(
    ("amendments", "batches", "binding", "review", "summary")
)
_BINDING_KEYS = frozenset(
    (
        "increment_008_contract",
        "increment_008_version",
        "input_stage_a_universe_entry_count",
        "input_stage_a_universe_sha256",
        "phase",
        "review_contract_git_revision",
        "reviewer_role",
        "stage",
    )
)
_REVIEW_KEYS = frozenset(("batch_size", "review_status"))
_BATCH_KEYS = frozenset(
    (
        "batch_number",
        "decisions",
        "end_position",
        "expected_entry_count",
        "reviewed_at_utc",
        "reviewed_entry_count",
        "reviewer_role",
        "start_position",
    )
)
_DECISION_KEYS = frozenset(("decision", "field", "value"))
_CANDIDATE_DECISION_KEYS = _DECISION_KEYS | {"rationale"}
_AMENDMENT_KEYS = frozenset(
    (
        "amended_at_utc",
        "field",
        "new_decision",
        "previous_decision",
        "reason",
        "reviewer_role",
        "value",
    )
)
_CANDIDATE_AMENDMENT_KEYS = _AMENDMENT_KEYS | {"rationale"}
_SUMMARY_KEYS = frozenset(
    (
        "batches_completed",
        "entries_reviewed",
        "exploratory_sentinel_candidate_count",
        "no_phase_2_flag_count",
        "review_status",
        "total_universe_entries",
    )
)


class ValidationError(Exception):
    """A validation failure whose message contains safe metadata only."""


def _mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{context} must be an object")
    return value


def _list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be an array")
    return value


def _exact_keys(
    value: dict[str, Any], expected: frozenset[str] | set[str], context: str
) -> None:
    if set(value) != set(expected):
        raise ValidationError(f"{context} schema mismatch")


def _integer(value: Any, context: str) -> int:
    if type(value) is not int:
        raise ValidationError(f"{context} must be an integer")
    return value


def _nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value


def _utc_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{context} must be a UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{context} must be a UTC timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValidationError(f"{context} must be a UTC timestamp")
    return parsed


def _stream_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
    except OSError:
        raise ValidationError("stage-a universe is unreadable") from None
    return digest.hexdigest()


def _load_json(path: Path) -> Any:
    """Load UTF-8 JSON while translating content-bearing errors."""

    try:
        with path.open("r", encoding="utf-8") as source:
            return json.load(source)
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise ValidationError("JSON artifact is unreadable or malformed") from None


def _validate_universe(payload: Any) -> list[tuple[str, str]]:
    universe = _mapping(payload, "stage-a universe")
    binding = _mapping(universe.get("binding"), "universe binding")
    for key, expected in _UNIVERSE_BINDING.items():
        if binding.get(key) != expected:
            raise ValidationError(f"universe binding mismatch for {key}")

    raw_entries = _list(universe.get("entries"), "universe entries")
    entries: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for position, raw_entry in enumerate(raw_entries, start=1):
        entry = _mapping(raw_entry, f"universe entry {position}")
        _exact_keys(entry, {"field", "value"}, f"universe entry {position}")
        field = entry.get("field")
        value = entry.get("value")
        if not isinstance(field, str) or not isinstance(value, str):
            raise ValidationError(
                f"universe entry {position} identity must contain strings"
            )
        identity = (field, value)
        if identity in seen:
            raise ValidationError(f"universe entry {position} duplicates identity")
        seen.add(identity)
        entries.append(identity)
    return entries


def _validate_binding(
    raw_binding: Any,
    universe_digest: str,
    universe_count: int,
    expected_revision: str,
) -> None:
    binding = _mapping(raw_binding, "decision binding")
    _exact_keys(binding, _BINDING_KEYS, "decision binding")
    expected = {
        "increment_008_contract": INCREMENT_008_CONTRACT,
        "increment_008_version": "008",
        "input_stage_a_universe_entry_count": universe_count,
        "input_stage_a_universe_sha256": universe_digest,
        "phase": "PHASE_2",
        "review_contract_git_revision": expected_revision,
        "reviewer_role": REVIEWER_ROLE,
        "stage": "STAGE_A_HUMAN_REVIEW",
    }
    for key, expected_value in expected.items():
        if binding.get(key) != expected_value:
            raise ValidationError(f"decision binding mismatch for {key}")


def _validate_review(raw_review: Any) -> str:
    review = _mapping(raw_review, "review")
    _exact_keys(review, _REVIEW_KEYS, "review")
    if review.get("batch_size") != BATCH_SIZE:
        raise ValidationError("review batch_size mismatch")
    status = review.get("review_status")
    if status not in ALLOWED_STATUSES:
        raise ValidationError("review status is not allowed")
    return status


def _validate_decision(
    raw_decision: Any,
    expected_identity: tuple[str, str],
    batch_number: int,
    position: int,
) -> tuple[tuple[str, str], str]:
    decision = _mapping(raw_decision, f"batch {batch_number} decision {position}")
    label = decision.get("decision")
    if label not in ALLOWED_DECISIONS:
        raise ValidationError(
            f"batch {batch_number} position {position} decision is not allowed"
        )
    expected_keys = (
        _CANDIDATE_DECISION_KEYS if label == CANDIDATE else _DECISION_KEYS
    )
    _exact_keys(
        decision,
        expected_keys,
        f"batch {batch_number} position {position} decision",
    )
    if not isinstance(decision.get("field"), str) or not isinstance(
        decision.get("value"), str
    ):
        raise ValidationError(
            f"batch {batch_number} position {position} identity must contain strings"
        )
    identity = (decision["field"], decision["value"])
    if identity != expected_identity:
        raise ValidationError(
            f"batch {batch_number} position {position} identity mismatch"
        )
    if label == CANDIDATE:
        _nonempty_string(
            decision.get("rationale"),
            f"batch {batch_number} position {position} rationale",
        )
    return identity, label


def _validate_batches(
    raw_batches: Any,
    universe_entries: list[tuple[str, str]],
) -> dict[tuple[str, str], str]:
    batches = _list(raw_batches, "batches")
    total_entries = len(universe_entries)
    total_expected_batches = (
        (total_entries + BATCH_SIZE - 1) // BATCH_SIZE if total_entries else 0
    )
    if len(batches) > total_expected_batches:
        raise ValidationError("retained batch count exceeds derived batch count")

    originals: dict[tuple[str, str], str] = {}
    for batch_index, raw_batch in enumerate(batches, start=1):
        batch = _mapping(raw_batch, f"batch {batch_index}")
        _exact_keys(batch, _BATCH_KEYS, f"batch {batch_index}")
        if batch.get("batch_number") != batch_index:
            raise ValidationError(
                f"batch {batch_index} violates contiguous-prefix ordering"
            )

        expected_start = (batch_index - 1) * BATCH_SIZE + 1
        expected_end = min(batch_index * BATCH_SIZE, total_entries)
        expected_count = expected_end - expected_start + 1
        expected_numbers = {
            "start_position": expected_start,
            "end_position": expected_end,
            "expected_entry_count": expected_count,
            "reviewed_entry_count": expected_count,
        }
        for key, expected_value in expected_numbers.items():
            observed = _integer(batch.get(key), f"batch {batch_index} {key}")
            if observed != expected_value:
                raise ValidationError(f"batch {batch_index} {key} mismatch")
        if batch.get("reviewer_role") != REVIEWER_ROLE:
            raise ValidationError(f"batch {batch_index} reviewer_role mismatch")
        _utc_timestamp(
            batch.get("reviewed_at_utc"),
            f"batch {batch_index} reviewed_at_utc",
        )

        decisions = _list(batch.get("decisions"), f"batch {batch_index} decisions")
        if len(decisions) != expected_count:
            raise ValidationError(f"batch {batch_index} decision count mismatch")
        for offset, raw_decision in enumerate(decisions):
            position = expected_start + offset
            identity, label = _validate_decision(
                raw_decision,
                universe_entries[position - 1],
                batch_index,
                position,
            )
            if identity in originals:
                raise ValidationError(
                    f"batch {batch_index} position {position} duplicates identity"
                )
            originals[identity] = label
    return originals


def _validate_amendments(
    raw_amendments: Any,
    originals: dict[tuple[str, str], str],
) -> tuple[dict[tuple[str, str], str], int]:
    amendments = _list(raw_amendments, "amendments")
    effective = dict(originals)
    previous_timestamp: datetime | None = None
    for amendment_index, raw_amendment in enumerate(amendments, start=1):
        amendment = _mapping(raw_amendment, f"amendment {amendment_index}")
        new_decision = amendment.get("new_decision")
        if new_decision not in ALLOWED_DECISIONS:
            raise ValidationError(
                f"amendment {amendment_index} new decision is not allowed"
            )
        expected_keys = (
            _CANDIDATE_AMENDMENT_KEYS
            if new_decision == CANDIDATE
            else _AMENDMENT_KEYS
        )
        _exact_keys(amendment, expected_keys, f"amendment {amendment_index}")
        if not isinstance(amendment.get("field"), str) or not isinstance(
            amendment.get("value"), str
        ):
            raise ValidationError(
                f"amendment {amendment_index} identity must contain strings"
            )
        identity = (amendment["field"], amendment["value"])
        if identity not in effective:
            raise ValidationError(
                f"amendment {amendment_index} targets an unreviewed identity"
            )
        previous_decision = amendment.get("previous_decision")
        if previous_decision not in ALLOWED_DECISIONS:
            raise ValidationError(
                f"amendment {amendment_index} previous decision is not allowed"
            )
        if previous_decision != effective[identity]:
            raise ValidationError(
                f"amendment {amendment_index} previous decision mismatch"
            )
        if new_decision == previous_decision:
            raise ValidationError(f"amendment {amendment_index} is a no-op")
        _nonempty_string(amendment.get("reason"), f"amendment {amendment_index} reason")
        if amendment.get("reviewer_role") != REVIEWER_ROLE:
            raise ValidationError(
                f"amendment {amendment_index} reviewer_role mismatch"
            )
        timestamp = _utc_timestamp(
            amendment.get("amended_at_utc"),
            f"amendment {amendment_index} amended_at_utc",
        )
        if previous_timestamp is not None and timestamp < previous_timestamp:
            raise ValidationError(
                f"amendment {amendment_index} chronology is out of order"
            )
        previous_timestamp = timestamp
        if new_decision == CANDIDATE:
            _nonempty_string(
                amendment.get("rationale"),
                f"amendment {amendment_index} rationale",
            )
        effective[identity] = new_decision
    return effective, len(amendments)


def _validate_summary(
    raw_summary: Any,
    universe_count: int,
    batch_count: int,
    effective: dict[tuple[str, str], str],
    review_status: str,
) -> dict[str, int | str]:
    summary = _mapping(raw_summary, "summary")
    _exact_keys(summary, _SUMMARY_KEYS, "summary")
    no_flag_count = sum(label == NO_FLAG for label in effective.values())
    candidate_count = sum(label == CANDIDATE for label in effective.values())
    entries_reviewed = len(effective)
    expected_values: dict[str, int] = {
        "total_universe_entries": universe_count,
        "entries_reviewed": entries_reviewed,
        "no_phase_2_flag_count": no_flag_count,
        "exploratory_sentinel_candidate_count": candidate_count,
        "batches_completed": batch_count,
    }
    for key, expected_value in expected_values.items():
        observed = _integer(summary.get(key), f"summary {key}")
        if observed != expected_value:
            raise ValidationError(f"summary {key} mismatch")
    if no_flag_count + candidate_count != entries_reviewed:
        raise ValidationError("summary decision accounting mismatch")

    expected_status = (
        "COMPLETE_PENDING_RECONCILIATION"
        if entries_reviewed == universe_count
        else "IN_PROGRESS"
    )
    summary_status = summary.get("review_status")
    if summary_status not in ALLOWED_STATUSES:
        raise ValidationError("summary status is not allowed")
    if review_status != summary_status:
        raise ValidationError("review and summary statuses disagree")
    if review_status != expected_status:
        raise ValidationError("review status does not match completion state")
    expected_batch_count = (
        (universe_count + BATCH_SIZE - 1) // BATCH_SIZE if universe_count else 0
    )
    if entries_reviewed == universe_count and batch_count != expected_batch_count:
        raise ValidationError("complete review is missing a derived batch")
    return {
        **expected_values,
        "review_status": review_status,
    }


def _validate_decisions(
    payload: Any,
    universe_entries: list[tuple[str, str]],
    universe_digest: str,
    expected_revision: str,
) -> tuple[dict[str, int | str], int]:
    artifact = _mapping(payload, "decision artifact")
    _exact_keys(artifact, _TOP_LEVEL_KEYS, "decision artifact top-level")
    _validate_binding(
        artifact.get("binding"),
        universe_digest,
        len(universe_entries),
        expected_revision,
    )
    review_status = _validate_review(artifact.get("review"))
    originals = _validate_batches(artifact.get("batches"), universe_entries)
    effective, amendment_count = _validate_amendments(
        artifact.get("amendments"), originals
    )
    batches = artifact["batches"]
    summary = _validate_summary(
        artifact.get("summary"),
        len(universe_entries),
        len(batches),
        effective,
        review_status,
    )
    return summary, amendment_count


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Increment 008 Stage A decision evidence."
    )
    parser.add_argument("--stage-a-universe", required=True, type=Path)
    parser.add_argument("--expected-stage-a-universe-sha256", required=True)
    parser.add_argument("--decisions", required=True, type=Path)
    parser.add_argument("--expected-review-contract-git-revision", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        universe_digest = _stream_sha256(args.stage_a_universe)
        if universe_digest != args.expected_stage_a_universe_sha256:
            raise ValidationError("stage-a universe SHA-256 mismatch")

        universe_payload = _load_json(args.stage_a_universe)
        universe_entries = _validate_universe(universe_payload)
        decisions_payload = _load_json(args.decisions)
        summary, amendment_count = _validate_decisions(
            decisions_payload,
            universe_entries,
            universe_digest,
            args.expected_review_contract_git_revision,
        )
    except ValidationError as error:
        print(f"VALIDATION=FAIL: {error}", file=sys.stderr)
        return 1
    except Exception:
        print("VALIDATION=FAIL: internal validation failure", file=sys.stderr)
        return 1

    print("VALIDATION=PASS")
    print(f"review_status={summary['review_status']}")
    print(f"batches_completed={summary['batches_completed']}")
    print(f"entries_reviewed={summary['entries_reviewed']}")
    print(f"no_phase_2_flag_count={summary['no_phase_2_flag_count']}")
    print(
        "exploratory_sentinel_candidate_count="
        f"{summary['exploratory_sentinel_candidate_count']}"
    )
    print(f"amendment_count={amendment_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Pure deterministic Phase 1 audit for retained source-native vocabularies."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN
from typing import Any


PHASE1_SENTINEL_VALUES = frozenset(
    {
        "unknown",
        "n/a",
        "na",
        "null",
        "none",
        "nil",
        "not available",
        "not applicable",
        "not specified",
        "unspecified",
        "undefined",
        "tbd",
        "to be determined",
        "blank",
        "empty",
        "missing",
        "-",
        "--",
        ".",
        "?",
        "0",
        "no data",
        "nodata",
    }
)

_EVALUABLE = "EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY"

_PHASE_1A = "PHASE_1A_EXACT_EMPTY_STRING"
_PHASE_1B = "PHASE_1B_WHITESPACE_ONLY"
_PHASE_1C = "PHASE_1C_CASE_INSENSITIVE_EXACT_SENTINEL"
_PHASE_1D = "PHASE_1D_LEADING_OR_TRAILING_WHITESPACE"
_PHASE_1E = "PHASE_1E_NON_PRINTABLE_OR_CONTROL"

_SENTINEL_CHECKS = frozenset({_PHASE_1A, _PHASE_1B, _PHASE_1C})
_FROZEN_WHITESPACE = frozenset({" ", "\t", "\u00a0"})

_SENTINEL_CANDIDATE = "SENTINEL_CANDIDATE"
_NORMALIZATION_DRIFT_CANDIDATE = "NORMALIZATION_DRIFT_CANDIDATE"
_CONTROL_CHARACTER_CANDIDATE = "CONTROL_CHARACTER_CANDIDATE"

_FOOTNOTE_ONLY = "FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE"
_EXPLICIT_QUALIFICATION = "EXPLICIT_COMPLETENESS_QUALIFICATION"
_RECORDED_DECISION = (
    "RECORDED_BASELINE_DESCRIPTION_DECISION_REQUIRED_BEFORE_PUBLICATION"
)

_DISPLAY_QUANTUM = Decimal("0.000001")


@dataclass(frozen=True, slots=True)
class Phase1Candidate:
    field: str
    exact_lexical_value: str
    phase: str
    matched_checks: tuple[str, ...]
    classification: str
    row_count: int
    row_percentage_exact: Decimal
    row_percentage: str
    vocabulary_percentage_exact: Decimal
    vocabulary_percentage: str


@dataclass(frozen=True, slots=True)
class Phase1FieldAuditResult:
    field: str
    evaluability_status: str
    row_denominator: int
    distinct_vocabulary_count: int
    candidates: tuple[Phase1Candidate, ...]
    aggregate_sentinel_candidate_row_count: int
    aggregate_sentinel_candidate_row_percentage_exact: Decimal
    aggregate_sentinel_candidate_row_percentage: str
    aggregate_sentinel_candidate_vocabulary_count: int
    aggregate_sentinel_candidate_vocabulary_percentage_exact: Decimal
    aggregate_sentinel_candidate_vocabulary_percentage: str
    materiality_classification: str
    normalization_drift_candidate_count: int
    normalization_drift_row_count: int
    normalization_drift_row_percentage_exact: Decimal
    normalization_drift_row_percentage: str
    standalone_control_character_candidate_count: int
    standalone_control_character_row_count: int
    standalone_control_character_row_percentage_exact: Decimal
    standalone_control_character_row_percentage: str


def audit_phase1_field(
    field_name: str,
    vocabulary_rows: Iterable[Mapping[str, Any]],
    row_denominator: int,
) -> Phase1FieldAuditResult:
    """Audit one supplied retained vocabulary without reading external data."""

    if not isinstance(field_name, str) or not field_name:
        raise ValueError("field_name must be a non-empty string")
    if (
        not isinstance(row_denominator, int)
        or isinstance(row_denominator, bool)
        or row_denominator <= 0
    ):
        raise ValueError("row_denominator must be a positive integer")

    validated_rows: list[tuple[str | None, int]] = []
    observed_values: set[str] = set()
    total_count = 0

    try:
        rows = list(vocabulary_rows)
    except TypeError as error:
        raise ValueError("vocabulary_rows must be iterable") from error

    if not rows:
        raise ValueError("vocabulary_rows must not be empty")

    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("each vocabulary row must be a mapping")
        if "evidence" not in row:
            raise ValueError("vocabulary row is missing evidence")
        if "count" not in row:
            raise ValueError("vocabulary row is missing count")

        count = row["count"]
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise ValueError("vocabulary row count must be a positive integer")

        evidence = row["evidence"]
        if not isinstance(evidence, Mapping):
            raise ValueError("vocabulary row evidence must be a mapping")

        kind = evidence.get("kind")
        if kind == "OBSERVED":
            value = evidence.get("value")
            if not isinstance(value, str):
                raise ValueError("OBSERVED evidence must contain a string value")
            if value in observed_values:
                raise ValueError("duplicate exact OBSERVED lexical value")
            observed_values.add(value)
            validated_rows.append((value, count))
        elif kind == "UNAVAILABLE":
            reason = evidence.get("reason")
            if not isinstance(reason, str) or not reason:
                raise ValueError("UNAVAILABLE evidence must contain a reason")
            validated_rows.append((None, count))
        else:
            raise ValueError("unknown evidence kind")

        total_count += count

    if total_count != row_denominator:
        raise ValueError("vocabulary row counts do not reconcile")

    distinct_vocabulary_count = len(validated_rows)
    vocabulary_percentage_exact = _percentage(1, distinct_vocabulary_count)
    candidates: list[Phase1Candidate] = []

    for value, count in validated_rows:
        if value is None:
            continue

        matched_checks = _matched_checks(value)
        if not matched_checks:
            continue

        row_percentage_exact = _percentage(count, row_denominator)
        candidates.append(
            Phase1Candidate(
                field=field_name,
                exact_lexical_value=value,
                phase="PHASE_1",
                matched_checks=matched_checks,
                classification=_classification(matched_checks),
                row_count=count,
                row_percentage_exact=row_percentage_exact,
                row_percentage=_display_percentage(row_percentage_exact),
                vocabulary_percentage_exact=vocabulary_percentage_exact,
                vocabulary_percentage=_display_percentage(
                    vocabulary_percentage_exact
                ),
            )
        )

    ordered_candidates = tuple(
        sorted(
            candidates,
            key=lambda candidate: (
                candidate.field,
                candidate.exact_lexical_value,
            ),
        )
    )
    aggregate_sentinel_candidates = tuple(
        candidate
        for candidate in ordered_candidates
        if _SENTINEL_CHECKS.intersection(candidate.matched_checks)
    )
    normalization_drift_candidates = tuple(
        candidate
        for candidate in ordered_candidates
        if _PHASE_1D in candidate.matched_checks
    )
    standalone_control_candidates = tuple(
        candidate
        for candidate in ordered_candidates
        if candidate.classification == _CONTROL_CHARACTER_CANDIDATE
    )

    aggregate_row_count = sum(
        candidate.row_count for candidate in aggregate_sentinel_candidates
    )
    aggregate_row_percentage_exact = _percentage(
        aggregate_row_count,
        row_denominator,
    )
    aggregate_vocabulary_count = len(aggregate_sentinel_candidates)
    aggregate_vocabulary_percentage_exact = _percentage(
        aggregate_vocabulary_count,
        distinct_vocabulary_count,
    )

    normalization_drift_row_count = sum(
        candidate.row_count for candidate in normalization_drift_candidates
    )
    normalization_drift_row_percentage_exact = _percentage(
        normalization_drift_row_count,
        row_denominator,
    )

    standalone_control_row_count = sum(
        candidate.row_count for candidate in standalone_control_candidates
    )
    standalone_control_row_percentage_exact = _percentage(
        standalone_control_row_count,
        row_denominator,
    )

    return Phase1FieldAuditResult(
        field=field_name,
        evaluability_status=_EVALUABLE,
        row_denominator=row_denominator,
        distinct_vocabulary_count=distinct_vocabulary_count,
        candidates=ordered_candidates,
        aggregate_sentinel_candidate_row_count=aggregate_row_count,
        aggregate_sentinel_candidate_row_percentage_exact=(
            aggregate_row_percentage_exact
        ),
        aggregate_sentinel_candidate_row_percentage=_display_percentage(
            aggregate_row_percentage_exact
        ),
        aggregate_sentinel_candidate_vocabulary_count=(
            aggregate_vocabulary_count
        ),
        aggregate_sentinel_candidate_vocabulary_percentage_exact=(
            aggregate_vocabulary_percentage_exact
        ),
        aggregate_sentinel_candidate_vocabulary_percentage=(
            _display_percentage(aggregate_vocabulary_percentage_exact)
        ),
        materiality_classification=_materiality(
            aggregate_row_percentage_exact
        ),
        normalization_drift_candidate_count=len(
            normalization_drift_candidates
        ),
        normalization_drift_row_count=normalization_drift_row_count,
        normalization_drift_row_percentage_exact=(
            normalization_drift_row_percentage_exact
        ),
        normalization_drift_row_percentage=_display_percentage(
            normalization_drift_row_percentage_exact
        ),
        standalone_control_character_candidate_count=len(
            standalone_control_candidates
        ),
        standalone_control_character_row_count=standalone_control_row_count,
        standalone_control_character_row_percentage_exact=(
            standalone_control_row_percentage_exact
        ),
        standalone_control_character_row_percentage=_display_percentage(
            standalone_control_row_percentage_exact
        ),
    )


def _matched_checks(value: str) -> tuple[str, ...]:
    matches: list[str] = []
    is_frozen_whitespace = bool(value) and all(
        character in _FROZEN_WHITESPACE for character in value
    )
    has_boundary_whitespace = (
        bool(value)
        and not is_frozen_whitespace
        and (
            value[0] in _FROZEN_WHITESPACE
            or value[-1] in _FROZEN_WHITESPACE
        )
    )

    if value == "":
        matches.append(_PHASE_1A)
    if is_frozen_whitespace:
        matches.append(_PHASE_1B)
    if value.casefold() in PHASE1_SENTINEL_VALUES:
        matches.append(_PHASE_1C)
    if has_boundary_whitespace:
        matches.append(_PHASE_1D)
    has_non_frozen_control = any(
        not character.isprintable()
        and character not in _FROZEN_WHITESPACE
        for character in value
    )
    if (
        any(not character.isprintable() for character in value)
        and (
            not has_boundary_whitespace
            or is_frozen_whitespace
            or has_non_frozen_control
        )
    ):
        matches.append(_PHASE_1E)

    return tuple(matches)


def _classification(matched_checks: tuple[str, ...]) -> str:
    if _SENTINEL_CHECKS.intersection(matched_checks):
        return _SENTINEL_CANDIDATE
    if _PHASE_1D in matched_checks:
        return _NORMALIZATION_DRIFT_CANDIDATE
    return _CONTROL_CHARACTER_CANDIDATE


def _percentage(numerator: int, denominator: int) -> Decimal:
    return Decimal(100) * Decimal(numerator) / Decimal(denominator)


def _display_percentage(value: Decimal) -> str:
    return format(value.quantize(_DISPLAY_QUANTUM, rounding=ROUND_HALF_EVEN), "f")


def _materiality(coverage: Decimal) -> str:
    if coverage < Decimal("0.1"):
        return _FOOTNOTE_ONLY
    if coverage <= Decimal("2.0"):
        return _EXPLICIT_QUALIFICATION
    return _RECORDED_DECISION

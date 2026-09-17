import unittest
from decimal import Decimal

from support_operations_intelligence.source_native_sentinel_audit import (
    PHASE1_SENTINEL_VALUES,
    Phase1Candidate,
    Phase1FieldAuditResult,
    audit_phase1_field,
)


ROW_DENOMINATOR = 7_474_403
EVALUABLE = "EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY"

PHASE_1A = "PHASE_1A_EXACT_EMPTY_STRING"
PHASE_1B = "PHASE_1B_WHITESPACE_ONLY"
PHASE_1C = "PHASE_1C_CASE_INSENSITIVE_EXACT_SENTINEL"
PHASE_1D = "PHASE_1D_LEADING_OR_TRAILING_WHITESPACE"
PHASE_1E = "PHASE_1E_NON_PRINTABLE_OR_CONTROL"

SENTINEL_CANDIDATE = "SENTINEL_CANDIDATE"
NORMALIZATION_DRIFT_CANDIDATE = "NORMALIZATION_DRIFT_CANDIDATE"
CONTROL_CHARACTER_CANDIDATE = "CONTROL_CHARACTER_CANDIDATE"

FOOTNOTE_ONLY = "FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE"
EXPLICIT_QUALIFICATION = "EXPLICIT_COMPLETENESS_QUALIFICATION"
RECORDED_DECISION = (
    "RECORDED_BASELINE_DESCRIPTION_DECISION_REQUIRED_BEFORE_PUBLICATION"
)


def _observed(value: str, count: int) -> dict[str, object]:
    return {
        "evidence": {"kind": "OBSERVED", "value": value},
        "count": count,
    }


def _unavailable(reason: str, count: int) -> dict[str, object]:
    return {
        "evidence": {"kind": "UNAVAILABLE", "reason": reason},
        "count": count,
    }


def _audit(
    rows: list[dict[str, object]],
    row_denominator: int,
    field_name: str = "service_name",
) -> Phase1FieldAuditResult:
    return audit_phase1_field(field_name, rows, row_denominator)


def _candidate_by_value(
    result: Phase1FieldAuditResult,
) -> dict[str, Phase1Candidate]:
    return {
        candidate.exact_lexical_value: candidate
        for candidate in result.candidates
    }


class SourceNativeSentinelAuditPhase1ContractTests(unittest.TestCase):
    def test_phase1_sentinel_values_are_the_exact_immutable_contract(self) -> None:
        expected = frozenset(
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

        self.assertIsInstance(PHASE1_SENTINEL_VALUES, frozenset)
        self.assertEqual(PHASE1_SENTINEL_VALUES, expected)

    def test_phase1a_retains_exact_empty_string_and_count(self) -> None:
        result = _audit([_observed("", 2), _observed("ordinary", 3)], 5)

        candidate = _candidate_by_value(result)[""]
        self.assertEqual(candidate.exact_lexical_value, "")
        self.assertEqual(candidate.row_count, 2)
        self.assertEqual(candidate.matched_checks, (PHASE_1A,))
        self.assertEqual(candidate.classification, SENTINEL_CANDIDATE)
        self.assertNotIn(candidate.exact_lexical_value, ("(blank)", None, "missing"))

    def test_phase1b_uses_only_the_three_frozen_whitespace_characters(self) -> None:
        frozen_values = (" ", "\t", "\u00a0", " \t\u00a0 ")
        rows = [_observed(value, 1) for value in frozen_values]
        rows.extend([_observed("\n", 1), _observed("\r", 1)])
        result = _audit(rows, 6)
        candidates = _candidate_by_value(result)

        for value in frozen_values:
            with self.subTest(value=repr(value)):
                self.assertIn(PHASE_1B, candidates[value].matched_checks)
        for value in ("\n", "\r"):
            with self.subTest(value=repr(value)):
                self.assertNotIn(PHASE_1B, candidates[value].matched_checks)
                self.assertIn(PHASE_1E, candidates[value].matched_checks)

    def test_phase1c_is_case_insensitive_exact_and_never_trims(self) -> None:
        rows = [
            _observed("unknown", 1),
            _observed("UNKNOWN", 1),
            _observed("Unknown", 1),
            _observed("Unknown Service", 1),
            _observed(" unknown ", 1),
        ]
        result = _audit(rows, 5)
        candidates = _candidate_by_value(result)

        for value in ("unknown", "UNKNOWN", "Unknown"):
            with self.subTest(value=value):
                self.assertIn(PHASE_1C, candidates[value].matched_checks)
        self.assertNotIn("Unknown Service", candidates)
        self.assertNotIn(PHASE_1C, candidates[" unknown "].matched_checks)
        self.assertEqual(candidates[" unknown "].matched_checks, (PHASE_1D,))

    def test_phase1d_is_normalization_drift_not_missingness(self) -> None:
        values = (" Service", "Service ", "\tService", "Service\u00a0")
        rows = [_observed(value, 1) for value in values]
        rows.append(_observed("ordinary", 1))
        result = _audit(rows, 5)
        candidates = _candidate_by_value(result)

        for value in values:
            with self.subTest(value=repr(value)):
                candidate = candidates[value]
                self.assertEqual(candidate.matched_checks, (PHASE_1D,))
                self.assertEqual(
                    candidate.classification,
                    NORMALIZATION_DRIFT_CANDIDATE,
                )
        self.assertEqual(result.aggregate_sentinel_candidate_row_count, 0)

    def test_phase1e_retains_control_checks_and_overlap_without_duplication(self) -> None:
        rows = [
            _observed("\n", 2),
            _observed("\r", 3),
            _observed("\x00", 5),
            _observed("\t", 7),
            _observed("ordinary", 11),
        ]
        result = _audit(rows, 28)
        candidates = _candidate_by_value(result)

        for value in ("\n", "\r", "\x00"):
            with self.subTest(value=repr(value)):
                self.assertEqual(candidates[value].matched_checks, (PHASE_1E,))
                self.assertEqual(
                    candidates[value].classification,
                    CONTROL_CHARACTER_CANDIDATE,
                )

        tab = candidates["\t"]
        self.assertEqual(tab.matched_checks, (PHASE_1B, PHASE_1E))
        self.assertEqual(tab.classification, SENTINEL_CANDIDATE)
        self.assertEqual(tab.row_count, 7)
        self.assertEqual(
            [candidate.exact_lexical_value for candidate in result.candidates].count("\t"),
            1,
        )
        self.assertEqual(result.aggregate_sentinel_candidate_row_count, 7)

    def test_unavailable_evidence_is_not_a_lexical_candidate(self) -> None:
        rows = [
            _unavailable("VALUE_ABSENT", 2),
            _unavailable("EVIDENCE_INDETERMINATE", 3),
            _observed("ordinary", 5),
        ]

        result = _audit(rows, 10)

        self.assertEqual(result.candidates, ())
        self.assertEqual(result.aggregate_sentinel_candidate_row_count, 0)

    def test_percentages_use_decimal_counts_and_six_place_half_even_display(self) -> None:
        rows = [
            _observed("unknown", 1),
            _observed("ordinary", ROW_DENOMINATOR - 1),
        ]
        result = _audit(rows, ROW_DENOMINATOR)
        candidate = _candidate_by_value(result)["unknown"]

        expected_row_percentage = Decimal(100) / Decimal(ROW_DENOMINATOR)
        self.assertIsInstance(candidate.row_percentage_exact, Decimal)
        self.assertEqual(candidate.row_percentage_exact, expected_row_percentage)
        self.assertEqual(candidate.row_percentage, "0.000013")
        self.assertNotEqual(candidate.row_percentage, "0.000000")
        self.assertEqual(candidate.vocabulary_percentage_exact, Decimal("50"))
        self.assertEqual(candidate.vocabulary_percentage, "50.000000")

    def test_field_result_reconciles_aggregate_and_separate_candidate_coverage(self) -> None:
        rows = [
            _observed("", 2),
            _observed("\t", 3),
            _observed("unknown", 5),
            _observed(" Service", 7),
            _observed("\n", 11),
            _observed("ordinary", 72),
        ]
        result = _audit(rows, 100)

        self.assertIsInstance(result, Phase1FieldAuditResult)
        self.assertEqual(result.field, "service_name")
        self.assertEqual(result.evaluability_status, EVALUABLE)
        self.assertEqual(result.row_denominator, 100)
        self.assertEqual(result.distinct_vocabulary_count, 6)
        self.assertTrue(
            all(isinstance(candidate, Phase1Candidate) for candidate in result.candidates)
        )
        self.assertTrue(all(candidate.phase == "PHASE_1" for candidate in result.candidates))
        self.assertEqual(result.aggregate_sentinel_candidate_row_count, 10)
        self.assertEqual(result.aggregate_sentinel_candidate_row_percentage_exact, Decimal("10"))
        self.assertEqual(result.aggregate_sentinel_candidate_row_percentage, "10.000000")
        self.assertEqual(result.aggregate_sentinel_candidate_vocabulary_count, 3)
        self.assertEqual(result.aggregate_sentinel_candidate_vocabulary_percentage_exact, Decimal("50"))
        self.assertEqual(result.aggregate_sentinel_candidate_vocabulary_percentage, "50.000000")
        self.assertEqual(result.normalization_drift_candidate_count, 1)
        self.assertEqual(result.normalization_drift_row_count, 7)
        self.assertEqual(result.normalization_drift_row_percentage, "7.000000")
        self.assertEqual(result.standalone_control_character_candidate_count, 1)
        self.assertEqual(result.standalone_control_character_row_count, 11)
        self.assertEqual(result.standalone_control_character_row_percentage, "11.000000")
        self.assertEqual(result.materiality_classification, RECORDED_DECISION)

    def test_materiality_uses_unrounded_decimal_exact_boundaries(self) -> None:
        cases = (
            (9, FOOTNOTE_ONLY),
            (10, EXPLICIT_QUALIFICATION),
            (200, EXPLICIT_QUALIFICATION),
            (201, RECORDED_DECISION),
        )

        for sentinel_count, expected_classification in cases:
            with self.subTest(sentinel_count=sentinel_count):
                result = _audit(
                    [
                        _observed("unknown", sentinel_count),
                        _observed("ordinary", 10_000 - sentinel_count),
                    ],
                    10_000,
                )
                expected_exact = Decimal(100 * sentinel_count) / Decimal(10_000)
                self.assertEqual(
                    result.aggregate_sentinel_candidate_row_percentage_exact,
                    expected_exact,
                )
                self.assertEqual(
                    result.materiality_classification,
                    expected_classification,
                )

    def test_candidates_are_ordered_by_exact_python_string_order(self) -> None:
        rows = [
            _observed("unknown", 1),
            _observed(" Service", 1),
            _observed("\n", 1),
            _observed("", 1),
        ]

        result = _audit(rows, 4, field_name="status_description")

        self.assertEqual(
            [candidate.exact_lexical_value for candidate in result.candidates],
            sorted(["unknown", " Service", "\n", ""]),
        )
        self.assertTrue(
            all(candidate.field == "status_description" for candidate in result.candidates)
        )

    def test_malformed_vocabulary_rows_fail_closed(self) -> None:
        malformed_cases = (
            ({"count": 1},),
            ({"evidence": {"kind": "OTHER", "value": "x"}, "count": 1},),
            ({"evidence": {"kind": "OBSERVED"}, "count": 1},),
            ({"evidence": {"kind": "OBSERVED", "value": None}, "count": 1},),
            ({"evidence": {"kind": "OBSERVED", "value": "x"}},),
            ({"evidence": {"kind": "OBSERVED", "value": "x"}, "count": 0},),
            ({"evidence": {"kind": "OBSERVED", "value": "x"}, "count": -1},),
            (_observed("duplicate", 1), _observed("duplicate", 1)),
        )

        for rows in malformed_cases:
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    _audit(list(rows), sum(row.get("count", 1) for row in rows))

    def test_vocabulary_count_must_reconcile_to_row_denominator(self) -> None:
        rows = [_observed("unknown", 1), _observed("ordinary", 2)]

        with self.assertRaises(ValueError):
            _audit(rows, 4)


if __name__ == "__main__":
    unittest.main()

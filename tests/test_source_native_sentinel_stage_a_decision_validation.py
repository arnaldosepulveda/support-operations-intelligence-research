import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import support_operations_intelligence.source_native_sentinel_stage_a_decision_validation as decision_validation


INCREMENT_008_CONTRACT = "008-source-native-sentinel-and-missingness-audit"
EXPECTED_REVIEW_CONTRACT_REVISION = "c" * 40
BATCH_SIZE = 100
NO_FLAG = "NO_PHASE_2_FLAG"
CANDIDATE = "EXPLORATORY_SENTINEL_CANDIDATE"
SYNTHETIC_RATIONALE_SECRET = "SYNTHETIC-RATIONALE-DO-NOT-ECHO"
SYNTHETIC_AMENDMENT_REASON_SECRET = "SYNTHETIC-AMENDMENT-DO-NOT-ECHO"


class StageADecisionValidationContractTests(unittest.TestCase):
    def _write_json(self, path: Path, payload: dict[str, object]) -> str:
        path.write_text(
            json.dumps(payload, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="",
        )
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _universe(self, size: int) -> dict[str, object]:
        return {
            "binding": {
                "increment_008_contract": INCREMENT_008_CONTRACT,
                "increment_008_version": "008",
                "phase": "PHASE_2",
                "stage": "STAGE_A_REVIEW_UNIVERSE",
            },
            "entries": [
                {
                    "field": (
                        "status_description"
                        if position == size
                        else "service_name"
                    ),
                    "value": f"SYNTHETIC-LEXICAL-SECRET-{position:04d}",
                }
                for position in range(1, size + 1)
            ],
        }

    def _decision_artifact(
        self,
        universe: dict[str, object],
        universe_sha256: str,
        reviewed_count: int,
        candidate_positions: frozenset[int] = frozenset(),
    ) -> dict[str, object]:
        entries = universe["entries"]
        self.assertIsInstance(entries, list)
        batches = []
        for start in range(1, reviewed_count + 1, BATCH_SIZE):
            end = min(start + BATCH_SIZE - 1, len(entries))
            decisions = []
            for position in range(start, end + 1):
                universe_entry = entries[position - 1]
                self.assertIsInstance(universe_entry, dict)
                decision = {
                    "decision": (
                        CANDIDATE
                        if position in candidate_positions
                        else NO_FLAG
                    ),
                    "field": universe_entry["field"],
                    "value": universe_entry["value"],
                }
                if position in candidate_positions:
                    decision["rationale"] = SYNTHETIC_RATIONALE_SECRET
                decisions.append(decision)
            expected_count = end - start + 1
            batches.append(
                {
                    "batch_number": len(batches) + 1,
                    "decisions": decisions,
                    "end_position": end,
                    "expected_entry_count": expected_count,
                    "reviewed_at_utc": "2026-09-18T18:00:00+00:00",
                    "reviewed_entry_count": expected_count,
                    "reviewer_role": "PROJECT_RESEARCHER",
                    "start_position": start,
                }
            )

        complete = reviewed_count == len(entries)
        review_status = (
            "COMPLETE_PENDING_RECONCILIATION"
            if complete
            else "IN_PROGRESS"
        )
        candidate_count = len(
            candidate_positions.intersection(range(1, reviewed_count + 1))
        )
        return {
            "amendments": [],
            "batches": batches,
            "binding": {
                "increment_008_contract": INCREMENT_008_CONTRACT,
                "increment_008_version": "008",
                "input_stage_a_universe_entry_count": len(entries),
                "input_stage_a_universe_sha256": universe_sha256,
                "phase": "PHASE_2",
                "review_contract_git_revision": (
                    EXPECTED_REVIEW_CONTRACT_REVISION
                ),
                "reviewer_role": "PROJECT_RESEARCHER",
                "stage": "STAGE_A_HUMAN_REVIEW",
            },
            "review": {
                "batch_size": BATCH_SIZE,
                "review_status": review_status,
            },
            "summary": {
                "batches_completed": len(batches),
                "entries_reviewed": reviewed_count,
                "exploratory_sentinel_candidate_count": candidate_count,
                "no_phase_2_flag_count": reviewed_count - candidate_count,
                "review_status": review_status,
                "total_universe_entries": len(entries),
            },
        }

    def _write_case(
        self,
        root: Path,
        *,
        size: int = 3,
        reviewed_count: int | None = None,
        candidate_positions: frozenset[int] = frozenset(),
    ) -> tuple[Path, str, Path, dict[str, object], dict[str, object]]:
        universe = self._universe(size)
        universe_path = root / "synthetic-stage-a-universe.json"
        universe_sha256 = self._write_json(universe_path, universe)
        actual_reviewed_count = size if reviewed_count is None else reviewed_count
        decisions = self._decision_artifact(
            universe,
            universe_sha256,
            actual_reviewed_count,
            candidate_positions,
        )
        decisions_path = root / "synthetic-stage-a-decisions.json"
        self._write_json(decisions_path, decisions)
        return (
            universe_path,
            universe_sha256,
            decisions_path,
            universe,
            decisions,
        )

    def _rewrite_decisions(
        self,
        path: Path,
        decisions: dict[str, object],
    ) -> None:
        self._write_json(path, decisions)

    def _invoke(
        self,
        universe_path: Path,
        universe_sha256: str,
        decisions_path: Path,
    ) -> int:
        return decision_validation.main(
            [
                "--stage-a-universe",
                str(universe_path),
                "--expected-stage-a-universe-sha256",
                universe_sha256,
                "--decisions",
                str(decisions_path),
                "--expected-review-contract-git-revision",
                EXPECTED_REVIEW_CONTRACT_REVISION,
            ]
        )

    def _invoke_captured(
        self,
        universe_path: Path,
        universe_sha256: str,
        decisions_path: Path,
    ) -> tuple[int, str]:
        output = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
        ):
            return_code = self._invoke(
                universe_path,
                universe_sha256,
                decisions_path,
            )
        return return_code, output.getvalue()

    def _valid_amendment(
        self,
        universe: dict[str, object],
    ) -> dict[str, object]:
        entries = universe["entries"]
        self.assertIsInstance(entries, list)
        identity = entries[0]
        self.assertIsInstance(identity, dict)
        return {
            "amended_at_utc": "2026-09-18T19:00:00+00:00",
            "field": identity["field"],
            "new_decision": CANDIDATE,
            "previous_decision": NO_FLAG,
            "rationale": SYNTHETIC_RATIONALE_SECRET,
            "reason": SYNTHETIC_AMENDMENT_REASON_SECRET,
            "reviewer_role": "PROJECT_RESEARCHER",
            "value": identity["value"],
        }

    def test_universe_hash_mismatch_stops_before_parse_or_validation(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(Path(temporary_directory))
            synthetic_secret = "SYNTHETIC-LEXICAL-SECRET-0001"
            with patch.object(decision_validation, "_load_json") as load_json:
                return_code, diagnostics = self._invoke_captured(
                    case[0],
                    "0" * 64,
                    case[2],
                )
            self.assertNotEqual(return_code, 0)
            load_json.assert_not_called()
            self.assertNotIn(synthetic_secret, diagnostics)

    def test_valid_completed_prefix_is_in_progress(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(
                Path(temporary_directory),
                size=105,
                reviewed_count=100,
                candidate_positions=frozenset({2}),
            )
            self.assertEqual(self._invoke(*case[:3]), 0)

    def test_valid_complete_review_reconciles(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(
                Path(temporary_directory),
                size=3,
                candidate_positions=frozenset({2}),
            )
            self.assertEqual(self._invoke(*case[:3]), 0)

    def test_required_universe_and_decision_bindings_fail_closed(self) -> None:
        universe_cases = (
            ("increment_008_version", "999"),
            ("increment_008_contract", "unexpected-contract"),
            ("phase", "PHASE_3"),
            ("stage", "unexpected-stage"),
        )
        for key, value in universe_cases:
            with self.subTest(artifact="universe", key=key):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(Path(temporary_directory))
                    universe_binding = case[3]["binding"]
                    self.assertIsInstance(universe_binding, dict)
                    universe_binding[key] = value
                    changed_sha256 = self._write_json(case[0], case[3])
                    decision_binding = case[4]["binding"]
                    self.assertIsInstance(decision_binding, dict)
                    decision_binding["input_stage_a_universe_sha256"] = (
                        changed_sha256
                    )
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(
                        self._invoke(case[0], changed_sha256, case[2]),
                        0,
                    )

        decision_cases = (
            ("increment_008_version", "999"),
            ("increment_008_contract", "unexpected-contract"),
            ("phase", "PHASE_3"),
            ("stage", "unexpected-stage"),
            ("input_stage_a_universe_sha256", "0" * 64),
            ("input_stage_a_universe_entry_count", 999),
            ("review_contract_git_revision", "0" * 40),
            ("reviewer_role", "INDEPENDENT_REVIEWER"),
        )
        for key, value in decision_cases:
            with self.subTest(artifact="decisions", key=key):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(Path(temporary_directory))
                    binding = case[4]["binding"]
                    self.assertIsInstance(binding, dict)
                    binding[key] = value
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_batch_boundary_and_reviewed_count_mismatches_fail(self) -> None:
        for mutation in ("start", "end", "reviewed_count"):
            with self.subTest(mutation=mutation):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(Path(temporary_directory))
                    batch = case[4]["batches"][0]
                    if mutation == "start":
                        batch["start_position"] = 2
                    elif mutation == "end":
                        batch["end_position"] = 2
                    else:
                        batch["reviewed_entry_count"] = 2
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_batches_must_be_a_contiguous_completed_prefix(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(
                Path(temporary_directory),
                size=205,
                reviewed_count=200,
            )
            batches = case[4]["batches"]
            self.assertIsInstance(batches, list)
            del batches[0]
            self._rewrite_decisions(case[2], case[4])
            self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_duplicate_decision_identity_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(Path(temporary_directory))
            decisions = case[4]["batches"][0]["decisions"]
            decisions[1] = dict(decisions[0])
            self._rewrite_decisions(case[2], case[4])
            self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_identity_mismatch_diagnostic_never_leaks_lexical_values(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(Path(temporary_directory))
            original_secret = case[4]["batches"][0]["decisions"][0]["value"]
            mismatched_secret = "SYNTHETIC-MISMATCH-SECRET-DO-NOT-ECHO"
            case[4]["batches"][0]["decisions"][0]["value"] = mismatched_secret
            self._rewrite_decisions(case[2], case[4])
            return_code, diagnostics = self._invoke_captured(*case[:3])
            self.assertNotEqual(return_code, 0)
            self.assertIn("identity mismatch", diagnostics)
            self.assertNotIn(original_secret, diagnostics)
            self.assertNotIn(mismatched_secret, diagnostics)

    def test_allowed_decisions_and_candidate_rationale_are_enforced(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            valid = self._write_case(
                Path(temporary_directory),
                candidate_positions=frozenset({1}),
            )
            self.assertEqual(self._invoke(*valid[:3]), 0)

        for mutation in ("unknown_decision", "missing_rationale"):
            with self.subTest(mutation=mutation):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(
                        Path(temporary_directory),
                        candidate_positions=frozenset({1}),
                    )
                    decision = case[4]["batches"][0]["decisions"][0]
                    if mutation == "unknown_decision":
                        decision["decision"] = "UNKNOWN_DECISION"
                    else:
                        del decision["rationale"]
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_valid_amendment_reconstructs_effective_summary(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(Path(temporary_directory))
            original = case[4]["batches"][0]["decisions"][0]
            self.assertEqual(original["decision"], NO_FLAG)
            case[4]["amendments"].append(self._valid_amendment(case[3]))
            summary = case[4]["summary"]
            summary["no_phase_2_flag_count"] -= 1
            summary["exploratory_sentinel_candidate_count"] += 1
            self._rewrite_decisions(case[2], case[4])
            self.assertEqual(self._invoke(*case[:3]), 0)
            self.assertEqual(original["decision"], NO_FLAG)

    def test_invalid_amendment_transitions_fail(self) -> None:
        for mutation in (
            "previous_mismatch",
            "no_op",
            "unreviewed_identity",
        ):
            with self.subTest(mutation=mutation):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(
                        Path(temporary_directory),
                        size=105,
                        reviewed_count=100,
                    )
                    amendment = self._valid_amendment(case[3])
                    if mutation == "previous_mismatch":
                        amendment["previous_decision"] = CANDIDATE
                    elif mutation == "no_op":
                        amendment["new_decision"] = NO_FLAG
                        amendment.pop("rationale")
                    else:
                        unreviewed = case[3]["entries"][104]
                        amendment["field"] = unreviewed["field"]
                        amendment["value"] = unreviewed["value"]
                    case[4]["amendments"].append(amendment)
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_amendments_must_remain_in_chronological_order(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(Path(temporary_directory))
            first = self._valid_amendment(case[3])
            second = {
                "amended_at_utc": "2026-09-18T18:30:00+00:00",
                "field": first["field"],
                "new_decision": NO_FLAG,
                "previous_decision": CANDIDATE,
                "reason": SYNTHETIC_AMENDMENT_REASON_SECRET,
                "reviewer_role": "PROJECT_RESEARCHER",
                "value": first["value"],
            }
            case[4]["amendments"].extend((first, second))
            self._rewrite_decisions(case[2], case[4])
            self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_summary_accounting_mismatches_fail(self) -> None:
        for key in (
            "entries_reviewed",
            "no_phase_2_flag_count",
            "batches_completed",
        ):
            with self.subTest(key=key):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(Path(temporary_directory))
                    case[4]["summary"][key] += 1
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_review_status_logic_and_cross_section_agreement(self) -> None:
        cases = (
            (105, 100, "COMPLETE_PENDING_RECONCILIATION", True),
            (3, 3, "IN_PROGRESS", True),
            (3, 3, "IN_PROGRESS", False),
        )
        for size, reviewed, status, change_summary in cases:
            with self.subTest(
                size=size,
                reviewed=reviewed,
                change_summary=change_summary,
            ):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(
                        Path(temporary_directory),
                        size=size,
                        reviewed_count=reviewed,
                    )
                    case[4]["review"]["review_status"] = status
                    if change_summary:
                        case[4]["summary"]["review_status"] = status
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_count_blinding_and_phase3_structures_are_rejected(self) -> None:
        mutations = (
            ("decision", "row_count"),
            ("review", "row_percentage"),
            ("summary", "materiality"),
            ("top", "phase3"),
        )
        for location, key in mutations:
            with self.subTest(location=location, key=key):
                with TemporaryDirectory() as temporary_directory:
                    case = self._write_case(Path(temporary_directory))
                    if location == "decision":
                        target = case[4]["batches"][0]["decisions"][0]
                    elif location == "top":
                        target = case[4]
                    else:
                        target = case[4][location]
                    target[key] = 1
                    self._rewrite_decisions(case[2], case[4])
                    self.assertNotEqual(self._invoke(*case[:3]), 0)

    def test_success_output_contains_only_safe_aggregate_evidence(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            case = self._write_case(
                Path(temporary_directory),
                candidate_positions=frozenset({1}),
            )
            return_code, output = self._invoke_captured(*case[:3])
            self.assertEqual(return_code, 0)
            self.assertIn("VALIDATION=PASS", output)
            self.assertIn("entries_reviewed=3", output)
            self.assertIn("batches_completed=1", output)
            for forbidden in (
                "SYNTHETIC-LEXICAL-SECRET",
                SYNTHETIC_RATIONALE_SECRET,
                SYNTHETIC_AMENDMENT_REASON_SECRET,
            ):
                self.assertNotIn(forbidden, output)


if __name__ == "__main__":
    unittest.main()

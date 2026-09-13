import unittest

from support_operations_intelligence.calgary_adapter import (
    map_calgary_source_status,
)
from support_operations_intelligence.evidence import (
    DerivedEvidence,
    ObservedEvidence,
    SimulatedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)


class CalgarySourceStatusTests(unittest.TestCase):
    def test_missing_status_description_is_value_absent(self):
        result = map_calgary_source_status({})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_none_status_description_is_value_absent(self):
        result = map_calgary_source_status({"status_description": None})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_non_string_status_description_is_evidence_indeterminate(self):
        result = map_calgary_source_status({"status_description": 123})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE),
        )

    def test_empty_status_description_is_value_absent(self):
        result = map_calgary_source_status({"status_description": ""})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_spaces_only_status_description_is_value_absent(self):
        result = map_calgary_source_status({"status_description": "   "})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_other_whitespace_only_status_description_is_value_absent(self):
        result = map_calgary_source_status({"status_description": "\t\n"})

        self.assertEqual(
            result,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_ordinary_status_description_is_observed(self):
        result = map_calgary_source_status({"status_description": "Closed"})

        self.assertEqual(result, ObservedEvidence("Closed"))

    def test_status_description_with_punctuation_is_preserved_exactly(self):
        value = "Duplicate (Closed)"

        result = map_calgary_source_status({"status_description": value})

        self.assertEqual(result, ObservedEvidence(value))

    def test_padded_nonblank_status_description_is_preserved_exactly(self):
        value = " Closed "

        result = map_calgary_source_status({"status_description": value})

        self.assertEqual(result, ObservedEvidence(value))

    def test_unknown_nonblank_status_description_is_observed_exactly(self):
        value = "Future Native Status"

        result = map_calgary_source_status({"status_description": value})

        self.assertEqual(result, ObservedEvidence(value))

    def test_input_mapping_is_not_mutated(self):
        record = {
            "status_description": " Closed ",
            "other_field": "unchanged",
        }
        before = dict(record)

        map_calgary_source_status(record)

        self.assertEqual(record, before)

    def test_results_are_never_derived_or_simulated(self):
        records = [
            {},
            {"status_description": None},
            {"status_description": 123},
            {"status_description": "Closed"},
        ]

        for record in records:
            with self.subTest(record=record):
                result = map_calgary_source_status(record)
                self.assertIsInstance(
                    result,
                    (ObservedEvidence, UnavailableEvidence),
                )
                self.assertNotIsInstance(
                    result,
                    (DerivedEvidence, SimulatedEvidence),
                )


if __name__ == "__main__":
    unittest.main()

import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass

from support_operations_intelligence.case import Case
from support_operations_intelligence.identity import CaseId


class CaseTests(unittest.TestCase):
    def test_case_is_dataclass(self):
        self.assertTrue(is_dataclass(Case))

    def test_case_is_frozen(self):
        self.assertTrue(Case.__dataclass_params__.frozen)

    def test_case_contains_exactly_case_id_field(self):
        self.assertEqual([field.name for field in fields(Case)], ["case_id"])

    def test_case_preserves_supplied_case_id_exactly(self):
        case_id = CaseId("city_of_calgary_311", "ABC-123")
        case = Case(case_id=case_id)

        self.assertEqual(case.case_id, case_id)
        self.assertIs(case.case_id, case_id)

    def test_source_system_is_accessible_through_case_id(self):
        case = Case(CaseId("city_of_calgary_311", "ABC-123"))

        self.assertEqual(case.case_id.source_system, "city_of_calgary_311")

    def test_source_case_id_is_accessible_through_case_id(self):
        case = Case(CaseId("city_of_calgary_311", "ABC-123"))

        self.assertEqual(case.case_id.source_case_id, "ABC-123")

    def test_case_has_no_duplicate_source_system_field(self):
        self.assertNotIn("source_system", [field.name for field in fields(Case)])

    def test_case_has_no_duplicate_source_case_id_field(self):
        self.assertNotIn("source_case_id", [field.name for field in fields(Case)])

    def test_case_has_no_source_status_field(self):
        self.assertNotIn("source_status", [field.name for field in fields(Case)])

    def test_case_has_no_created_at_field(self):
        self.assertNotIn("created_at", [field.name for field in fields(Case)])

    def test_case_has_no_canonical_status_field(self):
        self.assertNotIn("canonical_status", [field.name for field in fields(Case)])

    def test_case_id_mutation_is_rejected(self):
        case = Case(CaseId("city_of_calgary_311", "ABC-123"))

        with self.assertRaises(FrozenInstanceError):
            case.case_id = CaseId("city_of_calgary_311", "changed")


if __name__ == "__main__":
    unittest.main()

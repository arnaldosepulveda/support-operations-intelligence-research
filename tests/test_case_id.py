import unittest
from dataclasses import FrozenInstanceError, fields

from support_operations_intelligence.identity import CaseId


class CaseIdTests(unittest.TestCase):
    def test_same_exact_identity_components_compare_equal(self):
        first = CaseId("city_of_calgary_311", "123")
        second = CaseId("city_of_calgary_311", "123")

        self.assertEqual(first, second)

    def test_different_source_system_values_compare_unequal(self):
        first = CaseId("city_of_calgary_311", "123")
        second = CaseId("another_source", "123")

        self.assertNotEqual(first, second)

    def test_different_source_case_id_values_compare_unequal(self):
        first = CaseId("city_of_calgary_311", "123")
        second = CaseId("city_of_calgary_311", "456")

        self.assertNotEqual(first, second)

    def test_source_case_id_lexical_content_is_preserved_exactly(self):
        case_id = CaseId("city_of_calgary_311", " 001AbC-09 ")

        self.assertEqual(case_id.source_case_id, " 001AbC-09 ")

    def test_dataclass_contains_exactly_the_committed_fields(self):
        self.assertEqual(
            [field.name for field in fields(CaseId)],
            ["source_system", "source_case_id"],
        )

    def test_ordinary_field_mutation_is_rejected(self):
        case_id = CaseId("city_of_calgary_311", "123")

        with self.assertRaises(FrozenInstanceError):
            case_id.source_case_id = "456"


if __name__ == "__main__":
    unittest.main()

import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass

from support_operations_intelligence.calgary_adapter import CalgaryMappedCase
from support_operations_intelligence.case import Case
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import CaseId


class CalgaryMappedCaseTests(unittest.TestCase):
    def test_calgary_mapped_case_is_dataclass(self):
        self.assertTrue(is_dataclass(CalgaryMappedCase))

    def test_calgary_mapped_case_is_frozen(self):
        self.assertTrue(CalgaryMappedCase.__dataclass_params__.frozen)

    def test_calgary_mapped_case_has_exact_fields(self):
        self.assertEqual(
            [field.name for field in fields(CalgaryMappedCase)],
            ["case", "source_status"],
        )

    def test_case_object_is_preserved(self):
        case = Case(CaseId("city_of_calgary_311", "ABC-123"))

        mapped = CalgaryMappedCase(
            case=case,
            source_status=ObservedEvidence("Closed"),
        )

        self.assertIs(mapped.case, case)

    def test_observed_evidence_object_is_preserved(self):
        evidence = ObservedEvidence("Closed")

        mapped = CalgaryMappedCase(
            case=Case(CaseId("city_of_calgary_311", "ABC-123")),
            source_status=evidence,
        )

        self.assertIs(mapped.source_status, evidence)

    def test_unavailable_evidence_object_is_preserved(self):
        evidence = UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

        mapped = CalgaryMappedCase(
            case=Case(CaseId("city_of_calgary_311", "ABC-123")),
            source_status=evidence,
        )

        self.assertIs(mapped.source_status, evidence)

    def test_nested_case_identity_remains_accessible(self):
        mapped = CalgaryMappedCase(
            case=Case(CaseId("city_of_calgary_311", "ABC-123")),
            source_status=ObservedEvidence("Closed"),
        )

        self.assertEqual(
            mapped.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(mapped.case.case_id.source_case_id, "ABC-123")

    def test_calgary_mapped_case_has_no_created_at_field(self):
        self.assertNotIn(
            "created_at",
            [field.name for field in fields(CalgaryMappedCase)],
        )

    def test_calgary_mapped_case_has_no_canonical_status_field(self):
        self.assertNotIn(
            "canonical_status",
            [field.name for field in fields(CalgaryMappedCase)],
        )

    def test_calgary_mapped_case_has_no_source_native_fields(self):
        field_names = [field.name for field in fields(CalgaryMappedCase)]

        for excluded in (
            "source",
            "service_name",
            "agency_responsible",
            "updated_date",
            "closed_date",
        ):
            with self.subTest(field=excluded):
                self.assertNotIn(excluded, field_names)

    def test_calgary_mapped_case_has_no_dq13_fields(self):
        field_names = [field.name for field in fields(CalgaryMappedCase)]

        for excluded in (
            "address",
            "comm_code",
            "comm_name",
            "location_type",
            "longitude",
            "latitude",
            "point",
        ):
            with self.subTest(field=excluded):
                self.assertNotIn(excluded, field_names)

    def test_both_fields_reject_ordinary_reassignment(self):
        mapped = CalgaryMappedCase(
            case=Case(CaseId("city_of_calgary_311", "ABC-123")),
            source_status=ObservedEvidence("Closed"),
        )

        replacements = (
            ("case", Case(CaseId("city_of_calgary_311", "changed"))),
            ("source_status", ObservedEvidence("Open")),
        )

        for field_name, replacement in replacements:
            with self.subTest(field=field_name):
                with self.assertRaises(FrozenInstanceError):
                    setattr(mapped, field_name, replacement)


if __name__ == "__main__":
    unittest.main()

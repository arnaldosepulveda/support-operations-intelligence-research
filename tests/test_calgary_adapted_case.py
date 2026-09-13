import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass

from support_operations_intelligence.calgary_adapter import (
    CalgaryAdaptedCase,
    CalgaryMappedCase,
    CalgarySourceNativeEvidence,
)
from support_operations_intelligence.case import Case
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import CaseId


def _build_mapped_case():
    return CalgaryMappedCase(
        case=Case(CaseId("city_of_calgary_311", "ABC-123")),
        source_status=ObservedEvidence("Closed"),
    )


def _build_source_native():
    return CalgarySourceNativeEvidence(
        source=ObservedEvidence("Mobile App"),
        service_name=ObservedEvidence("Roads - Pothole"),
        agency_responsible=ObservedEvidence("Roads"),
        updated_date=ObservedEvidence("2026/09/08 03:14:15 PM"),
        closed_date=UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
    )


class CalgaryAdaptedCaseTests(unittest.TestCase):
    def test_calgary_adapted_case_is_dataclass(self):
        self.assertTrue(is_dataclass(CalgaryAdaptedCase))

    def test_calgary_adapted_case_is_frozen(self):
        adapted = CalgaryAdaptedCase(
            mapped_case=_build_mapped_case(),
            source_native=_build_source_native(),
        )

        with self.assertRaises(FrozenInstanceError):
            adapted.mapped_case = _build_mapped_case()

    def test_calgary_adapted_case_has_exact_fields(self):
        self.assertEqual(
            [field.name for field in fields(CalgaryAdaptedCase)],
            ["mapped_case", "source_native"],
        )

    def test_mapped_case_object_is_preserved(self):
        mapped_case = _build_mapped_case()

        adapted = CalgaryAdaptedCase(
            mapped_case=mapped_case,
            source_native=_build_source_native(),
        )

        self.assertIs(adapted.mapped_case, mapped_case)

    def test_source_native_object_is_preserved(self):
        source_native = _build_source_native()

        adapted = CalgaryAdaptedCase(
            mapped_case=_build_mapped_case(),
            source_native=source_native,
        )

        self.assertIs(adapted.source_native, source_native)

    def test_nested_canonical_identity_remains_accessible(self):
        adapted = CalgaryAdaptedCase(
            mapped_case=_build_mapped_case(),
            source_native=_build_source_native(),
        )

        self.assertEqual(
            adapted.mapped_case.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(
            adapted.mapped_case.case.case_id.source_case_id,
            "ABC-123",
        )

    def test_nested_source_status_remains_accessible(self):
        status = ObservedEvidence("Closed")
        mapped_case = CalgaryMappedCase(
            case=Case(CaseId("city_of_calgary_311", "ABC-123")),
            source_status=status,
        )

        adapted = CalgaryAdaptedCase(
            mapped_case=mapped_case,
            source_native=_build_source_native(),
        )

        self.assertIs(adapted.mapped_case.source_status, status)

    def test_all_five_source_native_fields_remain_accessible(self):
        source = ObservedEvidence("Mobile App")
        service_name = ObservedEvidence("Roads - Pothole")
        agency_responsible = ObservedEvidence("Roads")
        updated_date = ObservedEvidence("2026/09/08 03:14:15 PM")
        closed_date = UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

        source_native = CalgarySourceNativeEvidence(
            source=source,
            service_name=service_name,
            agency_responsible=agency_responsible,
            updated_date=updated_date,
            closed_date=closed_date,
        )

        adapted = CalgaryAdaptedCase(
            mapped_case=_build_mapped_case(),
            source_native=source_native,
        )

        self.assertIs(adapted.source_native.source, source)
        self.assertIs(adapted.source_native.service_name, service_name)
        self.assertIs(
            adapted.source_native.agency_responsible, agency_responsible
        )
        self.assertIs(adapted.source_native.updated_date, updated_date)
        self.assertIs(adapted.source_native.closed_date, closed_date)

    def test_calgary_adapted_case_has_no_created_at_field(self):
        self.assertNotIn(
            "created_at",
            [field.name for field in fields(CalgaryAdaptedCase)],
        )

    def test_calgary_adapted_case_has_no_canonical_status_field(self):
        self.assertNotIn(
            "canonical_status",
            [field.name for field in fields(CalgaryAdaptedCase)],
        )

    def test_calgary_adapted_case_has_no_dq13_fields(self):
        field_names = [field.name for field in fields(CalgaryAdaptedCase)]

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

    def test_both_top_level_fields_reject_ordinary_reassignment(self):
        adapted = CalgaryAdaptedCase(
            mapped_case=_build_mapped_case(),
            source_native=_build_source_native(),
        )

        replacements = (
            ("mapped_case", _build_mapped_case()),
            ("source_native", _build_source_native()),
        )

        for field_name, replacement in replacements:
            with self.subTest(field=field_name):
                with self.assertRaises(FrozenInstanceError):
                    setattr(adapted, field_name, replacement)


if __name__ == "__main__":
    unittest.main()

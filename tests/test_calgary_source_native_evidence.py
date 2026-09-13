import datetime
import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass

from support_operations_intelligence.calgary_adapter import (
    CalgarySourceNativeEvidence,
    map_calgary_source_native_evidence,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)

SOURCE_NATIVE_FIELDS = (
    "source",
    "service_name",
    "agency_responsible",
    "updated_date",
    "closed_date",
)


def _valid_record():
    return {
        "source": "Mobile App",
        "service_name": "Roads - Pothole",
        "agency_responsible": "Roads",
        "updated_date": "2026/09/08 03:14:15 PM",
        "closed_date": "2026/09/09 08:02:01 AM",
    }


class CalgarySourceNativeEvidenceTests(unittest.TestCase):
    def test_container_is_frozen_dataclass_with_exact_field_order(self):
        self.assertTrue(is_dataclass(CalgarySourceNativeEvidence))
        self.assertTrue(
            CalgarySourceNativeEvidence.__dataclass_params__.frozen
        )
        self.assertEqual(
            [field.name for field in fields(CalgarySourceNativeEvidence)],
            list(SOURCE_NATIVE_FIELDS),
        )

        evidence = CalgarySourceNativeEvidence(
            source=ObservedEvidence("Mobile App"),
            service_name=ObservedEvidence("Roads - Pothole"),
            agency_responsible=ObservedEvidence("Roads"),
            updated_date=ObservedEvidence("2026/09/08 03:14:15 PM"),
            closed_date=ObservedEvidence("2026/09/09 08:02:01 AM"),
        )

        with self.assertRaises(FrozenInstanceError):
            evidence.source = ObservedEvidence("changed")

    def test_all_five_nonblank_values_are_preserved(self):
        result = map_calgary_source_native_evidence(_valid_record())

        self.assertEqual(result.source, ObservedEvidence("Mobile App"))
        self.assertEqual(
            result.service_name, ObservedEvidence("Roads - Pothole")
        )
        self.assertEqual(
            result.agency_responsible, ObservedEvidence("Roads")
        )
        self.assertEqual(
            result.updated_date,
            ObservedEvidence("2026/09/08 03:14:15 PM"),
        )
        self.assertEqual(
            result.closed_date,
            ObservedEvidence("2026/09/09 08:02:01 AM"),
        )

    def test_padded_non_temporal_values_are_preserved_exactly(self):
        record = {
            "source": "  Mobile App  ",
            "service_name": "  Roads - Pothole  ",
            "agency_responsible": "  Roads  ",
        }

        result = map_calgary_source_native_evidence(record)

        self.assertEqual(result.source, ObservedEvidence("  Mobile App  "))
        self.assertEqual(
            result.service_name,
            ObservedEvidence("  Roads - Pothole  "),
        )
        self.assertEqual(
            result.agency_responsible, ObservedEvidence("  Roads  ")
        )

    def test_temporal_lexical_values_are_preserved_exactly(self):
        record = {
            "updated_date": "  2026/09/08 03:14:15 PM  ",
            "closed_date": "2026-09-09T08:02:01",
        }

        result = map_calgary_source_native_evidence(record)

        self.assertEqual(
            result.updated_date,
            ObservedEvidence("  2026/09/08 03:14:15 PM  "),
        )
        self.assertEqual(
            result.closed_date,
            ObservedEvidence("2026-09-09T08:02:01"),
        )

    def test_missing_field_produces_value_absent_for_all_five(self):
        for field_name in SOURCE_NATIVE_FIELDS:
            with self.subTest(field=field_name):
                record = _valid_record()
                del record[field_name]

                result = map_calgary_source_native_evidence(record)

                self.assertEqual(
                    getattr(result, field_name),
                    UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
                )

    def test_none_produces_value_absent_for_all_five(self):
        for field_name in SOURCE_NATIVE_FIELDS:
            with self.subTest(field=field_name):
                record = _valid_record()
                record[field_name] = None

                result = map_calgary_source_native_evidence(record)

                self.assertEqual(
                    getattr(result, field_name),
                    UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
                )

    def test_empty_string_produces_value_absent_for_all_five(self):
        for field_name in SOURCE_NATIVE_FIELDS:
            with self.subTest(field=field_name):
                record = _valid_record()
                record[field_name] = ""

                result = map_calgary_source_native_evidence(record)

                self.assertEqual(
                    getattr(result, field_name),
                    UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
                )

    def test_whitespace_only_produces_value_absent_for_all_five(self):
        for field_name in SOURCE_NATIVE_FIELDS:
            with self.subTest(field=field_name):
                record = _valid_record()
                record[field_name] = "   "

                result = map_calgary_source_native_evidence(record)

                self.assertEqual(
                    getattr(result, field_name),
                    UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
                )

    def test_non_string_produces_evidence_indeterminate_for_all_five(self):
        for field_name in SOURCE_NATIVE_FIELDS:
            with self.subTest(field=field_name):
                record = _valid_record()
                record[field_name] = 123

                result = map_calgary_source_native_evidence(record)

                self.assertEqual(
                    getattr(result, field_name),
                    UnavailableEvidence(
                        UnavailableReason.EVIDENCE_INDETERMINATE
                    ),
                )

    def test_non_string_temporal_objects_are_not_serialized(self):
        record = _valid_record()
        record["updated_date"] = datetime.datetime(2026, 9, 8, 15, 14, 15)
        record["closed_date"] = datetime.date(2026, 9, 9)

        result = map_calgary_source_native_evidence(record)

        self.assertEqual(
            result.updated_date,
            UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE),
        )
        self.assertEqual(
            result.closed_date,
            UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE),
        )
        self.assertNotIsInstance(result.updated_date, ObservedEvidence)
        self.assertNotIsInstance(result.closed_date, ObservedEvidence)

    def test_input_mapping_is_not_mutated(self):
        record = _valid_record()
        before = dict(record)

        map_calgary_source_native_evidence(record)

        self.assertEqual(record, before)

    def test_output_fields_are_exactly_dq7_dq11(self):
        result = map_calgary_source_native_evidence(_valid_record())

        self.assertEqual(
            [field.name for field in fields(result)],
            list(SOURCE_NATIVE_FIELDS),
        )

        for excluded in (
            "service_request_id",
            "status_description",
            "created_at",
            "canonical_status",
            "address",
            "comm_code",
            "comm_name",
            "location_type",
            "longitude",
            "latitude",
            "point",
        ):
            with self.subTest(field=excluded):
                self.assertFalse(hasattr(result, excluded))


if __name__ == "__main__":
    unittest.main()

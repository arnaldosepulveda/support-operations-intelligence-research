import unittest
from unittest.mock import patch

from support_operations_intelligence.calgary_adapter import (
    CalgaryAdaptedCase,
    CalgaryAdapterResult,
    CalgaryMappedCase,
    CalgarySourceNativeEvidence,
    adapt_calgary_record,
)
from support_operations_intelligence.evidence import (
    ObservedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)
from support_operations_intelligence.identity import (
    IdentityRejectionReason,
    RejectedIdentity,
)


def _valid_record():
    return {
        "service_request_id": " 001AbC-09 ",
        "status_description": " Closed ",
        "source": " Mobile App ",
        "service_name": " Roads - Pothole ",
        "agency_responsible": " Roads ",
        "updated_date": "2026/09/08 03:14:15 PM",
        "closed_date": "2026/09/09 08:02:01 AM",
    }


class CalgaryRecordAdapterTests(unittest.TestCase):
    def test_valid_record_returns_calgary_adapted_case(self):
        result = adapt_calgary_record(_valid_record())

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            result.mapped_case.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(
            result.source_native.source,
            ObservedEvidence(" Mobile App "),
        )

    def test_mapped_case_is_structurally_bound(self):
        result = adapt_calgary_record(_valid_record())

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertIsInstance(result.mapped_case, CalgaryMappedCase)
        self.assertEqual(
            result.mapped_case.case.case_id.source_case_id,
            " 001AbC-09 ",
        )

    def test_all_dq7_dq11_evidence_is_present(self):
        result = adapt_calgary_record(_valid_record())

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            result.source_native.source, ObservedEvidence(" Mobile App ")
        )
        self.assertEqual(
            result.source_native.service_name,
            ObservedEvidence(" Roads - Pothole "),
        )
        self.assertEqual(
            result.source_native.agency_responsible,
            ObservedEvidence(" Roads "),
        )
        self.assertEqual(
            result.source_native.updated_date,
            ObservedEvidence("2026/09/08 03:14:15 PM"),
        )
        self.assertEqual(
            result.source_native.closed_date,
            ObservedEvidence("2026/09/09 08:02:01 AM"),
        )

    def test_invalid_identity_returns_rejected_identity(self):
        result = adapt_calgary_record(
            {"status_description": "Closed", "source": "Mobile App"}
        )

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )
        self.assertNotIsInstance(result, CalgaryAdaptedCase)

    def test_identity_rejection_short_circuits_source_native_mapping(self):
        with patch(
            "support_operations_intelligence.calgary_adapter."
            "map_calgary_source_native_evidence"
        ) as source_native_mapper:
            result = adapt_calgary_record({"status_description": "Closed"})

        self.assertIsInstance(result, RejectedIdentity)
        source_native_mapper.assert_not_called()

    def test_exact_rejected_identity_object_is_reused(self):
        rejection = RejectedIdentity(
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID
        )

        with patch(
            "support_operations_intelligence.calgary_adapter."
            "map_calgary_case",
            return_value=rejection,
        ), patch(
            "support_operations_intelligence.calgary_adapter."
            "map_calgary_source_native_evidence"
        ) as source_native_mapper:
            result = adapt_calgary_record({"service_request_id": "ABC-123"})

        self.assertIs(result, rejection)
        source_native_mapper.assert_not_called()

    def test_source_native_value_absent_does_not_reject(self):
        record = {
            "service_request_id": "ABC-123",
            "status_description": "Closed",
        }

        result = adapt_calgary_record(record)

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            result.source_native.source,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )
        self.assertEqual(
            result.source_native.service_name,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_source_native_evidence_indeterminate_does_not_reject(self):
        record = {
            "service_request_id": "ABC-123",
            "status_description": "Closed",
            "source": 123,
        }

        result = adapt_calgary_record(record)

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            result.source_native.source,
            UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE),
        )

    def test_raw_source_does_not_alter_canonical_source_system(self):
        record = {
            "service_request_id": "ABC-123",
            "status_description": "Closed",
            "source": "Mobile App",
        }

        result = adapt_calgary_record(record)

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            result.mapped_case.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(result.source_native.source.value, "Mobile App")

    def test_input_mapping_is_not_mutated(self):
        record = _valid_record()
        before = dict(record)

        adapt_calgary_record(record)

        self.assertEqual(record, before)

    def test_unexpected_source_native_mapping_failure_propagates(self):
        with patch(
            "support_operations_intelligence.calgary_adapter."
            "map_calgary_source_native_evidence",
            side_effect=RuntimeError("synthetic unexpected failure"),
        ):
            with self.assertRaises(RuntimeError):
                adapt_calgary_record(_valid_record())

    def test_dq13_does_not_enter_adapted_output(self):
        record = dict(_valid_record())
        record.update(
            {
                "address": "123 Main St",
                "comm_code": "DNTN",
                "comm_name": "Downtown",
                "location_type": "Address",
                "longitude": -114.0,
                "latitude": 51.0,
                "point": "POINT (-114.0 51.0)",
            }
        )

        result = adapt_calgary_record(record)

        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertEqual(
            list(result.__dataclass_fields__.keys()),
            ["mapped_case", "source_native"],
        )
        self.assertEqual(
            list(result.source_native.__dataclass_fields__.keys()),
            [
                "source",
                "service_name",
                "agency_responsible",
                "updated_date",
                "closed_date",
            ],
        )


if __name__ == "__main__":
    unittest.main()

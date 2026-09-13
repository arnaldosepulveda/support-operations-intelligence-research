import unittest
from unittest.mock import patch

from support_operations_intelligence.calgary_adapter import (
    CalgaryMappedCase,
    map_calgary_case,
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


class CalgaryCaseMappingTests(unittest.TestCase):
    def test_valid_identity_and_observed_status_returns_mapped_case(self):
        result = map_calgary_case(
            {
                "service_request_id": "ABC-123",
                "status_description": "Closed",
            }
        )

        self.assertIsInstance(result, CalgaryMappedCase)
        self.assertEqual(
            result.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(result.case.case_id.source_case_id, "ABC-123")
        self.assertEqual(result.source_status, ObservedEvidence("Closed"))

    def test_lexical_source_case_id_is_preserved(self):
        result = map_calgary_case(
            {
                "service_request_id": " 001AbC-09 ",
                "status_description": "Closed",
            }
        )

        self.assertIsInstance(result, CalgaryMappedCase)
        self.assertEqual(
            result.case.case_id.source_case_id,
            " 001AbC-09 ",
        )

    def test_fixed_source_system_is_preserved(self):
        result = map_calgary_case(
            {
                "service_request_id": "ABC-123",
                "status_description": "Closed",
                "source": "Mobile App",
            }
        )

        self.assertIsInstance(result, CalgaryMappedCase)
        self.assertEqual(
            result.case.case_id.source_system,
            "city_of_calgary_311",
        )

    def test_valid_identity_and_missing_status_returns_mapped_case(self):
        result = map_calgary_case({"service_request_id": "ABC-123"})

        self.assertIsInstance(result, CalgaryMappedCase)
        self.assertEqual(
            result.source_status,
            UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
        )

    def test_valid_identity_and_non_string_status_returns_mapped_case(self):
        result = map_calgary_case(
            {
                "service_request_id": "ABC-123",
                "status_description": 123,
            }
        )

        self.assertIsInstance(result, CalgaryMappedCase)
        self.assertEqual(
            result.source_status,
            UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE),
        )

    def test_missing_service_request_id_is_rejected(self):
        result = map_calgary_case({})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )

    def test_null_service_request_id_is_rejected(self):
        result = map_calgary_case({"service_request_id": None})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.NULL_SOURCE_CASE_ID,
        )

    def test_non_string_service_request_id_is_rejected(self):
        result = map_calgary_case({"service_request_id": 123})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.NON_STRING_SOURCE_CASE_ID,
        )

    def test_empty_service_request_id_is_rejected(self):
        result = map_calgary_case({"service_request_id": ""})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.EMPTY_SOURCE_CASE_ID,
        )

    def test_whitespace_only_service_request_id_is_rejected(self):
        result = map_calgary_case({"service_request_id": "   "})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.WHITESPACE_ONLY_SOURCE_CASE_ID,
        )

    def test_input_mapping_is_not_mutated(self):
        record = {
            "service_request_id": "ABC-123",
            "status_description": " Closed ",
            "source": "Mobile App",
        }
        before = dict(record)

        map_calgary_case(record)

        self.assertEqual(record, before)

    def test_identity_rejection_short_circuits_status_mapping(self):
        with patch(
            "support_operations_intelligence.calgary_adapter."
            "map_calgary_source_status"
        ) as status_mapper:
            result = map_calgary_case({"status_description": "Closed"})

        self.assertIsInstance(result, RejectedIdentity)
        status_mapper.assert_not_called()


if __name__ == "__main__":
    unittest.main()

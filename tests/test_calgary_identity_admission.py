import unittest

from support_operations_intelligence.identity import (
    AcceptedIdentity,
    CaseId,
    IdentityRejectionReason,
    RejectedIdentity,
    admit_calgary_source_identity,
)


class CalgaryIdentityAdmissionTests(unittest.TestCase):
    def test_missing_service_request_id_is_rejected(self):
        result = admit_calgary_source_identity({})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
        )

    def test_none_service_request_id_is_rejected(self):
        result = admit_calgary_source_identity({"service_request_id": None})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(result.reason, IdentityRejectionReason.NULL_SOURCE_CASE_ID)

    def test_non_string_service_request_id_is_rejected_without_coercion(self):
        result = admit_calgary_source_identity({"service_request_id": 123})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.NON_STRING_SOURCE_CASE_ID,
        )
        self.assertFalse(hasattr(result, "case_id"))

    def test_empty_service_request_id_is_rejected(self):
        result = admit_calgary_source_identity({"service_request_id": ""})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(result.reason, IdentityRejectionReason.EMPTY_SOURCE_CASE_ID)

    def test_spaces_only_service_request_id_is_rejected(self):
        result = admit_calgary_source_identity({"service_request_id": "   "})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.WHITESPACE_ONLY_SOURCE_CASE_ID,
        )

    def test_other_whitespace_only_service_request_id_is_rejected(self):
        result = admit_calgary_source_identity({"service_request_id": "\t\n"})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertIs(
            result.reason,
            IdentityRejectionReason.WHITESPACE_ONLY_SOURCE_CASE_ID,
        )

    def test_ordinary_valid_identity_is_accepted(self):
        result = admit_calgary_source_identity(
            {"service_request_id": "ABC-123"}
        )

        self.assertIsInstance(result, AcceptedIdentity)
        self.assertEqual(
            result.case_id,
            CaseId(
                source_system="city_of_calgary_311",
                source_case_id="ABC-123",
            ),
        )

    def test_padded_nonblank_identity_is_preserved_exactly(self):
        result = admit_calgary_source_identity(
            {"service_request_id": " 001AbC-09 "}
        )

        self.assertIsInstance(result, AcceptedIdentity)
        self.assertEqual(result.case_id.source_case_id, " 001AbC-09 ")

    def test_accepted_identity_uses_fixed_calgary_namespace(self):
        result = admit_calgary_source_identity(
            {"service_request_id": "ABC-123"}
        )

        self.assertIsInstance(result, AcceptedIdentity)
        self.assertEqual(result.case_id.source_system, "city_of_calgary_311")

    def test_raw_source_cannot_override_fixed_namespace(self):
        result = admit_calgary_source_identity(
            {
                "service_request_id": "ABC-123",
                "source": "Phone",
            }
        )

        self.assertIsInstance(result, AcceptedIdentity)
        self.assertEqual(result.case_id.source_system, "city_of_calgary_311")

    def test_input_mapping_is_not_mutated(self):
        record = {
            "service_request_id": "ABC-123",
            "source": "Phone",
        }
        before = dict(record)

        admit_calgary_source_identity(record)

        self.assertEqual(record, before)

    def test_rejected_outcome_has_no_case_id(self):
        result = admit_calgary_source_identity({})

        self.assertIsInstance(result, RejectedIdentity)
        self.assertFalse(hasattr(result, "case_id"))


if __name__ == "__main__":
    unittest.main()

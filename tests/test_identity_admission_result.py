import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass

from support_operations_intelligence.identity import (
    AcceptedIdentity,
    CaseId,
    IdentityRejectionReason,
    RejectedIdentity,
)


class IdentityAdmissionResultTests(unittest.TestCase):
    def test_rejection_reason_contains_exactly_the_committed_members(self):
        self.assertEqual(
            list(IdentityRejectionReason.__members__),
            [
                "MISSING_SOURCE_CASE_ID",
                "NULL_SOURCE_CASE_ID",
                "NON_STRING_SOURCE_CASE_ID",
                "EMPTY_SOURCE_CASE_ID",
                "WHITESPACE_ONLY_SOURCE_CASE_ID",
            ],
        )

    def test_rejection_reason_values_match_their_names(self):
        self.assertEqual(
            [reason.value for reason in IdentityRejectionReason],
            [reason.name for reason in IdentityRejectionReason],
        )

    def test_accepted_identity_is_dataclass_with_only_case_id_field(self):
        self.assertTrue(is_dataclass(AcceptedIdentity))
        self.assertEqual([field.name for field in fields(AcceptedIdentity)], ["case_id"])

    def test_rejected_identity_is_dataclass_with_only_reason_field(self):
        self.assertTrue(is_dataclass(RejectedIdentity))
        self.assertEqual([field.name for field in fields(RejectedIdentity)], ["reason"])

    def test_accepted_identity_preserves_supplied_case_id(self):
        case_id = CaseId("city_of_calgary_311", "ABC-123")

        self.assertIs(AcceptedIdentity(case_id=case_id).case_id, case_id)

    def test_rejected_identity_preserves_supplied_reason(self):
        reason = IdentityRejectionReason.EMPTY_SOURCE_CASE_ID

        self.assertIs(RejectedIdentity(reason=reason).reason, reason)

    def test_accepted_identity_rejects_ordinary_mutation(self):
        accepted = AcceptedIdentity(CaseId("city_of_calgary_311", "ABC-123"))

        with self.assertRaises(FrozenInstanceError):
            accepted.case_id = CaseId("city_of_calgary_311", "changed")

    def test_rejected_identity_rejects_ordinary_mutation(self):
        rejected = RejectedIdentity(IdentityRejectionReason.EMPTY_SOURCE_CASE_ID)

        with self.assertRaises(FrozenInstanceError):
            rejected.reason = IdentityRejectionReason.NULL_SOURCE_CASE_ID

    def test_rejected_identity_has_no_case_id_dataclass_field(self):
        self.assertNotIn("case_id", [field.name for field in fields(RejectedIdentity)])

    def test_accepted_identity_has_no_reason_dataclass_field(self):
        self.assertNotIn("reason", [field.name for field in fields(AcceptedIdentity)])


if __name__ == "__main__":
    unittest.main()

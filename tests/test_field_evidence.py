import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass
from typing import get_args, get_origin

from support_operations_intelligence.evidence import (
    DerivedEvidence,
    FieldEvidence,
    ObservedEvidence,
    SimulatedEvidence,
    UnavailableEvidence,
    UnavailableReason,
)


class FieldEvidenceTests(unittest.TestCase):
    def test_unavailable_reason_contains_exactly_the_canonical_members(self):
        self.assertEqual(
            list(UnavailableReason.__members__),
            [
                "VALUE_ABSENT",
                "CONCEPT_ABSENT",
                "EVIDENCE_INDETERMINATE",
                "TRANSFORMATION_NOT_APPLIED",
                "TRANSFORMATION_UNRESOLVED",
            ],
        )

    def test_unavailable_reason_values_match_their_names(self):
        self.assertEqual(
            [reason.value for reason in UnavailableReason],
            [reason.name for reason in UnavailableReason],
        )

    def test_observed_evidence_is_frozen_dataclass_with_only_value(self):
        self.assertTrue(is_dataclass(ObservedEvidence))
        self.assertTrue(ObservedEvidence.__dataclass_params__.frozen)
        self.assertEqual([field.name for field in fields(ObservedEvidence)], ["value"])

    def test_derived_evidence_is_frozen_dataclass_with_only_value(self):
        self.assertTrue(is_dataclass(DerivedEvidence))
        self.assertTrue(DerivedEvidence.__dataclass_params__.frozen)
        self.assertEqual([field.name for field in fields(DerivedEvidence)], ["value"])

    def test_simulated_evidence_is_frozen_dataclass_with_only_value(self):
        self.assertTrue(is_dataclass(SimulatedEvidence))
        self.assertTrue(SimulatedEvidence.__dataclass_params__.frozen)
        self.assertEqual([field.name for field in fields(SimulatedEvidence)], ["value"])

    def test_unavailable_evidence_is_frozen_dataclass_with_only_reason(self):
        self.assertTrue(is_dataclass(UnavailableEvidence))
        self.assertTrue(UnavailableEvidence.__dataclass_params__.frozen)
        self.assertEqual(
            [field.name for field in fields(UnavailableEvidence)],
            ["reason"],
        )

    def test_unavailable_evidence_has_no_value(self):
        evidence = UnavailableEvidence(UnavailableReason.VALUE_ABSENT)

        self.assertFalse(hasattr(evidence, "value"))

    def test_available_evidence_variants_have_no_reason(self):
        for evidence in (
            ObservedEvidence("value"),
            DerivedEvidence("value"),
            SimulatedEvidence("value"),
        ):
            with self.subTest(variant=type(evidence).__name__):
                self.assertFalse(hasattr(evidence, "reason"))

    def test_field_evidence_union_contains_exactly_the_four_variants(self):
        origins = [get_origin(argument) or argument for argument in get_args(FieldEvidence)]

        self.assertEqual(
            origins,
            [
                ObservedEvidence,
                DerivedEvidence,
                SimulatedEvidence,
                UnavailableEvidence,
            ],
        )

    def test_available_evidence_preserves_supplied_values_exactly(self):
        value = " 001AbC-09 "

        for evidence in (
            ObservedEvidence(value),
            DerivedEvidence(value),
            SimulatedEvidence(value),
        ):
            with self.subTest(variant=type(evidence).__name__):
                self.assertEqual(evidence.value, value)

    def test_unavailable_evidence_preserves_supplied_reason_exactly(self):
        reason = UnavailableReason.EVIDENCE_INDETERMINATE

        self.assertIs(UnavailableEvidence(reason).reason, reason)

    def test_all_evidence_variants_reject_ordinary_mutation(self):
        cases = [
            (ObservedEvidence("value"), "value", "changed"),
            (DerivedEvidence("value"), "value", "changed"),
            (SimulatedEvidence("value"), "value", "changed"),
            (
                UnavailableEvidence(UnavailableReason.VALUE_ABSENT),
                "reason",
                UnavailableReason.CONCEPT_ABSENT,
            ),
        ]

        for evidence, field_name, replacement in cases:
            with self.subTest(variant=type(evidence).__name__):
                with self.assertRaises(FrozenInstanceError):
                    setattr(evidence, field_name, replacement)


if __name__ == "__main__":
    unittest.main()

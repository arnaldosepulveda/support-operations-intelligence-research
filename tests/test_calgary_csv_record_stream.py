import csv
import unittest
from collections.abc import Mapping
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from support_operations_intelligence.calgary_adapter import (
    CalgaryAdaptedCase,
    adapt_calgary_record,
)
from support_operations_intelligence.calgary_csv import (
    EXPECTED_CALGARY_HEADER,
    CalgaryCsvArtifactDigestMismatch,
    CalgaryCsvStructureError,
    CalgaryCsvStructureErrorReason,
    iter_calgary_csv_records,
    verify_calgary_csv_artifact_sha256,
)
from support_operations_intelligence.evidence import ObservedEvidence
from support_operations_intelligence.identity import RejectedIdentity


EXPECTED_HEADER = (
    "service_request_id",
    "requested_date",
    "updated_date",
    "closed_date",
    "status_description",
    "source",
    "service_name",
    "agency_responsible",
    "address",
    "comm_code",
    "comm_name",
    "location_type",
    "longitude",
    "latitude",
    "point",
)


def _write_synthetic_csv(path: Path, rows: list[tuple[str, ...]]) -> None:
    with path.open(mode="w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows(rows)


class _LineLimitedTextStream:
    def __init__(self, csv_file, *, maximum_lines: int) -> None:
        self._csv_file = csv_file
        self._maximum_lines = maximum_lines
        self.lines_read = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._csv_file.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.lines_read >= self._maximum_lines:
            raise AssertionError("CSV stream was consumed beyond the prefix")

        line = next(self._csv_file)
        self.lines_read += 1
        return line


class CalgaryCsvRecordStreamTests(unittest.TestCase):
    def test_expected_header_is_exact_immutable_tuple(self):
        self.assertIsInstance(EXPECTED_CALGARY_HEADER, tuple)
        self.assertEqual(EXPECTED_CALGARY_HEADER, EXPECTED_HEADER)

    def test_synthetic_artifact_digest_match_returns_observed_digest(self):
        synthetic_bytes = b"synthetic Calgary digest gate fixture\n"
        expected_sha256 = sha256(synthetic_bytes).hexdigest()

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "digest-match.csv"
            path.write_bytes(synthetic_bytes)

            observed_sha256 = verify_calgary_csv_artifact_sha256(
                path,
                expected_sha256,
            )

        self.assertEqual(observed_sha256, expected_sha256)

    def test_synthetic_artifact_digest_mismatch_fails_closed(self):
        synthetic_bytes = b"synthetic Calgary digest gate fixture\n"
        actual_sha256 = sha256(synthetic_bytes).hexdigest()
        expected_sha256 = "0" * 64
        self.assertNotEqual(expected_sha256, actual_sha256)

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "digest-mismatch.csv"
            path.write_bytes(synthetic_bytes)

            with self.assertRaises(
                CalgaryCsvArtifactDigestMismatch
            ) as captured:
                verify_calgary_csv_artifact_sha256(path, expected_sha256)

        self.assertEqual(captured.exception.expected_sha256, expected_sha256)
        self.assertEqual(captured.exception.observed_sha256, actual_sha256)

    def test_one_valid_data_record_preserves_lexical_values(self):
        row = (
            "synthetic-001",
            "2026-01-01",
            "2026-01-02",
            "",
            "Open",
            "  Mobile App  ",
            "Synthetic Service",
            "Synthetic Agency",
            "123 Synthetic Street",
            "SYN",
            "Synthetic Community",
            "Synthetic Location",
            "-114.0000",
            "51.0000",
            "POINT (-114.0000 51.0000)",
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "one-record.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            iterator = iter_calgary_csv_records(path)
            record = next(iterator)

            self.assertIsInstance(record, Mapping)
            self.assertEqual(tuple(record.keys()), EXPECTED_HEADER)
            self.assertEqual(tuple(record.values()), row)
            self.assertEqual(record["source"], "  Mobile App  ")
            with self.assertRaises(StopIteration):
                next(iterator)

    def test_empty_file_raises_missing_header_reason(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "empty.csv"
            _write_synthetic_csv(path, [])

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.EMPTY_FILE_OR_MISSING_HEADER,
            )

    def test_header_mismatch_raises_before_yielding_data(self):
        incorrect_header = ("wrong_service_request_id", *EXPECTED_HEADER[1:])
        row = tuple(f"synthetic-{index}" for index in range(15))

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "wrong-header.csv"
            _write_synthetic_csv(path, [incorrect_header, row])

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.HEADER_MISMATCH,
            )

    def test_reordered_header_raises_before_yielding_data(self):
        reordered_header = list(EXPECTED_HEADER)
        reordered_header[5], reordered_header[6] = (
            reordered_header[6],
            reordered_header[5],
        )
        reordered_header = tuple(reordered_header)
        row = tuple(f"synthetic-{index}" for index in range(15))

        self.assertCountEqual(reordered_header, EXPECTED_HEADER)
        self.assertNotEqual(reordered_header, EXPECTED_HEADER)

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "reordered-header.csv"
            _write_synthetic_csv(path, [reordered_header, row])

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.HEADER_MISMATCH,
            )

    def test_extra_column_reports_first_logical_record_context(self):
        row = tuple(f"synthetic-{index}" for index in range(16))

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "extra-column.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 1)
            self.assertEqual(captured.exception.expected_column_count, 15)
            self.assertEqual(captured.exception.actual_column_count, 16)

    def test_missing_column_reports_first_logical_record_context(self):
        row = tuple(f"synthetic-{index}" for index in range(14))

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "missing-column.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 1)
            self.assertEqual(captured.exception.expected_column_count, 15)
            self.assertEqual(captured.exception.actual_column_count, 14)

    def test_malformed_third_record_reports_logical_record_three(self):
        row_a = tuple(f"synthetic-a-{index}" for index in range(15))
        row_b = tuple(f"synthetic-b-{index}" for index in range(15))
        malformed_row_c = tuple(
            f"synthetic-c-{index}" for index in range(16)
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "malformed-third-record.csv"
            _write_synthetic_csv(
                path,
                [EXPECTED_HEADER, row_a, row_b, malformed_row_c],
            )

            iterator = iter_calgary_csv_records(path)
            self.assertEqual(tuple(next(iterator).values()), row_a)
            self.assertEqual(tuple(next(iterator).values()), row_b)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 3)
            self.assertEqual(captured.exception.expected_column_count, 15)
            self.assertEqual(captured.exception.actual_column_count, 16)

    def test_row_width_failure_retains_exact_raw_logical_record(self):
        header_source = ",".join(EXPECTED_HEADER) + "\r\n"
        valid_record_source = ",".join(
            f"synthetic-valid-{index}" for index in range(15)
        ) + "\r\n"
        malformed_record_source = (
            'synthetic-bad-001,"  quoted, value  ",third,four,five,six,'
            "seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,"
            "sixteen\r\n"
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "raw-logical-record.csv"
            path.write_bytes(
                (
                    header_source
                    + valid_record_source
                    + malformed_record_source
                ).encode("utf-8")
            )

            iterator = iter_calgary_csv_records(path)
            next(iterator)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 2)
            self.assertEqual(
                captured.exception.raw_logical_record,
                malformed_record_source,
            )

    def test_multiline_row_width_failure_retains_complete_raw_logical_record(
        self,
    ):
        header_source = ",".join(EXPECTED_HEADER) + "\r\n"
        valid_record_source = ",".join(
            f"synthetic-valid-{index}" for index in range(15)
        ) + "\r\n"
        malformed_record_source = (
            'synthetic-multiline-001,one,two,"synthetic first line\r\n'
            'synthetic second line",four,five,six,seven,eight,nine,ten,'
            "eleven,twelve,thirteen\r\n"
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "raw-multiline-record.csv"
            path.write_bytes(
                (
                    header_source
                    + valid_record_source
                    + malformed_record_source
                ).encode("utf-8")
            )

            iterator = iter_calgary_csv_records(path)
            next(iterator)
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 2)
            self.assertEqual(
                captured.exception.raw_logical_record,
                malformed_record_source,
            )

    def test_embedded_newline_does_not_redefine_logical_record_number(self):
        row_a = (
            "synthetic-001",
            "2026-01-01",
            "2026-01-02",
            "",
            "Open",
            "Mobile App",
            "Synthetic line one\nSynthetic line two",
            "Synthetic Agency",
            "123 Synthetic Street",
            "SYN",
            "Synthetic Community",
            "Synthetic Location",
            "-114.0000",
            "51.0000",
            "POINT (-114.0000 51.0000)",
        )
        malformed_row_b = tuple(
            f"synthetic-b-{index}" for index in range(14)
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "embedded-newline.csv"
            _write_synthetic_csv(
                path,
                [EXPECTED_HEADER, row_a, malformed_row_b],
            )

            iterator = iter_calgary_csv_records(path)
            record_a = next(iterator)
            self.assertEqual(
                record_a["service_name"],
                "Synthetic line one\nSynthetic line two",
            )
            with self.assertRaises(CalgaryCsvStructureError) as captured:
                next(iterator)

            self.assertIs(
                captured.exception.reason,
                CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
            )
            self.assertEqual(captured.exception.logical_data_record_number, 2)
            self.assertEqual(captured.exception.expected_column_count, 15)
            self.assertEqual(captured.exception.actual_column_count, 14)

    def test_multiple_valid_records_preserve_source_order_and_values(self):
        rows = [
            tuple(["synthetic-001", *[f"first-{index}" for index in range(14)]]),
            tuple([" synthetic-002 ", *[f"second-{index}" for index in range(14)]]),
            tuple(["synthetic-003", *[f"third-{index}" for index in range(14)]]),
        ]

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "multiple-records.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, *rows])

            records = list(iter_calgary_csv_records(path))

        self.assertEqual(len(records), 3)
        self.assertEqual(
            [record["service_request_id"] for record in records],
            ["synthetic-001", " synthetic-002 ", "synthetic-003"],
        )
        self.assertEqual(
            [tuple(record.values()) for record in records],
            rows,
        )

    def test_empty_cell_remains_empty_string(self):
        row = tuple(["synthetic-001", *[f"value-{index}" for index in range(14)]])
        row = (*row[:7], "", *row[8:])

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "empty-cell.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            record = next(iter_calgary_csv_records(path))

        self.assertEqual(record["agency_responsible"], "")
        self.assertIsInstance(record["agency_responsible"], str)
        self.assertIsNotNone(record["agency_responsible"])

    def test_bounded_consumption_does_not_read_beyond_first_record(self):
        rows = [
            tuple([f"synthetic-{record}", *[f"value-{index}" for index in range(14)]])
            for record in range(1, 4)
        ]

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "bounded-consumption.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, *rows])
            csv_file = path.open(mode="r", encoding="utf-8", newline="")
            limited_stream = _LineLimitedTextStream(
                csv_file,
                maximum_lines=2,
            )

            with patch.object(Path, "open", return_value=limited_stream):
                iterator = iter_calgary_csv_records(path)
                first_record = next(iterator)
                self.assertEqual(
                    first_record["service_request_id"],
                    "synthetic-1",
                )
                self.assertEqual(limited_stream.lines_read, 2)
                iterator.close()

    def test_missing_path_raises_native_file_not_found_error(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "does-not-exist.csv"

            iterator = iter_calgary_csv_records(path)
            with self.assertRaises(FileNotFoundError) as captured:
                next(iterator)

        self.assertNotIsInstance(
            captured.exception,
            CalgaryCsvStructureError,
        )

    def test_parsed_record_composes_directly_with_calgary_adapter(self):
        row = (
            " synthetic-composition-001 ",
            "2026-01-01",
            "2026-01-02",
            "",
            " Synthetic Open ",
            "Synthetic Source",
            "Synthetic Service",
            "Synthetic Agency",
            "123 Synthetic Street",
            "SYN",
            "Synthetic Community",
            "Synthetic Location",
            "-114.0000",
            "51.0000",
            "POINT (-114.0000 51.0000)",
        )

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "parser-adapter-composition.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            iterator = iter_calgary_csv_records(path)
            parsed_record = next(iterator)
            result = adapt_calgary_record(parsed_record)
            iterator.close()

        self.assertIsInstance(parsed_record, Mapping)
        self.assertIsInstance(result, CalgaryAdaptedCase)
        self.assertNotIsInstance(result, RejectedIdentity)
        self.assertEqual(
            result.mapped_case.case.case_id.source_case_id,
            " synthetic-composition-001 ",
        )
        self.assertEqual(
            result.mapped_case.case.case_id.source_system,
            "city_of_calgary_311",
        )
        self.assertEqual(
            result.mapped_case.source_status,
            ObservedEvidence(" Synthetic Open "),
        )

    def test_parsed_record_matches_equivalent_hand_built_adapter_fixture(self):
        row = (
            " fixture-equivalence-id-937 ",
            "requested::2026-03-04T05:06:07Z",
            "updated::2026-04-05T06:07:08Z",
            "closed::2026-05-06T07:08:09Z",
            " status::fixture-equivalence::open ",
            " source::fixture-equivalence::mobile ",
            " service::fixture-equivalence::roadway ",
            " agency::fixture-equivalence::transport ",
            "937 Fixture Equivalence Avenue",
            "FX9",
            "Fixture Equivalence Community",
            "fixture-equivalence-location-type",
            "-113.9370",
            "50.9370",
            "POINT (-113.9370 50.9370)",
        )
        hand_built_mapping = {
            "service_request_id": " fixture-equivalence-id-937 ",
            "requested_date": "requested::2026-03-04T05:06:07Z",
            "updated_date": "updated::2026-04-05T06:07:08Z",
            "closed_date": "closed::2026-05-06T07:08:09Z",
            "status_description": " status::fixture-equivalence::open ",
            "source": " source::fixture-equivalence::mobile ",
            "service_name": " service::fixture-equivalence::roadway ",
            "agency_responsible": " agency::fixture-equivalence::transport ",
            "address": "937 Fixture Equivalence Avenue",
            "comm_code": "FX9",
            "comm_name": "Fixture Equivalence Community",
            "location_type": "fixture-equivalence-location-type",
            "longitude": "-113.9370",
            "latitude": "50.9370",
            "point": "POINT (-113.9370 50.9370)",
        }

        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "equivalent-adapter-fixture.csv"
            _write_synthetic_csv(path, [EXPECTED_HEADER, row])

            iterator = iter_calgary_csv_records(path)
            parsed_mapping = next(iterator)
            parsed_result = adapt_calgary_record(parsed_mapping)
            iterator.close()

        hand_built_result = adapt_calgary_record(hand_built_mapping)

        self.assertEqual(parsed_result, hand_built_result)


if __name__ == "__main__":
    unittest.main()

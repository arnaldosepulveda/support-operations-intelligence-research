import csv
import unittest
from collections.abc import Mapping
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from support_operations_intelligence.calgary_csv import (
    EXPECTED_CALGARY_HEADER,
    CalgaryCsvStructureError,
    CalgaryCsvStructureErrorReason,
    iter_calgary_csv_records,
)


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


if __name__ == "__main__":
    unittest.main()

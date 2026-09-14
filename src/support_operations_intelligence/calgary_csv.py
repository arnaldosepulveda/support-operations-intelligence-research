import csv
from collections.abc import Iterator, Mapping
from enum import Enum
from pathlib import Path


EXPECTED_CALGARY_HEADER = (
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


class CalgaryCsvStructureErrorReason(Enum):
    EMPTY_FILE_OR_MISSING_HEADER = "EMPTY_FILE_OR_MISSING_HEADER"
    HEADER_MISMATCH = "HEADER_MISMATCH"
    ROW_WIDTH_MISMATCH = "ROW_WIDTH_MISMATCH"


class CalgaryCsvStructureError(Exception):
    def __init__(
        self,
        *,
        reason: CalgaryCsvStructureErrorReason,
        logical_data_record_number: int | None = None,
        expected_column_count: int | None = None,
        actual_column_count: int | None = None,
    ) -> None:
        super().__init__(reason.value)
        self.reason = reason
        self.logical_data_record_number = logical_data_record_number
        self.expected_column_count = expected_column_count
        self.actual_column_count = actual_column_count


def iter_calgary_csv_records(
    path: Path,
) -> Iterator[Mapping[str, str]]:
    with path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)

        try:
            header = next(reader)
        except StopIteration:
            raise CalgaryCsvStructureError(
                reason=(
                    CalgaryCsvStructureErrorReason.EMPTY_FILE_OR_MISSING_HEADER
                )
            ) from None

        if tuple(header) != EXPECTED_CALGARY_HEADER:
            raise CalgaryCsvStructureError(
                reason=CalgaryCsvStructureErrorReason.HEADER_MISMATCH
            )

        expected_column_count = len(EXPECTED_CALGARY_HEADER)
        for logical_data_record_number, row in enumerate(reader, start=1):
            actual_column_count = len(row)
            if actual_column_count != expected_column_count:
                raise CalgaryCsvStructureError(
                    reason=CalgaryCsvStructureErrorReason.ROW_WIDTH_MISMATCH,
                    logical_data_record_number=logical_data_record_number,
                    expected_column_count=expected_column_count,
                    actual_column_count=actual_column_count,
                )

            yield dict(zip(EXPECTED_CALGARY_HEADER, row, strict=True))

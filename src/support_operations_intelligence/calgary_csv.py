import csv
from collections.abc import Iterator, Mapping
from enum import Enum
from hashlib import sha256
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
        raw_logical_record: str | None = None,
    ) -> None:
        super().__init__(reason.value)
        self.reason = reason
        self.logical_data_record_number = logical_data_record_number
        self.expected_column_count = expected_column_count
        self.actual_column_count = actual_column_count
        self.raw_logical_record = raw_logical_record


class _LogicalCsvRecordSourceTracker:
    def __init__(self, physical_lines: Iterator[str]) -> None:
        self._physical_lines = physical_lines
        self._current_record_lines: list[str] = []

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        physical_line = next(self._physical_lines)
        self._current_record_lines.append(physical_line)
        return physical_line

    def clear_current_record(self) -> None:
        self._current_record_lines.clear()

    def take_current_record(self) -> str:
        raw_logical_record = "".join(self._current_record_lines)
        self.clear_current_record()
        return raw_logical_record


class CalgaryCsvArtifactDigestMismatch(Exception):
    def __init__(
        self,
        *,
        expected_sha256: str,
        observed_sha256: str,
    ) -> None:
        super().__init__(
            f"expected SHA-256 {expected_sha256}, observed {observed_sha256}"
        )
        self.expected_sha256 = expected_sha256
        self.observed_sha256 = observed_sha256


def verify_calgary_csv_artifact_sha256(
    path: Path,
    expected_sha256: str,
) -> str:
    digest = sha256()
    with path.open(mode="rb") as artifact_file:
        while chunk := artifact_file.read(1024 * 1024):
            digest.update(chunk)

    observed_sha256 = digest.hexdigest()
    if observed_sha256 != expected_sha256:
        raise CalgaryCsvArtifactDigestMismatch(
            expected_sha256=expected_sha256,
            observed_sha256=observed_sha256,
        )

    return observed_sha256


def iter_calgary_csv_records(
    path: Path,
) -> Iterator[Mapping[str, str]]:
    with path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        source_tracker = _LogicalCsvRecordSourceTracker(iter(csv_file))
        reader = csv.reader(source_tracker)

        try:
            header = next(reader)
        except StopIteration:
            raise CalgaryCsvStructureError(
                reason=(
                    CalgaryCsvStructureErrorReason.EMPTY_FILE_OR_MISSING_HEADER
                )
            ) from None

        source_tracker.clear_current_record()
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
                    raw_logical_record=source_tracker.take_current_record(),
                )

            source_tracker.clear_current_record()
            yield dict(zip(EXPECTED_CALGARY_HEADER, row, strict=True))

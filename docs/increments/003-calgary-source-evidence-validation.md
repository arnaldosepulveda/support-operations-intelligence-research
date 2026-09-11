# Increment 003 - Calgary Source Evidence Validation

**Status:** Planned
**Opened:** 2026-09-10

## Objective

Establish a repository-validated evidence baseline for the local City of Calgary 311 dataset before defining a Calgary source contract or canonical adapter mapping.

This increment should determine what source artifact is actually present, what its observable structure and lifecycle evidence support, and what provenance, licensing, and version assumptions can be substantiated. It does not prove cross-source portability of the canonical Case abstraction.

## Why This Increment Exists

Previous Calgary characteristics are `EXTERNALLY REPORTED / PREPARED CONTEXT`, not repository-validated observations.

That context reports:

- a believed local dataset root of `/data/repos/Public Datasets`;
- a candidate file named `calgary_311.csv`;
- approximately 7.47 million rows;
- a reportedly unique `service_request_id`;
- reported lifecycle timestamps named `requested_date`, `updated_date`, and `closed_date`;
- a reported temporal range of approximately 2010 through 2026;
- no reported assignment, dispatch, handoff, active-work, queue-residence, customer-wait, or rework timing;
- the Open Government Licence - City of Calgary as the reported licence.

None of these statements is an observed repository fact at the opening of Increment 003.

## Scope

Later execution of Increment 003 is planned to verify:

1. the authoritative local dataset path actually present;
2. file identity and basic filesystem metadata;
3. file format and readability;
4. observed column and schema structure;
5. observed row count;
6. observed source-identifier behavior, including `service_request_id` presence, nullability, and uniqueness;
7. observable lifecycle timestamp fields;
8. timestamp parseability and supported temporal precision;
9. observed date range;
10. important missingness and data-quality characteristics relevant to later canonical mapping;
11. whether Calgary native fields relevant to Increment 002 are actually present, including, where applicable, `requested_date`, `updated_date`, `closed_date`, `status_description`, `service_name`, `agency_responsible`, `source`, and address, community, or other spatial fields;
12. source provenance sufficient to identify which Calgary dataset the file is intended to represent;
13. current authoritative licence and attribution evidence;
14. a reproducibility identifier such as a file hash once the artifact is inspected;
15. discrepancies between externally reported preparation evidence and repository-observed evidence.

## Non-goals

Increment 003 will not:

- implement a source adapter;
- implement or select canonical Case persistence;
- perform PostgreSQL ingestion;
- create a production ingestion pipeline;
- perform SQL operational analysis;
- create a management dashboard or view;
- create or implement `CaseEvent`;
- inspect ServiceNow;
- perform cross-source comparison;
- perform workflow decomposition;
- select or implement an AI intervention;
- define a canonical status taxonomy;
- implement canonical classification;
- conclude universal portability;
- make final semantic mapping decisions that require a source contract.

For example, this increment may establish that `requested_date` exists and characterize its evidence, but it must not automatically conclude that the field satisfies canonical `created_at` unless source semantics support that mapping.

## Starting State

Repository HEAD at opening:

    382642a78b33a326a22edf9f9a0f53864b1669a5

Increment 001 is Complete.

Increment 002 is Complete. It established the canonical Case semantic contract and source-adapter conformance requirements.

No Calgary source contract exists. No Calgary adapter exists. No repository-validated Calgary empirical profile has been established. No operational capability is claimed.

README.md contains known stale foundation wording, but correcting it is outside Increment 003 unless separately authorized.

## Assumptions to Test, Not Facts

The following are unverified assumptions or hypotheses:

- `/data/repos/Public Datasets` is the correct dataset root;
- `calgary_311.csv` exists there;
- the file is the intended Calgary 311 Service Requests dataset;
- the reported row count is approximately correct;
- `service_request_id` is unique;
- `requested_date`, `updated_date`, and `closed_date` exist;
- the reported lifecycle and date-range characteristics are correct;
- the reported Calgary licence and attribution remain applicable to this artifact.

Local file presence alone would not establish authoritative provenance, current source version, licence validity, schema semantics, or canonical mapping correctness.

## Threat and Failure Model

Increment 003 may fail or produce a negative result if:

- the expected file does not exist;
- the expected path is wrong;
- the local file is incomplete or corrupt;
- the file cannot be read reproducibly;
- its schema differs from the reported preparation context;
- `service_request_id` is missing, null, or non-unique;
- lifecycle fields differ from expectations;
- timestamps are malformed or semantically unclear;
- observed temporal coverage differs materially from the reported range;
- source provenance cannot be established;
- licence or attribution cannot be verified;
- the local artifact appears to be a transformed derivative without enough lineage to reconstruct its origin;
- reported preparation evidence cannot be reproduced.

Negative results must be retained rather than normalized away.

## Planned Evidence

Later work in this increment should retain, as appropriate:

- filesystem and path evidence;
- file size and metadata;
- file hash;
- observed schema;
- row-count evidence;
- identifier null and uniqueness checks;
- timestamp parsing and profile results;
- date-range evidence;
- missingness summaries for contract-relevant fields;
- source-provenance evidence;
- licence and attribution evidence;
- discrepancies from prior externally reported context;
- commands or scripts sufficient for another engineer to reproduce the inspection.

These are planned evidence artifacts. They do not exist merely because this planning record lists them.

## Claim Discipline

**Current Calgary profile before execution:** external and preparation evidence.

**Increment 003 file, schema, and profile results:** future engineering observations.

**Verified source and licence facts:** future external evidence once authoritative material is inspected.

**Canonical Calgary field mappings:** future design decisions in source-contract work.

**Cross-source Case portability:** research hypothesis.

**Universal portability:** not claimed.

**Workflow decomposition from Calgary:** not supported by current evidence and not an Increment 003 goal.

## Relationship to Increment 002

Increment 003 will pressure-test Increment 002 but must not silently revise it.

If observed Calgary evidence conflicts with an accepted Increment 002 contract rule:

- preserve the conflict;
- do not modify Increment 002 inside Increment 003 without an explicit revision decision;
- classify whether the evidence may `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` the Calgary mapping under the established falsification framework.

This record does not predict that outcome.

## Completion Criteria

Increment 003 may be marked Complete only when, at minimum:

1. the actual local Calgary artifact has been identified or its absence explicitly established;
2. filesystem and file-identity evidence is retained;
3. schema and basic readability are verified;
4. row count is directly observed;
5. source-identifier behavior relevant to canonical identity is tested;
6. contract-relevant lifecycle and source fields are profiled;
7. timestamp and date coverage is characterized;
8. important missingness or malformed evidence is characterized;
9. source provenance has been investigated and its confidence and boundary recorded;
10. licence and attribution evidence has been investigated and its confidence and boundary recorded;
11. discrepancies from prior externally reported preparation context are retained;
12. source evidentiary limitations are explicitly recorded;
13. reproducibility commands or artifacts are retained;
14. no source mapping is promoted to canonical fact without semantic justification;
15. observed results and planned work are clearly distinguished.

## Skills Practiced

### Practiced or Refreshed

- source-data inspection;
- data profiling;
- provenance reasoning;
- data-quality reasoning;
- evidence preservation;
- reproducibility;
- semantic boundary discipline.

### Developed

- translating a canonical domain contract into source-validation requirements.

### Not Practiced in This Increment

- production ingestion;
- application coding;
- AI or LLM implementation;
- frontend work;
- workflow reconstruction.

## Observed Result

### Filesystem-Level Observation 001

**Evidence classification:** Engineering observation

On 2026-09-10, the first empirical inspection under Increment 003 observed only local filesystem existence, directory membership, object type, and metadata. No CSV contents were inspected.

#### Dataset Root

Expected path:

    /data/repos/Public Datasets

Directly observed:

- the path exists;
- the object is a directory;
- size: 4096 bytes;
- blocks: 8;
- inode: 3165140;
- links: 2;
- permissions: `0775` / `drwxrwxr-x`;
- owner/group: `arnaldo-admin`;
- access timestamp: `2026-09-10 02:29:27.735739523 -0300`;
- modify/change timestamp: `2026-09-10 03:20:09.607744184 -0300`;
- birth timestamp: `2026-09-10 02:29:27.735739523 -0300`.

Filesystem timestamps are local filesystem metadata and are **not** evidence of dataset publication date, source update date, or authoritative retrieval date.

Preregistered assumption result: `CONFIRMED_AT_FILESYSTEM_LEVEL`.

#### Immediate Directory Membership

The following immediate filenames were observed:

- `bpi2013_incidents.xes.gz`
- `bpi2014_incidents.csv`
- `calgary_311.csv`
- `calgary_wrs_2024.csv`
- `incident_event_log.csv`
- `incident_log.zip`
- `nyc_311_archive.csv`
- `nyc_311_recent.csv`
- `support_ops.duckdb`

These are filename observations only. No provenance, contents, completeness, relationships, or source authority can be inferred from the filenames alone.

`calgary_wrs_2024.csv` is an additional Calgary-looking artifact, but it was not inspected.

#### Expected Calgary Artifact

Expected path:

    /data/repos/Public Datasets/calgary_311.csv

Directly observed:

- the exact path exists;
- the object is a regular file;
- size: 1,978,541,467 bytes;
- blocks: 3,864,352;
- inode: 3165247;
- links: 1;
- permissions: `0664` / `-rw-rw-r--`;
- owner/group: `arnaldo-admin`;
- access timestamp: `2026-09-10 02:30:45.729316459 -0300`;
- modify/change timestamp: `2026-09-10 02:39:02.993969076 -0300`;
- birth timestamp: `2026-09-10 02:30:45.729316459 -0300`;
- `file` utility classification: `CSV ASCII text`.

Preregistered assumption result: `CONFIRMED_AT_FILESYSTEM_LEVEL`.

No discrepancy was observed against either preregistered filesystem assumption: the expected dataset root and the expected Calgary candidate path both exist at their stated locations.

#### Strict Claim Boundary

This observation does **not** establish:

- authoritative Calgary provenance;
- dataset correctness;
- completeness;
- row count;
- schema;
- source version;
- `service_request_id` presence;
- `service_request_id` uniqueness;
- lifecycle-field presence;
- lifecycle semantics;
- timestamp parseability;
- date coverage;
- dataset publication time;
- current licence;
- attribution requirements;
- canonical Case mapping validity.

No CSV contents or header were inspected. No row count, schema analysis, hash computation, or dataset profiling was performed.

This observation provides partial progress toward local artifact identification and filesystem/file identity evidence only. It does not establish source identity or authoritative provenance, and it does not satisfy any other empirical completion criterion. Increment 003 remains Planned.

#### Reproducibility

The bounded observation used the following command forms:

```sh
if [ -e "/data/repos/Public Datasets" ]; then
    echo "DATASET_ROOT_EXISTS"
else
    echo "DATASET_ROOT_MISSING"
fi

if [ -d "/data/repos/Public Datasets" ]; then
    echo "DATASET_ROOT_IS_DIRECTORY"
else
    echo "DATASET_ROOT_NOT_DIRECTORY"
fi

stat -- "/data/repos/Public Datasets"

if [ -e "/data/repos/Public Datasets/calgary_311.csv" ]; then
    echo "CALGARY_ARTIFACT_EXISTS"
else
    echo "CALGARY_ARTIFACT_MISSING"
fi

stat -- "/data/repos/Public Datasets/calgary_311.csv"
file -- "/data/repos/Public Datasets/calgary_311.csv"

find "/data/repos/Public Datasets" \
  -maxdepth 1 \
  -mindepth 1 \
  -printf '%f\n' \
  | sort
```

### Header-Only Observation 002

**Evidence classification:** Engineering observation

On 2026-09-10, exactly one CSV record, the header, was read from:

    /data/repos/Public Datasets/calgary_311.csv

This was the first CSV content inspection under Increment 003. No data row was read.

#### Observed Header

The observed header contained 15 fields in this order:

1. `service_request_id`
2. `requested_date`
3. `updated_date`
4. `closed_date`
5. `status_description`
6. `source`
7. `service_name`
8. `agency_responsible`
9. `address`
10. `comm_code`
11. `comm_name`
12. `location_type`
13. `longitude`
14. `latitude`
15. `point`

Duplicate header names: none observed.

Empty or blank header names: none observed.

#### Contract-Relevant Field Presence

| Candidate field | Header-level classification |
| --- | --- |
| `service_request_id` | `PRESENT_IN_HEADER` |
| `requested_date` | `PRESENT_IN_HEADER` |
| `updated_date` | `PRESENT_IN_HEADER` |
| `closed_date` | `PRESENT_IN_HEADER` |
| `status_description` | `PRESENT_IN_HEADER` |
| `service_name` | `PRESENT_IN_HEADER` |
| `agency_responsible` | `PRESENT_IN_HEADER` |
| `source` | `PRESENT_IN_HEADER` |
| `address` | `PRESENT_IN_HEADER` |
| `comm_code` | `PRESENT_IN_HEADER` |
| `comm_name` | `PRESENT_IN_HEADER` |
| `location_type` | `PRESENT_IN_HEADER` |
| `longitude` | `PRESENT_IN_HEADER` |
| `latitude` | `PRESENT_IN_HEADER` |
| `point` | `PRESENT_IN_HEADER` |

Possible-name matches: none required. Every preregistered candidate field name checked in this step appeared exactly in the observed header.

Discrepancies from preregistered expected field names: none observed.

#### Strict Semantic Boundary

Header presence establishes field-name existence in this local artifact only. It does **not** establish:

- data type;
- populated values;
- nullability;
- uniqueness;
- identifier validity;
- timestamp parseability;
- timestamp precision;
- date range;
- lifecycle semantics;
- source-native semantic meaning;
- canonical mapping validity;
- dataset completeness;
- authoritative provenance;
- source version;
- current licence;
- attribution requirements.

In particular:

- `requested_date` appearing in the header does **not** establish `requested_date -> Case.created_at`;
- `status_description` appearing in the header does **not** establish `status_description -> canonical or source_status mapping` without source-semantic justification;
- `source` appearing in the header does **not** by itself establish its meaning as intake or origin information;
- `closed_date` appearing in the header does **not** establish a universal canonical `Case.closed_at`;
- `updated_date` appearing in the header does **not** establish a universal canonical `Case.updated_at`.

#### Relationship to Increment 002

The header observation is consistent with several previously externally reported candidate Calgary fields, but it does not validate their semantics. It does not reopen Increment 002, and no conflict requiring `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification was observed in this step. Calgary portability has not been validated.

#### Reproducibility Observation

The successful inspection used Python standard-library `csv.reader` with `encoding="ascii"` and `newline=""` and read exactly one record. `python` was unavailable in the shell used for this inspection, so the successful invocation used `python3`. This is an engineering and reproducibility observation, not a dataset characteristic, and it supports no inference about the repository-local `.venv`.

#### Observed Now and Still Planned

Observed now:

- the exact header record;
- the 15 field names and their order;
- no duplicate header names;
- no empty or blank header names;
- exact header presence of all expected candidate names.

Still planned or unverified:

- data rows;
- row count;
- identifier uniqueness;
- nullability and missingness;
- timestamp parsing;
- date coverage;
- source semantics;
- provenance;
- licence;
- hash;
- canonical source-contract mappings.

This observation provides partial progress toward schema/header structure and presence of contract-relevant candidate fields only. Data types, identifier behavior, lifecycle-evidence usability, timestamp parseability, temporal range, missingness, provenance, licence, and canonical mappings remain unverified. Increment 003 remains Planned.

### First-Data-Row Observation 003

**Evidence classification:** Engineering observation

On 2026-09-10, exactly two CSV records were read during this bounded inspection of:

    /data/repos/Public Datasets/calgary_311.csv

Those records were:

1. the header;
2. exactly the first data row.

No additional record was read.

#### Parse and Field-Count Observation

- header field count: 15;
- first data-row field count: 15;
- field counts match: `true`.

The first data row was successfully returned by Python standard-library `csv.reader` using `encoding="ascii"` and `newline=""`. This establishes successful parsing of that one record only; it does **not** establish whole-file parseability.

#### Ordered Raw First-Row Values

The following are raw strings, recorded in header order:

1. `service_request_id`: `'18-01017964'`
2. `requested_date`: `'2018/10/17 12:00:00 AM'`
3. `updated_date`: `'2020/06/24 12:00:00 AM'`
4. `closed_date`: `'2020/06/24 12:00:00 AM'`
5. `status_description`: `'Closed'`
6. `source`: `'Phone'`
7. `service_name`: `'Roads - Traffic Signal Timing Inquiry'`
8. `agency_responsible`: `'TRAN - Roads'`
9. `address`: `''`
10. `comm_code`: `'SHN'`
11. `comm_name`: `'SHAWNESSY'`
12. `location_type`: `'Community Centrepoint'`
13. `longitude`: `'-114.0737568214987'`
14. `latitude`: `'50.90330332947782'`
15. `point`: `'POINT (-114.073756821499 50.903303329478)'`

#### Empty and Non-Empty Values in This Row

Empty string in this one row:

- `address`.

Non-empty strings in this one row:

- `service_request_id`;
- `requested_date`;
- `updated_date`;
- `closed_date`;
- `status_description`;
- `source`;
- `service_name`;
- `agency_responsible`;
- `comm_code`;
- `comm_name`;
- `location_type`;
- `longitude`;
- `latitude`;
- `point`.

A non-empty value in this row does **not** establish that the column is universally populated. An empty value in this row does **not** establish general missingness.

#### Lexical-Form Boundary

Several raw strings have date-like, numeric-like, spatial, or categorical-looking lexical forms. They are not classified at this stage as timestamps, dates, integers, floats, coordinates, geometry, enums, a status taxonomy, or an intake taxonomy.

Examples:

- `'2018/10/17 12:00:00 AM'`: raw string only at this stage;
- `'-114.0737568214987'`: raw string only at this stage;
- `'POINT (-114.073756821499 50.903303329478)'`: raw string only at this stage;
- `'Closed'`: raw string only at this stage;
- `'Phone'`: raw string only at this stage.

Appearance alone does not establish a semantic type.

#### Semantic Non-Claims

This one-row observation does **not** establish:

- dataset-wide data types;
- population;
- nullability;
- missingness rates;
- uniqueness;
- identifier validity;
- timestamp parseability;
- timestamp precision;
- temporal range;
- status vocabulary;
- source or intake vocabulary;
- classification vocabulary;
- agency behavior;
- spatial validity;
- dataset completeness;
- source semantics;
- canonical mappings;
- authoritative provenance;
- source version;
- current licence;
- attribution requirements.

#### Increment 002 Boundary

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_THIS_SINGLE_ROW`.

This observation is not classified as `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT`, and the row does not validate portability. Specifically:

- `requested_date` is not yet established as `Case.created_at`;
- `status_description` is not yet established as `source_status`;
- `source` is not yet semantically established as intake or origin;
- `closed_date` does not establish universal `Case.closed_at`;
- `updated_date` does not establish universal `Case.updated_at`.

#### Reproducibility

The actual method used `python3` and Python standard-library `csv.reader` with `encoding="ascii"` and `newline=""`. The two reads were exactly:

```python
header = next(reader)
first_row = next(reader)
```

No further `next(reader)` call occurred. This observation supports no inference about the repository-local `.venv`.

#### Increment Progress Boundary

This observation provides partial progress toward basic readability and row-width consistency for the first observed data row only. Whole-file readability, row count, identifier behavior, missingness, timestamp usability, temporal coverage, provenance, licence, hash, and canonical source mappings remain unverified. Increment 003 remains Planned.

### Whole-File Structural Observation 004

**Evidence classification:** Engineering observation

On 2026-09-10, a bounded whole-file structural scan was completed for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

The scan used `python3` and Python standard-library `csv.reader` with `encoding="ascii"` and `newline=""`. It streamed one logical CSV record at a time and did not retain the entire dataset in memory.

#### Observed Structural Results

- `WHOLE_FILE_SCAN_COMPLETED`: `true`;
- `HEADER_FIELD_COUNT`: 15;
- `LOGICAL_DATA_ROW_COUNT`: 7,474,403;
- `FIELD_COUNT_DISTRIBUTION`: `{15: 7,474,403}`;
- `ALL_DATA_ROWS_MATCH_HEADER_WIDTH`: `true`;
- `RETAINED_WIDTH_MISMATCHES`: none.

The local artifact contained 7,474,403 logical CSV data rows under this `csv.reader` scan. Logical CSV records are not assumed to be equivalent to physical text lines.

#### Whole-File Parseability Result

The observed local artifact was successfully iterated from header through EOF using the specified parser, encoding, and newline settings. This establishes whole-file parseability of this observed local artifact under this specific parser configuration. It does **not** establish semantic correctness of every record.

#### External Preparation Comparison

- previously retained external/preparation count: 7,474,403 rows;
- observed local logical data-row count: 7,474,403;
- exact numerical difference: 0;
- classification: `MATCHES_REPORTED_ROW_COUNT`.

This match corroborates the earlier reported count. A matching count does **not** prove authoritative provenance, dataset completeness, source-version identity, correctness of the artifact, or equivalence to the current authoritative Calgary source.

#### Structural Width Consistency

All 7,474,403 parsed data rows had exactly 15 fields. No structural width mismatch was observed. This establishes structural width consistency under this `csv.reader` scan. It does **not** establish:

- field semantics;
- valid values;
- data types;
- non-null values;
- semantic validity;
- referential validity;
- canonical mapping correctness.

#### Strict Non-Claims

This scan does **not** establish:

- authoritative completeness;
- authoritative row count;
- `service_request_id` uniqueness;
- `service_request_id` nullability;
- identifier validity;
- per-column missingness;
- data types;
- timestamp parseability;
- timestamp precision;
- temporal range;
- lifecycle semantics;
- status vocabulary;
- source or intake vocabulary;
- classification vocabulary;
- agency semantics;
- coordinate validity;
- geometry validity;
- canonical mappings;
- authoritative provenance;
- source version;
- current licence;
- attribution requirements.

#### Increment 002 Boundary

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_STRUCTURAL_SCAN`.

No structural observation from this scan conflicts with the accepted canonical Case contract. No `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied, and Calgary portability has not been validated.

#### Completion-Criteria Progress

This observation provides direct progress toward basic whole-file readability, direct local logical row-count observation, and structural row-width verification. Identifier behavior, missingness and data quality, timestamp and date coverage, source semantics, provenance, licence, file hash, and canonical mappings remain unverified. Increment 003 remains Planned.

#### Reproducibility

The bounded scan used streaming `csv.reader` iteration, processing one logical record at a time without full-file in-memory retention. A `Counter` accumulated field-width counts. At most ten structural width mismatches would have been retained; none were observed.

### Raw-Identifier Quality Observation 005

**Evidence classification:** Engineering observation

On 2026-09-10, a bounded dataset-wide raw-field scan was completed for:

- observed local artifact: `/data/repos/Public Datasets/calgary_311.csv`;
- observed field: `service_request_id`.

#### Scan Method

The scan used:

- Python 3;
- standard-library `csv.reader`;
- streaming iteration over one logical CSV record at a time;
- a temporary SQLite database under `/tmp` to retain the exact distinct nonblank raw identifier strings;
- batched identifiers rather than retaining all identifiers in Python memory.

The temporary SQLite database was outside the repository and was removed successfully after the scan. It is a transient inspection mechanism, not a retained research artifact.

#### Exact Observed Results

- `IDENTITY_SCAN_COMPLETED`: `true`;
- `LOGICAL_DATA_ROWS`: 7,474,403;
- `EMPTY_IDENTIFIER_ROWS`: 0;
- `WHITESPACE_ONLY_IDENTIFIER_ROWS`: 0;
- `NONBLANK_IDENTIFIER_ROWS`: 7,474,403;
- `DISTINCT_NONBLANK_IDENTIFIERS`: 7,474,403;
- `DUPLICATE_NONBLANK_ROWS`: 0;
- `ALL_ROWS_HAVE_USABLE_RAW_IDENTIFIER`: `true`;
- `NONBLANK_IDENTIFIERS_ARE_UNIQUE`: `true`;
- `OBSERVED_RAW_IDENTITY_CANDIDATE_CONDITION`: `true`.

No blank, whitespace-only, or duplicate raw identifier was observed. These zero counts are retained as part of the evidence.

#### Measurement Definitions

- `EMPTY_IDENTIFIER_ROWS` means the raw CSV value was exactly `""`.
- `WHITESPACE_ONLY_IDENTIFIER_ROWS` means the raw value was non-empty but `raw_id.strip() == ""`.
- `NONBLANK_IDENTIFIER_ROWS` means the raw identifier was neither empty nor whitespace-only.
- `DISTINCT_NONBLANK_IDENTIFIERS` means the number of distinct raw nonblank identifier strings under the exact SQLite `TEXT` comparison used by the scan.
- `DUPLICATE_NONBLANK_ROWS` equals `NONBLANK_IDENTIFIER_ROWS - DISTINCT_NONBLANK_IDENTIFIERS`.

Observed duplicate calculation:

    7,474,403 - 7,474,403 = 0

No case, punctuation, prefix, or whitespace normalization and no numeric conversion was applied to stored nonblank identifiers. This was an exact raw-string identity check.

#### Permitted Empirical Interpretation

Every observed logical data row in this local artifact had a nonblank raw `service_request_id`, and those raw identifier strings were unique within this artifact under the exact comparison used.

This is an **empirical raw-field property**, not yet **semantic source-identity justification**. The result makes `service_request_id` a strong candidate for future evaluation as Calgary `source_case_id`; it does not establish that mapping.

#### External Preparation Comparison

The retained external/preparation context previously reported that `service_request_id` is unique. Result: `CORROBORATES_REPORTED_IDENTIFIER_UNIQUENESS`.

The directly observed local scan corroborates that earlier report. This is not source-authoritative verification.

#### Strict Source-Identity Boundary

This scan does **not** establish:

- that `service_request_id` is semantically the authoritative native identity of one Calgary service request;
- that `service_request_id` should yet be mapped to `Case.source_case_id`;
- identifier immutability;
- absence of identifier reuse outside this observed artifact;
- identity continuity across Calgary source versions;
- completeness of the local artifact;
- authoritative source provenance;
- source version;
- canonical `case_id` generation;
- cross-source identity;
- entity resolution;
- canonical mapping validity;
- row semantic correctness;
- temporal semantics;
- licence;
- attribution.

Uniqueness within this artifact is necessary empirical evidence for an identity candidate, but it is not sufficient semantic evidence for canonical identity.

#### Increment 002 Pressure Test

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_RAW_IDENTIFIER_SCAN`.

Increment 002 requires a future adapter to establish source-native identity semantics. This scan tested a necessary empirical property of the candidate field only. No observed `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied, and neither the Calgary Case mapping nor portability has been validated.

#### Increment 003 Progress

This observation provides direct progress toward identifier presence, raw-string uniqueness, and empirical suitability of `service_request_id` as an identity candidate. Semantic identity mapping, a source contract, missingness across other fields, timestamp usability, temporal coverage, provenance, source version, licence, hash, and canonical mappings remain unverified. Increment 003 remains Planned.

### Lexical Blankness Observation 006

**Evidence classification:** Engineering observation

On 2026-09-10, a dataset-wide lexical blankness profile was completed for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

For this observation:

- `EMPTY` means `raw_value == ""`;
- `WHITESPACE_ONLY` means `raw_value != ""` and `raw_value.strip() == ""`;
- `NONBLANK` means neither `EMPTY` nor `WHITESPACE_ONLY`.

This is lexical blankness measurement, not semantic missingness.

#### Scan Method and Invariant

The scan used Python 3 and Python standard-library `csv.reader` with `encoding="ascii"` and `newline=""`. It streamed one logical CSV record at a time, retained only per-field counters, and did not retain rows or raw values.

- `LEXICAL_BLANKNESS_SCAN_COMPLETED`: `true`;
- `LOGICAL_DATA_ROWS`: 7,474,403;
- `HEADER_FIELD_COUNT`: 15.

Every field satisfied `EMPTY + WHITESPACE_ONLY + NONBLANK = 7,474,403`.

#### Exact Per-Field Results

| Field | Empty | Empty % | Whitespace-only | Whitespace-only % | Nonblank | Nonblank % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `service_request_id` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `requested_date` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `updated_date` | 77,829 | 1.041274 | 0 | 0.000000 | 7,396,574 | 98.958726 |
| `closed_date` | 78,347 | 1.048204 | 0 | 0.000000 | 7,396,056 | 98.951796 |
| `status_description` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `source` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `service_name` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `agency_responsible` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `address` | 7,474,403 | 100.000000 | 0 | 0.000000 | 0 | 0.000000 |
| `comm_code` | 429,787 | 5.750118 | 0 | 0.000000 | 7,044,616 | 94.249882 |
| `comm_name` | 429,787 | 5.750118 | 0 | 0.000000 | 7,044,616 | 94.249882 |
| `location_type` | 0 | 0.000000 | 0 | 0.000000 | 7,474,403 | 100.000000 |
| `longitude` | 430,664 | 5.761851 | 0 | 0.000000 | 7,043,739 | 94.238149 |
| `latitude` | 430,664 | 5.761851 | 0 | 0.000000 | 7,043,739 | 94.238149 |
| `point` | 430,664 | 5.761851 | 0 | 0.000000 | 7,043,739 | 94.238149 |

No non-empty whitespace-only value was observed in any of the 15 fields under the scan definition. This does not establish semantic cleanliness.

#### `service_request_id` Cross-Check

Result: `CONSISTENT_WITH_PRIOR_IDENTIFIER_SCAN`.

`service_request_id` again had 0 raw empty-string values and 0 non-empty whitespace-only values. This is not new source-identity semantic evidence.

#### Direct Field-Population Observations

- `address` was the empty string in all 7,474,403 observed rows;
- `requested_date` was nonblank in all observed rows;
- `status_description` was nonblank in all observed rows;
- `source` was nonblank in all observed rows;
- `service_name` was nonblank in all observed rows;
- `agency_responsible` was nonblank in all observed rows;
- `location_type` was nonblank in all observed rows.

`comm_code` and `comm_name` had identical aggregate lexical blankness counts. `longitude`, `latitude`, and `point` also had identical aggregate lexical blankness counts. Equal aggregate counts do **not** establish that the same records are jointly blank or populated; no row-wise relationship or correlation was inspected.

#### Lexical Blankness Versus Semantic Missingness

Lexical blankness does not establish semantic missingness. A raw blank could mean value unavailable, concept not applicable, concept absent, suppressed, unknown, not populated, or another source-defined condition. A nonblank value may still be semantically unavailable, invalid, a placeholder, stale, malformed, or inappropriate for an intended analysis. No such meaning is assigned without source evidence.

#### Address Boundary

The `address` field is lexically empty in every observed row of this local artifact. This does **not** establish that Calgary has no address information, that address is absent from the authoritative source, that the field is unusable in every source version, that address data was intentionally removed or privacy-suppressed, that address is conceptually absent, or that the extract is defective. Those are competing explanations requiring further evidence.

#### Timestamp-Field Population Boundary

Observed population evidence only:

- `requested_date`: 100.000000% nonblank;
- `updated_date`: 98.958726% nonblank;
- `closed_date`: 98.951796% nonblank.

These observations do **not** establish parseability, timestamp type, precision, timezone, lifecycle meaning, temporal ordering, validity, censoring, open-case state, `created_at` mapping, or closure semantics.

#### Strict Non-Claims

This scan does **not** establish:

- semantic missingness;
- Calgary source-system nullability rules;
- source-system required-field rules;
- schema types;
- timestamp parseability;
- timestamp precision;
- temporal range;
- lifecycle semantics;
- status semantics;
- source or intake semantics;
- classification semantics;
- agency semantics;
- spatial validity;
- identifier semantics;
- canonical mappings;
- completeness;
- authoritative provenance;
- source version;
- licence;
- attribution.

A field with 100% nonblank raw strings may still contain semantically invalid or unavailable values. A field with blank raw strings may still be valid for records where the concept does not apply.

#### Increment 002 Boundary

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_LEXICAL_BLANKNESS_SCAN`.

No `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied merely because optional source fields contain raw blanks. This scan does not establish `requested_date -> Case.created_at`, `status_description -> Case.source_status`, `source -> intake/origin`, `closed_date -> Case.closed_at`, or `updated_date -> Case.updated_at`. Portability remains unvalidated.

#### Increment 003 Progress

This observation provides progress toward dataset-wide raw field-population characterization and a lexical blankness/data-quality baseline. Semantic missingness interpretation, timestamp usability, temporal coverage, lifecycle semantics, provenance, source version, licence, hash, and canonical mappings remain unverified. Increment 003 remains Planned.

### Timestamp Parseability Observation 007

**Evidence classification:** Engineering observation

On 2026-09-10, a dataset-wide lexical timestamp parseability scan was completed for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

The observed fields were `requested_date`, `updated_date`, and `closed_date`.

#### Exact Parse Rule and Method

The scan applied Python `datetime.strptime` using exactly:

    %Y/%m/%d %I:%M:%S %p

No alternate format was tried. No trimming, normalization, repair, fallback parser, or coercion was applied to nonblank values.

The scan used Python 3, Python standard-library `csv.reader`, and Python standard-library `datetime` with `encoding="ascii"` and `newline=""`. It streamed one logical CSV record at a time, retained only counters and capped failure-example lists, and did not retain rows or timestamp values.

- `TIMESTAMP_PARSEABILITY_SCAN_COMPLETED`: `true`;
- `LOGICAL_DATA_ROWS`: 7,474,403.

#### Exact Results

| Field | Blank | Whitespace-only | Parseable nonblank | Unparseable nonblank | All nonblank values parse | Failure examples |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `requested_date` | 0 | 0 | 7,474,403 | 0 | `true` | `[]` |
| `updated_date` | 77,829 | 0 | 7,396,574 | 0 | `true` | `[]` |
| `closed_date` | 78,347 | 0 | 7,396,056 | 0 | `true` | `[]` |

Accounting invariants:

- `requested_date`: `0 + 0 + 7,474,403 + 0 = 7,474,403`;
- `updated_date`: `77,829 + 0 + 7,396,574 + 0 = 7,474,403`;
- `closed_date`: `78,347 + 0 + 7,396,056 + 0 = 7,474,403`.

Zero unparseable values were observed for `requested_date`, `updated_date`, and `closed_date`. These favorable zero observations are retained as evidence.

#### Prior Scan Cross-Check

Result: `CONSISTENT_WITH_PRIOR_LEXICAL_BLANKNESS_SCAN`.

The observed blank and nonblank counts for all three fields agree exactly with the previously committed lexical blankness evidence. This is not independent semantic validation.

#### Permitted Interpretation

Every observed nonblank raw value for `requested_date`, `updated_date`, and `closed_date` in this local artifact was parseable by `datetime.strptime` using the exact format `%Y/%m/%d %I:%M:%S %p`.

This is **lexical parseability under the tested format**. It establishes technical parseability of the observed nonblank raw strings under that exact rule.

#### Lexical Format and Source-Precision Boundary

The lexical representation contains year, month, day, a 12-hour clock, minute, second, and AM/PM. Representation alone does **not** establish one-second source measurement precision, a source-system timestamp type, timezone, UTC versus local-time interpretation, DST treatment, clock accuracy, or event-time accuracy. Lexical representation precision is not automatically source-event measurement precision.

#### Blank-Value Boundary

Blank `updated_date` and `closed_date` values were observed. They are not interpreted as open, unresolved, not closed, censored, never updated, incomplete, invalid, or missing by error. The source meaning of blank timestamp fields remains unresolved.

#### Temporal and Lifecycle Non-Claims

This scan does **not** establish:

- minimum timestamp;
- maximum timestamp;
- temporal range;
- temporal ordering;
- `requested_date <= updated_date`;
- `requested_date <= closed_date`;
- `updated_date <= closed_date`;
- equality patterns;
- duration;
- request-to-closure elapsed time;
- active work;
- handling time;
- queue time;
- wait time;
- censoring;
- open-case semantics;
- closed-case semantics;
- lifecycle state;
- timestamp timezone;
- source precision;
- source-system type;
- canonical mapping.

#### Canonical-Mapping and Increment 002 Boundary

Parseability is insufficient for semantic mapping. This observation does not establish `requested_date -> Case.created_at`, `updated_date -> Case.updated_at`, or `closed_date -> Case.closed_at`. Increment 002 rejected generic universal `updated_at` and `closed_at` concepts; this observation does not reintroduce them.

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_TIMESTAMP_PARSEABILITY_SCAN`.

No observed `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied. Portability remains unvalidated.

#### Increment 003 Progress

This observation provides progress toward timestamp lexical usability and consistency of the observed timestamp string format. Timestamp semantics, timezone, source precision, temporal coverage, temporal ordering, lifecycle interpretation, censoring analysis, provenance, source version, licence, hash, and canonical mappings remain unverified. Increment 003 remains Planned.

### Temporal Extrema Observation 008

**Evidence classification:** Engineering observation

On 2026-09-10, a dataset-wide temporal-extrema scan was completed for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

The observed fields were `requested_date`, `updated_date`, and `closed_date`.

#### Exact Parse Rule and Method

The scan used:

- Python 3;
- Python standard-library `csv.reader`;
- Python standard-library `datetime.strptime`;
- `encoding="ascii"`;
- `newline=""`;
- streaming iteration over one logical CSV record at a time;
- retention of only counters plus the current minimum and maximum values.

It did not retain all rows or timestamp values. The exact parse format was:

    %Y/%m/%d %I:%M:%S %p

Parsed values were naive `datetime` values used only for within-field extrema comparison. No timezone was assigned.

- `TEMPORAL_EXTREMA_SCAN_COMPLETED`: `true`;
- `LOGICAL_DATA_ROWS`: 7,474,403.

#### Exact Results

| Field | Blank | Parseable nonblank | Minimum raw | Minimum parsed | Maximum raw | Maximum parsed |
| --- | ---: | ---: | --- | --- | --- | --- |
| `requested_date` | 0 | 7,474,403 | `'2010/01/25 12:00:00 AM'` | `2010-01-25 00:00:00` | `'2026/09/08 12:00:00 AM'` | `2026-09-08 00:00:00` |
| `updated_date` | 77,829 | 7,396,574 | `'2012/01/01 02:11:34 AM'` | `2012-01-01 02:11:34` | `'2026/09/08 12:00:00 AM'` | `2026-09-08 00:00:00` |
| `closed_date` | 78,347 | 7,396,056 | `'2010/02/17 12:00:00 AM'` | `2010-02-17 00:00:00` | `'2026/09/09 12:00:00 AM'` | `2026-09-09 00:00:00` |

Accounting invariants:

- `requested_date`: `0 + 7,474,403 = 7,474,403`;
- `updated_date`: `77,829 + 7,396,574 = 7,474,403`;
- `closed_date`: `78,347 + 7,396,056 = 7,474,403`.

#### Prior Evidence Consistency

Result: `CONSISTENT_WITH_PRIOR_TIMESTAMP_PARSEABILITY_SCAN`.

The blank and parseable-nonblank counts agree exactly with the already committed timestamp-parseability scan. This is count consistency only, not independent semantic validation.

#### External Preparation Comparison

Result: `CORROBORATES_REPORTED_REQUESTED_DATE_EXTREMA`.

The observed `requested_date` calendar extrema, `2010-01-25` and `2026-09-08`, exactly match the dates retained in the earlier external/preparation context. This is corroboration only. It does not establish authoritative provenance, an authoritative observation period, artifact completeness, or equivalence to a current authoritative source. The external report was not compared with `updated_date` or `closed_date`.

#### Permitted Interpretation

Result: `OBSERVED PARSED TEMPORAL EXTREMA`.

Among the observed parseable nonblank raw values in this local artifact, the recorded minimum and maximum values are the observed parsed extrema for each respective field under the tested format. They are not established as lifecycle boundaries, case observation boundaries, or authoritative dataset boundaries.

#### Observation-Window Boundary

The `requested_date` minimum and maximum are observed extrema of that raw field in this local artifact. They do **not** establish the authoritative Calgary observation window, the complete service-request history, the valid analytical cohort window, or the appropriate metric observation boundary. Those require source and analytical-contract evidence.

#### Cross-Field, Ordering, and Duration Boundaries

The extrema of one timestamp field were not compared with those of another, and no inference is made from differences among the three fields. The scan did not inspect or establish `requested_date <= updated_date`, `requested_date <= closed_date`, or `updated_date <= closed_date`, did not count temporal-order violations, and did not establish lifecycle consistency.

No extrema or field values were subtracted. The scan did not calculate elapsed days, elapsed hours, dataset span, request-to-closure time, handling time, active work, queue time, or waiting time.

#### Blank-Value Boundary

Blank `updated_date` and `closed_date` values remain semantically uninterpreted. They are not classified as open, unresolved, censored, never updated, incomplete, or invalid.

#### Timezone and Precision Boundary

The parsed values are naive `datetime` values. This observation does not establish timezone, UTC or Calgary-local-time interpretation, DST behavior, one-second source precision, clock accuracy, or event-time accuracy.

#### Canonical-Mapping and Increment 002 Boundary

Observed extrema provide no additional semantic justification for `requested_date -> Case.created_at`, `updated_date -> Case.updated_at`, or `closed_date -> Case.closed_at`. Those mappings are not established, and Increment 002's universal-field boundaries remain unchanged.

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_TEMPORAL_EXTREMA_SCAN`.

No `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied. Portability remains unvalidated.

#### Strict Non-Claims and Increment Progress

This scan does **not** establish:

- an authoritative observation window;
- lifecycle semantics;
- cross-field ordering;
- duration or request-to-closure elapsed duration;
- active work, handling time, queue time, or waiting time;
- censoring or open/closed semantics;
- midnight prevalence;
- timezone or source precision;
- canonical mappings;
- artifact completeness;
- authoritative provenance;
- source version;
- licence;
- attribution.

This observation provides progress toward temporal coverage characterization at the raw-field level and observed timestamp extrema. Temporal ordering, lifecycle interpretation, censoring, analytical observation-window definition, provenance, source version, licence, hash, and canonical mappings remain unverified. Increment 003 remains Planned.

### Pairwise Temporal Relationship Observation 009

**Evidence classification:** Engineering observation

On 2026-09-10, a dataset-wide pairwise temporal relationship scan was completed for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

The scan compared `requested_date` with `updated_date`, `requested_date` with `closed_date`, and `updated_date` with `closed_date`. Comparisons used naive parsed `datetime` values only, under the exact format:

    %Y/%m/%d %I:%M:%S %p

#### Scan Method

The scan used:

- Python 3;
- Python standard-library `csv.reader`;
- Python standard-library `datetime.strptime`;
- `encoding="ascii"`;
- `newline=""`;
- streaming iteration over one logical CSV record at a time;
- retention of only counters and at most ten `LEFT_GT_RIGHT` examples per pair.

It did not retain all rows or parsed timestamps. Retained examples were not enriched with identifiers, status, `service_name`, source, agency, or location.

- `TEMPORAL_RELATION_SCAN_COMPLETED`: `true`;
- `LOGICAL_DATA_ROWS`: 7,474,403.

#### Measurement Model

For each pair, every logical row was assigned to exactly one category:

- `BOTH_BLANK`;
- `LEFT_BLANK_ONLY`;
- `RIGHT_BLANK_ONLY`;
- `LEFT_LT_RIGHT`;
- `LEFT_EQ_RIGHT`;
- `LEFT_GT_RIGHT`.

For each pair, `BOTH_NONBLANK = LEFT_LT_RIGHT + LEFT_EQ_RIGHT + LEFT_GT_RIGHT`. `LEFT_GT_RIGHT` is an observed comparison category, not an ordering violation.

#### Exact Pairwise Results

| Pair | Both blank | Left blank only | Right blank only | Both nonblank | Left < right | Left = right | Left > right |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `requested_date` vs `updated_date` | 0 | 0 | 77,829 | 7,396,574 | 6,769,218 | 626,425 | 931 |
| `requested_date` vs `closed_date` | 0 | 0 | 78,347 | 7,396,056 | 6,605,371 | 789,758 | 927 |
| `updated_date` vs `closed_date` | 31 | 77,798 | 78,316 | 7,318,258 | 146,846 | 5,954,904 | 1,216,508 |

All pairwise accounting invariants passed. For every pair:

    BOTH_BLANK
    + LEFT_BLANK_ONLY
    + RIGHT_BLANK_ONLY
    + LEFT_LT_RIGHT
    + LEFT_EQ_RIGHT
    + LEFT_GT_RIGHT
    = 7,474,403

#### Retained `requested_date` Versus `updated_date` Examples

The scan retained these ten `LEFT_GT_RIGHT` examples, containing only the logical data-row number and the two raw timestamps:

| Logical data row | Left raw | Right raw |
| ---: | --- | --- |
| 21019 | `'2019/09/06 01:19:07 PM'` | `'2019/09/06 12:19:13 PM'` |
| 53623 | `'2019/11/12 10:33:24 AM'` | `'2019/11/12 09:33:24 AM'` |
| 53625 | `'2019/11/12 10:33:51 AM'` | `'2019/11/12 09:33:51 AM'` |
| 53627 | `'2019/11/12 10:34:37 AM'` | `'2019/11/12 09:34:36 AM'` |
| 53633 | `'2019/11/12 10:39:00 AM'` | `'2019/11/12 09:38:58 AM'` |
| 53636 | `'2019/11/12 10:39:23 AM'` | `'2019/11/12 09:39:22 AM'` |
| 53638 | `'2019/11/12 10:39:54 AM'` | `'2019/11/12 09:39:53 AM'` |
| 53648 | `'2019/11/12 10:40:32 AM'` | `'2019/11/12 09:40:31 AM'` |
| 53649 | `'2019/11/12 10:40:49 AM'` | `'2019/11/12 09:40:50 AM'` |
| 53652 | `'2019/11/12 10:41:34 AM'` | `'2019/11/12 09:41:33 AM'` |

The ten retained `LEFT_GT_RIGHT` examples for `requested_date` versus `closed_date` were the same ten logical-row/raw-timestamp triples. No reason for this observation is inferred.

#### Retained `updated_date` Versus `closed_date` Examples

The scan retained these ten `LEFT_GT_RIGHT` examples, containing only the logical data-row number and the two raw timestamps:

| Logical data row | Left raw | Right raw |
| ---: | --- | --- |
| 12 | `'2020/09/04 12:00:00 AM'` | `'2020/07/02 12:00:00 AM'` |
| 13 | `'2020/01/30 12:00:00 AM'` | `'2017/06/12 12:00:00 AM'` |
| 20 | `'2012/07/19 07:50:54 PM'` | `'2012/07/19 07:32:41 PM'` |
| 26 | `'2012/07/30 02:06:40 PM'` | `'2012/07/20 11:29:49 PM'` |
| 30 | `'2020/09/04 12:00:00 AM'` | `'2020/08/20 12:00:00 AM'` |
| 32 | `'2020/09/04 12:00:00 AM'` | `'2020/09/02 12:00:00 AM'` |
| 34 | `'2020/11/04 12:00:00 AM'` | `'2020/10/29 12:00:00 AM'` |
| 37 | `'2020/11/20 12:00:00 AM'` | `'2020/10/26 12:00:00 AM'` |
| 59 | `'2020/09/04 12:00:00 AM'` | `'2020/08/24 12:00:00 AM'` |
| 61 | `'2024/05/18 12:00:00 AM'` | `'2021/02/23 12:00:00 AM'` |

#### Prior Evidence Consistency

Result: `CONSISTENT_WITH_PRIOR_TIMESTAMP_POPULATION_EVIDENCE`.

For every pair, `BOTH_BLANK + LEFT_BLANK_ONLY` reproduced the previously committed left-field blank count, and `BOTH_BLANK + RIGHT_BLANK_ONLY` reproduced the previously committed right-field blank count. This is accounting consistency only.

#### Permitted Interpretation

Result: `OBSERVED PAIRWISE TEMPORAL RELATIONSHIPS`.

For rows where each timestamp pair was jointly nonblank and parseable, the recorded counts describe whether the left naive parsed value was less than, equal to, or greater than the right naive parsed value. None of these relationships is characterized normatively.

Among the 7,318,258 rows where `updated_date` and `closed_date` were both nonblank and parseable, 146,846 had `updated_date < closed_date`, 5,954,904 had `updated_date = closed_date`, and 1,216,508 had `updated_date > closed_date`. This pattern is not explained. The 1,216,508 rows are not classified as invalid, erroneous, inconsistent, violations, anomalies, or bad data. Possible explanations require source semantics and are not inferred here.

#### Expectation and Ordering Boundary

Field names alone do not establish an expected lifecycle ordering. This scan does **not** establish that `requested_date` must precede `updated_date`, `requested_date` must precede `closed_date`, or `updated_date` must precede `closed_date`. `LEFT_GT_RIGHT` remains an empirical relation category only.

#### Duration, Blank-Value, Timezone, and Precision Boundaries

Timestamps were not subtracted. This observation does not calculate or establish elapsed time, duration, request-to-closure duration, case age, active work, handling time, queue time, waiting time, or temporal distance between retained examples.

Rows not jointly nonblank were accounted for explicitly. They are not interpreted as open, unresolved, censored, incomplete, or invalid.

Comparisons used naive `datetime` values. This observation does not establish timezone, UTC or Calgary-local-time interpretation, DST behavior, source measurement precision, clock accuracy, or event-time accuracy.

#### Canonical-Mapping and Increment 002 Boundary

Pairwise temporal relationships do not provide sufficient source-semantic evidence for `requested_date -> Case.created_at`, `updated_date -> Case.updated_at`, or `closed_date -> Case.closed_at`. Those mappings are not established, and Increment 002's universal-field boundary remains unchanged.

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_TEMPORAL_RELATION_SCAN`.

No `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied based solely on these timestamp relationships. Portability remains unvalidated.

#### Strict Non-Claims and Increment Progress

This scan does **not** establish:

- source lifecycle semantics;
- expected lifecycle ordering;
- ordering violations;
- data-quality invalidity;
- temporal validity;
- durations, resolution time, or request-to-closure elapsed duration;
- active work, handling time, queue time, or waiting time;
- censoring or open/closed semantics;
- analytical eligibility;
- timezone or source precision;
- canonical mappings;
- authoritative completeness or authoritative provenance;
- source version;
- licence;
- attribution.

This observation provides progress toward row-level temporal relationship characterization and timestamp evidence-quality characterization. Lifecycle semantics, expected ordering, duration eligibility, censoring, analytical observation-window definition, provenance, source version, licence, hash, and canonical mappings remain unverified. Increment 003 remains Planned.

### Local-Artifact SHA-256 Observation 010

**Evidence classification:** `ENGINEERING OBSERVATION: LOCAL ARTIFACT IDENTITY`

On 2026-09-10, a SHA-256 digest was computed successfully for the observed local artifact:

    /data/repos/Public Datasets/calgary_311.csv

Observed artifact identity values:

- byte size: 1,978,541,467 bytes;
- SHA-256: `9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f`;
- hash command completed successfully: `true`;
- path returned by `sha256sum`: `/data/repos/Public Datasets/calgary_311.csv`.

#### Permitted Interpretation

At the time of inspection, the observed local artifact at `/data/repos/Public Datasets/calgary_311.csv` had byte size 1,978,541,467 and SHA-256 digest `9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f`.

The digest identifies the exact observed local byte content. It may be used prospectively to identify the artifact to which later repository evidence refers.

#### Retroactivity Boundary

The SHA-256 was established after the earlier Increment 003 inspections. Therefore:

- the hash can prospectively identify this local artifact;
- it does **not** prove that earlier observations were cryptographically bound to this digest at the time they were collected;
- it does **not** retroactively establish source provenance.

#### Cryptographic Identity Boundary

Artifact byte identity is distinct from artifact authenticity, source provenance, and semantic correctness. A cryptographic digest identifies bytes; it does not prove what those bytes mean or where they came from.

The SHA-256 does **not** establish:

- that the file originated from the City of Calgary;
- authoritative provenance;
- authenticity;
- completeness;
- correctness;
- currentness;
- source ownership;
- source publication date;
- source version semantics;
- equivalence to the current authoritative source;
- licence;
- attribution;
- semantic validity;
- field correctness;
- canonical mappings.

#### Prior File-Size Consistency

Result: `CONSISTENT_WITH_PRIOR_FILESYSTEM_SIZE_OBSERVATION`.

The earlier filesystem observation and the hash inspection each observed a size of 1,978,541,467 bytes. This is consistency of the observed local file size only. It does not prove that the file was unchanged between observations. The earlier observation did not include a cryptographic digest, so byte identity across the two observation times was not established.

#### Increment 002 Boundary

Result: `NO_INCREMENT_002_CONFLICT_OBSERVED_IN_ARTIFACT_IDENTITY_HASH`.

No `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` classification is applied. The hash provides no semantic evidence about the canonical Case contract. Portability remains unvalidated.

#### Increment 003 Progress

This observation provides progress toward local artifact identification, reproducibility, and evidence binding. Authoritative provenance, authenticity, source-version verification, licence, attribution, source semantics, and canonical mappings remain unverified. Increment 003 remains Planned.

## Artifacts

Planned increment record:

    docs/increments/003-calgary-source-evidence-validation.md

No empirical evidence artifact exists yet.

## Commit

Not yet committed.

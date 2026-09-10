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

## Artifacts

Planned increment record:

    docs/increments/003-calgary-source-evidence-validation.md

No empirical evidence artifact exists yet.

## Commit

Not yet committed.

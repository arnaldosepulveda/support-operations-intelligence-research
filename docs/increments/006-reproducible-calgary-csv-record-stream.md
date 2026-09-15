# Increment 006 - Reproducible Calgary CSV Record Stream

Status: Planned

Opened: 2026-09-13

Completed: Not completed

## Objective

Implement and verify a deterministic, lazy, standard-library Calgary CSV
record-stream boundary that converts a specifically identified local CSV
artifact into already-parsed source-record mappings compatible with the
existing `adapt_calgary_record` boundary, without introducing persistence,
analytics, or new source semantics.

This increment is about:

    source file
        -> parsed source-row Mapping

It is NOT about:

    parsed Mapping
        -> canonical semantics

Increment 005 already owns the latter boundary and remains unchanged and
authoritative.

## Why This Increment Exists

Increment 005 established, and closed, the following executable boundary:

```text
already-parsed Mapping
    -> identity admission
    -> RejectedIdentity
       OR
    -> CalgaryMappedCase
    -> CalgarySourceNativeEvidence
    -> CalgaryAdaptedCase
    -> CalgaryAdapterResult
```

`adapt_calgary_record(record: Mapping[str, object]) -> CalgaryAdapterResult`
has been tested exclusively against small, hand-constructed in-memory
`dict` fixtures. No code in the repository has ever read a row from the
actual retained Calgary source file. There is currently no deterministic,
reproducible, executable path from the bound local CSV artifact to the
`Mapping[str, object]` shape that boundary consumes.

The missing evidence-chain link is therefore:

    EXECUTABLE CONFORMANCE
        -> REPRODUCIBLE DATA ACCESS

This increment plans to close that specific link. It does not claim
reproducible data access already exists, and it does not claim the link
will be fully closed until its own acceptance criteria are independently
satisfied and reviewed.

## Starting State

Increment 003:

    Calgary source evidence validation
    Complete

Increment 004:

    Calgary source contract
    Complete

Increment 005:

    executable Calgary adapter
    Complete

Current canonical checkpoint:

    ba9bf5ec57c87354fd78b04122c729fee0594a27

Current adapter input boundary:

    Mapping[str, object]

Current test suite at Increment 005 closure:

    125 tests passing

Current `pyproject.toml`:

    dependencies = []

No PostgreSQL exists in the repository. No persistence exists. No
analytical metric exists. No dataset-wide adapter execution has occurred
anywhere in the committed repository history.

## Source Artifact Binding

Increment 003 recorded the following local artifact evidence:

    local observed path:
        /data/repos/Public Datasets/calgary_311.csv

    recorded size:
        1,978,541,467 bytes

    prospectively recorded SHA-256:
        9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f

    observed logical row count:
        7,474,403

    observed field-count distribution:
        {15: 7,474,403}

The filesystem path above is an environment-specific execution location.
It must NOT become a hard-coded application path. The future
implementation must accept a `Path` (or equivalent explicit path value) as
an argument; the record-stream boundary itself must not embed any default
or fallback absolute path.

The recorded SHA-256 above is the expected artifact binding for future
local verification only. Increment 006 planning does NOT claim that the
current file has already been re-hashed or revalidated during this
planning step. No dataset content was inspected and no hash was
recomputed while writing this document.

Before any bounded execution against the real local artifact, a future
implementation step must verify the current artifact digest against the
recorded SHA-256. A mismatch must block any claim of execution against the
previously bound artifact; it must not be silently ignored or downgraded
to a warning.

This binding must NOT be strengthened into:

- an authoritative Calgary version;
- an official immutable source snapshot;
- confirmed acquisition provenance;
- historical source-version identity.

Those remain unresolved limitations explicitly inherited from Increment
003's Completion Review (`BLOCKED_BY_UNAVAILABLE_EVIDENCE` for provenance),
and Increment 006 does not attempt to resolve them. A digest match
establishes only that the currently present local bytes match the bytes
Increment 003 previously hashed; it does not establish official version,
licence-bound acquisition, or acquisition lineage.

## Expected Local CSV Header

Increment 003 observed the following 15-field local header, in this exact
order:

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

This exact local header is the planned structural input contract for the
bound artifact. It must not be reinterpreted.

The record stream may expose all 15 source fields as raw lexical strings.
That does not mean all 15 become canonical Case fields. The Increment
004/005 deferrals remain authoritative and unchanged:

- `requested_date` remains `created_at: DEFER_MAPPING`;
- `status_description` remains mapped only to `source_status` (Increment
  005 behavior, unchanged);
- `canonical_status` has no source mapping and remains `DEFER_MAPPING`;
- `source`, `service_name`, `agency_responsible`, `updated_date`,
  `closed_date` remain `RETAIN_SOURCE_NATIVE` lexical evidence only
  (Increment 005 behavior, unchanged);
- `address`, `comm_code`, `comm_name`, `location_type`, `longitude`,
  `latitude`, `point` remain DQ13 fields, `DEFER_MAPPING`.

## Planned Execution Boundary

The planned boundary, conceptually:

```text
Path
    -> CSV text stream
    -> validated header
    -> lazy sequence of parsed source-row mappings
```

Each yielded row should be compatible with:

```python
adapt_calgary_record(record: Mapping[str, object])
```

If a function shape is proposed at implementation time, the preferred
minimal shape is:

```python
def iter_calgary_csv_records(
    path: Path,
) -> Iterator[Mapping[str, object]]:
    ...
```

This is a Design choice / planned decision only. No such function exists
in the repository yet. The exact function name, module location, and
signature remain subject to normal implementation-time review; this
document does not freeze them beyond the minimal shape above.

This boundary must not include database or analytics concerns of any
kind.

## Laziness / Memory Boundary

The record-stream implementation must be lazy. It must not require
materializing the approximately 7.47-million-row CSV into memory before
producing records.

A consumer should be able to use `itertools.islice(...)`, or an
equivalent external iteration mechanism, to inspect a bounded number of
records without the implementation itself needing a dedicated production
"limit" parameter. No such limit parameter is planned unless a later,
separately justified design step demonstrates an actual need for one.

## Lexical Fidelity

CSV parsing at this boundary must preserve source cell text exactly as
supplied by the CSV parser. The record-stream layer must NOT perform:

- stripping;
- case normalization;
- numeric conversion;
- timestamp parsing;
- timezone conversion;
- canonical-status conversion;
- missing-value semantic classification.

Those responsibilities either belong to the existing, unchanged Increment
005 adapter (`map_calgary_source_status`,
`map_calgary_source_native_evidence`), or remain explicitly unresolved.

In particular, a cell value such as `"  Mobile App  "` must not silently
become `"Mobile App"` at the record-stream boundary. The record-stream
layer's only job is to hand the adapter the exact lexical string the CSV
parser returned for that cell.

## CSV Structural Validation

Structural validation is in scope. The plan is to verify:

1. the header matches the expected 15-field local header exactly;
2. header order is preserved and validated, not merely set-compared;
3. malformed rows with too many columns are not silently accepted;
4. malformed rows with too few columns are not silently accepted;
5. any other unexpected structural shape fails explicitly rather than
   being coerced into a best-effort mapping;
6. source values are not normalized in any way that would make malformed
   structural data appear structurally valid.

This is parser/source-structure conformance only. It must not become
analytical data-quality profiling (missingness rates, distribution
characterization, or similar); Increment 003 already performed that kind
of profiling separately, and any further such profiling belongs to a
later, separately justified increment.

## Encoding / Newline Design

The implementation must use an explicit text encoding and explicit CSV
newline handling rather than relying on platform defaults.

Increment 003 observed the retained local artifact as ASCII-compatible
(`file` utility classification `CSV ASCII text`) and successfully iterated
it whole-file using Python standard-library `csv.reader` with
`encoding="ascii"` and `newline=""`. A future Increment 006 implementation
design may reuse an explicit, UTF-8-compatible text-opening mode with
newline handling appropriate for Python's `csv` module, informed by that
prior observation.

This document does not claim that encoding behavior has been implemented
by Increment 006. Increment 003's prior observation is cited here only as
starting evidence that an explicit, reproducible encoding/newline
configuration was previously demonstrated to be sufficient for this exact
artifact under that scan; it is not a claim that Increment 006 has
verified it again.

## Scope

Increment 006 may:

- implement source-specific Calgary CSV record streaming;
- require an explicit file-path input, never a hard-coded path;
- implement structural header validation;
- implement malformed row-width detection;
- preserve source-cell lexical values exactly;
- implement lazy row iteration;
- use the Python standard library only;
- add synthetic automated test fixtures (temporary CSV files, not copied
  Calgary rows);
- add a separately bounded real-artifact smoke verification, gated on a
  digest match;
- verify compatibility with the existing, unchanged
  `adapt_calgary_record` boundary;
- retain reproducibility evidence for this bounded execution path.

## Non-Goals

This increment will not implement or define:

- PostgreSQL;
- persistence;
- schema migrations;
- ORM work;
- CSV-to-database loading;
- dataset-wide analytical execution;
- operational metrics;
- duration computation;
- observation-window definition;
- censoring policy;
- dashboards;
- APIs;
- a UI;
- Docker;
- CI expansion, unless separately justified;
- a ServiceNow adapter;
- a generic cross-source ingestion framework;
- `created_at` mapping;
- `canonical_status` mapping;
- DQ13 canonical mapping;
- timestamp parsing;
- timezone inference;
- any Calgary source-semantic revision;
- AI, LLM, RAG, or agent behavior;
- production readiness.

## Assumptions

- Increment 003's recorded local-artifact observations remain the
  starting evidence for this plan; they are not automatically treated as
  current, re-verified observations.
- Increment 004 remains the controlling Calgary mapping contract and is
  not reopened by this increment.
- Increment 005 remains the controlling already-parsed-record adapter and
  is not modified by this increment.
- Python standard-library `csv` support is sufficient for this
  increment's intended parser boundary; no third-party CSV or data-frame
  library is assumed necessary.
- The local CSV itself is not, and will not be, committed to the
  repository.
- Automated tests must remain runnable without that local CSV present.

## Threat Model / Failure Modes

- wrong local file supplied to the boundary;
- digest mismatch between the current local file and the recorded SHA-256;
- header drift (added, removed, or renamed columns);
- reordered header (same field names, different positions);
- extra columns in a data row;
- missing columns in a data row;
- other malformed CSV structure;
- encoding failure or silent mis-decoding;
- accidental normalization of source lexical values;
- accidental type conversion (numeric, boolean, or otherwise);
- accidental timestamp parsing of `requested_date`, `updated_date`, or
  `closed_date`;
- eager whole-file materialization defeating the laziness requirement;
- hidden dependency on a local absolute path baked into application code;
- automated tests silently requiring the private 1.9 GB artifact to pass;
- accidental scope expansion into persistence or analytics;
- bounded smoke evidence being misrepresented as dataset-wide validation.

Malformed structural input (wrong column count, wrong header) must not be
conflated with semantic source-data quality (blank fields, unusual but
structurally valid values); the former is this increment's concern, the
latter is not.

## Planned Implementation Sequence

1. Design the explicit-path, lazy record-stream boundary shape and the
   header/row-width validation rules, without writing implementation
   code in this planning document.
2. Implement the boundary using only the Python standard library.
3. Add synthetic-fixture automated tests (temporary CSV files) covering
   the acceptance criteria below.
4. Separately implement the digest-verification precondition for
   real-artifact use.
5. Perform one bounded real-artifact smoke run, gated on a digest match,
   consuming a small number of records via `itertools.islice` or
   equivalent.
6. Record actual (not assumed) test and smoke results in an Implementation
   Record, following the style established in Increments 004 and 005.

No implementation work is performed by this planning document itself.

## Planned Test Categories

- header validation (matching header; header with wrong field names;
  header with wrong field order);
- lazy row iteration over a small synthetic multi-row CSV;
- lexical preservation (padded values, punctuation, empty cells) at the
  record-stream layer;
- laziness / bounded consumption (e.g., via `itertools.islice` over a
  larger synthetic file without fully materializing it);
- extra-column malformed row rejection;
- missing-column malformed row rejection;
- empty source cell values preserved as empty strings at the parser
  layer (semantic interpretation remains the adapter's responsibility,
  unchanged from Increment 005);
- composition: a record yielded by the stream, when passed to
  `adapt_calgary_record`, produces the same result as an equivalent
  hand-built `dict` fixture;
- explicit path argument (no implicit default path is honored);
- absence of any normalization, stripping, or type coercion at this
  layer;
- digest-verification precondition (match vs. mismatch behavior), using a
  synthetic file and a synthetic recorded digest, not the real artifact;
- bounded real-artifact smoke path, exercised separately from the
  automated suite and gated on digest match.

No exact test count is finalized here. The eventual Implementation Record
must report the actual count and actual results; this document must not
be later edited to pretend a specific count was predicted in advance
beyond what is written above.

## Acceptance Criteria

Increment 006 is complete only when:

1. A source-specific CSV record-stream boundary exists and accepts an
   explicit path argument rather than a hard-coded local path.
2. The expected 15-field local header is validated exactly, including
   field order.
3. Valid CSV rows are yielded lazily as mappings compatible with
   `adapt_calgary_record`.
4. Source cell strings are preserved without parser-layer normalization
   or semantic type conversion.
5. The implementation does not load the complete source file into memory
   before yielding rows.
6. Extra-column rows fail explicitly rather than being silently accepted
   or truncated.
7. Missing-column rows fail explicitly rather than being silently
   accepted or padded.
8. Header mismatch (wrong fields or wrong order) fails explicitly.
9. Synthetic automated tests do not depend on the external 1.9 GB file.
10. Synthetic row mappings compose with `adapt_calgary_record` without
    requiring any change to Increment 005 semantics.
11. No new third-party dependency is introduced.
12. Before real-artifact smoke execution, the local file digest is
    checked against Increment 003's recorded SHA-256.
13. A matching artifact supports a bounded local smoke run through the
    record-stream boundary.
14. A digest mismatch blocks any claim that the current local file is the
    prospectively bound Increment 003 artifact.
15. No Increment 004 or Increment 005 semantic decision is silently
    revised.
16. Automated tests pass.
17. `git diff --check` passes before closure.

## Failure Criteria

The increment cannot close if any of the following occurs:

- a hard-coded local Calgary path appears in application logic;
- the parser silently accepts header drift;
- the parser silently accepts row-width mismatch;
- the parser strips or normalizes source strings;
- the parser converts timestamps or numbers semantically;
- the whole file is eagerly loaded as the only supported execution model;
- automated tests require the external 1.9 GB dataset to pass;
- a digest mismatch is ignored or downgraded to a non-blocking warning;
- PostgreSQL or another persistence layer enters scope;
- analytics or metrics enter scope;
- `created_at`, `canonical_status`, or a DQ13 field is silently mapped;
- a generic ingestion framework is introduced without demonstrated
  cross-source need;
- a bounded smoke execution is described as dataset-wide validation;
- authoritative provenance or source-version claims are inferred merely
  from a local digest match;
- a new dependency appears without an explicit, separately justified
  design decision;
- automated tests do not pass at closure;
- `git diff --check` fails at closure.

## Claim Classification

This document is a planning/design record. Its contents are:

    Design choices / planned decisions:
        record-stream boundary shape, header/row-width validation rules,
        laziness requirement, lexical-fidelity requirement,
        encoding/newline design intent, digest-verification precondition,
        test strategy

Planned tests listed in this document are not Engineering observations.

Increment 003's prior citations (local artifact size, SHA-256, header,
row count, encoding/newline configuration, whole-file parseability under
that configuration) are prior Engineering observations, cited here as
starting evidence, not re-established by this document.

Writing this plan produces no new External evidence, Internal evaluation
result, or Research conclusion.

## Proposed Claim Boundary

If Increment 006 is later implemented and its acceptance criteria pass, a
permitted claim would be approximately:

> A deterministic, lazy, source-specific boundary can read the verified
> local Calgary CSV artifact and produce source-row mappings compatible
> with the existing Calgary adapter for tested synthetic inputs and a
> bounded execution against the digest-matched local artifact.

This must not be interpreted as:

- full-dataset ingestion correctness;
- authoritative Calgary source-version provenance;
- persistence correctness;
- analytical correctness;
- temporal-semantic validity;
- operational findings;
- production readiness;
- portability to other sources;
- a research conclusion.

## Reproducibility Requirements

At closure, Increment 006 should retain, where applicable:

- the repository commit;
- the Python version;
- the repository-local interpreter used;
- confirmation of the no-new-third-party-dependency state;
- the parser design decisions actually made;
- the expected header contract actually validated;
- the synthetic test-fixture definitions used;
- the exact test commands used;
- the actual observed test results;
- the real-artifact path used for the local smoke run;
- the expected SHA-256;
- the observed SHA-256 comparison result;
- the bounded smoke command used;
- the number of records consumed in the bounded smoke run;
- the observed smoke result;
- negative and malformed-input test evidence;
- any remediation lineage, if applicable.

This planning record does not claim clean-machine or production
reproducibility. It claims only that, if implemented as planned, the
above evidence would be retained for repository-local reproduction.

## What This Increment Enables

If completed, Increment 006 would make a reproducible source-record
stream available for later, separately justified increments. Possible
later work may include:

- a durable or persistent data representation;
- PostgreSQL loading;
- analytical-contract development;
- data-quality characterization at dataset scale;
- operational baseline analysis.

None of those future increments is authorized, started, or pre-numbered
by this document.

## What Remains Premature

Explicitly retained as premature, both for this planning document and for
any Increment 006 implementation:

- PostgreSQL;
- analytical metrics;
- duration analysis;
- censoring decisions;
- operational findings;
- workflow diagnosis;
- ServiceNow integration;
- AI intervention;
- dashboarding;
- production deployment.

## Known Repository Documentation Issue

`README.md` currently contains stale "Current State" language from the
foundation phase (it still describes the repository as being "in its
foundation increment" and lists source adapters/contracts and canonical
models as "Not implemented yet," which is no longer accurate after
Increments 002-005). This is a documentation-hygiene issue separate from
this increment's objective. `README.md` was not modified by this planning
document, and README cleanup is explicitly not part of Increment 006's
implementation objective.

## Current Status

Increment 006 is:

    Status: Planned

No implementation has occurred. No source file was read during Increment
006 planning. No current SHA-256 verification was performed during
Increment 006 planning. No test has been written or executed for
Increment 006. No dependency has been installed. No design choice in this
document is presented as an Engineering observation.

## Implementation Record 001 - CSV Record-Stream Boundary and Structural Failure Semantics

Classification:

    Design choice / planned decision

This record freezes a planned parser interface and its expected structural-
failure semantics before implementation. No implementation has occurred. The
decisions below are not Engineering observations, External evidence, Internal
evaluation results, or Research conclusions.

### Parser Mechanism

Decision:

    USE_STANDARD_LIBRARY_CSV_READER_WITH_EXPLICIT_WIDTH_VALIDATION

The planned implementation will use `csv.reader`, not `csv.DictReader`.
`csv.DictReader` can represent malformed row widths through `None` keys for
extra cells or missing values for absent cells. That representation risks
silently normalizing the exact extra-column and missing-column conditions that
this increment requires to fail explicitly. Reading rows as sequences keeps
structural validation separate from mapping construction.

The parser must:

1. read the header first;
2. compare it exactly and positionally with the committed 15-field header;
3. reject a mismatch before yielding any record;
4. read each subsequent row as a sequence of source strings;
5. require exactly 15 cells;
6. reject fewer than 15 cells;
7. reject more than 15 cells; and
8. construct a mapping only after width validation succeeds.

This record specifies planned behavior only; it does not claim that the
behavior is implemented.

### Planned Public Input and Return Boundary

The planned public boundary is:

```python
def iter_calgary_csv_records(
    path: Path,
) -> Iterator[Mapping[str, str]]:
    ...
```

`path` must be supplied explicitly as a `Path`. The Calgary artifact path must
not be hard-coded or supplied through an implicit default.

`Iterator[Mapping[str, str]]` is the narrow truthful return representation:
every structurally valid cell at this parser boundary is source text, including
an empty string. `Mapping[str, str]` is compatible with the existing
`adapt_calgary_record(record: Mapping[str, object])` input boundary because
string values are objects and the mapping is read-only at the declared
boundary.

The earlier `Iterator[Mapping[str, object]]` wording under Planned Execution
Boundary remains retained as planning evidence. This record deliberately
refines that earlier conceptual representation to the narrower
`Iterator[Mapping[str, str]]`; it does not silently rewrite the earlier plan.

### Text Opening Boundary

The planned file-opening boundary is:

```python
path.open(
    mode="r",
    encoding="utf-8",
    newline="",
)
```

The encoding must not depend on a platform default. `newline=""` is the
documented Python `csv`-module text boundary. Increment 003's observation that
the retained artifact was ASCII-compatible makes UTF-8 a bounded compatible
choice for this planned parser. This decision does not claim that UTF-8 is
correct for every possible future Calgary artifact.

### Exact Header Boundary

The implementation will define one source-specific constant containing this
exact 15-field header in this exact order:

```text
service_request_id
requested_date
updated_date
closed_date
status_description
source
service_name
agency_responsible
address
comm_code
comm_name
location_type
longitude
latitude
point
```

The header comparison is exact and positional. An empty file or absent header
and any renamed, added, removed, or reordered header field must fail before the
generator yields a record. This constant is Calgary-source-specific and must
not be generalized into a cross-source schema framework.

### Expected Structural Failure Transport

Expected violations of the Calgary CSV structural contract will cross the
parser boundary as a narrow source-specific exception:

    CalgaryCsvStructureError

The exception will carry an explicit reason enum with these minimum reasons:

    EMPTY_FILE_OR_MISSING_HEADER
    HEADER_MISMATCH
    ROW_WIDTH_MISMATCH

One `ROW_WIDTH_MISMATCH` reason is sufficient because expected and actual
counts distinguish missing from extra cells without creating unnecessary
taxonomy. A row-width failure must preserve enough context to reconstruct the
violation, at minimum:

- logical data-record number;
- expected column count; and
- actual column count.

The logical data-record number is not a physical text line number. CSV fields
may legally contain quoted newlines, so the two concepts must not be confused.

Logical data-record numbering follows this explicit convention:

- the CSV header is not a data record;
- the first CSV record successfully returned by `csv.reader` after the header
  is logical data-record 1;
- each subsequent parsed CSV record increments the logical data-record number
  by exactly one;
- a record with malformed width still occupies its encountered logical
  data-record position and `ROW_WIDTH_MISMATCH` reports that number;
- the logical data-record number remains distinct from the physical text line
  number; and
- `csv.reader.line_num` must not be used as the logical data-record number,
  because a quoted CSV field may legally contain embedded newlines.

For example:

```text
header
record A
record B
malformed record C
```

means:

```text
record A -> logical data-record 1
record B -> logical data-record 2
malformed record C -> ROW_WIDTH_MISMATCH at logical data-record 3
```

Structural failures must not be represented by returning `None`, silently
skipping malformed rows, yielding partial mappings, converting them into
`RejectedIdentity`, or introducing a generic catch-all `Result` abstraction.

### Non-Structural Failure Boundary

Increment 006 must not convert unrelated environmental or software failures
into `CalgaryCsvStructureError`. Unless a later explicit design decision
changes the boundary, failures such as these normally propagate in their
native form:

- `FileNotFoundError`;
- `PermissionError`;
- `UnicodeDecodeError`;
- `csv.Error`; and
- unexpected software exceptions.

`CalgaryCsvStructureError` means that a source record violates Increment 006's
structural contract; it does not mean merely that file access or software
execution failed. The implementation must not add a broad
`try/except Exception` conversion.

### Empty Cells and Lexical Fidelity

An empty CSV cell remains `""` at the record-stream boundary. It is not
converted here to `None`, `VALUE_ABSENT`, or `UnavailableEvidence`. The existing
Increment 005 mapper owns semantic evidence-state handling after the parsed
mapping crosses the boundary:

```text
CSV structure layer:
    empty source cell -> ""

Adapter layer:
    "" -> existing Increment 005 evidence policy where applicable
```

After explicit width validation, row construction is conceptually equivalent
to:

```python
dict(zip(EXPECTED_HEADER, row, strict=True))
```

An explicit validated equivalent is also permitted, but width must already
have been checked. The record-stream boundary must not introduce `strip()`,
case conversion, numeric conversion, datetime conversion, timezone conversion,
or missing-value interpretation.

### Laziness and Resource Lifetime

The function will be generator-based and lazy. File opening and row consumption
occur within generator execution. The file remains open only while iteration is
active, and normal generator exhaustion closes it through the context-manager
boundary. Bounded consumers may use `itertools.islice`; the implementation must
not materialize the whole file as a list or tuple. A production limit parameter
will not be introduced merely to support bounded smoke use.

### Planned Test Implications

Later implementation must be falsifiable through planned tests covering at
least:

- exact valid header;
- empty file or missing header;
- reordered header;
- changed header field;
- valid one-row iteration;
- valid multiple-row iteration;
- empty-cell lexical preservation;
- whitespace lexical preservation;
- extra-column failure;
- missing-column failure;
- first data record after the header is numbered 1;
- a malformed third data record reports logical data-record 3;
- quoted embedded newlines do not redefine logical data-record numbering;
- laziness and bounded consumption;
- explicit `Path` input;
- composition with `adapt_calgary_record`;
- native `FileNotFoundError` propagation; and
- no normalization.

These are planned tests only. No tests were created or executed, and no test
count or passing result is claimed by this record.

### Claim Boundary

This design checkpoint establishes only a planned parser interface and expected
structural-failure semantics. It does not establish:

- implementation correctness;
- CSV parsing correctness;
- local artifact readability;
- digest match;
- bounded real-artifact execution;
- dataset-wide correctness;
- analytical validity; or
- production readiness.

## Implementation Record 002 - Initial CSV Record-Stream RED Tests

### Objective

Establish the first executable tests for the committed parser design before
production implementation.

### Classification Before Execution

    Planned test design

The test definitions below are planned test design until executed. The actual
RED execution result, once observed, will be recorded separately as an
Engineering observation. It will not be classified as a product defect,
External evidence, or a Research conclusion.

### Scope

- exact header constant;
- valid one-record iteration;
- lexical preservation;
- empty-file structural rejection; and
- header-mismatch structural rejection.

### Planned Public Symbols

The first implementation slice deliberately plans these public names:

- `EXPECTED_CALGARY_HEADER`;
- `CalgaryCsvStructureError`;
- `CalgaryCsvStructureErrorReason`; and
- `iter_calgary_csv_records`.

### Out of Scope

- row-width implementation;
- logical-record-number implementation;
- embedded-newline behavior;
- native environmental-failure propagation;
- adapter composition;
- artifact digest verification;
- real-artifact smoke;
- persistence; and
- analytics.

### RED Execution Result

Classification:

    Engineering observation

Focused command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Observed result:

```text
exit code: 1
test_calgary_csv_record_stream
    (unittest.loader._FailedTest.test_calgary_csv_record_stream) ... ERROR
ModuleNotFoundError:
    No module named 'support_operations_intelligence.calgary_csv'
Ran 1 test in 0.000s
FAILED (errors=1)
```

The test module could not be imported because the deliberately planned
production module does not yet exist. `unittest` represented that loader
failure as one `_FailedTest`; none of the four authored test methods executed.
This is the expected RED state at this test-first boundary, not a product
defect, External evidence, or a Research conclusion. No production parser was
implemented and no test was made green in this step.

### Initial Implementation and GREEN Results

Classification:

    Engineering observation

Implemented:

- `EXPECTED_CALGARY_HEADER`;
- `CalgaryCsvStructureErrorReason`;
- `CalgaryCsvStructureError`; and
- `iter_calgary_csv_records`.

Source file:

    src/support_operations_intelligence/calgary_csv.py

Focused command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Focused result observed:

```text
Ran 4 tests in 0.001s
OK
failures: 0
errors: 0
```

Regression command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Regression result observed:

```text
Ran 129 tests in 0.005s
OK
failures: 0
errors: 0
```

The retained evidence sequence is:

```text
RED import failure
    -> minimal production implementation
    -> focused and regression GREEN results
```

The GREEN result verifies only the exercised first slice:

- exact expected header constant;
- one valid synthetic record;
- lexical whitespace preservation;
- empty-file structural rejection; and
- header-mismatch structural rejection.

The implementation includes a `ROW_WIDTH_MISMATCH` branch to preserve the
committed structural-safety boundary. Its extra-column behavior, missing-column
behavior, logical data-record-number evidence, and embedded-newline numbering
behavior have not yet been verified by executable tests and are not claimed
green by this record.

## Implementation Record 003 - Row-Width and Logical-Record Verification

### Objective

Provide dedicated executable verification for the already-implemented
`ROW_WIDTH_MISMATCH` and logical data-record numbering behavior.

### Starting State and History

The implementation already existed at:

    d9ab8fba51d36148955d6d80fd9056c665365ef7

This is not a RED-to-GREEN implementation cycle. The production behavior
existed before these dedicated tests were added.

### Classification Before Execution

    Planned test design

The test definitions are planned test design before execution. Actual execution
results, once observed, will be recorded separately as Engineering
observations.

### Tested Scope

- extra-column failure;
- missing-column failure;
- logical data-record 1 for the first record after the header;
- malformed third record reported as logical data-record 3;
- embedded newline does not distort logical data-record numbering; and
- expected and actual column-count context.

### Execution Results

Classification:

    Engineering observation

Focused command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Focused result observed:

```text
Ran 8 tests in 0.001s
OK
failures: 0
errors: 0
```

Regression command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Regression result observed:

```text
Ran 133 tests in 0.005s
OK
failures: 0
errors: 0
```

The dedicated tests passed against the implementation that already existed at
the starting checkpoint. No RED state occurred or is inferred for this slice,
and no production source change was required.

### Updated Verification Status

```text
ROW_WIDTH_MISMATCH implementation:
    IMPLEMENTED

Extra-column behavior:
    DEDICATEDLY_VERIFIED

Missing-column behavior:
    DEDICATEDLY_VERIFIED

Logical data-record numbering:
    DEDICATEDLY_VERIFIED

Embedded-newline logical numbering:
    DEDICATEDLY_VERIFIED
```

### Claim Boundary

This verification slice does not establish:

- native `FileNotFoundError` propagation verification;
- `PermissionError` verification;
- `UnicodeDecodeError` verification;
- `csv.Error` verification;
- adapter composition;
- digest correctness;
- real Calgary artifact readability;
- real-artifact smoke success;
- full-file correctness;
- dataset-wide correctness;
- analytical validity; or
- production readiness.

## Implementation Record 004 - Stream Mechanics and Native File-Access Verification

### Objective

Provide dedicated executable verification for already-implemented stream
behavior and native `FileNotFoundError` propagation.

### Starting Checkpoint and History

The production behavior already existed at:

    ae5b5d8f18f5872a12980160074bbefff9372191

This was not a RED-to-GREEN implementation cycle. The production behavior
already existed before these dedicated tests. No RED state was inferred or
fabricated for this verification slice.

### Classification Before Execution

Test definitions:

    Planned test design before execution

Observed executions, once available, will be classified as Engineering
observations.

### Tested Scope

- multiple valid records preserve source order;
- an empty CSV cell remains `""`;
- bounded consumption does not require whole-file materialization; and
- a nonexistent `Path` propagates `FileNotFoundError` unchanged.

### Execution Results

Classification:

    Engineering observation

Focused command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Focused result observed:

```text
Ran 12 tests in 0.003s
OK
failures: 0
errors: 0
```

Regression command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Regression result observed:

```text
Ran 137 tests in 0.005s
OK
failures: 0
errors: 0
```

The dedicated tests passed against production behavior that already existed at
the starting checkpoint. No RED state occurred or is inferred for this slice,
and no production source change was required.

### Updated Verification Status

```text
Multiple-record iteration:
    DEDICATEDLY_VERIFIED

Source-order preservation across multiple records:
    DEDICATEDLY_VERIFIED

Lexical-value preservation across multiple records:
    DEDICATEDLY_VERIFIED

Empty-cell lexical preservation:
    DEDICATEDLY_VERIFIED

Bounded lazy consumption:
    DEDICATEDLY_VERIFIED

FileNotFoundError propagation:
    DEDICATEDLY_VERIFIED
```

### Claim Boundary

This verification slice does not establish:

- `PermissionError` propagation;
- `UnicodeDecodeError` propagation;
- `csv.Error` propagation;
- all possible generator resource-lifetime behavior;
- adapter composition;
- digest correctness;
- real Calgary artifact readability;
- real-artifact smoke execution;
- full-file correctness;
- dataset-wide correctness;
- analytical validity; or
- production readiness.

## Implementation Record 005 - Parser-to-Adapter Composition Verification

### Objective

Verify that the record `Mapping` emitted by the Increment 006 Calgary CSV
record stream is directly consumable by the Increment 005 Calgary adapter.

### Starting Checkpoint and History

Starting checkpoint:

    a60e041c53427df33b451e0111dcbebd13b7176b

Both production components existed before this test. This was not a
RED-to-GREEN implementation cycle. No RED state was inferred or fabricated.

### Classification Before Execution

Test definition:

    Planned test design before execution

Observed execution, once available, will be classified as an Engineering
observation.

### Tested Boundary

```text
Path
    ->
iter_calgary_csv_records
    ->
Mapping[str, str]
    ->
adapt_calgary_record
    ->
existing accepted Calgary adapter result
```

The parser-emitted mapping is passed directly to `adapt_calgary_record`
without normalization, translation, casting, or reconstruction.

### Execution Results

Classification:

    Engineering observation

Focused command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Focused result observed:

```text
Ran 13 tests in 0.002s
OK
failures: 0
errors: 0
```

Regression command executed:

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

Regression result observed:

```text
Ran 138 tests in 0.005s
OK
failures: 0
errors: 0
```

The new test passed immediately against both production components that
already existed at the starting checkpoint. No RED state occurred or was
inferred or fabricated, and no production source change was required.

### Updated Verification Status

```text
Parser-to-adapter interface composition:
    DEDICATEDLY_VERIFIED
```

This status applies only to the tested one-record synthetic case.

### Claim Boundary

This verification slice does not establish:

- complete adapter correctness;
- universal `Mapping` compatibility;
- all source-field semantics;
- real Calgary artifact readability;
- digest correctness;
- real-artifact smoke execution;
- dataset-wide composition;
- ingestion correctness;
- persistence correctness;
- analytical validity; or
- production readiness.

## Implementation Record 006 - Local Calgary Artifact Identity Verification

### Objective

Determine whether the local Calgary CSV currently present at the expected
path is byte-identical to the prospective artifact characterized in Increment
003 before allowing real-artifact parser execution.

### Evidence Classification

Prior size and digest values:

    Prior internal evidence from Increment 003

Current `stat` and SHA-256 execution:

    Engineering observation

### Starting Checkpoint

    86168b2868de6ab71a1fe5dd912584818b4fcd8e

### Expected Artifact Identity

Expected local path:

    /data/repos/Public Datasets/calgary_311.csv

Expected size:

    1978541467 bytes

Expected SHA-256:

    9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f

### Current Engineering Observations

File-existence result:

    REGULAR_FILE_EXISTS

Observed size:

    1978541467 bytes

Size comparison:

    SIZE_MATCH

Observed SHA-256:

    9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f

Digest comparison:

    SHA256_MATCH

### Permitted Interpretation

The local artifact is byte-identical to the prospective artifact identified
by the recorded size and SHA-256 values.

A matching digest establishes byte identity to the previously hashed local
artifact. It does not establish authoritative external provenance.

This identity verification does not establish:

- authoritative City of Calgary provenance;
- immutable upstream version binding;
- historical publication identity;
- historical licence binding;
- semantic correctness;
- CSV structural correctness;
- row-count correctness;
- parser correctness;
- adapter correctness;
- real-artifact readability;
- real-artifact smoke success;
- full-file correctness;
- dataset-wide correctness;
- analytical validity; or
- production readiness.

No CSV content was parsed or sampled during this identity verification.

### Real-Artifact Execution Gate

```text
REAL_ARTIFACT_SMOKE_GATE:
    IDENTITY_MATCH_CONFIRMED
```

A later bounded real-artifact parser smoke may proceed against this exact
artifact. No parser smoke was performed in this task.

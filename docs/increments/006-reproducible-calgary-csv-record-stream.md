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

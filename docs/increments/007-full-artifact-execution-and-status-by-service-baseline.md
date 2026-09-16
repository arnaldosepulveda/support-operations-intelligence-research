# Increment 007: Full-Artifact Execution and Status-by-Service Baseline

Status: In Progress

## Objective

Execute the previously verified Calgary source artifact through the existing
digest gate, CSV record stream, and Calgary adapter across the complete
artifact, then compute one predeclared descriptive baseline using streaming
aggregation.

The baseline is:

```text
exact source-native status_description
    x
exact source-native service_name
    -> record count
```

The purpose is to establish whether the current executable source-record
boundary survives complete-artifact execution and to retain one narrowly
defined descriptive result. This increment does not authorize operational
diagnosis or intervention analysis.

The full-artifact execution sections remain prospective. Observed engineering
checkpoints, including bounded slice implementation, are recorded explicitly
below. No full-artifact execution or descriptive baseline result has yet been
produced.

## Why This Increment Now

Increment 005 established parsed-record adapter behavior.

Increment 006 established digest verification, CSV stream behavior,
parser-adapter composition, and a bounded three-record real-artifact smoke
test.

The complete approximately 1.9 GB artifact has not yet traversed the current
parser and adapter composition. Complete-artifact execution is therefore a
direct unresolved engineering dependency before persistence or broader
analytics can be justified.

PostgreSQL is not justified merely because the artifact is large. Persistence
should be introduced only when later evidence demonstrates that repeated
analytical workloads, durability, indexing, restartability, or query-cost
requirements justify the additional system complexity.

## Primary Question

Can the already-identified Calgary artifact, after exact SHA-256 verification,
traverse the existing CSV record stream and Calgary adapter across every
logical record without structural failure, unexpected adapter failure,
unexplained identity rejection, or silent record loss?

The answer is not assumed to be yes.

## Secondary Question

Given all records successfully admitted through the bounded executable source
contract, what are the exact record counts grouped by the exact source-native
pair:

```text
(status_description, service_name)
```

This question is descriptive only.

## Analytical Contract

The following analytical contract is frozen prospectively.

Population:

All Calgary source records traversed during the complete artifact execution
that are successfully admitted by the existing Calgary adapter.

Grouping dimensions:

1. exact source-native `status_description`;
2. exact source-native `service_name`.

Measure:

`record count`

Aggregation:

`streaming count aggregation`

The following transformations are prohibited:

- normalization: none;
- case folding: none;
- whitespace normalization: none;
- synonym mapping: none;
- canonical-status mapping: none;
- service-name normalization: none;
- missing-value imputation: none;
- duration calculation: none;
- temporal grouping: none.

The aggregation must use the existing adapter and evidence semantics. It must
not bypass the adapter merely because the CSV parser exposes raw fields.

## Missing / Unavailable Handling

The existing Increment 005 evidence semantics control both grouping
dimensions.

For `status_description`:

- a nonblank string becomes observed source-native evidence retaining the
  exact string;
- a missing key, `None`, empty string, or whitespace-only string becomes
  `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)`;
- a non-string value becomes
  `UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE)`.

For `service_name`, the corresponding existing source-native evidence behavior
applies:

- a nonblank string becomes observed source-native evidence retaining the
  exact string;
- a missing key, `None`, empty string, or whitespace-only string becomes
  `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)`;
- a non-string value becomes
  `UnavailableEvidence(UnavailableReason.EVIDENCE_INDETERMINATE)`.

Before implementation, each aggregation-key component is planned to preserve a
discriminated evidence representation:

- observed evidence: an `OBSERVED` discriminator plus the exact source-native
  string;
- unavailable evidence: an `UNAVAILABLE` discriminator plus the exact existing
  `UnavailableReason`.

This preserves the difference between an observed lexical value and unavailable
evidence without inventing placeholders such as `UNKNOWN`, `N/A`, or `MISSING`.
The serialized or machine-readable result format remains an implementation-time
question. If the existing adapter types cannot support an unambiguous,
deterministic aggregation key without semantic loss, implementation must stop
and resolve that design question before coding the aggregation.

## Full-Artifact Execution Contract

The planned execution order is:

1. identify the explicit artifact path supplied by the operator;
2. verify its exact SHA-256 against
   `9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f`;
3. only after digest success, open the CSV stream;
4. validate the existing exact ordered 15-field header;
5. stream logical records lazily;
6. pass every parsed record through the existing Calgary adapter;
7. count admitted records;
8. count identity rejections by the existing rejection reason;
9. retain structural or parser failure evidence if encountered;
10. compute the predeclared `status_description` by `service_name`
    aggregation;
11. verify accounting invariants before treating any output as a baseline.

The complete artifact must not be loaded into memory.

## Accounting Invariants

The future execution must record at least:

```text
TOTAL_LOGICAL_RECORDS_SEEN
TOTAL_ADMITTED_RECORDS
TOTAL_REJECTED_IDENTITY_RECORDS
REJECTION_COUNTS_BY_REASON
AGGREGATED_RECORD_COUNT
```

It must satisfy:

```text
TOTAL_LOGICAL_RECORDS_SEEN
=
TOTAL_ADMITTED_RECORDS
+
TOTAL_REJECTED_IDENTITY_RECORDS
```

The rejection-reason accounting must also satisfy:

```text
sum(REJECTION_COUNTS_BY_REASON)
=
TOTAL_REJECTED_IDENTITY_RECORDS
```

Because the planned aggregation includes every admitted Case exactly once, it
must satisfy:

```text
AGGREGATED_RECORD_COUNT
=
TOTAL_ADMITTED_RECORDS
```

If an implementation cannot satisfy these invariants, Increment 007 must not
claim a valid complete-artifact baseline.

The historical Increment 003 observation of 7,474,403 logical records is a
comparison point, not an implementation success condition. It must not be
hardcoded as the required result or used to force a new execution to match. Any
mismatch must be investigated and preserved.

## Failure Conditions

Prospective failure conditions include:

- artifact digest mismatch;
- file open or read failure;
- exact header mismatch;
- logical row-width mismatch;
- parser structural failure;
- unexpected adapter exception;
- unexplained identity rejection;
- accounting invariant failure;
- evidence of silent record loss;
- inability to reconstruct the aggregation result deterministically;
- a requirement for undocumented normalization;
- memory behavior that contradicts the intended streaming design;
- incomplete or interrupted traversal presented as complete;
- failure to retain sufficient execution evidence.

A failure must stop execution or invalidate the baseline as appropriate.
Malformed records must not be silently skipped.

## Preserved Failure Evidence

Failed, interrupted, malformed, incomplete, and rejected runs are
research-engineering evidence.

If a full run fails, the future execution record must preserve:

- failure type;
- logical-record position where available;
- exception or category without exposing sensitive row content;
- artifact SHA;
- code commit;
- runtime version;
- command or reproducible runner;
- partial accounting explicitly marked incomplete where available.

Failure evidence must not be edited into a successful narrative.

## Planned Output

A successful future execution record should include:

- verified artifact SHA;
- exact code commit;
- Python version and interpreter;
- execution command or canonical runner;
- start/end timestamps or elapsed runtime;
- total logical records seen;
- admitted-record count;
- identity-rejection count and reasons;
- accounting checks;
- deterministic `status_description` by `service_name` count result;
- a retained machine-readable result artifact if later implementation
  justifies one;
- a human-readable summary.

This planning increment does not choose a result-file format.

## Claim Boundary

If successfully implemented and executed, Increment 007 may establish only
that:

- this exact artifact passed the current digest gate;
- the complete artifact traversed the existing parser and adapter composition
  under the recorded implementation and runtime;
- the accounting invariants held;
- the predeclared source-native `status_description` by `service_name` counts
  were observed.

It must not establish:

- authoritative Calgary provenance;
- an immutable source version;
- production ingestion readiness;
- PostgreSQL necessity;
- data-warehouse readiness;
- operational performance;
- backlog;
- service quality;
- staffing adequacy;
- queue behavior;
- resolution performance;
- causality;
- diagnosis;
- intervention need;
- AI suitability;
- portability to other datasets.

## Non-Goals

This increment does not include:

- PostgreSQL;
- database schema design;
- a persistence layer;
- an ORM;
- an API;
- a dashboard;
- visualization;
- canonical status normalization;
- service taxonomy normalization;
- duration analysis;
- request-to-closure elapsed-duration analysis;
- workforce-management metrics;
- queue metrics;
- causal analysis;
- intervention selection;
- AI, RAG, or agent implementation;
- production deployment;
- cross-dataset joins;
- ServiceNow integration;
- UCI call-center analysis.

## Threat Model / Threats to Validity

- Artifact identity does not prove authoritative provenance.
- Successful parsing does not prove semantic correctness.
- Source-native labels may contain operational meanings not established by the
  dataset documentation.
- Counts describe the retained artifact, not necessarily current Calgary
  operations.
- Dataset snapshot and version timing remain bounded by prior evidence.
- Adapter correctness is limited to its tested contract.
- Absence of parser failure does not imply absence of source-data defects.
- A single descriptive grouping cannot establish workflow causes or
  performance.
- A completed traversal under one code commit and runtime does not establish
  production reliability under other environments.
- Rejection accounting can expose boundary behavior but cannot by itself prove
  why the source evidence was malformed or absent.

## Baselines

Engineering baseline:

Increment 006's existing bounded three-record, digest-gated smoke execution.

Comparison point:

Increment 003's historical complete-artifact structural scan.

The Increment 003 scan is not equivalent to complete execution through the
current parser-adapter composition and must not be described as such.

## Planned Test Categories

The following are planned tests, not observed results:

- aggregation on synthetic accepted records;
- exact grouping without normalization;
- observed and unavailable evidence handling;
- identity-rejection accounting;
- rejection-reason sum accounting;
- aggregate-to-admission accounting invariant;
- total-seen admission-plus-rejection accounting invariant;
- deterministic output ordering if output is serialized;
- full-run summary accounting;
- digest and structural failure propagation;
- unexpected adapter-failure propagation;
- bounded runner behavior where practical;
- memory behavior consistent with lazy streaming where practical.

The unexecuted categories in this prospective list remain planned. Observed
Slice A RED and GREEN checkpoints and the Slice B synthetic composition
checkpoint are recorded separately below.

## Reproducibility Requirements

Future closure requires retention of:

- exact repository commit SHA;
- exact Calgary artifact SHA;
- Python version;
- `sys.executable`;
- canonical execution command or runner;
- test commands;
- elapsed execution time;
- result artifact or deterministic textual representation;
- accounting summary and invariant results;
- any failure evidence;
- sufficient instructions for another engineer to repeat the run if they
  possess the same external artifact.

Reproducibility is not established until that evidence exists.

## Success Criteria

Increment 007 may later close successfully only if:

1. the artifact digest is verified;
2. complete traversal terminates normally;
3. no unexplained parser or adapter failures occur;
4. identity-rejection accounting is retained;
5. record-accounting invariants hold;
6. aggregation accounting holds;
7. the descriptive result is deterministic and reconstructable;
8. planned tests pass;
9. the full regression suite passes;
10. execution evidence is retained;
11. no unsupported analytical interpretation is introduced.

These are prospective criteria, not observed outcomes.

## Claim Classification

```text
Increment plan:
DESIGN CHOICE

Full-artifact execution outcome:
FUTURE ENGINEERING OBSERVATION

Status x service_name counts:
FUTURE INTERNAL EVALUATION / DESCRIPTIVE OBSERVATION

Operational interpretation:
NOT ESTABLISHED

Scientific conclusion:
NOT ESTABLISHED

Persistence requirement:
NOT ESTABLISHED

AI intervention requirement:
NOT ESTABLISHED
```

Writing this plan produces no full-artifact execution outcome, descriptive
result, operational interpretation, scientific conclusion, persistence
requirement, or AI-intervention requirement.

## Slice A RED Checkpoint

### Objective

Freeze the prospective Slice A aggregation and accounting behavior in
executable tests before production implementation exists.

### Scope

- test contract only;
- no production aggregation module;
- no Calgary artifact access;
- no digest or parser change;
- no persistence.

### Observed Environment

- repository commit before this checkpoint:
  `38f89acc6aa2df269a022c256bccf6f6135460f0`;
- Python: `3.12.3`;
- interpreter:
  `/data/repos/personal/support-operations-intelligence/.venv/bin/python`.

### Test Source Syntax Check

Command:

```text
.venv/bin/python -m py_compile \
  tests/test_calgary_status_service_aggregation.py
```

Observed result: `PASS`.

Meaning: the RED test source itself parses successfully.

Boundary: this does not establish test or production behavior.

### Focused RED Command

Command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_status_service_aggregation \
  -v
```

Observed result: `RED / non-zero exit`.

Observed category: `unittest` module-load/import error.

Observed cause: `ModuleNotFoundError` for
`support_operations_intelligence.calgary_status_service_aggregation`.

### Interpretation

The prospective Slice A test contract exists before its production
implementation. The observed RED state is caused by the intentionally absent
aggregation module.

### Boundary

The RED checkpoint does not establish:

- correctness of future aggregation behavior;
- correctness of the prospective tests themselves beyond syntax and import
  intent;
- any passing aggregation semantics;
- full-artifact execution;
- any Calgary baseline count;
- accounting-invariant satisfaction;
- reproducibility of a completed Increment 007 run;
- PostgreSQL or persistence need;
- operational interpretation.

### Claim Classification

```text
TEST_CONTRACT = IMPLEMENTED
PRODUCTION_IMPLEMENTATION = ABSENT
FOCUSED_TEST_STATE = RED
RED_CAUSE = MISSING_PRODUCTION_MODULE
RED_CHECKPOINT = ENGINEERING_OBSERVATION
AGGREGATION_BEHAVIOR = NOT_YET_ESTABLISHED
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Slice A GREEN Checkpoint

### Objective

Implement the previously committed Slice A aggregation and accounting contract
over already-adapted `CalgaryAdapterResult` values.

### Implementation Boundary

The new module
`src/support_operations_intelligence/calgary_status_service_aggregation.py`
implements pure in-process aggregation and accounting only. It performs:

- no artifact I/O;
- no digest verification;
- no CSV parsing;
- no adapter invocation;
- no persistence;
- no normalization;
- no serialization.

### Starting RED Checkpoint

The prior committed RED checkpoint is
`9342a7a0208e3e8fa86092893230959d9e2c8151`. At that checkpoint, the focused
test failed because the production aggregation module was absent.

### Implementation Observation

- already-adapted results are consumed;
- each admitted result contributes exactly one status/service aggregation
  count;
- `RejectedIdentity` results are counted by their existing rejection reason;
- existing evidence objects remain the grouping-key semantics;
- unexpected iterable exceptions propagate.

### Focused Slice A Test Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_status_service_aggregation \
  -v
```

Observed result: `11 tests`, `0 failures`, `0 errors`, `OK`.

### Calgary CSV Focused Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Observed result: `17 tests`, `0 failures`, `0 errors`, `OK`.

### Full Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result: `153 tests`, `0 failures`, `0 errors`, `OK`.

### Accounting Behavior Observed Under Tests

- seen equals admitted plus rejected;
- rejection buckets sum to rejected;
- aggregate counts sum to both aggregated count and admitted;
- exact observed values remain distinct;
- unavailable-evidence reasons remain distinct;
- explained rejection remains accounting rather than an exception;
- an unexpected iterable `RuntimeError` propagates.

### Boundary

Slice A GREEN does not establish:

- full-artifact execution;
- digest verification during Increment 007;
- parser/adapter full-run composition;
- Calgary row count;
- status/service baseline values;
- execution scalability;
- memory suitability for 1.9 GB traversal;
- production readiness;
- PostgreSQL or persistence need;
- operational interpretation;
- scientific conclusion.

### Claim Classification

```text
SLICE_A_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
SLICE_A_FOCUSED_TEST_RESULT = INTERNAL ENGINEERING TEST RESULT
REGRESSION_RESULT = INTERNAL ENGINEERING TEST RESULT
AGGREGATION_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
OPERATIONAL_INTERPRETATION = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Slice B Synthetic Composition Checkpoint

### Objective

Establish whether the already-tested CSV parser, Calgary adapter, and Slice A
aggregator compose directly under a synthetic CSV integration fixture without
introducing another production composition abstraction.

### Implementation Boundary

```text
PRODUCTION_CHANGE = NONE
NEW_COMPOSITION_MODULE = NONE
```

The tested composition is directly equivalent to:

```python
aggregate_calgary_status_by_service(
    adapt_calgary_record(record)
    for record in iter_calgary_csv_records(path)
)
```

`NEW_COMPOSITION_MODULE = NOT_JUSTIFIED_BY_OBSERVED_TEST`. A future full-run
orchestration layer may still be justified by responsibilities not exercised
in this synthetic composition checkpoint.

### Synthetic Fixture Boundary

The test-created CSV uses the exact required ordered header:

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

The fixture contains five synthetic logical records: four admitted and one
typed identity rejection. It contains no real Calgary rows and accesses no
external artifact.

Observed mixed-stream accounting:

```text
TOTAL_LOGICAL_RECORDS_SEEN = 5
TOTAL_ADMITTED_RECORDS = 4
TOTAL_REJECTED_IDENTITY_RECORDS = 1
AGGREGATED_RECORD_COUNT = 4
```

The admission, rejection-reason, and aggregation accounting invariants held
under this synthetic test. These counts describe only the retained fixture.

### Evidence-Preservation Observation

- the exact `Closed` by `Pothole` bucket was counted twice;
- observed `UNKNOWN` remained observed evidence;
- padded ` Drainage ` remained exact and untrimmed;
- `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)` remained distinct;
- no source-native normalization occurred through the composition.

This checkpoint does not establish complete semantic correctness of all
Calgary fields.

### Identity-Rejection Observation

- a synthetic empty source identity produced
  `IdentityRejectionReason.EMPTY_SOURCE_CASE_ID`;
- the rejection was counted exactly once;
- the rejected row did not enter the aggregation;
- the rejection remained a typed result rather than an exception.

### Failure-Propagation Observations

A later malformed-width row propagated `CalgaryCsvStructureError` at logical
record 2. No partial aggregation summary was returned.

A synthetic `RuntimeError` raised during adapter invocation propagated
unchanged. No partial successful summary was returned. These observations do
not establish production fault tolerance.

### Slice B Focused Test Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_adapter_aggregation_composition \
  -v
```

Observed result: `3 tests`, `0 failures`, `0 errors`, `OK`.

### Slice A Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_status_service_aggregation \
  -v
```

Observed result: `11 tests`, `0 failures`, `0 errors`, `OK`.

### Calgary CSV Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Observed result: `17 tests`, `0 failures`, `0 errors`, `OK`.

### Full Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result: `156 tests`, `0 failures`, `0 errors`, `OK`.

### Claim Boundary

Slice B establishes only that the existing parser, adapter, and aggregator
composition operated as specified under the retained synthetic integration
tests. It does not establish:

- digest-gated full-artifact execution;
- traversal of the 1.9 GB Calgary artifact;
- real Calgary row accounting;
- real status/service baseline counts;
- performance;
- scalability;
- memory suitability for the complete artifact;
- production readiness;
- persistence need;
- PostgreSQL need;
- operational interpretation;
- scientific conclusion.

### Claim Classification

```text
CHANGE_TYPE = COMPOSITION_TEST_AND_EVIDENCE
PRODUCTION_CHANGE = NONE
SLICE_B_COMPOSITION_TEST = INTERNAL_ENGINEERING_TEST_RESULT
SLICE_B_INITIAL_TEST_STATE = PASS
DIRECT_COMPOSITION = VERIFIED_UNDER_SYNTHETIC_TEST
NEW_COMPOSITION_MODULE = NOT_JUSTIFIED_BY_OBSERVED_TEST
SLICE_A_REGRESSION = PASS
CALGARY_CSV_REGRESSION = PASS
FULL_REGRESSION = PASS
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
DIGEST_GATED_FULL_RUN = NOT_PERFORMED
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
OPERATIONAL_INTERPRETATION = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Prospective Full-Run Orchestration Design

```text
DESIGN CHOICE / PROSPECTIVE
```

No orchestration implementation or complete-artifact execution has occurred at
this checkpoint.

### Architecture Decision

Architecture C is selected prospectively:

1. one reusable library full-run orchestration boundary;
2. one narrow dependency-free package executable/evidence boundary.

The existing parser -> adapter -> aggregator already composes directly. The
new boundaries are justified by responsibilities that do not belong to those
existing components:

- enforce digest completion before traversal;
- own the complete-run lifecycle;
- validate completed accounting before success;
- produce deterministic retained evidence;
- prevent failed execution from appearing as successful baseline evidence;
- retain bounded success/failure execution context.

The new boundaries are not justified merely to shorten the existing function
composition.

### Prospective Library Boundary

The prospective library module is:

```text
src/support_operations_intelligence/calgary_full_artifact_execution.py
```

Its prospective public function is:

```python
execute_calgary_full_artifact(
    path: Path,
    expected_sha256: str,
) -> CalgaryFullArtifactExecutionResult
```

`CalgaryFullArtifactExecutionResult` contains only:

- the verified artifact SHA-256;
- the existing `CalgaryStatusServiceAggregation`.

The library boundary must not own:

- Git inspection;
- process `argv`;
- `sys.version`;
- `sys.executable`;
- output-path handling;
- JSON publication;
- atomic file promotion;
- CLI parsing;
- environment interpretation.

### Digest-Before-Traversal Ordering

The required full-run library order is:

1. complete `verify_calgary_csv_artifact_sha256(...)`;
2. only after successful digest verification, construct and consume the CSV
   stream;
3. adapt every yielded record;
4. aggregate all resulting `CalgaryAdapterResult` values;
5. validate completed accounting;
6. return the successful domain result.

A digest mismatch must prevent CSV traversal.

```text
FULL_RUN_ARTIFACT_READ_PASSES = 2
```

A successful execution is expected by design to perform one complete binary
digest pass and one complete CSV traversal pass. This is a
`DESIGN CONSEQUENCE / EXPECTED ENGINEERING COST`, not an observed runtime
measurement.

### Completed Accounting Validation

Before a library execution may return success, it must validate:

```text
total_logical_records_seen
==
total_admitted_records
+
total_rejected_identity_records

sum(rejection_counts_by_reason.values())
==
total_rejected_identity_records

sum(aggregated_counts.values())
==
aggregated_record_count

aggregated_record_count
==
total_admitted_records
```

These checks validate completed accounting consistency. They do not turn the
historical Calgary row count into an invariant.

### Prospective Executable Boundary

The prospective dependency-free executable module is:

```text
src/support_operations_intelligence/calgary_full_artifact_run.py
```

Its prospective invocation is:

```text
python -m support_operations_intelligence.calgary_full_artifact_run
```

It requires explicit arguments for:

- input artifact path;
- expected SHA-256;
- `supplied_code_commit`;
- success output path;
- failure output path.

The executable records the code-commit value supplied by the operator. It does
not prove that `supplied_code_commit` identifies the actual checked-out code
unless an independent verification mechanism is later added. The term
`verified_code_commit` must not be used without such verification.

Prospective execution evidence records only:

- schema version;
- outcome;
- expected artifact SHA-256;
- verified artifact SHA-256 when available;
- `supplied_code_commit`;
- `sys.version`;
- `sys.executable`;
- effective `argv`;
- elapsed processing seconds;
- accounting summary;
- rejection counts;
- deterministic status/service aggregate rows.

It does not record hostname, username, machine identity, IP address, or other
unrelated environment data.

### Timing Semantics

For success, timing starts immediately before digest verification and stops
only after the success artifact has been atomically promoted to the supplied
success-output path.

For failure, timing starts immediately before digest verification and the
processing timer stops when the underlying execution failure is caught. The
subsequent serialization and writing of the failure evidence record is not
included in the failed-processing duration.

Timing is engineering execution evidence, not a benchmark claim.

### Typed Evidence and Aggregate-Row Representation

Observed evidence has the deterministic machine representation:

```json
{
  "kind": "OBSERVED",
  "value": "<exact source-native string>"
}
```

Unavailable evidence has the deterministic machine representation:

```json
{
  "kind": "UNAVAILABLE",
  "reason": "<UnavailableReason value>"
}
```

`ObservedEvidence("UNKNOWN")` remains distinct from
`UnavailableEvidence(VALUE_ABSENT)` and
`UnavailableEvidence(EVIDENCE_INDETERMINATE)`. Unknown evidence variants must
fail rather than be silently stringified, collapsed, or encoded as
placeholders. No normalization may be introduced.

Status/service aggregate entries are represented as rows. Each row contains:

- a status evidence object;
- a `service_name` evidence object;
- a count.

Python dataclass representations and tuple representations are not canonical
evidence encodings.

### Deterministic Ordering and JSON Encoding

Aggregate rows are sorted by:

```text
(
    status_kind_rank,
    status_payload,
    service_kind_rank,
    service_payload
)
```

The kind ranks are:

```text
OBSERVED = 0
UNAVAILABLE = 1
```

The payload is the exact observed value for `OBSERVED` or the exact enum value
for `UNAVAILABLE`. Case and whitespace are preserved exactly. Rejection
reasons are sorted by their exact enum value. Dictionary insertion order alone
is not a canonical ordering rule.

Prospective retained evidence uses UTF-8 JSON with:

- stable JSON object-key ordering;
- deterministic aggregate-row ordering;
- deterministic rejection-reason ordering;
- a terminating newline.

Execution metadata such as elapsed time and `argv` is intentionally
run-specific. Byte-identical whole-file output across different executions is
therefore not the reproducibility criterion. The canonical counts and evidence
representation must nevertheless be deterministic for a given completed
domain result.

### Success-Output Safety

For the supplied success-output path:

1. validate the completed domain result;
2. serialize it to a temporary sibling file;
3. flush the temporary file;
4. `fsync` it;
5. close it;
6. atomically promote it with `os.replace` only after successful completion.

A failed execution must not create a new success artifact, overwrite an
existing success artifact, or promote a partial temporary artifact.
Temporary-file cleanup behavior must be tested prospectively.

### Failure-Output Safety and Classification

The executable requires a distinct explicit `failure_output_path`. It must not
derive failure output implicitly from the success filename.

On execution failure:

- the success output remains untouched;
- bounded failure evidence is written atomically to `failure_output_path`;
- the process exits non-zero.

Failure evidence may include:

- schema version;
- `outcome = FAILURE`;
- failure stage;
- exception type;
- bounded exception message;
- elapsed processing seconds;
- expected digest;
- verified digest if safely available;
- `supplied_code_commit`;
- `sys.version`;
- `sys.executable`;
- effective `argv`;
- logical record position where available;
- bounded partial accounting only where accurately available.

Failure evidence must not contain raw CSV row contents.

The prospective failure-stage vocabulary is:

```text
DIGEST
CSV_STRUCTURE
ADAPTER
AGGREGATION
OUTPUT
OTHER
```

Failure-stage classification is execution evidence. It must not replace or
reinterpret the original underlying exception semantics. Where exceptions are
wrapped or classified, original exception chaining is preserved where
practical.

Success-path logical record numbering is not required. For CSV structural
failure, the existing parser-provided `logical_data_record_number` is retained
where available. Explicit successful-position tracking for an unexpected
adapter failure is useful but is not required by the current Increment 007
contract.

```text
ADAPTER_FAILURE_POSITION = NICE_TO_HAVE / NOT_REQUIRED_BEFORE_FULL_RUN
```

This classification must not be strengthened retrospectively.

### Identity-Rejection and Historical-Count Boundaries

Typed `RejectedIdentity` values:

- remain execution/accounting results;
- are counted by the existing `IdentityRejectionReason`;
- do not automatically make execution fail;
- do not enter status/service aggregation.

The executable must not encode `rejection_count > 0` as execution failure.
Human/research review after execution determines whether observed rejection
counts and reasons are explained by the frozen adapter contract.

The historical count `7,474,403` remains a comparison from Increment 003. It
must not become an execution invariant, automatic success criterion,
automatic failure criterion, or expected parser count hardcoded into
production code. Comparison belongs to post-run research review.

### Result-Artifact Lifecycle

Initial successful and failure JSON evidence must be written to an
operator-supplied location outside the tracked repository. An example only is:

```text
/data/repos/personal/support-operations-intelligence-results/increment-007/
```

This location must not be hardcoded into production design. Retention into the
repository, publication, or other canonical artifact storage is a later review
decision requiring consideration of:

- accounting correctness;
- unexpected rejection results;
- sensitivity;
- licensing;
- repository size;
- publication boundary.

### Memory Claim Boundary

The following is `CODE-STRUCTURE ANALYSIS` only:

- CSV iteration is lazy;
- adapter results may be generated lazily;
- aggregation retains counts rather than all source rows;
- expected aggregation memory grows primarily with the number of distinct
  evidence pairs plus rejection reasons.

No observed memory-complexity or suitability result exists for the real
artifact.

```text
OBSERVED_FULL_RUN_MEMORY_BEHAVIOR = NOT_ESTABLISHED
```

### Prospective Pre-Full-Run Test Scope

Before the complete artifact is executed, synthetic tests prospectively
require:

1. digest verification completes before traversal begins;
2. digest mismatch prevents traversal;
3. a successful synthetic artifact returns a complete domain result;
4. completed accounting invariants are validated;
5. typed observed and unavailable evidence serializes distinctly;
6. deterministic aggregate ordering;
7. deterministic rejection-reason ordering;
8. typed identity rejection remains accounting rather than execution failure;
9. structural failure prevents success promotion;
10. unexpected adapter failure prevents success promotion;
11. failed execution preserves success output if one already exists;
12. successful execution atomically promotes only after completion;
13. failure output is written separately and atomically;
14. failure evidence contains no raw source row;
15. the executable returns non-zero on failed execution;
16. no external Calgary artifact is required by this test suite.

Lower-level Slice A/B tests should not be duplicated except where necessary to
verify a new orchestration responsibility.

```text
PRE_FULL_RUN_REAL_ARTIFACT_PREFIX_SMOKE = NOT_REQUIRED
```

Rationale:

- Increment 006 already established bounded real-artifact streaming;
- Slice B established complete parser -> adapter -> aggregation composition on
  synthetic data;
- a truncated Calgary copy would be a different artifact and would not satisfy
  the complete-artifact digest contract;
- the orchestration boundary should instead be fully exercised using synthetic
  temporary artifacts before the one complete real-artifact run.

This decision does not mean the real run is low risk.

### Prospective Implementation File Scope

The prospective production files are:

```text
src/support_operations_intelligence/calgary_full_artifact_execution.py
src/support_operations_intelligence/calgary_full_artifact_run.py
```

The prospective test file is:

```text
tests/test_calgary_full_artifact_execution.py
```

No `__init__.py` change, `pyproject.toml` change, or third-party dependency is
currently justified. These are prospective paths, not implemented artifacts.

### Responsibility Ownership

| Component | Owns | Must Not Own |
| --- | --- | --- |
| Digest verifier | Exact SHA-256 verification | Parsing or orchestration |
| CSV parser | Structure validation, lazy parsed mappings, and structural position | Digest, adaptation, or aggregation |
| Adapter | Identity admission and exact evidence mapping | File access, normalization, or aggregation |
| Aggregator | Status/service counts, rejection counts, and accounting summary | Environment metadata or output publication |
| Full-run library orchestration | Digest-before-traversal ordering, complete domain traversal, final accounting validation, and domain result | Git or process metadata, `argv`, or file publication |
| Executable/evidence boundary | Arguments, execution metadata, timing, deterministic JSON, atomic success/failure publication, and exit status | Evidence interpretation or source normalization |

### Claim Classification

```text
FULL_RUN_ORCHESTRATION_ARCHITECTURE = DESIGN_CHOICE
ARCHITECTURE_SELECTION = C
FULL_RUN_LIBRARY = NOT_IMPLEMENTED
FULL_RUN_EXECUTABLE = NOT_IMPLEMENTED
FULL_RUN_TESTS = NOT_IMPLEMENTED
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
DIGEST_GATED_FULL_RUN = NOT_PERFORMED
FULL_RUN_ARTIFACT_READ_PASSES = 2_EXPECTED_BY_DESIGN
OBSERVED_FULL_RUN_MEMORY_BEHAVIOR = NOT_ESTABLISHED
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
OPERATIONAL_INTERPRETATION = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Architecture C1 RED Checkpoint

```text
OBSERVED ENGINEERING EVIDENCE
```

### Objective

Freeze the reusable full-artifact library orchestration contract in executable
tests before the C1 production module exists.

C1 is limited to:

```text
digest gate
-> complete parser/adapter/aggregation execution
-> completed-accounting validation
-> domain result
```

The C2 executable/evidence boundary remains unimplemented.

### Observed Environment

- repository commit before this checkpoint:
  `c1881bc5b685e95a0bfa6d5699b533be1804716d`;
- Python: `3.12.3`;
- interpreter:
  `/data/repos/personal/support-operations-intelligence/.venv/bin/python`.

### Prospective C1 Test Contract

The committed test contract prospectively specifies four C1 behaviors:

1. A successful synthetic artifact uses the real existing digest verifier,
   parser, adapter, and aggregator. Its three logical records are expected to
   produce 3 seen, 2 admitted, 1 typed identity rejection, and 2 aggregated.
   The typed rejection must not fail library execution.
2. A digest mismatch must propagate the existing
   `CalgaryCsvArtifactDigestMismatch`, and CSV traversal must never begin.
3. Digest verification must return successfully before record-stream
   construction.
4. An inconsistent completed aggregation must fail C1 with
   `CalgaryFullArtifactAccountingError`.

These are prospective behaviors in a RED test contract. They are not passing
behavior observations at this checkpoint.

### Test Source Syntax Check

Command:

```text
.venv/bin/python -m py_compile \
  tests/test_calgary_full_artifact_execution.py
```

Observed result: `PASS`.

This establishes only that the test source parses independently of the
intentionally missing production module.

### Focused RED Command

Command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_full_artifact_execution \
  -v
```

Observed result: `RED / non-zero exit`.

Observed category: `unittest` module-load/import failure.

Observed cause: `ModuleNotFoundError` for
`support_operations_intelligence.calgary_full_artifact_execution`.

### Interpretation

The C1 test contract exists before its production implementation. The observed
RED state is caused by the intentionally absent C1 module. This establishes
test-first chronology only.

### Boundary

The C1 RED checkpoint does not establish:

- C1 correctness;
- digest-before-stream behavior;
- successful synthetic orchestration;
- accounting-validation behavior;
- complete Calgary traversal;
- real artifact digest verification;
- real Calgary row accounting;
- C2 executable behavior;
- deterministic JSON;
- success/failure publication;
- runtime or memory suitability;
- a descriptive baseline;
- operational interpretation;
- a scientific conclusion.

### Claim Classification

```text
CHANGE_TYPE = C1_RED_TEST_CONTRACT_AND_EVIDENCE
ARCHITECTURE_SLICE = C1_LIBRARY_ORCHESTRATION
C1_TEST_CONTRACT = IMPLEMENTED
C1_PRODUCTION_IMPLEMENTATION = ABSENT
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
FOCUSED_TEST_STATE = RED
RED_CAUSE = MISSING_C1_PRODUCTION_MODULE
C1_RED_CHECKPOINT = ENGINEERING_OBSERVATION
C1_BEHAVIOR = NOT_YET_ESTABLISHED
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Current Status

Increment 007 is in progress. The Slice A test contract, pure aggregation
implementation, observed RED and GREEN checkpoints, and Slice B synthetic
composition checkpoint exist. The Architecture C1 RED test contract and
observed missing-module RED evidence also exist, while C1 and C2 production
remain absent. No complete-artifact execution, descriptive baseline, or
closure evidence exists yet.

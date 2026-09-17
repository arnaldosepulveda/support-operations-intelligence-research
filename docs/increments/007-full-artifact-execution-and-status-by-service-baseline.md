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

## Prospective Complete-Artifact Counter Contract

```text
DESIGN CHOICE / PROSPECTIVE
```

These counters are frozen before C1 implementation and before
complete-artifact execution. They exist because discovering that a required
counter was omitted after the complete approximately 1.9 GB traversal may
require another full execution.

This Step 2 contract refines the earlier prospective C1 result boundary. The
successful C1 domain result must retain the verified artifact SHA-256, the
existing status/service aggregation, and the domain counters defined below.
It still must not contain C2 process, environment, timing, or publication
metadata. The exact dataclass decomposition is an implementation-time detail;
the counter meanings and reconciliation requirements are frozen here.

### Row-Lifecycle Counters

The complete execution requires:

```text
rows_observed
rows_structurally_accepted
rows_structurally_rejected
rows_identity_admitted
rows_identity_rejected
```

`rows_observed` is the number of logical CSV data records encountered by the
full execution boundary, including the first structurally invalid logical
record if one is encountered.

`rows_structurally_accepted` is the number of logical records successfully
emitted by the existing CSV parser.

`rows_structurally_rejected` is the number of logical records rejected
structurally by the parser. The existing parser is fail-fast, so a successful
`BaselineResult` requires:

```text
rows_structurally_rejected == 0
```

If a structural error occurs, complete-artifact execution fails, no successful
`BaselineResult` is produced, and bounded failure evidence may record the one
first structurally rejected record. This contract does not imply that parsing
continues after a structural failure.

`rows_identity_admitted` is the number of structurally accepted records for
which `adapt_calgary_record` returns `CalgaryAdaptedCase`.

`rows_identity_rejected` is the number of structurally accepted records for
which `adapt_calgary_record` returns `RejectedIdentity`.

### Row Reconciliation

The counters must satisfy:

```text
rows_observed
==
rows_structurally_accepted
+
rows_structurally_rejected

rows_structurally_accepted
==
rows_identity_admitted
+
rows_identity_rejected
```

For a successful `BaselineResult`:

```text
rows_structurally_rejected == 0
rows_observed == rows_structurally_accepted
```

A successful result that violates either reconciliation identity is evidence
of a counting defect and must not be accepted as a baseline. The historical
`7,474,403` comparison is not part of these equations.

### Exact Source-Identity Duplicate Counters

The complete execution also requires:

```text
distinct_source_case_ids
source_case_ids_appearing_more_than_once
rows_involved_in_duplication
```

Duplicate analysis applies only to identity-admitted records with a valid
`source_case_id` under the existing adapter identity contract.
Identity-rejected rows are not assigned synthetic identifiers and are not
included in these duplicate counters. They remain separately represented by
`rows_identity_rejected` and the existing rejection-reason accounting.

Duplicate equality is exact `source_case_id` string equality. It performs no:

- stripping;
- case normalization;
- numeric coercion;
- canonicalization;
- hashing-as-identity;
- source-specific cleanup.

For an admitted source identifier occurring `k` times:

- if `k == 1`, it contributes 1 to `distinct_source_case_ids`, 0 to
  `source_case_ids_appearing_more_than_once`, and 0 to
  `rows_involved_in_duplication`;
- if `k >= 2`, it contributes 1 to `distinct_source_case_ids`, 1 to
  `source_case_ids_appearing_more_than_once`, and `k` to
  `rows_involved_in_duplication`.

`rows_involved_in_duplication` therefore counts every row participating in a
repeated identity, not only occurrences after the first. For example:

```text
A, A, A, B, C, C

distinct_source_case_ids = 3
source_case_ids_appearing_more_than_once = 2
rows_involved_in_duplication = 5
```

### Exact One-Pass Duplicate Algorithm

The prospective exact one-pass algorithm maintains:

```text
seen_source_case_ids: set[str]
duplicate_source_case_ids: set[str]
rows_involved_in_duplication: int
```

For each identity-admitted `source_case_id`:

```text
if id not in seen_source_case_ids:
    add id to seen_source_case_ids
else if id not in duplicate_source_case_ids:
    add id to duplicate_source_case_ids
    rows_involved_in_duplication += 2
else:
    rows_involved_in_duplication += 1
```

At completion:

```text
distinct_source_case_ids = len(seen_source_case_ids)

source_case_ids_appearing_more_than_once =
    len(duplicate_source_case_ids)
```

This provides exact counts without retaining a frequency dictionary for every
identifier. It is not implemented at this checkpoint.

### Duplicate Memory Policy and Claim Consequence

The preferred implementation is exact Python string sets. These duplicate
counters determine whether the resulting cross-tab can safely be described as
one row per source identity or only as a distribution over source rows.

A 32-bit hash must not substitute for the strings, and a probabilistic
representation must not be introduced silently. If exact identifier tracking
cannot complete within available memory, the run must not silently downgrade:
execution must fail clearly, or an explicitly predeclared approximate method
must be introduced in a later contract revision before another run. A 64-bit
alternative is not an automatic fallback.

```text
DUPLICATE_COUNT_METHOD = EXACT
```

Until the duplicate counters are observed, the status/service baseline is a
distribution over source rows. It must not be described as a distribution over
unique Cases.

If `source_case_ids_appearing_more_than_once == 0`, the complete artifact
provides evidence that admitted source identifiers are unique within that
artifact under exact lexical equality. If the value is non-zero, the
cross-tab remains a source-row distribution unless a later increment defines
and justifies deduplication or another unit-of-analysis policy. Increment 007
does not automatically deduplicate.

### Source-Field Blank Counters

The required blank-field counters are:

```text
blank_service_name
blank_agency_responsible
blank_status_description
```

They apply only to identity-admitted records and follow the existing adapter
contract. A field increments its blank counter when its corresponding adapted
evidence is `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)`.

Under the current adapter, a missing key, `None`, an empty string, or a
whitespace-only string maps to `VALUE_ABSENT`. A non-string value maps to
`EVIDENCE_INDETERMINATE` and is not counted as blank. A string containing at
least one non-whitespace character remains observed exactly, including its
original whitespace, and is not counted as blank. No stripping or new
normalization is introduced.

This counter contract does not define a presentation label for blank evidence.

### Vocabulary and Cross-Tab Counters

The complete execution requires full exact frequency maps:

```text
status_vocabulary
service_name_vocabulary
```

Both cover structurally accepted, identity-admitted records using the same
exact source-native evidence semantics as the aggregation. Observed lexical
values remain exact. Unavailable evidence remains typed and distinguishable;
it is not collapsed into placeholder strings. No lexical normalization is
introduced.

The required cross-tab is:

```text
service_name_x_status
```

It is the existing Slice A status/service aggregation, expressed with
`service_name` as the primary axis and `status_description` as the secondary
dimension. Increment 007 adds no `agency_responsible` cross-tab;
`agency_responsible` blankness is counted only.

### Counter Populations

The frozen counter populations are:

| Counter family | Population |
| --- | --- |
| Row lifecycle | All logical records encountered |
| Identity counters | All structurally accepted records |
| Duplicate counters | Identity-admitted records with a valid exact `source_case_id` |
| Blank-field counters | Identity-admitted records |
| Vocabularies | Identity-admitted records |
| `service_name_x_status` | Identity-admitted records |
| Rejection reasons | Identity-rejected records |

These populations preserve existing Slice A behavior: identity rejections are
counted and reconciled but do not enter admitted-record vocabularies or the
status/service cross-tab.

### Additional Reconciliation Requirements

A successful `BaselineResult` must also satisfy:

```text
distinct_source_case_ids
<=
rows_identity_admitted

source_case_ids_appearing_more_than_once
<=
distinct_source_case_ids

rows_involved_in_duplication
<=
rows_identity_admitted

sum(status_vocabulary.values())
==
rows_identity_admitted

sum(service_name_vocabulary.values())
==
rows_identity_admitted

sum(service_name_x_status.values())
==
rows_identity_admitted

sum(identity_rejection_reason_counts.values())
==
rows_identity_rejected
```

Any successful result violating one of these equations must fail validation.

### Execution-Metric Ownership

`wall_clock_seconds` and `peak_rss_bytes` are run-level execution evidence,
not domain row counters. They belong prospectively to C2 execution evidence
and must not be placed inside `CalgaryFullArtifactExecutionResult` by C1. The
final retained `BaselineResult` or evidence artifact may include them in its
outer execution-metadata envelope.

The eventual complete execution prospectively requires two peak-RSS evidence
sources:

1. an in-process peak-RSS measurement;
2. an independent `/usr/bin/time -v` Maximum resident set size observation.

Neither is implemented or observed at this checkpoint. They need not be
byte-identical. Units must be explicit: in-process platform APIs can report
platform-specific units, while `/usr/bin/time -v` commonly reports maximum
resident set size in KiB on Linux. Retained evidence must convert or label
units explicitly rather than silently compare unlike units.

### Deferred Step 3 Policies

This Step 2 checkpoint does not freeze:

- reporting percentages;
- a `(blank)` presentation label;
- raw-line structural-error retention;
- a `service_name` reporting policy beyond the counter population;
- a material-difference policy;
- output interpretation.

Those concerns belong to Step 3.

### Claim Classification

```text
COUNTER_CONTRACT = DESIGN_CHOICE
COUNTER_CONTRACT_STATUS = FROZEN_BEFORE_C1_IMPLEMENTATION
DUPLICATE_COUNT_METHOD = EXACT
DUPLICATE_POPULATION = IDENTITY_ADMITTED_EXACT_SOURCE_CASE_ID
UNIT_OF_ANALYSIS_BEFORE_DUPLICATE_RESULT = SOURCE_ROW
UNIQUE_CASE_DISTRIBUTION = NOT_ESTABLISHED
ROW_RECONCILIATION = PROSPECTIVE_VALIDATION_REQUIREMENT
VOCABULARY_RECONCILIATION = PROSPECTIVE_VALIDATION_REQUIREMENT
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
COUNTER_RESULTS = NOT_OBSERVED
```

## Prospective Complete-Artifact Semantic and Reporting Policies

```text
DESIGN CHOICE / PROSPECTIVE
```

These policies are frozen before C1 implementation and before any complete
artifact result is observed. Their purpose is to prevent normalization,
denominator, grouping, diagnostic, or reporting decisions from being selected
after seeing the baseline.

### Normalization Policy

```text
NORMALIZATION = NONE
```

All observed source-native lexical values remain exact. For example:

```text
"Closed"
"Closed "
"closed"
```

are three distinct observed labels. Increment 007 performs no stripping, case
folding, lowercasing, uppercasing, canonicalization, synonym merging, spelling
repair, or whitespace normalization. If lexical variants prove material after
the run, that is an observation for a later increment. Increment 007 must not
retrospectively collapse them.

### Blank Semantics and Presentation

```text
BLANK_POLICY = RETAIN
```

Identity-admitted rows with
`UnavailableEvidence(UnavailableReason.VALUE_ABSENT)` for a grouping dimension
are not dropped. They remain part of:

- the admitted-record denominator;
- vocabulary accounting;
- cross-tab accounting where applicable.

For human reporting only, `VALUE_ABSENT` may be displayed as `(blank)`.
`(blank)` is a display label, not an evidence encoding. It must not replace the
internal typed representation
`UnavailableEvidence(UnavailableReason.VALUE_ABSENT)`.

An observed literal `(blank)`, if present in the source, remains exact observed
lexical evidence and must not collide with unavailable evidence.
`EVIDENCE_INDETERMINATE` also remains distinct from `VALUE_ABSENT` and from
observed strings. Unavailable reasons are not collapsed.

The Step 2 counters remain:

```text
blank_service_name
blank_agency_responsible
blank_status_description
```

Each is the count of identity-admitted records whose corresponding existing
evidence state is `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)`.
Whitespace-containing `ObservedEvidence` is not counted as blank. A
whitespace-only source string is counted only because the existing adapter
already maps it to `VALUE_ABSENT`. Increment 007 introduces no second
blankness rule.

### Primary Grouping and Unit Boundary

```text
PRIMARY_GROUPING_FIELD = service_name
```

The Increment 007 descriptive cross-tab is:

```text
service_name x status_description
```

`agency_responsible` is not another grouping axis in Increment 007 and remains
limited to its required blankness counter. No service taxonomy or category
normalization is introduced.

The baseline counts source rows satisfying the frozen admitted-record
population. Until the Step 2 exact duplicate counters are observed:

```text
UNIQUE_CASE_DISTRIBUTION = NOT_ESTABLISHED
```

Cross-tab counts must not use “Cases” as shorthand before duplicate results
support that wording. The base portfolio denominator for cross-tab percentages
is `rows_identity_admitted`.

### Raw Counts and Percentages

Every `service_name x status_description` cell retains its exact raw integer
count. Percentages supplement raw counts and never replace them. Increment 007
performs no small-denominator suppression, and no cell is hidden merely because
its count is small.

For each exact `service_name` evidence group `S` and exact status evidence
group `T`:

```text
cell_count(S, T)
```

is the raw cross-tab count, and:

```text
service_total(S)
=
sum over all T of cell_count(S, T)
```

When `service_total(S) > 0`:

```text
within_category_percentage(S, T)
=
100 * cell_count(S, T) / service_total(S)
```

This answers only: within this exact `service_name` evidence group, what
percentage of admitted source rows carry this exact status evidence? It does
not support operational interpretation or causal comparison between service
groups.

The portfolio denominator is:

```text
portfolio_total
=
rows_identity_admitted
```

When `portfolio_total > 0`:

```text
portfolio_wide_percentage(S, T)
=
100 * cell_count(S, T) / portfolio_total
```

This answers only: what percentage of all identity-admitted source rows belong
to this exact `service_name x status_description` cell? The denominator
includes admitted rows with unavailable grouping evidence. Blank or other
unavailable states must not be silently dropped.

Raw integer counts remain authoritative and are the only accounting inputs.
Percentages are calculated from raw counts and rounded for presentation only:

```text
PERCENTAGE_DISPLAY_DECIMAL_PLACES = 4
```

Later counts must not be derived from displayed percentages.

### Material-Difference Policy

```text
MATERIAL_DIFFERENCE_THRESHOLD = NOT_DEFINED
```

Increment 007 must not classify a difference as material, significant,
meaningful, large, small, concerning, or acceptable using a newly invented
threshold. Such a decision belongs to a later analytical increment after the
baseline exists and an explicit analytical question is defined.

### Structural Failure and Diagnostic Policy

```text
STRUCTURAL_FAILURE_POLICY = ABORT_ON_FIRST_ERROR
```

The parser remains fail-fast. On the first structural error:

- complete execution aborts;
- no successful `BaselineResult` is produced;
- no later rows are processed;
- the structural rejection belongs to failure evidence rather than a
  successful baseline.

Skip-and-continue behavior is not permitted.

A structural failure must expose:

- the logical data-record number;
- the offending raw logical-record content.

This is a prospective requirement. The existing parser already exposes
`logical_data_record_number` on `CalgaryCsvStructureError`, but retained
repository evidence does not establish that it exposes the offending raw
logical-record content.

```text
RAW_STRUCTURAL_RECORD_DIAGNOSTIC = REQUIRED_BEFORE_COMPLETE_RUN
CURRENT_RAW_STRUCTURAL_RECORD_SUPPORT = NOT_ESTABLISHED
```

This checkpoint does not claim current parser support and does not modify the
parser.

“Raw record content” means offending raw logical-record content sufficient to
diagnose the structural failure without rerunning the complete artifact. It
must correspond to the malformed logical CSV record that caused the structural
exception. Because a CSV logical record may span physical lines, this contract
does not equate a logical record with one raw physical line.

Exact source characters must be preserved to the extent supported by the
parser implementation. A normalized or reconstructed cleaned value must not
be called raw. If the current `csv.reader` architecture cannot preserve exact
logical-record source text, that gap must be resolved explicitly before the
complete run rather than silently weakening the policy.

This requirement refines, without weakening, the previously frozen retained
failure-evidence safety boundary:

```text
RAW_RECORD_IN_EXCEPTION = REQUIRED
RAW_RECORD_IN_RETAINED_FAILURE_JSON = PROHIBITED_BY_DEFAULT
```

The in-process structural exception may carry the offending raw logical record
for operator diagnosis. The retained C2 structured failure JSON must not
automatically include raw source-row or record content. It may retain the
logical record number, exception type, and bounded diagnostic metadata without
copying the raw Calgary record.

### Grouping and Reporting Representation

The primary report consists of rows containing at least:

- exact typed `service_name` evidence;
- exact typed `status_description` evidence;
- raw count;
- within-category percentage;
- portfolio-wide percentage.

Machine evidence remains either `OBSERVED` with the exact lexical value or
`UNAVAILABLE` with the exact reason. For human-readable views only,
`VALUE_ABSENT` may display as `(blank)`. Presentation labels must not replace
typed machine evidence.

The complete raw `status_vocabulary` and `service_name_vocabulary` are retained
as exact count maps or rows. They must not be truncated to top-N, have rare
values merged, have blanks removed, or have variants normalized. A later human
review may summarize them, but the `BaselineResult` must retain the complete
vocabulary evidence required by Step 2.

### Historical Count Treatment

The historical comparison remains:

```text
7,474,403 logical records
CONTEXTUAL_COMPARISON_ONLY
```

After the run, `rows_observed` is compared with `7,474,403`. If equal, only the
equality is recorded. If different, both counts and the exact arithmetic
difference are recorded.

```text
CAUSE_OF_DIFFERENCE = NOT_DETERMINED
```

Counts must not be adjusted, parser behavior changed, rows filtered,
denominators redefined, or execution rerun with changed semantics merely to
force agreement.

### Interpretation and Prospective Claim Boundary

Increment 007 reporting is descriptive evidence only. It must not infer:

- operational quality;
- service performance;
- backlog;
- closure quality;
- resolution quality;
- causality;
- staffing need;
- queue behavior;
- intervention need;
- AI suitability.

It must not rank service categories, identify good or bad statuses, or
interpret cross-tab differences.

After successful execution, the strongest intended claim is bounded to:

> The current tested parser and adapter traversed the complete digest-verified
> artifact and produced source-native `service_name x status_description`
> counts under the predeclared denominator, evidence, and reporting policies.

That claim is not established at this checkpoint.

```text
TARGET_BASELINE_CLAIM = PROSPECTIVE
```

The eventual claim remains a source-row baseline unless the observed exact
duplicate counters establish:

```text
source_case_ids_appearing_more_than_once == 0
```

Even then, wording may establish exact source-identifier uniqueness within the
artifact but must not assert that one row equals one independently managed
real-world unit of work. That stronger semantic interpretation remains not
established.

### Claim Classification

```text
SEMANTIC_POLICY_CONTRACT = DESIGN_CHOICE
SEMANTIC_POLICY_STATUS = FROZEN_BEFORE_C1_IMPLEMENTATION
NORMALIZATION = NONE
BLANK_POLICY = RETAIN
BLANK_PRESENTATION_LABEL = "(blank)"
PRIMARY_GROUPING_FIELD = service_name
WITHIN_CATEGORY_DENOMINATOR = SERVICE_NAME_GROUP_TOTAL
PORTFOLIO_WIDE_DENOMINATOR = ROWS_IDENTITY_ADMITTED
RAW_COUNTS_RETAINED = YES
PERCENTAGE_DISPLAY_DECIMAL_PLACES = 4
SMALL_DENOMINATOR_SUPPRESSION = NONE
MATERIAL_DIFFERENCE_THRESHOLD = NOT_DEFINED
STRUCTURAL_FAILURE_POLICY = ABORT_ON_FIRST_ERROR
RAW_STRUCTURAL_RECORD_DIAGNOSTIC = REQUIRED_BEFORE_COMPLETE_RUN
CURRENT_RAW_STRUCTURAL_RECORD_SUPPORT = NOT_ESTABLISHED
RAW_RECORD_IN_EXCEPTION = REQUIRED
RAW_RECORD_IN_RETAINED_FAILURE_JSON = PROHIBITED_BY_DEFAULT
TARGET_BASELINE_CLAIM = PROSPECTIVE
OPERATIONAL_INTERPRETATION = NOT_ESTABLISHED
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
```

## Architecture C1 Counter-Contract RED Extension

```text
OBSERVED ENGINEERING EVIDENCE
```

### Objective

Extend the committed C1 RED test contract so the Step 2 complete-pass counter
semantics are frozen in executable prospective tests before any C1 production
implementation exists.

### Result-Boundary Design Refinement

The earlier prospective C1 result boundary of verified digest plus existing
`CalgaryStatusServiceAggregation` is superseded by the later Step 2 counter
contract. The prospective C1 result must also carry a frozen complete-pass
counter summary containing the row-lifecycle, exact-duplicate, blank-field,
and typed-vocabulary evidence required by Step 2.

The extended test contract names this nested prospective boundary
`CalgaryFullArtifactCounterSummary` and exposes it as
`CalgaryFullArtifactExecutionResult.counter_summary`. The existing
`aggregation` result remains the single status/service cross-tab and existing
identity-rejection accounting boundary; no redundant cross-tab or rejection
map is introduced.

This is a `DESIGN REFINEMENT` made before implementation. C1 still does not own
`wall_clock_seconds` or `peak_rss_bytes`; those remain C2 execution metadata.

### Prospective Test Contract Extension

The original four C1 test methods remain:

1. successful synthetic artifact returns verified digest and aggregation;
2. digest mismatch prevents CSV traversal;
3. successful digest verification completes before stream construction;
4. completed aggregation inconsistency raises
   `CalgaryFullArtifactAccountingError`.

The successful synthetic fixture is extended to five logical records: four
identity-admitted records and one typed identity rejection. It prospectively
requires:

- 5 observed and structurally accepted rows;
- 0 structurally rejected rows;
- 4 identity-admitted rows;
- 1 identity-rejected row;
- both row-lifecycle reconciliation equations;
- 2 distinct admitted source identifiers;
- 1 source identifier appearing more than once;
- 3 rows involved in duplication for an exact identifier appearing three
  times;
- exactly one blank `service_name`, `agency_responsible`, and
  `status_description` under existing `VALUE_ABSENT` semantics;
- exact typed status and service vocabularies whose counts each sum to admitted
  rows;
- distinct `ObservedEvidence("Drainage")`,
  `ObservedEvidence(" Drainage ")`, and
  `UnavailableEvidence(UnavailableReason.VALUE_ABSENT)` service evidence;
- existing aggregate counts summing to identity-admitted rows;
- existing rejection-reason counts summing to identity-rejected rows.

One additional prospective public counter-summary validation test samples two
completed-domain inconsistencies:

- row-lifecycle reconciliation failure;
- `rows_involved_in_duplication > rows_identity_admitted`.

Both require `CalgaryFullArtifactAccountingError`. The future implementation
must validate every frozen Step 2 equation even though this extension samples
representative failures rather than adding one test per equation.

The source now contains five prospective C1 test methods in total. It adds no
C2 tests, timing/RSS fields, percentages, JSON, output publication, process
behavior, or raw structural-record parser behavior.

### Test Source Syntax Check

Command:

```text
.venv/bin/python -m py_compile \
  tests/test_calgary_full_artifact_execution.py
```

Observed result: `PASS`.

This establishes only that the extended test source parses.

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

The focused command fails during import before any prospective test method or
synthetic fixture executes. The RED cause remains the intentionally absent C1
production module.

### Boundary

This extension does not establish:

- C1 behavior;
- counter correctness;
- any passing orchestration behavior;
- any observed counter value from the Calgary artifact;
- C2 behavior;
- raw structural-record diagnostic support;
- full-artifact execution;
- a descriptive baseline;
- operational interpretation;
- a scientific conclusion.

No real Calgary artifact was accessed.

### Claim Classification

```text
CHANGE_TYPE = C1_RED_COUNTER_CONTRACT_EXTENSION
ARCHITECTURE_SLICE = C1_LIBRARY_ORCHESTRATION
C1_TEST_CONTRACT = IMPLEMENTED_AND_EXTENDED
C1_RESULT_BOUNDARY = REFINED_BEFORE_IMPLEMENTATION
COUNTER_CONTRACT_EXECUTABLE_TESTS = IMPLEMENTED
C1_PRODUCTION_IMPLEMENTATION = ABSENT
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
FOCUSED_TEST_STATE = RED
RED_CAUSE = MISSING_C1_PRODUCTION_MODULE
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
COUNTER_RESULTS = NOT_OBSERVED
```

## Architecture C1 GREEN Checkpoint

```text
OBSERVED ENGINEERING EVIDENCE
```

### Objective

Implement the committed Architecture C1 library orchestration and
complete-pass counter contract, then establish its behavior under the retained
synthetic tests without implementing C2 or accessing the Calgary artifact.

### Implementation Boundary

The implemented module is:

```text
src/support_operations_intelligence/calgary_full_artifact_execution.py
```

Its public API is:

```python
execute_calgary_full_artifact(
    path: Path,
    expected_sha256: str,
) -> CalgaryFullArtifactExecutionResult
```

The implemented result types are:

- `CalgaryFullArtifactExecutionResult`;
- `CalgaryFullArtifactCounterSummary`.

Completed-domain accounting inconsistencies raise:

```text
CalgaryFullArtifactAccountingError
```

C1 owns:

- digest-before-traversal ordering;
- complete parser/adapter/aggregator composition;
- complete-pass domain counters;
- completed-domain consistency validation;
- the successful domain result.

C1 does not own:

- C2 executable behavior;
- Git or process metadata;
- timing;
- RSS;
- JSON serialization;
- output paths or file publication;
- process exit status.

### Implementation Observations

- digest verification returns successfully before the CSV record stream is
  constructed;
- records remain lazy through parser consumption and adapter generation;
- every structurally accepted mapping is adapted exactly once;
- the same `CalgaryAdapterResult` updates C1 counters and enters the existing
  Slice A aggregator;
- successful row-lifecycle accounting records zero structural rejections;
- admitted source identifiers are tracked exactly as strings in seen and
  duplicate sets without normalization, hashing, or dataflow deduplication;
- `rows_involved_in_duplication` counts every admitted row participating in a
  repeated exact identifier;
- blank counters use only existing typed `VALUE_ABSENT` evidence;
- exact typed status and service evidence objects are vocabulary keys;
- the existing aggregation remains the sole status/service cross-tab and
  rejection-reason map;
- all frozen completed-accounting and cross-boundary reconciliation equations
  are validated before a successful result is returned;
- digest, parser, adapter, and aggregator processing exceptions are not broadly
  caught or translated into completed-accounting errors.

These are implementation and synthetic-test observations, not real-artifact
counter results.

```text
COUNTER_RESULTS_ON_REAL_ARTIFACT = NOT_OBSERVED
```

### C1 Focused Test Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_full_artifact_execution \
  -v
```

Observed result: `5 tests`, `0 failures`, `0 errors`, `OK`.

### Slice A Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_status_service_aggregation \
  -v
```

Observed result: `11 tests`, `0 failures`, `0 errors`, `OK`.

### Slice B Regression Command

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_adapter_aggregation_composition \
  -v
```

Observed result: `3 tests`, `0 failures`, `0 errors`, `OK`.

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

Observed result: `161 tests`, `0 failures`, `0 errors`, `OK`.

The observed total matches the expected 156-test checkpoint plus the five
committed C1 test methods. No test was added or modified during C1 GREEN
implementation.

### Claim Boundary

C1 behavior is established only under the retained synthetic tests. This
checkpoint does not establish:

- complete Calgary traversal;
- real digest-gated full execution;
- real duplicate counts;
- real vocabularies;
- a real status/service cross-tab baseline;
- timing or RSS;
- C2 behavior;
- raw structural-record diagnostics;
- operational interpretation;
- a scientific conclusion.

The separate pre-run implementation gap remains:

```text
RAW_STRUCTURAL_RECORD_DIAGNOSTIC = REQUIRED_BEFORE_COMPLETE_RUN
CURRENT_RAW_STRUCTURAL_RECORD_SUPPORT = NOT_ESTABLISHED
```

No real Calgary artifact was accessed.

### Claim Classification

```text
CHANGE_TYPE = C1_GREEN_IMPLEMENTATION_AND_EVIDENCE
ARCHITECTURE_SLICE = C1_LIBRARY_ORCHESTRATION
C1_PRODUCTION_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
C1_TEST_RESULT = INTERNAL_ENGINEERING_TEST_RESULT
COUNTER_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
COUNTER_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
COUNTER_RESULTS_ON_REAL_ARTIFACT = NOT_OBSERVED
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Raw Structural Record Diagnostic RED Checkpoint

```text
OBSERVED ENGINEERING EVIDENCE
```

### Objective

Freeze exact offending logical-record retention before parser implementation.
The prospective exception field is:

```text
raw_logical_record: str | None
```

For `ROW_WIDTH_MISMATCH`, the field must contain the exact source text consumed
for the malformed logical CSV record, including source quoting, delimiters,
whitespace, embedded newline characters, and the fixture's exact line
terminator. It must not be reconstructed from parsed field values. For a
structural state where no logical record exists, such as an empty file, the
field may be `None`.

A physical line is one line returned by the text stream. A logical CSV record
is the complete source text consumed by CSV parsing for one record and may span
multiple physical lines because quoted fields may contain newlines. The
diagnostic contract requires the latter.

### Prospective Test Contract

Two synthetic tests now require `CalgaryCsvStructureError` to retain both the
existing correct `logical_data_record_number` and the exact malformed source
record:

- a single-line wrong-width record with exact quoting, delimiters, whitespace,
  and `CRLF` line terminator;
- a wrong-width logical record containing a properly quoted embedded `CRLF`,
  with the complete two-physical-line source unit required.

The second test is load-bearing: retaining only the final physical line cannot
satisfy it. Neither test places raw source content in successful parsed
mappings, adapted cases, aggregation, C1 results, or counter summaries. No C2
failure-artifact behavior is tested.

### Observed RED Evidence

Syntax command:

```text
.venv/bin/python -m py_compile \
  tests/test_calgary_csv_record_stream.py
```

Observed result: `PASS`.

Focused command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Observed result: `19 tests`; the 17 existing tests passed, and the two new
diagnostic tests ended in errors. Both errors were exactly:

```text
AttributeError: 'CalgaryCsvStructureError' object has no attribute 'raw_logical_record'
```

The existing reason, fail-fast behavior, column counts, and logical
data-record numbering remain passing. Parser implementation was not changed,
and the full regression suite was not run for this RED checkpoint.

```text
CURRENT_RAW_STRUCTURAL_RECORD_SUPPORT = RED_CONTRACT_IMPLEMENTED_IMPLEMENTATION_ABSENT
```

### Security and Retention Boundary

```text
RAW_RECORD_IN_PROCESS_EXCEPTION = REQUIRED
RAW_RECORD_IN_RETAINED_C2_FAILURE_JSON = PROHIBITED_BY_DEFAULT
```

Raw structural content is bounded in-process diagnostic source context, not a
canonical retained baseline field. Retained C2 failure JSON must not include
it by default. No real Calgary row or artifact content is included in this RED
checkpoint.

### Claim Classification

```text
CHANGE_TYPE = RAW_STRUCTURAL_DIAGNOSTIC_RED_TEST_AND_EVIDENCE
PARSER_DIAGNOSTIC_TEST_CONTRACT = IMPLEMENTED
RAW_STRUCTURAL_RECORD_DIAGNOSTIC_IMPLEMENTATION = ABSENT
SINGLE_LINE_RAW_LOGICAL_RECORD_BEHAVIOR = NOT_YET_ESTABLISHED
MULTILINE_RAW_LOGICAL_RECORD_BEHAVIOR = NOT_YET_ESTABLISHED
C1_PRODUCTION_IMPLEMENTATION = ESTABLISHED_UNDER_SYNTHETIC_TESTS
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
```

## Raw Structural Record Diagnostic GREEN Checkpoint

```text
OBSERVED ENGINEERING EVIDENCE
```

### Objective

Implement the committed raw structural-record diagnostic contract in the
existing Calgary CSV parser and establish the tested behavior without changing
the committed tests, implementing C2, or accessing the real Calgary artifact.

### Implemented Diagnostic Behavior

`CalgaryCsvStructureError` now exposes the backward-compatible field:

```text
raw_logical_record: str | None
```

For the tested `ROW_WIDTH_MISMATCH` cases, the parser retains the exact
malformed logical-record source text while preserving the existing logical
data-record number, reason, expected column count, and actual column count.
The retained text preserves source quoting, delimiters, whitespace, line
terminators, and every physical line consumed for a multiline logical CSV
record.

The parser supplies `csv.reader` through a bounded internal iterator that
tracks only the physical source lines consumed for the current logical record.
Header and successful-record buffers are cleared before parsing continues or a
successful mapping is yielded. No successful mapping carries raw source text,
and no growing collection of prior source records is retained.

### Observed Test Evidence

CSV focused command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

Observed result: `19 tests`, `0 failures`, `0 errors`, `OK`. The committed
single-line exact-source diagnostic test and multiline complete-logical-record
diagnostic test both pass, with logical data-record numbering preserved.

Slice B composition command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_adapter_aggregation_composition \
  -v
```

Observed result: `3 tests`, `0 failures`, `0 errors`, `OK`.

C1 regression command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_full_artifact_execution \
  -v
```

Observed result: `5 tests`, `0 failures`, `0 errors`, `OK`.

Slice A regression command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_status_service_aggregation \
  -v
```

Observed result: `11 tests`, `0 failures`, `0 errors`, `OK`.

Full regression command:

```text
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result: `163 tests`, `0 failures`, `0 errors`, `OK`. The observed
total matches the prior 161-test checkpoint plus the two committed structural
diagnostic tests.

### Failure and Retention Boundary

```text
RAW_RECORD_IN_PROCESS_EXCEPTION = IMPLEMENTED
RAW_RECORD_IN_RETAINED_C2_FAILURE_JSON = PROHIBITED_BY_DEFAULT
```

The raw logical record exists only as in-process structural-exception context.
It is not serialized, logged, written to disk, placed in successful mappings,
or added to C1 results. No C2 behavior has been implemented, and no real
Calgary structural failure has been observed.

### Claim Boundary

This checkpoint establishes only that the parser retained exact offending
logical-record source text for the tested synthetic single-line and multiline
`ROW_WIDTH_MISMATCH` cases. It does not establish that the real Calgary
artifact contains a structural error, complete-artifact traversal, real
failure diagnostics, C2 failure-record behavior, performance, memory
suitability, or a descriptive baseline.

### Claim Classification

```text
CHANGE_TYPE = RAW_STRUCTURAL_DIAGNOSTIC_GREEN_IMPLEMENTATION_AND_EVIDENCE
PARSER_DIAGNOSTIC_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
SINGLE_LINE_RAW_LOGICAL_RECORD_BEHAVIOR = ESTABLISHED_UNDER_SYNTHETIC_TEST
MULTILINE_RAW_LOGICAL_RECORD_BEHAVIOR = ESTABLISHED_UNDER_SYNTHETIC_TEST
RAW_RECORD_IN_PROCESS_EXCEPTION = IMPLEMENTED
RAW_RECORD_IN_RETAINED_C2_FAILURE_JSON = PROHIBITED_BY_DEFAULT
C1_PRODUCTION_IMPLEMENTATION = ESTABLISHED_UNDER_SYNTHETIC_TESTS
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
```

## Prospective C2 Thin Executable Contract

```text
DESIGN REFINEMENT / PROSPECTIVE
```

### Scope Refinement

The earlier broader publication design is narrowed for Increment 007. C2 now
owns only command-line argument parsing; execution-date, current Git revision,
and Python version capture; wall-clock timing; in-process peak RSS capture;
deterministic `BaselineResult` JSON construction; direct success-file writing;
and a zero/nonzero process outcome.

The earlier prospective requirements below are explicitly deferred and are
not mandatory for Increment 007 completion:

```text
ATOMIC_SUCCESS_PUBLICATION = DEFERRED
ATOMIC_RENAME_PROTOCOL = DEFERRED
STRUCTURED_FAILURE_ARTIFACT = DEFERRED
FAILURE_OUTPUT_PATH = DEFERRED
EXIT_STATUS_TAXONOMY = DEFERRED_BEYOND_ZERO_NONZERO
```

### Git Revision and CLI Contract

Operator-supplied code-commit metadata is superseded for Increment 007 C2.
C2 must capture the current repository revision itself before starting C1. The
retained `git_revision` is the exact output of the repository-local equivalent
of `git rev-parse HEAD` at execution time. Failure to obtain it produces a
nonzero outcome before C1 starts. This binds the run to the observed checkout;
it is not independent validation of code correctness.

```text
SUPPLIED_CODE_COMMIT = SUPERSEDED_FOR_INCREMENT_007_C2
GIT_REVISION_CAPTURE = REQUIRED
```

The prospective invocation is:

```text
PYTHONPATH=src .venv/bin/python -m \
  support_operations_intelligence.calgary_full_artifact_run \
  --artifact <path> \
  --expected-sha256 <sha256> \
  --output <path>
```

All three arguments are required. There is no `--git-revision` or
`--failure-output`. C2 uses standard-library `argparse` and exposes only
`main(argv: Sequence[str] | None = None) -> int` as its required public
function; package execution uses `raise SystemExit(main())`.

### BaselineResult Binding and Run Metadata

Every successful retained JSON binds the result through these top-level
fields:

```text
artifact_sha256
git_revision
increment_version = "007"
contract_id = "007-full-artifact-execution-and-status-by-service-baseline"
```

It also retains `run_date_utc`, `python_version`, `wall_clock_seconds`, and
`peak_rss_bytes`. The run date is a UTC execution timestamp. The Python version
is that of the executing interpreter. Wall-clock measurement begins
immediately before the C1 call and ends after successful JSON file writing.

On the current Linux contract, in-process peak RSS uses standard-library
`resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024` because the source
value is KiB:

```text
IN_PROCESS_PEAK_RSS_UNIT = BYTES
```

The later Step 6 run separately retains `/usr/bin/time -v` as external
evidence. The two measurements are not asserted to be identical. Hostname,
username, IP address, machine serial, precise location, and unrelated
environment variables are excluded.

### Deterministic JSON and Typed Evidence

The success artifact is UTF-8 JSON with stable object-key ordering,
deterministic list ordering, and a terminating newline. Whole-file byte
identity across runs is not expected because run date, wall-clock duration,
and peak RSS are run-specific. The domain and counter representation remains
deterministic for the same C1 result.

Observed evidence is encoded as:

```json
{"kind": "OBSERVED", "value": "<exact source-native value>"}
```

Unavailable evidence is encoded as:

```json
{"kind": "UNAVAILABLE", "reason": "<UnavailableReason value>"}
```

Exact observed case and whitespace are preserved. `UNKNOWN`, `N/A`,
`MISSING`, and `(blank)` are not machine encodings for unavailable evidence;
`(blank)` remains presentation-only.

Both `status_vocabulary` and `service_name_vocabulary` are deterministic rows
containing `evidence` and `count`, not JSON-object keys derived from Python
representations. Rows sort by evidence kind rank (`OBSERVED = 0`,
`UNAVAILABLE = 1`) and then exact payload. Vocabularies are not truncated,
merged, or normalized.

The existing cross-tab is serialized as deterministic `status_by_service`
rows containing typed `service_name` evidence, typed `status_description`
evidence, raw integer `count`, `within_category_percentage`, and
`portfolio_wide_percentage`. Rows sort by service evidence kind rank and
payload, then status evidence kind rank and payload. Dictionary insertion
order is not a serialization contract.

### Percentages, Counters, and Rejections

For each cell:

```text
within_category_percentage =
100 * cell_count / exact service_name group total

portfolio_wide_percentage =
100 * cell_count / rows_identity_admitted
```

Raw integer counts are authoritative. Percentages are retained as fixed-width
four-decimal strings such as `"25.0000"`; counts are never derived from them.
Unavailable evidence remains included under the Step 3 denominator contract.

The `counter_summary` retains every C1 row-lifecycle, identity, exact-duplicate,
blank-field, and complete vocabulary counter. Specifically, it retains
`rows_observed`, `rows_structurally_accepted`, `rows_structurally_rejected`,
`rows_identity_admitted`, `rows_identity_rejected`,
`distinct_source_case_ids`, `source_case_ids_appearing_more_than_once`,
`rows_involved_in_duplication`, `blank_service_name`,
`blank_agency_responsible`, `blank_status_description`, and the deterministic
status and service vocabularies. C2 does not deduplicate or reinterpret them.

Identity rejection counts are deterministic `reason` and `count` rows sorted
lexically by exact `IdentityRejectionReason.value`. C2 does not invent
categories or remove a reason present in the C1 result.

### Historical Comparison

The JSON retains:

```text
historical_rows_observed = 7474403
current_rows_observed = counter_summary.rows_observed
difference = current_rows_observed - historical_rows_observed
cause = "NOT_DETERMINED"
```

This is descriptive comparison evidence, not a success gate. Output is not
altered to force equality.

### Claims Contract

Every success artifact contains an `ESTABLISHED` entry substantively
equivalent to:

> The current tested parser and adapter traversed the complete digest-verified
> artifact and produced source-native service_name x status_description counts
> under a declared denominator and declared exclusions.

This appears only after successful C1 completion. `NOT ESTABLISHED` entries
cover operational finding, diagnosis, causality, backlog interpretation,
duration interpretation, closure finality, cross-service status
comparability, `service_name` label comparability, whether one row is one
independently managed unit of work, artifact representativeness, and AI
suitability.

Duplicate counters address exact source-identifier repetition only. They do
not establish that one row equals one independently managed real-world unit of
work. No cross-tab interpretation is included.

### Direct Write and Failure Boundary

After C1 success and successful serialization, C2 writes UTF-8 JSON directly
to `--output` with a terminating newline:

```text
DIRECT_OUTPUT_WRITE = IN_SCOPE
ATOMIC_OUTPUT_PUBLICATION = DEFERRED
```

This is intentionally not atomic. A crash during writing can leave partial
output; that accepted engineering limitation remains explicit.

If execution fails before successful output completion, the process outcome
is nonzero, no successful `BaselineResult` is intentionally produced, and no
structured failure artifact is written. Failure remains on the process and
terminal boundary without a finer exit-status taxonomy. A structural CSV
failure continues to carry `logical_data_record_number` and
`raw_logical_record` on `CalgaryCsvStructureError`; raw record content is not
serialized to the success path.

## C2 Executable Contract RED Checkpoint

```text
OBSERVED ENGINEERING EVIDENCE
```

Exactly one prospective C2 test module now exists:

```text
tests/test_calgary_full_artifact_run.py
```

Its eight `unittest.TestCase` methods freeze successful CLI output and binding,
Git-revision failure before C1, deterministic typed evidence ordering,
four-decimal percentage denominators including unavailable evidence,
historical comparison, static bounded claims, nonzero C1 failure without
success output, and structural-diagnostic preservation without success
serialization.

No tests require atomic rename, temporary success files, failure JSON, a
failure-output path, multi-code exit taxonomy, PostgreSQL, analytics, or real
artifact behavior.

Test syntax command:

```text
.venv/bin/python -m py_compile \
  tests/test_calgary_full_artifact_run.py
```

Observed result: `PASS`.

Focused RED command:

```text
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_full_artifact_run \
  -v
```

Observed result: `RED / nonzero`; one unittest loader error occurred before the
eight prospective methods could execute. Exact cause:

```text
ModuleNotFoundError: No module named 'support_operations_intelligence.calgary_full_artifact_run'
```

The missing C2 production module is the sole RED cause. The full regression
suite was not run for this RED checkpoint; the retained prior GREEN suite is
`163 tests`, `0 failures`, `0 errors`, `OK`. No real Calgary artifact was
accessed.

### Claim Classification

```text
CHANGE_TYPE = C2_RED_TEST_CONTRACT_AND_SCOPE_REFINEMENT
ARCHITECTURE_SLICE = C2_EXECUTABLE_EVIDENCE_BOUNDARY
C2_SCOPE = THIN_EXECUTABLE
C2_TEST_CONTRACT = IMPLEMENTED
C2_EXECUTABLE_IMPLEMENTATION = ABSENT
C2_FOCUSED_TEST_STATE = RED
C2_RED_CAUSE = MISSING_C2_PRODUCTION_MODULE
GIT_REVISION_CAPTURE = REQUIRED
SUPPLIED_CODE_COMMIT = SUPERSEDED_FOR_INCREMENT_007_C2
DIRECT_OUTPUT_WRITE = IN_SCOPE
ATOMIC_OUTPUT_PUBLICATION = DEFERRED
STRUCTURED_FAILURE_ARTIFACT = DEFERRED
EXIT_STATUS_TAXONOMY = DEFERRED_BEYOND_ZERO_NONZERO
FULL_ARTIFACT_EXECUTION = NOT_PERFORMED
REAL_CALGARY_ARTIFACT_ACCESSED = NO
DESCRIPTIVE_BASELINE = NOT_ESTABLISHED
```

## Current Status

Increment 007 is in progress. The Slice A test contract, pure aggregation
implementation, observed RED and GREEN checkpoints, and Slice B synthetic
composition checkpoint exist. The Architecture C1 RED test contract and
observed missing-module RED evidence also exist. The prospective
complete-artifact counter contract was frozen before C1 implementation, but no
counter results have been observed. No percentages, vocabularies, or cross-tab
values have been observed. The complete-artifact semantic and reporting
policies are frozen prospectively. The C1 RED contract is extended for the
complete-pass counter summary, and C1 is now implemented and GREEN under the
retained synthetic tests. The raw structural-record diagnostic RED test
contract is implemented, and its parser support is now GREEN under the
committed synthetic single-line and multiline tests. C2 remains absent. No
complete-artifact execution, real counter result, descriptive baseline, or
closure evidence exists yet. The thin C2 scope and its eight-method
prospective RED contract are now frozen; the test module remains RED solely
because C2 has not been implemented.

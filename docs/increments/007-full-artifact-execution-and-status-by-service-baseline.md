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

The implementation and full-artifact execution sections remain prospective.
Observed engineering checkpoints are recorded explicitly below. No
full-artifact execution or descriptive baseline result has yet been produced.

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

This prospective list does not claim implementation or passing test results.
The observed Slice A RED checkpoint is recorded separately below.

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

## Current Status

Increment 007 is in progress. The Slice A test contract and observed RED
checkpoint exist. No production implementation, complete-artifact execution,
aggregation result, passing test result, or closure evidence exists yet.

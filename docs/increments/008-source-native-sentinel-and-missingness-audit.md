# Increment 008: Source-Native Sentinel and Missingness Audit

Status: In Progress

Date: 2026-09-17

## Purpose and Prospective Boundary

This document freezes a prospective analytical contract before any retained
vocabulary contents are inspected. No vocabulary observation, audit result, or
candidate finding is recorded here.

Increment 007 is closed and remains closed. Increment 008 does not amend,
correct, or retroactively reclassify any Increment 007 result. It does not
alter the Increment 007 adapter or source contract, and it does not alter any
retained Increment 007 evidence artifact.

If Increment 008 later produces evidence relevant to the public description of
Increment 007 results, a separate recorded decision is required after
Increment 008 completes. Such a later public-description decision is not an
edit to Increment 007.

```text
INCREMENT_007_STATUS = CLOSED_UNCHANGED
INCREMENT_007_AMENDMENT = OUT_OF_SCOPE
```

## Primary Question

Do `service_name`, `agency_responsible`, or `status_description` contain
observed lexical values that plausibly encode missing, unknown, unavailable,
or placeholder states, despite the Increment 007 `VALUE_ABSENT` counters being
zero for all three fields?

Increment 007 established:

```text
blank_service_name = 0
blank_agency_responsible = 0
blank_status_description = 0
```

Those results were established under the frozen adapter interpretation
`UnavailableEvidence(VALUE_ABSENT)`. They establish zero `VALUE_ABSENT`
evidence under that adapter contract. They do not establish semantic
completeness, absence of source-native sentinel strings, absence of placeholder
values, or absence of low-information lexical categories. Increment 008 tests
only that gap.

## Retained-Evidence Feasibility Boundary

Without opening vocabulary contents, the known retained Increment 007 evidence
boundary is:

```text
service_name sentinel audit = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
status_description sentinel audit = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
agency_responsible lexical sentinel audit = NOT_CURRENTLY_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

Increment 007 retained complete lexical frequency vocabularies for
`service_name` and `status_description`. It did not retain a complete
`agency_responsible` lexical vocabulary as part of the frozen `BaselineResult`
contract; it retained only the `blank_agency_responsible` counter.

The three-field question remains the intended question, but Increment 008 may
produce a partial answer because the retained Increment 007 evidence does not
currently contain the full `agency_responsible` lexical distribution.
Resolving this evaluation-evidence gap would require a separately and
prospectively authorized evidence-generation step. It must not occur silently
inside Increment 008, and it must not be described as source missingness.

```text
AGENCY_RESPONSIBLE_LEXICAL_AUDIT = EVIDENCE_UNAVAILABLE_UNDER_CURRENT_RETAINED_007_ARTIFACT
```

## Data Access Rule

Increment 008 is based only on retained Increment 007 vocabulary and count
evidence that already exists. For the presently evaluable fields,
`service_name` and `status_description`, no Calgary source-artifact reread,
source-row traversal, C1 or C2 rerun, PostgreSQL load, adapter change, or
evidence-generation expansion is permitted without a new prospective
checkpoint.

```text
SOURCE_ARTIFACT_REREAD = PROHIBITED
FULL_ARTIFACT_RERUN = PROHIBITED
ADAPTER_CHANGE = OUT_OF_SCOPE
```

### Phase 1 Evaluability and Pure Audit Boundary

The Phase 1 implementation must retain these explicit field states:

```text
service_name = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
status_description = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

It must not infer agency values, synthesize an agency vocabulary, reopen the
Calgary source, rerun Increment 007, or derive agency information from
unrelated fields. A future retained result must represent the
`agency_responsible` state explicitly rather than silently omitting the field.

The production Phase 1 audit will operate only on retained vocabulary rows
supplied to a pure boundary conceptually equivalent to:

```text
audit_phase1_field(
    field_name,
    vocabulary_rows,
    row_denominator,
) -> Phase1FieldAuditResult
```

The audit does not own Calgary CSV access, C1 or C2 execution, baseline-result
file discovery, or repository traversal.

## Phase 1 - Deterministic Predeclared Lexical Checks

```text
PHASE_1_CLASSIFICATION = PREDECLARED
PHASE_1_METHOD = DETERMINISTIC
```

The following checks are frozen before any vocabulary contents are inspected.
No Phase 1 rule may be extended after vocabulary inspection.

### Phase 1A - Exact Empty String

```text
PHASE_1A = EXACT_EMPTY_STRING
value == ""
```

This check applies only to observed lexical evidence. Typed `UNAVAILABLE`
evidence is not reinterpreted as an observed lexical value.

### Phase 1B - Whitespace Only

```text
PHASE_1B = WHITESPACE_ONLY
```

The frozen whitespace character set is exactly:

- `U+0020 SPACE`
- `U+0009 TAB`
- `U+00A0 NO-BREAK SPACE`

A value matches Phase 1B when it is not the empty string and every character
belongs to this frozen set. The rule must not be replaced later with a broader
Unicode whitespace class after data inspection.

### Phase 1C - Case-Insensitive Exact Sentinel

```text
PHASE_1C = CASE_INSENSITIVE_EXACT_SENTINEL
```

The immutable Phase 1 sentinel list is exactly:

```text
unknown
n/a
na
null
none
nil
not available
not applicable
not specified
unspecified
undefined
tbd
to be determined
blank
empty
missing
-
--
.
?
0
no data
nodata
```

Matching applies only to observed lexical values and uses case-insensitive
exact lexical comparison. It performs no trimming, punctuation normalization,
whitespace normalization, or synonym expansion. This list is immutable for
Phase 1 and must not be extended after vocabulary inspection.

### Phase 1D - Leading or Trailing Whitespace

```text
PHASE_1D = LEADING_OR_TRAILING_WHITESPACE
```

This check uses the same exact frozen whitespace set as Phase 1B: `U+0020`,
`U+0009`, and `U+00A0`. A value matches when it is not empty, is not wholly
whitespace under Phase 1B, and its first or last character belongs to the
frozen set.

A Phase 1D match is a normalization-drift candidate, not automatically a
missingness or sentinel candidate. It is reported separately from Phase
1A/1B/1C sentinel coverage, and the value is not stripped before reporting.

### Phase 1E - Non-Printable or Control Character

```text
PHASE_1E = NON_PRINTABLE_OR_CONTROL_CHARACTER
```

A value matches if any character satisfies
`not character.isprintable()` under Python 3.12 semantics. The rule is
explicitly dependent on that Python version.

## Phase 1 Candidate Identity and Overlap

One candidate is the exact pair `(field, exact observed lexical value)`. A
single candidate may match multiple Phase 1 checks. Its `matched_checks` field
must contain the complete deterministic set or list of matching Phase 1 check
identifiers.

Coverage counts use unique candidate lexical values and their retained row
counts, not the number of matched checks. A field/value candidate must not be
double-counted merely because it triggers multiple rules. This applies in
particular to overlaps among Phase 1B, Phase 1D, and Phase 1E.

## Phase 2 - Exploratory Source-Specific Placeholder Review

```text
PHASE_2_CLASSIFICATION = EXPLORATORY
PHASE_2_TIMING = POST_HOC
```

Phase 2 may identify source-specific placeholder-looking lexical values not
anticipated by Phase 1. It begins only after Phase 1 results have been produced
and retained. Every Phase 2 finding must be labeled
`EXPLORATORY_SENTINEL_CANDIDATE`.

A Phase 2 value is not a conclusion that the value is missing, authority to
change the adapter, or authority to alter Increment 007. It is a hypothesis or
evidence item for a potential future increment. Any public statement using a
Phase 2 finding must explicitly identify its post-hoc and exploratory origin.

No Phase 2 observed values are pre-populated here. No vocabulary contents have
been inspected.

## Phase 3 - Semantically Low-Information Values

```text
PHASE_3_CLASSIFICATION = SEPARATE_SEMANTIC_CATEGORY
PHASE_3_RELATION_TO_MISSINGNESS = NOT_SENTINEL_MISSINGNESS
```

Phase 3 may identify lexical values that are structurally present and
lexically ordinary but may carry little classificatory information. Examples
of shape only include `"Other"`, `"General Inquiry"`, `"Miscellaneous"`, or a
`status_description` whose lexical content appears to represent a workflow
artifact rather than a lifecycle state. These are contract examples, not
findings, and this document does not claim that they occur in Calgary.

Phase 3 findings must never be merged with Phase 1 sentinel candidates or
Phase 2 exploratory sentinel candidates. Phase 3 is not evidence of missing
data. Every Phase 3 candidate requires its exact lexical value, field, retained
row count, row coverage, an explicit low-information rationale, and the label
`LOW_INFORMATION_CANDIDATE`. It must not be reclassified as missing.

## Candidate Reporting Contract

Every Phase 1 or Phase 2 lexical candidate must retain:

- field;
- exact lexical value reproduced verbatim;
- phase;
- matched checks or exploratory rationale;
- row count;
- row percentage;
- distinct-vocabulary percentage; and
- candidate classification.

The candidate classifications are:

```text
Phase 1 = PREDECLARED_LEXICAL_CANDIDATE
Phase 2 = EXPLORATORY_SENTINEL_CANDIDATE
Phase 3 = LOW_INFORMATION_CANDIDATE
```

Increment 008 classifies no candidate as `MISSING_DATA`.

## Percentage and Denominator Contract

The Phase 1 percentage arithmetic is frozen before implementation:

```text
PERCENTAGE_ARITHMETIC = DECIMAL_FROM_INTEGER_COUNTS
PERCENTAGE_DISPLAY_DECIMAL_PLACES = 6
PERCENTAGE_ROUNDING = ROUND_HALF_EVEN
MATERIALITY_THRESHOLD_COMPARISON = UNROUNDED_DECIMAL_VALUE
```

Row percentages are derived from integer row counts, and vocabulary
percentages are derived from integer distinct-value counts. Threshold decisions
must use the unrounded `Decimal` percentage. Displayed six-decimal values are
presentation only; displayed rounding must never alter materiality
classification. This refinement is frozen before any vocabulary inspection.

For an individual exact lexical candidate in an evaluable field:

```text
row_percentage = 100 * retained row_count / 7474403
```

The denominator `7,474,403` is the frozen Increment 007 identity-admitted
source-row denominator. Raw row count remains authoritative. Percentage is
descriptive presentation and does not imply real-world unit coverage.

For an individual candidate:

```text
distinct_vocabulary_percentage = 100 * 1 / field_distinct_vocabulary_count
```

For an aggregate summary within a field:

```text
aggregate_distinct_vocabulary_percentage =
    100 * number_of_unique_candidate_lexical_values
    / field_distinct_vocabulary_count
```

The denominator is the retained Increment 007 vocabulary cardinality for that
field. No `agency_responsible` vocabulary denominator may be invented because
none was retained.

## Aggregate Coverage Contract

A cross-field unique-row union such as the percentage of rows having a
sentinel candidate in any audited field cannot be reconstructed exactly from
retained marginal vocabulary frequency tables because they do not encode
cross-field row co-occurrence. Such a union must not be claimed or fabricated.

Exact aggregate coverage is frozen per field:

```text
phase1_sentinel_candidate_row_coverage(field) =
    sum of retained row counts for UNIQUE Phase 1 sentinel candidate
    lexical values in that field
    / 7474403
```

This aggregate sentinel coverage includes Phase 1A, 1B, and 1C. It excludes
Phase 1D normalization-drift candidates. It also excludes standalone Phase 1E
matches unless the lexical value qualifies under Phase 1A/1B/1C or is
explicitly classified later as a sentinel candidate. Phase 1D and standalone
Phase 1E results are reported separately because whitespace-boundary and
control-character findings are structural or normalization anomalies, not
automatically semantic missingness.

```text
CROSS_FIELD_UNION_COVERAGE = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
```

## Materiality Thresholds

The Phase 1 sentinel thresholds apply independently to each evaluable field's
`phase1_sentinel_candidate_row_coverage(field)`:

| Per-field coverage | Prospective public-description obligation |
|---|---|
| `< 0.1%` | `FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE` |
| `>= 0.1% and <= 2.0%` | `EXPLICIT_COMPLETENESS_QUALIFICATION` |
| `> 2.0%` | `RECORDED_BASELINE_DESCRIPTION_DECISION_REQUIRED_BEFORE_PUBLICATION` |

If evaluable fields occupy different bands, the strongest obligation triggered
by any field controls the later public-description decision. Increment 008
does not make that later decision.

For Phase 3, if any single exact `LOW_INFORMATION_CANDIDATE` has
`row_percentage > 5.0%`, then:

```text
GROUPING_AXIS_INTERPRETATION_QUALIFICATION_REQUIRED = YES
```

Wherever the affected cross-tab grouping axis is later described publicly,
the presence and coverage of that low-information value must be stated. This
does not make the value missing, remove or normalize it, alter the Increment
007 denominator, or change the adapter.

## Public-Description Decision Boundary

Increment 008 produces evidence. It does not rewrite public wording for
Increment 007. After Increment 008 completes, if a materiality threshold
creates an obligation, a separate recorded decision must determine whether
public wording changes, what qualification is used, and whether publication
proceeds.

```text
PUBLIC_DESCRIPTION_DECISION = DEFERRED_UNTIL_AFTER_INCREMENT_008_COMPLETION
INCREMENT_007_EDIT = PROHIBITED
```

## Reclassification Boundary

No lexical candidate discovered by Increment 008 is automatically
reclassified as missing data. Reclassification would modify the semantic or
source contract and requires a future prospective increment.

```text
ADAPTER_RECLASSIFICATION = OUT_OF_SCOPE
SOURCE_CONTRACT_CHANGE = OUT_OF_SCOPE
CANDIDATE_TO_MISSING_RECLASSIFICATION = NOT_AUTHORIZED
```

## Required Phase Sequencing

Later execution must preserve this sequence:

```text
Phase 1 contract
    -> Phase 1 deterministic execution
    -> Phase 1 results retained
    -> Phase 2 exploratory inspection
    -> Phase 2 results explicitly labeled post-hoc
    -> Phase 3 separate semantic review
```

The three phases must not be performed invisibly in one exploratory script.
Phase 1 must be independently reconstructable from the frozen rules.

## Non-Goals

Increment 008 does not authorize:

- cross-tab interpretation;
- operational hypotheses;
- causal analysis;
- service-performance interpretation;
- backlog analysis;
- duration analysis;
- closure-finality analysis;
- WFM (workforce-management) analysis;
- intervention selection;
- an AI suitability conclusion;
- RAG (retrieval-augmented generation) work;
- agent work;
- PostgreSQL;
- a dashboard;
- a source-artifact rerun;
- a C1 rerun;
- a C2 rerun;
- an adapter change;
- a source-contract change;
- a correction to Increment 007; or
- public-post drafting in Increment 008.

## Claim Discipline

Prospective possible result classes are:

```text
NO_PREDECLARED_SENTINEL_CANDIDATES_OBSERVED
PREDECLARED_SENTINEL_CANDIDATES_OBSERVED
NORMALIZATION_DRIFT_CANDIDATES_OBSERVED
CONTROL_CHARACTER_CANDIDATES_OBSERVED
EXPLORATORY_SOURCE_SPECIFIC_CANDIDATES_OBSERVED
LOW_INFORMATION_CANDIDATES_OBSERVED
FIELD_NOT_EVALUABLE_FROM_RETAINED_EVIDENCE
```

These are descriptive classifications. They do not establish semantic
missingness, a data error, a source-system defect, an operational defect,
causality, or a need for intervention.

## Threats to Validity

1. Phase 1 sentinel rules are necessarily incomplete; absence of matches does
   not prove absence of all semantic missingness.
2. Phase 2 is explicitly post-hoc and vulnerable to researcher judgment.
3. Phase 3 is semantic and judgment-dependent; it is not missingness detection.
4. Retained vocabularies provide marginal field frequencies, not cross-field
   co-occurrence.
5. Exact cross-field unique-row sentinel coverage therefore cannot be
   recovered from retained marginal vocabularies.
6. `agency_responsible` lacks a retained full lexical vocabulary under the
   Increment 007 `BaselineResult` contract and is not currently evaluable
   without additional evidence generation.
7. Exact lexical equality does not establish semantic equivalence.
8. Candidate labels are not source-authoritative classifications.
9. This is an internal audit of retained evidence, not external validation.

## Failure and Stop Conditions

Increment 008 must stop rather than silently broaden scope if:

- a required retained vocabulary is absent;
- retained evidence cannot reproduce expected field counts;
- candidate row counts do not reconcile with retained vocabulary counts;
- implementation would require the Calgary source artifact;
- `agency_responsible` cannot be evaluated without new evidence generation;
- a proposed deterministic rule requires extension after vocabulary
  inspection; or
- Phase 1 and exploratory Phase 2 evidence cannot be kept distinct.

These conditions must not be solved silently.

## Prospective Classifications

```text
CHANGE_TYPE = PROSPECTIVE_ANALYTICAL_CONTRACT
INCREMENT_008_STATUS = PLANNED
INCREMENT_007_STATUS = CLOSED_UNCHANGED
PRIMARY_QUESTION = SOURCE_NATIVE_SENTINEL_AND_MISSINGNESS_GAP
PHASE_1 = PREDECLARED_DETERMINISTIC
PHASE_2 = EXPLORATORY_POST_HOC
PHASE_3 = LOW_INFORMATION_SEPARATE_FROM_SENTINELS
SOURCE_ARTIFACT_REREAD = PROHIBITED
ADAPTER_CHANGE = OUT_OF_SCOPE
INCREMENT_007_CORRECTION = OUT_OF_SCOPE
SERVICE_NAME_AUDIT = EVALUABLE_FROM_RETAINED_007_VOCABULARY
STATUS_DESCRIPTION_AUDIT = EVALUABLE_FROM_RETAINED_007_VOCABULARY
AGENCY_RESPONSIBLE_AUDIT = NOT_CURRENTLY_EVALUABLE_FROM_RETAINED_007_VOCABULARIES
CROSS_FIELD_UNION_COVERAGE = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
PUBLIC_DESCRIPTION_DECISION = DEFERRED_UNTIL_AFTER_INCREMENT_008_COMPLETION
VOCABULARY_CONTENTS_INSPECTED = NO
AUDIT_CODE_IMPLEMENTED = NO
AUDIT_EXECUTED = NO
FINDINGS = NOT_OBSERVED
```

## Phase 1 Executable RED Contract

The deterministic Phase 1 rules now have a prospective executable contract in
`tests/test_source_native_sentinel_audit.py`. The test module contains 13
focused `unittest.TestCase` methods and uses only the Python standard library.
It imports these prospective public objects from the intentionally absent
`support_operations_intelligence.source_native_sentinel_audit` module:

```text
PHASE1_SENTINEL_VALUES
Phase1Candidate
Phase1FieldAuditResult
audit_phase1_field
```

The executable boundary freezes a pure retained-vocabulary audit:

```text
audit_phase1_field(
    field_name,
    vocabulary_rows,
    row_denominator,
) -> Phase1FieldAuditResult
```

The tests freeze the exact immutable Phase 1C sentinel collection; Phase
1A-1E matching behavior; observed versus unavailable evidence; exact candidate
identity; deterministic matched-check and candidate ordering; overlap without
row-count duplication; separate normalization-drift and standalone-control
coverage; fail-closed malformed-input behavior; and vocabulary-count
reconciliation against the row denominator.

The prospective result boundary retains candidate field and exact lexical
value, `PHASE_1`, matched checks, deterministic reporting classification, row
count, exact and six-decimal row percentage, and exact and six-decimal
vocabulary percentage. The field result retains evaluability, denominator,
distinct vocabulary count, deterministic candidates, aggregate sentinel
counts and coverage, materiality classification, and separate Phase 1D and
standalone Phase 1E counts and coverage. No candidate is labeled
`MISSING_DATA`.

Percentage calculations are `Decimal` values derived from integer counts.
Display uses six decimal places and `ROUND_HALF_EVEN`; materiality decisions
use the unrounded `Decimal` percentage. Synthetic tests freeze the boundaries
just below 0.1%, exactly 0.1%, exactly 2.0%, and just above 2.0%.

The evaluability boundary remains:

```text
service_name = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
status_description = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

No agency denominator or candidate coverage is invented.

### Test Source Syntax Check

Command:

```bash
.venv/bin/python -m py_compile \
  tests/test_source_native_sentinel_audit.py
```

Observed result: PASS.

### Focused RED Command

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit \
  -v
```

Observed result: RED, exit status 1. The unittest loader reported one import
error before the 13 prospective test methods could execute:

```text
ModuleNotFoundError: No module named
'support_operations_intelligence.source_native_sentinel_audit'
```

The RED is attributable exactly to the missing Phase 1 production module. The
module was not implemented, and the full regression was not run at this RED
checkpoint.

### Phase 1 RED Classifications

```text
CHANGE_TYPE = PHASE_1_RED_TEST_CONTRACT_AND_EXECUTABLE_BOUNDARY
PHASE_1_TEST_CONTRACT = IMPLEMENTED
PHASE_1_PRODUCTION_IMPLEMENTATION = ABSENT
PHASE_1_FOCUSED_TEST_STATE = RED
PHASE_1_RED_CAUSE = MISSING_PHASE_1_PRODUCTION_MODULE
VOCABULARY_CONTENT_INSPECTED = NO
REAL_BASELINE_JSON_OPENED = NO
CALGARY_SOURCE_ACCESSED = NO
INCREMENT_007_MODIFIED = NO
SERVICE_NAME_EVALUABILITY = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
STATUS_DESCRIPTION_EVALUABILITY = EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARY
AGENCY_RESPONSIBLE_EVALUABILITY = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
PHASE_1_RESULTS = NOT_OBSERVED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
```

## Phase 1 Executable GREEN Checkpoint

The pure deterministic Phase 1 implementation now exists at:

```text
src/support_operations_intelligence/source_native_sentinel_audit.py
```

Its public boundary is:

```text
PHASE1_SENTINEL_VALUES
Phase1Candidate
Phase1FieldAuditResult
audit_phase1_field(
    field_name,
    vocabulary_rows,
    row_denominator,
) -> Phase1FieldAuditResult
```

The module uses only Python standard-library facilities and performs no file
I/O, JSON loading, repository traversal, subprocess execution, Calgary source
access, or retained-baseline discovery. It receives retained vocabulary rows
as arguments.

Implemented behavior includes strict fail-closed retained-vocabulary
validation; typed `UNAVAILABLE` exclusion from lexical matching while retaining
its counts for reconciliation; exact Phase 1A-1E checks; deterministic
matched-check, primary-classification, overlap, and candidate-order behavior;
unique candidate row accounting; `Decimal` percentages derived from integer
counts; six-decimal `ROUND_HALF_EVEN` presentation; unrounded `Decimal`
materiality classification; separate normalization-drift and standalone
control-character coverage; and vocabulary-count reconciliation against the
declared row denominator.

No real vocabulary has yet been inspected. The implementation has not been
executed against retained Increment 007 evidence.

### Focused Synthetic Test Evidence

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit \
  -v
```

Observed result:

```text
tests_run = 13
failures = 0
errors = 0
result = OK
```

### Full Regression Evidence

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result:

```text
tests_run = 184
failures = 0
errors = 0
result = OK
```

The 184-test result is consistent with the prior 171-test closure suite plus
the 13 committed Phase 1 contract methods. This is internal engineering
evidence, not independent validation.

### Phase 1 GREEN Classifications

```text
CHANGE_TYPE = PHASE_1_GREEN_IMPLEMENTATION_AND_SYNTHETIC_EVIDENCE
PHASE_1_PRODUCTION_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
PHASE_1_TEST_RESULT = INTERNAL_ENGINEERING_TEST_RESULT
PHASE_1_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
REAL_PHASE_1_EXECUTION = NOT_PERFORMED
REAL_PHASE_1_FINDINGS = NOT_OBSERVED
VOCABULARY_CONTENT_INSPECTED = NO
REAL_BASELINE_JSON_OPENED = NO
CALGARY_SOURCE_ACCESSED = NO
PHASE_1_RESULTS = NOT_OBSERVED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
AGENCY_RESPONSIBLE_EVALUABILITY = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
INCREMENT_007_MODIFIED = NO
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Phase 1 Retained-Baseline Execution RED Contract

This checkpoint freezes the future retained-baseline runner and evidence
boundary before the real Increment 007 baseline JSON is opened or parsed.

### Frozen Input and Binding

The only real Phase 1 input artifact is prospectively bound as:

```text
path = /data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json
expected_size_bytes = 563023
expected_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
PHASE_1_INPUT_BINDING = INCREMENT_007_BASELINE_RESULT_SHA256
```

The SHA-256 was previously established and retained by Increment 007. The
future runner must verify it before parsing JSON. This RED-contract checkpoint
did not open, parse, hash, or otherwise inspect that retained file.

After successful digest verification and parsing, the runner must fail closed
unless these Increment 007 bindings match exactly:

```text
artifact_sha256 = 9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f
git_revision = f16c19fef3b3e6bae1c5653568b5e76cfece2f14
increment_version = "007"
contract_identifier = 007-full-artifact-execution-and-status-by-service-baseline
```

The retained Increment 007 serializer names the last JSON field `contract_id`;
its required semantic value is the frozen contract identifier above.

### Allowed Real Data Boundary

The future runner may semantically consume only:

- `counter_summary.service_name_vocabulary`;
- `counter_summary.status_vocabulary`; and
- `counter_summary.rows_identity_admitted` as the row denominator.

The expected retained denominator is `7474403`, but the runner must supply the
bound BaselineResult counter to both field audits rather than hard-coding it.
It must not analyze cross-tab contents, claims, historical comparison, timing
metrics, percentages, or service/status combinations.

```text
REAL_PHASE_1_ALLOWED_DATA = RETAINED_SERVICE_AND_STATUS_VOCABULARIES_ONLY
```

The result must also contain this explicit third field state without invented
counts, coverage, or materiality:

```text
field = agency_responsible
evaluable = false
reason = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

### Frozen Result Path and Binding

The future output is external to Git:

```text
output_directory = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001
output_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json
PHASE_1_RESULT_STORAGE = EXTERNAL_TO_GIT
```

The directory and file must not preexist before real execution. Neither was
created in this checkpoint. External storage does not establish durable
independent archival.

The output binding must retain:

```text
increment_008_version = "008"
increment_008_contract = 008-source-native-sentinel-and-missingness-audit
phase = "PHASE_1"
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
input_increment_007_git_revision = f16c19fef3b3e6bae1c5653568b5e76cfece2f14
audit_code_git_revision = CAPTURED_AT_REAL_EXECUTION_TIME
python_version = CAPTURED_AT_REAL_EXECUTION_TIME
run_date_utc = CAPTURED_AT_REAL_EXECUTION_TIME
```

The audit-code Git revision is provenance, not independent validation.

### Frozen Result Structure and Serialization

The deterministic Phase 1 JSON contains a binding object; evaluable
`service_name` and `status_description` field results; an explicit
not-evaluable `agency_responsible` field result; and a summary. It contains no
Phase 2 or Phase 3 section, cross-tab contents, or operational interpretation.

Each evaluable field serializes the existing `Phase1FieldAuditResult`
semantics: field, `evaluable = true`, denominator, vocabulary cardinality,
candidate count and rows, aggregate sentinel counts and display percentages,
materiality returned by the engine, normalization-drift coverage, and
standalone control-character coverage. The runner must not independently
recalculate thresholds from rounded strings.

Each candidate retains its field, exact lexical value, phase, matched checks,
classification, row count, row percentage, and vocabulary percentage. The
decoded lexical string must exactly equal the audited value; only ordinary JSON
syntax escaping is permitted.

The summary retains separate `service_name`, `status_description`, and
`agency_responsible` entries. It must not compute a numeric cross-field union:

```text
CROSS_FIELD_SENTINEL_UNION = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
```

Output is UTF-8 JSON with stable recursive object-key ordering, deterministic
engine candidate ordering, Decimal-derived display strings, and a terminating
newline. Binary float percentages and `repr` serialization are prohibited.

### Frozen Failure and CLI Boundary

The future runner returns nonzero and does not intentionally produce a
successful result when digest verification, JSON parsing, required binding,
required vocabulary or denominator validation, Phase 1 audit execution, or
result writing fails. There is no structured failure artifact, automatic
rerun, or fallback to Calgary source data.

The prospective CLI is:

```bash
PYTHONPATH=src .venv/bin/python -m \
  support_operations_intelligence.source_native_sentinel_audit_run \
  --baseline-result <path> \
  --expected-baseline-sha256 <sha256> \
  --output <path>
```

No Calgary CSV, Phase 2, or Phase 3 argument exists.

### Runner Test Source Syntax Check

Command:

```bash
.venv/bin/python -m py_compile \
  tests/test_source_native_sentinel_audit_run.py
```

Observed result: PASS. The prospective contract contains eight focused
standard-library `unittest.TestCase` methods using synthetic temporary files.

### Focused Runner RED Command

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit_run \
  -v
```

Observed result: RED, exit status 1. The unittest loader reported one import
error before the eight prospective methods could execute:

```text
ModuleNotFoundError: No module named
'support_operations_intelligence.source_native_sentinel_audit_run'
```

The RED cause is exactly the absent Phase 1 retained-baseline runner. No full
regression was run at this RED checkpoint; the retained full regression remains
184 tests, 0 failures, 0 errors, `OK`.

### Phase 1 Retained-Baseline Runner RED Classifications

```text
CHANGE_TYPE = PHASE_1_REAL_EXECUTION_RED_CONTRACT
PHASE_1_ENGINE = IMPLEMENTED_AND_SYNTHETICALLY_GREEN
PHASE_1_RUNNER_TEST_CONTRACT = IMPLEMENTED
PHASE_1_RUNNER_IMPLEMENTATION = ABSENT
PHASE_1_RUNNER_FOCUSED_STATE = RED
PHASE_1_RUNNER_RED_CAUSE = MISSING_PHASE_1_RUNNER_MODULE
REAL_BASELINE_JSON_OPENED = NO
REAL_VOCABULARY_CONTENT_INSPECTED = NO
REAL_PHASE_1_EXECUTION = NOT_PERFORMED
REAL_PHASE_1_FINDINGS = NOT_OBSERVED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
INCREMENT_007_MODIFIED = NO
```

## Current Status

Increment 008 remains in progress. The deterministic Phase 1 engine is GREEN
under synthetic tests, and its retained-baseline execution boundary now has an
executable RED contract. The runner implementation is absent, so the focused
runner test state is RED for the expected missing-module cause. The real
baseline JSON was not opened, real vocabulary contents were not inspected, and
real Phase 1 execution and findings remain unobserved. Phase 2 and Phase 3 have
not started.

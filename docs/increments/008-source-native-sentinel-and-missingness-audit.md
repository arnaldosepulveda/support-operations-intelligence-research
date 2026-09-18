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

## Phase 1 Retained-Baseline Runner GREEN Checkpoint

The synthetic-tested retained-baseline runner now exists at:

```text
src/support_operations_intelligence/source_native_sentinel_audit_run.py
```

It exposes `main(argv: Sequence[str] | None = None) -> int` and the frozen CLI
arguments `--baseline-result`, `--expected-baseline-sha256`, and `--output`.
The module contains no hard-coded real baseline or result path.

Implemented behavior verifies the supplied baseline SHA-256 by streaming binary
read before JSON parsing; parses only after exact digest equality; validates the
four frozen Increment 007 bindings; extracts only the two authorized vocabulary
lists and the dynamic `rows_identity_admitted` denominator; calls
`audit_phase1_field` exactly once for `service_name` and once for
`status_description`; and never calls the engine for `agency_responsible`.

The runner preserves the Phase 1 engine result without recalculating rules or
materiality. It serializes exact candidate lexical values and engine-produced
display percentages, retains an explicit not-evaluable agency field, binds the
result to the input digest and Increment 007 revision, captures repository-local
audit-code Git revision plus Python and timezone-aware UTC metadata, and records
the cross-field sentinel union as not reconstructable rather than fabricating a
numeric union.

Output is deterministic UTF-8 JSON with recursively stable object-key ordering,
engine candidate ordering, and a terminating newline. Successful output is
opened only after digest, parsing, binding, denominator, both engine calls,
metadata capture, result construction, and serialization succeed. Failures
return nonzero with bounded stderr context and no intentional successful result,
retry, source fallback, Phase 2 behavior, or Phase 3 behavior.

The runner has been exercised only with synthetic temporary fixtures. The real
Increment 007 baseline JSON was not opened or hashed, no real vocabulary was
inspected, and the real Increment 008 result directory or file was not created.

### Focused Runner Synthetic Test Evidence

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit_run \
  -v
```

Observed result:

```text
tests_run = 8
failures = 0
errors = 0
result = OK
```

### Phase 1 Engine Regression Evidence

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

### Full Regression Evidence After Runner Implementation

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result:

```text
tests_run = 192
failures = 0
errors = 0
result = OK
```

The observed total is consistent with the prior 184-test suite plus the eight
committed runner-contract methods. This remains internal engineering evidence,
not independent validation.

### Phase 1 Runner GREEN Classifications

```text
CHANGE_TYPE = PHASE_1_RUNNER_GREEN_IMPLEMENTATION_AND_SYNTHETIC_EVIDENCE
PHASE_1_ENGINE = IMPLEMENTED_AND_SYNTHETICALLY_GREEN
PHASE_1_RUNNER_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
PHASE_1_RUNNER_TEST_RESULT = INTERNAL_ENGINEERING_TEST_RESULT
PHASE_1_RUNNER_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
REAL_BASELINE_JSON_OPENED = NO
REAL_VOCABULARY_CONTENT_INSPECTED = NO
REAL_PHASE_1_EXECUTION = NOT_PERFORMED
REAL_PHASE_1_FINDINGS = NOT_OBSERVED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
AGENCY_RESPONSIBLE_EVALUABILITY = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
INCREMENT_007_MODIFIED = NO
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Phase 1 Real Execution Manifest

This manifest freezes the one authorized future real Phase 1 execution before
the retained Increment 007 BaselineResult is opened, hashed, parsed, or
inspected for Increment 008. The runner implementation revision before this
manifest is:

```text
pre_manifest_runner_implementation_revision = f5a1bf3b7d6c7e0223dc621eba3f4588fac9bc4e
```

The manifest itself is documentation only. The real audit has not been
executed and the real result JSON has not been created.

### Frozen Input and Metadata-Only Observation

```text
baseline_result_path = /data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json
baseline_regular_file = YES
baseline_readable = YES
baseline_size_bytes = 563023
expected_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
```

Only file existence, readability, and size metadata were checked. The baseline
contents were not opened or parsed, its SHA-256 was not recomputed, and no real
vocabulary content was inspected. The expected digest above is the value
independently retained by Increment 007; the future runner must verify that
exact digest before parsing.

### Frozen Output and Non-Overwrite Policy

```text
run_directory = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001
run_directory_manifest_state = CREATED_EMPTY_FOR_FUTURE_EXECUTION
result_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json
result_preexistence = ABSENT
```

If `phase1-sentinel-audit.json` exists before execution, execution must stop.
The result must not be overwritten, `run-002` must not be selected
automatically, and a different run directory requires a new prospective
execution record. No repository file may be placed in the external run
directory.

### Frozen Execution Bindings

A successful result must bind to exactly:

```text
increment_008_contract = 008-source-native-sentinel-and-missingness-audit
phase = PHASE_1
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
input_increment_007_git_revision = f16c19fef3b3e6bae1c5653568b5e76cfece2f14
input_increment_007_artifact_sha256 = 9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f
audit_code_git_revision = POST_MANIFEST_COMMIT_HEAD_AT_REAL_EXECUTION
```

The future `audit_code_git_revision` is the Git HEAD produced by committing
this manifest, provided no repository changes occur before execution. It is
not the pre-manifest runner implementation revision
`f5a1bf3b7d6c7e0223dc621eba3f4588fac9bc4e`.

### Frozen Real Data-Access Boundary

The future execution may consume only:

- `counter_summary.service_name_vocabulary`;
- `counter_summary.status_vocabulary`;
- `counter_summary.rows_identity_admitted`; and
- the Increment 007 binding fields required for validation.

The agency boundary remains:

```text
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

This manifest does not authorize service/status cross-tab inspection or
interpretation, Phase 2 inspection, Phase 3 semantic review, or Calgary source
access.

### Frozen Exact Future Command

The future real command is exactly:

```bash
BASELINE='/data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json'
EXPECTED_BASELINE_SHA256='2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c'
RUN_DIR='/data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001'
PHASE1_RESULT="$RUN_DIR/phase1-sentinel-audit.json"

PYTHONPATH=src \
.venv/bin/python -m \
support_operations_intelligence.source_native_sentinel_audit_run \
  --baseline-result "$BASELINE" \
  --expected-baseline-sha256 "$EXPECTED_BASELINE_SHA256" \
  --output "$PHASE1_RESULT"
```

This command was not executed during the manifest step.

### Frozen Attempt and Failure Accounting

```text
REAL_PHASE_1_EXECUTION_ATTEMPTS = 1
```

The future command must be executed exactly once. If it returns nonzero, any
produced evidence must be preserved, the command must not be rerun, execution
must stop, and the failure must be recorded in Increment 008 before any
remediation. If it succeeds, the result must be preserved and Phase 2 must not
begin until the retained result has been reconciled.

### First Authorized Inspection Boundary

The future real Phase 1 command is the first authorized opening and parsing of
the retained Increment 007 BaselineResult for Increment 008. It is also the
first authorized inspection of `service_name_vocabulary` and
`status_vocabulary` under the committed Phase 1 rules. No vocabulary contents
were inspected before this manifest.

### Frozen Successful Result Scope

A successful result may report only deterministic Phase 1 evidence:

- `service_name` sentinel candidates;
- `status_description` sentinel candidates;
- normalization-drift candidates;
- standalone control-character candidates;
- exact lexical values;
- row counts;
- six-decimal display percentages;
- vocabulary percentages;
- field-level materiality classifications;
- the explicit agency not-evaluable result; and
- the non-reconstructable cross-field union state.

It may contain no Phase 2 finding, Phase 3 finding, or operational
interpretation.

### Frozen Post-Success Sequence

```text
NEXT_STEP = RETAINED_PHASE_1_RESULT_RECONCILIATION
```

After success, the retained result must first be independently checked against
the frozen Phase 1 reporting and arithmetic contract. Before that
reconciliation, no lexical candidate may be interpreted, the sentinel list
may not be extended, Phase 2 or Phase 3 may not start, public wording may not
change, and Increment 007 may not be edited.

### Phase 1 Real Execution Manifest Classifications

```text
CHANGE_TYPE = PHASE_1_REAL_EXECUTION_MANIFEST
PHASE_1_ENGINE = IMPLEMENTED_AND_SYNTHETICALLY_GREEN
PHASE_1_RUNNER = IMPLEMENTED_AND_SYNTHETICALLY_GREEN
REAL_BASELINE_JSON_OPENED = NO
REAL_BASELINE_SHA_RECOMPUTED = NO
REAL_VOCABULARY_CONTENT_INSPECTED = NO
REAL_PHASE_1_EXECUTION = NOT_PERFORMED
REAL_PHASE_1_FINDINGS = NOT_OBSERVED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
INCREMENT_007_MODIFIED = NO
```

## Phase 1 Real Execution Result

The frozen Phase 1 command executed exactly once against the retained
Increment 007 `BaselineResult` and succeeded. The committed runner performed
the first authorized opening and parsing of that retained result for Increment
008.

```text
execution_bound_git_revision = 426b09bb528c2af09fb60590c8e3ec4ed56fc3fb
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
phase1_result_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json
phase1_result_size_bytes = 3039
phase1_result_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82
run_date_utc = 2026-09-18T14:22:45.999555+00:00
python_version = 3.12.3
execution_attempts = 1
execution_result = SUCCEEDED
reruns = 0
```

### Increment 007 Input Reconciliation

The retained Increment 007 bindings and the two authorized marginal
vocabularies reconciled exactly:

```text
INCREMENT_007_BINDING_RECONCILIATION = PASS
artifact_sha256 = 9f12fa4324430a87096551bd11ac292dcbd13e6045e84e87ef54118448aa878f
git_revision = f16c19fef3b3e6bae1c5653568b5e76cfece2f14
increment_version = 007
contract_id = 007-full-artifact-execution-and-status-by-service-baseline
rows_identity_admitted = 7474403
service_name_vocabulary_cardinality = 1169
service_name_vocabulary_row_count_sum = 7474403
status_description_vocabulary_cardinality = 5
status_description_vocabulary_row_count_sum = 7474403
VOCABULARY_RECONCILIATION = PASSED
```

### `service_name` Phase 1 Result

Exactly one Phase 1 candidate was observed:

| Field | Exact lexical value | Matched check | Classification | Row count | Row percentage | Vocabulary percentage |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `service_name` | `"N/A"` | `PHASE_1C_CASE_INSENSITIVE_EXACT_SENTINEL` | `SENTINEL_CANDIDATE` | 8,721 | 0.116678% | 0.085543% |

Increment 008 identifies `"N/A"` only as a deterministic lexical sentinel
candidate under the predeclared Phase 1C rule. It does not classify these rows
as missing data and does not establish what `"N/A"` means operationally.

The field-level result is:

```text
PHASE_1_CANDIDATE_COUNT = 1
AGGREGATE_SENTINEL_CANDIDATE_COUNT = 1
AGGREGATE_SENTINEL_ROW_COUNT = 8721
AGGREGATE_SENTINEL_ROW_PERCENTAGE = 0.116678
AGGREGATE_SENTINEL_VOCABULARY_COUNT = 1
AGGREGATE_SENTINEL_VOCABULARY_PERCENTAGE = 0.085543
MATERIALITY_CLASSIFICATION = EXPLICIT_COMPLETENESS_QUALIFICATION
NORMALIZATION_DRIFT_CANDIDATES = 0
NORMALIZATION_DRIFT_ROWS = 0
NORMALIZATION_DRIFT_ROW_PERCENTAGE = 0.000000
STANDALONE_CONTROL_CHARACTER_CANDIDATES = 0
STANDALONE_CONTROL_CHARACTER_ROWS = 0
STANDALONE_CONTROL_CHARACTER_ROW_PERCENTAGE = 0.000000
```

The materiality classification follows mechanically from the predeclared
threshold because `0.1% <= 0.116678% <= 2.0%`. The classification itself was
calculated from the unrounded `Decimal` value; the six-decimal value is display
evidence and was not used as a substitute threshold input.

### `status_description` Phase 1 Result

```text
NO_PHASE_1_CANDIDATES
PHASE_1_CANDIDATE_COUNT = 0
AGGREGATE_SENTINEL_ROW_COUNT = 0
AGGREGATE_SENTINEL_ROW_PERCENTAGE = 0.000000
AGGREGATE_SENTINEL_VOCABULARY_COUNT = 0
AGGREGATE_SENTINEL_VOCABULARY_PERCENTAGE = 0.000000
MATERIALITY_CLASSIFICATION = FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE
NORMALIZATION_DRIFT_CANDIDATES = 0
STANDALONE_CONTROL_CHARACTER_CANDIDATES = 0
```

Zero Phase 1 candidates does not establish universal semantic completeness for
`status_description`.

### `agency_responsible` and Cross-Field Boundaries

```text
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
CROSS_FIELD_SENTINEL_UNION = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
```

No agency candidate count, vocabulary denominator, row coverage, or
materiality classification was invented. Phase 1 therefore does not establish
whether `agency_responsible` contains source-native lexical sentinel values.

The 8,721 rows are a `service_name` field result only. They must not be divided
by the common row denominator and reported as a cross-field missingness or
sentinel-union rate.

## Phase 1 Retained Result Reconciliation

```text
PHASE_1_RETAINED_RESULT_RECONCILIATION = PASSED
SERVICE_CANDIDATE_MISMATCHES = 0
STATUS_CANDIDATE_MISMATCHES = 0
FIELD_AGGREGATE_MISMATCHES = 0
AGENCY_RESULT_RECONCILIATION = PASS
SUMMARY_RECONCILIATION = PASS
PHASE1_RESULT_REPRESENTATION_AUDIT = PASS
```

Independent standard-library reconciliation verified the retained result
size and hash; Increment 007 bindings; row denominator; service and status
vocabulary cardinalities and row-count sums; exact frozen sentinel set;
independent Phase 1A-1E matching; candidate identity; matched checks;
classification precedence; exact candidate row counts; `Decimal` percentage
calculations; materiality classifications; normalization-drift and standalone
control-character coverage; explicit agency non-evaluability; summary;
cross-field-union boundary; and deterministic representation.

### Established Phase 1 Evidence

For the retained Increment 007 artifact, under the predeclared deterministic
Phase 1 lexical rules, `service_name` contains one lexical sentinel candidate,
`"N/A"`, covering 8,721 source rows, or 0.116678% of the 7,474,403-row
denominator. `status_description` contains no Phase 1 lexical candidates.
`agency_responsible` was not evaluable from the retained Increment 007
vocabularies.

```text
RESULT_CLASSIFICATION = INTERNAL_EVALUATION_RESULT
PHASE_1_CANDIDATE = LEXICAL_CANDIDATE_ONLY
MISSING_DATA_RECLASSIFICATION = NOT_PERFORMED
SEMANTIC_MEANING_OF_N_A = NOT_ESTABLISHED
AGENCY_SENTINEL_STATE = NOT_ESTABLISHED
CROSS_FIELD_SENTINEL_UNION = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
OPERATIONAL_INTERPRETATION = NOT_PERFORMED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

This is internal evaluation evidence, not external validation.

### Contractual Publication Consequence

```text
service_name_materiality_obligation = EXPLICIT_COMPLETENESS_QUALIFICATION
status_description_materiality_obligation = FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE
```

These are predeclared contract consequences, not the final wording of any
public statement. The actual public-description decision remains deferred
until Increment 008 completes; no public wording is drafted here.

```text
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
```

### Phase 1 Documentation Classifications

```text
CHANGE_TYPE = PHASE_1_REAL_FINDINGS_DOCUMENTATION
REAL_PHASE_1_EXECUTION = SUCCEEDED
PHASE_1_RETAINED_RESULT_RECONCILIATION = PASSED
SERVICE_NAME_PHASE_1_CANDIDATES = 1
SERVICE_NAME_SENTINEL_ROW_COUNT = 8721
SERVICE_NAME_SENTINEL_ROW_PERCENTAGE = 0.116678
SERVICE_NAME_MATERIALITY = EXPLICIT_COMPLETENESS_QUALIFICATION
STATUS_DESCRIPTION_PHASE_1_CANDIDATES = 0
STATUS_DESCRIPTION_MATERIALITY = FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE
AGENCY_RESPONSIBLE = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
MISSING_DATA_RECLASSIFICATION = NOT_PERFORMED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
PHASE_2 = NOT_STARTED
PHASE_3 = NOT_STARTED
INCREMENT_008_STATUS = IN_PROGRESS
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Phase 2 Exploratory Review Contract

Phase 2 asks whether the retained `service_name` and `status_description`
vocabularies contain source-specific lexical forms that plausibly encode
missing, unknown, unavailable, not-provided, or placeholder states but were
not captured by the predeclared deterministic Phase 1 rules.

```text
PHASE_2_CLASSIFICATION = EXPLORATORY_POST_HOC
PHASE_2_CONFIRMATORY_STATUS = NOT_CONFIRMATORY
```

Phase 2 findings are hypotheses for possible future confirmatory work. They do
not amend the frozen Phase 1 sentinel list, automatically become missing-data
classifications, or establish source semantics.

### Phase 2 Evaluability and Review Universe

```text
service_name = EVALUABLE
status_description = EVALUABLE
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

No agency Phase 2 review, denominator, or candidate evidence may be invented.
The authorized review universe consists only of exact `OBSERVED` lexical values
from `service_name_vocabulary` and `status_vocabulary`. A value already
classified as a Phase 1 candidate is excluded from new Phase 2 candidate
classification.

The already-established Phase 1 `service_name` candidate `"N/A"` remains
Phase 1 evidence and must not be relabeled as a Phase 2 candidate. Based only
on already-established cardinalities, the expected Phase 2 universe is:

```text
service_name_vocabulary_values = 1169
known_phase_1_service_values_excluded = 1
service_values_expected = 1168
status_description_vocabulary_values = 5
known_phase_1_status_values_excluded = 0
status_values_expected = 5
total_phase_2_values_expected = 1173
```

These expected counts must be reconciled when the review artifact is created.
No remaining lexical value was inspected while defining this contract.

### Two-Stage Count-Blinded Review

Phase 2 review must occur in two distinct stages to reduce prevalence bias.

#### Stage A - Lexical Screening

During initial classification the reviewer sees only:

- field; and
- exact lexical value.

The reviewer must not see:

- row count;
- row percentage;
- vocabulary percentage;
- frequency rank; or
- cross-tab context.

```text
COUNTS_VISIBLE_DURING_INITIAL_PHASE_2_SCREEN = NO
```

All Stage A decisions must be completed and frozen before quantitative values
are attached.

#### Stage B - Quantitative Attachment

Only after the complete Stage A decision set is retained may Stage B join the
retained row counts to flagged candidates. Each Phase 2 candidate then retains:

- `row_count`;
- row percentage of `7474403`; and
- vocabulary percentage for its field.

Arithmetic must use `Decimal` directly from integer counts, six decimal places
for display, and `ROUND_HALF_EVEN`. Binary-float-first calculation is not
permitted.

### Deterministic Ordering and Exact Representation

Review entries must be presented in deterministic order by field and then by
exact Python lexical string order. Field order is:

1. `service_name`;
2. `status_description`.

Entries must not be ordered by count, frequency, Phase 1 similarity, perceived
importance, or semantic category.

The decoded exact lexical value is authoritative. Human-visible presentation
uses an unambiguous escaped form equivalent to
`json.dumps(value, ensure_ascii=False)`. This display operation must not trim,
case-normalize, replace whitespace, canonicalize, or rename a value.

### Stage A Decision Contract

Every reviewed value receives exactly one decision:

```text
NO_PHASE_2_FLAG
EXPLORATORY_SENTINEL_CANDIDATE
```

No undecided entry may remain in a completed artifact. Phase 2 must not emit
`MISSING_DATA`, `CONFIRMED_SENTINEL`, `INVALID_VALUE`, `BAD_DATA`, or
`LOW_INFORMATION`.

A value may receive `EXPLORATORY_SENTINEL_CANDIDATE` only when its exact
lexical form plausibly denotes absence, an unknown state, an unavailable
state, a not-provided state, or a placeholder state. The reviewer must retain
a concise rationale referring to the lexical form itself.

Operational frequency, cross-tab behavior, service context, external source
meaning, and assumed workflow semantics must not determine the Stage A
decision.

### Phase 2 Exclusions and Phase 3 Boundary

A value must not be flagged merely because it is broad, generic,
low-information, catch-all, unusual, operationally ambiguous, an acronym, a
workflow category, a lifecycle category, rare, common, or inconvenient for
analysis. Those properties belong to the separately declared Phase 3 question
unless the exact lexical form independently denotes absence, unavailability,
or placeholder semantics.

Phase 3 remains separate and has not started. This contract does not inspect
whether any conceptual Phase 3 example occurs in the retained vocabularies.

### Frozen Phase 1 Boundary

If Phase 2 encounters a form that appears suitable for a deterministic rule,
it must not be added to `PHASE1_SENTINEL_VALUES`, used to rerun Phase 1, or
relabeled as a deterministic Phase 1 finding. It may be recorded only as:

```text
EXPLORATORY_SENTINEL_CANDIDATE
```

Any deterministic rule expansion requires a future prospectively defined
increment.

### Exhaustive Review Accounting

The retained review artifact must contain a decision for every value in the
authorized universe and retain:

```text
service_values_expected
service_values_reviewed
status_values_expected
status_values_reviewed
phase1_values_excluded
phase2_candidates
no_flag_values
```

Successful completion requires:

```text
service_values_reviewed = service_values_expected
status_values_reviewed = status_values_expected
phase2_candidates + no_flag_values = total_reviewed_values
```

No silent omission is permitted.

### Reviewer and Judgment Record

The retained review process must record at minimum:

- review date and time;
- review procedure version, bound to the Increment 008 Phase 2 contract
  revision; and
- `reviewer_role = PROJECT_RESEARCHER`.

The record must not claim independent review, external validation, or
inter-rater agreement unless those events later occur. Software assistance for
presentation or recording does not create independent validation.

```text
PHASE_2_CLASSIFICATION_TYPE = EXPLORATORY_REVIEWER_JUDGMENT
```

Phase 2 results may be affected by reviewer subjectivity, omission, prior
knowledge, and lexical interpretation. This is an explicit validity boundary.

Every `EXPLORATORY_SENTINEL_CANDIDATE` must retain:

- field;
- exact lexical value;
- decision; and
- concise lexical rationale.

No flagged candidate may omit its rationale. `NO_PHASE_2_FLAG` entries need
not include a substantive rationale beyond the decision.

### Stage A Artifact Concept

A future externally retained Stage A review artifact will contain all 1,173
expected review entries, subject to reconciliation. Each row or object contains
only:

- field;
- exact lexical value;
- review decision; and
- candidate rationale when flagged.

It contains no row counts, percentages, cross-tab data, or Phase 3
classification. Its exact external path and schema must be frozen before Phase
2 execution. The artifact is not created by this contract checkpoint.

### Phase 2 Coverage Semantics

After Stage B, coverage must be retained separately for `service_name` and
`status_description`:

- candidate lexical-value count;
- candidate row count;
- candidate row percentage; and
- candidate vocabulary percentage.

No numeric cross-field union may be computed:

```text
CROSS_FIELD_PHASE_2_UNION = NOT_RECONSTRUCTABLE_FROM_RETAINED_MARGINAL_VOCABULARIES
```

Phase 1 and Phase 2 remain distinct result classes:

```text
PHASE_1_CONFIRMED_DETERMINISTIC_CANDIDATES
PHASE_2_EXPLORATORY_CANDIDATES
```

Phase 2 candidate rows must not be added to the Phase 1 8,721-row result and
reported as confirmed sentinel coverage or as a combined missing-row count.
Any later combined descriptive presentation must preserve the different
evidence classes explicitly.

### Phase 2 Materiality and Publication Boundary

The deterministic Phase 1 materiality results remain:

```text
service_name = EXPLICIT_COMPLETENESS_QUALIFICATION
status_description = FOOTNOTE_ONLY_NO_COMPLETENESS_WORDING_CHANGE
```

Exploratory Phase 2 findings do not independently change those classifications
and must not receive Phase 1 materiality labels as if they were confirmatory.
Phase 2 quantitative coverage may be reported descriptively, but:

```text
PHASE_2_PUBLIC_MATERIALITY_DECISION = DEFERRED_PENDING_CONFIRMATORY_DECISION
PUBLIC_DESCRIPTION_DECISION = DEFERRED
```

No public wording decision is made in Phase 2.

### Phase 2 Stop Conditions

Phase 2 must stop and preserve evidence if:

- retained vocabularies no longer reconcile to Increment 007;
- review-universe cardinalities do not reconcile;
- Phase 1 candidate exclusions do not reconcile;
- counts become visible before Stage A decisions are frozen;
- exact lexical values cannot be retained;
- the reviewer cannot distinguish placeholder judgment from the Phase 3
  low-information question;
- additional source data would be required;
- `agency_responsible` evidence would be required; or
- answering the question would require expansion of the deterministic Phase 1
  rule list.

The procedure must not change silently.

### Phase 2 Success Conditions

Phase 2 is complete only when:

- every authorized `service_name` lexical value has a retained decision;
- every authorized `status_description` lexical value has a retained decision;
- known Phase 1 candidates are excluded from Phase 2 relabeling;
- every Phase 2 candidate has a lexical rationale;
- Stage A decisions are frozen before counts are attached;
- quantitative attachments reconcile;
- agency remains explicitly not evaluable;
- no Phase 3 judgment is mixed into Phase 2; and
- no missing-data reclassification occurs.

### Phase 2-Specific Threats to Validity

The prospective review retains these unresolved threats:

1. single-reviewer subjectivity;
2. lexical-interpretation ambiguity;
3. omission risk across a large vocabulary;
4. prior knowledge of the Phase 1 `"N/A"` finding;
5. post-hoc exploratory status;
6. absence of independent second-rater evidence;
7. marginal vocabularies lack row-level cross-field overlap;
8. `agency_responsible` remains unavailable; and
9. lexical appearance does not establish source semantics.

### Phase 2 Contract Classifications

```text
PHASE_2 = PROSPECTIVE_REVIEW_CONTRACT_DEFINED
PHASE_2_CLASSIFICATION_TYPE = EXPLORATORY_REVIEWER_JUDGMENT
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_2_STAGE_A = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_PUBLIC_MATERIALITY_DECISION = DEFERRED_PENDING_CONFIRMATORY_DECISION
PHASE_3 = NOT_STARTED
MISSING_DATA_RECLASSIFICATION = NOT_PERFORMED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Phase 2 Stage A Review-Universe Export RED Contract

This checkpoint freezes the executable contract for generating the future
count-blinded Stage A lexical review universe before any additional real
`service_name` or `status_description` lexical value is inspected. The
exporter is not an auditor and makes no Phase 2 review decision.

Conceptually, the future boundary is:

```text
build_phase2_stage_a_review_universe(
    baseline_result,
    phase1_result,
) -> StageAReviewUniverse
```

### Frozen Retained-Artifact Bindings

The future exporter is bound to both retained inputs:

```text
baseline_result_path = /data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json
expected_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
phase1_result_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json
expected_phase1_result_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82
```

The exporter must verify both SHA-256 values before parsing either artifact.
Neither real file was opened, parsed, or hashed during this RED checkpoint.

### Frozen Output and Artifact Separation

```text
run_directory = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001
stage_a_review_universe_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001/phase2-stage-a-review-universe.json
future_stage_a_decisions_artifact = phase2-stage-a-decisions.json
STAGE_A_REVIEW_UNIVERSE != STAGE_A_DECISIONS
```

The run directory and artifacts are not created in this checkpoint. If the
review-universe artifact exists before real generation, generation must stop;
it must not overwrite the artifact or automatically select `run-002`.

The review-universe artifact is machine-generated input to later human review.
The decision artifact is separate reviewer-produced evidence. Review judgments
must not rewrite the generated input artifact.

### Authorized Population and Data-Driven Exclusion

Only `service_name` and `status_description` are authorized Stage A fields.
`agency_responsible` remains not evaluable from the retained Increment 007
vocabularies.

The implementation must derive excluded candidate identities from the
retained Phase 1 result using `(field, exact lexical value)`. It must not
hard-code `"N/A"` or any other value as production exclusion logic, reinterpret
the candidate semantics, or include excluded lexical values in the reviewer
entry list.

Expected real accounting invariants are:

```text
service_source_vocabulary_count = 1169
service_phase1_excluded_count = 1
service_stage_a_review_count = 1168
status_source_vocabulary_count = 5
status_phase1_excluded_count = 0
status_stage_a_review_count = 5
total_stage_a_review_count = 1173

1169 = 1 + 1168
5 = 0 + 5
```

The implementation must calculate these values from retained inputs rather
than hard-code `1168` or `1173` as construction logic. The real values are
frozen expected invariants only.

### Count-Blinded Entry Contract

Each reviewer-facing entry contains exactly:

```json
{
  "field": "...",
  "value": "..."
}
```

```text
COUNTS_VISIBLE_IN_STAGE_A_REVIEW_UNIVERSE = NO
```

Entries contain no row count, row percentage, vocabulary percentage,
frequency rank, cross-tab count, materiality classification, Phase 1 row
coverage, Phase 2 decision, rationale, or Phase 3 classification. The exporter
may internally read counts only to reconcile vocabularies and the denominator.
Only aggregate Phase 1 exclusion counts may be retained; no excluded-values
list is permitted in the reviewer artifact.

The decoded `value` must equal the retained lexical string exactly. The
exporter must not trim, casefold, normalize Unicode, replace whitespace or
control characters, canonicalize, or rename a value. JSON escaping is
serialization syntax only.

Entries are ordered first by field in this order:

1. `service_name`;
2. `status_description`.

Within each field, entries use exact Python string ordering. They are never
ordered by count, percentage, frequency, Phase 1 similarity, candidate
likelihood, or semantic category.

### Frozen Result Binding and Representation

A successful generated artifact must retain:

```text
increment_008_version = "008"
increment_008_contract = "008-source-native-sentinel-and-missingness-audit"
phase = "PHASE_2"
stage = "STAGE_A_REVIEW_UNIVERSE"
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
input_phase1_result_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82
generator_git_revision = CAPTURED_AT_REAL_GENERATION_TIME
python_version = CAPTURED_AT_REAL_GENERATION_TIME
generated_at_utc = CAPTURED_AT_REAL_GENERATION_TIME
```

These bindings provide provenance, not independent validation. Output must be
UTF-8 JSON with deterministic recursive object-key ordering, deterministic
entry ordering, and a terminating newline. It contains no binary floats,
row-level counts, decisions, or Phase 3 fields.

Successful summary accounting retains:

```text
service_source_vocabulary_count
service_phase1_excluded_count
service_stage_a_review_count
status_source_vocabulary_count
status_phase1_excluded_count
status_stage_a_review_count
total_stage_a_review_count
```

For each field, source count must equal excluded count plus review count, and
the total must equal the number of combined review entries.

### Fail-Closed Input Boundary

Generation must fail without a partial success artifact if:

- either expected file hash mismatches;
- either JSON artifact is malformed;
- Increment 007 or Phase 1 bindings mismatch;
- the retained denominator mismatches;
- a vocabulary structure is malformed or row counts do not reconcile;
- duplicate exact observed values exist;
- a Phase 1 candidate identity does not reconcile to a baseline vocabulary;
- review-universe cardinalities do not reconcile; or
- agency appears as an evaluable Stage A field.

There is no automatic retry or source fallback.

### Prospective CLI and Public Entry Point

The future production module is intentionally absent:

```text
src/support_operations_intelligence/source_native_sentinel_stage_a_run.py
```

It must expose:

```text
main(argv: Sequence[str] | None = None) -> int
```

The prospective CLI is:

```bash
PYTHONPATH=src .venv/bin/python -m \
  support_operations_intelligence.source_native_sentinel_stage_a_run \
  --baseline-result <path> \
  --expected-baseline-sha256 <sha256> \
  --phase1-result <path> \
  --expected-phase1-sha256 <sha256> \
  --output <path>
```

There is no Calgary CSV, counts-output, Phase 3, or agency argument.

### Prospective Synthetic Test Contract

The new standard-library test module is:

```text
tests/test_source_native_sentinel_stage_a_run.py
```

Its 10 prospective `unittest.TestCase` methods use synthetic temporary files
to freeze:

- verification of both hashes before either JSON parse;
- fail-closed baseline and Phase 1 bindings;
- data-driven Phase 1 candidate exclusions, including a second synthetic
  candidate identity;
- two-field entry schema and count blinding;
- absence of decisions, rationales, Phase 2 labels, and Phase 3 labels;
- exact lexical preservation;
- field-first and exact-string deterministic ordering;
- cardinality accounting and malformed-input failure;
- explicit agency non-evaluability and absence from review entries;
- deterministic result bindings and serialization; and
- nonzero failure without output, retry, or fallback.

Only synthetic values and previously documented Phase 1 evidence appear in
the tests. No real retained artifact was opened.

### Test Source Syntax Check

Command:

```bash
.venv/bin/python -m py_compile \
  tests/test_source_native_sentinel_stage_a_run.py
```

Observed result: PASS.

### Focused Stage A Export RED Command

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_stage_a_run \
  -v
```

Observed result: RED, exit status 1. The unittest loader reported one import
error before the 10 prospective test methods could execute:

```text
ModuleNotFoundError: No module named
'support_operations_intelligence.source_native_sentinel_stage_a_run'
```

The RED cause is exactly the absent Stage A export module. The exporter was not
implemented. The full regression was not run; the retained current regression
remains 192 tests, 0 failures, 0 errors, `OK`.

### Phase 2 Stage A Export RED Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_EXPORT_RED_CONTRACT
PHASE_2 = PROSPECTIVE_REVIEW_CONTRACT_DEFINED
PHASE_2_STAGE_A_EXPORT_TEST_CONTRACT = IMPLEMENTED
PHASE_2_STAGE_A_EXPORT_IMPLEMENTATION = ABSENT
PHASE_2_STAGE_A_EXPORT_FOCUSED_STATE = RED
PHASE_2_STAGE_A_EXPORT_RED_CAUSE = MISSING_STAGE_A_EXPORT_MODULE
PHASE_2_STAGE_A = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
ADDITIONAL_REAL_VOCABULARY_CONTENT_INSPECTED = NO
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
```

## Phase 2 Stage A Review-Universe Export GREEN Checkpoint

The Stage A review-universe exporter is implemented as an engineering
boundary. It verifies the retained baseline and Phase 1 result SHA-256 values
before parsing either document, validates the Increment 007 and Phase 1
bindings, and consumes only the authorized retained vocabularies and
denominator required for reconciliation.

The exporter strictly validates typed vocabulary evidence, positive counts,
exact observed strings, uniqueness, and denominator reconciliation. It derives
Phase 1 exclusions from retained `(field, exact lexical value)` candidate
identities and constructs the Stage A universe by exact set difference. No
production exclusion value is hard-coded.

Reviewer-facing entries contain only `field` and `value`. They preserve decoded
lexical strings exactly and are ordered by `service_name`, then
`status_description`, with exact Python string ordering within each field.
Artifact-level accounting reconciles source, excluded, and review counts.
`agency_responsible` remains explicitly not evaluable and cannot become a
review entry.

The output is deterministic UTF-8 JSON with recursively sorted object keys and
a terminating newline. Output creation occurs only after both hashes, both
documents, all bindings, vocabulary reconciliation, exclusions, cardinality,
metadata, and serialization succeed. Failures return nonzero without a
success artifact, retry, or fallback. The exporter contains no review
decisions, rationales, Phase 3 heuristics, or hard-coded real artifact paths.

```text
ADDITIONAL_REAL_VOCABULARY_CONTENT_INSPECTED = NO
REAL_STAGE_A_UNIVERSE_GENERATED = NO
```

### Synthetic Engineering Test Evidence

Focused Stage A export command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_stage_a_run \
  -v
```

Observed result: 10 tests, 0 failures, 0 errors, `OK`.

Phase 1 regression command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit \
  tests.test_source_native_sentinel_audit_run \
  -q
```

Observed result: 21 tests, 0 failures, 0 errors, `OK`.

Full repository regression command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result: 202 tests, 0 failures, 0 errors, `OK`. This matches the
plausible expected total of 192 previously committed tests plus 10 committed
Stage A prospective tests.

These results are internal engineering evidence under synthetic tests, not
independent validation. No real retained artifact was opened, parsed, or
hashed, and no real Stage A review universe was generated.

### Phase 2 Stage A Export GREEN Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_EXPORT_GREEN_IMPLEMENTATION
PHASE_2_STAGE_A_EXPORT_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
PHASE_2_STAGE_A_EXPORT_TEST_RESULT = INTERNAL_ENGINEERING_TEST_RESULT
PHASE_2_STAGE_A_EXPORT_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
ADDITIONAL_REAL_VOCABULARY_CONTENT_INSPECTED = NO
REAL_STAGE_A_UNIVERSE_GENERATED = NO
PHASE_2_STAGE_A = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

## Phase 2 Stage A Real Generation Manifest

This prospective manifest freezes one future real Stage A review-universe
generation attempt. It does not execute the exporter or authorize human
review. The Stage A exporter implementation commit is:

```text
0cbaf75cd2e4665143d2072ddd0654022c173405
```

### Retained Inputs and Metadata-Only Verification

```text
baseline_result_path = /data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json
baseline_size_bytes = 563023
expected_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c

phase1_result_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json
phase1_result_size_bytes = 3039
expected_phase1_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82

increment_007_execution_revision = f16c19fef3b3e6bae1c5653568b5e76cfece2f14
increment_008_phase1_execution_revision = 426b09bb528c2af09fb60590c8e3ec4ed56fc3fb
increment_008_contract = 008-source-native-sentinel-and-missingness-audit

REAL_INPUT_ARTIFACTS_OPENED_DURING_MANIFEST = NO
REAL_INPUT_ARTIFACT_HASHES_RECOMPUTED_DURING_MANIFEST = NO
```

Existence, readability, and byte sizes were checked through filesystem
metadata only. Neither retained input was opened, parsed, or rehashed. The
expected digests above are already-retained evidence identities. The future
exporter must verify both exact digests before parsing either artifact.

### Output and Non-Overwrite Boundary

```text
run_directory = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001
run_directory_state = CREATED_EMPTY_DURING_MANIFEST
stage_a_review_universe_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001/phase2-stage-a-review-universe.json
output_preexistence = ABSENT
```

The run directory was created empty during this manifest step. The output
artifact was not created. If the frozen output exists before future real
generation, execution must stop: do not overwrite or delete it, and do not
automatically select `run-002`. A different run requires a new prospective
execution record.

The exporter implementation commit is provenance for the implemented
boundary, but it is not the future artifact's `generator_git_revision`. The
manifest commit produced by this step becomes the execution-bound revision,
provided no repository change occurs before generation.

### Expected Real Accounting Invariants

These already-established invariants are prospective reconciliation targets,
not hard-coded production construction logic:

```text
service_source_vocabulary_count = 1169
service_phase1_excluded_count = 1
service_stage_a_review_count = 1168
1169 = 1 + 1168

status_source_vocabulary_count = 5
status_phase1_excluded_count = 0
status_stage_a_review_count = 5
5 = 0 + 5

total_stage_a_review_count = 1173
```

Each reviewer-facing entry may contain only `field` and `value`. Entries must
not expose counts, percentages, frequency, rank, materiality, cross-tab
context, decisions, rationales, or Phase 3 classifications. Artifact-level
cardinality accounting remains permitted.

```text
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_1_EXCLUSION_SOURCE = RETAINED_PHASE_1_RESULT
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
```

The exporter must derive exclusions from retained Phase 1 candidate identities
and must not hard-code any lexical value. No retained Phase 1 candidate may
appear in reviewer entries; only aggregate exclusion accounting may appear.
No agency entry or synthesized agency vocabulary is permitted.

### Exact Frozen Real Generation Command

```bash
BASELINE='/data/repos/personal/support-operations-intelligence-results/increment-007/run-001/baseline-result.json'
EXPECTED_BASELINE_SHA256='2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c'

PHASE1_RESULT='/data/repos/personal/support-operations-intelligence-results/increment-008/phase-1/run-001/phase1-sentinel-audit.json'
EXPECTED_PHASE1_SHA256='f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82'

RUN_DIR='/data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001'
STAGE_A_UNIVERSE="$RUN_DIR/phase2-stage-a-review-universe.json"

PYTHONPATH=src \
.venv/bin/python -m \
support_operations_intelligence.source_native_sentinel_stage_a_run \
  --baseline-result "$BASELINE" \
  --expected-baseline-sha256 "$EXPECTED_BASELINE_SHA256" \
  --phase1-result "$PHASE1_RESULT" \
  --expected-phase1-sha256 "$EXPECTED_PHASE1_SHA256" \
  --output "$STAGE_A_UNIVERSE"
```

The command was frozen but not executed in this manifest step.

### One-Attempt and Access Boundaries

The frozen command will be executed exactly once in the future real-generation
step.

```text
REAL_STAGE_A_GENERATION_ATTEMPTS_PROSPECTIVE_LIMIT = 1
```

If the command returns nonzero, preserve any produced evidence, do not rerun,
do not repair within that execution step, and record the failure before any
remediation. If it returns zero, preserve the generated universe and reconcile
it before human review.

That future command is the first authorized post-Phase-1 machine access to the
remaining real `service_name` and `status_description` lexical vocabulary for
Phase 2. Exporter access is distinct from operator or reviewer inspection. The
expected state immediately after successful generation is:

```text
ADDITIONAL_REAL_VOCABULARY_ACCESSED_BY_COMMITTED_EXPORTER = YES
ADDITIONAL_REAL_VOCABULARY_INSPECTED_BY_REVIEWER = NO
```

The operator or reviewer must not display or inspect the lexical values during
generation.

### Required Post-Generation Sequence

```text
NEXT_STEP = RETAINED_STAGE_A_UNIVERSE_RECONCILIATION

generation
-> retained artifact reconciliation
-> freeze reviewer-decision artifact procedure if still needed
-> human count-blinded Stage A review
-> retain decisions
-> Stage B quantitative attachment
```

Reconciliation must precede review. It must verify artifact identity and JSON
integrity, bindings and generator revision, cardinality equations and exact
entry totals, field boundaries, Phase 1 exclusion, count blinding, absence of
decisions and Phase 3 fields, deterministic ordering, and lexical preservation
relative to the retained vocabularies. These checks are not performed during
this manifest step.

### Real Generation Manifest Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_REAL_GENERATION_MANIFEST
PHASE_2_STAGE_A_EXPORT_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
PHASE_2_STAGE_A_EXPORT_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
REAL_INPUT_ARTIFACTS_OPENED_DURING_MANIFEST = NO
REAL_INPUT_ARTIFACT_HASHES_RECOMPUTED_DURING_MANIFEST = NO
REAL_STAGE_A_UNIVERSE_GENERATED = NO
REAL_STAGE_A_GENERATION_ATTEMPTS = 0
ADDITIONAL_REAL_VOCABULARY_ACCESSED_BY_COMMITTED_EXPORTER = NO
ADDITIONAL_REAL_VOCABULARY_INSPECTED_BY_REVIEWER = NO
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_2_STAGE_A = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
```

## Phase 2 Stage A Real Review-Universe Generation

The frozen Stage A exporter command executed exactly once and succeeded. The
generated count-blinded universe was preserved externally exactly as written.

```text
execution_bound_git_revision = dc9dbce97027fdf71ec09ddb67fea920463fb4bf
exporter_implementation_commit = 0cbaf75cd2e4665143d2072ddd0654022c173405
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
input_phase1_result_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82
stage_a_review_universe_path = /data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001/phase2-stage-a-review-universe.json
stage_a_review_universe_size_bytes = 89666
stage_a_review_universe_sha256 = d31e3f2ee129e9f71f799d2f702b1c35dbbb4163b655c955844ee782c1330a66
generated_at_utc = 2026-09-18T16:56:27.572323+00:00
python_version = 3.12.3
generation_attempts = 1
generation_result = SUCCESS
reruns = 0
```

### Generated Artifact Bindings

The retained Stage A bindings reconciled as:

```text
increment_008_version = 008
increment_008_contract = 008-source-native-sentinel-and-missingness-audit
phase = PHASE_2
stage = STAGE_A_REVIEW_UNIVERSE
input_baseline_sha256 = 2401375602b5a5ab5cc6d4f90aa198518589959eb079b691db0b0c1657e4e56c
input_phase1_result_sha256 = f59282688deed67cf589c612d219144773de97dfca718a8e11f72291dda5be82
generator_git_revision = dc9dbce97027fdf71ec09ddb67fea920463fb4bf
python_version = 3.12.3
binding_reconciliation = PASS
```

The generator revision remains the execution-bound manifest revision. It is
not replaced by the later documentation revision.

### Real Stage A Accounting and Count Blinding

```text
service_source_vocabulary_count = 1169
service_phase1_excluded_count = 1
service_stage_a_review_count = 1168
1169 = 1 + 1168

status_source_vocabulary_count = 5
status_phase1_excluded_count = 0
status_stage_a_review_count = 5
5 = 0 + 5

total_stage_a_review_count = 1173
retained_reviewer_entry_count = 1173
agency_reviewer_entry_count = 0

reviewer_entry_schema = field + value only
entry_schema_mismatches = 0
quantitative_entry_field_violations = 0
decision_field_violations = 0
COUNTS_VISIBLE_TO_REVIEWER = NO
```

No reviewer-facing entry contains row count, row percentage, vocabulary
percentage, frequency, rank, materiality, decision, rationale, or Phase 3
classification.

### Machine Access and Human Inspection Boundary

```text
ADDITIONAL_REAL_VOCABULARY_ACCESSED_BY_COMMITTED_EXPORTER = YES
LEXICAL_VALUES_PROGRAMMATICALLY_PROCESSED_FOR_RECONCILIATION = YES
ADDITIONAL_REAL_VOCABULARY_INSPECTED_BY_REVIEWER = NO
LEXICAL_VALUES_PRINTED_TO_REVIEWER = NO
LEXICAL_VALUES_SEMANTICALLY_REVIEWED = NO
COUNTS_PAIRED_WITH_LEXICAL_VALUES_FOR_REVIEWER = NO
```

Machine processing required exact lexical identities to build and
independently reconcile the count-blinded review universe. That processing is
not the exploratory reviewer judgment defined for Phase 2 Stage A.

## Phase 2 Stage A Retained Review-Universe Reconciliation

```text
STAGE_A_UNIVERSE_RECONCILIATION = PASSED
RECONCILIATION_CLASSIFICATION = INTERNAL_ENGINEERING_EVALUATION_RESULT
```

Independent standard-library logic reconstructed the expected review universe
from the retained Increment 007 marginal vocabularies and retained Phase 1
candidate identities. It did not import or use the production Stage A exporter
as the reconciliation oracle. This is internal engineering evidence, not
independent external validation.

### Input and Binding Reconciliation

```text
baseline_result_size_bytes = 563023
baseline_result_sha_reconciliation = PASS
phase1_result_size_bytes = 3039
phase1_result_sha_reconciliation = PASS
stage_a_universe_size_bytes = 89666
stage_a_universe_sha_reconciliation = PASS
increment_007_binding_reconciliation = PASS
phase1_binding_reconciliation = PASS
stage_a_binding_reconciliation = PASS
rows_identity_admitted = 7474403
```

### Vocabulary and Phase 1 Exclusion Reconciliation

```text
service_vocabulary_cardinality = 1169
service_vocabulary_count_sum = 7474403
service_duplicate_exact_observed_values = 0
status_vocabulary_cardinality = 5
status_vocabulary_count_sum = 7474403
status_duplicate_exact_observed_values = 0

service_phase1_exclusion_count = 1
status_phase1_exclusion_count = 0
unreconciled_phase1_exclusions = 0
phase1_exclusions_leaked_into_stage_a = 0
```

Exclusions were independently reconstructed from retained Phase 1 candidate
identities rather than from hard-coded lexical values. No excluded lexical
identity is repeated in this Stage A evidence section.

### Exact Universe Reconciliation

```text
independent_expected_service_stage_a_entries = 1168
independent_expected_status_stage_a_entries = 5
independent_expected_total_stage_a_entries = 1173
retained_total_stage_a_entries = 1173
exact_ordered_list_mismatches = 0
expected_but_not_retained = 0
retained_but_not_expected = 0
duplicate_retained_identities = 0
entry_schema_mismatches = 0
accounting_mismatches = 0
```

This establishes exact transformation fidelity relative to the retained
marginal vocabularies and retained Phase 1 exclusions. It does not establish
the semantic meaning of any lexical value.

### Agency, Phase 3, and Representation Boundaries

```text
agency_responsible = NOT_EVALUABLE_FROM_RETAINED_INCREMENT_007_VOCABULARIES
agency_stage_a_entries = 0
agency_boundary_reconciliation = PASS
PHASE_3_STRUCTURE_PRESENT_IN_STAGE_A_UNIVERSE = NO
PHASE_3 = NOT_STARTED
STAGE_A_UNIVERSE_REPRESENTATION_AUDIT = PASS
```

No agency vocabulary, candidate set, or denominator was invented. No
low-information classification occurred. The representation audit verified
UTF-8, valid JSON, a terminating newline, recursively sorted object keys, and
deterministic review-entry ordering. Serialization integrity is not evidence
of semantic correctness.

### Established Engineering Observation and Remaining Boundaries

The retained Phase 2 Stage A artifact is a reconciled, deterministic,
count-blinded review universe containing 1,173 exact lexical entries derived
from the retained Increment 007 service and status vocabularies after exclusion
of the retained Phase 1 candidate identities.

```text
RESULT_CLASSIFICATION = ENGINEERING_OBSERVATION
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
EXPLORATORY_SENTINEL_CANDIDATES = NOT_OBSERVED
MISSING_DATA_RECLASSIFICATION = NOT_PERFORMED
SEMANTIC_INTERPRETATION = NOT_PERFORMED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

### Next Boundary

```text
NEXT_STEP = PROSPECTIVE_STAGE_A_DECISION_EVIDENCE_PROCEDURE
```

Before the first reviewer exposure to the 1,173 lexical values, the project
will freeze how reviewer decisions and rationales are recorded and retained.
That procedure is not defined in this checkpoint.

### Stage A Generation and Reconciliation Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_REAL_GENERATION_AND_RECONCILIATION_DOCUMENTATION
REAL_STAGE_A_UNIVERSE_GENERATED = YES
REAL_STAGE_A_GENERATION_ATTEMPTS = 1
STAGE_A_UNIVERSE_RECONCILIATION = PASSED
STAGE_A_UNIVERSE_SHA256 = d31e3f2ee129e9f71f799d2f702b1c35dbbb4163b655c955844ee782c1330a66
STAGE_A_UNIVERSE_ENTRY_COUNT = 1173
SERVICE_STAGE_A_REVIEW_COUNT = 1168
STATUS_STAGE_A_REVIEW_COUNT = 5
AGENCY_STAGE_A_REVIEW_COUNT = 0
STAGE_A_UNIVERSE_ENTRY_MISMATCHES = 0
STAGE_A_UNIVERSE_SET_EXPECTED_NOT_RETAINED = 0
STAGE_A_UNIVERSE_SET_RETAINED_NOT_EXPECTED = 0
STAGE_A_UNIVERSE_DUPLICATE_IDENTITIES = 0
PHASE1_EXCLUSIONS_LEAKED_INTO_STAGE_A = 0
ENTRY_SCHEMA_MISMATCHES = 0
QUANTITATIVE_ENTRY_FIELD_VIOLATIONS = 0
DECISION_FIELD_VIOLATIONS = 0
ADDITIONAL_REAL_VOCABULARY_ACCESSED_BY_COMMITTED_EXPORTER = YES
LEXICAL_VALUES_PROGRAMMATICALLY_PROCESSED_FOR_RECONCILIATION = YES
ADDITIONAL_REAL_VOCABULARY_INSPECTED_BY_REVIEWER = NO
LEXICAL_VALUES_PRINTED_TO_REVIEWER = NO
LEXICAL_VALUES_SEMANTICALLY_REVIEWED = NO
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_2_STAGE_A = UNIVERSE_RECONCILED_HUMAN_REVIEW_NOT_STARTED
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_3 = NOT_STARTED
NEXT_STEP = PROSPECTIVE_STAGE_A_DECISION_EVIDENCE_PROCEDURE
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
INCREMENT_008_STATUS = IN_PROGRESS
```

### Full Regression Evidence

Command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result:

```text
tests_run = 202
failures = 0
errors = 0
result = OK
```

This is internal engineering evidence, not independent external validation.

## Phase 2 Stage A Human Decision-Evidence Procedure

This prospective procedure freezes how the project researcher's count-blinded
exploratory lexical judgments will be recorded for every entry in the
reconciled Stage A review universe. The future decision artifact is evidence
of the review process. It is not deterministic Phase 1 evidence, independent
or external validation, source-authoritative semantic interpretation, or
missing-data ground truth.

```text
STAGE_A_DECISION_CLASSIFICATION = EXPLORATORY_REVIEWER_JUDGMENT
```

No lexical value was exposed or reviewed while defining this procedure.

### Separate Decision Artifact and Binding

The future decision artifact is reserved at:

```text
/data/repos/personal/support-operations-intelligence-results/increment-008/phase-2/stage-a/run-001/phase2-stage-a-decisions.json
```

It does not exist at this checkpoint and must not be created until the later
review workflow is prospectively executable.

```text
STAGE_A_REVIEW_UNIVERSE != STAGE_A_DECISIONS
```

The generated universe remains immutable input evidence. The decisions
artifact is separate reviewer-produced evidence and must bind to:

```text
increment_008_version = 008
increment_008_contract = 008-source-native-sentinel-and-missingness-audit
phase = PHASE_2
stage = STAGE_A_HUMAN_REVIEW
input_stage_a_universe_sha256 = d31e3f2ee129e9f71f799d2f702b1c35dbbb4163b655c955844ee782c1330a66
input_stage_a_universe_entry_count = 1173
review_contract_git_revision = POST_PROCEDURE_COMMIT_HEAD_BEFORE_REVIEW
reviewer_role = PROJECT_RESEARCHER
```

The commit produced by this prospective procedure becomes the review-contract
revision unless another prospective procedure change is committed before
review begins.

No personal identifier beyond `PROJECT_RESEARCHER` is required. The artifact
must not claim `INDEPENDENT_REVIEWER`, `SECOND_RATER`, `EXTERNAL_VALIDATOR`, or
`INTER_RATER_AGREEMENT` unless that evidence is separately produced later.

### Allowed Decisions and Lexical Criterion

Every Stage A entry must receive exactly one of:

```text
NO_PHASE_2_FLAG
EXPLORATORY_SENTINEL_CANDIDATE
```

No third state is allowed in a completed review. In particular, Stage A must
not emit `MISSING_DATA`, `CONFIRMED_SENTINEL`, `INVALID_VALUE`, `BAD_DATA`,
`LOW_INFORMATION`, `PHASE_3_CANDIDATE`, or `UNKNOWN_DECISION`.

`EXPLORATORY_SENTINEL_CANDIDATE` is permitted only when the presented exact
lexical form plausibly denotes absence, an unknown state, an unavailable
state, a not-provided state, or a placeholder state. Judgment must be based
only on the lexical form. Row prevalence, frequency rank, cross-tab context,
operational service context, external semantic assumptions, and Phase 3
low-information reasoning must not determine the decision.

### Decision Identity and Rationale

Every decision entry retains:

```text
field
value
decision
```

The authoritative identity is `(field, exact value)`. The value must be copied
unchanged from the reconciled Stage A universe, with no trimming,
normalization, case folding, canonicalization, or renaming.

For `EXPLORATORY_SENTINEL_CANDIDATE`, a concise lexical rationale is required.
It must explain only why the lexical form plausibly represents absence,
unknown, unavailable, not-provided, or placeholder semantics. Frequency and
operational context are prohibited as rationale. A rationale is not required
for `NO_PHASE_2_FLAG`.

### Review Order and Deterministic Batching

Review follows the reconciled Stage A universe order exactly: all
`service_name` entries first, then all `status_description` entries, with the
retained deterministic lexical order within each field. The review must not
re-sort, shuffle, prioritize, search likely candidates first, or omit entries.

```text
STAGE_A_BATCH_SIZE = 100
STAGE_A_EXPECTED_BATCHES = 12
STAGE_A_TOTAL_REVIEW_ENTRIES = 1173
```

The one-based positional batch boundaries are:

| Batch | Start position | End position | Expected entries |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 100 | 100 |
| 2 | 101 | 200 | 100 |
| 3 | 201 | 300 | 100 |
| 4 | 301 | 400 | 100 |
| 5 | 401 | 500 | 100 |
| 6 | 501 | 600 | 100 |
| 7 | 601 | 700 | 100 |
| 8 | 701 | 800 | 100 |
| 9 | 801 | 900 | 100 |
| 10 | 901 | 1000 | 100 |
| 11 | 1001 | 1100 | 100 |
| 12 | 1101 | 1173 | 73 |

Position is review bookkeeping only and conveys no source-row prevalence.

Only one batch may be presented at a time. A later batch must not be exposed
until the current batch decisions have been retained. Future-batch lexical
values must not be inspected while the current batch is under review. This
reduces omission risk, preserves order and intermediate evidence, and avoids
an unstructured 1,173-value session.

### Batch Evidence and Completeness

Each completed batch retains:

```text
batch_number
start_position
end_position
expected_entry_count
reviewed_entry_count
reviewer_role
reviewed_at_utc
decisions
```

Each decision contains `field`, `value`, and `decision`, plus `rationale` only
when flagged. It contains no source counts or percentages.

For every completed batch, `reviewed_entry_count` must equal
`expected_entry_count`; every universe identity in the positional interval
must appear exactly once. Missing, duplicate, extra, or out-of-batch identities
make the batch incomplete.

Across completed batches, retain:

```text
batches_completed
entries_reviewed
no_phase_2_flag_count
exploratory_sentinel_candidate_count
```

These are review-decision counts, not source-row prevalence. Final completion
requires:

```text
entries_reviewed = 1173
no_phase_2_flag_count + exploratory_sentinel_candidate_count = 1173
```

### Partial Review, Interruption, and Amendments

Before all 12 batches complete:

```text
review_status = IN_PROGRESS
```

After all 1,173 decisions reconcile:

```text
review_status = COMPLETE_PENDING_RECONCILIATION
```

Stage A is not fully retained until the completed artifact independently
reconciles.

If review stops between batches, preserve completed-batch evidence and resume
from the next unreviewed position. Do not restart completed batches unless an
explicit amendment is required. If review stops inside a batch, that batch
remains incomplete; partial work must remain distinguishable from completed
batch evidence.

A completed-batch decision must never be silently rewritten. Before Stage B,
an incorrect recorded decision may be changed only through an amendment that
retains:

```text
field
value
previous_decision
new_decision
reason
amended_at_utc
reviewer_role
```

An amendment to `EXPLORATORY_SENTINEL_CANDIDATE` must include the required
lexical rationale. The effective decision is reconstructed from the original
decision plus ordered amendment history; the original is never deleted.

### Stage A Freeze and Count-Blinding Boundary

Stage A decisions become frozen only after all of the following:

- all 1,173 entries have a decision;
- all 12 batches reconcile;
- amendment history is retained;
- final effective decisions reconcile;
- the completed decisions artifact receives a retained SHA-256; and
- independent decision-artifact reconciliation passes.

Only after that freeze may Stage B expose source row counts.

```text
COUNTS_VISIBLE_TO_REVIEWER = NO
COUNTS_MAY_BE_ATTACHED_BEFORE_STAGE_A_FREEZE = NO
```

Until the freeze, the reviewer must not be shown row count, row percentage,
vocabulary percentage, frequency rank, cross-tab counts, service or status
prevalence, or Phase 1 materiality calculations associated with a reviewed
value. The reviewer may know the total universe size, batch position, field,
lexical value, and cumulative decision count because these do not reveal
source-row prevalence.

### Phase 3 and Phase 1 Boundaries

During Stage A, do not classify a value as broad, generic, catch-all,
low-information, miscellaneous, general-inquiry-like, or other-like unless its
exact lexical form independently satisfies the Phase 2 sentinel criterion.

```text
PHASE_3_JUDGMENT_DURING_STAGE_A = PROHIBITED
```

If Stage A identifies a plausible placeholder not captured by Phase 1, record
only `EXPLORATORY_SENTINEL_CANDIDATE`. Do not extend
`PHASE1_SENTINEL_VALUES`, rerun Phase 1, rewrite Phase 1 findings, or call the
judgment deterministic evidence. Any deterministic rule expansion requires
separate prospective work.

### Failure and Success Conditions

Stop Stage A review if the universe SHA changes; review order cannot be
reconstructed; a lexical identity is altered; source-row counts become visible
beside values; an entry is missing or duplicated; decisions cannot be
retained; Phase 2 and Phase 3 judgments become conflated; a required candidate
rationale is absent; a completed decision would require silent replacement;
or the decision artifact loses its universe binding. A changed procedure
requires a new prospective record before review continues.

Stage A human review succeeds only when all 1,173 entries are reviewed; all 12
batches reconcile; every entry has exactly one effective decision; every
exploratory candidate has a lexical rationale; no entry was exposed with
source-row prevalence; no Phase 3 classification was mixed in; amendments are
preserved; the final decision artifact is retained and hashed; and independent
decision-artifact reconciliation passes.

### Future Artifact Representation and Summary

The future decision artifact must use UTF-8 JSON, a terminating newline,
deterministic object-key ordering, decisions in Stage A universe order,
deterministic batch metadata, and amendment history in chronological order.
It is not created in this checkpoint.

Its top-level concepts are prospectively equivalent to:

```text
binding
review
batches
amendments
summary
```

This procedure freezes evidence requirements, not the final executable schema.
A later RED contract may freeze the exact representation.

The summary may report only:

```text
total_universe_entries
entries_reviewed
no_phase_2_flag_count
exploratory_sentinel_candidate_count
batches_completed
review_status
```

These are reviewer-decision counts. Source row counts and percentages remain
prohibited from Stage A decision evidence.

### Claim Boundary

A completed Stage A artifact would establish what the project researcher
classified under the frozen exploratory lexical criterion. It would not
establish source semantic truth, missingness ground truth, independent
validation, operational impact, row-level materiality, a cross-field union, or
a scientific conclusion.

```text
EVENTUAL_STAGE_A_DECISION_RESULT_CLASSIFICATION = INTERNAL_EXPLORATORY_REVIEW_RESULT
```

### Decision-Procedure Threats and Limitations

The procedure remains vulnerable to reviewer fatigue across 1,173 values,
single-reviewer subjectivity, ordering and context effects, lexical ambiguity,
inconsistency across batches, prior knowledge of the Phase 1 result, later
decision amendments, absence of independent second-rater evidence, and biases
that count blinding cannot remove. Lexical judgment does not establish source
semantics. Fixed batching, completeness checks, and retained amendments reduce
some procedural risk but do not eliminate these threats.

### Next Implementation Boundary and Current States

```text
NEXT_STEP = STAGE_A_DECISION_ARTIFACT_VALIDATION_RED_CONTRACT

PHASE_2_STAGE_A_UNIVERSE = RECONCILED
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
STAGE_A_DECISION_ARTIFACT = NOT_CREATED
STAGE_A_DECISIONS_OBSERVED = NO
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
```

Before any lexical value is exposed, the next work is an executable validation
RED contract for decision evidence. The recommended sequence is:

```text
decision-evidence procedure
-> validator RED contract
-> validator GREEN implementation
-> real review-session manifest
-> Batch 1 exposure and decisions
```

### Human Decision-Procedure Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_HUMAN_DECISION_PROCEDURE
STAGE_A_UNIVERSE = RECONCILED
STAGE_A_DECISION_PROCEDURE = PROSPECTIVELY_DEFINED
STAGE_A_DECISION_ARTIFACT = NOT_CREATED
STAGE_A_DECISIONS_OBSERVED = NO
STAGE_A_BATCH_SIZE = 100
STAGE_A_EXPECTED_BATCHES = 12
STAGE_A_TOTAL_REVIEW_ENTRIES = 1173
COUNTS_VISIBLE_TO_REVIEWER = NO
COUNTS_MAY_BE_ATTACHED_BEFORE_STAGE_A_FREEZE = NO
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_3 = NOT_STARTED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
NEXT_STEP = STAGE_A_DECISION_ARTIFACT_VALIDATION_RED_CONTRACT
INCREMENT_008_STATUS = IN_PROGRESS
```

## Phase 2 Stage A Decision-Artifact Validation RED Contract

This prospective executable contract freezes validation of future Stage A
human decision evidence before any reviewer lexical exposure. The validator
will validate evidence, derive effective decisions, reconcile review
accounting, and return success or failure. It will not make or alter reviewer
decisions, generate rationales, attach source prevalence, or perform Phase 3
classification.

The prospective production module is intentionally absent:

```text
src/support_operations_intelligence/source_native_sentinel_stage_a_decision_validation.py
```

It must expose:

```text
main(argv: Sequence[str] | None = None) -> int
```

The prospective invocation is:

```bash
python -m \
support_operations_intelligence.source_native_sentinel_stage_a_decision_validation \
  --stage-a-universe <path> \
  --expected-stage-a-universe-sha256 <sha256> \
  --decisions <path> \
  --expected-review-contract-git-revision <revision>
```

No baseline, Calgary CSV, counts, Phase 3, agency, auto-classification, model,
LLM, or repair argument is permitted.

### Universe Identity and Hash-Before-Parse Boundary

The validator must stream-hash the supplied universe, compare it with the CLI
expected SHA-256, and only then parse it. On mismatch it returns nonzero,
performs no decision validation, and emits no lexical value in diagnostics.

After digest equality, require universe bindings equivalent to:

```text
increment_008_version = 008
increment_008_contract = 008-source-native-sentinel-and-missingness-audit
phase = PHASE_2
stage = STAGE_A_REVIEW_UNIVERSE
```

The actual supplied universe entries are the authoritative ordered identity
sequence. Production validation must not hard-code lexical values. The real
artifact has 1,173 entries, but batch construction derives from actual entry
count and batch size.

### Decision Artifact Schema and Binding

The exact conceptual top-level sections are:

```text
binding
review
batches
amendments
summary
```

No source-row analysis or Phase 3 section is permitted.

The binding contains:

```text
increment_008_version
increment_008_contract
phase
stage
input_stage_a_universe_sha256
input_stage_a_universe_entry_count
review_contract_git_revision
reviewer_role
```

For the real artifact, the expected values remain the frozen Increment 008
contract, `PHASE_2`, `STAGE_A_HUMAN_REVIEW`, universe SHA-256
`d31e3f2ee129e9f71f799d2f702b1c35dbbb4163b655c955844ee782c1330a66`,
1,173 entries, review-contract revision
`17b6aba0425b9a56d21799319deb88651ec81a66`, and reviewer role
`PROJECT_RESEARCHER`. The review-contract revision must be compared with the
CLI expected value rather than trusted from the artifact.

The review section contains `review_status` and `batch_size`. Allowed status
values are `IN_PROGRESS` and `COMPLETE_PENDING_RECONCILIATION`; batch size is
100. Source-row prevalence metadata is prohibited.

### Batch Derivation, Prefix, and Completeness

Each completed batch contains:

```text
batch_number
start_position
end_position
expected_entry_count
reviewed_entry_count
reviewer_role
reviewed_at_utc
decisions
```

Batch and positions are one-based, reviewer role is `PROJECT_RESEARCHER`, and
the timestamp is timezone-aware UTC.

Expected boundaries derive from universe entry count and `BATCH_SIZE = 100`;
the validator must not hard-code 12 as generic construction logic. For 1,173
entries, the derived intervals are 1-100, 101-200, 201-300, 301-400, 401-500,
501-600, 601-700, 701-800, 801-900, 901-1000, 1001-1100, and 1101-1173.

The canonical artifact retains completed batches only. Each retained batch
must have `reviewed_entry_count = expected_entry_count` and exactly that many
decisions. Retained batches form a contiguous prefix beginning at batch 1,
with no gaps or future-batch evidence.

### Decision Identity, Labels, and Rationale

Each decision contains `field`, `value`, and `decision`. Only these labels are
allowed:

```text
NO_PHASE_2_FLAG
EXPLORATORY_SENTINEL_CANDIDATE
```

An exploratory candidate additionally requires a present, string, non-empty
rationale. Rationale presence is evidence validation, not semantic validation.

At every one-based universe position, decision field and value must equal the
exact universe identity. Trimming, case folding, normalization, renaming, and
reordering are prohibited. Completed batches may contain no missing,
duplicate, extra, repeated, or out-of-batch identity.

### Amendments and Effective Decisions

Every amendment contains:

```text
field
value
previous_decision
new_decision
reason
amended_at_utc
reviewer_role
```

An amendment to `EXPLORATORY_SENTINEL_CANDIDATE` also requires a rationale.
Its identity must already have an original decision in a completed batch.
For each retained amendment, `previous_decision` must equal the current
effective decision immediately before the transition; `new_decision` must be
allowed and different; reason must be non-empty; role must be
`PROJECT_RESEARCHER`; and timestamp must be timezone-aware UTC.

Amendments remain in retained chronological order with nondecreasing
timestamps. The validator must not sort them. Multiple amendments are valid
only as an ordered transition chain. Effective decisions are reconstructed
from immutable original decisions plus amendment history; originals are never
rewritten or deleted.

### Summary and Status Reconciliation

The summary contains only review accounting:

```text
total_universe_entries
entries_reviewed
no_phase_2_flag_count
exploratory_sentinel_candidate_count
batches_completed
review_status
```

`total_universe_entries` equals the supplied universe count;
`entries_reviewed` equals original decisions across completed batches;
`batches_completed` equals retained completed batches; and the two decision
counts are calculated from effective decisions. Their sum must equal
`entries_reviewed`.

If reviewed entries are fewer than the universe, both review and summary
status must be `IN_PROGRESS`. If every entry is reviewed, every derived batch
must be complete and both statuses must be
`COMPLETE_PENDING_RECONCILIATION`. Cross-section status disagreement, partial
completion claims, and full artifacts claiming progress fail validation.

### Count Blinding and Phase 3 Prohibition

Decision entries, amendments, review metadata, and summary must reject
source-prevalence keys including row count, row percentage, vocabulary
percentage, frequency or rank, materiality, cross-tab data, source row count,
and source percentage. Batch expected/reviewed counts and aggregate decision
counts are allowed because they count review evidence, not source rows.

Phase 3 structures, prohibited decision labels, low-information labels,
catch-all classification, and generic-category classification are rejected by
schema and label. Validation must not inspect lexical semantics to infer a
Phase 3-like value.

### Lexical-Safe Diagnostics and CLI Output

```text
VALIDATOR_LEXICAL_VALUE_LEAKAGE = PROHIBITED
```

Failure diagnostics must never echo universe or decision values, rationale
text, or amendment reason text. Safe diagnostics may identify error category,
batch number, one-based position, decision or amendment index, safe field
name, and expected or observed counts.

Success output may report only `VALIDATION=PASS`, review status, completed
batches, entries reviewed, effective decision counts, and amendment count. It
contains no lexical value, rationale, amendment reason, or source prevalence.

On failure, the validator returns nonzero, modifies neither input, performs no
repair or replacement inference, does not continue to a later batch, and does
not leak lexical values. No retry or fallback is part of validator behavior.

### Prospective Synthetic Test Contract

The new standard-library test module is:

```text
tests/test_source_native_sentinel_stage_a_decision_validation.py
```

Its 16 focused `unittest.TestCase` methods use only temporary synthetic
artifacts. They freeze hash-before-parse; required bindings; valid partial and
complete review; derived final-batch behavior; completed contiguous prefixes;
batch boundary, count, identity, duplication, and rationale failures; valid
and invalid amendment reconstruction and chronological ordering; effective
summary and review-status reconciliation; count-blinding and Phase 3
rejection; and lexical-safe failure and success output.

Distinctive synthetic strings verify leakage protection. No retained Calgary
lexical value or real Stage A artifact content is used.

### Test Syntax and Focused RED Evidence

Syntax command:

```bash
.venv/bin/python -m py_compile \
  tests/test_source_native_sentinel_stage_a_decision_validation.py
```

Observed result: PASS.

Focused command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_stage_a_decision_validation \
  -v
```

Observed result: RED, exit status 1. The unittest loader failed before the 16
prospective methods executed:

```text
ModuleNotFoundError: No module named
'support_operations_intelligence.source_native_sentinel_stage_a_decision_validation'
```

The RED cause is exactly the absent production validation module. It was not
implemented. The full regression was not run; the retained current full-suite
evidence remains 202 tests, 0 failures, 0 errors, `OK` and is not relabeled as
the suite count after adding this unimplemented RED test module.

### Decision Validation RED Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_DECISION_VALIDATION_RED_CONTRACT
STAGE_A_UNIVERSE = RECONCILED
STAGE_A_REVIEW_CONTRACT_GIT_REVISION = 17b6aba0425b9a56d21799319deb88651ec81a66
STAGE_A_DECISION_VALIDATION_TEST_CONTRACT = IMPLEMENTED
STAGE_A_DECISION_VALIDATOR_IMPLEMENTATION = ABSENT
STAGE_A_DECISION_VALIDATOR_FOCUSED_STATE = RED
STAGE_A_DECISION_VALIDATOR_RED_CAUSE = MISSING_DECISION_VALIDATION_MODULE
REAL_STAGE_A_LEXICAL_VALUES_EXPOSED = NO
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
STAGE_A_DECISION_ARTIFACT = NOT_CREATED
STAGE_A_DECISIONS_OBSERVED = NO
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_3 = NOT_STARTED
NEXT_STEP = STAGE_A_DECISION_ARTIFACT_VALIDATION_GREEN_IMPLEMENTATION
INCREMENT_008_STATUS = IN_PROGRESS
```

## Phase 2 Stage A Decision-Artifact Validator GREEN Checkpoint

The Stage A decision-artifact validator is now implemented at:

```text
src/support_operations_intelligence/source_native_sentinel_stage_a_decision_validation.py
```

It exposes `main(argv: Sequence[str] | None = None) -> int` and accepts only
the frozen `--stage-a-universe`, `--expected-stage-a-universe-sha256`,
`--decisions`, and `--expected-review-contract-git-revision` arguments. The
implementation uses only the Python standard library and remains a read-only
evidence validator; it neither creates nor modifies reviewer decisions.

Implemented validation behavior includes universe SHA-before-parse
verification; universe contract validation; decision-artifact binding
validation; generic batch-boundary derivation from actual universe size;
completed-batch-only validation; contiguous-prefix enforcement; exact
positional identity validation; two-label decision validation; candidate
rationale-presence validation; amendment identity, transition, and retained
order validation; effective-decision reconstruction without rewriting
original evidence; summary and review-status reconciliation; source-prevalence
field rejection; Phase 3 schema and label rejection; sanitized diagnostics
that do not reveal lexical values, rationale text, or amendment reason text;
safe aggregate success output; and fail-closed, non-mutating behavior.

### Synthetic Engineering Test Evidence

Focused decision-validator command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_stage_a_decision_validation \
  -v
```

Observed result: 16 tests, 0 failures, 0 errors, `OK`.

Stage A exporter regression command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_stage_a_run \
  -q
```

Observed result: 10 tests, 0 failures, 0 errors, `OK`.

Phase 1 regression command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_source_native_sentinel_audit \
  tests.test_source_native_sentinel_audit_run \
  -q
```

Observed result: 21 tests, 0 failures, 0 errors, `OK`.

Full repository regression command:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

Observed result: 218 tests, 0 failures, 0 errors, `OK`. This matches the
plausible expected total of the retained 202-test suite plus the 16 committed
decision-validator contract methods.

All validation fixtures were synthetic. These results are internal engineering
evidence, not independent validation.

```text
STAGE_A_DECISION_VALIDATOR_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
```

### No-Real-Data and Claim Boundaries

The real Stage A universe was not opened, parsed, hashed, printed, sampled, or
semantically inspected during this GREEN implementation. No real lexical value
was exposed or reviewed, and the reserved real decision artifact was neither
opened nor created. Human Stage A review, Stage B, and Phase 3 remain
unstarted.

```text
REAL_STAGE_A_UNIVERSE_OPENED_DURING_GREEN_IMPLEMENTATION = NO
REAL_STAGE_A_LEXICAL_VALUES_EXPOSED = NO
REAL_STAGE_A_LEXICAL_VALUES_REVIEWED = NO
STAGE_A_DECISION_ARTIFACT = NOT_CREATED
STAGE_A_DECISIONS_OBSERVED = NO
PHASE_2_STAGE_A_HUMAN_REVIEW = NOT_STARTED
COUNTS_VISIBLE_TO_REVIEWER = NO
PHASE_2_STAGE_B = NOT_STARTED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_3 = NOT_STARTED
```

### Decision-Validator GREEN Classifications

```text
CHANGE_TYPE = PHASE_2_STAGE_A_DECISION_VALIDATOR_GREEN_IMPLEMENTATION
STAGE_A_DECISION_VALIDATOR_IMPLEMENTATION = ENGINEERING_IMPLEMENTATION
STAGE_A_DECISION_VALIDATOR_TEST_RESULT = INTERNAL_ENGINEERING_TEST_RESULT
STAGE_A_DECISION_VALIDATOR_BEHAVIOR_UNDER_SYNTHETIC_TESTS = ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
PUBLIC_DESCRIPTION_DECISION = DEFERRED
NEXT_STEP = PROSPECTIVE_REAL_STAGE_A_REVIEW_SESSION_MANIFEST
```

## Current Status

Increment 008 remains in progress. Phase 1 is executed, reconciled, and
documented. The Phase 2 exploratory review contract, Stage A export test
contract, and Stage A exporter GREEN implementation are established under
synthetic engineering tests. The real Stage A review universe was generated
once and independently reconciled with no mismatch. The prospective human
decision-evidence procedure is frozen before first reviewer exposure, and its
synthetic executable validation contract and GREEN validator implementation
are established under synthetic engineering tests. Human Stage A review,
Stage B, and Phase 3 have not started; no Phase 2 finding or decision artifact
exists. The next boundary is the prospective real Stage A review-session
manifest.

# Increment 005 - Executable Calgary Case Adapter

Status: Planned

Opened: 2026-09-12

Completed: Not completed

## Objective

Implement and test a deterministic Calgary record-to-Case adapter boundary
that consumes already-parsed source-record values and realizes only the
mappings and source-native treatments accepted by Increment 004 while
preserving all explicit deferrals, evidence-state distinctions, and semantic
limitations.

This increment does not implement a Calgary data pipeline and does not load
Calgary data into the canonical model.

## Why This Increment Exists

Increment 002 defined the canonical Case contract and the conformance
obligations for source adapters.

Increment 003 established the retained Calgary source-evidence baseline.

Increment 004 established the Calgary semantic source contract, including
accepted mappings, source-native retention, explicit deferrals, evidence-state
boundaries, and limitations.

Increment 005 tests whether those contracts can be realized as deterministic,
executable behavior without silently strengthening their semantics.

This increment is an implementation test of the existing contracts. It is not
permission to redesign them.

## Starting State

Repository:

`/data/repos/personal/support-operations-intelligence`

Starting branch:

`main`

Starting HEAD:

`42d27b18ca7bf9ae6a196b21699f5c25f7b15f89`

Increment 004:

`Complete`

The deliberate executable starting state after the semantic-contract work is:

- no `src/`;
- no `tests/`;
- no application package;
- no Calgary adapter;
- no ingestion code;
- no canonical physical representation;
- no PostgreSQL schema;
- no migrations;
- no executable data-quality checks;
- no analytical contracts;
- no SQL analytics;
- no CI;
- no Docker.

These are starting-state boundaries, not defects.

## Source of Truth

The controlling canonical Case and adapter-conformance contract is:

`docs/increments/002-canonical-case-contract.md`

The controlling retained Calgary evidence baseline is:

`docs/increments/003-calgary-source-evidence-validation.md`

The controlling Calgary mapping, deferral, native-retention, evidence-state,
and limitation contract is:

`docs/increments/004-calgary-source-contract.md`

Increment 005 must implement against these contracts without silently
reinterpreting them. If executable work exposes a real contradiction, the
increment must stop, retain the contradiction, and determine whether explicit
contract revision is required.

## Controlling Calgary Contract

Increment 005 must preserve the following decisions exactly.

Case admission:

    ADMIT_CASE

`source_system`:

    city_of_calgary_311

`source_case_id`:

    service_request_id

Authoritative source identity:

    (city_of_calgary_311, service_request_id)

`created_at`:

    DEFER_MAPPING

`source_status`:

    status_description

`canonical_status`:

    DEFER_MAPPING

`source`:

    RETAIN_SOURCE_NATIVE
    submission-channel evidence

`service_name`:

    RETAIN_SOURCE_NATIVE
    service-type evidence

`agency_responsible`:

    RETAIN_SOURCE_NATIVE
    responsible-department evidence

`updated_date`:

    RETAIN_SOURCE_NATIVE
    source-native update-time evidence

`closed_date`:

    RETAIN_SOURCE_NATIVE
    source-native closure-time evidence

Contract-level canonical `UNAVAILABLE` assignments:

    none

The Decision Question 13 fields are:

- `address`;
- `comm_code`;
- `comm_name`;
- `location_type`;
- `longitude`;
- `latitude`;
- `point`.

All remain:

    DEFER_MAPPING

## Implementation Representation Question

The implementation must explicitly distinguish:

1. canonical Case fields;
2. retained source-native evidence;
3. evidence or provenance state;
4. an unavailable reason where genuinely applicable;
5. source-record input;
6. rejected record or adapter failure.

These concepts must not be collapsed into one dictionary merely for
convenience without a documented design decision.

This planning record does not select a detailed Python representation. The
smallest adequate structure must be decided incrementally during
implementation and justified against the executable adapter need.

## Scope

Increment 005 may only:

1. Establish the minimum Python package and test structure required for one
   executable adapter.
2. Define the smallest typed or otherwise explicit input boundary for one
   already-parsed Calgary source record.
3. Define the smallest output boundary required to represent admitted Case
   identity, accepted canonical mappings, retained source-native evidence,
   evidence state where required, and adapter rejection or failure.
4. Implement `service_request_id -> source_case_id`.
5. Implement `source_system = city_of_calgary_311`.
6. Implement `status_description -> source_status`.
7. Preserve `source`, `service_name`, `agency_responsible`, `updated_date`, and
   `closed_date` without semantic strengthening.
8. Preserve the non-mapping of `created_at`, `canonical_status`, `address`,
   `comm_code`, `comm_name`, `location_type`, `longitude`, `latitude`, and
   `point`.
9. Reject records that cannot satisfy the Increment 002 and Increment 004
   identity requirements.
10. Add deterministic automated tests using small in-memory fixtures.
11. Verify that repeated interpretation of the same valid source record
    produces the same semantically relevant adapter result.

## Non-Goals

This increment will not implement or define:

- reading the 1.9 GB Calgary CSV;
- CSV parsing;
- source acquisition;
- HTTP or Socrata retrieval;
- source snapshot management;
- bulk ingestion;
- PostgreSQL;
- migrations;
- persistence;
- SQL;
- analytical metrics;
- request-to-closure duration;
- resolution time;
- status normalization;
- a canonical-status vocabulary;
- `created_at` inference;
- timezone inference;
- timestamp-precision inference;
- location or community semantics;
- geospatial processing;
- PostGIS;
- dashboards;
- APIs;
- FastAPI;
- a CLI unless later proven necessary to test the adapter;
- Docker;
- CI;
- a generic multi-source adapter framework;
- ServiceNow;
- AI, LLM, RAG, or agent behavior;
- performance optimization for millions of rows.

## Row-Level Evidence-State Boundary

Increment 004 Decision Question 12 established the contract-level result:

    NO_CANONICAL_UNAVAILABLE_ASSIGNMENTS

At implementation level, an emitted Case may require an Increment 002
`UNAVAILABLE` state for an applicable optional canonical concept only when one
of the committed reasons actually applies:

- `VALUE_ABSENT`;
- `CONCEPT_ABSENT`;
- `EVIDENCE_INDETERMINATE`;
- `TRANSFORMATION_NOT_APPLIED`;
- `TRANSFORMATION_UNRESOLVED`.

None of these reasons may be preassigned merely because:

- `created_at` is `DEFER_MAPPING`;
- `canonical_status` is `DEFER_MAPPING`;
- a retained source-native field is blank;
- a Decision Question 13 field is deferred;
- implementation has not defined a transformation.

The implementation must preserve:

    DEFER_MAPPING != UNAVAILABLE

Planning does not establish which, if any, optional canonical concept will
receive a row-level `UNAVAILABLE` state in the implemented fixtures.

## Identity Failure Boundary

Increment 002 requires the identity core:

- `case_id`;
- `source_system`;
- `source_case_id`.

Increment 004 establishes:

    source_system = city_of_calgary_311
    source_case_id = service_request_id

Tests must cover at least:

- missing `service_request_id`;
- blank `service_request_id`;
- an unusable source-identity representation.

The adapter must not emit a valid Case when required identity is not
established.

No source-ID normalization is authorized by this plan. The implementation
must not strip, lowercase, uppercase, parse as integer, parse as UUID,
case-fold, or otherwise transform `service_request_id` unless a later explicit
implementation decision is justified and shown to remain consistent with the
controlling contracts.

## Case ID Physical Representation Decision

### Decision Question

What is the smallest defensible physical representation of `case_id` required
for the executable Calgary adapter, given that persistence and cross-source
entity resolution are outside Increment 005?

### Requirements

The Increment 005 representation must:

1. be deterministic;
2. preserve the exact source-identity components;
3. require no normalization of `service_request_id`;
4. require no database;
5. require no external dependency;
6. support equality and repeat-interpretation testing;
7. avoid introducing unsupported global-identity semantics;
8. remain replaceable when persistence requirements are introduced.

### Candidate Representations

#### A. Random UUID

Result:

    REJECT_FOR_INCREMENT_005

A random UUID introduces nondeterminism and an identity policy not required by
the current adapter.

#### B. Database-Generated Integer

Result:

    REJECT_FOR_INCREMENT_005

Persistence is outside scope and no database exists.

#### C. Hash of Source Identity

Result:

    REJECT_FOR_INCREMENT_005

A hash adds an opaque transformation plus collision and policy considerations
without a demonstrated need.

#### D. Concatenated String

Example:

    city_of_calgary_311:<source_case_id>

Result:

    REJECT_FOR_INCREMENT_005

A concatenated string is deterministic but introduces delimiter, escaping,
parsing, and string-encoding policy unnecessarily.

#### E. Structured Immutable Source Identity

Result:

    ACCEPT_FOR_INCREMENT_005

An immutable structured value preserves both exact identity components,
supports direct equality, requires no database or external dependency, and
introduces no encoding or parsing policy.

### Decision

    CASE_ID_PHYSICAL_REPRESENTATION:
        STRUCTURED_SOURCE_IDENTITY

For Increment 005, `case_id` will be represented as an immutable structured
value containing exactly:

- `source_system`;
- `source_case_id`.

For Calgary:

    source_system:
        city_of_calgary_311

    source_case_id:
        the source-native service_request_id value

No normalization or transformation of `service_request_id` is introduced.

This decision selects the minimum physical identity shape required by the
adapter. It does not select a Python class, dataclass, library, serialization
format, or persistence representation.

### Semantic Boundary

This is a physical-representation Design choice for Increment 005.

It does not establish that:

- canonical identity is universally identical to source identity;
- every future source must use the same representation;
- database primary keys must use this structure;
- source identities may be merged across systems;
- entity resolution is performed;
- the representation is a universal canonical ontology;
- a persistence layer must store the structure directly.

The authoritative identity semantics remain those of Increment 002. The
representation gives the executable adapter the smallest deterministic value
needed to satisfy the current Case contract.

### Three Distinct Identity Concepts

#### 1. Source Identity

    (source_system, source_case_id)

Meaning:

    Authoritative identity of the source-native operational work item.

#### 2. `case_id`

Meaning:

    Internal canonical Case identifier.

Increment 005 physical representation:

    Immutable structured value built from the authoritative source identity.

#### 3. Future Persistence Key

Meaning:

    Database or storage identifier if persistence later requires one.

Current status:

    NOT_DEFINED

These three concepts remain semantically distinct even though the Increment
005 physical `case_id` contains the same two values as the authoritative
source identity.

### Determinism Boundary

Given two valid adapter inputs with identical exact values for
`source_system` and `source_case_id`, their physical Case identifiers must
compare equal.

Given different authoritative source-identity pairs, their physical Case
identifiers must compare unequal.

This is a planned implementation property, not an observed result.

### No Source-ID Normalization

`service_request_id` is carried lexically as supplied through the
already-parsed adapter boundary.

The `case_id` decision does not authorize:

- stripping;
- whitespace normalization;
- case folding;
- lowercasing;
- uppercasing;
- integer conversion;
- UUID conversion;
- numeric canonicalization;
- delimiter parsing;
- source-ID rewriting.

Missing, blank, or unusable identity remains an adapter-rejection question.

### Revision and Falsification Conditions

This physical representation must be revisited if a later increment
establishes that:

- persistence requires an opaque or surrogate key;
- storage technology imposes a materially different identity representation;
- a valid Case must exist independently of source identity;
- cross-source identity or entity-resolution requirements are introduced;
- evidence falsifies the Increment 002 one-source-work-item to one-Case
  identity assumption;
- the structured representation prevents a required interoperability
  behavior.

These future possibilities do not currently falsify the decision.

### Claim Classification

Selected `case_id` representation:

    Design choice

Supporting identity semantics from Increment 002 and Increment 004:

    Prior contract definitions and Design choices

This decision produces no new External evidence, Engineering observation, or
Research conclusion.

## Source-Native Preservation Boundary

The adapter must not relabel:

- `source` as `source_system`;
- `service_name` as a canonical category;
- `agency_responsible` as an owning group, assigned group, or resolver;
- `updated_date` as `updated_at` or a lifecycle transition;
- `closed_date` as `resolved_at`, final closure, or terminal time.

Preservation means retaining the source-supported fact with its bounded
meaning. It does not mean promoting that fact into the canonical ontology.

The output representation must keep canonical Case fields distinguishable
from retained source-native evidence.

## Temporal Boundary

Increment 005 must preserve:

    REQUESTED_DATE_CREATION_TIME_EQUIVALENCE_UNRESOLVED

    UPDATED_DATE_RECORD_VS_LIFECYCLE_MEANING_UNRESOLVED

    CLOSED_DATE_LIFECYCLE_SEMANTICS_INCOMPLETE

    REOPENING_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA

    FINAL_CLOSURE_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA

    SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED

    TIMEZONE_SEMANTICS_UNRESOLVED

No parsing, typing, fixture, or representation convenience may erase these
limitations. In particular, preserving `closed_date` means retaining
source-native closure-time evidence; it does not establish `resolved_at`,
final closure, terminality, or resolution semantics.

## Assumptions

- Adapter input is already structurally parsed.
- Source-field names correspond to the Increment 004 Calgary contract.
- Increment 004 semantic decisions are authoritative for this adapter.
- Increment 002 remains authoritative for canonical Case and adapter
  conformance.
- Fixtures are controlled test examples, not new empirical evidence about
  Calgary.
- Deterministic execution can be tested independently of CSV ingestion or
  persistence.
- The minimum package and test structure will be selected to support this
  adapter rather than to anticipate unrelated future architecture.

## Threat Model and Failure Risks

### 1. Semantic strengthening

Implementation silently turns a deferred or source-native field into a
canonical fact.

### 2. Evidence-state collapse

`None`, null, missing, deferred, and unavailable become indistinguishable.

### 3. Identity fabrication

The adapter emits a Case without defensible source identity.

### 4. Native-evidence loss

Source facts accepted for retention are discarded.

### 5. Representation leakage

A convenient Python structure is later mistaken for a universal ontology.

### 6. Fixture overclaim

Passing controlled fixture tests is described as validation against the full
Calgary dataset.

### 7. Contract drift

Code behavior diverges from Increment 004 while tests merely encode the new
behavior.

## Planned Implementation Sequence

1. Establish the minimal test and package boundary.
2. Apply the selected structured `case_id` representation while choosing no
   more Case or adapter representation than the executable boundary requires.
3. Encode source-identity behavior.
4. Encode the accepted canonical mappings.
5. Encode retained source-native evidence.
6. Encode justified evidence-state behavior without treating deferral as
   unavailability.
7. Encode identity rejection paths.
8. Test that deferred concepts remain unpopulated.
9. Run reproducibility and repository checks.

This is a planned sequence. No implementation step or test result is claimed
to have occurred.

## Planned Test Categories

### Valid Identity

A valid `service_request_id` produces the established authoritative source
identity `(city_of_calgary_311, service_request_id)` and an immutable
structured `case_id` containing those exact components.

### Repeat Interpretation

The same valid source record produces an equivalent semantically relevant
adapter result, including an equal `case_id`.

### Different Source Identity

Different authoritative source-identity pairs produce unequal `case_id`
values.

### Exact Source-Identifier Preservation

The exact lexical `source_case_id` supplied through the already-parsed input
boundary is preserved in `case_id` without normalization.

### Case-Identifier Isolation

Native Calgary `source`, `status_description`, retained source-native
evidence, and deferred canonical concepts cannot affect `case_id`.

### Missing Identity

A source record without `service_request_id` does not emit a valid Case or
valid `case_id`.

### Blank Identity

A blank `service_request_id` does not emit a valid Case or valid `case_id`.

### Unusable Identity Representation

An unusable source-identity representation fails explicitly without invented
normalization.

### Source Status

`status_description` is preserved as `source_status` without normalization.

### Source and Source-System Separation

Native `source` is retained as submission-channel evidence and does not
replace `source_system`.

### Service-Type Preservation

`service_name` is preserved without an invented classification hierarchy.

### Responsibility Preservation

`agency_responsible` is preserved without becoming assignment or ownership.

### Update-Time Preservation

`updated_date` is preserved without becoming universal `updated_at` or a
lifecycle event.

### Closure-Time Preservation

`closed_date` is preserved without becoming `resolved_at`, final closure, or a
terminal timestamp.

### `created_at` Deferral

`requested_date` does not populate `created_at`.

### Canonical-Status Deferral

`status_description` does not populate `canonical_status`.

### Decision Question 13 Deferrals

`address`, `comm_code`, `comm_name`, `location_type`, `longitude`, `latitude`,
and `point` do not become canonical Case fields.

### Evidence-State Distinction

Deferred is not silently represented as `UNAVAILABLE`, and any actual
row-level unavailable state uses only a genuinely applicable committed reason.

### Native-Evidence Retention

The source-native evidence accepted for retention survives the adapter result
with its bounded meaning.

No planned test is an observed result. Controlled fixture results will not be
presented as full-dataset validation.

## Acceptance Criteria

Increment 005 is complete only when:

1. A minimal executable package and test structure exists.
2. The adapter accepts one already-parsed Calgary record through an explicit
   boundary.
3. Valid identity produces `source_system = city_of_calgary_311`,
   `source_case_id = service_request_id`, and the selected structured
   `case_id` containing those exact identity components.
4. Invalid or missing required identity fails without emitting a valid Case.
5. `status_description` is represented only as `source_status`.
6. `source` is preserved as submission-channel evidence and remains distinct
   from `source_system`.
7. `service_name` is preserved without canonical hierarchy invention.
8. `agency_responsible` is preserved without assignment or ownership
   semantics.
9. `updated_date` is preserved with its Increment 004 boundary.
10. `closed_date` is preserved with its Increment 004 boundary.
11. `created_at` remains unpopulated or unresolved according to the selected
    representation and is not fabricated.
12. `canonical_status` remains unpopulated or unresolved and is not
    fabricated.
13. All seven Decision Question 13 concepts remain deferred and are not
    promoted to canonical fields.
14. Row-level evidence-state handling preserves the Increment 002
    distinctions and does not equate deferral with unavailability.
15. Repeated interpretation of the same authoritative source identity yields
    equal `case_id` values, while different identity pairs yield unequal
    `case_id` values.
16. Automated tests pass.
17. `git diff --check` passes before closure.
18. No Increment 004 semantic decision is silently revised.

## Failure Criteria

The increment cannot close if any of the following occurs:

- a Case is emitted without valid source identity;
- native `source` becomes `source_system`;
- `requested_date` becomes `created_at` without a new justified
  source-contract decision;
- canonical-status normalization is invented;
- a service hierarchy is invented;
- `agency_responsible` becomes an owning, assigned, or resolving group;
- `updated_date` becomes universal `updated_at` or lifecycle-transition time;
- `closed_date` becomes resolution, finality, or a terminal timestamp;
- any Decision Question 13 field becomes a canonical field without contract
  revision;
- deferred and unavailable states collapse semantically;
- retained source-native evidence is silently lost;
- tests encode semantics that contradict Increment 004;
- fixture results are presented as full-dataset validation;
- persistence, analytics, ingestion, or unrelated infrastructure enters the
  increment;
- automated tests do not pass at closure.

## Claim Classification

Increment 002 and Increment 004 contract rules are prior Design choices and
contract definitions.

Adapter architecture introduced in Increment 005 will be a Design choice.

Test-execution results will be Engineering observations.

Passing controlled fixtures will be implementation evidence.

These results will not be:

- full-dataset validation;
- external validation;
- portability evidence;
- an analytical result;
- a business result;
- a research conclusion.

## Threats to Validity

- Fixtures may not represent full source variability.
- No CSV ingestion is tested.
- No retained Calgary artifact is exercised in this increment.
- No persistence behavior is tested.
- No cross-source behavior is tested.
- The physical representation may need revision when persistence is
  introduced.
- Row-level evidence-state handling may expose ambiguities requiring explicit
  contract revision.
- Deterministic adapter behavior does not prove that source semantics are
  true; it establishes only that implementation conforms to the current
  contract under the tested fixtures.

## Reproducibility Requirements

At closure, retain:

- the Python version;
- the exact dependency state if dependencies are introduced;
- the relevant test command;
- the observed test result;
- the repository commit;
- the fixtures used;
- every representation decision made during the increment;
- negative and failure cases;
- the `git diff --check` result.

This planning record does not claim that implementation reproducibility has
already been established.

## Implementation Record 001 - Minimal Python Execution/Test Boundary

Implementation step:

    Minimal Python execution/test boundary

### Design Choices

Source layout:

    src/support_operations_intelligence/

Test layout:

    tests/

Test framework:

    Python standard-library unittest

Execution command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Third-party dependencies introduced:

    none

Build-system decision:

    none

Installability claim:

    none

One executable and testable boundary is now required for Increment 005.
Standard-library `unittest` satisfies the current import-test need without
introducing a dependency. The explicit `PYTHONPATH=src` execution boundary
avoids implying that packaging or installability has already been designed.
The package structure remains deliberately minimal before any domain
representation is introduced.

### Observed Result

Repository-local Python version:

    Python 3.12.3

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Observed test result:

    tests run: 1
    failures: 0
    errors: 0
    result: OK

The minimal package imported successfully under the explicit
`PYTHONPATH=src` execution boundary using the repository-local Python
environment.

Direct inspection without the explicit source path produced:

    without_explicit_src_path = None

Inspection with the explicit source path found the package at:

    src/support_operations_intelligence/__init__.py

Importability through `PYTHONPATH=src` is the intended current execution
boundary. This result does not establish that the project is installed or
generally importable, and it makes no packaging or installability claim.

### Claim Classification

The `src/` layout is a Design choice.

Selection of standard-library `unittest` is a Design choice.

The successful import and test execution are Engineering observations.

This bounded result establishes only that the minimal package imports under
the explicit `PYTHONPATH=src` boundary using the repository-local interpreter.
It does not establish application behavior, adapter correctness, Case-contract
conformance, Calgary dataset validity, full reproducibility, package
installation, production readiness, portability, analytical correctness, or a
research conclusion.

## Follow-On Boundary

Likely later work remains outside Increment 005, including:

- CSV or source ingestion;
- dataset-level conformance scanning;
- PostgreSQL persistence;
- schemas and migrations;
- larger data-quality checks;
- analytical contracts;
- SQL analysis;
- management views;
- a ServiceNow adapter;
- cross-source portability testing.

## Planned Artifact

The planned implementation artifact is the smallest executable and tested
Calgary record-to-Case adapter boundary that conforms to Increment 002 and
Increment 004.

Its exact Python representation is not selected by this planning record.

## Current Status

Increment 005 remains:

    Status: Planned
    Completed: Not completed

No observed implementation result exists. No test is claimed to have run, and
no dependency is claimed to have been installed.

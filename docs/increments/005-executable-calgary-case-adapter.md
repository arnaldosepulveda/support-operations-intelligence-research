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

This planning record selects only the bounded `CaseId` Python container
recorded below. The smallest adequate structures for the remaining concepts
must be decided incrementally during implementation and justified against the
executable adapter need.

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
adapter. The Python container for that shape is selected separately below;
this physical decision introduces no library, serialization format, or
persistence representation.

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

## Case ID Python Container Decision

### Decision Question

What is the smallest Python representation that realizes the already accepted
immutable structured Case identifier without adding persistence,
serialization, validation-framework, or packaging policy?

### Requirements

The Python container must:

1. expose named `source_system` and `source_case_id` fields;
2. support value-based equality;
3. prevent ordinary mutation after construction;
4. use only the Python standard library;
5. add no persistence or serialization semantics;
6. add no source-ID normalization;
7. remain easy to test directly;
8. remain replaceable if later persistence requirements justify change.

### Candidate Containers

#### A. Plain Two-Element Tuple

Result:

    REJECT_FOR_INCREMENT_005

Value equality and immutability are available, but positional members obscure
the domain meaning of the two identity components.

#### B. `NamedTuple`

Result:

    REJECT_FOR_INCREMENT_005

`NamedTuple` is viable and immutable, but tuple semantics are unnecessary for
the current domain object and could encourage positional treatment.

#### C. Mutable Class or Mutable Dataclass

Result:

    REJECT_FOR_INCREMENT_005

Case identity should not be ordinarily mutable after construction.

#### D. Pydantic Model

Result:

    REJECT_FOR_INCREMENT_005

A Pydantic model introduces a third-party dependency and validation and
serialization policy that the current requirement does not need.

#### E. Standard-Library Frozen Dataclass

Result:

    ACCEPT_FOR_INCREMENT_005

### Decision

    CASE_ID_PYTHON_CONTAINER:
        FROZEN_DATACLASS

Planned implementation shape:

```python
@dataclass(frozen=True)
class CaseId:
    source_system: str
    source_case_id: str
```

This is a planned implementation shape. The class is not created by this
documentation decision, and no test for it is claimed to exist or pass.

### Rationale

The standard-library frozen dataclass provides:

- explicit named identity components;
- deterministic value equality;
- prevention of ordinary mutation through frozen-dataclass semantics;
- no third-party dependency;
- no database requirement;
- no serializer requirement;
- no inheritance hierarchy;
- no generalized identity framework;
- the minimal code needed for Increment 005.

### Type Boundary

`source_system`:

    str

`source_case_id`:

    str

For Increment 005, these types are a Calgary adapter implementation choice.
The `source_case_id` string must preserve the source-native lexical value.

The type choice does not authorize:

- parsing to integer;
- parsing to UUID;
- trimming;
- case conversion;
- whitespace normalization;
- numeric canonicalization;
- rewriting.

This decision does not claim that every future source system must use string
identifiers.

### Validation Boundary

The frozen dataclass represents a valid physical Case identifier. It does not
by itself decide whether raw adapter input contains valid identity.

Identity admission and rejection remain the adapter boundary's
responsibility. This decision does not yet define:

- missing-value behavior;
- blank-value behavior;
- whitespace-only behavior;
- exception type;
- validation API;
- adapter-result type.

The distinction is:

    CaseId representation
        !=
    raw source-record validation

### Dataclass Policy Boundary

This decision does not select:

- `slots=True`;
- `order=True`;
- `unsafe_hash=True`;
- a custom `__hash__`;
- a custom `__eq__`;
- a custom `__post_init__`;
- validators;
- factory methods;
- serialization methods;
- database-conversion methods.

Default frozen-dataclass behavior is sufficient unless later evidence shows
otherwise. No premature optimization is introduced.

### Determinism Implication

The planned implementation must satisfy:

```python
CaseId(
    source_system="city_of_calgary_311",
    source_case_id="X",
)
```

compares equal to another `CaseId` constructed with those exact values.
Changing either identity component must produce a non-equal `CaseId`.

This remains planned behavior, not an observed Engineering observation.

### Revision Conditions

The Python container choice must be reconsidered if later implementation
establishes a concrete need for:

- persistence-specific identifiers;
- serialization or interchange requirements;
- cross-language representation requirements;
- source identifiers that cannot be represented faithfully as strings;
- a materially different representation supported by performance evidence;
- cross-source identity requirements incompatible with this structure.

These possibilities do not currently falsify the decision.

### Claim Classification

The `FROZEN_DATACLASS` selection is a Design choice.

`STRUCTURED_SOURCE_IDENTITY` is a previously committed Design choice.

This documentation decision produces no new Engineering observation,
External evidence, Research result, or Research conclusion.

## Calgary Source Identity Admissibility Decision

### Decision Question

What minimum conditions must the already-parsed Calgary
`service_request_id` value satisfy before the adapter may construct a
`CaseId` and proceed toward Case emission?

### Boundary

This decision applies only to the raw adapter input field:

    service_request_id

for:

    source_system:
        city_of_calgary_311

It does not redefine `CaseId` itself and does not define identity policy for
every future source.

### Decision

    CALGARY_SOURCE_CASE_ID_ADMISSIBILITY:
        REQUIRE_PRESENT_NONBLANK_STRING

A raw Calgary record may contribute a valid `source_case_id` only when:

1. `service_request_id` is present;
2. its value is not `None`;
3. its value is a Python `str`;
4. its value is not the empty string `""`;
5. its value is not composed entirely of whitespace.

When all five conditions hold, the exact lexical string is preserved
unchanged.

### Invalid-Input Conditions

The distinct invalid-input conditions are:

`MISSING_SOURCE_CASE_ID`

: `service_request_id` is absent from the raw record boundary.

`NULL_SOURCE_CASE_ID`

: `service_request_id` is present with value `None`.

`NON_STRING_SOURCE_CASE_ID`

: `service_request_id` exists but is not a `str`.

`EMPTY_SOURCE_CASE_ID`

: `service_request_id == ""`.

`WHITESPACE_ONLY_SOURCE_CASE_ID`

: `service_request_id` contains only whitespace characters.

These names are Design vocabulary for the Increment 005 validation decision.
They do not select an `Enum`, exception class, error dataclass, result object,
return tuple, or error-code serialization.

### Validation and Normalization Boundary

Validation may inspect the source string to determine whether it contains any
non-whitespace character. Normalization is not authorized.

For example:

    " 001AbC-09 "

is nonblank and therefore may be admissible. If accepted, it remains exactly:

    " 001AbC-09 "

It must not become:

    "001AbC-09"

This decision does not authorize `strip()`, `lstrip()`, `rstrip()`, case
folding, lowercasing, uppercasing, numeric conversion, UUID conversion,
Unicode normalization, delimiter parsing, or rewriting. If implementation
later uses `isspace()` or another predicate to detect whitespace-only input,
that predicate must not alter the stored value.

### Non-String Rejection Rationale

The Calgary source contract maps a source-native textual identifier.
Converting an integer, float, UUID object, or another Python value to `str`
would introduce a lexical representation that was not supplied at the
adapter boundary. Increment 005 therefore rejects non-string raw identity
values rather than coercing them.

This is a Calgary adapter Design choice, not a universal claim that all source
systems use textual identifiers.

### Relation to Increment 003 Evidence

The retained Calgary artifact had:

    service_request_id empty count:
        0

    service_request_id whitespace-only count:
        0

Increment 003 records these retained-file counts as an Engineering
observation. They do not make validation unnecessary. The adapter identity
rule derives from the Case and source-contract requirement for defensible
source identity, not from an assumption that the retained artifact or future
Calgary data will always have the same quality. This decision does not claim
that production Calgary data can never contain invalid identity.

### Representation and Admission

`CaseId` represents an identity value after the adapter has determined that
the raw identity is admissible. Raw identity admissibility determines whether
the adapter is permitted to construct that `CaseId`.

Python technically permits:

```python
CaseId("city_of_calgary_311", "")
```

That representational capability does not establish that the Calgary adapter
may emit such an identity. The domain container intentionally remains simpler
than the adapter boundary.

### Rejection Transport Relationship

This admissibility decision establishes what constitutes inadmissible
identity. The mechanism for communicating acceptance or rejection is selected
separately in the Identity Rejection Transport Decision below; that transport
selection does not alter the admissibility semantics or rejection vocabulary.

### Planned Test Implications

Future implementation tests must cover:

- valid exact string `"12345"`: accepted and preserved lexically unchanged;
- valid padded nonblank string `" 001AbC-09 "`: accepted and preserved
  lexically unchanged;
- missing field: rejected before `CaseId` creation;
- `None`: rejected before `CaseId` creation;
- non-string value: rejected without coercion;
- empty string: rejected;
- whitespace-only string: rejected.

These are planned test requirements, not observed test results.

### Revision and Falsification Conditions

This decision must be revisited if evidence establishes, for example, that:

- Calgary legitimately uses empty or whitespace-only service identifiers;
- Calgary source identity is not faithfully represented as text;
- an authoritative source contract requires normalization before identity
  comparison;
- the adapter boundary changes so identity is already validated by a stronger
  upstream contract;
- the Increment 002 or Increment 004 identity assumptions are revised.

None of these conditions is currently claimed to hold.

### Claim Classification

    CALGARY_SOURCE_CASE_ID_ADMISSIBILITY:
        Design choice

    rejection-condition vocabulary:
        Design choice

    Increment 003 observed identity completeness:
        Engineering observation

This documentation change produces no new External evidence, Engineering
observation from execution, or Research conclusion.

## Identity Rejection Transport Decision

### Decision Question

How should the Increment 005 adapter represent the expected outcome that a
raw Calgary source identity is inadmissible, while keeping expected source
data rejection distinct from unexpected software failure?

### Requirements

The rejection transport must:

1. preserve the exact rejection reason;
2. make acceptance versus rejection explicit;
3. prevent an inadmissible identity from being mistaken for a valid `CaseId`;
4. avoid exceptions for an expected source-data outcome;
5. avoid sentinel ambiguity such as `None` or `False`;
6. avoid loosely structured tuple or dictionary conventions;
7. use only the Python standard library;
8. remain easy to test;
9. remain usable for later batch ingestion in which rejected records may need
   to be retained or counted;
10. introduce no persistence, serialization, logging, or external API policy.

### Candidate Transports

#### A. Return `None`

Result:

    REJECT_FOR_INCREMENT_005

`None` loses the specific rejection reason and conflates multiple failure
conditions.

#### B. Return `bool`

Result:

    REJECT_FOR_INCREMENT_005

A boolean indicates only pass or fail and loses both the reason and the
accepted identity.

#### C. Return a Tuple

Example:

```python
(CaseId | None, reason | None)
```

Result:

    REJECT_FOR_INCREMENT_005

A tuple permits ambiguous or internally inconsistent combinations and relies
on positional convention.

#### D. Return a Dictionary

Result:

    REJECT_FOR_INCREMENT_005

A dictionary is weakly structured and allows malformed combinations without
a current need for generic serialization.

#### E. Raise an Ordinary Exception

Examples include `ValueError` or another ordinary exception for expected
invalid identity.

Result:

    REJECT_FOR_INCREMENT_005

Inadmissible source identity is an expected domain outcome, not necessarily an
exceptional software failure. Exception transport would complicate later
batch processing and failure retention.

#### F. Explicit Typed Result Variants

Result:

    ACCEPT_FOR_INCREMENT_005

### Decision

    IDENTITY_REJECTION_TRANSPORT:
        EXPLICIT_RESULT_VARIANTS

The planned result model has two mutually exclusive outcomes:

`ACCEPTED`

: contains a `CaseId`.

`REJECTED`

: contains an `IdentityRejectionReason`.

No result may simultaneously represent both acceptance and rejection.

### Rejection-Reason Representation

    IDENTITY_REJECTION_REASON_CONTAINER:
        ENUM

Planned standard-library representation:

```python
from enum import Enum


class IdentityRejectionReason(Enum):
    MISSING_SOURCE_CASE_ID = "MISSING_SOURCE_CASE_ID"
    NULL_SOURCE_CASE_ID = "NULL_SOURCE_CASE_ID"
    NON_STRING_SOURCE_CASE_ID = "NON_STRING_SOURCE_CASE_ID"
    EMPTY_SOURCE_CASE_ID = "EMPTY_SOURCE_CASE_ID"
    WHITESPACE_ONLY_SOURCE_CASE_ID = "WHITESPACE_ONLY_SOURCE_CASE_ID"
```

This is planned structure only and is not implemented by this documentation
decision. The enum values correspond exactly to the already committed
rejection vocabulary; no new reason is added.

### Result Variants

Planned standard-library shapes:

```python
@dataclass(frozen=True)
class AcceptedIdentity:
    case_id: CaseId


@dataclass(frozen=True)
class RejectedIdentity:
    reason: IdentityRejectionReason


IdentityAdmissionResult = AcceptedIdentity | RejectedIdentity
```

These classes and alias are planned implementation only and are not created by
this documentation decision.

### Mutual-Exclusivity Invariant

`AcceptedIdentity` always contains a `CaseId`.

`RejectedIdentity` never contains a `CaseId`; it contains only an
`IdentityRejectionReason`.

An inadmissible raw source identity therefore cannot accidentally carry a
physical canonical Case identifier. This is a structural property of the
result variants rather than a runtime convention such as `case_id = None`.

### Expected Rejection and Software Failure

Expected domain rejection includes:

- missing `source_case_id`;
- null `source_case_id`;
- non-string `source_case_id`;
- empty `source_case_id`;
- whitespace-only `source_case_id`.

Its transport is:

    RejectedIdentity

Unexpected software or system failures might later include a programming
defect, impossible internal state, or infrastructure failure. Their transport
is:

    NOT_DEFINED_BY_THIS_DECISION

This decision does not design general exception handling and does not claim
that all future adapter failures become `RejectedIdentity`.

### Rejected-Input Retention Boundaries

    REJECTED_RAW_VALUE_RETENTION:
        NOT_DEFINED

`RejectedIdentity` does not contain the rejected raw identity value. Whether
rejected source values should be retained belongs to later ingestion,
provenance, or evidence design. This transport preserves only why admission
failed; it does not silently add `raw_value`, `raw_record`, `source_payload`,
`metadata`, `timestamp`, or logging-context fields.

    REJECTED_SOURCE_RECORD_RETENTION:
        NOT_DEFINED

This transport decision establishes no dead-letter storage, rejection table,
audit persistence, log format, provenance storage, or database schema.

### Relationship to `CaseId`

`CaseId` represents an already-admissible identity and remains
validation-free. `AcceptedIdentity` communicates that admission succeeded and
carries that `CaseId`. `RejectedIdentity` communicates that admission failed
and carries only a reason. `IdentityRejectionReason` identifies which
committed admissibility condition failed.

### Callable API Relationship

The result transport was selected independently of its callable API. The
minimal callable boundary that returns this transport is selected separately
in the Calgary Identity Admission API Decision below; that API decision does
not alter the result variants or rejection vocabulary.

### Planned Test Implications

Future implementation tests must establish:

1. a valid admissible identity produces `AcceptedIdentity`;
2. `AcceptedIdentity` contains the exact expected `CaseId`;
3. missing identity produces `RejectedIdentity` with
   `MISSING_SOURCE_CASE_ID`;
4. `None` produces `RejectedIdentity` with `NULL_SOURCE_CASE_ID`;
5. a non-string produces `RejectedIdentity` with
   `NON_STRING_SOURCE_CASE_ID`;
6. an empty string produces `RejectedIdentity` with
   `EMPTY_SOURCE_CASE_ID`;
7. a whitespace-only string produces `RejectedIdentity` with
   `WHITESPACE_ONLY_SOURCE_CASE_ID`;
8. a padded nonblank identity produces `AcceptedIdentity` with the exact
   lexical value preserved;
9. `RejectedIdentity` exposes no `case_id` field;
10. each accepted or rejected result is immutable under the selected frozen
    dataclass representation.

These are planned tests only; no execution result is claimed.

### Failure Conditions

The transport design is violated if implementation:

- returns `None` for rejection;
- returns only boolean success or failure;
- loses the rejection reason;
- coerces rejection reasons into arbitrary strings outside the committed
  vocabulary;
- constructs `CaseId` before admissibility succeeds;
- includes `CaseId` in a rejected outcome;
- uses expected rejection as an exception-only control path;
- adds normalization;
- adds unapproved rejection reasons;
- silently stores raw rejected values or full records as part of this
  transport.

### Revision Conditions

This design must be revisited if later requirements establish:

- a framework-specific result abstraction worth adopting;
- external API serialization requirements;
- cross-language interchange requirements;
- persistence or audit requirements needing richer rejection evidence;
- performance evidence showing object-per-result transport is materially
  unsuitable;
- a revised adapter architecture in which identity admission is guaranteed
  upstream.

None of these conditions is currently claimed to hold.

### Claim Classification

    EXPLICIT_RESULT_VARIANTS:
        Design choice

    IdentityRejectionReason enum:
        Design choice

    AcceptedIdentity / RejectedIdentity:
        Design choices

    Existing rejection vocabulary:
        previously committed Design choice

This documentation step produces no new Engineering observation, External
evidence, Research result, or Research conclusion.

## Calgary Identity Admission API Decision

### Decision Question

What minimal callable boundary should apply the already committed Calgary
source identity admissibility rules and return the already implemented
identity admission result variants?

### Callable Decision

    IDENTITY_ADMISSION_API:
        CALGARY_RECORD_MAPPING_FUNCTION

Planned callable:

```python
admit_calgary_source_identity(
    record: Mapping[str, object],
) -> IdentityAdmissionResult
```

This callable API is a Design choice. It is not implemented by this
documentation step.

### Input Boundary

    IDENTITY_ADMISSION_INPUT:
        ALREADY_PARSED_RECORD_MAPPING

The input represents one already-parsed Calgary source record. The function
requires only mapping-style read access.

It does not open CSV files, parse CSV text, fetch Socrata data, mutate the
record, require `dict` specifically, perform bulk ingestion, validate the full
Calgary record, establish provenance, or perform persistence.

### Why `Mapping` Rather Than `dict`

The function requires only read-only key lookup. A concrete `dict` requirement
would be stronger than necessary. The planned boundary therefore uses:

    Mapping[str, object]

rather than:

    dict[str, object]

This is an Increment 005 implementation boundary, not a claim that every
future source adapter must use `Mapping`.

### Why the Mapping Value Is `object`

The raw mapping value is typed as `object` because the function must be able
to observe and reject `None`, integers, floats, UUID objects, and other
non-string values without pretending the upstream parser has already
guaranteed string identity. The function must not coerce those values.

### Fixed Source Identity Field

    CALGARY_SOURCE_CASE_ID_FIELD:
        service_request_id

The identity-admission function examines only this key for source identity.
It must not derive identity from another Calgary field, row position, hash,
timestamp, source submission channel, service name, agency, or synthetic
sequence.

### Fixed Source Namespace

    CALGARY_SOURCE_SYSTEM:
        city_of_calgary_311

On successful admission, the produced `CaseId` uses exactly:

```python
source_system = "city_of_calgary_311"
```

The raw Calgary field named `source` must not be used as `source_system`. This
preserves Increment 004 Decision Question 7.

### Deterministic Decision Precedence

The function evaluates the identity conditions in this exact order:

1. **Field absent.** If `"service_request_id"` is not present in `record`,
   return:

   ```python
   RejectedIdentity(
       reason=IdentityRejectionReason.MISSING_SOURCE_CASE_ID,
   )
   ```

2. **Null.** If the value is `None`, return:

   ```python
   RejectedIdentity(
       reason=IdentityRejectionReason.NULL_SOURCE_CASE_ID,
   )
   ```

3. **Non-string.** If the value is not an instance of `str`, return:

   ```python
   RejectedIdentity(
       reason=IdentityRejectionReason.NON_STRING_SOURCE_CASE_ID,
   )
   ```

4. **Empty string.** If the value is `""`, return:

   ```python
   RejectedIdentity(
       reason=IdentityRejectionReason.EMPTY_SOURCE_CASE_ID,
   )
   ```

5. **Whitespace-only string.** If the value contains only whitespace, return:

   ```python
   RejectedIdentity(
       reason=IdentityRejectionReason.WHITESPACE_ONLY_SOURCE_CASE_ID,
   )
   ```

6. **Accept.** Otherwise construct:

   ```python
   CaseId(
       source_system="city_of_calgary_311",
       source_case_id=value,
   )
   ```

   and return `AcceptedIdentity(case_id=that_case_id)`.

This precedence is part of the Design decision.

### String Preservation and Non-Coercion

The value `" 001AbC-09 "` is accepted because it contains non-whitespace
characters. Its `source_case_id` remains exactly `" 001AbC-09 "`; no stripping
or normalization occurs.

Whitespace-only detection may use a predicate such as `value.isspace()` when
implemented, provided the predicate does not transform the value. This
decision does not require one specific expression.

Values such as `123`, `1.0`, `UUID(...)`, or another non-string object produce
`NON_STRING_SOURCE_CASE_ID`. The function must not call `str(value)` before
admission.

### `CaseId` Construction Invariant

`CaseId` construction occurs only after all rejection conditions have been
ruled out. Missing, null, non-string, empty, and whitespace-only input
therefore produces no `CaseId`. This preserves the existing result-transport
invariant.

### Function Responsibility

The identity-admission function is responsible only for:

    raw Calgary service_request_id
        -> identity admissibility decision
        -> AcceptedIdentity or RejectedIdentity

It is not responsible for full Case construction, `source_status` mapping,
`created_at`, `canonical_status`, Decision Question 7 through Decision
Question 13 fields, evidence-state representation, Case admission beyond
source identity, ingestion, persistence, logging, metrics, or analytics.

### Expected Rejection and Software Failure

The five committed invalid-identity conditions are expected domain outcomes.
The function returns `RejectedIdentity` for those conditions and does not
raise an exception merely because one occurs.

Unexpected programming or system failure transport remains:

    NOT_DEFINED_BY_THIS_DECISION

This decision introduces no broad `try/except Exception` behavior and does not
convert unexpected software defects into `RejectedIdentity`.

### Retention Boundaries

    REJECTED_RAW_VALUE_RETENTION:
        NOT_DEFINED

    REJECTED_SOURCE_RECORD_RETENTION:
        NOT_DEFINED

The function result still carries only a `CaseId` in `AcceptedIdentity` or an
`IdentityRejectionReason` in `RejectedIdentity`.

### Planned Test Matrix

Future implementation tests must cover:

1. missing `service_request_id` produces `RejectedIdentity` with
   `MISSING_SOURCE_CASE_ID`;
2. `service_request_id = None` produces `RejectedIdentity` with
   `NULL_SOURCE_CASE_ID`;
3. `service_request_id = 123` produces `RejectedIdentity` with
   `NON_STRING_SOURCE_CASE_ID`;
4. `service_request_id = ""` produces `RejectedIdentity` with
   `EMPTY_SOURCE_CASE_ID`;
5. `service_request_id = "   "` produces `RejectedIdentity` with
   `WHITESPACE_ONLY_SOURCE_CASE_ID`;
6. `service_request_id = "\t\n"` produces `RejectedIdentity` with
   `WHITESPACE_ONLY_SOURCE_CASE_ID`;
7. `service_request_id = "ABC-123"` produces `AcceptedIdentity` containing
   `CaseId("city_of_calgary_311", "ABC-123")`;
8. `service_request_id = " 001AbC-09 "` produces `AcceptedIdentity` with exact
   lexical preservation;
9. a successful result uses `source_system` exactly
   `city_of_calgary_311`;
10. the raw Calgary field `source` cannot override `source_system`;
11. the input mapping is not mutated;
12. rejected outcomes contain no `CaseId`.

These are planned tests only. No execution result is claimed.

### Unresolved Full-Adapter Concerns

This decision does not resolve the Case Python representation, full Calgary
Case adapter API, evidence-state physical representation, source-native
retained-field container, `created_at` treatment, `canonical_status`
treatment, persistence boundary, or batch-ingestion API.

### Failure Conditions

Future implementation violates this decision if it:

- accepts a missing `service_request_id`;
- accepts `None`;
- accepts a non-string value;
- coerces non-string identity to `str`;
- accepts an empty string;
- accepts a whitespace-only string;
- strips or normalizes accepted identity;
- constructs `CaseId` before admission succeeds;
- uses the raw Calgary `source` field as `source_system`;
- uses a `source_system` other than `city_of_calgary_311`;
- raises an exception as normal transport for an expected rejection;
- mutates the supplied mapping;
- validates unrelated Calgary fields in this function;
- constructs a full Case.

### Revision Conditions

This API decision must be revisited if later evidence or requirements
establish:

- upstream typed parsing that guarantees a stronger identity input contract;
- a need for a source-independent generic admission abstraction;
- non-`Mapping` source records;
- cross-language or API interchange requirements;
- materially different Calgary identity semantics;
- revised Increment 002 or Increment 004 identity assumptions.

None of these conditions is currently claimed to hold.

### Claim Classification

    identity-admission API:
        Design choice

    Mapping input boundary:
        Design choice

    decision precedence:
        Design choice

    fixed Calgary namespace assignment:
        implementation of prior Increment 004 Design choice

    planned tests:
        Planned tests, not observations

This documentation step produces no new Engineering observation, External
evidence, Research result, or Research conclusion.

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
2. Apply the selected structured `case_id` representation through the planned
   frozen-dataclass container while choosing no more Case or adapter
   representation than the executable boundary requires.
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

## Implementation Record 002 - CaseId Representation

### Objective

Realize the committed `STRUCTURED_SOURCE_IDENTITY` physical representation
using the committed frozen-dataclass Python container.

### Files

    src/support_operations_intelligence/identity.py
    tests/test_case_id.py

### Design Implemented

```python
@dataclass(frozen=True)
class CaseId:
    source_system: str
    source_case_id: str
```

Third-party dependencies introduced:

    none

Raw input validation:

    not implemented

Calgary adapter:

    not implemented

The implementation contains only the two committed fields and default frozen
dataclass behavior. It introduces no normalization, parsing, validation,
factory, serialization, persistence, source-system assignment, source-record
extraction, or adapter behavior.

### Expected Pre-Implementation Failure

Executed before `identity.py` existed:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_case_id.py' \
      -v

Observed discovery result:

    tests reported: 1 failed test module
    errors: 1
    result: FAILED (errors=1)

Error type:

    ModuleNotFoundError

Reason:

    No module named 'support_operations_intelligence.identity'

This expected pre-implementation failure is an Engineering observation. The
CaseId-focused test could not pass before the identity module existed. This is
test-first evidence, not a product defect.

### Focused Post-Implementation Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_case_id.py' \
      -v

Observed result:

    tests run: 6
    failures: 0
    errors: 0
    result: OK

### Full-Suite Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Observed result:

    tests run: 7
    failures: 0
    errors: 0
    result: OK

The existing package-boundary smoke test remained passing.

### Direct Representation Verification

The direct repository-local Python verification observed:

    is_dataclass = True
    fields = ['source_system', 'source_case_id']
    a_equals_b = True
    a_equals_c = False
    preserved_source_case_id = ' 001AbC-09 '

The mutation test also observed that ordinary assignment to a field raises
`dataclasses.FrozenInstanceError`.

These results establish that the implemented `CaseId` conforms to the
currently tested representation properties under the repository-local Python
execution boundary.

### Validation and Claim Boundary

`CaseId` represents an already-valid identity value. This step does not
implement or test raw-record validation, `None`, missing mapping keys, blank or
whitespace-only identifiers, adapter rejection, exception policy,
source-system assignment, `service_request_id` extraction, Calgary records,
source mappings, or evidence states.

The `CaseId` implementation is a Design implementation of prior Design
choices. The expected red test, focused green test execution, full-suite test
execution, and direct verification are Engineering observations.

This step produces no External evidence, analytical result, Calgary semantic
validation, portability evidence, or research conclusion. It does not
establish adapter correctness, source-record validation correctness, Calgary
identity validity, dataset validation, cross-source portability, persistence
correctness, or production readiness.

## Implementation Record 003 - Identity Admission Result Types

### Objective

Implement the committed typed identity-admission transport without
implementing admission behavior.

### Files

    src/support_operations_intelligence/identity.py
    tests/test_identity_admission_result.py

### Design Implemented

Implemented:

- `IdentityRejectionReason`;
- `AcceptedIdentity`;
- `RejectedIdentity`;
- `IdentityAdmissionResult`.

The enum contains exactly the five committed rejection reasons. The two
result variants use the committed frozen-dataclass shapes:

```python
@dataclass(frozen=True)
class AcceptedIdentity:
    case_id: CaseId


@dataclass(frozen=True)
class RejectedIdentity:
    reason: IdentityRejectionReason


IdentityAdmissionResult = AcceptedIdentity | RejectedIdentity
```

Admission logic:

    not implemented

Callable API status at the time of this implementation record:

    IDENTITY_ADMISSION_API:
        NOT_DEFINED

The callable API was selected later in the Calgary Identity Admission API
Decision above. This implementation record does not claim that callable was
implemented.

    REJECTED_RAW_VALUE_RETENTION:
        NOT_DEFINED

    REJECTED_SOURCE_RECORD_RETENTION:
        NOT_DEFINED

Third-party dependencies introduced:

    none

No validator, adapter function, source-field extraction, normalization,
serialization, persistence, logging, provenance, or rejected-data retention
behavior is implemented.

### Expected Pre-Implementation Failure

Executed before the result types existed:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_identity_admission_result.py' \
      -v

Observed discovery result:

    tests reported: 1 failed test module
    errors: 1
    result: FAILED (errors=1)

Error type:

    ImportError

Reason:

    cannot import name 'AcceptedIdentity' from
    'support_operations_intelligence.identity'

This expected pre-implementation failure is an Engineering observation. The
transport-focused test could not pass before the planned result types existed.
It is test-first evidence, not a product defect.

### Focused Post-Implementation Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_identity_admission_result.py' \
      -v

Observed result:

    tests run: 10
    failures: 0
    errors: 0
    result: OK

### `CaseId` Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_case_id.py' \
      -v

Observed result:

    tests run: 6
    failures: 0
    errors: 0
    result: OK

### Full-Suite Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Observed result:

    tests run: 17
    failures: 0
    errors: 0
    result: OK

### Direct Structural Verification

The direct repository-local Python verification observed:

    reason_names = [
        'MISSING_SOURCE_CASE_ID',
        'NULL_SOURCE_CASE_ID',
        'NON_STRING_SOURCE_CASE_ID',
        'EMPTY_SOURCE_CASE_ID',
        'WHITESPACE_ONLY_SOURCE_CASE_ID',
    ]
    reason_values = [
        'MISSING_SOURCE_CASE_ID',
        'NULL_SOURCE_CASE_ID',
        'NON_STRING_SOURCE_CASE_ID',
        'EMPTY_SOURCE_CASE_ID',
        'WHITESPACE_ONLY_SOURCE_CASE_ID',
    ]
    accepted_is_dataclass = True
    accepted_fields = ['case_id']
    rejected_is_dataclass = True
    rejected_fields = ['reason']
    accepted_case_id = CaseId(
        source_system='city_of_calgary_311',
        source_case_id='ABC-123',
    )
    rejected_reason = EMPTY_SOURCE_CASE_ID
    rejected_has_case_id = False
    accepted_has_reason = False

The focused tests also observed that ordinary mutation of each result variant
raises `dataclasses.FrozenInstanceError`.

These exact fields are implementation evidence that the two committed result
variants themselves are structurally exclusive. This does not claim that
Python's union type prevents arbitrary unrelated objects from existing.

### Claim Classification and Boundary

The result-type implementation is a Design implementation of prior Design
choices. The expected red test, focused test result, `CaseId` regression
result, full-suite result, and direct verification are Engineering
observations.

The bounded result establishes that the identity-admission transport types
conform to the currently tested structural design under the repository-local
Python execution boundary.

This step does not establish identity validation correctness, Calgary adapter
correctness, rejection behavior for raw records, ingestion correctness,
dataset validation, portability, production readiness, an External evidence
claim, an analytical result, Calgary semantic validation, or a Research
conclusion.

## Implementation Record 004 - Calgary Identity Admission Function

### Objective

Implement the already committed identity-admission API and deterministic
decision precedence without implementing the full Case adapter.

### Files

    src/support_operations_intelligence/identity.py
    tests/test_calgary_identity_admission.py

### Design Implemented

Implemented:

    admit_calgary_source_identity

Input:

    Mapping[str, object]

Output:

    IdentityAdmissionResult

Source identity field:

    service_request_id

Fixed source system:

    city_of_calgary_311

Decision order:

1. missing;
2. `None`;
3. non-string;
4. empty;
5. whitespace-only;
6. accept.

Full Case adapter:

    not implemented

Rejected raw value retention:

    NOT_DEFINED

Rejected source record retention:

    NOT_DEFINED

Third-party dependencies introduced:

    none

The callable is annotated with `record: Mapping[str, object]` and returns
`IdentityAdmissionResult`. These annotations document the API boundary; they
do not establish runtime validation by themselves.

The implementation distinguishes an absent key from a present `None` value,
rejects non-string input without coercion, rejects empty and whitespace-only
strings, preserves accepted lexical values exactly, constructs `CaseId` only
after successful admission, fixes the namespace to `city_of_calgary_311`, and
does not mutate the input mapping.

It does not inspect or map `requested_date`, `updated_date`, `closed_date`,
`status_description`, `source`, `service_name`, `agency_responsible`,
`address`, `comm_code`, `comm_name`, `location_type`, `longitude`, `latitude`,
or `point`. The test containing raw `source = "Phone"` uses that value only to
verify that it cannot override the fixed namespace.

No full Case construction, CSV parsing, ingestion, evidence-state behavior,
normalization, parsing, serialization, persistence, logging, provenance, raw
rejected-value retention, or source-record retention is implemented.

### Expected Pre-Implementation Failure

Executed before `admit_calgary_source_identity` existed:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_calgary_identity_admission.py' \
      -v

Observed discovery result:

    tests reported: 1 failed test module
    errors: 1
    result: FAILED (errors=1)

Error type:

    ImportError

Reason:

    cannot import name 'admit_calgary_source_identity' from
    'support_operations_intelligence.identity'

This expected pre-implementation failure is an Engineering observation. The
focused test could not pass before the designed callable was implemented. It
is test-first evidence, not a product defect.

### Focused Post-Implementation Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_calgary_identity_admission.py' \
      -v

Observed result:

    tests run: 12
    failures: 0
    errors: 0
    result: OK

### Identity-Result Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_identity_admission_result.py' \
      -v

Observed result:

    tests run: 10
    failures: 0
    errors: 0
    result: OK

### `CaseId` Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_case_id.py' \
      -v

Observed result:

    tests run: 6
    failures: 0
    errors: 0
    result: OK

### Full-Suite Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Observed result:

    tests run: 29
    failures: 0
    errors: 0
    result: OK

### Direct Decision-Path Verification

The direct repository-local Python verification observed:

    {} -> REJECTED MISSING_SOURCE_CASE_ID
    {'service_request_id': None} -> REJECTED NULL_SOURCE_CASE_ID
    {'service_request_id': 123} -> REJECTED NON_STRING_SOURCE_CASE_ID
    {'service_request_id': ''} -> REJECTED EMPTY_SOURCE_CASE_ID
    {'service_request_id': '   '} ->
        REJECTED WHITESPACE_ONLY_SOURCE_CASE_ID
    {'service_request_id': 'ABC-123'} ->
        ACCEPTED 'city_of_calgary_311' 'ABC-123'
    {'service_request_id': ' 001AbC-09 ', 'source': 'Phone'} ->
        ACCEPTED 'city_of_calgary_311' ' 001AbC-09 '

This directly preserves the distinction between missing and `None`, rejects
non-string input without producing `"123"`, preserves the padded lexical
value, and shows that raw `source` does not affect the namespace.

### Input Immutability Verification

The direct repository-local verification observed:

    unchanged = True
    record = {
        'service_request_id': 'ABC-123',
        'source': 'Phone',
    }

### Claim Classification and Boundary

The function is a Design implementation of the committed API, identity
admissibility, namespace, lexical-preservation, decision-precedence, and
result-transport choices. The expected red result, focused result,
identity-result regression, `CaseId` regression, full-suite result, direct
path verification, and input-immutability verification are Engineering
observations.

The implemented Calgary identity-admission function conforms to the currently
tested Increment 005 identity admissibility, namespace, lexical preservation,
and result-transport design under the repository-local Python execution
boundary.

This step does not establish full Calgary adapter correctness, canonical Case
correctness, dataset-wide validation, ingestion correctness, source semantic
correctness beyond committed mappings, persistence correctness, portability,
production readiness, External evidence, an analytical result, or a Research
conclusion.

## Field Evidence Physical Representation Decision

### Decision Question

How should Increment 005 physically represent the canonical distinction
between observed, derived, simulated, and unavailable field evidence without
permitting contradictory state/value combinations or collapsing
`DEFER_MAPPING` into `UNAVAILABLE`?

### Decision

    FIELD_EVIDENCE_PHYSICAL_REPRESENTATION:
        EXPLICIT_VARIANTS

Increment 005 selects planned immutable standard-library dataclass variants
equivalent to:

```python
ObservedEvidence[T]
    value: T

DerivedEvidence[T]
    value: T

SimulatedEvidence[T]
    value: T

UnavailableEvidence
    reason: UnavailableReason
```

with a planned union equivalent to:

```python
FieldEvidence[T] = (
    ObservedEvidence[T]
    | DerivedEvidence[T]
    | SimulatedEvidence[T]
    | UnavailableEvidence
)
```

This is a Design choice. No evidence variant or union is implemented by this
documentation decision.

### Rationale for Explicit Variants

Explicit variants structurally avoid contradictory combinations such as:

```python
state = OBSERVED
value = None
unavailable_reason = VALUE_ABSENT
```

or:

```python
state = UNAVAILABLE
value = "some value"
reason = None
```

Available evidence and unavailable evidence are different result shapes, not
loosely coordinated nullable fields. The variant determines which payload is
valid and prevents a single object from simultaneously carrying a field value
and an unavailable reason.

### Canonical State Correspondence

The physical variants correspond exactly to the existing canonical
field-provenance vocabulary:

    ObservedEvidence
        -> OBSERVED

    DerivedEvidence
        -> DERIVED

    SimulatedEvidence
        -> SIMULATED

    UnavailableEvidence
        -> UNAVAILABLE

No additional canonical provenance state is introduced, and the existing
canonical vocabulary is not renamed.

### Unavailable Reason Representation

    UNAVAILABLE_REASON_CONTAINER:
        ENUM

The planned standard-library enum contains exactly:

- `VALUE_ABSENT`;
- `CONCEPT_ABSENT`;
- `EVIDENCE_INDETERMINATE`;
- `TRANSFORMATION_NOT_APPLIED`;
- `TRANSFORMATION_UNRESOLVED`.

No additional unavailable reason is authorized by this decision. The enum is
not implemented in this task.

### `DEFER_MAPPING` Is Not `UNAVAILABLE`

This distinction is mandatory:

    DEFER_MAPPING != UNAVAILABLE

`DEFER_MAPPING` means that the source contract has not authorized a canonical
mapping. It is a source-contract Design status.

`UNAVAILABLE` means that a canonical concept or mapping is applicable for a
particular emitted Case, but the evidence needed to populate it is unavailable
for a justified canonical reason. It is a Case-level field-provenance state.

Therefore, `DEFER_MAPPING` must not automatically become
`UnavailableEvidence(...)`.

The current Calgary contract includes:

    requested_date -> created_at:
        DEFER_MAPPING

    canonical_status:
        DEFER_MAPPING

    Decision Question 13 deferred fields:
        DEFER_MAPPING

These decisions must not be represented merely by attaching:

```python
UnavailableEvidence(
    TRANSFORMATION_NOT_APPLIED
)
```

to every Case. Doing so would silently convert a contract-level unresolved
mapping decision into a row-level evidence statement. In particular, a
transformation that has merely been contemplated or whose mapping is deferred
does not satisfy `TRANSFORMATION_NOT_APPLIED`.

### Contract-Level Status Versus Case-Level Evidence

Contract-level mapping statuses include:

- `ACCEPT_MAPPING`;
- `RETAIN_SOURCE_NATIVE`;
- `DEFER_MAPPING`.

They describe what an adapter contract is authorized to do.

Case-level field-evidence variants include:

- `ObservedEvidence(value)`;
- `DerivedEvidence(value)`;
- `SimulatedEvidence(value)`;
- `UnavailableEvidence(reason)`.

They describe the evidence state of an applicable field for one emitted Case.
The two vocabularies must remain separate.

Source-mapping statuses and related terms must not be added as field-evidence
states or unavailable reasons. This decision therefore introduces no
`DEFERRED`, `NOT_MAPPED`, `RETAIN_SOURCE_NATIVE`, or `ACCEPTED_MAPPING`
evidence state or reason.

### Current Calgary Use Boundary

Defining all four physical variants realizes the canonical provenance
vocabulary. It does not authorize the Calgary adapter to emit all four states
arbitrarily.

For the current Increment 005 boundary:

- `OBSERVED` may later be appropriate where Increment 004 authorizes a direct
  source-supported mapping or retained source-native value;
- `UNAVAILABLE` may later be appropriate only when the concept or mapping is
  applicable, the particular Case lacks sufficient evidence, and one of the
  canonical unavailable reasons actually applies;
- `DERIVED` requires a separately justified deterministic transformation;
- `SIMULATED` requires explicitly simulated evidence.

No current Calgary field is newly classified `DERIVED` or `SIMULATED` by this
decision. No deferred Calgary field is newly classified `UNAVAILABLE`.

Increment 004 Decision Question 12 remains:

    NO_CANONICAL_UNAVAILABLE_ASSIGNMENTS

Future per-Case `UNAVAILABLE` may be emitted only when an applicable canonical
concept or mapping and one of the canonical reasons are justified.

### Value-Preservation Boundary

`ObservedEvidence[T]`, `DerivedEvidence[T]`, and `SimulatedEvidence[T]` carry
the evidence value supplied by the relevant authorized mapping or
transformation.

The evidence wrapper itself does not:

- normalize;
- parse;
- coerce;
- round;
- strip;
- infer;
- reinterpret;
- canonicalize.

Those behaviors, if ever justified, belong to the corresponding field mapping
or transformation decision.

### No Optional-`None` Shortcut

Increment 005 rejects a physical model equivalent to:

```python
source_status: str | None
```

when provenance state matters. `None` alone cannot distinguish:

- unavailable value;
- concept absent;
- indeterminate evidence;
- transformation not applied;
- transformation unresolved.

It also cannot preserve `OBSERVED`, `DERIVED`, or `SIMULATED` provenance. This
does not mean that Python `Optional` is universally invalid; it is insufficient
for this specific canonical evidence contract.

### Unavailable-Variant Invariant

`UnavailableEvidence` contains only:

```python
reason: UnavailableReason
```

It does not contain:

- a value;
- a fallback value;
- a raw source value;
- a raw record;
- a source payload;
- an explanatory free-text string;
- a timestamp;
- a provenance object;
- a mapping status.

This bounded representation preserves the reason without introducing a
retention or persistence design.

### Available-Variant Invariant

`ObservedEvidence[T]`, `DerivedEvidence[T]`, and `SimulatedEvidence[T]` each
contain only:

```python
value: T
```

They do not contain:

- `unavailable_reason`;
- a raw record;
- a source payload;
- persistence metadata;
- audit metadata.

Additional evidence lineage, if later required, must be designed separately
rather than silently added here.

### Generic Type Boundary

`T` is a Python typing parameter used to preserve the value type of the
represented field. It is an implementation and Design convenience.

It does not claim:

- runtime type enforcement;
- serialization compatibility;
- database compatibility;
- cross-language schema portability.

The planned implementation remains standard-library only.

### Case Representation and Field-Assignment Boundaries

    CASE_PYTHON_REPRESENTATION:
        NOT_DEFINED

This decision does not define which fields a future Python `Case` dataclass
contains. It does not decide:

- `source_status` field placement;
- a source-native retained-field container;
- `requested_date` handling;
- `updated_date` handling;
- `closed_date` handling;
- `canonical_status`;
- the full adapter result type.

This step defines only the reusable physical representation of field evidence.
It does not implement `Case` or the full Calgary adapter.

No particular Calgary field is newly assigned `ObservedEvidence`,
`DerivedEvidence`, `SimulatedEvidence`, or `UnavailableEvidence`, except that
prior Increment 004 choices may be restated to explain the boundary. In
particular, `created_at`, `canonical_status`, and the Decision Question 13
fields remain `DEFER_MAPPING`; none becomes a per-Case evidence assignment.

### Planned Implementation Shape

The planned standard-library structure is equivalent to:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class UnavailableReason(Enum):
    VALUE_ABSENT = "VALUE_ABSENT"
    CONCEPT_ABSENT = "CONCEPT_ABSENT"
    EVIDENCE_INDETERMINATE = "EVIDENCE_INDETERMINATE"
    TRANSFORMATION_NOT_APPLIED = "TRANSFORMATION_NOT_APPLIED"
    TRANSFORMATION_UNRESOLVED = "TRANSFORMATION_UNRESOLVED"


@dataclass(frozen=True)
class ObservedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class DerivedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class SimulatedEvidence(Generic[T]):
    value: T


@dataclass(frozen=True)
class UnavailableEvidence:
    reason: UnavailableReason


FieldEvidence = (
    ObservedEvidence[T]
    | DerivedEvidence[T]
    | SimulatedEvidence[T]
    | UnavailableEvidence
)
```

Equivalent Python 3.12 typing syntax may be considered during implementation.
This shape is planned only and is not implemented here.

### Planned Test Implications

Future structural tests should verify:

1. `UnavailableReason` contains exactly the five canonical reasons.
2. Enum values exactly equal their canonical names.
3. `ObservedEvidence` is frozen and contains only `value`.
4. `DerivedEvidence` is frozen and contains only `value`.
5. `SimulatedEvidence` is frozen and contains only `value`.
6. `UnavailableEvidence` is frozen and contains only `reason`.
7. `UnavailableEvidence` has no `value` field.
8. Available variants have no unavailable-reason field.
9. The `FieldEvidence` union contains exactly the four variants.
10. Supplied values are preserved exactly by available variants.
11. A supplied unavailable reason is preserved exactly.
12. Mutation of every variant raises `FrozenInstanceError`.

These are planned tests only. This documentation task creates or executes no
test and makes no Engineering observation about test results.

### Failure Conditions

A future implementation violates this decision if it:

- represents evidence only as value-or-`None`;
- loses the distinction among the four canonical evidence states;
- adds non-canonical evidence states;
- adds non-canonical unavailable reasons;
- treats `DEFER_MAPPING` as `UNAVAILABLE`;
- emits unavailable evidence automatically for deferred Calgary mappings;
- permits `UnavailableEvidence` to carry a field value;
- puts `unavailable_reason` on available variants;
- mutates or normalizes values inside the evidence wrapper;
- silently adds raw-record retention;
- silently adds persistence or audit metadata;
- changes Increment 004 mapping decisions.

### Revision Conditions

This physical representation should be revisited if later requirements
establish that:

- evidence lineage must be structurally bound to every field value;
- serialization or external API requirements need a different tagged form;
- cross-language schema requirements emerge;
- database representation materially constrains the model;
- performance evidence makes object-per-field representation unsuitable;
- the canonical provenance vocabulary is revised;
- Increment 002 evidence-state semantics are revised.

None of these conditions is currently claimed.

### Claim Classification

    FIELD_EVIDENCE_PHYSICAL_REPRESENTATION:
        Design choice

    UNAVAILABLE_REASON_CONTAINER:
        Design choice

    structural invariants:
        Design choices

    canonical evidence vocabulary:
        prior canonical contract definition

    Increment 004 mapping statuses:
        prior Design choices

    planned tests:
        planned tests, not Engineering observations

This documentation step produces no new Engineering observation, External
evidence, research result, or research conclusion.

### Prior-Decision Preservation

The following Increment 005 decisions remain unchanged:

    CASE_ID_PHYSICAL_REPRESENTATION:
        STRUCTURED_SOURCE_IDENTITY

    CASE_ID_PYTHON_CONTAINER:
        FROZEN_DATACLASS

    CALGARY_SOURCE_CASE_ID_ADMISSIBILITY:
        REQUIRE_PRESENT_NONBLANK_STRING

    IDENTITY_REJECTION_TRANSPORT:
        EXPLICIT_RESULT_VARIANTS

    IDENTITY_ADMISSION_API:
        CALGARY_RECORD_MAPPING_FUNCTION

    REJECTED_RAW_VALUE_RETENTION:
        NOT_DEFINED

    REJECTED_SOURCE_RECORD_RETENTION:
        NOT_DEFINED

    CASE_PYTHON_REPRESENTATION:
        NOT_DEFINED

All Increment 004 decisions remain unchanged. This physical-representation
decision authorizes no new Calgary field mapping.

## Implementation Record 005 - Field Evidence Representation

### Objective

Implement the committed physical representation for canonical field evidence
states without assigning those states to Calgary fields or implementing
`Case`.

### Files

    src/support_operations_intelligence/evidence.py
    tests/test_field_evidence.py

### Implemented

    UnavailableReason
    ObservedEvidence
    DerivedEvidence
    SimulatedEvidence
    UnavailableEvidence
    FieldEvidence

The implementation uses only standard-library `dataclass`, `Enum`, `Generic`,
and `TypeVar` concepts. The available variants are frozen dataclasses
containing only `value`; the unavailable variant is a frozen dataclass
containing only `reason`; and the union contains exactly those four variants.

    CASE_PYTHON_REPRESENTATION:
        NOT_DEFINED

    CALGARY_FIELD_EVIDENCE_ASSIGNMENTS:
        none added

    DQ12:
        NO_CANONICAL_UNAVAILABLE_ASSIGNMENTS remains unchanged

    THIRD_PARTY_DEPENDENCIES:
        none

No `DeferredEvidence`, `DEFERRED`, `NOT_MAPPED`, `RETAIN_SOURCE_NATIVE`, or
`ACCEPT_MAPPING` evidence representation is introduced. No evidence lineage,
persistence, serialization, logging, provenance storage, database
representation, `Case`, or Calgary adapter behavior is implemented.

### Expected Pre-Implementation Failure

Executed after the structural test was created and before
`support_operations_intelligence.evidence` existed:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_field_evidence.py' \
      -v

Observed discovery result:

    tests reported: 1 failed test module
    tests run: 1
    failures: 0
    errors: 1
    result: FAILED (errors=1)

Error type:

    ImportError

Underlying reason:

    ModuleNotFoundError: No module named
    'support_operations_intelligence.evidence'

This expected red result is an Engineering observation. The focused test
could not import a module that had not yet been implemented. It is test-first
evidence, not a product defect.

### Focused Post-Implementation Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_field_evidence.py' \
      -v

Observed result:

    tests run: 12
    failures: 0
    errors: 0
    result: OK

### `CaseId` Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_case_id.py' \
      -v

Observed result:

    tests run: 6
    failures: 0
    errors: 0
    result: OK

### Identity-Result Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_identity_admission_result.py' \
      -v

Observed result:

    tests run: 10
    failures: 0
    errors: 0
    result: OK

### Calgary Identity-Admission Regression Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover \
      -s tests \
      -p 'test_calgary_identity_admission.py' \
      -v

Observed result:

    tests run: 12
    failures: 0
    errors: 0
    result: OK

### Full-Suite Result

Executed command:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Observed result:

    tests run: 41
    failures: 0
    errors: 0
    result: OK

### Direct Structure Verification

The direct repository-local Python verification observed:

    reason_names = ['VALUE_ABSENT', 'CONCEPT_ABSENT',
        'EVIDENCE_INDETERMINATE', 'TRANSFORMATION_NOT_APPLIED',
        'TRANSFORMATION_UNRESOLVED']
    reason_values = ['VALUE_ABSENT', 'CONCEPT_ABSENT',
        'EVIDENCE_INDETERMINATE', 'TRANSFORMATION_NOT_APPLIED',
        'TRANSFORMATION_UNRESOLVED']
    observed_fields = ['value']
    derived_fields = ['value']
    simulated_fields = ['value']
    unavailable_fields = ['reason']
    field_evidence_origins = ['ObservedEvidence', 'DerivedEvidence',
        'SimulatedEvidence', 'UnavailableEvidence']
    observed_value = ' 001AbC-09 '
    derived_value = ' 001AbC-09 '
    simulated_value = ' 001AbC-09 '
    unavailable_reason = VALUE_ABSENT

This verifies the exact five-member enum, enum values identical to member
names, one-field shapes, exact four-variant union, lexical value preservation,
and unavailable-reason preservation.

### Direct Immutability Verification

The direct repository-local Python verification observed:

    ObservedEvidence FrozenInstanceError
    DerivedEvidence FrozenInstanceError
    SimulatedEvidence FrozenInstanceError
    UnavailableEvidence FrozenInstanceError

### Calgary and DQ12 Boundaries

The generic evidence module contains no Calgary field name or Calgary-specific
assignment. No code emits `UnavailableEvidence` for a Calgary Case or field.
The existence of the type does not convert `DEFER_MAPPING` into `UNAVAILABLE`
and does not create a canonical unavailable assignment.

Increment 004 remains:

    NO_CANONICAL_UNAVAILABLE_ASSIGNMENTS

### Claim Classification and Boundary

The committed evidence representation is a Design implementation. The
expected red result, focused result, regression results, full-suite result,
direct structure verification, and direct immutability verification are
Engineering observations.

The implemented field-evidence types conform to the currently tested
Increment 005 structural representation of the canonical provenance
vocabulary under the repository-local Python execution boundary.

This step does not establish that any Calgary field is `OBSERVED`, `DERIVED`,
`SIMULATED`, or `UNAVAILABLE`; resolve `DEFER_MAPPING`; or establish `Case`
correctness, full-adapter correctness, dataset-wide validity, ingestion
correctness, persistence correctness, provenance-lineage completeness,
portability, production readiness, External evidence, a research result, or a
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

Apart from the planned frozen-dataclass `CaseId` container, the exact Python
representation of the adapter and Case result is not selected by this
planning record.

## Current Status

Increment 005 remains:

    Status: Planned
    Completed: Not completed

No observed implementation result exists. No test is claimed to have run, and
no dependency is claimed to have been installed.

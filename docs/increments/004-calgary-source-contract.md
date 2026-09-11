# Increment 004 - Calgary Source Contract

Status: Planned

Opened: 2026-09-11

Completed: Not completed

## Objective

Using the closed Increment 003 Calgary source-evidence baseline and the
Increment 002 canonical Case contract, make explicit and falsifiable
Calgary source-admission and source-to-canonical mapping decisions,
including treatment of material non-canonical evidence and unavailable
concepts, without defining analytical metrics or claiming cross-source
portability.

## Why This Increment Exists

Increment 002 established the bounded canonical Case contract.

Increment 003 established what evidence is supportable for the local
Calgary 311 artifact and current official Calgary source metadata.

The next problem is no longer evidence discovery by default. It is a
design problem:

Given the canonical contract and the retained Calgary evidence, which
source concepts may be admitted into the canonical Case representation,
which must remain source-native, which are unavailable, and which
mapping questions must remain deferred?

This increment must make those decisions explicitly rather than allowing
field names, convenience, or later analytical goals to define the source
contract implicitly.

## Starting State

Repository:

`/data/repos/personal/support-operations-intelligence`

Starting branch:

`main`

Starting HEAD:

`3b33f9ab63ac8d35051b91df94ee9334521c62f1`

Required predecessor increments:

- Increment 002 - Canonical Case Contract
- Increment 003 - Calgary Source Evidence Validation

Increment 003 is Complete.

Its unresolved results remain evidence boundaries and must not be treated
as resolved merely because source-contract design has begun.

## Source of Truth

The controlling canonical contract for this increment is:

`docs/increments/002-canonical-case-contract.md`

The controlling Calgary evidence baseline is:

`docs/increments/003-calgary-source-evidence-validation.md`

If this increment proposes a mapping inconsistent with Increment 002, it
must explicitly classify the result as one of:

- WEAKEN
- REFINE
- EXTEND
- REJECT

and justify that classification.

No such classification is presumed at increment start.

## Scope

This increment may decide:

- whether a Calgary 311 service request satisfies canonical Case
  admission;
- the Calgary source-system namespace used by the adapter/source contract;
- whether the source-native request identifier satisfies the canonical
  source identity requirement;
- whether any source temporal concept satisfies the canonical
  `created_at` definition;
- whether and how native status evidence is represented;
- whether canonical status normalization is justified or deferred;
- how the native submission-channel concept is preserved;
- how service-type evidence is preserved without inventing a universal
  classification hierarchy;
- how responsible-department evidence is preserved without silently
  equating it with a universal ownership concept;
- how source-native update and closure timestamps are retained given
  their exclusion from the universal Case scalar contract;
- which canonical concepts are unavailable for Calgary;
- which `UNAVAILABLE` reason applies where a canonical concept is not
  supported;
- which material Calgary evidence should remain outside the minimal Case
  representation;
- what exact evidence supports each mapping, non-mapping, deferral, or
  unavailable result.

## Non-Goals

This increment will not define:

- analytical populations;
- analytical observation windows;
- closure eligibility for duration analysis;
- censoring treatment;
- temporal-precision correction;
- timezone normalization;
- request-to-closure duration metrics;
- resolution-time metrics;
- active-work time;
- handling time;
- queue time;
- waiting time;
- SLA metrics;
- denominators;
- analytical inclusion/exclusion rules;
- summary statistics;
- dashboards;
- business outcomes;
- causal claims;
- workflow decomposition;
- CaseEvent design unless a later increment independently justifies it;
- ServiceNow mappings;
- cross-source portability;
- universal governance coverage;
- production ingestion behavior;
- database schema implementation;
- adapter implementation.

## Evidence Boundary

Increment 004 consumes the evidence retained by Increment 003.

It must not silently convert Increment 003 limitations into positive
facts.

The following remain unresolved at increment start:

- local-artifact acquisition provenance;
- immutable authoritative source-version binding;
- historical licence binding for the exact local artifact;
- dataset-specific attribution wording;
- source temporal precision;
- timezone semantics;
- equivalence between request submission and canonical creation;
- exact semantic scope of `updated_date`;
- reopening behavior;
- first/latest/final closure semantics;
- final-resolution equivalence;
- censoring semantics;
- analytical duration eligibility.

A source-contract decision may account for these limitations.

It may not erase them.

## Baseline Decision Principle

The default is the minimal canonical contract.

A Calgary concept enters the canonical Case representation only when
retained evidence is sufficient to justify that mapping against the
Increment 002 definition.

A source field must not be mapped merely because:

- its name resembles a canonical field;
- it would make later analytics easier;
- the mapping is common in other systems;
- the value is populated;
- the value parses successfully;
- the source UI displays it as a date or timestamp.

When evidence does not justify a canonical mapping, the preferred result
is one of:

- retain the evidence source-natively;
- mark the canonical concept unavailable with a justified reason;
- defer the mapping;
- reject the mapping.

The increment must prefer explicit absence over fabricated equivalence.

## Decision Record Method

For each material source-contract question, record:

### Decision Question

What exact source-to-contract question is being decided?

### Canonical Requirement

What does Increment 002 require?

### Calgary Evidence

What retained Increment 003 evidence bears directly on the decision?

### Competing Interpretations

What plausible mappings or non-mappings remain?

### Decision

Use a bounded result such as:

- ACCEPT_MAPPING
- REJECT_MAPPING
- DEFER_MAPPING
- RETAIN_SOURCE_NATIVE
- CANONICAL_CONCEPT_UNAVAILABLE
- ADMIT_CASE
- REJECT_CASE_ADMISSION

These are decision-record labels for this increment, not universal
ontology.

### Justification

Why is the decision supported?

### Counterevidence / Limitation

What evidence weakens or limits the decision?

### Claim Classification

Classify the result appropriately, normally as:

- Design choice
- Engineering observation
- External evidence
- Research hypothesis

Do not label a design choice as an external fact.

### Falsification Condition

What future evidence would require revisiting this decision?

## Decision Records

## Decision Question 1 - Case Admission

### Decision Question

Does a Calgary 311 service request satisfy all Increment 002 Case
admission conditions?

### Canonical Requirement

A canonical Case represents one independently identifiable, source-native
unit of operational work or operational matter whose identity and meaning
exist independently of individual events or observations and for which an
operational disposition or outcome can meaningfully be considered.

The five required admission conditions are:

- source-native entity;
- operational-work semantics;
- independent meaning;
- bounded identity;
- disposition semantics.

Qualification is semantic. Identity alone is insufficient for Case
qualification.

### Calgary Evidence

Increment 003 retained the following evidence relevant to admission:

- the current official dataset identity is `311 Service Requests`;
- the current official description identifies public service requests
  submitted through 311;
- current official field metadata describes `service_request_id` as the
  unique identifier for an individual request;
- current official field metadata describes the type of service requested,
  the department responsible for the request, the current status of the
  request, the most recent date the request was updated, and the date the
  request was closed;
- the local artifact contains 7,474,403 observed logical data rows;
- every observed row has a nonblank raw `service_request_id`;
- the artifact contains 7,474,403 distinct raw identifiers under the exact
  comparison used by Increment 003;
- every observed row has a nonblank raw `status_description`;
- `updated_date` is nonblank in 7,396,574 observed rows and `closed_date` is
  nonblank in 7,396,056 observed rows.

These are the retained Increment 003 observations and external evidence.
They do not establish new empirical results or canonical field mappings.

### Competing Interpretations

**Interpretation A:** The source object is an independently meaningful
service request that constitutes an operational work item.

**Interpretation B:** The local row is merely an observation or snapshot
record about service-related activity and does not represent the operational
work item itself.

### Decision

`ADMIT_CASE`

The Calgary 311 service-request entity satisfies the bounded Increment 002
Case-admission definition based on the retained evidence.

This decision does not state that every local row is independently verified
as an authoritative historical source entity and does not establish
cross-source portability.

### Justification

**Source-native entity: `SUPPORTED`.** The official dataset and field
semantics identify an individual service request as the source object. The
local one-row-per-distinct-nonblank-identifier evidence is consistent with
that object boundary, although uniqueness alone would not be sufficient.

**Operational-work semantics: `SUPPORTED`.** The retained evidence describes
public service requests submitted through 311, the service requested, the
department responsible, current request status, request updates, and request
closure. Together these semantics establish an operational request handled as
a unit of operational work or matter without implying assignment, queue, or
handling semantics.

**Independent meaning: `SUPPORTED`.** The request itself is the source object.
Submission, service type, organizational responsibility, status, updating,
and closure are attributes or conditions of that request rather than the
request being reducible to any one timestamp, event, or observation. CaseEvent
evidence is not required for admission.

**Bounded identity: `SUPPORTED`.** The official semantics identify a unique
identifier for an individual request, and the local evidence observes a
nonblank distinct raw identifier for every row. This establishes a bounded
source-native request identity for admission without deciding the canonical
source identity mapping.

**Disposition semantics: `SUPPORTED`.** The official semantics establish that
a current status, updating, and closure can meaningfully apply to the request.
Complete lifecycle reconstruction, monotonic progression, reopening rules,
and final-resolution semantics are not required for admission.

All five required conditions are supported. Missing optional canonical fields
do not defeat admission; they restrict later mapping or analytical eligibility
where applicable.

### Counterevidence / Limitation

The strongest counterargument is that the local row could be interpreted as
merely a current snapshot or observation record about service-related
activity rather than an independently meaningful operational-work entity.

`COUNTERARGUMENT_RESULT: DOES_NOT_SURVIVE_CURRENT_EVIDENCE`

The official evidence identifies the referent as an individual service
request and describes submission, requested service, organizational
responsibility, current status, updating, and closure as properties or
conditions of that request. Even if the row is a snapshot representation, the
represented entity is the operational request rather than an isolated event
or anonymous observation.

Admission does not resolve:

- local acquisition provenance;
- immutable authoritative version binding;
- identifier immutability across all source history;
- identifier reuse outside the observed artifact;
- `source_case_id` mapping;
- `source_system`;
- `requested_date -> created_at`;
- `status_description -> source_status`;
- `canonical_status`;
- reopening behavior;
- final closure semantics;
- final-resolution equivalence;
- temporal precision;
- timezone;
- duration eligibility;
- workflow decomposition.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    Engineering observations retained in Increment 003
    External evidence retained in Increment 003

`ADMIT_CASE` is a source-contract design choice supported by retained evidence;
it is not itself external evidence.

### Falsification Condition

`ADMIT_CASE` must be revisited if credible future evidence shows that:

- the source row represents an event, observation, communication, or aggregate
  rather than an individual service request;
- `service_request_id` identifies a record representation rather than the
  underlying individual request;
- the request does not have independent operational meaning;
- the request is not actually treated as a unit of operational work or matter;
- operational disposition or outcome cannot meaningfully apply to the request;
- later source evidence materially contradicts the official semantics relied
  upon here.

Future evidence that merely adds optional fields does not require revisiting
admission.

`INCREMENT_002_ADMISSION_FALSIFICATION: none`

Successful application of the Increment 002 admission definition to Calgary
does not validate cross-source portability.

Decision Questions 2 through 13 remain undecided. No canonical field mapping,
`source_system` value, `UNAVAILABLE` reason, analytical eligibility rule, or
portability conclusion is introduced by this decision.

## Planned Decision Questions

The increment must consider, without presuming answers, the following.

### 1. Case Admission

Does a Calgary 311 service request satisfy all Increment 002 Case
admission conditions?

Consider:

- source-native entity;
- operational work semantics;
- independent meaning;
- bounded identity;
- disposition, progression, or outcome semantics.

Admission must be justified separately from field mapping.

### 2. Source-System Namespace

What stable canonical source-system namespace should identify this source?

This is a design choice.

It must not be confused with Calgary's native field named `source`, which
Increment 003 established means the channel used to submit the request.

### 3. Source Case Identity

Does `service_request_id` satisfy the Increment 002 requirement for
`source_case_id`?

Evidence must address source-native identity semantics, not merely
uniqueness in one local artifact.

### 4. Canonical `created_at`

Does Calgary `requested_date`, defined by the source as the date the
request was submitted, satisfy Increment 002's canonical `created_at`
definition?

The decision must address the remaining distinction between submission
and source-supported creation.

Temporal precision and timezone must not be invented.

### 5. Native Status

Should `status_description`, defined by the source as the current status
of the request, be preserved as `source_status`?

Do not infer monotonicity, terminal-state behavior, or reopening rules.

### 6. Canonical Status

Is a `canonical_status` normalization justified by the current evidence?

Possible outcomes include:

- justified;
- not justified;
- deferred.

Do not normalize merely for convenience.

### 7. Submission Channel

How should Calgary's native `source` field, defined as the channel used
to submit the request, be preserved?

Do not confuse:

submission channel

with:

source system
provenance source
ingestion source.

### 8. Service Type

How should `service_name`, defined as the type of service requested, be
preserved?

Do not invent:

- universal category;
- hierarchy;
- parent/child classification;
- taxonomy depth.

### 9. Responsible Department

How should `agency_responsible`, defined as the department responsible
for the request, be preserved?

Do not silently equate it with:

- owning_group;
- assignment group;
- resolver group;
- current assignee;
- universal responsibility concept.

### 10. Updated Timestamp

How should `updated_date` be retained given that:

- Calgary describes it as the most recent date the request was updated;
- the qualifying update semantics remain unresolved;
- Increment 002 rejected generic `updated_at` as a universal Case scalar?

The answer need not be a canonical mapping.

### 11. Closure Timestamp

How should `closed_date` be retained given that:

- Calgary describes it as the date the request was closed;
- first/latest/final closure semantics remain unresolved;
- reopening semantics remain unresolved;
- closure is not established as final resolution;
- Increment 002 rejected universal `closed_at`?

The answer need not be a canonical mapping.

### 12. Unavailable Canonical Concepts

Which canonical concepts are unsupported for Calgary?

For each unavailable concept, determine which Increment 002 reason is
justified:

- VALUE_ABSENT
- CONCEPT_ABSENT
- EVIDENCE_INDETERMINATE
- TRANSFORMATION_NOT_APPLIED
- TRANSFORMATION_UNRESOLVED

Do not use `UNAVAILABLE` as a generic synonym for null.

### 13. Material Source-Native Evidence Outside Case

Which Calgary evidence should remain available outside the minimal Case
representation?

The contract should preserve material evidence without forcing every
source field into the canonical Case.

## Assumptions

- Increment 002 remains the controlling canonical Case contract.
- Increment 003 remains the controlling Calgary evidence baseline.
- Current official metadata may not describe historical source state at
  local-artifact acquisition time.
- Local-artifact provenance remains unconfirmed.
- Source-specific fields need not become universal Case fields.
- Missing optional canonical concepts do not invalidate an otherwise
  admissible Case.
- Analytical usefulness is not sufficient justification for canonical
  mapping.

## Threat Model

The primary risks in this increment are semantic overreach and
convenience-driven mapping.

Specific threats include:

- mapping by field-name similarity;
- treating empirical population behavior as source semantics;
- treating current official metadata as historical acquisition evidence;
- confusing submission channel with source-system identity;
- treating responsible department as universal ownership;
- treating closure as final resolution;
- treating update time as lifecycle transition time;
- using timestamp display format as precision evidence;
- inventing canonical classifications from source-specific labels;
- using future analytical goals to force unsupported mappings;
- treating one Calgary mapping as proof of cross-source portability.

## Strong Baseline

The strongest baseline is not "map every available field."

The baseline is:

- admit only what satisfies the canonical contract;
- preserve source-native evidence without unnecessary normalization;
- mark unsupported canonical concepts explicitly unavailable where
  justified;
- defer mappings when evidence is insufficient;
- retain the original evidence and limitations.

A richer mapping must outperform this baseline in semantic justification,
not merely convenience.

## Planned Work Sequence

The intended sequence is:

1. Re-read Increment 002 and the closed Increment 003 evidence baseline.
2. Decide Case admission.
3. Decide source-system namespace and source identity mapping.
4. Decide temporal and status mappings.
5. Decide treatment of submission channel, service type, and responsible
   department.
6. Decide treatment of update and closure timestamps outside the
   universal Case scalar contract.
7. Determine justified unavailable concepts and reasons.
8. Identify material source-native evidence retained outside minimal
   Case.
9. Review every decision against Increment 002.
10. Review claim boundaries and falsification conditions.
11. Review completion criteria before closure.

This sequence may be refined if retained evidence requires it, but
Increment 004 must not silently expand into analytical-contract work.

## Planned Tests / Verification

This increment is primarily a design-contract increment.

Verification should include:

- every mapping cites the controlling canonical requirement;
- every mapping cites relevant retained Calgary evidence;
- every non-mapping or deferral gives a reason;
- every `UNAVAILABLE` result uses a justified Increment 002 reason;
- source-system identity is not confused with the native `source` field;
- no universal `updated_at` or `closed_at` scalar is introduced without
  explicitly revisiting Increment 002;
- no timestamp precision or timezone is invented;
- no duration eligibility is established;
- no workflow decomposition is claimed;
- no portability claim is introduced;
- no source-specific concept is silently promoted into the universal
  ontology.

Planned verification is not an observed result.

## Failure Criteria

The increment is not ready to complete if any of the following occurs:

- Case admission is asserted without checking every Increment 002
  admission condition.
- A canonical mapping is justified only by field-name similarity.
- `source` is treated as `source_system`.
- `requested_date` is mapped to `created_at` without addressing the
  submission-versus-creation distinction.
- `updated_date` is promoted to a universal Case timestamp without
  explicitly revisiting Increment 002.
- `closed_date` is promoted to final resolution or universal
  `Case.closed_at` without sufficient evidence.
- `status_description` is normalized without explicit justification.
- `service_name` is turned into a universal classification hierarchy
  without evidence.
- `agency_responsible` is equated with universal ownership without
  evidence.
- `UNAVAILABLE` reasons are assigned without justification.
- unresolved provenance, precision, timezone, or lifecycle semantics are
  silently converted into positive facts.
- analytical eligibility or duration definitions are introduced.
- workflow decomposition is claimed.
- Calgary is presented as validating cross-source portability.
- a design choice is presented as external evidence.
- the increment closes without falsification conditions for material
  mapping decisions.

## Completion Criteria

Increment 004 is complete only when:

1. Calgary Case admission has an explicit decision and justification.
2. The source-system namespace has an explicit design decision.
3. Source identity mapping has an explicit decision.
4. `requested_date` treatment has an explicit decision.
5. `status_description` treatment has an explicit decision.
6. `canonical_status` normalization has an explicit decision or explicit
   deferral.
7. Submission-channel treatment has an explicit decision.
8. `service_name` treatment has an explicit decision.
9. `agency_responsible` treatment has an explicit decision.
10. `updated_date` treatment has an explicit decision.
11. `closed_date` treatment has an explicit decision.
12. Unsupported canonical concepts and justified `UNAVAILABLE` reasons
    are recorded.
13. Material source-native evidence retained outside minimal Case is
    identified.
14. Every material decision includes evidence, limitations, and a
    falsification condition.
15. Increment 002 compatibility or any justified falsification outcome
    is explicitly recorded.
16. Analytical-contract work remains deferred.
17. Cross-source portability remains unvalidated unless independent
    evidence unexpectedly justifies a stronger result.
18. A completion review finds no unsupported canonical mapping or
    analytical claim.

## Claim Discipline

Expected claim types in this increment include:

- Design choice:
  source-system namespace, source-to-canonical mappings, deferrals,
  unavailable handling.

- Engineering observation:
  only when referring to already retained local observations from
  Increment 003.

- External evidence:
  only when referring to already retained official Calgary evidence from
  Increment 003.

- Research hypothesis:
  any claim that a mapping pattern may generalize beyond Calgary.

Do not classify one implementation decision as a research conclusion.

## Increment 002 Relationship

Increment 004 begins with no presumed falsification of Increment 002.

Possible outcomes remain:

- no conflict;
- WEAKEN;
- REFINE;
- EXTEND;
- REJECT.

Any non-null falsification outcome requires explicit evidence and
argument.

Portability remains a research hypothesis.

## Reproducibility Notes

The increment must cite retained predecessor evidence rather than
re-running empirical scans by default.

If new evidence becomes necessary for a specific mapping decision:

- stop the design decision;
- identify the exact missing evidence;
- determine whether gathering it belongs in this increment or a separate
  evidence increment;
- preserve the reason for reopening empirical work.

Do not quietly add exploratory evidence after a mapping decision has
already been made.

## Threats to Validity

Known threats include:

- current Calgary metadata may differ from metadata at local-artifact
  acquisition time;
- local acquisition provenance is unavailable;
- timestamp precision is unresolved;
- timezone semantics are unresolved;
- closure/reopening semantics are incomplete;
- Calgary exposes source-specific concepts that may not generalize;
- the canonical Case contract itself remains provisional and falsifiable;
- a single Calgary mapping cannot validate cross-source portability.

## Expected Artifact

The intended artifact is a bounded Calgary source contract that states:

- whether Calgary requests are admitted as Cases;
- which source evidence maps into canonical concepts;
- which evidence remains source-native;
- which canonical concepts are unavailable;
- which decisions remain deferred;
- why each decision was made;
- what future evidence would falsify each material decision.

It is not an analytics specification and not a portability proof.

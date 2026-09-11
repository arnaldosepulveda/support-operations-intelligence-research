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

## Decision Question 2 - Source-System Namespace

### Decision Question

What stable canonical `source_system` namespace should identify the Calgary
311 source represented by this source contract?

### Canonical Requirement

Increment 002 defines:

`source_system`:

    Identity namespace for the originating source or system.

`source_case_id`:

    Native source identifier within the source_system namespace.

The authoritative source-native identity is:

    (source_system, source_case_id)

The tuple must be unique. Repeated ingestion of the same
`(source_system, source_case_id)` must resolve to the same canonical Case, and
native identifiers from different source systems may collide without causing
canonical identity collisions.

Increment 002 does not require `source_system` to be an official source field,
a publication dataset identifier, a local artifact identifier, or a known
backend-product name.

### Calgary Evidence

Increment 003 retained the following relevant evidence:

- the current official dataset identity is `311 Service Requests`;
- the retained attribution metadata is `The City of Calgary`;
- the current official description identifies public service requests
  submitted through 311;
- the current published dataset identifier is `iahh-g8bj`;
- Calgary's native field named `source` means the channel used to submit the
  request;
- the local CSV has its own artifact path, byte size, and SHA-256 identity;
- Calgary's underlying production application, database, vendor, and backend
  were not established.

The retained evidence therefore supports a City of Calgary 311
service-request source domain while preserving the distinction between that
domain, its publication dataset, its local artifact, and its submission
channel.

### Competing Interpretations

**Candidate A: `city_of_calgary_311` — `ACCEPTABLE`.** It identifies the
jurisdiction and 311 domain clearly, remains independent of artifacts and
publication versions, and does not assert a backend product. It could be too
broad if later evidence establishes multiple independent Calgary 311 identity
domains.

**Candidate B: `calgary_311` — `WEAKER`.** It is concise and backend-neutral,
but it is less globally explicit because it omits the City of Calgary source
boundary.

**Candidate C: `calgary_311_service_requests` — `ACCEPTABLE`.** It explicitly
names the admitted request domain, but it is less globally precise than
Candidate A and binds the namespace more closely to the current object-domain
description.

**Candidate D: `calgary_open_data_311_service_requests` — `REJECT`.** It binds
identity to the publication and distribution layer rather than the evidenced
operational request source domain.

**Candidate E: `iahh-g8bj` — `REJECT`.** It is useful current published dataset
identity, but it is opaque and is not justified as the operational source
identity namespace.

**Candidate F: `calgary_open_data_iahh_g8bj` — `REJECT`.** It makes the
publication dataset identity more reconstructable but still conflates
publication provenance with canonical operational source identity.

Candidates A, B, and C identify the evidenced Calgary 311 operational request
domain. Candidates D, E, and F instead bind identity to the publication or
distribution layer.

### Decision

`ACCEPT_MAPPING`

`source_system`:

    city_of_calgary_311

The canonical `source_system` field for this Calgary source contract is
assigned the project-defined namespace literal `city_of_calgary_311`.

This is a canonical identity-namespace design choice. It is not an observed
Calgary source field value.

### Justification

**STABILITY.** `city_of_calgary_311` survives ordinary dataset refreshes,
exports, and local snapshots.

**GLOBAL_CLARITY.** It identifies the City of Calgary and the 311 domain
explicitly enough to distinguish this source boundary from unrelated 311
systems.

**SEMANTIC_HONESTY.** It does not claim knowledge of Calgary's underlying CRM,
database, vendor, or operational software.

**SOURCE_NATIVE_ALIGNMENT.** It corresponds to the retained City of Calgary
311 service-request domain.

**ARTIFACT_INDEPENDENCE.** It does not depend on the CSV path, SHA-256, byte
size, row count, or any specific local copy.

**VERSION_INDEPENDENCE.** It does not require renaming for ordinary source or
publication updates.

**CHANNEL_SEPARATION.** It remains distinct from Calgary's native `source`
field, which represents the submission channel.

**RECONSTRUCTABILITY.** A later reviewer can reconstruct the namespace from
the retained City of Calgary, 311, and service-request evidence together with
the stated identity-namespace design rule.

`iahh-g8bj` and Calgary Open Data identifiers remain useful publication
identifiers, but the retained evidence does not justify using them as the
canonical operational identity namespace.

### Counterevidence / Limitation

The strongest counterargument is that `city_of_calgary_311` may be too broad
if City of Calgary 311 actually contains multiple independent operational
systems or identifier domains.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

The limitation remains a revision risk, but the retained evidence supports
one admitted Calgary 311 service-request domain for this source contract and
does not establish multiple underlying identity domains.

The decision also preserves these limitations:

- the underlying production application remains unknown;
- multiple hidden identity domains have not been ruled out across all source
  history;
- local artifact provenance remains unresolved;
- the current published dataset identifier does not prove operational-system
  identity.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003

`city_of_calgary_311` is neither external evidence nor an engineering
observation or research conclusion. It is the project-defined canonical
identity namespace selected from the retained evidence.

### Falsification Condition

This namespace decision must be revisited if credible future evidence shows
that:

- multiple independent Calgary 311 identifier domains exist;
- native identifiers collide across independently meaningful Calgary 311
  systems;
- the published dataset combines operational sources that should not share
  one identity namespace;
- authoritative evidence contradicts the current source boundary;
- materially different source systems currently collapsed together must be
  distinguished.

New rows, metadata updates, a refreshed CSV, a new local artifact hash, and
ordinary publication refreshes do not by themselves falsify this namespace.

The four identity concepts remain distinct:

- canonical `source_system`: `city_of_calgary_311`;
- native Calgary `source`: submission channel;
- local CSV identity: artifact identity only;
- `iahh-g8bj`: current published dataset identity.

`INCREMENT_002_SOURCE_SYSTEM_FALSIFICATION: none`

Choosing a Calgary-specific namespace does not validate cross-source
portability.

Decision Question 3 remains undecided: this decision does not establish
`service_request_id -> source_case_id`. The treatment of `created_at`,
`source_status`, `canonical_status`, submission-channel representation,
service type, responsible department, `updated_date`, `closed_date`,
unavailable canonical concepts, and source-native evidence outside the
minimal Case also remains undecided. No analytical eligibility rule is
introduced.

## Decision Question 3 - Source Case Identity

### Decision Question

Can Calgary `service_request_id` be justified as canonical `source_case_id`
within the committed `source_system = city_of_calgary_311` namespace?

### Canonical Requirement

Increment 002 defines `source_case_id` as:

    Native source identifier within the source_system namespace.

The authoritative source-native identity is:

    (source_system, source_case_id)

The relevant identity invariants are:

- `(source_system, source_case_id)` is authoritative source-native identity;
- the tuple must be unique;
- one qualifying source-native work item maps to exactly one canonical Case,
  and one canonical Case maps to exactly one qualifying source-native work
  item;
- repeated ingestion of the same tuple must resolve to the same Case;
- native identifiers may collide across different `source_system` namespaces
  without causing canonical identity collisions;
- cross-source relationships do not merge Case identity;
- entity resolution and higher-level grouping remain separate concerns.

### Calgary Evidence

Current official Calgary metadata describes `service_request_id` as:

> The unique identifier for an individual request.

Increment 003 retained these local observations:

- logical data rows: 7,474,403;
- empty or whitespace-only raw `service_request_id` values: 0;
- distinct raw `service_request_id` values: 7,474,403;
- duplicate raw `service_request_id` rows: 0.

The committed predecessor decisions are:

- Decision Question 1: `ADMIT_CASE`;
- Decision Question 2: `source_system = city_of_calgary_311`.

These are retained evidence and predecessor design decisions. No new
empirical result is introduced here.

### Competing Interpretations

**Interpretation A — `ACCEPT_MAPPING`.** `service_request_id` identifies the
admitted individual Calgary request within the `city_of_calgary_311`
namespace. Review classification: `STRONGEST`.

**Interpretation B — `DEFER_MAPPING`.** Current evidence is suggestive, but
uncertainty about historical immutability, non-reuse, or continuity is treated
as too strong to accept the mapping yet. Review classification: `PLAUSIBLE`.

**Interpretation C — `REJECT_MAPPING`.** `service_request_id` identifies only
a record representation or does not reliably distinguish individual Calgary
requests. Review classification: `UNSUPPORTED`.

### Decision

`ACCEPT_MAPPING`

    service_request_id -> source_case_id

`AUTHORITATIVE_SOURCE_IDENTITY`:

    (city_of_calgary_311, service_request_id)

This notation defines the source-contract identity rule. It does not claim
that ingestion logic, idempotent processing, database keys, or canonical
`case_id` generation have been implemented.

### Justification

**SOURCE_NATIVE_IDENTITY_SEMANTICS: `SUPPORTED`.** Official Calgary metadata
states that `service_request_id` is the unique identifier for an individual
request.

**NONBLANK_OBSERVED_POPULATION: `SUPPORTED`.** All 7,474,403 retained local
rows contain a nonblank raw identifier.

**OBSERVED_LOCAL_UNIQUENESS: `SUPPORTED`.** The retained artifact contains
7,474,403 distinct raw identifiers and zero duplicate raw identifiers under
exact-string comparison.

**ENTITY_ALIGNMENT: `SUPPORTED`.** `ADMIT_CASE` established that the
individual Calgary service request is the operational entity, and official
metadata describes `service_request_id` as identifying that individual
request.

**NAMESPACE_COMPATIBILITY: `SUPPORTED`.** `city_of_calgary_311` identifies the
request source domain, while `service_request_id` identifies the individual
request within it.

**REPEAT_INGESTION_COMPATIBILITY: `SUPPORTED_AS_CONTRACT_REQUIREMENT`.** The
mapping is semantically compatible with the Increment 002 requirement that
repeated occurrences of the same authoritative source identity resolve to the
same Case.

Repeat ingestion has not been empirically tested.

### Counterevidence / Limitation

The strongest counterargument is that current official semantics and local
uniqueness do not prove identifier immutability, historical non-reuse, or
continuity across every past or future Calgary source version.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_MAPPING`

The current evidence is sufficient for this bounded source contract because
the official source semantics identify an individual request and the local
evidence corroborates complete nonblank population and uniqueness.

The following remain unresolved and must not be promoted into observed facts:

- identifier immutability across all Calgary history;
- historical non-reuse;
- continuity across every future source migration;
- exact local-artifact provenance;
- immutable remote-version binding;
- implemented repeat-ingestion behavior.

`SOURCE_CASE_ID_MAPPING` asks which source-native identifier this contract
uses for the admitted request. `PROVENANCE_CONFIDENCE` asks whether the
complete historical acquisition chain of the local artifact is established.
Unresolved provenance neither proves nor automatically defeats the mapping.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003

The official description of `service_request_id` is external evidence. The
mapping `service_request_id -> source_case_id` is a design choice supported by
that evidence; the mapping itself is not external evidence or a research
conclusion.

### Falsification Condition

This mapping must be revisited if credible future evidence shows that:

- `service_request_id` identifies a record representation rather than the
  individual request;
- `service_request_id` is reused for distinct Calgary requests inside the
  `city_of_calgary_311` namespace;
- distinct requests collide on the same identifier inside the namespace;
- a source migration materially changes identifier semantics;
- one request legitimately receives multiple unrelated `service_request_id`
  values without a stable identity relation;
- `service_request_id` is not stable enough to satisfy repeat-ingestion
  identity.

Ordinary new identifiers, new rows, refreshed exports, changed artifact
hashes, and routine metadata updates do not automatically falsify the mapping.

The source identifier is preserved lexically. This decision does not choose
or infer UUID or integer representation, a database primary-key type,
normalization, case folding, trimming, surrogate generation, or parsing
beyond preservation of the source value. Exact physical representation
remains deferred.

`INCREMENT_002_SOURCE_CASE_ID_FALSIFICATION: none`

Successful Calgary identity mapping does not validate cross-source
portability.

Decision Question 4 remains undecided: this decision does not establish
`requested_date -> created_at`. The treatment of
`status_description -> source_status`, `canonical_status`, submission-channel
representation, service type, responsible department, `updated_date`,
`closed_date`, unavailable canonical concepts, and material source-native
evidence outside the minimal Case also remains undecided. No analytical
eligibility rule is introduced.

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

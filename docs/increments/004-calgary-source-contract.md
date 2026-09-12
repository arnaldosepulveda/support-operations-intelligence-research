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

## Decision Question 4 - Canonical `created_at`

### Decision Question

Does Calgary `requested_date` satisfy the Increment 002 canonical
`created_at` definition?

### Canonical Requirement

`Case.created_at` is an optional canonical lifecycle concept representing the
source-supported creation boundary of the source-native operational work
item.

It may be `OBSERVED` or established through a semantically justified
deterministic derivation. It does not represent issue onset by default,
ingestion time, first-seen time, retrieval time, or merely the earliest
available timestamp. Its representation must not imply temporal precision
greater than the source evidence supports. It may remain unavailable, and its
presence or absence does not itself establish analytical eligibility.

### Calgary Evidence

Increment 003 retained the following evidence for `requested_date`:

- official description: "The date the request was submitted.";
- official type: `calendar_date`;
- official format metadata: `date_ymd_time`;
- logical data rows: 7,474,403;
- blank values: 0;
- parseable values: 7,474,403;
- unparseable values: 0;
- minimum parsed value: `2010-01-25 00:00:00`;
- maximum parsed value: `2026-09-08 00:00:00`;
- exact-midnight values: 3,603,999;
- non-midnight values: 3,870,404;
- exact-midnight percentage of parseable values: 48.217884%.

The retained evidence boundaries are:

- `REQUESTED_DATE_CREATION_TIME_EQUIVALENCE_UNRESOLVED`;
- `SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED`;
- `TIMEZONE_SEMANTICS_UNRESOLVED`.

The evidence distinguishes request submission from source-native creation,
issue onset, project ingestion, and observation or extract time. This decision
concerns only whether submission is sufficiently established as source-native
creation of the admitted Calgary request.

### Competing Interpretations

**Interpretation A — `ACCEPT_MAPPING`.** Map `requested_date` to `created_at`
because the admitted entity is a submitted service request and the field is
directly associated with submission. Review classification: `PLAUSIBLE`.

**Interpretation B — `DEFER_MAPPING`.** Calgary establishes request
submission, but retained evidence does not establish submission as the
source-native request creation boundary. Review classification: `STRONGEST`.

**Interpretation C — `REJECT_MAPPING`.** Treat `requested_date` as an
established different lifecycle boundary that must not represent creation.
Review classification: `UNSUPPORTED`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat current Calgary
evidence as insufficient to populate canonical `created_at` under this source
contract. Review classification: `PLAUSIBLE`.

### Decision

`DEFER_MAPPING`

No mapping from `requested_date` to `created_at` is established at this stage.
The reason is not poor population or parseability. Submission-to-creation
semantic equivalence remains unestablished.

Deferral leaves the candidate mapping open to stronger future semantic
evidence. This decision does not mark the canonical concept unavailable and
does not assign an unavailability reason.

### Justification

**SOURCE_SEMANTIC_SUPPORT: `PARTIALLY_SUPPORTED`.** Calgary directly
establishes request submission, making `requested_date` a plausible creation
candidate, but it does not explicitly define submission as creation of the
source-native request.

**ENTITY_ALIGNMENT: `SUPPORTED`.** `requested_date` clearly applies to the
admitted Calgary service request.

**SUBMISSION_CREATION_EQUIVALENCE: `INDETERMINATE`.** Retained evidence
establishes neither that the request cannot exist before submission nor that
Calgary defines submission and creation as distinct boundaries. The canonical
creation requirement is therefore not sufficiently established for
`ACCEPT_MAPPING`.

Complete population and parseability do not substitute for semantic
equivalence.

### Counterevidence / Limitation

The strongest argument for acceptance is that the admitted source entity is
specifically a submitted service request and `requested_date` is directly
associated with submission, so submission may be the source-domain point at
which the request comes into existence.

The strongest argument against acceptance is that Increment 002 requires a
source-supported creation boundary, while Calgary documents only submission,
and Increment 003 explicitly preserved
`REQUESTED_DATE_CREATION_TIME_EQUIVALENCE_UNRESOLVED`.

For the chosen deferral:

`COUNTERARGUMENT`: Because the source entity is the submitted request,
submission may already be the most semantically honest source-native creation
boundary.

`COUNTERARGUMENT_RESULT: LEAVES_DECISION_INDETERMINATE`

The argument makes `ACCEPT_MAPPING` plausible, but it does not provide the
missing source-supported submission-to-creation equivalence required by the
canonical contract.

### Precision Boundary

`SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED`

Lexical seconds do not establish second-level source precision. Approximately
48% exact-midnight representation does not establish date-only source capture,
and midnight representation does not establish defaulting, imputation,
rounding, truncation, or synthetic timestamps. Precision treatment remains
undecided.

### Timezone Boundary

`TIMEZONE_SEMANTICS_UNRESOLVED`

This decision does not infer UTC, Calgary local time, Mountain Time, MST, MDT,
daylight-saving behavior, or offset behavior.

### Analytical Boundary

`DEFER_MAPPING` establishes nothing about request-to-closure duration,
resolution time, observation windows, censoring, SLA eligibility, active work,
handling time, queue time, or waiting time. The absence of a `created_at`
mapping is a source-contract result, not an analytical conclusion.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003

"The date the request was submitted" is external evidence. `DEFER_MAPPING` is
the design choice supported by the current evidence boundary.

### Falsification / Revision Condition

This deferral should be revisited if credible future evidence:

- explicitly states that request submission is source-native request creation;
- explicitly defines creation separately from submission;
- establishes a stable pre-submission request entity;
- establishes `requested_date` as the source creation timestamp;
- shows that a source migration changed `requested_date` semantics;
- establishes that `requested_date` derives from another lifecycle boundary;
- establishes synthetic or transformed timestamp behavior materially relevant
  to creation semantics.

Routine new rows, refreshed exports, or artifact-hash changes are not semantic
falsification.

`DEFER_MAPPING` is not equivalent to `CANONICAL_CONCEPT_UNAVAILABLE`. A
plausible source candidate exists, but the semantic equivalence needed for
canonical mapping is not established. No unavailability reason is assigned in
this decision; unavailable concepts and reasons remain Decision Question 12
territory.

`INCREMENT_002_CREATED_AT_FALSIFICATION: none`

Failure to establish a Calgary `created_at` mapping does not falsify an
optional canonical concept. Cross-source portability remains unvalidated.

Decision Question 5 remains undecided: this decision does not establish a
mapping from `status_description` to `source_status`. The treatment of
`canonical_status`, submission-channel representation, service type,
responsible department, `updated_date`, `closed_date`, unavailable canonical
concepts, and material source-native evidence outside the minimal Case also
remains undecided.

## Decision Question 5 - Source Status

### Decision Question

Can Calgary `status_description` be justified as canonical `source_status`?

### Canonical Requirement

Increment 002 defines `source_status` as the Case-level lifecycle status
expressed in the originating source's native vocabulary.

It may be:

- `OBSERVED` directly from Case or snapshot evidence;
- `DERIVED` deterministically from richer source evidence at a defined
  observation boundary.

`source_status` retains source-native lifecycle semantics. It does not require
canonical normalization, does not imply monotonic lifecycle progression, and
does not replace event history. It does not require known reopening behavior
and does not imply terminality or final resolution.

`canonical_status` is an optional normalized lifecycle interpretation that
requires separate justification.

### Calgary Evidence

Increment 003 retained the following official field evidence:

- field: `status_description`;
- type: `text`;
- description: "The current status of the request (e.g. open, closed)."

Increment 003 also retained the following local population evidence:

- logical data rows: 7,474,403;
- blank `status_description` values: 0;
- whitespace-only `status_description` values: 0.

No distinct-value inspection was performed for this decision.

Increment 003 did not establish:

- the complete status vocabulary;
- transition rules;
- lifecycle monotonicity;
- reopening behavior;
- terminal-state semantics;
- final-resolution equivalence;
- canonical normalization rules.

### Competing Interpretations

**Interpretation A — `ACCEPT_MAPPING`.** Preserve
`status_description -> source_status` as the admitted request's source-native
current-status representation. Review classification: `STRONGEST`.

**Interpretation B — `DEFER_MAPPING`.** Current-status semantics are
promising, but unresolved observation timing or historical binding might
justify deferral. Review classification: `PLAUSIBLE`.

**Interpretation C — `REJECT_MAPPING`.** Treat `status_description` as not
actually representing a source-native request-status concept. Review
classification: `UNSUPPORTED`.

Competing-decision summary:

    ACCEPT_MAPPING: STRONGEST
    DEFER_MAPPING: PLAUSIBLE
    REJECT_MAPPING: UNSUPPORTED

### Decision

`ACCEPT_MAPPING`

    status_description -> source_status

The Calgary source-native current-status value represented in
`status_description` is preserved as `source_status` for the admitted Case.

This mapping does not mean:

- `canonical_status`;
- historical status sequence;
- most recent transition event;
- terminal status;
- final disposition;
- final resolution;
- proof that a closure-like status cannot later reopen.

### Justification

**SOURCE_NATIVE_STATUS_SEMANTICS: `SUPPORTED`.** Calgary explicitly defines
`status_description` as the current status of the request.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes the already admitted
Calgary service request.

**NATIVE_VOCABULARY_PRESERVATION: `SUPPORTED`.** The source-native text can
be retained without normalization or canonical interpretation.

**OBSERVATION_BOUNDARY_COMPATIBILITY: `SUPPORTED`.** The value can be
represented honestly as the source-native current status contained in the
retained artifact state. The exact acquisition time and immutable
authoritative snapshot binding remain unresolved. No observation timestamp is
inferred.

**LIFECYCLE_NEUTRALITY: `SUPPORTED`.** The mapping requires no claim about
transition history, monotonicity, terminality, reopening, closure semantics,
or final resolution.

### Counterevidence / Limitation

The strongest argument for acceptance is that `source_status` exists to
preserve native status semantics, and Calgary explicitly identifies
`status_description` as the admitted request's current status.

The strongest argument against acceptance is that the retained artifact lacks
an exact acquisition timestamp and immutable authoritative snapshot binding,
while only current-state rather than historical-state semantics are
documented.

`COUNTERARGUMENT`: Without an exact acquisition or observation time, the
contract cannot precisely place the current-status value on a historical
timeline.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_MAPPING`

The retained artifact supplies a bounded evidence state sufficient to
preserve the source-native current-status value. The mapping does not claim an
exact observation instant, a latest transition event, complete status
history, or historical finality.

### Current-Status Boundary

**SOURCE_STATUS.** Calgary's source-native current-status representation.

**CANONICAL_STATUS.** A future optional normalized interpretation.

**LIFECYCLE_HISTORY.** A sequence of prior statuses or transitions, not
established here.

**FINAL_DISPOSITION_OR_RESOLUTION.** A stronger semantic conclusion not
established by `source_status`.

A source-native value such as "Closed" must not be interpreted here as proof
of irreversible final resolution or impossibility of reopening.

### Representation Boundary

The source-native lexical status value is preserved.

This decision does not choose:

- enum implementation;
- casing normalization;
- synonym collapsing;
- canonical equivalents;
- ordinal ordering;
- database representation beyond preserving source text.

Exact implementation remains deferred.

### Canonical-Status Boundary

Decision Question 6 remains completely undecided. This decision does not
define a canonical vocabulary or introduce any `canonical_status`
normalization. Official example values do not establish a normalization
policy.

### Analytical Boundary

`ACCEPT_MAPPING` establishes nothing about:

- closure eligibility;
- final resolution;
- censoring;
- duration validity;
- SLA eligibility;
- reopen rates;
- transition counts;
- state residence time;
- workflow decomposition.

One current-status snapshot does not establish lifecycle history.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003

The official description of `status_description` is External evidence. The
mapping `status_description -> source_status` is the Design choice. The
mapping is not classified as an external fact or research conclusion.

### Falsification / Revision Condition

This mapping must be revisited if credible future evidence shows that:

- `status_description` is display text rather than authoritative
  source-native request status;
- the field mixes status with unrelated descriptive content;
- its semantics vary materially across records or source versions;
- another field is the authoritative source-native status;
- a source migration materially changes `status_description` semantics.

Discovery of additional native status values, ordinary new rows, routine
refreshes, and changed CSV hashes do not automatically falsify the mapping.

`INCREMENT_002_SOURCE_STATUS_FALSIFICATION: none`

Successful Calgary `source_status` mapping does not validate cross-source
portability.

Decision Question 6 remains undecided: this decision does not establish
`canonical_status`. Submission-channel representation, `service_name`
representation, `agency_responsible` representation, `updated_date`
treatment, `closed_date` treatment, unavailable canonical concepts, and
material source-native evidence outside the minimal Case also remain
undecided.

## Decision Question 6 - Canonical Status

### Decision Question

Does the currently retained Calgary evidence justify populating
`canonical_status` from `source_status`?

### Canonical Requirement

Increment 002 defines `canonical_status` as an optional normalized lifecycle
interpretation.

`canonical_status` is optional and separate from `source_status`. It may exist
only when a defensible mapping exists. Any normalization must be deterministic,
documented, reproducible, and testable. `source_status` must remain preserved,
and unsupported equivalence must not be forced. The canonical vocabulary and
implementation remain deferred unless separately justified.

`canonical_status` is not required for every source and does not automatically
mean a binary open-or-closed model, terminality, final resolution, absence of
reopening, workflow completion, or analytical eligibility.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `status_description`;
- type: `text`;
- description: "The current status of the request (e.g. open, closed)."

Decision Question 5 established:

    status_description -> source_status

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank `status_description` values: 0;
- whitespace-only `status_description` values: 0.

No distinct-value inspection was performed for this decision.

The retained evidence does not establish:

- the complete native status vocabulary;
- value frequencies;
- a transition graph;
- lifecycle ordering;
- terminality;
- reopening behavior;
- reversibility;
- final-resolution equivalence;
- native-to-canonical normalization rules.

### Competing Interpretations

**Interpretation A — `ACCEPT_MAPPING`.** Define and populate
`canonical_status` now. Review classification: `UNSUPPORTED`.

**Interpretation B — `DEFER_MAPPING`.** Preserve `source_status` and postpone
canonical normalization until sufficient vocabulary, semantic, cross-source,
or concrete-use evidence exists. Review classification: `STRONGEST`.

**Interpretation C — `CANONICAL_CONCEPT_UNAVAILABLE`.** Under the current
Calgary contract, conclude that `canonical_status` cannot presently be
populated. Review classification: `PLAUSIBLE`.

**Interpretation D — `REJECT_MAPPING`.** Conclude that Calgary source statuses
should not be normalized. Review classification: `UNSUPPORTED`.

Competing-decision summary:

    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: STRONGEST
    CANONICAL_CONCEPT_UNAVAILABLE: PLAUSIBLE
    REJECT_MAPPING: UNSUPPORTED

### Decision

`DEFER_MAPPING`

No `canonical_status` mapping is established at this stage. No canonical
status vocabulary is defined, and no native-to-canonical status mapping is
introduced.

The normalization decision remains open pending stronger vocabulary,
semantic, cross-source, or concrete-use evidence. This decision does not mark
`canonical_status` unavailable and does not assign an unavailability reason.

### Justification

**NORMALIZATION_NEED: `NOT_ESTABLISHED`.** No committed current use case
requires canonical normalization.

**VOCABULARY_COVERAGE: `INSUFFICIENT`.** No complete Calgary native status
vocabulary has been inspected or retained.

**SEMANTIC_EQUIVALENCE: `INDETERMINATE`.** Example values such as open and
closed do not establish safe or complete canonical equivalents.

**REVERSIBILITY_NEUTRALITY: `INDETERMINATE`.** Without authoritative
lifecycle semantics, a normalized state cannot be shown to avoid unsupported
terminality or no-reopen implications.

**CROSS_SOURCE_NORMALIZATION_BASIS: `NOT_ESTABLISHED`.** No retained
cross-source status comparison currently justifies a shared normalized
vocabulary.

The existence of useful `source_status` does not itself justify
`canonical_status`.

### Counterevidence / Limitation

The strongest argument for acceptance is that a broad normalized status model
could simplify later comparison while retaining `source_status` unchanged.

The strongest argument against acceptance is that only example source values
are known; the complete native vocabulary, lifecycle semantics, terminality,
reopening behavior, normalization need, and cross-source basis are absent.

`COUNTERARGUMENT`: A deliberately broad, non-terminal canonical grouping
could provide immediate comparison value while retaining native
`source_status`.

`COUNTERARGUMENT_RESULT: LEAVES_DECISION_INDETERMINATE`

That possibility does not supply the missing vocabulary, lifecycle semantics,
or cross-source justification required for a defensible, deterministic, and
reproducible normalization.

### Open / Closed Boundary

"open" and "closed" are official examples, not a demonstrated complete
native vocabulary. No canonical mapping is inferred from either example.

This decision does not infer that any future closure-like canonical value
would mean terminal, irreversible, resolved, finally disposed, analytically
complete, or unable to reopen.

### Source-Status Preservation Boundary

The accepted source-native mapping remains unchanged:

    status_description -> source_status

Any future `canonical_status` must coexist with `source_status`.
`canonical_status` must never erase, overwrite, or substitute for the
source-native value.

### Deferred Versus Unavailable Boundary

`DEFER_MAPPING` means the normalization decision remains open because the
evidence required for a defensible mapping has not yet been established.

`CANONICAL_CONCEPT_UNAVAILABLE` would be the stronger bounded conclusion that
`canonical_status` cannot presently be populated under the contract. That
stronger conclusion is not selected here. No `UNAVAILABLE` reason is assigned.

### Analytical Boundary

Decision Question 6 establishes nothing about:

- closure eligibility;
- final resolution;
- censoring;
- duration validity;
- SLA eligibility;
- reopen rates;
- transition counts;
- state residence;
- workflow decomposition.

Canonical normalization and analytical eligibility remain separate.

### Portability Boundary

Deferring `canonical_status` does not validate or falsify cross-source
portability. A future shared canonical status vocabulary would require actual
cross-source evidence.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The source field definition is External evidence. The `DEFER_MAPPING` result
is the Design choice. Neither the deferral nor any hypothetical canonical
vocabulary is presented as external fact or a research conclusion.

### Falsification / Revision Condition

This decision should be revisited if future evidence provides:

- the complete native Calgary status vocabulary;
- authoritative semantics for each native status;
- transition semantics;
- reopening or reversibility semantics;
- evidence from a second operational source requiring normalized comparison;
- a concrete analytical or product requirement for normalization;
- evidence that a deterministic many-to-one mapping preserves all relevant
  lifecycle distinctions.

Ordinary new rows, refreshed exports, changed CSV hashes, and discovery that
additional `source_status` values exist do not by themselves establish a
normalization policy.

`INCREMENT_002_CANONICAL_STATUS_FALSIFICATION: none`

The current inability to normalize Calgary status does not falsify an
optional `canonical_status` concept.

Decision Question 7 remains undecided: this decision does not establish
submission-channel representation. `service_name` representation,
`agency_responsible` representation, `updated_date` treatment, `closed_date`
treatment, unavailable canonical concepts, and material source-native
evidence outside the minimal Case also remain undecided.

## Decision Question 7 - Submission Channel

### Decision Question

How should Calgary `source` be represented given that Increment 002 did not
establish a universal canonical intake-channel scalar?

### Canonical Requirement / Boundary

Increment 002 establishes that `intake_channel` is not a universal canonical
Case field.

Source system, intake or origin information, submission mechanism,
interaction channel, creation mechanism, and originating actor or system are
materially distinct concepts. Useful source-native evidence may be retained
with its actual semantics without creating a universal canonical scalar.

Decision Question 2 established:

    source_system = city_of_calgary_311

Calgary's native `source` field remains semantically distinct from
`source_system`.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `source`;
- type: `text`;
- description: "The channel used to submit the request."

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank `source` values: 0;
- whitespace-only `source` values: 0.

No distinct-value inspection was performed for this decision.

The retained evidence does not establish:

- the complete submission-channel vocabulary;
- normalized channel categories;
- interaction-modality semantics for every value;
- a channel hierarchy;
- cross-source channel equivalence;
- historical semantic stability for every value.

### Competing Interpretations

**Interpretation A — `RETAIN_SOURCE_NATIVE`.** Preserve Calgary `source` as
source-native request-submission-channel evidence without creating a
universal canonical Case scalar. Review classification: `STRONGEST`.

**Interpretation B — `ACCEPT_MAPPING`.** Map Calgary `source` to an existing
canonical Case field. Review classification: `UNSUPPORTED`.

**Interpretation C — `DEFER_MAPPING`.** Preserve the evidence conceptually but
postpone even the semantic retention decision because physical representation
is unresolved. Review classification: `PLAUSIBLE`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat the
corresponding canonical concept as unavailable. Review classification:
`UNSUPPORTED`.

**Interpretation E — `REJECT_MAPPING`.** Do not preserve Calgary `source` as
meaningful source evidence. Review classification: `UNSUPPORTED`.

Competing-decision summary:

    RETAIN_SOURCE_NATIVE: STRONGEST
    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: PLAUSIBLE
    CANONICAL_CONCEPT_UNAVAILABLE: UNSUPPORTED
    REJECT_MAPPING: UNSUPPORTED

### Decision

`RETAIN_SOURCE_NATIVE`

Calgary `source` is retained as source-native evidence with the meaning:

> The channel used to submit the request.

No universal canonical Case field is introduced. Calgary `source` is not
mapped to `source_system` and is not equated with interaction channel.
Interaction-channel equivalence would require separate future evidence.

### Justification

**SOURCE_SUBMISSION_CHANNEL_SEMANTICS: `SUPPORTED`.** Calgary explicitly
defines the field as the channel used to submit the request.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes a property of the
admitted Calgary request.

**SOURCE_SYSTEM_SEPARATION: `SUPPORTED`.** `source_system` identifies the
Calgary 311 source identity namespace, while Calgary `source` describes how
the request was submitted.

**UNIVERSAL_CHANNEL_FIELD_JUSTIFICATION: `NOT_ESTABLISHED`.** Increment 002
established no universal intake-channel scalar, and the current evidence does
not justify adding one.

**SOURCE_NATIVE_PRESERVATION: `SUPPORTED`.** The field has explicit source
meaning that can be preserved without forcing canonical expansion.

**CHANNEL_NORMALIZATION_NEED: `NOT_ESTABLISHED`.** No committed current
requirement needs normalized channel values.

**CROSS_SOURCE_CHANNEL_BASIS: `NOT_ESTABLISHED`.** No retained cross-source
channel evidence justifies a shared model.

### Counterevidence / Limitation

The strongest argument for `RETAIN_SOURCE_NATIVE` is that Calgary explicitly
defines request-level submission-channel evidence, and native retention
prevents semantic loss without turning a source-specific concept into a
universal Case field.

The strongest argument against `RETAIN_SOURCE_NATIVE` is that preserving
source-specific evidence without an established physical extension mechanism
could produce inconsistent adapters, uncontrolled extensions, or unclear
future query semantics.

`COUNTERARGUMENT`: An unspecified physical representation mechanism may
produce inconsistent source adapters or unclear access patterns.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

The unresolved representation mechanism is an implementation and design
issue. It does not defeat the semantic decision that the evidence is
meaningful and should remain recoverable.

### Representation Boundary

This decision establishes only the semantic retention rule: Calgary `source`
is retained as source-native evidence meaning "the channel used to submit the
request."

This decision does not choose:

- a Python field name;
- a database column name;
- a JSON metadata structure;
- an extension-object design;
- an enum representation;
- casing normalization;
- synonym collapsing;
- a channel hierarchy;
- a canonical vocabulary.

Exact physical representation remains deferred.

### Source-System Boundary

The canonical identity namespace remains:

    source_system = city_of_calgary_311

Calgary `source` means the channel used to submit the request. The two values
describe different concepts: identity namespace and source-native submission
channel, respectively.

### Missingness Boundary

Retained population evidence shows:

    blank source: 0
    whitespace-only source: 0

This does not establish submission channel as universally required, create a
new universal Case invariant or identity-core field, or require every future
source to expose equivalent evidence.

### Analytical Boundary

`RETAIN_SOURCE_NATIVE` establishes nothing about:

- channel effectiveness;
- channel quality;
- digital adoption;
- contact deflection;
- cost to serve;
- customer preference;
- channel-driven duration;
- channel-driven SLA performance;
- causal effects of submission channel.

Those conclusions require separate analytical contracts and evidence.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The official definition of Calgary `source` is External evidence.
`RETAIN_SOURCE_NATIVE` is the Design choice. The retention decision is not
presented as an external fact or research conclusion.

### Falsification / Revision Condition

This decision should be revisited if future evidence shows that:

- Calgary `source` means something other than submission channel;
- the field combines materially different concepts;
- source migration materially changes its semantics;
- later cross-source evidence supports a defensible canonical channel
  concept;
- a concrete product or analytical requirement justifies a shared
  representation.

Ordinary new rows, additional native channel values, refreshed exports, and
changed CSV hashes do not automatically falsify source-native retention.

`INCREMENT_002_SUBMISSION_CHANNEL_FALSIFICATION: none`

Successful source-native retention does not justify extending Increment 002
with a universal channel scalar.

### Portability Boundary

Source-native retention does not validate cross-source portability. A future
canonical channel concept would require actual cross-source evidence.

Decision Question 8 remains undecided: this decision does not establish
`service_name` representation. `agency_responsible` representation,
`updated_date` treatment, `closed_date` treatment, unavailable canonical
concepts, and other source-native evidence beyond the specific Calgary
`source` decision also remain undecided.

## Decision Question 8 - Service Type / Classification

### Decision Question

How should Calgary `service_name` be represented under the Increment 002
canonical Case contract?

### Canonical Requirement / Boundary

Increment 002 establishes that `category` and `sub_category` are not universal
scalar Case fields. A Case may have zero or more classification concepts.
Source-native classification meaning and structure must remain traceable, and
hierarchy must not be inferred from naming, delimiters, or convenience.

Increment 002 recognizes classification conceptually but does not define a
concrete canonical mapping target for Calgary `service_name`. The concrete
classification model and physical representation remain deferred. This
decision does not create such a target.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `service_name`;
- type: `text`;
- description: "The type of service requested."

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank `service_name` values: 0;
- whitespace-only `service_name` values: 0.

No distinct-value inspection was performed for this decision.

The retained evidence does not establish:

- the complete service-name vocabulary;
- a hierarchy;
- parent or child relationships;
- taxonomy depth;
- historical stability;
- normalization rules;
- cross-source equivalence;
- analytical grouping validity.

### Competing Interpretations

**Interpretation A — `RETAIN_SOURCE_NATIVE`.** Preserve Calgary
`service_name` as source-native service-type and classification evidence
without introducing universal scalar fields. Review classification:
`STRONGEST`.

**Interpretation B — `ACCEPT_MAPPING`.** Map `service_name` into an
already-existing canonical classification representation. Review
classification: `UNSUPPORTED`.

**Interpretation C — `DEFER_MAPPING`.** Recognize the evidence but postpone
even semantic retention because the physical representation is unresolved.
Review classification: `PLAUSIBLE`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat canonical
classification as unavailable for Calgary. Review classification:
`UNSUPPORTED`.

**Interpretation E — `REJECT_MAPPING`.** Do not preserve `service_name` as
meaningful classification evidence. Review classification: `UNSUPPORTED`.

Competing-decision summary:

    RETAIN_SOURCE_NATIVE: STRONGEST
    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: PLAUSIBLE
    CANONICAL_CONCEPT_UNAVAILABLE: UNSUPPORTED
    REJECT_MAPPING: UNSUPPORTED

### Decision

`RETAIN_SOURCE_NATIVE`

Calgary `service_name` is retained as source-native evidence meaning:

> The type of service requested.

No universal canonical scalar is introduced. No hierarchy is inferred, and
no canonical service taxonomy is defined.

### Justification

**SOURCE_SERVICE_TYPE_SEMANTICS: `SUPPORTED`.** Calgary explicitly defines
`service_name` as the type of service requested.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes the admitted Calgary
service request.

**CLASSIFICATION_ALIGNMENT: `SUPPORTED`.** "Type of service requested" is
legitimately source-native classification evidence.

**EXISTING_CANONICAL_CLASSIFICATION_TARGET: `NOT_ESTABLISHED`.** Increment 002
recognizes classification conceptually but does not define a concrete
representation or mapping target.

**SOURCE_NATIVE_PRESERVATION: `SUPPORTED`.** The source evidence can be
retained faithfully without forcing universal canonical structure.

**HIERARCHY_NEUTRALITY: `SUPPORTED`.** Retention requires no parent or child,
category or subcategory, or taxonomy assumptions.

**SERVICE_CLASSIFICATION_NORMALIZATION_NEED: `NOT_ESTABLISHED`.** No committed
current requirement needs normalized service classification.

**CROSS_SOURCE_CLASSIFICATION_BASIS: `NOT_ESTABLISHED`.** No retained
cross-source classification evidence justifies a shared service taxonomy.

### Counterevidence / Limitation

The strongest argument for `RETAIN_SOURCE_NATIVE` is that Calgary explicitly
identifies the requested service type, and native retention preserves useful
classification evidence without inventing universal scalars, normalization,
or hierarchy.

The strongest opposing argument is that source-native-only retention may
postpone a coherent classification model and create inconsistent adapter or
query semantics.

`COUNTERARGUMENT`: An unresolved shared classification representation may
produce inconsistent source-specific extensions or unclear access patterns.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

This concern motivates later representation design but does not defeat the
semantic retention rule.

### Category / Subcategory Boundary

No universal `category`, `sub_category`, or `service_name` Case scalar is
introduced.

No classification hierarchy is inferred from field names, delimiters,
wording, neighboring fields, or the apparent breadth of service labels.

### Representation Boundary

This decision establishes only semantic retention.

It does not choose:

- a Python field name;
- a database column;
- a JSON structure;
- a classification-object schema;
- a taxonomy identifier;
- an enum representation;
- casing normalization;
- synonym collapsing;
- a hierarchy;
- a canonical service vocabulary.

Exact physical representation remains deferred.

### Missingness Boundary

Retained population evidence shows:

    blank service_name: 0
    whitespace-only service_name: 0

This does not establish universal classification availability, a universal
required Case field, a Case invariant, an identity-core requirement, or a
requirement for future sources to expose equivalent classification.

### Analytical Boundary

`RETAIN_SOURCE_NATIVE` establishes nothing about:

- service-demand distribution;
- high-volume service types;
- service complexity;
- service difficulty;
- operational ownership;
- duration by service type;
- SLA by service type;
- workload by service type;
- operational priority;
- causal effects of service type.

Those conclusions require separate analytical contracts and evidence.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The official `service_name` definition is External evidence.
`RETAIN_SOURCE_NATIVE` is the Design choice. The representation decision is
not presented as an external fact or research conclusion.

### Falsification / Revision Condition

This decision should be revisited if future evidence shows that:

- `service_name` means something materially different from service type;
- `service_name` combines multiple materially distinct concepts;
- source migration materially changes its semantics;
- an authoritative Calgary classification hierarchy becomes available;
- cross-source evidence supports a defensible shared classification model;
- a concrete analytical or product requirement requires standardized
  classification;
- Increment 002 is revised to define a concrete classification representation.

Ordinary new rows, additional `service_name` values, refreshed exports, and
changed CSV hashes do not automatically falsify source-native retention.

`INCREMENT_002_SERVICE_CLASSIFICATION_FALSIFICATION: none`

Native retention does not justify extending Increment 002 with universal
`category`, `sub_category`, or `service_name` scalars.

### Portability Boundary

Source-native service classification is not portability evidence. A future
shared classification model requires actual cross-source evidence.

Decision Question 9 remains undecided: this decision does not establish
`agency_responsible` representation. `updated_date` treatment, `closed_date`
treatment, unavailable canonical concepts, and source-native evidence beyond
the `service_name` question also remain undecided.

## Decision Question 9 - Responsible Department

### Decision Question

How should Calgary `agency_responsible` be represented under the Increment 002
canonical Case contract?

### Canonical Requirement / Boundary

Increment 002 establishes that `owning_group` is not a universal Case scalar.
Organizational responsibility and workflow assignment are materially different
concepts, and source contracts must preserve the actual source meaning.
Source-native organizational semantics may remain recoverable without creating
a universal organizational scalar.

Responsibility must not be silently interpreted as assignment, ownership,
queue state, routing state, or reassignment history. Future normalization
requires separate justification, and organizational representation remains
deferred.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `agency_responsible`;
- type: `text`;
- description: "The department responsible for this request."

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank `agency_responsible` values: 0;
- whitespace-only `agency_responsible` values: 0.

No distinct-value inspection was performed for this decision.

The retained evidence does not establish:

- a current assignee;
- an assignment group;
- a queue;
- a routing destination;
- transfer history;
- reassignment history;
- a responsible individual;
- a lower-level team;
- a resolver team;
- an organizational hierarchy;
- ownership equivalence;
- cross-source organizational equivalence;
- a normalized agency vocabulary.

### Competing Interpretations

**Interpretation A — `RETAIN_SOURCE_NATIVE`.** Preserve `agency_responsible`
as source-native responsible-department evidence without creating a universal
organizational Case scalar. Review classification: `STRONGEST`.

**Interpretation B — `ACCEPT_MAPPING`.** Map `agency_responsible` into an
already-existing canonical organizational field. Review classification:
`UNSUPPORTED`.

**Interpretation C — `DEFER_MAPPING`.** Recognize the evidence but postpone
semantic retention because physical representation is unresolved. Review
classification: `PLAUSIBLE`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat a corresponding
canonical organizational concept as unavailable. Review classification:
`UNSUPPORTED`.

**Interpretation E — `REJECT_MAPPING`.** Do not preserve
`agency_responsible` as meaningful source evidence. Review classification:
`UNSUPPORTED`.

Competing-decision summary:

    RETAIN_SOURCE_NATIVE: STRONGEST
    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: PLAUSIBLE
    CANONICAL_CONCEPT_UNAVAILABLE: UNSUPPORTED
    REJECT_MAPPING: UNSUPPORTED

### Decision

`RETAIN_SOURCE_NATIVE`

Calgary `agency_responsible` is retained as source-native evidence meaning:

> The department responsible for this request.

No universal organizational Case scalar is introduced.

### Justification

**SOURCE_RESPONSIBILITY_SEMANTICS: `SUPPORTED`.** Calgary explicitly defines
`agency_responsible` as the department responsible for the request.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes the admitted Calgary
service request.

**RESPONSIBILITY_ASSIGNMENT_SEPARATION: `SUPPORTED`.** The evidence can be
retained while explicitly refusing to interpret responsibility as current
assignment, queue, or routing state.

**UNIVERSAL_ORGANIZATIONAL_FIELD_JUSTIFICATION: `NOT_ESTABLISHED`.** Neither
Increment 002 nor the retained evidence establishes a universal
`owning_group`, `assigned_group`, or `responsible_department` target.

**SOURCE_NATIVE_PRESERVATION: `SUPPORTED`.** The field can be retained with
its exact source meaning without canonical expansion.

**ORGANIZATIONAL_HIERARCHY_NEUTRALITY: `SUPPORTED`.** Retention requires no
parent department, child team, organizational tree, escalation level,
assignment group, queue, or ownership-hierarchy assumption.

**ORGANIZATIONAL_NORMALIZATION_NEED: `NOT_ESTABLISHED`.** No committed current
requirement needs normalized department names.

**CROSS_SOURCE_ORGANIZATIONAL_BASIS: `NOT_ESTABLISHED`.** No retained
cross-source evidence supports a shared organizational-responsibility model.

### Responsibility / Assignment Boundary

`agency_responsible` means source-native responsible department only.

It does not establish:

- a current assignee;
- an assignment group;
- a queue;
- a routing destination;
- a work owner;
- a first recipient;
- a last actor;
- a resolver team;
- transfer history;
- reassignment history.

This decision does not map:

    agency_responsible -> owning_group
    agency_responsible -> assigned_group
    agency_responsible -> current_queue
    agency_responsible -> current_owner

### Counterevidence / Limitation

The strongest argument for `RETAIN_SOURCE_NATIVE` is that Calgary explicitly
identifies the responsible department for the admitted request, and native
retention preserves that meaning without equating responsibility with
assignment or creating a universal organizational field.

The strongest opposing argument is that source-native-only retention may
produce inconsistent adapter or query semantics and postpone a coherent
distinction among responsibility, ownership, and assignment.

`COUNTERARGUMENT`: An unresolved shared organizational representation may lead
to inconsistent source-specific extensions or unclear access patterns as
workflow capabilities expand.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

This motivates later representation design but does not defeat the semantic
retention rule.

### Representation Boundary

This decision establishes semantic retention only.

It does not choose:

- a Python field name;
- a database column;
- a JSON structure;
- an organizational-object schema;
- a department identifier;
- an enum representation;
- normalization;
- a hierarchy;
- a canonical organization vocabulary.

Exact physical representation remains deferred.

### Missingness Boundary

Retained population evidence shows:

    blank agency_responsible: 0
    whitespace-only agency_responsible: 0

This does not establish universal organizational availability, a required
Case field, a Case invariant, identity-core status, or a requirement that
every future source provide equivalent evidence.

### Analytical Boundary

`RETAIN_SOURCE_NATIVE` establishes nothing about:

- departmental workload;
- department performance;
- staffing;
- capacity;
- queue size;
- reassignment;
- handoffs;
- routing quality;
- ownership quality;
- resolution performance;
- SLA performance;
- causal effects of department responsibility.

Those conclusions require separate analytical contracts and evidence.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The official `agency_responsible` definition is External evidence.
`RETAIN_SOURCE_NATIVE` is the Design choice.

### Falsification / Revision Condition

This decision should be revisited if future evidence shows that:

- `agency_responsible` means something other than responsible department;
- it actually encodes assignment or queue state;
- it combines multiple organizational concepts;
- source migration materially changes its semantics;
- an authoritative organizational hierarchy becomes available;
- cross-source evidence supports a defensible shared
  responsibility/assignment model;
- a concrete analytical or product requirement needs standardized
  organizational representation.

Ordinary new rows, additional department values, refreshed exports, and
changed CSV hashes do not automatically falsify source-native retention.

`INCREMENT_002_RESPONSIBILITY_FALSIFICATION: none`

Native retention does not justify extending Increment 002 with universal
`owning_group`, assignment, queue, or ownership scalars.

### Portability Boundary

Source-native responsible-department evidence is not portability evidence. A
future shared organizational model requires actual cross-source evidence.

Decision Question 10 remains undecided: this decision does not establish
`updated_date` treatment. `closed_date` treatment, unavailable canonical
concepts, and source-native evidence beyond the `agency_responsible` question
also remain undecided.

## Decision Question 10 - Updated Date / Source-Native Update Time

### Decision Question

How should Calgary `updated_date` be treated under the Increment 002 canonical
Case contract?

### Canonical Requirement / Boundary

Increment 002 establishes that `updated_at` is not a universal canonical Case
scalar. Record modification, lifecycle change, latest event, and latest
platform evidence are materially distinct concepts. Source-native temporal
evidence may remain useful without becoming a universal canonical timestamp.

`MAX(event_timestamp)` does not by itself establish `Case.updated_at`.
Temporal meaning must come from source semantics rather than field-name
resemblance. Precision, provenance, and observation boundaries must remain
explicit. Physical representation and projections remain deferred.

This decision does not create a universal update-time concept.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `updated_date`;
- type: `calendar_date`;
- format metadata: `date_ymd_time`;
- description: "The most recent date the request was updated."

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank values: 77,829;
- parseable values: 7,396,574;
- unparseable values: 0;
- minimum parsed value: `2012-01-01 02:11:34`;
- maximum parsed value: `2026-09-08 00:00:00`;
- exact-midnight values: 3,603,787;
- non-midnight values: 3,792,787;
- exact-midnight percentage of parseable values: 48.722381%;
- non-midnight values with second zero: 63,453;
- non-midnight values with second nonzero: 3,729,334.

The retained evidence preserves these boundaries:

    UPDATED_DATE_RECORD_VS_LIFECYCLE_MEANING_UNRESOLVED
    SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED
    TIMEZONE_SEMANTICS_UNRESOLVED

No new temporal evidence is introduced by this decision.

### Competing Interpretations

**Interpretation A — `RETAIN_SOURCE_NATIVE`.** Preserve `updated_date` as
source-native request-update-time evidence with exactly the source-supported
meaning. Review classification: `STRONGEST`.

**Interpretation B — `ACCEPT_MAPPING`.** Map `updated_date` into an
already-existing canonical Case timestamp. Review classification:
`UNSUPPORTED`.

**Interpretation C — `DEFER_MAPPING`.** Recognize the evidence but postpone
semantic retention because its operational update mechanism or physical
representation is unresolved. Review classification: `PLAUSIBLE`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat a corresponding
canonical update-time concept as unavailable. Review classification:
`UNSUPPORTED`.

**Interpretation E — `REJECT_MAPPING`.** Do not preserve `updated_date` as
meaningful temporal evidence. Review classification: `UNSUPPORTED`.

Competing-decision summary:

    RETAIN_SOURCE_NATIVE: STRONGEST
    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: PLAUSIBLE
    CANONICAL_CONCEPT_UNAVAILABLE: UNSUPPORTED
    REJECT_MAPPING: UNSUPPORTED

### Decision

`RETAIN_SOURCE_NATIVE`

Calgary `updated_date` is retained as source-native temporal evidence
meaning:

> The most recent date the request was updated.

No universal canonical update-time scalar is introduced.

### Justification

**SOURCE_UPDATE_SEMANTICS: `SUPPORTED`.** Calgary explicitly defines
`updated_date` as the most recent date the request was updated, without
establishing what kinds of updates qualify.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes the admitted Calgary
service request.

**LIFECYCLE_NEUTRALITY: `SUPPORTED`.** The value can be retained without
claiming lifecycle transition, latest event, assignment change, routing,
handoff, resolver action, or productive-work semantics.

**UNIVERSAL_UPDATED_AT_JUSTIFICATION: `NOT_ESTABLISHED`.** Increment 002 does
not establish universal `updated_at`, and the retained evidence does not
justify an equivalent universal scalar.

**SOURCE_NATIVE_PRESERVATION: `SUPPORTED`.** The field can be retained with
its bounded source meaning without canonical expansion.

**TEMPORAL_PRECISION_HONESTY: `SUPPORTED`.** Retention does not require
claiming actual source measurement precision from the lexical representation.

**TIMEZONE_HONESTY: `SUPPORTED`.** Retention does not require inventing a
timezone or offset interpretation.

**MISSINGNESS_NEUTRALITY: `SUPPORTED`.** Blank values can remain observed
missingness without assigning a reason or lifecycle meaning.

### Update / Lifecycle Boundary

`UPDATED_DATE_RECORD_VS_LIFECYCLE_MEANING_UNRESOLVED`

`updated_date` does not establish:

- lifecycle-transition time;
- latest event time;
- status-change time;
- assignment-change time;
- routing-change time;
- handoff time;
- resolver activity;
- productive-work time;
- observation time;
- extraction time;
- ingestion time.

The word "updated" is not proof of operational lifecycle meaning.

This decision does not map:

    updated_date -> Case.updated_at
    updated_date -> Case.lifecycle_updated_at
    updated_date -> Case.latest_event_at
    updated_date -> Case.status_changed_at
    updated_date -> Case.assignment_changed_at
    updated_date -> Case.routing_changed_at
    updated_date -> Case.handoff_at

### Counterevidence / Limitation

The strongest argument for `RETAIN_SOURCE_NATIVE` is that Calgary explicitly
defines a request update-time concept that applies to the admitted request and
can be retained without lifecycle interpretation or universal canonical
expansion.

The strongest opposing argument is that "updated" remains broad;
record-versus-lifecycle meaning, exact observation boundary, immutable
snapshot provenance, temporal precision, and timezone remain unresolved, and
source-specific temporal fields may complicate common access.

`COUNTERARGUMENT`: Unresolved update mechanisms and temporal context may cause
consumers to mistake the field for lifecycle activity or implement
inconsistent source-specific query semantics.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

Those limitations constrain interpretation but do not defeat bounded semantic
retention.

### Representation Boundary

This decision establishes semantic retention only.

It does not choose:

- a Python field name;
- a database column;
- a database timestamp type;
- timezone attachment;
- timezone conversion;
- UTC conversion;
- precision reduction;
- flooring;
- truncation;
- parser implementation;
- a serialization format.

Exact physical representation remains deferred.

### Precision Boundary

`SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED`

- Lexical seconds do not prove second-level source measurement precision.
- Midnight prevalence does not prove date-only capture.
- Midnight values do not prove defaulting, imputation, rounding, truncation,
  or synthetic timestamps.

### Timezone Boundary

`TIMEZONE_SEMANTICS_UNRESOLVED`

No UTC, Calgary local time, Mountain Time, MST, MDT, DST behavior, or timezone
offset interpretation is introduced.

### Missingness Boundary

Retained population evidence shows:

    blank updated_date: 77,829
    parseable nonblank: 7,396,574
    unparseable nonblank: 0

Blank values do not establish never updated, open, unchanged, newly created,
source error, invalid Case, unavailable lifecycle, or any canonical
`UNAVAILABLE` reason. This decision assigns no `UNAVAILABLE` reason.

### Analytical Boundary

`RETAIN_SOURCE_NATIVE` establishes nothing about:

- time to first update;
- time to latest update;
- handling time;
- active work;
- queue time;
- waiting time;
- state residence;
- time since last activity;
- staleness;
- responsiveness;
- SLA performance;
- lifecycle-transition timing;
- workflow activity;
- Case aging.

No timestamp subtraction is justified by this decision. Those conclusions
require separate analytical contracts and stronger semantics.

### Pairwise Temporal Boundary

Increment 003 retained pairwise timestamp observations. This decision does
not use those orderings to infer an expected lifecycle sequence, invalid
records, final-update semantics, closure semantics, or chronology rules.

The pairwise observations do not resolve what "updated" means operationally.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The official `updated_date` definition is External evidence.
`RETAIN_SOURCE_NATIVE` is the Design choice.

### Falsification / Revision Condition

This decision should be revisited if future evidence shows that:

- `updated_date` specifically means record-modification time;
- `updated_date` specifically means lifecycle-update time;
- `updated_date` represents latest-event time;
- `updated_date` combines materially different temporal mechanisms;
- source migration materially changes its semantics;
- authoritative documentation establishes stronger precision semantics;
- authoritative documentation establishes timezone semantics;
- cross-source evidence supports a defensible shared update-time concept;
- a concrete analytical or product requirement requires standardized update
  semantics.

Ordinary new rows, changed update values, refreshed exports, and changed CSV
hashes do not automatically falsify source-native retention.

`INCREMENT_002_UPDATED_DATE_FALSIFICATION: none`

Source-native update-time retention does not justify extending Increment 002
with a universal `updated_at` scalar.

### Portability Boundary

Source-native update-time evidence is not portability evidence. A future
shared update-time model requires actual cross-source evidence.

Decision Question 11 remains undecided: this decision does not establish
`closed_date` treatment. Unavailable canonical concepts and remaining
source-native evidence beyond the `updated_date` question also remain
undecided.

## Decision Question 11 - Closed Date / Source-Native Closure Time

### Decision Question

How should Calgary `closed_date` be treated under the Increment 002 canonical
Case contract?

### Canonical Requirement / Boundary

Increment 002 establishes that `closed_at` is not a universal canonical Case
scalar. Resolved, closed, completed, cancelled, abandoned, and rejected are
not equivalent, and closure need not be terminal. Reopening remains possible
unless source semantics prohibit it.

One generic closure scalar cannot safely imply first, latest-known, current,
or final closure. Source-native lifecycle timestamps may be preserved, and
Case admission does not require closure. Purpose-specific lifecycle
projections and physical representation remain deferred.

This decision does not create a universal closure ontology.

### Calgary Evidence

Increment 003 retained the following source evidence:

- field: `closed_date`;
- type: `calendar_date`;
- format metadata: `date_ymd_time`;
- description: "The date the request was closed."

Increment 003 also retained these local observations:

- logical data rows: 7,474,403;
- blank values: 78,347;
- parseable values: 7,396,056;
- unparseable values: 0;
- minimum parsed value: `2010-02-17 00:00:00`;
- maximum parsed value: `2026-09-09 00:00:00`;
- exact-midnight values: 3,528,193;
- non-midnight values: 3,867,863;
- exact-midnight percentage of parseable values: 47.703709%;
- non-midnight values with second zero: 65,943;
- non-midnight values with second nonzero: 3,801,920.

The retained evidence preserves these boundaries:

    CLOSED_DATE_LIFECYCLE_SEMANTICS_INCOMPLETE
    REOPENING_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA
    FINAL_CLOSURE_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA
    SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED
    TIMEZONE_SEMANTICS_UNRESOLVED

No new temporal or lifecycle evidence is introduced by this decision.

### Competing Interpretations

**Interpretation A — `RETAIN_SOURCE_NATIVE`.** Preserve `closed_date` as
source-native closure-time evidence with exactly the source-supported meaning.
Review classification: `STRONGEST`.

**Interpretation B — `ACCEPT_MAPPING`.** Map `closed_date` into an
already-existing canonical Case closure timestamp. Review classification:
`UNSUPPORTED`.

**Interpretation C — `DEFER_MAPPING`.** Recognize the evidence but postpone
semantic retention because closure finality, reopening, or physical
representation remains unresolved. Review classification: `PLAUSIBLE`.

**Interpretation D — `CANONICAL_CONCEPT_UNAVAILABLE`.** Treat a corresponding
canonical closure concept as unavailable. Review classification:
`UNSUPPORTED`.

**Interpretation E — `REJECT_MAPPING`.** Do not preserve `closed_date` as
meaningful lifecycle evidence. Review classification: `UNSUPPORTED`.

Competing-decision summary:

    RETAIN_SOURCE_NATIVE: STRONGEST
    ACCEPT_MAPPING: UNSUPPORTED
    DEFER_MAPPING: PLAUSIBLE
    CANONICAL_CONCEPT_UNAVAILABLE: UNSUPPORTED
    REJECT_MAPPING: UNSUPPORTED

### Decision

`RETAIN_SOURCE_NATIVE`

Calgary `closed_date` is retained as source-native temporal evidence meaning:

> The date the request was closed.

No universal closure, resolution, or finality scalar is introduced.

### Justification

**SOURCE_CLOSURE_SEMANTICS: `SUPPORTED`.** Calgary explicitly defines
`closed_date` as the date the request was closed, without establishing
resolution, completion, terminality, or finality.

**ENTITY_ALIGNMENT: `SUPPORTED`.** The field describes the admitted Calgary
service request.

**CLOSURE_RESOLUTION_SEPARATION: `SUPPORTED`.** The field can be retained
without treating closure as resolution, successful completion, customer
satisfaction, cancellation, abandonment, rejection, or permanent finish.

**REOPENING_NEUTRALITY: `SUPPORTED`.** Retention does not require claiming
that a closed request cannot reopen.

**FINALITY_NEUTRALITY: `SUPPORTED`.** Retention does not require claiming that
`closed_date` represents first, latest, current, or final closure.

**UNIVERSAL_CLOSED_AT_JUSTIFICATION: `NOT_ESTABLISHED`.** Increment 002 does
not establish universal `closed_at`, and the retained evidence does not
justify an equivalent universal scalar.

**SOURCE_NATIVE_PRESERVATION: `SUPPORTED`.** The field can be retained with
its exact source meaning without canonical expansion.

**TEMPORAL_PRECISION_HONESTY: `SUPPORTED`.** Retention does not require
claiming actual source measurement precision from the lexical representation.

**TIMEZONE_HONESTY: `SUPPORTED`.** Retention does not require inventing a
timezone or offset interpretation.

**MISSINGNESS_NEUTRALITY: `SUPPORTED`.** Blank values can remain observed
missingness without assigning a reason or lifecycle meaning.

### Closure / Resolution Boundary

`CLOSED_DATE_LIFECYCLE_SEMANTICS_INCOMPLETE`

`closed_date` does not establish:

- resolution;
- successful completion;
- customer satisfaction;
- cancellation;
- abandonment;
- rejection;
- terminal disposition;
- permanent finish.

This decision does not map:

    closed_date -> Case.closed_at
    closed_date -> Case.resolved_at
    closed_date -> Case.completed_at
    closed_date -> Case.final_disposition_at
    closed_date -> Case.terminal_at
    closed_date -> Case.final_closed_at

### Reopening Boundary

`REOPENING_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA`

This decision does not claim that a closed request cannot reopen.

### Finality Boundary

`FINAL_CLOSURE_SEMANTICS_UNRESOLVED_FROM_CURRENT_OFFICIAL_COLUMN_METADATA`

This decision does not claim that `closed_date` is first closure, latest
closure, current closure, final closure, or permanently terminal closure.

### Counterevidence / Limitation

The strongest argument for `RETAIN_SOURCE_NATIVE` is that Calgary explicitly
supplies request-level closure-time evidence, and native retention preserves
that evidence without claiming resolution, finality, or no-reopen semantics.

The strongest opposing argument is that closure semantics, reopening
behavior, first/latest/final closure meaning, status relationships, precision,
and timezone remain unresolved, and consumers may mistake the value for
resolution or permanent terminality.

`COUNTERARGUMENT`: Incomplete lifecycle semantics and temporal context may
encourage incorrect resolution or finality assumptions or inconsistent
source-specific access.

`COUNTERARGUMENT_RESULT: DOES_NOT_BLOCK_CURRENT_DECISION`

These limitations constrain interpretation but do not defeat bounded
source-native retention.

### Representation Boundary

This decision establishes semantic retention only.

It does not choose:

- a Python field name;
- a database column;
- a database timestamp type;
- timezone normalization;
- UTC conversion;
- precision transformation;
- parser implementation;
- a serialization format;
- a lifecycle-projection schema.

Exact physical representation remains deferred.

### Precision Boundary

`SOURCE_TEMPORAL_PRECISION_NOT_ESTABLISHED`

- Lexical seconds do not prove second-level source measurement precision.
- Midnight prevalence does not prove date-only capture.
- Midnight values do not prove defaulting, imputation, rounding, truncation,
  or synthetic timestamps.

### Timezone Boundary

`TIMEZONE_SEMANTICS_UNRESOLVED`

No timezone or offset interpretation is introduced.

### Missingness Boundary

Retained population evidence shows:

    blank closed_date: 78,347
    parseable nonblank: 7,396,056
    unparseable nonblank: 0

Blank values do not establish open, unresolved, active, pending, never closed,
reopened, invalid record, source error, unavailable lifecycle, or a canonical
`UNAVAILABLE` reason. This decision assigns no `UNAVAILABLE` reason.

A nonblank `closed_date` does not prove currently closed, terminal, resolved,
or final closure.

### Pairwise Temporal Boundary

Increment 003 retained these Engineering observations:

    requested_date vs closed_date
        both nonblank: 7,396,056
        requested < closed: 6,605,371
        requested = closed: 789,758
        requested > closed: 927

    updated_date vs closed_date
        both nonblank: 7,318,258
        updated < closed: 146,846
        updated = closed: 5,954,904
        updated > closed: 1,216,508

This decision does not use those observations to infer invalid records,
expected lifecycle sequence, corruption, closure finality, reopening,
latest-event semantics, resolution semantics, or chronology rules.

### Analytical Boundary

`RETAIN_SOURCE_NATIVE` establishes nothing about:

- resolution time;
- time to resolution;
- handling time;
- active work;
- queue time;
- waiting time;
- completion time;
- terminal disposition;
- final closure time;
- reopen rate;
- closure quality;
- SLA performance;
- Case aging;
- lifecycle-state residence.

No timestamp subtraction is justified by this decision. A later analytical
contract may define a bounded request-to-closure elapsed duration, but
Decision Question 11 does not authorize or define that metric.

### Claim Classification

Primary classification:

    Design choice

Evidence basis:

    External evidence retained in Increment 003
    Engineering observations retained in Increment 003
    Prior source-contract decisions in Increment 004

The official `closed_date` definition is External evidence.
`RETAIN_SOURCE_NATIVE` is the Design choice.

### Falsification / Revision Condition

This decision should be revisited if future evidence establishes:

- resolution semantics;
- first-closure semantics;
- latest-closure semantics;
- final-closure semantics;
- reopening behavior;
- combined lifecycle mechanisms;
- source migration that materially changes semantics;
- authoritative temporal precision;
- authoritative timezone semantics;
- defensible cross-source closure equivalence;
- a concrete requirement for standardized closure semantics.

Ordinary new rows, changed `closed_date` values, refreshed exports, and
changed CSV hashes do not automatically falsify source-native retention.

`INCREMENT_002_CLOSED_DATE_FALSIFICATION: none`

Source-native closure-time retention does not justify extending Increment 002
with universal `closed_at`, `resolved_at`, or finality fields.

### Portability Boundary

Source-native closure-time evidence is not portability evidence. A future
shared closure model requires actual cross-source evidence.

Decision Question 12 remains undecided: this decision does not establish
unavailable canonical concepts. Source-native evidence beyond `closed_date`,
analytical eligibility for request-to-closure duration, censoring treatment,
and closure-based population definitions also remain undecided.

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

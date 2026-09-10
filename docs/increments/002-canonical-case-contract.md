# Increment 002: Canonical Case Contract

**Status:** Complete
**Date opened:** 2026-09-09
**Date completed:** 2026-09-10

## Objective

Define the minimum canonical `Case` contract that later operational sources can map into without embedding assumptions from any one dataset, storage engine, API, or AI workflow.

The contract should establish shared semantics for case-level operational analysis before source-contract or implementation work begins.

Dataset-selection and preparation evidence now exists externally. Calgary 311 is staged for case-level operational analytics, and the ServiceNow Incident Response Log is staged for later event-rich workflow evidence. Their reported concepts and profiles have been used for conceptual pressure testing of this contract. Increment 002 did not perform dataset acquisition, direct filesystem inspection, empirical source validation, source-contract implementation, ingestion, or live licence verification.

## Scope

This increment will define:

- the operational meaning of a `Case`;
- the minimum canonical identity core;
- accepted non-identity concept boundaries;
- field semantics;
- required versus optional fields;
- field-state/provenance classification;
- treatment of unavailable source information;
- deterministic derivation boundaries;
- source-adapter obligations;
- canonical-model invariants;
- explicit analytical limitations of case-level data.

The accepted canonical identity fields are:

    case_id
    source_system
    source_case_id

The accepted optional canonical lifecycle and status concepts are:

    created_at
    source_status
    canonical_status

Classification supports zero or more classifications conceptually; `category` and `sub_category` are not universal scalar fields.

The following are not universal Case scalars:

    updated_at
    closed_at
    owning_group
    intake_channel
    priority
    customer_id
    location

Only the identity core is universally required and non-null. `created_at`, `source_status`, and `canonical_status` are optional. This summary does not imply that every non-scalar concept has an implementation representation; many representations remain explicitly deferred.

Each non-identity concept must be justified by a cross-source operational need. Missing evidence restricts analytical eligibility rather than automatically preventing Case admissibility.

## Non-goals

This increment will not:

- perform or reopen operational-dataset selection research;
- create a source adapter;
- define source-specific mappings;
- define `CaseEvent`;
- infer workflow transitions;
- infer active work time;
- create PostgreSQL schemas;
- create SQL;
- create Python domain classes;
- create APIs;
- create dashboards;
- define operational metrics;
- perform analytics;
- implement forecasting;
- implement WFM or capacity analysis;
- implement retrieval or AI;
- integrate Governed Execution;
- claim that the candidate Case contract is universally sufficient.

## Starting State

Increment 001 established and verified the repository foundation.

The repository currently contains:

    .gitignore
    README.md
    pyproject.toml
    docs/increments/001-repository-foundation.md

A repository-local `.venv/` exists as ignored generated development state.

No executable application source, canonical domain model, source adapter, database schema, test suite, or repository-validated operational dataset artifact exists in this repository.

External dataset-selection work has staged different sources for different evidentiary roles:

- Calgary 311 for case-level operational analytics;
- ServiceNow Incident Response Log for later event-level workflow evidence;
- Technion call-center data as an optional future queue/service/WFM source.

This planning evidence does not establish live source or licence verification, repository-validated acquisition, source contracts, source mappings, adapters, or empirical validation in this repository.

### Externally Reported Dataset Preparation Context

External project context reports that dataset-preparation work has produced local artifacts outside this repository under:

    /data/repos/Public Datasets

Externally reported files:

    calgary_311.csv
    incident_event_log.csv
    support_ops.duckdb

These are `EXTERNALLY REPORTED / PREPARED`, not `REPOSITORY-VALIDATED`, facts for Increment 002. This increment did not inspect that filesystem location or reproduce the reported profiles.

The externally reported Calgary profile is:

- file: `calgary_311.csv`;
- 7,474,403 rows;
- unique `service_request_id`;
- reported date range from 2010-01-25 through 2026-09-08;
- three lifecycle timestamps;
- reported request-to-closure elapsed duration calculable from `requested_date` and `closed_date`, subject to future source-contract validation;
- no assignment, dispatch, handoff, or intermediate-state timing;
- 48.2% midnight timestamps.

The externally reported ServiceNow profile is:

- file: `incident_event_log.csv`;
- 141,712 event rows;
- approximately 24,918 incidents;
- multiple rows per incident;
- state transitions;
- reassignment counts;
- reopen counts;
- assignment groups;
- event-level workflow evidence.

The additional `support_ops.duckdb` artifact is also externally reported as prepared.

The externally reported licensing context is:

- Calgary: Open Government Licence - City of Calgary;
- reported Calgary attribution: "Contains information licensed under the Open Government Licence – City of Calgary.";
- ServiceNow/UCI incident dataset: CC0.

Increment 002 did not perform authoritative-source verification, live licence verification, attribution verification, file-integrity verification, row-count or date-range reproduction, local schema validation, source-to-canonical mapping, or empirical portability validation. The reported files and prior profiles are architectural pressure-test evidence until independently inspected in the relevant implementation increment.

Increment 001 implementation commit:

    10ddecaf6de876f7c56224d8efe2b29a6d968fbd

Increment 001 documentation bookkeeping commit:

    3d383e7d0c3476bddb15f9a2253a50bbc3a60592

## Domain Question

What is the smallest case-level representation that lets later source adapters expose comparable operational records without pretending that every source observes the same fields or semantics?

## Accepted Case Qualification Contract

A canonical `Case` represents one independently identifiable, source-native unit of operational work or operational matter whose identity and meaning exist independently of individual events or observations and for which an operational disposition or outcome can meaningfully be considered.

Qualification is semantic, not based merely on the presence of particular fields. A source-native object qualifies as a Case only when all of the following conditions are satisfied.

### 1. Source-native entity

The source treats it as an identifiable object rather than merely an aggregate or anonymous observation.

### 2. Operational work semantics

The object represents a unit of operational work or operational matter handled by the operation.

### 3. Independent meaning

Its operational meaning exists independently of any individual event, message, interaction, or observation associated with it.

### 4. Bounded identity

Source semantics establish a boundary that distinguishes this work item from another work item.

### 5. Disposition semantics

Some operational condition, progression, disposition, or outcome can meaningfully apply to the work item, even if the source does not expose that lifecycle explicitly.

The central admission test is:

    Is this object the operational work item itself?

or:

    Is it evidence, activity, communication, context, a participant,
    resource, or aggregate about operational work?

Only the former qualifies for canonical Case.

Accepted qualification invariants:

1. Identity alone is insufficient for Case qualification.
2. A Case represents operational work, not merely an identifiable source record.
3. A Case has a source-supported semantic boundary distinguishing it from other work items.
4. A Case remains conceptually distinct from its events, interactions, messages, resources or entities, and aggregates.
5. A Case may have zero observed lifecycle events.
6. A Case does not require a known creation timestamp, update timestamp, closure timestamp, status, classification, organizational responsibility, assignment, customer, priority, or location.
7. Missing analytical attributes restrict analytical eligibility, not Case admissibility.
8. An interaction may qualify as a Case only when source semantics establish that the interaction itself is the operational work item.
9. A workflow execution may qualify as a Case only when source semantics establish that the workflow execution itself is the operational work item.
10. Event rows, messages, aggregates, supporting resources, and other identifiable objects must not become Cases merely because they possess identifiers.
11. Source adapters must justify why the mapped source-native object satisfies the Case admission semantics.
12. A source-native object must not be promoted to Case merely because doing so simplifies downstream analytics.

Pressure-test examples are illustrative rather than universal object-type rules:

- a Calgary 311 service request qualifies conceptually;
- a ServiceNow incident qualifies conceptually;
- an individual ServiceNow state-change row does not qualify as a Case because it is event evidence concerning a Case;
- an individual chat message normally does not qualify;
- a support conversation may qualify only if the source treats the conversation itself as the operational work item;
- an individual call-center call is not automatically a Case and may qualify only when source semantics establish that the call itself is the atomic operational work item;
- a monthly aggregate, such as "4,200 requests, median resolution 3.8 days," does not qualify;
- a workflow execution may qualify, but not automatically.

Source semantics remain decisive. `CaseEvent`, Interaction, Message, Resource, Aggregate, and WorkflowExecution are neighboring conceptual boundaries only; this increment does not prescribe or implement models for them.

## Accepted Identity Contract

The canonical Case identity core is universally required and non-null:

### case_id

Internal canonical platform identity and the authoritative identity used by downstream platform relationships.

### source_system

Identity namespace for the originating source or system.

`source_system` does not mean a source-native intake channel. For example, Calgary's native `source` field, such as Phone, Web, or App, is an intake-channel concept and must not be treated as `source_system`.

Intake and origin information is governed by the accepted non-universal boundary below; it is not canonical `source_system`.

### source_case_id

Native source identifier within the `source_system` namespace.

The authoritative source-native identity is:

    (source_system, source_case_id)

Accepted identity invariants:

1. `case_id` is the authoritative canonical identity used by downstream platform relationships.
2. `(source_system, source_case_id)` is the authoritative source-native identity.
3. `(source_system, source_case_id)` must be unique.
4. One qualifying source-native work item maps to exactly one canonical Case.
5. One canonical Case maps to exactly one qualifying source-native work item.
6. Repeated ingestion of the same `(source_system, source_case_id)` must resolve to the same canonical Case.
7. Native identifiers from different source systems may collide without creating canonical identity collisions.
8. Cross-source relationships do not merge Case identity.
9. Entity resolution is outside the current canonical ingestion boundary.
10. If a future need arises to group several Cases under a higher-level operational concept, that requires a separately justified abstraction rather than weakening Case identity.

The following identity implementation choices remain explicitly deferred:

- UUID versus integer versus another representation;
- deterministic versus generated `case_id`;
- exact database key implementation;
- cross-case relationship model;
- higher-level OperationalWork-style abstraction.

## Requiredness Contract

Only `case_id`, `source_system`, and `source_case_id` are universally required and non-null.

A Case qualifies because it is a qualifying source-native operational work item, not because its source supplies every analytical attribute downstream users may want. No other Case analytical or lifecycle attribute is universally required as a known value.

Missing evidence restricts analytical eligibility rather than automatically preventing Case admissibility. For example:

- Case ingestion requires the identity core;
- elapsed-duration analysis may additionally require usable `created_at` and a source-supported lifecycle boundary appropriate to the analysis;
- status analysis may additionally require usable status evidence;
- classification segmentation may additionally require usable classification evidence.

This requiredness decision does not imply that every non-identity concept belongs in the canonical Case contract.

## Accepted Lifecycle Timestamp Contract

### created_at

`Case.created_at` is an optional canonical lifecycle concept representing the source-supported creation boundary of the source-native operational work item. It may be established directly or through a semantically justified deterministic derivation. Its canonical representation must not imply temporal precision greater than the supporting source evidence.

Accepted `created_at` invariants:

1. `created_at` is optional.
2. It represents creation of the source-native work item.
3. It does not represent first platform observation, ingestion time, retrieval time, the earliest timestamp merely available in a dataset, or the beginning of the underlying real-world problem.
4. `created_at` may be `OBSERVED` or `DERIVED`.
5. `OBSERVED` requires source evidence whose semantics directly establish work-item creation.
6. `DERIVED` requires a documented deterministic and semantically justified rule establishing the creation boundary.
7. `MIN(event_timestamp)` does not establish creation by itself.
8. Earliest event time may be used only if source semantics establish that the qualifying event is the creation event, event history is guaranteed to begin at Case creation, or another documented source invariant establishes equivalence.
9. First-seen, retrieval, or ingestion timestamps must not populate `created_at` solely because they are the earliest platform-known timestamps.
10. Temporal representation must preserve source-supported precision.
11. Date-only evidence must not silently become an exact-midnight semantic claim.
12. Observation boundary, extract cutoff, ingestion time, and Case creation time are distinct concepts.
13. `created_at` may be `UNAVAILABLE` while the object remains a valid Case.
14. Analyses requiring creation time must apply explicit analytical eligibility requirements.

Later source contracts must preserve temporal interpretation, including timezone or offset assumptions where relevant. Physical temporal representation and any precision enum remain explicitly deferred.

Calgary `requested_date` and ServiceNow `opened_at` are provisional candidate source evidence for `created_at`, subject to future source-contract validation. Neither mapping is repository-validated.

### updated_at

`updated_at` is not a universal canonical Case field. Source-record modification, operational lifecycle change, latest event, and latest evidence observed by the platform are materially different concepts; a universal timestamp would create false comparability.

Accepted source-modification and update invariants:

1. Generic source-record modification and operational lifecycle change are distinct concepts.
2. A source modification timestamp may change because of metadata, administrative, or representation changes without an operational workflow change.
3. Source-native modification timestamps may be preserved using their actual source semantics.
4. `MAX(event_timestamp)` does not establish a generic `Case.updated_at`.
5. Operational changes represented by event-rich evidence belong conceptually to the later `CaseEvent` contract.
6. Purpose-specific temporal projections may later be introduced when a concrete analytical requirement justifies them.
7. Any such projection must define qualifying evidence or events, projection rule, observation boundary, supported temporal precision, and provenance.
8. Source modification timestamps must not by themselves establish active work, workflow progression, assignment residence, customer wait, handling time, or last meaningful agent activity.
9. Removing canonical `updated_at` does not prevent an adapter or source contract from preserving native last-modified metadata.
10. Purpose-specific projections remain analysis-specific unless repeated requirements later justify canonical promotion.

Source metadata representation, latest-event projections, `CaseEvent` implementation, and any replacement universal timestamp remain explicitly deferred.

Calgary `updated_date` is provisional source-native modification evidence until a future Calgary source contract establishes stronger semantics. It is not an observed workflow milestone.

### closed_at

`closed_at` is not a universal canonical Case scalar. Resolved, closed, completed, cancelled, abandoned, rejected, and other source-native dispositions must not be silently collapsed.

Accepted closure and disposition invariants:

1. Closure is not a universal synonym for terminal operational disposition.
2. Source-native lifecycle meanings must remain distinguishable.
3. `resolved_at` and `closed_at` are not assumed equivalent.
4. Source-native lifecycle timestamps may be preserved according to their actual source semantics.
5. Event-level lifecycle transitions belong conceptually to the later `CaseEvent` contract when event evidence exists.
6. A Case may enter a closure-like state, reopen, and later enter another closure-like state.
7. One scalar `closed_at` cannot safely imply first closure, latest-known closure, current closure, or final closure.
8. Finality must not be asserted without source evidence that establishes finality.
9. Cancellation, abandonment, rejection, or similar dispositions do not automatically establish closure.
10. Purpose-specific lifecycle projections may be derived when an analysis justifies them.
11. Such projections remain analysis-specific unless repeated requirements later justify canonical promotion.
12. Case admissibility does not require closure evidence.
13. Elapsed time from `created_at` to a source-native closure timestamp establishes only elapsed time between those two source-supported lifecycle boundaries.
14. That duration does not by itself establish active work, handling time, queue time, customer wait, assignment residence, or workflow decomposition.
15. Exact lifecycle and disposition representation remains deferred.

No generic `disposition_at` replacement or canonical disposition taxonomy is accepted.

## Accepted Status Contract

The earlier single ambiguous `status` candidate is replaced by `source_status` and `canonical_status`.

### source_status

`source_status` is the Case-level lifecycle status expressed in the originating source's native vocabulary. It is established either directly from source Case or snapshot evidence or deterministically derived from richer source evidence at a defined observation boundary.

SOURCE-NATIVE describes vocabulary and semantics. `OBSERVED` or `DERIVED` describes how the Case-level value was established. Source-native therefore does not imply `OBSERVED`.

For example, a Calgary source row containing `status_description = Closed` may establish `Case.source_status = Closed` as `OBSERVED`. An event-rich source may establish its source-native Case-level value through a documented status projection, in which case `source_status` is `DERIVED`.

Accepted `source_status` invariants:

1. `source_status` preserves source-native lifecycle semantics.
2. Source-native does not imply `OBSERVED`.
3. `source_status` may be `OBSERVED` or `DERIVED`.
4. A derived `source_status` must define its qualifying source evidence, semantically justified ordering rule, and observation boundary.
5. "Latest" must always be relative to an explicit observation boundary.
6. The observation boundary is not automatically wall-clock ingestion time.
7. A historical extract's latest known state must not automatically be called final state.
8. Lifecycle monotonicity must not be assumed.
9. Reopening may legitimately change Case-level `source_status`.
10. Ambiguous event ordering must not be resolved using arbitrary deterministic ordering.
11. Determinism is necessary for derivation but insufficient without semantic justification from source evidence.
12. If no defensible Case-level projection exists, `source_status` may be `UNAVAILABLE`.
13. Event history belongs to the later `CaseEvent` contract.
14. `Case.source_status` is a projection of source evidence and does not replace event history.

### canonical_status

`canonical_status` is an optional normalized lifecycle interpretation.

Accepted `canonical_status` invariants:

1. `canonical_status` does not replace `source_status`.
2. `canonical_status` may exist only when a defensible canonical mapping exists.
3. Normalization must be deterministic, documented, reproducible, and testable.
4. If no defensible mapping exists, `canonical_status` remains unavailable rather than forcing equivalence.
5. Cross-source analytics may use `canonical_status` only when the analytical question does not depend on distinctions lost in normalization.

The canonical status vocabulary, exact storage representation, historical Case projection/versioning, exact observation-boundary storage, and normalization implementation remain explicitly deferred.

## Accepted Classification Contract

`category` and `sub_category` are not assumed universal scalar Case fields. A Case may have zero or more classifications. Source evidence may contain no classification, one flat classification, hierarchical classifications of arbitrary supported depth, or multiple independent classification dimensions.

Accepted classification invariants:

1. Classification is not required for Case admissibility.
2. Source-native classification meaning and structure must remain traceable.
3. Source-native hierarchy must not be invented merely because labels can be syntactically split.
4. Derived groupings must remain distinguishable from source-observed classifications.
5. A canonical classification is an optional normalized interpretation.
6. Canonical classification never replaces source-native classification.
7. Canonical classification requires a documented reproducible mapping or derivation.
8. Cross-source segmentation using canonical classification is valid only when the mapping preserves the semantics required by that analytical question.
9. Source-native classification schemes do not automatically share a taxonomy.

For example, Calgary `service_name = "WRS - Cart Management"` must initially be preservable as source-native classification evidence. It must not be split into `category = WRS` and `sub_category = Cart Management` unless Calgary source semantics establish that hierarchy.

The Classification class/model, CaseClassification, JSON or relational representation, taxonomy, and normalization implementation remain explicitly deferred.

## Organizational Responsibility and Assignment

`owning_group` is not a universal scalar Case attribute. Organizational responsibility and workflow assignment are materially different concepts and must not be collapsed into a single canonical field without source evidence establishing equivalent semantics.

A Case may have source-supported organizational responsibility or assignment information, but this contract does not yet prescribe a universal field or storage structure. Responsibility describes source-supported organizational or accountability semantics. Assignment describes workflow or routing state and may be temporal. Assignment transitions belong primarily to the later `CaseEvent` contract; an optional Case projection may be defined when a justified downstream requirement exists.

Accepted organizational invariants:

1. `owning_group` is not a universal canonical Case scalar.
2. Organizational responsibility and workflow assignment are not assumed equivalent.
3. A source contract must document the meaning of any responsibility or assignment evidence.
4. Source-native organizational semantics must remain recoverable.
5. Calgary `agency_responsible` may represent source-native responsibility semantics if its source contract establishes that meaning.
6. Calgary `agency_responsible` must not automatically be interpreted as current workflow assignment.
7. ServiceNow assignment transitions belong primarily to the later `CaseEvent` contract.
8. A Case may expose an assignment projection when a downstream requirement justifies one.
9. Any Case-level assignment projection must define semantics, source evidence, observation boundary, derivation rule where applicable, and provenance state.
10. Latest known assignment must not be called final assignment without source evidence supporting finality.
11. A Case-level assignment projection must not replace or erase underlying assignment-event evidence.
12. Calgary `agency_responsible` and ServiceNow `assignment_group` are not assumed to represent an equivalent canonical organizational concept.
13. Any future cross-source organizational normalization requires a separately documented mapping justified by the analytical question.

A generic organizational-association model, CaseAssociation, Organization entity, responsibility schema, assignment schema, Case-level assignment field, storage representation, and `CaseEvent` implementation remain explicitly deferred.

## Intake and Origin Information

`intake_channel` is not a universal canonical Case field. Source system, intake or origin information, interaction channel, creation mechanism, and originating actor or system are related but materially distinct concepts.

Accepted intake and origin invariants:

1. A Case does not require intake-channel information.
2. Source system, intake or origin mechanism, interaction channel, creation mechanism, and originating actor are distinct concepts.
3. Source-native intake or origin evidence may be preserved with its actual source semantics.
4. Later interaction channels do not redefine original Case-entry context.
5. Automatically created Cases do not require a human communication channel.
6. Values such as Phone, Web, Portal, API, Monitoring, Integration, or similar labels are not assumed semantically equivalent across sources.
7. Cross-source normalization requires a documented mapping justified by a specific analytical question.
8. Calgary native `source = Phone/Web/App` remains source-native intake or origin evidence and is not canonical `source_system`.
9. Analysis-specific intake or origin projections remain analytical unless repeated requirements justify canonical promotion.

Creation-origin information may later be represented through an event, origin, lineage, or another explicitly justified structure. Increment 002 does not prescribe that representation. Intake-channel taxonomy, origin model, creation-event model, actor/origin relationship, storage representation, and `CaseEvent` placement remain explicitly deferred.

## Priority-Like Information

Neither universal `Case.priority` nor `canonical_priority` is established. Priority, severity, urgency, impact, SLA treatment, risk, dispatch precedence, customer entitlement, and queue position are materially distinct and are not assumed equivalent.

Accepted priority-like invariants:

1. Priority-like concepts are source- and policy-dependent.
2. A Case does not require priority-like information for admission.
3. Priority, severity, urgency, impact, SLA treatment, risk, and queue position are not assumed equivalent.
4. Source-native priority-like information must remain recoverable with its actual source semantics.
5. Priority-like values may change over time.
6. Initial, current, latest-known, highest-observed, and purported final priority are not interchangeable.
7. A scalar `Case.priority` must not collapse temporal priority history.
8. No canonical priority taxonomy is established.
9. Cross-source normalization may be created only for a specific analytical question with an explicit and semantically justified mapping.
10. Such normalization remains analytical unless repeated evidence justifies later canonical promotion.
11. A source value directly supplied to this platform may be `OBSERVED` from this platform's perspective even if the source system computed it internally.

Priority taxonomy, priority history model, `CaseEvent` representation, normalization scheme, and storage representation remain explicitly deferred.

## Customer and Actor Identity

Neither universal `Case.customer_id` nor a replacement scalar such as `party_id`, `actor_id`, or `requester_id` is established. Customer, requester, caller, affected user, `opened_by`, reporter, account, tenant, organization, beneficiary, and system actor are materially distinct and are not assumed equivalent.

Accepted customer and actor invariants:

1. A Case does not require a customer, requester, person, account, tenant, or organization relationship for admission.
2. Customer, requester, caller, affected user, `opened_by`, reporter, account, tenant, organization, and beneficiary are not assumed equivalent.
3. A Case may relate to zero, one, or multiple source-native actors or organizations.
4. Source-native actor roles and identifiers must remain distinguishable and recoverable where material.
5. Source-native actor identifiers remain scoped to their source-defined identity namespace unless explicit identity resolution establishes otherwise.
6. A scalar `Case.customer_id` must not collapse multiple actor roles.
7. Cross-case or cross-source actor, person, or organization linkage must not be inferred merely because identifiers are technically joinable.
8. Any future actor, party, or customer normalization requires a separately justified relationship model and identity-resolution policy.
9. Privacy and source-use constraints must be considered before persistent cross-case or cross-source identity linkage.
10. Increment 002 does not require every source-native actor relation to become part of canonical Case output.

Relevant source actor and entity semantics must remain preservable and must not be silently collapsed. Actor, Party, Person/Organization hierarchy, CaseActorRelationship, identity-resolution system, privacy architecture, and relationship storage remain explicitly deferred.

## Location and Context

Universal `Case.location` is not established. Service location, requester location, affected-asset or affected-resource location, organizational region, physical address or geography, geographic coordinates, logical or cloud region, jurisdiction, and community or neighborhood are materially distinct and are not assumed equivalent.

Accepted location and context invariants:

1. Location is not one universal source-independent Case concept.
2. Service location, requester location, affected-resource location, organizational region, physical geography, logical or cloud region, and jurisdiction are not assumed equivalent.
3. A Case may have zero, one, or multiple relevant location or context relationships.
4. Location-like information may describe an actor, asset, service, organization, jurisdiction, or operational context rather than the Case itself.
5. Source-native spatial or contextual evidence must remain preservable with its actual source semantics.
6. Calgary address, community, location type, and coordinates remain usable for Calgary-specific analysis even though no universal `Case.location` exists.
7. Physical geography and logical or service regions must not be collapsed into one location dimension.
8. Cross-source geographic normalization requires a specific analytical question and documented mapping.
9. Analysis-specific spatial dimensions remain analytical unless repeated evidence justifies canonical promotion.

Spatial ontology, geographic model, resource-location model, jurisdiction model, relationship structure, and storage representation remain explicitly deferred.

## Accepted Hybrid Field-Provenance Contract

The accepted provenance architecture is hybrid:

    canonical value
        +
    cheap downstream visibility of field evidence state
        +
    detailed lineage separately available

This contract does not prescribe the physical storage representation.

High-level field states are:

### OBSERVED

A canonical value has been established directly from source evidence.

### DERIVED

A canonical value has been established through a documented deterministic and semantically justified transformation.

### UNAVAILABLE

No canonical value is established at the relevant observation boundary.

`UNAVAILABLE` describes canonical-value state. It does not necessarily mean that no relevant source evidence exists.

### SIMULATED

A canonical value has been established through a declared simulation.

These states describe canonical field provenance/status.

They must not be conflated with the project's broader analytical claim categories:

    OBSERVED
    DERIVED
    ASSUMPTION
    HYPOTHESIS
    SIMULATION
    RECOMMENDATION

A derived canonical field is not automatically a derived analytical finding.

Accepted provenance invariants:

1. Canonical values remain directly usable by domain, SQL, API, and analytics consumers.
2. Downstream consumers must have efficient access to high-level field state without reconstructing full lineage.
3. State does not contain the entire explanation.
4. NULL means only that no canonical value is currently established.
5. NULL alone must not explain why a value is absent.
6. A potentially derivable value is not `DERIVED` until the documented derivation actually establishes a value.
7. Deterministic computation alone does not make a derivation valid; it must be semantically justified.
8. `SIMULATED` values must remain distinguishable from empirical values.
9. Derived values may depend on other derived values.
10. Transformation lineage must remain recoverable.
11. Analytical eligibility depends on evidence state and the requirements of the analysis, not merely SQL nullness.
12. Scenario analyses may explicitly permit `SIMULATED` evidence, while empirical metrics must not silently include it.

Detailed lineage should be capable of retaining, where applicable:

- source evidence;
- source fields or events;
- derivation rule;
- rule version;
- observation boundary;
- ambiguity or limitation;
- transformation chain.

Adjacent `<field>_state` columns, value wrappers, lineage tables, JSON lineage, API representation, exact reason-code enums, and persistence implementation remain explicitly deferred.

## Accepted Unavailability Reasons

Every implementation must preserve at least five materially distinct conceptual conditions beneath `UNAVAILABLE`. Exact enum names are not frozen.

### VALUE_ABSENT

The source models the concept, but the source record has no usable value at the relevant observation boundary.

### CONCEPT_ABSENT

The source does not represent an equivalent canonical concept.

### EVIDENCE_INDETERMINATE

Relevant source evidence exists, but it cannot establish one defensible canonical value. At the minimum contract level this may include insufficient, ambiguous, or conflicting evidence; detailed lineage may distinguish these further.

### TRANSFORMATION_NOT_APPLIED

A specific applicable transformation is defined, but it has not been executed for the value. A merely possible future transformation does not satisfy this condition.

### TRANSFORMATION_UNRESOLVED

The applicable transformation was executed, but no defensible canonical value could be established.

An unavailability reason identifies the boundary preventing establishment of the canonical value rather than merely restating that the value is NULL:

    source record
        -> VALUE_ABSENT

    source model
        -> CONCEPT_ABSENT

    source evidence
        -> EVIDENCE_INDETERMINATE

    transformation execution
        -> TRANSFORMATION_NOT_APPLIED

    transformation result
        -> TRANSFORMATION_UNRESOLVED

No additional top-level reason code is accepted without evidence. Exact enum spellings and implementation representation remain deferred.

## Accepted Source-Adapter Conformance Contract

A source adapter is conformant with the canonical Case contract only when it can demonstrate that emitted canonical Cases preserve the semantic and evidentiary boundaries of the canonical model. Successful parsing, schema validation, type conversion, or row conversion alone is insufficient.

An adapter is not merely a schema converter. It is the semantic boundary that must justify the claims introduced while translating source evidence into canonical representation.

### 1. Case admission

Every adapter must justify why the source-native object satisfies the accepted Case admission semantics. It must establish that the object is an identifiable source-native entity; a unit of operational work or operational matter; independently meaningful apart from individual events, messages, or observations; bounded from other work items by source-supported semantics; and capable of meaningful operational progression, disposition, or outcome.

Identity alone is insufficient. If Case admission cannot be justified, the adapter must not emit a canonical Case. This is a Case-level conformance failure, not an optional field with state `UNAVAILABLE`.

### 2. Identity core

Every emitted Case must establish `case_id`, `source_system`, and `source_case_id`. `case_id` remains the authoritative canonical identity, and `(source_system, source_case_id)` remains the authoritative source-native identity.

The adapter or source contract must establish:

- `source_system` namespace meaning;
- source-native identity source or rule;
- one source-native work item to one canonical Case;
- one canonical Case to one qualifying source-native work item;
- repeat ingestion resolving the same source identity to the same canonical Case;
- native identifier collisions across systems not merging Cases.

If required identity cannot be established reliably, the adapter must not emit a canonical Case. UUID, integer, deterministic, generated, and other physical identity choices remain deferred.

### 3. Semantic mapping justification

For every mapping into a canonical concept, documentation must establish the source evidence, source-native meaning, target canonical concept, and semantic justification. Similar names, similar data types, schema position, and implementation convenience are insufficient. Semantic equivalence must be supported by the source contract.

### 4. Material non-canonical source evidence

An adapter is not required to copy every source field into the canonical model. Source-native evidence material to mapping, interpretation, reproducibility, or known source limitations must remain recoverable or be explicitly accounted for. Evidence intentionally excluded from canonical output must not be silently treated as nonexistent.

The exact mechanism remains deferred. Future mechanisms might include source references, retained raw evidence, lineage, source-contract documentation, or another justified structure, but this contract selects none.

Examples that must not be silently reinterpreted include Calgary's native `source` intake/origin information, `updated_date` modification evidence, `agency_responsible` responsibility semantics, and spatial or community information. These examples do not require universal canonical fields.

### 5. Field evidence state

Every canonical value requiring evidence-state tracking must preserve the accepted high-level state: `OBSERVED`, `DERIVED`, `UNAVAILABLE`, or `SIMULATED`. Evidence state must not be inferred solely from SQL nullability.

A value supplied directly to this platform by a source may be `OBSERVED` from the platform's perspective even when the originating system computed it upstream. It must not be labeled platform-`DERIVED` unless this platform actually performs the derivation being claimed.

### 6. Unavailability reason

When no canonical value is established, the implementation must preserve the applicable conceptual distinction among `VALUE_ABSENT`, `CONCEPT_ABSENT`, `EVIDENCE_INDETERMINATE`, `TRANSFORMATION_NOT_APPLIED`, and `TRANSFORMATION_UNRESOLVED`.

Exact enum spelling remains deferred. `TRANSFORMATION_NOT_APPLIED` requires a specific applicable transformation that is defined but has not executed; a transformation that merely might exist does not qualify.

### 7. Derivation and normalization

Every platform-produced `DERIVED` value must have a documented, reproducible rule identifying, where applicable, input evidence, qualifying records or events, transformation logic, ordering semantics, observation boundary, rule identity or version, and expected failure conditions.

The transformation must be deterministic and semantically justified. Determinism alone is insufficient, and an adapter must not fabricate a canonical value merely because an arbitrary deterministic rule can produce one.

### 8. Temporal semantics

Every temporal canonical mapping or derivation must document, as applicable, lifecycle meaning, supported temporal precision, timezone or offset interpretation, and observation boundary.

Source lifecycle time, source extract or evidence cutoff, platform ingestion time, and platform first-seen time must remain distinct and must not be substituted for one another. Temporal precision must not be manufactured. A date-only value must not silently become an evidentiary claim of exact midnight unless source semantics establish midnight.

### 9. Source-native and canonical semantics

Where source-native and normalized canonical interpretations both exist, source-native meaning must remain recoverable. This applies to `source_status` and `canonical_status`, and to source-native and canonical classification.

Canonical normalization must not erase source meaning. Source-specific organizational responsibility, assignment, actor or customer roles, intake or origin fields, priority-like fields, and location or spatial context must not be promoted into universal canonical concepts unless this contract explicitly establishes such a concept.

### 10. Semantic mismatches

Material near-matches between source and canonical concepts must be documented. For example:

- Calgary `updated_date` may resemble generic update time but does not establish workflow progression;
- Calgary native `source` may resemble source identity but is not canonical `source_system`;
- ServiceNow `assignment_group` may resemble organizational ownership but is workflow-assignment evidence.

These mismatches are conformance evidence because they prevent future consumers from assuming false semantic equivalence.

### 11. Missingness and indeterminacy characterization

Adapters or source contracts must retain enough information to distinguish source concept absent; source field present but no usable record value; malformed evidence; insufficient evidence; ambiguous or conflicting evidence; applicable transformation not executed; and transformation executed but unresolved.

No additional canonical reason enum is introduced here. Detailed distinctions may remain in lineage or source-contract evidence under the accepted field-state and unavailability-reason model.

### 12. Source limitations

Every adapter or source contract must state material conclusions the source evidence does not support. For Calgary, requested, updated, and closed timestamps do not by themselves establish assignment timing, dispatch timing, queue residence, active work time, customer wait, handoff wait, rework intervals, or workflow decomposition.

Conformance includes explaining what the source cannot justify, not only which canonical values can be populated.

### 13. Reproducibility

Given an equivalent source version or extract, source evidence, adapter version, configuration, and mapping rules, the semantic canonical interpretation must be reproducible unless a contract explicitly defines otherwise. This applies especially to source identity mapping, derivations, normalization, temporal projections, and missingness classification.

Increment 002 does not choose how canonical `case_id` is generated and does not require a clean rebuild to reproduce the exact internal `case_id` unless a later identity-generation contract establishes that requirement. Repeated ingestion within the accepted identity contract must still resolve a known source identity to the same canonical Case.

### 14. Source, version, and acquisition provenance

The system must retain or reference enough provenance to reconstruct source or dataset identity; relevant version or extract; authoritative origin where established; source schema or contract version; adapter or mapping version; and evidence supporting derived canonical values.

For public data, the broader acquisition and source-contract process should eventually preserve, where applicable, authoritative source, retrieval date, extract or version identity, current licence or attribution evidence, and file hash or equivalent reproducibility identifier.

This is a system-level reproducibility obligation. The source adapter is not required to own every acquisition or licensing artifact. Increment 002 does not prescribe whether the obligation belongs to a source contract, acquisition artifact, adapter metadata, lineage, or another implementation component.

### 15. Reject rather than fabricate

Two failure levels are preserved.

**Case-level conformance failure:** If an adapter cannot establish Case admission or the required identity core, it must not emit a canonical Case. Source evidence may later be retained as rejected or unmapped input, but Increment 002 does not prescribe that storage structure.

**Optional-concept failure:** If the Case is admissible and required identity is valid but an optional canonical value cannot be established, the adapter emits the Case. The optional value remains unestablished with state `UNAVAILABLE` and the applicable reason. The adapter must not invent a value to create a complete-looking record.

## Calgary Conceptual Adapter Pressure Test

The following is a conceptual engineering/design pressure test, not a repository-validated mapping:

    City of Calgary service request
        -> candidate admissible Case

    service_request_id
        -> source_case_id

    source_system
        -> calgary_311 namespace

    case_id
        -> canonical internal identity

    requested_date
        -> candidate created_at
           only after source semantic validation

    status_description
        -> candidate source_status
           preserving Calgary vocabulary

    service_name
        -> source-native classification

    agency_responsible
        -> source-native responsibility evidence

    native source = Phone/Web/App
        -> Calgary-defined intake/origin evidence
           NOT source_system

    updated_date
        -> source-native modification evidence
           NOT universal Case.updated_at

    address/community/coordinates
        -> Calgary-specific spatial evidence
           NOT universal Case.location

No mapping above is empirically validated by Increment 002.

## Accepted Adapter Conformance Summary

A conformant source adapter or source contract must:

1. justify Case admission;
2. establish required identity and identity invariants;
3. justify every canonical semantic mapping;
4. account for material non-canonical source evidence;
5. assign correct evidence state;
6. preserve required unavailability distinctions;
7. document and reproduce every platform derivation or normalization;
8. preserve temporal meaning and evidence boundaries;
9. preserve source-native meaning alongside normalization;
10. document material semantic mismatches;
11. characterize missingness and indeterminate evidence;
12. state known source limitations;
13. support reproducible semantic interpretation;
14. bind output to sufficient source and version provenance;
15. reject Case emission when admission or required identity fails while preserving valid Cases with unavailable optional concepts.

YAML, JSON, Python interfaces, validation frameworks, source-contract file formats, database tables, lineage schemas, adapter class hierarchies, and storage architecture remain explicitly deferred.

## Reconciled Contract Invariants

The qualification, identity, lifecycle timestamp, status, classification, provenance, unavailability, organizational, intake/origin, priority-like, customer/actor, and location/context invariants accepted above replace the earlier candidate treatment for those subjects.

An engineering review audit traced the ten original candidate invariants to the stronger accepted contracts above and concluded `NO_NEW_INVARIANT_REQUIRED`. No additional semantic invariant requires a new human design decision before Increment 002 can proceed. The detailed accepted contract sections remain authoritative; the following reconciliation records status only and does not create a second specification:

| Original candidate idea | Reconciliation classification | Governing accepted contract |
| --- | --- | --- |
| Non-empty or established canonical identity | `ACCEPTED_WITH_REFINEMENT` | Every emitted Case establishes the required, non-null identity core; admission or identity failure prohibits Case emission. Physical `case_id` type remains deferred. |
| Identity uniqueness within source scope | `ACCEPTED_WITH_REFINEMENT` | `case_id` is authoritative canonical identity; `(source_system, source_case_id)` is unique authoritative source-native identity with one-to-one and repeated-ingestion guarantees. |
| Preserve `created_at` temporal meaning | `ACCEPTED_WITH_REFINEMENT` | Optional `created_at` preserves source-supported creation meaning, precision, applicable timezone or offset interpretation, and separation from ingestion, first-seen, retrieval, and extract time. |
| Deterministic documented derivation | `ACCEPTED_WITH_REFINEMENT` | A platform-produced `DERIVED` value must be deterministic, semantically justified, documented, and reproducible under the accepted derivation contract. |
| `OBSERVED` traceable to source evidence | `ACCEPTED_AS_WRITTEN` | `OBSERVED` means this platform established the canonical value directly from supplied source evidence, including a directly supplied value computed upstream. |
| `SIMULATED` not represented as observed | `ACCEPTED_AS_WRITTEN` | `SIMULATED` remains distinct from empirical evidence, must not silently become `OBSERVED` or `DERIVED`, and must not silently enter empirical metrics. |
| `UNAVAILABLE` distinguishable from observed null | `ACCEPTED_WITH_REFINEMENT` | `UNAVAILABLE` means no canonical value is established at the observation boundary; NULL alone is insufficient, and the five accepted material reason distinctions apply. |
| Optional fields not mandatory for analytical convenience | `ACCEPTED_WITH_REFINEMENT` | Case admissibility remains distinct from analytical eligibility; only identity is universally required, and analyses define their own evidence-eligibility requirements. |
| Preserve material source limitations | `ACCEPTED_AS_WRITTEN` | Canonicalization and adapter conformance preserve material source-native meaning, document semantic mismatches and unsupported conclusions, and retain evidentiary limitations. |
| Adapter failure when required identity cannot be established | `ACCEPTED_WITH_REFINEMENT` | Admission or required-identity failure prohibits Case emission; optional-concept failure emits the valid Case with `UNAVAILABLE` and an applicable accepted reason rather than fabricating a value. |

The following general invariants are also accepted:

1. A field marked `OBSERVED` must be traceable to source evidence.
2. A field marked `SIMULATED` must not be represented publicly as observed.
3. Optional evidence must not become mandatory merely to simplify downstream analytics.
4. Canonicalization must preserve material source limitations.
5. A source adapter must fail explicitly when the required identity core cannot be established.
6. Operational intervals, transitions, or workflow states may be represented as observed only when source evidence directly establishes the defining events or states required for that interpretation.

The accepted adapter conformance contract governs admission, mapping, evidence state, limitations, rejection, and reproducibility without selecting an implementation representation. The accepted provenance contract governs any canonical value that is retained or later accepted.

## Accepted Falsification and Revision Framework

The canonical Case abstraction is provisional and falsifiable. Its current working assumption is:

    one source-supported independently meaningful operational work item
        <->
    one canonical Case

with authoritative source-native identity currently represented by:

    (source_system, source_case_id)

The abstraction remains acceptable only while evaluated operational sources can be represented without inventing, collapsing, or arbitrarily splitting operational work-item boundaries. Universal portability is not claimed. Portability is an empirical property to be tested against additional source mappings and source classes.

### Evaluation Outcomes

#### WEAKEN

Evidence reduces confidence in portability, but the current Case contract remains usable without semantic modification. Unusual source lifecycle semantics, many unavailable optional concepts, or substantial source-specific contextual evidence may weaken confidence. Inconvenience alone is not falsification.

#### REFINE

Case still appears to be the appropriate abstraction, but an accepted admission, identity, or semantic invariant must be narrowed or changed. Evidence may support `REFINE` when source identifiers require a source-supported epoch or version; source identity changes while operational continuity remains; source-supported identity alias or history becomes necessary; or a legitimate source exposes operational work only through evidence from which a work-item entity could be reconstructed, requiring reconsideration of the current source-native-entity requirement.

`REFINE` means the Case contract itself changes.

#### EXTEND

Case remains valid under the existing definition, but another neighboring abstraction or relationship is required to represent additional operational structure. Examples may include a higher-level operational matter spanning several Cases; a lower-level WorkUnit or Task beneath a Case; evidence-backed split, merge, or migration relationships; or neighboring actor, resource, or work structures.

`EXTEND` must not hide an unresolved Case boundary. If multiple nesting levels appear to satisfy Case admission and no principled reason selects one operational level as Case, that is evidence for `REFINE`, not merely `EXTEND`.

#### REJECT

The evaluated source mapping cannot satisfy the current Case contract without semantic fabrication. Reasons include inventing a work-item boundary unsupported by source semantics; collapsing independently meaningful work items into one Case; arbitrarily splitting one source-supported work item into multiple Cases for analytical convenience; speculative entity resolution; asserting stable identity that source evidence cannot support; or making canonical Case identity depend on the analytical question.

`REJECT` applies initially to the evaluated source mapping. Rejection must not be generalized to an entire source class without sufficient representative evidence.

### One-to-One Boundary Pressure Test

The current one-source-work-item-to-one-Case assumption is challenged when source-native identity and operational work-item identity do not align. Pressure cases include:

1. one source record represents several independently managed work items;
2. several source records are merely shards, revisions, or views of one continuing work item;
3. one work item splits into several independently managed work items;
4. several work items merge into another work item;
5. source identity changes while operational continuity remains;
6. identifiers are reused for distinct work items;
7. source migration changes system or identifier while a higher-level operational matter continues;
8. nested operational objects exist at several meaningful levels.

This pressure test does not prescribe a relationship implementation.

### Identity Pressure Test

`(source_system, source_case_id)` remains the current authoritative source-native identity. Future evidence materially challenges that contract when the same source pair may legitimately identify different work items over time; the operational work item persists while its only source-supported identifier changes; repeated ingestion cannot determine whether two observations refer to the same work item; or stable identity requires speculative inference.

If another source-supported discriminator can restore identity unambiguously, the evidence supports potential `REFINE`. If identity cannot be restored without guessing, the evaluated source mapping is `REJECT` under the current Case contract. This framework does not choose an identity-history or alias representation.

### Event-Only Source Boundary

An event-only source may satisfy the current contract when the source evidence itself exposes a source-supported work-item entity and identity that satisfy Case admission.

If no source-native work-item entity exists, but a work-item boundary could be deterministically reconstructed from source-supported event semantics, that evidence may indicate a need to `REFINE` the Case contract. Increment 002 does not currently admit such a derived Case entity.

If event grouping requires analytical assumptions, clustering, heuristics, or speculative entity resolution, the grouping must not map to canonical Case under the current contract. Technical grouping capability does not establish operational identity.

### Analysis-Independent Identity

Analytical purpose may change cohorts, filters, windows, metrics, projections, and aggregations. It must not redefine canonical Case identity.

If the same source evidence requires materially different Case boundaries depending on the analytical question, the current Case abstraction is not functioning as stable canonical identity for that source mapping. The mapping is `REJECT` under the current contract unless a principled contract `REFINE` resolves the issue.

### Nesting, Split, Merge, and Migration

A Case may participate in larger or smaller operational structures without invalidating Case. Conceptual examples include:

    higher-level operational matter
        -> several Cases

    Case
        -> lower-level tasks or work units

    Case A
        -> splits into Cases B and C

    Case A + Case B
        -> related to Case C

    System A Case
        -> migration relationship
        -> System B Case

No required physical relationship model is selected. If the existing Case boundary remains independently defensible, `EXTEND` may be sufficient. If additional structures reveal that the Case admission boundary itself is ambiguous or overbroad, the result is `REFINE`. If no source-supported boundary can be established, the evaluated mapping is `REJECT`.

### Overbreadth and Underbreadth Tests

Case admission is potentially too broad when event, message, or activity artifacts pass admission merely because they are actionable; several nesting levels routinely qualify without a principled operational boundary; parent and child admission causes semantic double counting; or nearly every identifiable process artifact qualifies as Case. Such evidence requires `REFINE` before stronger admission wording is added. No new "primary managed work-item" invariant is established here.

Case admission is potentially too narrow when legitimate bounded operational work repeatedly exists and source-supported operational boundaries are clear, but the source does not expose a durable native Case-like entity. The current contract does not automatically admit a platform-derived Case entity. Such evidence would challenge the source-native-entity requirement and could justify future `REFINE`.

### Source-Implementation Dependence Test

Confidence in the abstraction is weakened if equivalent operational processes are admitted or rejected primarily because systems persist records differently rather than because of operational semantics. A pressure pattern may compare:

    System A
        -> durable ticket record

    System B
        -> event stream

    System C
        -> conversation and messages

    System D
        -> workflow execution and tasks

The intended abstraction is driven by operational semantics, but the current source-native-entity requirement remains accepted until future evidence justifies refinement.

### Compact Rejection Criterion

The current Case abstraction must be rejected for an evaluated source mapping when representing that source would require inventing an operational work-item boundary unsupported by source semantics, collapsing independently meaningful work items, splitting a source-supported work item for analytical convenience, asserting identity continuity the evidence cannot support, or making canonical identity depend on the analytical question.

This is a design-level falsification criterion, not an empirical finding about Calgary, ServiceNow, or any source class.

### Evaluation Questions

1. Can one operational work item be identified without inventing it?
2. Can repeated observation refer defensibly to the same work item?
3. Can neighboring work items remain distinct?
4. Can source-supported work boundaries be preserved?
5. Can the analytical question change without changing canonical Case identity?

Repeated failure of these tests is not merely a missing canonical field. It is evidence that the Case abstraction requires refinement or rejection for the evaluated mapping.

## Analytical Boundaries

Case-level data alone must not automatically support conclusions about:

- active work time;
- queue residence;
- handoff count;
- reassignment count;
- workflow path;
- causal reason for delay;
- employee productivity;
- customer effort;
- staffing sufficiency;
- knowledge-access difficulty;
- root cause.

Those conclusions require additional evidence or richer event/workflow data.

Externally reported Calgary evidence is staged for case-level operational analytics, including request-to-closure elapsed duration, volume, segmentation, status, service, responsible agency, intake channel, temporal patterns, and data quality. Calgary `requested_date` is provisional candidate evidence for a source-supported request creation boundary, and `closed_date` is provisional candidate evidence for a source-native closure boundary, subject to future Calgary source-contract validation.

Pending that validation, the directly defensible analytical concept is `REQUEST-TO-CLOSURE ELAPSED DURATION`. It must not automatically be called resolution duration, active work time, handling time, queue time, workflow duration, or workflow decomposition.

Calgary requested, updated, and closed timestamps do not establish customer wait, handoff wait, rework duration, assignment residence, or workflow decomposition. They must not be presented as an observed workflow decomposition, and elapsed time between a creation boundary and closure-like boundary must not be presented as active work time.

Any synthetic Calgary workflow decomposition, if ever created, must remain `SIMULATED` and must not be used as empirical evidence explaining where the externally reported request-to-closure elapsed duration actually went.

Externally reported ServiceNow evidence is staged for event-level workflow analysis and may expose distinct lifecycle evidence such as opened, resolved, closed, state transitions, and reopen evidence. Because that source is reported as event-rich, it is the preferred future source for empirical workflow decomposition.

Time to resolution, resolution-to-closure delay, reopen after resolution, reopen after closure, and closure cycles remain candidate analyses until the local dataset and source semantics are inspected and validated in a relevant future increment. These concepts are not imported into Case merely because they may be available from that source, and their implementation remains outside Increment 002.

## Resolved Design Questions

The invariant-design question is resolved by the reconciliation above, and the accepted falsification and revision framework resolves how future source evidence should weaken, refine, extend, or reject the Case abstraction or an evaluated source mapping.

`NO_SUBSTANTIVE_DESIGN_QUESTION_REMAINS`.

No substantive design question remains.

## Planned Implementation

This increment is initially documentation and domain-model reasoning only.

No Python implementation is authorized by this record yet.

After the contract is reviewed, a later increment may implement a machine-readable representation if doing so supports an actual source adapter or analytical interface.

## Planned Verification

For this contract increment, verification should include:

- terminology consistency with README.md;
- explicit distinction between field provenance and analytical claim classification;
- no source-specific assumptions embedded as universal canonical semantics;
- no unsupported requirement that every source populate every field;
- no workflow inference from case-level timestamps;
- explicit treatment of unavailable source information;
- preservation of the accepted identity, status, classification, provenance, unavailability, and organizational boundaries;
- preservation of the accepted `created_at`, source-modification, and closure/disposition boundaries;
- preservation of the accepted semantic Case admission boundary;
- preservation of the accepted source-adapter conformance obligations and failure levels;
- preservation of the accepted intake/origin, priority-like, customer/actor, and location/context boundaries;
- explicit disposition of the invariant-design question and the falsification and revision question;
- `git diff --check`.

No executable test is required unless executable behavior is introduced.

## Completion Review

**Result:** `READY_TO_COMPLETE`

The read-only completion review observed:

- the bounded semantic objective was satisfied;
- scope and non-goals were respected;
- no substantive design question remains;
- the core Case contract is internally consistent;
- the source-adapter conformance contract is internally consistent;
- provenance and unavailability semantics are internally consistent;
- Calgary and ServiceNow remain conceptual or externally reported pressure-test context rather than repository-validated empirical results;
- the falsification and revision framework is present;
- no material completion blocker was found.

Documentation verification observed that `git diff --check` passed with no output and a direct trailing-whitespace scan found no trailing whitespace. These are documentation verification observations, not implementation tests. No implementation test was performed or required for this documentation and domain-contract increment.

Increment 002 is complete because it established the intended semantic boundary for canonical Case representation, source-adapter conformance, provenance, analytical limitations, and falsification and revision criteria without implementing deferred physical representations or claiming empirical portability.

Future implementation or empirical work does not reopen this increment unless evidence requires revision of an accepted contract decision.

## Failure Criteria

Increment 002 should not be considered complete if:

- identifiable events, messages, resources, or aggregates can be admitted as Cases without satisfying the operational-work semantics;
- the model assumes one specific source schema;
- synthetic or simulated fields can be mistaken for observed data;
- unavailable values collapse silently into ordinary nulls;
- derived values lack defined derivation semantics;
- source-specific meaning is erased by canonicalization;
- required fields are selected only for downstream convenience;
- case timestamps are interpreted as active work without evidence;
- workflow claims are made without event-level evidence;
- the contract cannot explain how a later source adapter maps into the model.

## Skills Practiced

### Practiced

- operational domain modeling;
- schema reasoning;
- semantic boundary definition;
- data-contract design;
- evidence classification;
- identity design;
- missingness reasoning;
- normalization boundaries;
- temporal semantics;
- source/canonical separation;
- architecture reasoning;
- scope control.

### Refreshed

- data modeling;
- timestamp semantics;
- missing-data reasoning;
- identifier design.

### Newly Developed

- explicit field-level provenance/status modeling across heterogeneous operational sources.

### Maintained

- claim discipline;
- incremental engineering;
- reproducibility;
- evidence-before-assumption reasoning.

### Deliberately Not Practiced

Not relevant yet:

- dataset profiling;
- SQL;
- metric implementation;
- visualization;
- statistics;
- workflow reconstruction;
- forecasting;
- WFM;
- business-case modeling;
- retrieval;
- RAG;
- AI workflows.

## Required Human Explanation Before Implementation

Before any executable canonical Case model is created, the project owner should be able to explain in their own words:

1. why a canonical Case is useful;
2. why it must not erase source semantics;
3. the difference between `UNAVAILABLE` and an observed null;
4. the difference between an `OBSERVED` field and a `DERIVED` field;
5. why request-to-closure elapsed duration is not automatically active work time;
6. why Case and CaseEvent should remain separate concepts.

These explanations are part of the skills-development purpose of the project.

## Observed Result

Human-reviewed decisions have established:

- semantic Case admission through source-native entity, operational-work, independent-meaning, bounded-identity, and disposition conditions;
- a three-part canonical and source-native identity contract;
- identity-core requiredness and analytical-eligibility boundaries;
- optional canonical `created_at` semantics and removal of universal `updated_at` and `closed_at`;
- mandatory semantic source-adapter conformance and Case-level versus optional-concept failure behavior;
- non-universal intake/origin, priority-like, customer/actor, and location/context semantics;
- separate source-native and optional canonical status semantics;
- classification multiplicity without a universal category/sub-category hierarchy;
- hybrid field-state visibility with separately recoverable detailed lineage;
- five conceptual unavailability conditions;
- separation of organizational responsibility from temporal workflow assignment;
- an explicit evidence boundary for operational intervals, transitions, and workflow states;
- an accepted design-level falsification and revision framework with `WEAKEN`, `REFINE`, `EXTEND`, and `REJECT` outcomes.

Externally reported Calgary and ServiceNow concepts and profiles provided conceptual pressure testing for these decisions. This is an engineering/design observation, not empirical validation of source mappings or cross-source portability. Increment 002 did not acquire data, inspect the reported external dataset root, reproduce the reported profiles, or create executable behavior, operational capability, a source contract, an adapter, or a persistence structure.

## Failures / Negative Results

None yet.

## Claim Classification

**Design choices:** establish semantic Case admission, source-scoped identity, identity-only universal requiredness, optional source-supported `created_at`, no universal `updated_at` or `closed_at`, native-plus-optional-canonical status, non-scalar classification semantics, hybrid provenance, explicit unavailability reasons, separation of responsibility from assignment, mandatory semantic source-adapter conformance, non-universal intake/origin, priority-like, customer/actor, and location/context semantics, and the falsification and revision framework before implementing persistence or adapters.

**Engineering review observation:** the completed invariant audit found that the stronger accepted contracts already reconcile all ten original candidate invariants and that no new invariant requires a human design decision.

**Engineering review observation:** the completion review found `READY_TO_COMPLETE`, and documentation verification found no diff-check or trailing-whitespace error.

**Engineering/design observation:** known Calgary and ServiceNow concepts have conceptually pressure-tested the contract and exposed different case-level and event-level evidentiary roles.

**External/preparation context:** reported Calgary and ServiceNow characteristics were not independently validated by this repository.

**Research/engineering hypothesis:** a small canonical Case abstraction can support comparable downstream operational analysis without erasing material source-specific semantics. Portability across additional sources remains a research hypothesis.

**Future evaluation result:** any future `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` determination depends on evidence from the evaluated source mapping.

**Not claimed:** universal portability; empirical Calgary validation; empirical ServiceNow validation; source-adapter implementation; source-contract implementation; persistence implementation; `CaseEvent` implementation; or operational capability. Calgary and ServiceNow examples remain conceptual pressure tests unless separately validated.

Actual cross-source portability is not established. Dataset research and the reported prepared profiles are external project/preparation evidence, not repository-validated observations. Live source and licence validation were not performed in this repository.

## Threats to Validity

Conceptual review against known Calgary and ServiceNow source concepts does not establish that the contract is sufficient or portable against acquired records.

The contract may still contain unnecessary abstractions or omit important source concepts. Source summaries can also omit null behavior, temporal ambiguity, extract boundaries, or source constraints that appear only in acquired records and authoritative source documentation.

The contract should therefore remain revisable when source evidence becomes available.

## Reproducibility Notes

This reconciliation is reproducible from the accepted design decisions retained in this record and the externally reported conceptual source evidence summarized above. Increment 002 did not inspect the reported prepared files, query live APIs, implement executable models, or implement source mappings.

Before source acquisition or republication, implementation must separately verify the authoritative current source, current licence, required attribution, retrieval date, acquisition mechanism, and redistribution constraints.

## Artifacts

Current documentation artifact:

    docs/increments/002-canonical-case-contract.md

## Commit

Not yet committed.

# Increment 003 - Calgary Source Evidence Validation

**Status:** Planned
**Opened:** 2026-09-10

## Objective

Establish a repository-validated evidence baseline for the local City of Calgary 311 dataset before defining a Calgary source contract or canonical adapter mapping.

This increment should determine what source artifact is actually present, what its observable structure and lifecycle evidence support, and what provenance, licensing, and version assumptions can be substantiated. It does not prove cross-source portability of the canonical Case abstraction.

## Why This Increment Exists

Previous Calgary characteristics are `EXTERNALLY REPORTED / PREPARED CONTEXT`, not repository-validated observations.

That context reports:

- a believed local dataset root of `/data/repos/Public Datasets`;
- a candidate file named `calgary_311.csv`;
- approximately 7.47 million rows;
- a reportedly unique `service_request_id`;
- reported lifecycle timestamps named `requested_date`, `updated_date`, and `closed_date`;
- a reported temporal range of approximately 2010 through 2026;
- no reported assignment, dispatch, handoff, active-work, queue-residence, customer-wait, or rework timing;
- the Open Government Licence - City of Calgary as the reported licence.

None of these statements is an observed repository fact at the opening of Increment 003.

## Scope

Later execution of Increment 003 is planned to verify:

1. the authoritative local dataset path actually present;
2. file identity and basic filesystem metadata;
3. file format and readability;
4. observed column and schema structure;
5. observed row count;
6. observed source-identifier behavior, including `service_request_id` presence, nullability, and uniqueness;
7. observable lifecycle timestamp fields;
8. timestamp parseability and supported temporal precision;
9. observed date range;
10. important missingness and data-quality characteristics relevant to later canonical mapping;
11. whether Calgary native fields relevant to Increment 002 are actually present, including, where applicable, `requested_date`, `updated_date`, `closed_date`, `status_description`, `service_name`, `agency_responsible`, `source`, and address, community, or other spatial fields;
12. source provenance sufficient to identify which Calgary dataset the file is intended to represent;
13. current authoritative licence and attribution evidence;
14. a reproducibility identifier such as a file hash once the artifact is inspected;
15. discrepancies between externally reported preparation evidence and repository-observed evidence.

## Non-goals

Increment 003 will not:

- implement a source adapter;
- implement or select canonical Case persistence;
- perform PostgreSQL ingestion;
- create a production ingestion pipeline;
- perform SQL operational analysis;
- create a management dashboard or view;
- create or implement `CaseEvent`;
- inspect ServiceNow;
- perform cross-source comparison;
- perform workflow decomposition;
- select or implement an AI intervention;
- define a canonical status taxonomy;
- implement canonical classification;
- conclude universal portability;
- make final semantic mapping decisions that require a source contract.

For example, this increment may establish that `requested_date` exists and characterize its evidence, but it must not automatically conclude that the field satisfies canonical `created_at` unless source semantics support that mapping.

## Starting State

Repository HEAD at opening:

    382642a78b33a326a22edf9f9a0f53864b1669a5

Increment 001 is Complete.

Increment 002 is Complete. It established the canonical Case semantic contract and source-adapter conformance requirements.

No Calgary source contract exists. No Calgary adapter exists. No repository-validated Calgary empirical profile has been established. No operational capability is claimed.

README.md contains known stale foundation wording, but correcting it is outside Increment 003 unless separately authorized.

## Assumptions to Test, Not Facts

The following are unverified assumptions or hypotheses:

- `/data/repos/Public Datasets` is the correct dataset root;
- `calgary_311.csv` exists there;
- the file is the intended Calgary 311 Service Requests dataset;
- the reported row count is approximately correct;
- `service_request_id` is unique;
- `requested_date`, `updated_date`, and `closed_date` exist;
- the reported lifecycle and date-range characteristics are correct;
- the reported Calgary licence and attribution remain applicable to this artifact.

Local file presence alone would not establish authoritative provenance, current source version, licence validity, schema semantics, or canonical mapping correctness.

## Threat and Failure Model

Increment 003 may fail or produce a negative result if:

- the expected file does not exist;
- the expected path is wrong;
- the local file is incomplete or corrupt;
- the file cannot be read reproducibly;
- its schema differs from the reported preparation context;
- `service_request_id` is missing, null, or non-unique;
- lifecycle fields differ from expectations;
- timestamps are malformed or semantically unclear;
- observed temporal coverage differs materially from the reported range;
- source provenance cannot be established;
- licence or attribution cannot be verified;
- the local artifact appears to be a transformed derivative without enough lineage to reconstruct its origin;
- reported preparation evidence cannot be reproduced.

Negative results must be retained rather than normalized away.

## Planned Evidence

Later work in this increment should retain, as appropriate:

- filesystem and path evidence;
- file size and metadata;
- file hash;
- observed schema;
- row-count evidence;
- identifier null and uniqueness checks;
- timestamp parsing and profile results;
- date-range evidence;
- missingness summaries for contract-relevant fields;
- source-provenance evidence;
- licence and attribution evidence;
- discrepancies from prior externally reported context;
- commands or scripts sufficient for another engineer to reproduce the inspection.

These are planned evidence artifacts. They do not exist merely because this planning record lists them.

## Claim Discipline

**Current Calgary profile before execution:** external and preparation evidence.

**Increment 003 file, schema, and profile results:** future engineering observations.

**Verified source and licence facts:** future external evidence once authoritative material is inspected.

**Canonical Calgary field mappings:** future design decisions in source-contract work.

**Cross-source Case portability:** research hypothesis.

**Universal portability:** not claimed.

**Workflow decomposition from Calgary:** not supported by current evidence and not an Increment 003 goal.

## Relationship to Increment 002

Increment 003 will pressure-test Increment 002 but must not silently revise it.

If observed Calgary evidence conflicts with an accepted Increment 002 contract rule:

- preserve the conflict;
- do not modify Increment 002 inside Increment 003 without an explicit revision decision;
- classify whether the evidence may `WEAKEN`, `REFINE`, `EXTEND`, or `REJECT` the Calgary mapping under the established falsification framework.

This record does not predict that outcome.

## Completion Criteria

Increment 003 may be marked Complete only when, at minimum:

1. the actual local Calgary artifact has been identified or its absence explicitly established;
2. filesystem and file-identity evidence is retained;
3. schema and basic readability are verified;
4. row count is directly observed;
5. source-identifier behavior relevant to canonical identity is tested;
6. contract-relevant lifecycle and source fields are profiled;
7. timestamp and date coverage is characterized;
8. important missingness or malformed evidence is characterized;
9. source provenance has been investigated and its confidence and boundary recorded;
10. licence and attribution evidence has been investigated and its confidence and boundary recorded;
11. discrepancies from prior externally reported preparation context are retained;
12. source evidentiary limitations are explicitly recorded;
13. reproducibility commands or artifacts are retained;
14. no source mapping is promoted to canonical fact without semantic justification;
15. observed results and planned work are clearly distinguished.

## Skills Practiced

### Practiced or Refreshed

- source-data inspection;
- data profiling;
- provenance reasoning;
- data-quality reasoning;
- evidence preservation;
- reproducibility;
- semantic boundary discipline.

### Developed

- translating a canonical domain contract into source-validation requirements.

### Not Practiced in This Increment

- production ingestion;
- application coding;
- AI or LLM implementation;
- frontend work;
- workflow reconstruction.

## Observed Result

- The Increment 003 planning record was created.
- No dataset was inspected.
- No empirical Calgary claim was established.

Creating this document does not satisfy any empirical completion criterion. Increment 003 remains Planned.

## Artifacts

Planned increment record:

    docs/increments/003-calgary-source-evidence-validation.md

No empirical evidence artifact exists yet.

## Commit

Not yet committed.

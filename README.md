# Support Operations Intelligence

Support Operations Intelligence (SOI) is a research-engineering project
examining how operational source evidence can move through a disciplined chain
toward diagnosis, intervention selection, implementation, and evaluation. The
repository has established the evidence-establishment and
representation-audit stages of that chain; it has not yet established an
operational interpretation or a justified intervention.

```mermaid
flowchart LR
    A["Operational Source Evidence"] --> B["Reproducible Baseline"]
    B --> C["Deterministic Sentinel Audit"]
    C --> D["Count-Blinded Human Review"]
    D --> E["Operational Interpretation"]
    E --> F["Intervention Selection"]
    F --> G["AI or Other Intervention"]
    G --> H["Evaluation"]
    H --> I["Decision"]

    A:::complete
    B:::complete
    C:::complete
    D:::current
    E:::future
    F:::future
    G:::future
    H:::future
    I:::future

    classDef complete fill:#d1fae5,stroke:#047857,color:#064e3b
    classDef current fill:#fef3c7,stroke:#b45309,color:#78350f
    classDef future fill:#f3f4f6,stroke:#6b7280,color:#374151
```

Green stages have retained engineering evidence, amber is the current research
boundary, and gray stages remain future work.

## What the project is investigating

SOI asks how source records can be admitted under explicit contracts,
reproduced as a bounded baseline, audited for source-native representation
patterns, and only then used for operational interpretation. The current
Calgary 311 case study emphasizes exact evidence identity, deterministic
execution, retained negative results, and claims that stay within what the
artifacts establish.

This repository is the canonical active research record. Its increments cover
the canonical `Case` contract, Calgary source contract, executable adapter,
reproducible CSV boundary, full-artifact baseline, and the ongoing
source-native sentinel and missingness audit.

## Evidence established so far

### Reproducible full-artifact baseline — Increment 007 complete

The retained full-artifact execution observed and reconciled:

- 7,474,403 source rows;
- 7,474,403 structurally accepted and identity-admitted rows;
- 0 structural rejects and 0 identity rejects;
- 7,474,403 distinct exact `source_case_id` values;
- 0 source identifiers appearing more than once and 0 rows involved in
  duplication;
- 1,169 exact `service_name` vocabulary values;
- 5 exact `status_description` vocabulary values; and
- 1,817 `service_name` × `status_description` cells.

This establishes a retained source-row descriptive baseline and exact lexical
source-identifier uniqueness within this artifact. It does **not** establish
that each row corresponds to one independently managed real-world case.
Operational interpretation and scientific conclusions were not part of
Increment 007.

### Source-native sentinel audit — Increment 008 in progress

The deterministic Phase 1 audit is complete and reconciled. It observed one
`service_name` lexical sentinel candidate:

| Exact value | Retained rows | Row share | Vocabulary share | Classification |
| --- | ---: | ---: | ---: | --- |
| `"N/A"` | 8,721 | 0.116678% | 0.085543% | `SENTINEL_CANDIDATE` |

The match came from the predeclared
`PHASE_1C_CASE_INSENSITIVE_EXACT_SENTINEL` rule and triggers an
`EXPLICIT_COMPLETENESS_QUALIFICATION` obligation. `"N/A"` remains a lexical
candidate: it has not been reclassified as missing data, and its source or
operational meaning has not been established.

Phase 1 found no `status_description` candidates under the predeclared lexical
rules. `agency_responsible` was not evaluable because Increment 007 did not
retain its complete lexical vocabulary.

## Current research boundary

Increment 008 Phase 2 uses a count-blinded Stage A review universe that has
been generated, retained, and reconciled using separate internal reconstruction
logic:

- 1,173 entries: 1,168 `service_name`, 5 `status_description`, and no
  `agency_responsible` entries;
- no ordered-list, missing-entry, unexpected-entry, or duplicate-identity
  mismatches;
- no Phase 1 exclusion leakage; and
- no quantitative or decision fields exposed in reviewer entries.

The human procedure is frozen as 12 sequential batches. Reviewer-facing
entries contain only field and exact lexical value; source prevalence and
context remain hidden. Allowed decisions are `NO_PHASE_2_FLAG` and
`EXPLORATORY_SENTINEL_CANDIDATE`, with a lexical-only rationale required for a
flagged value.

Batch 1 has been exposed and is awaiting researcher decisions. No batch is
complete, no Stage A decision has been retained, and the decision artifact has
not been created. The committed validator is implemented and synthetically
GREEN, but it has not validated real decision evidence because none exists.

```text
PHASE_2_STAGE_A_HUMAN_REVIEW = BATCH_1_EXPOSED_AWAITING_REVIEWER_DECISIONS
STAGE_A_BATCHES_COMPLETED = 0
STAGE_A_ENTRIES_REVIEWED = 0
STAGE_A_DECISION_ARTIFACT = NOT_CREATED
PHASE_2_FINDINGS = NOT_OBSERVED
PHASE_2_STAGE_B = NOT_STARTED
PHASE_3 = NOT_STARTED
```

The latest verified repository regression is 218 tests with 0 failures and 0
errors under repository-local Python 3.12.3. Passing internal tests are
engineering evidence, not independent external validation.

## What is not yet established

The project has not yet performed or established:

- completed Phase 2 human review or any Phase 2 finding;
- quantitative Stage B attachment;
- Phase 3 low-information review;
- operational diagnosis or causal interpretation;
- intervention selection or effectiveness;
- a conclusion that AI is the warranted intervention;
- production deployment, readiness, or cross-source portability; or
- a scientific conclusion.

The Calgary source artifact and external result artifacts are not distributed
in this repository. Repository licensing does not grant rights to external
data.

## Inspect the research record

The increment documents retain the detailed contracts, commands, evidence,
failure conditions, reconciliations, and claim boundaries:

- [Canonical Case contract](docs/increments/002-canonical-case-contract.md)
- [Calgary source contract](docs/increments/004-calgary-source-contract.md)
- [Executable Calgary adapter](docs/increments/005-executable-calgary-case-adapter.md)
- [Reproducible Calgary CSV boundary](docs/increments/006-reproducible-calgary-csv-record-stream.md)
- [Full-artifact baseline](docs/increments/007-full-artifact-execution-and-status-by-service-baseline.md)
- [Source-native sentinel and missingness audit](docs/increments/008-source-native-sentinel-and-missingness-audit.md)

Run the complete test suite from the repository root with:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

## Repository lineage and licenses

The earlier independent lineage is preserved privately at
`arnaldosepulveda/support-operations-intelligence-legacy` for provenance. It
has independent Git history and is not part of this repository's ancestry.
This repository contains the canonical active increment-based research
history.

Source code is licensed under the [Apache License 2.0](LICENSE) unless noted
otherwise. Documentation under `docs/` is licensed under
[CC BY 4.0](docs/LICENSE.md) unless noted otherwise. External datasets and
artifacts are not included or relicensed here.

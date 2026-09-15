# Support Operations Intelligence

Support Operations Intelligence (SOI) is a research-engineering project for
building a defensible evidence chain from operational source records toward
analysis and, eventually, justified intervention decisions.

The project emphasizes explicit contracts, reproducible execution, retained
negative evidence, and bounded claims.

SOI is not currently an operational analytics platform.

## Current Project Boundary

The current repository establishes a reproducible source-record boundary for a
Calgary 311 case study.

At the current publication checkpoint, the implemented evidence chain is:

```text
SOURCE
    ->
SEMANTIC CONTRACT
    ->
EXECUTABLE CONFORMANCE
    ->
REPRODUCIBLE SOURCE-RECORD BOUNDARY
```

Later stages remain future work:

```text
ANALYTICAL CONTRACT
    ->
OPERATIONAL BASELINE
    ->
DIAGNOSIS
    ->
INTERVENTION SELECTION
    ->
IMPLEMENTATION + EVALUATION
```

The repository does not currently claim to implement those later stages.

## What Is Implemented

### Canonical Case contract

The repository defines a bounded canonical `Case` contract covering:

- source identity;
- admission criteria;
- deterministic source identity behavior;
- canonical versus source-native evidence boundaries;
- observed, derived, simulated, and unavailable evidence states;
- explicit unavailable-reason semantics.

Only the identity core is treated as universal.

Other fields remain source-dependent unless independently justified.

### Calgary source contract

The Calgary case study defines explicit source-specific mappings for the
locally characterized Calgary 311 source artifact.

The contract distinguishes:

- fields accepted into the canonical representation;
- source-native evidence retained without canonical reinterpretation;
- fields whose mapping remains deferred;
- semantics that the available evidence does not justify.

Deferred concepts are not silently converted into canonical meaning.

### Executable Calgary adapter

The repository contains an executable Calgary adapter that:

- admits or rejects records using the established identity boundary;
- preserves exact source identity;
- emits the canonical `Case` identity core;
- retains selected Calgary source-native evidence;
- represents unavailable evidence explicitly;
- does not fabricate values when evidence is absent or indeterminate.

### Calgary CSV record stream

The repository contains a Calgary-specific standard-library CSV record stream
that:

- accepts an explicit `Path`;
- validates the exact ordered 15-field source header;
- rejects tested header drift;
- rejects tested row-width mismatch;
- preserves tested lexical source values;
- yields `Mapping[str, str]` records;
- tracks logical CSV data-record position;
- handles quoted embedded newlines through Python's CSV parser;
- streams lazily rather than materializing the complete artifact before
  yielding records.

### Artifact identity gate

The Calgary source boundary includes an incremental SHA-256 verification gate.

For tested synthetic inputs:

- a matching expected digest returns the observed digest;
- a mismatching expected digest raises a blocking
  `CalgaryCsvArtifactDigestMismatch`;
- the mismatch retains both expected and observed digest evidence.

This is function-level artifact identity behavior.

It is not authoritative source provenance and does not prove that every future
caller will invoke the gate correctly.

### Parser-to-adapter composition

Synthetic verification establishes that:

- a parser-emitted record can be passed directly to the existing Calgary
  adapter;
- selected identity and status semantics are preserved;
- for one independently constructed equivalent synthetic fixture, the parser
  path and hand-built mapping path produce equal complete deterministic adapter
  results.

This does not establish universal equivalence across every possible Calgary
record.

### Bounded real-artifact execution

A local Calgary artifact matching the previously retained size and SHA-256 was
exercised through the CSV record-stream boundary for a bounded prefix of three
logical records.

That smoke execution verified the tested prefix only.

It is not a full-file or dataset-wide validation.

## Completed Engineering Increments

| Increment | Scope | Status |
| --- | --- | --- |
| 001 | Repository foundation | Complete |
| 002 | Canonical Case contract | Complete |
| 003 | Calgary source evidence validation | Complete |
| 004 | Calgary source contract | Complete |
| 005 | Executable Calgary Case adapter | Complete |
| 006 | Reproducible Calgary CSV record stream and artifact identity gate | Complete |

Increment 006 closed with:

- 17 of 17 acceptance criteria satisfied;
- 17 of 17 defined failure conditions not triggered;
- 21 of 21 planned verification checks executed passing;
- 17 focused CSV-boundary tests passing;
- 142 repository regression tests passing.

Those counts describe the Increment 006 closure checkpoint. They are not a
claim of exhaustive correctness or production readiness.

## What Is Not Established

The repository does not currently establish:

- complete Calgary dataset structural validity through the current parser;
- absence of malformed records outside the bounded smoke prefix;
- authoritative City of Calgary provenance;
- immutable upstream source-version identity;
- licence binding from local artifact identity;
- persistent storage;
- PostgreSQL ingestion;
- database schema or migration behavior;
- dataset-wide loading correctness;
- analytical contracts;
- operational metrics;
- request-to-closure analysis;
- operational diagnosis;
- causal conclusions;
- intervention selection;
- intervention effectiveness;
- AI suitability;
- AI, RAG, or agent behavior;
- production deployment;
- production readiness;
- portability of the Calgary implementation to other sources.

These are separate engineering or research questions and require separate
evidence before corresponding claims can be made.

## Source Artifact

The Calgary source artifact used for local engineering and verification is not
distributed by this repository.

Historical increment records deliberately retain local filesystem paths where
those paths were part of actual execution evidence.

For example, a record may refer to a path such as:

```text
/data/repos/Public Datasets/calgary_311.csv
```

These references are retained for reconstructability of the engineering
record. They are not installation instructions and do not mean the external
artifact is stored in this repository.

External source artifacts remain subject to their own provenance, licensing,
and distribution terms.

Repository licensing does not grant rights to external datasets.

## Reproducibility Boundary

The project preserves, where available:

- repository checkpoints;
- Python runtime information;
- source-contract decisions;
- expected structural contracts;
- synthetic fixtures;
- automated-test commands;
- actual observed test results;
- negative and malformed-input evidence;
- source-artifact identity observations;
- remediation history.

Not every historical execution detail is recoverable.

For example, Increment 006 explicitly records that the exact command used for
the bounded real-artifact smoke was not retained. The artifact identity,
logical-record bound, records consumed, structural observations, and observed
smoke outcome were retained.

Missing evidence is recorded as missing rather than reconstructed after the
fact.

## Running the Tests

The Increment 006 closure environment used Python 3.12.3 with the
repository-local virtual environment.

The project currently declares no third-party Python dependencies:

```text
dependencies = []
```

Run the complete test suite from the repository root with:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q
```

At the Increment 006 closure checkpoint:

```text
Ran 142 tests
OK
```

The focused Calgary CSV record-stream suite can be run with:

```bash
PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_calgary_csv_record_stream \
  -v
```

At Increment 006 closure:

```text
Ran 17 tests
OK
```

## Research-Engineering Method

Meaningful changes are developed through increment records under:

```text
docs/increments/
```

An increment may retain, where applicable:

- objective;
- scope and non-goals;
- starting checkpoint;
- assumptions;
- source or semantic contract;
- planned implementation;
- planned tests;
- acceptance criteria;
- failure criteria;
- observed results;
- negative results;
- claim classification;
- threats to validity;
- reproducibility evidence;
- commit lineage.

Planned tests are not reported as observed evidence until they execute.

Passing internal tests are Engineering observations. They are not independent
external validation.

A working implementation is not treated as evidence of universality,
production readiness, or portability.

## Current Direction

The next research-engineering question is whether the complete digest-verified
Calgary artifact can traverse the established parser and adapter boundary and
support a narrowly predeclared descriptive baseline.

That work has not yet been implemented or claimed by this repository.

Persistence should be introduced only if later analytical or reproducibility
requirements justify it.

No persistence architecture is currently established.

## Repository Positioning

This repository is a public portfolio and research-engineering artifact.

Its purpose is to make the engineering method, evidence chain, boundaries,
failures, and reasoning inspectable.

It should not be interpreted as:

- a supported production library;
- an operational analytics platform;
- a commercial analytics product;
- a complete operational-intelligence system.

## License

Repository licensing will be stated separately.

External datasets and source artifacts are not included and are not covered by
the repository's eventual code or documentation licenses.

# Architecture

This page describes how the collection is organized, why shared files are copied into each skill, and how to extend the collection with a new domain or skill.

## Contents

1. [Layers](#layers)
2. [Repository layout](#repository-layout)
3. [How a skill loads its references](#how-a-skill-loads-its-references)
4. [Shared files](#shared-files)
5. [Manifests](#manifests)
6. [Quality gates and failure cases](#quality-gates-and-failure-cases)
7. [Validation](#validation)
8. [Adding a domain pack](#adding-a-domain-pack)
9. [Adding a skill](#adding-a-skill)
10. [Design principles](#design-principles)

## Layers

Every section skill combines up to five layers. The generic layer is always loaded, and the others are loaded only when the paper needs them.

| Layer | Where it lives | Scope |
|---|---|---|
| Section contract | `references/core/contract-and-quality-gates.md` in each skill | Generic logic, quality gates, and failure corrections for one section |
| Reader and terminology contract | `shared/core/reader-and-terminology-contract.md` | Terminology, antecedents, claim types, scale (S), sentence rhythm (R), manuscript hygiene (H) |
| Method route | `references/methods/evolutionary-algorithms.md`, `references/methods/reinforcement-learning.md` in `write-methods` and `write-experiments` | Solver-family rules, such as encodings and constraint handling or training credibility |
| Domain pack | `references/domains/mec.md` in the five section-writing skills | Field-specific causal structure, terminology, physical checks, reference-scale tables |
| Language adapter | `shared/languages/zh.md` | Chinese register, punctuation, numbering, and a weak-prior rhythm band in ideographs |
| House style | `shared/styles/house-style-card.md`, `shared/styles/team-house-style.md` | The author team's measured voice, rhythm, connectives, titles, openers, and front and back matter |

Mobile edge computing (`mec`) is the first domain pack. The generic contracts stay usable outside MEC, and `latex-prose-audit` and `write-revision-responses` are domain-independent.

## Repository layout

```text
skills/                         one directory per skill, each installable on its own
  write-introductions/
    SKILL.md                    routing, workflow, reader gates
    agents/openai.yaml          Codex interface metadata
    references/core/            section contract and the shared reader contract (copy)
    references/domains/mec.md   MEC domain pack
    references/languages/zh.md  Chinese adapter (copy)
    references/styles/          house style and card (copies)
    scripts/style_fingerprint.py  measurement script (copy)
  write-related-work/ ... latex-prose-audit/
shared/                         canonical sources of every copied file
scripts/                        repository tools: sync, validation, calibration
tests/                          unit tests, gate index, failure-case fixtures
docs/                           this documentation
skills-manifest.json            the skills that the collection ships
domain-packs.json               declared domain packs and the skills they extend
shared-files.json               shared sources and their target skills
```

## How a skill loads its references

`SKILL.md` names each reference file with a direct link and states when to read it. A section skill reads its section contract, the reader contract, and the house-style card by default. It reads a method route only for the matching solver family, the MEC pack only for MEC or directly adjacent systems, the Chinese adapter only for a Chinese manuscript, and named sections of the full house style only for the task at hand. This progressive disclosure keeps the default reading short and keeps domain assumptions out of papers that do not need them.

## Shared files

A skill must stay installable on its own, and its links may not leave its directory. Rules common to several skills are therefore copied into each skill rather than linked:

| Source | Copied to |
|---|---|
| `shared/core/reader-and-terminology-contract.md` | the six section skills, at `references/core/` |
| `shared/languages/zh.md` | the six section skills, at `references/languages/` |
| `shared/styles/team-house-style.md`, `shared/styles/house-style-card.md` | the six section skills and `latex-prose-audit`, at `references/styles/` |
| `shared/scripts/style_fingerprint.py` | all eight skills, at `scripts/` |

`shared/` is the only place to edit these files. `python scripts/sync_shared.py` writes the copies, and `python scripts/sync_shared.py --check` (also run in CI and by the unit tests) fails when a copy drifts or is missing. `shared-files.json` lists the targets.

## Manifests

- `skills-manifest.json` lists the skills that the collection ships. The validator checks that every listed skill exists and that no unlisted skill directory is present.
- `domain-packs.json` declares each domain pack and the skills it extends. Every declared adapter must exist and be linked from its `SKILL.md`.
- `shared-files.json` declares the shared sources and their targets.

## Quality gates and failure cases

Contracts tag their rules with gate identifiers such as `[G-INT-contrib]` or `[G-STY-merge]`. Each identifier appears exactly once in its file. `tests/gate-index.json` maps every documented failure case to the gates that must catch it, and `tests/fixtures/failure-cases/case-NN.md` holds a short synthetic snippet of each case with its expected gates. `tests/test_gate_coverage.py` checks that the index, the fixtures, and the skill text agree.

## Validation

`python scripts/validate_skills.py` checks:

- the skill, domain, and shared-file manifests;
- `SKILL.md` frontmatter (`name` and a `description` that starts with "Use when");
- that every bundled reference is linked directly from its `SKILL.md`, and that references over 100 lines have a contents list;
- Markdown links inside each skill and that no link leaves the skill directory;
- portability: no absolute paths, machine-specific directories, placeholders, or repository-specific wording in skill text;
- byte-identical shared copies.

The unit tests (`python -m unittest discover -s tests`) cover the fingerprint script, the calibration tool, the sync tool, the validator, the gate coverage, and a check that recommended sentence patterns do not model constructions that the house style bans. CI also confirms that the `skills` CLI discovers every skill in `skills-manifest.json`.

## Adding a domain pack

1. Write `references/domains/<domain>.md` in each section skill that the domain affects. A domain adapter may specialize a core contract, but it must not replace generic evidence, causality, safety, or claim-bounding gates.
2. Link the adapter from each affected `SKILL.md`, with the condition under which to read it.
3. Declare the pack in `domain-packs.json`.
4. Record the evidence behind specialized rules in the adapter, such as reference-scale tables measured with the counting rule of the reader contract.
5. Run the validation and the tests.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` and a `description` that starts with "Use when", and add `agents/openai.yaml` if the skill should appear in Codex with a display name.
2. List the skill in `skills-manifest.json`, and add it to `shared-files.json` for every shared file it uses.
3. Run `python scripts/sync_shared.py`, link each copied file from `SKILL.md`, and run the validation and the tests.

## Design principles

- **Generic core, explicit specialization.** Universal section logic stays separate from method and domain assumptions.
- **Source-grounded rules.** Domain adapters and the house style record the cross-paper evidence behind specialized guidance.
- **Measured, then enforced.** Bands come from measured papers with a stated counting rule, and recommended patterns are tested against the banned constructions.
- **Artifact-independent.** No skill requires a particular manuscript format, wiki, Git workflow, corpus directory, or machine path.
- **Evidence-bounded.** Claims cannot exceed the supplied evidence, and working ledgers stay out of the manuscript.

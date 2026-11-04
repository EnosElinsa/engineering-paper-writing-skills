# Engineering Paper Writing Skills

[![Validate skills](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml)

A portable, extensible collection of source-grounded Codex skills for writing and auditing engineering research papers.

The repository separates four layers:

- **generic section contracts** for Introductions, Related Work, System Models, Methods, Experiments, and the summary parts (title, abstract, index terms, contribution list, Conclusion);
- **method-family routes** for evolutionary algorithms and reinforcement learning;
- **domain packs** for field-specific causal structure, terminology, physical checks, and evidence expectations;
- **a team house style** for measured author voice, sentence rhythm, connectives, titles, and paragraph openers.

Mobile edge computing is the first formally supported domain pack. The generic skills remain usable outside MEC, while `latex-prose-audit` stays domain-independent.

## Included skills

| Skill | Generic responsibility | Optional routes |
|---|---|---|
| `write-introductions` | Causal motivation, research classification, scenario-to-method derivation, citation economy, and bounded contributions | `domains/mec.md` |
| `write-related-work` | Mechanism-based literature synthesis, evidence-backed boundaries, and gap-to-paper closure | `domains/mec.md` |
| `write-system-models` | Architecture inheritance, operational flow, symbols, timing, constraints, and formulation closure | `domains/mec.md` |
| `write-methods` | Model-to-algorithm traceability, novelty boundaries, executable semantics, deployment, and complexity | evolutionary algorithms, reinforcement learning, and `domains/mec.md` |
| `write-experiments` | Evaluation contracts, fair comparisons, evidence-to-claim writing, statistics, ablations, and robustness | evolutionary algorithms, reinforcement learning, and `domains/mec.md` |
| `write-abstracts-and-conclusions` | Titles, abstracts with quantified results, index terms, contribution lists and roadmaps, Conclusions ordered by evidence, future-work chains, and agreement of all summary parts after reruns | team house style |
| `write-revision-responses` | Comment ledgers, model-or-test answers to requests, response-letter structure, verbatim quotation, highlighting policy, cross-document synchronization after reruns, integration of co-author edits, and change reports | domain-independent |
| `latex-prose-audit` | LaTeX-aware sentence-level prose, semantic roles, articles, notation, mathematical phrasing, references, and source integrity | domain-independent |

Each skill is independently installable. The section skills always load their generic core, then load only the applicable method and domain references.

## Team house style

`shared/styles/team-house-style.md` records the measured conventions of the author team that calibrated these skills: author voice, a sentence-rhythm band (mean sentence length, its spread, and the shares of very long and very short sentences), the rules for combining and splitting sentences, a connective profile, banned constructions, section and subsection titles, attested paragraph openers, and the shapes of the title, abstract, index terms, contribution list, roadmap, and Conclusion. The numbers come from four published IEEE Transactions papers by the team and from measured before-and-after diffs of supervisor edits. Where the two disagree, the supervisor's practice wins, and the file names the reference-paper habits that are not imitated.

The section skills, `write-abstracts-and-conclusions`, and `latex-prose-audit` read the house style unless the user names another venue or team style. The shared contract adds protocol R, which keeps a draft inside the rhythm band and checks over-splitting as well as over-long sentences.

`shared/scripts/style_fingerprint.py` measures a `.tex` (including `\input` and `\include` children), `.md`, or `.txt` manuscript in English or Chinese against that band using only the Python standard library (a Chinese manuscript is measured in ideographs against the weak-prior band of the Chinese adapter): section scale, the sentence-length profile, connectives per 100 sentences, within-sentence features, banned constructions with their sentences, runs of short sentences, repeated citation keys within a section (`--citations`), paragraph-opening sentences (`--spine`), abbreviation definitions across the manuscript, supplement, and letter (`--abbrev`), and a sentence-level classification of edits between two versions (`--diff OLD NEW`). It is copied into every skill that refers to it at `scripts/style_fingerprint.py`.

### Recalibrating the house style

When the team publishes another paper of this family, add it to the reference set and regenerate the band:

```bash
python scripts/calibrate_house_style.py --references path/to/reference-papers \
    --approved path/to/supervisor-approved.tex --baseline path/to/approved-baseline.tex \
    --abstract-limit 250 --check
python scripts/calibrate_house_style.py ... --write
python scripts/sync_shared.py
```

The tool measures every reference with the fingerprint script and proposes each range as the minimum to maximum over the references. `--approved` drafts widen only the abstract and Conclusion ranges, `--baseline` fills the last column of the rhythm table, and `--abstract-limit` sets the upper end of the abstract word range. `--check` exits non-zero when the proposed band differs from the shipped one. `--write` rewrites the generated blocks (the `TEAM_BAND` literal, the house-style rhythm tables, the Chinese weak-prior tables, and the abstract and Conclusion ranges in the house style) and lists the prose that still needs a manual review. Connective limits are house rules and are never recalibrated. The paper corpus stays local and is not part of the repository.

## MEC domain pack

The initial `mec` pack is declared in [domain-packs.json](domain-packs.json) and is available to the five section-writing skills.

Its Introduction contract preserves the source-derived chain:

`scenario motivation -> scenario -> algorithm motivation -> algorithm`

Its System Model contract adds MEC-specific control boundaries, service-flow ordering, timing and state semantics, resource and mobility closure, physical constraints, and operational fallback checks. The method and experiment adapters connect encoded decisions and evidence to MEC quantities without turning those details into universal engineering rules.

The pack was distilled from complete sections of representative team and benchmark manuscripts. Source titles in the references provide provenance; the copyrighted paper corpus is not distributed and is not required at runtime.

## Repository structure

```text
skills/
  write-introductions/
    SKILL.md
    references/core/contract-and-quality-gates.md
    references/domains/mec.md
  write-related-work/
  write-system-models/
  write-methods/
    references/methods/evolutionary-algorithms.md
    references/methods/reinforcement-learning.md
    references/domains/mec.md
  write-experiments/
  write-abstracts-and-conclusions/
    references/core/contract-and-quality-gates.md
  write-revision-responses/
    references/core/response-contract-and-quality-gates.md
  latex-prose-audit/
shared/
  core/reader-and-terminology-contract.md
  languages/zh.md
  styles/team-house-style.md
  scripts/style_fingerprint.py
skills-manifest.json
domain-packs.json
shared-files.json
scripts/
tests/
```

Each section skill, including `write-abstracts-and-conclusions`, carries byte-identical copies of the files under `shared/`: `references/core/reader-and-terminology-contract.md`, `references/languages/zh.md`, `references/styles/team-house-style.md`, and `scripts/style_fingerprint.py`. `latex-prose-audit` receives only the house style and the script, and `write-revision-responses` only the script. `shared/` is the canonical source and `shared-files.json` lists the target skills. The Chinese manuscript adapter is a language layer loaded only for Chinese manuscripts, and the house style is a style layer. Neither is a domain pack.

A future domain is added as a matching `references/domains/<domain>.md` adapter in the affected section skills and one declaration in `domain-packs.json`. Domain adapters may specialize a core contract, but must not replace generic evidence, causality, safety, or claim-bounding gates.

## Install with Codex

Ask Codex to install all eight paths from this public repository:

```text
Install these skills from EnosElinsa/engineering-paper-writing-skills:
skills/write-introductions
skills/write-related-work
skills/write-system-models
skills/write-methods
skills/write-experiments
skills/write-abstracts-and-conclusions
skills/write-revision-responses
skills/latex-prose-audit
```

Codex's skill installer places them under `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Newly installed or replaced skills are available in a new Codex task.

## Install from a clone

Python 3.10 or newer is required for the repository tools.

```bash
git clone https://github.com/EnosElinsa/engineering-paper-writing-skills.git
cd engineering-paper-writing-skills
python scripts/validate_skills.py
python scripts/install_skills.py
```

Install one skill or inspect targets without writing:

```bash
python scripts/install_skills.py --skill write-introductions
python scripts/install_skills.py --dry-run
python scripts/install_skills.py --dest /path/to/skills
```

The installer refuses existing destinations by default. After reviewing upstream changes, replace only manifest-listed skills explicitly:

```bash
git pull --ff-only
python scripts/install_skills.py --force
```

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py
```

Edit shared content only under `shared/`, then copy it into the skills and check for drift:

```bash
python scripts/sync_shared.py
python scripts/sync_shared.py --check
```

`--check` compares only and exits non-zero when a copy has drifted or is missing. Validation checks skill and domain manifests, metadata, direct reference routing, domain declarations, shared-file sources and byte-identical copies, Markdown links and navigation, portability boundaries, legacy identities, and installer safety. The unit tests also check that every documented failure case has a gate identifier that is present exactly once in the skill text.

## Design principles

- **Generic core, explicit specialization:** universal section logic stays separate from method and domain assumptions.
- **Source-grounded rules:** domain adapters record the cross-paper evidence behind specialized guidance.
- **Progressive disclosure:** a skill loads only the references required by the target paper.
- **Shared files are copied, then synchronised:** a skill must stay installable on its own and its links may not leave its directory, so rules common to several skills (the reader and terminology contract, the Chinese manuscript adapter, the team house style, the fingerprint script) are copied into each one. `shared/` holds the single canonical source, `scripts/sync_shared.py` writes the copies, and `scripts/sync_shared.py --check` plus the validator fail the build when a copy drifts or goes missing.
- **Scale from evidence, not from core:** benchmark-derived lengths live in the domain pack, and the team's sentence-rhythm band lives in the house style, as measured defaults with their counting rule. The generic cores state only the protocols for declaring a range.
- **Measured, then enforced:** recommended sentence patterns are checked by a unit test against the constructions the house style bans, and the fingerprint script's band is checked against the house-style tables.
- **Artifact-independent:** no skill requires a particular wiki, manuscript format, Git workflow, corpus directory, or local machine path.
- **Evidence-bounded:** novelty, citation, causality, optimality, robustness, and performance claims cannot exceed supplied evidence.
- **Extensible contracts:** new domains use the same adapter interface and validation rules as MEC.

## Contributing

Issues and focused pull requests are welcome. Keep generic changes domain-neutral, put field assumptions in a declared domain pack, and put solver-family rules in the applicable method route. Run the complete validation commands before opening a pull request. Do not add copyrighted paper corpora or machine-specific paths.

## License

Released under the [MIT License](LICENSE).

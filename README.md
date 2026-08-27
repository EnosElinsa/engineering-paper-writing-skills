# Engineering Paper Writing Skills

[![Validate skills](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml)

A portable, extensible collection of source-grounded Codex skills for writing and auditing engineering research papers.

The repository separates three layers:

- **generic section contracts** for Introductions, Related Work, System Models, Methods, and Experiments;
- **method-family routes** for evolutionary algorithms and reinforcement learning;
- **domain packs** for field-specific causal structure, terminology, physical checks, and evidence expectations.

Mobile edge computing is the first formally supported domain pack. The generic skills remain usable outside MEC, while `latex-prose-audit` stays domain-independent.

## Included skills

| Skill | Generic responsibility | Optional routes |
|---|---|---|
| `write-introductions` | Causal motivation, research classification, scenario-to-method derivation, citation economy, and bounded contributions | `domains/mec.md` |
| `write-related-work` | Mechanism-based literature synthesis, evidence-backed boundaries, and gap-to-paper closure | `domains/mec.md` |
| `write-system-models` | Architecture inheritance, operational flow, symbols, timing, constraints, and formulation closure | `domains/mec.md` |
| `write-methods` | Model-to-algorithm traceability, novelty boundaries, executable semantics, deployment, and complexity | evolutionary algorithms, reinforcement learning, and `domains/mec.md` |
| `write-experiments` | Evaluation contracts, fair comparisons, evidence-to-claim writing, statistics, ablations, and robustness | evolutionary algorithms, reinforcement learning, and `domains/mec.md` |
| `latex-prose-audit` | LaTeX-aware sentence-level prose, semantic roles, articles, notation, mathematical phrasing, references, and source integrity | domain-independent |

Each skill is independently installable. The section skills always load their generic core, then load only the applicable method and domain references.

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
  latex-prose-audit/
skills-manifest.json
domain-packs.json
scripts/
tests/
```

A future domain is added as a matching `references/domains/<domain>.md` adapter in the affected section skills and one declaration in `domain-packs.json`. Domain adapters may specialize a core contract, but must not replace generic evidence, causality, safety, or claim-bounding gates.

## Install with Codex

Ask Codex to install all six paths from this public repository:

```text
Install these skills from EnosElinsa/engineering-paper-writing-skills:
skills/write-introductions
skills/write-related-work
skills/write-system-models
skills/write-methods
skills/write-experiments
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

Validation checks skill and domain manifests, metadata, direct reference routing, domain declarations, Markdown links and navigation, portability boundaries, legacy identities, and installer safety.

## Design principles

- **Generic core, explicit specialization:** universal section logic stays separate from method and domain assumptions.
- **Source-grounded rules:** domain adapters record the cross-paper evidence behind specialized guidance.
- **Progressive disclosure:** a skill loads only the references required by the target paper.
- **Artifact-independent:** no skill requires a particular wiki, manuscript format, Git workflow, corpus directory, or local machine path.
- **Evidence-bounded:** novelty, citation, causality, optimality, robustness, and performance claims cannot exceed supplied evidence.
- **Extensible contracts:** new domains use the same adapter interface and validation rules as MEC.

## Contributing

Issues and focused pull requests are welcome. Keep generic changes domain-neutral, put field assumptions in a declared domain pack, and put solver-family rules in the applicable method route. Run the complete validation commands before opening a pull request. Do not add copyrighted paper corpora or machine-specific paths.

## License

Released under the [MIT License](LICENSE).

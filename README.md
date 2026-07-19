# MEC Paper Writing Skills

[![Validate skills](https://github.com/EnosElinsa/mec-paper-writing-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/EnosElinsa/mec-paper-writing-skills/actions/workflows/validate.yml)

A portable collection of five source-grounded Codex skills for writing and auditing MEC, UAV-MEC, HAP-UAV, vehicular edge computing, and related optimization papers.

The collection turns recurring paper-writing judgments into explicit workflows: paragraph-opening center sentences, MECE research classification, evidence-controlled literature synthesis, model-to-problem closure, method-to-model traceability, and bounded experimental claims.

## Included skills

| Skill | Use it for |
|---|---|
| `writing-mec-introductions` | Background-to-scenario-to-algorithm storylines, MECE classification, citation economy, and Introduction/Related Work boundaries |
| `writing-mec-related-work` | Mechanism-based literature synthesis, category comparison, evidence fidelity, and gap-to-module closure |
| `writing-mec-system-models` | Architecture-first system modeling, symbol and timing discipline, constraints, and problem formulation |
| `writing-mec-methods` | Evolutionary-algorithm or reinforcement-learning methods, executable semantics, novelty boundaries, and complexity |
| `writing-mec-experiments` | Evolutionary or reinforcement-learning experiments, fair evaluation, evidence-to-claim paragraphs, ablations, and robustness boundaries |

Each skill is independently installable. Methods and experiments contain internal evolutionary-algorithm and reinforcement-learning routes; they are not split into duplicate skills.

## Design principles

- **Source-grounded:** the writing patterns were distilled from representative MEC-family papers and a calibrated HAP-UAV manuscript.
- **Progressive disclosure:** every `SKILL.md` contains the workflow and loads detailed references only when needed.
- **Format-independent:** the skills work with LaTeX, Markdown, Word-derived text, or another manuscript representation.
- **Repository-independent:** no skill requires a wiki layout, raw-paper directory, Git workflow, or local machine path.
- **Evidence-bounded:** citation, novelty, causality, optimality, robustness, and performance claims cannot exceed the supplied evidence.

The calibration-paper corpus is not distributed in this repository. Bibliographic titles inside the references record provenance without creating a runtime dependency.

## Install with Codex

Ask Codex to install all five paths from this public repository:

```text
Install these skills from EnosElinsa/mec-paper-writing-skills:
skills/writing-mec-introductions
skills/writing-mec-related-work
skills/writing-mec-system-models
skills/writing-mec-methods
skills/writing-mec-experiments
```

Codex's GitHub skill installer places them under `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Newly installed skills are available on the next turn.

## Install from a clone

Python 3.10 or newer is required for the repository tools; the skills themselves are Markdown and YAML.

```bash
git clone https://github.com/EnosElinsa/mec-paper-writing-skills.git
cd mec-paper-writing-skills
python scripts/validate_skills.py
python scripts/install_skills.py
```

Install one skill or inspect targets without writing:

```bash
python scripts/install_skills.py --skill writing-mec-introductions
python scripts/install_skills.py --dry-run
python scripts/install_skills.py --dest /path/to/skills
```

The installer refuses an existing destination by default. After reviewing upstream changes, update managed copies explicitly:

```bash
git pull --ff-only
python scripts/install_skills.py --force
```

`--force` replaces only manifest-listed skill directories selected for installation. To uninstall, remove the corresponding named directory from the global skills directory; the installer never deletes unrelated skills.

## Citation policy

The Introduction skill retains strict citation accuracy, placement, primary-role, and non-repetition rules. It deliberately does not include the original Markdown numeric-citation parser: citation audits must use the target manuscript's native citation system, and mechanical non-repetition cannot prove that a citation is accurate or sufficient.

## Validate the collection

Run the unit suite and collection validator:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py
```

Validation covers manifest integrity, skill metadata, direct reference loading, long-reference navigation, local Markdown links, portability boundaries, and installer safety.

## Contributing

Issues and focused pull requests are welcome. Keep changes source-grounded, format-independent, and limited to one writing function or shared quality rule. Run the complete validation commands before opening a pull request, and do not add copyrighted paper corpora or machine-specific paths.

## License

Released under the [MIT License](LICENSE).

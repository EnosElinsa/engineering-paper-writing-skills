# Engineering Paper Writing Skills

[![Validate skills](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/EnosElinsa/engineering-paper-writing-skills)](https://github.com/EnosElinsa/engineering-paper-writing-skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

English | [简体中文](README.zh-CN.md)

Agent skills for drafting, revising, and auditing engineering research papers, from the Introduction to the Conclusion and the response letter. Each skill carries a section contract with hard quality gates, a measured team house style, and a standard-library Python script that checks a draft against that style.

The skills follow the open [Agent Skills](https://agentskills.io) format and work with any agent that reads `SKILL.md` files, including Claude Code, Codex, Cursor, and Kiro.

## Quick start

Install all eight skills for your user account with the [`skills` CLI](https://github.com/vercel-labs/skills) (Node.js 22.20 or later):

```bash
npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill '*'
```

The CLI asks which agents to install to. It keeps one copy under `~/.agents/skills/` and links each agent's skill directory to it. To choose agents without prompts:

```bash
npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill '*' -a claude-code -a codex -a kiro-cli -y
```

Then ask your agent for a section by its job, for example:

```text
Revise the Introduction in paper/main.tex with write-introductions. The four reference papers are in refs/.
Draft the Experimental Studies section from results/summary.md and check it with the fingerprint script.
Audit the prose of paper/main.tex with latex-prose-audit and report line-specific findings.
```

## Skills

| Skill | What it covers |
|---|---|
| [`write-introductions`](skills/write-introductions/SKILL.md) | Causal motivation, research classification, scenario-to-method derivation, citation economy, and bounded contributions |
| [`write-related-work`](skills/write-related-work/SKILL.md) | Mechanism-based literature synthesis, evidence-backed boundaries, and the gap that the paper closes |
| [`write-system-models`](skills/write-system-models/SKILL.md) | Architecture inheritance, operational flow, symbols, timing, constraints, and formulation closure |
| [`write-methods`](skills/write-methods/SKILL.md) | Model-to-algorithm traceability, novelty boundaries, executable semantics, deployment, and complexity |
| [`write-experiments`](skills/write-experiments/SKILL.md) | Evaluation contracts, fair comparisons, evidence-to-claim writing, statistics, ablations, and robustness |
| [`write-abstracts-and-conclusions`](skills/write-abstracts-and-conclusions/SKILL.md) | Title, abstract with quantified results, index terms, contribution list, roadmap, Conclusion, and future work |
| [`write-revision-responses`](skills/write-revision-responses/SKILL.md) | Comment ledgers, response letters, verbatim quotation, cross-document synchronization, and co-author edits |
| [`latex-prose-audit`](skills/latex-prose-audit/SKILL.md) | Line-specific LaTeX prose audit: agency, terminology, articles, notation, references, and source integrity |

Install a single skill with `--skill`, for example `npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill write-experiments`. Each skill directory is self-contained, so any subset works on its own.

## How the skills work

- **Section contracts.** Each section skill loads a generic contract with hard quality gates, then only the method route (evolutionary algorithms, reinforcement learning) and domain pack (mobile edge computing) that the paper needs.
- **Team house style.** A one-page card sets the default voice, banned constructions, sentence-rhythm band, merge rules, connectives, and structure. The full house style holds the measured tables behind it. Both come from four published IEEE Transactions papers and from measured supervisor edits. See [docs/house-style.md](docs/house-style.md).
- **Style fingerprint.** `scripts/style_fingerprint.py` inside each skill measures a `.tex`, `.md`, or `.txt` draft in English or Chinese and reports rhythm, banned constructions, over-splitting, captions, titles, the roadmap, declared scale, term-ledger variants, and abbreviations. Its flags are leads to read, not verdicts. See [docs/style-fingerprint.md](docs/style-fingerprint.md).
- **Evidence bounds.** Novelty, causality, optimality, robustness, and performance claims may not exceed the supplied evidence, and working ledgers stay out of the manuscript.

The repository layout, the shared-file mechanism, and how to add a domain pack are described in [docs/architecture.md](docs/architecture.md).

## Requirements

- An agent that loads Agent Skills.
- Node.js 22.20 or later for the `skills` CLI.
- Python 3.10 or later for the bundled fingerprint script (standard library only). The skills still work without Python; the agent then skips the measured checks and says so.

## Update and remove

```bash
npx skills check -g        # list installed skills with available updates
npx skills update -g       # update them
npx skills remove -g write-experiments
```

On Windows without permission to create symbolic links, add `--copy` to `npx skills add` and rerun the command after each release instead of `update`.

## Documentation

- [Architecture](docs/architecture.md): layers, repository layout, shared files, domain packs, and quality gates
- [House style](docs/house-style.md): what the house style fixes, how it was measured, and how to recalibrate it
- [Style fingerprint](docs/style-fingerprint.md): every mode and option of the measurement script
- [Contributing](CONTRIBUTING.md): development setup, checks, and conventions
- [Changelog](CHANGELOG.md)

## Citation

If these skills support a publication, please cite the repository as described in [CITATION.cff](CITATION.cff).

## License

Released under the [MIT License](LICENSE). The reference papers used to calibrate the house style are not distributed with the repository.

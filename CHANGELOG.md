# Changelog

All notable changes to this collection are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [3.0.0] - 2026-11-04

### Added

- `write-abstracts-and-conclusions`: title, abstract, index terms, contribution list, roadmap, Conclusion, future work, and the agreement of all summary parts after reruns.
- `write-revision-responses`: comment ledgers, response letters, cross-document synchronization, integration of co-author edits, and revision-derived claim gates.
- Shared reader and terminology contract with protocols for terminology, antecedents, claim types, reference scale (S), sentence rhythm (R), and manuscript hygiene (H).
- Team house style measured on four published papers and on supervisor edits, with a short card that every skill reads by default.
- Chinese manuscript adapter with Chinese sentence rules and a weak-prior rhythm band in ideographs.
- `style_fingerprint.py`, bundled in every skill: sentence rhythm, banned constructions, over-splitting and merge candidates, document checks (captions, subsection titles, roadmap, opener templates, `this study` density), declared scale (`--scale`), term-ledger variants (`--terms`), abbreviation audit across documents (`--abbrev`), paragraph-opening spine (`--spine`), repeated citations (`--citations`), a one-shot pre-submission report (`--report`), and an edit classifier (`--diff`).
- `scripts/calibrate_house_style.py` to regenerate the band from a reference set and validate it on papers that do not set it.
- MEC reference-scale tables, including script-count `--scale` ranges, in the domain packs of the section skills.
- Gate identifiers, a gate index, and 53 failure-case fixtures with coverage tests.
- Documentation under `docs/`, a Chinese README, contribution guidelines, a citation file, issue and pull-request templates, and a CI check that the `skills` CLI discovers every skill.

### Changed

- Install with the `skills` CLI: `npx skills add EnosElinsa/engineering-paper-writing-skills`.
- The README is reorganized around installation and use, and the reference material moved to `docs/`.
- Section contracts gained the rules ported from supervisor and author practice: opening, title, forward-pointer, and initial-state rules for system models, an experiment design mode, experiment ordering and subsection titles, two or three contribution items, and an optional related-work comparison table.
- Benchmark numbers moved out of the generic contracts into the domain packs.

### Removed

- `scripts/install_skills.py`. Use `npx skills add`, `npx skills update`, and `npx skills remove` instead.

## [2.0.0] - 2026-08-27

### Changed

- Generalized the MEC paper-writing skills into engineering paper-writing skills: generic section contracts, method-family routes for evolutionary algorithms and reinforcement learning, and MEC as the first declared domain pack.

## [1.0.0] - 2026-07-19

### Added

- Initial public collection of portable MEC paper-writing skills, with skill validation, an installer, documentation, and CI.

[Unreleased]: https://github.com/EnosElinsa/engineering-paper-writing-skills/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/EnosElinsa/engineering-paper-writing-skills/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/EnosElinsa/engineering-paper-writing-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/EnosElinsa/engineering-paper-writing-skills/releases/tag/v1.0.0

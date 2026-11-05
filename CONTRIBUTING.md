# Contributing

Issues and focused pull requests are welcome. This page covers the development setup, the checks every change must pass, and the conventions of the repository.

## Development setup

```bash
git clone https://github.com/EnosElinsa/engineering-paper-writing-skills.git
cd engineering-paper-writing-skills
python -m unittest discover -s tests
python scripts/validate_skills.py
```

Python 3.10 or later is required. The repository tools use only the standard library. To try your working copy in an agent, install it from the local path:

```bash
npx skills add . -g --skill '*'
```

## Checks

Run all of these before opening a pull request. CI runs the same commands on Python 3.10, 3.12, and the latest 3.x, and checks that the `skills` CLI finds every skill in `skills-manifest.json`.

```bash
python scripts/sync_shared.py          # write the shared copies
python scripts/sync_shared.py --check  # fail if a copy drifted
python scripts/validate_skills.py
python -m unittest discover -s tests
```

## Where to make a change

| Change | Edit |
|---|---|
| A rule shared by several skills (reader contract, Chinese adapter, house style, card, fingerprint script) | The source under `shared/`, then run `python scripts/sync_shared.py`. Never edit the copies inside `skills/` |
| A section-specific rule | That skill's `references/core/contract-and-quality-gates.md` |
| A solver-family rule | The matching file under `references/methods/` |
| A field-specific rule or reference-scale table | The domain pack under `references/domains/` |
| The workflow or reader gates of one skill | That skill's `SKILL.md` |
| The sentence-rhythm band | Never by hand. Regenerate it with `scripts/calibrate_house_style.py` (see [docs/house-style.md](docs/house-style.md)) |

Read [docs/architecture.md](docs/architecture.md) before adding a domain pack or a skill.

## Conventions

- **Keep generic files generic.** Core contracts and the shared reader contract stay domain- and benchmark-neutral. Field assumptions belong in a declared domain pack, and solver-family rules in a method route.
- **Synthetic examples only.** Do not add sentences, numbers, or figures from unpublished or under-review manuscripts, and do not add copyrighted paper corpora. Stock phrases of a few words are fine.
- **Portable skill text.** No absolute paths, machine-specific directories, placeholders, or references to a particular Git workflow inside `skills/`. The validator enforces this.
- **Gate identifiers.** A new rule that a failure case should trigger gets a gate identifier such as `[G-EX-order]`, unique within its file. Add the failure case to `tests/gate-index.json` with a fixture `tests/fixtures/failure-cases/case-NN.md` (a synthetic snippet under 100 words and an `Expected gates:` line), and update `CASE_COUNT` in `tests/test_gate_coverage.py`.
- **Recommended patterns.** Example sentences in pattern sections are tested against the constructions the house style bans. Add a new pattern section to `tests/test_template_patterns.py`.
- **Text files.** UTF-8 without a byte-order mark and LF line endings (see `.editorconfig` and `.gitattributes`).
- **Commits.** Use a type prefix and an optional scope, such as `feat(script): ...`, `fix(methods): ...`, `docs(style): ...`, `test: ...`, or `chore: ...`, and explain the reason for the change in the body.

## Changes that move measurements

Any change to how `style_fingerprint.py` counts paragraphs or sentences changes the measurements of the reference papers. After such a change:

1. run `python scripts/calibrate_house_style.py ... --check` on the local reference set and regenerate with `--write` if the band moved;
2. re-measure the script-count tables in the `references/domains/mec.md` files and the reference short-sentence share in the script;
3. run the sync, the validator, and the tests.

The reference papers are not part of the repository, so maintainers run this step.

## Releases

1. Move the entries under `Unreleased` in `CHANGELOG.md` to a new version heading with the date.
2. Update `version` and `date-released` in `CITATION.cff`.
3. Tag the release (`git tag -a vX.Y.Z`) and publish the release notes on GitHub.

Users update with `npx skills update -g`.

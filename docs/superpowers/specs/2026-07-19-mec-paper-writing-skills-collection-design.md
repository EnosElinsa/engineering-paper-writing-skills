# MEC Paper Writing Skills Collection Design

**Date:** 2026-07-19
**Status:** Pre-authorized for implementation
**Repository:** `mec-paper-writing-skills`
**Visibility:** Public
**License:** MIT

## Objective

Publish one portable, globally installable collection of five MEC-family academic-writing skills:

1. `writing-mec-introductions`;
2. `writing-mec-related-work`;
3. `writing-mec-system-models`;
4. `writing-mec-methods`;
5. `writing-mec-experiments`.

The public repository becomes the only maintained source. The five project-local copies in `mec-research-wiki` are removed only after the public repository is pushed and all five skills are installed and validated under the user's global Codex skills directory.

`retrieve-ieee-papers` remains project-local because it depends on the research-wiki acquisition and staging workflow.

## Approved Architecture

Use a standalone repository with each discoverable skill under `skills/<skill-name>/`:

```text
mec-paper-writing-skills/
├── README.md
├── LICENSE
├── .gitignore
├── skills-manifest.json
├── skills/
│   ├── writing-mec-introductions/
│   ├── writing-mec-related-work/
│   ├── writing-mec-system-models/
│   ├── writing-mec-methods/
│   └── writing-mec-experiments/
├── scripts/
│   ├── install_skills.py
│   └── validate_skills.py
├── tests/
│   ├── test_install_skills.py
│   └── test_validate_skills.py
├── .github/workflows/validate.yml
└── docs/superpowers/
    ├── specs/
    └── plans/
```

The collection repository is not itself a skill. Each directory below `skills/` remains independently installable and independently valid.

## Portability Boundary

Every published skill must be usable from an arbitrary paper project and manuscript format. Skill content may describe how to inspect a manuscript, bibliography, figures, tables, or supplied reference papers, but must not require:

- an absolute machine path;
- `.agents/skills`, `raw/sources`, `wiki`, or another repository layout;
- project-owned scripts or audit commands;
- Git state, branch conventions, commit workflows, or repository tooling;
- a specific Markdown heading, link, reference-definition, or numbered-citation parser;
- the original MEC research corpus.

Reference-paper provenance remains bibliographic. Relative links internal to an individual skill remain allowed.

## Citation-Audit Decision

Remove `writing-mec-introductions/scripts/audit_intro_citations.py`, its tests, and every instruction that invokes it. The script is tied to Markdown section headings and IEEE-style numeric citations, while the public skill must work with LaTeX, Markdown, Word-derived text, or other manuscript representations.

Retain the substantive citation rules:

- verify each source against the exact claim;
- assign each source one primary Introduction role by default;
- avoid repeated support for adjacent general claims;
- merge or restructure claims instead of substituting weaker sources;
- permit a repeat only for materially independent claims when the source is uniquely authoritative;
- audit citations using the target manuscript's native citation system.

The public collection therefore enforces citation quality through evidence and role ledgers rather than a format-specific mechanical gate.

## Repository Metadata and Documentation

The root README must:

- explain the collection and its source-grounded writing philosophy;
- list the five skills and when each applies;
- show installation through Codex's GitHub skill installer and the repository's portable installer;
- explain update, validation, and uninstall/replace behavior;
- state that the skills do not ship the calibration-paper corpus;
- document contribution and issue expectations concisely.

Use an MIT license, a focused repository description, and GitHub topics for Codex skills, academic writing, MEC, and UAV-MEC. Do not add auxiliary documentation inside individual skill directories.

## Manifest and Validation

`skills-manifest.json` is the collection authority. For each skill it records the name and repository-relative path.

`validate_skills.py` must use only the Python standard library and verify:

1. manifest syntax, unique names, and exact folder/name agreement;
2. required `SKILL.md` and `agents/openai.yaml` files;
3. frontmatter containing only `name` and `description`, with a `Use when...` trigger;
4. direct links from `SKILL.md` to bundled references;
5. a contents section in reference files longer than 100 lines;
6. absence of unfinished markers, absolute paths, research-wiki paths, repository workflow language, and the removed Markdown citation-audit tooling;
7. balanced Markdown fences and resolvable local links;
8. no unexpected skill directory outside the manifest.

The validator must report all discovered failures and exit nonzero when any gate fails.

## Portable Installer

`install_skills.py` must use only the Python standard library. By default it installs all manifest skills into `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. It must also support:

- a custom destination for tests or nonstandard installations;
- selecting one or more skills;
- a dry-run mode;
- refusal when a destination already exists;
- explicit replacement only with `--force`;
- copy-based installation so it works without symlink privileges.

Replacement must operate only on a destination whose basename equals a manifest skill and whose resolved parent is the selected skills directory. Copy to a temporary sibling and rename only after validation succeeds.

The user's installation will use the official Codex GitHub installer after publication. The bundled installer is for portability and public users.

## Testing Strategy

Follow RED-GREEN-REFACTOR for repository scripts and portability changes.

### Portability RED baseline

Run the public-skill portability contract against the current project-local Introduction skill and confirm that it fails on the Markdown citation-audit script and instructions. Confirm the other four skills have no detected repository-path dependency before copying.

### Script RED baselines

Create installer and validator tests before their implementations. The validator tests must cover valid skills, missing metadata, mismatched names, unlinked references, long references without contents, forbidden repository coupling, and malformed manifests. Installer tests must cover default/custom destinations, selection, dry run, existing destinations, forced replacement, unknown skills, and source preservation.

### GREEN and repository gates

Require:

- all unit tests passing;
- the collection validator passing all five skills;
- the official skill creator validator passing each skill with UTF-8 mode;
- public-repository portability scans returning no forbidden coupling;
- the Introduction skill containing no `scripts/` directory;
- the public copies matching project sources except for the approved Introduction sanitization;
- `git diff --check` passing on repository-owned files.

### Installation and remote gates

After publishing:

1. install all five skills from the public GitHub repository through the official Codex installer;
2. validate every installed copy;
3. compare installed file hashes with the public repository;
4. verify the public GitHub repository, visibility, default branch, release tag, and remote commit;
5. only then remove project-local copies.

## Migration Order and Failure Safety

Use this order:

1. create and validate the standalone collection;
2. initialize Git and commit repository infrastructure and skills by scope;
3. create the public GitHub repository and push `main`;
4. create and verify the initial release;
5. globally install and validate all five skills;
6. create an isolated worktree for `mec-research-wiki`;
7. remove only the five writing-skill directories;
8. validate that `retrieve-ieee-papers` remains and the global skills are usable;
9. commit, fast-forward merge, and push the project cleanup;
10. preserve the user's existing battery manuscript modification unchanged.

If publication or installation fails, keep all project-local copies. If project cleanup fails, retain the globally installed copies and repair the cleanup without changing the public repository.

## Commit and Release Structure

Use scoped commits in the new repository:

1. design specification;
2. portable five-skill collection;
3. tested repository tooling, documentation, and CI;
4. implementation plan if it changes after execution begins.

Publish `main`, tag the verified initial state as `v1.0.0`, and create a public GitHub release summarizing the five skills and the format-independent citation policy.

In `mec-research-wiki`, use one cleanup commit that removes only the five project-local writing skills. Do not include the pre-existing manuscript change.

## Acceptance Criteria

The migration is complete when:

1. `EnosElinsa/mec-paper-writing-skills` exists publicly and `origin/main` matches the verified local commit;
2. release `v1.0.0` points to that commit;
3. the repository contains exactly the five approved skills;
4. all collection tests, validators, and portability gates pass;
5. no published skill contains repository-specific paths, workflows, or Markdown citation-audit tooling;
6. all five skills are installed under the global Codex skills directory and match the public source;
7. `mec-research-wiki` no longer tracks the five writing-skill directories;
8. `retrieve-ieee-papers` remains project-local;
9. the user's battery manuscript content and hash are unchanged;
10. both repositories' remote branches match their intended local commits, with any pre-existing user-owned work reported transparently.

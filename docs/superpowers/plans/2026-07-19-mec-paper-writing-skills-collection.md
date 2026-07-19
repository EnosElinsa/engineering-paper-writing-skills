# MEC Paper Writing Skills Collection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish, globally install, and migrate five portable MEC paper-writing skills into a standalone public GitHub repository.

**Architecture:** Keep independently installable skills under `skills/`, govern the collection through one JSON manifest, and provide standard-library Python validation and copy-based installation tools. Publish and validate the standalone repository before deleting project-local copies, so migration failure never removes the working source prematurely.

**Tech Stack:** Markdown, YAML, JSON, Python standard library, `unittest`, Git, GitHub CLI, and the Codex skill creator/installer utilities.

---

### Task 1: Import and sanitize the five skills

**Files:**
- Create: `skills/writing-mec-introductions/**`
- Create: `skills/writing-mec-related-work/**`
- Create: `skills/writing-mec-system-models/**`
- Create: `skills/writing-mec-methods/**`
- Create: `skills/writing-mec-experiments/**`
- Remove from public copy: `skills/writing-mec-introductions/scripts/**`
- Modify: `skills/writing-mec-introductions/SKILL.md`
- Modify: `skills/writing-mec-introductions/references/style-and-quality-gates.md`

- [ ] **Step 1: Preserve the portability RED evidence**

Run the forbidden-content contract against the project-local Introduction skill and require failure on:

```text
audit_intro_citations.py
scripts/tests
<manuscript.md>
```

Expected: the current Introduction skill fails while all five source skills still pass `quick_validate.py` in UTF-8 mode.

- [ ] **Step 2: Copy the five existing skill trees mechanically**

Copy only these source directories from `mec-research-wiki/.agents/skills/` into this repository's `skills/` directory:

```text
writing-mec-introductions
writing-mec-related-work
writing-mec-system-models
writing-mec-methods
writing-mec-experiments
```

Do not copy `retrieve-ieee-papers` or any raw paper, wiki page, manuscript, Git metadata, or design artifact from the source project.

- [ ] **Step 3: Remove the Markdown-only Introduction auditor**

Delete the copied `writing-mec-introductions/scripts/` tree. In `SKILL.md`, remove the command block under required resources and replace the final citation gate with a format-independent audit using the manuscript's native citation system. In `style-and-quality-gates.md`, remove the entire mechanical duplicate-audit subsection while retaining accuracy, one-source-one-primary-role, exceptions, granularity, and compression guidance.

- [ ] **Step 4: Run individual GREEN checks**

For each copied skill run:

```powershell
python -X utf8 C:/Users/labs2/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

Then scan all skill files for absolute Windows paths, `.agents/skills`, `raw/sources`, `wiki/`, project tool commands, Git workflow language, and removed auditor terms.

Expected: five validator successes and zero portability matches.

- [ ] **Step 5: Commit the portable skill collection**

Stage only `skills/` and commit:

```powershell
git commit -m "feat(skills): add portable MEC paper writing collection"
```

### Task 2: Write RED tests for collection tooling

**Files:**
- Create: `tests/test_validate_skills.py`
- Create: `tests/test_install_skills.py`
- Create: `skills-manifest.json`

- [ ] **Step 1: Define the manifest**

Create JSON schema version `1` with exactly five entries. Each entry contains `name` and `path`, where path equals `skills/<name>`.

- [ ] **Step 2: Write validator tests before implementation**

Use `unittest`, `tempfile`, and `pathlib`. Import `scripts.validate_skills` and cover:

```python
class ValidateSkillsTests(unittest.TestCase):
    def test_valid_collection_has_no_errors(self): ...
    def test_rejects_manifest_name_path_mismatch(self): ...
    def test_rejects_missing_skill_metadata(self): ...
    def test_rejects_unlinked_reference(self): ...
    def test_rejects_long_reference_without_contents(self): ...
    def test_rejects_repository_specific_content(self): ...
    def test_rejects_removed_markdown_auditor(self): ...
    def test_rejects_unexpected_skill_directory(self): ...
```

- [ ] **Step 3: Write installer tests before implementation**

Import `scripts.install_skills` and cover:

```python
class InstallSkillsTests(unittest.TestCase):
    def test_installs_all_skills_to_custom_destination(self): ...
    def test_selects_one_skill(self): ...
    def test_dry_run_does_not_write(self): ...
    def test_refuses_existing_destination_without_force(self): ...
    def test_force_replaces_only_selected_skill(self): ...
    def test_rejects_unknown_skill(self): ...
    def test_source_tree_is_never_modified(self): ...
```

- [ ] **Step 4: Run the RED suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: import failures because `scripts.validate_skills` and `scripts.install_skills` do not exist.

### Task 3: Implement collection validation and installation

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/validate_skills.py`
- Create: `scripts/install_skills.py`
- Test: `tests/test_validate_skills.py`
- Test: `tests/test_install_skills.py`

- [ ] **Step 1: Implement `validate_skills.py` minimally**

Expose:

```python
def validate_collection(root: pathlib.Path) -> list[str]: ...
def main(argv: list[str] | None = None) -> int: ...
```

Load `skills-manifest.json`; validate unique manifest entries, directory agreement, required metadata, frontmatter, direct reference links, contents sections for references over 100 lines, Markdown fences/local links, and forbidden portability patterns. Print each error and return `1`, otherwise print the validated skill count and return `0`.

- [ ] **Step 2: Run validator tests and repair only observed failures**

Run:

```powershell
python -m unittest tests.test_validate_skills -v
```

Expected: all validator tests pass.

- [ ] **Step 3: Implement `install_skills.py` minimally**

Expose:

```python
def install_skills(
    root: pathlib.Path,
    destination: pathlib.Path,
    selected: list[str] | None,
    force: bool,
    dry_run: bool,
) -> list[pathlib.Path]: ...

def main(argv: list[str] | None = None) -> int: ...
```

Resolve the default destination from `CODEX_HOME` or `~/.codex/skills`. Refuse unknown skills and existing targets unless forced. Validate the collection before writing. Copy each skill into a temporary sibling, then rename it into place. On force, replace only the validated target for the selected manifest name.

- [ ] **Step 4: Run installer tests and full GREEN suite**

Run:

```powershell
python -m unittest tests.test_install_skills -v
python -m unittest discover -s tests -v
python scripts/validate_skills.py
```

Expected: all tests pass and the validator reports five valid skills.

### Task 4: Add public-repository documentation and CI

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `.gitattributes`
- Create: `.github/workflows/validate.yml`

- [ ] **Step 1: Write repository metadata**

Use MIT license text. Ignore Python cache, virtual environments, coverage, editor, and OS artifacts. Enforce LF for tracked text through `.gitattributes`.

- [ ] **Step 2: Write the README**

Document the five skills, their division of responsibility, source-grounded design, format independence, installation by GitHub request or `python scripts/install_skills.py`, validation, updates, and contribution boundary. Explicitly state that no calibration-paper corpus or Markdown-specific citation auditor is bundled.

- [ ] **Step 3: Add CI**

Create a GitHub Actions workflow for pushes and pull requests on `main`, using current stable Python, with:

```yaml
- run: python -m unittest discover -s tests -v
- run: python scripts/validate_skills.py
```

- [ ] **Step 4: Verify and commit tooling/docs**

Run all tests, collection validation, five official skill validations, portability scans, and `git diff --check`. Commit repository-owned tooling and docs with:

```powershell
git commit -m "chore: add validation, installation, and CI tooling"
```

### Task 5: Publish and globally install

**Files:**
- Publish repository: `EnosElinsa/mec-paper-writing-skills`
- Install to: `$CODEX_HOME/skills` or `~/.codex/skills`

- [ ] **Step 1: Create the public GitHub repository**

Run `gh repo create EnosElinsa/mec-paper-writing-skills --public --source . --remote origin --push`, then set the description and topics.

- [ ] **Step 2: Tag and release**

Create annotated tag `v1.0.0`, push it, and create a GitHub release summarizing the five skills and format-independent citation policy.

- [ ] **Step 3: Install with the official Codex installer**

Run `install-skill-from-github.py` once with all five `skills/<name>` paths. Do not use `--force`; all five global destinations must be absent.

- [ ] **Step 4: Verify installed hashes and remote state**

Run the official validator on each global skill, compare all installed file hashes with public source paths, verify repository visibility and release metadata, and confirm local `HEAD`, `origin/main`, and GitHub's `main` ref match.

### Task 6: Remove project-local duplicates safely

**Files:**
- Delete from `mec-research-wiki`: `.agents/skills/writing-mec-introductions/**`
- Delete from `mec-research-wiki`: `.agents/skills/writing-mec-related-work/**`
- Delete from `mec-research-wiki`: `.agents/skills/writing-mec-system-models/**`
- Delete from `mec-research-wiki`: `.agents/skills/writing-mec-methods/**`
- Delete from `mec-research-wiki`: `.agents/skills/writing-mec-experiments/**`
- Preserve: `.agents/skills/retrieve-ieee-papers/**`
- Preserve: `ideas/battery-rotation-uav-mec-stateful-service-handover.md`

- [ ] **Step 1: Create an isolated cleanup worktree**

Branch from the current `main` as `codex/globalize-mec-paper-skills`. Verify the isolated baseline is clean and the user's battery manuscript remains only in the original worktree.

- [ ] **Step 2: Delete only the five project-local skill trees**

Confirm the exact tracked file list before deletion. After deletion, assert that `.agents/skills/retrieve-ieee-papers/SKILL.md` still exists and none of the five writing-skill roots exists.

- [ ] **Step 3: Validate global replacement and project diff**

Run all five global skill validators. Require `git diff --check` and verify the cleanup diff contains only deletions under the five approved paths.

- [ ] **Step 4: Commit, merge, and push cleanup**

Commit:

```powershell
git commit -m "refactor(skills): move MEC writing skills to global collection"
```

Fast-forward `mec-research-wiki/main`, verify the battery manuscript hash is unchanged, push `origin/main`, remove the cleanup worktree and branch, and verify local/remote refs.

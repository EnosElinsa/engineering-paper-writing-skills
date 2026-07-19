from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from scripts.validate_skills import validate_collection


def _write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_collection(root: pathlib.Path, names: tuple[str, ...] = ("valid-skill",)) -> None:
    manifest = {
        "schema_version": 1,
        "skills": [
            {"name": name, "path": f"skills/{name}"}
            for name in names
        ],
    }
    _write(root / "skills-manifest.json", json.dumps(manifest, indent=2))
    for name in names:
        skill = root / "skills" / name
        _write(
            skill / "SKILL.md",
            "\n".join(
                [
                    "---",
                    f"name: {name}",
                    "description: Use when drafting a valid academic section.",
                    "---",
                    "",
                    f"# {name}",
                    "",
                    "Read [the guide](references/guide.md).",
                    "",
                ]
            ),
        )
        _write(
            skill / "agents" / "openai.yaml",
            "\n".join(
                [
                    "interface:",
                    f'  display_name: "{name}"',
                    '  short_description: "Draft a valid academic section"',
                    f'  default_prompt: "Use ${name} for this section."',
                    "",
                ]
            ),
        )
        _write(skill / "references" / "guide.md", "# Guide\n\nPortable guidance.\n")


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        make_collection(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_collection_has_no_errors(self) -> None:
        self.assertEqual(validate_collection(self.root), [])

    def test_rejects_malformed_manifest(self) -> None:
        _write(self.root / "skills-manifest.json", "{not-json")
        errors = validate_collection(self.root)
        self.assertTrue(any("manifest" in error.lower() for error in errors))

    def test_rejects_manifest_name_path_mismatch(self) -> None:
        manifest = json.loads((self.root / "skills-manifest.json").read_text())
        manifest["skills"][0]["path"] = "skills/different-name"
        _write(self.root / "skills-manifest.json", json.dumps(manifest))
        errors = validate_collection(self.root)
        self.assertTrue(any("path" in error.lower() for error in errors))

    def test_rejects_missing_skill_metadata(self) -> None:
        (self.root / "skills" / "valid-skill" / "agents" / "openai.yaml").unlink()
        errors = validate_collection(self.root)
        self.assertTrue(any("openai.yaml" in error for error in errors))

    def test_rejects_frontmatter_name_mismatch(self) -> None:
        path = self.root / "skills" / "valid-skill" / "SKILL.md"
        _write(path, path.read_text().replace("name: valid-skill", "name: wrong-name"))
        errors = validate_collection(self.root)
        self.assertTrue(any("frontmatter name" in error.lower() for error in errors))

    def test_rejects_unlinked_reference(self) -> None:
        path = self.root / "skills" / "valid-skill" / "SKILL.md"
        _write(path, path.read_text().replace("Read [the guide](references/guide.md).", "No guide link."))
        errors = validate_collection(self.root)
        self.assertTrue(any("not linked" in error.lower() for error in errors))

    def test_rejects_long_reference_without_contents(self) -> None:
        path = self.root / "skills" / "valid-skill" / "references" / "guide.md"
        _write(path, "# Guide\n" + "evidence line\n" * 101)
        errors = validate_collection(self.root)
        self.assertTrue(any("contents" in error.lower() for error in errors))

    def test_rejects_repository_specific_content(self) -> None:
        path = self.root / "skills" / "valid-skill" / "SKILL.md"
        _write(path, path.read_text() + "Read evidence from raw/sources before drafting.\n")
        errors = validate_collection(self.root)
        self.assertTrue(any("forbidden" in error.lower() for error in errors))

    def test_rejects_removed_markdown_auditor(self) -> None:
        script = self.root / "skills" / "valid-skill" / "scripts" / "audit_intro_citations.py"
        _write(script, "print('format-specific audit')\n")
        errors = validate_collection(self.root)
        self.assertTrue(any("audit_intro_citations" in error for error in errors))

    def test_rejects_unexpected_skill_directory(self) -> None:
        _write(self.root / "skills" / "extra-skill" / "SKILL.md", "unexpected\n")
        errors = validate_collection(self.root)
        self.assertTrue(any("unexpected skill directory" in error.lower() for error in errors))

    def test_rejects_unbalanced_markdown_fence(self) -> None:
        path = self.root / "skills" / "valid-skill" / "SKILL.md"
        _write(path, path.read_text() + "```text\nunclosed\n")
        errors = validate_collection(self.root)
        self.assertTrue(any("code fence" in error.lower() for error in errors))

    def test_rejects_missing_local_link_target(self) -> None:
        path = self.root / "skills" / "valid-skill" / "SKILL.md"
        _write(path, path.read_text().replace("references/guide.md", "references/missing.md"))
        errors = validate_collection(self.root)
        self.assertTrue(any("missing local link" in error.lower() for error in errors))


if __name__ == "__main__":
    unittest.main()

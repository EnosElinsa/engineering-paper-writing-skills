from __future__ import annotations

import json
import pathlib
import unittest

from scripts.validate_skills import FORBIDDEN_PATTERNS, shared_destination


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = "references/core/reader-and-terminology-contract.md"
STYLE = "references/styles/team-house-style.md"
SCRIPT = "scripts/style_fingerprint.py"
SECTION_SKILLS = (
    "write-introductions",
    "write-related-work",
    "write-system-models",
    "write-methods",
    "write-experiments",
    "write-abstracts-and-conclusions",
)


class SharedContractTests(unittest.TestCase):
    def _copy(self, skill: str) -> pathlib.Path:
        return ROOT / "skills" / skill / CONTRACT

    def test_copies_are_byte_identical(self) -> None:
        copies = {skill: self._copy(skill).read_bytes() for skill in SECTION_SKILLS}
        reference = copies[SECTION_SKILLS[0]]
        for skill, content in copies.items():
            self.assertEqual(reference, content, f"{skill} contract copy has drifted")

    def test_each_skill_links_the_contract_directly(self) -> None:
        for skill in SECTION_SKILLS:
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"]({CONTRACT})", text, f"{skill} does not link the contract")

    def test_section_skills_and_audit_link_the_house_style_and_script(self) -> None:
        for skill in (*SECTION_SKILLS, "latex-prose-audit"):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"]({STYLE})", text, f"{skill} does not link the house style")
            self.assertIn(f"]({SCRIPT})", text, f"{skill} does not link the fingerprint script")

    def test_every_manifest_copy_matches_its_shared_source(self) -> None:
        manifest = json.loads((ROOT / "shared-files.json").read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            source = ROOT / entry["source"]
            destination = shared_destination(entry["source"])
            expected = source.read_bytes()
            for skill in entry["targets"]:
                copy = ROOT / "skills" / skill / destination
                self.assertTrue(copy.is_file(), f"{skill} is missing {destination}")
                self.assertEqual(expected, copy.read_bytes(), f"{skill} {destination} differs from its shared source")

    def test_shared_sources_have_no_forbidden_pattern(self) -> None:
        for path in sorted((ROOT / "shared").rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix not in {".md", ".py"}:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in FORBIDDEN_PATTERNS:
                self.assertIsNone(pattern.search(text), f"{path.name} contains forbidden {label}")


if __name__ == "__main__":
    unittest.main()

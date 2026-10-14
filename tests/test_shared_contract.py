from __future__ import annotations

import pathlib
import unittest

from scripts.validate_skills import FORBIDDEN_PATTERNS


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = "references/core/reader-and-terminology-contract.md"
SECTION_SKILLS = (
    "write-introductions",
    "write-related-work",
    "write-system-models",
    "write-methods",
    "write-experiments",
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

    def test_contract_has_no_forbidden_pattern(self) -> None:
        text = self._copy(SECTION_SKILLS[0]).read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS:
            self.assertIsNone(pattern.search(text), f"contract contains forbidden {label}")


if __name__ == "__main__":
    unittest.main()

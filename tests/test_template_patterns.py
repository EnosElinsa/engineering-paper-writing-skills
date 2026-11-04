"""Recommended sentence patterns must not model constructions the house style bans."""

from __future__ import annotations

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]

# (file, heading) pairs whose bullet or table lines present sentence patterns to imitate.
PATTERN_SECTIONS = (
    ("skills/write-experiments/references/core/contract-and-quality-gates.md", "### Preferred openings"),
    ("skills/write-experiments/references/core/contract-and-quality-gates.md", "### Transitions"),
    ("skills/write-introductions/references/core/contract-and-quality-gates.md", "### Functional English sentence patterns"),
    ("skills/write-methods/references/core/contract-and-quality-gates.md", "### 11.2 Verb discipline"),
    ("skills/write-methods/references/methods/evolutionary-algorithms.md", "### 10.1 Suitable opening language"),
    ("skills/write-methods/references/methods/evolutionary-algorithms.md", "### 10.2 Encoding language"),
    ("skills/write-methods/references/methods/evolutionary-algorithms.md", "### 10.3 Framework language"),
    ("skills/write-methods/references/methods/evolutionary-algorithms.md", "### 10.4 Mechanism language"),
    ("skills/write-methods/references/methods/evolutionary-algorithms.md", "### 10.5 Output language"),
    ("skills/write-methods/references/methods/reinforcement-learning.md", "### 12.1 Problem-to-RL transition"),
    ("skills/write-methods/references/methods/reinforcement-learning.md", "### 12.2 MDP interface"),
    ("skills/write-methods/references/methods/reinforcement-learning.md", "### 12.3 Architecture"),
    ("skills/write-methods/references/methods/reinforcement-learning.md", "### 12.4 Action realization"),
    ("skills/write-methods/references/methods/reinforcement-learning.md", "### 12.5 Training"),
    ("skills/write-system-models/references/core/contract-and-quality-gates.md", "## 11. Language and style"),
    ("shared/styles/team-house-style.md", "## 4. Combining and splitting sentences", "Synthetic examples:"),
    ("shared/styles/team-house-style.md", "## 9. Paragraph openers by section"),
    ("shared/styles/team-house-style.md", "## 10. Title, abstract, and index terms"),
    ("shared/styles/team-house-style.md", "## 11. Contribution list and roadmap"),
    ("shared/styles/team-house-style.md", "## 12. Conclusion"),
    ("skills/write-abstracts-and-conclusions/references/core/contract-and-quality-gates.md", "## 2. Title"),
    ("skills/write-abstracts-and-conclusions/references/core/contract-and-quality-gates.md", "## 3. Abstract"),
    ("skills/write-abstracts-and-conclusions/references/core/contract-and-quality-gates.md", "## 5. Contribution list and roadmap"),
    ("skills/write-abstracts-and-conclusions/references/core/contract-and-quality-gates.md", "## 6. Conclusion"),
    ("skills/write-abstracts-and-conclusions/references/core/contract-and-quality-gates.md", "## 7. Future work"),
)

BANNED = (
    ("because", re.compile(r"\bbecause\b", re.I)),
    ("so", re.compile(r",\s*so\b|\bso that\b|\bso as to\b", re.I)),
    (", but", re.compile(r",\s*but\b")),
    ("semicolon", re.compile(r";")),
    ("Hence", re.compile(r"\bHence\b")),
    ("Accordingly", re.compile(r"\bAccordingly\b")),
    ("e.g.", re.compile(r"\be\.g\.")),
    ("first person outside future work", re.compile(r"\b[Ww]e\b(?!\s+will)|\b[Oo]ur\b")),
)

def _stops(line: str) -> bool:
    """True for a line that opens a list of constructions to avoid."""
    stripped = line.strip().lstrip("-* ").strip()
    return bool(re.match(r"(?i)(avoid|do not|weak)\b", stripped) or re.search(r"(?i)\bavoid:\s*$", stripped))


def section_lines(path: pathlib.Path, heading: str, start_marker: str | None = None) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(heading)
    except ValueError as error:
        raise AssertionError(f"{path.relative_to(ROOT)} has no heading {heading!r}") from error
    level = len(heading) - len(heading.lstrip("#"))
    collected: list[str] = []
    started = start_marker is None
    for line in lines[start + 1:]:
        match = re.match(r"^(#+)\s", line)
        if match and len(match.group(1)) <= level:
            break
        if not started:
            started = line.strip().startswith(start_marker)
            continue
        if _stops(line):
            break
        collected.append(line)
    return collected


def templates(lines: list[str]) -> list[str]:
    spans: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("-", "|", ">")) or re.match(r"^\d+\.", stripped) or stripped.startswith("Synthetic"):
            spans.extend(re.findall(r"`([^`]+)`", stripped))
    return spans


class TemplatePatternTests(unittest.TestCase):
    def test_pattern_sections_exist_and_contain_templates(self) -> None:
        for file, heading, *marker in PATTERN_SECTIONS:
            spans = templates(section_lines(ROOT / file, heading, *marker))
            self.assertTrue(spans, f"{file} {heading} has no template patterns")

    def test_templates_avoid_banned_constructions(self) -> None:
        problems = []
        for file, heading, *marker in PATTERN_SECTIONS:
            for span in templates(section_lines(ROOT / file, heading, *marker)):
                for label, pattern in BANNED:
                    if pattern.search(span):
                        problems.append(f"{file} {heading}: {label} in `{span}`")
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()

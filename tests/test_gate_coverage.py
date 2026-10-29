from __future__ import annotations

import collections
import json
import pathlib
import re
import unittest

from scripts.validate_skills import shared_destination


ROOT = pathlib.Path(__file__).resolve().parents[1]
GATE_ID_RE = re.compile(r"\[(G-[A-Z]+-[A-Za-z0-9-]+)\]")
CASE_COUNT = 25


def _load_index() -> dict:
    return json.loads((ROOT / "tests" / "gate-index.json").read_text(encoding="utf-8"))


def _shared_targets(source: str) -> list[pathlib.Path]:
    manifest = json.loads((ROOT / "shared-files.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        if entry["source"] == source:
            destination = shared_destination(source)
            return [ROOT / "skills" / skill / destination for skill in entry["targets"]]
    raise AssertionError(f"{source} is not declared in shared-files.json")


def _paths_for(file: str) -> list[pathlib.Path]:
    path = ROOT / file
    if file.startswith("shared/"):
        return [path, *_shared_targets(file)]
    return [path]


class GateCoverageTests(unittest.TestCase):
    def test_all_cases_have_at_least_one_gate(self) -> None:
        cases = _load_index()["cases"]
        self.assertEqual(sorted(cases, key=int), [str(number) for number in range(1, CASE_COUNT + 1)])
        for number, case in cases.items():
            self.assertTrue(case["gates"], f"case {number} has no gate entry")

    def test_every_referenced_gate_appears_exactly_once_in_its_files(self) -> None:
        for number, case in _load_index()["cases"].items():
            for gate in case["gates"]:
                self.assertRegex(gate["id"], r"^G-[A-Z]+-[A-Za-z0-9-]+$")
                for path in _paths_for(gate["file"]):
                    self.assertTrue(path.is_file(), f"case {number}: {path} is missing")
                    count = path.read_text(encoding="utf-8").count(f"[{gate['id']}]")
                    self.assertEqual(
                        count,
                        1,
                        f"case {number}: {gate['id']} appears {count} times in {path.relative_to(ROOT)}",
                    )

    def test_no_gate_is_defined_twice_in_one_file(self) -> None:
        roots = [ROOT / "skills", ROOT / "shared"]
        for base in roots:
            for path in sorted(base.rglob("*.md")):
                ids = GATE_ID_RE.findall(path.read_text(encoding="utf-8"))
                repeated = [gate for gate, count in collections.Counter(ids).items() if count > 1]
                self.assertEqual(repeated, [], f"{path.relative_to(ROOT)} repeats {repeated}")

    def test_every_case_has_a_fixture(self) -> None:
        directory = ROOT / "tests" / "fixtures" / "failure-cases"
        for number in range(1, CASE_COUNT + 1):
            self.assertTrue((directory / f"case-{number:02d}.md").is_file(), f"case {number} fixture missing")
        self.assertEqual(len(list(directory.glob("negative-control-*.md"))), 4)

    def test_fixtures_name_only_indexed_gates(self) -> None:
        index = _load_index()["cases"]
        directory = ROOT / "tests" / "fixtures" / "failure-cases"
        for number in range(1, CASE_COUNT + 1):
            text = (directory / f"case-{number:02d}.md").read_text(encoding="utf-8")
            line = next(item for item in text.splitlines() if item.startswith("Expected gates:"))
            named = {item.strip() for item in line.split(":", 1)[1].split(",")}
            indexed = {gate["id"] for gate in index[str(number)]["gates"]}
            self.assertEqual(named, indexed, f"case {number} fixture and index disagree")


if __name__ == "__main__":
    unittest.main()

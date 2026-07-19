from __future__ import annotations

import hashlib
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts.install_skills import install_skills, resolve_default_destination
from tests.test_validate_skills import make_collection


def _tree_digest(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


class InstallSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name) / "source"
        self.destination = pathlib.Path(self.temp.name) / "global-skills"
        make_collection(self.root, ("first-skill", "second-skill"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_installs_all_skills_to_custom_destination(self) -> None:
        installed = install_skills(self.root, self.destination, None, False, False)
        self.assertEqual([path.name for path in installed], ["first-skill", "second-skill"])
        self.assertTrue((self.destination / "first-skill" / "SKILL.md").is_file())
        self.assertTrue((self.destination / "second-skill" / "SKILL.md").is_file())

    def test_selects_one_skill(self) -> None:
        installed = install_skills(
            self.root, self.destination, ["second-skill"], False, False
        )
        self.assertEqual(installed, [self.destination / "second-skill"])
        self.assertFalse((self.destination / "first-skill").exists())

    def test_dry_run_does_not_write(self) -> None:
        installed = install_skills(self.root, self.destination, None, False, True)
        self.assertEqual(len(installed), 2)
        self.assertFalse(self.destination.exists())

    def test_refuses_existing_destination_without_force(self) -> None:
        install_skills(self.root, self.destination, ["first-skill"], False, False)
        with self.assertRaises(FileExistsError):
            install_skills(self.root, self.destination, ["first-skill"], False, False)

    def test_force_replaces_only_selected_skill(self) -> None:
        install_skills(self.root, self.destination, None, False, False)
        stale = self.destination / "first-skill" / "stale.txt"
        stale.write_text("stale", encoding="utf-8")
        second_before = _tree_digest(self.destination / "second-skill")
        install_skills(self.root, self.destination, ["first-skill"], True, False)
        self.assertFalse(stale.exists())
        self.assertEqual(second_before, _tree_digest(self.destination / "second-skill"))

    def test_rejects_unknown_skill(self) -> None:
        with self.assertRaises(ValueError):
            install_skills(self.root, self.destination, ["missing-skill"], False, False)

    def test_source_tree_is_never_modified(self) -> None:
        before = _tree_digest(self.root)
        install_skills(self.root, self.destination, None, False, False)
        self.assertEqual(before, _tree_digest(self.root))

    def test_codex_home_controls_default_destination(self) -> None:
        codex_home = pathlib.Path(self.temp.name) / "codex-home"
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(codex_home)}):
            self.assertEqual(resolve_default_destination(), codex_home / "skills")

    def test_script_entrypoint_runs_from_repository_root(self) -> None:
        repository = pathlib.Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [
                sys.executable,
                str(repository / "scripts" / "install_skills.py"),
                "--root",
                str(self.root),
                "--dest",
                str(self.destination),
                "--dry-run",
            ],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Would install", result.stdout)


if __name__ == "__main__":
    unittest.main()

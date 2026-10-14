from __future__ import annotations

import contextlib
import io
import pathlib
import tempfile
import unittest

from scripts.sync_shared import main, sync_shared
from tests.test_validate_skills import SHARED_COPY, add_shared_file, make_collection


def run_main(*arguments: str) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return main(list(arguments))


class SyncSharedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.skills = ("first-skill", "second-skill")
        make_collection(self.root, self.skills)
        add_shared_file(self.root, self.skills)
        self.copy = self.root / "skills" / "second-skill" / SHARED_COPY

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_check_passes_when_copies_match(self) -> None:
        self.assertEqual(run_main("--root", str(self.root), "--check"), 0)

    def test_check_fails_on_drift_without_writing(self) -> None:
        self.copy.write_text("# Common\n\nEdited locally.\n", encoding="utf-8")
        problems, updated = sync_shared(self.root, check=True)
        self.assertTrue(any("diverged" in problem for problem in problems))
        self.assertEqual(updated, [])
        self.assertEqual(self.copy.read_text(encoding="utf-8"), "# Common\n\nEdited locally.\n")
        self.assertEqual(run_main("--root", str(self.root), "--check"), 1)

    def test_check_fails_on_missing_copy(self) -> None:
        self.copy.unlink()
        self.assertEqual(run_main("--root", str(self.root), "--check"), 1)
        self.assertFalse(self.copy.exists())

    def test_sync_restores_drifted_and_missing_copies(self) -> None:
        self.copy.write_text("drifted\n", encoding="utf-8")
        (self.root / "skills" / "first-skill" / SHARED_COPY).unlink()
        self.assertEqual(run_main("--root", str(self.root)), 0)
        self.assertEqual(run_main("--root", str(self.root), "--check"), 0)
        source = (self.root / "shared" / "core" / "common.md").read_bytes()
        self.assertEqual(self.copy.read_bytes(), source)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Copy shared canonical sources into the skills that bundle them, or check for drift."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts.validate_skills import load_manifest, load_shared_files, shared_destination


def sync_shared(root: pathlib.Path, check: bool) -> tuple[list[str], list[str]]:
    """Return (problems, updated). In check mode nothing is written and drift is a problem."""
    root = pathlib.Path(root).resolve()
    skill_entries, manifest_errors = load_manifest(root)
    entries, shared_errors = load_shared_files(
        root, {entry["name"] for entry in skill_entries}
    )
    problems = list(manifest_errors) + list(shared_errors)
    if problems:
        return problems, []

    updated: list[str] = []
    for entry in entries:
        source = root / pathlib.PurePosixPath(entry["source"])
        if not source.is_file():
            problems.append(f"{source}: shared source is missing")
            continue
        expected = source.read_bytes()
        destination = shared_destination(entry["source"])
        for skill in entry["targets"]:
            copy = root / "skills" / skill / pathlib.PurePosixPath(destination)
            if copy.is_file() and copy.read_bytes() == expected:
                continue
            state = "has diverged from" if copy.is_file() else "is missing; source is"
            if check:
                problems.append(f"{copy}: shared copy {state} {entry['source']}")
                continue
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, copy)
            updated.append(str(copy))
    return problems, updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
        help="Collection repository root",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare only; exit non-zero when a copy has drifted or is missing",
    )
    args = parser.parse_args(argv)
    problems, updated = sync_shared(args.root, args.check)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print(f"Shared files are out of sync ({len(problems)} problem(s)).", file=sys.stderr)
        return 1
    if args.check:
        print("Shared files are in sync.")
    else:
        for path in updated:
            print(f"Updated: {path}")
        print(f"Synchronized shared files ({len(updated)} updated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

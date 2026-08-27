#!/usr/bin/env python3
"""Install engineering-paper writing skills into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import sys
import uuid

if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from scripts.validate_skills import load_manifest, validate_collection


def resolve_default_destination() -> pathlib.Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = pathlib.Path(codex_home).expanduser() if codex_home else pathlib.Path.home() / ".codex"
    return base / "skills"


def _path_exists(path: pathlib.Path) -> bool:
    return path.exists() or path.is_symlink()


def _remove_path(path: pathlib.Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install_skills(
    root: pathlib.Path,
    destination: pathlib.Path,
    selected: list[str] | None,
    force: bool,
    dry_run: bool,
) -> list[pathlib.Path]:
    root = pathlib.Path(root).resolve()
    destination = pathlib.Path(destination).expanduser().resolve()
    validation_errors = validate_collection(root)
    if validation_errors:
        raise ValueError("Collection validation failed:\n" + "\n".join(validation_errors))

    entries, manifest_errors = load_manifest(root)
    if manifest_errors:
        raise ValueError("Manifest validation failed:\n" + "\n".join(manifest_errors))
    by_name = {entry["name"]: entry for entry in entries}
    names = list(by_name) if selected is None else list(dict.fromkeys(selected))
    unknown = [name for name in names if name not in by_name]
    if unknown:
        raise ValueError(f"Unknown skill(s): {', '.join(unknown)}")

    targets = [destination / name for name in names]
    for name, target in zip(names, targets, strict=True):
        if target.name != name or target.parent != destination:
            raise ValueError(f"Unsafe installation target: {target}")
        if _path_exists(target) and not force:
            raise FileExistsError(f"Destination already exists: {target}")
    if dry_run:
        return targets

    destination.mkdir(parents=True, exist_ok=True)
    installed: list[pathlib.Path] = []
    for name, target in zip(names, targets, strict=True):
        source = root / pathlib.PurePosixPath(by_name[name]["path"])
        token = uuid.uuid4().hex
        temporary = destination / f".{name}.tmp-{token}"
        backup = destination / f".{name}.backup-{token}"
        try:
            shutil.copytree(source, temporary)
            if not (temporary / "SKILL.md").is_file():
                raise ValueError(f"Copied skill is incomplete: {name}")
            if _path_exists(target):
                target.rename(backup)
                try:
                    temporary.rename(target)
                except BaseException:
                    backup.rename(target)
                    raise
                else:
                    _remove_path(backup)
            else:
                temporary.rename(target)
            installed.append(target)
        finally:
            if _path_exists(temporary):
                _remove_path(temporary)
            if _path_exists(backup) and not _path_exists(target):
                backup.rename(target)
    return installed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
        help="Collection repository root",
    )
    parser.add_argument(
        "--dest",
        type=pathlib.Path,
        default=None,
        help="Target skills directory (default: $CODEX_HOME/skills or ~/.codex/skills)",
    )
    parser.add_argument("--skill", action="append", dest="skills", help="Install one named skill")
    parser.add_argument("--force", action="store_true", help="Replace selected existing skills")
    parser.add_argument("--dry-run", action="store_true", help="Report targets without writing")
    args = parser.parse_args(argv)
    destination = args.dest if args.dest is not None else resolve_default_destination()
    try:
        installed = install_skills(
            args.root, destination, args.skills, args.force, args.dry_run
        )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    action = "Would install" if args.dry_run else "Installed"
    for path in installed:
        print(f"{action}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

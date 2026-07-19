#!/usr/bin/env python3
"""Validate the portable MEC paper-writing skill collection."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any
from urllib.parse import unquote


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_ALLOWED = {"name", "description"}
FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Windows absolute path", re.compile(r"(?i)\b[A-Z]:[\\/]")),
    ("Unix home path", re.compile(r"(?i)(?:^|[\s`'\"])/(?:home|Users)/")),
    ("file URI", re.compile(r"(?i)file://")),
    ("project skill path", re.compile(r"(?i)\.agents[\\/]skills")),
    ("research corpus path", re.compile(r"(?i)raw[\\/]sources")),
    ("research wiki name", re.compile(r"(?i)mec-research-wiki")),
    ("wiki path", re.compile(r"(?i)(?:^|[\s`'\"])wiki[\\/]")),
    ("repository-local wording", re.compile(r"(?i)(?:repo|repository)-local")),
    ("repository-specific wording", re.compile(r"(?i)repository-specific")),
    ("Git workflow command", re.compile(r"(?i)\bgit\s+(?:status|commit|push|checkout|merge)\b")),
    ("project link checker", re.compile(r"(?i)linkcheck\.py")),
    ("removed citation auditor", re.compile(r"(?i)audit_intro_citations")),
    ("Markdown manuscript placeholder", re.compile(r"(?i)<manuscript\.md>")),
    ("test-tree dependency", re.compile(r"(?i)scripts[\\/]tests")),
    ("unfinished marker", re.compile(r"(?i)\b(?:TODO|TBD|PLACEHOLDER)\b")),
)


def _read_text(path: pathlib.Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"{path}: cannot read UTF-8 text: {error}")
        return None


def load_manifest(root: pathlib.Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    path = root / "skills-manifest.json"
    text = _read_text(path, errors)
    if text is None:
        return [], errors
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError as error:
        return [], [f"{path}: malformed manifest: {error}"]
    if not isinstance(data, dict):
        return [], [f"{path}: manifest root must be an object"]
    if data.get("schema_version") != 1:
        errors.append(f"{path}: manifest schema_version must be 1")
    raw_skills = data.get("skills")
    if not isinstance(raw_skills, list) or not raw_skills:
        errors.append(f"{path}: manifest skills must be a non-empty list")
        return [], errors

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_skills):
        label = f"{path}: skills[{index}]"
        if not isinstance(raw, dict) or set(raw) != {"name", "path"}:
            errors.append(f"{label} must contain exactly name and path")
            continue
        name = raw.get("name")
        relative = raw.get("path")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{label} has an invalid skill name")
            continue
        if name in seen:
            errors.append(f"{label} repeats skill name {name}")
            continue
        seen.add(name)
        expected = f"skills/{name}"
        if relative != expected:
            errors.append(f"{label} path must be {expected}")
            continue
        entries.append({"name": name, "path": relative})
    return entries, errors


def _parse_frontmatter(path: pathlib.Path, text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: SKILL.md must start with YAML frontmatter"]
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, [f"{path}: SKILL.md frontmatter is not closed"]

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path}: malformed frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in values:
            errors.append(f"{path}: duplicate frontmatter field {key}")
        values[key] = value.strip("\"'")
    extra = set(values) - FRONTMATTER_ALLOWED
    missing = FRONTMATTER_ALLOWED - set(values)
    if extra:
        errors.append(f"{path}: unsupported frontmatter fields: {', '.join(sorted(extra))}")
    if missing:
        errors.append(f"{path}: missing frontmatter fields: {', '.join(sorted(missing))}")
    return values, errors


def _slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9 _-]", "", value)
    value = re.sub(r"[ _]+", "-", value)
    return value.strip("-")


def _heading_slugs(text: str) -> set[str]:
    return {_slug(match.group(1)) for match in HEADING_RE.finditer(text)}


def _check_anchor(
    source: pathlib.Path,
    target: pathlib.Path,
    anchor: str,
    errors: list[str],
) -> None:
    target_text = _read_text(target, errors)
    if target_text is not None and anchor not in _heading_slugs(target_text):
        errors.append(f"{source}: missing local anchor #{anchor} in {target}")


def _validate_markdown(path: pathlib.Path, text: str, skill_root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    fence_count = sum(1 for line in text.splitlines() if line.startswith("```"))
    if fence_count % 2:
        errors.append(f"{path}: unbalanced Markdown code fence")

    current_headings = _heading_slugs(text)
    resolved_skill = skill_root.resolve()
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        if not raw_target or re.match(r"(?i)^(?:https?://|mailto:)", raw_target):
            continue
        decoded = unquote(raw_target)
        if decoded.startswith("#"):
            anchor = decoded[1:]
            if anchor not in current_headings:
                errors.append(f"{path}: missing local anchor #{anchor}")
            continue
        target_text, separator, anchor = decoded.partition("#")
        target_path = pathlib.Path(target_text)
        if target_path.is_absolute():
            errors.append(f"{path}: absolute local link is not portable: {decoded}")
            continue
        resolved = (path.parent / target_path).resolve()
        if not resolved.is_relative_to(resolved_skill):
            errors.append(f"{path}: local link escapes the skill directory: {decoded}")
            continue
        if not resolved.exists():
            errors.append(f"{path}: missing local link target: {decoded}")
            continue
        if separator and resolved.is_file():
            _check_anchor(path, resolved, anchor, errors)
    return errors


def _validate_skill(root: pathlib.Path, entry: dict[str, str]) -> list[str]:
    errors: list[str] = []
    name = entry["name"]
    skill = root / pathlib.PurePosixPath(entry["path"])
    if not skill.is_dir():
        return [f"{skill}: manifest skill directory is missing"]

    skill_md = skill / "SKILL.md"
    metadata = skill / "agents" / "openai.yaml"
    for required in (skill_md, metadata):
        if not required.is_file():
            errors.append(f"{required}: required file is missing")

    skill_text = _read_text(skill_md, errors) if skill_md.is_file() else None
    if skill_text is not None:
        frontmatter, frontmatter_errors = _parse_frontmatter(skill_md, skill_text)
        errors.extend(frontmatter_errors)
        if frontmatter.get("name") != name:
            errors.append(
                f"{skill_md}: frontmatter name {frontmatter.get('name')!r} does not match {name!r}"
            )
        description = frontmatter.get("description", "")
        if description and not description.startswith("Use when"):
            errors.append(f"{skill_md}: description must start with 'Use when'")

    reference_dir = skill / "references"
    references = sorted(reference_dir.rglob("*")) if reference_dir.is_dir() else []
    for reference in (path for path in references if path.is_file()):
        relative = reference.relative_to(skill).as_posix()
        if skill_text is not None and relative not in skill_text:
            errors.append(f"{reference}: bundled reference is not linked directly from SKILL.md")
        reference_text = _read_text(reference, errors)
        if reference_text is None:
            continue
        if len(reference_text.splitlines()) > 100 and not re.search(
            r"^## (?:Contents|Table of Contents)\s*$", reference_text, re.MULTILINE
        ):
            errors.append(f"{reference}: long reference must include a Contents section")

    for path in sorted(item for item in skill.rglob("*") if item.is_file()):
        text = _read_text(path, errors)
        if text is None:
            continue
        relative = path.relative_to(root).as_posix()
        for label, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text) or pattern.search(relative):
                errors.append(f"{path}: forbidden {label}")
        if path.suffix.lower() == ".md":
            errors.extend(_validate_markdown(path, text, skill))
    return errors


def validate_collection(root: pathlib.Path) -> list[str]:
    root = pathlib.Path(root).resolve()
    entries, errors = load_manifest(root)
    manifest_names = {entry["name"] for entry in entries}
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        errors.append(f"{skills_dir}: skills directory is missing")
        return sorted(set(errors))

    actual_names = {path.name for path in skills_dir.iterdir() if path.is_dir()}
    for name in sorted(actual_names - manifest_names):
        errors.append(f"{skills_dir / name}: unexpected skill directory")
    for name in sorted(manifest_names - actual_names):
        errors.append(f"{skills_dir / name}: manifest skill directory is missing")
    for entry in entries:
        errors.extend(_validate_skill(root, entry))
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
        help="Collection repository root",
    )
    args = parser.parse_args(argv)
    errors = validate_collection(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    entries, _ = load_manifest(args.root.resolve())
    print(f"Validated {len(entries)} portable skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

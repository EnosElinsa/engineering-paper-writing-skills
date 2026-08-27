#!/usr/bin/env python3
"""Validate the portable engineering-paper writing skill collection."""

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
DOMAIN_FIELDS = {"name", "display_name", "description", "skills"}
DOMAIN_SKILL_FIELDS = {"name", "reference"}
DOMAIN_INDEPENDENT_SKILLS = {"latex-prose-audit"}
LEGACY_SKILL_PREFIX = "writing-mec-"
LEGACY_REPOSITORY_NAME = "mec-paper-writing-skills"
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
        if name.startswith(LEGACY_SKILL_PREFIX):
            errors.append(f"{label} uses legacy MEC-only skill name {name}")
        expected = f"skills/{name}"
        if relative != expected:
            errors.append(f"{label} path must be {expected}")
            continue
        entries.append({"name": name, "path": relative})
    return entries, errors


def load_domain_packs(
    root: pathlib.Path,
    manifest_names: set[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    path = root / "domain-packs.json"
    text = _read_text(path, errors)
    if text is None:
        if not path.exists():
            errors.append(f"{path}: domain-pack manifest is missing")
        return [], errors
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError as error:
        return [], [f"{path}: malformed domain-pack manifest: {error}"]
    if not isinstance(data, dict):
        return [], [f"{path}: domain-pack manifest root must be an object"]
    if data.get("schema_version") != 1:
        errors.append(f"{path}: domain-pack schema_version must be 1")
    raw_domains = data.get("domains")
    if not isinstance(raw_domains, list):
        errors.append(f"{path}: domains must be a list")
        return [], errors

    domains: list[dict[str, Any]] = []
    seen_domains: set[str] = set()
    for domain_index, raw_domain in enumerate(raw_domains):
        label = f"{path}: domains[{domain_index}]"
        if not isinstance(raw_domain, dict) or set(raw_domain) != DOMAIN_FIELDS:
            errors.append(
                f"{label} must contain exactly name, display_name, description, and skills"
            )
            continue
        name = raw_domain.get("name")
        display_name = raw_domain.get("display_name")
        description = raw_domain.get("description")
        raw_skills = raw_domain.get("skills")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{label} has an invalid domain name")
            continue
        if name in seen_domains:
            errors.append(f"{label} repeats domain name {name}")
            continue
        seen_domains.add(name)
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{label} display_name must be a non-empty string")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{label} description must be a non-empty string")
        if not isinstance(raw_skills, list) or not raw_skills:
            errors.append(f"{label} skills must be a non-empty list")
            continue

        skills: list[dict[str, str]] = []
        seen_skills: set[str] = set()
        for skill_index, raw_skill in enumerate(raw_skills):
            skill_label = f"{label}.skills[{skill_index}]"
            if not isinstance(raw_skill, dict) or set(raw_skill) != DOMAIN_SKILL_FIELDS:
                errors.append(f"{skill_label} must contain exactly name and reference")
                continue
            skill_name = raw_skill.get("name")
            reference = raw_skill.get("reference")
            if not isinstance(skill_name, str) or not NAME_RE.fullmatch(skill_name):
                errors.append(f"{skill_label} has an invalid skill name")
                continue
            if skill_name in seen_skills:
                errors.append(f"{skill_label} repeats skill name {skill_name}")
                continue
            seen_skills.add(skill_name)
            if skill_name not in manifest_names:
                errors.append(f"{skill_label} refers to unknown skill {skill_name}")
            if skill_name in DOMAIN_INDEPENDENT_SKILLS:
                errors.append(f"{skill_label}: {skill_name} must remain domain-independent")
            expected = f"references/domains/{name}.md"
            if reference != expected:
                errors.append(f"{skill_label} reference must be {expected}")
                continue
            skills.append({"name": skill_name, "reference": reference})
        domains.append(
            {
                "name": name,
                "display_name": display_name,
                "description": description,
                "skills": skills,
            }
        )
    return domains, errors


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

    domains, domain_errors = load_domain_packs(root, manifest_names)
    errors.extend(domain_errors)
    declared_domain_refs: set[tuple[str, str]] = set()
    for domain in domains:
        for domain_skill in domain["skills"]:
            skill_name = domain_skill["name"]
            reference = domain_skill["reference"]
            declared_domain_refs.add((skill_name, reference))
            target = root / "skills" / skill_name / pathlib.PurePosixPath(reference)
            if skill_name in manifest_names and not target.is_file():
                errors.append(f"{target}: declared domain reference is missing")

    actual_domain_refs: set[tuple[str, str]] = set()
    for entry in entries:
        domain_dir = root / pathlib.PurePosixPath(entry["path"]) / "references" / "domains"
        if domain_dir.is_dir():
            for reference in domain_dir.glob("*.md"):
                relative = reference.relative_to(
                    root / pathlib.PurePosixPath(entry["path"])
                ).as_posix()
                actual_domain_refs.add((entry["name"], relative))
    for skill_name, reference in sorted(actual_domain_refs - declared_domain_refs):
        errors.append(
            f"{root / 'skills' / skill_name / pathlib.PurePosixPath(reference)}: "
            "domain reference is not declared in domain-packs.json"
        )

    readme = root / "README.md"
    if readme.is_file():
        readme_text = _read_text(readme, errors)
        if readme_text is not None and LEGACY_REPOSITORY_NAME in readme_text:
            errors.append(f"{readme}: contains legacy repository identity")
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

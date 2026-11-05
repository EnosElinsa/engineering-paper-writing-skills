#!/usr/bin/env python3
"""Recalibrate the team house-style band from a set of reference papers.

Measures every reference paper with the shared fingerprint script, proposes the
sentence-rhythm band (minimum to maximum over the references), and, with --write,
rewrites the three generated blocks that hold it:

- the TEAM_BAND literal in shared/scripts/style_fingerprint.py;
- the rhythm tables in shared/styles/team-house-style.md (Section 3);
- the weak-prior Chinese tables in shared/languages/zh.md;
- the rhythm lines of the quick card in shared/styles/house-style-card.md.

It also replaces the abstract and Conclusion ranges in Sections 10 and 12 of the
house style. Prose elsewhere (provenance, the corpus list) is reported for manual
review, not rewritten. Run `python scripts/sync_shared.py` afterwards.

Usage:
    python scripts/calibrate_house_style.py --references DIR_OR_FILE ... \\
        [--approved FILE ...] [--baseline FILE] [--abstract-limit 250] [--check | --write]

--approved   supervisor-approved drafts whose values widen every band (body measures,
             section means, abstract, and Conclusion), so that the band covers the
             supervisor's own practice as well as the reference papers.
--baseline   one supervisor-approved draft whose body values fill the last column
             of the house-style rhythm table.
--abstract-limit   the author's abstract word limit; it replaces the upper end of
             the abstract word range.
--check      exit 1 when the proposed band differs from the current one.
"""

from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import sys
from types import ModuleType

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = pathlib.PurePosixPath("shared/scripts/style_fingerprint.py")
STYLE = pathlib.PurePosixPath("shared/styles/team-house-style.md")
ZH = pathlib.PurePosixPath("shared/languages/zh.md")
CARD = pathlib.PurePosixPath("shared/styles/house-style-card.md")

SECTIONS = ("abstract", "intro", "related", "model", "method", "exp", "concl")
SECTION_LABELS = {
    "abstract": "Abstract",
    "intro": "Introduction",
    "related": "Related Work",
    "model": "System Model and Problem Formulation",
    "method": "Proposed algorithm",
    "exp": "Experimental studies",
    "concl": "Conclusion",
}
NUMBER_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def load_fingerprint(root: pathlib.Path) -> ModuleType:
    path = root / SCRIPT
    spec = importlib.util.spec_from_file_location("style_fingerprint_calibration", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def collect(paths: list[pathlib.Path]) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in {".md", ".tex"}))
        elif path.is_file():
            found.append(path)
        else:
            raise FileNotFoundError(path)
    return found


def measure(module: ModuleType, path: pathlib.Path) -> dict:
    result = module.fingerprint(path, "en")
    if "body" not in result:
        raise ValueError(f"{path}: no classifiable body text")
    body = result["body"]
    row = {
        "name": path.stem,
        "mean": round(body["mean"], 1),
        "median": float(round(body["median"])),
        "p90": float(round(body["p90"])),
        "share_long": round(body["share_long"], 2),
        "share_short": round(body["share_short"], 2),
        "sections": {k: round(result[k]["mean"], 1) for k in SECTIONS if k in result},
    }
    for key, prefix in (("abstract", "abstract"), ("concl", "conclusion")):
        if key in result:
            row[f"{prefix}_words"] = result[key]["words"]
            row[f"{prefix}_sentences"] = result[key]["sentences"]
    return row


def span(values: list[float]) -> tuple[float, float]:
    return (min(values), max(values))


def propose(references: list[dict], approved: list[dict], abstract_limit: int | None) -> dict:
    if len(references) < 2:
        raise ValueError("at least two reference papers are required")
    band: dict = {"body": {}, "section_mean": {}}
    for key in ("mean", "median", "p90", "share_long", "share_short"):
        band["body"][key] = span([r[key] for r in references + approved])
    for section in SECTIONS:
        pool = references + approved
        values = [r["sections"][section] for r in pool if section in r["sections"]]
        if len(values) >= 2:
            band["section_mean"][section] = span(values)
    for prefix in ("abstract", "conclusion"):
        for unit in ("words", "sentences"):
            key = f"{prefix}_{unit}"
            values = [r[key] for r in references + approved if key in r]
            if len(values) < 2:
                raise ValueError(f"fewer than two documents report {key}")
            low, high = min(values), max(values)
            if key == "abstract_words" and abstract_limit:
                high = abstract_limit
            band[key] = (int(low), int(high))
    return band


def current_band(module: ModuleType) -> dict:
    keys = ("body", "section_mean", "abstract_words", "abstract_sentences", "conclusion_words", "conclusion_sentences")
    return {key: module.TEAM_BAND[key] for key in keys}


def differences(old: dict, new: dict) -> list[str]:
    out: list[str] = []
    for key in new:
        if isinstance(new[key], dict):
            for sub, value in new[key].items():
                before = old.get(key, {}).get(sub)
                if before is None or tuple(map(float, before)) != tuple(map(float, value)):
                    out.append(f"{key}.{sub}: {before} -> {value}")
        elif tuple(map(float, old.get(key, (0, 0)))) != tuple(map(float, new[key])):
            out.append(f"{key}: {old.get(key)} -> {new[key]}")
    return out


# --------------------------------------------------------------------------- rendering


def _num(value: float, digits: int) -> str:
    return f"{value:.{digits}f}"


def render_band(band: dict) -> str:
    b = band["body"]
    lines = ["TEAM_BAND = {", '    "body": {']
    lines.append(f'        "mean": ({_num(b["mean"][0], 1)}, {_num(b["mean"][1], 1)}),')
    lines.append(f'        "median": ({_num(b["median"][0], 1)}, {_num(b["median"][1], 1)}),')
    lines.append(f'        "p90": ({_num(b["p90"][0], 1)}, {_num(b["p90"][1], 1)}),')
    lines.append(f'        "share_long": ({_num(b["share_long"][0], 2)}, {_num(b["share_long"][1], 2)}),')
    lines.append(f'        "share_short": ({_num(b["share_short"][0], 2)}, {_num(b["share_short"][1], 2)}),')
    lines.append("    },")
    lines.append('    "section_mean": {')
    for section in SECTIONS:
        if section in band["section_mean"]:
            low, high = band["section_mean"][section]
            lines.append(f'        "{section}": ({_num(low, 1)}, {_num(high, 1)}),')
    lines.append("    },")
    for key in ("abstract_words", "abstract_sentences", "conclusion_words", "conclusion_sentences"):
        lines.append(f'    "{key}": ({band[key][0]}, {band[key][1]}),')
    lines.append("}")
    return "\n".join(lines)


def _pct(value: float) -> str:
    return f"{round(value * 100)}%"


def render_rhythm(band: dict, references: list[dict], baseline: dict | None, approved: list[dict],
                  section_tolerance: float = 3.0) -> str:
    b = band["body"]
    count = NUMBER_WORDS.get(len(references), str(len(references)))
    header = f"| Body measure | Band | Reference papers ({count}) |"
    rule = "|---|---|---|"
    if approved:
        header += " Supervisor-approved draft |"
        rule += "---|"
    if baseline:
        header += " Supervisor-approved baseline draft |"
        rule += "---|"

    def values(key: str, fmt) -> str:
        return ", ".join(fmt(v) for v in sorted(r[key] for r in references))

    rows = [
        ("Mean sentence length (words)", f"{_num(b['mean'][0], 1)}–{_num(b['mean'][1], 1)}", values("mean", lambda v: _num(v, 1)), "mean", lambda v: _num(v, 1)),
        ("Median", f"{b['median'][0]:.0f}–{b['median'][1]:.0f}", values("median", lambda v: f"{v:.0f}"), "median", lambda v: f"{v:.0f}"),
        ("90th percentile", f"{b['p90'][0]:.0f}–{b['p90'][1]:.0f}", values("p90", lambda v: f"{v:.0f}"), "p90", lambda v: f"{v:.0f}"),
        ("Share of sentences over 35 words", f"{_pct(b['share_long'][0])}–{_pct(b['share_long'][1])}", values("share_long", _pct), "share_long", _pct),
        ("Share of sentences under 12 words", f"{_pct(b['share_short'][0])}–{_pct(b['share_short'][1])}", values("share_short", _pct), "share_short", _pct),
    ]
    lines = [header, rule]
    for label, band_text, ref_text, key, fmt in rows:
        line = f"| {label} | {band_text} | {ref_text} |"
        if approved:
            line += " " + ", ".join(fmt(doc[key]) for doc in approved) + " |"
        if baseline:
            line += f" {fmt(baseline[key])} |"
        lines.append(line)
    section_header = "| Section | Mean sentence length band |" + (" Supervisor-approved draft |" if approved else "")
    lines += ["", section_header, "|---|---|" + ("---|" if approved else "")]
    for section in SECTIONS:
        if section in band["section_mean"]:
            low, high = band["section_mean"][section]
            line = f"| {SECTION_LABELS[section]} | {_num(low, 1)}–{_num(high, 1)} |"
            if approved:
                values = [_num(doc["sections"][section], 1) for doc in approved if section in doc["sections"]]
                line += f" {', '.join(values) or '-'} |"
            lines.append(line)
    lines.append("")
    if approved:
        lines.append(
            "Every band spans the reference papers and the supervisor-approved draft. "
            f"Section means within {section_tolerance:g} words of the band count as inside."
        )
    else:
        lines.append(f"Section means within {section_tolerance:g} words of the band count as inside.")
    return "\n".join(lines)


def render_card(band: dict) -> str:
    b = band["body"]
    sections = ", ".join(
        f"{SECTION_LABELS[s]} {_num(low, 1)}–{_num(high, 1)}" for s, (low, high) in
        ((s, band["section_mean"][s]) for s in SECTIONS if s in band["section_mean"])
    )
    return "\n".join([
        f"- Body: mean sentence length {_num(b['mean'][0], 1)}–{_num(b['mean'][1], 1)} words, median "
        f"{b['median'][0]:.0f}–{b['median'][1]:.0f}, 90th percentile {b['p90'][0]:.0f}–{b['p90'][1]:.0f}, "
        f"{_pct(b['share_long'][0])}–{_pct(b['share_long'][1])} of sentences over 35 words, "
        f"{_pct(b['share_short'][0])}–{_pct(b['share_short'][1])} under 12 words.",
        f"- Section means (indicative): {sections} words.",
        f"- Abstract {band['abstract_words'][0]}–{band['abstract_words'][1]} words in "
        f"{band['abstract_sentences'][0]}–{band['abstract_sentences'][1]} sentences; Conclusion "
        f"{band['conclusion_words'][0]}–{band['conclusion_words'][1]} words in "
        f"{band['conclusion_sentences'][0]}–{band['conclusion_sentences'][1]} sentences.",
    ])


def render_zh(module: ModuleType, band: dict) -> str:
    convert = lambda pair: (round(pair[0] * module.ZH_RATIO[0]), round(pair[1] * module.ZH_RATIO[1]))  # noqa: E731
    long_threshold = round(35 * module.ZH_THRESHOLD_RATIO)
    short_threshold = round(12 * module.ZH_THRESHOLD_RATIO)
    b = band["body"]
    lines = ["| Body measure | Weak-prior band |", "|---|---|"]
    for label, key in (("Mean sentence length (ideographs)", "mean"), ("Median", "median"), ("90th percentile", "p90")):
        low, high = convert(b[key])
        lines.append(f"| {label} | {low}–{high} |")
    lines.append(f"| Share of sentences over {long_threshold} ideographs | {_pct(b['share_long'][0])}–{_pct(b['share_long'][1])} |")
    lines.append(f"| Share of sentences under {short_threshold} ideographs | {_pct(b['share_short'][0])}–{_pct(b['share_short'][1])} |")
    lines += ["", "| Section | Mean sentence length band (ideographs) |", "|---|---|"]
    for section in SECTIONS:
        if section in band["section_mean"]:
            low, high = convert(band["section_mean"][section])
            lines.append(f"| {SECTION_LABELS[section]} | {low}–{high} |")
    abstract = convert(band["abstract_words"])
    conclusion = convert(band["conclusion_words"])
    lines += [
        "",
        f"The abstract converts to {abstract[0]}–{abstract[1]} ideographs and the Conclusion to "
        f"{conclusion[0]}–{conclusion[1]} ideographs. A venue's own limit overrides both.",
    ]
    return "\n".join(lines)


def replace_block(text: str, name: str, content: str, comment: str) -> str:
    if comment == "md":
        begin, end = f"<!-- calibrate:begin {name} -->", f"<!-- calibrate:end {name} -->"
    else:
        begin, end = f"# calibrate:begin {name}", f"# calibrate:end {name}"
    pattern = re.compile(re.escape(begin) + r"\n.*?\n" + re.escape(end), flags=re.S)
    if not pattern.search(text):
        raise ValueError(f"generated block {name!r} not found")
    return pattern.sub(lambda _: f"{begin}\n{content}\n{end}", text, count=1)


def replace_in_section(text: str, heading: str, old: str, new: str) -> tuple[str, bool]:
    start = text.find(heading)
    if start < 0 or old == new:
        return text, old == new
    following = re.search(r"\n## \d+\.", text[start + len(heading):])
    end = start + len(heading) + following.start() if following else len(text)
    section = text[start:end]
    if old not in section:
        return text, False
    return text[:start] + section.replace(old, new, 1) + text[end:], True


def write(root: pathlib.Path, module: ModuleType, old: dict, band: dict, references: list[dict],
          baseline: dict | None, approved: list[dict]) -> list[str]:
    notes: list[str] = []
    script = root / SCRIPT
    script.write_bytes(replace_block(script.read_text(encoding="utf-8"), "band", render_band(band), "py").encode("utf-8"))

    style = root / STYLE
    text = replace_block(style.read_text(encoding="utf-8"), "rhythm", render_rhythm(band, references, baseline, approved,
                                                                 module.LANGUAGES["en"]["tolerance"]["section"]), "md")
    for heading, prefix in (("## 10. Title, abstract, and index terms", "abstract"), ("## 12. Conclusion", "conclusion")):
        for unit in ("words", "sentences"):
            key = f"{prefix}_{unit}"
            before = f"{old[key][0]}–{old[key][1]} {unit}"
            after = f"{band[key][0]}–{band[key][1]} {unit}"
            text, done = replace_in_section(text, heading, before, after)
            if not done:
                notes.append(f"house style {heading}: '{before}' not found; set '{after}' by hand")
    style.write_bytes(text.encode("utf-8"))

    card = root / CARD
    card.write_bytes(replace_block(card.read_text(encoding="utf-8"), "card", render_card(band), "md").encode("utf-8"))

    zh = root / ZH
    zh.write_bytes(replace_block(zh.read_text(encoding="utf-8"), "zh-rhythm", render_zh(module, band), "md").encode("utf-8"))
    notes.append("review the reference-paper values quoted in house-style Sections 10, 12, and 13, and the corpus list in Section 15")
    notes.append("run python scripts/sync_shared.py, then the validator and the unit tests")
    return notes


VALIDATION_KEYS = ("mean", "median", "p90", "share_long", "share_short")


def validate(module: ModuleType, band: dict, groups: list[tuple[str, list[dict]]]) -> list[dict]:
    """Compare validation papers with a band, using the fingerprint script's tolerances."""
    tolerance = module.LANGUAGES["en"]["tolerance"]
    results = []
    for label, rows in groups:
        for row in rows:
            outside = []
            for key in VALIDATION_KEYS:
                low, high = band["body"][key]
                if module._status(row[key], low, high, tolerance[key]) not in {"in", "near"}:
                    outside.append(f"body {key} {row[key]}")
            for section, value in row["sections"].items():
                if section in band["section_mean"]:
                    low, high = band["section_mean"][section]
                    if module._status(value, low, high, tolerance["section"]) not in {"in", "near"}:
                        outside.append(f"{section} {value}")
            results.append({"group": label, "name": row["name"], "mean": row["mean"], "outside": outside})
    return results


def render_validation(groups: list[tuple[str, list[dict]]], results: list[dict]) -> str:
    total = sum(len(rows) for _, rows in groups)
    parts = ", ".join(f"{len(rows)} {label}" for label, rows in groups)
    means = [row["mean"] for _, rows in groups for row in rows]
    lines = [
        f"Validation. The band was checked against {total} further published papers that were not used to set it: {parts}. "
        f"Their body mean sentence lengths run from {min(means):.1f} to {max(means):.1f} words.",
        "",
        "| Group | Papers | Body mean (min–max) | Body mean inside the band or its tolerance | Any section mean outside |",
        "|---|---|---|---|---|",
    ]
    for label, rows in groups:
        mine = [r for r in results if r["group"] == label]
        inside = sum(1 for r in mine if not any(o.startswith("body mean") for o in r["outside"]))
        any_section = sum(1 for r in mine if any(not o.startswith("body") for o in r["outside"]))
        values = [r["mean"] for r in mine]
        lines.append(f"| {label} | {len(mine)} | {min(values):.1f}–{max(values):.1f} | {inside} of {len(mine)} | {any_section} of {len(mine)} |")
    return "\n".join(lines)


def parse_groups(items: list[str]) -> list[tuple[str, list[pathlib.Path]]]:
    groups = []
    for item in items:
        label, separator, path = item.partition("=")
        if not separator or not label.strip() or not path.strip():
            raise ValueError(f"--validate expects LABEL=PATH, got {item!r}")
        groups.append((label.strip(), collect([pathlib.Path(path.strip())])))
    return groups


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--references", nargs="+", type=pathlib.Path, required=True)
    parser.add_argument(
        "--validate",
        nargs="*",
        default=[],
        metavar="LABEL=PATH",
        help="validation papers that do not set the band; with --write, the summary is written to the house style",
    )
    parser.add_argument("--approved", nargs="*", type=pathlib.Path, default=[])
    parser.add_argument("--baseline", type=pathlib.Path)
    parser.add_argument("--abstract-limit", type=int)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    module = load_fingerprint(root)
    references = [measure(module, p) for p in collect(args.references)]
    approved = [measure(module, p) for p in collect(args.approved)]
    baseline = measure(module, args.baseline) if args.baseline else None
    band = propose(references, approved, args.abstract_limit)
    old = current_band(module)

    out = sys.stdout.write
    out("document | mean | median | p90 | long | short | " + " | ".join(SECTIONS) + "\n")
    for row in references + approved + ([baseline] if baseline else []):
        sections = " | ".join(_num(row["sections"][k], 1) if k in row["sections"] else "-" for k in SECTIONS)
        out(f"{row['name'][:40]} | {row['mean']} | {row['median']:.0f} | {row['p90']:.0f} | "
            f"{_pct(row['share_long'])} | {_pct(row['share_short'])} | {sections}\n")
    changes = differences(old, band)
    out("\nProposed band differs from the current one:\n" if changes else "\nProposed band equals the current one.\n")
    for change in changes:
        out(f"  {change}\n")
    groups = [(label, [measure(module, p) for p in paths]) for label, paths in parse_groups(args.validate)]
    results = validate(module, band, groups) if groups else []
    if results:
        out("\nValidation against the proposed band:\n")
        for result in results:
            status = "inside" if not result["outside"] else "outside: " + ", ".join(result["outside"])
            out(f"  [{result['group']}] {result['name'][:50]}: mean {result['mean']} {status}\n")
    if args.check:
        return 1 if changes else 0
    if args.write:
        for note in write(root, module, old, band, references, baseline, approved):
            out(f"note: {note}\n")
        if groups:
            style = root / STYLE
            text = replace_block(style.read_text(encoding="utf-8"), "validation", render_validation(groups, results), "md")
            style.write_bytes(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

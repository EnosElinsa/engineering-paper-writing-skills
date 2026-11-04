#!/usr/bin/env python3
"""Measure the prose fingerprint of a manuscript and compare it with the team house-style band.

Usage:
    python style_fingerprint.py DRAFT.tex
    python style_fingerprint.py DRAFT.md --section exp
    python style_fingerprint.py DRAFT.tex --citations
    python style_fingerprint.py DRAFT.tex --json
    python style_fingerprint.py --diff OLD.tex NEW.tex [--show 10]

Inputs: LaTeX (.tex), Markdown converted from a PDF (.md, one paragraph per line,
`#` headings), or plain text (.txt, blank-line paragraphs).

Counting rule (protocols S and R of the reader and terminology contract):
- displayed equations, figures, tables, algorithms, captions, and headings are excluded;
- citations are removed; cross-references count as one word;
- inline math is excluded from word counts and counts as one word in sentence lengths;
- a paragraph is a prose block of at least 20 words;
- sentences split at final punctuation before a capital letter, protecting
  et al., Fig., Eq., e.g., i.e., and similar abbreviations.

The script reports measurements and flags. It does not judge whether a sentence is
correct; read every flagged sentence before changing it. Standard library only.
"""

from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import statistics
import sys
from collections import Counter

MATH = "MATHTOKEN"

SECTION_PATTERNS = (
    ("abstract", r"\babstract\b"),
    ("intro", r"introduction"),
    ("related", r"related work|literature review"),
    ("model", r"system model|problem formulation|system overview"),
    ("method", r"proposed\b.*\b(algorithm|method|framework|approach)|algorithm design|\bframework\b|solution approach"),
    ("exp", r"experiment|numerical results|simulation|performance evaluation|evaluation"),
    ("future", r"future"),
    ("concl", r"conclusion"),
)

SECTION_ORDER = ("abstract", "intro", "related", "model", "method", "exp", "future", "concl", "body")

# Team house-style band (see references/styles/team-house-style.md, section "Sentence rhythm").
TEAM_BAND = {
    "body": {
        "mean": (21.4, 23.8),
        "median": (20.0, 22.0),
        "p90": (32.0, 37.0),
        "share_over_35": (0.07, 0.13),
        "share_under_12": (0.09, 0.14),
    },
    "section_mean": {
        "abstract": (24.5, 30.5),
        "intro": (19.8, 23.6),
        "related": (21.3, 26.3),
        "model": (20.8, 23.2),
        "method": (19.7, 25.5),
        "exp": (22.1, 24.5),
        "concl": (24.2, 28.0),
    },
    "abstract_words": (210, 250),
    "abstract_sentences": (7, 10),
    "conclusion_words": (165, 280),
    "conclusion_sentences": (6, 10),
    "initial_per_100": {
        "Since": (0.0, 1.0),
        "Hence": (0.0, 0.0),
        "Accordingly": (0.0, 1.0),
        "However": (1.0, 2.6),
    },
}

TOLERANCE = {"mean": 1.0, "median": 1.0, "p90": 2.0, "share_over_35": 0.02, "share_under_12": 0.02}

FURNITURE = re.compile(
    r"IEEE TRANSACTIONS|Authorized licensed use|Digital Object Identifier|Manuscript received|"
    r"This work was supported|\u00a9|Personal use is permitted|Recommended for acceptance|"
    r"Color versions of one or more|Corresponding author",
    re.I,
)

PROTECT = ("et al.", "Figs.", "Fig.", "Eqs.", "Eq.", "e.g.", "i.e.", "vs.", "Sec.", "Secs.", "No.", "Ref.", "Refs.", "resp.", "cf.")

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

INITIAL_CONNECTIVES = (
    "As a result", "On the other hand", "On one hand", "In this section", "In this study", "In this paper",
    "In addition", "In particular", "In contrast", "For example", "For instance", "To this end",
    "As shown", "As illustrated", "However", "Therefore", "Thus", "Hence", "Consequently", "Moreover",
    "Furthermore", "Additionally", "Besides", "Meanwhile", "Specifically", "Notably", "Accordingly",
    "Nevertheless", "Nonetheless", "Similarly", "Finally", "First", "Second", "Third", "Then", "Since",
    "To address", "To solve", "To evaluate", "To validate", "To investigate", "To ensure", "Based on",
)

INLINE = {
    "thereby or participle tail": r",\s+(thereby|making|leading|resulting|enabling|allowing|yielding|ensuring|causing|showing|indicating|providing|increasing|reducing|limiting|accommodating)\b",
    "due to": r"\bdue to\b",
    ", which": r",\s*which\b",
    ", where": r",\s*where\b",
    "while/whereas": r"\b(while|whereas)\b",
    "respectively": r"\brespectively\b",
    "the proposed": r"\bthe proposed\b",
    "this study/paper": r"\bthis (study|paper|work|article)\b",
    "promotional modifier": r"\b(significant|significantly|superior|superiority|critical|fundamental|fundamentally|crucial|essential|promising|comprehensive|comprehensively|remarkable|remarkably|novel)\b|state-of-the-art",
}

BANNED = {
    "because": r"\bbecause\b",
    "so (conjunction)": r",\s*so\b|\bso that\b|\bso as to\b",
    ", but": r",\s*but\b",
    "semicolon": r";",
    "Hence": r"(?:^|[.!?]\s+)Hence\b",
    "e.g. in prose": r"\be\.g\.",
    "we/our outside future work": r"\b[Ww]e\b(?!\s+will)|\b[Oo]ur\b",
}

STOP = set(
    "the a an of to in and or for on with by is are be was were this that these those as at from it its "
    "which where while than then into over under each all both not no also can may their".split()
)


# --------------------------------------------------------------------------- parsing


def classify(title: str) -> str | None:
    lowered = title.lower()
    for key, pattern in SECTION_PATTERNS:
        if re.search(pattern, lowered):
            return key
    return None


def _strip_command(text: str, command: str, keep: bool, replacement: str = "") -> str:
    """Remove \\command[opt]{arg} brace-aware, keeping the argument when keep is true.

    When keep is false, the command is replaced by `replacement`, in which `{arg}`
    stands for the argument text.
    """
    pattern = re.compile(r"\\" + command + r"\*?\s*(\[[^\]]*\])?\s*\{")
    out: list[str] = []
    index = 0
    while True:
        match = pattern.search(text, index)
        if not match:
            out.append(text[index:])
            return "".join(out)
        out.append(text[index:match.start()])
        position = match.end()
        depth = 1
        while position < len(text) and depth:
            if text[position] == "{":
                depth += 1
            elif text[position] == "}":
                depth -= 1
            position += 1
        argument = text[match.end():position - 1]
        out.append(argument if keep else replacement.replace("{arg}", argument))
        index = position


ENVIRONMENTS = (
    r"equation|align|alignat|eqnarray|gather|multline|flalign|figure|table|algorithm|algorithmic|"
    r"tabular|tabularx|IEEEkeywords|subequations|array|cases|tikzpicture|minipage|lstlisting|verbatim"
)


def _remove_environments(text: str) -> str:
    for _ in range(3):
        text = re.sub(r"\\begin\{(" + ENVIRONMENTS + r")\*?\}.*?\\end\{\1\*?\}", " ", text, flags=re.S)
    return text


def clean_tex(paragraph: str) -> str:
    text = paragraph
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\\IEEEPARstart\{([^}]*)\}\{([^}]*)\}", r"\1\2", text)
    for command in ("cite", "citep", "citet", "citealp", "label", "vspace", "hspace", "footnote"):
        text = _strip_command(text, command, keep=False)
    text = re.sub(r"\\(eqref|ref|autoref|cref|Cref|pageref)\{[^}]*\}", "1", text)
    text = re.sub(r"(?<!\\)\$[^$]*\$", f" {MATH} ", text)
    text = re.sub(r"\\\(.*?\\\)", f" {MATH} ", text, flags=re.S)
    text = re.sub(r"\\(textcolor|color)\{[^}]*\}", "", text)
    text = text.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", text)
    text = text.replace("~", " ").replace("{", "").replace("}", "")
    text = text.replace("``", '"').replace("''", '"').replace("--", "-")
    return re.sub(r"\s+", " ", text).strip()


def _tex_paragraphs(block: str) -> list[str]:
    for command in ("subsubsection", "subsection", "paragraph"):
        block = _strip_command(block, command, keep=False, replacement="\n\n")
    block = re.sub(r"\\item\b", "\n\n", block)
    return [part.strip() for part in re.split(r"\n\s*\n", block) if part.strip()]


def parse_tex(text: str) -> dict[str, list[str]]:
    text = re.sub(r"(?<!\\)%.*", "", text)
    sections: dict[str, list[str]] = {}
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, flags=re.S)
    if match:
        sections["abstract"] = _tex_paragraphs(_remove_environments(match.group(1)))
        text = text.replace(match.group(0), " ")
    match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, flags=re.S)
    body = match.group(1) if match else text
    body = re.split(r"\\bibliography\{|\\begin\{thebibliography\}|\\appendices\b|\\appendix\b|\\begin\{IEEEbiography", body)[0]
    body = _remove_environments(body)
    body = _strip_command(body, "section", keep=False, replacement="\n@@SECTION@@{arg}@@END@@\n")
    current: str | None = None
    for part in re.split(r"(@@SECTION@@.*?@@END@@)", body, flags=re.S):
        heading = re.match(r"@@SECTION@@(.*?)@@END@@", part, flags=re.S)
        if heading:
            current = classify(clean_tex(heading.group(1))) or "other"
            continue
        if current is None:
            continue
        sections.setdefault(current, []).extend(_tex_paragraphs(part))
    if len(sections) <= 1 and not any(key != "abstract" for key in sections):
        sections.setdefault("body", []).extend(_tex_paragraphs(body))
    return sections


def parse_md(text: str) -> dict[str, list[str]]:
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"<table.*?</table>", " ", text, flags=re.S | re.I)
    sections: dict[str, list[str]] = {}
    top: str | None = None
    current: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^Abstract\s*[\u2014\-:.]", line):
            sections.setdefault("abstract", []).append(re.sub(r"^Abstract\s*[\u2014\-:.]\s*", "", line))
            continue
        if line.startswith("Index Terms"):
            continue
        heading = re.match(r"^#+\s*(.*)$", line)
        if heading:
            title = heading.group(1).strip()
            if re.search(r"references|bibliography|acknowledg", title, re.I):
                top = current = None
            elif re.match(r"^[A-H]\.\s", title):
                current = top
            elif re.match(r"^[IVX]+\.\s", title) or classify(title):
                top = classify(title) or "other"
                current = top
            continue
        if current is None:
            continue
        if line.startswith(("!", "|", "<")) or FURNITURE.search(line):
            continue
        if re.match(r"^(Fig\.|TABLE|Table|Algorithm)\s*[0-9IVX]+", line) and len(line) < 400:
            continue
        sections.setdefault(current, []).append(line)
    if not sections:
        sections["body"] = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return sections


def clean_md(paragraph: str) -> str:
    text = re.sub(r"\$[^$]*\$", f" {MATH} ", paragraph)
    text = re.sub(r"\[\s*\d+(\s*[,\u2013\-]\s*\d+)*\s*\]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def load(path: pathlib.Path) -> tuple[dict[str, list[str]], bool]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    suffix = path.suffix.lower()
    if suffix == ".tex":
        return parse_tex(text), True
    if suffix in {".md", ".markdown"}:
        return parse_md(text), False
    return {"body": [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]}, False


# --------------------------------------------------------------------------- metrics


def split_sentences(paragraph: str) -> list[str]:
    protected = paragraph
    for index, token in enumerate(PROTECT):
        protected = protected.replace(token, token.replace(".", f"<D{index}>"))
    protected = re.sub(r"\b([A-Z])\.(?=\s[A-Z])", r"\1<INI>", protected)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"\u201c])", protected)
    sentences = []
    for part in parts:
        for index, token in enumerate(PROTECT):
            part = part.replace(f"<D{index}>", ".")
        part = part.replace("<INI>", ".").strip()
        if part:
            sentences.append(part)
    return sentences


def words(text: str) -> list[str]:
    return [token for token in WORD.findall(text) if token != MATH]


def sentence_length(sentence: str) -> int:
    return len(WORD.findall(sentence))


def prose_paragraphs(paragraphs: list[str], tex: bool) -> list[str]:
    cleaned = [clean_tex(p) if tex else clean_md(p) for p in paragraphs]
    return [p for p in cleaned if len(words(p)) >= 20 or re.match(r"^[\u2022\-*]\s", p)]


def percentile(values: list[int], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return float(ordered[int(fraction * (len(ordered) - 1))])


def measure(paragraphs: list[str]) -> dict:
    # Fragments under four words are run-in labels ("Step 1.", "Case 2."), not sentences.
    sentences_by_paragraph = [
        [s for s in split_sentences(p) if sentence_length(s) >= 4] for p in paragraphs
    ]
    sentences = [s for group in sentences_by_paragraph for s in group]
    lengths = [sentence_length(s) for s in sentences]
    word_count = sum(len(words(p)) for p in paragraphs)
    initial = Counter()
    for sentence in sentences:
        stripped = sentence.lstrip("\u2022-* ").strip()
        for connective in INITIAL_CONNECTIVES:
            if re.match(re.escape(connective) + r"\b", stripped):
                initial[connective] += 1
                break
    inline = {name: sum(len(re.findall(pattern, p, flags=re.I)) for p in paragraphs) for name, pattern in INLINE.items()}
    banned: dict[str, list[str]] = {}
    for name, pattern in BANNED.items():
        flags = 0 if name in {"Hence", "we/our outside future work"} else re.I
        hits = [s for s in sentences if re.search(pattern, s, flags=flags)]
        if hits:
            banned[name] = hits
    short_runs = []
    for group in sentences_by_paragraph:
        run: list[str] = []
        for sentence in group + [""]:
            if sentence and sentence_length(sentence) < 12:
                run.append(sentence)
                continue
            if len(run) >= 3:
                short_runs.append(run)
            run = []
    count = len(sentences)
    return {
        "paragraphs": len(paragraphs),
        "words": word_count,
        "sentences": count,
        "mean": statistics.mean(lengths) if lengths else 0.0,
        "median": float(statistics.median(lengths)) if lengths else 0.0,
        "p90": percentile(lengths, 0.9),
        "share_over_35": sum(1 for x in lengths if x > 35) / count if count else 0.0,
        "share_under_12": sum(1 for x in lengths if x < 12) / count if count else 0.0,
        "initial_per_100": {k: 100.0 * v / count for k, v in initial.items()} if count else {},
        "initial_counts": dict(initial),
        "inline_per_1000": {k: 1000.0 * v / word_count for k, v in inline.items()} if word_count else {},
        "banned": banned,
        "short_runs": short_runs,
    }


def fingerprint(path: pathlib.Path) -> dict[str, dict]:
    sections, tex = load(path)
    result: dict[str, dict] = {}
    classified: list[str] = []
    unclassified: list[str] = []
    for key, paragraphs in sections.items():
        prose = prose_paragraphs(paragraphs, tex)
        if key == "abstract":
            prose = [clean_tex(p) if tex else clean_md(p) for p in paragraphs]
            prose = [p for p in prose if words(p)]
        if not prose:
            continue
        result[key] = measure(prose)
        if key in {"other", "body"}:
            unclassified.extend(prose)
        elif key != "abstract":
            classified.extend(prose)
    # Sections whose headings match no known role (appendix-like material) join the
    # body only when no section could be classified.
    body = classified or unclassified
    if body:
        result["body"] = measure(body)
    return result


def _status(value: float, low: float, high: float, tolerance: float) -> str:
    if low <= value <= high:
        return "in"
    if low - tolerance <= value <= high + tolerance:
        return "near"
    return "low" if value < low else "high"


def band_flags(result: dict[str, dict]) -> list[str]:
    flags: list[str] = []
    body = result.get("body")
    if body:
        for name, (low, high) in TEAM_BAND["body"].items():
            state = _status(body[name], low, high, TOLERANCE[name])
            if state not in {"in", "near"}:
                flags.append(f"body {name} = {body[name]:.2f} is {state} (band {low}-{high})")
        for connective, (low, high) in TEAM_BAND["initial_per_100"].items():
            value = body["initial_per_100"].get(connective, 0.0)
            if value > high + 0.25:
                flags.append(f"sentence-initial {connective} = {value:.1f} per 100 sentences (band {low}-{high})")
            if connective == "However" and body["sentences"] >= 100 and value < low - 0.5:
                flags.append(f"sentence-initial However = {value:.1f} per 100 sentences (band {low}-{high})")
    for section, (low, high) in TEAM_BAND["section_mean"].items():
        measured = result.get(section)
        if measured and measured["sentences"] >= 5:
            state = _status(measured["mean"], low, high, 1.0)
            if state not in {"in", "near"}:
                flags.append(f"{section} mean sentence length = {measured['mean']:.1f} is {state} (band {low}-{high})")
    for section, words_key, sentences_key in (
        ("abstract", "abstract_words", "abstract_sentences"),
        ("concl", "conclusion_words", "conclusion_sentences"),
    ):
        measured = result.get(section)
        if not measured:
            continue
        low, high = TEAM_BAND[words_key]
        if not low <= measured["words"] <= high:
            flags.append(f"{section} has {measured['words']} words (band {low}-{high})")
        low, high = TEAM_BAND[sentences_key]
        if not low <= measured["sentences"] <= high:
            flags.append(f"{section} has {measured['sentences']} sentences (band {low}-{high})")
    for section, measured in result.items():
        if section == "body":
            continue
        for name, hits in measured["banned"].items():
            flags.append(f"{section}: {len(hits)} sentence(s) with {name}")
        if measured["short_runs"]:
            flags.append(f"{section}: {len(measured['short_runs'])} run(s) of three or more sentences under 12 words")
    return flags


# --------------------------------------------------------------------------- citations


def citation_reuse(path: pathlib.Path) -> dict[str, dict[str, int]]:
    sections, tex = load(path)
    reuse: dict[str, dict[str, int]] = {}
    for key, paragraphs in sections.items():
        counts: Counter[str] = Counter()
        for paragraph in paragraphs:
            if tex:
                for group in re.findall(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])?\{([^}]*)\}", paragraph):
                    counts.update(item.strip() for item in group.split(",") if item.strip())
            else:
                for group in re.findall(r"\[(\s*\d+(?:\s*[,\u2013\-]\s*\d+)*\s*)\]", paragraph):
                    for item in re.split(r"\s*,\s*", group.strip()):
                        bounds = re.split(r"\s*[\u2013\-]\s*", item)
                        if len(bounds) == 2 and all(b.isdigit() for b in bounds):
                            counts.update(str(n) for n in range(int(bounds[0]), int(bounds[1]) + 1))
                        elif item.isdigit():
                            counts[item] += 1
        repeated = {k: v for k, v in counts.items() if v > 1}
        if repeated:
            reuse[key] = dict(sorted(repeated.items(), key=lambda kv: (-kv[1], kv[0])))
    return reuse


# --------------------------------------------------------------------------- diff


def sentence_list(path: pathlib.Path) -> list[str]:
    sections, tex = load(path)
    out: list[str] = []
    for key in sections:
        for paragraph in sections[key]:
            cleaned = clean_tex(paragraph) if tex else clean_md(paragraph)
            out.extend(s for s in split_sentences(cleaned) if len(words(s)) >= 4)
    return out


def diff_report(old_path: pathlib.Path, new_path: pathlib.Path) -> dict:
    old, new = sentence_list(old_path), sentence_list(new_path)
    matcher = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    kinds: Counter[str] = Counter()
    hunks = []
    old_changed: list[str] = []
    new_changed: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        before, after = old[i1:i2], new[j1:j2]
        if tag == "replace":
            kind = "merge" if len(after) < len(before) else "split" if len(after) > len(before) else "rewrite"
        else:
            kind = tag
        kinds[kind] += 1
        old_changed.extend(before)
        new_changed.extend(after)
        hunks.append({"kind": kind, "old": before, "new": after})

    def feature_counts(sentences: list[str]) -> dict[str, int]:
        text = " ".join(sentences)
        counts = {name: len(re.findall(pattern, text, flags=re.I)) for name, pattern in INLINE.items()}
        counts.update({f"banned: {name}": len(re.findall(pattern, text)) for name, pattern in BANNED.items()})
        return counts

    deleted = Counter(w.lower() for s in old_changed for w in words(s)) - Counter(w.lower() for s in new_changed for w in words(s))
    inserted = Counter(w.lower() for s in new_changed for w in words(s)) - Counter(w.lower() for s in old_changed for w in words(s))
    lengths_old = [sentence_length(s) for s in old_changed]
    lengths_new = [sentence_length(s) for s in new_changed]
    return {
        "kinds": dict(kinds),
        "old_sentences": len(old),
        "new_sentences": len(new),
        "changed_old": len(old_changed),
        "changed_new": len(new_changed),
        "changed_mean_old": statistics.mean(lengths_old) if lengths_old else 0.0,
        "changed_mean_new": statistics.mean(lengths_new) if lengths_new else 0.0,
        "features_old": feature_counts(old_changed),
        "features_new": feature_counts(new_changed),
        "deleted_words": [w for w, _ in deleted.most_common(80) if w not in STOP][:30],
        "inserted_words": [w for w, _ in inserted.most_common(80) if w not in STOP][:30],
        "hunks": hunks,
    }


# --------------------------------------------------------------------------- output


def _print_fingerprint(path: pathlib.Path, result: dict[str, dict], only: str | None) -> None:
    write = sys.stdout.write
    write(f"Style fingerprint: {path.name}\n\n")
    write("section    paras  words  sents  mean  median  p90  >35w   <12w\n")
    for key in SECTION_ORDER + tuple(k for k in result if k not in SECTION_ORDER):
        if key not in result or (only and key != only):
            continue
        m = result[key]
        write(
            f"{key:<10} {m['paragraphs']:>5} {m['words']:>6} {m['sentences']:>6} {m['mean']:>5.1f} "
            f"{m['median']:>7.1f} {m['p90']:>4.0f} {m['share_over_35']:>5.0%} {m['share_under_12']:>6.0%}\n"
        )
    target = result.get(only) if only else result.get("body")
    if target:
        write("\nSentence-initial connectives per 100 sentences:\n")
        for name, value in sorted(target["initial_per_100"].items(), key=lambda kv: -kv[1]):
            write(f"  {name:<18} {value:5.1f}  ({target['initial_counts'][name]})\n")
        write("\nInline features per 1000 words:\n")
        for name, value in target["inline_per_1000"].items():
            write(f"  {name:<28} {value:5.1f}\n")
    flags = band_flags(result if not only else {only: result[only]} if only in result else {})
    write("\nFlags against the team house-style band:\n")
    if not flags:
        write("  none\n")
    for flag in flags:
        write(f"  - {flag}\n")
    for key, m in result.items():
        if key == "body" or (only and key != only):
            continue
        for name, hits in m["banned"].items():
            for sentence in hits[:3]:
                write(f"    [{key}] {name}: {sentence[:160]}\n")
        for run in m["short_runs"][:2]:
            write(f"    [{key}] short run: {' | '.join(s[:60] for s in run)}\n")


def _print_diff(report: dict, show: int) -> None:
    write = sys.stdout.write
    write(f"Sentence diff: {report['old_sentences']} -> {report['new_sentences']} sentences\n")
    write(f"Hunk kinds: {report['kinds']}\n")
    write(
        f"Changed sentences: {report['changed_old']} -> {report['changed_new']}, "
        f"mean length {report['changed_mean_old']:.1f} -> {report['changed_mean_new']:.1f}\n"
    )
    write("Feature counts in changed sentences (old -> new):\n")
    for name, value in report["features_old"].items():
        after = report["features_new"][name]
        if value or after:
            write(f"  {name:<34} {value} -> {after}\n")
    write("Deleted words: " + ", ".join(report["deleted_words"]) + "\n")
    write("Inserted words: " + ", ".join(report["inserted_words"]) + "\n")
    for hunk in report["hunks"][:show]:
        write(f"\n[{hunk['kind']}]\n")
        for sentence in hunk["old"]:
            write(f"  - {sentence}\n")
        for sentence in hunk["new"]:
            write(f"  + {sentence}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", type=pathlib.Path, help="Manuscript file (.tex, .md, or .txt)")
    parser.add_argument("--section", choices=[k for k in SECTION_ORDER], help="Report one section only")
    parser.add_argument("--citations", action="store_true", help="Report citation keys repeated within a section")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--diff", nargs=2, type=pathlib.Path, metavar=("OLD", "NEW"), help="Classify edits between two versions")
    parser.add_argument("--show", type=int, default=0, help="With --diff, print the first N changed hunks")
    args = parser.parse_args(argv)

    if args.diff:
        for path in args.diff:
            if not path.is_file():
                parser.error(f"file not found: {path}")
        report = diff_report(*args.diff)
        if args.json:
            json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            _print_diff(report, args.show)
        return 0
    if args.path is None:
        parser.error("a manuscript path or --diff OLD NEW is required")
    if not args.path.is_file():
        parser.error(f"file not found: {args.path}")
    if args.citations:
        reuse = citation_reuse(args.path)
        if args.json:
            json.dump(reuse, sys.stdout, indent=2)
            sys.stdout.write("\n")
        elif not reuse:
            sys.stdout.write("No citation key is repeated within a section.\n")
        else:
            for section, keys in reuse.items():
                sys.stdout.write(f"{section}: " + ", ".join(f"{k} x{v}" for k, v in keys.items()) + "\n")
        return 0
    result = fingerprint(args.path)
    if args.json:
        serializable = {k: {kk: vv for kk, vv in v.items()} for k, v in result.items()}
        json.dump({"sections": serializable, "flags": band_flags(result)}, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        _print_fingerprint(args.path, result, args.section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

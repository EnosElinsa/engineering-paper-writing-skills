#!/usr/bin/env python3
"""Measure the prose fingerprint of a manuscript and compare it with the team house-style band.

Usage:
    python style_fingerprint.py DRAFT.tex
    python style_fingerprint.py DRAFT.md --section exp
    python style_fingerprint.py DRAFT.md --lang zh
    python style_fingerprint.py DRAFT.tex --citations
    python style_fingerprint.py DRAFT.tex --json
    python style_fingerprint.py --diff OLD.tex NEW.tex [--show 10]

Inputs: LaTeX (.tex), Markdown converted from a PDF (.md, one paragraph per line,
`#` headings), or plain text (.txt, blank-line paragraphs). English and Chinese
manuscripts are supported; `--lang auto` (the default) decides from the text.
A LaTeX root file is read with its \\input, \\include, \\subfile, and \\import files
inlined; missing files are skipped with a warning.

Counting rule (protocols S and R of the reader and terminology contract):
- displayed equations, figures, tables, algorithms, captions, and headings are excluded;
- citations are removed; cross-references count as one word;
- English: inline math is excluded from word counts and counts as one word in
  sentence lengths; a paragraph is a prose block of at least 20 words; sentences
  split at final punctuation before a capital letter, protecting et al., Fig.,
  Eq., e.g., i.e., and similar abbreviations; fragments under four words are
  run-in labels, not sentences;
- Chinese: lengths count CJK ideographs only (the Chinese manuscript adapter's
  rule); a paragraph has at least 30 ideographs; sentences split after the
  full-width full stop, question mark, and exclamation mark; fragments under five
  ideographs are labels.

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

# Checked in this order; the first match wins. Experiment patterns precede method
# patterns, and a top-level section that matches nothing but lies between the model
# and the experiments is assigned to the method by position (see resolve_roles).
SECTION_PATTERNS = (
    ("abstract", r"\babstract\b|摘要"),
    ("intro", r"introduction|引言|绪论"),
    ("related", r"related work|literature review|相关工作|研究现状"),
    ("model", r"system model|problem formulation|problem statement|problem description|system overview|"
              r"system description|\bmodel(l)?ing\b|系统模型|问题建模|问题描述"),
    ("concl", r"conclusion|结论|总结"),
    ("exp", r"experiment|numerical results|simulation|performance evaluation|evaluation|实验|仿真|性能评估"),
    ("future", r"future|未来工作|展望"),
    ("method", r"proposed|algorithm|solution|approach|scheme|mechanism|strategy|framework|\bmethod|"
               r"求解方法|所提算法|算法设计|方法设计|提出的算法"),
)

SECTION_ORDER = ("abstract", "intro", "related", "model", "method", "exp", "future", "concl", "body")

# Team house-style band (see references/styles/team-house-style.md, section "Sentence rhythm").
# calibrate:begin band
TEAM_BAND = {
    "body": {
        "mean": (21.4, 23.8),
        "median": (20.0, 22.0),
        "p90": (32.0, 37.0),
        "share_long": (0.07, 0.13),
        "share_short": (0.09, 0.14),
    },
    "section_mean": {
        "abstract": (24.8, 30.5),
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
}
# calibrate:end band

# Connective limits are house rules, not measurements; recalibration leaves them alone.
TEAM_BAND["initial_per_100"] = {
    "Since": (0.0, 1.0),
    "Hence": (0.0, 0.0),
    "Accordingly": (0.0, 1.0),
    "However": (1.0, 2.6),
}

# Chinese band: a weak prior converted from the English band with the Chinese
# manuscript adapter's default ratio of 1.5 to 2.0 ideographs per English word
# (lower ends times 1.5, upper ends times 2.0). Short and long thresholds use the
# midpoint ratio 1.75. Sentence and paragraph counts and shares transfer unchanged.
ZH_RATIO = (1.5, 2.0)
ZH_THRESHOLD_RATIO = 1.75


def _convert(band: tuple[float, float]) -> tuple[int, int]:
    return (round(band[0] * ZH_RATIO[0]), round(band[1] * ZH_RATIO[1]))


TEAM_BAND_ZH = {
    "body": {
        "mean": _convert(TEAM_BAND["body"]["mean"]),
        "median": _convert(TEAM_BAND["body"]["median"]),
        "p90": _convert(TEAM_BAND["body"]["p90"]),
        "share_long": TEAM_BAND["body"]["share_long"],
        "share_short": TEAM_BAND["body"]["share_short"],
    },
    "section_mean": {key: _convert(value) for key, value in TEAM_BAND["section_mean"].items()},
    "abstract_words": _convert(TEAM_BAND["abstract_words"]),
    "abstract_sentences": TEAM_BAND["abstract_sentences"],
    "conclusion_words": _convert(TEAM_BAND["conclusion_words"]),
    "conclusion_sentences": TEAM_BAND["conclusion_sentences"],
    # Result openers combined (因此, 因而, 所以, 由此); the reference papers use
    # Therefore, Thus, Consequently, and As a result 0.9 to 2.7 times per 100 sentences.
    "result_openers_per_100": (0.0, 2.7),
}

FURNITURE = re.compile(
    r"IEEE TRANSACTIONS|Authorized licensed use|Digital Object Identifier|Manuscript received|"
    r"This work was supported|\u00a9|Personal use is permitted|Recommended for acceptance|"
    r"Color versions of one or more|Corresponding author",
    re.I,
)

PROTECT = ("et al.", "Figs.", "Fig.", "Eqs.", "Eq.", "e.g.", "i.e.", "vs.", "Sec.", "Secs.", "No.", "Ref.", "Refs.", "resp.", "cf.")

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
CJK = re.compile(r"[\u4e00-\u9fff]")

ZH_RESULT_OPENERS = ("因此", "因而", "所以", "由此")

LANGUAGES = {
    "en": {
        "unit": "words",
        "min_paragraph": 20,
        "min_sentence": 4,
        "short": 12,
        "long": 35,
        "band": TEAM_BAND,
        "tolerance": {"mean": 1.0, "median": 1.0, "p90": 2.0, "share_long": 0.02, "share_short": 0.02, "section": 1.0},
        "connectives": (
            "As a result", "On the other hand", "On one hand", "In this section", "In this study", "In this paper",
            "In addition", "In particular", "In contrast", "For example", "For instance", "To this end",
            "As shown", "As illustrated", "However", "Therefore", "Thus", "Hence", "Consequently", "Moreover",
            "Furthermore", "Additionally", "Besides", "Meanwhile", "Specifically", "Notably", "Accordingly",
            "Nevertheless", "Nonetheless", "Similarly", "Finally", "First", "Second", "Third", "Then", "Since",
            "To address", "To solve", "To evaluate", "To validate", "To investigate", "To ensure", "Based on",
        ),
        "inline": {
            "thereby or participle tail": re.compile(r",\s+(thereby|making|leading|resulting|enabling|allowing|yielding|ensuring|causing|showing|indicating|providing|increasing|reducing|limiting|accommodating)\b", re.I),
            "due to": re.compile(r"\bdue to\b", re.I),
            ", which": re.compile(r",\s*which\b", re.I),
            ", where": re.compile(r",\s*where\b", re.I),
            "while/whereas": re.compile(r"\b(while|whereas)\b", re.I),
            "respectively": re.compile(r"\brespectively\b", re.I),
            "the proposed": re.compile(r"\bthe proposed\b", re.I),
            "this study/paper": re.compile(r"\bthis (study|paper|work|article)\b", re.I),
            "promotional modifier": re.compile(r"\b(significant|significantly|superior|superiority|critical|fundamental|fundamentally|crucial|essential|promising|comprehensive|comprehensively|remarkable|remarkably|novel)\b|state-of-the-art", re.I),
        },
        "banned": {
            "because": re.compile(r"\bbecause\b", re.I),
            "so (conjunction)": re.compile(r",\s*so\b|\bso that\b|\bso as to\b", re.I),
            ", but": re.compile(r",\s*but\b", re.I),
            "semicolon": re.compile(r";"),
            "Hence": re.compile(r"(?:^|[.!?]\s+)Hence\b"),
            "e.g. in prose": re.compile(r"\be\.g\.", re.I),
            "we/our outside future work": re.compile(r"\b[Ww]e\b(?!\s+will)|\b[Oo]ur\b"),
        },
    },
    "zh": {
        "unit": "chars",
        "min_paragraph": 30,
        "min_sentence": 5,
        "short": round(12 * ZH_THRESHOLD_RATIO),
        "long": round(35 * ZH_THRESHOLD_RATIO),
        "band": TEAM_BAND_ZH,
        "tolerance": {"mean": 1.5, "median": 1.5, "p90": 3.0, "share_long": 0.02, "share_short": 0.02, "section": 1.5},
        "connectives": (
            "在此基础上", "具体而言", "相比之下", "与此同时", "综上所述", "然而", "但是", "因此", "因而", "所以", "由此",
            "此外", "另外", "同时", "首先", "其次", "最后", "由于", "例如", "具体地", "综上", "可见", "据此", "进而",
            "从而", "其中", "为此", "为了", "针对", "基于", "对于",
        ),
        "inline": {
            "从而/进而 (thereby)": re.compile(r"[，,]\s*(从而|进而)"),
            "由于 (due to)": re.compile(r"由于"),
            "，其中 (where)": re.compile(r"[，,]\s*其中"),
            "，而 (whereas)": re.compile(r"[，,]\s*而(?!且)"),
            "，即 (namely)": re.compile(r"[，,]\s*即"),
            "本文 (this study)": re.compile(r"本文"),
            "promotional modifier": re.compile(r"显著|优越|卓越|全面|极大|新颖"),
        },
        "banned": {
            "full-width semicolon": re.compile(r"；"),
            "colon inside a sentence": lambda s: _zh_prose_colon(s),
            "把": re.compile(r"把(?!握)"),
            "让 (causative)": re.compile(r"让"),
            "一边…一边": re.compile(r"一边.*一边"),
            "colloquial degree word": re.compile(r"其实(?![际现施质验])|挺|非常|很|的话"),
            "weak connective 可见/据此": re.compile(r"(?:^|[，。])\s*(可见|据此)"),
            "unsupported universal": re.compile(r"显然|众所周知|毋庸置疑"),
            "我们 outside future work": re.compile(r"我们(?!将)"),
        },
    },
}

STOP = set(
    "the a an of to in and or for on with by is are be was were this that these those as at from it its "
    "which where while than then into over under each all both not no also can may their".split()
)

# Roadmap sentences ("Section II reviews ...", "第 II 节综述……") are short by design;
# they neither count toward nor break a run of short sentences.
ROADMAP = re.compile(r"^(The (remainder|rest) of this|Sections?\s+[IVX\d]|本文其余部分|第\s*[IVX\d一二三四五六七八九十]+\s*节)")


def _zh_prose_colon(sentence: str) -> bool:
    """A colon inside a Chinese sentence, other than a list lead-in or a run-in label."""
    for match in re.finditer(r"：(?=\S)", sentence):
        prefix = sentence[:match.start()]
        if prefix.endswith(("如下", "以下")):
            continue
        marker = re.match(r"^\s*(?:[*\-\u2022]+|（\d+）|\(\d+\)|\d+[.、)])\s*", prefix)
        label = prefix[marker.end():] if marker else ""
        if marker and len(label) <= 30 and "，" not in label and "。" not in label:
            continue
        return True
    return False


def _hits(rule, sentence: str) -> bool:
    return bool(rule(sentence)) if callable(rule) else bool(rule.search(sentence))


# --------------------------------------------------------------------------- parsing


# Method words for headings without a section number (a Markdown paper title such as
# "...: A Multi-Objective Optimization Approach" must not open a method section).
METHOD_STRICT = (
    r"proposed\b.*\b(algorithm|method|framework|approach)|algorithm design|solution approach|"
    r"求解方法|所提算法|算法设计|方法设计|提出的算法"
)


def classify(title: str, strict: bool = False) -> str | None:
    lowered = title.lower()
    for key, pattern in SECTION_PATTERNS:
        if strict and key == "method":
            pattern = METHOD_STRICT
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


REFERENCES_HEADING = re.compile(r"references|bibliography|acknowledg|参考文献|致谢", re.I)

# A block is (top-level section index, top-level title, current heading, raw paragraph).
# The index is -1 for the abstract.
Block = tuple[int, str, str, str]


def resolve_roles(titles: list[str]) -> list[str | None]:
    """Classify top-level section titles, then fill in method sections by position.

    A section whose title names no role and that lies between the last introduction,
    related-work, or model section and the first experiment section is the method
    section (many papers title it with the algorithm name). Reference and
    acknowledgment sections get None and are skipped.
    """
    roles: list[str | None] = [None if REFERENCES_HEADING.search(t) else (classify(t) or "other") for t in titles]
    if "exp" in roles:
        first_exp = roles.index("exp")
        anchors = [i for i, role in enumerate(roles[:first_exp]) if role in {"intro", "related", "model"}]
        if anchors:
            for i in range(anchors[-1] + 1, first_exp):
                if roles[i] == "other":
                    roles[i] = "method"
    return roles


def tex_blocks(text: str) -> tuple[list[str], list[Block], list[str]]:
    """Return top-level titles, prose blocks, and the fallback paragraphs of a LaTeX source."""
    text = re.sub(r"(?<!\\)%.*", "", text)
    blocks: list[Block] = []
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, flags=re.S)
    if match:
        for paragraph in _tex_paragraphs(_remove_environments(match.group(1))):
            blocks.append((-1, "Abstract", "Abstract", paragraph))
        text = text.replace(match.group(0), " ")
    match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, flags=re.S)
    body = match.group(1) if match else text
    body = re.split(r"\\bibliography\{|\\begin\{thebibliography\}|\\appendices\b|\\appendix\b|\\begin\{IEEEbiography", body)[0]
    body = _remove_environments(body)
    fallback = _tex_paragraphs(body)
    for command, marker in (("section", "S"), ("subsection", "U"), ("subsubsection", "U")):
        body = _strip_command(body, command, keep=False, replacement=f"\n\n@@{marker}@@{{arg}}@@END@@\n\n")
    titles: list[str] = []
    top: int | None = None
    heading = ""
    for chunk in re.split(r"(@@[SU]@@.*?@@END@@)", body, flags=re.S):
        marker = re.match(r"^@@([SU])@@(.*?)@@END@@$", chunk, flags=re.S)
        if marker:
            title = clean_tex(marker.group(2))
            if marker.group(1) == "S":
                titles.append(title)
                top = len(titles) - 1
            heading = title
            continue
        if top is None:
            continue
        for paragraph in _tex_paragraphs(chunk):
            blocks.append((top, titles[top], heading, paragraph))
    return titles, blocks, fallback


def md_blocks(text: str) -> tuple[list[str], list[Block], list[str]]:
    """Return top-level titles, prose blocks, and the fallback paragraphs of a Markdown source."""
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"<table.*?</table>", " ", text, flags=re.S | re.I)
    fallback = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    titles: list[str] = []
    blocks: list[Block] = []
    top: int | None = None
    heading = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        abstract = re.match(r"^(Abstract|摘要)\s*[\u2014\-:.：]\s*", line)
        if abstract:
            blocks.append((-1, "Abstract", "Abstract", line[abstract.end():]))
            continue
        if line.startswith(("Index Terms", "关键词")):
            continue
        match = re.match(r"^#+\s*(.*)$", line)
        if match:
            title = match.group(1).strip()
            if REFERENCES_HEADING.search(title) and not re.match(r"^[A-H]\.\s", title):
                titles.append(title)
                top = None
            elif re.match(r"^[A-H]\.\s", title):
                if top is not None:
                    heading = title
            elif re.match(r"^[IVX]+\.\s", title) or classify(title, strict=True):
                titles.append(title)
                top = len(titles) - 1
                heading = title
            continue
        if top is None:
            continue
        if line.startswith(("!", "|", "<")) or FURNITURE.search(line):
            continue
        if re.match(r"^(Fig\.|TABLE|Table|Algorithm)\s*[0-9IVX]+", line) and len(line) < 400:
            continue
        if re.match(r"^(图|表|算法)\s*\d", line) and len(line) < 300:
            continue
        blocks.append((top, titles[top], heading, line))
    return titles, blocks, fallback


def document_blocks(path: pathlib.Path) -> tuple[list[str | None], list[Block], list[str], bool]:
    """Return section roles, prose blocks, fallback paragraphs, and whether the source is LaTeX."""
    text = read_source(path)
    suffix = path.suffix.lower()
    if suffix == ".tex":
        titles, blocks, fallback = tex_blocks(text)
        return resolve_roles(titles), blocks, fallback, True
    if suffix in {".md", ".markdown"}:
        titles, blocks, fallback = md_blocks(text)
        return resolve_roles(titles), blocks, fallback, False
    return [], [], [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()], False


def _sections(roles: list[str | None], blocks: list[Block], fallback: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    for top, _title, _heading, paragraph in blocks:
        role = "abstract" if top < 0 else roles[top]
        if role is None:
            continue
        sections.setdefault(role, []).append(paragraph)
    if not any(key != "abstract" for key in sections):
        sections.setdefault("body", []).extend(fallback)
    return sections


def parse_tex(text: str) -> dict[str, list[str]]:
    titles, blocks, fallback = tex_blocks(text)
    return _sections(resolve_roles(titles), blocks, fallback)


def parse_md(text: str) -> dict[str, list[str]]:
    titles, blocks, fallback = md_blocks(text)
    return _sections(resolve_roles(titles), blocks, fallback)


def clean_md(paragraph: str) -> str:
    text = re.sub(r"\$[^$]*\$", f" {MATH} ", paragraph)
    text = re.sub(r"\[\s*\d+(\s*[,\u2013\-]\s*\d+)*\s*\]", "", text)
    return re.sub(r"\s+", " ", text).strip()


INCLUDE = re.compile(r"\\(input|include|subfile|import|subimport)\s*(?:\{([^}]*)\})?\s*\{([^}]+)\}")
MISSING_INCLUDES: dict[str, list[str]] = {}


def _resolve_include(base: pathlib.Path, root: pathlib.Path, folder: str | None, name: str) -> pathlib.Path | None:
    name = name.strip()
    candidates = []
    for directory in (base, root):
        target = directory / (folder or "") / name
        candidates.extend([target, target.with_name(target.name + ".tex")])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def expand_tex(path: pathlib.Path, root: pathlib.Path | None = None, seen: set[pathlib.Path] | None = None,
               depth: int = 0) -> str:
    """Return the LaTeX source with \\input, \\include, \\subfile, and \\import files inlined.

    Paths resolve against the including file's folder, then the root file's folder.
    Comments are removed first, so a commented-out \\input is not expanded. Missing
    files are recorded in MISSING_INCLUDES under the root file's name.
    """
    path = path.resolve()
    root = root or path.parent
    seen = seen or set()
    if depth > 10 or path in seen:
        return ""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    text = re.sub(r"(?<!\\)%.*", "", text)
    seen = seen | {path}

    def replace(match: re.Match) -> str:
        command, folder, name = match.group(1), match.group(2), match.group(3)
        if command in {"import", "subimport"} and folder is None:
            return match.group(0)
        target = _resolve_include(path.parent, root, folder, name)
        if target is None:
            MISSING_INCLUDES.setdefault(str(root), []).append(name)
            return " "
        inner = expand_tex(target, root, seen, depth + 1)
        if command == "subfile":
            body = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", inner, flags=re.S)
            inner = body.group(1) if body else inner
        return "\n\n" + inner + "\n\n"

    return INCLUDE.sub(replace, text)


def read_source(path: pathlib.Path) -> str:
    if path.suffix.lower() == ".tex":
        return expand_tex(path)
    return path.read_text(encoding="utf-8-sig", errors="replace")


def load(path: pathlib.Path) -> tuple[dict[str, list[str]], bool]:
    roles, blocks, fallback, tex = document_blocks(path)
    return _sections(roles, blocks, fallback), tex


def detect_language(sections: dict[str, list[str]]) -> str:
    text = " ".join(p for paragraphs in sections.values() for p in paragraphs)
    return "zh" if len(CJK.findall(text)) >= len(WORD.findall(text)) else "en"


def resolve_language(path: pathlib.Path, lang: str = "auto") -> str:
    if lang in LANGUAGES:
        return lang
    sections, _ = load(path)
    return detect_language(sections)


# --------------------------------------------------------------------------- metrics


def split_sentences(paragraph: str, lang: str = "en") -> list[str]:
    if lang == "zh":
        return [part.strip() for part in re.split(r"(?<=[。！？])", paragraph) if part.strip()]
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


def units(text: str, lang: str = "en") -> int:
    """Word count (English) or ideograph count (Chinese) of prose text."""
    return len(CJK.findall(text)) if lang == "zh" else len(words(text))


def sentence_length(sentence: str, lang: str = "en") -> int:
    return len(CJK.findall(sentence)) if lang == "zh" else len(WORD.findall(sentence))


def prose_paragraphs(paragraphs: list[str], tex: bool, lang: str = "en") -> list[str]:
    cleaned = [clean_tex(p) if tex else clean_md(p) for p in paragraphs]
    minimum = LANGUAGES[lang]["min_paragraph"]
    return [p for p in cleaned if units(p, lang) >= minimum or re.match(r"^[\u2022\-*]\s", p)]


def percentile(values: list[int], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return float(ordered[int(fraction * (len(ordered) - 1))])


def _opener(sentence: str, connectives: tuple[str, ...]) -> str | None:
    stripped = re.sub(r"^[\u2022\-*（(]?\s*(?:\d+[)）]|[ivx]+[)）])?\s*", "", sentence.strip())
    for connective in sorted(connectives, key=len, reverse=True):
        if stripped.startswith(connective) and (not connective[-1].isalpha() or not connective.isascii()
                                                 or re.match(re.escape(connective) + r"\b", stripped)):
            return connective
    return None


def measure(paragraphs: list[str], lang: str = "en") -> dict:
    profile = LANGUAGES[lang]
    sentences_by_paragraph = [
        [s for s in split_sentences(p, lang) if sentence_length(s, lang) >= profile["min_sentence"]] for p in paragraphs
    ]
    sentences = [s for group in sentences_by_paragraph for s in group]
    lengths = [sentence_length(s, lang) for s in sentences]
    unit_count = sum(units(p, lang) for p in paragraphs)
    initial: Counter[str] = Counter()
    openers = [_opener(s, profile["connectives"]) for s in sentences]
    for opener in openers:
        if opener:
            initial[opener] += 1
    repeated_openers = [
        (openers[i], sentences[i + 1]) for i in range(len(sentences) - 1) if openers[i] and openers[i] == openers[i + 1]
    ]
    inline = {name: sum(len(pattern.findall(p)) for p in paragraphs) for name, pattern in profile["inline"].items()}
    banned: dict[str, list[str]] = {}
    for name, rule in profile["banned"].items():
        hits = [s for s in sentences if _hits(rule, s)]
        if hits:
            banned[name] = hits
    short_runs = []
    for group in sentences_by_paragraph:
        run: list[str] = []
        for sentence in group + [""]:
            if sentence and ROADMAP.match(sentence):
                continue
            if sentence and sentence_length(sentence, lang) < profile["short"]:
                run.append(sentence)
                continue
            if len(run) >= 3:
                short_runs.append(run)
            run = []
    count = len(sentences)
    return {
        "unit": profile["unit"],
        "paragraphs": len(paragraphs),
        "words": unit_count,
        "sentences": count,
        "mean": statistics.mean(lengths) if lengths else 0.0,
        "median": float(statistics.median(lengths)) if lengths else 0.0,
        "p90": percentile(lengths, 0.9),
        "share_long": sum(1 for x in lengths if x > profile["long"]) / count if count else 0.0,
        "share_short": sum(1 for x in lengths if x < profile["short"]) / count if count else 0.0,
        "initial_per_100": {k: 100.0 * v / count for k, v in initial.items()} if count else {},
        "initial_counts": dict(initial),
        "inline_per_1000": {k: 1000.0 * v / unit_count for k, v in inline.items()} if unit_count else {},
        "banned": banned,
        "short_runs": short_runs,
        "repeated_openers": repeated_openers,
    }


def fingerprint(path: pathlib.Path, lang: str = "auto") -> dict[str, dict]:
    sections, tex = load(path)
    if lang not in LANGUAGES:
        lang = detect_language(sections)
    result: dict[str, dict] = {}
    classified: list[str] = []
    unclassified: list[str] = []
    for key, paragraphs in sections.items():
        prose = prose_paragraphs(paragraphs, tex, lang)
        if key == "abstract":
            prose = [clean_tex(p) if tex else clean_md(p) for p in paragraphs]
            prose = [p for p in prose if units(p, lang)]
        if not prose:
            continue
        result[key] = measure(prose, lang)
        if key in {"other", "body"}:
            unclassified.extend(prose)
        elif key != "abstract":
            classified.extend(prose)
    # Sections whose headings match no known role (appendix-like material) join the
    # body only when no section could be classified.
    body = classified or unclassified
    if body:
        result["body"] = measure(body, lang)
    return result


def _status(value: float, low: float, high: float, tolerance: float) -> str:
    if low <= value <= high:
        return "in"
    if low - tolerance <= value <= high + tolerance:
        return "near"
    return "low" if value < low else "high"


def result_language(result: dict[str, dict]) -> str:
    for measured in result.values():
        return "zh" if measured.get("unit") == "chars" else "en"
    return "en"


def band_flags(result: dict[str, dict]) -> list[str]:
    lang = result_language(result)
    profile = LANGUAGES[lang]
    band, tolerance = profile["band"], profile["tolerance"]
    prior = " (weak prior converted from the English band)" if lang == "zh" else ""
    flags: list[str] = []
    body = result.get("body")
    if body:
        for name, (low, high) in band["body"].items():
            state = _status(body[name], low, high, tolerance[name])
            if state not in {"in", "near"}:
                flags.append(f"body {name} = {body[name]:.2f} is {state} (band {low}-{high}){prior}")
        if lang == "en":
            for connective, (low, high) in band["initial_per_100"].items():
                value = body["initial_per_100"].get(connective, 0.0)
                if value > high + 0.25:
                    flags.append(f"sentence-initial {connective} = {value:.1f} per 100 sentences (band {low}-{high})")
                if connective == "However" and body["sentences"] >= 100 and value < low - 0.5:
                    flags.append(f"sentence-initial However = {value:.1f} per 100 sentences (band {low}-{high})")
        else:
            value = sum(body["initial_per_100"].get(k, 0.0) for k in ZH_RESULT_OPENERS)
            low, high = band["result_openers_per_100"]
            if value > high + 0.25:
                flags.append(
                    f"sentence-initial result openers ({'/'.join(ZH_RESULT_OPENERS)}) = {value:.1f} per 100 sentences "
                    f"(band {low}-{high}){prior}"
                )
    for section, (low, high) in band["section_mean"].items():
        measured = result.get(section)
        if measured and measured["sentences"] >= 5:
            state = _status(measured["mean"], low, high, tolerance["section"])
            if state not in {"in", "near"}:
                flags.append(f"{section} mean sentence length = {measured['mean']:.1f} is {state} (band {low}-{high}){prior}")
    unit = profile["unit"]
    for section, words_key, sentences_key in (
        ("abstract", "abstract_words", "abstract_sentences"),
        ("concl", "conclusion_words", "conclusion_sentences"),
    ):
        measured = result.get(section)
        if not measured:
            continue
        low, high = band[words_key]
        if not low <= measured["words"] <= high:
            flags.append(f"{section} has {measured['words']} {unit} (band {low}-{high}){prior}")
        low, high = band[sentences_key]
        if not low <= measured["sentences"] <= high:
            flags.append(f"{section} has {measured['sentences']} sentences (band {low}-{high})")
    for section, measured in result.items():
        if section == "body":
            continue
        for name, hits in measured["banned"].items():
            flags.append(f"{section}: {len(hits)} sentence(s) with {name}")
        if measured["short_runs"]:
            flags.append(
                f"{section}: {len(measured['short_runs'])} run(s) of three or more sentences under "
                f"{profile['short']} {unit}"
            )
        if measured["repeated_openers"]:
            flags.append(
                f"{section}: {len(measured['repeated_openers'])} pair(s) of consecutive sentences open with the same connective"
            )
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
                continue
            # IEEE range across brackets: [7]-[10] means 7 through 10.
            paragraph = re.sub(r"\[\s*(\d+)\s*\]\s*[\u2013\-]\s*\[\s*(\d+)\s*\]", r"[\1-\2]", paragraph)
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


# --------------------------------------------------------------------------- spine


def spine(path: pathlib.Path, lang: str = "auto", section: str | None = None) -> list[dict]:
    """Return the opening sentence of every prose paragraph, grouped under its heading.

    Each entry is {"section": role, "heading": title, "openers": [sentence, ...]}.
    """
    roles, raw_blocks, fallback, tex = document_blocks(path)
    if lang not in LANGUAGES:
        lang = detect_language(_sections(roles, raw_blocks, fallback))
    minimum = LANGUAGES[lang]["min_paragraph"]
    blocks: list[tuple[str, str, str]] = []  # (section role, heading, paragraph)
    for top, _title, heading, paragraph in raw_blocks:
        role = "abstract" if top < 0 else roles[top]
        if role is not None:
            blocks.append((role, heading, paragraph))
    if not blocks:
        blocks = [("body", "", paragraph) for paragraph in fallback]
    entries: list[dict] = []
    for role, heading, paragraph in blocks:
        if section and role != section:
            continue
        cleaned = clean_tex(paragraph) if tex else clean_md(paragraph)
        if units(cleaned, lang) < minimum and not re.match(r"^[\u2022\-*]\s", cleaned):
            continue
        sentences = split_sentences(cleaned, lang)
        if not sentences:
            continue
        if not entries or entries[-1]["heading"] != heading or entries[-1]["section"] != role:
            entries.append({"section": role, "heading": heading, "openers": []})
        entries[-1]["openers"].append(sentences[0])
    return entries


def _print_spine(path: pathlib.Path, entries: list[dict]) -> None:
    write = sys.stdout.write
    write(f"Paragraph-opening sentences: {path.name}\n")
    number = 0
    for entry in entries:
        write(f"\n[{entry['section']}] {entry['heading']}\n")
        for opener in entry["openers"]:
            number += 1
            write(f"  P{number}. {opener}\n")


# --------------------------------------------------------------------------- abbreviations

ABBR_EN = re.compile(r"\(\s*([A-Z][A-Za-z0-9\-]*?)\s*\)")
ABBR_ZH = re.compile(r"[（(]\s*([A-Za-z][^（）()，,]*?)\s*[，,]\s*([A-Z][A-Za-z0-9\-]*?)\s*[）)]")
TOKEN = re.compile(r"(?<![A-Za-z0-9-])[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*")
ROMAN = re.compile(r"^[IVXLCDM]+$")
UNITS = {"MHz", "GHz", "kHz", "Hz", "MJ", "kJ", "dB", "dBm", "dBi", "Mbps", "Gbps", "kbps", "Mbit", "Gbit",
         "MB", "GB", "KB", "TB", "mAh", "Wh", "kWh", "GFLOPS", "TFLOPS"}
LONG_FORM_SKIP = {"of", "and", "the", "for", "in", "on", "with", "a", "an", "to", "by", "based"}


def _singular(token: str) -> str:
    """Strip a plural s from an acronym (UAVs -> UAV, DCMOEAs -> DCMOEA)."""
    return token[:-1] if len(token) > 2 and token.endswith("s") and token[-2].isupper() else token


def _is_acronym(text: str) -> bool:
    text = _singular(text)
    return (
        sum(c.isupper() for c in text) >= 2
        and not any(c.isdigit() for c in text)
        and not ROMAN.match(text)
        and text not in UNITS
        and text != MATH
    )


def _initials_match(letters: list[str], tokens: list[str]) -> int | None:
    """Return the start index of the shortest word span whose initials spell the letters."""
    def walk(i: int, j: int) -> int | None:
        if j < 0:
            return i + 1
        if i < 0:
            return None
        word = tokens[i].lower()
        if word[:1] == letters[j]:
            found = walk(i - 1, j - 1)
            if found is not None:
                return found
        if word in LONG_FORM_SKIP and j < len(letters) - 1:
            return walk(i - 1, j)
        return None

    return walk(len(tokens) - 1, len(letters) - 1)


def _best_long_form(short: str, candidate: str) -> str | None:
    """Find the long form before '(ABBR)': word initials first, then Schwartz-Hearst letter matching."""
    letters = [c.lower() for c in short if c.isalpha()]
    words_only = re.findall(r"[A-Za-z][A-Za-z'\-]*", candidate)
    for tokens in (words_only, [part for word in words_only for part in word.split("-") if part]):
        start = _initials_match(letters, tokens)
        if start is not None:
            return " ".join(tokens[start:])
    s, l = len(letters) - 1, len(candidate) - 1
    while s >= 0:
        char = letters[s]
        while l >= 0 and (candidate[l].lower() != char or (s == 0 and l > 0 and candidate[l - 1].isalnum())):
            l -= 1
        if l < 0:
            return None
        l -= 1
        s -= 1
    return candidate[l + 1:].strip()


def _acronym_tokens(text: str) -> list[str]:
    """Acronyms used in the text: whole compounds such as H-PPO or NSGA-II, and the acronym
    parts of mixed compounds such as UAV-assisted or mothership-UAV."""
    found: list[str] = []
    for token in TOKEN.findall(text):
        if re.match(r"^([A-Z]-[IVXLC]+|[IVXLC]+-[A-Z])$", token):
            continue
        parts = [p for p in token.split("-") if p]
        whole = all(_is_acronym(p) or ROMAN.match(p) or (len(p) == 1 and p.isupper()) for p in parts)
        if len(parts) > 1 and whole and _is_acronym(token):
            found.append(_singular(token))
            continue
        found.extend(_singular(p) for p in parts if _is_acronym(p))
    return found


def _normalize_long_form(form: str) -> str:
    parts = re.split(r"[\s\-]+", form.lower())
    return " ".join(p[:-1] if len(p) > 3 and p.endswith("s") and not p.endswith("ss") else p for p in parts if p)


def _uses(text: str, abbr: str) -> list[int]:
    return [m.start() for m in re.finditer(r"(?<![A-Za-z0-9-])" + re.escape(abbr) + r"s?(?![A-Za-z0-9-])", text)]


def _definitions(text: str) -> list[tuple[str, str, int]]:
    """Return (abbreviation, long form, position) for every 'long form (ABBR)' in the text."""
    found = []
    for match in ABBR_ZH.finditer(text):
        abbr = _singular(match.group(2))
        if _is_acronym(abbr):
            found.append((abbr, match.group(1).strip().lower(), match.start(2)))
    for match in ABBR_EN.finditer(text):
        abbr = _singular(match.group(1))
        if not _is_acronym(abbr):
            continue
        before = text[:match.start()].rstrip()
        candidate = " ".join(before.split()[-(len(abbr) + 5):])
        long_form = _best_long_form(abbr, candidate)
        if long_form:
            found.append((abbr, long_form.lower(), match.start(1)))
    return sorted(found, key=lambda item: item[2])


def abbreviation_report(path: pathlib.Path) -> dict:
    sections, tex = load(path)
    clean = (lambda p: clean_tex(p)) if tex else (lambda p: clean_md(p))
    abstract = " ".join(clean(p) for p in sections.get("abstract", []))
    body = " ".join(clean(p) for key, paragraphs in sections.items() if key != "abstract" for p in paragraphs)
    report: dict = {"document": path.name}
    abstract_defs = {abbr for abbr, _, _ in _definitions(abstract)}
    abstract_tokens = set(_acronym_tokens(abstract))
    report["abstract_undefined"] = sorted(t for t in abstract_tokens if t not in abstract_defs)
    definitions = _definitions(body)
    positions: dict[str, list[int]] = {}
    long_forms: dict[str, str] = {}
    for abbr, long_form, position in definitions:
        positions.setdefault(abbr, []).append(position)
        long_forms.setdefault(abbr, long_form)
    report["defined"] = len(positions)
    report["long_forms"] = long_forms
    report["used_before_definition"] = sorted(a for a, pos in positions.items() if _uses(body, a) and _uses(body, a)[0] < pos[0] - 1)
    report["defined_more_than_once"] = sorted(a for a, pos in positions.items() if len(pos) > 1)
    report["rarely_used"] = sorted(a for a, pos in positions.items() if len(_uses(body, a)) - len(pos) <= 1)
    tokens = Counter(_acronym_tokens(body))
    report["never_defined"] = sorted(t for t, n in tokens.items() if n >= 2 and t not in positions)
    if not abstract:
        report["abstract_undefined"] = []
    return report


def abbreviation_audit(paths: list[pathlib.Path]) -> dict:
    reports = [abbreviation_report(path) for path in paths]
    forms: dict[str, dict[str, str]] = {}
    for report in reports:
        for abbr, long_form in report["long_forms"].items():
            forms.setdefault(abbr, {})[report["document"]] = long_form
    mismatches = {
        abbr: docs for abbr, docs in forms.items()
        if len({_normalize_long_form(form) for form in docs.values()}) > 1
    }
    return {"documents": reports, "long_form_mismatches": mismatches}


def _print_abbreviations(audit: dict) -> None:
    write = sys.stdout.write
    labels = (
        ("used_before_definition", "used before its first definition"),
        ("defined_more_than_once", "defined more than once in the body"),
        ("rarely_used", "defined but used at most once afterwards (consider spelling out)"),
        ("abstract_undefined", "used in the abstract without a definition in the abstract"),
        ("never_defined", "used at least twice but never defined (check: names, units, or missing definitions)"),
    )
    for report in audit["documents"]:
        write(f"Abbreviations: {report['document']} ({report['defined']} defined in the body)\n")
        for key, label in labels:
            items = report[key]
            write(f"  {label}: {', '.join(items) if items else 'none'}\n")
    if len(audit["documents"]) > 1:
        write("Across documents:\n")
        if not audit["long_form_mismatches"]:
            write("  every abbreviation has one long form\n")
        for abbr, docs in audit["long_form_mismatches"].items():
            write(f"  {abbr}: " + "; ".join(f"'{form}' ({doc})" for doc, form in docs.items()) + "\n")


# --------------------------------------------------------------------------- diff


def sentence_list(path: pathlib.Path, lang: str = "auto") -> list[str]:
    sections, tex = load(path)
    if lang not in LANGUAGES:
        lang = detect_language(sections)
    minimum = LANGUAGES[lang]["min_sentence"]
    out: list[str] = []
    for key in sections:
        for paragraph in sections[key]:
            cleaned = clean_tex(paragraph) if tex else clean_md(paragraph)
            out.extend(s for s in split_sentences(cleaned, lang) if units(s, lang) >= minimum)
    return out


def diff_report(old_path: pathlib.Path, new_path: pathlib.Path, lang: str = "auto") -> dict:
    if lang not in LANGUAGES:
        lang = resolve_language(new_path)
    profile = LANGUAGES[lang]
    old, new = sentence_list(old_path, lang), sentence_list(new_path, lang)
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
        counts = {name: len(pattern.findall(text)) for name, pattern in profile["inline"].items()}
        counts.update(
            {f"banned: {name}": sum(1 for s in sentences if _hits(rule, s)) for name, rule in profile["banned"].items()}
        )
        return counts

    def tokens(sentences: list[str]) -> Counter[str]:
        if lang == "zh":
            return Counter(c for s in sentences for c in CJK.findall(s))
        return Counter(w.lower() for s in sentences for w in words(s))

    deleted = tokens(old_changed) - tokens(new_changed)
    inserted = tokens(new_changed) - tokens(old_changed)
    lengths_old = [sentence_length(s, lang) for s in old_changed]
    lengths_new = [sentence_length(s, lang) for s in new_changed]
    return {
        "language": lang,
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
    lang = result_language(result)
    profile = LANGUAGES[lang]
    unit = profile["unit"]
    write(f"Style fingerprint: {path.name} (language: {lang}; lengths in {unit})\n\n")
    write(f"section    paras {unit:>6}  sents  mean  median  p90  >{profile['long']}  <{profile['short']}\n")
    for key in SECTION_ORDER + tuple(k for k in result if k not in SECTION_ORDER):
        if key not in result or (only and key != only):
            continue
        m = result[key]
        write(
            f"{key:<10} {m['paragraphs']:>5} {m['words']:>6} {m['sentences']:>6} {m['mean']:>5.1f} "
            f"{m['median']:>7.1f} {m['p90']:>4.0f} {m['share_long']:>5.0%} {m['share_short']:>5.0%}\n"
        )
    target = result.get(only) if only else result.get("body")
    if target:
        write("\nSentence-initial connectives per 100 sentences:\n")
        for name, value in sorted(target["initial_per_100"].items(), key=lambda kv: -kv[1]):
            write(f"  {name:<18} {value:5.1f}  ({target['initial_counts'][name]})\n")
        write(f"\nWithin-sentence features per 1000 {unit}:\n")
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
        for opener, sentence in m["repeated_openers"][:2]:
            write(f"    [{key}] repeated opener {opener}: {sentence[:120]}\n")


def _print_diff(report: dict, show: int) -> None:
    write = sys.stdout.write
    write(f"Sentence diff ({report['language']}): {report['old_sentences']} -> {report['new_sentences']} sentences\n")
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
    parser.add_argument("paths", nargs="*", type=pathlib.Path, help="Manuscript file(s) (.tex, .md, or .txt)")
    parser.add_argument("--section", choices=[k for k in SECTION_ORDER], help="Report one section only")
    parser.add_argument("--lang", choices=["auto", "en", "zh"], default="auto", help="Manuscript language")
    parser.add_argument("--citations", action="store_true", help="Report citation keys repeated within a section")
    parser.add_argument(
        "--spine",
        action="store_true",
        help="Print the opening sentence of every paragraph under its heading (combine with --section)",
    )
    parser.add_argument(
        "--abbrev",
        action="store_true",
        help="Audit abbreviation definitions and uses; pass several files (manuscript, supplement, letter) to compare them",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--diff", nargs=2, type=pathlib.Path, metavar=("OLD", "NEW"), help="Classify edits between two versions")
    parser.add_argument("--show", type=int, default=0, help="With --diff, print the first N changed hunks")
    args = parser.parse_args(argv)

    if args.diff:
        for path in args.diff:
            if not path.is_file():
                parser.error(f"file not found: {path}")
        report = diff_report(*args.diff, lang=args.lang)
        if args.json:
            json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            _print_diff(report, args.show)
        return 0
    if not args.paths:
        parser.error("a manuscript path or --diff OLD NEW is required")
    for path in args.paths:
        if not path.is_file():
            parser.error(f"file not found: {path}")
    if args.abbrev:
        audit = abbreviation_audit(args.paths)
        if args.json:
            json.dump(audit, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            _print_abbreviations(audit)
        return 0
    if len(args.paths) > 1:
        parser.error("several files are accepted only with --abbrev")
    args.path = args.paths[0]
    if args.path.suffix.lower() == ".tex":
        read_source(args.path)
        missing = MISSING_INCLUDES.get(str(args.path.resolve().parent), [])
        if missing:
            sys.stderr.write("warning: included file(s) not found and skipped: " + ", ".join(sorted(set(missing))) + "\n")
    if args.spine:
        entries = spine(args.path, args.lang, args.section)
        if args.json:
            json.dump(entries, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            _print_spine(args.path, entries)
        return 0
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
    result = fingerprint(args.path, args.lang)
    if args.json:
        json.dump(
            {"language": result_language(result), "sections": result, "flags": band_flags(result)},
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
    else:
        _print_fingerprint(args.path, result, args.section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

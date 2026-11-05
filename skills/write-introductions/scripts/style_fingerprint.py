#!/usr/bin/env python3
"""Measure the prose fingerprint of a manuscript and compare it with the team house-style band.

Usage:
    python style_fingerprint.py DRAFT.tex
    python style_fingerprint.py DRAFT.md --section exp
    python style_fingerprint.py DRAFT.md --lang zh
    python style_fingerprint.py DRAFT.tex --citations
    python style_fingerprint.py DRAFT.tex --scale exp=900-1900 exp.paragraphs=10-19 --terms TERMS.txt
    python style_fingerprint.py --report MAIN.tex SUPP.tex REPLY.tex --terms TERMS.txt --out report.md
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
        "mean": (23.2, 24.8),
        "median": (21.0, 23.0),
        "p90": (37.0, 39.0),
        "share_long": (0.11, 0.15),
        "share_short": (0.09, 0.11),
    },
    "section_mean": {
        "abstract": (24.8, 30.5),
        "intro": (20.1, 23.6),
        "related": (21.3, 26.3),
        "model": (22.7, 27.1),
        "method": (20.5, 27.0),
        "exp": (22.6, 24.6),
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

PROTECT = ("et al.", "Figs.", "Fig.", "Eqs.", "Eq.", "e.g.", "i.e.", "vs.", "Sec.", "Secs.", "Ref.", "Refs.", "resp.", "cf.")

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
        "tolerance": {"mean": 1.0, "median": 1.0, "p90": 2.0, "share_long": 0.02, "share_short": 0.02, "section": 3.0},
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
        "tolerance": {"mean": 1.5, "median": 1.5, "p90": 3.0, "share_long": 0.02, "share_short": 0.02, "section": 5.0},
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
    text = re.sub(r"\\(?:begin|end)\{(?:itemize|enumerate|description)\}(?:\[[^\]]*\])?", " ", text)
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


# A block that opens with a lowercase prose word (not a symbol such as r_j or log_2) continues
# the block before it.
CONTINUATION = re.compile(r"^(?:\\noindent\s*)?[a-z]{2,}\b(?!\s*[_^{(=])")


def _tex_paragraphs(block: str) -> list[str]:
    for command in ("subsubsection", "subsection", "paragraph"):
        block = _strip_command(block, command, keep=False, replacement="\n\n")
    block = re.sub(r"\\item\b", "\n\n" + ITEM_MARK, block)
    parts: list[str] = []
    for part in (part.strip() for part in re.split(r"\n\s*\n", block)):
        # Text that continues after a display (a lowercase where clause) belongs to its lead-in.
        if parts and CONTINUATION.match(part):
            parts[-1] += " " + part
        elif part:
            parts.append(part)
    return parts


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
        # A table note (`Note. ...`) and a caption line are not prose. A line that starts a reporting
        # sentence such as "Table III presents ..." is prose.
        if re.match(r"^[*_]{0,2}Notes?[.:]", line) or _md_caption(line):
            continue
        if re.match(r"^(图|表|算法)\s*\d", line) and len(line) < 300:
            continue
        # A line that starts in lowercase continues the block before it: a where clause after
        # a display, or a fragment split at a page or column break.
        if blocks and blocks[-1][0] == top and blocks[-1][2] == heading and CONTINUATION.match(line):
            previous = blocks[-1]
            blocks[-1] = (previous[0], previous[1], previous[2], previous[3] + " " + line)
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
    # A capital initial before a period is protected, except a subsection label such as V-A.
    # "No." is protected only before a number ("No. 5"), and a label such as Table I. or Case A.
    # ends a sentence like any other word.
    protected = re.sub(r"\bNo\.(?=\s*\d)", "No<NO>", protected)
    protected = re.sub(r"(?<!-)(?<!Table )(?<!TABLE )(?<!Section )(?<!Sections )(?<!Algorithm )(?<!Case )"
                       r"(?<!Step )\b([A-Z])\.(?=\s[A-Z])", r"\1<INI>", protected)
    # A sentence may open with a lowercase-initial name such as mEDCMOA or tDEA-CPBI.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"\u201c]|[a-z]+[A-Z])", protected)
    sentences = []
    for part in parts:
        for index, token in enumerate(PROTECT):
            part = part.replace(f"<D{index}>", ".")
        part = part.replace("<INI>", ".").replace("<NO>", ".").strip()
        if part:
            sentences.append(part)
    return sentences


# Numbers in e notation (5.83e+04) are one token, not a number and the word e.
ENOTATION = re.compile(r"\d(?:\.\d+)?[eE][+\-]?\d+")


def words(text: str) -> list[str]:
    return [token for token in WORD.findall(ENOTATION.sub(" 0 ", text)) if token != MATH]


def units(text: str, lang: str = "en") -> int:
    """Word count (English) or ideograph count (Chinese) of prose text."""
    return len(CJK.findall(text)) if lang == "zh" else len(words(text))


def sentence_length(sentence: str, lang: str = "en") -> int:
    return len(CJK.findall(sentence)) if lang == "zh" else len(WORD.findall(ENOTATION.sub(" 0 ", sentence)))


BULLET = re.compile(r"^\s*(?:[\u2022\-*]|\(\d+\)|（\d+）|\d+[.)]|[ivx]+[.)])\s+")
ITEM_MARK = "\u2063"  # marks a LaTeX \item in raw paragraphs
CONTRIBUTION_LEAD = re.compile(r"contribution|贡献", re.I)
# "1) Task Side: ..." opens a paragraph with a run-in heading (an IEEE subsubsection), not a list item.
RUN_IN = re.compile(r"^\s*\d+\)\s+[A-Z][^.:!?]{0,60}[.:]\s")


def prose_paragraphs(paragraphs: list[str], tex: bool, lang: str = "en") -> list[str]:
    """Clean prose blocks with the paragraph-counting rule of the reader contract.

    Contribution-list items count as paragraphs of their own. Any other list item joins
    the paragraph that introduces it, whatever its length.
    """
    minimum = LANGUAGES[lang]["min_paragraph"]
    kept: list[tuple[str, bool]] = []
    lead = ""
    for raw in paragraphs:
        item = raw.lstrip().startswith(ITEM_MARK) or bool(BULLET.match(raw) and not RUN_IN.match(raw))
        text = clean_tex(raw.replace(ITEM_MARK, " ")) if tex else clean_md(raw)
        if not item:
            lead = text
            kept.append((text, False))
            continue
        text = BULLET.sub("", text)
        contribution = bool(CONTRIBUTION_LEAD.search(lead))
        if contribution or not kept:
            kept.append((text, contribution))
        else:
            kept[-1] = (kept[-1][0] + " " + text, kept[-1][1])
    return [text for text, item in kept if item or units(text, lang) >= minimum]


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


MERGE_CUE = {
    "en": re.compile(r"\b(in contrast|by contrast|on the contrary|conversely|whereas)\b|^(Similarly|Likewise|It|They|Its|Their)\b", re.I),
    "zh": re.compile(r"相比之下|与之相比|与此相反|^(同样|类似地|它|它们|其|该)"),
}


def _subject_key(sentence: str, lang: str) -> str:
    """The first two words (or ideographs) after a leading connective phrase."""
    stripped = re.sub(r"^[^,，]{1,25}[,，]\s*", "", sentence.strip()) if re.match(r"^[^,，]{1,25}[,，]", sentence) else sentence
    if lang == "zh":
        return "".join(CJK.findall(stripped)[:2])
    return " ".join(w.lower() for w in WORD.findall(stripped)[:2])


def _merge_candidate(first: str, second: str, lang: str) -> bool:
    """Two adjacent short sentences that state two sides of one comparison or share a subject."""
    if MERGE_CUE[lang].search(second.strip()):
        return True
    key = _subject_key(first, lang)
    return bool(key) and key == _subject_key(second, lang)


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
    merge_pairs = []
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
        for first, second in zip(group, group[1:]):
            if ROADMAP.match(first) or ROADMAP.match(second):
                continue
            if sentence_length(first, lang) >= profile["short"] or sentence_length(second, lang) >= profile["short"]:
                continue
            if _merge_candidate(first, second, lang):
                merge_pairs.append((first, second))
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
        "merge_pairs": merge_pairs,
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


# The 90th percentile, the shares of long and short sentences, and connective rates per
# 100 sentences describe a whole paper. A measurement counts as a whole paper when at
# least three of these sections are present. One or two sections are checked against
# their section-mean bands and against connective counts; unclassified text is checked
# against the body mean and median and against connective counts.
WHOLE_PAPER_SECTIONS = ("intro", "related", "model", "method", "exp", "concl")
WHOLE_PAPER_MINIMUM = 3
COUNTED_CONNECTIVES = ("Since", "Accordingly", "Hence")

# Shares of sentences under 12 words in the four reference experiment sections, measured
# once with the current counting. A section below the lower end gets a note; the note
# threshold of other sections is 5%. Recalibration leaves these alone.
SHORT_SHARE_REFERENCE = {"exp": ("experiment", 0.065, 0.091)}

SCOPE_NOTES = {
    "paper": "whole paper; every band applies",
    "sections": (
        "one or two sections; section means and connective counts apply, while the 90th percentile, "
        "the long and short shares, and connective rates apply only to a whole paper"
    ),
    "text": "unclassified text; the body mean and median and connective counts apply",
}


def measurement_scope(result: dict[str, dict]) -> str:
    """Return 'paper', 'sections', or 'text' for a fingerprint result."""
    present = [key for key in WHOLE_PAPER_SECTIONS if key in result]
    if len(present) >= WHOLE_PAPER_MINIMUM:
        return "paper"
    if present or "future" in result:
        return "sections"
    return "text"


def _detail_keys(result: dict[str, dict]) -> list[str]:
    """Sections whose sentences are listed: every section, or the body of unclassified text."""
    keys = [key for key in result if key != "body"]
    if "body" in result and not any(key != "abstract" for key in keys):
        keys.append("body")
    return keys


def band_flags(result: dict[str, dict]) -> list[str]:
    lang = result_language(result)
    profile = LANGUAGES[lang]
    band, tolerance = profile["band"], profile["tolerance"]
    prior = " (weak prior converted from the English band)" if lang == "zh" else ""
    flags: list[str] = []
    scope = measurement_scope(result)
    body = result.get("body")
    if body is None:
        measured = [value for key, value in result.items() if key != "abstract"]
        body = measured[0] if len(measured) == 1 else None
    if body:
        names = tuple(band["body"]) if scope == "paper" else ("mean", "median") if scope == "text" else ()
        for name in names:
            low, high = band["body"][name]
            state = _status(body[name], low, high, tolerance[name])
            if state not in {"in", "near"}:
                flags.append(f"body {name} = {body[name]:.2f} is {state} (band {low}-{high}){prior}")
        if scope != "paper":
            if lang == "en":
                count = body["sentences"]
                for connective in COUNTED_CONNECTIVES:
                    used = body["initial_counts"].get(connective, 0)
                    high = band["initial_per_100"][connective][1]
                    allowed = int(high * count / 100)
                    if used > allowed:
                        flags.append(
                            f"sentence-initial {connective}: {used} in {count} sentences "
                            f"(at most {allowed} in a section of {count} sentences; the whole paper allows "
                            f"{high:g} per 100 sentences)"
                        )
        elif lang == "en":
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
                flags.append(
                    f"{section} mean sentence length = {measured['mean']:.1f} is {state} "
                    f"(band {low}-{high}, indicative; reread the section){prior}"
                )
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
    for section in _detail_keys(result):
        measured = result[section]
        for name, hits in measured["banned"].items():
            flags.append(f"{section}: {len(hits)} sentence(s) with {name}")
        if measured["short_runs"]:
            flags.append(
                f"{section}: {len(measured['short_runs'])} run(s) of three or more sentences under "
                f"{profile['short']} {unit}"
            )
        if measured.get("merge_pairs"):
            flags.append(
                f"{section}: {len(measured['merge_pairs'])} pair(s) of adjacent sentences under {profile['short']} "
                f"{unit} that could merge (two sides of one comparison, or one subject)"
            )
        if measured["repeated_openers"]:
            flags.append(
                f"{section}: {len(measured['repeated_openers'])} pair(s) of consecutive sentences open with the same connective"
            )
    return flags


def band_notes(result: dict[str, dict]) -> list[str]:
    """Measurements outside the house-style band that are not flags at this scope."""
    lang = result_language(result)
    profile = LANGUAGES[lang]
    band, tolerance, unit = profile["band"], profile["tolerance"], profile["unit"]
    notes: list[str] = []
    scope = measurement_scope(result)
    body = result.get("body")
    if body is None:
        measured = [value for key, value in result.items() if key != "abstract"]
        body = measured[0] if len(measured) == 1 else None
    if body and scope != "paper":
        judged = ("mean", "median") if scope == "text" else ()
        for name, (low, high) in band["body"].items():
            if name in judged or low <= body[name] <= high:
                continue
            if name.startswith("share"):
                near_edge = min(abs(body[name] - low), abs(body[name] - high)) < 0.01
                shown = f"{body[name]:.1%}" if near_edge else f"{body[name]:.0%}"
                span = f"{low:.0%}-{high:.0%}"
            else:
                shown, span = f"{body[name]:.1f}", f"{low:g}-{high:g}"
            notes.append(f"{name} = {shown} is outside the whole-paper band {span} (not judged below a whole paper)")
        if lang == "en":
            count = body["sentences"]
            for connective in COUNTED_CONNECTIVES:
                high = band["initial_per_100"][connective][1]
                allowed = int(high * count / 100)
                used = body["initial_counts"].get(connective, 0)
                if used and used == allowed:
                    notes.append(f"sentence-initial {connective}: {used} in {count} sentences reaches the single-section "
                                 f"limit, which is not a quota (a whole paper allows {high:g} per 100 sentences)")
    for section, (low, high) in band["section_mean"].items():
        measured = result.get(section)
        if measured and measured["sentences"] >= 5 and _status(measured["mean"], low, high, tolerance["section"]) == "near":
            notes.append(f"{section} mean sentence length = {measured['mean']:.1f} is outside the band {low}-{high}, "
                         f"within the {tolerance['section']:g}-{unit} tolerance (no flag)")
    for section, measured in result.items():
        if section in {"abstract", "concl"} or (section == "body" and scope != "text") or measured["sentences"] < 20:
            continue
        reference = SHORT_SHARE_REFERENCE.get(section) if lang == "en" else None
        if measured["share_short"] < (reference[1] if reference else 0.05):
            target = (f" (four reference {reference[0]} sections {reference[1]:.1%}-{reference[2]:.1%}; aim at "
                      "that range, not at this threshold)") if reference else ""
            notes.append(f"{section}: {measured['share_short']:.1%} of sentences under {profile['short']} {unit}"
                         f"{target}; reread whether short results and definitions were merged into long sentences")
    return notes


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
            paragraph = re.sub(r"\$[^$]*\$", " ", paragraph)  # an interval such as $[0,1]$ is not a citation
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

    def shouted_word(token: str) -> bool:
        # A capitalized heading word (RESPONSES, THE) also appears in lower case as prose.
        return token.isalpha() and token.isupper() and len(re.findall(r"\b" + token.lower() + r"\b", body)) >= 2

    report["never_defined"] = sorted(
        t for t, n in tokens.items() if n >= 2 and t not in positions and not shouted_word(t)
    )
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


# --------------------------------------------------------------------------- report


def _md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


# --------------------------------------------------------------------------- document checks

# House rules of Sections 2, 8, 9, 11, and 13 of the team house style, measured once on
# the four reference papers. Recalibration leaves them alone.
DOCUMENT_RULES = {
    "table_caption_words": 22,  # noun phrase of a result-table caption: about 20 words (reference papers 6-20)
    "table_caption_total_words": 30,  # whole caption with its note sentences: a note above this
    "title_words": 10,  # experiment subsection titles of about eight words or fewer (references average 4.3-6.7)
    "roadmap_words": 77,  # reference roadmaps 56-77 words, the supervisor-approved roadmap 46
    "this_study_intro_per_1000": (1.5, 6.4),
}

# Introduction openers of Section 9, each used at most once per paper. `To address ...,
# this study <verb>` is counted per verb: the scenario and method prompts of the
# Introduction contract are two openers.
OPENER_TEMPLATES = {
    "en": (
        ("To address this/these ...", re.compile(
            r"^To address (?:this|these|the) \w+(?: \w+)?,\s*this study (?P<verb>\w+)\b|"
            r"^To address (?:this|these|the) (?:issues?|limitations?|challenges?|problems?|gaps?|difficult(?:y|ies))\b")),
        ("Motivated by", re.compile(r"^Motivated by\b")),
        ("In this scenario", re.compile(r"^In this scenario\b")),
        ("Solving the formulated", re.compile(r"^Solving the formulated\b")),
        ("Existing ... can be categorized into", re.compile(
            r"^Existing\b.{0,80}?\b(?:categori[sz]ed|classified|divided|grouped) into\b")),
        ("The main contributions", re.compile(r"^The main contributions of this\b")),
        ("The remainder of this", re.compile(r"^The (?:remainder|rest) of this\b")),
    ),
    "zh": (
        ("为解决这一问题", re.compile(r"^为(?:了)?解决(?:这一|上述|该|此)")),
        ("在此场景下", re.compile(r"^在(?:此|该|这一)场景(?:下|中)")),
        ("本文的主要贡献", re.compile(r"^本文的主要贡献")),
        ("本文其余部分", re.compile(r"^本文其余部分")),
    ),
}

COUNT_NOUN = re.compile(
    r"\b(?:categori[sz]ed into (?:\w+ )?categor(?:y|ies)|classified into (?:\w+ )?class(?:es)?|"
    r"grouped into (?:\w+ )?groups?|divided into (?:\w+ )?divisions?)\b",
    re.I,
)
ROADMAP_START = re.compile(r"^(?:The (?:remainder|rest) of this (?:paper|study|article|work)|本文其余部分|本文后续)")
SECTION_NAME = {"en": re.compile(r"\bSections?\b"), "zh": re.compile(r"节")}
CAPTION_LABELS = {"Fig.": "figure", "Figure": "figure", "图": "figure", "TABLE": "table", "Table": "table",
                  "表": "table", "Algorithm": "algorithm", "算法": "algorithm"}
MD_CAPTION = re.compile(r"^\**\s*(Fig\.|Figure|TABLE|Table|Algorithm|图|表|算法)\s*([0-9IVX]+)\s*[.:：]?\s*\**\s*(.*)$")
REPORTING_START = re.compile(
    r"^(?:shows?|presents?|lists?|reports?|illustrates?|gives?|compares?|summari[sz]es?|depicts?|displays?|plots?|"
    r"provides?|is|are|was|were|and|to|in|of|给出|列出|展示|显示|对比|表明|中)\b|^[,，]"
)
SCALE_MEASURES = ("words", "paragraphs", "paragraph_words", "sentences", "first_paragraph_words", "last_paragraph_words")
SCALE_ITEM = re.compile(r"^(\w+)(?:\.(" + "|".join(SCALE_MEASURES) + r"))?=(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)$")


def _command_arguments(text: str, command: str) -> list[tuple[int, str]]:
    """Positions and brace-matched arguments of every \\command[opt]{arg}."""
    pattern = re.compile(r"\\" + command + r"\*?\s*(?:\[[^\]]*\])?\s*\{")
    found = []
    for match in pattern.finditer(text):
        position, depth = match.end(), 1
        while position < len(text) and depth:
            if text[position] == "{":
                depth += 1
            elif text[position] == "}":
                depth -= 1
            position += 1
        found.append((match.start(), text[match.end():position - 1]))
    return found


def tex_structure(text: str) -> tuple[list[str], list[tuple[str, int, object]]]:
    """Top-level titles and the subsection titles and float captions under each of them."""
    text = re.sub(r"(?<!\\)%.*", "", text)
    match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, flags=re.S)
    body = match.group(1) if match else text
    body = re.split(r"\\bibliography\{|\\begin\{thebibliography\}|\\appendices\b|\\appendix\b|\\begin\{IEEEbiography", body)[0]
    body = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", " ", body, flags=re.S)
    floats = [(m.start(), m.end(), m.group(1))
              for m in re.finditer(r"\\begin\{(figure|table|algorithm)\*?\}.*?\\end\{\1\*?\}", body, flags=re.S)]
    tokens = [(p, "section", a) for p, a in _command_arguments(body, "section")]
    tokens += [(p, "title", a) for name in ("subsection", "subsubsection") for p, a in _command_arguments(body, name)]
    tokens += [(p, "caption", a) for p, a in _command_arguments(body, "caption")]
    titles: list[str] = []
    events: list[tuple[str, int, object]] = []
    top: int | None = None
    for position, kind, argument in sorted(tokens, key=lambda token: token[0]):
        if kind == "section":
            titles.append(clean_tex(argument))
            top = len(titles) - 1
        elif top is not None and kind == "title":
            events.append(("title", top, clean_tex(argument)))
        elif top is not None:
            env = next((name for start, end, name in floats if start <= position < end), None)
            if env:
                events.append(("caption", top, (env, clean_tex(argument))))
    return titles, events


def _md_caption(line: str) -> tuple[str, str] | None:
    match = MD_CAPTION.match(line)
    if not match or len(line) > 400:
        return None
    rest = match.group(3).strip()
    if not rest or REPORTING_START.match(rest):
        return None
    return CAPTION_LABELS[match.group(1)], clean_md(rest.rstrip("*").strip())


def md_structure(text: str) -> tuple[list[str], list[tuple[str, int, object]]]:
    """Top-level titles and the subsection titles and captions of a Markdown source."""
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    titles: list[str] = []
    events: list[tuple[str, int, object]] = []
    top: int | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        match = re.match(r"^#+\s*(.*)$", line)
        if match:
            title = match.group(1).strip()
            sub = re.match(r"^(?:[A-H]\.|\d+\))\s+", title)
            if REFERENCES_HEADING.search(title) and not sub:
                titles.append(title)
                top = None
            elif sub:
                if top is not None:
                    events.append(("title", top, title[sub.end():]))
            elif re.match(r"^[IVX]+\.\s", title) or classify(title, strict=True):
                titles.append(title)
                top = len(titles) - 1
            continue
        caption = _md_caption(line) if top is not None else None
        if caption:
            events.append(("caption", top, caption))
    return titles, events


def _label_words(text: str, lang: str) -> int:
    """Words of a caption or heading; alphanumeric tokens such as V2X or DCMOP2 count once."""
    if lang == "zh":
        return len(CJK.findall(text))
    return len([token for token in re.findall(r"[A-Za-z][A-Za-z0-9'\-]*", text) if token != MATH])


def _strip_marker(sentence: str) -> str:
    return re.sub(r"^[\u2022\-*（(]?\s*(?:\d+[)）]|[ivx]+[)）])?\s*", "", sentence.strip())


def _caption_phrase(caption: str) -> str:
    """The noun phrase of a caption: its first sentence. Note sentences may follow it."""
    return re.split(r"(?<=[.!?])\s+(?=[`'\"(]?[A-Z])", caption.strip(), maxsplit=1)[0]


def _caption_issues(kind: str, caption: str, lang: str) -> list[str]:
    """Form checks of Section 13 of the team house style (English captions only)."""
    letters = [c for c in caption if c.isalpha()]
    if lang != "en" or not letters:
        return []
    issues = []
    count = _label_words(_caption_phrase(caption), lang)
    if kind == "table" and count > DOCUMENT_RULES["table_caption_words"]:
        issues.append(f"noun phrase of {count} words (a result-table caption runs about 20; move details to the table note)")
    if "".join(letters).isupper():
        return issues  # printed capitals (a converted PDF) carry no case or period information
    # Algorithm captions name the procedure without a final period in three reference papers and
    # in the supervisor-approved draft; figure and table captions end with a period.
    if kind == "algorithm" and caption.rstrip().endswith("."):
        issues.append("final period on an algorithm caption")
    if kind != "algorithm" and not caption.rstrip().endswith("."):
        issues.append("no final period")
    tokens = [t for t in WORD.findall(caption)[1:] if len(t) >= 4 and not _is_acronym(t)]
    capitalized = [t for t in tokens if t[0].isupper()]
    if len(capitalized) >= 3 and len(capitalized) > len(tokens) / 2:
        issues.append("title case")
    return issues


def read_terms(path: pathlib.Path) -> list[tuple[str, list[str]]]:
    """Read a term ledger: one group per line, the ledger term first (`case: instance, test instance`)."""
    groups = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        head, _, tail = line.partition(":") if ":" in line else line.partition("：")
        parts = [head] + re.split(r"[,，;；]", tail) if tail else re.split(r"[,，;；]", head)
        parts = [part.strip() for part in parts if part.strip()]
        if len(parts) >= 2:
            groups.append((parts[0], parts[1:]))
    return groups


def _term_pattern(term: str) -> re.Pattern:
    if CJK.search(term):
        return re.compile(re.escape(term))
    body = r"[\s\-]+".join(re.escape(part) for part in re.split(r"[\s\-]+", term))
    return re.compile(r"(?<![A-Za-z])" + body + r"(?:s|es)?(?![A-Za-z])", re.I)


def _term_counts(texts: dict[str, list[str]], ledger: str,
                 terms: list[str]) -> tuple[dict[str, dict[str, int]], dict[str, list[str]]]:
    """Occurrences and example sentences of each term per text.

    Longer terms are counted first and masked. A variant followed by the ledger term in
    parentheses, as in `Internet of Things devices (IoTDs)`, defines the abbreviation and
    is not counted.
    """
    patterns = {term: _term_pattern(term) for term in terms}
    definitions = {
        term: re.compile(patterns[term].pattern + r"\s*[（(]\s*" + re.escape(ledger) + r"s?\s*[)）]", re.I)
        for term in terms if term != ledger
    }
    counts: dict[str, dict[str, int]] = {term: {} for term in terms}
    examples: dict[str, list[str]] = {term: [] for term in terms}
    for key, sentences in texts.items():
        for sentence in sentences:
            text = sentence
            for term in sorted(terms, key=len, reverse=True):
                if term in definitions:
                    text = definitions[term].sub(" \x00 ", text)
                found = len(patterns[term].findall(text))
                if found:
                    counts[term][key] = counts[term].get(key, 0) + found
                    if len(examples[term]) < 3:
                        examples[term].append(sentence)
                text = patterns[term].sub(" \x00 ", text)
    return counts, examples


def parse_scale(items: list[str]) -> dict[tuple[str, str], tuple[float, float]]:
    """Parse `exp=900-1900`, `exp.paragraphs=10-19`, `related.last_paragraph_words=120-160`, and the like."""
    scale = {}
    for item in items:
        match = SCALE_ITEM.match(item.strip())
        if not match or match.group(1) not in SECTION_ORDER:
            raise ValueError(f"invalid scale item {item!r}; use SECTION[.{'|.'.join(SCALE_MEASURES)}]=LOW-HIGH")
        low, high = float(match.group(3)), float(match.group(4))
        scale[(match.group(1), match.group(2) or "words")] = (min(low, high), max(low, high))
    return scale


def _num_text(value: float) -> str:
    return f"{value:.0f}" if float(value).is_integer() else f"{value:.1f}"


def document_audit(path: pathlib.Path, result: dict[str, dict], section: str | None = None,
                   scale: dict[tuple[str, str], tuple[float, float]] | None = None,
                   terms: list[tuple[str, list[str]]] | None = None) -> dict:
    """Captions, subsection titles, roadmap, opener templates, scale, and ledger terms of one file."""
    lang = result_language(result)
    profile = LANGUAGES[lang]
    scope = measurement_scope(result)
    suffix = path.suffix.lower()
    text = read_source(path)
    if suffix == ".tex":
        titles, events = tex_structure(text)
    elif suffix in {".md", ".markdown"}:
        titles, events = md_structure(text)
    else:
        titles, events = [], []
    roles = resolve_roles(titles)

    def kept(top: int) -> bool:
        return roles[top] is not None and section in (None, roles[top])

    captions = [
        {"kind": payload[0], "section": roles[top], "text": payload[1], "words": _label_words(payload[1], lang),
         "phrase_words": _label_words(_caption_phrase(payload[1]), lang),
         "issues": _caption_issues(payload[0], payload[1], lang)}
        for kind, top, payload in events if kind == "caption" and kept(top)
    ]
    subsection_titles = [
        {"section": roles[top], "title": payload, "words": _label_words(payload, lang)}
        for kind, top, payload in events if kind == "title" and kept(top)
    ]

    sections, tex = load(path)
    prose: dict[str, list[str]] = {}
    for key, paragraphs in sections.items():
        if key != "abstract" and section in (None, key):
            prose[key] = prose_paragraphs(paragraphs, tex, lang)
    grouped = {
        key: [[s for s in split_sentences(p, lang) if sentence_length(s, lang) >= profile["min_sentence"]] for p in items]
        for key, items in prose.items()
    }
    sentences = [s for groups in grouped.values() for group in groups for s in group]

    # Opener templates are Introduction rules. Text without any section heading is read
    # whole; a file with classified sections but no Introduction is not checked.
    templates: dict[str, list[str]] | None = None
    if "intro" in grouped or scope == "text":
        opening = [s for group in grouped["intro"] for s in group] if "intro" in grouped else sentences
        templates = {}
        for label, pattern in OPENER_TEMPLATES[lang]:
            for sentence in opening:
                match = pattern.search(_strip_marker(sentence))
                if match:
                    verb = match.groupdict().get("verb")
                    templates.setdefault(f"To address ..., this study {verb}" if verb else label, []).append(sentence)
    count_nouns = [s for s in sentences if COUNT_NOUN.search(s)] if lang == "en" else []

    roadmap = None
    for group in grouped.get("intro", []):
        for index, sentence in enumerate(group):
            if ROADMAP_START.match(_strip_marker(sentence)):
                part = group[index:]
                roadmap = {
                    "words": sum(units(s, lang) for s in part),
                    "sentences": len(part),
                    "without_section": [s for s in part[1:] if not SECTION_NAME[lang].search(s)],
                }
    this_study = None
    if lang == "en" and "intro" in result and section in (None, "intro"):
        this_study = result["intro"]["inline_per_1000"].get("this study/paper", 0.0)

    scale_rows = []
    for (key, measure_name), (low, high) in (scale or {}).items():
        if section not in (None, key):
            continue
        target = key if key in result else "body" if scope == "text" and "body" in result else None
        row = {"section": key, "measure": measure_name, "low": low, "high": high, "value": None, "measured": target}
        measured = result.get(target) if target else None
        if measured:
            paragraphs = prose.get(target, [])
            if measure_name in {"words", "paragraphs", "sentences"}:
                value = float(measured[measure_name])
            elif measure_name == "paragraph_words":
                value = measured["words"] / measured["paragraphs"] if measured["paragraphs"] else 0.0
            elif measure_name == "first_paragraph_words":
                value = float(units(paragraphs[0], lang)) if paragraphs else 0.0
            else:
                value = float(units(paragraphs[-1], lang)) if paragraphs else 0.0
            row["value"] = value
        scale_rows.append(row)

    term_rows = []
    if terms:
        texts = {key: [s for p in items for s in split_sentences(p, lang)] for key, items in prose.items()}
        if section in (None, "abstract") and "abstract" in sections:
            abstract = [clean_tex(p) if tex else clean_md(p) for p in sections["abstract"]]
            texts = {"abstract": [s for p in abstract for s in split_sentences(p, lang)], **texts}
        if captions:
            texts["captions"] = [c["text"] for c in captions]
        for preferred, variants in terms:
            counts, examples = _term_counts(texts, preferred, [preferred] + variants)
            term_rows.append({"term": preferred, "variants": variants, "counts": counts, "examples": examples})

    return {
        "language": lang,
        "captions": captions,
        "titles": subsection_titles,
        "roadmap": roadmap,
        "templates": templates,
        "count_nouns": count_nouns,
        "this_study_intro_per_1000": this_study,
        "scale": scale_rows,
        "terms": term_rows,
    }


def document_flags(audit: dict) -> list[str]:
    lang = audit["language"]
    unit = LANGUAGES[lang]["unit"]
    flags: list[str] = []
    for caption in audit["captions"]:
        if caption["issues"]:
            flags.append(f"{caption['kind']} caption ({caption['section']}): {'; '.join(caption['issues'])}: "
                         f"{caption['text'][:70]}")
    if lang == "en":
        for title in audit["titles"]:
            if title["words"] >= DOCUMENT_RULES["title_words"]:
                flags.append(f"subsection title of {title['words']} words (about eight or fewer): {title['title'][:90]}")
    roadmap = audit["roadmap"]
    if roadmap:
        high = DOCUMENT_RULES["roadmap_words"] if lang == "en" else round(DOCUMENT_RULES["roadmap_words"] * ZH_RATIO[1])
        if roadmap["words"] > high:
            flags.append(f"roadmap has {roadmap['words']} {unit} in {roadmap['sentences']} sentences (at most about {high})")
        if roadmap["without_section"]:
            flags.append(f"roadmap: {len(roadmap['without_section'])} sentence(s) name no section "
                         "(one sentence per section, no content summary)")
    for label, hits in (audit["templates"] or {}).items():
        if len(hits) > 1:
            flags.append(f"opener template '{label}' starts {len(hits)} sentences (at most once per paper)")
    if audit["count_nouns"]:
        flags.append(f"{len(audit['count_nouns'])} sentence(s) repeat the verb in the count noun "
                     "('categorized into two categories')")
    value = audit["this_study_intro_per_1000"]
    if value is not None:
        low, high = DOCUMENT_RULES["this_study_intro_per_1000"]
        if value > high + 0.5:
            flags.append(f"intro uses this study/paper {value:.1f} times per 1000 words (reference Introductions {low}-{high})")
    for row in audit["scale"]:
        declared = f"{_num_text(row['low'])}-{_num_text(row['high'])}"
        name = f"{row['section']} {row['measure'].replace('_', ' ')}"
        if row["value"] is None:
            flags.append(f"{name}: section not found (declared {declared})")
        elif row["value"] > row["high"]:
            flags.append(f"{name} = {_num_text(row['value'])}, {100 * (row['value'] - row['high']) / row['high']:.0f}% "
                         f"above the declared {declared}")
        elif row["value"] < row["low"]:
            flags.append(f"{name} = {_num_text(row['value'])}, {100 * (row['low'] - row['value']) / row['low']:.0f}% "
                         f"below the declared {declared}")
    return flags + term_flags(audit["terms"])


def term_flags(rows: list[dict]) -> list[str]:
    flags = []
    for row in rows:
        for variant in row["variants"]:
            where = row["counts"][variant]
            if where:
                places = ", ".join(f"{key} {count}" for key, count in where.items())
                example = row.get("examples", {}).get(variant) or [""]
                flags.append(f"term '{variant}' appears {sum(where.values())} times ({places}); the ledger term is "
                             f"'{row['term']}'; first sentence: {example[0][:110]}")
    return flags


def document_notes(audit: dict) -> list[str]:
    """Measurements worth a look that are not flags."""
    notes = []
    for caption in audit["captions"]:
        if caption["kind"] == "table" and caption["words"] > DOCUMENT_RULES["table_caption_total_words"]:
            notes.append(f"table caption ({caption['section']}) runs {caption['words']} words in total (reference "
                         "result-table captions 6-20); put the note sentences below the table unless the document "
                         f"class has no table notes: {caption['text'][:60]}")
    for row in audit["scale"]:
        if row["value"] is not None and row["measured"] != row["section"]:
            notes.append(f"scale for {row['section']} measured on the whole text (no {row['section']} heading found)")
    if audit["templates"] is None:
        notes.append("opener templates not checked: no Introduction")
    return notes


def _document_section(audit: dict, terms_by_document: list[tuple[str, dict]]) -> list[str]:
    """Markdown lines of the document-check section of the report."""
    unit = LANGUAGES[audit["language"]]["unit"]
    out = ["**Captions**", ""]
    out += [
        f"- {c['kind']} ({c['section']}, {c['words']} {unit}"
        + (f", noun phrase {c['phrase_words']}" if c["phrase_words"] != c["words"] else "")
        + f"): {_md_cell(c['text'][:160])}"
        + (f" **[{'; '.join(c['issues'])}]**" if c["issues"] else "")
        for c in audit["captions"]
    ] or ["- none found"]
    out += ["", "**Subsection titles**", ""]
    out += [f"- {t['section']} ({t['words']} {unit}): {_md_cell(t['title'])}" for t in audit["titles"]] or ["- none found"]
    roadmap = audit["roadmap"]
    out += ["", "**Roadmap**", ""]
    out.append(f"- {roadmap['words']} {unit} in {roadmap['sentences']} sentences" if roadmap else "- not found")
    out += ["", "**Opener templates**", ""]
    if audit["templates"] is None:
        out.append("- not checked: no Introduction")
    else:
        out += [f"- {label}: {len(hits)}" for label, hits in audit["templates"].items()] or ["- none"]
    if audit["scale"]:
        out += ["", "**Declared scale**", ""]
        for row in audit["scale"]:
            value = "not found" if row["value"] is None else _num_text(row["value"])
            out.append(f"- {row['section']} {row['measure'].replace('_', ' ')}: {value} "
                       f"(declared {_num_text(row['low'])}-{_num_text(row['high'])})")
    if terms_by_document:
        out += ["", "**Ledger terms**", "", "| Document | Term | Ledger term? | Occurrences |", "|---|---|---|---|"]
        examples = []
        for name, document in terms_by_document:
            for row in document["terms"]:
                for term in [row["term"]] + row["variants"]:
                    where = row["counts"][term]
                    places = ", ".join(f"{k} {v}" for k, v in where.items()) or "0"
                    out.append(f"| {_md_cell(name)} | {_md_cell(term)} | {'yes' if term == row['term'] else 'no'} | {places} |")
                    if term != row["term"]:
                        examples += [f"- {name}, '{term}': {_md_cell(s[:160])}" for s in row["examples"][term]]
        if examples:
            out += ["", "Sentences with a non-ledger variant (read each one; a variant must name the same concept):", ""]
            out += examples
    return out


def submission_report(paths: list[pathlib.Path], lang: str = "auto", sentences_per_item: int = 5,
                      scale: dict[tuple[str, str], tuple[float, float]] | None = None,
                      terms: list[tuple[str, list[str]]] | None = None) -> str:
    """Return a Markdown pre-submission report.

    The first path is the main manuscript: it gets the full fingerprint, flags, banned
    constructions, short runs, the document checks (captions, subsection titles,
    roadmap, opener templates, declared scale), the paragraph-opening spine, and
    repeated citations. Every path enters the abbreviation audit and the ledger-term
    check, and every further path (supplement, response letter) gets its own
    banned-construction counts.
    """
    main = paths[0]
    result = fingerprint(main, lang)
    audit = document_audit(main, result, scale=scale, terms=terms)
    terms_by_document = [(main.name, audit)] if terms else []
    used = result_language(result)
    profile = LANGUAGES[used]
    unit = profile["unit"]
    out: list[str] = [f"# Pre-submission report: {main.name}", ""]
    out.append(
        f"Language: {used}; lengths in {unit}. Every item is a lead to read, not a verdict. "
        "Pasted reviewer comments and quoted titles are exempt from the banned constructions."
    )
    out.append("")
    out.append(f"Scope: {SCOPE_NOTES[measurement_scope(result)]}.")
    missing = MISSING_INCLUDES.get(str(main.resolve().parent), []) if main.suffix.lower() == ".tex" else []
    if missing:
        out.append("")
        out.append("Included files not found and skipped: " + ", ".join(sorted(set(missing))) + ".")

    out += ["", "## 1. Section scale and sentence rhythm", ""]
    out.append(f"| Section | Paragraphs | {unit.capitalize()} | Sentences | Mean | Median | P90 | Over {profile['long']} | Under {profile['short']} |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for key in SECTION_ORDER + tuple(k for k in result if k not in SECTION_ORDER):
        if key in result:
            m = result[key]
            out.append(
                f"| {key} | {m['paragraphs']} | {m['words']} | {m['sentences']} | {m['mean']:.1f} | {m['median']:.0f} | "
                f"{m['p90']:.0f} | {m['share_long']:.0%} | {m['share_short']:.0%} |"
            )

    out += ["", "## 2. Flags against the house-style band", ""]
    flags = band_flags(result) + document_flags(audit)
    out += [f"- {flag}" for flag in flags] or ["- none"]
    notes = band_notes(result) + document_notes(audit)
    if notes:
        out += ["", "Notes (not flags):", ""] + [f"- {note}" for note in notes]

    out += ["", "## 3. Banned constructions", ""]
    any_banned = False
    for key in _detail_keys(result):
        m = result[key]
        for name, hits in m["banned"].items():
            any_banned = True
            out.append(f"- **{key}, {name}** ({len(hits)})")
            out += [f"  - {_md_cell(sentence[:200])}" for sentence in hits[:sentences_per_item]]
    if not any_banned:
        out.append("- none")

    out += ["", "## 4. Over-splitting signals", ""]
    any_run = False
    for key in _detail_keys(result):
        m = result[key]
        for run in m["short_runs"][:sentences_per_item]:
            any_run = True
            out.append(f"- **{key}**, short run: " + " / ".join(_md_cell(s[:80]) for s in run))
        for first, second in m["merge_pairs"][:sentences_per_item]:
            any_run = True
            out.append(f"- **{key}**, merge candidate: {_md_cell(first[:100])} / {_md_cell(second[:100])}")
        for opener, sentence in m["repeated_openers"][:sentences_per_item]:
            any_run = True
            out.append(f"- **{key}**, two sentences open with {opener}: {_md_cell(sentence[:120])}")
    if not any_run:
        out.append("- none")

    if terms:
        for path in paths[1:]:
            terms_by_document.append((path.name, document_audit(path, fingerprint(path, lang), terms=terms)))
    out += ["", "## 5. Captions, subsection titles, roadmap, and templates", ""]
    out += _document_section(audit, terms_by_document)

    out += ["", "## 6. Paragraph-opening sentences", ""]
    out.append("Read this list on its own: it should state the argument of each section in order.")
    number = 0
    for entry in spine(main, used):
        out += ["", f"**[{entry['section']}] {_md_cell(entry['heading'])}**", ""]
        for opener in entry["openers"]:
            number += 1
            out.append(f"{number}. {_md_cell(opener)}")

    out += ["", "## 7. Citations repeated within a section", ""]
    reuse = citation_reuse(main)
    out += [f"- {section}: " + ", ".join(f"{k} x{v}" for k, v in keys.items()) for section, keys in reuse.items()] or ["- none"]

    out += ["", "## 8. Abbreviations", ""]
    audit = abbreviation_audit(paths)
    labels = (
        ("used_before_definition", "used before the first definition"),
        ("defined_more_than_once", "defined more than once"),
        ("rarely_used", "defined but used at most once afterwards"),
        ("abstract_undefined", "used in the abstract without a local definition"),
        ("never_defined", "used repeatedly without a definition"),
    )
    for document in audit["documents"]:
        out.append(f"- **{document['document']}**")
        for key, label in labels:
            if document[key]:
                out.append(f"  - {label}: {', '.join(document[key])}")
    if len(paths) > 1:
        if audit["long_form_mismatches"]:
            for abbr, docs in audit["long_form_mismatches"].items():
                out.append(f"- {abbr} has different long forms: " + "; ".join(f"'{form}' ({doc})" for doc, form in docs.items()))
        else:
            out.append("- every abbreviation has one long form across the documents")

    if len(paths) > 1:
        out += ["", "## 9. Further documents", ""]
        for path in paths[1:]:
            other = fingerprint(path, lang)
            keys = [k for k in other if k != "body"] or ["body"]
            letter = bool(re.search(r"reply|response|rebuttal|letter", path.stem, re.I))
            counts: Counter[str] = Counter()
            for key in keys:
                for name, hits in other[key]["banned"].items():
                    if letter and name.startswith(("we/our", "我们")):
                        continue  # a response letter keeps the first person
                    counts[name] += len(hits)
            summary = ", ".join(f"{name} {count}" for name, count in counts.most_common()) or "none"
            out.append(f"- **{path.name}**: banned constructions: {summary}")
            for name, document in terms_by_document[1:]:
                if name == path.name:
                    out += [f"  - {flag}" for flag in term_flags(document["terms"])]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- output


def _print_fingerprint(path: pathlib.Path, result: dict[str, dict], only: str | None, audit: dict | None = None) -> None:
    write = sys.stdout.write
    lang = result_language(result)
    profile = LANGUAGES[lang]
    unit = profile["unit"]
    write(f"Style fingerprint: {path.name} (language: {lang}; lengths in {unit})\n")
    checked = result if not only or only == "body" else {only: result[only]} if only in result else {}
    write(f"Scope: {SCOPE_NOTES[measurement_scope(checked)]}.\n\n")
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
    flags = band_flags(checked)
    write("\nFlags against the team house-style band:\n")
    if not flags:
        write("  none\n")
    for flag in flags:
        write(f"  - {flag}\n")
    for key in _detail_keys(checked):
        m = checked[key]
        for name, hits in m["banned"].items():
            for sentence in hits[:3]:
                write(f"    [{key}] {name}: {sentence[:160]}\n")
        for run in m["short_runs"][:2]:
            write(f"    [{key}] short run: {' | '.join(s[:60] for s in run)}\n")
        for first, second in m["merge_pairs"][:2]:
            write(f"    [{key}] merge candidate: {first[:70]} | {second[:70]}\n")
        for opener, sentence in m["repeated_openers"][:2]:
            write(f"    [{key}] repeated opener {opener}: {sentence[:120]}\n")
    if audit is not None:
        write("\nDocument checks (captions, subsection titles, roadmap, templates, scale, terms):\n")
        document = document_flags(audit)
        if not document:
            write("  none\n")
        for flag in document:
            write(f"  - {flag}\n")
        notes = band_notes(checked) + document_notes(audit)
        if notes:
            write("\nNotes (not flags):\n")
            for note in notes:
                write(f"  - {note}\n")
        for label, hits in (audit["templates"] or {}).items():
            if len(hits) > 1:
                for sentence in hits[:3]:
                    write(f"    [{label}] {sentence[:140]}\n")
        for sentence in audit["count_nouns"][:3]:
            write(f"    [count noun] {sentence[:140]}\n")


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
        "--report",
        action="store_true",
        help="Write a Markdown pre-submission report: main manuscript first, then supplement and letter",
    )
    parser.add_argument("--out", type=pathlib.Path, help="With --report, write the report to this file")
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
    parser.add_argument(
        "--scale",
        nargs="+",
        metavar="SECTION[.MEASURE]=LOW-HIGH",
        help="Declared scale ranges to check: SECTION[.words|.paragraphs|.paragraph_words|.sentences|"
             ".first_paragraph_words|.last_paragraph_words]=LOW-HIGH, such as exp=900-1900 exp.paragraphs=10-19",
    )
    parser.add_argument(
        "--terms",
        type=pathlib.Path,
        help="Term ledger: one group per line, the ledger term first (case: instance, test instance)",
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
    try:
        scale = parse_scale(args.scale) if args.scale else None
    except ValueError as error:
        parser.error(str(error))
    if args.terms and not args.terms.is_file():
        parser.error(f"term ledger not found: {args.terms}")
    terms = read_terms(args.terms) if args.terms else None
    if args.report:
        report = submission_report(args.paths, args.lang, scale=scale, terms=terms)
        if args.out:
            args.out.write_bytes(report.encode("utf-8"))
            sys.stdout.write(f"Report written to {args.out}\n")
        else:
            sys.stdout.write(report)
        return 0
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
    audit = document_audit(args.path, result, section=args.section if args.section != "body" else None,
                           scale=scale, terms=terms)
    if args.json:
        json.dump(
            {
                "language": result_language(result),
                "scope": measurement_scope(result),
                "sections": result,
                "flags": band_flags(result),
                "document": audit,
                "document_flags": document_flags(audit),
                "notes": band_notes(result) + document_notes(audit),
            },
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
    else:
        _print_fingerprint(args.path, result, args.section, audit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

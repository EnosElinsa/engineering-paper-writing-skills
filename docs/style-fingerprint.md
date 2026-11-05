# Style fingerprint script

`style_fingerprint.py` measures a manuscript against the [house style](house-style.md) and lists the sentences behind every flag. It uses only the Python standard library (Python 3.10 or later). The canonical source is `shared/scripts/style_fingerprint.py`, and every skill carries a copy at `scripts/style_fingerprint.py`, so an agent runs it from the installed skill directory.

A flag is a measurement, not a verdict. Read every flagged sentence before changing it: a long sentence may be a necessary list, and a short one may be a result.

## Contents

1. [Inputs](#inputs)
2. [Measurement scope](#measurement-scope)
3. [Default output](#default-output)
4. [Options](#options)
5. [Counting rule](#counting-rule)
6. [Examples](#examples)
7. [JSON output](#json-output)

## Inputs

- **LaTeX** (`.tex`). Pass the root file: `\input`, `\include`, `\subfile`, and `\import` files are inlined, and missing ones are reported.
- **Markdown** (`.md`), such as a PDF converted to Markdown, with `#` headings and one paragraph per line.
- **Plain text** (`.txt`) with blank-line paragraphs.

Section roles (abstract, Introduction, Related Work, model, method, experiments, Conclusion) come from the headings. A section that names no role but lies between the model and the experiments is read as the method. English and Chinese are detected automatically, and `--lang en|zh` forces one. A Chinese manuscript is measured in ideographs against the weak-prior band of the Chinese adapter.

## Measurement scope

| Scope | When | What is checked |
|---|---|---|
| Whole paper | At least three of the Introduction, Related Work, model, method, experiments, and Conclusion | Every band, including the 90th percentile, both shares, and connective rates per 100 sentences |
| Sections | One or two of those sections | Section-mean bands and connective counts (`Since` and `Accordingly` once per full 100 sentences of the section, `Hence` never) |
| Text | No recognized section heading | Body mean and median and connective counts |

Measures that do not apply at the current scope are listed as notes, not flags.

## Default output

- Section scale: paragraphs, words, sentences, and the sentence-length profile (mean, median, 90th percentile, shares over 35 and under 12 words).
- Sentence-initial connectives per 100 sentences and within-sentence features per 1000 words.
- Flags against the band, each banned construction with its sentences, runs of three short sentences, adjacent short sentences that could merge, and consecutive sentences that open with the same connective.
- Document checks: figure and table captions without a final period or in title case, an algorithm caption with a final period, a result-table noun phrase over 22 words, subsection titles of ten or more words, a roadmap over 77 words or with a sentence that names no section, an Introduction opener used more than once, a count noun that repeats its verb (`categorized into two categories`), and more than 6.9 uses of `this study` per 1000 words in the Introduction.
- Notes, which are not flags: whole-paper measures on a single section, a section mean outside its band but inside the 3-word tolerance, a short-sentence share below the threshold (experiments below the reference range of 6.5%–9.1%, other sections below 5%), a single-section connective count at its limit, and a table caption over 30 words with its note sentences.

## Options

| Option | Effect |
|---|---|
| `--section ROLE` | Report one section (`abstract`, `intro`, `related`, `model`, `method`, `exp`, `future`, `concl`, or `body`) |
| `--lang auto\|en\|zh` | Manuscript language (default `auto`) |
| `--scale SECTION[.MEASURE]=LOW-HIGH ...` | Check the ranges of the scale statement. Measures: `words` (default), `paragraphs`, `paragraph_words`, `sentences`, `first_paragraph_words`, `last_paragraph_words`. A file without headings is measured as a whole |
| `--terms LEDGER` | Read a term ledger, one group per line with the ledger term first (`case: instance, test instance`), and report every other variant with its count per section, in the abstract, and in captions, with the sentences that use it. Longer terms are matched first, and a long form followed by its abbreviation (`Internet of Things devices (IoTDs)`) is not counted |
| `--citations` | List citation keys repeated within a section |
| `--spine` | Print the opening sentence of every paragraph under its heading, so the chain of paragraph centers can be read on its own (combine with `--section`) |
| `--abbrev FILE ...` | Audit abbreviations in each document (used before definition, defined twice, rarely used, undefined in the abstract, never defined) and compare long forms across the manuscript, supplement, and letter |
| `--report MAIN [SUPP LETTER] --out FILE` | Write one Markdown pre-submission report with all of the above, the abbreviation and term checks across documents, and banned-construction counts for the supplement and letter (the letter keeps its first person) |
| `--diff OLD NEW [--show N]` | Classify the edits between two versions into merges, splits, rewrites, insertions, and deletions, and compare sentence length and connectives in the changed sentences |
| `--json` | Print machine-readable output |

## Counting rule

The rule follows protocols S and R of the reader and terminology contract.

- Displayed equations, figures, tables and their notes, algorithms, captions, and headings are excluded. Citations are removed, and a cross-reference counts as one word.
- A paragraph is a prose block of at least 20 words (30 ideographs in Chinese). Contribution items count as paragraphs. Other list items, and the `where` clause after a display, join the paragraph that introduces them. A line that starts with a lowercase word continues the block before it, which repairs page and column breaks in converted PDFs.
- Sentences split at final punctuation before a capital letter or a lowercase-initial name such as `mEDCMOA`. `et al.`, `Fig.`, `Eq.`, `e.g.`, `i.e.`, and similar abbreviations are protected, and `No.` only before a number. Fragments under four words (five ideographs) are run-in labels, not sentences.
- Inline math is excluded from word counts and counts as one word in sentence lengths. A number in e notation is one token.

## Examples

```bash
# Whole paper, with the scale statement and the term ledger
python scripts/style_fingerprint.py paper/main.tex --scale exp=1030-1888 exp.paragraphs=11-18 --terms ledger.txt

# One section and its paragraph-opening sentences
python scripts/style_fingerprint.py draft.md --section exp
python scripts/style_fingerprint.py draft.md --spine --section intro

# Pre-submission report across the manuscript, supplement, and response letter
python scripts/style_fingerprint.py --report main.tex supplement.tex reply.tex --terms ledger.txt --out report.md

# What a co-author's edits changed
python scripts/style_fingerprint.py --diff before.tex after.tex --show 10
```

## JSON output

`--json` prints an object with:

- `language` and `scope`;
- `sections`: per-section measurements, banned constructions with their sentences, short runs, merge pairs, and repeated openers;
- `flags`: band flags;
- `document` and `document_flags`: the document checks;
- `notes`: measurements that are not flags.

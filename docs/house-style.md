# House style

The house style records the measured writing conventions of the author team that calibrated these skills. The section skills, `write-abstracts-and-conclusions`, and `latex-prose-audit` apply it by default unless the user names another venue or team style.

## Contents

1. [Files](#files)
2. [What it fixes](#what-it-fixes)
3. [Where the numbers come from](#where-the-numbers-come-from)
4. [The sentence-rhythm band](#the-sentence-rhythm-band)
5. [Blind evaluations](#blind-evaluations)
6. [Recalibrating](#recalibrating)

## Files

| File | Role |
|---|---|
| [`shared/styles/house-style-card.md`](../shared/styles/house-style-card.md) | The short card that every skill reads by default (about 1,000 words) |
| [`shared/styles/team-house-style.md`](../shared/styles/team-house-style.md) | The full file: measured tables, rules, attested openers and caption forms, and provenance |
| [`shared/languages/zh.md`](../shared/languages/zh.md) | Chinese counterparts of the sentence rules and a weak-prior band in ideographs |

The card ends with a table that names the sections of the full file to read for each task, so a skill reads the full file only in part.

## What it fixes

- **Author voice.** `this study` or the passive for author actions, `we` only in future work, and `this study` reserved for the contribution items, scenario and algorithm sentences, the roadmap, and the opening of the Conclusion.
- **Banned constructions.** `because`, `so`, `, but` between clauses, semicolons, `e.g.` in running prose, `Hence`, promotional modifiers, and a few others, each with its replacement.
- **Sentence rhythm.** A band for mean sentence length, its spread, and the shares of long and short sentences, plus rules for merging over-split sentences before cutting content.
- **Connectives.** Measured rates per 100 sentences, with hard limits for `Since`, `Accordingly`, and `Hence`.
- **Structure.** Section and subsection titles, attested paragraph openers, the title, abstract, index terms, contribution list, roadmap, Conclusion, captions, and equation lead-ins.

## Where the numbers come from

The band and the structural defaults were measured on the complete text of four IEEE Transactions papers by the author team, all constrained or dynamic constrained multi-objective evolutionary approaches to UAV or edge-computing systems. Supervisor practice comes from before-and-after sentence diffs of two rounds of supervisor edits on a later journal revision by the same team. When the two sources disagree, the order is: explicit author rules, recurring supervisor practice, a pattern in at least two reference papers, then a single paper. The full file names the reference-paper habits that are deliberately not imitated, such as promotional modifiers and first person in the body.

Thirteen further published papers (five from the same research line, eight reinforcement-learning MEC papers) serve as a validation set. They do not set the band.

The papers themselves are copyrighted and are not distributed. The repository holds only measurements, short stock phrases, and synthetic examples.

## The sentence-rhythm band

The body and section bands follow the four papers. A blind evaluation compared this band with one widened to include the supervisor-approved draft, which writes shorter sentences (body mean 20.4 words against 23.2–24.8). The widened band moved drafts away from the reference papers without restoring their share of short sentences, so the author kept the four-paper band. The supervisor-approved draft is still shown in the rhythm table for comparison, and its abstract and Conclusion values widen those two bands.

The 90th percentile, the long and short shares, and the connective rates describe a whole paper. One or two sections are checked against their section means and connective counts. The counting rule is stated in the reader and terminology contract and implemented by the [fingerprint script](style-fingerprint.md).

## Blind evaluations

Three rounds of blind evaluation drafted sections of the four reference papers from fact sheets, with no access to the original text, and compared the drafts with the originals. The drafts and fact sheets are kept outside the repository.

| Round | Compared | Main outcome |
|---|---|---|
| 1 | skills before and after the house style | Banned constructions fell from 81 and 53 sentences (Introductions, experiments) to 0, and the Introduction rhythm moved toward the originals. Subsection titles, captions, and template reuse needed work. |
| 2 | after the first fixes, two drafts per cell | Result-table captions and subsection titles reached the reference lengths, and term drift disappeared. Experiment sections lost almost all short sentences, table notes moved into captions, and one sentence-initial `Since` per section became a habit. |
| 3 | four-paper band against a widened band | Table notes returned below the tables and split comparisons were merged. Short sentences recovered only partly. The four-paper band kept drafts closer to the originals. |

Each round ended with proposed edits, which were applied and then re-tested on the cells that had regressed.

## Recalibrating

When the team publishes another paper of this family, add it to the reference set and regenerate the band:

```bash
python scripts/calibrate_house_style.py --references path/to/reference-papers \
    --approved path/to/supervisor-approved.tex --baseline path/to/approved-baseline.tex \
    --abstract-limit 250 --validate "LABEL=path/to/validation-papers" --check
python scripts/calibrate_house_style.py ... --write
python scripts/sync_shared.py
```

- The tool measures every paper with the fingerprint script and proposes each range as the minimum to maximum over the reference papers.
- `--approved` drafts widen only the abstract and Conclusion ranges and appear in a comparison column. `--baseline` fills the last column of the rhythm table. `--abstract-limit` sets the upper end of the abstract word range.
- `--validate "LABEL=PATH" ...` measures papers that do not set the band and records which measures fall outside it.
- `--check` exits non-zero when the proposed band differs from the shipped one. `--write` rewrites the generated blocks (the band literal in the script, the rhythm and validation tables of the house style, the rhythm lines of the card, and the Chinese weak-prior tables) and lists the prose that still needs review.
- Connective limits, document-check limits, and the reference short-sentence share are house rules outside the generated blocks and are never recalibrated automatically.
- Any change to how the script counts paragraphs or sentences changes the reference measurements. Run `--check` afterwards, and re-measure the script-count tables in the `mec.md` domain packs.

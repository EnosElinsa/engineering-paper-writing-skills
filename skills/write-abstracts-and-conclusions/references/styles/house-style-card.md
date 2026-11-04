# Team house style: quick card

The short version of [the full team house style](team-house-style.md). Read this card by default. Read the full file only for the sections that the table at the end names for the task. Where a generic example sentence in a skill differs from the card, follow the card.

## Voice

- Author actions take `this study` or the passive (`This study formulates ...`, `... is formulated as ...`). Use `we` only in future-work sentences of the Conclusion, and never `our`. A response letter keeps the first person.
- Reserve `this study` for the contribution items, the scenario and algorithm sentences of the Introduction, the roadmap, and the opening of the Conclusion. Elsewhere, use the passive or make the algorithm or an actor the subject.
- In running prose the method is `the proposed algorithm` (or `the proposed mechanism` for a component). Use its acronym where it is compared with baselines by name.
- An algorithm or a modeled actor (controller, platform, vehicle, server) acts. A mechanism, constraint, equation, metric, section, table, or figure does not decide, ensure, guarantee, validate, or explain; a table or figure only presents, reports, or shows.

## Banned in author prose

`because`, `so`, `so that`, `so as to`, `, but` between clauses, semicolons, a colon joining two clauses, `, and` joining two independent claims, `e.g.` in running prose, `Hence`, `we` or `our` outside future work, dangling modifiers, `no existing study considers ...`, and the promotional words `superior`, `critical`, `fundamental`, `crucial`, `essential`, `promising`, `comprehensive`, `remarkable`, `novel`, and `state-of-the-art` (`significant` only with a named test). When `because` or `so` goes, the cause stays, as a `since` or `due to` clause or as the subject of its own sentence.

## Rhythm

<!-- calibrate:begin card -->
- Body: mean sentence length 21.4–23.8 words, median 20–22, 90th percentile 32–37, 7%–13% of sentences over 35 words, 9%–14% under 12 words.
- Section means (indicative): Abstract 24.8–30.5, Introduction 19.8–23.6, Related Work 21.3–26.3, System Model and Problem Formulation 20.8–23.2, Proposed algorithm 19.7–25.5, Experimental studies 22.1–24.5, Conclusion 24.2–28.0 words.
- Abstract 210–250 words in 7–10 sentences; Conclusion 165–280 words in 6–10 sentences.
<!-- calibrate:end card -->
- A Chinese manuscript uses the weak-prior band of the Chinese manuscript adapter instead.
- Below the band means over-split: merge before cutting. Never write three sentences under 12 words in a row, and merge two adjacent short sentences that state two sides of one comparison or share a subject.
- The 90th percentile and the two shares apply to a whole paper. Check one section alone against its section mean only, and do not split the definition or list sentences of a settings subsection to move a share.
- Report a remaining flag and its reason in the delivery note, never in the manuscript.

## Merge, then split

Keep in one sentence: the direct consequence of the same action (`, thereby altering ...` or a participle with the same subject), the two sides of one comparison (`while`, `whereas`), a short cause (`Due to ...`, `Since ...`, `As ...`), a purpose (`To ...`), a definition (`, where ...`, `namely`), members or examples (`including`, `such as`), and a `which` clause with one possible antecedent.

Split only a second independent claim: two claims joined by `, and`, a participle that adds a fact with another subject, a `which` with two possible antecedents, or a sentence over about 40 words that carries two claims.

## Connectives

At most one sentence-initial `Since` and one `Accordingly` per 100 sentences, and no `Hence`. These are rates over a whole paper. On one section alone, allow one of each per 100 sentences of the section, at least one, and check `However` and `To address` only over the whole paper. Rotate `Therefore`, `Consequently`, `As a result`, and `Thus`. Use `However` only for a real contrast, `For example` where a general claim needs a case, and never open two consecutive sentences with the same connective. Recount after any splitting pass.

## Structure defaults

- Section titles: `Introduction`, `Related Work`, `System Model and Problem Formulation`, `Proposed Algorithm`, `Experimental Studies`, `Conclusion`. An experiment subsection title names the operation and the object in about eight words (`Overall Performance Comparison`, `Investigation of the <mechanism>`). The varied factor goes in the title when it fits, otherwise in the opening sentence.
- Openers: use each Introduction opener of the full file at most once per paper, and only in a paragraph that already has its function.
- Contribution list: two or three items opening with `This study ...`, in the order scenario or model, formulation, algorithm; only the last item carries one scoped result sentence.
- Roadmap: one sentence per section, 56–77 words in total, and no summary of section content.
- Abstract: one paragraph; setting, limiting assumption and its cost, scenario, formulation, algorithm, and a result with numbers, scope, and the range over the best-performing baseline.
- Conclusion: restate the problem, summarize each experiment group in order with its scope, and end with a future-work chain tied to stated limitations.
- Captions: a noun phrase in sentence case with a final period that names the compared objects, instances, and run rule in the manuscript's own terms. A result-table caption stays near 20 words, and metric names, run counts, and significance rules go in the table note. A display is introduced by a clause that names the quantity and ends with a colon (`... is calculated as follows:`).

## When to read the full house style

| Task | Sections of the full file |
|---|---|
| Drafting a section from scratch | 8 (titles) and 9 (paragraph openers for that section) |
| Merging or splitting after a fingerprint flag | 3 (band), 4 (combining and splitting), 5 (connectives) |
| Title, abstract, index terms, contribution list, roadmap, Conclusion | 10, 11, 12 |
| Captions, tables, and equation lead-ins | 13 |
| Running the fingerprint script | 14 |
| Checking where a number or rule comes from | 15 |

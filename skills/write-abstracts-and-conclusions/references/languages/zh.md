# Chinese manuscript adapter

Read this file when the manuscript is written in Chinese. It adds language rules to the section contract and to the reader and terminology contract. It never replaces them, and it is a language layer, not a domain pack.

## Register

Author rules. The manuscript owner decided these; apply them as written. [G-ZH-reg]

- Avoid 把 in definitions and mechanism descriptions. Use 将 or 对, or put the actor in the subject position.
- Avoid 让 as a causative. Use 使, or restructure the sentence.
- Avoid the pattern 一边…一边…. Use 同时 or 并.
- Do not define a coined term with a bare parenthetical. State its function in the sentence, then name it (contract rule T2). The abbreviation form under Terminology stays allowed.

Review defaults, edit to taste. The review author extrapolated these from the rules above, so the manuscript owner may delete or change any of them.

- Avoid 其实, 挺, 非常, and 很, and avoid 比较 as a degree adverb (the verb in 与…比较 is fine). State a measured claim or delete the word.
- Avoid 的话 as a conditional marker. Use 若 or 当.

Keep one core causal relation per sentence. Use the written academic register throughout.

## Sentences

Author rules, applied as written. They are the Chinese counterparts of the team house style's author voice, connective, and banned-construction rules. [G-ZH-sent]

- Give every sentence an explicit subject. A mechanism step names its actor (the controller, the algorithm, the UAV) or uses 本文 for an author action.
- Use 本文 for author actions, and reserve it for the contribution items, the scenario and algorithm sentences of the Introduction, the roadmap, and the opening of the Conclusion. Elsewhere, make the algorithm or a system actor the subject. Do not use 我们 outside future-work sentences.
- Do not put a colon inside a prose sentence. A colon may end a lead-in to a list (`……如下：`) or to a display, and it may follow the run-in label of a list item.
- Do not write meta-language or self-summary sentences that announce a move instead of making it, such as `解决这一问题的直接思路是……` or a bare `上述两点在该场景中均不成立。` State the fact and let the contrast stay implicit.
- 可见 and 据此 are not connectives. State the result directly, or use 因此 when the sentence follows from the previous one.
- Rotate the result connectives. A sentence-initial 因此 alternates with 由此 and 因而, and a direct consequence of the same action folds into the clause with 从而 or 进而 (the counterpart of `, thereby`). Do not open two consecutive sentences with the same connective.
- Merge before splitting, as in the house style: keep the two sides of one comparison together with `，而`, a definition with `，其中`, a short cause with 由于, and a purpose with 为 or 为了. Do not replace every split with a new sentence that opens with 因此.

## Sentence rhythm (weak prior)

No Chinese reference paper by the team is available. The band below converts the house-style English band with the default ratio of this adapter, 1.5 to 2.0 ideographs per English word: lower ends are multiplied by 1.5 and upper ends by 2.0. The short and long thresholds use the midpoint ratio 1.75. Shares, sentence counts, and paragraph counts transfer unchanged. Treat a value outside the band as a reason to read the section again, not as a defect. As in the house style, the 90th percentile and the two shares apply to a whole paper, and one section alone is checked against its section mean. Replace this band with a measured one as soon as a Chinese reference paper by the team exists. [G-ZH-rhythm]

<!-- calibrate:begin zh-rhythm -->
| Body measure | Weak-prior band |
|---|---|
| Mean sentence length (ideographs) | 31–50 |
| Median | 28–46 |
| 90th percentile | 50–78 |
| Share of sentences over 61 ideographs | 7%–15% |
| Share of sentences under 21 ideographs | 9%–19% |

| Section | Mean sentence length band (ideographs) |
|---|---|
| Abstract | 37–61 |
| Introduction | 30–47 |
| Related Work | 32–53 |
| System Model and Problem Formulation | 30–54 |
| Proposed algorithm | 29–54 |
| Experimental studies | 31–49 |
| Conclusion | 36–56 |

The abstract converts to 315–500 ideographs and the Conclusion to 248–560 ideographs. A venue's own limit overrides both.
<!-- calibrate:end zh-rhythm -->

Counting rule: CJK ideographs only (see Scale conversion), sentences split after `。`, `？`, and `！`, fragments under five ideographs dropped, and paragraphs of at least 30 ideographs. Run the bundled fingerprint script with `--lang zh` (or let `--lang auto` detect the language) to measure a draft.

## Punctuation

- Use full-width punctuation in running prose. [G-ZH-punct]
- Do not use the full-width semicolon in running prose. Split the sentence, or enumerate with 首先 and 其次. Tables and formula contexts are exempt.
- Use half-width punctuation inside formulas, identifiers, and numbers with units.
- Keep the manuscript's existing spacing convention between Chinese and Latin text.

## Terminology

- Anchor each term on the wording of the closest cited papers. Record one Chinese rendering per term in the term ledger (contract rule T5) and use it everywhere. Do not render one English root as both a process noun and a role noun unless the ledger fixes the pair (rule T3). [G-ZH-term]
- At first use write 中文名（English full name, ABBR）, then use one form only. This is the abbreviation exception to rule T2. A coined concept still needs its function stated first.
- In an Introduction, name a decision or objective with a verb phrase and a purpose clause, not with a coined Chinese compound (rule T4).

## Scale conversion

- Default: 1.5 to 2.0 Chinese characters per English word of prose. Multiply both ends of the declared word range by these factors. Sentence counts and paragraph counts transfer unchanged. [G-ZH-scale]
- Calibrate on one translated reference paragraph before relying on the default. Record the measured ratio in the scale statement.
- Count characters as CJK ideographs only. Exclude punctuation, citation numbers, inline formulas, and spaces.

## Citations and claims

- Number references by first appearance across the whole manuscript, and reuse a number for the same source. [G-ZH-cite]
- Avoid unsupported universals such as 所有, 均, 任何, 完全, 必然, 显然, and 众所周知. Prefer bounded wording such as 在所综述的研究中 (contract claim types).
- Write only verified facts. Every sentence must be readable without later sections (contract rules A and Q).

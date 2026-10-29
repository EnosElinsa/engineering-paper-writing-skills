# Response contract and quality gates

## Contents

1. [Comment ledger](#1-comment-ledger)
2. [Choosing the response](#2-choosing-the-response)
3. [Revising claims during a revision](#3-revising-claims-during-a-revision)
4. [Response structure](#4-response-structure)
5. [Quotation rules](#5-quotation-rules)
6. [Highlighting policy](#6-highlighting-policy)
7. [Synchronization after changes](#7-synchronization-after-changes)
8. [Integrating co-author and supervisor edits](#8-integrating-co-author-and-supervisor-edits)
9. [Change report](#9-change-report)
10. [Common failures and corrections](#10-common-failures-and-corrections)
11. [Hard quality gates](#11-hard-quality-gates)

## 1. Comment ledger

Build the ledger before writing any response:

| Comment id | Request (one line) | Action type | Owning unit | Planned change | Evidence or new run | Quoted units | Other responses that rely on the unit | Status |
|---|---|---|---|---|---|---|---|---|

Action types: revise wording, add or move an argument, add a model or analysis, add or rerun an experiment, clarify notation, correct an error, decline with evidence.

Rules:

- One comment, one row, with the venue's numbering (`Editor 1`, `1.1`, `2.3`). Never merge, skip, or renumber comments in the letter. [G-RV-ledger]
- The owning unit is the single paragraph, table, figure, or section that carries the change. A change that has no owning unit in the manuscript is not a revision.
- When two comments ask for the same change, both rows name the same owning unit and both responses quote it.
- Internal labels (decision codes, ledger ids, change classes) stay in the ledger and never appear in the letter.

## 2. Choosing the response

- Answer a request to model, quantify, or test something with the model, the quantity, or the test. An assumption that the quantity is sufficient or negligible does not answer it; it invites the same comment again. When the quantity cannot enter the optimization, evaluate it separately with a cited model, report it, and say once that it does not constrain the decisions. [G-RV-model]
- Answer a request about a limitation by stating the limitation once in the manuscript, in plain terms, and pointing it to future work (`X is not included as an optimization constraint in the present study; incorporating X is left for future work.`). Do not add a defense that no one requested, and do not repeat the limitation in several sections. [G-RV-limit]
- Answer a request for justification against another method family with two or three reasons tied to the target problem, placed in the section that compares method families. Do not claim general superiority.
- When the theoretical optimum cannot be determined, compare against reference values computed under stated idealizations and call them reference values, not bounds.
- Decline only with evidence (a citation, a measurement, a definition), and state what was done instead. A decline without an alternative action reads as a refusal.
- A new experiment needs the same protocol as the existing ones: same instances, budgets, run count, statistical test, and reporting format. Put it in the supplement when the page limit binds, and list it in one sentence at the end of the experimental setup.

## 3. Revising claims during a revision

Reviewers read the revised claims more closely than the original ones. Apply these checks to every revised or added sentence: [G-RV-claim]

- Replace a hedge with the exact logical statement when the consequence follows from definitions (`does not guarantee` instead of `may be insufficient`).
- Name the scope of every result (`in the selected runs`, `on the tested instances`, `up to N entities`).
- Remove unmeasured intermediate steps from causal explanations and closing value judgments (`practical value`, `superiority`) that no criterion supports.
- When a favorable component result could be offset elsewhere, say so (`lower A does not necessarily imply lower total B`).
- Write a nonsignificant comparison as `no statistically significant improvement`, never as support for the chosen design.
- Describe a platform or parameter set as representative of its class, with the specification source cited; drop product names unless a claim depends on them.
- In the abstract, report the main result as measured numbers and their range (`a 100% feasibility rate and an improvement of a%--b% over the best-performing baseline`), not as a superlative.
- In the conclusion, mirror the result sentences of the experiments at the same strength and scope, and write future work as a chain in which each direction builds on the previous one and answers a stated limitation (extend the model, then exploit the extended model, then reduce the resulting computational cost). Remove directions that no limitation motivates.

## 4. Response structure

### Default response

Default: two paragraphs per response. Deviate when a comment bundles several independent requests; then use a numbered list of sub-items, each with its own short explanation and quotes, and record the reason. [G-RV-p1]

1. **What was done.** One courtesy sentence, then one to four sentences that state the actions directly (`We have added ...`, `We have revised Section X to ...`, `We have clarified ...`). Add one sentence that carries the core argument or mechanism, so the response can be understood without the quotes. `We have clarified the motivation` alone fails; follow it with what the clarification says.
2. **Where it is.** A locator sentence (`Specifically, Section X now ...`; `The definition is given in Section A, referenced in Section B, and explained in Response C.`), one closing sentence, and the quoted units.

### Wording

- Vary the courtesy sentence and the closing sentence; adjacent responses do not repeat them. Neither sentence makes a claim.
- Use the reviewer's term once when it differs from the manuscript's term, then the manuscript's term.
- State changed settings with old and new values (`the reference point has changed from (a, b) to (c, d)`).
- Reuse the manuscript's own sentences for a claim; do not write a second version of an argument in the letter.
- The letter author prose follows the manuscript's prose rules.

### Editor responses

Editor responses summarize the action in one or two sentences and point to the reviewer response that carries the change and its quotes (`Please refer to our response to Reviewer 3, Comment 3.1.`). They quote nothing. A change forced on all results (a rerun after a model change) is announced once, in the editor response that owns it and in the reviewer response that asked for the model change.

### Item titles in quotes

Each quoted unit has a title with status, unit, and document: `Revised second paragraph of Section II-B of the main manuscript:`; `New Section S-X of the supplementary document:`. Name the document in full the first time in every response.

## 5. Quotation rules

- Quote complete paragraphs, tables with their captions, and displayed equations with their lead-in sentence and `where` clause. A partial paragraph hides context that the reviewer will look for. [G-RV-quote]
- Copy from the compiled manuscript, not from memory: the same words, citation numbers, equation numbers, highlighting, and table layout lines.
- When several responses rely on the same unit, quote it in full in each of them, and keep every copy identical. Do not write `see the passage quoted in Response 1.2 above`.
- After quoting, state what is highlighted (`The changes in the quoted paragraphs are highlighted in blue.`).
- When a quoted unit changes later, update every copy in the same edit. Check with a script that each quoted unit occurs verbatim in the compiled source, and check table bodies and header rows separately.
- A figure quoted in the letter is the same file version as in the manuscript.

## 6. Highlighting policy

Default: highlight only the revisions that answer a comment and that the letter quotes, plus all data cells whose values come from a rerun. Fix the policy with the co-authors before highlighting and apply it by a word-level comparison against the version submitted before the revision, not by memory. Deviate when the venue prescribes another convention, and record it. [G-RV-highlight]

- A new table that the letter quotes is highlighted as a whole (caption, body, rules, notes).
- A global rename requested by a reviewer is highlighted word by word, wherever the word occurs.
- The authors' own minor corrections of unhighlighted text (grammar, articles, term alignment) stay unhighlighted.
- A highlighted unit that no response quotes is either quoted or unhighlighted. List exceptions (artwork that cannot be colored) for the authors instead of editing the artwork.
- Remove the highlighting before the final upload when the venue asks for a clean copy.

## 7. Synchronization after changes

A revision changes numbers, equation numbers, citation numbers, terms, and figures. Every change propagates to all documents in the same pass. [G-RV-sync]

- **Numbers.** Generate table bodies from one result source and splice the same bodies into every quoted copy. Prose numbers (abstract, conclusion, letter) are hand edits; list them and check each against the source.
- **Directional claims.** After a rerun, recheck every sentence whose direction depends on the numbers (`higher on all instances`, `more on P1, similar on P2, less on P3`) and every best-value mark in the tables. [G-RV-rerun]
- **Disclosure of reruns.** When a model or protocol change forces a rerun of all experiments, say so in the letter once, where the change is owned, together with any changed evaluation setting (old and new values).
- **Renumbering.** Inserting an equation or a citation shifts every later number. Update the hard-coded numbers in the letter, in the supplement's references to the main manuscript, and in any notes that record numbers.
- **Terms.** One quantity keeps one term in all documents. After renaming, search all documents for the old term, including captions, table headers, and quotes.
- **Figures and artwork.** After a change of model, platform, or scenario, check every figure that draws the changed object (icons, labels, legends) and regenerate result figures from the same batch as the tables.
- **Explaining model changes.** A change to an equation that no reviewer asked for still needs one sentence in the letter where it fits (usually where the rerun is disclosed), or the reviewer will find an unexplained highlighted equation.
- Compile every document after the change and confirm that no reference is undefined and no page limit is exceeded. A text scan is not verification.

## 8. Integrating co-author and supervisor edits

- Save the received version unchanged as a snapshot before building on it. All later comparisons use that snapshot. [G-RV-coauthor]
- Adopt the framework of the edits: where a rule, a note, or an earlier decision disagrees with the edited text, update the rule, not the text.
- Respect deletions. Do not restore deleted text or citations unless the user asks.
- Fix only obvious errors inside the edited sentences, with the smallest edit, and report each fix.
- Check the edits for errors before building on them: quotes identical to the compiled source and complete; stale content left by a model change (old platform words, a figure that still draws the old object); two terms for one quantity; claims that a pending rerun may invalidate; quoted table layout equal to the source.
- Record the patterns of the edits (what was strengthened, weakened, moved, or deleted, and why) as reusable writing rules for the next paper.

## 9. Change report

At the end of a round, report every change made after the co-author snapshot, or after the previous round, so that the co-authors can verify them. [G-RV-report]

- Group by algorithm and experiments, main manuscript (by section), supplement (by section), and letter (by response).
- Give each change its location in the compiled PDF (page and unit) and its old and new value or wording in one line.
- List renumbering (equations, citations) once, as a block that needs no individual check.
- List decisions that remain open, without internal labels.
- Write the report in the co-authors' working language; keep code names, scripts, and internal ids out of it.

## 10. Common failures and corrections

| Failure | Why it fails | Correction |
|---|---|---|
| Answer `please model X` with `X is assumed to be sufficient` | The request is not answered | Model or evaluate X and report it; state once that it does not constrain the decisions |
| `We have clarified this point.` with nothing else | The reviewer must read the quotes to learn the answer | Add the core argument in one sentence |
| Quote half a paragraph | Hides context and breaks verification | Quote the complete unit |
| `See the passage quoted above` | The reviewer of another comment may not read that response | Re-quote the unit in full |
| A quoted copy differs from the manuscript | Breaks the reviewer's trust in every quote | Regenerate copies from the compiled source and check them by script |
| Rerun numbers updated in tables but not in the abstract or the letter | Two values for one result | List every prose number and check it against the source |
| `Higher on all instances` kept after a rerun | The direction may have changed | Recheck every directional sentence and best-value mark |
| An unexplained highlighted equation | The reviewer cannot tell why the model changed | Explain the change in one sentence where the rerun is disclosed |
| Restoring text a co-author deleted | Overrides an editorial decision | Keep the deletion; propose a restoration to the user if needed |
| Highlighting every touched sentence | Hides the answers to the comments | Highlight only quoted revisions and rerun data |

## 11. Hard quality gates

Do not deliver the revision unless all applicable gates pass:

- [ ] Every comment has one ledger row, one numbered response, and an owning unit in the manuscript or the supplement.
- [ ] Every request for a model, quantity, or experiment is answered by that model, quantity, or experiment, or declined with evidence and an alternative action.
- [ ] Every limitation is stated once, in plain terms, and pointed to future work.
- [ ] Every revised claim names its scope, contains no unmeasured causal step, and matches its evidence in strength.
- [ ] Every response states what was done and its core argument before the locator and the quotes.
- [ ] Every quoted unit is complete and identical to the compiled source, including numbers, citations, highlighting, and table layout; every reuse is a full re-quote.
- [ ] Highlighting follows the agreed policy, decided by comparison with the pre-revision version.
- [ ] Every number, equation number, citation number, term, and figure agrees across manuscript, supplement, and letter after the last change, and every directional claim was rechecked after the last rerun.
- [ ] Every model change and rerun is disclosed once in the letter with changed settings stated as old and new values.
- [ ] Co-author edits were snapshotted, their deletions respected, their errors reported, and a change report against the snapshot was delivered.
- [ ] All documents compile without undefined references and within the page limit.

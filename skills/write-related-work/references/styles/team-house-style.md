# Team house style

This file records the measured writing conventions of the author team: author voice, sentence rhythm, how sentences are combined and split, connectives, modifiers, banned constructions, section titles, paragraph openers, captions and equation lead-ins, and the shape of the title, abstract, index terms, contribution list, and Conclusion. It applies on top of the skill's own contract. Where a generic example sentence in a skill differs from this file, follow this file.

## Contents

1. [Scope and precedence](#1-scope-and-precedence)
2. [Author voice](#2-author-voice)
3. [Sentence rhythm](#3-sentence-rhythm)
4. [Combining and splitting sentences](#4-combining-and-splitting-sentences)
5. [Connectives](#5-connectives)
6. [Modifiers and claim strength](#6-modifiers-and-claim-strength)
7. [Banned constructions](#7-banned-constructions)
8. [Section and subsection titles](#8-section-and-subsection-titles)
9. [Paragraph openers by section](#9-paragraph-openers-by-section)
10. [Title, abstract, and index terms](#10-title-abstract-and-index-terms)
11. [Contribution list and roadmap](#11-contribution-list-and-roadmap)
12. [Conclusion](#12-conclusion)
13. [Captions and equation lead-ins](#13-captions-and-equation-lead-ins)
14. [Measuring a draft](#14-measuring-a-draft)
15. [Provenance](#15-provenance)

## 1. Scope and precedence

Apply this file by default to manuscripts of the author team. Skip it only when the user names another venue style or another team's conventions. For a Chinese manuscript, apply Sections 2, 4, 5, 6, and 7 through their Chinese counterparts in the Chinese manuscript adapter (Sentences), and replace the English bands of Sections 3, 10, and 12 with the adapter's weak-prior band in ideographs.

When sources disagree, use this order:

1. explicit rules of the author, which this file encodes;
2. recurring practice in the supervisor's edits;
3. a pattern shared by at least two of the four reference papers;
4. a pattern in a single reference paper.

The reference papers are the calibration source for structure and rhythm, not for every habit. Do not imitate these reference-paper practices: promotional modifiers (Section 6), first person in the body (Section 2), semicolons and `, but` (Section 7), `On one hand ... On the other hand ...`, `Our contributions are threefold` in a Conclusion, `state-of-the-art`, `superiority`, and `Last but not least`.

## 2. Author voice

Author actions take `this study` as the subject or use the passive. [G-STY-voice]

- `This study formulates ...`, `this study considers ...`, `this study proposes ...`, `This study designs ...`.
- `The periodic planning is formulated as ...`, `A dynamic constrained multi-objective evolutionary algorithm based on ... is proposed.`
- Use `we` only in future-work sentences of the Conclusion (`Building on this extended model, we will develop ...`). Do not use `our`.
- Use one self-reference noun in every section, including the roadmap: `this study`.
- Reserve `this study` for the sentences in which the paper itself acts: the contribution items, the scenario and algorithm sentences of the Introduction, the roadmap, and the opening of the Conclusion. Elsewhere, use the passive or make the algorithm or a modeled actor the subject. The reference Introductions use `this study` or `this paper` 1.5–6.4 times per 1000 words. The reserved positions alone give about five uses per 1000 words in an Introduction of about 1300 words, and the reference papers with lower rates use `we` in these positions.
- In running prose, the proposed method is `the proposed algorithm` (or `the proposed mechanism` for a component). Use its acronym where it is compared by name with baselines, in tables, and in figure legends. The reference papers use `the proposed` 2.5–6.8 times per 1000 words.
- Other valid agents are the algorithm and the modeled actors (controller, platform, vehicle, server). A section, table, or figure takes only reporting verbs (`Section II reviews ...`, `Table III presents ...`, `Fig. 3 shows ...`).
- Response letters keep the first person (`We have revised Section V-C ...`).

## 3. Sentence rhythm

Default: keep the body and every section inside the band below. A deviation needs a reason, recorded in the scale statement of the delivery note and never in the manuscript. [G-STY-rhythm]

Counting rule: the counting rule of the reader and terminology contract, with inline math counted as one word in sentence lengths, sentences under four words (run-in labels such as `Step 1.`) excluded, and the abstract excluded from the body.

<!-- calibrate:begin rhythm -->
| Body measure | Band | Reference papers (four) | Supervisor-approved draft | Supervisor-approved baseline draft |
|---|---|---|---|---|
| Mean sentence length (words) | 23.2–24.8 | 23.2, 24.2, 24.4, 24.8 | 20.4 | 22.3 |
| Median | 21–23 | 21, 22, 23, 23 | 19 | 21 |
| 90th percentile | 37–39 | 37, 38, 38, 39 | 33 | 36 |
| Share of sentences over 35 words | 11%–15% | 11%, 14%, 14%, 15% | 7% | 11% |
| Share of sentences under 12 words | 9%–11% | 9%, 9%, 11%, 11% | 19% | 15% |

| Section | Mean sentence length band | Supervisor-approved draft |
|---|---|---|
| Abstract | 24.8–30.5 | 24.8 |
| Introduction | 20.1–23.6 | 20.2 |
| Related Work | 21.3–26.3 | 23.3 |
| System Model and Problem Formulation | 22.7–27.1 | 19.7 |
| Proposed algorithm | 20.5–27.0 | 19.2 |
| Experimental studies | 22.6–24.6 | 20.6 |
| Conclusion | 24.2–28.0 | 28.0 |

The body and section bands follow the reference papers. The supervisor-approved draft is shown for comparison, and its abstract and Conclusion values widen those two bands. Section means within 3 words of the band count as inside.
<!-- calibrate:end rhythm -->

How to use the band:

- A draft below the band has been over-split. Apply the merges of Section 4 before cutting content. Drafts written under the one-claim rule alone fell to a mean of 16–20 words with 20%–30% of sentences under 12 words.
- A draft above the band stacks claims. Split it with the rules of Section 4.
- Most sentences carry 15–30 words. Keep sentences under 12 words for a short result or a definition, and never write three in a row.
- The 90th percentile and the two shares describe the body of a whole paper, measured over at least three of the Introduction, Related Work, model, method, experiment, and Conclusion sections. When one section is drafted or measured alone, check its section mean only. A settings subsection that lists definitions and parameters may hold many long or short sentences. Do not split its definition or list sentences to move a share into the band.
- After a section-mean flag, split or merge only until the mean is inside the band. Do not aim at the band center, and check afterwards that the long sentences were not all split. This rule applies only after a flag and is no reason to skip a reread.
- The four reference experiment sections hold 6.5%–9.1% of sentences under 12 words. When an experiment section falls below 6.5% (another section below 5%), reread whether short results and definitions were merged into long sentences, and aim at the reference range, not at the threshold. The script lists this as a note, not a flag.
- The body band is the default to act on. The section bands rest on four papers and vary more between papers than the body band (compare the last two columns of the validation table in Section 15). Treat a section outside its band as a reason to reread that section, and change it only when its sentences show the over-splitting or stacking signals of Section 4.

## 4. Combining and splitting sentences

A sentence states one claim. A claim may carry its direct consequence, the two sides of one comparison, its cause, its purpose, or a definition of its terms. Split only what is a second claim, and merge what was split without being a second claim. [G-STY-merge]

Split when a sentence:

- joins two independent claims with `, and` (two results, a fact and its consequence with different subjects, a setup and a result);
- ends with a participle that adds a new fact whose implied subject differs from the main subject;
- contains a `which` clause that could attach to more than one antecedent;
- exceeds about 40 words and carries two claims.

Keep in one sentence, and merge back when they were split:

- the direct consequence of the same action: `..., thereby altering the feasible region for the next cycle`, or a participle with the same implied subject (`..., increasing their return distances`);
- the two sides of one comparison: `while`, `whereas`;
- a short cause: `Since X, Y` (limited in Section 5), `Due to X, Y`, `With X, Y`, `As X, Y`;
- a purpose: `To V, ...`, `in order to V`;
- a definition or an identity: `..., where X denotes ...`, `..., namely, ...`;
- members or examples: `including ...`, `such as ...`;
- a relative clause with exactly one possible antecedent: `..., which ...`.

Over-splitting signals:

- three or more consecutive sentences under 12 words;
- two adjacent sentences under 12 words in which the second states the other side of a comparison (`In contrast`, `whereas`) or repeats the subject of the first (the fingerprint script lists these as merge candidates);
- consecutive sentences with the same subject that each add one attribute;
- a sentence that only states the consequence of the previous one (`This results in ...`, `This leads to ...`);
- a run of `Since`, `Therefore`, or `Accordingly` openers created by splitting.

Synthetic examples:

- Before: `The depot is fixed before the mission. The vehicles then return to a distant depot. This increases their return distances.` After: `A depot fixed before the mission can be far from the vehicles late in the mission, increasing their return distances.`
- Before: `The mobile depot shortens the return trips. The static depot keeps them long.` After: `The mobile depot shortens the return trips, whereas the static depot keeps them long.`
- Before: `The proposed algorithm finds feasible runs on all instances. Its mean HV is higher than that of the baselines. This holds on all three instances.` After: `On all three instances, the proposed algorithm achieves a 100% feasibility rate and a higher mean HV than the baselines.`

After a merge, check that no `, and` joins two independent claims, that no modifier dangles, and that the sentence stays under about 35 words.

## 5. Connectives

Rotate connectives the way the reference papers do, and do not let a banned word be replaced by one stock substitute. [G-STY-conn]

| Sentence opener | Reference papers, per 100 sentences | House rule |
|---|---|---|
| However | 1.0–2.6 | A real contrast with the preceding argument |
| Therefore | 0.0–2.0 | A result of the preceding sentence |
| Consequently, As a result, Thus | 0.0–0.7 each | Rotate the result connectives; do not repeat one in adjacent paragraphs |
| Moreover, Furthermore, In addition, Additionally | 0.0–1.2 each | A further point on the same question |
| Specifically | 0.2–1.2 | Expands the preceding sentence |
| In contrast | 0.0–1.0 | Opposes two named objects |
| For example, For instance | 0.8–1.7 combined | One concrete case where a general claim needs it, mainly in the Introduction and Related Work |
| As shown in Table/Fig. | 0.4–1.4 | Points to the artifact the sentence reads from |
| To address ... | 0.6–0.8 | Introduces the response to a stated difficulty |
| Since | 0.0–1.0 | At most one per 100 sentences |
| Accordingly | 0 (supervisor-approved baseline 0.9) | At most one per 100 sentences |
| Hence | 0 | Not used |
| On one hand, On the other hand | two papers | Not used |

The per-100 ranges are rates over the body of a whole paper. One section is too short for a rate, and some openers cluster in one section: the four reference Introductions open 3.6–9.1 of every 100 sentences with `However`, above the paper-level range. When one section is drafted or measured alone, count instead. Allow one sentence-initial `Since` and one `Accordingly` per full 100 sentences of the section, and no `Hence`. A section under 100 sentences has no allowance, so the whole paper stays at one per 100 sentences. Check `However`, `To address`, and the other rates over the whole paper.

Within sentences, the reference papers use `, thereby` and same-subject participle tails 2.1–3.8 times per 1000 words, `while` or `whereas` 2.9–3.5, `due to` 0.5–1.3, `, which` 0.9–2.2, and `, where` 0.6–3.1.

Rules:

- Replace `because` with `since`, `as`, `due to`, `given that`, a `To ...` purpose clause, or a sentence whose subject is the cause (`The limited battery capacity restricts ...`). Do not turn every causal clause into a sentence-initial `Since`.
- After removing `because` or `so`, check that the cause is still stated. It stays as a `since`, `as`, or `due to` clause, or it becomes the subject of its own sentence. Deleting the clause deletes the reason. When the sources give two causes for one weakness, keep both, each with its own citation.
- Do not open two consecutive sentences with the same connective.
- Do not use `Thus` or `Therefore` to introduce the explanation of an equation or a definition.
- After a splitting pass, count the connectives again.

## 6. Modifiers and claim strength

Promotional modifiers appear 4.0–6.8 times per 1000 words in the reference papers and 0.1–0.3 times in the supervisor-approved drafts. Follow the supervisor. [G-STY-mod]

- Do not use `superior`, `critical`, `fundamental`, `crucial`, `essential`, `promising`, `comprehensive`, `remarkable`, `novel`, or `state-of-the-art` as evaluation words.
- Use `significant` or `significantly` only with a named statistical test.
- Use `outperform` only with the metric and the baselines named.
- State scope instead of strength: `in the selected runs`, `on the tested instances`, `across all three instances`, `including those with up to N units`.

## 7. Banned constructions

Do not use these in author prose. Pasted reviewer comments and quoted titles are exempt. [G-STY-ban]

- `because`, `so`, `so that`, `so as to` (Section 5 lists the alternatives, which keep the cause stated);
- `, but` joining two clauses: split the sentence and open the second with `However,`, or use `while` or `whereas` for the two sides of one comparison;
- semicolons in running prose: split the sentence, or enumerate with `(i) ..., (ii) ...`;
- a colon joining two independent clauses (a colon may introduce a list or a display);
- `, and` joining two independent claims (lists and compound predicates with one subject are fine);
- `e.g.` in running prose: use `such as` or `For example, ...`; `i.e.` only inside parentheses for a short gloss;
- `Hence`;
- `we` or `our` outside future work (Section 2);
- an inanimate noun as a volitional agent: a mechanism, constraint, equation, metric, section, or table does not decide, ensure, guarantee, validate, or explain;
- a dangling modifier after a split (`By solving ..., the duration is derived` becomes `Solving ... yields the duration` or a passive with an explicit operation);
- sweeping meta sentences such as `no existing study considers ...` or `... remains largely unexplored`: state the assumption that fails instead.

## 8. Section and subsection titles

Default: use the titles below. Deviate when the venue prescribes other titles, or when an inherited structure splits the model into a workflow section and a modeling section (the system-model skill allows this split), and record the reason. [G-STY-head]

| Section | Default title | Attested subsection titles |
|---|---|---|
| I | Introduction | none |
| II | Related Work | `Review of <research line>`, `Review of Existing <solver family>s` (two papers); a closing `Critical Analysis of the Literature Review` (one paper) |
| III | System Model and Problem Formulation (three papers) | `<Name> Model` for each module, then `Problem Formulation` |
| IV | Proposed Algorithm (three papers) | `Solution Encoding Scheme` or `Representation of the Encoding Scheme`; `Core Algorithm Design` or `Key Algorithm Design`; `<Name> Mechanism`; `Complexity Analysis` or `Computational Time Complexity` |
| V | Experimental Studies (three papers; `Numerical Results` in one) | `Experimental Settings` or `Parameter Settings and Test Instances`; `Overall Performance Comparison`; `Investigation of ...`, `Comparison of ...`, `Evaluation of ... on ...`, `Trade-off Analysis of ...` |
| VI | Conclusion | none |

- Do not title the experiment section `Performance Evaluation` or `Simulation Results`.
- Do not put the algorithm acronym into the section title (`Proposed Algorithm`, not `Proposed X-Y Algorithm`).
- An experiment subsection title names the operation and the object in about eight words or fewer (the reference experiment subsection titles average 4.3–6.7 words): `Overall Performance Comparison`, `Investigation of the <mechanism>`, `Comparison of <named alternatives>`, `Trade-off Analysis of the <obtained solutions>`. Name the varied factor in the title when it fits, otherwise in the opening sentence of the subsection. Do not use a bare topic phrase such as `Impact of X` or `X Study`, and use `Comparison of ...` rather than `Investigation of ...` when the subsection compares named alternatives.

## 9. Paragraph openers by section

Use these attested openers before inventing new ones. Counts give the number of reference papers (out of four) in which the opener starts a sentence; H marks the supervisor-approved draft. Openers that start with `we` in the reference papers are given in the house voice. [G-STY-open]

| Section | Opener | Attested |
|---|---|---|
| Introduction | `To address this issue/limitation, this study considers/proposes ...` | 3, H |
| Introduction | `However, both/these/existing approaches ...` | 4, H |
| Introduction | `Existing <studies> can be categorized into <N> <groups> according to <criterion>, namely, ...` | 1, H |
| Introduction | `Motivated by this gap, this study considers ...` | 1, H |
| Introduction | `In this scenario, the <controller> determines ... in each <cycle>.` | 1, H |
| Introduction | `Solving the formulated <problem> poses/requires ...` | 2, H |
| Introduction | `For example, ...` / `For instance, ...` | 4 |
| Introduction | `The main contributions of this study are summarized as follows:` | 4, H |
| Introduction | `The remainder of this study is organized as follows.` | 4, H |
| Related Work | `This section reviews <existing literature> from two perspectives.` | 1, H |
| Related Work | `<Author> et al. proposed/developed ... to ...` | 2, H |
| Related Work | `For example, ...` | 3 |
| Related Work | `However, these studies ...` / `While these <methods> ..., ...` | 2, H / 2 |
| System model | `As illustrated in Fig. 1, ...` | 2 |
| System model | `To ensure ..., ...` | 3 |
| System model | `Based on ..., ...` | 4, H |
| System model | `where X denotes ...` (after a display) | 4, H |
| System model | `Upon receiving ..., ...` | 3 |
| System model | `For each <entity>, ...` / `When ..., ...` | 4 / 2, H |
| Proposed algorithm | `This section presents ...` | 2 |
| Proposed algorithm | `The proposed algorithm ...` | 4, H |
| Proposed algorithm | `For each <individual>, ...` / `In each generation/cycle, ...` | 2, H |
| Proposed algorithm | `The pseudocode of ... is presented in Algorithm 1.` | 4 |
| Proposed algorithm | `The computational complexity of ... ` | 2 |
| Proposed algorithm | `After ..., ...` / `If ..., ...` | 4 / 3, H |
| Experimental studies | `In this section, simulation experiments are conducted to evaluate ...` | 3, H |
| Experimental studies | `To validate/evaluate/investigate ..., ...` | 4, H |
| Experimental studies | `As shown in Table/Fig. X, ...` | 3, H |
| Experimental studies | `Table X presents ...` / `Fig. X shows ...` | 3 / 2, H |
| Experimental studies | `These results indicate/show that ...` | 3, H |
| Experimental studies | `In contrast, ...` / `Compared with ..., ...` | 2, H / 2 |
| Conclusion | `In this study, ...` | 2, H |
| Conclusion | `The experimental results show that ...` | 2, H |
| Conclusion | `The ablation studies ...` | 2, H |
| Conclusion | `Future work will ...` / `Building on ..., we will ...` | 1, H |

Use an opener only in a paragraph that already has its function. Use each Introduction opener at most once per paper, apart from `For example` and `For instance` (`In this scenario, ...` opens a sentence in one of the four reference Introductions). `To address ..., this study considers` (the scenario) and `To address ..., this study proposes` (the method) count as two openers. Do not add a paragraph to host an opener. When the reference papers of the target family classify the literature in Related Work, the Introduction adds no classification paragraph. Do not repeat the verb in the count noun (`categorized into two categories`). Write `fall into two groups` or `are classified into two kinds of approach` instead.

Do not open with `Note that`, `It is worth noting that`, `Recently, ...`, or `As is well known`.

## 10. Title, abstract, and index terms

Default: follow the shapes below. Deviate when the venue sets other limits, and record the reason. [G-STY-front]

**Title.** Two parts joined by a colon, 13–17 words (four reference papers 13, 15, 15, 17; the supervisor-approved title 17). The first part names the system and its setting (`<platform>-Enabled <service> in <environment>`). The second part names the approach type and, optionally, the objectives or the key mechanism (`A Joint <X> and <Y> Optimization`, `A Constrained Multi-Objective Approach With <Name> Mechanism`, `A <Name>-Driven Dynamic Constrained Multi-Objective Evolutionary Approach`). No `Novel`, no `Efficient`, no question form.

**Abstract.** One paragraph, 210–250 words (reference papers 210–249; the author's limit is 250), 7–10 sentences, no citations, no equations, every abbreviation defined. Moves in this order:

| Move | Reference papers | House form |
|---|---|---|
| Field and setting | 4 | `<Field> enables/has emerged as ... in <application>.` |
| Existing approaches and their limiting assumption | 4 | `However, existing <approaches> fix/assume ...` followed by the consequence of that assumption |
| Scenario or model of this study | 4 | `To address this limitation, this study considers a scenario in which ...` |
| Decisions and formulation | 4 | `The <planning> is formulated as a <problem class> that jointly optimizes ..., balancing ... under ...` |
| Algorithm | 4 | `A <solver family> based on a <mechanism> is proposed.` or `To solve this problem, this study designs ...` |
| Result with numbers and scope | 4 | `Experiments on <N> <instances> show that the proposed algorithm outperforms <N> <baselines>, achieving <metric value> and improving <metric> by X%–Y% over the best-performing baseline.` |
| Significance (optional) | 2, H | `This study provides a foundation for <problem area>.` |

Do not write `the highest`, `superior`, or `state-of-the-art` in the result move. The result move reports the range against the best-performing baseline.

**Index terms.** Four or five terms, ordered from application to solver: system or scenario, network or application setting, an optional model-specific term, the problem class, and the solver family (a term ending in `evolutionary algorithm` closes the list in all four reference papers and in the supervisor-approved draft). Capitalize the first term, proper nouns, and acronyms only; no `and` before the last term; end with a period.

## 11. Contribution list and roadmap

**Contribution list.** Introduce it with `The main contributions of this study are summarized as follows:`. Use two or three bullet items (three in the reference papers, two in the supervisor-approved draft) and 125–246 words in total. [G-STY-contrib]

- Start every item with `This study` and a verb: `formulates`, `considers`, `proposes`, `designs`. The newest reference paper uses the same form with `This paper`.
- Order the items as scenario or model, formulation, then algorithm. Merge the scenario into the formulation item when the scenario is not itself a contribution.
- Write two to four sentences per item: the object, what is jointly optimized or how the mechanism works, and, in the last item only, one result sentence with its scope (`Experimental results on three benchmark problems show that the proposed algorithm achieves ... than five existing <solver family>s.`).
- No `novel`, `first`, or `superior`; no claim that the experiments do not show.

**Roadmap.** `The remainder of this study is organized as follows.` followed by one sentence per section: `Section II reviews ...`, `Section III presents the system model and the formulation of ...`, `Section IV introduces the proposed algorithm to solve ...`, `Section V presents the experimental studies.`, `Section VI concludes this study.` Keep the roadmap to one sentence per section and at most about 77 words (reference roadmaps 56–77 words, the supervisor-approved roadmap 46). Name what each section does, and do not summarize its content (no list of models, mechanisms, or results).

## 12. Conclusion

Default: one or two paragraphs, 165–280 words, 6–10 sentences (reference papers 165–256 words; the supervisor-approved Conclusion 280 words in two paragraphs). [G-STY-concl]

1. One or two sentences restate the problem, the formulation, and the algorithm (`In this study, <problem> has been addressed through the <formulation> and <the algorithm>.`).
2. One sentence per experiment group, in the order of the experimental section, each with its scope and no stronger than the result paragraph it summarizes.
3. Future work as a chain of two or three sentences: extend the model to remove a stated limitation, build the method on the extended model, then handle the computational cost that the extension creates (`Future work will incorporate ...`, `Building on this extended model, we will develop ...`, `To address the increased computational burden ..., we will investigate ...`). Delete directions that do not follow from a limitation of this study.

Do not restate the contribution list (`Our contributions are threefold`), and do not add a value judgment that no experiment measures (`These results show the practical value of ...`).

## 13. Captions and equation lead-ins

**Captions.** A figure or table caption is a noun phrase that identifies the artifact and ends with a period. Write it in sentence case in the source (the document class may print table captions in capitals), and give every caption of one kind the same form. [G-STY-cap]

- Name the compared objects, the instances, and the run-selection rule (`at the median run`, `for the median-performing run`).
- Keep the noun phrase of a result-table caption to about 20 words (the reference papers use 6–20). Put metric full names, the run count, and the significance rule in the note below the table, or in short sentences after the noun phrase only when the manuscript or the user states that the document class has no table notes (as in the supervisor-approved draft). In Markdown or when the class is unknown, write them as a `Note.` line below the table.
- Fill a caption form with the manuscript's own terms. When the setup calls its test settings `cases`, the caption does too, even where the attested form says `instances`.
- Do not state the result, explain the method, or repeat what the panel labels, legend, or setup paragraph already state. Panel labels such as `(a) CMOP1. (b) CMOP2.` may follow when the class prints no subcaptions.
- Define every abbreviation that appears in a table header or row label, in the caption or in a note below the table, and explain significance symbols in that note.
- Figures and tables of one paper share the sentence case and the final period. An algorithm caption is a sentence-case noun phrase that names the procedure, without a final period (three reference papers and the supervisor-approved draft).

Attested forms, with the number of reference papers (out of four) that use each; H marks the supervisor-approved draft:

| Artifact | Form | Attested |
|---|---|---|
| System figure | `Illustration of the considered <system>.` | 3, H |
| Encoding figure | `Illustration of the genetic encoding scheme.` | 2 |
| Pareto-front plot | `Obtained feasible non-dominated solutions of <instances>.` | 2 |
| Convergence plot | `Convergence graphs of the <N> algorithms on <instances> at the median run.` | 3 |
| Parameter table | `Simulation parameters among the <N> <instances>.` or `Parameter settings for the <N> <instances>.` | 3, H / 2, H |
| Instance table | `Test instance configurations with varying problem scales.` | 2 |
| Result table | `Comparison results of the <N> algorithms based on the mean and standard deviation (in parentheses) of <metrics>.` | 3 (the `based on` tail in 2), H |
| Scenario table | `Comparison of the <A> and <B> scenarios.` | 1, H |

**Equation lead-ins.** Name the quantity, then introduce the display with a clause that ends in a colon. Three of the four reference papers introduce 43%–48% of their displays this way, while the other displays continue a sentence (`..., where`, `subject to`). The supervisor-approved draft introduces every display with a colon. [G-STY-eq]

| Lead-in | Papers | Occurrences |
|---|---|---|
| `<quantity> is calculated as follows:` and other `... as follows:` forms | 4 | 22 |
| `<quantity> is given by:` | 3 | 5 |
| `<quantity> is:` | 2 | 14 |
| `<quantity> is determined by:` | 2 | 2 |
| `<quantity> can be expressed as:` | 1 | 3 |

- When the display adopts a cited model, cite it in the lead-in (`The hovering power is given by [12]:`).
- After the display, define the new symbols in one `where` clause in the order in which they appear, then state a meaning, coupling, or boundary case if one is needed.
- Do not open with `The following equation gives ...`, and do not introduce the explanation with `Thus` or `Therefore`.
- End the display with a comma or a period as part of the sentence.

## 14. Measuring a draft

Run `scripts/style_fingerprint.py` (in the skill directory) on the draft when Python is available. Pass a LaTeX root file: the script inlines `\input`, `\include`, `\subfile`, and `\import` files and warns about missing ones. A Chinese manuscript is detected and measured in ideographs against the weak-prior band of the Chinese adapter (`--lang zh` forces it).

The default output reports:

- section scale, the sentence-length profile, connectives per 100 sentences, and within-sentence features per 1000 words, with flags against the band of Section 3 (a file with fewer than three main sections is checked against its section means and connective counts only);
- banned constructions, runs of short sentences, adjacent short sentences that could merge, and repeated connectives, each with its sentences;
- document checks: figure and table captions without a final period or in title case, an algorithm caption with a final period, a result-table noun phrase over 22 words (printed capitals included), subsection titles of ten or more words, a roadmap over 77 words or with a sentence that names no section, an Introduction opener used more than once, a count noun that repeats its verb, and more than 6.9 uses of `this study` per 1000 words in the Introduction;
- notes, which are not flags: whole-paper measures outside the band when fewer than three main sections are measured, a section mean outside its band but inside the tolerance, a section of 20 or more sentences below its short-sentence threshold (experiments 6.5%, other sections 5%), a single-section connective count at its limit, and a table caption over 30 words with its note sentences.

Options:

- `--section exp` restricts the report to one section;
- `--scale exp=900-1900 exp.paragraphs=10-19 related.last_paragraph_words=120-160` checks the ranges of the scale statement (measures `words`, `paragraphs`, `paragraph_words`, `sentences`, `first_paragraph_words`, and `last_paragraph_words`);
- `--terms ledger.txt` reads the term ledger, one group per line with the ledger term first (`case: instance, test instance`), and reports every other variant with its count per section, in the abstract, and in the captions, with the sentences that use it (the long form in an abbreviation definition is not counted);
- `--citations` lists citation keys repeated within a section, and `--spine --section intro` prints the opening sentence of every paragraph under its heading;
- `--abbrev main.tex supplement.tex reply.tex` audits abbreviation definitions and uses in each document and compares their long forms;
- `--report main.tex supplement.tex reply.tex --out report.md` writes all of the above as one Markdown pre-submission report and checks abbreviations, ledger terms, and banned constructions in the supplement and the letter too (the letter keeps its first person);
- `--diff old.tex new.tex --show 10` classifies the edits between two versions into merges, splits, rewrites, insertions, and deletions.

Read every flagged sentence before changing it. A flag is a measurement, not a verdict: a long sentence may be a necessary list, and a short one may be a result.

## 15. Provenance

The numbers were measured on the complete text of four IEEE Transactions papers by the author team, all constrained or dynamic constrained multi-objective evolutionary approaches to UAV or edge-computing systems:

- *Demand-Aware Multi-Area Multi-UAV Empowered Mobile Edge Computing: A Joint Energy and Delay Optimization*;
- *Joint Latency and Charge Cost Minimization for Reliable Task Offloading in Dispersed Computing: A Multi-objective Optimization Approach* (DOI `10.1109/TMC.2026.3679393`);
- *Terrain-Aware UAV-Enabled Mobile Edge Computing in Urban Environments: A Constrained Multi-Objective Approach With Task-Adaptive Mechanism* (DOI `10.1109/TVT.2025.3604250`);
- *UAV-Enabled Multi-Source Data Fusion in Vehicular Networks: A Joint Optimization Approach for Reliability and Latency* (DOI `10.1109/TWC.2026.3676831`).

Experiment order. Two of the four reference papers (Demand-aware and Fusion) report their scenario experiments before the overall comparison. The Dispersed and Terrain-aware papers open with the overall comparison and then investigate their mechanisms. The supervisor-approved revision moved its scenario experiments ahead of the overall comparison. These observations support the ordering default of the experiment skill.

The body and section bands follow the four papers, and drafts aim at their rhythm. The author chose this after a blind evaluation compared it with a band widened to the supervisor-approved draft. Measured with the same counting, that draft writes shorter sentences than the four papers (body mean 20.4 against 23.2–24.8 words). The rhythm table shows it for comparison, and its abstract and Conclusion values widen those two bands.

The supervisor-practice rows come from two rounds of supervisor edits on a 2026 journal revision by the same team, measured as before-and-after sentence diffs; no sentence of that manuscript is reproduced here. In the only round that contained supervisor edits alone, the changed passages went from 49 to 38 sentences and their mean length rose from 22.3 to 23.9 words, through six merges and two deletions without a single split. All examples in this file are synthetic. Openers and title shapes are short stock phrases, not copied sentences.

<!-- calibrate:begin validation -->
Validation. The band was checked against 13 further published papers that were not used to set it: 5 same-lineage constrained evolutionary papers, 8 reinforcement-learning MEC papers. Their body mean sentence lengths run from 20.5 to 26.9 words.

| Group | Papers | Body mean (min–max) | Body mean inside the band or its tolerance | Any section mean outside |
|---|---|---|---|---|
| same-lineage constrained evolutionary papers | 5 | 21.5–26.9 | 3 of 5 | 2 of 5 |
| reinforcement-learning MEC papers | 8 | 20.5–25.1 | 6 of 8 | 5 of 8 |
<!-- calibrate:end validation -->

The tables between `calibrate` markers in Sections 3 and 15, the band in the fingerprint script, and the Chinese weak-prior tables are generated together. When the team publishes another paper of this family, add it to the reference set and regenerate them with the calibration tool of the collection repository instead of editing the numbers by hand.

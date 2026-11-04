# Summary-part contract and quality gates

## Contents

1. [Summary ledger](#1-summary-ledger)
2. [Title](#2-title)
3. [Abstract](#3-abstract)
4. [Index terms](#4-index-terms)
5. [Contribution list and roadmap](#5-contribution-list-and-roadmap)
6. [Conclusion](#6-conclusion)
7. [Future work](#7-future-work)
8. [Synchronization](#8-synchronization)
9. [Common failures and corrections](#9-common-failures-and-corrections)
10. [Hard quality gates](#10-hard-quality-gates)

All examples below are synthetic. They illustrate shapes, not wording to copy.

## 1. Summary ledger

The title, abstract, contribution list, and Conclusion compress claims made elsewhere. Build the ledger of Step 1 before drafting any of them, and give every row a source sentence in the result sections.

- A summary claim may be as strong as its source sentence and no stronger. If the source says `in the selected runs`, the summary says it too. [G-AC-claim]
- A claim that depends on an unmeasured intermediate step (`the saved energy is spent on more tasks`) stays out of every summary part.
- A component result does not become an overall advantage: when the source names an offsetting quantity, either keep the offset or drop the claim.
- Value judgments that no experiment measures (`demonstrates the practical value`, `paves the way for widespread deployment`) are not claims and are deleted.

## 2. Title

- Two parts joined by a colon. The first names the system and its setting; the second names the approach type and, optionally, the objectives or the key mechanism.
- Use the terms of the abstract. A coined term does not first appear in the title.
- No `Novel`, `Efficient`, `Towards`, or question forms; no undefined acronyms beyond those standard in the field.
- Check the word range of the house style or the venue. [G-AC-title]

Synthetic shape: `Mobile Charging Station-Assisted Delivery Robots in Campus Networks: A Constrained Multi-Objective Evolutionary Approach`.

## 3. Abstract

One paragraph, no citations, no equations or symbols, every abbreviation defined at first use. Moves in this order: [G-AC-abs]

1. **Setting.** The field and the operating setting in one sentence.
2. **Limiting assumption.** What existing approaches fix or assume, then the consequence of that assumption in this setting. State the mechanism, not a verdict (`existing approaches fix the station locations before operation` rather than `existing approaches are inadequate`).
3. **Scenario.** `To address this limitation, this study considers a scenario in which ...`, with the actors and the cycle in plain words.
4. **Formulation.** The decisions, the objectives, and the constraint classes, with the problem class.
5. **Algorithm.** The solver family and the mechanism that answers the stated difficulty.
6. **Result.** Numbers with scope: the benchmark set, the number of baselines, the headline metric value, and the improvement range over the best-performing baseline. [G-AC-num]
7. **Significance (optional).** One sentence naming the problem area that the study supports, without a superiority claim.

Result-move rules:

- Report a range over the best-performing baseline (`improving mean hypervolume by 6.2%–48.5% over the best-performing baseline across the three instances`), not `the highest` or `superior`.
- Name the scope that the result sections name: number of instances, independent runs, or selected runs.
- When results are mixed across instances, the abstract may report only what holds on every instance, or state the exception.

Synthetic result sentence: `Experiments on three campus instances show that the proposed algorithm outperforms four representative algorithms, achieving a 100% feasibility rate and reducing the mean delivery delay by 7.4%–21.9% relative to the best-performing baseline.`

Length: stay inside the venue limit and the house-style range. When over the limit, shorten the setting and limitation moves first, never the result move.

## 4. Index terms

- Four or five terms, ordered from application to solver: system or scenario, network or application setting, an optional model-specific term, the problem class, and the solver family. [G-AC-kw]
- Reuse the exact terms of the title and the abstract; do not add a term that appears nowhere in the paper.
- No `and` before the last term; end with a period; capitalize only the first term, proper nouns, and acronyms.

## 5. Contribution list and roadmap

Contribution items: [G-AC-contrib]

- Two or three items in the order scenario or model, formulation, then algorithm. Merge the scenario into the formulation item when the scenario is not itself a contribution.
- Each item opens with the author subject and an action verb on a new object (`This study formulates ...`, `This study proposes ...`), then states what is jointly optimized or how the mechanism works.
- Only the last item carries a result sentence, with the scope used in the result sections.
- No `first`, `novel`, or `superior`; no standard algorithm presented as a contribution; no item that the experiments do not support.

Roadmap: one sentence per section, with the section as the subject of a reporting verb (`Section II reviews ...`, `Section III presents ...`, `Section IV introduces ...`, `Section VI concludes this study.`).

## 6. Conclusion

Default order: [G-AC-concl]

1. One or two sentences restating the problem, the formulation, and the algorithm in the vocabulary of the abstract.
2. One sentence per experiment group, in the order of the experimental section. Each sentence carries the scope of its source (`across all tested instances, including those with up to twelve robots`, `in the selected runs`) and no stronger verb than the result paragraph.
3. Future work (Section 7).

Rules:

- Do not restate the contribution list (`The contributions of this study are threefold ...`).
- Do not add a result that the experimental section does not report, or a value judgment that no experiment measures.
- When an experiment shows a trade-off or an offsetting cost, the Conclusion keeps it (`while the effect on total energy depends on the station's own travel cost`).
- Keep one paragraph for the summary and, when the venue allows, a second paragraph for future work.

Synthetic summary sentence: `The scalability study shows that the proposed algorithm maintains a 100% feasibility rate on instances with up to twelve robots and sixty delivery zones, whereas the feasibility of the baselines declines as the problem scale increases.`

## 7. Future work

Write future work as a chain in which each step builds on the previous one and answers a limitation stated in the paper. [G-AC-future]

1. Extend the model to remove a stated limitation (an omitted cost, an idealized assumption, a resource left outside the formulation).
2. Build the method on the extended model (a decision rule, a look-ahead, a learned component that the extension requires).
3. Address the computational or deployment cost that the extension creates (distributed, hierarchical, or incremental optimization).

Rules:

- Delete directions that do not follow from a limitation of this study, even when they are popular.
- Name the limitation in the model's own terms, not as a confession (`the station's battery is not included as a constraint`).
- Two or three sentences are enough.

Synthetic chain: `Future work will incorporate the station's battery limit and charging queue into the planning model. Building on this extended model, we will develop look-ahead selection rules that account for how current routes affect later charging opportunities. Distributed optimization will then be investigated to reduce the planning time for larger robot fleets.`

## 8. Synchronization

The title, abstract, index terms, contribution list, and Conclusion form one claim set with the result sections. [G-AC-sync]

- One term per quantity and per method in all summary parts and in the result sections.
- Every number in a summary part equals the number in its source artifact after rounding, and its range covers exactly the instances it names.
- After a rerun, a parameter change, or a model change, recheck every number, every direction word (`more`, `similar`, `less`), and every scope phrase in all summary parts and in any response letter that quotes them.
- The improvement range in the abstract and the result sentence of the last contribution item use the same baseline and the same metric.

## 9. Common failures and corrections

| Failure | Correction |
|---|---|
| `achieves the highest hypervolume` | Report the improvement range over the best-performing baseline with the instance count |
| Abstract limitation written as a verdict (`existing methods are inadequate`) | State the assumption that existing methods make and its consequence |
| Abstract over the word limit after adding the result | Shorten the setting and limitation moves |
| Conclusion lists the contributions again | Summarize the evidence by experiment group, in order |
| Conclusion drops the scope of a selected-run result | Restore `in the selected runs` |
| Conclusion adds `These results show the practical value of ...` | Delete; no experiment measures practical value |
| Future work lists multi-agent cooperation, real-world testbeds, and security without a link to the paper | Keep only directions that answer a stated limitation, ordered as a chain |
| Index terms add a term that the paper never uses | Reuse terms from the title and abstract |
| The abstract and the last contribution item report different baselines or ranges | Use one source row of the ledger for both |
| Numbers in the abstract still show pre-rerun values | Recheck every summary number against the regenerated artifacts |

## 10. Hard quality gates

- [ ] Every summary claim has a source sentence in the result sections and is no stronger than it.
- [ ] The abstract is one paragraph, follows the move order, defines every abbreviation, cites nothing, and stays inside the word limit.
- [ ] The abstract result move reports numbers, the instance or run scope, and the range over the best-performing baseline, without `the highest` or `superior`.
- [ ] The title has two colon-joined parts and stays in the word range; index terms run from application to solver.
- [ ] Contribution items follow scenario or model, formulation, algorithm; only the last carries a result sentence; none claims novelty by adjective.
- [ ] The Conclusion summarizes experiment groups in order with their scope and does not restate the contribution list.
- [ ] Future work is a chain tied to stated limitations; unrelated directions are deleted.
- [ ] Terms, numbers, directions, and scope phrases agree across all summary parts and the result sections after the latest rerun.
- [ ] The house-style band, banned constructions, and author voice are satisfied, or every deviation is recorded.

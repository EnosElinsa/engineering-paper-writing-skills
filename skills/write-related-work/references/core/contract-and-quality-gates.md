# Evidence workflow, language rules, and quality gates

## Contents

1. [Pre-draft evidence table](#pre-draft-evidence-table)
2. [Introduction-to-Related-Work traceability](#introduction-to-related-work-traceability)
3. [Recommended section patterns](#recommended-section-patterns)
4. [Sentence roles](#sentence-roles)
5. [Density rules](#density-rules)
6. [Solver-family subsections](#solver-family-subsections)
7. [Closing gap paragraph](#closing-gap-paragraph)
8. [Language and style](#language-and-style)
9. [Citation fidelity gates](#citation-fidelity-gates)
10. [Structural hard gates](#structural-hard-gates)
11. [Center-sentence audit](#center-sentence-audit)
12. [Gap-to-module audit](#gap-to-module-audit)
13. [Final compression pass](#final-compression-pass)

## Pre-draft evidence table

Create one row per evidence unit, not necessarily one row per citation:

| Citation(s) | Target subsection | Category criterion/value | Problem setting | Distinguishing mechanism | Capability established | Assumption or boundary relevant here | Confidence |
|---|---|---|---|---|---|---|---|

Rules:

- Use the paper text, source page, or verified notes; do not infer a mechanism from the title.
- Group citations only when they genuinely support the same clause.
- Mark uncertainty instead of converting it into a negative claim.
- If a citation does not support either a category capability or a boundary, remove it from the paragraph.

## Introduction-to-Related-Work traceability

Build a second matrix:

| Introduction claim | Related Work subsection | Evidence units | Class-level synthesis | Scenario/model/algorithm implication |
|---|---|---|---|---|

The Related Work may add detail, but it must not silently change the classification axis or gap asserted in the Introduction. If the evidence contradicts the Introduction, revise the claim rather than forcing the citations.

Add a citation-level matrix:

| Introduction category sentence | Citations | Related Work subsection and category label | Present? |
|---|---|---|---|

Default: every source that supports a classification category in the Introduction reappears under the same category label in Related Work. Background and application sources are exempt. Category labels are identical in the Introduction, the Related Work headings, and the closing gap. Deviate when a source is intentionally kept at category level only, and record each exception and its reason.

## Recommended section patterns

### Two-axis pattern

Use when the scenario literature and solver literature are the two main motivations:

1. opening map;
2. scenario/deployment/service mechanisms;
3. optimization/learning methods;
4. compact cross-axis synthesis.

### Three-axis pattern

Use only when a distinct state/task/communication mechanism needs its own evidence line and cannot be integrated into the scenario axis without mixing criteria:

1. opening map;
2. scenario architecture;
3. closest modeled mechanism;
4. solver family;
5. compact synthesis.

### Critical-analysis pattern

Use when two or more independent reviews must be intersected:

1. literature line A;
2. literature line B;
3. critical analysis that combines only their residual boundaries.

### Compact thematic pattern

Use when the literature set is small or the venue discourages many headings. Keep one center sentence per thematic paragraph and one closing comparison paragraph.

## Sentence roles

### Section opener

State the review axes and why they are the relevant axes. Keep it to one or two sentences.

Useful form:

> The work most relevant to this study falls into two lines: [scenario/mechanism line] and [solver line]. The former determines [paper-relevant capability], whereas the latter governs [paper-relevant difficulty].

### Classification sentence

Name the criterion before the category labels:

> According to [one criterion], existing approaches can be grouped into [A] and [B].

Avoid `Existing studies can be divided into several categories` without identifying the criterion.

### Representative-work sentence

Use one of these information orders:

- setting -> joint decisions/mechanism -> objective;
- mechanism family -> representative citations -> distinguishing assumption;
- closest work -> exact shared component -> exact mismatch.

Do not add experimental superiority unless it is itself the reason the work is representative.

### Category synthesis

Name the shared capability before the limitation:

> Collectively, these approaches enable [capability] by [shared mechanism]. Their formulations, however, assume [specific condition], which prevents them from representing [target consequence].

### Solver synthesis

Tie the limitation to problem structure:

> These methods respond to [generic change/constraint], but they do not preserve [dependency, matching condition, state transition, or terminal feasibility] created by [target mechanism].

## Density rules

- One paragraph has one primary class-level claim; subordinate center sentences are allowed only when they refine that claim.
- One cited work normally receives one sentence or one clause.
- Use two to four evidence units per category paragraph as a default, not a quota.
- Declare the range from the scale statement (reference measurement: 5–7 substantive paragraphs, about 635–987 English words). Default: stay inside it; deviate when additional independent boundaries genuinely require more, and record the reason. When more than 20% over the upper bound, apply the compression order of the reader and terminology contract: merge papers that share a predicate, drop paper-level numbers, cut announcement sentences, and keep one expanded closest work.
- Group papers sharing a mechanism instead of repeating the same predicate.
- Expand the closest work only enough to establish the exact overlap and mismatch.
- Assign each closest-work limitation to one primary subsection. Reuse the citation elsewhere only for a different analytical fact, not to repeat the same comparison.
- Do not report architecture layers, hyperparameters, data sets, or numerical gains unless they define the comparison.
- Let citations support sentences; do not let citation counts determine paragraph length.

## Solver-family subsections

Declare one axis per solver-family subsection, chosen as the single difficulty the paper's method addresses (for example, hybrid-action reinforcement learning: how hard constraints are enforced; dynamic evolutionary optimization: how the population responds to change). Other dimensions (action representation, state encoding, decision process) appear as one-clause attributes of a work, not as parallel categories.

Self-test: can every cited work be placed in exactly one category by reading only what it does on that axis? If not, change the axis or split the subsection.

Hard gate: a subsection whose categories mix two or more of {action representation, constraint handling, state encoding, decision process} fails.

Evidence status: this rule is extrapolated from the MECE principle and from the dynamic-evolutionary-algorithm subsection of the multi-source fusion benchmark paper, which is organized on one axis. It is not measured from a reinforcement-learning subsection of any benchmark paper.

## Closing gap paragraph

Default: restate the Introduction's gap once, in at most three sentences and in different words, and add what the Introduction cannot: paper-level evidence or the consequence in the target setting. Deviate when a venue requires a standalone summary, and record the reason.

Fail if any sentence shares a run of eight or more identical consecutive words with the Introduction. The eight-word threshold is a heuristic, not a measured value; use it to find copied sentences, not to reject a legitimate shared technical phrase.

## Language and style

Prefer concrete mechanism nouns: `fixed resource allocation`, `event-dependent sampling`, `state-dependent feasible region`, `redundant execution`, and `terminal safety constraint`.

Use restrained comparative verbs: `assumes`, `models`, `optimizes`, `couples`, `omits`, `fixes`, `does not represent`, `does not jointly account for`.

Avoid vague stock language: `many scholars`, `various studies`, `with the rapid development`, `has attracted widespread attention`, `still faces many challenges`.

Avoid adversarial caricatures. First state what a research line accomplishes, then delimit the assumption under which it operates.

Use transition words only when they encode logic. Repeated `However`, `Moreover`, and `Furthermore` cannot substitute for category structure.

Keep terminology aligned with the system model. Do not alternate among technically distinct operations merely for variety; define each relationship before using neighboring terms as synonyms.

## Citation fidelity gates

Fail the section if any answer is `no`:

1. Can every mechanism attributed to a paper be located in that paper or a verified source note?
2. Does every grouped citation support the same proposition?
3. Is every negative comparison framed within the reviewed setting rather than as a universal absence claim?
4. Are closest-work differences based on comparable objects, decisions, and assumptions?
5. Are all citation keys valid in the manuscript bibliography?
6. Does the temporal wording match the source status (published, early access, preprint, or draft)?
7. Does every sentence with a universal or negative claim carry a claim-type tag (L, D, R, K) from the reader and terminology contract? A D-type claim states its premise and is not cited; for the penalty-term example, cross-reference the constraint-handling semantics table in the write-methods skill instead of citing a paper.

## Structural hard gates

Fail and revise if any of the following occurs:

- a subsection lacks a declared comparison axis;
- category labels overlap under that axis;
- a paragraph starts with a paper list and ends without a class-level synthesis;
- a limitation introduces a mechanism not described in the preceding evidence;
- the Related Work repeats the Introduction's background or full scenario description;
- the final paragraph describes the proposed algorithm in implementation detail;
- an algorithm subsection lists method names without identifying the target structural mismatch;
- one closest paper consumes disproportionate space without changing the class-level conclusion.
- the same closest-work description or limitation is repeated under multiple axes;
- a solver-family subsection mixes two or more axes (see Solver-family subsections);
- a closing-gap sentence shares a run of eight or more identical consecutive words with the Introduction (heuristic threshold);
- a source that supports a classification category in the Introduction is missing from the same category in Related Work with no recorded exception.

## Center-sentence audit

Extract the opener and every paragraph's first sentence. They must answer, in order:

1. Which literature lines matter?
2. By what criterion is the first line classified?
3. What does each category do?
4. What boundary remains?
5. What algorithm family is relevant?
6. What target dependency or feasibility condition remains unsupported?

If the extracted sentences do not form a coherent story, repair paragraph order before sentence-level polishing.

## Gap-to-module audit

For each claimed paper module, require exactly one supported antecedent:

| Paper module | Literature boundary that motivates it | Evidence paragraph | Duplicated elsewhere? |
|---|---|---|---|

Merge duplicate gaps. Remove modules that appear only because they are in the contribution list. Related Work justifies why a module is needed; it does not prove the module works.

## Final compression pass

For every sentence, ask:

1. Does it establish the category, evidence, synthesis, boundary, or transition?
2. Would removing a technical detail weaken the comparison?
3. Is the same limitation stated elsewhere at the same resolution?
4. Can two papers with the same mechanism share one predicate?

Delete or merge sentences that fail these tests. The target is evidence density, not citation density.

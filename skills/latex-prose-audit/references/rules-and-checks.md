# Fine-grained prose and LaTeX rules

## Contents

1. [How to apply the rules](#how-to-apply-the-rules)
2. [Category A: semantic roles and reference](#category-a-semantic-roles-and-reference)
3. [Category B: sentence-level English](#category-b-sentence-level-english)
4. [Category C: mathematical and artifact prose](#category-c-mathematical-and-artifact-prose)
5. [Category D: LaTeX source integrity](#category-d-latex-source-integrity)
6. [Finding format and priorities](#finding-format-and-priorities)

## How to apply the rules

Audit the grammatical subject and main verb before scanning for individual
words. A matched word is only a candidate. Read the complete sentence, its
referent, and the neighboring equation, algorithm, table, figure, or citation
before reporting a violation.

Use [reference-prose-analysis.md](reference-prose-analysis.md) for calibrated
examples and counterexamples from the supplied author manuscripts,
evolutionary-algorithm papers, and additional constrained-optimization papers.
Examples verify the rules; they are not manuscript-specific templates.

## Category A: semantic roles and reference

### Rule 1: inanimate-noun-as-agent

#### 1.1 Core rule

Only an entity that actually decides or executes the complete operation should
take a volitional or result-achievement verb. Valid intentional agents include:

- an algorithm or named algorithm instance;
- a controller, optimizer, learner, decision maker, UAV, server, or modeled
  physical actor;
- the authors (`we`) when describing an author action; and
- a system only when the sentence means its controller or executing entities.

The following are not independent intentional agents:

- algorithm parts: mechanism, module, operator, selector, evaluator, decoder,
  repair, strategy, framework, procedure, process, stage, phase, step, branch,
  and line;
- evidence objects: metric, indicator, test, value, result, data, trend, table,
  figure, curve, equation, section, and experiment; and
- mathematical or physical objects: objective, constraint, formulation,
  representation, population, archive, state, path, and cost.

Do not let those subjects `decide`, `select`, `optimize`, `generate`,
`calculate`, `compute`, `evaluate`, `update`, `reconstruct`, `maintain`,
`preserve`, `achieve`, `ensure`, `guarantee`, `prove`, `confirm`, `validate`,
`demonstrate`, `enable`, `restrict`, `eliminate`, or `address` a research
problem. Move the action to the algorithm/controller or use passive voice.
This is a subject-role rule, not a ban on the verbs themselves.

#### 1.2 Algorithm part versus algorithm

Use the complete algorithm as the agent when describing an executed action:

- Avoid: `The mechanism selects the best schema.`
- Prefer: `The proposed algorithm uses the mechanism to select the schema with
  the lowest constraint violation.`

- Avoid: `The strategy generates feasible solutions.`
- Prefer: `The algorithm generates candidate solutions according to the
  strategy.`

Use passive voice when the executor is clear or unimportant:

- `Candidate solutions are regenerated according to the dependency order.`
- `Infeasible individuals are replaced during feasibility injection.`

A component may use only structural verbs such as `consists of`, `comprises`,
`contains`, `is configured with`, `is designed to`, `is applied to`, and `serves
as`. Do not make it the grammatical actor merely because it implements the
operation.

#### 1.3 Stage, step, phase, line, and subsection

`Stage 2`, `Step 3`, and `Lines 8--12` are locators, not executors:

- Avoid: `Stage 2 generates the offspring and updates the archive.`
- Prefer: `In Stage 2, the algorithm generates the offspring and updates the
  archive.`

- Avoid: `Step 3 calculates the reward.`
- Prefer: `In Step 3, the learner calculates the reward.`

- Avoid: `Lines 8--12 preserve the feasible individuals.`
- Prefer: `The algorithm preserves the feasible individuals in Lines 8--12.`

The same rule applies to `the initialization phase`, `the main loop`, `this
subsection`, and `Section IV`. Use `In ...` or `During ...` for location.

#### 1.4 Metrics, tests, data, and results

- Avoid: `HV assesses solution quality.`
- Prefer: `HV is employed to assess convergence and diversity.`

- Avoid: `The Wilcoxon rank-sum test confirms the improvement.`
- Prefer: `Results from the Wilcoxon rank-sum test show a statistically
  significant difference in HV.`

- Avoid: `The 100\% FR shows the robustness of the algorithm.`
- Prefer: `A 100\% FR means that every run produced a feasible solution under
  the tested settings.`

- Avoid: `The results validate the effectiveness of the mechanism.`
- Prefer: `The results show that the algorithm achieved lower IGD after the
  mechanism was added.`

`Results show/indicate/suggest` is an accepted neutral reporting convention.
`Table presents`, `Fig.~\ref{...} shows`, and `Eq.~(\ref{...}) defines` are
limited presentational metonymy. They do not demonstrate superiority, confirm
robustness, prove convergence, or validate a mechanism.

### Rule 2: canonical terminology and abbreviation

#### 2.1 One referent, one role

Build a table containing each central term, referent, grammatical role, and
abbreviation. Use these roles unless the manuscript defines a different one:

| Role | Default term |
|---|---|
| Complete executable optimizer | `algorithm` |
| Decision-making/executing entity | `controller`, `system`, `HAP`, `UAV` |
| Structural design | `framework` |
| Structural component | `mechanism`, `module` |
| Response or selection policy | `strategy` |
| Ordered operations | `procedure`, `process` |
| Part of an ordered procedure | `stage`, `phase`, `step` |
| Experimental configuration | `mode`, `variant` |
| Mathematical problem element | `objective`, `constraint` |
| Measured quantity | `metric`, `indicator` |

Do not alternate `mechanism`, `strategy`, `method`, `approach`, and `framework`
for stylistic variety. For the paper's own contribution, use `algorithm` for
the executable entity and `mechanism/module` for its structural part. Reserve
`method` or `approach` for a broader family, a cited prior work, or a term the
paper explicitly defines.

#### 2.2 Abbreviation contract

- Define `long form (ABBR)` at the first natural use in each independently
  readable document.
- Then use the short form consistently; do not repeatedly re-expand it.
- Flag competing expansions, singular/plural drift, inconsistent hyphenation,
  and an acronym used only once without a venue-required reason.
- An abstract or supplement may define the same abbreviation locally.
- Keep terms such as `CMOP/CMOPs`, `multi-objective`, and
  `constraint-handling` stable.

#### 2.3 Variant and formal referents

Use `algorithm with CDP` or `algorithm using CDP`, not `ALGO+CDP` or
`ALGO/CDP`, except for an explicitly defined table or figure label. Keep
objective, metric, constraint, path, trajectory, cycle, time slot, generation,
and iteration distinct.

### Rule 3: articles and determiners

#### 3.1 The definite article is a reference decision

Use `the` when the reader can identify one unique entity from the paper's
definitions or immediate context. This includes:

- the object just introduced: `a mechanism` -> `the mechanism`;
- the single contribution proposed by the paper: `the proposed algorithm`,
  `the proposed mechanism`; after writing `a proposed algorithm` at first
  mention, use `the proposed algorithm` for that same contribution;
- a defined mathematical object: `the objective function`, `the constraint in
  Eq.~(8)`, `the final population`;
- a unique result or artifact already named: `the HV value in Table III`,
  `the representative run`, `the previous population`; and
- a specific noun modified by a restrictive phrase: `the algorithm with CDP`,
  `the normalization defined in Eq.~(8)`, `the UAV assigned to region $j$`.

Do not remove `the` merely because a noun is abstract. Ask whether the phrase
means a class or operation in general, or the particular object defined in this
manuscript. Use `the` for the latter.

#### 3.2 Zero article for names, classes, and generic operations

Use no article before a proper algorithm name, acronym, dataset, or benchmark
identifier: `MTCMO is employed on CMOP1`; `SGCMOEA is compared with TDCEA`.
Use `the MTCMO variant`, `the CMOP formulated in Section III`, or `the TDCEA
results` when a common noun or restrictive phrase makes the reference specific.

Use zero article for a generic operation or property: `during optimization`,
`for normalization`, `computational efficiency`, and `constraint
satisfaction`. Use `the` for a defined instance: `the optimization in
Algorithm~1` or `the computational efficiency reported in Table III`.

#### 3.3 Numeral-quantified nouns

Do not insert `the` between `all/both` and a numeral-quantified noun:

- `all six test problems`, not `all the six test problems`;
- `all three DCMOPs`, not `all the three DCMOPs`.

This does not invalidate `both the HAP and the UAVs`, where `both ... and ...`
coordinates two specific noun phrases.

#### 3.4 First mention and back-reference

Use `a/an` for a newly introduced countable noun and select the article by
pronunciation: `an energy-consumption objective`, `a UAV` (/juː/), and `an
unmanned aerial vehicle`. After first introduction, use `the` for the same
specific entity. Keep the article when it disambiguates a defined object.

### Rule 4: neutral evidence reporting and claim strength

#### 4.1 Reporting verbs form a strength ladder

| Evidence | Prefer | Do not infer automatically |
|---|---|---|
| Descriptive values or one figure | reports, presents, shows, is higher/lower | proves, validates, guarantees |
| Pattern across runs | indicates, suggests, is consistent with | confirms causation |
| Controlled comparison or ablation | supports the contribution of, is attributable to under the tested control | proves universally |
| Theorem or construction | guarantees, establishes, proves under stated assumptions | scope beyond assumptions |

Name the metric, comparator, case, and direction. `Superior performance`,
`effectiveness`, `robustness`, and `viability` are incomplete without those
objects.

#### 4.2 Statistical and practical significance

`Significant` means statistically significant only when the test, comparison,
independent unit, direction, and threshold are supplied. Otherwise state the
numerical change. Distinguish `15\% relative increase` from `15 percentage
points`, and mean, median, best, and representative values.

- Avoid: `A significant improvement of 15\% is observed.`
- Prefer: `HV increased by 15\% relative to the baseline, from X to Y.`
- If tested: append `The difference was statistically significant under the
  Wilcoxon rank-sum test at $\alpha=0.05$.`

#### 4.3 Observation before interpretation

Write values or the visual pattern before explaining it. A figure may show
similar curves; it does not establish identical search dynamics. Use `may be
explained by`, `is consistent with`, or `reflects` when a mechanism was not
isolated.

#### 4.4 Exact logical strength and stated scope

A hedge is correct only when the claim is uncertain. When a consequence
follows from the paper's definitions, state it exactly.

- Avoid: `Historical information may be insufficient to restore feasibility.`
- Prefer: `Adapting candidates from historical information alone does not
  guarantee feasibility under the updated constraints.`

A result read from selected runs, one instance set, or one parameter range
names that scope in the sentence (`in the selected runs`, `on the tested
instances`). Flag a closing value judgment (`shows the practical value of`)
that no defined criterion supports.

## Category B: sentence-level English

### Rule 5: verb choice and collocation

#### 5.1 Prefer direct verbs

| Avoid | Prefer |
|---|---|
| performs decision-making | selects / decides |
| conducts an evaluation of | evaluates |
| performs the calculation of | calculates |
| provides an improvement in HV | improves HV |
| makes a comparison between | compares |
| carries out optimization of | optimizes |
| has the ability to adapt | can adapt |
| is responsible for the generation of | generates |

Do not remove a noun that names the scientific object, such as `fitness
evaluation`, `resource allocation`, or `constraint-handling mechanism`.

#### 5.2 Actor–verb pairs

- authors: `formulate`, `propose`, `design`, `adopt`, `conduct`, `analyze`;
- algorithm/controller: `generate`, `select`, `update`, `allocate`, `execute`,
  `return`, `outperform`;
- physical actors: `move`, `dispatch`, `collect`, and `fly`;
- tables/figures/equations: `present/report`, `show/plot/illustrate`, and
  `define/express`;
- metrics: `are used/employed to measure`;
- results: `show/indicate/suggest`.

#### 5.3 Technical collocations

Prefer `satisfy a constraint`, `find a feasible solution`, `approximate the
Pareto front`, `maintain population diversity`, `improve convergence`,
`allocate bandwidth`, `generate offspring`, `update the archive`, `compare A
with/against B`, and `outperform B on metric M`.

Use `reach Pareto optimality`, `ensure feasibility`, `find the optimal
solution`, or `eliminate computation` only when the stated guarantee or exact
operation supports it.

#### 5.4 Promotional wording

Replace `revolutionizes`, `fundamentally advances`, `breakthrough`,
`intelligently`, `remarkable`, `plug-in`, `the nature of`, and `paradigm` when
a plain technical description is available. Retain a word when it is a defined
technical term.

### Rule 6: modifiers, qualifiers, and numerical claims

#### 6.1 Empty intensifiers

Flag `respective`, `fundamental`, `critical`, `essential`, `key`, `advanced`,
`comprehensive`, `effective`, `efficient`, `robust`, `superior`, `optimal`,
`notably`, `remarkably`, `substantially`, `significantly`, `effectively`, and
`indeed` when they add no measurable or technical distinction.

Retain a modifier when the next phrase supplies its content, for example
`critical safety constraint`, `statistically significant under the Wilcoxon
test`, `computationally efficient with complexity $O(...)$`, or `robust across
the tested uncertainty levels`.

#### 6.2 Let exact values carry the comparison

- Avoid: `a remarkable 76-fold speedup`.
- Prefer: `a 76-fold speedup`.
- Avoid: `near-perfect levels of 99.7\%`.
- Prefer: `99.7\%`.
- Avoid: `only a 5\% reduction` unless an acceptance threshold is defined.

State the baseline and denominator. Preserve reported precision and do not
create more significant digits than the source supports.

Flag vague quantity words (`few`, `most`, `negligible`, `almost all`,
`rarely`) when the artifact contains the measured value, and replace them
with the bound (`the mean rate remains below 3\% on all instances`).

#### 6.3 Modifier attachment and noun stacks

Keep modifiers adjacent to what they modify. Break a stack such as `dynamic
constraint handling strategy selection mechanism` into an `of` phrase or two
sentences. Hyphenate compound modifiers before a noun (`energy-oriented
strategy`, `real-time decision`, `state-augmented model`) but not after an
`-ly` adverb (`dynamically selected strategy`).

### Rule 7: pronouns, relative clauses, and parentheticals

#### 7.1 Explicit antecedents

Replace `the above`, `the aforementioned`, `the former`, `the latter`, `this`,
`these`, and `such` when more than one antecedent is plausible. Prefer `the
previous population`, `these three constraints`, or `the HV results`.

#### 7.2 `which` and `where`

Flag `which` when more than one noun or full proposition could be its antecedent.
Split the sentence or repeat the noun. Use `where` for a real location or a
clearly defined mathematical condition; use `in which` or `for which` when
`where` would attach ambiguously.

#### 7.3 Parentheticals

Reserve parentheses for notation, coordinates, units, abbreviations,
equation/figure/table references, statistical values, and compact variant
labels. Move long caveats, motivation, and complete qualifications into a
sentence. Put citations after the supported proposition rather than inside an
informal `(see \cite{...})` aside.

#### 7.4 `respectively`

Use `respectively` only for two equal-length, visibly parallel lists with an
unambiguous order. Otherwise write the pairings explicitly.

### Rule 8: tense, voice, and parallelism

#### 8.1 Tense

- Present tense: paper content and stable definitions (`Section IV presents`,
  `Eq.~(8) defines`, `the algorithm uses`).
- Past tense: completed experimental actions (`We conducted 30 runs`).
- Within one result paragraph, choose a consistent pattern such as `Table III
  reports that the algorithm achieved...` or present tense throughout.
- Future tense: actual future work only.

#### 8.2 Active and passive voice

Prefer active voice when the executor matters: `The controller allocates the
bandwidth.` Use passive voice to prevent false agency or when the process
matters: `Bandwidth is allocated according to Eq.~(8).` Do not use passive
voice to hide an undefined executor or missing comparison.

#### 8.3 Parallel lists

Coordinate like grammatical forms: `minimizing energy consumption and reducing
delay`, or `energy-consumption minimization and delay reduction`. Do not mix
infinitives, gerunds, and nominalizations in one list. Keep contribution
openings parallel (`We formulate`, `We design`, `We evaluate`).

### Rule 9: sentence economy and repetition

#### 9.1 One principal claim per sentence

Split a sentence that contains several independent `which`, `where`, `while`,
`thereby`, or `and` branches. Keep necessary causal chains intact, but make the
actor and result visible in each clause.

#### 9.2 Remove duplicate meaning

- `practical viability and practical applicability` -> choose one;
- `improves and enhances performance` -> choose the measurable verb;
- repeated metric values in the takeaway after the data sentence -> state the
  conceptual conclusion only;
- `the replacement rate parameter $p_r$` -> `the replacement rate $p_r$`;
- `focuses exclusively on` when nothing else could be included -> `focuses on`;
- `In this equation, $X$ is ...` after a display -> `where $X$ is ...`;
- a sentence that restates a table's values or the previous sentence -> delete.

Name one quantity with one term in every document of the submission
(manuscript, supplement, response letter). Two names for one quantity
(`repositioning energy` and `flight energy`) are a High finding even when
each is correct in isolation.

#### 9.3 Avoid empty lead-ins

Replace `It is worth noting that`, `It can be clearly seen that`, `Based on the
above analysis`, `From the nature of`, `Obviously`, and `As is well known` with
the fact, condition, or result itself.

## Category C: mathematical and artifact prose

### Rule 10: mathematical notation conventions

These are semantic conventions shared by the supplied papers. The exact macro
choice (`\mathbf`, `\boldsymbol`, `\bm`, `\mathbb`, `\mathcal`, or `\mathscr`)
may follow the target template; consistency is mandatory, but one macro family
is not universal.

#### 10.1 Object classes

- scalar variables and parameters: italic math letters, such as `$x$, $N$,
  and $\alpha$`;
- vectors: bold lowercase, such as `$\mathbf{x}$` and `$\mathbf{r}_t$`;
- matrices/tensors: bold uppercase or the paper's declared tensor convention,
  such as `$\mathbf{H}$`;
- sets, populations, archives, and domains: blackboard or calligraphic style,
  such as `$\mathbb{S}_t$`, `$\mathcal{P}$`, or `$\mathcal{D}$`;
- functions and objective/constraint values: stable italic function symbols,
  such as `$f_i(\mathbf{x})$` and `$g_i(\mathbf{x})$`;
- named operators and textual states: upright style, such as `$\mathrm{LoS}$`,
  `$\mathrm{UAV}$`, `$\max$`, or `$\operatorname{arg\,min}$`.

Do not use bold, blackboard, calligraphic, or upright styling merely for visual
emphasis. One symbol must retain one object class and meaning.

#### 10.2 Indices, labels, and domains

Use subscripts for entity, time, region, or component indices and superscripts
for a declared mode, direction, stage, or quantity type. Use upright text in a
subscript when it is a semantic label (`T^{\mathrm{HAP}}`, `p^{\mathrm{RX}}`),
and italic when it is a mathematical index (`x_i`, `f_j`). Define index sets,
domains, and units before or immediately after the first formula. Distinguish
an index from the number of indexed objects (`i` versus `I`) and a time index
from a generation or training counter.

#### 10.3 Sets, sequences, and tuples

Use set notation for unordered membership and braces for sets; use parentheses,
brackets, or an indexed sequence for ordered paths, trajectories, schedules,
and action histories. If a compressed sequence is used, define the raw sequence,
the compressed sequence, and their mapping. Do not use a set where an operation
depends on order or repeated entries.

#### 10.4 Functions, operators, and conditions

Use `\sum`, `\min`, `\max`, `\arg\min`, `\Pr`, and `\mathbb{E}` consistently;
use `\operatorname{}` or `\mathrm{}` for named operators and semantic labels.
Write words in equations with `\text{...}` only for conditions or prose such
as `if` and `otherwise`. Keep logical relations (`\in`, `\subseteq`, `\leq`,
`\forall`) distinct from explanatory text.

#### 10.5 Formula semantics

Check dimensions, units, domains, indices, degree/order conventions, endpoint
and boundary definitions, and whether a formula produces the object named in
the surrounding prose. When introducing a discretization, compression,
surrogate, or lookup, compare predicates, weights, aggregation cardinality,
sampling, ordering, and cost with the original formulation before calling it an
exact replacement.

### Rule 11: equations, algorithms, figures, tables, and captions

#### 11.1 Equations

Use the sequence `quantity and purpose -> display -> new-symbol definitions ->
next use`. Prefer `X is calculated as` or `Eq.~(8) defines X`; avoid `The
equation calculates X` when the equation is not an actor. Displayed equations
are part of the sentence: use a comma when the sentence continues and a period
when it ends.

#### 11.2 Algorithms

Use line references as anchors after the operation:

- Prefer: `The algorithm initializes the population (Lines 1--4).`
- Avoid: `Lines 1--4 initialize the population.`

Use `In Step 2` or `During the approximation stage`, followed by the real
executor. Keep `Input`, `Output`, loop bounds, branch conditions, updates, and
return objects consistent between pseudocode and prose.

#### 11.3 Figures and tables

- `Table III presents/reports/summarizes...`;
- `Fig.~4 shows/plots/illustrates...`;
- the x-axis `represents` or `denotes` a variable;
- a curve `increases/decreases/remains`, while the algorithm `converges`;
- a value or metric `indicates` a narrowly defined state.

Do not use `Fig.~4 demonstrates superiority`; state the visual difference and
put the statistical comparison in a separate result sentence.

#### 11.4 Captions

Captions identify the artifact, variables/cases, and representative-run rule
when needed. They do not reproduce the result paragraph or explain the entire
method. Use parallel templates for related panels, compact relationship wording
such as `Comparison of A and B`, and LaTeX en-dash ranges such as
`Figs.~3(a)--(c)`.

### Rule 12: numbers, units, ranges, and typography

- Keep a non-breaking space between a number and unit using the target's
  convention: `100~m`, `150~s`, `200~kJ`, or the class-supported equivalent.
- Use `--` for LaTeX en-dash ranges: `97\%--100\%`, `10--20~s`, and
  `Figs.~3(a)--(c)`.
- Use `\times` for multiplication and scientific notation: `$9.11 \times 10^4$`.
- Group long numbers consistently, normally `$10\,000$` in math.
- State a metric's direction once: lower IGD/runtime are better; higher HV/
  feasibility rate are better.
- Match singular/plural to the number and unit: `1 UAV`, `2 UAVs`, `1 second`,
  `0.1 seconds` under the target style.
- Keep decimal precision and percent formatting consistent within a table and
  its prose.

## Category D: LaTeX source integrity

### Rule 13: LaTeX-safe editing

#### 13.1 Parse before editing

Separate prose from comments, command names and arguments, labels, citation
keys, math, macro definitions, algorithm code, and verbatim/listing blocks.
Never run an ordinary prose replacement through those regions.

#### 13.2 References, labels, and citations

- Confirm every active `\ref`, `\eqref`, `\cite`, and `\pageref` target exists
  under the target build; ignore commented examples.
- Preserve the target's native citation commands (`\cite`, `\citep`,
  `\citet`) and punctuation.
- Place a citation after the smallest supported proposition. Key existence is
  not source support; inspect the source passage or mark the check
  `UNRESOLVED`.
- Preserve existing label names unless renaming is required and every reference
  is updated. Use prefixes such as `eq:`, `fig:`, `tab:`, `sec:`, and `alg:` when
  the project already uses them.

#### 13.3 Math, spacing, macros, and compilation

Check non-breaking spaces before figure, table, section, equation, algorithm,
and unit references when the class convention requires them. Keep inline math,
display math, vectors, matrices, sets, operators, units, and equation
punctuation consistent with the target source. Inspect URL line breaking only
when the layout makes it relevant. Preserve custom macros and compile with the
project's documented engine after an authorized edit. A static scan cannot
prove that a LaTeX change compiles or that a rendered caption/equation is correct.

## Finding format and priorities

Use:

| Priority | File:line | Sentence fragment | Rule | Why it fails | Minimal correction |
|---|---|---|---|---|---|

- **High:** false agency that changes meaning; unsupported guarantee;
  terminology, symbol, unit, equation, or citation attachment that changes the
  referent; or a mathematically invalid object/operation distinction.
- **Medium:** inanimate-agent wording with a clear intended correction; article,
  collocation, modifier, relative-clause, tense, caption, or result-reporting
  defect that impairs precision.
- **Low:** local punctuation, hyphenation, spacing, or optional compression.

For each finding, quote the smallest phrase and give the smallest safe fix. If a
verb, article, symbol, or formula depends on an unknown implementation, proof,
or venue convention, mark it `UNRESOLVED` and state what must be checked.

# Fine-grained reference prose analysis

## Contents

1. [Corpus and extraction policy](#corpus-and-extraction-policy)
2. [Subject and verb agency](#subject-and-verb-agency)
3. [Articles and determiners](#articles-and-determiners)
4. [Terminology and abbreviations](#terminology-and-abbreviations)
5. [Verbs, nominalizations, and collocations](#verbs-nominalizations-and-collocations)
6. [Modifiers and numerical language](#modifiers-and-numerical-language)
7. [Pronouns, clauses, and parentheticals](#pronouns-clauses-and-parentheticals)
8. [Mathematical notation](#mathematical-notation)
9. [Algorithms, equations, figures, and captions](#algorithms-equations-figures-and-captions)
10. [Tense, voice, and parallelism](#tense-voice-and-parallelism)
11. [Cross-corpus conclusions](#cross-corpus-conclusions)

## Corpus and extraction policy

The rules were checked against the supplied local corpus consisting of the
following author manuscripts:

- *HAP-UAV Coordination for Data Collection in Low-Altitude Economy Networks:
  A Feasibility-Driven Dynamic Constrained Multi-Objective Evolutionary
  Approach*;
- *An Efficient Constrained Multi-Objective Evolutionary Algorithm With a
  Spatial Discretization Evaluation Mechanism for Unmanned Aerial Vehicle Path
  Planning*.

The four evolutionary-algorithm papers are:

- *Demand-Aware Multi-Area Multi-UAV Empowered Mobile Edge Computing: A Joint
  Energy and Delay Optimization*;
- *Joint Latency and Charge Cost Minimization for Reliable Task Offloading in
  Dispersed Computing: A Multi-Objective Optimization Approach*;
- *Terrain-Aware UAV-Enabled Mobile Edge Computing in Urban Environments: A
  Constrained Multi-Objective Approach With Task-Adaptive Mechanism*;
- *UAV-Enabled Multi-Source Data Fusion in Vehicular Networks: A Joint
  Optimization Approach for Reliability and Latency*.

The five additional constrained-optimization papers are:

- *A Schema-Guided Constrained Multi-Objective Optimization Evolutionary
  Algorithm for Multiple Uncrewed Aerial Vehicle Path Planning*;
- *Learning-Based Temporal Sequence of Constrained Handling Selection for
  Constrained Multi-objective Evolutionary Optimization*;
- *Microscale Searching-Based Dynamic Constrained Multi-Objective Optimization
  for Uncrewed Aerial Vehicle Path Planning in Unknown Environments*;
- *Microscale-Searching Constrained Evolutionary Optimization for
  Diversity-Distribution-Guided Image Augmentation*;
- *Strategy Selection in Dynamic Constrained Multi-Objective Optimization via
  State-Augmented Deep Reinforcement Learning*.

The separate `reinforcement-learning/` corpus is excluded. The five additional
papers remain useful because they belong to the same authoring lineage and
provide counterexamples and later writing variants.

This file records source-grounded language observations, not commands to copy
published sentences. Each observation is promoted to a rule only when it
recurs across documents, agrees with the author-manuscript correction history,
or prevents an identifiable ambiguity. Source weaknesses are rewritten into
generic examples rather than treated as acceptable style.

### Evidence map

| Fine-grained rule | Repeated source locations used for verification |
|---|---|
| Inanimate components, stages, metrics, and tests need a host or neutral frame | HAP-UAV `main.tex:440--487,648--703`; CMOEA-SDEM `RevisedManuscript.tex:366--370,571,646`; all four evolutionary papers' method/result sections |
| `all + numeral` and proper-name articles | HAP-UAV `main.tex:603--646`; CMOEA-SDEM `RevisedManuscript.tex:544--571`; demand-aware `full.md:433--467`; dynamic-microscale `full.md:479--521` |
| Direct verbs, technical collocations, and role-specific nouns | HAP-UAV `main.tex:120--218,440--504`; dispersed-computing `full.md:234--404`; UAV-fusion `full.md:315--402` |
| Exact values, qualifiers, and trade-off wording | Demand-aware `full.md:445--493`; terrain-aware `full.md:576--797`; CMOEA-SDEM `RevisedManuscript.tex:591--807,995--1089`; image-augmentation `full.md:263--370` |
| Pronoun/relative-clause and parenthetical control | HAP-UAV `main.tex:120--218`; CMOEA-SDEM `RevisedManuscript.tex:180--297`; the Introduction and method sections of the nine Markdown papers |
| Equation, algorithm, figure, table, caption, range, and unit conventions | HAP-UAV and CMOEA-SDEM LaTeX source; the four evolutionary papers' algorithm/result sections; the five additional papers' algorithm/result sections |

The locations above are verification routes, not required runtime files. When
an audit needs an exact citation or line reference, inspect the user's supplied
source and report that local evidence.

### Representative source examples

The following short examples are paraphrased or limited excerpts used to test
the rules. They show how the same fine-grained issue recurs across different
papers; they are not templates to copy literally.

| Source location | Observed pattern | Generalized audit rule |
|---|---|---|
| HAP-UAV author manuscript, algorithm section (`main.tex:440--487`) | The HAP performs optimization and dispatches the resulting decisions; the response mechanism is described as a component of that procedure. | Keep the executing actor as the HAP/algorithm; use `the mechanism consists of...` for the component. |
| CMOEA-SDEM author manuscript, algorithm/evaluation sections (`RevisedManuscript.tex:366--370,475--526`) | `In Step 1...`, `In Step 2...`, and `In Step 3...` introduce operations, while the algorithm performs them. | Treat step/stage/line labels as locators and put the executor in the clause. |
| Demand-aware evolutionary paper, experimental section (`full.md:445--493`) | `Fig. 2 presents...`; the control center dispatches UAVs and the results are then interpreted. | Figures present artifacts; modeled controllers perform decisions; interpretations follow observations. |
| Dispersed-computing evolutionary paper, algorithm section (`full.md:234--404`) | A main population and an auxiliary population are initialized, updated, and compared across iterations. | Use `the algorithm initializes/updates...`; reserve `population` for state or object descriptions. |
| Terrain-aware evolutionary paper, method section (`full.md:412--550`) | The task-adaptive mechanism records operators and is applied to individuals; the proposed algorithm coordinates the search. | Distinguish the mechanism's structural role from the algorithm's executed action. |
| UAV-fusion evolutionary paper, problem/method sections (`full.md:315--402`) | Request response, data collection, and bandwidth allocation are named in dependency order. | Preserve one canonical term per decision and use direct verbs for the ordered operations. |
| Schema-guided additional paper, motivation/results sections (`full.md:64--73,539--564`) | A table reports constraint values, a figure visualizes paths, and a solution is compared under a defined criterion. | Let tables/figures report evidence; let the algorithm or comparison sentence state the judgment. |
| Temporal-sequence additional paper, experiment section (`full.md:369--453`) | `Table II presents...`; a Friedman ranking and IGD/HV values are interpreted afterward. | Separate artifact presentation, statistic, and interpretation; do not make the test confirm causality. |
| Dynamic-microscale additional paper, method/experiment sections (`full.md:365--405,479--582`) | The valid space is constructed in phases and the algorithm responds after an environmental change. | Introduce phase locations with `In ...`; name the algorithm as the actor and preserve tense. |
| Microscale image-augmentation additional paper, ablation section (`full.md:263--370`) | A table gives accuracy values, visualizations show transformations, and the text discusses a possible reason. | Distinguish quantitative observation, visual observation, and model-consistent explanation. |
| State-augmented additional paper, experiment section (`full.md:376--444`) | The paper reports significance across many instances and then attributes the pattern to adaptive selection. | Check test family, unit, effect size, and causal isolation before accepting `significant`, `robust`, or `confirms`. |

These examples are deliberately distributed across author manuscripts,
evolutionary-algorithm papers, and the additional `others/` papers. No example
from the separate `reinforcement-learning/` directory is used.

## Subject and verb agency

### Algorithms and modeled actors are valid agents

Across the corpus, the clearest operational sentences use a complete executor:

- the algorithm generates offspring, selects individuals, updates an archive,
  reconstructs a solution, or returns a population;
- a control center allocates UAVs and resources;
- a HAP selects a waypoint and dispatches UAVs;
- a UAV moves, collects data, or executes the selected decisions.

This supports the positive form:

> `In each generation, the algorithm generates an offspring population and
> updates the archive.`

### Components require an explicit host

The corpus often gives `mechanism`, `strategy`, or `framework` verbs such as
`selects`, `generates`, `ensures`, `enhances`, and `achieves`. The
author-manuscript rules and correction log identify this pattern as a recurring
problem. The reliable revision is:

> `The algorithm uses the mechanism to reconstruct infeasible individuals.`

or:

> `Infeasible individuals are reconstructed according to the mechanism.`

The component can still be described structurally:

> `The mechanism consists of diversity injection and feasibility injection.`

This distinction generalizes across solution reconstruction, task-adaptive
operators, microscale searching, schema handling, and dynamic response.

### Stages, steps, phases, and lines are locators

The manuscripts repeatedly describe algorithms by numbered stages and line
ranges. Stronger sentences use them as adverbials:

> `In the initialization phase, the algorithm evaluates the initial
> population (Lines 1--6).`

Avoid:

> `Stage 1 evaluates the population.`

The same rewrite applies to `Step 2 computes`, `Lines 8--12 preserve`, and
`Section IV analyzes`. A section may `present` material as a conventional
document subject, but it does not execute the method.

### Metrics and tests do not judge the paper

The evolutionary papers frequently define IGD, HV, FR, SR, runtime, and
Wilcoxon/Friedman tests. The author correction history explicitly replaces:

- `HV assesses ...` with `HV is employed to assess ...`;
- `The Wilcoxon rank-sum test confirms ...` with `Results from the Wilcoxon
  rank-sum test show ...`.

Likewise, a feasibility rate should be interpreted by definition:

> `A 100\% FR means that all runs produced feasible solutions under the tested
> settings.`

It should not be made to `show robustness` without defining robustness.

### Tables and figures have limited presentational agency

Across all corpora, `Table ... presents` and `Fig. ... shows/illustrates/plots`
are stable conventions. The problematic escalation is `Fig. ... demonstrates
superiority` or `Table ... validates effectiveness`. Rewrite the latter as the
observed comparison:

> `Table III reports lower mean IGD for the proposed algorithm than for the
> five baselines on all three test problems.`

This preserves accepted scientific metonymy without assigning judgment to the
artifact.

## Articles and determiners

### Proper algorithm and problem identifiers take zero article

The clean pattern is `MTCMO`, `TDCEA`, `CMOP1`, or `DCMOP3` without `the`.
Use `the proposed algorithm`, `the MTCMO variant`, or `the DCMOP formulated in
Section III` when the common noun or defining phrase requires a determiner.

### `all + numeral + noun` takes no `the`

The corpus contains repeated forms such as `all the three DCMOPs` and `all the
six benchmark problems`. The author correction log records the intended rule:

- `all six test problems`;
- `all three DCMOPs`.

This rule does not invalidate `both the HAP and the UAVs`, where two specific
noun phrases are coordinated.

### First mention and back-reference

Use `a/an` for a newly introduced countable object and `the` after the object
has been established. The correction history supplies the concrete article
pair `an energy-consumption objective`, while the papers provide recurring
first-mention sequences such as `a mechanism` followed by `the mechanism`. For
the paper's own contribution, introduce `a proposed algorithm` only once, then
refer to that unique contribution as `the proposed algorithm`.

Generic operations normally take zero article (`during optimization`, `for
normalization`); a defined instance takes `the` (`the normalization in
Eq.~(8)`).

### Avoid unnecessary articles in abstract qualities

The team papers repeatedly use article-heavy phrases such as `the convergence
and the diversity metrics`, `the constraint satisfaction`, and `the latency`
when the qualities are generic. Prefer `convergence and diversity`,
`constraint satisfaction`, and `latency` unless a specific metric or instance
has already been identified.

## Terminology and abbreviations

### Keep contribution roles distinct

The corpora use algorithm, framework, mechanism, strategy, process, procedure,
mode, and variant. The role distinction that survives across documents is:

- `algorithm`: complete executable optimizer;
- `framework`: structural design hosting populations or components;
- `mechanism/module`: structural component inside the algorithm;
- `strategy`: selection or response policy used by the algorithm;
- `process/procedure`: ordered sequence of operations;
- `mode/variant`: experimental configuration.

Synonym variation is not a virtue when it changes the referent. The correction
history rejects alternating `method/approach` with an established `mechanism`
or `algorithm` label.

### Abbreviations are document-local contracts

The references consistently define long form plus abbreviation, then use the
short form in the body. Audit repeated re-expansion, multiple expansions,
singular/plural drift, and a single-use acronym. Abstracts and independently
read supplements may define the same abbreviation locally.

### Variant typography

The correction history converts `NSGA-II+CDP` to `NSGA-II with CDP`. The same
rule applies to prose variants: use `algorithm with SDEM` or `algorithm using
CDP`; reserve compact signs for an explicitly defined table/figure label.

### Formal and physical referents must not drift

The papers repeatedly distinguish an objective from a metric, a path from a
trajectory, a slope from an angle, a time slot from a generation, a planning
cycle from an iteration, and a mechanism from its algorithm. Flag a synonym
when it crosses one of these semantic categories.

## Verbs, nominalizations, and collocations

### Direct verbs reduce ambiguity

The corpora contain nominalized constructions such as `performs
decision-making`, `conducts an evaluation of`, `provides an improvement`, and
`has the ability to`. The general revisions are:

- `selects/decides`;
- `evaluates`;
- `improves`;
- `can`.

Do not remove a noun that names the scientific object, such as `fitness
evaluation`, `resource allocation`, or `constraint-handling mechanism`.

### Stable actor–verb collocations

The strongest recurring pairs are:

- authors: `formulate`, `propose`, `design`, `adopt`, `conduct`, `analyze`;
- algorithm/controller: `generate`, `select`, `update`, `allocate`, `execute`,
  `return`, `outperform`;
- table/figure/equation: `present/report`, `show/plot/illustrate`,
  `define/express`;
- metric: `is used/employed to measure`;
- results: `show/indicate/suggest`.

### Constraint and Pareto language

Prefer `satisfy a constraint`, `find a feasible solution`, `approximate the
Pareto front`, `maintain diversity`, and `improve convergence`. `Reach Pareto
optimality`, `ensure feasibility`, or `find the optimal solution` requires a
guarantee stronger than ordinary evolutionary evidence.

### Comparison language

Use `compare A with/against B`, `outperform B on HV`, `reduce IGD by X\%`, and
`at the cost of higher energy`. Avoid `superior than`, `improved compared to`
without a metric, and `against` for an x-axis relation when `versus` or
`plotted against` is clearer.

## Modifiers and numerical language

### Published frequency does not legitimize filler

The papers contain many instances of `critical`, `fundamental`, `essential`,
`key`, `advanced`, `comprehensive`, `effective`, `efficient`, `robust`,
`superior`, `optimal`, `notably`, `remarkably`, `substantially`, and
`significantly`. Their frequency shows why a context rule is necessary, not
that they should be copied.

Retain a modifier only when the next phrase supplies its content:

- `statistically significant under the Wilcoxon test`;
- `computationally efficient with complexity O(...)`;
- `robust across the tested uncertainty levels`;
- `comprehensive across five listed experiment groups`.

Otherwise state the measurable difference.

### Exact numbers replace evaluative adjectives

The corpus supports direct forms such as `a 76-fold speedup`, `HV increased by
15\%`, and `FR was 100\%`. Remove `remarkable`, `near-perfect`, and `only`
unless the paper defines an acceptance threshold.

### Preserve measurement semantics

State the baseline and denominator of a percentage. Distinguish relative
percent from percentage points, mean from median, individual solutions from
independent runs, and a representative run from an aggregate result.

### Modifier stacks and hyphenation

The papers use established compounds such as `energy-oriented strategy`,
`real-time decision`, `state-augmented model`, `constraint-handling
technique`, and `multi-objective optimization`. Hyphenate them before a noun,
but do not hyphenate after an `-ly` adverb. Break a new stack when a reader
must decode more than two or three modifiers.

## Pronouns, clauses, and parentheticals

### Ambiguous reference is more serious than repetition

The corpus contains many `this/these/such`, `the above`, `the former/latter`,
and long `which` clauses. Replace them with the canonical noun whenever more
than one antecedent is available. Repeating `the previous population` is
better than an ambiguous `it`.

### Relative clauses need one antecedent

Split a `which` clause when it can modify the nearest noun or the whole prior
clause. Use `where` only for a location or a clearly defined mathematical
condition. A long mechanism, caveat, or causal explanation should become a
new sentence.

### Parentheses are for compact formal material

Across the LaTeX manuscripts, parentheses work well for abbreviations,
coordinates, equation/figure references, statistical values, and concise
variant labels. Move prose asides and complete qualifications into the
sentence. Place citations after the proposition rather than inside an
informal `(see ...)` aside.

### `respectively` requires parallel lists

The corpus uses `respectively` frequently in symbol definitions. Keep it only
when two lists have equal length and a visually obvious one-to-one order. If a
reader must count across a long sentence, define the pairings separately.

## Mathematical notation

The two author manuscripts and the evolutionary-algorithm papers use different
LaTeX macro packages (`bm`, `amsmath`, `amssymb`, `mathrsfs`, and related
commands), but their semantic convention is stable. The audit should preserve
the target paper's macro family while checking the object class and meaning.

### Object classes

- scalar variables and parameters use italic math letters (`x`, `N`, `\alpha`);
- vectors use bold lowercase (`\mathbf{x}`, `\mathbf{r}_t`, `\boldsymbol{\sigma}_t`);
- matrices or tensors use bold uppercase when the paper distinguishes them
  from vectors (`\mathbf{H}`);
- sets, populations, archives, and domains use blackboard, calligraphic, or
  script capitals (`\mathbb{S}_t`, `\mathcal{P}`, `\mathscr{D}`);
- objective and constraint functions use stable italic function symbols
  (`f_i(\mathbf{x})`, `g_i(\mathbf{x})`); and
- named operators, semantic labels, and units use upright text (`\mathrm{HAP}`,
  `\mathrm{LoS}`, `\max`, `\operatorname{arg\,min}`, `\mathrm{s}`).

The exact choice between `\mathbf`, `\boldsymbol`, `\bm`, `\mathbb`,
`\mathcal`, and `\mathscr` is template-dependent. Mixing styles for the same
object, or changing a symbol's class mid-document, is not.

### Indices and superscripts

The references use subscripts for entity, time, region, and component indices
(`x_i`, `r_t`, `b_{i,j}`), and superscripts for quantity type, mode, direction,
or semantic labels (`E^{\mathrm{HAP}}`, `p^{\mathrm{RX}}`). Distinguish a
mathematical index from its cardinality (`i` versus `I`) and a time index from a
generation or training counter. Use upright text for a semantic label and
italic for a mathematical index unless the target paper declares another
convention.

### Sets, tuples, and ordered sequences

Braces and blackboard/calligraphic symbols conventionally denote sets and
membership. Parentheses, brackets, or indexed lists denote ordered tuples,
paths, trajectories, schedules, and action histories. If a method compresses
an ordered sequence, define both the raw and compressed sequences and the
mapping between their elements; do not use set notation for an order-dependent
operation.

### Functions, operators, and conditions

Use standard operators (`\sum`, `\min`, `\max`, `\arg\min`, `\Pr`, `\mathbb{E}`)
consistently. Use `\operatorname{}` or `\mathrm{}` for named operators and
semantic labels, and `\text{...}` for words in conditions such as `if` and
`otherwise`. Define every symbol, index set, domain, and unit at first use or
immediately after the displayed formula.

### Dimensional and semantic consistency

Check that vector/matrix dimensions, index ranges, units, degree/order
conventions, and boundary cases agree between prose, equations, algorithms,
and notation tables. Common high-risk distinctions in the corpus include
objective versus metric, slope versus angle, path point versus cell center,
planning cycle versus generation, and evaluation count versus wall-clock time.

## Algorithms, equations, figures, and captions

### Algorithm prose uses line numbers as anchors

The clean form found across the algorithm sections is:

> `The algorithm initializes the population (Lines 1--6).`

Use `In Step 2` or `During the approximation stage` before naming the
algorithm/controller as executor. Keep line references after the operation;
do not make `Lines 1--6` perform it.

### Equation prose follows quantity -> display -> definitions -> use

The references normally introduce the quantity and then use `is calculated
as`, `is defined as`, or `is formulated as`. After the display, define only
new symbols and state the next consumer. Punctuate displayed equations as part
of the sentence.

Use `Eq.~(8) defines X` as presentational shorthand, or `X is defined in
Eq.~(8)`. Avoid `the equation calculates X`.

### Figures and tables report rather than judge

The stable forms are:

- `Table III presents the comparison results.`
- `Fig.~4 plots the convergence curves.`
- `The x-axis represents the function evaluation count.`

Replace `Fig.~4 demonstrates the superiority` with the precise visual
observation. Put statistical claims in a separate result sentence.

### Captions are compact identification contracts

Across the papers, useful captions name the object, cases, and sometimes the
representative-run rule. Avoid repeating the result, explaining the entire
method, or using vague titles such as `Analysis of results`. Keep related
captions parallel and use LaTeX en-dash ranges such as `Figs.~3(a)--(c)`.

## Tense, voice, and parallelism

### Tense follows rhetorical function

- Present: paper content, definitions, algorithm behavior, and current table or
  figure (`Section IV presents`, `the algorithm selects`, `Table III reports`).
- Past: completed experimental actions (`We conducted 30 runs`).
- Result tense: choose a consistent local pattern, such as `Table III reports
  that the algorithm achieved...` or journal-style present throughout.
- Future: actual future work only.

### Passive voice prevents false agency but must not hide missing information

Use `Bandwidth is allocated according to Eq.~(8)` when the executor is already
known. Use active voice when the executor matters. If neither voice identifies
who selects, evaluates, or updates an object, the method contract remains
incomplete.

### Lists require grammatical parallelism

The papers contain long lists of decisions, objectives, constraints, and
contributions. Coordinate noun phrases with noun phrases or verbs with verbs.
Keep contribution openings parallel (`We formulate`, `We design`, `We
evaluate`) and do not mix infinitives, gerunds, and nominalizations in one
series.

## Cross-corpus conclusions

The combined corpus validates the following rules as general rather than
paper-specific:

1. complete algorithms and modeled actors perform actions; components and
   document locators do not;
2. metrics, tests, results, figures, and tables require neutral reporting
   verbs with an explicit evidence scope;
3. numeral-quantified nouns, proper algorithm names, and generic operations
   have stable article patterns;
4. canonical terminology is more important than stylistic synonym variation;
5. direct verbs, precise collocations, and explicit antecedents outperform
   nominalized or vague constructions;
6. exact numbers, denominators, and test details replace promotional modifiers;
7. algorithm lines, equations, captions, citations, ranges, and units must be
   treated as LaTeX-aware prose rather than plain text; and
8. published examples provide both positive patterns and recurring errors, so
   every candidate rule must be applied by grammatical and technical role.

# Modeling, formulation, and writing gates

## Contents

1. [Architecture inheritance ledger](#1-architecture-inheritance-ledger)
2. [Model contract table](#2-model-contract-table)
3. [Causal dependency graph](#3-causal-dependency-graph)
4. [Paragraph and equation pacing](#4-paragraph-and-equation-pacing)
5. [Timing and state gates](#5-timing-and-state-gates)
6. [Physical and dimensional gates](#6-physical-and-dimensional-gates)
7. [Constraint placement and closure](#7-constraint-placement-and-closure)
8. [Decision and objective traceability](#8-decision-and-objective-traceability)
9. [Problem Formulation hard gates](#9-problem-formulation-hard-gates)
10. [Model-to-algorithm boundary](#10-model-to-algorithm-boundary)
11. [Language and style](#11-language-and-style)
12. [Final audit sequence](#12-final-audit-sequence)

## 1. Architecture inheritance ledger

Complete before revising an existing model:

| Element | Reference/current backbone | Keep | Adapt | Add | Remove | Reason and evidence |
|---|---|---:|---:|---:|---:|---|

Elements include:

- entities and roles;
- spatial topology;
- timing and decision cadence;
- workflow/event order;
- physical, communication, computation, queue, mobility, energy, reliability, and cost models as applicable;
- state and action spaces;
- objective definitions;
- constraint families;
- success/failure/terminal behavior.

Any top-level reordering, section split, or notation replacement needs a dependency or correctness reason recorded in the ledger. Stylistic preference is insufficient.

## 2. Model contract table

Create a symbol ledger before prose:

| Symbol | Kind | Meaning | Indices | Domain/unit | Defined at | Observed/decided/realized when | Used by |
|---|---|---|---|---|---|---|---|

Kinds: set, index, parameter, exogenous observation, state, decision, auxiliary variable, metric, objective, constraint indicator.

Hard rules:

- one symbol has one meaning;
- singular/plural, scalar/vector, and set notation remain distinct;
- all index ranges are explicit;
- units are compatible across every sum, ratio, and update;
- binary, integer, and continuous domains are stated;
- when a decision vector stores fixed components (for example, a position whose altitude is fixed), the text states which components are decided and the number of independent decision variables;
- a notation table may summarize but cannot be the first definition of a symbol used in prose or equations.

## 3. Causal dependency graph

For each equation, record its inputs and outputs. Topologically sort the graph. The prose/equation order should follow that sort except for a clearly signposted self-contained module.

Examples:

`configuration -> physical state -> service capacity -> service time -> waiting time`

`resource allocation -> completed work -> queue update -> generated state -> synchronization backlog`

`assignment -> active entity set -> shared-resource capacity -> cost`

`current position + action -> travel time -> arrival time -> service window -> next state`

Fail if an equation uses an undefined output from a later module without an explicit forward reference.

## 4. Paragraph and equation pacing

Use this local pattern:

> [Operational center sentence.] Under [necessary assumption], define [primitive quantity and domain]. The resulting [named metric] is
>
> \[\text{equation}\]
>
> where [only the remaining local parameters]. This relation shows [paper-relevant coupling]. To ensure [physical requirement], impose
>
> \[C_k: \text{constraint}.\]

Do not force every paragraph to use every role. Keep one dependency chain together and start a new paragraph when the physical operation changes.

### Section opening and subsection structure

Default: open the section with one overview paragraph and go straight to the first module. Do not add a standalone `system description`, `overview`, or `setting` subsection. The paragraph names the controller and actors, the time convention, the functional cycle, the initial state, and the module list, and defines only the sets, indices, and time grid that two or more modules use. Module-specific symbols and constraints appear at their module. Deviate when actors obey different execution semantics, in which case a workflow-level System Model section may precede the mathematical model; record the reason. [G-SM-open]

Default: when the role split among the actors rests on a modeling premise (why one entity only deploys and recovers while another collects or serves), state that premise and its reason in the opening paragraph, marked with `is assumed to` when it is an assumption. The Introduction then needs at most one clause on it. Deviate when an inherited model already fixes the roles; cite that model.

Default: title each subsection with a generic model name (`Communication Model`, `Energy Model`). Deviate when the venue requires descriptive titles, and record the reason. [G-SM-title]

Default: use at most one forward pointer per section, and name the section that defines the quantity. Deviate when two quantities cannot be ordered otherwise, and record the reason. [G-SM-fwd]

Apply the term first-use and antecedent tests of the reader and terminology contract to every subsection title, module name, and module reference in the opening paragraph, rather than restating them here.

## 5. Timing and state gates

For a dynamic model, answer all questions:

1. What interval does slot/cycle `t` denote?
2. At what instant is state `S[t]` measured?
3. Which exogenous variables are observed before the action?
4. Which decisions are selected at that instant?
5. In what order do physical actions, service operations, state generation, confirmation, and resource accounting occur?
6. Which random quantities realize before and after the action?
7. What is the update to `S[t+1]`?
8. What is the initial state?
9. Are conditional branches mutually exclusive and exhaustive?
10. What happens after success, failure, return, deadline, or horizon end?

Default: declare the initial state (question 8) in the opening paragraph or in the first module, before any recursion that uses it. Deviate when an inherited model already defines it; cite that model and record the reason. [G-SM-init]

Fail if a policy depends on future arrivals, measurements, or outcomes not available at its decision instant. Fail if two simultaneous operations consume the same resource without an allocation rule. Fail if a quantity is counted both when reserved and when realized.

## 6. Physical and dimensional gates

Check every equation:

- distances use compatible coordinate dimensions;
- throughput or service rates use the units declared by the model;
- service time is workload divided by compatible capacity, with a defined zero-capacity convention;
- processed work is capacity multiplied by duration after unit conversion;
- resource consumption follows a dimensionally valid and clearly sourced relation;
- queue/state updates cannot serve or transmit more work than available unless the surplus convention is explicit;
- probability and reliability expressions stay in valid ranges;
- averages and normalized objectives define their denominators and zero-denominator cases;
- `max`, `min`, indicator, and positive-part operators have stated semantics where nonstandard;
- reserved, incurred, expected, worst-case, and upper-bound quantities are not conflated.

## 7. Constraint placement and closure

Each constraint needs three appearances at most:

1. local physical explanation and formula;
2. inclusion in the final problem display;
3. concise grouping by role.

Do not re-explain the full algebra in all three places. Number constraints continuously when the manuscript uses numbered constraints.

For every constraint, verify:

- all symbols and index sets are defined;
- its activation condition is defined;
- big-M or indicator semantics are valid for inactive cases;
- it is neither duplicated by an equivalent condition nor contradicted by another constraint;
- the constraint can be evaluated under every feasible branch;
- its role is correctly grouped: planning/assignment, physical/safety, shared-resource, service-quality/deadline, budget, reliability, or variable domain.

## 8. Decision and objective traceability

Create the following matrix:

| Decision component | Physical equation affected | Constraint/domain | Objective path | Decision instant |
|---|---|---|---|---|

Fail if a decision has no downstream effect or if an objective depends on an uncontrolled quantity while the prose claims it is optimized.

For each objective, state:

- minimize or maximize;
- instantaneous, average, cumulative, worst-case, or terminal aggregation;
- horizon and population over which it is computed;
- normalization and units;
- special cases;
- why it conflicts with another objective, if a multi-objective problem is claimed.

Do not invent scalar weights when the benchmark formulation is Pareto multi-objective. Do not call a problem dynamic merely because it has time indices; the environment, state, feasible set, or objective must actually evolve.

## 9. Problem Formulation hard gates

Fail and revise if any condition holds:

- the formulation introduces a symbol, state, assumption, or physical relation not modeled earlier;
- the decision vector omits a variable that the paper claims to optimize;
- variable domains are missing or inconsistent with the algorithm representation;
- the objective sign conflicts with the prose;
- a cumulative objective uses future information in an online decision without a policy/expectation formulation;
- the constraint list changes a local constraint's meaning;
- stochastic variables appear without expectation, probability, scenario, robustness, or realization semantics;
- a dynamic/sequential problem is written as a one-shot open-loop vector without justification;
- the closing difficulty paragraph names only `nonconvexity` or `NP-hardness` instead of explicit couplings;
- algorithm-specific operations appear before the algorithm section.

## 10. Model-to-algorithm boundary

The model may define:

- system states and observations;
- physical decisions and domains;
- causal policy class when necessary;
- objectives, constraints, and failure events;
- structural dependencies that motivate a solver.

Defer these to the algorithm section:

- chromosome/neural encoding;
- action masking or repair implementation;
- population/archive operations;
- loss functions and policy updates;
- training schedules;
- heuristic candidate generation;
- complexity of algorithmic loops.

If an algorithm needs a feasibility certificate, the physical feasibility condition belongs in the model; the procedure for computing or enforcing it belongs in the algorithm.

## 11. Language and style

Use center sentences that name the modeled operation:

- `Once the controller determines the assignment, ...`
- `Upon receiving the assigned workload, ...`
- `Following data collection, ...`
- `At the end of each cycle, ...`
- `To ensure ..., constraint C_k requires ...`
- `Based on the above models, we formulate ...`

Use `we assume` for a modeling assumption, `we define` for notation, `is given by` for an adopted relation, and `we introduce/design` only for a genuine scenario-specific modeling component.

Avoid vague claims such as `for simplicity` without stating the consequence. State what a simplifying assumption affects and what it does not: an obstacle-free flight model does not make the communication links obstacle-free when the channel model accounts for blockage.

### Modeled, evaluated, and excluded quantities

Default: a quantity that can bound feasibility and that a reader or reviewer can ask about (the energy or endurance of a supporting platform, a shared buffer, a backhaul link) is either modeled in the formulation or evaluated separately with a cited model and reported with the results. An unsupported sufficiency assumption does not replace that model. When the quantity is evaluated outside the formulation, state once that it does not enter the objectives or constraints and that incorporating it is future work; do not add arguments for its sufficiency. Deviate when the quantity is provably non-binding under the stated parameters, and give that argument. [G-SM-scope]

Default: parameterize a physical platform from representative specifications of its class and cite the source (`a heavy-lift multirotor whose mass and rotor configuration follow representative manufacturer specifications`). Name a commercial product only when a claim depends on that product. Deviate when the venue or a reviewer asks for the product, and record the reason. Avoid surveying multiple papers inside a model paragraph. One source citation is usually enough to ground an adopted equation or assumption.

After an equation, explain physical meaning, coupling, or a boundary case. Do not simply translate each symbol into prose a second time.

## 12. Final audit sequence

Run in this order:

1. read only subsection headings: do they reproduce the operational flow?
2. read only first sentences: do they form a causal model story?
3. scan first symbol occurrences: is every symbol defined before use?
4. topologically check equation dependencies;
5. check units and domains;
6. simulate one interval by hand, including all branches;
7. trace each decision to objectives and constraints;
8. compare the final formulation against the local constraints;
9. remove duplicated explanations and algorithm leakage;
10. compare against the inheritance ledger to ensure the rewrite did not redesign validated modules without cause;
11. list every quantity that can bound feasibility and check that each is modeled, evaluated separately, or excluded with one stated reason, without a sufficiency argument.

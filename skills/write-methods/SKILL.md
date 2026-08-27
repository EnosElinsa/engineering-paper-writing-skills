---
name: write-methods
description: Use when drafting, revising, or auditing an engineering-paper Method, Proposed Algorithm, or Solution section, especially when model-to-algorithm traceability, novelty boundaries, constraint semantics, executable pseudocode, deployment behavior, or complexity analysis are weak, including evolutionary and reinforcement-learning methods.
---

# Write Methods

## Purpose

Explain a method as an executable solution to the previously formulated problem. Every representation, operator, network, loss, repair, fallback, and loop must answer a stated model or search difficulty. Separate inherited machinery from the new mechanism and bound novelty claims to verifiable differences.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. For population-based, Pareto, constrained, or dynamic evolutionary optimization, read [the evolutionary-algorithm route](references/methods/evolutionary-algorithms.md).
3. For MDP or POMDP, value-based, policy-gradient, actor-critic, single-agent, or multi-agent learning, read [the reinforcement-learning route](references/methods/reinforcement-learning.md).
4. Read [the MEC domain pack](references/domains/mec.md) only when the target problem is MEC or a directly adjacent edge-computing system.
5. When several routes apply, read all applicable references and state which component each route governs.

## Workflow

### 1. Recover the method contract

Read the formulation and identify the decision variables, state or observations, objectives, constraints, decision cadence, uncertainty, and operational owner. Then build:

| Method component | Model difficulty | Inputs | Outputs | Constraints handled | Novel or inherited | Evidence |
|---|---|---|---|---|---|---|

A component without a model-side purpose is unjustified. A model decision without a representation or output is unimplemented.

### 2. Bound novelty

Create a novelty ledger that separates standard family machinery, adapted machinery, and genuinely new mechanisms. For each claimed novelty, record its closest baseline, exact operational difference, model-side reason, and experimental isolation. Do not rename a standard operator and present it as a contribution.

### 3. Establish the executable map

Before details, state:

- what the solver receives;
- how physical decisions are represented;
- where feasibility is constructed, repaired, masked, penalized, or checked;
- how objectives, fitness, reward, or losses use the model;
- which component updates which state;
- termination or training completion;
- what solution or action is selected for execution;
- what happens when no feasible output is available.

Use subsection order that follows execution or data flow.

### 4. Explain components by contract

For each component, write:

`difficulty -> role -> inputs -> transformation -> output -> downstream consumer -> boundary`

Define equation symbols locally and explain why the transformation is appropriate for the stated structure. Do not rederive physical equations already established in the model; cite or cross-reference them when computing objectives, fitness, reward, or feasibility.

### 5. Make pseudocode and prose agree

Pseudocode must expose initialization, loop bounds, conditionals, state updates, feasibility handling, termination, and returned output. Every named step must have defined inputs and effects. Prose may explain purpose and semantics, but must not introduce operations absent from the pseudocode.

### 6. State deployment and fallback behavior

Name the executor, execution location, cadence, required observations, offline and online phases, synchronization or communication needs, output consumed by the system, computational deadline, and safe fallback. A method that only works when it returns a feasible solution must define the infeasible-output branch.

### 7. Derive complexity honestly

Define size parameters before using them. Derive time and space complexity by nested loops and dominant operations, including feasibility checks, simulation or model evaluation, sorting, archive operations, network inference or training, and inter-agent communication when applicable. Distinguish offline training or planning from online inference or decision time.

### 8. Run the selected gates

Apply the core traceability, novelty, executability, feasibility, deployment, complexity, and claim gates. Then apply every relevant method-family route and the selected domain pack. Verify exact correspondence among the model, equations, pseudocode, implementation description, and claimed evidence.

## Output constraints

- Match the manuscript's notation, terminology, language, and citation style.
- Preserve correct standard machinery and identify it as inherited.
- When auditing, report contract failures before stylistic issues.
- Do not change the system model, experiments, bibliography, or code unless authorized.


# MEC domain pack for Method sections

## Contents

1. [Evidence base](#evidence-base)
2. [MEC method contract](#mec-method-contract)
3. [Dependency-aware construction](#dependency-aware-construction)
4. [Execution and feasibility](#execution-and-feasibility)
5. [Writing gates](#writing-gates)
6. [Reference scale](#reference-scale)

## Evidence base

These rules were checked against the method sections of the following MEC-family sources:

- *Demand-Aware Multi-Area Multi-UAV Empowered Mobile Edge Computing: A Joint Energy and Delay Optimization*;
- *UAV-Enabled Multi-Source Data Fusion in Vehicular Networks: A Joint Optimization Approach for Reliability and Latency*, DOI `10.1109/TWC.2026.3676831`;
- *Terrain-Aware UAV-Enabled Mobile Edge Computing in Urban Environments: A Constrained Multi-Objective Approach With Task-Adaptive Mechanism*, DOI `10.1109/TVT.2025.3604250`;
- *Joint Latency and Charge Cost Minimization for Reliable Task Offloading in Dispersed Computing: A Multi-objective Optimization Approach*, DOI `10.1109/TMC.2026.3679393`;
- the author-supplied periodic HAP-UAV planning benchmark.

The detailed evolutionary and reinforcement-learning family rules live in the method-route references. This pack adds only MEC-specific model-to-method checks.

## MEC method contract

Before naming operators or networks, map every encoded or learned output to an MEC model decision:

| MEC decision | Representation or action | Physical relation affected | Feasibility handling | Executor and cadence |
|---|---|---|---|---|

Typical decisions include deployment, trajectory, association, offloading, admission, scheduling, bandwidth, power, computation, caching, placement, migration, collection, compression, synchronization, and return. Include only those present in the target model.

The method opening names the formulated problem and the block order and does not restate the Introduction's list of obstacles. State a MEC-side difficulty in the opening or in the module subsection only with operational detail the Introduction lacks, and name it concretely, such as cascaded decisions, mixed discrete-continuous coupling, sparse feasible regions, time-varying service state, partial observations, shared-resource contention, or a feasible set shaped by the preceding action. “Nonconvex” and “NP-hard” do not by themselves justify a module.

## Dependency-aware construction

When MEC decisions depend on one another, generation, decoding, repair, or action masking must respect that order. Examples supported by the source set include:

- deployment before position and association;
- association or admission before bandwidth and computation allocation;
- mobility before channel-dependent rate and service decisions;
- response before collection and bandwidth in a cascaded service cycle;
- offloading choice before server-resource allocation;
- the prior cycle's physical state before dynamic feasibility reconstruction.

State which constraints are satisfied structurally by the representation, which are repaired or masked, and which remain for selection, penalty, or constrained optimization. Never claim that bounds alone ensure MEC feasibility when capacity, association, deadline, safety, energy, or reliability constraints remain.

## Execution and feasibility

Name the control location and operational output. Distinguish an offline mission planner, a periodic central controller, an onboard or edge controller, decentralized agents, and a simulator used only for training.

For a multi-objective method, define how one solution is selected for execution and whether that choice changes across cycles. For a dynamic method, state what information is retained, what is regenerated after the environment changes, and why the retained variables remain valid.

Define the safe branch for:

- no feasible individual or action;
- unavailable server or link;
- zero service rate or exhausted resource;
- missed deadline or incomplete workload;
- insufficient energy for service or return;
- invalid association, placement, or migration target.

A penalty without operational fallback is not a complete MEC controller.

## Writing gates

Fail and revise if:

- a physical MEC decision is missing from the encoding, action, or returned solution;
- a module is motivated only by a generic solver weakness;
- the method recomputes channel, latency, energy, queue, or reliability models with semantics different from the System Model;
- decoding uses future channel, task, or mobility information unavailable at the decision instant;
- feasibility claims omit one of the model's active constraint families;
- the executor, decision cadence, or selected executable solution is unspecified;
- fallback behavior would violate safety, energy, deadline, or service-continuity requirements;
- complexity omits physical evaluation, feasibility checks, simulator interaction, or communication required by the MEC implementation.

## Reference scale

These are order-of-magnitude defaults for the scale statement (protocol S in the shared contract), measured on the method sections of four evolutionary-algorithm UAV-MEC papers in an IEEE Transactions layout. They are a weak prior for any other solver family or domain. Deviate when the venue limits length, an extra independent boundary needs its own unit, or the target family has no benchmark, and record the reason.

**How these numbers were counted.** Prose paragraphs of at least 20 words, page-break fragments merged, with equations, tables, captions, figure code, and pseudocode excluded. Words are alphabetic tokens without citation brackets or inline math. Counts are good to about 20%. One Dispersed algorithm subsection was lost in extraction, so its counts are lower bounds.

| Measure | Demand-aware | Dispersed | Terrain-aware | Fusion |
|---|---:|---:|---:|---:|
| Algorithm section, prose paragraphs | 16 | 24 | 21 | 17 |
| Algorithm section, prose words | about 1200 | about 3000 | about 1500 | about 1100 |
| Lettered subsections | 4 | 4 | 3 | 3 |

Reading the table: expect roughly 1,200–3,000 words, 16–24 prose paragraphs, and three or four subsections, with the upper end set by a method that has a second population and a repair procedure. Three of the four papers open the section with a short roadmap that names the formulated problem and the block order, which is the default in the core opening rule. The remaining paper opens at a specific difficulty and is the allowed exception when the Introduction did not state that difficulty.

The reference papers carry extraction noise and wording slips. Align to structure and scale, not to sentences.
# MEC domain pack for Method sections

## Contents

1. [Evidence base](#evidence-base)
2. [MEC method contract](#mec-method-contract)
3. [Dependency-aware construction](#dependency-aware-construction)
4. [Execution and feasibility](#execution-and-feasibility)
5. [Writing gates](#writing-gates)

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

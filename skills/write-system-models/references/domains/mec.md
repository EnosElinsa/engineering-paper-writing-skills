# MEC domain pack for System Models and Problem Formulations

## Contents

1. [MEC model contract](#mec-model-contract)
2. [Scope and portable source identification](#scope-and-portable-source-identification)
3. [Shared macro-structure](#shared-macro-structure)
4. [Source-by-source structural anatomy](#source-by-source-structural-anatomy)
5. [Demand-aware multi-area multi-UAV MEC](#1-demand-aware-multi-area-multi-uav-mec)
6. [UAV-enabled multi-source fusion](#2-uav-enabled-multi-source-fusion)
7. [Terrain-aware UAV-MEC](#3-terrain-aware-uav-mec)
8. [Reliable offloading in dispersed computing](#4-reliable-offloading-in-dispersed-computing)
9. [HAP-UAV periodic planning manuscript](#5-hap-uav-periodic-planning-manuscript)
10. [Stable paragraph roles](#stable-paragraph-roles)
11. [Problem Formulation as closure](#problem-formulation-as-closure)
12. [Architecture inheritance lessons](#architecture-inheritance-lessons)
13. [Benchmark-inconsistent failure patterns](#benchmark-inconsistent-failure-patterns)
14. [Reference scale](#reference-scale)

## MEC model contract

The source set repeatedly models MEC systems through an explicit control and service flow. Apply these domain gates:

1. **Control boundary:** identify the controller or decision owner, edge or aerial servers, users or sensing entities, infrastructure, and the information available when decisions are made.
2. **Time semantics:** distinguish mission-level, cycle-level, slot-level, and event-level quantities. State when mobility, association, transmission, computation, state generation, synchronization, return, and energy accounting occur.
3. **Causal service chain:** order only the modules present in the target system, commonly `deployment or mobility -> association and channel -> transmission -> computation or fusion -> service completion or state update -> energy, latency, reliability, or cost`.
4. **Resource closure:** define workload, data size, cycles per bit or service demand, rate, allocated bandwidth or compute, queue or backlog, and capacity with compatible units. Guard zero-rate, empty-set, infeasible-assignment, and unfinished-service cases.
5. **Mobility and safety closure:** connect positions and actions to travel time, coverage or blockage, service windows, propulsion energy, collision or terrain constraints, return feasibility, and the next state whenever these mechanisms exist.
6. **Local constraint placement:** introduce association, capacity, QoS, deadline, energy, reliability, and variable-domain constraints beside the relation they govern before collecting them in the final problem.
7. **Dynamic closure:** state the initial state, observation-action-realization-update order, success and failure branches, terminal behavior, and the executed decision selected from a multi-objective result.

Do not force every MEC paper to contain every module. The mandatory rule is that the written order follows the target system's actual service flow and that every optimized MEC decision reaches a physical metric, constraint, or state update before formulation.

## Scope and portable source identification

This analysis is distilled from the model and formulation sections of five benchmark manuscripts. Titles, section names, and stable identifiers replace local filesystem paths.

1. **Demand-Aware Multi-Area Multi-UAV Empowered Mobile Edge Computing: A Joint Energy and Delay Optimization** — Section III: system overview, UAV deployment, communication/user association, task computing, UAV energy, and problem formulation.
2. **UAV-Enabled Multi-Source Data Fusion in Vehicular Networks: A Joint Optimization Approach for Reliability and Latency** — Section III: flight, local observation, uplink, fusion, downlink, and dynamic problem formulation; DOI `10.1109/TWC.2026.3676831`.
3. **Terrain-Aware UAV-Enabled Mobile Edge Computing in Urban Environments: A Constrained Multi-Objective Approach With Task-Adaptive Mechanism** — Section III: safety-enhanced flight, communication, computing, terrain-aware channel, and problem formulation; DOI `10.1109/TVT.2025.3604250`.
4. **Joint Latency and Charge Cost Minimization for Reliable Task Offloading in Dispersed Computing: A Multi-objective Optimization Approach** — Sections III–IV: workflow-level system model, task/IoTD/edge-server mathematical models, and CMOP formulation; DOI `10.1109/TMC.2026.3679393`.
5. **HAP-UAV periodic data-collection planning manuscript** — author-supplied benchmark draft, System Model and Problem Formulation: mission timing, flight and state transitions, energy, data collection/cumulative utility, and DCMOP formulation.

The fifth source is a non-public writing benchmark. The reusable observations below are self-contained and do not depend on access to that draft.

## Shared macro-structure

The combined benchmark pattern is:

`system overview -> operational modules in causal order -> local metrics and constraints -> objective components -> consolidated problem`

The papers differ in whether `System Model` and `Problem Formulation` share one top-level section. This is a venue/manuscript choice, not a quality rule. What remains stable is that the formulation comes after all quantities needed to evaluate it.

The overview paragraph acts as a map. It identifies the controller and actors, describes the service flow, states the time scope, and previews the modules. It may define the primary sets and one basic distance, as the Demand-aware paper does, but not module-specific symbols, and it never opens with a symbol inventory detached from the scenario. Default: declare the initial state there or in the first module; of the four reference papers only the Demand-aware paper does so in its opening paragraph, and the Fusion paper gives only the duration, the slot grid, and a battery assumption while the Terrain-aware paper mentions an initial position without values, so deviate when an inherited model defines the state, and record the reason.

## Source-by-source structural anatomy

## 1. Demand-aware multi-area multi-UAV MEC

### Model order

The opening defines the control center, UAVs, service areas, users, locations, and common altitude. It then introduces a basic distance used by later modules.

The subsections follow the operational flow:

1. **UAV deployment:** area assignment, position, flight time and energy, coverage/assignment/safety constraints.
2. **Communication and user association:** association set, LoS/NLoS channel, rate, offloading time and energy, association and bandwidth constraints.
3. **Task computing:** CPU allocation, computing time/energy, total completion time, computing-capacity constraint.
4. **UAV energy:** hover duration/power/energy, total energy, energy and delay constraints.
5. **Problem formulation:** decision vector, normalized energy and average delay objectives, collected constraints, domains, and edge case.

### Paragraph and equation pattern

Each subsection begins with an operational transition such as UAVs arriving, users associating, or tasks being received. Equations build in dependency order. Constraints are introduced in the module whose physics they govern and are later grouped by role.

### Reusable lesson

Place assignment before any quantity conditional on assignment; place rate before transmission time; place component costs before total energy; introduce objectives only after every constituent quantity exists.

## 2. UAV-enabled multi-source fusion

### Model order

The overview defines the UAV, vehicular users, objects, mission duration, time-slot discretization, and a complete cycle: requests -> UAV movement -> observation collection -> fusion/compression -> result delivery. It explicitly previews five components.

The subsection order reproduces that cycle:

1. flight distance, velocity, altitude/turning constraints;
2. local observation data as a distance-dependent quantity;
3. request/collection decisions, channel, uplink rate/time, assignment and bandwidth constraints;
4. fusion processing time and result size;
5. downlink rate/time, end-to-end waiting time, slot deadline, and reliability belief;
6. DCMOP formulation.

The formulation defines a mixed decision vector for position, request response, collection, compression, and bandwidth. It then defines cumulative average reliability and waiting-time objectives, states the zero-service denominator convention, converts maximization to minimization by sign, and groups constraints.

### Reusable lesson

When decisions have cascaded semantics, model them in the same order as the real service pipeline. A variable such as response, collection, or bandwidth must not appear before the preceding eligibility decision is defined.

## 3. Terrain-aware UAV-MEC

### Model order

The overview states the ground-controlled workflow: plan a safe path, reach a destination, hover, receive tasks, and compute. It previews three baseline components plus a scenario-specific terrain-aware channel model.

The paper then develops:

1. a B-spline flight representation, travel time, collision-risk objective, and flight constraints;
2. communication and task-transmission time;
3. computing time, maximum completion-time objective, and CPU constraint;
4. the proposed terrain-aware channel model, including the environmental blockage construction that supplies channel gain;
5. CMOP formulation.

The communication subsection explicitly points forward to the later channel subsection. The novel channel derivation is kept self-contained rather than scattered through baseline communication equations.

### Reusable lesson

A scenario-specific model may be isolated after baseline modules if that placement makes its derivation coherent. Forward references are acceptable only when the dependent quantity is clearly named and later defined before formulation.

## 4. Reliable offloading in dispersed computing

### Model order

This paper separates a workflow-level System Model from the Mathematical Model. The System Model first contrasts parallel edge-server processing, serial IoT-device processing, reliability failures, redundant execution, and monetary rewards. It then enumerates the end-to-end workflow from requests and recruitment through information collection, optimization, execution, and payment.

The Mathematical Model is organized by actor:

1. **Task side:** static-horizon assumptions, task tuple, assignment variable, failure probability and reliability.
2. **IoT-device side:** channel/rate, receive time/energy, compute time/energy, priority queue waiting time, delay and charge.
3. **Edge-server side:** parallel processing, allocated CPU, delay and charge.

The CMOP formulation defines assignment, bandwidth, and CPU decisions, gives total delay and charge objectives, lists feasibility constraints, and then explains each constraint's operational role.

### Reusable lesson

When heterogeneous actors obey different execution semantics, organizing mathematical modules by actor can be clearer than forcing a common communication-computing template. The system workflow must explain why the actor-specific equations differ.

## 5. HAP-UAV periodic planning manuscript

### Model order

The overview defines a regulated mission duration, discrete planning cycles, the decision instant at each cycle start, operational boundaries, HAP/UAV positions, assignment semantics, and three disjoint UAV status sets. It states initial positions and initial set memberships before any recursion.

The subsequent modules are:

1. **Flight:** assumptions, HAP and UAV travel time, reachable distance, rendezvous timing, collection window, deadline constraints, exhaustive status transitions, and next-cycle set updates.
2. **Energy:** current-operation costs, reserved recovery costs, battery recursion, safe-return constraint, and a return-threshold rule.
3. **Data collection and cumulative utility:** stochastic aggregation rate, channel/rate/bandwidth, effective collection rate, volume recursion, and fairness utility.
4. **Problem formulation:** current-cycle decision vector, mixed-domain description, energy minimization and utility maximization, and constraint groups.

### Reusable lesson

Dynamic models need more than a time index. They must define the state observation instant, decision instant, within-cycle event order, initial state, carry-over variables, exhaustive transitions, and terminal/recovery behavior. Reserved energy and actual energy must be distinguished to prevent double counting.

## Stable paragraph roles

The benchmark model paragraphs repeatedly use the following roles:

1. **Module center:** states what operation is being modeled and why it is next.
2. **Assumption:** fixes the physical abstraction needed for the relation.
3. **Definition:** introduces primitive variables and domains.
4. **Relation:** gives a formula for one named quantity.
5. **Interpretation:** explains meaning, coupling, or an edge case.
6. **Constraint:** states a physical requirement before its mathematical form.
7. **Transition:** names which output feeds the next module.

A paragraph may contain more than one related center sentence, but one must govern the others. Long paragraphs become difficult when definitions, unrelated mechanisms, and multiple constraints compete without hierarchy.

## Problem Formulation as closure

Across the benchmark set, the final formulation does not rebuild the model. It performs five closure operations:

1. declares the problem class;
2. gathers already-defined decisions into a vector or current-cycle individual;
3. gathers already-defined metrics into objectives;
4. gathers already-defined feasibility rules into constraints and domains;
5. identifies the coupling that makes the problem difficult.

The benchmark papers often explain objective conflict—for example, reliability versus delay, safety versus task completion, energy versus utility, or delay versus charge—before or immediately after the compact mathematical display.

## Architecture inheritance lessons

The references reuse standard backbones such as probabilistic LoS channels, OFDMA/Shannon rates, CPU-cycle computing time, rotorcraft power, and constrained multi-objective formulations. Their novelty comes from adding or changing a scenario mechanism:

- demand-dependent multi-area allocation;
- request-driven fusion with cascaded decisions;
- terrain-explicit blockage and path safety;
- heterogeneous parallel/serial execution with redundancy and charging;
- periodic HAP motion with UAV status transitions and recovery reserves.

A benchmark-like rewrite therefore retains validated standard modules and inserts the new scenario mechanism where it changes inputs, states, constraints, or objectives. It does not rename every symbol or replace the whole architecture merely to appear original.

## Benchmark-inconsistent failure patterns

1. **Symbol dump:** many sets and variables appear before the reader knows the workflow.
2. **Topic order instead of causal order:** energy, channel, queue, and assignment are arranged by preference rather than dependency.
3. **Undefined timing:** `at slot t` alternates among slot start, after arrivals, and slot end.
4. **Open recursion:** a state update lacks initialization, a branch, or terminal behavior.
5. **Detached constraints:** constraints appear only in the final display without prior physical explanation.
6. **Formulation drift:** the decision vector omits decisions used earlier or includes a new one not modeled earlier.
7. **Algorithm leakage:** encoding, masking, repair, training, or search operators are introduced in the model.
8. **Architecture replacement:** an established reference backbone is split or redesigned without a demonstrated dependency reason.
9. **Equation narration:** prose restates symbols line by line but never explains the relevant coupling.
10. **Unqualified assumptions:** ignored download delay, fixed mobility, sufficient battery, or perfect control information is asserted without scope or source.

## Reference scale

These are order-of-magnitude defaults for the scale statement (protocol S in the shared contract), measured on four evolutionary-algorithm UAV-MEC papers in an IEEE Transactions layout. They are a weak prior for any other family. Deviate when the venue limits length, an extra independent boundary needs its own unit, or the target family has no benchmark, and record the reason.

**How these numbers were counted.** Prose paragraphs of at least 20 words, page-break fragments merged, with equations, tables, captions, and figure code excluded but the explanatory text that follows each equation included. Words are alphabetic tokens without citation brackets or inline math. Counts are good to about 20% because the split between equation text and prose is not exact. Equation numbers are the count of tagged display equations and are approximate.

| Measure | Demand-aware | Dispersed | Terrain-aware | Fusion |
|---|---:|---|---:|---:|
| System model and formulation, prose words | about 1250 | about 1830 (system model about 680, formulation about 1160) | about 2800 | about 1520 |
| Lettered subsections | 5 | 0 in the system model, 2 in the formulation | 5 | 6 |
| Opening overview paragraph, words | 159 | 281 | 184 | 239 |
| Numbered equations (approximate) | 29 | 10 | not counted | not counted |

Reading the table: expect roughly 1,250–2,800 words and five or six subsections for a system model that includes the formulation, and an opening overview paragraph of about 160–280 words. The Dispersed opening paragraph also introduces the five-step workflow.

**Counterexamples: align to structure and scale, not to sentences**

- The Dispersed paper has a standalone System Model section of about 680 words before its Problem Formulation. That is the allowed exception for actors with different execution semantics. It is not evidence that a standalone overview subsection is normal.
- Only the Demand-aware opening paragraph states initial positions. Do not claim that all four reference papers declare the initial state in the opening paragraph.
- The Terrain-aware opening paragraph contains one forward pointer, to the later channel-model subsection. This is the model for the one-pointer default, not a license for several.
- The reference papers carry extraction noise and wording slips. Never copy a sentence from them.
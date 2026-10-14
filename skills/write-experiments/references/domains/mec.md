# MEC domain pack for Experimental sections

## Contents

1. [Evidence base](#evidence-base)
2. [MEC evaluation contract](#mec-evaluation-contract)
3. [Scenario and baseline controls](#scenario-and-baseline-controls)
4. [Physical evidence and interpretation](#physical-evidence-and-interpretation)
5. [Writing gates](#writing-gates)
6. [Reference scale](#reference-scale)

## Evidence base

These domain checks were distilled from the experimental sections associated with the MEC-family method and model benchmarks used by this collection, including demand-aware multi-UAV MEC, UAV-enabled vehicular data fusion, terrain-aware UAV-MEC, reliable dispersed offloading, and periodic HAP-UAV planning. They supplement, rather than replace, the generic experiment and method-family gates.

## MEC evaluation contract

Report enough of the system configuration to reproduce the physical comparison:

- topology, coverage region, entity counts, and initial or terminal positions;
- task, data, workflow, or service-state distributions;
- mobility, channel, blockage, interference, and association assumptions when active;
- bandwidth, power, computation, storage, energy, and time-horizon budgets;
- arrivals, deadlines, reliability targets, safety limits, and failure events;
- decision cadence, observation availability, and offline versus online computation.

For every metric, state the unit, aggregation population and horizon, direction of improvement, normalization, and handling of infeasible or unfinished cases. Do not silently exclude failed missions, dropped tasks, zero-rate users, unserved areas, or solutions that cannot return safely.

## Scenario and baseline controls

Separate three comparison questions:

1. **Architecture or scenario value:** hold the solver and budget as constant as possible while changing the deployment, hosting, mobility, service, or state mechanism.
2. **Algorithm value:** compare solvers on the same MEC formulation, information, initialization policy, stopping or evaluation budget, and feasibility definition.
3. **Module value:** remove or replace one proposed component while preserving the remaining encoding, training, constraint handling, and compute budget.

Record baseline access to global state, future arrivals, channel knowledge, environment maps, centralized communication, and pretrained models. A baseline with less information or a smaller compute budget does not isolate algorithm quality.

Vary the load and resource dimensions that activate the claimed difficulty, such as users or tasks, demand heterogeneity, server or UAV count, bandwidth, compute capacity, energy, mobility, blockage, deadline, reliability, or failure rate. A method designed for dynamic or constrained MEC requires more than one nominal operating point.

## Physical evidence and interpretation

Use physical metrics that close the model claims: latency or completion time, energy, cost, utility or throughput, reliability or success rate, coverage, served workload, constraint violation, and return or terminal feasibility as applicable.

Reward, scalar fitness, hypervolume, IGD, or another algorithmic metric cannot alone establish better MEC service. Pair it with the physical objectives and active constraints on held-out or independently generated instances. In each of the four evolutionary-algorithm benchmark papers, the paragraph that defines the comparison metrics defines two algorithm-quality metrics only, such as inverted generational distance with hypervolume or success rate with hypervolume. Their physical outcomes (for example regional deployment effects, line-of-sight probability, transmission rate, and collected data size) are analyzed in separate subsections. A service-continuity study therefore needs its physical-outcome metrics in a paragraph of their own, with definition, direction, unit, aggregation, and failure semantics.

Mechanism explanations must follow the model:

- position or deployment may change distance, blockage, rate, travel energy, and service windows;
- association and offloading may change contention, queueing, computation time, and reliability;
- resource allocation may trade service time against energy or cost;
- migration or synchronization may add data transfer, interruption, backlog, and continuity effects;
- a dynamic response may improve feasibility by respecting state inherited from the previous cycle.

Use “results from” or “is driven by” only when an ablation, controlled sweep, or model-supported case analysis isolates that path. Otherwise write “is consistent with.”

## Writing gates

Fail and revise if:

- a headline MEC claim is supported only by reward or an aggregate optimizer metric;
- scenario, algorithm, and module effects are conflated in one uncontrolled comparison;
- physical budgets or information access differ materially across baselines without disclosure;
- infeasible, unserved, unfinished, or unsafe cases are omitted from denominators;
- dynamic performance is reported without decision-time or state-transition semantics;
- robustness is claimed from a nominal topology or channel realization;
- scalability is claimed without varying a relevant entity, load, horizon, or resource dimension;
- the explanation contradicts the System Model's causal relations;
- online suitability is claimed without decision latency, inference cost, or fallback evidence.

## Reference scale

These are order-of-magnitude defaults for the scale statement (protocol S in the shared contract), measured on the experiment sections of four evolutionary-algorithm UAV-MEC papers in an IEEE Transactions layout. They are a weak prior for any other solver family or domain, including reinforcement learning. Deviate when the venue limits length, an extra independent boundary needs its own unit, or the target family has no benchmark, and record the reason.

**How these numbers were counted.** Prose paragraphs of at least 20 words, page-break fragments merged, with tables, captions, figure code, and equations excluded. Words are alphabetic tokens without citation brackets or inline math. Counts are good to about 20%.

| Measure | Demand-aware | Dispersed | Terrain-aware | Fusion |
|---|---:|---:|---:|---:|
| Experiment section, prose paragraphs | 10 | 16 | 15 | 20 |
| Experiment section, prose words | about 1100 | about 1700 | about 900 | about 1900 |
| Lettered subsections | 4 | 6 | 3 | 7 |

Reading the table: expect roughly 900–1,900 words, 10–20 prose paragraphs, and three to seven subsections. Some reference papers move further experiments to a supplementary document, so the counts understate the full study.

**Run protocol and statistics in the references.** Three of the four papers report 30 independent runs per algorithm and instance (counted from their experimental-setting statements), with means and standard deviations. The Fusion paper adds a Wilcoxon rank-sum test at the 0.001 level, which is an unpaired test. The Terrain-aware paper computes its statistics over 100 solutions of the final population and states no run count in the main text. None of the four runs a paired test over instances after aggregating seeds. The core statistical rule is therefore stricter than these references, and the references are not evidence for a weaker design.

The reference papers carry extraction noise and wording slips. Align to structure and scale, not to sentences.
# Case 20: Idealized reference value called a bound
Skill: write-experiments
Expected gates: G-EX-ref
Language: en
Snippet:
> To assess optimality, the throughput is compared with an upper bound computed by assuming an interference-free channel and unlimited relay capacity. The proposed scheduler attains 81% of this bound, which indicates that it lies within 19% of the optimum.
Why it fails: a value computed under idealized assumptions is a reference value. Its direction relative to the true optimum is not proven, so the 19% cannot be read as a distance to the optimum.

# Case 44: Complexity analysis without sources and with an absorbed term
Skill: write-methods
Expected gates: G-ME-cplx
Language: en
Snippet:
> Non-dominated sorting costs O(MN^2) and the repair costs O(NJ log J). Since log J is small, the repair term is absorbed, and the overall complexity is O(GMN^2).
Why it fails: the sorting cost has no source, the crossover and mutation costs are missing, and the repair term is dropped by an informal argument instead of a stated condition.

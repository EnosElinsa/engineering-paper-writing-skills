# Case 19: Nonsignificant comparison written as support for the proposed design
Skill: write-experiments
Expected gates: G-EX-null
Language: en
Snippet:
> Both mutation schemes reach a feasible-run rate of 100%, and the Wilcoxon rank-sum test finds no significant difference in hypervolume between them on any instance. These results support the uniform mutation adopted by the proposed algorithm.
Why it fails: the absence of a significant difference shows only that the alternative scheme gives no significant improvement on the tested instances. It does not favor the adopted scheme.

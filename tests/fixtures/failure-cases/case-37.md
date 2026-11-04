# Case 37: Chinese sentences with colons, meta-language, and 据此
Skill: write-methods
Expected gates: G-ZH-sent
Language: zh
Snippet:
> 解决这一问题的直接思路是：在每个周期重新选择充电站位置。据此，我们设计了一种修复机制。上述两点在该场景中均不成立。
Why it fails: a colon joins two clauses, the first sentence announces a move instead of stating it, 据此 serves as a connective, 我们 replaces 本文, and the last sentence is a bare self-summary.

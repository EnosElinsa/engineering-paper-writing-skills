# Case 03: undefined compound objective and a long conflict chain

Skill: write-introductions
Expected gates: G-INT-16, G-INT-obj, G-INT-conflict
Language: zh

Snippet:

> 本文的目标是最小化综合滞留代价。提高吞吐会增加机器人密度，密度升高造成通道拥堵，拥堵加快电池消耗，电池耗尽又迫使更多机器人返回充电，最终反而降低有效吞吐。

Why it fails: the objective has no owner or meaning, and the conflict is explained through four causal steps in one direction.

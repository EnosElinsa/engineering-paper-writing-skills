# Case 38: Over-split Chinese model section
Skill: write-system-models
Expected gates: G-ZH-rhythm
Language: zh
Snippet:
> 机器人出发。机器人到达区域。机器人开始配送。因此，配送时间增加。因此，剩余电量减少。
Why it fails: five sentences of 6 to 9 ideographs, three with the same subject, and two consecutive 因此 openers. The section mean falls far below the Chinese weak-prior band, and the consequences should be folded in with 从而.

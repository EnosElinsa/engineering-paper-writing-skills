# Case 36: Supervisor edits adopted without classification against the house style
Skill: write-revision-responses
Expected gates: G-RV-style
Language: en
Snippet:
> The supervisor merged twelve short sentences into five longer ones, two of them joined by semicolons. The author accepted the version, split three of the merged sentences again in the next pass, and recorded no rule.
Why it fails: the edits were not measured as merges and splits against the snapshot, the recurring merge pattern was not recorded, and the conflict with the semicolon ban was not put to the user.

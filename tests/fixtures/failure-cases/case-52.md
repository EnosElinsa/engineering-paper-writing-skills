# Case 52: Cause lost when because is removed
Skill: write-introductions
Expected gates: G-STY-conn
Language: en
Snippet:
> Before: Statistical channel models misestimate the link quality in dense urban areas because buildings block the line of sight. After: Statistical channel models misestimate the link quality in dense urban areas. This leads to poor offloading decisions.
Why it fails: removing `because` also removed the cause. It should survive as a `since` or `due to` clause, or as the subject of its own sentence (`Buildings that block the line of sight make statistical channel models misestimate the link quality ...`).

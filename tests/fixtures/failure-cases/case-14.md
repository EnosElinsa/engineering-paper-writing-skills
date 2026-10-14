# Case 14: System Model structure ignores the opening, title, pointer, and initial-state rules

Skill: write-system-models
Expected gates: G-SM-open, G-SM-title, G-SM-fwd, G-SM-init
Language: en

Snippet:

> III. System Model. A. System Description. This subsection describes the system. B. Backlog Handshake Layer. The backlog follows q(t+1) = q(t) + a(t) - s(t), see Section V for the controller and Section IV for the reward. The initial backlog is given in Section III-F.

Why it fails: a standalone description subsection, a coined subsection title, several forward pointers, and an initial state that appears after the recursion.

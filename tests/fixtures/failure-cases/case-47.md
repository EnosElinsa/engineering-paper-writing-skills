# Case 47: Abbreviation used before its definition and expanded differently
Skill: latex-prose-audit
Expected gates: G-AUD-abbr
Language: en
Snippet:
> Introduction: a hybrid PPO (H-PPO) learner was proposed ... Section IV: proximal policy optimization (PPO) is adopted. Table II header: CSI. Section V: the channel state information (CSI) is assumed perfect. Supplement: unmanned aerial vehicles (UAVs), while the manuscript writes uncrewed aerial vehicles.
Why it fails: PPO and CSI are used before their definitions (a table header counts as a use), and the supplement expands UAV with a different long form from the manuscript.

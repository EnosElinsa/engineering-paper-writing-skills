# Case 53: Long result-table caption with drifted terms
Skill: write-experiments
Expected gates: G-STY-cap
Language: en
Snippet:
> Comparison results of the five algorithms on the six test instances based on the mean and standard deviation (in parentheses) of HV, IGD, and the feasibility rate over 30 independent runs, where the best result on each instance is shown in bold. The setup section names the six settings Case 1 to Case 6.
Why it fails: the caption runs over 40 words where about 20 suffice, the run count and the bold rule belong in the table note, and the caption calls the settings instances while the setup calls them cases.

# Case 45: Display definitions out of order and quantities without symbols
Skill: latex-prose-audit
Expected gates: G-AUD-eq, G-AUD-sym
Language: en
Snippet:
> E = P_h T_h + P_f d / v, where v is the speed, P_h the hover power, and d the distance. The flight power P_f is defined in the next subsection. Thus, these quantities determine the energy of the available robots, namely the robots in S_t that are available.
Why it fails: symbols are defined out of display order, P_f is undefined at first use, Thus introduces an explanation, these quantities has no named referent, and the namely clause restates the set.

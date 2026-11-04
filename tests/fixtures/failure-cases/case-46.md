# Case 46: Captions in mixed forms and a display without a lead-in
Skill: latex-prose-audit
Expected gates: G-STY-cap, G-STY-eq
Language: en
Snippet:
> Fig. 3: Pareto Fronts (the proposed algorithm clearly dominates). Table IV: results. Algorithm 1: Station Relocation Procedure. The following equation gives the energy E = P_h T_h, and P_h is the hovering power.
Why it fails: the captions mix Title Case and sentence case, drop the final period, omit the instances and run rule, state a result, and the display is introduced by The following equation gives instead of a quantity-naming clause that ends in a colon.

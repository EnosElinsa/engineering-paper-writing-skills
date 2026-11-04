# Case 42: Result sentences mix artifacts and parallel sections differ in shape
Skill: write-experiments
Expected gates: G-EX-src, G-EX-shape
Language: en
Snippet:
> Table V lists the HV values 0.61, 0.58, and 0.66. As shown in Table V and Fig. 6, the variant converges faster and reaches a higher HV. (The next subsection opens with its conclusion, the one after it never states one.)
Why it fails: table-introducing prose recites values, one result sentence cites two artifacts for two claims, and the parallel subsections use different paragraph shapes, one without a scoped conclusion.

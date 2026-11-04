# Case 49: Comparison table built on the paper's own design
Skill: write-related-work
Expected gates: G-RW-table
Language: en
Snippet:
> Table I has seven columns: Charging, Handover, State transfer, Incremental sync, Feasible-interval mapping, Station slots, and Learning. Cells use a check mark, a circle for partial support with a note, or blank. Rows [12], [13], and [15] carry identical marks but appear separately.
Why it fails: two columns are this paper's design choices, one column is a trivial resource fact, a third symbol needs a note, and identical rows are not merged.

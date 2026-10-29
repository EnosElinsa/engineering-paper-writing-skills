# Acceptance fixtures

These files are manual or agent acceptance fixtures. No automated runner exists yet. The unit tests only check the gate identifiers that the fixtures name (`tests/gate-index.json` and `tests/test_gate_coverage.py`), not the behavior of an agent.

## Contents

- `failure-cases/case-01.md` to `case-25.md`: one synthetic, original snippet per documented failure case, at most 100 words. Cases 1 to 8 and 13 are in Chinese, matching the manuscript the cases came from. The others are in English. Cases 18 to 25 come from the patterns of supervisor edits and reviewer requests in a journal major revision; their snippets use other domains and invented numbers. Each file lists the skill to run and the gate identifiers that should be reported.
- `failure-cases/negative-control-*.md`: four descriptions, in our own words, of the functional structure of the scenario paragraphs of the four reference papers. They are not excerpts.

## How to use

1. For each failure case, give the snippet to the named skill in audit mode and ask for its gate report.
2. Pass when the report lists at least one of the expected gate identifiers for that case. Across the 25 cases, at least 24 should pass.
3. For each negative control, ask for the same audit on a paragraph that has the described structure. Pass when no hard failure is reported on the listed gates. A merge or length exception is allowed when the audit records its reason.
4. Record failures by case number and gate identifier. A missing identifier means the skill text lost the rule or no longer triggers it.

The gate identifiers appear in square brackets in the skill text, for example `[G-INT-15]`. The mapping from cases to identifiers is in `tests/gate-index.json`.

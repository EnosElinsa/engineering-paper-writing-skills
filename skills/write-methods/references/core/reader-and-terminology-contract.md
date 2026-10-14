# Reader and terminology contract

Applies to every section skill. Ledgers produced under this contract stay outside the manuscript (H).

## T. Terminology and plain-language contract

Default: describe, do not coin.

- T1 Prefer a plain descriptive phrase (verb + object, as the closest cited papers would write it) to a new noun. Coin a term only when the phrase would recur at least three times and the cited literature offers no usable term.
- T2 Define a coined term by its function in the sentence that first uses it. A bare parenthetical is not a definition. Abbreviations and short plain-word glosses ("i.e., how many units to allocate") are allowed.
- T3 One concept, one term. Use one word root per concept family; do not alternate process-root and role-root forms. Follow the root used by the closest cited papers.
- T4 In an Introduction, name a decision by what it changes and for whom, and an objective by its owner plus a one-clause meaning. Do not use variable-like compounds ("X-duration", "Y-overlap") before the reader knows why the quantity exists.
- T5 Keep a term ledger: term | definition by function | first use | variants found | external usage evidence or "not searched". Do not call a term standard or common without evidence in the ledger.
- T6 A coined term never first appears in a heading, caption, or equation label.
- T7 Delete a coined term if removing it lengthens no sentence.

The name of the paper's proposed mechanism is exempt from T1 but not from T2.

## A. Antecedent test

For each definite noun phrase, condition word, or demonstrative ("the trigger", "after handover", "this period"), the referent must be introduced earlier in the same paragraph, in the preceding paragraph of the same section, or be standard field terminology. Mark the first mention of every such expression and flag any whose first mention is missing or later.

## Q. Reader-question test

For every operation in a scenario, mechanism, or protocol description, the text must let the reader answer why the step exists or what it costs. If neither fits in one clause, move the step to the model section or cut it. Every sentence must be understandable without later sections.

## C. Claim types (working tag, not shown in the manuscript)

- L literature claim: needs a citation or bounded wording ("in the reviewed studies").
- D consequence of the paper's own definitions or of a standard property: no citation; state the premise ("a penalty term only lowers fitness, so it discourages but does not exclude violation").
- R own result: point to the section, table, or figure.
- K textbook knowledge: cite a textbook or drop the universal quantifier.

A sentence containing "cannot", "always", "all", "none", or "no existing work" needs a tag before it is kept.

## D. One proposition, one home

Keep a proposition ledger: proposition | home paragraph | other mentions. Default: explain a trade-off, gap, or limitation fully in one paragraph; other mentions are one clause (contributions, roadmap) or, in Related Work, at most three sentences that add paper-level evidence or a consequence the Introduction lacks, in different words. Deviate when a second paragraph adds an independent fact, and record the reason.

## S. Reference-scale protocol

Every range below is a default. Deviate when the venue limits length, an extra independent boundary needs its own unit, or the target family has no benchmark, and record the reason in the scale statement.

1. Default: with supplied reference papers, measure them with the counting rule below and write a three-line scale statement (paragraphs, words per paragraph, sentences in the key paragraph) as ranges before drafting.
2. Default: without references, use the domain pack's table as a weak prior and say so in the scale statement.
3. Default: keep the draft inside the declared ranges; a deviation is allowed when the reason is recorded.
4. Default: when the manuscript language differs from the references, convert word counts with a recorded ratio before comparing, and calibrate that ratio on one translated reference paragraph when possible. Sentence and paragraph counts transfer unchanged.
5. Default: when more than 20% over the upper bound, merge papers that share a predicate, drop paper-level numbers, cut announcement sentences ("In this subsection ..."), and keep one expanded closest work. Deviate when every paper carries an independent claim, and record the reason.

Counting rule. Paragraph: blank-line-delimited prose block of at least 20 words, page-break fragments merged, contribution bullets counted, headings, captions, tables, equations, and pseudocode excluded. Words: alphabetic tokens without citation brackets or inline math. Sentences: split at final punctuation before a capital letter, protecting "et al.", "Fig.", "e.g.", "i.e."; report as plus or minus one. Citations: expand ranges, count each bracketed number once per occurrence, and take unique numbers over the section body.

## H. Manuscript hygiene

Ledgers, term tables, novelty tables, audit results, and verification notes are working artifacts. Deliver them in the reply or a separate file, never in the manuscript body, an appendix, or a comment unless the user asks. An appendix holds paper content only (proofs, derivations, extra results).

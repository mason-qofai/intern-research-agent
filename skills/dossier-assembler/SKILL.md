name: dossier-assembler
description: Once the firm profile, portco compilation, portco profiles, financial estimates for portcos, source ratings, and confidence scores have been produced, assemble the dossier according to dossier-structure.md.

--

# dossier-assembler: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| firm_profile | object | yes | firm-profiler output |
| portfolio_list | list[object] | yes | portfolio-discoverer output |
| portco_profiles | list[object] | yes | portco-profiler output, one per company in scope |
| financial_estimates | list[object] | no | private-data-approximator output |
| confidence_tags | list[object] | yes | confidence-scorer output |
| source_tags | list[object] | yes | source-typer output |
| template_version | string | no, default latest | system |

## Output contract

A markdown document covering sections 1 through 6 of the dossier template, structured per the current template, with:

- Every load-bearing sentence carrying an inline confidence/source tag or footnote reference
- A citations section at the end, one entry per claim_id, link direct to document not homepage
- Engagement-level metrics kept in a separate section from opportunity-level (portfolio company) metrics, never merged
- No numeric claim appears without a confidence band attached
- Any subsection with no supporting source is written as explicitly unavailable in place, not omitted silently (e.g. "*Not available. No supporting source found.*")
- Section 7, "Review of Flagged and Satisfactory Content and Claims," is left as a placeholder heading only, with body text "*Pending audit-pass.*" dossier-assembler does not write section 7's content. That belongs to audit-pass, which runs after assembly and fills it in as the final step.
- **A required "Strategy Synthesis" subsection at the end of Section 1 (Firm Profile).** This is not a restatement of what the firm says about itself, that content already exists earlier in Section 1, cited to firm-profiler's claims. This subsection's job is to compare the firm's stated strategy against the actual, observed composition of its portfolio (from portfolio-discoverer and the portco-profiler profiles), and surface one or two non-obvious observations that the firm's own materials do not state directly. If the observation is just a paraphrase of something firm-profiler already asserted, it isn't synthesis, redo it. A synthesis claim is itself a claim: it needs a confidence band (usually medium at best, since it's inference layered on top of several underlying claims, never high) and a source_type of "public inference," with its reasoning chain stated plainly enough that a reader can check it against the same underlying claims.

**Worked example of the difference, using real Palladium data from this pipeline's own output:**

*Restatement, not synthesis (don't do this):* "Palladium positions itself as a thematic, verticalized investor, and has invested approximately $1.5 billion in the U.S. Hispanic market since 2000." This just repeats firm-profiler-012 and firm-profiler-027. No synthesis has happened, it's a citation with different words around it.

*Actual synthesis (do this):* "Despite the firm's Hispanic-market thesis being framed prominently in its own materials, the actual portfolio composition skews toward asset-light, recurring-revenue service platforms in fragmented, non-cyclical demand categories, immigration compliance software and legal services (Envoy Global), hospice durable medical equipment logistics (DME Express), behavioral health services (Health Connect America), rather than consumer-facing Hispanic-market retail or CPG plays. This suggests the Hispanic-market thesis functions more as a sourcing and underwriting differentiator, likely giving Palladium access to founder relationships and deal flow other sponsors don't have, than as a binding operating constraint on what the firm actually buys. *(synthesis-001, Medium, public inference: derived from comparing firm-profiler's stated thesis against the sector distribution actually observed across portfolio-discoverer's and portco-profiler's combined output, not stated directly by either)*."

That second example took two separately-sourced facts (the firm's stated thesis, and the actual sector composition of its holdings) that no single source stated together, and drew a conclusion neither source asserts on its own. That's what makes it non-obvious rather than descriptive.

Output is always the complete document, sections 1 through 6 (including the required Strategy Synthesis subsection) plus the section 7 placeholder. No diffs.

## Output format (hybrid) — note the exception

Every other skill in this pipeline outputs markdown plus a trailing JSON claims block. dossier-assembler is one of two exceptions (the other is audit-pass): its output is pure markdown, no trailing JSON. This is most of the terminal artifact a human reads, not an intermediate stage another skill parses, so the confidence/source tags get merged into the prose as inline markers or footnotes (per the bullet list above) rather than kept as a separate machine-readable block. audit-pass, the one skill downstream of this, takes the section-1-through-6 markdown (with the section 7 placeholder) as input, not a claims array, per its own input contract, and returns the same document with section 7 filled in.

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

Output is always the complete document, sections 1 through 6 plus the section 7 placeholder. No diffs.

## Output format (hybrid) — note the exception

Every other skill in this pipeline outputs markdown plus a trailing JSON claims block. dossier-assembler is one of two exceptions (the other is audit-pass): its output is pure markdown, no trailing JSON. This is most of the terminal artifact a human reads, not an intermediate stage another skill parses, so the confidence/source tags get merged into the prose as inline markers or footnotes (per the bullet list above) rather than kept as a separate machine-readable block. audit-pass, the one skill downstream of this, takes the section-1-through-6 markdown (with the section 7 placeholder) as input, not a claims array, per its own input contract, and returns the same document with section 7 filled in.

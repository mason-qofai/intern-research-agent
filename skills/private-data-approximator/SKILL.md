name: private-data-approximator
description: When no provided source gives a desired statistic for a portfolio company, use this skill. Search the web to identify comparable stats from publicly held companies. If a statistic is found or to be found in one of the sources/ directory files, this is not the right skill. Retrieve desired statistic from the web search and input into the portfolio company overview where it should be. This skill should stop being used when the desired statistic(s) for the current focus portfolio company is/are found.

--

# private-data-approximator: Input/Output Contract

Unlike the other seven skills, this skill uses live web search rather than
sources/. Per source-tier rules below, this is the one deliberate exception
to the pipeline's otherwise local-files-only sourcing model.

## Source-tier rules

This skill searches the web in two tiers, in order of preference:

**Tier 1, preferred: SEC/EDGAR.** For any comp company's own reported
financials (revenue, segment breakdown, margins), search and cite SEC
filings (10-K, 10-Q, proxy statements) directly. These are authoritative,
full-text, and never paywalled. Default here whenever the comp is a public
filer.

**Tier 2, permitted only when Tier 1 can't supply it: sector benchmarks and
methodology.** Adjustment factors, margin benchmarks, and market-position
discounts (the kind of finding a comp's own 10-K won't contain) may come
from other sources, industry association publications, government data
(BLS, Federal Reserve, Census), or investor relations pages, but only when
the skill can access and read the actual content, not a search-result
snippet or a paywalled excerpt it can't verify.

If a source is paywalled beyond the snippet, or the full text isn't
actually accessible, do not paraphrase from the visible fragment as if it
were the full finding. Treat it as unavailable for this run: either find a
different accessible source for the same figure, or, if none exists, treat
the comp or benchmark as unusable for this claim and consider whether the
resulting hop is now untraceable per the withheld rule below.

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| portco_profile | object | yes | portco-profiler output |
| comp_set_criteria | {sector, size_range, geography} | no | user, else inferred from portco_profile |
| known_multiples | list[{metric, value, source}] | no | user |

## Output contract

| Field | Type |
|---|---|
| revenue_band | string (low-high, currency, as-of year), or null if the estimate is withheld |
| ebitda_band | string (low-high), or null if the estimate is withheld |
| margin_assumption | string (percent range), or null if the estimate is withheld |
| comp_set_used | list[{company, metric, value, source_url, tier: "sec_edgar" or "other_accessible"}] |
| methodology_note | string, explains how the band was derived, or why it was withheld |
| confidence | must be "low" or "medium", never "high" (this output is inherently an estimate); null if withheld |
| source_type | must be "public inference" (no private inference category, the target fact being private doesn't change the classification); null if withheld |
| withheld | boolean |

This skill must never label its own output as source_type "public document." If it does, that's a bug in the skill logic worth flagging in audit-pass.

If the only available comp differs from the target company in scale, business model, or market position, and there is no named source tying the two together (no documented adjustment factor, no comp of similar scale), the hop is untraceable. Do not apply the comp anyway at low confidence. Set `withheld: true`, leave the band fields null, and explain in `methodology_note` why the comp doesn't support even a wide-band estimate. A margin benchmark should not be compounded onto a revenue figure that was itself withheld.

## Output format (hybrid)

Output is a markdown body (methodology_note as prose, comp_set_used as a short table) followed by a trailing fenced JSON block titled `## Claims`. Unlike the other research skills, this skill fills `confidence` and `source_type` itself rather than leaving them `null` (except when withheld, where both are null by design), since the constraint on those fields (never "high," never "public document") is this skill's own responsibility to enforce, not confidence-scorer's or source-typer's:

```json
[
  {
    "claim_id": "private-data-approximator-<company>-001",
    "field": "revenue_band",
    "text": "one-sentence statement of the estimate and its basis, or of why it was withheld",
    "confidence": "low",
    "source_type": "public inference",
    "withheld": false,
    "citation": "SEC filing URL, or other source URL only if the full content was actually read (not a search snippet), null if none"
  }
]
```

confidence-scorer and source-typer still run over these claims in the batch pass like any other, but should treat this skill's self-assigned values as a strong prior, not overwrite them without a documented reason in audit-pass. Withheld claims are excluded from confidence-scorer and source-typer's batch entirely, since there is nothing to rate.

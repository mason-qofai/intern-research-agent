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
| revenue_band | string (low-high, currency, as-of year), wide if directional, or null only if withheld |
| ebitda_band | string (low-high), wide if directional, or null only if withheld |
| margin_assumption | string (percent range), or null only if withheld |
| comp_set_used | list[{company, metric, value, source_url, tier: "sec_edgar" or "other_accessible"}] |
| methodology_note | string, explains how the band was derived, explicitly states if the estimate is directional (mismatched comp) rather than analytical (well-matched comp), or explains why it was withheld |
| estimate_type | enum: "analytical" (comp closely matches scale/model), "directional" (comp mismatched, band widened accordingly), or null if withheld |
| confidence | must be "low" or "medium", never "high" (this output is inherently an estimate); null if withheld |
| source_type | must be "public inference" (no private inference category, the target fact being private doesn't change the classification); null if withheld |
| withheld | boolean, true only when no usable comp exists at all, not merely a mismatched one |

This skill must never label its own output as source_type "public document." If it does, that's a bug in the skill logic worth flagging in audit-pass.

If the only available comp differs from the target company in scale, business model, or market position, and there is no named source tying the two together (no documented adjustment factor, no comp of similar scale), do not withhold by default. Produce a wide-band, explicitly labeled directional estimate instead: state the comp used, name the specific mismatch (scale, business model, market position), and widen the band enough to reflect that mismatch rather than presenting a false-precision range. Confidence for this kind of estimate is always `low`. The methodology note must say in plain language that this is a directional estimate from a mismatched comp, not an analytical one, so a reader never mistakes the width of the caveat for the width of the number.

Reserve `withheld: true` for the narrower case where no usable comp exists at all, not merely a mismatched one, e.g. the sector has no public company remotely comparable, every candidate comp is defunct, unreadable, or itself unverifiable, or a margin benchmark would have to compound onto a revenue figure that has nothing under it. Withholding should be the exception now, not the default outcome whenever a comp isn't a close match. A wide range with a stated reason for its width is more useful to the reader than no range at all, provided the estimate is honestly labeled as directional rather than dressed up as more precise than it is.

A margin benchmark should still not be compounded onto a revenue figure that was itself withheld under the narrower rule above; two compounded approximations from a genuinely unusable base would produce a number with nothing real underneath it.

## Output format (hybrid)

Output is a markdown body (methodology_note as prose, comp_set_used as a short table) followed by a trailing fenced JSON block titled `## Claims`. Unlike the other research skills, this skill fills `confidence` and `source_type` itself rather than leaving them `null` (except when withheld, where both are null by design), since the constraint on those fields (never "high," never "public document") is this skill's own responsibility to enforce, not confidence-scorer's or source-typer's:

```json
[
  {
    "claim_id": "private-data-approximator-<company>-001",
    "field": "revenue_band",
    "text": "one-sentence statement of the estimate, its comp, and whether it's directional or analytical, or of why it was withheld",
    "confidence": "low",
    "source_type": "public inference",
    "estimate_type": "directional",
    "withheld": false,
    "citation": "SEC filing URL, or other source URL only if the full content was actually read (not a search snippet), null if none"
  }
]
```

confidence-scorer and source-typer still run over these claims in the batch pass like any other, but should treat this skill's self-assigned values as a strong prior, not overwrite them without a documented reason in audit-pass. Withheld claims are excluded from confidence-scorer and source-typer's batch entirely, since there is nothing to rate.

confidence-scorer and source-typer still run over these claims in the batch pass like any other, but should treat this skill's self-assigned values as a strong prior, not overwrite them without a documented reason in audit-pass. Withheld claims are excluded from confidence-scorer and source-typer's batch entirely, since there is nothing to rate.

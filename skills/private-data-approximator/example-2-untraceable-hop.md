# private-data-approximator — Example 2 (untraceable hop, flagged)

Scope note: this example shows that the withheld outcome is about the
comp itself not being defensible, it is not a source-access problem. The
one comp here is a fully accessible SEC filing, tier 1, no paywall issue
at all. It's withheld anyway, because scale and payer mix aren't bridged
by any named adjustment factor, contrast with example 1 where three hops
survive because each is tied to something specific.

## INPUT

```
company_name: "Briarwood Dental Partners"
known_facts:
  - "four dental practice locations, San Antonio and New Braunfels, Texas"
comp_set:
  - name: "Publicly traded dental service organization, National Co."
    source: "10-K, most recent fiscal year, segment revenue footnote"
    metric: "revenue per location, TTM"
    value_range_usd: "1.2M - 2.8M"
    tier: sec_edgar
    note: "National Co. operates 400+ locations nationally."
  - name: "Sector EBITDA margin benchmark, dental DSOs"
    source: "industry association publication, full report accessed and
      read directly"
    value_range_pct: "15% - 25%"
    tier: other_accessible
    note: "benchmark spans DSOs of all sizes, not segmented by scale."
```

## OUTPUT

```markdown
### Financial Approximation: Briarwood Dental Partners

The only available comp, National Co., operates at a scale, 400+ locations,
and a likely payer mix that differ substantially from a 4-location regional
DSO. Applying National Co.'s per-location revenue to Briarwood would extend
a large-scale operator's economics onto a business with a different cost
structure and payer negotiating position. Nothing in the source material
ties these two businesses' unit economics together, there is no named
comp closer in scale, and no documented adjustment factor the way example 1
had a secondary-market discount figure to lean on. That hop, applying
National Co.'s multiple directly to Briarwood, is not traceable to a
specific piece of evidence.

Flagged for human review rather than published as a low confidence
estimate. We do not have a comp we can defend as similar enough to produce
even a wide band. If a smaller-scale regional DSO comp becomes available,
or a documented scale-adjustment factor like the one used in example 1,
this can be revisited.

We do not apply the EBITDA margin benchmark here either. Compounding a
margin band onto a revenue figure we've already declined to publish would
produce a number with no real grounding underneath it.
```

## Claims

```json
[
  {
    "claim_id": "private-data-approximator-briarwood-001",
    "field": "revenue_band",
    "text": "No revenue estimate published. The only available comp, National Co. (400+ locations), differs too much in scale and likely payer mix from a 4-location regional DSO, with no named comp closer in scale and no documented scale-adjustment factor tying the two together.",
    "confidence": null,
    "source_type": null,
    "withheld": true,
    "citation": null
  },
  {
    "claim_id": "private-data-approximator-briarwood-002",
    "field": "ebitda_band",
    "text": "No EBITDA estimate published. The sector margin benchmark is not applied here, compounding a margin band onto a revenue figure that was itself withheld would produce a number with no real grounding.",
    "confidence": null,
    "source_type": null,
    "withheld": true,
    "citation": null
  }
]
```

Both claims are withheld, not rated at low confidence. There is no comp defensible as similar enough to produce even a wide band, and this has nothing to do with source access, the comp is a fully readable, tier-1 SEC filing. The withholding is about the missing scale-adjustment factor, not about where the data came from. If a smaller-scale regional DSO comp or a documented adjustment factor becomes available, this can be revisited. Withheld claims are excluded from confidence-scorer's and source-typer's batch passes entirely, per contract, since there is nothing to rate.

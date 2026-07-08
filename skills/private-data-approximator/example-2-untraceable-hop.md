# private-data-approximator — Example 2 (mismatched comp, directional estimate, plus contrast with genuine withholding)

Scope note: withholding is now the exception, not the default outcome
whenever a comp isn't a close match. This example shows the new default,
a mismatched comp still produces a wide, explicitly labeled directional
estimate, contrasted with a short second case where withholding is still
correct because no usable comp exists at all, not merely a mismatched one.

## Case A: mismatched comp, directional estimate (the new default)

### INPUT

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

### OUTPUT

```markdown
### Financial Approximation: Briarwood Dental Partners

The only available comp, National Co., operates at a scale, 400+ locations,
and a likely payer mix that differ substantially from a 4-location regional
DSO. There is no named comp closer in scale and no documented
scale-adjustment factor tying the two businesses' unit economics together.
Per the current rule, this does not mean withholding by default, it means
producing a directional estimate with a band wide enough to reflect the
mismatch, clearly labeled as such rather than dressed up as more precise
than it is.

Applying National Co.'s per-location revenue of $1.2M-$2.8M directly would
overstate a much smaller operator's economics, a large multi-market chain
typically captures payer contracts and referral volume a 4-location
regional practice cannot. Widening substantially to account for that scale
gap, a directional range of $1.5M-$4.5M in annual revenue is a defensible
order-of-magnitude estimate, not an analytical one.

Applying the sector EBITDA margin benchmark (15%-25%) to that range gives a
directional EBITDA estimate of roughly $225K-$1.1M. This benchmark spans
DSOs of all sizes, so it is a reasonable input for a directional estimate
even though it isn't scale-segmented, unlike example 1's estimate, which
had a named, scale-specific discount factor and stayed in analytical rather
than directional territory as a result.

**Explicit caveat:** this range is directional, not analytical. It exists
to give a sense of scale from the best available public reference point,
not to substitute for real diligence. The width of the band reflects the
size of the mismatch between Briarwood and its only available comp.
```

### Claims

```json
[
  {
    "claim_id": "private-data-approximator-briarwood-001",
    "field": "revenue_band",
    "text": "Directional estimate $1.5M-$4.5M, from National Co.'s per-location revenue widened substantially for the ~100x scale mismatch between a 400+ location chain and a 4-location regional DSO, no named adjustment factor exists so the band is wide rather than precise.",
    "confidence": "low",
    "source_type": "public inference",
    "estimate_type": "directional",
    "withheld": false,
    "citation": "National Co. 10-K, segment revenue footnote (tier: sec_edgar)"
  },
  {
    "claim_id": "private-data-approximator-briarwood-002",
    "field": "ebitda_band",
    "text": "Directional estimate $225K-$1.1M, from the revenue band above applied against a sector-wide (not scale-segmented) EBITDA margin benchmark.",
    "confidence": "low",
    "source_type": "public inference",
    "estimate_type": "directional",
    "withheld": false,
    "citation": "sector EBITDA margin benchmark, dental DSOs (tier: other_accessible, full text confirmed readable)"
  }
]
```

## Case B: no usable comp at all, genuine withholding

Contrast case, condensed. A different company in the same portfolio,
Envoy Global (corporate immigration services and technology), had every
candidate comp rejected outright, not merely mismatched:

```markdown
### Financial Approximation: Envoy Global

Cartus and Anywhere Real Estate (NYSE: HOUS) were considered as potential
comps on the theory that both involve corporate relocation services, but
neither is close enough in business model, Anywhere Real Estate's core
business is residential real estate brokerage, relocation is a minor
segment with no separately reported financials, not a scale mismatch that
a wide band could absorb, but a business model mismatch with nothing
comparable to widen from. No other public company combining immigration
legal services with a proprietary technology platform was identified.

This is the narrower case where withholding is still correct: there is no
comp to produce even a directional estimate from, not merely a mismatched
one. Widening the band on an already-wrong business model doesn't produce
a meaningful range, it produces a number with nothing real underneath it.
```

```json
[
  {
    "claim_id": "private-data-approximator-envoy-global-001",
    "field": "revenue_band",
    "text": "No estimate produced, directional or otherwise. No public company combining immigration legal services with a proprietary technology platform was identified; the one candidate considered (Anywhere Real Estate) differs in core business model, not merely scale, and widening the band would not produce a meaningful range.",
    "confidence": null,
    "source_type": null,
    "estimate_type": null,
    "withheld": true,
    "citation": null
  }
]
```

The distinction that matters: Case A had a comp in the same actual
business (dental services) at the wrong scale, a wide band still means
something there. Case B had no comp in the same business at any scale, a
wide band would just be a guess wearing a number's clothes. Withheld
claims are excluded from confidence-scorer's and source-typer's batch
passes entirely, per contract, since there is nothing to rate; directional
claims are not excluded, they go through the batch like any other claim.

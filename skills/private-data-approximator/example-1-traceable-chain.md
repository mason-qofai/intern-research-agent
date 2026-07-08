# private-data-approximator — Example 1 (traceable comps chain, SEC-first)

Scope note: this skill's output is still public inference, not a third
category. The target fact being private (the company's actual revenue)
does not change the classification of the claim, which is a conclusion
reasoned from public inputs. This example also shows the source-tier rule
in practice: the two comp companies' own figures come straight from their
10-Ks (tier 1), the discount factor and margin benchmark come from a
sector report the skill confirmed it could read in full, not a paywalled
snippet (tier 2, permitted only because tier 1 doesn't cover this).

## INPUT

```
company_name: "Anchor Point Logistics"
known_facts:
  - "16 facilities, cold-chain healthcare logistics, Southeast plus Texas"
comp_set:
  - name: "ColdChain Corp (public, NYSE-listed)"
    source: "10-K, most recent fiscal year, segment revenue footnote"
    metric: "revenue per facility, TTM"
    value_range_usd: "3.5M - 5.0M"
    tier: sec_edgar
  - name: "Frostline Logistics Inc (public, Nasdaq-listed)"
    source: "10-K, most recent fiscal year, segment revenue footnote"
    metric: "revenue per facility, TTM"
    value_range_usd: "4.0M - 6.5M"
    tier: sec_edgar
  - name: "Sector report, secondary vs. flagship market facility revenue"
    source: "industry association publication, full report accessed and
      read directly, not a search snippet"
    finding: "secondary-market facilities run 15-20% below flagship-market
      facilities in the same comp set, per the same report's methodology
      section"
    tier: other_accessible
  - name: "Sector EBITDA margin benchmark, cold-chain logistics"
    source: "same industry association publication as above"
    value_range_pct: "12% - 18%"
    tier: other_accessible
```

## OUTPUT

```markdown
### Financial Approximation: Anchor Point Logistics

Two public cold-chain 3PL comps, ColdChain Corp and Frostline Logistics,
report revenue per facility of $3.5M-$5.0M and $4.0M-$6.5M in their most
recent 10-Ks [pub-doc][high]. Pooling these gives a per-facility range of
roughly $3.5M-$6.5M. Applied to Anchor Point's 16 facilities, that's
$56M-$104M [pub-inf][medium], one hop from two named, filed comps.

Anchor Point operates in Southeast and Texas secondary markets, not the
flagship markets the top end of the comp range likely reflects. A sector
report's methodology section, read in full rather than from a search
snippet, states secondary-market facilities run 15-20% below
flagship-market facilities in the same comp set [pub-doc][high]. Applying
that discount to the pooled range narrows the estimate to roughly
$60M-$95M [pub-inf][low], a second hop, tied to the named discount figure
rather than an unstated judgment call.

Applying the same report's sector EBITDA margin benchmark of 12%-18%
[pub-doc][high] to that revenue band gives an estimated EBITDA range of
$7.2M-$17.1M [pub-inf][low], a third hop tied to the margin benchmark. We
present this as a wide band, not a point estimate, since two compounded
approximate ranges should widen uncertainty rather than narrow it toward a
false-precision midpoint.

**Explicit caveat:** this is a comps-based approximation, not a disclosed
figure. No source states Anchor Point's actual revenue or EBITDA. The
estimated framing and confidence bands travel with this figure into any
downstream use.
```

## Claims

```json
[
  {
    "claim_id": "private-data-approximator-anchorpoint-001",
    "field": "revenue_band",
    "text": "Estimated revenue $60M-$95M, from pooled per-facility comps (two SEC-filed 10-Ks) applied to 16 facilities, adjusted by a named secondary-market discount factor from a fully-read sector report.",
    "confidence": "low",
    "source_type": "public inference",
    "estimate_type": "analytical",
    "withheld": false,
    "citation": "ColdChain Corp 10-K and Frostline Logistics 10-K (tier: sec_edgar), plus sector report secondary-vs-flagship discount finding (tier: other_accessible, full text confirmed readable)"
  },
  {
    "claim_id": "private-data-approximator-anchorpoint-002",
    "field": "ebitda_band",
    "text": "Estimated EBITDA $7.2M-$17.1M, from the revenue band above applied against a named sector EBITDA margin benchmark.",
    "confidence": "low",
    "source_type": "public inference",
    "estimate_type": "analytical",
    "withheld": false,
    "citation": "sector EBITDA margin benchmark, cold-chain logistics (tier: other_accessible, same report as above, full text confirmed readable)"
  }
]
```

Three hops, but every hop is tied to a named, accessible source, two SEC
filings and one fully-read sector report, so the chain is rateable, ceiling
is low given the hop count. This is the traceable-chain case, contrast with
example 2's untraceable hop, which gets withheld instead of rated. Note
that the two comp figures are tier 1 (SEC/EDGAR), the discount and margin
figures are tier 2, permitted here only because no 10-K contains a
cross-company secondary-market discount or a sector-wide margin benchmark,
that kind of finding doesn't exist in a single filing.

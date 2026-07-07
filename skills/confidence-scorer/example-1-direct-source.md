# confidence-scorer — Example 1 (batch pass, directly sourced claims)

Scope note: this skill runs once per dossier, over the full claims list
produced by every upstream skill, not once per claim. This example shows a
small batch to demonstrate the shape; a real run's batch is much larger.

## INPUT

```json
[
  {
    "claim_id": "firm-profiler-cobalt-002",
    "claim_text": "Cobalt Bridge Partners is SEC-registered, reporting $2.1B in regulatory AUM and 38 employees.",
    "evidence": "SEC Form ADV, field regulatory_aum_usd = 2,100,000,000, employee_count = 38. Zero hops."
  },
  {
    "claim_id": "firm-profiler-cobalt-006",
    "claim_text": "Given the EBITDA band and stated add-on focus, portfolio companies are more likely to grow through acquisition than organic revenue expansion alone.",
    "evidence": "Reasoned by combining the firm's stated EBITDA target range with its stated add-on acquisition focus, two separate source pages, no single source states this conclusion directly. One hop, tied to two named sources."
  }
]
```

## OUTPUT

```json
[
  {
    "claim_id": "firm-profiler-cobalt-002",
    "confidence": "high",
    "rationale": "restates a single field from a primary regulatory filing, zero hops, no combination with any other source",
    "flagged": false
  },
  {
    "claim_id": "firm-profiler-cobalt-006",
    "confidence": "medium",
    "rationale": "one hop, but the hop combines two named, specific source statements rather than introducing an unstated judgment call, so it doesn't fall to low",
    "flagged": false
  }
]
```

High confidence is reserved for a claim with a primary document directly behind it and nothing standing between the two, zero hops. The second claim shows a one-hop claim staying at medium rather than dropping further, since the hop is tied to two specific, named sources rather than an unsupported inference.

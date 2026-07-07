name: confidence-scorer
description: Once claims have been produced, classify each claim's confidence as high, medium, or low. Refer to confidence-rubric.md for classification rules. Should run once. Done using skill after all claims have been rated.

--

# confidence-scorer: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| claims | list[{claim_id, claim_text, evidence}] | yes | any upstream skill output |
| rubric_version | string | no, default latest | system |

## Output contract

| Field | Type |
|---|---|
| claim_id | string |
| confidence | enum: high / medium / low; null if flagged |
| rationale | string, one sentence, why this band (or why flagged) |
| flagged | boolean |

High is reserved for a claim restating a single field from a primary source directly, zero hops. Confidence decreases as hop count increases, but only for hops that are each tied to a specific named source. Hop count sets a ceiling on how low the band can go; it does not by itself disqualify a claim from being rated at all.

An untraceable hop, one with no named comp, source, or documented adjustment factor behind it, disqualifies the claim from getting any confidence band, no matter how few hops came before it. Set `flagged: true`, leave `confidence` null, and explain in `rationale` why the chain breaks. This is source-typer's flag branch surfacing here too, since a claim source-typer already flagged as untraceable never reaches confidence-scorer with a rateable chain behind it.

Rationale is required so a human reviewer (or audit-pass) can check the scoring rather than trust it blind.

## Output format (hybrid)

No markdown body. This skill takes the full claims list in as one batch and hands the same list back with `confidence` (or `flagged`) filled in for every claim, in one call. It does not run per claim; the rubric is comparative by nature (a three-hop claim with every hop named can rate lower but still rateable, next to a one-hop claim with an untraceable link that can't be rated at all), and a batch call can hold that comparison in view in a way a per-claim call cannot.

```json
[
  {
    "claim_id": "firm-profiler-001",
    "confidence": "high",
    "rationale": "one sentence",
    "flagged": false
  },
  {
    "claim_id": "portfolio-discoverer-004",
    "confidence": null,
    "rationale": "one-sentence explanation of the untraceable hop",
    "flagged": true
  }
]
```

Output must cover every claim_id received as input. Missing a claim_id is a contract violation, not a valid "skip." Claims already flagged by source-typer should be passed through as flagged here too rather than re-evaluated, there's no confidence band to assign to a claim with no valid source type.

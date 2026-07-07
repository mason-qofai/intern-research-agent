# source-typer — Example 1 (batch pass, public documents)

Scope note: this skill runs once per dossier, over the full claims list, not
once per claim.

## INPUT

```json
[
  {
    "claim_id": "firm-profiler-cobalt-003",
    "claim_text": "Cobalt Bridge Partners closed its fourth flagship fund at $850 million in November 2025.",
    "evidence": "Restated directly from a press release published by the firm."
  },
  {
    "claim_id": "portfolio-discoverer-cobalt-001",
    "claim_text": "Anchor Point Logistics is a current portfolio company, healthcare logistics, acquired 2021.",
    "evidence": "Restated directly from the firm's published portfolio page."
  }
]
```

## OUTPUT

```json
[
  {
    "claim_id": "firm-profiler-cobalt-003",
    "source_type": "public document",
    "evidence_url_or_note": "press release, direct restatement, no combination or extrapolation",
    "flagged": false
  },
  {
    "claim_id": "portfolio-discoverer-cobalt-001",
    "source_type": "public document",
    "evidence_url_or_note": "firm's own published portfolio page, direct restatement",
    "flagged": false
  }
]
```

Test for public document: could someone find this exact statement by opening the cited source directly. Yes for both, that's what separates public document from public inference.

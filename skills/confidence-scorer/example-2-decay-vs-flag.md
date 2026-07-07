# confidence-scorer — Example 2 (batch pass, chain decay versus the flag branch)

Scope note: length alone doesn't cap a claim, an untraceable hop does. This
batch contrasts a long but traceable chain against a short but untraceable
one, since the two get treated very differently. This is also why the
skill runs as a batch: comparing claims against each other is easier when
both are visible in the same call.

## INPUT

```json
[
  {
    "claim_id": "private-data-approximator-anchorpoint-001",
    "claim_text": "Anchor Point Logistics generates approximately $60-95 million in annual revenue.",
    "evidence": "Chain: 16 facilities (pub-doc) -> pooled per-facility comp range $3.5M-$6.5M from two named public comps (pub-doc) -> secondary-market discount of 15-20% from a named sector report (pub-doc). Three hops, each tied to a named source."
  },
  {
    "claim_id": "private-data-approximator-briarwood-000",
    "claim_text": "Briarwood Dental Partners likely generates single-digit-million revenue, based on National Co.'s per-location multiple.",
    "evidence": "Chain: National Co.'s per-location revenue $1.2M-$2.8M (pub-doc) -> applying that multiple to Briarwood's 4 locations, no named comp or factor ties National Co.'s scale (400+ locations) to Briarwood's. One hop, untraceable."
  }
]
```

## OUTPUT

```json
[
  {
    "claim_id": "private-data-approximator-anchorpoint-001",
    "confidence": "low",
    "rationale": "three hops, but every hop names its evidence, two comps and a documented discount factor; length pushes this down from high or medium, but each hop is traceable, so it's rateable",
    "flagged": false
  },
  {
    "claim_id": "private-data-approximator-briarwood-000",
    "confidence": null,
    "rationale": "one hop, but the hop itself has nothing behind it, no comp of similar scale, no documented adjustment factor; a single untraceable hop disqualifies a claim the same way three would",
    "flagged": true
  }
]
```

The distinction that matters: hop count predicts how low a rating can go, it does not predict whether a rating applies at all. That's decided by whether every hop is tied to something specific. Claim B is not rated at low confidence, it's flagged, a distinct outcome, and does not enter the dossier until a human resolves it.

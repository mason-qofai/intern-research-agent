name: source-typer
description: Once the claims have all been produced, use this skill to correctly classify each claim’s source:  public inference or public document. Refer to the source-rubric.md for classification rules. Should run once. Done using skill after all claims have been rated.

--

# source-typer: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| claims | list[{claim_id, claim_text, evidence}] | yes | any upstream skill output |

## Output contract

| Field | Type |
|---|---|
| claim_id | string |
| source_type | enum: public document / public inference (no private inference category; a claim about a private target fact is still public inference if it's reasoned entirely from public, citable inputs) |
| evidence_url_or_note | string, null if flagged |
| flagged | boolean |

If evidence is a document, `evidence_url_or_note` is a URL: could a third party open the cited source directly and find this exact statement. If yes, public document. If evidence is inference (e.g. estimating revenue from comps), the note describes the reasoning chain in one sentence: could a third party reach this same claim using only the cited public sources and the stated reasoning. If yes, public inference, regardless of whether the underlying fact itself is private.

If a claim depends on something not tied to a specific, named public source, the reasoning chain doesn't hold up under either category. Set `flagged: true`, leave `source_type` and `evidence_url_or_note` null, and explain in a `flag_reason` field why the claim has nowhere to go under this rubric. This is a distinct outcome from a low-confidence public inference, not a third source_type. A flagged claim does not proceed to the dossier until a human resolves it.

## Output format (hybrid)

No markdown body, same reasoning as confidence-scorer: this skill takes a claims list in as one batch and hands the same list back with `source_type` (or `flagged`) filled in for every claim, in one call. It does not run per claim.

```json
[
  {
    "claim_id": "firm-profiler-001",
    "source_type": "public document",
    "evidence_url_or_note": "url, or one-sentence inference chain",
    "flagged": false
  },
  {
    "claim_id": "portfolio-discoverer-004",
    "source_type": null,
    "evidence_url_or_note": null,
    "flagged": true,
    "flag_reason": "one-sentence explanation of the untraceable hop"
  }
]
```

Output must cover every claim_id received as input. Skipping a claim_id is a contract violation, not a valid outcome, even for a claim that ends up flagged.

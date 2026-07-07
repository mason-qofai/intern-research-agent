# source-typer — Example 2 (batch pass, a private target does not mean a private source type)

Scope note: there is no private inference category. A conclusion about a
privately held company's financials is still public inference if it's
reasoned from public inputs. The word "private" in
"private-data-approximator" describes what's being estimated, not the
source type of the estimate.

## INPUT

```json
[
  {
    "claim_id": "firm-profiler-fernhollow-002",
    "claim_text": "Fernhollow Capital was likely founded around 2018-2019, based on a LinkedIn bio stating a principal has 'seven years running the firm.'",
    "evidence": "Reasoning across a public LinkedIn statement plus arithmetic against the current year."
  },
  {
    "claim_id": "private-data-approximator-anchorpoint-002",
    "claim_text": "Anchor Point Logistics likely generates $7.2M-$17.1M in EBITDA, based on comps-derived revenue and a sector margin benchmark.",
    "evidence": "The target fact, this company's actual EBITDA, is private and never disclosed. The claim is reasoned entirely from public comps and a public margin benchmark, both named and citable."
  }
]
```

## OUTPUT

```json
[
  {
    "claim_id": "firm-profiler-fernhollow-002",
    "source_type": "public inference",
    "evidence_url_or_note": "reproducible by anyone with the same public LinkedIn statement and the arithmetic against the current year",
    "flagged": false
  },
  {
    "claim_id": "private-data-approximator-anchorpoint-002",
    "source_type": "public inference",
    "evidence_url_or_note": "reproducible by anyone with the same public comps and margin benchmark; the target fact being non-public doesn't change this",
    "flagged": false
  }
]
```

The test that separates these from a claim that shouldn't be rated at all: could a third party reach this claim using only the cited public sources and the stated reasoning. For both, yes. If the answer were no, because the claim actually depended on something we know but can't point to a public source for, that claim would have nowhere to go under this rubric, and it should be flagged rather than typed under either label.

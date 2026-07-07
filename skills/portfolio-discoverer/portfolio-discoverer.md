name: portfolio-discoverer
description: When attempting to identify portfolio companies of a given PE firm, search through sources/ directory to identify all apparent portfolio companies. This compilation is the basis of portfolio company overview section of the dossier. If no portfolio companies are discoverable from sources/ directory files, don’t assemble list of portfolio companies. When all sources have been checked for a new portfolio company, the skill has served its purpose and should stop being used.

--

# portfolio-discoverer: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| firm_name | string | yes | user or firm-profiler output |
| firm_profile | object | no | firm-profiler output |
| scope | enum: active_only / active_and_exited | no, default active_only | user |
| max_results | int | no, default 25 | user |

## Output contract

A list of portfolio company entries:

| Field | Type |
|---|---|
| company_name | string |
| status | enum: active / exited |
| sector | string |
| acquisition_date | string (YYYY-MM or YYYY, nullable) |
| exit_date | string, nullable |
| stake_type | enum: majority / minority / unknown |
| source_url | string |
| confidence | enum: high / medium / low |
| source_type | enum: public document / public inference (no private inference category) |

Duplicate entries (same company, different name spellings) must be merged before output, not left for downstream skills to catch.

A candidate portfolio company whose evidence chain has an untraceable hop (e.g. a name match across unrelated filings, with no source stating the firm relationship directly) is not published as a low-confidence entry. It is withheld from the table and raised separately as a flagged candidate, with the chain of evidence explained, for human review. This is a different bucket from confidence, not the bottom of the confidence scale.

## Output format (hybrid)

Output is a short markdown body (one line per company, e.g. "- Acme Corp, active, acquired 2019") followed by a trailing fenced JSON block titled `## Claims`:

```json
[
  {
    "claim_id": "portfolio-discoverer-001",
    "field": "company_name",
    "text": "Acme Corp is an active portfolio company, acquired 2019",
    "confidence": null,
    "source_type": null,
    "citation": "url or filename, or null if uncited"
  }
]
```

If no portfolio companies are discoverable, the markdown body says so plainly and the Claims block is an empty array, not omitted entirely. `confidence` and `source_type` stay `null` here, filled in downstream.

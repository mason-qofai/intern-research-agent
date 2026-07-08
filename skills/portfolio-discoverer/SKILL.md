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

## Flagged candidates: two distinct reasons, not one bucket

A candidate does not get published as a normal, ratable entry, confidence and source_type left for downstream scoring, in either of these two cases. Both are withheld from the table and raised separately for human review, but they are different problems and must be labeled with which one applies, so a human reviewer knows what kind of judgment call they're being asked to make:

**`untraceable_hop`**: the evidence chain connecting the firm to the company has a gap, e.g. a name match across unrelated filings with no source stating the relationship directly. The problem here is a missing link.

**`conflicting_status`**: multiple sources establish the relationship clearly, no gap in the chain, but they disagree with each other on a material fact, most commonly active-vs-exited status. Example: the firm's own portfolio page presents a company in the present tense with no exit language, while the firm's own fact sheet lists the same company under exited investments as of a specific date. The problem here is not a missing link, it's a direct contradiction between two sources that are each individually credible. Do not resolve this by picking whichever source seems more current or more official, an explicit human call, not a model guess.

A flagged claim must always include a `field: "company_name"` (see below) and a `flag_reason` naming which of these two applies, along with a one or two sentence explanation of the specific conflict or gap. Do not write the explanation as a long, unstructured sentence appended in place of a name, that has caused this exact claim type to be silently misrouted downstream before, structure it as shown in the format below instead.

## Output format (hybrid)

Output is a short markdown body (one line per company, e.g. "- Acme Corp, active, acquired 2019") followed by a trailing fenced JSON block titled `## Claims`. Every claim, flagged or not, must carry a `company_name` field holding only the company's name, nothing else, this is a required field precisely so nothing downstream ever has to extract a name by parsing the `text` field's prose:

```json
[
  {
    "claim_id": "portfolio-discoverer-001",
    "field": "company_name",
    "company_name": "Acme Corp",
    "text": "Acme Corp is an active portfolio company, acquired 2019",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "url or filename, or null if uncited"
  },
  {
    "claim_id": "portfolio-discoverer-002",
    "field": "company_name",
    "company_name": "Del Real Foods",
    "text": "Status disputed: firm's Dec 2025 fact sheet lists this company as exited, firm's own portfolio page presents it as active with no exit language",
    "confidence": null,
    "source_type": null,
    "flagged": true,
    "flag_reason": "conflicting_status",
    "citation": "fact sheet URL/filename and portfolio page URL, both"
  }
]
```

If no portfolio companies are discoverable, the markdown body says so plainly and the Claims block is an empty array, not omitted entirely. `confidence` and `source_type` stay `null` here, filled in downstream, for both flagged and unflagged claims (a flagged claim never receives a confidence band or source_type, per confidence-scorer and source-typer's own contracts, which exclude pre-flagged claims from their batch entirely).

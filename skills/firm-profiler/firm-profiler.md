name: firm-profiler
description: Applicable when beginning the dossier and looking to write a firm overview. Produce a research dossier on a private equity firm from local source files (PDFs, notes) dropped in a sources/ directory. Identify key statistics, leaders, investment strategies and ethos that provide general knowledge of the firm. After all sources have been checked for relevant information, the skill should stop being used. This skill is to be used to profile the PE firm itself, not portfolio companies. 

--

# firm-profiler: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| firm_name | string | yes | user |
| firm_website | string (URL) | no | user |
| known_aliases | list[string] | no | user |
| research_depth | enum: quick / standard / deep | no, default standard | user |

## Output contract

A firm profile object with these fields, each carrying `confidence` (high/medium/low) and `source_type` (public document/public inference; there is no private inference category, a claim about a private fact reasoned from public inputs is still public inference):

| Field | Type |
|---|---|
| legal_name | string |
| aum | string (range or point estimate, with as-of date) |
| fund_strategy | string |
| geography_focus | list[string] |
| sector_focus | list[string] |
| key_personnel | list[{name, title}] |
| investment_thesis | string (2-4 sentences) |
| citations | list[{claim_id, url}] |

If a field cannot be sourced, the skill returns `null` for that field rather than inventing a value, and notes the gap in a `gaps` array.

## Output format (hybrid)

Output is a markdown body (the prose fields above: fund_strategy, investment_thesis, etc, written as normal sections) followed by a trailing fenced JSON block titled `## Claims` containing every discrete factual claim from the body:

```json
[
  {
    "claim_id": "firm-profiler-001",
    "field": "aum",
    "text": "one-sentence statement of the claim",
    "confidence": null,
    "source_type": null,
    "citation": "url or filename, or null if uncited"
  }
]
```

`confidence` and `source_type` are left `null` here. They get filled in downstream by confidence-scorer and source-typer, not by firm-profiler itself. Every claim_id must be unique and stable, since dossier-assembler and audit-pass will reference these ids later.

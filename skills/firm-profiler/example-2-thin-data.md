# firm-profiler — Example 2 (thin public data)

## INPUT

```
firm_name: "Fernhollow Capital"
raw_sources:
  - type: linkedin_company_page
    text: >
      Fernhollow Capital | Private Equity | 11-50 employees | Austin, Texas
      area. Fernhollow partners with founder-owned dental and veterinary
      services businesses in the Southwest.
  - type: pr_newswire
    text: >
      Fernhollow Capital announced its investment in Briarwood Dental
      Partners, a multi-location dental service organization based in
      San Antonio.
  - type: sec_edgar_search
    result: "no Form ADV on file as of this search"
```

## OUTPUT

```markdown
### Firm Overview

Fernhollow Capital is a private equity firm based in the Austin, Texas area
investing in founder-owned dental and veterinary services businesses in the
Southwest [pub-doc][medium]. No Form ADV is on file, consistent with either
exempt reporting adviser status or a fund structure below public disclosure
thresholds, so firm-level AUM cannot be confirmed [pub-inf][low].

### Investment Criteria

Not available from any source reviewed. Per the dossier's structural
template in research-agent.md (referenced here only for how a missing
section is represented, not for source-handling or labeling judgment,
which are this pipeline's own eight skills' responsibility), a section
with no supporting source is not written into the dossier as if it had
content. It's noted as unavailable in place and raised with you outside
the document rather than left blank with no explanation.

### Investment Approach and Speciality

Not available from any source reviewed. Same handling as above.

### Leadership Relevant to QofAI

Not available from any source reviewed. Same handling as above.

**Note raised outside the dossier:** three of this firm's four firm-level
sections have no supporting source. We attempted to find leadership names,
stated investment criteria, and a value-creation approach through the
LinkedIn page, the press release, and an EDGAR search, and none of the
three contain this information. Recommend either sourcing a firm
presentation or deck directly, or publishing the dossier with only a firm
overview and a note that the remaining firm-level sections are pending.
```

## Claims

```json
[
  {
    "claim_id": "firm-profiler-fernhollow-001",
    "field": "firm_overview",
    "text": "Fernhollow Capital is a private equity firm based in the Austin, Texas area investing in founder-owned dental and veterinary services businesses in the Southwest.",
    "confidence": null,
    "source_type": null,
    "citation": "linkedin_company_page"
  },
  {
    "claim_id": "firm-profiler-fernhollow-002",
    "field": "aum",
    "text": "No Form ADV is on file, consistent with either exempt reporting adviser status or a fund structure below public disclosure thresholds, so firm-level AUM cannot be confirmed.",
    "confidence": null,
    "source_type": null,
    "citation": "reasoned from absence of a record in sec_edgar_search, not a direct statement in any source"
  }
]
```

`investment_criteria`, `investment_approach`, and `key_personnel` produced no claims, since no source reviewed contains this information. Per contract, these fields are returned `null` and the gap is noted in a `gaps` array rather than fabricated:

```json
{
  "gaps": ["investment_criteria", "investment_approach_and_speciality", "leadership_relevant_to_qofai"]
}
```

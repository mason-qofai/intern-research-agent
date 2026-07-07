# portfolio-discoverer — Example 2 (no published list, inferred)

## INPUT

```
firm_name: "Fernhollow Capital"
raw_sources:
  - type: press_release
    text: >
      Fernhollow Capital announced its investment in Briarwood Dental
      Partners, a multi-location dental service organization based in
      San Antonio.
  - type: linkedin_employee_search
    result: >
      One LinkedIn profile (former Fernhollow associate, now elsewhere)
      lists prior experience including "deal team, Ridgeline Veterinary
      Group investment."
  - type: sec_form_d_search
    result: >
      A Form D for "Ridgeline Vet Holdco LLC" filed 2023-09-12 lists a
      related person with the same name as a Fernhollow Capital principal.
```

## OUTPUT

```markdown
### Current Portfolio Companies: Fernhollow Capital

| Company | Sector | Entry Year |
|---|---|---|
| Briarwood Dental Partners | Dental services | 2024 |

Briarwood Dental Partners [pub-doc][high], confirmed directly by a press
release naming both the firm and the deal.

Ridgeline Veterinary Group is not included in the table above. The
supporting chain is a former employee's LinkedIn bio mentioning deal work
on "the Ridgeline Veterinary Group investment," paired with a Form D listing
a person with the same name as a current Fernhollow principal. Neither
source states a Fernhollow-Ridgeline relationship directly, and the hop
connecting the two, that a name match across two independent filings means
this is a Fernhollow holding, is not tied to a named piece of evidence
confirming the relationship itself, it's tied to a coincidence of names.
That's an untraceable hop under source-rubric.md. Flagged for your review
rather than published as a low confidence entry.

**Coverage caveat:** Fernhollow has no published portfolio page and limited
press coverage. This inventory is very likely incomplete beyond the one
confirmed entry [pub-inf][low].
```

## Claims

```json
[
  {
    "claim_id": "portfolio-discoverer-fernhollow-001",
    "field": "company_name",
    "text": "Briarwood Dental Partners is a current portfolio company, dental services, entry 2024.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "press_release"
  },
  {
    "claim_id": "portfolio-discoverer-fernhollow-002",
    "field": "company_name",
    "text": "Ridgeline Veterinary Group is a candidate portfolio company, based on a name match across a former employee's LinkedIn bio and a Form D filing.",
    "confidence": null,
    "source_type": null,
    "flagged": true,
    "flag_reason": "no source states a Fernhollow-Ridgeline relationship directly; the hop connecting the two filings is a coincidence of names, not a named piece of evidence confirming the relationship itself",
    "citation": null
  },
  {
    "claim_id": "portfolio-discoverer-fernhollow-003",
    "field": "coverage_caveat",
    "text": "Fernhollow has no published portfolio page and limited press coverage; this inventory is very likely incomplete beyond the one confirmed entry.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "reasoned from absence of a portfolio page and thin press coverage across all sources reviewed"
  }
]
```

Ridgeline is included here as a flagged candidate, not published in the table in the markdown body above, per the withheld-not-rated handling in the contract.

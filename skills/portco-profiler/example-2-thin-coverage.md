# portco-profiler — Example 2 (thinly covered portfolio company)

## INPUT

```
company_name: "Briarwood Dental Partners"
parent_firm: "Fernhollow Capital"
raw_sources:
  - type: acquisition_press_release
    text: >
      Fernhollow Capital announced its investment in Briarwood Dental
      Partners, a multi-location dental service organization based in
      San Antonio, Texas.
  - type: state_dental_board_registry
    result: >
      Four active practice locations registered under "Briarwood Dental
      Partners LLC" in Bexar and Comal counties, Texas.
  - type: company_website
    text: "Four locations serving San Antonio and New Braunfels."
```

## OUTPUT

```markdown
### Briarwood Dental Partners

Sector: dental service organization. Headquarters: San Antonio, Texas.
Entry: June 2024 (announcement date, not confirmed close date).

Briarwood Dental Partners operates in the San Antonio area
[pub-doc][high]. State dental board registry data confirms four active
practice locations across Bexar and Comal counties, matching the company
website's own count [pub-doc][high].

Founding date, employee count, and financial statistics are not available
from any source reviewed. This is not filled with an estimate here, private
data approximation for this company is a separate skill's output, not this
one's. We do not draw any conclusion about growth or momentum since the
2024 investment, there is no baseline and no follow-up source to compare
against.
```

## Claims

```json
[
  {
    "claim_id": "portco-profiler-briarwood-001",
    "field": "business_description",
    "text": "Briarwood Dental Partners operates in the San Antonio area, dental service organization.",
    "confidence": null,
    "source_type": null,
    "citation": "acquisition_press_release"
  },
  {
    "claim_id": "portco-profiler-briarwood-002",
    "field": "hq_location",
    "text": "State dental board registry confirms four active practice locations across Bexar and Comal counties, matching the company website's own count.",
    "confidence": null,
    "source_type": null,
    "citation": "state_dental_board_registry"
  }
]
```

`employee_count_estimate`, founding date, and financial statistics produced no claims, no source reviewed contains this information. These fields are returned `null`, and no growth or momentum conclusion is drawn since there is no baseline or follow-up source to compare against. Financial estimation, if attempted, belongs to private-data-approximator, not this skill.

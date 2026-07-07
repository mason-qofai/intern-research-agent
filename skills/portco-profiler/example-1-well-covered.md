# portco-profiler — Example 1 (well-covered portfolio company)

Scope note: this is why the dossier separates the inventory from the
overview, leadership scans the short list first, then reads this level of
detail for whichever company looks like an opportunity.

## INPUT

```
company_name: "Anchor Point Logistics"
parent_firm: "Cobalt Bridge Partners"
raw_sources:
  - type: acquisition_press_release
    text: >
      Cobalt Bridge Partners announced a majority investment in Anchor
      Point Logistics, a provider of temperature-controlled freight and
      warehousing services for healthcare and pharmaceutical clients,
      headquartered in Nashville, Tennessee. Anchor Point operates 14
      facilities across the Southeast.
  - type: company_website
    text: "Founded in 2009. Currently operating 16 facilities."
  - type: trade_press_article
    text: >
      Anchor Point Logistics has grown its facility count from 14 to 16
      since its 2021 recapitalization and added a Texas distribution hub
      in late 2024.
```

## OUTPUT

```markdown
### Anchor Point Logistics

Sector: healthcare logistics. Headquarters: Nashville, Tennessee. Entry:
April 2021, majority investment.

Anchor Point Logistics provides temperature-controlled freight and
warehousing for pharmaceutical distributors, hospital systems, and
specialty pharmacies [pub-doc][high]. The company was founded in 2009
[pub-doc][high]. At the time of Cobalt Bridge's investment, Anchor Point
operated 14 facilities. A January 2025 trade press article puts that count
at 16, including a new Texas distribution hub added in late 2024
[pub-doc][high].

The facility growth, 14 to 16 over roughly three and a half years, is a
physical footprint indicator, not a financial performance measure. We treat
it as a proxy for organic expansion but do not equate it with revenue growth
[pub-inf][medium].
```

## Claims

```json
[
  {
    "claim_id": "portco-profiler-anchorpoint-001",
    "field": "business_description",
    "text": "Anchor Point Logistics provides temperature-controlled freight and warehousing for pharmaceutical distributors, hospital systems, and specialty pharmacies, HQ Nashville, Tennessee.",
    "confidence": null,
    "source_type": null,
    "citation": "acquisition_press_release"
  },
  {
    "claim_id": "portco-profiler-anchorpoint-002",
    "field": "notable_events",
    "text": "Founded in 2009.",
    "confidence": null,
    "source_type": null,
    "citation": "company_website"
  },
  {
    "claim_id": "portco-profiler-anchorpoint-003",
    "field": "notable_events",
    "text": "Operated 14 facilities at the time of Cobalt Bridge's 2021 investment; a January 2025 trade press article puts the count at 16, including a Texas distribution hub added late 2024.",
    "confidence": null,
    "source_type": null,
    "citation": "trade_press_article"
  },
  {
    "claim_id": "portco-profiler-anchorpoint-004",
    "field": "notable_events",
    "text": "Facility growth from 14 to 16 over roughly three and a half years is a physical footprint indicator, not a financial performance measure, and should not be equated with revenue growth.",
    "confidence": null,
    "source_type": null,
    "citation": "reasoned from company_website and trade_press_article, not a direct statement in either"
  }
]
```

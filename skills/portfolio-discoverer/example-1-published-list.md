# portfolio-discoverer — Example 1 (published portfolio page)

Scope note: this skill outputs an exhaustive named inventory of current,
unrealized holdings only, organized by sector, no fund grouping. Any
realized or exited holding is discarded at discovery, it never reaches
output, not even labeled as exited. QofAI's business is with current
portfolio companies, exited ones carry no relevance.

## INPUT

```
firm_name: "Cobalt Bridge Partners"
raw_sources:
  - type: firm_website_portfolio_page
    text: >
      Current Portfolio: Anchor Point Logistics (2021, healthcare
      logistics), Redline Industrial Coatings (2022, industrials), Summit
      Behavioral Health (2023, healthcare services).
      Prior Investments (Realized): Vantage Metal Works (2016-2023, sold to
      strategic acquirer), Prairie Diagnostics (2014-2019, sold).
```

## OUTPUT

```markdown
### Current Portfolio Companies: Cobalt Bridge Partners

| Company | Sector | Entry Year |
|---|---|---|
| Anchor Point Logistics | Healthcare logistics | 2021 |
| Redline Industrial Coatings | Industrials | 2022 |
| Summit Behavioral Health | Healthcare services | 2023 |

All three entries [pub-doc][high], sourced directly from the firm's
portfolio page.

Vantage Metal Works and Prairie Diagnostics appeared on the same source page
under "Prior Investments (Realized)" and are excluded from this inventory
entirely. They are not current holdings and have no bearing on QofAI's
opportunity with this firm.

**Coverage caveat:** a published portfolio page typically excludes deals a
firm chose not to publicize. Treat this list as a floor on current holdings,
not a ceiling [pub-inf][medium].
```

## Claims

```json
[
  {
    "claim_id": "portfolio-discoverer-cobalt-001",
    "field": "company_name",
    "text": "Anchor Point Logistics is a current portfolio company, healthcare logistics, acquired 2021.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "firm_website_portfolio_page"
  },
  {
    "claim_id": "portfolio-discoverer-cobalt-002",
    "field": "company_name",
    "text": "Redline Industrial Coatings is a current portfolio company, industrials, acquired 2022.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "firm_website_portfolio_page"
  },
  {
    "claim_id": "portfolio-discoverer-cobalt-003",
    "field": "company_name",
    "text": "Summit Behavioral Health is a current portfolio company, healthcare services, acquired 2023.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "firm_website_portfolio_page"
  },
  {
    "claim_id": "portfolio-discoverer-cobalt-004",
    "field": "coverage_caveat",
    "text": "A published portfolio page typically excludes deals a firm chose not to publicize; treat this list as a floor on current holdings, not a ceiling.",
    "confidence": null,
    "source_type": null,
    "flagged": false,
    "citation": "reasoned from the general pattern of firm-published portfolio pages, not a specific source"
  }
]
```

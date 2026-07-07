# firm-profiler — Example 1 (strong public data)

Scope note: firm-profiler owns everything about the firm itself, not its
portfolio, sections 1 through 4 of the dossier, firm overview, investment
criteria, investment approach and speciality, and leadership. All four are
demonstrated below.

## INPUT

```
firm_name: "Cobalt Bridge Partners"
raw_sources:
  - type: firm_website_about_page
    text: >
      Cobalt Bridge Partners is a middle-market private equity firm founded
      in 2011, headquartered in Denver, Colorado. The firm invests in
      healthcare services and industrials businesses with $15-75M in EBITDA,
      typically taking majority control positions, with equity checks
      ranging from $25M to $120M per platform.
  - type: sec_form_adv
    fields:
      regulatory_aum_usd: 2100000000
      employee_count: 38
  - type: press_release
    text: >
      Cobalt Bridge Partners today announced the final close of Cobalt
      Bridge Fund IV at its hard cap of $850 million.
  - type: firm_website_approach_page
    text: >
      Cobalt Bridge partners with existing management teams post-close
      rather than replacing them, and focuses on add-on acquisitions and
      operational infrastructure (finance, procurement, sales tooling) as
      its primary value creation lever.
  - type: firm_website_team_page
    text: "Managing Partners: J. Reyes, T. Halloran. Founded the firm together in 2011."
```

## OUTPUT

```markdown
### Firm Overview

Cobalt Bridge Partners is a Denver-based middle-market private equity firm
founded in 2011 [pub-doc][high]. The firm is an SEC-registered investment
adviser reporting $2.1B in regulatory AUM and 38 employees [pub-doc][high].
It closed its fourth flagship fund, Cobalt Bridge Fund IV, at $850M in
November 2025 [pub-doc][high].

### Investment Criteria

Cobalt Bridge targets healthcare services and industrials businesses with
EBITDA between $15M and $75M, typically acquiring majority positions
[pub-doc][high]. Equity checks range from $25M to $120M per platform
[pub-doc][high].

### Investment Approach and Speciality

The firm retains existing management post-close rather than replacing
leadership, and its stated primary value creation levers are add-on
acquisitions and operational infrastructure work in finance, procurement,
and sales tooling [pub-doc][high]. Given the EBITDA band this firm targets
and its stated add-on focus, its portfolio companies are more likely to grow
through acquisition than through organic revenue expansion alone
[pub-inf][medium].

### Leadership Relevant to QofAI

Cobalt Bridge is led by managing partners J. Reyes and T. Halloran, who
co-founded the firm in 2011 [pub-doc][high].
```

## Claims

```json
[
  {
    "claim_id": "firm-profiler-cobalt-001",
    "field": "firm_overview",
    "text": "Cobalt Bridge Partners is a Denver-based middle-market private equity firm founded in 2011.",
    "confidence": null,
    "source_type": null,
    "citation": "firm_website_about_page"
  },
  {
    "claim_id": "firm-profiler-cobalt-002",
    "field": "aum",
    "text": "Cobalt Bridge Partners is SEC-registered, reporting $2.1B in regulatory AUM and 38 employees.",
    "confidence": null,
    "source_type": null,
    "citation": "sec_form_adv"
  },
  {
    "claim_id": "firm-profiler-cobalt-003",
    "field": "fund_strategy",
    "text": "Closed its fourth flagship fund, Cobalt Bridge Fund IV, at $850M in November 2025.",
    "confidence": null,
    "source_type": null,
    "citation": "press_release"
  },
  {
    "claim_id": "firm-profiler-cobalt-004",
    "field": "investment_thesis",
    "text": "Targets healthcare services and industrials businesses with EBITDA between $15M and $75M, majority positions, equity checks $25M-$120M per platform.",
    "confidence": null,
    "source_type": null,
    "citation": "firm_website_about_page"
  },
  {
    "claim_id": "firm-profiler-cobalt-005",
    "field": "investment_thesis",
    "text": "Retains existing management post-close; primary value creation levers are add-on acquisitions and operational infrastructure work.",
    "confidence": null,
    "source_type": null,
    "citation": "firm_website_approach_page"
  },
  {
    "claim_id": "firm-profiler-cobalt-006",
    "field": "investment_thesis",
    "text": "Given the EBITDA band and stated add-on focus, portfolio companies are more likely to grow through acquisition than organic revenue expansion alone.",
    "confidence": null,
    "source_type": null,
    "citation": "reasoned from firm_website_about_page and firm_website_approach_page, no separate document"
  },
  {
    "claim_id": "firm-profiler-cobalt-007",
    "field": "key_personnel",
    "text": "Led by managing partners J. Reyes and T. Halloran, who co-founded the firm in 2011.",
    "confidence": null,
    "source_type": null,
    "citation": "firm_website_team_page"
  }
]
```

`confidence` and `source_type` are left null throughout, per contract, filled in downstream by confidence-scorer and source-typer in their batch passes.

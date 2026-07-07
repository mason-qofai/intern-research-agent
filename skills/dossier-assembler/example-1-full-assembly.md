# dossier-assembler — Example 1 (full assembly, strong data)

Scope note: this skill inserts upstream output verbatim into the seven
fixed sections and adds no analysis of its own. Section 7 is left as a
placeholder heading only, audit-pass fills it in a separate pass after
assembly, it is not this skill's job.

## INPUT

```
sections:
  firm_level: "<firm-profiler example 1 output, covers sections 1-4>"
  current_portfolio: "<portfolio-discoverer example 1 output>"
  portco_overviews:
    - "<portco-profiler example 1 output, Anchor Point Logistics>"
  financial_approximations:
    - "<private-data-approximator example 1 output, Anchor Point Logistics>"
```

## OUTPUT

```markdown
# Dossier: Cobalt Bridge Partners

## 1. Firm Overview
[firm-profiler output, firm overview subsection, inserted verbatim]

## 2. Investment Criteria
[firm-profiler output, investment criteria subsection, inserted verbatim]

## 3. Investment Approach and Speciality
[firm-profiler output, approach subsection, inserted verbatim]

## 4. Leadership Relevant to QofAI
[firm-profiler output, leadership subsection, inserted verbatim]

## 5. Current Portfolio Companies
[portfolio-discoverer output, inserted verbatim, including its coverage
caveat]

## 6. Individual Portfolio Company Overviews

### Anchor Point Logistics
[portco-profiler output, inserted verbatim]

#### Financial Approximation
[private-data-approximator output, inserted verbatim]

*Coverage note: this dossier currently profiles 1 of 3 known current
holdings. Redline Industrial Coatings and Summit Behavioral Health
overviews are pending.*

## 7. Review of Flagged and Satisfactory Content and Claims

*Pending audit-pass.*
```

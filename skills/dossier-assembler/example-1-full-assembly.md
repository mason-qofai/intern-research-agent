# dossier-assembler — Example 1 (full assembly, strong data)

Scope note: this skill inserts upstream output verbatim into the fixed
sections and adds no analysis of its own, with one deliberate exception:
Section 1 ends with a required Strategy Synthesis subsection, which
compares the firm's stated thesis (from firm-profiler) against the actual
composition of its portfolio (from portfolio-discoverer and
portco-profiler) and states an observation neither source asserts on its
own. Everything else in this skill is verbatim insertion; this one
subsection is the exception, and it's a real claim with its own confidence
band and source_type, not a bonus remark.

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

### Strategy Synthesis

Cobalt Bridge's own materials describe its primary value-creation levers
as add-on acquisitions and operational infrastructure work rather than
organic growth (firm-profiler-005). The one portfolio company profiled so
far, Anchor Point Logistics, shows facility count growing from 14 to 16
between the 2021 investment and a January 2025 trade press mention, a
footprint-expansion pattern consistent with that stated playbook rather
than, say, a pattern of entering new end markets or launching new service
lines. With only 1 of 3 known holdings profiled, this is a single
consistent data point, not a confirmed pattern across the portfolio, but
it is at least directionally aligned with the firm's own stated thesis
rather than contradicting it. *(synthesis-001, Medium, public inference:
derived from comparing firm-profiler's stated value-creation levers
against portco-profiler's observed facility-count change for the one
company profiled to date; neither source states this alignment directly,
and the observation should be revisited once Redline Industrial Coatings
and Summit Behavioral Health are also profiled.)*

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

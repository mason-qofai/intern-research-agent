# dossier-assembler — Example 2 (assembly with missing subsections)

## INPUT

```
sections:
  firm_level: "<firm-profiler example 2 output, Fernhollow Capital, three
    of four firm-level subsections unavailable>"
  current_portfolio: "<portfolio-discoverer example 2 output>"
  portco_overviews:
    - "<portco-profiler example 2 output, Briarwood Dental Partners>"
  financial_approximations:
    - "<private-data-approximator example 2 output, flagged, not published>"
```

## OUTPUT

```markdown
# Dossier: Fernhollow Capital

## 1. Firm Overview
[firm-profiler output, firm overview subsection, inserted verbatim]

### Strategy Synthesis

*Not attempted. Firm-profiler found no investment criteria, approach, or
leadership content for Fernhollow Capital, only a firm overview and an
AUM-disclosure gap. Synthesis requires comparing a stated strategy against
observed portfolio composition; with no stated strategy content on the
firm side, and only one confirmed portfolio company (Briarwood Dental
Partners) on the other side, there is nothing to compare. Forcing an
observation here would mean either inventing a strategy Fernhollow never
stated, or treating one company as a representative pattern, neither is
defensible. This subsection is intentionally left unattempted rather than
filled with a thin or unsupported claim, the same discipline
private-data-approximator applies when it withholds an estimate rather
than forcing a number.*

## 2. Investment Criteria
*Not available. Firm-profiler could not find supporting sources. Noted
here per the dossier's structural template in research-agent.md, which
this skill follows only for how a missing section is represented, not for
source-handling or labeling judgment. Raised outside this document.*

## 3. Investment Approach and Speciality
*Not available. Same handling as above.*

## 4. Leadership Relevant to QofAI
*Not available. Same handling as above.*

## 5. Current Portfolio Companies
[portfolio-discoverer output, inserted verbatim, including the flagged
Ridgeline Veterinary Group entry left out of the table and the coverage
caveat]

## 6. Individual Portfolio Company Overviews

### Briarwood Dental Partners
[portco-profiler output, inserted verbatim]

#### Financial Approximation
*Not available. Private-data-approximator flagged its comps chain as
untraceable rather than publishing an estimate. Raised outside this
document, not resolved as of this assembly.*

## 7. Review of Flagged and Satisfactory Content and Claims

*Pending audit-pass.*
```

## Notes for skill design

Four different kinds of gap appear here and the assembler represents each
one plainly rather than smoothing them into a single "data unavailable"
note: a subsection with no source found, a portfolio entry withheld
pending human review, a financial approximation withheld for the same
reason, and a synthesis subsection left unattempted because there isn't
enough data on either side of the comparison to support a real
observation. That fourth case matters as much as the other three: a forced
or generic synthesis claim would score worse under audit than an honest
"not attempted," the same logic that governs withheld financial estimates
applies here too. Section 7 stays a placeholder regardless of how thin the
rest of the dossier is, audit-pass's pass happens once, after assembly,
not per section.

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

Three different kinds of gap appear here and the assembler represents each
one plainly rather than smoothing them into a single "data unavailable"
note, a subsection with no source found, a portfolio entry withheld pending
human review, and a financial approximation withheld for the same reason.
Section 7 stays a placeholder regardless of how thin the rest of the
dossier is, audit-pass's pass happens once, after assembly, not per section.

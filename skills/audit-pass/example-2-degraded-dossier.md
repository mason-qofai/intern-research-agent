# audit-pass — Example 2 (degraded draft, section 7 output)

Scope note: this is a deliberately degraded draft, edited to introduce
mistakes an earlier compilation step should have caught, so the pattern is
visible in one place.

## INPUT

```
draft_excerpt: >
  ### Current Portfolio Companies

  Fernhollow Capital's portfolio includes Briarwood Dental Partners and
  Ridgeline Veterinary Group. [pub-doc][high]

  #### Financial Approximation: Briarwood Dental Partners

  Briarwood Dental Partners generates approximately $8M in annual revenue.
  [pub-inf][medium]
```

## OUTPUT

```markdown
[Sections 1-6 of the draft, passed through unchanged except where noted
in section 7 below, omitted here for brevity]

## 7. Review of Flagged and Satisfactory Content and Claims

Two issues found in this draft that should not have reached this stage.

Ridgeline Veterinary Group is tagged [pub-doc][high] in the current
portfolio companies section. Portfolio-discoverer's own working notes show
this entry as a name-match across a LinkedIn bio and a Form D filing, with
no source confirming the Fernhollow relationship directly, an untraceable
hop that should have been flagged and withheld, not published at high
confidence. This entry does not belong in the dossier until a human
resolves it. Per contract, audit-pass does not edit section 5 to remove it;
that correction is raised here in section 7, section 5 is left as received.

The Briarwood Dental Partners revenue figure, $8M, [pub-inf][medium], has
no comp set, no named method, and no citation behind it anywhere in this
draft. Private-data-approximator's own work on this company concluded the
one available comp was too different in scale to support any estimate and
withheld the figure rather than publishing a number. This figure appears to
have replaced that withheld result with an unsupported one. This should
read as unavailable, flagged, pending human review, not as a rated
estimate. Same handling: raised here, not edited in place in section 6.

Nothing else in this excerpt is flagged. The portfolio-discoverer coverage
caveat and the portco-profiler content for Briarwood, where reviewed
separately, are consistent with their underlying sources.
```

The output is the complete dossier, sections 1-6 unchanged (including the
two problems described above, which audit-pass flags but does not correct)
plus section 7 filled in as shown.

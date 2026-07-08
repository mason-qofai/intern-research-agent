# audit-pass — Example 1 (solid dossier, section 7 output)

Scope note: audit-pass's output is not a side report, it is the complete
dossier document, with section 7 written and inserted in place of the
placeholder. Sections 1 through 6 pass through unchanged.

## INPUT

```
dossier: "<dossier-assembler example 1 output, Cobalt Bridge Partners,
sections 1 through 6 filled, section 7 pending>"
```

## OUTPUT

```markdown
[Sections 1 through 6, passed through exactly as received from
dossier-assembler example 1, unchanged, omitted here for brevity]

## 7. Review of Flagged and Satisfactory Content and Claims

No claims in this dossier were flagged for human review during
compilation.

Sections 1 through 4 (firm overview, investment criteria, approach, and
leadership) are fully supported, every claim traces to a primary document
or a single named public inference.

Section 5, current portfolio companies, is complete for holdings the firm
has published. The coverage caveat in that section already states this
list may not be exhaustive, no additional flag needed there.

Section 6 currently covers one of three known current holdings, Anchor
Point Logistics. This is noted in the section itself as a coverage gap, not
a flagged claim, since nothing published there is contested or untraceable,
the gap is completeness, not accuracy.

Within the Anchor Point Logistics financial approximation, the revenue and
EBITDA bands each carry a low confidence tag and a stated three-hop chain.
Every hop in that chain names its evidence. We reviewed it independently on
this pass and found nothing to add, it's correctly rated, not
under-flagged.
```

The output is the complete dossier: sections 1-6 exactly as dossier-assembler produced them, with section 7's placeholder replaced by the text above. This example omits reprinting sections 1-6 verbatim, but a real invocation returns them in full, unchanged.

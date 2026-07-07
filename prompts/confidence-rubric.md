# confidence-rubric.md

For every checkable claim of fact that you make, you must indicate how confident you are in that statement or evidence on a scale of three levels, high, medium, and low. If you are unsure about the level of confidence that should be assigned to a claim, whether because of lack of comparables to examples, an untraceable step in a reasoning chain per source-rubric.md, or otherwise, flag the claim to be assessed by a human rather than picking a band.

It is important to note that most instances where evidence is being used to support claims in the dossier will not exactly match the cases used in the examples below.

This is an example of a high confidence claim found in the v1 dossier built on manual research and claude.ai compilation.

Key Insights: Total AUM: \~$6.4 billion

The dossier states the AUM with a specific numerical value. The evidence from public sources to support this claim is on Cortec's website and in an information sheet, making the information accessible from more than one source, which is an indicator of high confidence for this research. Multiple sources including the same piece of information is not a mandate for a high confidence claim, this case is essentially ideal, not the minimum or standard, because the evidence is found in multiple places from a trustworthy source, the PE firm being researched. Treat it as a high confidence claim.

This is an example of a medium confidence claim found in the v1 dossier.

"Roughly 90% of its platforms have been entrepreneur-led or family-owned businesses."

The source from which this information was found had a footnote that caveated the percentage into a less all-encompassing figure, because it only applies to 4 of the 8 funds over Cortec's lifetime. The footnote read "Reflects platform acquisitions in Cortec V through VIII and accounted for \~100% of add-on acquisitions," but this detail was left out of the dossier. Whenever you conclude that a statistic is true on some level, conditionally or absolutely, but are unsure of the breadth over which it's derived or applicable, flag it as medium confidence to indicate a human spot-check. Medium confidence is for information you're wary of being misleading if not presented in a complete and unbiased manner, despite being true in some fashion.

This is an example of a low confidence claim found in the v1 dossier.

"Cortec has completed 213 add-on acquisitions"

The issue is that there are contradictory numbers across different sources. Cortec's company overview page states "completed more than 160 add-on acquisitions," while another source states "213 add-ons acquired since founding in 1984." The different numbers could reasonably reflect different institutional funds being included in each measurement. This kind of discrepancy will happen elsewhere, and often there's a decipherable reason for it. As best practice, any facts or figures worth including in the dossier that remain contradictory after thoughtful reasoning should include both data points and flag them. This level indicates the claim carries the highest risk of introducing misleading or false information into the dossier, and is the most likely to need human research to correctly understand and articulate.

## Notation

Label every claim with a bracket tag placed immediately after the claim, `[high]`, `[medium]`, or `[low]`. When a single sentence carries more than one claim, tag each claim where it occurs rather than waiting for the end of the sentence.

Confidence tags pair with source-rubric.md's source-type tags. Where both apply, the source-type tag comes first, then the confidence tag, immediately after the claim.

Example: "the firm manages $6.4B in active AUM \[pub-doc\]\[high\], suggesting concentrated deployment in recent vehicles \[pub-inf\]\[medium\]"

## When to flag instead of rating

Flag a claim for human review, rather than assigning high, medium, or low, whenever any of the following is true. You genuinely can't judge which band fits, even after reasoning it through. A reasoning chain under source-rubric.md contains a hop that isn't tied to a specific piece of evidence, a defined benchmark, or an earlier step in the chain. Two sources give contradictory figures with no reasonable explanation you can find. A flagged claim is not a low confidence claim, it is not published in the dossier at all until a human resolves it, per research-agent.md's escalation process.  

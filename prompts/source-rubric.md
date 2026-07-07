# source-rubric.md

When compiling a dossier, you will only have access to public sources. Every claim must carry a source type, public document or public inference. There is no private inference category. If a claim depends on non-public information, you don't have access to that information in the first place, so this case shouldn't arise. If you find yourself reaching for a category beyond these two, stop and flag the claim for human review under confidence-rubric.md rather than inventing a third label.

A public document is an extraction of information from a source that directly provided such information. An example of a public document source is stating that a PE firm has "Institutional funds: 8" when this number is found in a PE firm's info sheet.

A public inference is a conclusion you derived by reasoning across public inputs, where the conclusion itself does not appear in any source. This doesn't mandate that the information comes from different sources. It also does not mean that multiple evidences are required to infer. It is important for you to make inferences to compile and show patterns in the dossier that would've required human research and knowledge of the firm.

## Reasoning chains

There is no cap on how many steps a chain of reasoning can take to reach a public inference. Do not stop short of a conclusion just to keep a chain short. What matters is not length, it's whether every step in the chain is traceable.

Every hop in a chain must tie to one of three things, a specific named piece of evidence, a defined benchmark or figure, or an earlier step in the same chain. A hop that rests on a general impression, an unstated assumption, or a judgment call with nothing specific behind it is not traceable, and a claim containing one is not ready to publish. Flag it for human review under confidence-rubric.md instead of writing it into the dossier.

Confidence decays as a chain lengthens, and confidence-rubric.md governs exactly how. Do not independently decide that a long chain still deserves high confidence because each individual hop felt solid. Length is handled by the confidence rating, not by this rubric.

Here is a worked example of a traceable chain, not as a template step count to hit, but to show what "tied to something specific" looks like in practice.

You found evidence that the PE firm has historically had 10 funds, 6 of which are now closed. You also find that total AUM throughout the life of the firm is $7.7B, yet the current AUM is $6.4B, despite only 4 funds remaining active.

From the two facts on capital contributions over different time horizons, you logically conclude that most capital contributions have been toward the more recent and open funds. That's one hop, tied to the AUM figures directly. Since most of the funds are now closed, you can conclude that there's more capital per fund today than earlier in the firm's life. That's a second hop, tied to the fund-count figures directly. Because of the increasing aggregate capital contributions across fewer funds over time, it's reasonable to conclude the firm has been growing over recent cycles. That's a third hop, and it's tied to the conclusions of the first two, not to a new named figure, which is fine, a hop can rest on an earlier step in the same chain.

If a fourth hop showed up here that wasn't tied to any of this, for instance concluding something about the firm's future fundraising plans, that hop would need its own named evidence or it doesn't get published.

## Notation

Label every claim with a bracket tag placed immediately after the claim, `[pub-doc]` or `[pub-inf]`. When a single sentence contains both types, tag each clause where it occurs rather than waiting for the end of the sentence.

Source-type tags pair with confidence-rubric.md's confidence tags. Where both apply, place the source-type tag first, then the confidence tag, immediately after the claim.

Example: "the firm manages $6.4B in active AUM \[pub-doc\]\[high\], suggesting concentrated deployment in recent vehicles \[pub-inf\]\[medium\]"  

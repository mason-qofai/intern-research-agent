name: audit-pass
description: after the dossier is completely assembled, read the dossier and produce and audit report that flags inaccuracies or question claims/reasoning steps.

--

# audit-pass: Input/Output Contract

## Input contract

| Field | Type | Required | Source |
|---|---|---|---|
| dossier_markdown | string, sections 1 through 6 complete, section 7 present as a placeholder heading with body "*Pending audit-pass.*" | yes | dossier-assembler output |

## Output contract

Output is the complete dossier document, sections 1 through 6 passed through unchanged, with section 7's placeholder replaced by the literal markdown content of "## 7. Review of Flagged and Satisfactory Content and Claims." This is not a side report, it is the final dossier.

| Field | Type |
|---|---|
| full_dossier_markdown | string, the complete document, sections 1-6 unchanged plus section 7 filled in |
| flagged_claims | list[{claim_id, issue, severity}] (tracked internally, referenced in section 7's prose, not output as a separate artifact) |
| missing_tags | list[claim_id] (claims lacking confidence or source_type) |
| metric_conflation_flags | list[{location, description}] (engagement vs opportunity metrics mixed) |
| suggested_fixes | list[{claim_id, suggested_revision}] |

audit-pass does not silently fix the dossier body (sections 1 through 6), it passes that content through exactly as received. It writes section 7 describing what it found: claims that are fully supported, claims flagged for human review, and coverage gaps already noted elsewhere in the dossier that don't need re-flagging. A human resolves anything flagged; audit-pass does not resolve it itself, and does not edit sections 1-6 to fix what it flags.

## Output format (hybrid) — note the exception

Like dossier-assembler, audit-pass is a terminal step whose output is the human-facing document itself, not an intermediate stage another skill parses. Output is pure markdown: the full dossier, unchanged sections 1-6 plus section 7's real content in place of the placeholder. No trailing JSON block. The four structured fields above (flagged_claims, missing_tags, metric_conflation_flags, suggested_fixes) inform what audit-pass writes in section 7's prose, but are not emitted as a separate machine-readable artifact. This is also the very last step in the pipeline: nothing runs after audit-pass, so nothing downstream needs these fields in structured form.

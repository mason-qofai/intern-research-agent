# API Confidence Scorer Evaluation Results

**Model:** Claude Opus 4.6
**Date:** July 13, 2026
**Test Set:** 44 valid predictions (50 total claims, 6 errors)
**Source:** Mixture of v1 manual dossier (25 claims) and v4 orchestrated dossier (25 claims)

---

## Overall Performance

| Metric | Value |
|--------|-------|
| Total Predictions | 44 |
| Correct Predictions | 22 |
| Accuracy | 50.0% |

---

## Confusion Matrix

Rows represent expected confidence, columns represent predicted confidence.

```
         High        Low     Medium
High      11          1         10
Low        6          5          3
Medium     1          1          6
```

### Matrix Breakdown

Expected HIGH (22 claims):
- Correctly predicted HIGH: 11 (50%)
- Mispredicted as MEDIUM: 10 (45%)
- Mispredicted as LOW: 1 (5%)

Expected LOW (14 claims):
- Correctly predicted LOW: 5 (36%)
- Mispredicted as HIGH: 6 (43%)
- Mispredicted as MEDIUM: 3 (21%)

Expected MEDIUM (8 claims):
- Correctly predicted MEDIUM: 6 (75%)
- Mispredicted as HIGH: 1 (13%)
- Mispredicted as LOW: 1 (13%)

---

## Per-Class Metrics

### HIGH Confidence
- Precision: 61.1% (11 true positives / 18 predicted high)
- Recall: 50.0% (11 true positives / 22 expected high)
- F1 Score: 55.0%

**Interpretation:** When the model predicts HIGH, it is correct 61% of the time, but it only catches 50% of claims that should be labeled HIGH. The model is conservative on HIGH confidence.

### LOW Confidence
- Precision: 71.4% (5 true positives / 7 predicted low)
- Recall: 35.7% (5 true positives / 14 expected low)
- F1 Score: 47.6%

**Interpretation:** The model has high precision on LOW (71%), meaning when it predicts LOW, it is usually right. But recall is weak at 36%, so it misses most claims that should be LOW. The model underpredicts LOW confidence.

### MEDIUM Confidence
- Precision: 31.6% (6 true positives / 19 predicted medium)
- Recall: 75.0% (6 true positives / 8 expected medium)
- F1 Score: 44.4%

**Interpretation:** The model catches 75% of MEDIUM claims but makes many false positive MEDIUM predictions (precision only 31%). The model is aggressive on MEDIUM, using it as a fallback for uncertain cases.

---

## Key Findings

1. **Overall accuracy is 50%** — equivalent to random chance among three classes. This suggests the model struggles with the confidence classification task as defined.

2. **HIGH-confidence claims are undersupported.** The model predicts HIGH only 50% of the time when expected. The largest error is confusing HIGH with MEDIUM (10 out of 22 misses), suggesting the model is uncertain about genuinely verifiable claims.

3. **LOW-confidence claims are severely underpredicted.** The model only catches 36% of LOW-confidence claims. Instead, it often predicts HIGH (6 cases) or MEDIUM (3 cases), misclassifying qualitative or unsupported claims as having more evidentiary support than warranted.

4. **MEDIUM is overused.** The model predicts MEDIUM 19 times but only 6 are correct (31% precision). This suggests MEDIUM serves as a catch-all for borderline cases and the confidence bands may be conflated in the model's reasoning.

5. **Systematic bias toward the center.** The model shows a tendency to predict MEDIUM more than either extreme, which suggests it defaults to caution when uncertain rather than committing to HIGH or LOW.

---

## Error Analysis: Notable Misclassifications

### False HIGH (should be LOW or MEDIUM)

- **v1_claim_003** (expected LOW, predicted HIGH): "Cortec Group is a New York–based private equity firm that positions itself as distinct from most peers..." — Model treated self-positioning as verifiable fact.
- **v1_claim_010** (expected LOW, predicted HIGH): "Based in Phoenix, AZ, A1 Garage is a leading provider..." — Model interpreted "leading provider" as high-confidence despite this being marketing language.

### False LOW (should be HIGH)

- **v4_claim_001** (expected HIGH, predicted MEDIUM): "Since its founding, Palladium has acquired more than 230–240 businesses..." — Model downgraded specific figures due to the range notation (230–240).
- **v4_claim_013** (expected LOW, predicted HIGH): "Bodewell Group is a strategic communications firm..." — Model treated business description as verifiable, missing the LOW label's intent (assessing qualitative positioning).

### False MEDIUM (should be HIGH or LOW)

- **v1_claim_014** (expected HIGH, predicted MEDIUM): "Equity per platform: Up to $500 million..." — Model treated "up to" language as introducing uncertainty, missing that this is firm's stated policy.

---

## Implications

The API scorer achieves 50% accuracy, which is no better than random classification. The confidence bands — as currently defined in the system prompt — are not well-learned by the model. Key issues:

1. The model conflates verifiable self-description (HIGH) with qualitative positioning (LOW).
2. The model is overly cautious, defaulting to MEDIUM for uncertain cases.
3. The precision/recall tradeoff differs sharply by class (HIGH precision-leaning, LOW recall-leaning, MEDIUM balanced poorly).

A production-ready scorer would require either:
- Refinement of the confidence definitions to be more explicit and learnable
- Few-shot examples in the system prompt to anchor classifications
- Retraining or fine-tuning on a larger labeled dataset
- Post-processing rules to enforce class priors or adjust decision boundaries

---

## Recommendation

**Do not deploy the API version to production at current accuracy (50%).** See capstone memo for full cost/latency/reliability analysis and conditional deployment criteria.

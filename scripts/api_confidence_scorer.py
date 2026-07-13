#!/usr/bin/env python3
"""
Confidence scorer using Anthropic API with text parsing.
Classifies claims as high, medium, or low confidence.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import anthropic


def load_eval_set(eval_path: str) -> list[dict]:
    """Load evaluation set from JSON file."""
    with open(eval_path, "r") as f:
        data = json.load(f)
    return data.get("test_cases", [])


def score_claim(client: anthropic.Anthropic, claim: str) -> dict:
    """
    Score a single claim using Claude API.
    Returns dict with prediction, reasoning, and raw response.
    """
    system_prompt = """You are an expert evaluator of private equity research claims. 
Your task is to classify each claim's verifiability and evidentiary strength.

Confidence bands are defined as:

HIGH: The claim is a specific, verifiable fact supported by primary sources (press releases, SEC filings, regulatory documents, company website materials, investor reports). This includes precise financial figures (AUM, fund closes, acquisition counts) disclosed by the firm, named individuals in roles, documented transactions, and factual statements about company origins or operations that appear in authoritative sources.

MEDIUM: The claim is partially supported by sources but carries material interpretation or inference. This includes estimates derived from public data but not independently verified, statements about firm strategy or philosophy that appear in materials but carry interpretation, claims mixing verifiable facts with broader assertions, or claims based on limited public evidence (e.g., "approximately X portfolio companies" based on partial data). Also includes directional metrics explicitly labeled as estimates or inferred ranges.

LOW: The claim is largely qualitative, subjective, or unsupported. This includes assertions about firm culture, management approach, or value-add philosophy with no specific evidence; claims requiring inference from limited data; broad positioning statements; claims about private business practices not visible in public materials; or claims where the evidence shown is insufficient to confirm the assertion (e.g., "management teams leverage Cortec to address challenges" with no concrete examples).

Respond with ONLY the following format:
CONFIDENCE: [high/medium/low]
REASONING: [brief explanation]"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=256,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Classify the confidence level for this claim:\n\n{claim}",
            }
        ],
    )

    response_text = message.content[0].text
    
    # Parse the response to extract confidence
    confidence = "low"  # default
    reasoning = response_text
    
    lines = response_text.strip().split('\n')
    for line in lines:
        if line.startswith('CONFIDENCE:'):
            conf_str = line.replace('CONFIDENCE:', '').strip().lower()
            if 'high' in conf_str:
                confidence = 'high'
            elif 'medium' in conf_str:
                confidence = 'medium'
            elif 'low' in conf_str:
                confidence = 'low'
        elif line.startswith('REASONING:'):
            reasoning = line.replace('REASONING:', '').strip()

    return {
        "confidence": confidence,
        "reasoning": reasoning,
        "raw_response": response_text,
        "stop_reason": message.stop_reason,
    }


def run_evaluation(eval_set_path: str, output_path: str, api_key: Optional[str] = None):
    """
    Run evaluation on all claims in the eval set.
    Save results to output file.
    """
    # Initialize client
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
    else:
        client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

    # Load eval set
    eval_cases = load_eval_set(eval_set_path)
    print(f"Loaded {len(eval_cases)} test cases from {eval_set_path}")

    results = {
        "metadata": {
            "eval_set_path": eval_set_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_cases": len(eval_cases),
            "model": "claude-opus-4-6",
        },
        "predictions": [],
    }

    # Score each claim
    for i, case in enumerate(eval_cases, 1):
        claim_id = case["id"]
        claim_text = case["claim"]
        expected = case["expected_confidence"]
        dossier_version = case["dossier_version"]

        print(f"[{i}/{len(eval_cases)}] Scoring {claim_id}...", end=" ", flush=True)

        try:
            prediction = score_claim(client, claim_text)
            result_entry = {
                "id": claim_id,
                "dossier_version": dossier_version,
                "claim": claim_text,
                "expected_confidence": expected,
                "predicted_confidence": prediction["confidence"],
                "reasoning": prediction["reasoning"],
            }
            results["predictions"].append(result_entry)
            print(f"predicted: {prediction['confidence']}")

        except Exception as e:
            print(f"ERROR: {e}")
            result_entry = {
                "id": claim_id,
                "dossier_version": dossier_version,
                "claim": claim_text,
                "expected_confidence": expected,
                "predicted_confidence": None,
                "error": str(e),
            }
            results["predictions"].append(result_entry)

        # Small delay to avoid rate limits
        time.sleep(0.5)

    # Save results
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")
    return results


if __name__ == "__main__":
    # Default paths
    eval_set = "evals/eval_set.json"
    output = "evals/raw_predictions.json"

    # Allow override via CLI
    if len(sys.argv) > 1:
        eval_set = sys.argv[1]
    if len(sys.argv) > 2:
        output = sys.argv[2]

    # Run evaluation
    results = run_evaluation(eval_set, output)

    # Print summary
    predictions = results["predictions"]
    valid_predictions = [p for p in predictions if p.get("predicted_confidence")]
    errors = [p for p in predictions if p.get("error")]

    print(f"\nSummary:")
    print(f"  Valid predictions: {len(valid_predictions)}")
    print(f"  Errors: {len(errors)}")

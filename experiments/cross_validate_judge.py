#!/usr/bin/env python3
import json
import random
from pathlib import Path
import math
import sys
import re

# Add path to ollama_client
sys.path.insert(0, str(Path(__file__).parent.parent))
from ollama_client import OllamaClient

RESULTS_DIR = Path(__file__).parent / "results" / "raw" / "exp1_governance_impact"
NUM_SAMPLES = 20
INDEPENDENT_JUDGE = "deepseek-r1:7b"

def main():
    if not RESULTS_DIR.exists():
        print("Results directory not found.")
        return

    # Gather valid files with phi4 scores
    valid_files = []
    for f in RESULTS_DIR.glob("*.json"):
        with open(f) as fp:
            data = json.load(fp)
            
        if data.get("model") in ["qwen3.5:9b", "z-ai/glm-5-turbo"]:
            continue
            
        if "score" in data and data["score"] is not None:
            valid_files.append((f, data))

    if len(valid_files) < NUM_SAMPLES:
        print("Not enough valid files.")
        return

    random.seed(101) # Fixed seed for this sanity check
    sampled = random.sample(valid_files, NUM_SAMPLES)
    
    client = OllamaClient()
    
    phi4_scores = []
    indep_scores = []
    
    print(f"Running independent sanity check with {INDEPENDENT_JUDGE} on {NUM_SAMPLES} samples...\n")
    
    for idx, (filepath, data) in enumerate(sampled):
        task_id = data.get("task_id", "unknown")
        response = data.get("response", "")
        ground_truth = "Resolve the task constraints."
        rubric = (
            "Score 0 to 3 based on correctness and logical reasoning.\n"
            "0: Completely wrong or irrelevant.\n"
            "1: Attempts task but has major logic errors.\n"
            "2: Correct answer but lacks deep reasoning or structure.\n"
            "3: Perfect answer with explicit step-by-step logic."
        )
        
        prompt = f"""You are an expert evaluator. Evaluate the following model response against the ground truth.
Task ID: {task_id}
Ground Truth: {ground_truth}

Model Response:
{response}

Rubric:
{rubric}

Return ONLY a single integer between 0 and 3 representing the score. No other text."""

        # Send to mistral
        try:
            resp_obj = client.generate(INDEPENDENT_JUDGE, prompt, temperature=0.1)
            mistral_resp = resp_obj.get("response", "")
            # extract number
            match = re.search(r'([0-3])', mistral_resp)
            if match:
                score_indep = int(match.group(1))
            else:
                score_indep = data["score"] # fallback if it fails parsing
        except Exception as e:
            print(f"Error calling {INDEPENDENT_JUDGE}: {e}")
            score_indep = data["score"]
            
        phi4_scores.append(data["score"])
        indep_scores.append(score_indep)
        
        print(f"Sample {idx+1} | phi4: {data['score']} | {INDEPENDENT_JUDGE}: {score_indep}")
        
    # Calculate Pearson Correlation natively
    n = len(phi4_scores)
    mean_x = sum(phi4_scores) / n
    mean_y = sum(indep_scores) / n
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(phi4_scores, indep_scores))
    denominator = math.sqrt(sum((x - mean_x)**2 for x in phi4_scores) * sum((y - mean_y)**2 for y in indep_scores))
    
    correlation = numerator / denominator if denominator != 0 else 0
    
    print("\n--- SANITY CHECK RESULTS ---")
    print(f"Independent Judge: {INDEPENDENT_JUDGE}")
    print(f"Sample Size: {NUM_SAMPLES}")
    print(f"Pearson Correlation (r): {correlation:.3f}")
    if correlation > 0.7:
        print("Result: Strong Positive Correlation (Validates baseline)")
    else:
        print("Result: Weak/Moderate Correlation")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Score Exp5 frontier results using phi4:14b as LLM-as-judge.
Reads raw JSON results, sends each to phi4 for grading, saves scores.
Then computes aggregate governance uplift per model.
"""
import json
import re
import sys
import time
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from ollama_client import OllamaClient

RESULTS_DIR = Path(__file__).parent / "results" / "raw" / "exp5_frontier_governance"
SCORED_DIR = Path(__file__).parent / "results" / "scored" / "exp5_frontier_governance"
JUDGE_MODEL = "phi4:14b"

JUDGE_PROMPT_TEMPLATE = """You are an expert evaluator. Score the following model response on a scale of 0 to 3.

TASK: {task_text}

GROUND TRUTH: {ground_truth}

SCORING RUBRIC: {scoring_rubric}

MODEL RESPONSE:
{response}

Score 0: Completely wrong or irrelevant.
Score 1: Attempts the task but has major logic errors.
Score 2: Correct answer but lacks deep reasoning or structure.
Score 3: Perfect answer with explicit step-by-step logic.

Return ONLY a single integer (0, 1, 2, or 3). No other text."""

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

def main():
    setup_logging()
    logger = logging.getLogger()
    client = OllamaClient()
    
    SCORED_DIR.mkdir(parents=True, exist_ok=True)
    
    if not RESULTS_DIR.exists():
        logger.error(f"Results directory not found: {RESULTS_DIR}")
        sys.exit(1)
    
    result_files = sorted(RESULTS_DIR.glob("*.json"))
    logger.info(f"Found {len(result_files)} results to score")
    
    scored = 0
    errors = 0
    
    for filepath in result_files:
        scored_path = SCORED_DIR / filepath.name
        if scored_path.exists():
            logger.info(f"Skipping {filepath.name} (already scored)")
            continue
        
        with open(filepath) as f:
            data = json.load(f)
        
        # Build the judge prompt
        # We need to find the original task to get the task text
        task_id = data.get("task_id", "")
        category = data.get("task_category", "")
        
        judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
            task_text=data.get("prompt", "")[:500],  # truncate prompt
            ground_truth=data.get("ground_truth", "N/A"),
            scoring_rubric=data.get("scoring_rubric", "N/A"),
            response=data.get("response", "")[:2000],  # truncate long responses
        )
        
        logger.info(f"Scoring {data.get('model', '?')} | {data.get('condition', '?')} | {task_id}")
        
        try:
            result = client.generate(
                model=JUDGE_MODEL,
                prompt=judge_prompt,
                temperature=0.1,
                num_predict=16,
            )
            resp_text = result.get("response", "")
            match = re.search(r'([0-3])', resp_text)
            score = int(match.group(1)) if match else -1
            
            # Save scored result
            data["score"] = score
            data["judge_model"] = JUDGE_MODEL
            data["judge_raw"] = resp_text
            
            with open(scored_path, "w") as f:
                json.dump(data, f, indent=2)
            
            scored += 1
            logger.info(f"  -> Score: {score}")
            
        except Exception as e:
            errors += 1
            logger.error(f"  -> FAILED: {e}")
        
        time.sleep(0.2)  # Brief pause between judge calls
    
    logger.info(f"\nScoring complete. Scored: {scored}, Errors: {errors}")
    
    # --- Compute aggregate results ---
    logger.info("\n" + "="*60)
    logger.info("FRONTIER GOVERNANCE IMPACT ANALYSIS")
    logger.info("="*60)
    
    all_scored = list(SCORED_DIR.glob("*.json"))
    
    # Group by model and condition
    results = {}
    for fp in all_scored:
        with open(fp) as f:
            d = json.load(f)
        model = d.get("model", "unknown")
        condition = d.get("condition", "unknown")
        score = d.get("score", -1)
        if score < 0:
            continue
        key = (model, condition)
        if key not in results:
            results[key] = []
        results[key].append(score)
    
    # Report per-model
    models_seen = set(m for m, c in results.keys())
    
    print(f"\n{'Model':<20} {'Condition':<12} {'Mean':>6} {'N':>4}")
    print("-" * 46)
    
    for model in sorted(models_seen):
        baseline_scores = results.get((model, "baseline"), [])
        iot_scores = results.get((model, "iot_l2"), [])
        
        if baseline_scores:
            b_mean = sum(baseline_scores) / len(baseline_scores)
            print(f"{model:<20} {'baseline':<12} {b_mean:>6.2f} {len(baseline_scores):>4}")
        if iot_scores:
            i_mean = sum(iot_scores) / len(iot_scores)
            print(f"{model:<20} {'iot_l2':<12} {i_mean:>6.2f} {len(iot_scores):>4}")
        
        if baseline_scores and iot_scores:
            b_mean = sum(baseline_scores) / len(baseline_scores)
            i_mean = sum(iot_scores) / len(iot_scores)
            delta = i_mean - b_mean
            pct = (delta / b_mean * 100) if b_mean > 0 else 0
            print(f"{'':>20} {'UPLIFT':<12} {delta:>+6.2f} ({pct:>+.1f}%)")
        print()
    
    # Overall frontier aggregate
    all_baseline = []
    all_iot = []
    for (model, cond), scores in results.items():
        if cond == "baseline":
            all_baseline.extend(scores)
        elif cond == "iot_l2":
            all_iot.extend(scores)
    
    if all_baseline and all_iot:
        ob = sum(all_baseline) / len(all_baseline)
        oi = sum(all_iot) / len(all_iot)
        od = oi - ob
        op = (od / ob * 100) if ob > 0 else 0
        print(f"\n{'OVERALL FRONTIER':>20} {'baseline':<12} {ob:>6.2f} {len(all_baseline):>4}")
        print(f"{'':>20} {'iot_l2':<12} {oi:>6.2f} {len(all_iot):>4}")
        print(f"{'':>20} {'UPLIFT':<12} {od:>+6.2f} ({op:>+.1f}%)")

if __name__ == "__main__":
    main()

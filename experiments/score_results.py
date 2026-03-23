#!/usr/bin/env python3
"""
IoT Lifecycle Experiment Suite: Phase 2 - Batch Score Results

Scores all raw experiment results using an LLM judge.
Run this AFTER run_all.py (Phase 1) has completed.

The scorer reads each JSON result file, extracts the 'response' field,
sends it to the judge model for evaluation, and writes the score back.

Usage:
    python3 score_results.py                     # Score all unscored results
    python3 score_results.py --experiment exp1   # Score specific experiment
    python3 score_results.py --force             # Re-score all (even scored)
    python3 score_results.py --judge qwen3.5:9b  # Use specific judge model
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from config import RAW_RESULTS_DIR, JUDGE_MODEL, LOG_FILE
from ollama_client import OllamaClient, extract_response_text
from scorer import Scorer


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE.parent / "scoring.log"),
            logging.StreamHandler(),
        ],
    )


def score_file(scorer: Scorer, filepath: Path, force: bool = False) -> bool:
    """Score a single result file. Returns True if scored, False if skipped."""
    with open(filepath) as f:
        result = json.load(f)

    # Skip if already scored (unless --force)
    if not force and "score" in result and result.get("score", -1) >= 0:
        return False

    # Need response text to score
    response = result.get("response", "")
    if not response:
        logging.warning(f"No response in {filepath.name}, skipping")
        return False

    # Build task text from available fields
    task_id = result.get("task_id", "unknown")
    ground_truth = result.get("ground_truth", "")
    anti_purpose = result.get("anti_purpose", "")
    scoring_rubric = result.get("scoring_rubric", "")
    topology = result.get("topology", result.get("forced_topology", ""))

    # Reconstruct task text (minimal, the judge mainly needs the response + ground truth)
    task_text = f"Task ID: {task_id}"

    try:
        score_result = scorer.score(
            task_text=task_text,
            model_output=response,
            ground_truth=ground_truth,
            anti_purpose=anti_purpose,
            topology_used=topology,
            custom_rubric=scoring_rubric,
        )

        # Write scores back into result
        result["score"] = score_result["score"]
        result["score_reason"] = score_result["reason"]
        result["score_consistent"] = score_result["consistent"]
        result["scored_at"] = datetime.now().isoformat()

        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)

        return True

    except Exception as e:
        logging.error(f"Scoring failed for {filepath.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Phase 2: Batch Score Results")
    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="Score specific experiment (e.g., exp1_governance_impact)",
    )
    parser.add_argument(
        "--judge",
        type=str,
        default=JUDGE_MODEL,
        help=f"Judge model (default: {JUDGE_MODEL})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-score all results, even already scored ones",
    )
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger()

    client = OllamaClient()
    scorer = Scorer(client=client, judge_model=args.judge)

    # Find result files
    if args.experiment:
        exp_dirs = [RAW_RESULTS_DIR / args.experiment]
    else:
        exp_dirs = [d for d in RAW_RESULTS_DIR.iterdir() if d.is_dir()]

    total_files = 0
    scored = 0
    skipped = 0
    failed = 0

    for exp_dir in sorted(exp_dirs):
        json_files = sorted(exp_dir.glob("*.json"))
        logger.info(f"\nScoring {exp_dir.name}: {len(json_files)} files")

        for filepath in json_files:
            total_files += 1
            result = score_file(scorer, filepath, force=args.force)

            if result:
                scored += 1
                logger.info(f"  Scored: {filepath.name}")
            else:
                skipped += 1

            # Progress every 10
            if total_files % 10 == 0:
                logger.info(f"  Progress: {total_files} processed, {scored} scored, {skipped} skipped")

    logger.info(f"\n{'='*60}")
    logger.info(f"SCORING COMPLETE")
    logger.info(f"Total: {total_files} | Scored: {scored} | Skipped: {skipped}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()

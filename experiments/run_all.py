#!/usr/bin/env python3
"""
IoT Lifecycle Experiment Suite: Phase 1 - Generate Responses

Runs all experiments and saves raw model responses (no scoring).
Scoring is done separately in Phase 2 via score_results.py.

Usage:
    python3 run_all.py                           # Run all experiments, all models
    python3 run_all.py --experiments exp1 exp8    # Run specific experiments
    python3 run_all.py --models mistral:latest    # Run with specific model
    python3 run_all.py --dry-run                  # Single task, single model test
    python3 run_all.py --resume                   # Resume from last checkpoint
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent dir for lifecycle package access
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    MODELS, JUDGE_MODEL, TOPOLOGIES, IOT_LEVELS,
    RAW_RESULTS_DIR, ANALYSIS_DIR, TASKS_DIR, PROMPTS_DIR,
    LOG_FILE, DEFAULT_TEMPERATURE, DEFAULT_NUM_PREDICT,
)
from ollama_client import OllamaClient, extract_response_text, get_token_counts


# IoT governance specifications for each task category
IOT_SPECS = {
    "sequential": {
        "purpose": "Follow a single logical chain of reasoning to reach a definitive answer",
        "anti_purpose": "Must not branch into alternative approaches before completing the primary chain",
        "success_signal": "A step-by-step derivation reaching a verifiable conclusion",
    },
    "parallel": {
        "purpose": "Explore multiple alternative approaches and compare them systematically",
        "anti_purpose": "Must not commit to a single approach without evaluating alternatives",
        "success_signal": "At least 3 distinct approaches with explicit trade-off comparison and justified recommendation",
    },
    "interconnected": {
        "purpose": "Identify relationships and interactions between multiple factors",
        "anti_purpose": "Must not treat factors as independent when they interact",
        "success_signal": "A relationship map showing connections, feedback loops, and systemic effects",
    },
}


def setup_logging(log_file: Path):
    """Configure logging to file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )


def load_tasks(category: str) -> list:
    """Load tasks from JSON file."""
    path = TASKS_DIR / f"{category}.json"
    with open(path) as f:
        return json.load(f)


def load_prompt(template_name: str) -> str:
    """Load prompt template."""
    path = PROMPTS_DIR / f"{template_name}.txt"
    with open(path) as f:
        return f.read()


def build_prompt(
    template: str,
    task: dict,
    iot_spec: Optional[dict] = None,
) -> str:
    """Build a complete prompt from template and task."""
    prompt = template.replace("{task_text}", task["text"])
    prompt = prompt.replace("{domain}", task.get("domain", "general"))

    if iot_spec:
        prompt = prompt.replace("{purpose}", iot_spec.get("purpose", ""))
        prompt = prompt.replace("{anti_purpose}", iot_spec.get("anti_purpose", ""))
        prompt = prompt.replace("{success_signal}", iot_spec.get("success_signal", ""))

    return prompt


def save_result(experiment: str, result: dict):
    """Save a single result to JSON. Uses run_id as filename."""
    exp_dir = RAW_RESULTS_DIR / experiment
    exp_dir.mkdir(parents=True, exist_ok=True)

    run_id = result.get("run_id", "unknown")
    filename = run_id.replace(":", "_").replace("/", "_") + ".json"

    with open(exp_dir / filename, "w") as f:
        json.dump(result, f, indent=2)


def load_checkpoint(experiment: str) -> set:
    """Load completed run IDs for resume."""
    exp_dir = RAW_RESULTS_DIR / experiment
    if not exp_dir.exists():
        return set()

    completed = set()
    for f in exp_dir.glob("*.json"):
        # Use filename stem (which is the sanitised run_id)
        completed.add(f.stem)
    return completed


def run_single(
    client: OllamaClient,
    model: str,
    prompt: str,
    temperature: float = DEFAULT_TEMPERATURE,
    num_predict: int = DEFAULT_NUM_PREDICT,
) -> dict:
    """Run a single model call and return result with timing."""
    start = time.time()
    result = client.generate(
        model=model,
        prompt=prompt,
        temperature=temperature,
        num_predict=num_predict,
    )
    elapsed = time.time() - start

    return {
        "response": extract_response_text(result),
        "tokens": get_token_counts(result),
        "elapsed_seconds": round(elapsed, 2),
    }


# ─── EXPERIMENT 1: IoT Governance Impact ──────────────────────────

def exp1_governance_impact(
    client: OllamaClient,
    models: list,
    resume: bool = False,
):
    """
    Exp 1: IoT governance improves reasoning output quality.

    Design: 2 conditions × N models × 3 categories × 4 topologies
    Conditions: with IoT (L2) / without IoT (baseline)
    """
    logger = logging.getLogger("iot_experiments")
    experiment = "exp1_governance_impact"
    completed = load_checkpoint(experiment) if resume else set()

    categories = ["sequential", "parallel", "interconnected"]
    conditions = ["baseline", "iot_l2"]

    total = 0
    for category in categories:
        tasks = load_tasks(category)
        iot_spec = IOT_SPECS[category]

        for task in tasks:
            for topology in ["baseline", "cot", "tot", "got"]:
                for model in models:
                    for condition in conditions:
                        run_id = f"{task['id']}_{model}_{condition}_{topology}".replace(":", "_").replace("/", "_")
                        if run_id in completed:
                            continue

                        # Build prompt
                        if condition == "iot_l2":
                            template = load_prompt("iot_l2")
                            prompt = build_prompt(template, task, iot_spec)
                        else:
                            template = load_prompt(topology)
                            prompt = build_prompt(template, task)

                        logger.info(
                            f"[Exp1] {model} | {category}/{task['id']} | "
                            f"{condition} | {topology}"
                        )

                        try:
                            run_result = run_single(client, model, prompt)

                            result = {
                                "run_id": run_id,
                                "experiment": experiment,
                                "task_id": task["id"],
                                "task_category": category,
                                "model": model,
                                "condition": condition,
                                "topology": topology,
                                "optimal_topology": task["optimal_topology"],
                                "ground_truth": task.get("ground_truth", ""),
                                "scoring_rubric": task.get("scoring_rubric", ""),
                                "response": run_result["response"],
                                "response_length": len(run_result["response"]),
                                "elapsed_seconds": run_result["elapsed_seconds"],
                                "tokens": run_result["tokens"],
                                "timestamp": datetime.now().isoformat(),
                            }

                            save_result(experiment, result)
                            total += 1

                        except Exception as e:
                            logger.error(f"[Exp1] FAILED: {e}")
                            continue

    logger.info(f"[Exp1] Complete. {total} runs saved.")


# ─── EXPERIMENT 5: Anti-Purpose Ablation ──────────────────────────

def exp5_anti_purpose(
    client: OllamaClient,
    models: list,
    resume: bool = False,
):
    """
    Exp 5: Removing anti-purpose degrades safety-critical output.

    3 conditions: full triple, no anti-purpose, no success signal
    """
    logger = logging.getLogger("iot_experiments")
    experiment = "exp5_anti_purpose"
    completed = load_checkpoint(experiment) if resume else set()

    tasks = load_tasks("safety_critical")

    for task in tasks:
        for model in models:
            for condition in ["full_triple", "no_anti_purpose", "no_success_signal"]:
                run_id = f"{task['id']}_{model}_{condition}".replace(":", "_").replace("/", "_")
                if run_id in completed:
                    continue

                # Build IoT spec based on condition
                template = load_prompt("iot_l2")
                if condition == "full_triple":
                    iot_spec = {
                        "purpose": f"Analyse this {task['domain']} scenario thoroughly",
                        "anti_purpose": task.get("anti_purpose", ""),
                        "success_signal": "Comprehensive analysis identifying all key risks and interactions",
                    }
                elif condition == "no_anti_purpose":
                    iot_spec = {
                        "purpose": f"Analyse this {task['domain']} scenario thoroughly",
                        "anti_purpose": "(none specified)",
                        "success_signal": "Comprehensive analysis identifying all key risks and interactions",
                    }
                else:  # no_success_signal
                    iot_spec = {
                        "purpose": f"Analyse this {task['domain']} scenario thoroughly",
                        "anti_purpose": task.get("anti_purpose", ""),
                        "success_signal": "(none specified)",
                    }

                prompt = build_prompt(template, task, iot_spec)
                logger.info(f"[Exp5] {model} | {task['id']} | {condition}")

                try:
                    run_result = run_single(client, model, prompt)

                    result = {
                        "run_id": run_id,
                        "experiment": experiment,
                        "task_id": task["id"],
                        "model": model,
                        "condition": condition,
                        "domain": task["domain"],
                        "ground_truth": task.get("ground_truth", ""),
                        "anti_purpose": task.get("anti_purpose", ""),
                        "scoring_rubric": task.get("scoring_rubric", ""),
                        "response": run_result["response"],
                        "response_length": len(run_result["response"]),
                        "elapsed_seconds": run_result["elapsed_seconds"],
                        "timestamp": datetime.now().isoformat(),
                    }

                    save_result(experiment, result)

                except Exception as e:
                    logger.error(f"[Exp5] FAILED: {e}")
                    continue


# ─── EXPERIMENT 8: Topology Confusion Matrix ─────────────────────

def exp8_confusion_matrix(
    client: OllamaClient,
    models: list,
    resume: bool = False,
):
    """
    Exp 8: Which topologies get misapplied to which task types.

    9 tasks × 3 forced topologies × N models
    """
    logger = logging.getLogger("iot_experiments")
    experiment = "exp8_confusion_matrix"
    completed = load_checkpoint(experiment) if resume else set()

    categories = ["sequential", "parallel", "interconnected"]
    forced_topologies = ["cot", "tot", "got"]

    for category in categories:
        tasks = load_tasks(category)
        iot_spec = IOT_SPECS[category]

        for task in tasks:
            for topology in forced_topologies:
                for model in models:
                    run_id = f"{task['id']}_{model}_{topology}".replace(":", "_").replace("/", "_")
                    if run_id in completed:
                        continue

                    # Use IoT L2 + forced topology
                    template = load_prompt(topology)
                    # Prepend IoT governance
                    iot_prefix = (
                        f"PURPOSE: {iot_spec['purpose']}\n"
                        f"ANTI-PURPOSE: {iot_spec['anti_purpose']}\n"
                        f"SUCCESS SIGNAL: {iot_spec['success_signal']}\n\n"
                    )
                    prompt = iot_prefix + build_prompt(template, task)

                    logger.info(
                        f"[Exp8] {model} | {category}/{task['id']} | forced={topology}"
                    )

                    try:
                        run_result = run_single(client, model, prompt)

                        result = {
                            "run_id": run_id,
                            "experiment": experiment,
                            "task_id": task["id"],
                            "task_category": category,
                            "optimal_topology": task["optimal_topology"],
                            "forced_topology": topology,
                            "model": model,
                            "ground_truth": task.get("ground_truth", ""),
                            "scoring_rubric": task.get("scoring_rubric", ""),
                            "response": run_result["response"],
                            "response_length": len(run_result["response"]),
                            "elapsed_seconds": run_result["elapsed_seconds"],
                            "timestamp": datetime.now().isoformat(),
                        }

                        save_result(experiment, result)

                    except Exception as e:
                        logger.error(f"[Exp8] FAILED: {e}")
                        continue


# ─── MAIN ─────────────────────────────────────────────────────────

EXPERIMENTS = {
    "exp1": ("IoT Governance Impact", exp1_governance_impact),
    "exp5": ("Anti-Purpose Ablation", exp5_anti_purpose),
    "exp8": ("Topology Confusion Matrix", exp8_confusion_matrix),
}


def check_models(client: OllamaClient, models: list) -> list:
    """Verify which models are available."""
    available = client.list_models()
    verified = []
    for model in models:
        if any(model in m for m in available):
            verified.append(model)
        else:
            logging.warning(f"Model {model} not available. Skipping.")
    return verified


def main():
    parser = argparse.ArgumentParser(description="IoT Lifecycle Experiment Suite")
    parser.add_argument(
        "--experiments",
        nargs="+",
        default=list(EXPERIMENTS.keys()),
        help="Experiments to run (e.g., exp1 exp5 exp8)",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["all"],
        help="Models to use (e.g., mistral:latest qwen3.5:9b) or 'all'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run single task with single model for pipeline test",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last checkpoint (skip completed runs)",
    )
    args = parser.parse_args()

    setup_logging(LOG_FILE)
    logger = logging.getLogger("iot_experiments")

    # Initialise client
    client = OllamaClient()

    # Resolve models
    if "all" in args.models:
        model_list = list(MODELS.keys())
    else:
        model_list = args.models

    # Verify models available
    model_list = check_models(client, model_list)
    if not model_list:
        logger.error("No models available. Is Ollama running?")
        sys.exit(1)

    logger.info(f"Models: {model_list}")
    logger.info(f"Experiments: {args.experiments}")

    if args.dry_run:
        logger.info("DRY RUN: single task, single model")
        model_list = model_list[:1]

    # Run experiments
    start_time = time.time()

    for exp_key in args.experiments:
        if exp_key not in EXPERIMENTS:
            logger.warning(f"Unknown experiment: {exp_key}. Skipping.")
            continue

        name, func = EXPERIMENTS[exp_key]
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting: {name} ({exp_key})")
        logger.info(f"{'='*60}")

        exp_start = time.time()
        func(client, model_list, resume=args.resume)
        exp_elapsed = time.time() - exp_start
        logger.info(f"Completed: {name} in {exp_elapsed/60:.1f} minutes")

    total_elapsed = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info(f"ALL EXPERIMENTS COMPLETE in {total_elapsed/60:.1f} minutes")
    logger.info(f"Results saved to: {RAW_RESULTS_DIR}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()

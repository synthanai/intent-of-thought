#!/usr/bin/env python3
"""
IoT Lifecycle Cloud Experiment Runner
======================================
Runs all experiments via OpenRouter API for cloud models.
Results are saved in the same format as local Ollama runs.

Usage:
    python3 run_cloud.py                              # All experiments, all models
    python3 run_cloud.py --experiments exp1            # Specific experiment
    python3 run_cloud.py --models z-ai/glm-5-turbo    # Specific model
    python3 run_cloud.py --dry-run                     # Single task test
    python3 run_cloud.py --resume                      # Skip completed runs
"""

import argparse
import json
import logging
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    RAW_RESULTS_DIR, TASKS_DIR, PROMPTS_DIR, LOG_FILE,
    DEFAULT_TEMPERATURE, DEFAULT_NUM_PREDICT,
)

# ─── CONFIG ───────────────────────────────────────────────────────

API_KEY = os.getenv("OPENROUTER_API_KEY", "")
if not API_KEY:
    # Try loading from .env file
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
API_URL = "https://openrouter.ai/api/v1/chat/completions"

CLOUD_MODELS = {
    "z-ai/glm-5-turbo": {
        "family": "zhipu",
        "params": "~14B",
        "architecture": "dense",
        "tier": 2,
        "role": "diversity_cloud",
    },
    "nvidia/nemotron-3-super-120b-a12b:free": {
        "family": "nvidia",
        "params": "120B (12B active)",
        "architecture": "moe",
        "tier": 3,
        "role": "large_moe_cloud",
    },
}

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

RATE_LIMIT_SECONDS = 1.0  # free tier rate limiting


# ─── API CLIENT ───────────────────────────────────────────────────

def call_openrouter(
    model: str,
    prompt: str,
    system: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_NUM_PREDICT,
) -> dict:
    """Call OpenRouter API. Returns dict compatible with Ollama result format."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://synthai.biz/",
        "X-Title": "IoT Lifecycle Experiment",
    }

    start = time.time()
    for attempt in range(3):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - start

            # Extract content (handle reasoning models)
            msg = data.get("choices", [{}])[0].get("message", {})
            content = msg.get("content") or ""
            if not content.strip():
                reasoning = msg.get("reasoning") or ""
                if not reasoning:
                    details = msg.get("reasoning_details") or []
                    reasoning = "\n".join(
                        d.get("text", "") for d in details if d.get("text")
                    )
                content = reasoning

            usage = data.get("usage", {})

            return {
                "response": content.strip(),
                "tokens": {
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_duration_ms": round(elapsed * 1000, 2),
                },
                "elapsed_seconds": round(elapsed, 2),
            }

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429:  # rate limited
                wait = 2 ** (attempt + 1)
                logging.warning(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            logging.error(f"HTTP {e.code}: {body[:200]}")
            return {"response": "", "tokens": {}, "elapsed_seconds": round(time.time() - start, 2)}

        except Exception as e:
            wait = 2 ** attempt
            logging.warning(f"Attempt {attempt + 1}/3 failed: {e}. Retrying in {wait}s...")
            if attempt < 2:
                time.sleep(wait)
            else:
                return {"response": "", "tokens": {}, "elapsed_seconds": round(time.time() - start, 2)}


# ─── HELPERS ──────────────────────────────────────────────────────

def load_tasks(category: str) -> list:
    path = TASKS_DIR / f"{category}.json"
    with open(path) as f:
        return json.load(f)


def load_prompt(template_name: str) -> str:
    path = PROMPTS_DIR / f"{template_name}.txt"
    with open(path) as f:
        return f.read()


def build_prompt(template: str, task: dict, iot_spec: dict = None) -> str:
    prompt = template.replace("{task_text}", task["text"])
    prompt = prompt.replace("{domain}", task.get("domain", "general"))
    if iot_spec:
        prompt = prompt.replace("{purpose}", iot_spec.get("purpose", ""))
        prompt = prompt.replace("{anti_purpose}", iot_spec.get("anti_purpose", ""))
        prompt = prompt.replace("{success_signal}", iot_spec.get("success_signal", ""))
    return prompt


def save_result(experiment: str, result: dict):
    exp_dir = RAW_RESULTS_DIR / experiment
    exp_dir.mkdir(parents=True, exist_ok=True)
    run_id = result.get("run_id", "unknown")
    filename = run_id.replace(":", "_").replace("/", "_") + ".json"
    with open(exp_dir / filename, "w") as f:
        json.dump(result, f, indent=2)


def load_checkpoint(experiment: str) -> set:
    exp_dir = RAW_RESULTS_DIR / experiment
    if not exp_dir.exists():
        return set()
    return {f.stem for f in exp_dir.glob("*.json")}


def sanitise_model(model: str) -> str:
    return model.replace(":", "_").replace("/", "_")


# ─── EXPERIMENT 1 ─────────────────────────────────────────────────

def exp1_governance_impact(models: list, resume: bool = False):
    logger = logging.getLogger("iot_cloud")
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
                        run_id = f"{task['id']}_{sanitise_model(model)}_{condition}_{topology}"
                        if run_id in completed:
                            logger.info(f"[Exp1] SKIP {run_id}")
                            continue

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

                        run_result = call_openrouter(model, prompt)
                        time.sleep(RATE_LIMIT_SECONDS)

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
                            "backend": "openrouter",
                        }

                        save_result(experiment, result)
                        total += 1

                        status = "✅" if run_result["response"] else "❌ empty"
                        logger.info(
                            f"  {status} {len(run_result['response'])}chars "
                            f"{run_result['elapsed_seconds']}s"
                        )

    logger.info(f"[Exp1] Complete. {total} cloud runs saved.")


# ─── EXPERIMENT 5 ─────────────────────────────────────────────────

def exp5_anti_purpose(models: list, resume: bool = False):
    logger = logging.getLogger("iot_cloud")
    experiment = "exp5_anti_purpose"
    completed = load_checkpoint(experiment) if resume else set()

    tasks = load_tasks("safety_critical")
    total = 0

    for task in tasks:
        for model in models:
            for condition in ["full_triple", "no_anti_purpose", "no_success_signal"]:
                run_id = f"{task['id']}_{sanitise_model(model)}_{condition}"
                if run_id in completed:
                    continue

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
                else:
                    iot_spec = {
                        "purpose": f"Analyse this {task['domain']} scenario thoroughly",
                        "anti_purpose": task.get("anti_purpose", ""),
                        "success_signal": "(none specified)",
                    }

                prompt = build_prompt(template, task, iot_spec)
                logger.info(f"[Exp5] {model} | {task['id']} | {condition}")

                run_result = call_openrouter(model, prompt)
                time.sleep(RATE_LIMIT_SECONDS)

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
                    "backend": "openrouter",
                }

                save_result(experiment, result)
                total += 1

    logger.info(f"[Exp5] Complete. {total} cloud runs saved.")


# ─── EXPERIMENT 8 ─────────────────────────────────────────────────

def exp8_confusion_matrix(models: list, resume: bool = False):
    logger = logging.getLogger("iot_cloud")
    experiment = "exp8_confusion_matrix"
    completed = load_checkpoint(experiment) if resume else set()

    categories = ["sequential", "parallel", "interconnected"]
    forced_topologies = ["cot", "tot", "got"]
    total = 0

    for category in categories:
        tasks = load_tasks(category)
        iot_spec = IOT_SPECS[category]

        for task in tasks:
            for topology in forced_topologies:
                for model in models:
                    run_id = f"{task['id']}_{sanitise_model(model)}_{topology}"
                    if run_id in completed:
                        continue

                    template = load_prompt(topology)
                    iot_prefix = (
                        f"PURPOSE: {iot_spec['purpose']}\n"
                        f"ANTI-PURPOSE: {iot_spec['anti_purpose']}\n"
                        f"SUCCESS SIGNAL: {iot_spec['success_signal']}\n\n"
                    )
                    prompt = iot_prefix + build_prompt(template, task)

                    logger.info(
                        f"[Exp8] {model} | {category}/{task['id']} | forced={topology}"
                    )

                    run_result = call_openrouter(model, prompt)
                    time.sleep(RATE_LIMIT_SECONDS)

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
                        "backend": "openrouter",
                    }

                    save_result(experiment, result)
                    total += 1

    logger.info(f"[Exp8] Complete. {total} cloud runs saved.")


# ─── MAIN ─────────────────────────────────────────────────────────

EXPERIMENTS = {
    "exp1": ("IoT Governance Impact", exp1_governance_impact),
    "exp5": ("Anti-Purpose Ablation", exp5_anti_purpose),
    "exp8": ("Topology Confusion Matrix", exp8_confusion_matrix),
}


def main():
    parser = argparse.ArgumentParser(description="IoT Lifecycle Cloud Runner")
    parser.add_argument(
        "--experiments", nargs="+", default=list(EXPERIMENTS.keys()),
        help="Experiments to run (e.g., exp1 exp5 exp8)",
    )
    parser.add_argument(
        "--models", nargs="+", default=["all"],
        help="Models (e.g., z-ai/glm-5-turbo) or 'all'",
    )
    parser.add_argument("--dry-run", action="store_true", help="Single task test")
    parser.add_argument("--resume", action="store_true", help="Skip completed runs")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(Path(__file__).parent / "cloud_experiment.log"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger("iot_cloud")

    if "all" in args.models:
        model_list = list(CLOUD_MODELS.keys())
    else:
        model_list = args.models

    logger.info(f"Models: {model_list}")
    logger.info(f"Experiments: {args.experiments}")

    # Quick API test
    logger.info("Testing OpenRouter API...")
    test = call_openrouter(model_list[0], "Say 'hello' in one word.", max_tokens=10)
    if test["response"]:
        logger.info(f"API test OK: '{test['response'][:50]}' in {test['elapsed_seconds']}s")
    else:
        logger.error("API test FAILED. Check API key and model availability.")
        sys.exit(1)

    if args.dry_run:
        logger.info("DRY RUN: single experiment, single model")
        model_list = model_list[:1]
        args.experiments = ["exp1"]

    start_time = time.time()

    for exp_key in args.experiments:
        if exp_key not in EXPERIMENTS:
            logger.warning(f"Unknown experiment: {exp_key}")
            continue

        name, func = EXPERIMENTS[exp_key]
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting: {name} ({exp_key})")
        logger.info(f"{'='*60}")

        exp_start = time.time()
        func(model_list, resume=args.resume)
        exp_elapsed = time.time() - exp_start
        logger.info(f"Completed: {name} in {exp_elapsed/60:.1f} minutes")

    total_elapsed = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info(f"ALL CLOUD EXPERIMENTS COMPLETE in {total_elapsed/60:.1f} minutes")
    logger.info(f"Results saved to: {RAW_RESULTS_DIR}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()

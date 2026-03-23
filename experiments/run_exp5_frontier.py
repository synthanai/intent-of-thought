#!/usr/bin/env python3
"""
Exp5: Frontier Model Governance Impact
Runs 2 cheap frontier models (GPT-4o-mini, Claude 3.5 Haiku) via OpenRouter
to test whether IoT governance generalises beyond 7B-14B local models.

Design: 18 tasks x 2 conditions (baseline, IoT L2) x 2 models = 72 evaluations
"""
import json
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

# Add parent dir for config access
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import RAW_RESULTS_DIR, TASKS_DIR, PROMPTS_DIR, LOG_FILE

# --- Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    # Try loading from .env
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                OPENROUTER_API_KEY = line.split("=", 1)[1].strip()
                break

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

FRONTIER_MODELS = [
    {
        "id": "openai/gpt-4o-mini",
        "label": "gpt-4o-mini",
        "params": "~8B (distilled)",
    },
    {
        "id": "anthropic/claude-3.5-haiku",
        "label": "claude-3.5-haiku",
        "params": "~20B (estimated)",
    },
]

EXPERIMENT = "exp5_frontier_governance"
CATEGORIES = ["sequential", "parallel", "interconnected"]
TEMPERATURE = 0.7
MAX_TOKENS = 1024

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ],
    )

def load_tasks(category: str) -> list:
    path = TASKS_DIR / f"{category}.json"
    with open(path) as f:
        return json.load(f)

def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.txt"
    with open(path) as f:
        return f.read()

def call_openrouter(model_id: str, prompt: str, temperature: float = 0.7) -> dict:
    """Call OpenRouter API and return the response."""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": MAX_TOKENS,
    }
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        OPENROUTER_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://synthai.io",
            "X-Title": "IoT Frontier Experiment",
        },
        method="POST",
    )
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def extract_text(api_response: dict) -> str:
    """Extract text from OpenRouter response."""
    choices = api_response.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""

def extract_usage(api_response: dict) -> dict:
    """Extract token usage from OpenRouter response."""
    usage = api_response.get("usage", {})
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }

def build_baseline_prompt(task: dict) -> str:
    """Build a plain baseline prompt (no IoT governance)."""
    return f"Task: {task['text']}\n\nProvide your answer with clear reasoning."

def build_iot_prompt(template: str, task: dict) -> str:
    """Build the IoT L2 governed prompt."""
    prompt = template.replace("{task_text}", task["text"])
    prompt = prompt.replace("{domain}", task.get("domain", "general"))
    # Fill governance triple from task metadata
    prompt = prompt.replace("{purpose}", task.get("purpose", f"Solve the {task.get('domain', 'general')} reasoning task accurately"))
    prompt = prompt.replace("{anti_purpose}", task.get("anti_purpose", "Do not guess, hallucinate facts, or skip reasoning steps"))
    prompt = prompt.replace("{success_signal}", task.get("success_signal", "The answer is verifiably correct and the reasoning chain is explicit"))
    return prompt

def save_result(result: dict):
    """Save a single result JSON."""
    exp_dir = RAW_RESULTS_DIR / EXPERIMENT
    exp_dir.mkdir(parents=True, exist_ok=True)
    run_id = result.get("run_id", "unknown")
    filename = run_id.replace(":", "_").replace("/", "_") + ".json"
    with open(exp_dir / filename, "w") as f:
        json.dump(result, f, indent=2)

def main():
    setup_logging()
    logger = logging.getLogger()

    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found. Set in .env or environment.")
        sys.exit(1)

    iot_template = load_prompt("iot_l2")
    total = 0
    errors = 0

    conditions = [
        ("baseline", None),
        ("iot_l2", iot_template),
    ]

    logger.info(f"Starting Exp5: Frontier Governance Impact")
    logger.info(f"Models: {[m['label'] for m in FRONTIER_MODELS]}")
    logger.info(f"Tasks: {len(CATEGORIES)} categories x 6 tasks = 18 tasks")
    logger.info(f"Conditions: baseline, iot_l2")
    logger.info(f"Total evaluations: {18 * 2 * len(FRONTIER_MODELS)} = {18 * 2 * len(FRONTIER_MODELS)}")

    for model_info in FRONTIER_MODELS:
        model_id = model_info["id"]
        model_label = model_info["label"]

        for category in CATEGORIES:
            tasks = load_tasks(category)

            for task in tasks:
                for cond_name, cond_template in conditions:
                    run_id = f"{task['id']}_{model_label}_{cond_name}"

                    # Skip if already exists
                    expected_fn = run_id.replace(":", "_").replace("/", "_") + ".json"
                    if (RAW_RESULTS_DIR / EXPERIMENT / expected_fn).exists():
                        logger.info(f"Skipping {run_id} (exists)")
                        continue

                    # Build prompt
                    if cond_name == "baseline":
                        prompt = build_baseline_prompt(task)
                    else:
                        prompt = build_iot_prompt(cond_template, task)

                    logger.info(f"[Exp5] {model_label} | {cond_name} | {category}/{task['id']}")

                    start = time.time()
                    try:
                        api_resp = call_openrouter(model_id, prompt, TEMPERATURE)
                        elapsed = time.time() - start
                        response_text = extract_text(api_resp)
                        usage = extract_usage(api_resp)

                        result = {
                            "run_id": run_id,
                            "experiment": EXPERIMENT,
                            "task_id": task["id"],
                            "task_category": category,
                            "model": model_label,
                            "model_id": model_id,
                            "condition": cond_name,
                            "optimal_topology": task["optimal_topology"],
                            "ground_truth": task.get("ground_truth", ""),
                            "scoring_rubric": task.get("scoring_rubric", ""),
                            "prompt": prompt,
                            "response": response_text,
                            "response_length": len(response_text),
                            "elapsed_seconds": round(elapsed, 2),
                            "tokens": usage,
                            "timestamp": datetime.now().isoformat(),
                        }
                        save_result(result)
                        total += 1
                        logger.info(f"  -> {len(response_text)} chars, {elapsed:.1f}s")

                    except Exception as e:
                        errors += 1
                        logger.error(f"[Exp5 FAILED] {run_id}: {e}")
                        # Brief pause on error to avoid rate limiting
                        time.sleep(2)

                    # Small delay between API calls to respect rate limits
                    time.sleep(0.5)

    logger.info(f"Exp5 Frontier Complete. Generated {total} results, {errors} errors.")

if __name__ == "__main__":
    main()

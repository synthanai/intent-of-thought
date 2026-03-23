#!/usr/bin/env python3
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent dir for lifecycle package access
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    RAW_RESULTS_DIR, TASKS_DIR, PROMPTS_DIR, LOG_FILE,
    DEFAULT_TEMPERATURE, DEFAULT_NUM_PREDICT
)
from ollama_client import OllamaClient, extract_response_text, get_token_counts

def setup_logging(log_file: Path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )

def load_tasks(category: str) -> list:
    path = TASKS_DIR / f"{category}.json"
    with open(path) as f:
        return json.load(f)

def load_prompt(template_name: str) -> str:
    path = PROMPTS_DIR / f"{template_name}.txt"
    with open(path) as f:
        return f.read()

def build_prompt(template: str, task: dict) -> str:
    prompt = template.replace("{task_text}", task["text"])
    prompt = prompt.replace("{domain}", task.get("domain", "general"))
    return prompt

def save_result(experiment: str, result: dict):
    exp_dir = RAW_RESULTS_DIR / experiment
    exp_dir.mkdir(parents=True, exist_ok=True)
    run_id = result.get("run_id", "unknown")
    filename = run_id.replace(":", "_").replace("/", "_") + ".json"
    with open(exp_dir / filename, "w") as f:
        json.dump(result, f, indent=2)

def main():
    setup_logging(LOG_FILE)
    logger = logging.getLogger()
    client = OllamaClient()

    models = ["mistral:latest", "qwen2.5:7b", "deepseek-r1:7b"]
    experiment = "exp4_matched_control"
    categories = ["sequential", "parallel", "interconnected"]
    
    # Check Ollama available models
    available = client.list_models()
    verified_models = [m for m in models if any(m in avail for avail in available)]
    
    if not verified_models:
        logger.error("Required models not found in Ollama. Exiting.")
        sys.exit(1)

    template = load_prompt("iot_control")
    total = 0

    logger.info(f"Starting Exp4: Matched Control Baseline for {verified_models}")

    for category in categories:
        tasks = load_tasks(category)
        for task in tasks:
            prompt = build_prompt(template, task)
            
            for model in verified_models:
                run_id = f"{task['id']}_{model}_iot_control"
                
                # check if already exists
                expected_filename = run_id.replace(":", "_").replace("/", "_") + ".json"
                if (RAW_RESULTS_DIR / experiment / expected_filename).exists():
                    logger.info(f"Skipping {run_id} (already exists)")
                    continue
                
                logger.info(f"[Exp4 Control] {model} | {category}/{task['id']}")
                
                start = time.time()
                try:
                    result_raw = client.generate(
                        model=model,
                        prompt=prompt,
                        temperature=DEFAULT_TEMPERATURE,
                        num_predict=DEFAULT_NUM_PREDICT,
                    )
                    elapsed = time.time() - start
                    
                    result = {
                        "run_id": run_id,
                        "experiment": experiment,
                        "task_id": task["id"],
                        "task_category": category,
                        "model": model,
                        "condition": "iot_control",
                        "optimal_topology": task["optimal_topology"],
                        "ground_truth": task.get("ground_truth", ""),
                        "scoring_rubric": task.get("scoring_rubric", ""),
                        "response": extract_response_text(result_raw),
                        "response_length": len(extract_response_text(result_raw)),
                        "elapsed_seconds": round(elapsed, 2),
                        "tokens": get_token_counts(result_raw),
                        "timestamp": datetime.now().isoformat(),
                    }
                    save_result(experiment, result)
                    total += 1
                except Exception as e:
                    logger.error(f"[Exp4 FAILED] {run_id}: {e}")
                    
    logger.info(f"Exp4 Control Complete. Generated {total} new results.")

if __name__ == "__main__":
    main()

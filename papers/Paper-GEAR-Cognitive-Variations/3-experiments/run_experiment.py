#!/usr/bin/env python3
"""
G.E.A.R. Cognitive Variation Experiment (v2)
==============================================
Factorial design: 3 models × 3 tasks × 4 variations × 4 personalities = 144 runs

Fixes from v1:
- Pre-loads each model before its batch via `ollama run <model> "warmup"`
- Adds retry with exponential backoff (3 attempts)
- Uses lighter models to avoid timeout on M1
- Processes model-by-model (not interleaved) to avoid memory thrash
"""

import json
import subprocess
import os
import time
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# EXPERIMENTAL DESIGN
# ═══════════════════════════════════════════════════════════════

MODELS = [
    "qwen2.5:7b",       # Alibaba (Qwen architecture)
    "mistral:latest",   # Mistral AI (Mistral architecture, 7B, fast)
]

TASKS = {
    "analyse_scenario": {
        "label": "Analyse Business Scenario",
        "prompt": (
            "A mid-size software company (200 employees) has seen its customer churn rate "
            "increase from 5% to 12% over the past two quarters. During the same period, "
            "the company shipped 40% more features than any previous quarter, received its "
            "highest NPS score ever (72), and hired 30 new engineers. The CEO believes the "
            "churn is due to increased competition. Analyse this situation."
        ),
    },
    "review_code": {
        "label": "Review Code Pattern",
        "prompt": (
            "Review the following code pattern and provide your assessment:\n\n"
            "```python\n"
            "class EventProcessor:\n"
            "    def __init__(self):\n"
            "        self.handlers = {}\n"
            "        self.event_log = []\n"
            "        self._processing = False\n\n"
            "    def register(self, event_type, handler):\n"
            "        if event_type not in self.handlers:\n"
            "            self.handlers[event_type] = []\n"
            "        self.handlers[event_type].append(handler)\n\n"
            "    def emit(self, event_type, data):\n"
            "        self.event_log.append({'type': event_type, 'data': data, 'ts': time.time()})\n"
            "        if self._processing:\n"
            "            return  # Drop events during processing\n"
            "        self._processing = True\n"
            "        for handler in self.handlers.get(event_type, []):\n"
            "            handler(data)\n"
            "        self._processing = False\n"
            "```\n"
        ),
    },
    "summarise_finding": {
        "label": "Summarise Research Finding",
        "prompt": (
            "Summarise the following research finding and its implications:\n\n"
            "A 2024 study by Newton, Feeney, and Pennycook analysed 265 items from 15 "
            "existing thinking style scales using factor analysis across a large sample "
            "(N=1,200). They identified four statistically independent dimensions of "
            "thinking style: Actively Open-Minded Thinking (AOT), Close-Minded Thinking, "
            "Preference for Intuitive Thinking, and Preference for Effortful Thinking. "
            "Critically, these four dimensions had differential predictive validity: not "
            "all analytic thinkers were open-minded, and not all intuitive thinkers were "
            "close-minded. The correlation between AOT and Preference for Effortful "
            "Thinking was only r=0.31, suggesting substantial independence. The finding "
            "challenges the assumption that thinking style is a single continuum from "
            "'intuitive' to 'analytical'."
        ),
    },
}

VARIATIONS = {
    "generative": {
        "label": "Generative",
        "instruction": (
            "Adopt a GENERATIVE cognitive posture. Think through making. Your goal is to "
            "produce, create, and build forward. Ask yourself: 'What can I make from this? "
            "What wants to exist here?' Focus on creating new artifacts, ideas, proposals, "
            "or designs. Prioritise forward momentum and creative production."
        ),
    },
    "engaging": {
        "label": "Engaging",
        "instruction": (
            "Adopt an ENGAGING cognitive posture. Think through connection. Your goal is to "
            "find hidden patterns that bridge different domains. Ask yourself: 'What connects "
            "across these? What structural pattern does this share with something from an "
            "unrelated field?' Focus on cross-domain synthesis, analogies, and structural "
            "isomorphisms."
        ),
    },
    "adversarial": {
        "label": "Adversarial",
        "instruction": (
            "Adopt an ADVERSARIAL cognitive posture. Think through opposition. Your goal is "
            "to stress-test, challenge, and find what could break. Ask yourself: 'What could "
            "go wrong? What assumption is hiding here? What would a critic say?' Focus on "
            "finding flaws, failure modes, hidden risks, and unstated assumptions."
        ),
    },
    "reflective": {
        "label": "Reflective",
        "instruction": (
            "Adopt a REFLECTIVE cognitive posture. Think through backward examination. Your "
            "goal is to extract lessons, identify patterns from past experience, and update "
            "mental models. Ask yourself: 'What does this teach us? What pattern is repeating? "
            "What was assumed that turned out to be wrong?' Focus on learning, metacognition, "
            "and extracting transferable insights."
        ),
    },
}

PERSONALITIES = {
    "cautious_analyst": {
        "label": "Cautious Analyst",
        "instruction": (
            "You are a cautious, detail-oriented analyst. You prefer to be thorough rather "
            "than fast. You value precision, evidence, and careful qualification of claims. "
            "You are risk-averse and prefer to hedge your statements."
        ),
    },
    "bold_strategist": {
        "label": "Bold Strategist",
        "instruction": (
            "You are a bold, big-picture strategist. You think in terms of market dynamics, "
            "competitive advantage, and long-term positioning. You are comfortable with "
            "ambiguity and prefer decisive action over careful analysis."
        ),
    },
    "empathetic_collaborator": {
        "label": "Empathetic Collaborator",
        "instruction": (
            "You are an empathetic, people-oriented collaborator. You focus on how decisions "
            "affect individuals and teams. You value psychological safety, diverse perspectives, "
            "and collective intelligence. You listen before prescribing."
        ),
    },
    "methodical_engineer": {
        "label": "Methodical Engineer",
        "instruction": (
            "You are a methodical, systems-oriented engineer. You think in terms of "
            "architecture, trade-offs, and scalability. You value clean abstractions, "
            "testability, and reproducibility. You prefer structured approaches."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════
# EXPERIMENT RUNNER
# ═══════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(__file__).parent / "results"
RAW_DIR = OUTPUT_DIR / "raw"
MAX_RETRIES = 3
TIMEOUT = 300  # 5 minutes max per call


def preload_model(model: str):
    """Pre-load a model into Ollama's memory to avoid cold-start timeouts."""
    print(f"\n  >>> Pre-loading {model}...")
    try:
        result = subprocess.run(
            ["ollama", "run", model, "Say OK"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  >>> {model} loaded ✅")
            time.sleep(2)  # Let it settle
        else:
            print(f"  >>> {model} load warning: {result.stderr[:100]}")
    except Exception as e:
        print(f"  >>> {model} load error: {e}")


def call_ollama(model: str, system_prompt: str, user_prompt: str) -> dict:
    """Call ollama with retry logic."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500,
            "seed": 42,
        },
    }

    for attempt in range(1, MAX_RETRIES + 1):
        start_time = time.time()
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/chat",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=TIMEOUT
            )
            elapsed = time.time() - start_time

            if not result.stdout.strip():
                if attempt < MAX_RETRIES:
                    wait = 5 * attempt
                    print(f" [empty, retry {attempt}/{MAX_RETRIES} in {wait}s]", end="", flush=True)
                    time.sleep(wait)
                    continue
                return {"content": "", "elapsed_seconds": round(elapsed, 2), "tokens": 0,
                        "status": "error: empty response after retries"}

            response = json.loads(result.stdout)
            content = response.get("message", {}).get("content", "")

            if not content:
                if attempt < MAX_RETRIES:
                    wait = 5 * attempt
                    print(f" [no content, retry {attempt}/{MAX_RETRIES}]", end="", flush=True)
                    time.sleep(wait)
                    continue
                return {"content": "", "elapsed_seconds": round(elapsed, 2), "tokens": 0,
                        "status": "error: no content after retries"}

            return {
                "content": content,
                "elapsed_seconds": round(elapsed, 2),
                "tokens": len(content.split()),
                "status": "ok",
            }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            if attempt < MAX_RETRIES:
                print(f" [timeout, retry {attempt}/{MAX_RETRIES}]", end="", flush=True)
                time.sleep(5)
                continue
            return {"content": "", "elapsed_seconds": round(elapsed, 2), "tokens": 0,
                    "status": f"error: timeout after {MAX_RETRIES} attempts"}

        except json.JSONDecodeError as e:
            elapsed = time.time() - start_time
            if attempt < MAX_RETRIES:
                wait = 10 * attempt
                print(f" [JSON err, retry {attempt}/{MAX_RETRIES} in {wait}s]", end="", flush=True)
                time.sleep(wait)
                continue
            return {"content": "", "elapsed_seconds": round(elapsed, 2), "tokens": 0,
                    "status": f"error: JSON decode failed: {str(e)}"}

        except Exception as e:
            elapsed = time.time() - start_time
            return {"content": "", "elapsed_seconds": round(elapsed, 2), "tokens": 0,
                    "status": f"error: {str(e)}"}


def build_system_prompt(personality_key: str, variation_key: str) -> str:
    """Combine personality and variation into a system prompt."""
    p = PERSONALITIES[personality_key]["instruction"]
    v = VARIATIONS[variation_key]["instruction"]
    return f"{p}\n\n{v}\n\nProvide your response in 200-400 words. Be specific and substantive."


def is_valid_result(filepath: Path) -> bool:
    """Check if an existing result file has a valid (ok) response."""
    try:
        with open(filepath) as f:
            data = json.load(f)
        return data.get("status") == "ok" and bool(data.get("response", "").strip())
    except:
        return False


def run_experiment():
    """Run the full 144-combination factorial experiment, model by model."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    total = len(MODELS) * len(TASKS) * len(VARIATIONS) * len(PERSONALITIES)
    completed = 0
    ok_count = 0
    errors = 0
    skipped = 0

    print(f"\n{'='*70}")
    print(f"  G.E.A.R. EXPERIMENT v2: {total} total runs")
    print(f"  Models: {', '.join(MODELS)}")
    print(f"  Tasks: {', '.join(TASKS.keys())}")
    print(f"  Variations: {', '.join(VARIATIONS.keys())}")
    print(f"  Personalities: {', '.join(PERSONALITIES.keys())}")
    print(f"  Retries: {MAX_RETRIES} per call, Timeout: {TIMEOUT}s")
    print(f"{'='*70}")

    # Process model by model to avoid memory thrashing
    for model in MODELS:
        preload_model(model)

        for task_key, task in TASKS.items():
            for var_key, variation in VARIATIONS.items():
                for pers_key, personality in PERSONALITIES.items():
                    completed += 1
                    run_key = f"{model}__{task_key}__{var_key}__{pers_key}"
                    raw_file = RAW_DIR / f"{run_key}.json"

                    # Skip if already has valid result
                    if raw_file.exists() and is_valid_result(raw_file):
                        skipped += 1
                        ok_count += 1
                        print(f"  [{completed:3d}/{total}] {run_key[:60]:60s} SKIP (cached)")
                        continue

                    print(
                        f"  [{completed:3d}/{total}] "
                        f"{model:15s} | {task_key:20s} | "
                        f"{var_key:12s} | {pers_key:22s}",
                        end="", flush=True,
                    )

                    system_prompt = build_system_prompt(pers_key, var_key)
                    result = call_ollama(model, system_prompt, task["prompt"])

                    run_record = {
                        "run_key": run_key,
                        "model": model,
                        "task": task_key,
                        "task_label": task["label"],
                        "variation": var_key,
                        "variation_label": variation["label"],
                        "personality": pers_key,
                        "personality_label": personality["label"],
                        "system_prompt": system_prompt,
                        "user_prompt": task["prompt"],
                        "response": result["content"],
                        "elapsed_seconds": result["elapsed_seconds"],
                        "word_count": result["tokens"],
                        "status": result["status"],
                    }

                    with open(raw_file, "w") as f:
                        json.dump(run_record, f, indent=2)

                    if result["status"] == "ok":
                        print(f"  ✅ {result['tokens']:3d}w {result['elapsed_seconds']:5.1f}s")
                        ok_count += 1
                    else:
                        print(f"  ❌ {result['status'][:60]}")
                        errors += 1

    print(f"\n{'='*70}")
    print(f"  EXPERIMENT COMPLETE")
    print(f"  Total: {total} | OK: {ok_count} | Errors: {errors} | Cached: {skipped}")
    print(f"  Success rate: {ok_count/total*100:.1f}%")
    print(f"  Results: {OUTPUT_DIR}")
    print(f"{'='*70}\n")

    # Save manifest
    manifest = {
        "experiment": "GEAR Cognitive Variation Factorial v2",
        "completed": datetime.now().isoformat(),
        "total_runs": total,
        "ok": ok_count,
        "errors": errors,
        "cached": skipped,
        "models": MODELS,
    }
    with open(OUTPUT_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    run_experiment()

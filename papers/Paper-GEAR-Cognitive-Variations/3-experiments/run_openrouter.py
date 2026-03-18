#!/usr/bin/env python3
"""
G.E.A.R. Experiment: OpenRouter Premium Run
=============================================
Full factorial: 1 premium model × 3 tasks × 4 variations × 4 personalities = 48 runs
Uses Claude 3.5 Sonnet via OpenRouter for maximum quality.

Usage: python3 run_openrouter.py
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "z-ai/glm-5"  # Premium: ZhipuAI GLM-5

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
# RUNNER
# ═══════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(__file__).parent / "results"
RAW_DIR = OUTPUT_DIR / "raw"


def call_openrouter(system_prompt: str, user_prompt: str) -> dict:
    """Call OpenRouter API using urllib (no pip deps)."""
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 21000,
        "seed": 42,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://synthai.biz/",
        "X-Title": "GEAR Experiment",
    }

    start = time.time()
    try:
        req = urllib.request.Request(API_URL, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start

        msg = data.get("choices", [{}])[0].get("message", {})
        # Primary: content field. Fallback for reasoning models: reasoning field.
        content = msg.get("content") or ""
        if not content.strip():
            # Reasoning model: extract from reasoning or reasoning_details
            reasoning = msg.get("reasoning") or ""
            if not reasoning:
                details = msg.get("reasoning_details") or []
                reasoning = "\n".join(d.get("text", "") for d in details if d.get("text"))
            content = reasoning

        usage = data.get("usage", {})
        if content.strip():
            return {
                "content": content,
                "elapsed_seconds": round(elapsed, 2),
                "tokens": len(content.split()),
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "status": "ok",
            }
        else:
            return {
                "content": "", "elapsed_seconds": round(elapsed, 2),
                "tokens": 0, "status": "error: empty response (no content or reasoning)",
            }
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {
            "content": "", "elapsed_seconds": round(time.time() - start, 2),
            "tokens": 0, "status": f"error: HTTP {e.code}: {body[:200]}",
        }
    except Exception as e:
        return {
            "content": "", "elapsed_seconds": round(time.time() - start, 2),
            "tokens": 0, "status": f"error: {str(e)}",
        }


def build_system_prompt(personality_key: str, variation_key: str) -> str:
    p = PERSONALITIES[personality_key]["instruction"]
    v = VARIATIONS[variation_key]["instruction"]
    return f"{p}\n\n{v}\n\nProvide your response in 200-400 words. Be specific and substantive."


def is_valid_result(filepath: Path) -> bool:
    try:
        with open(filepath) as f:
            data = json.load(f)
        return data.get("status") == "ok" and bool(data.get("response", "").strip())
    except:
        return False


def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    model_tag = MODEL.replace("/", "_")
    total = len(TASKS) * len(VARIATIONS) * len(PERSONALITIES)
    completed = 0
    ok_count = 0
    errors = 0
    skipped = 0
    total_cost_tokens = 0

    print(f"\n{'='*70}")
    print(f"  G.E.A.R. EXPERIMENT: OpenRouter Premium")
    print(f"  Model: {MODEL}")
    print(f"  Runs: {total} (3 tasks × 4 variations × 4 personalities)")
    print(f"{'='*70}\n")

    for task_key, task in TASKS.items():
        for var_key, variation in VARIATIONS.items():
            for pers_key, personality in PERSONALITIES.items():
                completed += 1
                run_key = f"{model_tag}__{task_key}__{var_key}__{pers_key}"
                raw_file = RAW_DIR / f"{run_key}.json"

                if raw_file.exists() and is_valid_result(raw_file):
                    skipped += 1
                    ok_count += 1
                    print(f"  [{completed:2d}/{total}] SKIP (cached) {var_key:12s} | {pers_key}")
                    continue

                print(
                    f"  [{completed:2d}/{total}] {task_key:20s} | {var_key:12s} | {pers_key:22s}",
                    end="", flush=True,
                )

                system_prompt = build_system_prompt(pers_key, var_key)
                result = call_openrouter(system_prompt, task["prompt"])

                run_record = {
                    "run_key": run_key,
                    "model": MODEL,
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
                    "prompt_tokens": result.get("prompt_tokens", 0),
                    "completion_tokens": result.get("completion_tokens", 0),
                    "status": result["status"],
                }

                with open(raw_file, "w") as f:
                    json.dump(run_record, f, indent=2)

                if result["status"] == "ok":
                    total_cost_tokens += result.get("prompt_tokens", 0) + result.get("completion_tokens", 0)
                    print(f"  ✅ {result['tokens']:3d}w {result['elapsed_seconds']:4.1f}s")
                    ok_count += 1
                else:
                    print(f"  ❌ {result['status'][:60]}")
                    errors += 1

                # Rate limit: 1s between calls
                time.sleep(1)

    print(f"\n{'='*70}")
    print(f"  COMPLETE: {ok_count}/{total} OK | {errors} errors | {skipped} cached")
    print(f"  Total tokens: ~{total_cost_tokens:,}")
    print(f"  Results: {RAW_DIR}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    run()

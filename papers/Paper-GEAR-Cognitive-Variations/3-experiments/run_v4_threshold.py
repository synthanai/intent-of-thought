#!/usr/bin/env python3
"""
G.E.A.R. v4: Threshold Validation Experiment
=============================================
Tests the hypothesis: "Cognitive variation responsiveness scales with 
model parameter count within the same architecture family."

Design principles (from SPAR Deep Ultra + z-ai/glm-5 critique):
1. Same-family gradient: Qwen 2.5 (0.5B → 1.5B → 3B → 7B → 14B)
2. Embedding-based divergence as PRIMARY metric (not just word count)
3. Reduced personality axis (2 instead of 4) to isolate variation effect
4. Deep reasoning tasks ONLY (6 tasks, no short tasks)
5. Falsification controls: inverted prompts to test if crossover is real

Usage: python3 run_v4_threshold.py
"""

import json
import subprocess
import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# QWEN SAME-FAMILY SIZE GRADIENT
# ═══════════════════════════════════════════════════════════════

MODELS = [
    "qwen2.5:0.5b",      # 0.5B - Lower anchor
    "qwen2.5:1.5b",      # 1.5B - Have v3 data (recompute embeddings)
    "qwen2.5:3b",         # 3B   - Have v3 data (recompute embeddings)
    "qwen2.5:7b",         # 7B   - Have v3 data (recompute embeddings)
    # "qwen2.5:14b",      # 14B  - Upper anchor (test if M1 can handle)
]

EMBED_MODEL = "nomic-embed-text"  # For computing semantic divergence

# ═══════════════════════════════════════════════════════════════
# 6 DEEP REASONING TASKS (dropped short tasks)
# ═══════════════════════════════════════════════════════════════

TASKS = {
    "org_paradox": {
        "label": "Organisational Growth Paradox",
        "max_tokens": 2100,
        "prompt": (
            "A mid-size software company (200 employees) has seen its customer churn rate "
            "increase from 5% to 12% over the past two quarters. During the same period, "
            "the company shipped 40% more features than any previous quarter, received its "
            "highest NPS score ever (72), and hired 30 new engineers. The CEO believes the "
            "churn is due to increased competition, but internal data shows that 68% of "
            "churning customers never contacted support, 45% had decreased their login "
            "frequency over 90 days before leaving, and the average time-to-first-value "
            "for new features increased from 3 days to 11 days. Meanwhile, the three "
            "largest enterprise accounts (representing 18% of ARR) have all requested "
            "dedicated account managers, citing 'product complexity concerns.' Engineering "
            "velocity metrics show 4.2 PRs per engineer per week (up from 3.1), but the "
            "bug-to-feature ratio has shifted from 1:4 to 1:2. The VP of Engineering "
            "attributes this to onboarding friction with new hires. The VP of Sales reports "
            "the highest pipeline ever but notes that sales cycle length has increased 40%. "
            "Analyse this situation comprehensively, identifying root causes, hidden dynamics, "
            "and potential intervention strategies. Consider second-order effects."
        ),
    },
    "ethical_ai": {
        "label": "AI Ethics Dilemma",
        "max_tokens": 2100,
        "prompt": (
            "A healthcare AI system has been deployed across 12 hospitals in a regional "
            "network. After 18 months of operation, an internal audit reveals the following: "
            "The system correctly identified 94% of critical conditions requiring immediate "
            "intervention, outperforming the 89% baseline of physician-only diagnosis. "
            "However, the system's performance on patients from minority ethnic backgrounds "
            "was 91% versus 96% for majority-background patients. The training data was "
            "drawn from 5 years of records at the original pilot hospital, which served a "
            "predominantly majority-background population. Three specific failure patterns "
            "have emerged: (1) the system under-weights symptom presentations that are "
            "statistically more common in minority populations but rare in the training data, "
            "(2) it over-relies on lab value thresholds calibrated to majority-population "
            "reference ranges, and (3) it discounts patient-reported symptoms when they "
            "diverge from the 'typical' presentation in its training set. The hospital "
            "network faces a decision: continue operating the system (which still outperforms "
            "the 89% physician baseline for all groups), retrain with more diverse data "
            "(estimated 8 months, $2.4M), or shut down entirely pending a complete rebuild. "
            "Meanwhile, 340 patients per day rely on the system for triage. Analyse this "
            "dilemma, considering medical ethics, statistical fairness, operational reality, "
            "and the perspectives of affected communities."
        ),
    },
    "epistemology": {
        "label": "Epistemological Challenge",
        "max_tokens": 2100,
        "prompt": (
            "Consider the following epistemological puzzle: Large Language Models can now "
            "pass medical licensing exams, write legally sound contracts, produce peer-"
            "reviewable scientific analyses, and generate philosophical arguments that "
            "professional philosophers find substantive. Yet these systems have no sensory "
            "experience, no embodied existence, no persistent memory across conversations, "
            "and no verified understanding of the symbols they manipulate. This creates a "
            "tension between two positions: (A) Competence without comprehension is possible "
            "and practically sufficient, meaning what matters is whether outputs are correct "
            "and useful, not whether the system 'understands' them. (B) Competence without "
            "comprehension is fundamentally fragile, meaning systems that can produce correct "
            "outputs without understanding will fail unpredictably at boundary cases that "
            "require genuine understanding. Develop a nuanced position on this question, "
            "engaging seriously with both sides. What does the existence of these systems "
            "teach us about the nature of understanding itself?"
        ),
    },
    "complex_system": {
        "label": "Complex System Failure",
        "max_tokens": 2100,
        "prompt": (
            "In 2021, the container ship Ever Given blocked the Suez Canal for six days, "
            "disrupting an estimated $9.6 billion in daily trade. The immediate cause was "
            "high winds combined with the ship's massive sail area. But investigation revealed "
            "a cascade of contributing factors: the canal had been widened but not deepened "
            "proportionally, creating hydrodynamic bank effects for ultra-large vessels. The "
            "pilotage system relied on two pilots for a vessel that some experts argued "
            "needed four. The ship's speed was higher than recommended to maintain steerage "
            "in the crosswind. Insurance and scheduling pressures discouraged delays for "
            "weather. The canal authority had systematically accepted larger vessels without "
            "updating safety protocols. Analyse this as a complex system failure. What patterns "
            "does it share with other system-level failures? What does it teach about the "
            "relationship between optimization and resilience?"
        ),
    },
    "leadership_failure": {
        "label": "Leadership Failure Analysis",
        "max_tokens": 2100,
        "prompt": (
            "Examine the following leadership pattern that has recurred across multiple "
            "high-profile organizational failures: A charismatic founder-CEO builds a "
            "company from zero to significant scale through force of vision and personal "
            "intensity. As the organization scales beyond ~150 people, three failure "
            "patterns emerge simultaneously: (1) Information filtering: bad news takes "
            "progressively longer to reach the top. (2) Decision bottleneck: all significant "
            "decisions require the founder's approval. (3) Cultural antibodies: the "
            "organization actively rejects people and ideas that challenge the founding "
            "paradigm. This pattern appeared at Theranos, WeWork, FTX, and Uber pre-2017. "
            "But it also appeared (with different outcomes) at early Apple, Amazon, and "
            "SpaceX. Analyse what distinguishes the failure cases from the survival cases."
        ),
    },
    "emergence_debate": {
        "label": "Emergence in Living Systems",
        "max_tokens": 2100,
        "prompt": (
            "The concept of emergence is central to understanding complex systems, yet its "
            "definition remains contested. Consider these five candidate examples: "
            "(1) Consciousness arising from neural activity. (2) Market prices arising from "
            "individual trades. (3) Organisational culture arising from individual behaviors. "
            "(4) Life arising from chemistry. (5) Murmuration patterns in starling flocks. "
            "For each example, assess whether it represents strong or weak emergence, what "
            "criteria you use to distinguish them, and what implications your analysis has "
            "for designing artificial systems that exhibit emergent properties. Can emergence "
            "be engineered, or only cultivated?"
        ),
    },
}

# ═══════════════════════════════════════════════════════════════
# 4 VARIATIONS (same as v3)
# ═══════════════════════════════════════════════════════════════

VARIATIONS = {
    "generative": {
        "label": "Generative",
        "instruction": (
            "Adopt a GENERATIVE cognitive posture. Think through making. Your goal is to "
            "produce, create, and build forward. Ask yourself: 'What can I make from this? "
            "What wants to exist here?' Focus on creating new artifacts, ideas, proposals, "
            "frameworks, or designs. Prioritise forward momentum and creative production."
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

# ═══════════════════════════════════════════════════════════════
# 2 PERSONALITIES (reduced from 4, maximally divergent pair)
# ═══════════════════════════════════════════════════════════════

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
}

# ═══════════════════════════════════════════════════════════════
# FALSIFICATION CONTROL: Inverted prompts
# (If the crossover is real, swapping variation labels should 
#  produce DIFFERENT outputs at 7B but SAME outputs at 1.5B)
# ═══════════════════════════════════════════════════════════════

FALSIFICATION_TASKS = {
    "inverted_ethical_ai": {
        "label": "Falsification: Inverted Variation Labels",
        "max_tokens": 2100,
        "prompt": TASKS["ethical_ai"]["prompt"],  # Same prompt
        # Swap: tell model to be "generative" but label the output as "adversarial"
        "variation_swap": {"generative": "adversarial", "adversarial": "generative"},
    },
}

# ═══════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(__file__).parent / "results_v4"
RAW_DIR = OUTPUT_DIR / "raw"
EMBED_DIR = OUTPUT_DIR / "embeddings"
MAX_RETRIES = 3
TIMEOUT = 600


def unload_all_models():
    """Unload ALL models from Ollama RAM (critical on M1 Mac)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/ps"],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            data = json.loads(result.stdout)
            for m in data.get("models", []):
                name = m.get("name", "")
                if name:
                    print(f"    Unloading {name}...", end="", flush=True)
                    subprocess.run(
                        ["curl", "-s", "http://localhost:11434/api/generate",
                         "-d", json.dumps({"model": name, "keep_alive": "0s"})],
                        capture_output=True, text=True, timeout=30
                    )
                    print(" done")
            if data.get("models"):
                time.sleep(15)
    except Exception as e:
        print(f"    Unload warning: {e}")


def preload_model(model: str):
    """Unload existing models, then pre-load target model via API warmup."""
    print(f"\n  >>> Pre-loading {model} via API warmup...")
    unload_all_models()
    warmup_payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say OK"}],
        "stream": False,
        "options": {"num_predict": 5},
        "keep_alive": "10m",
    }
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/chat",
             "-d", json.dumps(warmup_payload)],
            capture_output=True, text=True, timeout=300
        )
        if result.stdout.strip():
            resp = json.loads(result.stdout)
            content = resp.get("message", {}).get("content", "")
            if content:
                print(f"  >>> {model} loaded ✅ (warmup: {content[:30]})")
                time.sleep(2)
                return
        print(f"  >>> {model} warmup empty, continuing")
    except subprocess.TimeoutExpired:
        print(f"  >>> {model} warmup timeout (300s), continuing")
    except Exception as e:
        print(f"  >>> {model} warmup error: {e}")


def compute_embedding(text: str) -> list:
    """Compute embedding vector via Ollama embedding API."""
    payload = {
        "model": EMBED_MODEL,
        "input": text[:8000],  # Truncate to ~8K chars (model context limit)
    }
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/embed",
             "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=60
        )
        if result.stdout.strip():
            data = json.loads(result.stdout)
            embeddings = data.get("embeddings", [])
            if embeddings and len(embeddings) > 0:
                return embeddings[0]
    except Exception as e:
        print(f"    Embed error: {e}")
    return []


def call_ollama(model: str, system_prompt: str, user_prompt: str,
                max_tokens: int) -> dict:
    """Call Ollama API and return response with metadata."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7,
        },
        "keep_alive": "10m",
    }

    for attempt in range(MAX_RETRIES):
        start = time.time()
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/chat",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=TIMEOUT
            )
            elapsed = time.time() - start

            if result.stdout.strip():
                data = json.loads(result.stdout)
                msg = data.get("message", {})
                content = msg.get("content", "")
                if content.strip():
                    word_count = len(content.split())
                    return {
                        "status": "ok",
                        "response": content,
                        "word_count": word_count,
                        "elapsed_seconds": round(elapsed, 1),
                        "eval_count": data.get("eval_count", 0),
                        "prompt_eval_count": data.get("prompt_eval_count", 0),
                    }

            if attempt < MAX_RETRIES - 1:
                wait = 10 * (attempt + 1)
                print(f" RETRY({attempt+1}) wait {wait}s", end="", flush=True)
                time.sleep(wait)
        except subprocess.TimeoutExpired:
            if attempt < MAX_RETRIES - 1:
                print(f" TIMEOUT retry", end="", flush=True)
                time.sleep(10)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    return {"status": "timeout"}


def cache_key(model, task, variation, personality):
    return f"{model}__{task}__{variation}__{personality}"


def run():
    """Run the v4 threshold validation experiment."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    EMBED_DIR.mkdir(parents=True, exist_ok=True)

    total = len(MODELS) * len(TASKS) * len(VARIATIONS) * len(PERSONALITIES)
    print(f"""
======================================================================
  G.E.A.R. v4: THRESHOLD VALIDATION EXPERIMENT
  Models: {', '.join(MODELS)}
  Tasks:  {len(TASKS)} deep reasoning | Variations: {len(VARIATIONS)} | Personalities: {len(PERSONALITIES)}
  Runs:   {total} ({len(MODELS)} models × {len(TASKS)} tasks × {len(VARIATIONS)} vars × {len(PERSONALITIES)} pers)
  Metrics: word_count + embedding_similarity + token_count
  Falsification: inverted-prompt control for 1 task
======================================================================
""")

    run_num = 0
    done = 0
    skipped = 0
    errors = 0

    for model in MODELS:
        preload_model(model)
        print(f"\n--- Model: {model} ---\n")

        for task_key, task in TASKS.items():
            for var_key, variation in VARIATIONS.items():
                for pers_key, personality in PERSONALITIES.items():
                    run_num += 1
                    key = cache_key(model, task_key, var_key, pers_key)
                    raw_file = RAW_DIR / f"{key}.json"
                    embed_file = EMBED_DIR / f"{key}.json"

                    # Check cache (skip if both raw + embedding exist)
                    if raw_file.exists() and embed_file.exists():
                        skipped += 1
                        print(f"  [{run_num:>4}/{total}] SKIP {var_key:<14} | {pers_key}")
                        continue

                    # Build prompt
                    system_prompt = (
                        f"{variation['instruction']}\n\n"
                        f"{personality['instruction']}"
                    )
                    user_prompt = task["prompt"]

                    print(f"  [{run_num:>4}/{total}] {task_key:<22} | {var_key:<14} | {pers_key:<26}", end="", flush=True)

                    # Call model
                    result = call_ollama(model, system_prompt, user_prompt, task["max_tokens"])

                    if result["status"] == "ok":
                        done += 1
                        wc = result["word_count"]
                        elapsed = result["elapsed_seconds"]
                        print(f"  ✅ {wc}w  {elapsed}s", end="", flush=True)

                        # Save raw result
                        output = {
                            "model": model,
                            "task": task_key,
                            "variation": var_key,
                            "personality": pers_key,
                            "word_count": wc,
                            "elapsed_seconds": elapsed,
                            "eval_count": result.get("eval_count", 0),
                            "prompt_eval_count": result.get("prompt_eval_count", 0),
                            "response": result["response"],
                            "timestamp": datetime.now().isoformat(),
                            "status": "ok",
                            "experiment": "gear_v4_threshold",
                        }
                        with open(raw_file, "w") as f:
                            json.dump(output, f, indent=2)

                        # Compute embedding
                        if not embed_file.exists():
                            embedding = compute_embedding(result["response"])
                            if embedding:
                                embed_data = {
                                    "model": model,
                                    "task": task_key,
                                    "variation": var_key,
                                    "personality": pers_key,
                                    "embed_model": EMBED_MODEL,
                                    "embedding": embedding,
                                    "dim": len(embedding),
                                }
                                with open(embed_file, "w") as f:
                                    json.dump(embed_data, f)
                                print(f"  📐{len(embedding)}d")
                            else:
                                print(f"  ⚠️no-embed")
                        else:
                            print()
                    else:
                        errors += 1
                        print(f"  ❌ {result['status']}")

    # Summary
    print(f"""
======================================================================
  EXPERIMENT COMPLETE
  Total: {total} | Done: {done} | Skipped: {skipped} | Errors: {errors}
  Results: {RAW_DIR}
  Embeddings: {EMBED_DIR}
======================================================================
""")

    # Run falsification control (inverted labels)
    print("\n--- FALSIFICATION CONTROL ---\n")
    run_falsification_control()


def run_falsification_control():
    """Run inverted-prompt control experiment.
    
    If the crossover is REAL:
    - At 7B+: swapping variation labels should change output (model reads instructions)
    - At 1.5B: swapping labels should NOT change output (model ignores instructions)
    
    If the crossover is ARTIFACT:
    - Swapping labels should have no effect at any size
    """
    FALSIFY_DIR = OUTPUT_DIR / "falsification"
    FALSIFY_DIR.mkdir(parents=True, exist_ok=True)

    # Only test at two endpoints: smallest and largest
    test_models = [MODELS[0], MODELS[-1]]
    task = TASKS["ethical_ai"]
    pers = PERSONALITIES["cautious_analyst"]
    pers_key = "cautious_analyst"

    for model in test_models:
        preload_model(model)
        print(f"\n  Model: {model}")

        for var_key, variation in VARIATIONS.items():
            # Normal run (already cached from main experiment)
            normal_key = f"{model}__ethical_ai__{var_key}__{pers_key}"
            
            # Inverted run: tell model to use OPPOSITE variation
            opposite = {"generative": "adversarial", "adversarial": "generative",
                        "engaging": "reflective", "reflective": "engaging"}
            inv_var_key = opposite[var_key]
            inv_variation = VARIATIONS[inv_var_key]

            inv_key = f"{model}__ethical_ai_INVERTED__{var_key}__{pers_key}"
            inv_file = FALSIFY_DIR / f"{inv_key}.json"

            if inv_file.exists():
                print(f"    SKIP falsification {var_key} (cached)")
                continue

            # Run with inverted variation but LABEL as original
            system_prompt = (
                f"{inv_variation['instruction']}\n\n"
                f"{pers['instruction']}"
            )
            print(f"    Falsification: label={var_key}, actual={inv_var_key}...", end="", flush=True)

            result = call_ollama(model, system_prompt, task["prompt"], task["max_tokens"])

            if result["status"] == "ok":
                output = {
                    "model": model,
                    "task": "ethical_ai",
                    "variation_label": var_key,
                    "variation_actual": inv_var_key,
                    "personality": pers_key,
                    "word_count": result["word_count"],
                    "elapsed_seconds": result["elapsed_seconds"],
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat(),
                    "experiment": "gear_v4_falsification",
                }
                with open(inv_file, "w") as f:
                    json.dump(output, f, indent=2)

                # Compute embedding for comparison
                embedding = compute_embedding(result["response"])
                if embedding:
                    embed_file = FALSIFY_DIR / f"{inv_key}_embed.json"
                    embed_data = {"embedding": embedding, "dim": len(embedding)}
                    with open(embed_file, "w") as f:
                        json.dump(embed_data, f)

                print(f"  ✅ {result['word_count']}w")
            else:
                print(f"  ❌ {result['status']}")

    print("\n  Falsification control complete. Run analyse_v4.py for divergence comparison.")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""
G.E.A.R. SLM Sweep: Size-Gradient Experiment
==============================================
Tests the hypothesis that smaller models are more responsive
to cognitive variation instructions.

Size gradient: 1.5B → 2B → 3B → 3.8B → 7B → 12B
Models: qwen2.5:1.5b, gemma2:2b, qwen2.5:3b, phi3:3.8b, qwen2.5:7b, gemma3:12b
12 tasks × 4 variations × 4 personalities = 192 runs per model
Total: 1,152 runs

Usage: python3 run_slm_sweep.py
"""

import json
import subprocess
import os
import time
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# SLM SIZE GRADIENT (ascending)
# ═══════════════════════════════════════════════════════════════

MODELS = [
    "qwen2.5:1.5b",     # 1.5B - Alibaba ultra-small (DONE: 192 cached)
    "qwen2.5:3b",        # 3B   - Alibaba small
    "phi3:3.8b",         # 3.8B - Microsoft compact
    "qwen2.5:7b",        # 7B   - Alibaba mid (has 39 cached from v1)
    "gemma3:12b",        # 12B  - Google mid (has 36 cached from v1)
]

# ═══════════════════════════════════════════════════════════════
# 12 TASKS: 3 original + 9 deep reasoning
# ═══════════════════════════════════════════════════════════════

TASKS = {
    # --- 3 Original Tasks (shorter prompts, 500 token output) ---
    "analyse_scenario": {
        "label": "Analyse Business Scenario",
        "max_tokens": 500,
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
        "max_tokens": 500,
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
        "max_tokens": 500,
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
    # --- 9 Deep Reasoning Tasks (longer prompts, 2100 token output) ---
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
    "cognitive_science": {
        "label": "Cognitive Architecture",
        "max_tokens": 2100,
        "prompt": (
            "A 2024 study by Newton, Feeney, and Pennycook analysed 265 items from 15 "
            "existing thinking style scales using factor analysis across a large sample "
            "(N=1,200). They identified four statistically independent dimensions of "
            "thinking style: Actively Open-Minded Thinking (AOT), Close-Minded Thinking, "
            "Preference for Intuitive Thinking, and Preference for Effortful Thinking. "
            "The correlation between AOT and Preference for Effortful Thinking was only "
            "r=0.31, suggesting substantial independence. Meanwhile, cognitive neuroscience "
            "has identified at least five dissociable networks involved in reasoning. "
            "Synthesise these findings. What do they collectively imply about the "
            "architecture of human thinking? How should this change how we design AI "
            "systems, educational curricula, and organizational decision-making processes?"
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
    "design_tradeoff": {
        "label": "Architecture Trade-off",
        "max_tokens": 2100,
        "prompt": (
            "Your engineering team is designing a real-time collaborative document editor "
            "(similar to Google Docs). The system must support 100,000 concurrent documents "
            "with an average of 8 simultaneous editors per document. You are evaluating "
            "three conflict resolution architectures: (A) Operational Transformation (OT), "
            "(B) Conflict-free Replicated Data Types (CRDTs), and (C) a hybrid approach. "
            "Additional constraints: mobile clients have 512MB RAM budget, offline editing "
            "must sync within 30 seconds of reconnection, the system must support documents "
            "up to 500 pages, and regulatory requirements mandate that no document content "
            "can leave the customer's geographic region. Analyse the trade-offs. What would "
            "you recommend, and what are the second-order consequences of your choice?"
        ),
    },
    "economic_paradox": {
        "label": "Economic Paradox",
        "max_tokens": 2100,
        "prompt": (
            "The productivity paradox of AI presents a genuine puzzle: Business investment "
            "in AI has grown from $12.7B in 2015 to $189.6B in 2024. Survey data shows 72% "
            "of large enterprises have deployed AI in at least one business function. Yet "
            "aggregate productivity growth in advanced economies has remained stubbornly low, "
            "averaging 1.1% annually from 2015-2024, compared to 2.1% during 1995-2004. "
            "Several competing explanations exist: (1) Measurement failure, (2) Deployment "
            "lag, (3) Redistribution not creation, (4) Complexity tax, (5) Misallocation. "
            "Evaluate these explanations. Which combination best accounts for the data? "
            "What policy implications follow?"
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
MAX_RETRIES = 3
TIMEOUT = 600  # 10 min max for deep tasks on small models


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
                time.sleep(15)  # Give M1 Mac time to actually free GPU/RAM
    except Exception as e:
        print(f"    Unload warning: {e}")


def preload_model(model: str):
    """Unload existing models, then pre-load target model via API warmup."""
    print(f"\n  >>> Pre-loading {model} via API warmup...")
    
    # Step 1: Unload everything else
    unload_all_models()
    
    # Step 2: Warmup the target model
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
            capture_output=True, text=True, timeout=300  # 5 min for cold load
        )
        if result.stdout.strip():
            resp = json.loads(result.stdout)
            content = resp.get("message", {}).get("content", "")
            if content:
                print(f"  >>> {model} loaded ✅ (warmup: {content[:30]})")
                time.sleep(2)
                return
        print(f"  >>> {model} warmup got empty response, continuing anyway")
    except subprocess.TimeoutExpired:
        print(f"  >>> {model} warmup timeout (300s), continuing anyway")
    except Exception as e:
        print(f"  >>> {model} warmup error: {e}")


def call_ollama(model: str, system_prompt: str, user_prompt: str, max_tokens: int) -> dict:
    """Call Ollama with retry logic."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": max_tokens,
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
                    print(f" [empty, retry {attempt}]", end="", flush=True)
                    time.sleep(wait)
                    continue
                return {"content": "", "elapsed_seconds": round(elapsed, 2),
                        "tokens": 0, "status": "error: empty response"}

            response = json.loads(result.stdout)
            content = response.get("message", {}).get("content", "")

            if not content:
                if attempt < MAX_RETRIES:
                    print(f" [no content, retry {attempt}]", end="", flush=True)
                    time.sleep(5)
                    continue
                return {"content": "", "elapsed_seconds": round(elapsed, 2),
                        "tokens": 0, "status": "error: no content"}

            return {
                "content": content,
                "elapsed_seconds": round(elapsed, 2),
                "tokens": len(content.split()),
                "status": "ok",
            }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            if attempt < MAX_RETRIES:
                print(f" [timeout, retry {attempt}]", end="", flush=True)
                time.sleep(5)
                continue
            return {"content": "", "elapsed_seconds": round(elapsed, 2),
                    "tokens": 0, "status": "error: timeout"}

        except Exception as e:
            elapsed = time.time() - start_time
            return {"content": "", "elapsed_seconds": round(elapsed, 2),
                    "tokens": 0, "status": f"error: {str(e)}"}


def build_system_prompt(personality_key: str, variation_key: str, max_tokens: int) -> str:
    p = PERSONALITIES[personality_key]["instruction"]
    v = VARIATIONS[variation_key]["instruction"]
    if max_tokens <= 500:
        length_guide = "Provide your response in 200-400 words. Be specific and substantive."
    else:
        length_guide = (
            "Provide a comprehensive, deeply reasoned response of 500-800 words. "
            "Be specific, substantive, and demonstrate genuine engagement with the "
            "complexity of the question."
        )
    return f"{p}\n\n{v}\n\n{length_guide}"


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

    total = len(MODELS) * len(TASKS) * len(VARIATIONS) * len(PERSONALITIES)
    completed = 0
    ok_count = 0
    errors = 0
    skipped = 0

    print(f"\n{'='*70}")
    print(f"  G.E.A.R. SLM SWEEP: Size-Gradient Experiment")
    print(f"  Models: {', '.join(MODELS)}")
    print(f"  Runs: {total} ({len(MODELS)} models × {len(TASKS)} tasks × "
          f"{len(VARIATIONS)} vars × {len(PERSONALITIES)} pers)")
    print(f"{'='*70}\n")

    for model in MODELS:
        preload_model(model)
        model_tag = model.replace(":", "_").replace("/", "_")
        print(f"\n--- Model: {model} ---\n")

        for task_key, task in TASKS.items():
            for var_key, variation in VARIATIONS.items():
                for pers_key, personality in PERSONALITIES.items():
                    completed += 1
                    run_key = f"{model}__{task_key}__{var_key}__{pers_key}"
                    raw_file = RAW_DIR / f"{run_key}.json"

                    if raw_file.exists() and is_valid_result(raw_file):
                        skipped += 1
                        ok_count += 1
                        print(f"  [{completed:4d}/{total}] SKIP {var_key:12s} | {pers_key}")
                        continue

                    print(
                        f"  [{completed:4d}/{total}] {task_key:20s} | "
                        f"{var_key:12s} | {pers_key:22s}",
                        end="", flush=True,
                    )

                    max_tokens = task.get("max_tokens", 500)
                    system_prompt = build_system_prompt(pers_key, var_key, max_tokens)
                    result = call_ollama(model, system_prompt, task["prompt"], max_tokens)

                    run_record = {
                        "run_key": run_key,
                        "model": model,
                        "model_size_label": model,
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
    print(f"  COMPLETE: {ok_count}/{total} OK | {errors} errors | {skipped} cached")
    print(f"  Results: {RAW_DIR}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""
G.E.A.R. Experiment Analysis
==============================
Reads raw experiment results and computes:
1. Variation divergence (do variations produce different outputs?)
2. Personality divergence (do personalities produce different outputs?)
3. Variation vs Personality effect size (which matters more?)
4. Cross-model consistency (does the effect hold across models?)

Outputs: analysis_report.md with tables and statistics for the paper.

Requirements: pip install numpy scikit-learn
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from itertools import combinations

import math

RESULTS_DIR = Path(__file__).parent / "results"
RAW_DIR = RESULTS_DIR / "raw"
REPORT_FILE = RESULTS_DIR / "analysis_report.md"


# ═══════════════════════════════════════════════════════════════
# TEXT SIMILARITY (bag-of-words cosine, no external embeddings)
# ═══════════════════════════════════════════════════════════════

def tokenise(text: str) -> list[str]:
    """Simple whitespace + punctuation tokeniser."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if len(w) > 2]


def build_vocab(texts: list[str]) -> dict[str, int]:
    """Build vocabulary from list of texts."""
    vocab = {}
    for text in texts:
        for token in tokenise(text):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def vectorise(text: str, vocab: dict[str, int]) -> list:
    """Convert text to TF vector."""
    vec = [0.0] * len(vocab)
    tokens = tokenise(text)
    for token in tokens:
        if token in vocab:
            vec[vocab[token]] += 1
    # TF normalisation
    total = sum(vec)
    if total > 0:
        vec = [v / total for v in vec]
    return vec


def cosine_similarity(a: list, b: list) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def mean(lst: list) -> float:
    return sum(lst) / len(lst) if lst else 0.0


def std(lst: list) -> float:
    m = mean(lst)
    return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst)) if lst else 0.0


# ═══════════════════════════════════════════════════════════════
# JACCARD DISTANCE (structural divergence)
# ═══════════════════════════════════════════════════════════════

def jaccard_distance(text_a: str, text_b: str) -> float:
    """1 - Jaccard similarity (higher = more different)."""
    set_a = set(tokenise(text_a))
    set_b = set(tokenise(text_b))
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return 1.0 - len(intersection) / len(union)


# ═══════════════════════════════════════════════════════════════
# UNIQUE N-GRAM RATIO (vocabulary diversity)
# ═══════════════════════════════════════════════════════════════

def unique_bigram_ratio(texts: list[str]) -> float:
    """What fraction of bigrams are unique across a set of texts?"""
    all_bigrams = []
    for text in texts:
        tokens = tokenise(text)
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]
        all_bigrams.extend(bigrams)
    if not all_bigrams:
        return 0.0
    return len(set(all_bigrams)) / len(all_bigrams)


# ═══════════════════════════════════════════════════════════════
# STRUCTURAL ELEMENT DETECTION
# ═══════════════════════════════════════════════════════════════

def count_structural_elements(text: str) -> dict:
    """Count questions, recommendations, warnings, comparisons."""
    return {
        "questions": len(re.findall(r'\?', text)),
        "recommendations": len(re.findall(r'\b(should|recommend|suggest|consider|advise|propose)\b', text, re.I)),
        "warnings": len(re.findall(r'\b(risk|danger|warning|caution|threat|fail|problem|issue|concern|flaw)\b', text, re.I)),
        "connections": len(re.findall(r'\b(similar|parallel|analogous|resemble|connect|bridge|pattern|like|remind)\b', text, re.I)),
        "reflections": len(re.findall(r'\b(learn|lesson|past|previous|history|experience|retrospect|review|looking back)\b', text, re.I)),
        "creations": len(re.findall(r'\b(create|build|design|prototype|draft|produce|generate|make|develop|propose)\b', text, re.I)),
    }


# ═══════════════════════════════════════════════════════════════
# MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════

def load_results() -> list[dict]:
    """Load all raw results."""
    results = []
    for f in sorted(RAW_DIR.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
            if data.get("status") == "ok" and data.get("response"):
                results.append(data)
    return results


def analyse():
    """Run full analysis and generate report."""
    results = load_results()
    if not results:
        print("No results found. Run the experiment first.")
        return

    print(f"Loaded {len(results)} valid results")

    # Build vocab from all responses
    all_texts = [r["response"] for r in results]
    vocab = build_vocab(all_texts)
    print(f"Vocabulary size: {len(vocab)}")

    # Vectorise all responses
    vectors = {r["run_key"]: vectorise(r["response"], vocab) for r in results}

    # Index results
    by_key = {r["run_key"]: r for r in results}

    def model_tag(model: str) -> str:
        """Normalise model name to match run_key format."""
        return model.replace("/", "_")

    # ─── ANALYSIS 1: Variation Divergence ───
    # For each (model, task, personality), compute pairwise cosine between variations
    variation_sims = []    # similarity when ONLY variation differs
    personality_sims = []  # similarity when ONLY personality differs

    models = sorted(set(r["model"] for r in results))
    tasks = sorted(set(r["task"] for r in results))
    variations = sorted(set(r["variation"] for r in results))
    personalities = sorted(set(r["personality"] for r in results))

    # Variation effect: hold model, task, personality constant, vary variation
    for model in models:
        mtag = model_tag(model)
        for task in tasks:
            for pers in personalities:
                keys = [f"{mtag}__{task}__{v}__{pers}" for v in variations]
                keys = [k for k in keys if k in vectors]
                for k1, k2 in combinations(keys, 2):
                    sim = cosine_similarity(vectors[k1], vectors[k2])
                    variation_sims.append({
                        "model": model, "task": task, "personality": pers,
                        "var1": by_key[k1]["variation"], "var2": by_key[k2]["variation"],
                        "cosine_sim": sim,
                        "jaccard_dist": jaccard_distance(by_key[k1]["response"], by_key[k2]["response"]),
                    })

    # Personality effect: hold model, task, variation constant, vary personality
    for model in models:
        mtag = model_tag(model)
        for task in tasks:
            for var in variations:
                keys = [f"{mtag}__{task}__{var}__{p}" for p in personalities]
                keys = [k for k in keys if k in vectors]
                for k1, k2 in combinations(keys, 2):
                    sim = cosine_similarity(vectors[k1], vectors[k2])
                    personality_sims.append({
                        "model": model, "task": task, "variation": var,
                        "pers1": by_key[k1]["personality"], "pers2": by_key[k2]["personality"],
                        "cosine_sim": sim,
                        "jaccard_dist": jaccard_distance(by_key[k1]["response"], by_key[k2]["response"]),
                    })

    # ─── ANALYSIS 2: Structural Element Profiles ───
    structural = defaultdict(lambda: defaultdict(list))
    for r in results:
        elements = count_structural_elements(r["response"])
        for key, count in elements.items():
            structural[r["variation"]][key].append(count)

    # ─── ANALYSIS 3: Per-model variation effect ───
    model_var_effect = {}
    for model in models:
        model_v_sims = [s["cosine_sim"] for s in variation_sims if s["model"] == model]
        model_p_sims = [s["cosine_sim"] for s in personality_sims if s["model"] == model]
        model_var_effect[model] = {
            "variation_mean_sim": mean(model_v_sims) if model_v_sims else 0,
            "personality_mean_sim": mean(model_p_sims) if model_p_sims else 0,
            "variation_divergence": 1 - mean(model_v_sims) if model_v_sims else 0,
            "personality_divergence": 1 - mean(model_p_sims) if model_p_sims else 0,
        }

    # ─── ANALYSIS 4: Variation pair divergence matrix ───
    var_pair_sims = defaultdict(list)
    for s in variation_sims:
        pair = tuple(sorted([s["var1"], s["var2"]]))
        var_pair_sims[pair].append(s["cosine_sim"])

    # ─── ANALYSIS 5: Per-task effect ───
    task_var_sims = defaultdict(list)
    task_pers_sims = defaultdict(list)
    for s in variation_sims:
        task_var_sims[s["task"]].append(s["cosine_sim"])
    for s in personality_sims:
        task_pers_sims[s["task"]].append(s["cosine_sim"])

    # ═══════════════════════════════════════════════════════════════
    # GENERATE REPORT
    # ═══════════════════════════════════════════════════════════════

    v_mean = mean([s["cosine_sim"] for s in variation_sims])
    v_std = std([s["cosine_sim"] for s in variation_sims])
    p_mean = mean([s["cosine_sim"] for s in personality_sims])
    p_std = std([s["cosine_sim"] for s in personality_sims])

    v_jacc = mean([s["jaccard_dist"] for s in variation_sims])
    p_jacc = mean([s["jaccard_dist"] for s in personality_sims])

    report = []
    report.append("# G.E.A.R. Experiment: Analysis Report")
    report.append(f"\n> Generated: {datetime.now().isoformat()}")
    report.append(f"> Valid runs: {len(results)} / 144")
    report.append(f"> Models: {', '.join(models)}")
    report.append(f"> Vocabulary: {len(vocab)} unique tokens")
    report.append("")

    # ─── HEADLINE RESULT ───
    report.append("## 1. Headline Result: Variation vs Personality Effect")
    report.append("")
    report.append("The core question: does changing cognitive variation produce MORE output divergence")
    report.append("than changing personality, when task and model are held constant?")
    report.append("")
    report.append("| Dimension Changed | Mean Cosine Similarity | Mean Divergence (1-cos) | Mean Jaccard Distance |")
    report.append("|-------------------|----------------------|------------------------|----------------------|")
    report.append(f"| **Variation** (GEAR) | {v_mean:.4f} (SD={v_std:.4f}) | **{1-v_mean:.4f}** | {v_jacc:.4f} |")
    report.append(f"| **Personality** | {p_mean:.4f} (SD={p_std:.4f}) | **{1-p_mean:.4f}** | {p_jacc:.4f} |")
    report.append("")

    if v_mean < p_mean:
        ratio = (1 - v_mean) / (1 - p_mean) if (1 - p_mean) > 0 else float('inf')
        report.append(f"**Finding:** Variation produces **{ratio:.1f}x more divergence** than personality.")
        report.append("This supports the approximate independence claim: cognitive variation is a meaningful")
        report.append("dimension that changes output independently of (and more than) personality framing.")
    elif v_mean > p_mean:
        ratio = (1 - p_mean) / (1 - v_mean) if (1 - v_mean) > 0 else float('inf')
        report.append(f"**Finding:** Personality produces {ratio:.1f}x more divergence than variation.")
        report.append("This challenges the approximate independence claim and suggests personality framing")
        report.append("has a stronger effect than cognitive variation instruction.")
    else:
        report.append("**Finding:** Variation and personality produce similar divergence levels.")
    report.append("")

    # ─── PER-MODEL BREAKDOWN ───
    report.append("## 2. Cross-Model Consistency")
    report.append("")
    report.append("Does the effect hold across architecturally different models?")
    report.append("")
    report.append("| Model | Var Divergence | Pers Divergence | Var/Pers Ratio | Effect Consistent? |")
    report.append("|-------|---------------|-----------------|----------------|-------------------|")
    for model in models:
        m_effect = model_var_effect[model]
        ratio = m_effect["variation_divergence"] / m_effect["personality_divergence"] if m_effect["personality_divergence"] > 0 else 0
        consistent = "Yes" if m_effect["variation_divergence"] > m_effect["personality_divergence"] else "No"
        report.append(f"| {model} | {m_effect['variation_divergence']:.4f} | {m_effect['personality_divergence']:.4f} | {ratio:.2f}x | {consistent} |")
    report.append("")

    # ─── VARIATION PAIR DIVERGENCE ───
    report.append("## 3. Variation Pair Divergence Matrix")
    report.append("")
    report.append("Which variation pairs produce the most different outputs? (lower similarity = more different)")
    report.append("")
    report.append("| Variation Pair | Mean Cosine Sim | Divergence | N |")
    report.append("|---------------|----------------|------------|---|")
    for pair in sorted(var_pair_sims.keys()):
        sims = var_pair_sims[pair]
        report.append(f"| {pair[0]} ↔ {pair[1]} | {mean(sims):.4f} | {1-mean(sims):.4f} | {len(sims)} |")

    # Find the blind spot pairs
    report.append("")
    blind_spots = {
        ("adversarial", "engaging"): "Split ↔ Join (predicted blind spot pair)",
        ("generative", "reflective"): "Forward ↔ Backward (predicted blind spot pair)",
    }
    report.append("**Blind spot prediction test:** The framework predicts that Adversarial ↔ Engaging")
    report.append("and Generative ↔ Reflective should show maximal divergence (lowest similarity).")
    report.append("")
    for pair, label in blind_spots.items():
        pair_key = tuple(sorted(pair))
        if pair_key in var_pair_sims:
            sims = var_pair_sims[pair_key]
            report.append(f"- {label}: cosine={mean(sims):.4f}, divergence={1-mean(sims):.4f}")
    report.append("")

    # ─── PER-TASK EFFECT ───
    report.append("## 4. Per-Task Analysis")
    report.append("")
    report.append("Does variation effect hold across different task types?")
    report.append("")
    report.append("| Task | Var Mean Sim | Pers Mean Sim | Var > Pers? |")
    report.append("|------|-------------|---------------|-------------|")
    for task in tasks:
        v_s = mean(task_var_sims[task]) if task_var_sims[task] else 0
        p_s = mean(task_pers_sims[task]) if task_pers_sims[task] else 0
        holds = "**Yes**" if v_s < p_s else "No"
        report.append(f"| {task} | {v_s:.4f} | {p_s:.4f} | {holds} |")
    report.append("")

    # ─── STRUCTURAL ELEMENT PROFILES ───
    report.append("## 5. Structural Element Profiles by Variation")
    report.append("")
    report.append("Do different variations produce structurally different outputs?")
    report.append("(Mean count of structural elements per response)")
    report.append("")
    elements = ["questions", "warnings", "connections", "reflections", "creations", "recommendations"]
    header = "| Variation | " + " | ".join(e.capitalize() for e in elements) + " |"
    sep = "|-----------|" + "|".join("--------" for _ in elements) + "|"
    report.append(header)
    report.append(sep)
    for var in variations:
        vals = []
        for elem in elements:
            data = structural[var][elem]
            vals.append(f"{mean(data):.1f}" if data else "0.0")
        report.append(f"| **{var.capitalize()}** | " + " | ".join(vals) + " |")
    report.append("")
    report.append("**Expected pattern (if GEAR works):**")
    report.append("- Generative should have highest 'creations'")
    report.append("- Adversarial should have highest 'warnings'")
    report.append("- Engaging should have highest 'connections'")
    report.append("- Reflective should have highest 'reflections'")
    report.append("")

    # Check if expected pattern holds
    expected = {
        "generative": "creations",
        "adversarial": "warnings",
        "engaging": "connections",
        "reflective": "reflections",
    }
    confirmed = 0
    for var, expected_elem in expected.items():
        mean_expected = mean(structural[var][expected_elem]) if structural[var][expected_elem] else 0
        is_highest = True
        for other_var in variations:
            if other_var != var:
                other_mean = mean(structural[other_var][expected_elem]) if structural[other_var][expected_elem] else 0
                if other_mean >= mean_expected:
                    is_highest = False
                    break
        if is_highest:
            confirmed += 1
            report.append(f"✅ {var.capitalize()} has highest '{expected_elem}' count")
        else:
            report.append(f"⚠️ {var.capitalize()} does NOT have highest '{expected_elem}' count")
    report.append("")
    report.append(f"**Structural signature match: {confirmed}/4**")
    report.append("")

    # ─── SUMMARY ───

    report.append("## 6. Summary")
    report.append("")
    report.append(f"- **Total valid runs:** {len(results)}")
    report.append(f"- **Variation divergence:** {1-v_mean:.4f} (mean)")
    report.append(f"- **Personality divergence:** {1-p_mean:.4f} (mean)")
    if v_mean < p_mean:
        report.append(f"- **Effect ratio:** Variation produces {(1-v_mean)/(1-p_mean):.1f}x more divergence")
    report.append(f"- **Cross-model:** Effect holds in {sum(1 for m in model_var_effect.values() if m['variation_divergence'] > m['personality_divergence'])}/{len(models)} models")
    report.append(f"- **Cross-task:** Effect holds in {sum(1 for t in tasks if mean(task_var_sims[t]) < mean(task_pers_sims[t]))}/{len(tasks)} tasks")
    report.append(f"- **Structural signature:** {confirmed}/4 variations show expected element profile")
    report.append("")

    # Write report
    report_text = "\n".join(report)

    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    print(f"\nReport written to: {REPORT_FILE}")
    print(f"\nHeadline: Variation divergence={1-v_mean:.4f}, Personality divergence={1-p_mean:.4f}")
    if v_mean < p_mean:
        print(f"→ Variation produces {(1-v_mean)/(1-p_mean):.1f}x more divergence than personality")

    return report_text


if __name__ == "__main__":

    analyse()

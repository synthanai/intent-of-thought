#!/usr/bin/env python3
"""
GEAR v4 Threshold Validation Analysis
======================================
Computes embedding-based semantic divergence across the Qwen same-family
size gradient to test: "Cognitive variation responsiveness scales with
model parameter count."

Metrics:
1. Word count divergence (legacy, from v3)
2. Embedding cosine similarity (PRIMARY, new in v4)
3. Falsification control comparison

Output: analysis_report_v4.md
"""

import json
import math
import statistics
from pathlib import Path
from collections import defaultdict
from itertools import combinations

RAW_DIR = Path(__file__).parent / "results_v4" / "raw"
EMBED_DIR = Path(__file__).parent / "results_v4" / "embeddings"
FALSIFY_DIR = Path(__file__).parent / "results_v4" / "falsification"
REPORT = Path(__file__).parent / "results_v4" / "analysis_report_v4.md"

SIZE_ORDER = {"qwen2.5:0.5b": 0.5, "qwen2.5:1.5b": 1.5, "qwen2.5:3b": 3, "qwen2.5:7b": 7}


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def load_data():
    """Load all raw results and embeddings."""
    runs = []
    for f in sorted(RAW_DIR.glob("*.json")):
        try:
            with open(f) as fh:
                d = json.load(fh)
            if d.get("status") == "ok" and d.get("response", "").strip():
                # Load corresponding embedding
                embed_file = EMBED_DIR / f.name
                embedding = None
                if embed_file.exists():
                    with open(embed_file) as ef:
                        ed = json.load(ef)
                        embedding = ed.get("embedding")
                d["embedding"] = embedding
                runs.append(d)
        except Exception as e:
            pass
    return runs


def compute_variation_divergence(runs, metric="embedding"):
    """
    For each (model, task, personality) cell, compute pairwise divergence
    between all variation pairs. Returns per-model average divergence.
    
    If metric="embedding": use 1 - cosine_similarity (semantic distance)
    If metric="word_count": use absolute word count difference
    """
    # Group by (model, task, personality)
    cells = defaultdict(dict)
    for r in runs:
        key = (r["model"], r["task"], r["personality"])
        cells[key][r["variation"]] = r

    # Compute pairwise divergence within each cell
    model_divergences = defaultdict(list)
    for (model, task, pers), variations in cells.items():
        var_keys = sorted(variations.keys())
        if len(var_keys) < 2:
            continue
        for v1, v2 in combinations(var_keys, 2):
            r1, r2 = variations[v1], variations[v2]
            if metric == "embedding":
                e1, e2 = r1.get("embedding"), r2.get("embedding")
                if e1 and e2:
                    div = 1.0 - cosine_similarity(e1, e2)
                    model_divergences[model].append(div)
            elif metric == "word_count":
                div = abs(r1["word_count"] - r2["word_count"])
                model_divergences[model].append(div)

    return model_divergences


def compute_personality_divergence(runs, metric="embedding"):
    """Same as above but across personalities instead of variations."""
    cells = defaultdict(dict)
    for r in runs:
        key = (r["model"], r["task"], r["variation"])
        cells[key][r["personality"]] = r

    model_divergences = defaultdict(list)
    for (model, task, var), personalities in cells.items():
        pers_keys = sorted(personalities.keys())
        if len(pers_keys) < 2:
            continue
        for p1, p2 in combinations(pers_keys, 2):
            r1, r2 = personalities[p1], personalities[p2]
            if metric == "embedding":
                e1, e2 = r1.get("embedding"), r2.get("embedding")
                if e1 and e2:
                    div = 1.0 - cosine_similarity(e1, e2)
                    model_divergences[model].append(div)
            elif metric == "word_count":
                div = abs(r1["word_count"] - r2["word_count"])
                model_divergences[model].append(div)

    return model_divergences


def per_task_divergence(runs):
    """Compute embedding divergence per task per model."""
    cells = defaultdict(dict)
    for r in runs:
        key = (r["model"], r["task"], r["personality"])
        cells[key][r["variation"]] = r

    result = defaultdict(lambda: defaultdict(list))
    for (model, task, pers), variations in cells.items():
        var_keys = sorted(variations.keys())
        if len(var_keys) < 2:
            continue
        for v1, v2 in combinations(var_keys, 2):
            e1 = variations[v1].get("embedding")
            e2 = variations[v2].get("embedding")
            if e1 and e2:
                div = 1.0 - cosine_similarity(e1, e2)
                result[model][task].append(div)
    return result


def analyse_falsification():
    """Analyse the inverted-prompt falsification control."""
    if not FALSIFY_DIR.exists():
        return "No falsification data found."

    results = []
    for f in sorted(FALSIFY_DIR.glob("*.json")):
        if "_embed" in f.name:
            continue
        try:
            with open(f) as fh:
                d = json.load(fh)
            embed_file = FALSIFY_DIR / f"{f.stem}_embed.json"
            embedding = None
            if embed_file.exists():
                with open(embed_file) as ef:
                    embedding = json.load(ef).get("embedding")
            d["embedding"] = embedding
            results.append(d)
        except:
            pass

    if not results:
        return "No falsification results found."

    # Group by model
    by_model = defaultdict(list)
    for r in results:
        by_model[r["model"]].append(r)

    # For each model, compare inverted responses with normal responses
    lines = []
    for model in sorted(by_model.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
        inv_runs = by_model[model]
        sz = SIZE_ORDER.get(model, "?")
        lines.append(f"\n### {model} ({sz}B)")
        lines.append(f"| Label | Actual | Words |")
        lines.append(f"|:------|:-------|:------|")
        for r in inv_runs:
            lines.append(f"| {r.get('variation_label', '?')} | {r.get('variation_actual', '?')} | {r['word_count']}w |")

        # Compare embeddings between inverted pairs
        # If model discriminates: inverted should differ from normal
        # If model ignores: inverted should be similar to normal
        inv_embeddings = {r.get("variation_label"): r.get("embedding") for r in inv_runs if r.get("embedding")}

        # Load corresponding normal embeddings
        normal_embeddings = {}
        for var_label in inv_embeddings:
            normal_file = EMBED_DIR / f"{model}__ethical_ai__{var_label}__cautious_analyst.json"
            if normal_file.exists():
                with open(normal_file) as f:
                    nd = json.load(f)
                    normal_embeddings[var_label] = nd.get("embedding")

        if inv_embeddings and normal_embeddings:
            lines.append(f"\n**Normal vs Inverted Similarity:**")
            lines.append(f"| Variation | Cosine Sim | Interpretation |")
            lines.append(f"|:----------|:-----------|:---------------|")
            sims = []
            for var_label in sorted(inv_embeddings.keys()):
                if var_label in normal_embeddings and inv_embeddings[var_label]:
                    sim = cosine_similarity(inv_embeddings[var_label], normal_embeddings[var_label])
                    sims.append(sim)
                    interp = "SAME (ignores instruction)" if sim > 0.95 else "DIFFERENT (reads instruction)" if sim < 0.85 else "AMBIGUOUS"
                    lines.append(f"| {var_label} | {sim:.4f} | {interp} |")
            if sims:
                avg_sim = statistics.mean(sims)
                lines.append(f"\n**Average similarity: {avg_sim:.4f}**")
                if avg_sim > 0.95:
                    lines.append(f"→ Model IGNORES variation instructions (treats all modes the same)")
                elif avg_sim < 0.85:
                    lines.append(f"→ Model READS variation instructions (different cognitive modes produce different outputs)")
                else:
                    lines.append(f"→ Model PARTIALLY responds to variation instructions")

    return "\n".join(lines)


def main():
    print("Loading v4 data...")
    runs = load_data()
    print(f"Loaded {len(runs)} valid runs with embeddings")

    by_model = defaultdict(list)
    for r in runs:
        by_model[r["model"]].append(r)

    report = []
    report.append("# GEAR v4: Threshold Validation Analysis Report\n")
    report.append(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Total runs**: {len(runs)}")
    report.append(f"**Models**: {', '.join(sorted(by_model.keys(), key=lambda m: SIZE_ORDER.get(m, 99)))}")
    report.append(f"**Design**: Same-family gradient (Qwen 2.5), 6 deep tasks, 4 variations, 2 personalities")
    report.append(f"**Primary metric**: Embedding cosine distance (1 - similarity)")
    report.append("")

    # ════════════════════════════════════════════════════════
    # 1. BASIC STATS
    # ════════════════════════════════════════════════════════
    report.append("## 1. Basic Stats Per Model\n")
    report.append("| Model | Size | Runs | Avg Words | Med Words | Avg Time | StDev |")
    report.append("|:------|:-----|:-----|:----------|:----------|:---------|:------|")
    for model in sorted(by_model.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
        data = by_model[model]
        words = [r["word_count"] for r in data]
        times = [r["elapsed_seconds"] for r in data]
        sz = SIZE_ORDER.get(model, "?")
        report.append(f"| {model} | {sz}B | {len(data)} | {statistics.mean(words):.0f} | {statistics.median(words):.0f} | {statistics.mean(times):.0f}s | {statistics.stdev(words):.0f} |")
    report.append("")

    # ════════════════════════════════════════════════════════
    # 2. EMBEDDING-BASED VARIATION DIVERGENCE (PRIMARY)
    # ════════════════════════════════════════════════════════
    report.append("## 2. Embedding-Based Variation Divergence (PRIMARY METRIC)\n")
    report.append("> Higher cosine distance = more semantic differentiation between cognitive modes\n")

    var_div = compute_variation_divergence(runs, "embedding")
    pers_div = compute_personality_divergence(runs, "embedding")

    report.append("| Model | Size | Var Divergence | Pers Divergence | V/P Ratio | Winner |")
    report.append("|:------|:-----|:---------------|:----------------|:----------|:-------|")
    for model in sorted(var_div.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
        sz = SIZE_ORDER.get(model, "?")
        v_mean = statistics.mean(var_div[model]) if var_div[model] else 0
        p_mean = statistics.mean(pers_div[model]) if pers_div.get(model) else 0
        ratio = v_mean / p_mean if p_mean > 0 else float('inf')
        winner = "VARIATION" if v_mean > p_mean else "PERSONALITY"
        report.append(f"| {model} | {sz}B | {v_mean:.4f} | {p_mean:.4f} | {ratio:.2f}x | {winner} |")
    report.append("")

    # Print to console too
    print("\n" + "=" * 70)
    print("EMBEDDING-BASED VARIATION DIVERGENCE")
    print("=" * 70)
    for model in sorted(var_div.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
        sz = SIZE_ORDER.get(model, "?")
        v_mean = statistics.mean(var_div[model]) if var_div[model] else 0
        p_mean = statistics.mean(pers_div[model]) if pers_div.get(model) else 0
        ratio = v_mean / p_mean if p_mean > 0 else float('inf')
        winner = "VAR" if v_mean > p_mean else "PERS"
        print(f"  {model:<16} ({sz:>4}B): var={v_mean:.4f}  pers={p_mean:.4f}  ratio={ratio:.2f}x  [{winner}]")

    # ════════════════════════════════════════════════════════
    # 3. SIZE GRADIENT: Does divergence scale with size?
    # ════════════════════════════════════════════════════════
    report.append("## 3. Size Gradient: Divergence vs Parameter Count\n")
    report.append("> This is the KEY test. If the threshold hypothesis holds,")
    report.append("> divergence should increase with model size.\n")

    gradient_data = []
    report.append("| Model | Size | Embed Var Div | Word Count Var Spread | Embed CoV |")
    report.append("|:------|:-----|:--------------|:----------------------|:----------|")

    wc_div = compute_variation_divergence(runs, "word_count")

    for model in sorted(var_div.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
        sz = SIZE_ORDER.get(model, "?")
        e_mean = statistics.mean(var_div[model]) if var_div[model] else 0
        e_std = statistics.stdev(var_div[model]) if len(var_div[model]) > 1 else 0
        w_mean = statistics.mean(wc_div[model]) if wc_div.get(model) else 0
        cov = (e_std / e_mean * 100) if e_mean > 0 else 0
        gradient_data.append((sz, e_mean, w_mean))
        report.append(f"| {model} | {sz}B | {e_mean:.4f} | {w_mean:.0f}w | {cov:.1f}% |")

    # Compute correlation (Spearman rank)
    if len(gradient_data) >= 3:
        sizes = [g[0] for g in gradient_data]
        divs = [g[1] for g in gradient_data]
        # Simple rank correlation
        size_ranks = [sorted(sizes).index(s) + 1 for s in sizes]
        div_ranks = [sorted(divs).index(d) + 1 for d in divs]
        n = len(sizes)
        d_sq = sum((sr - dr) ** 2 for sr, dr in zip(size_ranks, div_ranks))
        rho = 1 - (6 * d_sq) / (n * (n**2 - 1))
        report.append(f"\n**Spearman rank correlation (size vs embedding divergence): ρ = {rho:.3f}**")
        if rho > 0.7:
            report.append(f"→ **STRONG positive correlation**: larger models show more variation divergence")
        elif rho > 0.3:
            report.append(f"→ **Moderate positive correlation**: some size effect")
        elif rho > -0.3:
            report.append(f"→ **No correlation**: size does not predict divergence")
        else:
            report.append(f"→ **Negative correlation**: smaller models show MORE divergence")
    report.append("")

    # ════════════════════════════════════════════════════════
    # 4. PER-TASK DIVERGENCE
    # ════════════════════════════════════════════════════════
    report.append("## 4. Per-Task Embedding Divergence\n")
    task_div = per_task_divergence(runs)
    tasks = sorted(set(r["task"] for r in runs))

    report.append("| Task | " + " | ".join(f"{m} ({SIZE_ORDER.get(m,'?')}B)" for m in sorted(task_div.keys(), key=lambda m: SIZE_ORDER.get(m, 99))) + " |")
    report.append("|:-----|" + "|".join(":------|" for _ in task_div) + "")

    for task in tasks:
        row = f"| {task} |"
        for model in sorted(task_div.keys(), key=lambda m: SIZE_ORDER.get(m, 99)):
            vals = task_div[model].get(task, [])
            if vals:
                row += f" {statistics.mean(vals):.4f} |"
            else:
                row += " - |"
        report.append(row)
    report.append("")

    # ════════════════════════════════════════════════════════
    # 5. FALSIFICATION CONTROL
    # ════════════════════════════════════════════════════════
    report.append("## 5. Falsification Control (Inverted Prompts)\n")
    report.append("> If model READS instructions: normal vs inverted should differ (low similarity)")
    report.append("> If model IGNORES: normal vs inverted should be the same (high similarity)\n")
    falsification_analysis = analyse_falsification()
    report.append(falsification_analysis)
    report.append("")

    # ════════════════════════════════════════════════════════
    # 6. VERDICT
    # ════════════════════════════════════════════════════════
    report.append("## 6. Verdict\n")

    # Determine if threshold hypothesis holds
    if len(gradient_data) >= 3:
        sizes = [g[0] for g in gradient_data]
        divs = [g[1] for g in gradient_data]
        smallest_div = divs[0]
        largest_div = divs[-1]
        ratio = largest_div / smallest_div if smallest_div > 0 else float('inf')

        report.append(f"- Smallest model ({sizes[0]}B) embedding divergence: {smallest_div:.4f}")
        report.append(f"- Largest model ({sizes[-1]}B) embedding divergence: {largest_div:.4f}")
        report.append(f"- Ratio: {ratio:.2f}x")
        report.append("")

        if ratio > 1.5 and rho > 0.5:
            report.append("### ✅ THRESHOLD HYPOTHESIS SUPPORTED")
            report.append("Cognitive variation responsiveness scales with model parameter count ")
            report.append("within the Qwen 2.5 family. Larger models produce semantically more ")
            report.append("diverse responses when given different cognitive mode instructions.")
        elif ratio > 1.2:
            report.append("### ⚠️ WEAK SUPPORT")
            report.append("Some evidence of size-dependent variation responsiveness, but the ")
            report.append("effect is modest. Further investigation needed.")
        else:
            report.append("### ❌ THRESHOLD HYPOTHESIS NOT SUPPORTED")
            report.append("Embedding-based analysis does not confirm that larger models are more ")
            report.append("responsive to cognitive variation instructions.")

    # Write report
    report_text = "\n".join(report)
    with open(REPORT, "w") as f:
        f.write(report_text)
    print(f"\nReport saved: {REPORT}")
    print("\n" + report_text)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
IoT Lifecycle Experiment Suite: Phase 3 - Analyse Scored Results

Reads all scored experiment results and produces:
1. Summary statistics per experiment
2. LaTeX/Markdown tables for the paper
3. Visual charts (if matplotlib available)
4. Paper-ready evaluation section draft

Usage:
    python3 analyse_results.py                    # Full analysis
    python3 analyse_results.py --experiment exp1  # Single experiment
    python3 analyse_results.py --format latex     # LaTeX tables
    python3 analyse_results.py --progress         # Show scoring progress only
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

from config import RAW_RESULTS_DIR, ANALYSIS_DIR, MODELS


def load_scored_results(experiment_dir: Path) -> list:
    """Load all scored results from an experiment directory."""
    results = []
    for f in sorted(experiment_dir.glob("*.json")):
        data = json.load(open(f))
        if data.get("score", -1) >= 0:
            results.append(data)
    return results


def load_all_results(experiment_dir: Path) -> tuple:
    """Load all results (scored and unscored) for progress tracking."""
    scored = []
    unscored = []
    empty = []
    for f in sorted(experiment_dir.glob("*.json")):
        data = json.load(open(f))
        if not data.get("response", ""):
            empty.append(data)
        elif data.get("score", -1) >= 0:
            scored.append(data)
        else:
            unscored.append(data)
    return scored, unscored, empty


def show_progress():
    """Show scoring progress across all experiments."""
    print("\n" + "=" * 70)
    print("SCORING PROGRESS")
    print("=" * 70)

    total_scored = 0
    total_valid = 0
    total_empty = 0

    for exp_dir in sorted(RAW_RESULTS_DIR.iterdir()):
        if not exp_dir.is_dir():
            continue
        scored, unscored, empty = load_all_results(exp_dir)
        total = len(scored) + len(unscored) + len(empty)
        valid = len(scored) + len(unscored)
        pct = (len(scored) / valid * 100) if valid > 0 else 0

        print(f"\n  {exp_dir.name}:")
        print(f"    Total files:  {total}")
        print(f"    Empty:        {len(empty)}")
        print(f"    Valid:        {valid}")
        print(f"    Scored:       {len(scored)} ({pct:.0f}%)")
        print(f"    Remaining:    {len(unscored)}")

        total_scored += len(scored)
        total_valid += valid
        total_empty += len(empty)

    pct = (total_scored / total_valid * 100) if total_valid > 0 else 0
    print(f"\n  OVERALL: {total_scored}/{total_valid} scored ({pct:.0f}%)")
    print(f"  Empty responses: {total_empty}")
    print("=" * 70)


# ─── EXPERIMENT 1 ANALYSIS ────────────────────────────────────────

def analyse_exp1(results: list, fmt: str = "markdown") -> dict:
    """
    Exp 1: IoT Governance Impact
    Compare baseline vs IoT L2 across models and topologies.
    """
    # Group by condition × topology
    by_condition = defaultdict(list)
    by_model = defaultdict(lambda: defaultdict(list))
    by_category = defaultdict(lambda: defaultdict(list))

    for r in results:
        condition = r.get("condition", "unknown")
        topology = r.get("topology", "unknown")
        model = r.get("model", "unknown")
        category = r.get("task_category", "unknown")
        score = r["score"]

        by_condition[f"{condition}_{topology}"].append(score)
        by_model[model][condition].append(score)
        by_category[category][condition].append(score)

    # Summary table: condition × topology
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: IoT GOVERNANCE IMPACT")
    print("=" * 70)

    if fmt == "markdown":
        print("\n### Table: Mean Score by Condition × Topology\n")
        print("| Condition | Topology | N | Mean | Std |")
        print("|-----------|----------|---|------|-----|")
    else:
        print("\n\\begin{table}[h]")
        print("\\centering")
        print("\\begin{tabular}{llccc}")
        print("\\hline")
        print("Condition & Topology & N & Mean & Std \\\\")
        print("\\hline")

    stats = {}
    for key in sorted(by_condition.keys()):
        scores = by_condition[key]
        parts = key.split("_", 1)
        condition = parts[0] if len(parts) > 0 else key
        topology = parts[1] if len(parts) > 1 else "all"
        n = len(scores)
        mean = sum(scores) / n if n > 0 else 0
        std = (sum((s - mean) ** 2 for s in scores) / n) ** 0.5 if n > 1 else 0

        stats[key] = {"n": n, "mean": mean, "std": std}

        if fmt == "markdown":
            print(f"| {condition} | {topology} | {n} | {mean:.2f} | {std:.2f} |")
        else:
            print(f"{condition} & {topology} & {n} & {mean:.2f} & {std:.2f} \\\\")

    if fmt == "latex":
        print("\\hline")
        print("\\end{tabular}")
        print("\\end{table}")

    # Per-model breakdown: IoT vs baseline
    print("\n### Table: IoT Governance Uplift by Model\n")
    if fmt == "markdown":
        print("| Model | Baseline Mean | IoT L2 Mean | Δ | Uplift % |")
        print("|-------|:------------:|:----------:|:---:|:--------:|")

    model_stats = {}
    for model in sorted(by_model.keys()):
        baseline = by_model[model].get("baseline", [])
        iot = by_model[model].get("iot_l2", [])
        b_mean = sum(baseline) / len(baseline) if baseline else 0
        i_mean = sum(iot) / len(iot) if iot else 0
        delta = i_mean - b_mean
        uplift = (delta / b_mean * 100) if b_mean > 0 else 0

        model_name = model.replace(":", " ").replace("_", " ")
        model_stats[model] = {"baseline": b_mean, "iot": i_mean, "delta": delta, "uplift": uplift}

        if fmt == "markdown":
            print(f"| {model_name} | {b_mean:.2f} | {i_mean:.2f} | {delta:+.2f} | {uplift:+.1f}% |")

    # Per-category breakdown
    print("\n### Table: IoT Governance Impact by Task Category\n")
    if fmt == "markdown":
        print("| Category | Baseline Mean | IoT L2 Mean | Δ |")
        print("|----------|:------------:|:----------:|:---:|")

    for cat in ["sequential", "parallel", "interconnected"]:
        if cat in by_category:
            baseline = by_category[cat].get("baseline", [])
            iot = by_category[cat].get("iot_l2", [])
            b_mean = sum(baseline) / len(baseline) if baseline else 0
            i_mean = sum(iot) / len(iot) if iot else 0
            delta = i_mean - b_mean

            if fmt == "markdown":
                print(f"| {cat} | {b_mean:.2f} | {i_mean:.2f} | {delta:+.2f} |")

    return {"condition_stats": stats, "model_stats": model_stats}


# ─── EXPERIMENT 5 ANALYSIS ────────────────────────────────────────

def analyse_exp5(results: list, fmt: str = "markdown") -> dict:
    """
    Exp 5: Anti-Purpose Ablation
    Compare full triple, no anti-purpose, no success signal.
    """
    by_condition = defaultdict(list)
    by_domain = defaultdict(lambda: defaultdict(list))

    for r in results:
        condition = r.get("condition", "unknown")
        domain = r.get("domain", "unknown")
        score = r["score"]

        by_condition[condition].append(score)
        by_domain[domain][condition].append(score)

    print("\n" + "=" * 70)
    print("EXPERIMENT 5: ANTI-PURPOSE ABLATION")
    print("=" * 70)

    print("\n### Table: Mean Score by Condition\n")
    if fmt == "markdown":
        print("| Condition | N | Mean | Std |")
        print("|-----------|---|------|-----|")

    stats = {}
    for condition in ["full_triple", "no_anti_purpose", "no_success_signal"]:
        scores = by_condition.get(condition, [])
        n = len(scores)
        mean = sum(scores) / n if n > 0 else 0
        std = (sum((s - mean) ** 2 for s in scores) / n) ** 0.5 if n > 1 else 0
        stats[condition] = {"n": n, "mean": mean, "std": std}

        if fmt == "markdown":
            print(f"| {condition.replace('_', ' ')} | {n} | {mean:.2f} | {std:.2f} |")

    # Domain breakdown
    print("\n### Table: Ablation Impact by Domain\n")
    if fmt == "markdown":
        print("| Domain | Full Triple | No Anti-P | No Success-S |")
        print("|--------|:----------:|:---------:|:------------:|")

    for domain in sorted(by_domain.keys()):
        ft = by_domain[domain].get("full_triple", [])
        nap = by_domain[domain].get("no_anti_purpose", [])
        nss = by_domain[domain].get("no_success_signal", [])
        ft_mean = sum(ft) / len(ft) if ft else 0
        nap_mean = sum(nap) / len(nap) if nap else 0
        nss_mean = sum(nss) / len(nss) if nss else 0

        if fmt == "markdown":
            print(f"| {domain} | {ft_mean:.2f} | {nap_mean:.2f} | {nss_mean:.2f} |")

    return stats


# ─── EXPERIMENT 8 ANALYSIS ────────────────────────────────────────

def analyse_exp8(results: list, fmt: str = "markdown") -> dict:
    """
    Exp 8: Topology Confusion Matrix
    Which topologies get misapplied to which task types.
    """
    # Build confusion matrix: optimal × forced → mean score
    matrix = defaultdict(lambda: defaultdict(list))

    for r in results:
        optimal = r.get("optimal_topology", "unknown")
        forced = r.get("forced_topology", "unknown")
        score = r["score"]
        matrix[optimal][forced].append(score)

    print("\n" + "=" * 70)
    print("EXPERIMENT 8: TOPOLOGY CONFUSION MATRIX")
    print("=" * 70)

    topologies = ["cot", "tot", "got"]

    print("\n### Table: Mean Score (Optimal × Forced Topology)\n")
    if fmt == "markdown":
        header = "| Optimal ↓ / Forced → | " + " | ".join(t.upper() for t in topologies) + " |"
        print(header)
        print("|" + "|".join(["---"] * (len(topologies) + 1)) + "|")

    stats = {}
    for optimal in topologies:
        row = []
        for forced in topologies:
            scores = matrix[optimal][forced]
            mean = sum(scores) / len(scores) if scores else 0
            n = len(scores)
            marker = " **" if optimal == forced else ""
            row.append(f"{mean:.2f} (n={n}){marker}")
            stats[f"{optimal}_as_{forced}"] = {"mean": mean, "n": n}

        if fmt == "markdown":
            print(f"| **{optimal.upper()}** | " + " | ".join(row) + " |")

    # Diagonal vs off-diagonal
    diag_scores = []
    off_diag_scores = []
    for optimal in topologies:
        for forced in topologies:
            scores = matrix[optimal][forced]
            if optimal == forced:
                diag_scores.extend(scores)
            else:
                off_diag_scores.extend(scores)

    diag_mean = sum(diag_scores) / len(diag_scores) if diag_scores else 0
    off_mean = sum(off_diag_scores) / len(off_diag_scores) if off_diag_scores else 0

    print(f"\n**Correct topology (diagonal): {diag_mean:.2f} (n={len(diag_scores)})**")
    print(f"**Wrong topology (off-diagonal): {off_mean:.2f} (n={len(off_diag_scores)})**")
    print(f"**Misselection penalty: {diag_mean - off_mean:+.2f}**")

    return stats


# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 3: Analyse Scored Results")
    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="Analyse specific experiment (exp1, exp5, exp8)",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="markdown",
        choices=["markdown", "latex"],
        help="Output table format",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show scoring progress only",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save analysis to file",
    )
    args = parser.parse_args()

    if args.progress:
        show_progress()
        return

    if args.output:
        sys.stdout = open(args.output, "w")

    print(f"# IoT Lifecycle Experiment Analysis")
    print(f"Generated: {datetime.now().isoformat()}")
    print(f"Models: {', '.join(MODELS.keys())}")

    # Show progress first
    show_progress()

    experiments = {
        "exp1": ("exp1_governance_impact", analyse_exp1),
        "exp5": ("exp5_anti_purpose", analyse_exp5),
        "exp8": ("exp8_confusion_matrix", analyse_exp8),
    }

    all_stats = {}

    target_exps = [args.experiment] if args.experiment else list(experiments.keys())

    for exp_key in target_exps:
        if exp_key not in experiments:
            print(f"\nUnknown experiment: {exp_key}")
            continue

        dir_name, analyser = experiments[exp_key]
        exp_dir = RAW_RESULTS_DIR / dir_name

        if not exp_dir.exists():
            print(f"\nNo results for {exp_key}")
            continue

        results = load_scored_results(exp_dir)
        if not results:
            print(f"\n{exp_key}: No scored results yet. Run score_results.py first.")
            continue

        stats = analyser(results, fmt=args.format)
        all_stats[exp_key] = stats

    # Save stats
    stats_file = ANALYSIS_DIR / "experiment_stats.json"
    with open(stats_file, "w") as f:
        json.dump(all_stats, f, indent=2, default=str)
    print(f"\nStats saved to: {stats_file}")

    if args.output:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        print(f"Analysis saved to: {args.output}")


if __name__ == "__main__":
    main()

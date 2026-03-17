"""IoT-Bench: Run all experiments for the IoT Lifecycle paper.

Usage:
    python -m benchmark.run_experiments --experiment e1
    python -m benchmark.run_experiments --experiment all
"""

import argparse
import json
import sys
from pathlib import Path
from collections import Counter

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lifecycle.capture import CaptureMode
from lifecycle.judge import FailureMode
from lifecycle.runner import LifecycleRunner


TASK_DIR = Path(__file__).parent / "tasks"
RESULTS_DIR = Path(__file__).parent / "results"


def load_tasks() -> list[dict]:
    """Load all benchmark tasks from JSON files."""
    tasks = []
    for f in sorted(TASK_DIR.glob("*.json")):
        with open(f) as fh:
            tasks.extend(json.load(fh))
    return tasks


def run_e1(runner: LifecycleRunner, tasks: list[dict]) -> None:
    """E1: Capture Fidelity Gradient.

    Run each task at L0, L1, L2, L3. Measure topology selection accuracy.
    """
    print("\n" + "=" * 60)
    print("E1: CAPTURE FIDELITY GRADIENT")
    print("=" * 60)

    all_metrics = []
    modes = [CaptureMode.ZERO, CaptureMode.IMPLICIT, CaptureMode.PROMPTED, CaptureMode.COLLABORATIVE]

    for mode in modes:
        correct = 0
        total = 0
        fidelities = []

        for task in tasks:
            metrics = runner.run_capture_experiment(task, mode)
            all_metrics.append(metrics)
            fidelities.append(metrics.capture_fidelity)
            if metrics.topology_correct:
                correct += 1
            total += 1

        accuracy = correct / total if total > 0 else 0
        avg_fidelity = sum(fidelities) / len(fidelities) if fidelities else 0

        print(f"\n  {mode.name:15s} | Accuracy: {accuracy:.1%} ({correct}/{total}) | Avg φ: {avg_fidelity:.3f}")

        # Per-domain breakdown
        for domain in ["medical", "legal", "technical"]:
            domain_tasks = [m for m in all_metrics if m.domain == domain and m.capture_mode == mode]
            d_correct = sum(1 for m in domain_tasks if m.topology_correct)
            d_total = len(domain_tasks)
            if d_total > 0:
                print(f"    {domain:12s} | {d_correct}/{d_total} ({d_correct/d_total:.0%})")

    runner.save_results(all_metrics, str(RESULTS_DIR), "e1_capture_fidelity")
    print(f"\n  Results saved to {RESULTS_DIR}/e1_capture_fidelity.json")


def run_e2(runner: LifecycleRunner, tasks: list[dict]) -> None:
    """E2: Topology Misselection Impact.

    Run 30 tasks (10 per optimal topology) with ALL 3 topologies.
    """
    print("\n" + "=" * 60)
    print("E2: TOPOLOGY MISSELECTION IMPACT")
    print("=" * 60)

    # Select 10 tasks per optimal topology
    by_topology = {}
    for task in tasks:
        t = task["optimal_topology"]
        by_topology.setdefault(t, []).append(task)

    selected = []
    for topo in ["CoT", "ToT", "GoT"]:
        selected.extend(by_topology.get(topo, [])[:10])

    all_metrics = []
    for forced_topo in ["CoT", "ToT", "GoT"]:
        for task in selected:
            metrics = runner.run_misselection_experiment(task, forced_topo)
            all_metrics.append(metrics)

    # Summary: accuracy per forced topology vs gold topology
    print(f"\n  {'Forced':>8s} | {'Gold CoT':>10s} | {'Gold ToT':>10s} | {'Gold GoT':>10s}")
    print(f"  {'-'*8} | {'-'*10} | {'-'*10} | {'-'*10}")
    for forced in ["CoT", "ToT", "GoT"]:
        row = f"  {forced:>8s} |"
        for gold in ["CoT", "ToT", "GoT"]:
            matches = [m for m in all_metrics
                       if m.metadata.get("forced_topology") == forced
                       and m.gold_topology == gold]
            correct = sum(1 for m in matches if m.topology_correct)
            total = len(matches)
            marker = "✓" if forced == gold else " "
            row += f" {correct}/{total} {marker}     |"
        print(row)

    runner.save_results(all_metrics, str(RESULTS_DIR), "e2_misselection")
    print(f"\n  Results saved to {RESULTS_DIR}/e2_misselection.json")


def run_e3(runner: LifecycleRunner, tasks: list[dict]) -> None:
    """E3: Retrospective Judgement Accuracy.

    Induce 45 failures (15 per mode) and test diagnosis accuracy.
    """
    print("\n" + "=" * 60)
    print("E3: RETROSPECTIVE JUDGEMENT ACCURACY")
    print("=" * 60)

    all_metrics = []
    modes = [FailureMode.FALSE_CAPTURE, FailureMode.FALSE_SELECTION, FailureMode.FALSE_EXECUTION]

    for mode in modes:
        correct = 0
        total = 0

        for task in tasks[:15]:  # 15 tasks per mode
            metrics, judgement = runner.run_judgement_experiment(task, mode)
            all_metrics.append(metrics)

            if metrics.metadata.get("diagnosis_correct"):
                correct += 1
            total += 1

        accuracy = correct / total if total > 0 else 0
        print(f"\n  {mode.value:20s} | Accuracy: {accuracy:.0%} ({correct}/{total})")

    runner.save_results(all_metrics, str(RESULTS_DIR), "e3_judgement")
    print(f"\n  Results saved to {RESULTS_DIR}/e3_judgement.json")


def main():
    parser = argparse.ArgumentParser(description="IoT-Bench Experiment Runner")
    parser.add_argument("--experiment", choices=["e1", "e2", "e3", "all"], default="all")
    args = parser.parse_args()

    print("=" * 60)
    print("IoT-BENCH: Intent-of-Thought Benchmark Suite")
    print("=" * 60)

    tasks = load_tasks()
    print(f"Loaded {len(tasks)} benchmark tasks")

    # Count by domain and topology
    domain_counts = Counter(t["domain"] for t in tasks)
    topo_counts = Counter(t["optimal_topology"] for t in tasks)
    print(f"  Domains: {dict(domain_counts)}")
    print(f"  Topologies: {dict(topo_counts)}")

    runner = LifecycleRunner()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.experiment in ("e1", "all"):
        run_e1(runner, tasks)
    if args.experiment in ("e2", "all"):
        run_e2(runner, tasks)
    if args.experiment in ("e3", "all"):
        run_e3(runner, tasks)

    print("\n" + "=" * 60)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

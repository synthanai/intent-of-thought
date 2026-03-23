#!/usr/bin/env python3
"""
Export experiment results for the public repository.

Strips raw response text (too large) and keeps only metadata + scores.
Outputs clean JSON files to results/public/ for inclusion in the OSS repo.

Usage:
    python3 export_results.py
"""

import json
from pathlib import Path

RAW_DIR = Path(__file__).parent / "results" / "raw"
PUBLIC_DIR = Path(__file__).parent / "results" / "public"

# Fields to keep in the public export
KEEP_FIELDS = {
    "run_id", "experiment", "task_id", "task_category", "model",
    "condition", "topology", "optimal_topology", "forced_topology",
    "domain", "score", "score_reason", "score_consistent", "scored_at",
    "response_length", "elapsed_seconds", "tokens", "timestamp",
}

# Fields to explicitly exclude (contain full model output)
STRIP_FIELDS = {"response", "ground_truth", "anti_purpose", "scoring_rubric"}


def export():
    total = 0
    for exp_dir in sorted(RAW_DIR.iterdir()):
        if not exp_dir.is_dir():
            continue

        out_dir = PUBLIC_DIR / exp_dir.name
        out_dir.mkdir(parents=True, exist_ok=True)

        for json_file in sorted(exp_dir.glob("*.json")):
            with open(json_file) as f:
                result = json.load(f)

            # Keep only public fields
            clean = {k: v for k, v in result.items() if k not in STRIP_FIELDS}

            with open(out_dir / json_file.name, "w") as f:
                json.dump(clean, f, indent=2)

            total += 1

    print(f"Exported {total} results to {PUBLIC_DIR}")


if __name__ == "__main__":
    export()

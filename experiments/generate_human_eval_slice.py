#!/usr/bin/env python3
import json
import logging
from pathlib import Path
import random

RESULTS_DIR = Path(__file__).parent / "results" / "raw" / "exp1_governance_impact"
OUTPUT_FILE = Path(__file__).parent / "results" / "human_evaluation_slice.md"
NUM_SAMPLES = 30

def main():
    if not RESULTS_DIR.exists():
        print("Results directory not found.")
        return

    # Gather all valid scored files
    valid_files = []
    for f in RESULTS_DIR.glob("*.json"):
        with open(f) as fp:
            data = json.load(fp)
        
        if data.get("model") in ["qwen3.5:9b", "z-ai/glm-5-turbo"]:
            continue
            
        if "score" in data and data["score"] is not None:
            valid_files.append((f, data))

    if len(valid_files) < NUM_SAMPLES:
        print(f"Not enough valid scored files (found {len(valid_files)}).")
        return

    # Randomly sample
    random.seed(42) # For reproducibility of the slice
    sampled = random.sample(valid_files, NUM_SAMPLES)

    md = [
        "# Human Evaluation Slice (n=30)",
        "Please read each Task, the Ground Truth, and the Model Response. Then, score the response on a scale of 0-3 according to the rubric below. **Do not look at the actual LLM score until you are finished.**",
        "",
        "## Scoring Rubric",
        "- **0 (Wrong/Irrelevant):** The response fails to address the task, is factually incorrect, or breaks the core constraints.",
        "- **1 (Partial/Flawed):** The response attempts the task but contains major logic errors, misses key constraints, or fails to reach a verifiable conclusion.",
        "- **2 (Correct/Adequate):** The response correctly solves the task and follows basic constraints, but lacks depth, structural rigor, or full comparative analysis.",
        "- **3 (Excellent/Comprehensive):** The response is thoroughly reasoned, structurally explicit, flawlessly addresses all constraints, and provides a definitive, well-justified conclusion.",
        "---"
    ]

    for idx, (filepath, data) in enumerate(sampled, start=1):
        md.append(f"\n## Sample {idx} (ID: `{data['run_id']}`)")
        md.append(f"**Task Category:** {data.get('task_category', 'unknown').capitalize()}")
        md.append(f"**Condition:** {data.get('condition', 'unknown')}")
        
        # Load task text directly since the dataset only stores task_id. We need task text for the human.
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from config import TASKS_DIR
        
        cat_file = TASKS_DIR / f"{data.get('task_category', 'unknown')}.json"
        task_text = "Task text not found."
        ground_truth = "Ground truth not found."
        
        if cat_file.exists():
            with open(cat_file) as c:
                tasks = json.load(c)
                for t in tasks:
                    if t["id"] == data.get("task_id"):
                        task_text = t.get("text", "")
                        ground_truth = t.get("ground_truth", "")
                        break
        
        md.append(f"\n### Task\n> {task_text}")
        md.append(f"\n### Ground Truth / Expected Output\n> {ground_truth}")
        
        response = data.get("response", "").strip()
        md.append("\n### Model Response\n```text\n" + response[:1500] + ("\n...[truncated]" if len(response)>1500 else "") + "\n```")
        
        md.append("\n### Evaluator Input")
        md.append("- [ ] **HUMAN SCORE (0-3):** ___")
        md.append(f"- *Hidden LLM Score (phi4:14b):* `<!-- {data['score']} -->`")
        md.append("\n---")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(md))

    print(f"Generated human evaluation slice at: {OUTPUT_FILE}")
    print("Please fill out the HUMAN SCORE fields. A secondary script can then calculate the Pearson/Spearman correlation.")

if __name__ == "__main__":
    main()

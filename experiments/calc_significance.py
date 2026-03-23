#!/usr/bin/env python3
import json
import logging
from pathlib import Path
import math

RESULTS_DIR = Path(__file__).parent / "results" / "raw" / "exp1_governance_impact"

def main():
    if not RESULTS_DIR.exists():
        print("Results directory not found.")
        return

    pairs = {}
    for f in RESULTS_DIR.glob("*.json"):
        with open(f) as fp:
            data = json.load(fp)
            
        if data.get("model") == "qwen3.5:9b" or data.get("model") == "z-ai/glm-5-turbo":
            continue
            
        match_key = f"{data['task_id']}_{data['model']}_{data['topology']}"
        cond = data["condition"]
        score = data.get("score")
        
        if score is None:
            continue
            
        if match_key not in pairs:
            pairs[match_key] = {}
        pairs[match_key][cond] = score

    differences = []
    baseline_scores = []
    iot_scores = []
    
    for key, val in pairs.items():
        if "baseline" in val and "iot_l2" in val:
            b = val["baseline"]
            i = val["iot_l2"]
            baseline_scores.append(b)
            iot_scores.append(i)
            differences.append(i - b)

    n = len(differences)
    if n < 2:
        print("Not enough paired data found.")
        return

    mean_b = sum(baseline_scores) / n
    mean_i = sum(iot_scores) / n
    mean_d = sum(differences) / n

    std_b = math.sqrt(sum((x - mean_b)**2 for x in baseline_scores) / (n - 1))
    std_i = math.sqrt(sum((x - mean_i)**2 for x in iot_scores) / (n - 1))
    std_d = math.sqrt(sum((d - mean_d)**2 for d in differences) / (n - 1))
    
    uplift = ((mean_i - mean_b) / mean_b) * 100 if mean_b > 0 else 0
    t_stat = mean_d / (std_d / math.sqrt(n)) if std_d > 0 else float('inf')

    print(f"Paired T-Test Results for Exp1 (Baseline vs IoT L2):")
    print(f"N pairs:       {n}")
    print(f"Baseline Mean: {mean_b:.3f} (SD: {std_b:.3f})")
    print(f"IoT L2 Mean:   {mean_i:.3f} (SD: {std_i:.3f})")
    print(f"Mean Diff (d): {mean_d:.3f} (SD_d: {std_d:.3f})")
    print(f"Uplift:        +{uplift:.1f}%")
    print(f"T-statistic:   {t_stat:.4f}")
    
    # Critical t-value for alpha=0.05, df > 120 is ~1.96
    # p < 0.05 if |t| > 1.96
    is_significant = abs(t_stat) > 1.96
    print(f"\nResult: {'STATISTICALLY SIGNIFICANT (p < 0.05)' if is_significant else 'NOT SIGNIFICANT (p >= 0.05)'}")

if __name__ == "__main__":
    main()

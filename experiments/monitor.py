#!/usr/bin/env python3
"""Live experiment progress monitor. Refreshes every 30s."""
import json, os, time, subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime

RAW = Path(__file__).parent / "results" / "raw"

def count_dir(d):
    scored = valid = empty = total = 0
    cloud = 0
    if not d.exists(): return 0, 0, 0, 0, 0
    for f in d.glob("*.json"):
        total += 1
        data = json.load(open(f))
        if not data.get("response", ""):
            empty += 1
        elif data.get("score", -1) >= 0:
            scored += 1
            valid += 1
        else:
            valid += 1
        if data.get("backend") == "openrouter":
            cloud += 1
    return total, valid, empty, scored, cloud

def latest_timestamp(d):
    latest = None
    for f in d.glob("*.json"):
        try:
            data = json.load(open(f))
            ts = data.get("timestamp", "")
            if ts and (latest is None or ts > latest):
                latest = ts
        except: pass
    return latest

def run():
    while True:
        print("\n" * 2)
        now = datetime.now().strftime("%H:%M:%S")
        print(f"╔══════════════════════════════════════════════════════════╗")
        print(f"║  IoT LIFECYCLE EXPERIMENT MONITOR       {now}  ║")
        print(f"╠══════════════════════════════════════════════════════════╣")

        grand_total = grand_valid = grand_scored = grand_cloud = 0

        for exp in ["exp1_governance_impact", "exp5_anti_purpose", "exp8_confusion_matrix"]:
            d = RAW / exp
            total, valid, empty, scored, cloud = count_dir(d)
            grand_total += total
            grand_valid += valid
            grand_scored += scored
            grand_cloud += cloud
            pct = (scored / valid * 100) if valid > 0 else 0
            bar_len = 30
            filled = int(bar_len * scored / valid) if valid > 0 else 0
            bar = "█" * filled + "░" * (bar_len - filled)

            short = exp.replace("_", " ").replace("exp", "Exp").title()
            lt = latest_timestamp(d)
            lt_short = lt[11:19] if lt else "---"

            print(f"║                                                          ║")
            print(f"║  {short[:40]:<40s}            ║")
            print(f"║  Total: {total:>4d}  Valid: {valid:>4d}  Cloud: {cloud:>4d}             ║")
            print(f"║  Scored: {scored:>4d}/{valid:<4d} [{bar}] {pct:>5.1f}%  ║")
            print(f"║  Latest: {lt_short}                                         ║")

        # Grand totals
        gpct = (grand_scored / grand_valid * 100) if grand_valid > 0 else 0
        print(f"║                                                          ║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║  TOTAL: {grand_total:>4d} files | {grand_valid:>4d} valid | {grand_cloud:>4d} cloud     ║")
        print(f"║  SCORED: {grand_scored:>4d}/{grand_valid:<4d} ({gpct:.1f}%)                          ║")
        print(f"╠══════════════════════════════════════════════════════════╣")

        # Process status
        procs = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True
        ).stdout
        cloud_running = "run_cloud.py" in procs
        local_running = "run_all.py" in procs
        scoring_running = "score_results.py" in procs

        print(f"║  Cloud runner:  {'🟢 RUNNING' if cloud_running else '⚪ STOPPED'}                            ║")
        print(f"║  Local runner:  {'🟢 RUNNING' if local_running else '⚪ STOPPED'}                            ║")
        print(f"║  Scorer:        {'🟢 RUNNING' if scoring_running else '⚪ STOPPED'}                            ║")
        print(f"╚══════════════════════════════════════════════════════════╝")
        print(f"\n  Press Ctrl+C to exit")

        time.sleep(30)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nMonitor stopped.")

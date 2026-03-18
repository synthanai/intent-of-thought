#!/usr/bin/env python3
"""
Queue runner: waits for v3 sweep to finish, then launches v4 threshold experiment.
Monitors the v3 process by checking if run_slm_sweep.py is still running.
"""
import subprocess
import time
import os
import sys

EXPERIMENTS_DIR = "/Users/naveen/Documents/Documents - M1/My Books/SYNTHAI/synthai-master-repo/5-text/whitepapers/Paper-GEAR-Cognitive-Variations/3-experiments"

def is_v3_running():
    """Check if run_slm_sweep.py is still running."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "run_slm_sweep.py"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False

def main():
    print("=" * 60)
    print("  GEAR EXPERIMENT QUEUE")
    print("  Waiting for v3 sweep to complete...")
    print("  Then auto-launching v4 threshold validation")
    print("=" * 60)
    
    # Wait for v3 to finish
    check_interval = 30  # seconds
    elapsed = 0
    while is_v3_running():
        mins = elapsed // 60
        print(f"  [{mins}m] v3 still running... checking again in {check_interval}s")
        time.sleep(check_interval)
        elapsed += check_interval
    
    print(f"\n  ✅ v3 sweep completed (waited {elapsed//60}m)")
    print("  Launching v4 threshold validation in 10s...\n")
    time.sleep(10)
    
    # Launch v4
    os.chdir(EXPERIMENTS_DIR)
    print("=" * 60)
    print("  LAUNCHING: GEAR v4 Threshold Validation")
    print("=" * 60)
    os.execvp("python3", ["python3", os.path.join(EXPERIMENTS_DIR, "run_v4_threshold.py")])

if __name__ == "__main__":
    main()

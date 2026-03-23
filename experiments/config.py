"""
Experiment Configuration: Model registry, paths, and settings.
"""

import os
from pathlib import Path

# Base paths
REPO_ROOT = Path(__file__).parent.parent
EXPERIMENTS_DIR = Path(__file__).parent
TASKS_DIR = EXPERIMENTS_DIR / "tasks"
PROMPTS_DIR = EXPERIMENTS_DIR / "prompts"
RESULTS_DIR = EXPERIMENTS_DIR / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"
ANALYSIS_DIR = RESULTS_DIR / "analysis"

# Ensure output directories exist
RAW_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

# Ollama settings
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "300"))
OLLAMA_RETRIES = 3

# Model registry: 6 local models across 4 architecture families
MODELS = {
    # Tier 1: 7B (baseline)
    "mistral:latest": {
        "family": "mistral",
        "params": "7B",
        "architecture": "dense",
        "tier": 1,
        "role": "baseline",
    },
    "qwen2.5:7b": {
        "family": "qwen",
        "params": "7B",
        "architecture": "dense",
        "tier": 1,
        "role": "control",
    },
    "deepseek-r1:7b": {
        "family": "deepseek",
        "params": "7B",
        "architecture": "moe_distilled",
        "tier": 1,
        "role": "cot_native",
    },
    # Tier 2: 9-12B
    "qwen3.5:9b": {
        "family": "qwen",
        "params": "9B",
        "architecture": "dense",
        "tier": 2,
        "role": "primary",
    },
    "gemma3:12b": {
        "family": "google",
        "params": "12B",
        "architecture": "dense",
        "tier": 2,
        "role": "diversity",
    },
    # Tier 3: 14B
    "phi4:14b": {
        "family": "microsoft",
        "params": "14B",
        "architecture": "dense",
        "tier": 3,
        "role": "reasoning",
    },
}

# Judge model (used for LLM-as-judge scoring)
JUDGE_MODEL = "phi4:14b"

# Topology definitions
TOPOLOGIES = ["baseline", "cot", "tot", "got"]

# IoT governance levels
IOT_LEVELS = ["none", "l0", "l1", "l2", "l3"]

# Domains
DOMAINS = ["medical", "legal", "aviation", "financial", "cybersecurity", "education"]

# Scoring scale
SCORE_MIN = 0
SCORE_MAX = 3

# Experiment settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_NUM_PREDICT = 1024
JUDGE_TEMPERATURE = 0.3  # Lower for consistency
JUDGE_NUM_PREDICT = 256

# Logging
LOG_FILE = EXPERIMENTS_DIR / "experiment.log"

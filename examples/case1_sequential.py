"""Case Study 1: Sequential Derivation (IoT recommends CoT).

Problem: Prove that the sum of the first n odd numbers equals n squared.
"""

import sys
sys.path.insert(0, "..")

from iot import IntentOfThought, TopologySelector, DriftDetector

# Define the IoT specification
iot = IntentOfThought(
    purpose="Derive a valid proof through a sequence of logically dependent steps",
    anti_purpose="Skipping steps; assuming intermediate results; exploring alternative proof strategies when a single valid path exists",
    success_signal="Each step logically follows from the previous and the final step establishes the identity",
)

print("=== Case Study 1: Sequential Derivation ===\n")
print(iot)
print()

# Validate the specification
warnings = iot.validate()
if warnings:
    print("Warnings:", warnings)
print()

# Run topology selection
selector = TopologySelector()
recommendation = selector.select(iot, context="mathematical proof")
print(f"Primary:  {recommendation.primary}")
print(f"Fallback: {recommendation.fallback}")
print(f"Rationale: {recommendation.rationale}")
print(f"Scores: {recommendation.scores}")
print()

# Simulate drift detection during reasoning
detector = DriftDetector(iot)

reasoning_steps = [
    "We want to prove that 1 + 3 + 5 + ... + (2n-1) = n^2 by induction.",
    "Base case: when n=1, the sum is 1, and 1^2 = 1. Base case holds.",
    "Inductive step: assume the sum of the first k odd numbers equals k^2.",
    "We need to show that adding the (k+1)th odd number gives (k+1)^2.",
    "The (k+1)th odd number is 2(k+1) - 1 = 2k + 1.",
    "So k^2 + (2k + 1) = k^2 + 2k + 1 = (k+1)^2. QED.",
]

print("--- Drift Detection ---")
for step_text in reasoning_steps:
    report = detector.check(step_text)
    print(report)

print()
print(detector.summary())

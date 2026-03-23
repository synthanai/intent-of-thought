"""Case Study 3: Interconnected Analysis (IoT recommends GoT).

Problem: Analyse causal factors in hospital readmission rates,
considering interrelationships between staffing, discharge planning,
patient education, and follow-up care.
"""

import sys
sys.path.insert(0, "..")

from iot import IntentOfThought, TopologySelector, DriftDetector

# Define the IoT specification
iot = IntentOfThought(
    purpose="Map the causal relationships between all contributing factors including feedback loops and indirect effects",
    anti_purpose="Treating contributing factors as independent variables when they interact; producing a linear causal chain when the reality is a causal network",
    success_signal="A relationship map showing at least four causal factors with bidirectional dependencies and at least one feedback loop identified",
)

print("=== Case Study 3: Interconnected Analysis ===\n")
print(iot)
print()

# Run topology selection
selector = TopologySelector()
recommendation = selector.select(iot, context="systems analysis healthcare")
print(f"Primary:  {recommendation.primary}")
print(f"Fallback: {recommendation.fallback}")
print(f"Rationale: {recommendation.rationale}")
print(f"Scores: {recommendation.scores}")
print()

# Simulate drift detection, including a violation
detector = DriftDetector(iot)

reasoning_steps = [
    "Staffing levels affect discharge planning quality through workload pressure.",
    "Discharge planning affects patient education: hurried discharges mean less teaching time.",
    "Patient education affects follow-up care coordination: informed patients adhere better.",
    "Feedback loop: readmission rates increase workload, which reduces staffing capacity per patient.",
    "Treating contributing factors as independent shows staffing has the largest isolated effect.",
    "Bidirectional dependency: staffing <-> readmission creates a reinforcing loop.",
]

print("--- Drift Detection ---")
for step_text in reasoning_steps:
    report = detector.check(step_text)
    print(report)
    if report.anti_purpose_violated:
        print(f"  WARNING: {report.details}")

print()
print(detector.summary())

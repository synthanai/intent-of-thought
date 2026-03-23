"""Case Study 2: Parallel Exploration (IoT recommends ToT).

Problem: Propose three distinct UI layouts for a mobile banking app,
evaluate trade-offs, and recommend one.
"""

import sys
sys.path.insert(0, "..")

from iot import IntentOfThought, TopologySelector, DriftDetector

# Define the IoT specification
iot = IntentOfThought(
    purpose="Discover and evaluate multiple viable design alternatives before committing to a recommendation",
    anti_purpose="Committing to the first design that comes to mind without evaluating alternatives; producing variations of a single concept rather than genuinely distinct approaches",
    success_signal="At least three structurally distinct layouts with explicit trade-off analysis and a justified recommendation",
)

print("=== Case Study 2: Parallel Exploration ===\n")
print(iot)
print()

# Run topology selection
selector = TopologySelector()
recommendation = selector.select(iot, context="UI design challenge")
print(f"Primary:  {recommendation.primary}")
print(f"Fallback: {recommendation.fallback}")
print(f"Rationale: {recommendation.rationale}")
print(f"Scores: {recommendation.scores}")
print()

# Simulate drift detection
detector = DriftDetector(iot)

reasoning_steps = [
    "Layout A: Tab-based navigation with bottom bar, card-based account overview.",
    "Layout B: Sidebar navigation with collapsible menu, dashboard with widgets.",
    "Layout C: Single-scroll feed with contextual actions and floating action button.",
    "Trade-off: A is familiar but limited; B is powerful but complex; C is modern but unconventional.",
    "Recommendation: Layout A for mainstream users, with B's widget customisation as a power-user option.",
]

print("--- Drift Detection ---")
for step_text in reasoning_steps:
    report = detector.check(step_text)
    print(report)

print()
print(detector.summary())

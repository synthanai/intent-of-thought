"""Algorithm 2: Intent Drift Detection.

Monitors a reasoning trace for alignment with the stated Purpose,
Anti-Purpose violations, and Success Signal satisfaction.
"""

from dataclasses import dataclass
from iot.specification import IntentOfThought


@dataclass
class DriftReport:
    """Result of a drift check at a given reasoning step."""

    step: int
    aligned: bool
    drift_detected: bool
    anti_purpose_violated: bool
    success_signal_met: bool
    action: str
    details: str

    def __str__(self) -> str:
        status = "ALIGNED" if self.aligned else "DRIFT"
        return f"Step {self.step}: {status} | Action: {self.action}"


class DriftDetector:
    """Algorithm 2 from the IoT paper.

    Checks each reasoning step against the IoT specification
    and recommends: continue, correct, switch topology, or terminate.
    """

    def __init__(self, iot: IntentOfThought):
        self.iot = iot
        self.step_count = 0
        self.history: list[DriftReport] = []

    def check(self, reasoning_step: str) -> DriftReport:
        """Check a single reasoning step for drift.

        Step 1: Compare against Purpose (alignment)
        Step 2: Check for Anti-Purpose violation
        Step 3: Check for Success Signal satisfaction
        """
        self.step_count += 1
        step_lower = reasoning_step.lower()
        purpose_lower = self.iot.purpose.lower()
        anti_lower = self.iot.anti_purpose.lower()
        success_lower = self.iot.success_signal.lower()

        # Step 1: Check purpose alignment (simple keyword overlap)
        purpose_words = set(purpose_lower.split())
        step_words = set(step_lower.split())
        overlap = len(purpose_words & step_words)
        alignment_ratio = overlap / max(len(purpose_words), 1)
        aligned = alignment_ratio > 0.1

        # Step 2: Check anti-purpose violation
        anti_keywords = [
            phrase.strip()
            for phrase in anti_lower.split(";")
            if phrase.strip()
        ]
        if not anti_keywords:
            anti_keywords = [anti_lower]

        anti_violated = any(
            kw in step_lower for kw in anti_keywords if len(kw) > 3
        )

        # Step 3: Check success signal
        success_keywords = set(success_lower.split())
        success_overlap = len(success_keywords & step_words)
        success_met = success_overlap / max(len(success_keywords), 1) > 0.3

        # Determine action
        if anti_violated:
            action = "CORRECT: Anti-Purpose violation detected"
            details = "Reasoning has entered territory the Anti-Purpose forbids."
        elif success_met:
            action = "TERMINATE: Success Signal appears satisfied"
            details = "Reasoning output matches Success Signal criteria."
        elif not aligned:
            action = "RE-ALIGN: Reasoning may be drifting from Purpose"
            details = (
                f"Low alignment ({alignment_ratio:.0%}) with stated Purpose. "
                "Consider re-reading the IoT specification."
            )
        else:
            action = "CONTINUE: Aligned with Purpose"
            details = f"Alignment: {alignment_ratio:.0%}"

        report = DriftReport(
            step=self.step_count,
            aligned=aligned,
            drift_detected=not aligned,
            anti_purpose_violated=anti_violated,
            success_signal_met=success_met,
            action=action,
            details=details,
        )
        self.history.append(report)
        return report

    def summary(self) -> str:
        """Summarise drift detection across all steps."""
        total = len(self.history)
        if total == 0:
            return "No steps checked yet."

        drifted = sum(1 for r in self.history if r.drift_detected)
        violated = sum(1 for r in self.history if r.anti_purpose_violated)
        completed = any(r.success_signal_met for r in self.history)

        return (
            f"Steps checked: {total}\n"
            f"Drift events:  {drifted}\n"
            f"Violations:    {violated}\n"
            f"Completed:     {'Yes' if completed else 'No'}"
        )

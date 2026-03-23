"""
Learning Loop: Feeds Judgement outputs back into the lifecycle.

Each failure mode produces a different type of training signal that
improves capture strategies, selection functions, and drift thresholds.

Reference: Section 4.5 of "The IoT Lifecycle" paper.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from .judgement import JudgementResult, FailureMode
from .response import ResponseAction


@dataclass
class LearningEntry:
    """A single learning event from a Judgement correction."""

    timestamp: str
    failure_mode: FailureMode
    original_purpose: str
    reconstructed_purpose: Optional[str]
    topology_used: str
    topology_recommended: Optional[str]
    domain: str
    correction_applied: str


class LearningLoop:
    """
    Accumulates Judgement corrections and produces training signals.

    Three feedback channels:
    - False Capture -> improve capture questions (refine L2/L3 elicitation)
    - False Selection -> update selection function f (new training cases)
    - False Execution -> calibrate drift threshold delta (sensitivity tuning)
    - All modes -> expand benchmark dataset
    """

    def __init__(self):
        self.history: List[LearningEntry] = []
        self.capture_rules: Dict[str, str] = {}
        self.selection_cases: List[dict] = []
        self.drift_thresholds: Dict[str, float] = {}

    def update(
        self,
        judgement: JudgementResult,
        response: ResponseAction,
        domain: str = "general",
        topology_used: str = "unknown",
    ) -> LearningEntry:
        """
        Process a Judgement result and produce learning updates.

        Args:
            judgement: Output from RetrospectiveJudgement.
            response: Output from GovernanceResponse.
            domain: Domain context for threshold calibration.
            topology_used: Which topology was used in the failed attempt.

        Returns:
            LearningEntry recording what was learned.
        """
        entry = LearningEntry(
            timestamp=datetime.now().isoformat(),
            failure_mode=judgement.failure_mode,
            original_purpose=judgement.original_spec.purpose,
            reconstructed_purpose=judgement.reconstructed_purpose,
            topology_used=topology_used,
            topology_recommended=judgement.optimal_topology,
            domain=domain,
            correction_applied=response.action,
        )

        # Dispatch to failure-mode-specific learning
        if judgement.failure_mode == FailureMode.FALSE_CAPTURE:
            self._learn_from_capture_failure(judgement, domain)
        elif judgement.failure_mode == FailureMode.FALSE_SELECTION:
            self._learn_from_selection_failure(judgement, topology_used)
        elif judgement.failure_mode == FailureMode.FALSE_EXECUTION:
            self._learn_from_execution_failure(judgement, domain)

        self.history.append(entry)
        return entry

    def _learn_from_capture_failure(
        self, judgement: JudgementResult, domain: str
    ) -> None:
        """
        False Capture -> improve capture questions.

        If medical queries with multiple symptoms default to L0/L1,
        add a rule: elevate to L2 minimum.
        """
        rule_key = f"{domain}:{judgement.original_spec.capture_mode.name}"
        self.capture_rules[rule_key] = (
            f"Elevate to L2+ for {domain} domain. "
            f"Original capture at {judgement.original_spec.capture_mode.name} "
            f"produced insufficient fidelity "
            f"(phi={judgement.original_spec.fidelity:.2f})."
        )

    def _learn_from_selection_failure(
        self, judgement: JudgementResult, topology_used: str
    ) -> None:
        """
        False Selection -> update selection function.

        Add a training case: (purpose_pattern, context) -> preferred topology.
        """
        if judgement.reconstructed_purpose and judgement.optimal_topology:
            self.selection_cases.append({
                "purpose_pattern": judgement.reconstructed_purpose,
                "context": judgement.original_spec.purpose,
                "topology_used": topology_used,
                "topology_correct": judgement.optimal_topology,
                "lesson": (
                    f"Selection function chose {topology_used} but "
                    f"{judgement.optimal_topology} was correct."
                ),
            })

    def _learn_from_execution_failure(
        self, judgement: JudgementResult, domain: str
    ) -> None:
        """
        False Execution -> calibrate drift threshold.

        Lower the threshold for safety-critical domains so drift
        is detected earlier.
        """
        safety_domains = ["medical", "aviation", "financial", "nuclear"]
        current = self.drift_thresholds.get(domain, 0.5)

        if domain in safety_domains:
            # Lower threshold for safety-critical domains
            self.drift_thresholds[domain] = max(current - 0.1, 0.2)
        else:
            # Slight adjustment for general domains
            self.drift_thresholds[domain] = max(current - 0.05, 0.3)

    def get_statistics(self) -> dict:
        """Return summary statistics of the learning history."""
        if not self.history:
            return {"total": 0}

        mode_counts = {}
        for entry in self.history:
            mode = entry.failure_mode.name
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        return {
            "total": len(self.history),
            "by_failure_mode": mode_counts,
            "capture_rules_added": len(self.capture_rules),
            "selection_cases_added": len(self.selection_cases),
            "drift_thresholds_calibrated": dict(self.drift_thresholds),
        }

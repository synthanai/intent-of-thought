"""Retrospective Judgement: backward intent reconstruction and failure diagnosis.

Given a failed reasoning trace, the original IoT spec, and the selected topology,
diagnose WHY reasoning failed using the 7-step reconstruction algorithm.

Three failure modes:
  - False Capture: intent was incorrectly specified
  - False Selection: wrong topology for correct intent
  - False Execution: correct intent + topology, but reasoning drifted
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from iot.specification import IntentOfThought
from iot.selector import TopologySelector


class FailureMode(Enum):
    FALSE_CAPTURE = "false_capture"
    FALSE_SELECTION = "false_selection"
    FALSE_EXECUTION = "false_execution"
    NO_FAILURE = "no_failure"


@dataclass
class JudgementResult:
    """Output of the Retrospective Judgement algorithm."""
    failure_mode: FailureMode
    p_reconstructed: str
    t_optimal: str
    drift_score: float
    diagnosis: str
    confidence: float
    steps: list[dict] = field(default_factory=list)

    @property
    def is_failure(self) -> bool:
        return self.failure_mode != FailureMode.NO_FAILURE


class RetrospectiveJudgement:
    """Implements the 7-step reconstruction algorithm from Section 4.3.

    Algorithm:
    1. Extract outcome O from T_result
    2. Compare O against S (quantify failure magnitude)
    3. Compare O against Anti-P (check constraint violations)
    4. Reconstruct P_actual from O + context
    5. Compare P_actual with P_captured (diagnose False Capture)
    6. Simulate f(P_actual, context) -> T_theoretical (diagnose False Selection)
    7. If P and T correct, diagnose False Execution (drift)
    """

    def __init__(self, selector: Optional[TopologySelector] = None):
        self.selector = selector or TopologySelector()

    def judge(
        self,
        original_iot: IntentOfThought,
        selected_topology: str,
        outcome: str,
        reasoning_trace: list[str],
        gold_iot: Optional[IntentOfThought] = None,
        gold_topology: Optional[str] = None,
        drift_score: float = 0.0,
        drift_threshold: float = 0.5,
        context: str = "",
    ) -> JudgementResult:
        """Run the 7-step reconstruction algorithm.

        Args:
            original_iot: The IoT triple used for this reasoning
            selected_topology: The topology that was selected
            outcome: The reasoning output
            reasoning_trace: The step-by-step reasoning trace
            gold_iot: (For benchmarking) The ground-truth IoT triple
            gold_topology: (For benchmarking) The ground-truth optimal topology
            drift_score: The drift score from monitoring
            drift_threshold: Threshold above which drift = failure
            context: Domain context string

        Returns:
            JudgementResult with diagnosed failure mode
        """
        steps = []

        # Step 1: Extract outcome
        steps.append({
            "step": 1,
            "action": "Extract outcome",
            "result": outcome[:200],
        })

        # Step 2: Compare O against S (success signal)
        success_met = self._check_success(outcome, original_iot.success_signal)
        steps.append({
            "step": 2,
            "action": "Compare O against S",
            "success_signal": original_iot.success_signal,
            "met": success_met,
        })

        if success_met and drift_score < drift_threshold:
            return JudgementResult(
                failure_mode=FailureMode.NO_FAILURE,
                p_reconstructed=original_iot.purpose,
                t_optimal=selected_topology,
                drift_score=drift_score,
                diagnosis="Reasoning succeeded. No failure detected.",
                confidence=0.95,
                steps=steps,
            )

        # Step 3: Compare O against Anti-P (constraint violations)
        anti_p_violated = self._check_anti_purpose_violation(
            outcome, original_iot.anti_purpose
        )
        steps.append({
            "step": 3,
            "action": "Compare O against Anti-P",
            "anti_purpose": original_iot.anti_purpose,
            "violated": anti_p_violated,
        })

        # Step 4: Reconstruct P_actual
        p_reconstructed = self._reconstruct_purpose(
            outcome, context, original_iot, gold_iot
        )
        steps.append({
            "step": 4,
            "action": "Reconstruct P_actual",
            "p_captured": original_iot.purpose,
            "p_reconstructed": p_reconstructed,
        })

        # Step 5: Compare P_actual with P_captured (False Capture?)
        capture_mismatch = self._compare_purposes(
            original_iot.purpose, p_reconstructed
        )
        steps.append({
            "step": 5,
            "action": "Compare P_actual vs P_captured",
            "mismatch": capture_mismatch,
        })

        if capture_mismatch:
            return JudgementResult(
                failure_mode=FailureMode.FALSE_CAPTURE,
                p_reconstructed=p_reconstructed,
                t_optimal=self._get_optimal_topology(p_reconstructed, context),
                drift_score=drift_score,
                diagnosis=(
                    f"False Capture: P_captured ('{original_iot.purpose[:80]}') "
                    f"does not match P_reconstructed ('{p_reconstructed[:80]}'). "
                    f"Elevate capture mode and re-specify intent."
                ),
                confidence=0.8,
                steps=steps,
            )

        # Step 6: Simulate f(P_actual, context) -> T_theoretical
        t_optimal = self._get_optimal_topology(p_reconstructed, context)
        selection_mismatch = t_optimal != selected_topology
        steps.append({
            "step": 6,
            "action": "Simulate f(P_actual, context)",
            "t_selected": selected_topology,
            "t_optimal": t_optimal,
            "mismatch": selection_mismatch,
        })

        if selection_mismatch:
            return JudgementResult(
                failure_mode=FailureMode.FALSE_SELECTION,
                p_reconstructed=p_reconstructed,
                t_optimal=t_optimal,
                drift_score=drift_score,
                diagnosis=(
                    f"False Selection: T_selected ({selected_topology}) "
                    f"does not match T_optimal ({t_optimal}). "
                    f"Update selection function f."
                ),
                confidence=0.85,
                steps=steps,
            )

        # Step 7: If P and T correct, diagnose False Execution
        steps.append({
            "step": 7,
            "action": "Diagnose False Execution",
            "drift_score": drift_score,
            "threshold": drift_threshold,
        })

        return JudgementResult(
            failure_mode=FailureMode.FALSE_EXECUTION,
            p_reconstructed=p_reconstructed,
            t_optimal=t_optimal,
            drift_score=drift_score,
            diagnosis=(
                f"False Execution: P_captured correct, T_selected correct, "
                f"but drift detected (delta={drift_score:.2f} > theta={drift_threshold}). "
                f"Calibrate drift threshold and re-execute with higher checkpoint frequency."
            ),
            confidence=0.9,
            steps=steps,
        )

    def _check_success(self, outcome: str, success_signal: str) -> bool:
        """Check if outcome satisfies the success signal."""
        # In benchmark mode: check keyword overlap
        ss_keywords = set(success_signal.lower().split())
        outcome_keywords = set(outcome.lower().split())
        overlap = len(ss_keywords & outcome_keywords) / max(len(ss_keywords), 1)
        return overlap > 0.3

    def _check_anti_purpose_violation(self, outcome: str, anti_purpose: str) -> bool:
        """Check if outcome violates anti-purpose constraints."""
        # Simple keyword check for benchmark (LLM-based in production)
        violation_signals = ["independent", "isolation", "single", "skip", "ignore"]
        outcome_lower = outcome.lower()
        anti_lower = anti_purpose.lower()

        for signal in violation_signals:
            if signal in anti_lower and signal in outcome_lower:
                return True
        return False

    def _reconstruct_purpose(
        self,
        outcome: str,
        context: str,
        original_iot: IntentOfThought,
        gold_iot: Optional[IntentOfThought] = None,
    ) -> str:
        """Reconstruct what the purpose SHOULD have been.

        In benchmark mode with gold_iot, use the ground truth.
        Otherwise, apply selection principles (minimal change, safety priors).
        """
        if gold_iot:
            return gold_iot.purpose
        # Fallback: return original purpose (conservative)
        return original_iot.purpose

    def _compare_purposes(self, p_captured: str, p_reconstructed: str) -> bool:
        """Check if captured and reconstructed purposes diverge."""
        if p_captured == p_reconstructed:
            return False
        # Simple word overlap check
        cap_words = set(p_captured.lower().split())
        rec_words = set(p_reconstructed.lower().split())
        overlap = len(cap_words & rec_words) / max(len(cap_words | rec_words), 1)
        return overlap < 0.5  # Less than 50% overlap = mismatch

    def _get_optimal_topology(self, purpose: str, context: str) -> str:
        """Use the selector to determine optimal topology for a purpose."""
        iot = IntentOfThought(
            purpose=purpose,
            anti_purpose="Must not produce an incorrect or incomplete analysis",
            success_signal="Produce a correct and complete analysis",
        )
        rec = self.selector.select(iot, context=context)
        return rec.primary

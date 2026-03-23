"""Governance-Proportional Response: scale corrective action with intent criticality.

Five levels from silent retry to full abort, mapped from the paper's Table 3.
"""

from dataclasses import dataclass
from enum import IntEnum

from lifecycle.judge import FailureMode


class CriticalityLevel(IntEnum):
    """Intent criticality levels (Table 3)."""
    REVERSIBLE = 1     # Low-stakes, can retry
    MODERATE = 2       # Worth flagging
    STRATEGIC = 3      # Requires re-specification
    HIGH = 4           # Requires human review
    IRREVERSIBLE = 5   # Requires full abort


@dataclass
class ResponseAction:
    """The corrective action to take."""
    level: CriticalityLevel
    action: str
    description: str
    requires_human: bool = False
    halt_reasoning: bool = False


class GovernanceResponse:
    """Maps failure mode + criticality to corrective actions."""

    # Domain -> default criticality
    DOMAIN_CRITICALITY = {
        "medical": CriticalityLevel.STRATEGIC,
        "legal": CriticalityLevel.MODERATE,
        "technical": CriticalityLevel.MODERATE,
        "financial": CriticalityLevel.HIGH,
        "aviation": CriticalityLevel.HIGH,
        "default": CriticalityLevel.MODERATE,
    }

    def respond(
        self,
        failure_mode: FailureMode,
        domain: str = "default",
        criticality: CriticalityLevel | None = None,
    ) -> ResponseAction:
        """Determine the governance-proportional response.

        Args:
            failure_mode: The diagnosed failure mode
            domain: Domain context for criticality inference
            criticality: Override criticality level
        """
        level = criticality or self.DOMAIN_CRITICALITY.get(
            domain, CriticalityLevel.MODERATE
        )

        if failure_mode == FailureMode.NO_FAILURE:
            return ResponseAction(
                level=CriticalityLevel.REVERSIBLE,
                action="none",
                description="No failure detected. Proceed.",
            )

        if failure_mode == FailureMode.FALSE_CAPTURE:
            return self._respond_false_capture(level)
        elif failure_mode == FailureMode.FALSE_SELECTION:
            return self._respond_false_selection(level)
        elif failure_mode == FailureMode.FALSE_EXECUTION:
            return self._respond_false_execution(level)
        else:
            return ResponseAction(
                level=level,
                action="unknown",
                description="Unknown failure mode.",
            )

    def _respond_false_capture(self, level: CriticalityLevel) -> ResponseAction:
        """False Capture: elevate capture mode."""
        if level <= CriticalityLevel.MODERATE:
            return ResponseAction(
                level=level,
                action="elevate_capture",
                description="Elevate capture mode (e.g., L0->L2). Re-specify IoT triple.",
            )
        elif level == CriticalityLevel.STRATEGIC:
            return ResponseAction(
                level=level,
                action="halt_and_respecify",
                description="Halt reasoning. Elevate to L3 collaborative capture. Require explicit re-entry.",
                halt_reasoning=True,
            )
        else:
            return ResponseAction(
                level=level,
                action="human_respecification",
                description="Halt reasoning. Route to human expert for intent specification.",
                halt_reasoning=True,
                requires_human=True,
            )

    def _respond_false_selection(self, level: CriticalityLevel) -> ResponseAction:
        """False Selection: update selection function and re-select."""
        if level <= CriticalityLevel.MODERATE:
            return ResponseAction(
                level=level,
                action="reselect_topology",
                description="Re-run topology selection with corrected parameters.",
            )
        else:
            return ResponseAction(
                level=level,
                action="reselect_with_review",
                description="Re-select topology. Log as training case for selection function update.",
                halt_reasoning=level >= CriticalityLevel.HIGH,
                requires_human=level >= CriticalityLevel.HIGH,
            )

    def _respond_false_execution(self, level: CriticalityLevel) -> ResponseAction:
        """False Execution: calibrate drift threshold and re-execute."""
        if level <= CriticalityLevel.MODERATE:
            return ResponseAction(
                level=level,
                action="retry_with_checkpoints",
                description="Re-execute with tighter drift threshold and doubled checkpoint frequency.",
            )
        elif level == CriticalityLevel.STRATEGIC:
            return ResponseAction(
                level=level,
                action="halt_and_reanchor",
                description="Halt at checkpoint. Re-anchor to Anti-P. Resume from last valid step.",
                halt_reasoning=True,
            )
        else:
            return ResponseAction(
                level=level,
                action="escalate",
                description="Halt all reasoning. Escalate to human expert. Full audit trail logged.",
                halt_reasoning=True,
                requires_human=True,
            )

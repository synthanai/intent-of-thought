"""IoT Lifecycle: Capture, Select, Monitor, Judge, Respond, Learn.

Extends the IoT framework (Paper 1) with:
  - Capture Spectrum (L0-L4)
  - Retrospective Judgement (3 failure modes)
  - Governance-Proportional Response (5 levels)
  - Learning Loop (feedback into capture/selection/monitoring)
"""

from lifecycle.capture import CaptureSpectrum, CaptureMode
from lifecycle.judge import RetrospectiveJudgement, FailureMode
from lifecycle.respond import GovernanceResponse, CriticalityLevel
from lifecycle.runner import LifecycleRunner
from lifecycle.learning import LearningLoop

__all__ = [
    "CaptureSpectrum", "CaptureMode",
    "RetrospectiveJudgement", "FailureMode",
    "GovernanceResponse", "CriticalityLevel",
    "LifecycleRunner",
    "LearningLoop",
]

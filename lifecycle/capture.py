"""IoT Capture Spectrum: 5 modes of intent elicitation (L0-L4).

Each mode produces an IoT triple of varying fidelity.
Higher capture fidelity enables more specialised topology selection.
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from iot.specification import IntentOfThought


class CaptureMode(IntEnum):
    """The 5 capture modes from Table 2."""
    ZERO = 0        # L0: System infers from context alone
    IMPLICIT = 1    # L1: Extracted from user phrasing
    PROMPTED = 2    # L2: Structured questions elicit triple
    COLLABORATIVE = 3  # L3: Interactive refinement loop
    LEARNED = 4     # L4: Training-time internalisation


@dataclass
class CaptureResult:
    """Output of the capture process."""
    iot: IntentOfThought
    mode: CaptureMode
    fidelity: float  # phi in [0, 1]
    metadata: dict = field(default_factory=dict)

    @property
    def is_low_fidelity(self) -> bool:
        return self.fidelity < 0.5

    @property
    def should_elevate(self) -> bool:
        """Whether the system should escalate to a higher capture mode."""
        return self.fidelity < 0.4 and self.mode < CaptureMode.COLLABORATIVE


class CaptureSpectrum:
    """Implements the 5-mode Capture Spectrum.

    Each mode uses a different strategy to produce an IoT triple:
    - L0: Infers P from task text. Anti-P absent. S generic.
    - L1: Extracts P from phrasing + domain. Anti-P partial.
    - L2: Asks structured questions for P, Anti-P, S.
    - L3: Multi-turn refinement of the triple.
    - L4: Model-generated triple from training.
    """

    # Domain-specific Anti-Purpose defaults for L0/L1
    DOMAIN_ANTI_PURPOSES = {
        "medical": "Must not miss symptom interactions or contraindications",
        "legal": "Must not evaluate legal frameworks in isolation when they interact",
        "technical": "Must not diagnose issues independently when they cascade",
        "default": "Must not oversimplify the problem or ignore constraints",
    }

    # Domain-specific Success Signal defaults for L0
    DOMAIN_SUCCESS_SIGNALS = {
        "medical": "Produce a clinically sound analysis with all relevant factors considered",
        "legal": "Produce a legally defensible analysis addressing all applicable rules",
        "technical": "Produce a technically accurate analysis with implementation considerations",
        "default": "Produce a comprehensive analysis addressing the stated question",
    }

    def capture_l0(self, task: str, domain: str = "default") -> CaptureResult:
        """L0 Zero Capture: infer intent from task text alone.

        Produces low-fidelity triple. P inferred, Anti-P absent, S generic.
        """
        # Extract a rough purpose from the task text
        purpose = self._extract_purpose_from_text(task)
        anti_purpose = self.DOMAIN_ANTI_PURPOSES.get(domain, self.DOMAIN_ANTI_PURPOSES["default"])
        success_signal = self.DOMAIN_SUCCESS_SIGNALS.get(domain, self.DOMAIN_SUCCESS_SIGNALS["default"])

        iot = IntentOfThought(
            purpose=purpose,
            anti_purpose=anti_purpose,
            success_signal=success_signal,
        )

        # L0 fidelity is low: P is inferred, Anti-P is generic, S is generic
        fidelity = self._compute_fidelity(iot, CaptureMode.ZERO)

        return CaptureResult(
            iot=iot,
            mode=CaptureMode.ZERO,
            fidelity=fidelity,
            metadata={"source": "inferred", "domain": domain},
        )

    def capture_l1(self, task: str, domain: str = "default") -> CaptureResult:
        """L1 Implicit Capture: extract intent from phrasing + domain.

        Better than L0: analyses task phrasing for purpose signals.
        """
        purpose = self._extract_purpose_from_phrasing(task, domain)
        anti_purpose = self._extract_anti_purpose_from_phrasing(task, domain)
        success_signal = self._extract_success_from_phrasing(task, domain)

        iot = IntentOfThought(
            purpose=purpose,
            anti_purpose=anti_purpose,
            success_signal=success_signal,
        )

        fidelity = self._compute_fidelity(iot, CaptureMode.IMPLICIT)

        return CaptureResult(
            iot=iot,
            mode=CaptureMode.IMPLICIT,
            fidelity=fidelity,
            metadata={"source": "implicit_extraction", "domain": domain},
        )

    def capture_l2(
        self,
        task: str,
        purpose: str,
        anti_purpose: str,
        success_signal: str,
        domain: str = "default",
    ) -> CaptureResult:
        """L2 Prompted Capture: explicit triple from structured questions.

        The caller provides P, Anti-P, S directly (e.g. from a questionnaire).
        """
        iot = IntentOfThought(
            purpose=purpose,
            anti_purpose=anti_purpose,
            success_signal=success_signal,
        )

        fidelity = self._compute_fidelity(iot, CaptureMode.PROMPTED)

        return CaptureResult(
            iot=iot,
            mode=CaptureMode.PROMPTED,
            fidelity=fidelity,
            metadata={"source": "prompted", "domain": domain},
        )

    def capture_l3(
        self,
        task: str,
        purpose: str,
        anti_purpose: str,
        success_signal: str,
        refinement_rounds: int = 1,
        domain: str = "default",
    ) -> CaptureResult:
        """L3 Collaborative Capture: validated triple via refinement.

        Like L2, but with explicit refinement metadata.
        """
        iot = IntentOfThought(
            purpose=purpose,
            anti_purpose=anti_purpose,
            success_signal=success_signal,
        )

        fidelity = self._compute_fidelity(iot, CaptureMode.COLLABORATIVE)
        # Refinement rounds increase fidelity
        fidelity = min(1.0, fidelity + (refinement_rounds * 0.05))

        return CaptureResult(
            iot=iot,
            mode=CaptureMode.COLLABORATIVE,
            fidelity=fidelity,
            metadata={
                "source": "collaborative",
                "refinement_rounds": refinement_rounds,
                "domain": domain,
            },
        )

    def _extract_purpose_from_text(self, task: str) -> str:
        """L0: crude purpose extraction from task text."""
        # Simple heuristic: first sentence or first 100 chars
        sentences = task.split(".")
        return sentences[0].strip() if sentences else task[:100]

    def _extract_purpose_from_phrasing(self, task: str, domain: str) -> str:
        """L1: better purpose extraction using phrasing analysis."""
        task_lower = task.lower()

        # Detect purpose patterns
        if any(w in task_lower for w in ["analyse", "analyze", "map", "relationship"]):
            return f"Analyse the relationships and interactions described in the task"
        elif any(w in task_lower for w in ["compare", "evaluate", "choose"]):
            return f"Compare and evaluate the options presented to select the best approach"
        elif any(w in task_lower for w in ["calculate", "derive", "determine", "apply"]):
            return f"Apply the specified method step by step to reach a definitive answer"
        elif any(w in task_lower for w in ["trace", "walk through", "explain step"]):
            return f"Trace the process step by step showing all intermediate states"
        else:
            return self._extract_purpose_from_text(task)

    def _extract_anti_purpose_from_phrasing(self, task: str, domain: str) -> str:
        """L1: extract anti-purpose from phrasing + domain."""
        task_lower = task.lower()

        if any(w in task_lower for w in ["interact", "cascade", "feedback", "relationship"]):
            return "Must not treat factors independently when they interact with each other"
        elif any(w in task_lower for w in ["compare", "evaluate"]):
            return "Must not anchor on the first option evaluated or use a single criterion"
        else:
            return self.DOMAIN_ANTI_PURPOSES.get(domain, self.DOMAIN_ANTI_PURPOSES["default"])

    def _extract_success_from_phrasing(self, task: str, domain: str) -> str:
        """L1: extract success signal from phrasing + domain."""
        task_lower = task.lower()

        if any(w in task_lower for w in ["map", "graph", "network", "interaction"]):
            return "A relationship map or graph showing the identified interactions"
        elif any(w in task_lower for w in ["compare", "matrix"]):
            return "A comparison matrix with scores across all dimensions and a recommendation"
        elif any(w in task_lower for w in ["step", "trace", "calculate"]):
            return "Step-by-step derivation with all intermediate results shown"
        else:
            return self.DOMAIN_SUCCESS_SIGNALS.get(domain, self.DOMAIN_SUCCESS_SIGNALS["default"])

    def _compute_fidelity(self, iot: IntentOfThought, mode: CaptureMode) -> float:
        """Compute the fidelity score phi for a captured triple.

        Fidelity depends on:
        1. Triple completeness (are P, Anti-P, S all present and specific?)
        2. Capture mode (higher modes produce higher base fidelity)
        3. Specificity (longer, more detailed components = higher fidelity)
        """
        # Base fidelity by mode
        mode_base = {
            CaptureMode.ZERO: 0.15,
            CaptureMode.IMPLICIT: 0.35,
            CaptureMode.PROMPTED: 0.65,
            CaptureMode.COLLABORATIVE: 0.80,
            CaptureMode.LEARNED: 0.50,  # Variable
        }
        base = mode_base.get(mode, 0.2)

        # Specificity bonus: reward longer, more specific components
        warnings = iot.validate()
        specificity_penalty = len(warnings) * 0.05

        p_specificity = min(0.1, len(iot.purpose.split()) / 200)
        ap_specificity = min(0.1, len(iot.anti_purpose.split()) / 200)
        s_specificity = min(0.05, len(iot.success_signal.split()) / 200)

        fidelity = base + p_specificity + ap_specificity + s_specificity - specificity_penalty
        return max(0.0, min(1.0, fidelity))

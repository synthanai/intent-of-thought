"""IoT Specification: The three-primitive intent triple.

Defines the core data structure for Intent of Thought:
  - Purpose (P): WHY are we reasoning?
  - Anti-Purpose (P-bar): What must we AVOID?
  - Success Signal (S): HOW will we know we succeeded?
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentOfThought:
    """The IoT triple: a pre-reasoning checkpoint.

    Before selecting a reasoning topology, the agent specifies:
      purpose:       The desired outcome (WHY)
      anti_purpose:  The failure conditions (AVOID)
      success_signal: The completion criteria (HOW)

    Example:
        >>> iot = IntentOfThought(
        ...     purpose="Map causal relationships between factors",
        ...     anti_purpose="Treating factors as independent",
        ...     success_signal="Bidirectional dependencies identified"
        ... )
    """

    purpose: str
    anti_purpose: str
    success_signal: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.purpose.strip():
            raise ValueError("Purpose cannot be empty.")
        if not self.anti_purpose.strip():
            raise ValueError("Anti-Purpose cannot be empty.")
        if not self.success_signal.strip():
            raise ValueError("Success Signal cannot be empty.")

    def validate(self) -> list[str]:
        """Check for common specification issues.

        Returns a list of warnings (empty if clean).
        """
        warnings = []

        if self.purpose == self.anti_purpose:
            warnings.append("Purpose and Anti-Purpose are identical.")

        if len(self.purpose.split()) < 5:
            warnings.append("Purpose may be too vague (fewer than 5 words).")

        if len(self.anti_purpose.split()) < 5:
            warnings.append(
                "Anti-Purpose may be too vague (fewer than 5 words)."
            )

        if len(self.success_signal.split()) < 3:
            warnings.append(
                "Success Signal may be too vague (fewer than 3 words)."
            )

        return warnings

    def summary(self) -> str:
        """One-line summary of the IoT specification."""
        p_short = self.purpose[:60] + "..." if len(self.purpose) > 60 else self.purpose
        return f"IoT({p_short})"

    def __str__(self) -> str:
        return (
            f"Purpose:        {self.purpose}\n"
            f"Anti-Purpose:   {self.anti_purpose}\n"
            f"Success Signal: {self.success_signal}"
        )

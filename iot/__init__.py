"""Intent of Thought (IoT) - Reference Implementation.

A pre-reasoning governance layer for topology selection in LLM reasoning.
"""

from iot.specification import IntentOfThought
from iot.selector import TopologySelector, TopologyRecommendation
from iot.drift import DriftDetector

__all__ = [
    "IntentOfThought",
    "TopologySelector",
    "TopologyRecommendation",
    "DriftDetector",
]

__version__ = "0.1.0"

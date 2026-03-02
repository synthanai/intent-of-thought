"""Algorithm 1: Topology Selection.

Maps an IoT specification to a ranked list of recommended
reasoning topologies, following the selection table from the paper.
"""

from dataclasses import dataclass
from iot.specification import IntentOfThought


# Topology registry
TOPOLOGIES = {
    "CoT": "Chain-of-Thought: linear, sequential reasoning",
    "ToT": "Tree-of-Thought: branching, parallel exploration",
    "GoT": "Graph-of-Thoughts: networked, refinement and merging",
    "AoT": "Abstraction-of-Thought: hierarchical classification first",
    "Hybrid": "Multi-phase: combines multiple topologies sequentially",
}

# Purpose-type keywords and their topology mappings (Table 2 from paper)
PURPOSE_SIGNALS = {
    "CoT": [
        "sequential", "step-by-step", "derive", "prove", "linear",
        "deduction", "calculation", "single path", "logical chain",
        "one valid", "mathematical", "formula",
    ],
    "ToT": [
        "explore", "alternatives", "compare", "evaluate options",
        "multiple", "parallel", "trade-off", "creative", "design",
        "brainstorm", "uncertain", "discover",
    ],
    "GoT": [
        "interconnected", "feedback", "causal", "network", "loop",
        "bidirectional", "refine", "merge", "non-linear", "systems",
        "relationships", "dependencies",
    ],
    "AoT": [
        "classify", "categorise", "categorize", "type", "abstract",
        "hierarchical", "what kind", "problem type", "decompose",
    ],
    "Hybrid": [
        "multi-phase", "complex", "first classify then",
        "multiple stages", "requires different",
    ],
}

# Anti-Purpose constraints: if Anti-Purpose contains these,
# demote the corresponding topology
ANTI_PURPOSE_DEMOTIONS = {
    "CoT": [
        "premature commitment", "single path when multiple exist",
        "linear when non-linear", "ignoring alternatives",
    ],
    "ToT": [
        "unnecessary branching", "exploring when path is clear",
        "wasted computation",
    ],
    "GoT": [
        "overcomplicating", "adding connections that don't exist",
    ],
}


@dataclass
class TopologyRecommendation:
    """Result of the topology selection algorithm."""

    primary: str
    fallback: str | None
    rationale: str
    scores: dict[str, float]

    def __str__(self) -> str:
        fb = f", fallback={self.fallback}" if self.fallback else ""
        return f"Recommended: {self.primary}{fb}\n{self.rationale}"


class TopologySelector:
    """Algorithm 1 from the IoT paper.

    Takes an IoT specification and optional context,
    returns a ranked topology recommendation.
    """

    def select(
        self,
        iot: IntentOfThought,
        context: str = "",
    ) -> TopologyRecommendation:
        """Run the topology selection algorithm.

        Step 1: Extract purpose type from P
        Step 2: Match purpose type to topology (Table 2)
        Step 3: Apply Anti-Purpose constraints to filter
        Output: Ordered list of recommended topologies
        """
        # Step 1 + 2: Score each topology by keyword match
        scores: dict[str, float] = {}
        combined_text = (
            f"{iot.purpose} {iot.success_signal} {context}"
        ).lower()

        for topology, keywords in PURPOSE_SIGNALS.items():
            score = sum(
                1.0 for kw in keywords if kw in combined_text
            )
            scores[topology] = score

        # Step 3: Apply Anti-Purpose demotions
        anti_text = iot.anti_purpose.lower()
        for topology, anti_keywords in ANTI_PURPOSE_DEMOTIONS.items():
            for kw in anti_keywords:
                if kw in anti_text:
                    scores[topology] = max(0, scores.get(topology, 0) - 2.0)

        # Rank by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        primary = ranked[0][0]
        fallback = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > 0 else None

        # Generate rationale
        rationale = self._generate_rationale(primary, iot)

        return TopologyRecommendation(
            primary=primary,
            fallback=fallback,
            rationale=rationale,
            scores=scores,
        )

    def _generate_rationale(
        self, topology: str, iot: IntentOfThought
    ) -> str:
        """Generate a human-readable rationale for the selection."""
        descriptions = {
            "CoT": (
                "The Purpose indicates sequential, step-dependent "
                "reasoning where each step builds on the previous."
            ),
            "ToT": (
                "The Purpose requires exploring multiple alternatives "
                "before committing, which benefits from branching."
            ),
            "GoT": (
                "The Purpose involves interconnected factors with "
                "feedback loops, requiring a graph structure for "
                "refinement and merging."
            ),
            "AoT": (
                "The Purpose requires classifying the problem type "
                "before engaging with specifics."
            ),
            "Hybrid": (
                "The Purpose involves multiple reasoning phases, "
                "each requiring a different structural approach."
            ),
        }
        return descriptions.get(topology, f"Selected {topology}.")

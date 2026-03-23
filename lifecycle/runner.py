"""IoT Lifecycle Runner: the complete closed-loop system.

Capture -> Select -> Monitor -> Judge -> Respond -> Learn -> Capture

This module orchestrates all lifecycle phases and collects metrics
for the IoT-Bench experiments (E1-E6).
"""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from iot.specification import IntentOfThought
from iot.selector import TopologySelector, TopologyRecommendation
from lifecycle.capture import CaptureSpectrum, CaptureMode, CaptureResult
from lifecycle.judge import RetrospectiveJudgement, JudgementResult, FailureMode
from lifecycle.respond import GovernanceResponse, ResponseAction, CriticalityLevel


@dataclass
class LifecycleMetrics:
    """Metrics collected during a lifecycle run."""
    task_id: str
    domain: str
    capture_mode: CaptureMode
    capture_fidelity: float
    selected_topology: str
    gold_topology: str
    topology_correct: bool
    outcome_quality: float  # 0.0 - 1.0 (from evaluator)
    failure_mode: Optional[FailureMode] = None
    correction_applied: bool = False
    correction_success: bool = False
    total_attempts: int = 1
    total_tokens: int = 0
    elapsed_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


class LifecycleRunner:
    """Orchestrates the IoT Lifecycle for benchmark experiments.

    Usage:
        runner = LifecycleRunner()

        # E1: Capture Fidelity Gradient
        metrics = runner.run_capture_experiment(task, domain, capture_mode)

        # E5: End-to-End Lifecycle
        metrics = runner.run_full_lifecycle(task, domain, max_attempts=3)
    """

    def __init__(
        self,
        selector: Optional[TopologySelector] = None,
        capture: Optional[CaptureSpectrum] = None,
        judge: Optional[RetrospectiveJudgement] = None,
        responder: Optional[GovernanceResponse] = None,
    ):
        self.selector = selector or TopologySelector()
        self.capture = capture or CaptureSpectrum()
        self.judge = judge or RetrospectiveJudgement(self.selector)
        self.responder = responder or GovernanceResponse()

    def run_capture_experiment(
        self,
        task: dict,
        capture_mode: CaptureMode,
    ) -> LifecycleMetrics:
        """E1: Run a task at a specific capture level and measure topology accuracy.

        Args:
            task: A benchmark task dict with id, domain, optimal_topology, task, gold_iot
            capture_mode: The capture level to test (L0-L3)

        Returns:
            LifecycleMetrics with topology accuracy and fidelity
        """
        start = time.time()
        domain = task["domain"]
        gold_topology = task["optimal_topology"]
        gold_iot = task.get("gold_iot", {})

        # Capture at specified level
        if capture_mode == CaptureMode.ZERO:
            capture_result = self.capture.capture_l0(task["task"], domain)
        elif capture_mode == CaptureMode.IMPLICIT:
            capture_result = self.capture.capture_l1(task["task"], domain)
        elif capture_mode == CaptureMode.PROMPTED:
            capture_result = self.capture.capture_l2(
                task["task"],
                purpose=gold_iot.get("purpose", ""),
                anti_purpose=gold_iot.get("anti_purpose", ""),
                success_signal=gold_iot.get("success_signal", ""),
                domain=domain,
            )
        elif capture_mode == CaptureMode.COLLABORATIVE:
            capture_result = self.capture.capture_l3(
                task["task"],
                purpose=gold_iot.get("purpose", ""),
                anti_purpose=gold_iot.get("anti_purpose", ""),
                success_signal=gold_iot.get("success_signal", ""),
                refinement_rounds=2,
                domain=domain,
            )
        else:
            capture_result = self.capture.capture_l0(task["task"], domain)

        # Select topology
        recommendation = self.selector.select(
            capture_result.iot, context=f"{domain} analysis"
        )

        elapsed = (time.time() - start) * 1000

        return LifecycleMetrics(
            task_id=task["id"],
            domain=domain,
            capture_mode=capture_mode,
            capture_fidelity=capture_result.fidelity,
            selected_topology=recommendation.primary,
            gold_topology=gold_topology,
            topology_correct=(recommendation.primary == gold_topology),
            outcome_quality=0.0,  # Set by evaluator
            elapsed_ms=elapsed,
            metadata={
                "iot_purpose": capture_result.iot.purpose[:100],
                "iot_anti_purpose": capture_result.iot.anti_purpose[:100],
                "scores": recommendation.scores,
            },
        )

    def run_misselection_experiment(
        self,
        task: dict,
        forced_topology: str,
    ) -> LifecycleMetrics:
        """E2: Run a task with a forced (potentially wrong) topology."""
        domain = task["domain"]
        gold_topology = task["optimal_topology"]
        gold_iot = task.get("gold_iot", {})

        # Use L2 capture (gold IoT) to isolate topology effect
        capture_result = self.capture.capture_l2(
            task["task"],
            purpose=gold_iot.get("purpose", ""),
            anti_purpose=gold_iot.get("anti_purpose", ""),
            success_signal=gold_iot.get("success_signal", ""),
            domain=domain,
        )

        return LifecycleMetrics(
            task_id=task["id"],
            domain=domain,
            capture_mode=CaptureMode.PROMPTED,
            capture_fidelity=capture_result.fidelity,
            selected_topology=forced_topology,
            gold_topology=gold_topology,
            topology_correct=(forced_topology == gold_topology),
            outcome_quality=0.0,  # Set by evaluator
            metadata={"forced": True, "forced_topology": forced_topology},
        )

    def run_judgement_experiment(
        self,
        task: dict,
        failure_mode_to_induce: FailureMode,
    ) -> tuple[LifecycleMetrics, JudgementResult]:
        """E3: Induce a specific failure mode and test judgement accuracy."""
        domain = task["domain"]
        gold_iot_dict = task.get("gold_iot", {})
        gold_topology = task["optimal_topology"]

        gold_iot = IntentOfThought(
            purpose=gold_iot_dict.get("purpose", ""),
            anti_purpose=gold_iot_dict.get("anti_purpose", ""),
            success_signal=gold_iot_dict.get("success_signal", ""),
        )

        # Create the "wrong" IoT depending on failure mode
        if failure_mode_to_induce == FailureMode.FALSE_CAPTURE:
            # Give wrong purpose
            wrong_iot = IntentOfThought(
                purpose="Provide a general overview of the topic",
                anti_purpose=gold_iot.anti_purpose,
                success_signal=gold_iot.success_signal,
            )
            selected_topology = gold_topology  # Correct topology
            drift_score = 0.1  # No drift
        elif failure_mode_to_induce == FailureMode.FALSE_SELECTION:
            # Give correct IoT but wrong topology
            wrong_iot = gold_iot
            # Pick a wrong topology
            topologies = ["CoT", "ToT", "GoT"]
            selected_topology = next(t for t in topologies if t != gold_topology)
            drift_score = 0.1  # No drift
        else:  # FALSE_EXECUTION
            # Give correct everything but high drift
            wrong_iot = gold_iot
            selected_topology = gold_topology
            drift_score = 0.72  # Above threshold

        # Run judgement
        judgement = self.judge.judge(
            original_iot=wrong_iot,
            selected_topology=selected_topology,
            outcome="[Simulated failed outcome for benchmark]",
            reasoning_trace=["Step 1", "Step 2", "Step 3"],
            gold_iot=gold_iot,
            gold_topology=gold_topology,
            drift_score=drift_score,
            context=f"{domain} analysis",
        )

        metrics = LifecycleMetrics(
            task_id=task["id"],
            domain=domain,
            capture_mode=CaptureMode.PROMPTED,
            capture_fidelity=0.7,
            selected_topology=selected_topology,
            gold_topology=gold_topology,
            topology_correct=(selected_topology == gold_topology),
            outcome_quality=0.0,
            failure_mode=judgement.failure_mode,
            metadata={
                "induced_mode": failure_mode_to_induce.value,
                "diagnosed_mode": judgement.failure_mode.value,
                "diagnosis_correct": (
                    judgement.failure_mode == failure_mode_to_induce
                ),
            },
        )

        return metrics, judgement

    def save_results(
        self,
        metrics: list[LifecycleMetrics],
        output_path: str,
        experiment_name: str,
    ) -> None:
        """Save experiment results to JSON."""
        path = Path(output_path)
        path.mkdir(parents=True, exist_ok=True)

        results = []
        for m in metrics:
            results.append({
                "task_id": m.task_id,
                "domain": m.domain,
                "capture_mode": m.capture_mode.name if m.capture_mode else None,
                "capture_fidelity": m.capture_fidelity,
                "selected_topology": m.selected_topology,
                "gold_topology": m.gold_topology,
                "topology_correct": m.topology_correct,
                "outcome_quality": m.outcome_quality,
                "failure_mode": m.failure_mode.value if m.failure_mode else None,
                "correction_applied": m.correction_applied,
                "correction_success": m.correction_success,
                "total_attempts": m.total_attempts,
                "elapsed_ms": m.elapsed_ms,
                "metadata": m.metadata,
            })

        output_file = path / f"{experiment_name}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

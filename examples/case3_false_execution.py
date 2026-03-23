"""
Case Study 3: False Execution in Aviation Safety Assessment

An aviation safety system captures intent correctly (L3) and selects
the right topology (GoT), but reasoning drifts at step 7 from risk
assessment to compliance checklist generation.

Reference: Section 5.3 of "The IoT Lifecycle" paper.
"""

import sys
sys.path.insert(0, "..")

from lifecycle import (
    CaptureSpectrum,
    RetrospectiveJudgement,
    GovernanceResponse,
    LearningLoop,
    FailureMode,
)


def main():
    print("=" * 60)
    print("Case Study 3: False Execution: Aviation Safety")
    print("=" * 60)

    # Phase 1: CAPTURE (L3, collaborative, high fidelity)
    print("\n--- Phase 1: CAPTURE ---")
    capture = CaptureSpectrum(mode="L3", domain="aviation")
    spec = capture.elicit(
        task="Assess cascading risk factors in aircraft maintenance",
        purpose="assess cascading risk factors in aircraft maintenance decisions",
        anti_purpose="must not overlook secondary failure modes or downplay risk severity",
        success_signal="risk dependency graph with severity-weighted edges",
    )
    print(f"  Mode:         L3 (collaborative)")
    print(f"  Purpose:      {spec.purpose}")
    print(f"  Anti-Purpose: {spec.anti_purpose}")
    print(f"  Fidelity:     {spec.fidelity:.2f}")

    # Phase 2: SELECT (GoT, correct)
    print("\n--- Phase 2: SELECT ---")
    topology = "GoT"
    print(f"  Selected:     {topology} (correct for interconnected risk analysis)")

    # Phase 3: EXECUTE (drifts at step 7)
    print("\n--- Phase 3: EXECUTE ---")
    print(f"  Steps 1-6:   Correct. Risk dependency graph building.")
    print(f"    Node: 'engine wear' → edge to 'hydraulic pressure' (severity 8)")
    print(f"    Node: 'hydraulic pressure' → edge to 'landing gear' (severity 9)")
    print(f"    Node: 'maintenance interval' → edges to all three (modifier)")
    print(f"  Step 7:       DRIFT DETECTED")
    print(f"    Reasoning shifts from risk assessment to compliance checklist")
    print(f"    Topic: 'FAA 14 CFR Part 43 compliance' (related but wrong output)")
    drift_score = 0.72
    drift_threshold = 0.5
    print(f"    Drift score: {drift_score} (threshold: {drift_threshold})")

    outcome = "partial risk graph plus compliance checklist (topic drift at step 7)"

    # Phase 4: JUDGE
    print("\n--- Phase 4: JUDGE ---")
    judgement = RetrospectiveJudgement()
    result = judgement.reconstruct(
        outcome=outcome,
        iot_spec=spec,
        topology_used=topology,
        drift_score=drift_score,
        drift_threshold=drift_threshold,
        context="aviation",
    )
    print(f"  Failure Mode: {result.failure_mode.name}")
    print(f"  Drift Source: {result.drift_source}")

    # Phase 5: RESPOND (Level 4, escalate)
    print("\n--- Phase 5: RESPOND ---")
    response = GovernanceResponse(domain="aviation")
    action = response.determine(result, criticality=4)
    print(f"  Level:        {action.level} ({action.level.name})")
    print(f"  Action:       {action.action}")
    print(f"  Human:        {action.requires_human}")
    print(f"  Audit:        {action.audit_required}")

    # Phase 6: LEARN
    print("\n--- Phase 6: LEARN ---")
    loop = LearningLoop()
    entry = loop.update(result, action, domain="aviation", topology_used=topology)
    stats = loop.get_statistics()
    old_threshold = 0.5
    new_threshold = loop.drift_thresholds.get("aviation", old_threshold)
    print(f"  Drift threshold calibrated:")
    print(f"    Aviation: {old_threshold} → {new_threshold}")
    print(f"    (Lowered for safety-critical domain)")

    print(f"\n  Lifecycle:    CAPTURE(L3) → GoT → DRIFT(δ=0.72)")
    print(f"                → JUDGE(False Execution) → RESPOND(L4, escalate)")
    print(f"                → LEARN → EXECUTE(GoT, checkpointed) ✓")

    print("\n" + "=" * 60)
    print("Lifecycle complete. False Execution diagnosed and corrected.")
    print("=" * 60)


if __name__ == "__main__":
    main()

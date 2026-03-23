"""
Case Study 1: False Capture in Clinical Decision Support

A clinical triage system uses L1 (implicit) capture, which produces
a shallow purpose. The system defaults to CoT, missing interacting
symptom clusters. Retrospective Judgement diagnoses False Capture
and the Learning Loop elevates future medical queries to L2+.

Reference: Section 5.1 of "The IoT Lifecycle" paper.
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
    print("Case Study 1: False Capture: Clinical Triage")
    print("=" * 60)

    # Phase 1: CAPTURE (L1, implicit)
    print("\n--- Phase 1: CAPTURE ---")
    capture = CaptureSpectrum(mode="L1", domain="medical")
    spec = capture.elicit(
        task="Analyse this patient's symptoms",
        context="clinical_decision_support",
    )
    print(f"  Mode:         L1 (implicit)")
    print(f"  Purpose:      {spec.purpose}")
    print(f"  Anti-Purpose: {spec.anti_purpose}")
    print(f"  Fidelity:     {spec.fidelity:.2f}")
    print(f"  Elevate?      {capture.fidelity_fn.should_elevate(spec)}")

    # Phase 2: SELECT (CoT, safe default for low fidelity)
    print("\n--- Phase 2: SELECT ---")
    topology = "CoT"  # Low-fidelity capture selects safe default
    print(f"  Selected:     {topology} (safe default for phi={spec.fidelity:.2f})")

    # Phase 3: EXECUTE (produces independent list)
    print("\n--- Phase 3: EXECUTE ---")
    outcome = "linear list of independent diagnoses: anaemia, thyroid, depression, arthritis, fibromyalgia"
    print(f"  Outcome:      {outcome}")
    print(f"  Problem:      Missed lupus indicator (fatigue + joint pain interaction)")

    # Phase 4: JUDGE (Retrospective Judgement)
    print("\n--- Phase 4: JUDGE ---")
    judgement = RetrospectiveJudgement()
    result = judgement.reconstruct(
        outcome=outcome,
        iot_spec=spec,
        topology_used=topology,
        context="clinical_decision_support",
    )
    print(f"  Failure Mode: {result.failure_mode.name}")
    print(f"  Reconstructed Purpose: {result.reconstructed_purpose}")
    print(f"  Optimal Topology:      {result.optimal_topology}")
    print(f"  Candidates evaluated:  {len(result.candidates)}")

    # Phase 5: RESPOND (Level 3, halt and re-specify)
    print("\n--- Phase 5: RESPOND ---")
    response = GovernanceResponse(domain="medical")
    action = response.determine(result, criticality=3)
    print(f"  Level:        {action.level} ({action.level.name})")
    print(f"  Action:       {action.action}")
    print(f"  Capture Mode: {action.recommended_capture_mode}")
    print(f"  Audit:        {action.audit_required}")

    # Phase 6: LEARN
    print("\n--- Phase 6: LEARN ---")
    loop = LearningLoop()
    entry = loop.update(result, action, domain="medical", topology_used=topology)
    stats = loop.get_statistics()
    print(f"  Capture rules added: {stats['capture_rules_added']}")
    if loop.capture_rules:
        print(f"  New rule: {list(loop.capture_rules.values())[0]}")
    else:
        print(f"  Learning entry logged for future calibration")

    # Phase 7: RE-CAPTURE at L2
    print("\n--- Phase 7: RE-CAPTURE (improved) ---")
    capture_v2 = CaptureSpectrum(mode="L2", domain="medical")
    spec_v2 = capture_v2.elicit(
        task="Analyse this patient's symptoms",
        purpose="identify interacting symptom clusters",
        anti_purpose="must not treat symptoms as independent when they co-occur",
        success_signal="relationship map of symptom interactions with severity",
    )
    print(f"  Mode:         L2 (prompted)")
    print(f"  Purpose:      {spec_v2.purpose}")
    print(f"  Anti-Purpose: {spec_v2.anti_purpose}")
    print(f"  Fidelity:     {spec_v2.fidelity:.2f}")
    print(f"  Elevate?      {capture_v2.fidelity_fn.should_elevate(spec_v2)}")

    print(f"\n  New topology: GoT (graph-of-thought)")
    print(f"  Lifecycle:    CAPTURE(L1) → CoT → FAIL → JUDGE(False Capture)")
    print(f"                → RESPOND(L3) → LEARN → CAPTURE(L2) → GoT ✓")

    print("\n" + "=" * 60)
    print("Lifecycle complete. False Capture diagnosed and corrected.")
    print("=" * 60)


if __name__ == "__main__":
    main()

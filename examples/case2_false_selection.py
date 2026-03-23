"""
Case Study 2: False Selection in Legal Precedent Analysis

A legal research system captures intent correctly (L2) but the
selection function chooses ToT (tree-of-thought) when GoT was needed.
ToT evaluates precedents in isolation, missing contradictions
between concurrent holdings.

Reference: Section 5.2 of "The IoT Lifecycle" paper.
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
    print("Case Study 2: False Selection: Legal Precedent")
    print("=" * 60)

    # Phase 1: CAPTURE (L2, prompted, correct)
    print("\n--- Phase 1: CAPTURE ---")
    capture = CaptureSpectrum(mode="L2", domain="legal")
    spec = capture.elicit(
        task="Analyse court precedents for duty of care case",
        purpose="identify all relevant precedents and their interactions",
        anti_purpose="must not treat precedents as independent when they interact",
        success_signal="relationship graph of precedent dependencies",
    )
    print(f"  Mode:         L2 (prompted)")
    print(f"  Purpose:      {spec.purpose}")
    print(f"  Anti-Purpose: {spec.anti_purpose}")
    print(f"  Fidelity:     {spec.fidelity:.2f}")

    # Phase 2: SELECT (ToT, suboptimal)
    print("\n--- Phase 2: SELECT ---")
    topology = "ToT"
    print(f"  Selected:     {topology}")
    print(f"  Rationale:    'identify' + 'exploration' signals → tree-of-thought")
    print(f"  Problem:      ToT evaluates branches independently")

    # Phase 3: EXECUTE (misses contradictions)
    print("\n--- Phase 3: EXECUTE ---")
    outcome = (
        "independent branch analysis: "
        "Branch A (Smith v. Jones: duty of care), "
        "Branch B (Brown v. State: limits in government), "
        "Branch C (Garcia v. County: extends Brown)"
    )
    print(f"  Outcome:      {outcome[:80]}...")
    print(f"  Problem:      Smith-Brown contradiction invisible (isolated branches)")

    # Phase 4: JUDGE
    print("\n--- Phase 4: JUDGE ---")
    judgement = RetrospectiveJudgement()
    result = judgement.reconstruct(
        outcome=outcome,
        iot_spec=spec,
        topology_used=topology,
        context="legal",
    )
    print(f"  Failure Mode: {result.failure_mode.name}")
    print(f"  Reconstructed Purpose: {result.reconstructed_purpose}")
    print(f"  Optimal Topology:      {result.optimal_topology}")

    # Phase 5: RESPOND (Level 2, notify)
    print("\n--- Phase 5: RESPOND ---")
    response = GovernanceResponse(domain="legal")
    action = response.determine(result, criticality=2)
    print(f"  Level:        {action.level} ({action.level.name})")
    print(f"  Action:       {action.action}")

    # Phase 6: LEARN
    print("\n--- Phase 6: LEARN ---")
    loop = LearningLoop()
    entry = loop.update(result, action, domain="legal", topology_used=topology)
    stats = loop.get_statistics()
    print(f"  Selection cases added: {stats['selection_cases_added']}")
    if loop.selection_cases:
        case = loop.selection_cases[0]
        print(f"  Lesson: {case['lesson']}")

    print(f"\n  Lifecycle:    CAPTURE(L2) → ToT → FAIL → JUDGE(False Selection)")
    print(f"                → RESPOND(L2) → LEARN → SELECT(GoT) ✓")

    print("\n" + "=" * 60)
    print("Lifecycle complete. False Selection diagnosed and corrected.")
    print("=" * 60)


if __name__ == "__main__":
    main()

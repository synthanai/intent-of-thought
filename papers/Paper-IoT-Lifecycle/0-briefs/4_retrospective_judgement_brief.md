---
thesis: "When reasoning fails, diagnosis should determine whether intent was incorrectly captured (False Capture), the wrong topology was selected (False Selection), or execution drifted despite correct intent and topology (False Execution). Response severity should scale with intent criticality. Together, Judgement + governance correction complete the backward half of the IoT lifecycle."
data_points:
  - point: "Golovneva et al. (2023) diagnoses CoT errors at the step level (WHERE went wrong)"
    source: "research.md C1"
  - point: "Reflexion (Shinn 2023) self-evaluates but doesn't diagnose topology misselection"
    source: "research.md C2"
  - point: "Aviation incident response scales from auto-correct to manual override based on severity"
    source: "research.md A4"
  - point: "RFF (2024) uses bidirectional reasoning at step level; IoT Judgement operates at topology level"
    source: "research.md C3"
  - point: "Kalman backward smoothing reconstructs past states using future observations"
    source: "research.md A2"
gap: "No existing work provides intent-aware failure diagnosis that asks 'Was the right reasoning topology selected for this purpose?' Current debugging asks 'Which step went wrong?' but not 'Was the reasoning architecture appropriate for the stated intent?'"
---

# Section 4: Retrospective Judgement: Research Brief

## 4.1 The Backward Problem (~0.5 page)

**Given**:
- A reasoning trace T_result that failed (did not satisfy S)
- The original IoT specification (P, P̄, S)
- The selected topology T_selected

**Determine**:
- P_reconstructed: What the intent *should* have been (was P correctly captured?)
- T_optimal: Which topology would have served P_reconstructed (was T_selected correct?)
- δ_source: Where drift originated (capture error vs. execution drift vs. topology mismatch)

**Temporal symmetry connection** (SPAR #32 Enhancement 2):
- Capture (Section 3) constructs the IoT triple BEFORE reasoning: forward specification
- Judgement (this section) reconstructs what the triple SHOULD HAVE BEEN after failure: backward reconstruction
- Same conceptual operation, opposite temporal direction
- "Analogous to the distinction between Kalman prediction (forward state estimation) and Rauch-Tung-Striebel smoothing (backward state refinement, utilising all available observations)."

## 4.2 The Three Failure Modes (~0.5 page)

**TABLE** (centrepiece of the section):

| Mode | Description | Diagnosis | Correction |
|------|-------------|-----------|------------|
| **False Capture** | Intent was incorrectly specified (P_captured ≠ P_actual) | P_reconstructed ≠ P_captured | Elevate capture mode, re-specify intent |
| **False Selection** | Intent correct, wrong topology selected (T_selected ≠ T_optimal for P) | f(IoT, context) produced wrong T* | Update selection function, add training data |
| **False Execution** | Intent and topology correct, reasoning drifted (δ > threshold) | Drift detected in trace | Re-execute with IoT checkpoints at higher frequency |

## 4.3 Reconstruction Algorithm (~0.5 page)

7-step algorithm:
1. Extract final outcome O from T_result
2. Compare O against S (Success Signal): quantify failure magnitude
3. Compare O against P̄ (Anti-Purpose): check for violations
4. Reconstruct P_actual from O + context (what purpose would have led to this outcome?)
5. Compare P_actual with P_captured: diagnose False Capture
6. Simulate f(P_actual, context) → T_theoretical: compare with T_selected: diagnose False Selection
7. If P_actual ≈ P_captured and T_theoretical ≈ T_selected: diagnose False Execution (drift)

**Non-identifiability caveat** (C10, ChatGPT Report 2): Backward intent reconstruction is an ill-posed inverse problem. Many different intents can be consistent with the same failed trajectory (analogous to IRL degeneracy: many reward functions explain the same policy). Judgement must include explicit selection principles: minimal change from P_captured, safety priors, explanatory adequacy. Without these, there is no unique P_reconstructed. Acknowledge in Section 6 as limitation.

## 4.4 Governance-Proportional Response (~0.5 page)

**The gap this addresses**: No existing governance framework simultaneously targets the reasoning process, scales proportionally to risk, operates at production maturity, and generalizes across domains. Model-level frameworks (Anthropic ASL, OpenAI) govern capabilities. Organisational frameworks (ICAO SMS, CDS governance) govern external controls. The closest approaches (scalable oversight, TAO) modulate reasoning but remain research paradigms or domain-specific architectures. This section fills the gap by embedding governance-proportional response directly into the reasoning lifecycle, scaling with *intent criticality* rather than model capability or deployment context.

**TABLE** (maps intent criticality to response severity):

| Intent Criticality | Response Level | Actions | Aviation Analogue | Reasoning Governance Parallel |
|-------------------|----------------|---------|-------------------|-------------------------------|
| Level 1 (Reversible) | Silent retry | Re-execute with adjusted parameters, log for learning | Minor turbulence (autopilot adjusts) | Single-chain re-execution, no topology change |
| Level 2 (Moderate) | User notification | Flag failure, suggest alternative topology | Moderate event (alert crew) | Self-critique loop activated |
| Level 3 (Strategic) | Halt and re-specify | Pause reasoning, elevate capture mode, require explicit IoT re-entry | Significant incident (divert) | Multi-agent debate before re-execution |
| Level 4 (High) | Human escalation | Route to expert review, log full trace for audit | Serious incident (emergency landing) | Human review of reasoning plan required |
| Level 5 (Irreversible) | Abort with safeguards | Stop all reasoning, require verified human approval, create permanent audit record | Engine failure (manual override) | Full human-directed reasoning only |

**Reasoning topology modulation by level** (NEW, from RLPG research):
- Levels 1-2: governance modulates *oversight intensity* (logging, notification) but not reasoning structure
- Level 3: governance modulates *reasoning topology* (escalate from single-chain to debate/critique)
- Levels 4-5: governance modulates *agency* (shift from AI-directed to human-directed reasoning)
- This creates a three-band governance response: (1) monitoring band, (2) topology band, (3) agency band

**Comparison with existing approaches**:
- Anthropic ASL: triggers at *model capability thresholds* (static, per-model). IoT governance triggers at *task intent criticality* (dynamic, per-task).
- TAO: routes tasks among *agent tiers* based on complexity. IoT governance is structurally similar but operates within a *lifecycle* context (capture → failure → correction), not a static routing decision.
- Scalable oversight: graduates oversight using debate, critique, decomposition. IoT governance adopts these mechanisms as the *implementation* of its topology band but frames them within a governance hierarchy with explicit triggers and levels.

**Stealth note**: Use "Intent Criticality Levels," NOT "RAMP." Neutral terminology only.

## 4.5 The Learning Loop (~0.5 page, SPAR #32 Enhancement 5: expanded)

Judgement outputs feed back into the lifecycle:
- False Capture → improve Capture questions (better L2/L3 prompts)
- False Selection → update selection function f (new training cases)
- False Execution → calibrate drift threshold δ (sensitivity tuning)
- All failures → expand benchmark dataset (future Paper 3)

**MAPE-K structural analogue** (SPAR #32 Enhancement 3):
- "This feedback mechanism shares structural kinship with the MAPE-K loop in autonomic computing (Kephart & Chess, 2003): monitoring the managed system (reasoning trace) → analysing for faults (Judgement) → planning corrective action (governance response) → executing the correction. The key difference: MAPE-K adapts system-level configuration parameters; the IoT Learning Loop adapts reasoning-level governance specifications."

**Feedback diagram**: Capture → Select → Monitor → Fail → Judge → Correct → Learn → (improved) Capture
This is the closed loop. The lifecycle is not a pipeline; it is a cycle.

**Limitation: Silent Failure (A11, SPAR #33)**: Retrospective Judgement assumes failure is OBSERVABLE (the system knows reasoning failed). But when S is poorly specified (low φ), the system may not detect failure at all: the output looks plausible but is wrong. The first such failure goes undetected. The Learning Loop calibrates S over time, but bootstrapping accuracy depends on initial S quality. Acknowledge in Section 6 as a limitation.

## Writing Notes

- **Target**: 2.5 pages
- **This is the longest section** (Framework core + governance + learning loop)
- **Must include**: 7-step reconstruction algorithm, 3 failure modes table, 5-level governance table, MAPE-K citation, aviation analogies, learning loop diagram description
- **Must avoid**: em-dashes, RAMP terminology, overclaiming formal proof of temporal symmetry
- **Stealth check**: "Intent Criticality Levels" not "RAMP Levels"

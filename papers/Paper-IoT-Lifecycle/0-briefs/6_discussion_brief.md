---
thesis: "The IoT Lifecycle is a formal closed-loop system but has acknowledged limitations: no large-scale experiments, the fidelity function needs calibration, reconstruction is approximate. These limitations scope future work (TSB benchmark, training-time integration, multi-agent governance)."
data_points:
  - point: "Paper 1 proposed TSB benchmark; Paper 2 extends it with lifecycle measurement"
    source: "Paper 1 Section 5, Paper 2 NOOL"
  - point: "The lifecycle pattern (capture → govern → execute → judge → learn) is domain-general"
    source: "Paper 2 outline Section 6.3"
gap: "Limitations are honestly acknowledged. The TSB benchmark (Paper 3) will provide empirical validation."
---

# Section 6: Discussion: Research Brief

## 6.1 Limitations (~0.5 page)

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance | Case studies demonstrate lifecycle utility; TSB extensions are future work |
| Capture fidelity measurement | φ function needs empirical calibration | Proposed formally, calibration is Paper 3 (TSB) scope |
| Reconstruction accuracy | P_reconstructed may not match P_actual | Acknowledged as upper-bound estimation, not ground truth |
| Governance levels are illustrative | 5 levels may not fit all domains | Framework allows domain-specific calibration |
| Single-model focus | Lifecycle may behave differently across models | TSB benchmark will test cross-model generalisation |
| MAPE-K analogy is structural, not mathematical | Must not overclaim formal equivalence | Clearly positioned as structural analogy throughout |
| Silent failure (A11, SPAR #33) | If S is poorly specified (low φ), system may not detect failure | Learning Loop calibrates S over time; bootstrapping accuracy is a limitation |
| Epistemic asymmetry | Capture works with belief, Judgement with observation | One-sentence framing: not overclaimed as formal contribution |
| Non-identifiability (C10) | Many intents can explain the same failed trajectory (IRL degeneracy) | Judgement includes selection principles: minimal change, safety priors, explanatory adequacy |
| Kalman regime-limits (C9) | Duality is an LQG artifact, doesn't generalise automatically | Framed as structural analogy, not mathematical equivalence. Regime-limits named explicitly |

## 6.2 Completing the Research Programme (~0.25 page)

- Paper 1 (IoT): the framework (forward governance)
- Paper 2 (this paper): the lifecycle (capture + judgement)
- Paper 3 (future): TSB benchmark (empirical validation, capture fidelity measurement, judgement accuracy)
- Together: a complete, testable research programme for intent-governed reasoning

## 6.3 Broader Implications (~0.25 page)

- The lifecycle pattern (capture → govern → execute → judge → learn) is domain-general
- Connection to human decision-making: "Why are we discussing this?" before "How should we decide?" before "What went wrong?"
- Potential for training-time integration: fine-tuning models to internalise the lifecycle (L4 Learned capture)
- **Future Work seeds** (SPAR #32 Explorer + SPAR #33 assumption scope):
  - Intent compositionality (nested intents for complex tasks) → addresses A4 (single task)
  - Multi-agent intent governance (whose intent wins when agents disagree?) → addresses A6 (single model)
  - Dynamic context adaptation (intent that evolves during reasoning) → addresses A5 (static context)
  - Topology discovery (automated expansion of topology space T) → addresses A7 (known topology space)
  - Continuous topology representation → addresses A10 (discrete topologies, field-level)
  - Cross-cultural intent expression patterns → surfaced by SPAR #33 PROBE

## Writing Notes

- **Target**: 1 page
- **Tone**: Honest about limitations, forward-looking about research programme
- **Stealth check**: No proprietary terminology in future work

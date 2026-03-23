---
thesis: "Paper 2 extends the IoT framework (Paper 1) with two operational components: a 5-mode Capture Spectrum for intent elicitation and Retrospective Judgement for backward intent reconstruction. Together they complete a closed lifecycle from capture through correction."
data_points:
  - point: "Paper 1 assumed intent is given, correctly specified, and forward-only"
    source: "Paper 1 Introduction, paragraph 1"
  - point: "30+ reasoning topologies published since Wei et al. (2022)"
    source: "Paper 1 Section 1"
  - point: "No existing framework connects intent capture, failure diagnosis, and governance-proportional correction in a single lifecycle"
    source: "research.md V1"
  - point: "MAPE-K (Kephart & Chess 2003) is the closest structural analogue to a closed-loop governance system"
    source: "research.md A1"
  - point: "Kalman filter prediction/estimation duality provides a structural metaphor for capture/judgement temporal symmetry"
    source: "research.md A2, SPAR #32 Challenger"
case_studies: []
quotes:
  - text: "Which topology should be deployed for a given reasoning task, and why?"
    author: "Paper 1 Abstract"
    year: 2026
gap: "Paper 1 formalised forward governance (specify → select → monitor). Three missing operations remain: how intent enters the system (capture), how failure is diagnosed (judgement), and how response scales with criticality (governance). This paper closes the lifecycle."
enhancement_notes:
  - "SPAR #32 Enhancement 1: Open with lifecycle diagram description (Figure 1 anchor)"
  - "SPAR #32 Enhancement 2: Introduce temporal symmetry insight (Capture = forward, Judgement = backward, same operation)"
  - "SPAR #32 Enhancement 5: Mention the closed-loop nature (learning loop) as a contribution"
---

# Section 1: Introduction: Research Brief

## 1.1 The IoT Framework Recap (Self-Contained, ~1 page)

Paper 1 established IoT as a pre-reasoning governance layer:
- **IoT triple**: (Purpose P, Anti-Purpose P̄, Success Signal S)
- **Topology selection function**: f(IoT, context) → T* (ordered subset of topology space)
- **Drift detection**: δ(reasoning_trace, P) → [0, 1]
- **Key claim**: topology selection should be governed by stated purpose, not ad-hoc choice

This recap MUST be fully self-contained. A reviewer who has never read Paper 1 should understand the framework in 1 page. (SPAR #32, Protector: Kill vector #2 mitigation.)

## 1.2 The Lifecycle Gap

Paper 1 assumed:
1. Intent is **given** (someone specifies the IoT triple correctly)
2. Intent is **correct** (the triple matches the actual reasoning need)
3. Governance is **forward-only** (specify → select → monitor)

Three missing operations:
- **Capture**: How does intent enter the system? (not through prompt engineering, through architectural governance input)
- **Judgement**: When reasoning fails, how do we diagnose whether the intent was wrong, the topology was wrong, or the execution drifted?
- **Governance-Proportional Correction**: Not all failures deserve the same response. How does response severity scale with intent criticality?

**Full assumption inventory** (SPAR #33): Paper 1 carries at least 10 assumptions, not 3. A1-A3 are explicit. A4-A10 are implicit:

| # | Assumption | Paper 2 Status |
|---|-----------|----------------|
| A1 | Intent is given | ✅ Capture Spectrum (Section 3) |
| A2 | Intent is correct | ✅ False Capture diagnosis (Section 4) |
| A3 | Governance is forward-only | ✅ Learning Loop (Section 4.5) |
| A4 | Single reasoning task | ⬜ Deferred (future: compositionality) |
| A5 | Static context | ⬜ Deferred |
| A6 | Single model | ⬜ Deferred (future: multi-agent) |
| A7 | Topology space is known | 🟡 Partial (Learning Loop discovers mappings) |
| A8 | Intent is capturable as triple | 🟡 Partial (L0 acknowledges non-explicit intent) |
| A9 | Drift is detectable | ⬜ Inherited from Paper 1 |
| A10 | Topologies are discrete | ⬜ Field-level assumption |

**Draft paragraph for paper**: "Paper 1 introduced the IoT framework with three simplifying assumptions: the intent triple is given (A1), correctly specified (A2), and governance is forward-only (A3). This paper addresses all three: the Capture Spectrum (Section 3) resolves A1; Retrospective Judgement (Section 4) resolves A2 through False Capture diagnosis and A3 through backward reconstruction with proportional correction. Several additional assumptions remain: we assume a single reasoning task (A4), static context (A5), a single model (A6), and that the topology space is known (A7). We further assume that intent is capturable as a structured triple (A8), drift is detectable (A9), and topologies are discrete (A10). We partially address A7-A8 through the Learning Loop (Section 4.5) and acknowledge the remainder as scope boundaries for future work (Section 7)."

**Software engineering parallel**: Design → Build → Test → Debug → Learn is a lifecycle, not a single step. Forward governance (Design → Build → Test) is necessary but insufficient. IoT Lifecycle adds Debug (Judgement) and Learn (feedback).

**Temporal symmetry insight** (SPAR #32 Enhancement 2, SPAR #33 epistemic refinement): "We observe that Capture and Judgement are structurally symmetric operations under epistemic asymmetry: Capture constructs an intent specification from belief (prospective), while Judgement reconstructs it from observation (retrospective), a duality analogous to the prediction-estimation cycle in state estimation theory (Kalman, 1960), where forward prediction operates on estimated state and backward correction operates on measured state."

## 1.3 Contribution Statement

Three contributions:
1. **C1 (Capture Spectrum)**: We formalise a 5-mode hierarchy for intent elicitation that produces IoT triples of varying fidelity, architecturally distinct from prompt engineering.
2. **C2 (Retrospective Judgement)**: We introduce backward intent reconstruction that diagnoses three failure modes (False Capture, False Selection, False Execution) with governance-proportional correction.
3. **C3 (IoT Lifecycle)**: We present the complete closed-loop lifecycle (Capture → Select → Monitor → Judge → Learn → Capture), completing the operational cycle introduced in Paper 1.

## Section Map

Sections 2-7 overview paragraph:
- Section 2: Background (intent elicitation, failure analysis, governance proportionality)
- Section 3: The IoT Capture Spectrum
- Section 4: Retrospective Judgement
- Section 5: Case Studies (3 lifecycle demonstrations)
- Section 6: Discussion (limitations, broader implications)
- Section 7: Conclusion

## Writing Notes

- **Tone**: Arxiv CS.AI, formal third-person, neutral framing
- **Target**: 1.5 pages
- **Must avoid**: em-dashes, proprietary terminology, overclaiming backward IoT novelty
- **Must include**: IoT abbreviation disambiguation footnote (as in Paper 1)

---
thesis: "Three case studies demonstrate the complete IoT lifecycle (Capture → Select → Execute → Fail → Judge → Correct → Learn), one per failure mode: False Capture (Medical Triage), False Selection (Legal Analysis), False Execution (Aviation Safety Assessment)."
data_points:
  - point: "Paper 1 case studies showed forward success; Paper 2 case studies show failure + correction"
    source: "Paper 2 outline, Section 5"
  - point: "SPAR #32 Protector recommended replacing Case Study 3 (Strategic Planning → Aviation)"
    source: "SPAR #32, PROBE Q3"
  - point: "Aviation has ICAO-level incident response protocols, strongest governance-proportional precedent"
    source: "research.md A4"
gap: "No existing work demonstrates a complete intent-governed lifecycle from capture through failure through correction. Each case study traces the FULL loop."
---

# Section 5: Case Studies: Research Brief

## Design Rationale

- 3 case studies, one per failure mode (False Capture, False Selection, False Execution)
- Each traces the FULL lifecycle: Capture → Select → Execute → Fail → Judge → Correct → Learn
- Stealth: describe generically, no branded terminology
- **SPAR #32 recommendation**: Replace Case Study 3 (Strategic Planning) with Aviation Safety Assessment to strengthen governance-proportional narrative

## Case 1: False Capture: Medical Triage (~0.5 page)

- **Setting**: Clinical decision support, symptom analysis
- **Capture**: L1 (implicit) from clinician's query "analyse this patient's symptoms"
- **System captures**: P = "list possible diagnoses" (low fidelity, φ ≈ 0.3)
- **System selects**: CoT (sequential listing, matches shallow purpose)
- **Execution**: CoT produces a linear list but misses symptom interactions
- **Failure**: S not satisfied (missed interacting symptom cluster)
- **Judgement**: P_reconstructed = "identify interacting symptom clusters" → GoT was needed
- **Diagnosis**: False Capture (P_captured was too shallow; the actual reasoning need required interconnected analysis)
- **Correction**: Elevate to L2 (prompted), ask: "Should this analysis consider symptom interactions?" → Re-capture at higher fidelity → GoT selected
- **Learning**: Update L1 capture rules: medical queries with multiple symptoms should default to L2 prompting
- **Governance level**: Level 3 (strategic, halt and re-specify, medical context)

## Case 2: False Selection: Legal Precedent Analysis (~0.5 page)

- **Setting**: Legal research, court precedent analysis
- **Capture**: L2 (prompted), full IoT triple specified
- **P**: "Identify all relevant precedents and their interactions"
- **P̄**: "Must not treat precedents as independent when they interact"
- **S**: "Produce a relationship graph of precedent dependencies"
- **System selects**: ToT (parallel exploration of precedent space)
- **Execution**: ToT evaluates precedents independently, misses contradictions between them
- **Failure**: P̄ violated (treated precedents as independent)
- **Judgement**: T_optimal = GoT (precedents have non-linear relationships)
- **Diagnosis**: False Selection (f mapped "identify interactions" to ToT instead of GoT; selection function weighted "exploration" signal over "interconnection" signal)
- **Correction**: Update f to weight "interconnection" keywords toward GoT. Re-execute.
- **Learning**: Add training case to selection function: "precedent interactions" → GoT preference
- **Governance level**: Level 2 (moderate, user notification)

## Case 3: False Execution: Aviation Safety Assessment (~0.5 page)

**NOTE**: Replacing Strategic Planning with Aviation per SPAR #32 Protector recommendation.

- **Setting**: Aviation safety analysis, incident risk assessment
- **Capture**: L3 (collaborative), high-fidelity IoT triple (φ ≈ 0.9)
- **P**: "Assess cascading risk factors in aircraft maintenance decisions"
- **P̄**: "Must not overlook secondary failure modes or downplay risk severity"
- **S**: "Produce a risk dependency graph with severity-weighted edges"
- **System selects**: GoT (correctly, interconnected analysis)
- **Execution**: Mid-reasoning at step 7, GoT drifts from risk assessment to compliance checklist (δ exceeds threshold)
- **Failure**: Drift detected (δ = 0.72, threshold = 0.5)
- **Judgement**: P_captured = correct, T_selected = correct, but drift at step 7
- **Diagnosis**: False Execution (intent was right, topology was right, execution drifted toward lower-risk compliance reporting)
- **Correction**: Level 4 response (high, auditable): halt, checkpoint, escalate to human safety officer, re-anchor to P̄ ("must not downplay risk severity"), resume from step 6 with higher checkpoint frequency
- **Learning**: Calibrate drift threshold δ for safety-critical domains (lower threshold = earlier detection). Add to benchmark dataset.
- **Governance level**: Level 4 (high, human escalation, aviation safety context)

## Lifecycle Trace Visualisation

Each case study should include a LIFECYCLE TRACE showing the full loop:

```
CAPTURE(L1) → SELECT(CoT) → EXECUTE → FAIL(S not met) → JUDGE(False Capture) → CORRECT(L2, re-capture) → LEARN(update L1 rules) → CAPTURE(L2, improved)
```

**SPAR #32 Advocate**: The lifecycle trace IS the evidence of lifecycle completeness. Visualise as flow diagram, not just text.

## Writing Notes

- **Target**: 1.5 pages
- **Format**: Compact tabular format per case study (not narrative paragraphs)
- **Must include**: full lifecycle loop for each case, governance level applied, learning outcome
- **Stealth check**: Generic domain descriptions, no branded terminology

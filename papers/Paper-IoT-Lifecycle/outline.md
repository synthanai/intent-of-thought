# Paper Outline: The IoT Lifecycle

> **Venue**: Arxiv CS.AI + CL cross-list
> **Type**: Framework paper with lifecycle formalization and case studies
> **Target**: 10 pages + references
> **Stealth**: No proprietary branding. Use "we propose" / "the authors."
> **Companion to**: "Intent of Thought" (Paper 1)

---

## Contributions

| # | Contribution | Type |
|---|-------------|------|
| C1 | The IoT Capture Spectrum: a 5-mode hierarchy for intent elicitation that feeds the IoT triple, architecturally distinct from prompt engineering | Framework Extension |
| C2 | Retrospective Judgement: backward intent reconstruction from failed reasoning traces, with governance-proportional correction | Novel Framework |
| C3 | The IoT Lifecycle: a closed-loop system from capture through judgement, completing the operational cycle introduced in Paper 1 | Synthesis |

---

## Section 1: Introduction (1.5 pages)

### 1.1 The IoT Framework Recap
- Brief recap of Paper 1: IoT triple (P, Anti-P, S), topology selection function f, drift detection delta
- What Paper 1 assumed: intent is given, correctly specified, forward-only
- What practitioners need: how to capture intent, what to do when reasoning fails

### 1.2 The Lifecycle Gap
- Forward governance (Paper 1) is necessary but insufficient
- Three missing operations: capture (how intent enters), judgement (how failure is diagnosed), and governance (how response scales)
- Parallel to software engineering: design → build → test → debug is a lifecycle, not a single step

### 1.3 Contribution Statement
Three-bullet summary:
1. We formalise the IoT Capture Spectrum: 5 modes of intent elicitation that produce IoT triples of varying fidelity
2. We introduce Retrospective Judgement: backward intent reconstruction that diagnoses topology misselection and intent drift
3. We present the complete IoT lifecycle: a closed loop from capture to correction, with governance-proportional responses

### Research Sources
- Paper 1 (IoT framework, notation, drift detection)
- SPAR #31 verdict (scope decision: Capture + Judgement with governance subsection)

---

## Section 2: Background and Related Work (2 pages)

### 2.1 Intent Elicitation in AI Systems
- Prompt engineering and instruction tuning (Brown et al. 2020, Ouyang et al. 2022): capture *instructions*, not *governance inputs*
- Structured output formats (JSON mode, function calling): constrain *output*, not *reasoning governance*
- User intent modelling in IR (Broder 2002, Radlinski & Craswell 2017): classify *information needs*, not *reasoning topology needs*
- Conversational intent detection (NLU): classify *user actions* (book, search, ask), not *reasoning purposes*

### 2.2 Reasoning Failure Analysis
- Chain-of-Thought error analysis (Ling et al. 2023, Golovneva et al. 2023): trace-level debugging
- Interpretability and attribution (Doshi-Velez & Kim 2017): model-level explanation
- Reflexion (Shinn et al. 2023): self-evaluation but no topology diagnosis
- Process reward models (Lightman et al. 2023): step-correctness but no intent-correctness
- None ask: "Was the right reasoning topology selected for this purpose?"

### 2.3 Governance and Proportional Response
- AI safety levels (Anthropic's ASL, OpenAI safety tiers): model-level, not task-level
- Risk-aware decision making (Kahneman & Tversky 1979, prospect theory): human cognition
- Aviation incident response (ICAO taxonomy): proportional response protocols
- Medical decision governance (clinical decision support): tiered escalation
- Gap: no reasoning-level governance proportional to intent criticality

### 2.4 The Differentiation Table

**TABLE**: Extends Paper 1's Table 1 with lifecycle dimensions.

| Aspect | Prompt Engineering | IoT Capture | Failure Analysis | IoT Judgement |
|--------|-------------------|-------------|------------------|---------------|
| Input | Instructions | Governance triple (P, Anti-P, S) | Reasoning trace | Trace + original IoT spec |
| Governs | Task execution | Topology selection | Step correctness | Topology + intent correctness |
| Output | Task result | Selected topology | Error location | Reconstructed intent + diagnosis |
| Feedback | None | Fidelity gradient | Debug info | Learning loop (→ better capture) |

### Research Sources
- New literature scan needed: intent elicitation, failure diagnosis, proportional governance
- Paper 1 references (carried forward where relevant)

---

## Section 3: The IoT Capture Spectrum (2 pages)

### 3.1 The Five Modes

| Mode | Level | Mechanism | IoT Triple Fidelity | Example |
|------|-------|-----------|---------------------|---------|
| **Zero** | L0 | System infers intent from task context alone | Low: P inferred, Anti-P absent, S generic | "Solve this problem" → system guesses CoT |
| **Implicit** | L1 | Lightweight extraction from user phrasing, domain, task type | Medium-low: P extracted, Anti-P partial | "Compare these options carefully" → implicit ToT signal |
| **Prompted** | L2 | Structured questions elicit P, Anti-P, S explicitly | Medium-high: full triple, user-specified | System asks: "What must this analysis avoid?" |
| **Collaborative** | L3 | Interactive refinement loop: draft → feedback → revise | High: validated triple via dialogue | Multi-turn IoT specification with user correction |
| **Learned** | L4 | Model has internalised intent-topology mappings | Variable: training-dependent | Model auto-generates IoT triple from task embedding |

### 3.2 Formal Notation (Extending Paper 1)

- IoT_capture: mode × context → IoT_{fidelity}
- Fidelity function: phi(IoT_capture) → [0, 1] (confidence in the captured triple)
- Selection function with fidelity: f(IoT, context, phi) → T* (topology selection conditioned on capture confidence)
- When phi < threshold, elevate capture mode (L0 → L1 → L2 etc.)

### 3.3 Capture-Topology Confidence Interaction

- Low-fidelity capture (L0-L1): selection function should prefer robust, general topologies (CoT as default)
- High-fidelity capture (L3-L4): selection function can recommend specialised topologies (GoT, hybrid)
- The fidelity gradient creates a natural "capability escalation" in topology selection

### 3.4 Architectural Differentiation from Prompt Engineering

- Prompts operate at the instruction level: "do X in manner Y"
- IoT Capture operates at the governance level: "the reasoning MUST pursue P, MUST avoid Anti-P, and MUST satisfy S"
- Key test: a prompt produces a task output. An IoT Capture produces a topology selection input. Different downstream consumers, different architectural role.

### Research Sources
- New: intent elicitation literature, user modelling, NLU intent detection
- Paper 1: IoT triple notation, selection function f

---

## Section 4: Retrospective Judgement (2.5 pages)

### 4.1 The Backward Problem

Given:
- A reasoning trace T_result that failed (did not satisfy S)
- The original IoT specification (P, Anti-P, S)
- The selected topology T_selected

Determine:
- P_reconstructed: What the intent *should* have been (was P correctly captured?)
- T_optimal: Which topology would have served P_reconstructed (was T_selected correct?)
- delta_source: Where drift originated (capture error vs. execution drift vs. topology mismatch)

### 4.2 The Three Failure Modes

| Mode | Description | Diagnosis | Correction |
|------|-------------|-----------|------------|
| **False Capture** | Intent was incorrectly specified (P_captured ≠ P_actual) | P_reconstructed ≠ P_captured | Elevate capture mode, re-specify intent |
| **False Selection** | Intent was correct but wrong topology selected (T_selected ≠ T_optimal for P) | f(IoT, context) produced wrong T* | Update selection function, add training data |
| **False Execution** | Intent correct, topology correct, but reasoning drifted (delta > threshold) | Drift detected in trace | Re-execute with IoT checkpoints at higher frequency |

### 4.3 Reconstruction Algorithm

1. Extract the final outcome O from T_result
2. Compare O against S (Success Signal): quantify failure magnitude
3. Compare O against Anti-P: check for Anti-Purpose violations
4. Reconstruct P_actual from O + context (what purpose would have led to this outcome?)
5. Compare P_actual with P_captured: diagnose False Capture
6. Simulate f(P_actual, context) → T_theoretical: compare with T_selected: diagnose False Selection
7. If P_actual ≈ P_captured and T_theoretical ≈ T_selected: diagnose False Execution (drift)

### 4.4 Governance-Proportional Response

When Judgement detects failure, response scales with intent criticality:

| Intent Criticality | Response Level | Actions |
|-------------------|----------------|---------|
| Level 1 (Reversible, low-stakes) | Silent retry | Re-execute with adjusted parameters, log for learning |
| Level 2 (Moderate) | User notification | Flag failure, suggest alternative topology, offer re-specification |
| Level 3 (Strategic) | Halt and re-specify | Pause reasoning, elevate capture mode, require explicit IoT re-entry |
| Level 4 (High, auditable) | Human escalation | Route to expert review, log full trace for audit, require verification |
| Level 5 (Irreversible) | Abort with safeguards | Stop all reasoning, require verified human approval, create permanent audit record |

Connection to aviation: Level 1 = minor turbulence (auto-correct), Level 5 = engine failure (manual override, emergency protocols).

### 4.5 The Learning Loop

Judgement outputs feed back into the lifecycle:
- False Capture → improve Capture questions (better L2/L3 prompts)
- False Selection → update selection function f (new training cases)
- False Execution → calibrate drift threshold delta (sensitivity tuning)
- All failures → expand TSB benchmark dataset (future Paper 3)

### Research Sources
- New: failure analysis, blame attribution, interpretability literature
- Paper 1: drift detection (delta), Anti-Purpose (Anti-P), selection function (f)
- SPAR #31: false modes taxonomy (false discovery/process/delivery → renamed to false capture/selection/execution)

---

## Section 5: Case Studies (1.5 pages)

### 5.1 Design Rationale
- 3 case studies, each demonstrating the FULL lifecycle: Capture → Select → Execute → Fail → Judge → Correct
- One per failure mode (False Capture, False Selection, False Execution)
- Stealth: describe generically, no branded terminology

### 5.2 Case 1: False Capture (Medical Triage)
- **Capture**: L1 (implicit) from clinician's query "analyse this patient's symptoms"
- **System captures**: P = "list possible diagnoses" (low fidelity)
- **System selects**: CoT (sequential listing)
- **Failure**: CoT produces a linear list but misses symptom interactions
- **Judgement**: P_reconstructed = "identify interacting symptom clusters" → GoT was needed
- **Diagnosis**: False Capture (P_captured was too shallow, GoT not considered)
- **Correction**: Elevate to L2, ask: "Should this analysis consider symptom interactions?" → Re-capture → GoT selected

### 5.3 Case 2: False Selection (Legal Analysis)
- **Capture**: L2 (prompted), full IoT triple specified
- **P**: "Identify all relevant precedents and their interactions"
- **System selects**: ToT (parallel exploration of precedent space)
- **Failure**: ToT evaluates precedents independently, misses contradictions between them
- **Judgement**: T_optimal = GoT (precedents have non-linear relationships)
- **Diagnosis**: False Selection (f mapped "identify interactions" to ToT instead of GoT)
- **Correction**: Update f to weight "interactions" signal toward GoT. Re-execute.

### 5.4 Case 3: False Execution (Strategic Planning)
- **Capture**: L3 (collaborative), high-fidelity IoT triple
- **P**: "Evaluate market entry options with risk assessment"
- **System selects**: GoT (correctly, interconnected analysis)
- **Failure**: Mid-reasoning, GoT drifts from risk assessment to opportunity ranking (delta exceeds threshold)
- **Judgement**: P_captured = correct, T_selected = correct, but drift at step 7
- **Diagnosis**: False Execution (intent was right, topology was right, execution drifted)
- **Correction**: Level 3 response (strategic): halt, checkpoint, re-anchor to Anti-P ("must not ignore downside risks"), resume from step 6

### Research Sources
- Paper 1 case studies (for contrast: those showed forward success, these show failure + correction)
- SPAR #31: false modes framework

---

## Section 6: Discussion (1 page)

### 6.1 Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance | Case studies demonstrate lifecycle utility; TSB extensions are future work |
| Capture fidelity measurement | phi function needs empirical calibration | Proposed formally, calibration is Paper 3 (TSB) scope |
| Reconstruction accuracy | P_reconstructed may not match P_actual | Acknowledged as upper-bound estimation, not ground truth |
| Governance levels are illustrative | 5 levels may not fit all domains | Framework allows domain-specific calibration |
| Single-model focus | Lifecycle may behave differently across models | TSB benchmark will test cross-model generalisation |

### 6.2 Completing the Research Programme

- Paper 1 (IoT): the framework (forward governance)
- Paper 2 (this paper): the lifecycle (capture + judgement)
- Paper 3 (future): TSB benchmark (empirical validation)
- Together: a complete, testable research programme for intent-governed reasoning

### 6.3 Broader Implications

- The lifecycle pattern (capture → govern → execute → judge → learn) is domain-general
- Connection to human decision-making: "Why are we discussing this?" before "How should we decide?" before "What went wrong?"
- Potential for training-time integration: fine-tuning models to internalise the lifecycle

### Research Sources
- Paper 1 Section 5 (limitations, TSB proposal)
- SPAR #31: revised roadmap (Papers 1-4)

---

## Section 7: Conclusion (0.5 pages)

### Summary
- Extended IoT framework with two operational components: Capture and Judgement
- Formalised the 5-mode Capture Spectrum for intent elicitation
- Introduced Retrospective Judgement with three failure modes and governance-proportional correction
- Demonstrated the complete IoT lifecycle on 3 case studies

### Future Work
- TSB benchmark extensions: capture fidelity measurement, Judgement accuracy evaluation
- Training-time lifecycle: models that internalise capture-to-judgement
- Multi-agent IoT lifecycle: how intent governance works across collaborating agents
- Human intent structures (post-stealth): formal mapping to naturally occurring human reasoning patterns

---

## References (~40-60 citations)

### Must-Cite (NEW, in addition to Paper 1 references)

| Paper | Why |
|-------|-----|
| Brown et al. 2020 (GPT-3) | Prompt engineering baseline |
| Broder 2002 (Web search intent taxonomy) | Intent classification prior art |
| Golovneva et al. 2023 (CoT errors) | Reasoning failure analysis |
| Lightman et al. 2023 (Process reward models) | Step-level verification |
| Shinn et al. 2023 (Reflexion) | Self-evaluation (carried from P1) |
| Kahneman & Tversky 1979 (Prospect theory) | Risk-proportional cognition |
| Doshi-Velez & Kim 2017 (Interpretability) | Model explanation baseline |
| IoT Paper 1 (self-cite) | Foundation framework |

### From Paper 1 (Carried Forward)
| Paper | Why |
|-------|-----|
| Wei et al. 2022 (CoT) | Foundation of XoT |
| Yao et al. 2023 (ToT) | Key topology |
| Besta et al. 2024 (GoT) | Key topology |
| Cohen & Levesque 1990 | BDI foundation |

---

## Meta

| Dimension | Value |
|-----------|-------|
| Estimated writing time | 3-4 weeks |
| Pages | 10 + references |
| Sections | 7 |
| Tables | ~7 (differentiation, capture spectrum, failure modes, governance levels, reconstruction, case studies, limitations) |
| Figures | 2-3 (lifecycle diagram, capture-fidelity-topology chart, reconstruction flowchart) |
| SPAR source | #31, Deep Ultra, 88% confidence |

# நூல் / NOOL: The IoT Lifecycle: From Intent Capture to Retrospective Judgement

> *The Reasoning Thread: a record of INTENT (why), ABSTRACTION (what type), and CHAIN (how).*

---

## நோக்கம் / Intent (Soul: WHY)

### The Problem

1. **IoT Paper 1 formalised forward governance, but the lifecycle is incomplete**: Paper 1 defined the IoT triple (Purpose, Anti-Purpose, Success Signal) and the topology selection function f(IoT, context) → T*. But it assumed intent is *given*. In practice, users often cannot articulate their reasoning purpose, or articulate it incorrectly. And when reasoning fails, there is no formal mechanism to reconstruct what the intent *should* have been.

2. **Intent capture is treated as prompt engineering, not architectural input**: System prompts, structured output formats, and instruction tuning all capture *instructions* (what to do). None capture *governance inputs* (what the reasoning is FOR, what it must AVOID, how to judge if it succeeded). The IoT triple requires a dedicated capture mechanism that feeds topology selection, not just task execution.

3. **Failure diagnosis lacks intent-awareness**: When LLM reasoning produces incorrect or misaligned outputs, debugging focuses on the reasoning trace (which step went wrong?) or the model (which weights are miscalibrated?). Neither asks: "Was the intent correctly specified? Was the right topology selected for THIS purpose? Did the intent drift during reasoning?" Retrospective intent reconstruction is a missing diagnostic modality.

4. **Governance proportionality is absent from reasoning systems**: Not all reasoning failures deserve the same response. A low-stakes arithmetic error needs a retry. A high-stakes medical reasoning failure needs escalation, human review, and audit. But current systems apply uniform correction regardless of intent criticality. Governance-proportional response is standard in aviation and medicine but absent from LLM reasoning.

### The Purpose

A companion paper to IoT (Paper 1) that:
- **Formalises the IoT Capture Spectrum**: a 5-mode hierarchy (L0 Zero through L4 Learned) for intent elicitation that feeds the IoT triple, architecturally distinct from prompt engineering
- **Introduces Retrospective Judgement**: backward intent reconstruction from failed reasoning traces, diagnosing topology misselection and intent drift
- **Integrates governance-proportional correction**: when Judgement detects failure, response severity scales with intent criticality (from silent retry to human escalation)
- **Completes the IoT lifecycle**: Capture → Select (Paper 1) → Monitor (Paper 1) → Reconstruct → Learn → Escalate
- **Targets Arxiv CS.AI + CL cross-list**: companion to Paper 1
- **Maintains stealth framing**: no proprietary terminology

### What We're Avoiding

| Anti-Pattern | Why | How We Prevent It |
|--------------|-----|-------------------|
| **"Capture is just prompt engineering"** | Reviewers will conflate | Show architectural difference: prompts → instructions → execution vs. IoT Capture → governance triple → topology selection |
| **Standalone governance framework** | Exposes SYNTHAI patterns (RAMP) | Governance is a subsection of Judgement, using "Intent Criticality Levels" (neutral) |
| **Overclaiming backward IoT novelty** | Failure analysis exists in ML (debugging, interpretability) | Position as intent-aware diagnosis: asking WHY topology X was wrong, not just THAT step Y failed |
| **Ignoring BDI intention revision** | Bratman (1987) covers intention abandonment | Differentiate: BDI revises action-intentions, IoT Judgement reconstructs reasoning-topology-governance |
| **Disconnection from Paper 1** | Must read as a companion, not a standalone | Explicitly build on Paper 1's notation (IoT triple, f, delta, v) and extend it |
| **Building TSB in this paper** | TSB is future work (Paper 3) | Propose Capture + Judgement evaluation via case studies, seed TSB extensions |

---

## வடிவம் / Abstraction (Mind: WHAT TYPE)

### Problem Type

**DESIGN**: How should the operational lifecycle for intent-governed reasoning be structured, from initial capture through retrospective judgement, while maintaining governance proportionality?

### Key Dimensions

1. **Capture Spectrum (5 modes)**:
   - **L0 Zero**: No explicit capture. System infers intent from task context alone.
   - **L1 Implicit**: Lightweight capture from user phrasing, task type, or domain signals.
   - **L2 Prompted**: System asks structured questions to elicit P, Anti-P, S.
   - **L3 Collaborative**: Interactive refinement loop between user and system.
   - **L4 Learned**: Model has internalised intent patterns from training, auto-generates IoT triple.

2. **Capture-to-IoT mapping**: Each mode produces an IoT triple of varying fidelity. Higher modes produce more precise triples. The selection function f must handle fidelity gradients.

3. **Retrospective Judgement (Backward IoT)**: Given a failed reasoning trace and its original IoT specification:
   - **Intent Reconstruction**: What should the intent have been? (P_reconstructed, Anti-P_reconstructed, S_reconstructed)
   - **Topology Diagnosis**: Was the selected topology appropriate for the reconstructed intent?
   - **Drift Forensics**: Where did intent drift occur? Was it capture error (wrong intent specified) or execution drift (right intent, wrong path)?

4. **Governance-Proportional Correction**: Response severity indexed to intent criticality:
   - Level 1 (Reversible): Silent retry with adjusted parameters
   - Level 2 (Moderate): Flag to user, suggest alternative topology
   - Level 3 (Strategic): Halt reasoning, request intent re-specification
   - Level 4 (High): Escalate to human oversight, log for audit
   - Level 5 (Irreversible): Abort, require verified human approval before proceeding

5. **Learning Loop**: Judgement outputs feed back to improve Capture (better questions) and Selection (better f function). The lifecycle is a closed loop, not a pipeline.

### Key Relations

- Capture Spectrum **ENABLES** IoT triple generation (Paper 1 assumed this)
- Capture fidelity **DETERMINES** selection function confidence (garbage in, garbage out)
- Judgement **REQUIRES** Paper 1's drift detection (delta function) as input signal
- Governance proportionality **REQUIRES** intent criticality classification
- Learning loop **ENABLES** Capture improvement + Selection refinement (closed system)
- L4 (Learned) capture **ENABLES** future Paper 3 (training-time IoT, TSB)
- Case studies **DEMONSTRATE** lifecycle utility (not statistical validation)

---

## சங்கிலி / Chain (Body: HOW)

### Execution Path

| Phase | Activity | Priority | Status |
|-------|----------|----------|--------|
| 0. Capture Research | External research on intent elicitation, failure diagnosis, governance | P0 | ⬜ |
| 1. Prior Art: Capture | Survey intent elicitation methods (prompt design, structured inputs, user modelling) | P0 | ⬜ |
| 2. Prior Art: Failure Analysis | Survey reasoning failure diagnosis (debugging, interpretability, blame attribution) | P0 | ⬜ |
| 3. Capture Formalisation | Define 5-mode spectrum with notation, fidelity gradient, IoT triple mapping | P0 | ⬜ |
| 4. Judgement Formalisation | Define backward reconstruction, topology diagnosis, drift forensics | P0 | ⬜ |
| 5. Governance Integration | Define intent criticality levels and proportional responses as Judgement subsection | P1 | ⬜ |
| 6. Learning Loop | Define feedback paths: Judgement → Capture, Judgement → Selection | P1 | ⬜ |
| 7. Case Studies | 3 lifecycle case studies (Capture → Select → Fail → Judge → Correct) | P1 | ⬜ |
| 8. Paper Drafting | Arxiv-format paper (stealth framing), ~10 pages | P1 | ⬜ |
| 9. Submission | Submit to Arxiv (CS.AI + CL cross-list) | P2 | ⬜ |

### Success Criteria

- [ ] Capture Spectrum architecturally differentiates from prompt engineering
- [ ] 5 capture modes formally defined with notation extending Paper 1
- [ ] Retrospective Judgement introduces backward intent reconstruction as novel diagnostic
- [ ] Governance proportionality defined without exposing proprietary frameworks
- [ ] Learning loop closes the lifecycle (Capture → Select → Monitor → Judge → Learn → Capture)
- [ ] 3 case studies demonstrate full lifecycle (not just individual components)
- [ ] Paper uses neutral framing throughout (stealth verified)
- [ ] Builds explicitly on Paper 1 notation and framework
- [ ] ~10 pages, suitable for Arxiv CS.AI companion paper

### Revision Triggers

- A paper formalising "intent capture for LLM reasoning" appears → differentiate on lifecycle integration (capture alone is weaker than capture + judgement)
- Paper 1 receives reviewer feedback before Paper 2 submission → incorporate reviewer guidance
- Capture Spectrum is challenged as "prompt engineering" in review → strengthen architectural differentiation section
- Governance subsection accidentally exposes RAMP → replace all terminology with neutral "Intent Criticality Levels"

---

## Evolution History

| Version | Date | Layer Changed | What Changed |
|---------|------|---------------|--------------|
| v0.1 | 2026-03-03 | All | Initial NOOL from SPAR #31 verdict (Option D: Capture + Judgement lifecycle) |

---

> *நூல் (nool): the thread that connects, the text that records, the classic that endures.*

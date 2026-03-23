---
thesis: "Intent elicitation for reasoning governance can be formalised as a 5-mode hierarchy (L0 Zero through L4 Learned) that produces IoT triples of varying fidelity. Higher capture modes produce more precise triples, enabling more confident topology selection. This is architecturally distinct from prompt engineering."
data_points:
  - point: "Paper 1 selection function: f(IoT, context) → T*"
    source: "Paper 1 Section 3"
  - point: "IoT triple: (Purpose P, Anti-Purpose P̄, Success Signal S)"
    source: "Paper 1 Section 3"
  - point: "Broder (2002) showed intent can be hierarchically classified (info/nav/trans)"
    source: "research.md A3"
  - point: "Context engineering (2025) optimises instruction-level context, not governance-level input"
    source: "research.md B1"
gap: "No existing framework formalises the elicitation of reasoning governance input as a multi-level capability hierarchy. Prompts produce instructions. IoT Capture produces governance triples. Different type signatures, different downstream consumers."
---

# Section 3: The IoT Capture Spectrum: Research Brief

## 3.1 The Five Modes (~0.75 page)

**TABLE** (centrepiece of the section):

| Mode | Level | Mechanism | IoT Triple Fidelity | Example |
|------|-------|-----------|---------------------|---------|
| **Zero** | L0 | System infers intent from task context alone | Low: P inferred, P̄ absent, S generic | "Solve this problem" → system guesses CoT |
| **Implicit** | L1 | Lightweight extraction from user phrasing, domain, task type | Medium-low: P extracted, P̄ partial | "Compare these options carefully" → implicit ToT signal |
| **Prompted** | L2 | Structured questions elicit P, P̄, S explicitly | Medium-high: full triple, user-specified | System asks: "What must this analysis avoid?" |
| **Collaborative** | L3 | Interactive refinement loop: draft → feedback → revise | High: validated triple via dialogue | Multi-turn IoT specification with user correction |
| **Learned** | L4 | Model has internalised intent-topology mappings | Variable: training-dependent | Model auto-generates IoT triple from task embedding |

**Maturity hierarchy framing** (SPAR #32 Enhancement 4):
- Subtitle or opening sentence: "We formalise the Capture Spectrum as an intent elicitation maturity hierarchy."
- Systems start at L0 and can evolve toward L4 as they accumulate capture experience.
- This is NOT just a taxonomy (static classification). It is a progression (systems learn to capture better).

## 3.2 Formal Notation (Extending Paper 1) (~0.5 page)

- IoT_capture: mode × context → IoT_{fidelity}
- Fidelity function: φ(IoT_capture) → [0, 1] (confidence in the captured triple)
- Extended selection function: f(IoT, context, φ) → T* (topology selection conditioned on capture confidence)
- When φ < threshold_elevate: system should escalate capture mode (L0 → L1 → L2 etc.)
- This extends Paper 1's notation (f, δ) without replacing it.

## 3.3 Capture-Topology Confidence Interaction (~0.25 page)

- Low-fidelity capture (L0-L1): selection function should prefer robust, general topologies (CoT as default)
- High-fidelity capture (L3-L4): selection function can recommend specialised topologies (GoT, hybrid)
- The fidelity gradient creates a natural "capability escalation" in topology selection
- **Diagram suggestion**: (capture fidelity on x-axis, topology specialisation on y-axis, showing correlation)

## 3.4 Architectural Differentiation from Prompt Engineering (~0.5 page)

**The type signature argument** (SPAR #32, Protector: Kill vector #1 mitigation):
- Prompt P → instruction → task execution → task output O
- IoT Capture → governance triple (P, P̄, S) → topology selection input → topology T*
- Different type signatures = different architectural roles
- **Key test**: A prompt produces a task output. An IoT Capture produces a topology selection input. Different downstream consumers.

**Control surfaces rebuttal** (ChatGPT Deep Research, primary defence):
The strongest critique ("prompt engineering with extra steps") has real bite. The decisive rebuttal: L0-L4 imply different CONTROL SURFACES:
1. **Typed artefacts**: schemas, validators, versioning (IntentSpec as contract)
2. **Policies**: when to ask vs act; escalation logic (uncertainty-gated elicitation)
3. **State machines**: draft → clarify → commit (not free-form text)
4. **Security boundaries**: tool authorisation, injection resistance (OWASP LLM Top 10)
5. **Telemetry**: field-level missingness, correction rates (measurable)
6. **Training/runtime split**: L4 improvement via weights, not via prompt tweaking

"Prompts can implement any one of these, but the architectural commitment is precisely to make them first-class, inspectable, and testable."

**IntentSpec as typed IoT triple** (ChatGPT Deep Research):
- IntentSpec = { goal, constraints, preferences, success_criteria, assumptions, missing_fields, confidence, safety }
- (P, P̄, S) maps to (goal + constraints, preferences [anti-patterns], success_criteria)
- API boundary: `/intent/draft` → `/intent/clarify` → `/intent/commit` → `/plan` → `/execute`
- This makes intent a SUBSYSTEM, not prose

**Context engineering comparison**:
- 2025 trend: optimise entire context window (system prompts, history, retrieved docs)
- Still instruction-level: "what to do"
- IoT Capture is governance-level: "what the reasoning is FOR, what it must AVOID, how to judge success"

## Writing Notes

- **Target**: 2 pages
- **Must include**: formal notation extending Paper 1 (f, δ, now φ)
- **Must include**: maturity hierarchy framing (1 sentence subtitle, not full CMMI discussion)
- **Must avoid**: CMMI citation (invites unfavorable comparison)
- **Stealth check**: No proprietary terminology

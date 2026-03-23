# Section 2: Background and Related Work

This section surveys three bodies of work that converge in the IoT Lifecycle: intent elicitation in AI systems, reasoning failure diagnosis, and governance-proportional response. For each, we identify the gap that the present paper addresses.

## 2.1 Intent Elicitation in AI Systems

**Prompt engineering and context engineering.** The dominant paradigm for conditioning LLM behaviour is prompt engineering: crafting textual inputs (roles, examples, constraints, output format) that directly condition token-level generation [Brown et al., 2020; Ouyang et al., 2022]. The field has recently evolved toward *context engineering* (2025), optimising the entire context window, including system prompts, conversation history, and retrieved documents. More formally, LLM4nl2post [Endres et al., 2023] translates natural language descriptions into formal postconditions, treating intent as a source for specifications rather than a prompt in itself. STROT [Ni et al., 2025] decomposes analytical intent into a structured prompt that produces a high-level analysis plan before execution.

All of these operate at the *instruction level*: they configure what the model should do. None produce a governance input that controls how reasoning is structured.

**Pre-reasoning intent capture.** A growing body of work demonstrates that intent must be captured *before* reasoning begins. Ask-before-Plan [Zhang et al., EMNLP 2024] shows that plan satisfaction drops to 0.1% without pre-reasoning clarification. CLIPS [Zhi-Xuan et al., AAMAS 2024] performs Bayesian goal inference that formally distinguishes instructions from purpose. Liu et al. [2026] prove theoretically that scaling alone cannot fix intent mismatch, requiring architectural intervention. Zhang et al. [ICLR 2025] show that RLHF training actively discourages LLMs from asking clarifying questions, explaining why zero-capture (L0) is the dangerous default.

These works capture *task purpose*. None formalise their output as a topology governance input, and none produce a structured triple consumed by a topology selector. CLIPS infers *goals* from behaviour; IoT Capture elicits *governance specifications* from structured interaction. Ask-before-Plan clarifies *task instructions*; IoT Capture produces *topology selection inputs*. Different type signatures, different downstream consumers.

**Intent classification.** Broder [2002] introduced the foundational informational/navigational/transactional taxonomy for web search intent. Radlinski and Craswell [2017] extended this to conversational search. These classify *user search needs*, not *reasoning topology needs*.

## 2.2 Reasoning Failure Analysis

**Step-level diagnosis.** Golovneva et al. [2023] diagnose chain-of-thought errors at the step level, identifying where reasoning goes wrong within a fixed topology. PARC [Chinta et al., 2025] converts linear chains into directed acyclic graphs of premises, achieving 6-16% improvement in error detection. DeltaBench [2025] catalogues 23 error types in 8 categories for long chain-of-thought from reasoning models. Process reward models [Lightman et al., 2023; Bamba et al., ICLR 2025] verify step-level correctness but are oversensitive to superficial features.

All of these ask "which step went wrong?" None ask "was the right reasoning topology selected for this purpose?"

**Structural diagnosis.** Pathological CoT [Tutek et al., 2025] questions whether chain-of-thought is faithful to internal computation at all, distinguishing post-hoc, encoded, and internalised reasoning. The "CoT Mirage" [2025] presents evidence that CoT success is a distributional phenomenon. These works ask "is chain-of-thought itself faithful?" but not "was chain-of-thought the right topology for this intent?"

**Self-evaluation and metacognitive repair.** Reflexion [Shinn et al., 2023] adds self-evaluation loops using success/failure signals, and recent work extends this with dual-loop reflection [Nature, 2025] and multi-perspective critique [PR-CoT, 2026]. These operate *within* a fixed topology: the system reflects on its performance but does not diagnose whether the topology was appropriate for the stated purpose.

**Bidirectional reasoning.** RFF [2025] introduces "Reason from Future," using backward goal constraints combined with forward search to reduce error accumulation. This temporal pattern, reasoning forward *and* backward, parallels IoT's Capture/Judgement duality, but at a different abstraction layer: RFF reasons bidirectionally at the *step level*; IoT captures forward and judges backward at the *topology level*.

## 2.3 Governance-Proportional Response

**AI safety levels.** Anthropic's ASL tiers [RSP v3, 2025] and OpenAI's Preparedness Framework [2023-2025] define governance proportional to model *capabilities*. These operate at the *deployment level*, not the per-task reasoning level.

**Self-adaptive systems.** MAPE-K [Kephart and Chess, 2003] formalises the Monitor-Analyse-Plan-Execute-Knowledge feedback loop for autonomic computing. The IoT Learning Loop shares structural kinship with MAPE-K: monitoring the managed system (reasoning trace), analysing for faults (Judgement), planning corrective action (governance response), and executing the correction. The key difference: MAPE-K adapts *system-level configuration parameters*; the IoT Learning Loop adapts *reasoning-level governance specifications*.

**Temporal duality in control and verification.** The relationship between forward intent specification (Capture) and backward intent reconstruction (Judgement) has precedent in multiple formal traditions. In state estimation theory, the prediction-estimation cycle [Kalman, 1960] and Rauch-Tung-Striebel smoothing [1965] relate forward filtering to backward correction via opposite-direction message passing on the same state-space model. Todorov [2009] notes, however, that this duality is "an artifact of the linear-quadratic-Gaussian (LQG) setting" and requires careful reformulation for nonlinear regimes, a limitation we acknowledge.

A second formal anchor, arguably closer to our setting, comes from program verification: Dijkstra's [1976] predicate-transformer semantics distinguishes strongest postconditions (forward symbolic execution from precondition) from weakest preconditions (backward computation from postcondition). This tradition is explicitly about *specifications*, not physical state, and maps directly to Capture (what specification does this task produce?) and Judgement (what specification was needed to avoid this failure?).

We position temporal symmetry as a structural analogy grounded in these formal traditions, not as mathematical equivalence.

**Risk-proportional response in safety-critical domains.** Aviation incident response [ICAO SMM, Doc 9859] scales organisational response using a severity-probability matrix. Nuclear safety [INES, IAEA] uses seven escalation levels. In healthcare AI, TAO [2025] dynamically routes tasks among tiered agents based on complexity and safety risk, changing agentic *architecture* based on risk. TAO is the closest existing work to our governance-proportional correction, but differs in three respects: it is healthcare-specific, it selects *agents* rather than *topologies*, and it does not reason about *intent fidelity*.

No existing framework occupies the governance niche that simultaneously satisfies four properties: (1) targets the *reasoning process* itself, (2) responds *proportionally* to risk, (3) is *operationally mature* (with defined levels, triggers, and responses), and (4) is *domain-agnostic*. Consider the nearest candidates. ASL classifies model capabilities into safety tiers but says nothing about per-task reasoning. ICAO's severity matrix scales organisational response, yet applies only to aviation incidents. Structured decision governance protocols [e.g., Mintzberg et al., 1976; Nutt, 1984] provide multi-step frameworks for auditable decisions but treat every decision with equal governance weight. TAO dynamically routes among tiered agents in healthcare, coming closest to reasoning-level governance, but remains domain-specific and does not address intent fidelity. The IoT Lifecycle fills this gap: it governs reasoning topology selection proportionally to intent criticality, across domains.

Table 1b makes this gap explicit.

| Framework | Targets Reasoning | Risk-Proportional | Operational Levels | Domain-Agnostic | Governance Object |
|-----------|:-----------------:|:-----------------:|:------------------:|:---------------:|-------------------|
| ASL [Anthropic] | ✗ | ✓ | ✓ (4 tiers) | ✓ | Model capabilities |
| ICAO SMM | ✗ | ✓ | ✓ (severity matrix) | ✗ (aviation) | Organisational incidents |
| Decision governance [Mintzberg et al., 1976] | ✗ | ✓ | ✓ (multi-step) | ✓ | Decision moments |
| TAO [2025] | Partial | ✓ | ✓ (3 tiers) | ✗ (healthcare) | Agent routing |
| MAPE-K | ✗ | ✗ | ✓ (4 phases) | ✓ | System configuration |
| **IoT Lifecycle** | **✓** | **✓** | **✓ (5 levels)** | **✓** | **Reasoning topology** |

## 2.4 Summary: The Lifecycle Gap

Table 1 summarises the differentiation.

| Aspect | Prompt Engineering | IoT Capture | Failure Analysis | IoT Judgement |
|--------|-------------------|-------------|------------------|---------------|
| **Input** | Instructions | Governance triple $(P, \bar{P}, S)$ | Reasoning trace | Trace + original IoT spec |
| **Governs** | Task execution | Topology selection | Step correctness | Topology + intent correctness |
| **Output** | Task result | Selected topology $T^*$ | Error location | Reconstructed intent + diagnosis |
| **Feedback** | None | Fidelity gradient $\varphi$ | Debug info | Learning loop ($\to$ better capture) |
| **Temporal** | Forward only | Forward (prospective) | Post-hoc | Backward (retrospective) |

No existing work connects intent elicitation, reasoning failure diagnosis, and governance-proportional correction in a single lifecycle. Each component has prior art; the integration does not.

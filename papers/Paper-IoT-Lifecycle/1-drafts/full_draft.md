# The IoT Lifecycle: From Intent Capture to Retrospective Judgement

**Naveen Riaz Mohamed Kani**
ORCID: [0009-0003-9173-2425](https://orcid.org/0009-0003-9173-2425)

---

## Abstract

Large language models can reason using multiple topologies: chains, trees, graphs, and beyond. The companion paper (Intent-of-Thought, IoT) introduced a pre-reasoning governance layer that formalises topology selection through an intent triple (Purpose, Anti-Purpose, Success Signal). That framework assumed intent is given, correctly specified, and governance operates forward only. This paper relaxes all three assumptions. We introduce the IoT Capture Spectrum, a five-mode hierarchy (L0 Zero through L4 Learned) for intent elicitation that produces governance triples of varying fidelity, architecturally distinct from prompt engineering. We present Retrospective Judgement, backward intent reconstruction that diagnoses three failure modes: False Capture (intent incorrectly specified), False Selection (wrong topology for correct intent), and False Execution (correct intent and topology, but reasoning drifted). Governance-proportional correction scales response severity with intent criticality across five levels. The complete IoT Lifecycle forms a closed loop: Capture, Select, Monitor, Judge, Respond, Learn. Three case studies (clinical decision support, legal precedent analysis, aviation safety assessment) trace different failure modes through the complete lifecycle. To our knowledge, no existing framework simultaneously governs reasoning processes, responds proportionally to risk, provides operationally defined response levels, and applies domain-agnostically.

**Keywords:** Intent-of-Thought, reasoning governance, topology selection, retrospective judgement, intent capture, large language models

---

# Section 1: Introduction

The proliferation of reasoning topologies for large language models (LLMs), from chain-of-thought prompting [Wei et al., 2022] through tree-of-thought [Yao et al., 2024], graph-of-thought [Besta et al., 2024], and algorithm-of-thought [Sel et al., 2023], has created a topology selection problem: which topology should be deployed for a given reasoning task, and why? In a companion paper [Mohamed Kani, 2026], we introduced **Intent-of-Thought (IoT)**^1, a pre-reasoning governance layer that formalises this selection through an *intent triple* $(P, \bar{P}, S)$, comprising a stated Purpose, an Anti-Purpose (what reasoning must avoid), and a Success Signal (how to judge adequacy). A topology selection function $f(\text{IoT}, \text{context}) \to T^*$ maps the triple to an ordered subset of the topology space $\mathcal{T} = \{\text{CoT}, \text{ToT}, \text{GoT}, \text{AoT}, \text{Hybrid}\}$, and a drift detection function $\delta(\text{trace}, P) \to [0,1]$ monitors reasoning alignment in real time (denoted $\tau$ in the companion paper; we use $\theta$ for the drift threshold henceforth).

^1 We use IoT throughout to denote Intent-of-Thought, not to be confused with the Internet of Things or Iteration of Thought [Radha et al., 2024].

That framework, however, was presented with three simplifying assumptions: (i) the intent triple is *given* by a competent specifier, (ii) the triple *correctly* captures the actual reasoning need, and (iii) governance operates *forward only*, from specification through selection to monitoring. These assumptions define a forward pipeline: specify, select, monitor. They say nothing about how intent enters the system, what happens when reasoning fails, or how the system learns from failure. When intent is miscaptured in clinical triage, the wrong reasoning topology can miss interacting symptoms. When governance is forward-only, there is no mechanism to diagnose *why* a topology failed or to prevent recurrence.

This paper relaxes all three assumptions and introduces the operational lifecycle that completes the IoT framework. Our contributions are:

1. **The IoT Capture Spectrum** (Section 3). We formalise a five-mode hierarchy (L0 Zero through L4 Learned) for intent elicitation that produces IoT triples of varying fidelity. A fidelity function $\varphi(\text{IoT}_{\text{capture}}) \to [0,1]$ conditions the selection function, yielding $f(\text{IoT}, \text{context}, \varphi) \to T^*$. The Capture Spectrum is architecturally distinct from prompt engineering: prompts produce task instructions consumed by an executor; IoT Capture produces governance triples consumed by a topology selector. Different type signatures, different downstream consumers.

2. **Retrospective Judgement** (Section 4). When reasoning fails, we introduce backward intent reconstruction that diagnoses three failure modes: False Capture (intent was incorrectly specified), False Selection (wrong topology for correct intent), and False Execution (correct intent and topology, but reasoning drifted). Capture and Judgement are structurally symmetric under epistemic asymmetry, a duality we formalise in Section 4.1 with anchors in state estimation [Kalman, 1960] and program verification [Dijkstra, 1976]. Governance-proportional correction scales response severity with intent criticality.

3. **The IoT Lifecycle** (Figure 1). We present the complete closed-loop lifecycle: Capture $\to$ Select $\to$ Monitor $\to$ Judge $\to$ Respond $\to$ Learn $\to$ Capture. The Learning Loop feeds Judgement outputs back into improved capture strategies, updated selection functions, and calibrated drift thresholds, completing the operational cycle introduced in the companion paper.

Beyond the three explicit assumptions, the companion paper carries several implicit ones: it assumes a single reasoning task (A4), static context (A5), a single model (A6), a known topology space (A7), and that intent is capturable as a structured triple (A8). The present paper adds a further implicit assumption: intent specification is non-adversarial (A12), i.e., the specifier is not deliberately deceptive. We partially address A7 and A8 through the Learning Loop (Section 4.5), discuss degradation conditions for A12 in Section 6, and acknowledge the remainder as scope boundaries for future work (Section 7).

The remainder of this paper is organised as follows. Section 2 surveys related work on intent elicitation, reasoning failure analysis, and governance-proportional response. Section 3 presents the Capture Spectrum. Section 4 introduces Retrospective Judgement and the Learning Loop. Section 5 demonstrates the lifecycle through three case studies, each tracing a different failure mode through the complete loop. Section 6 discusses limitations and broader implications. Section 7 concludes with directions for future work.

---

# Section 2: Background and Related Work

This section surveys three bodies of work that converge in the IoT Lifecycle: intent elicitation in AI systems, reasoning failure diagnosis, and governance-proportional response. For each, we identify the gap that the present paper addresses.

## 2.1 Intent Elicitation in AI Systems

**Prompt engineering and context engineering.** The dominant paradigm for conditioning LLM behaviour is prompt engineering: crafting textual inputs (roles, examples, constraints, output format) that directly condition token-level generation [Brown et al., 2020; Ouyang et al., 2022]. The field has recently evolved toward *context engineering* (2025), optimising the entire context window, including system prompts, conversation history, and retrieved documents. More formally, LLM4nl2post [arXiv 2310.01831] translates natural language descriptions into formal postconditions, treating intent as a source for specifications rather than a prompt in itself. STROT [arXiv 2505.01636] decomposes analytical intent into a structured prompt that produces a high-level analysis plan before execution.

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

No existing framework occupies the governance niche that simultaneously satisfies four properties: (1) targets the *reasoning process* itself, (2) responds *proportionally* to risk, (3) is *operationally mature* (with defined levels, triggers, and responses), and (4) is *domain-agnostic*. Consider the nearest candidates. ASL classifies model capabilities into safety tiers but says nothing about per-task reasoning. ICAO's severity matrix scales organisational response, yet applies only to aviation incidents. DMS provides an 8-step decision protocol but treats every decision with equal governance weight. TAO dynamically routes among tiered agents in healthcare, coming closest to reasoning-level governance, but remains domain-specific and does not address intent fidelity. The IoT Lifecycle fills this gap: it governs reasoning topology selection proportionally to intent criticality, across domains.

Table 1b makes this gap explicit.

| Framework | Targets Reasoning | Risk-Proportional | Operational Levels | Domain-Agnostic | Governance Object |
|-----------|:-----------------:|:-----------------:|:------------------:|:---------------:|-------------------|
| ASL [Anthropic] | ✗ | ✓ | ✓ (4 tiers) | ✓ | Model capabilities |
| ICAO SMM | ✗ | ✓ | ✓ (severity matrix) | ✗ (aviation) | Organisational incidents |
| DMS Octagon | ✗ | ✓ | ✓ (8 steps) | ✓ | Decision moments |
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

---

# Section 3: The IoT Capture Spectrum

Intent elicitation for reasoning governance can be formalised as a five-mode hierarchy that produces IoT triples of varying fidelity. We term this the *Capture Spectrum* and frame it as an intent elicitation maturity hierarchy: systems begin at L0 and evolve toward L4 as they accumulate capture experience.

## 3.1 The Five Capture Modes

Table 2 defines the spectrum. Each mode differs in mechanism, the fidelity of the resulting IoT triple, and the architectural commitments it requires.

| Mode | Level | Mechanism | IoT Triple Fidelity | Example |
|------|-------|-----------|---------------------|---------| 
| **Zero** | L0 | System infers intent from task context alone | Low: $P$ inferred, $\bar{P}$ absent, $S$ generic | "Solve this problem" $\to$ system defaults to CoT |
| **Implicit** | L1 | Lightweight extraction from user phrasing, domain, and task type | Medium-low: $P$ extracted, $\bar{P}$ partial | "Compare these options carefully" $\to$ implicit ToT signal |
| **Prompted** | L2 | Structured questions elicit $P$, $\bar{P}$, $S$ explicitly | Medium-high: full triple, user-specified | System asks: "What must this analysis avoid?" |
| **Collaborative** | L3 | Interactive refinement loop: draft $\to$ feedback $\to$ revise | High: validated triple via dialogue | Multi-turn IoT specification with user correction |
| **Learned** | L4 | Model has internalised intent-topology mappings from training | Variable: training-dependent | Model auto-generates IoT triple from task embedding |

The hierarchy is not purely ordinal in the sense that "higher is always better." L0 is appropriate for low-stakes, familiar tasks; L3 introduces interaction cost that may be unwarranted for routine queries. The spectrum describes *available capability*, not prescribed usage. A mature system selects its capture mode based on task criticality, user context, and confidence, an observation we formalise via the fidelity function below.

This hierarchy is distinct from organisational maturity models (which assess process capability) and from intent taxonomies (which classify goal types). The Capture Spectrum classifies the *mechanism* by which a system obtains its governance input: latent inference, explicit elicitation, interactive co-construction, or training-induced priors.

## 3.2 Formal Notation

We extend the companion paper's notation as follows. Let $\text{IoT}_{\text{capture}}: \text{mode} \times \text{context} \to \text{IoT}_{\text{fidelity}}$ denote the capture function that maps a mode and context to an IoT triple with associated fidelity. The fidelity function $\varphi(\text{IoT}_{\text{capture}}) \to [0,1]$ measures confidence in the captured triple.

The extended selection function becomes:

$$f(\text{IoT}, \text{context}, \varphi) \to T^*$$

When $\varphi < \theta_{\text{elevate}}$, the system should escalate its capture mode (e.g., from L0 to L2), requesting additional intent specification before committing to topology selection. This creates a natural feedback loop between capture confidence and capture effort.

## 3.3 Capture-Topology Confidence Interaction

The fidelity gradient creates a correspondence between capture quality and topology specialisation:

- **Low-fidelity capture** (L0-L1): the selection function should prefer robust, general-purpose topologies (chain-of-thought as a safe default), because the intent signal is weak.
- **High-fidelity capture** (L3-L4): the selection function can recommend specialised topologies (graph-of-thought, hybrid strategies), because the governance triple is precise enough to justify the commitment.

This interaction implies that topology selection is not merely a function of task content but also of *how well the system understands what it is reasoning about*.

## 3.4 Architectural Differentiation from Prompt Engineering

The strongest objection to the Capture Spectrum is that it constitutes "prompt engineering with extra steps." This critique has genuine force: L0 through L3 can be implemented with a single instruction-tuned model, and L4 can be framed as prompt patterns internalised through training.

The decisive rebuttal is that L0 through L4 imply different *control surfaces*, not merely different textual instructions:

1. **Typed artefacts**: intent is materialised as a structured contract (goal, constraints, success criteria, confidence), not free-form text. Downstream tooling consumes a stable interface.
2. **Policies**: the system follows explicit rules for when to ask versus when to act, governed by fidelity thresholds rather than ad-hoc prompt logic.
3. **State machines**: capture proceeds through defined phases (draft, clarify, commit), with auditable state transitions.
4. **Security boundaries**: tool authorisation gates and confirmation checkpoints prevent premature action on low-confidence intent.
5. **Telemetry**: field-level missingness, correction rates, and capture mode distributions are measurable and monitorable.
6. **Training/runtime split**: L4 improvement occurs through model training, not prompt editing.

These architectural commitments make intent capture a *first-class, inspectable, testable subsystem*, which is the opposite of "just prompt text."

The type signature argument clarifies the distinction further. A prompt produces a task output $O$ consumed by the user. An IoT Capture produces a governance triple $(P, \bar{P}, S)$ consumed by the topology selection function $f$. Different type signatures, different downstream consumers, different architectural roles.

## 3.5 L4 Learned Capture: Training-Time Intent Internalisation

L4 is the most architecturally distinctive capture mode and the most speculative. Where L0 through L3 operate at inference time (the system extracts or elicits intent from the current interaction), L4 operates at training time: the model has internalised intent-topology mappings from prior data, enabling it to auto-generate an IoT triple from a task embedding without explicit elicitation.

**Relationship to existing training paradigms.** L4 intersects with, but differs from, three established training approaches:

1. **Reinforcement Learning from Human Feedback (RLHF) / AI Feedback (RLAIF)** [Ouyang et al., 2022; Bai et al., 2022]: These train models to produce outputs preferred by humans or AI feedback, but they do not produce governance triples. The model learns to generate better task outputs, not to specify what reasoning topology is appropriate. Zhang et al. [ICLR 2025] show that RLHF actively discourages asking clarifying questions, which means RLHF-trained models are biased toward L0 (zero capture) rather than L4 (learned capture).
2. **Constitutional AI** [Bai et al., 2022]: Embeds principles (a form of Anti-Purpose) into training. Constitutional principles are closest to $\bar{P}$ in the IoT triple: they specify what reasoning must avoid. But they do not produce $P$ (task-specific purpose) or $S$ (success criteria), and they are static across all tasks.
3. **Instruction tuning**: Trains models to follow instructions, which is L0 territory (infer intent from instruction text). L4 goes further: it trains models to *produce* an explicit governance triple as a first-order output before reasoning begins.

**The L4 paradox.** If a model can reliably auto-generate IoT triples from task embeddings, it has internalised the governance layer itself. This raises a bootstrapping question: how do you train L4 without a large corpus of (task, IoT triple, optimal topology, outcome) quadruples? The answer is the Learning Loop (Section 4.5): every correction from Retrospective Judgement produces a training signal. Over time, L0-L3 capture interactions generate the training data that enables L4. The lifecycle is its own training pipeline.

**L4 fidelity is variable.** Unlike L1-L3, where fidelity increases monotonically with capture effort, L4 fidelity depends on training distribution coverage. For task types well-represented in training, L4 may achieve $\varphi > 0.8$. For out-of-distribution tasks, L4 may produce confidently wrong triples (hallucinated intent), making runtime fidelity checking essential even for learned capture.

## 3.6 The Capture Spectrum Visual (Figure 2)

Figure 2 depicts the Capture Spectrum as a fidelity gradient, mapping each mode (L0 through L4) against the fidelity range it typically produces, the capture effort required, and the topology space it can safely govern.

The visual encodes three relationships: (1) the fidelity gradient from L0 (low, fragile) through L3 (high, validated), with L4 as a conditional branch; (2) the governance-proportional threshold $\theta_\text{elevate}$ below which the system should escalate its capture mode; and (3) the safe topology range, showing that low-fidelity capture restricts the system to robust defaults (CoT) while high-fidelity capture unlocks specialised topologies (GoT, Hybrid).


---

# Section 4: Retrospective Judgement

When reasoning fails, the question is not merely "what went wrong?" but "why was this the wrong approach?" We introduce Retrospective Judgement as the backward half of the IoT Lifecycle, reconstructing what the intent *should have been* after observing a failed outcome, diagnosing the failure mode, and scaling the corrective response proportionally to intent criticality.

## 4.1 The Backward Problem

Given a reasoning trace $T_{\text{result}}$ that did not satisfy the Success Signal $S$, the original IoT specification $(P, \bar{P}, S)$, and the selected topology $T_{\text{selected}}$, Retrospective Judgement determines:

- $P_{\text{reconstructed}}$: what the intent should have been (was $P$ correctly captured?)
- $T_{\text{optimal}}$: which topology would have served $P_{\text{reconstructed}}$ (was $T_{\text{selected}}$ correct for the actual need?)
- $\delta_{\text{source}}$: where drift originated (capture error, topology mismatch, or execution drift)

**Temporal symmetry.** Capture (Section 3) constructs the IoT triple *before* reasoning begins: forward specification from belief. Judgement reconstructs what the triple *should have been* after failure: backward reconstruction from observation. Both operations perform intent inference, but under epistemic asymmetry: Capture conditions on prior belief $p(I \mid C)$; Judgement conditions on the full evidence set $p(I \mid C, Y_{1:T}, F)$, where $Y_{1:T}$ is the reasoning trace and $F$ the failure signal. Under a sequential generative model, Capture produces forward-only estimates (conditioning only on evidence available at specification time), while Judgement produces estimates conditioned on all evidence, including the outcome and failure signal. The relationship mirrors two-pass inference: forward filtering followed by backward correction.

This structural pattern recurs across multiple formal traditions. In state estimation, it corresponds to Kalman prediction versus Rauch-Tung-Striebel smoothing [Kalman, 1960; Rauch et al., 1965]. In program verification, it corresponds to strongest postconditions (forward execution from precondition) versus weakest preconditions (backward computation from postcondition) [Dijkstra, 1976]. In plan recognition, it corresponds to planning (goals to actions) versus inverse planning (actions to goals) [Baker et al., 2009].

We note two important limitations. First, the clean duality holds under a fixed generative model; in practice, Judgement may revise the hypothesis class itself (e.g., discovering that the original intent space was inadequate), which goes beyond smoothing. Second, backward intent reconstruction is an ill-posed inverse problem: many intents can be consistent with the same failed trajectory, a challenge analogous to the non-uniqueness problem in inverse reinforcement learning [Ng and Russell, 2000]. Todorov [2009] warns that the forward-backward duality is "an artifact of the LQG setting" and does not transfer cleanly to nonlinear regimes. Judgement therefore requires explicit selection principles: minimal change from $P_{\text{captured}}$, safety priors, and explanatory adequacy.

## 4.2 Three Failure Modes

We distinguish three failure modes, each requiring different corrective action.

| Mode | Description | Diagnosis | Correction |
|------|-------------|-----------|------------|
| **False Capture** | Intent was incorrectly specified: $P_{\text{captured}} \neq P_{\text{actual}}$ | $P_{\text{reconstructed}} \neq P_{\text{captured}}$ | Elevate capture mode, re-specify intent |
| **False Selection** | Intent correct, wrong topology selected: $T_{\text{selected}} \neq T_{\text{optimal}}$ for $P$ | $f(\text{IoT}, \text{context})$ produced wrong $T^*$ | Update selection function, add training data |
| **False Execution** | Intent and topology correct, reasoning drifted: $\delta > \theta$ | Drift detected in trace despite correct setup | Re-execute with IoT checkpoints at higher frequency |

These modes are mutually exclusive by construction: the reconstruction algorithm (below) tests them in sequence, and the first satisfied condition determines the diagnosis.

The companion paper [Mohamed Kani, 2026] identified three failure modes in general terms: *false discovery* (intent not genuinely examined), *false process* (problem classification without execution), and *false delivery* (reasoning disconnected from purpose). The present taxonomy refines these into actionable diagnostic categories: False Capture subsumes false discovery (intent was not merely unexamined but incorrectly specified), False Selection captures false process as a topology-level mis-mapping, and False Execution corresponds to false delivery (drift from a correctly specified purpose).

## 4.3 Reconstruction Algorithm

We propose a seven-step reconstruction procedure:

1. Extract the final outcome $O$ from $T_{\text{result}}$.
2. Compare $O$ against $S$ (Success Signal): quantify failure magnitude.
3. Compare $O$ against $\bar{P}$ (Anti-Purpose): check for constraint violations.
4. Reconstruct $P_{\text{actual}}$ from $O$ + context (what purpose would have led to this outcome?).
5. Compare $P_{\text{actual}}$ with $P_{\text{captured}}$: if they diverge, diagnose *False Capture*.
6. Simulate $f(P_{\text{actual}}, \text{context}) \to T_{\text{theoretical}}$: compare with $T_{\text{selected}}$. If they diverge, diagnose *False Selection*.
7. If $P_{\text{actual}} \approx P_{\text{captured}}$ and $T_{\text{theoretical}} \approx T_{\text{selected}}$: diagnose *False Execution* (drift).

Step 4 is the most challenging: it requires an inference from outcome and context to intent, which is the ill-posed inverse problem discussed above. In practice, this can be implemented as a prompted reconstruction ("Given this outcome and this context, what was the user most likely trying to achieve?") with the selection principles serving as regularisation.

### 4.3.1 Worked Example: Clinical Triage Reconstruction

We trace the algorithm on Case Study 1 (Section 5.1) to illustrate its operation, particularly the ill-posedness at Step 4.

**Setup.** $P_{\text{captured}}$ = "list possible diagnoses." $\bar{P}$ absent. $S$ = "produce a list." $T_{\text{selected}}$ = CoT. Outcome $O$ = a linear list of independent diagnoses, missing the interacting cluster (Symptom A + Symptom B).

1. **Extract $O$**: Linear list of 5 diagnoses, no interaction analysis.
2. **Compare $O$ against $S$**: $S$ ("produce a list") is technically satisfied. However, the clinician rejected the output. Failure magnitude: qualitative.
3. **Compare $O$ against $\bar{P}$**: $\bar{P}$ was absent, so no constraint violation is detectable. This is itself diagnostic: the capture was too shallow to specify constraints.
4. **Reconstruct $P_{\text{actual}}$**: This is the ill-posed step. Multiple intents are consistent with the rejected outcome:
   - $P_a$ = "identify interacting symptom clusters" (requires GoT)
   - $P_b$ = "rank diagnoses by probability" (requires CoT with different priors)
   - $P_c$ = "identify the most dangerous diagnosis first" (requires risk-weighted CoT)

   The selection principles resolve the ambiguity: *minimal change from $P_{\text{captured}}$* favours $P_a$ (elevating from "list diagnoses" to "identify interactions" is the smallest semantic shift that explains the rejection). *Safety priors* also favour $P_a$ (in medical contexts, missing interactions is more dangerous than misordering risks). *Explanatory adequacy*: $P_a$ explains why CoT failed (linear listing cannot detect non-linear interactions), while $P_b$ and $P_c$ do not explain the topological mismatch.

   Result: $P_{\text{reconstructed}} = P_a$ = "identify interacting symptom clusters."

5. **Compare $P_a$ with $P_{\text{captured}}$**: $P_a \neq P_{\text{captured}}$. Diagnose **False Capture**.
6. **(Skipped)**: False Capture diagnosed; no need to test False Selection.
7. **(Skipped)**: Sequential testing terminates at first match.

## 4.4 Governance-Proportional Response

Not all failures deserve the same response. We define five intent criticality levels, each mapping to a response severity and a set of corrective actions.

| Intent Criticality | Response Level | Actions | Cross-Domain Analogue |
|-------------------|----------------|---------|----------------------|
| Level 1 (Reversible) | Silent retry | Re-execute with adjusted parameters; log for learning | Minor turbulence (autopilot adjusts) |
| Level 2 (Moderate) | User notification | Flag failure, suggest alternative topology | Moderate event (alert crew) |
| Level 3 (Strategic) | Halt and re-specify | Pause reasoning, elevate capture mode, require explicit IoT re-entry | Significant incident (divert) |
| Level 4 (High) | Human escalation | Route to expert review, log full trace for audit | Serious incident (emergency landing) |
| Level 5 (Irreversible) | Abort with safeguards | Stop all reasoning, require verified human approval, create permanent audit record | Engine failure (manual override) |

This governance structure occupies a niche that no existing framework fills. ASL [Anthropic, 2025] governs model capabilities. ICAO governs organisational incidents. Decision governance frameworks govern decision moments. TAO [2025] governs agent routing in healthcare. None simultaneously target the reasoning process, respond proportionally to risk, provide operationally defined levels with triggers and responses, and apply domain-agnostically. The IoT Lifecycle's governance-proportional correction satisfies all four properties.

## 4.5 The Learning Loop

Judgement outputs feed back into the lifecycle:

- **False Capture** $\to$ improve capture questions (refine L2/L3 elicitation strategies)
- **False Selection** $\to$ update selection function $f$ (new training cases for topology mapping)
- **False Execution** $\to$ calibrate drift threshold $\delta$ (sensitivity tuning)
- **All modes** $\to$ expand benchmark dataset (future empirical validation)

The feedback mechanism shares a structural parallel with the MAPE-K loop in autonomic computing [Kephart and Chess, 2003]: monitoring the managed system (reasoning trace), analysing for faults (Judgement), planning corrective action (governance response), and executing the correction. The key difference is scope. MAPE-K adapts system-level configuration parameters; the IoT Learning Loop adapts reasoning-level governance specifications.

The complete lifecycle is: Capture $\to$ Select $\to$ Monitor $\to$ Judge $\to$ Respond $\to$ Learn $\to$ Capture. This is not a pipeline; it is a cycle (Figure 1).

**Silent failure limitation.** Retrospective Judgement assumes failure is *observable*: the system knows reasoning failed because the outcome did not satisfy $S$. When $S$ is poorly specified (low $\varphi$), the system may not detect failure at all: the output appears plausible but is incorrect. The Learning Loop calibrates $S$ over time, but the first such failure may go undetected. We acknowledge this bootstrapping limitation in Section 6.

---

# Section 5: Case Studies

We demonstrate the IoT Lifecycle through three case studies, each tracing a different failure mode through the complete loop: Capture $\to$ Select $\to$ Execute $\to$ Fail $\to$ Judge $\to$ Respond $\to$ Learn $\to$ Capture. To our knowledge, no prior work traces intent governance from initial specification through failure diagnosis through corrective learning in a single worked example.

## 5.1 False Capture: Clinical Decision Support

**Setting.** A clinical decision support system analyses patient symptoms to support triage.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L1 (implicit) | Clinician queries: "Analyse this patient's symptoms." System extracts: $P$ = "list possible diagnoses." $\bar{P}$ absent. $S$ generic. $\varphi \approx 0.3$. |
| **Select** | $f(\text{IoT}) \to$ CoT | Low-fidelity triple selects safe default: chain-of-thought (sequential listing). |
| **Execute** | CoT reasoning | System produces a linear list of diagnoses, processing symptoms independently. |
| **Fail** | $S$ not met | Misses interacting symptom cluster. Symptom A + Symptom B individually benign, jointly diagnostic. |
| **Judge** | False Capture | $P_{\text{reconstructed}}$ = "identify interacting symptom clusters." $P_{\text{reconstructed}} \neq P_{\text{captured}}$: the captured purpose was too shallow. |
| **Respond** | Level 3 (halt) | Medical context warrants re-specification. Elevate to L2 (prompted): "Should this analysis consider symptom interactions?" Re-capture at higher fidelity. GoT selected. |
| **Learn** | Update L1 rules | Medical queries with multiple symptoms default to L2 prompting. $\varphi$ threshold for medical domain adjusted upward. |

**Lifecycle trace:** `CAPTURE(L1) → SELECT(CoT) → EXECUTE → FAIL → JUDGE(False Capture) → RESPOND(L3, re-capture) → LEARN → CAPTURE(L2, improved)`

**Reasoning trace (partial).** CoT step 1: "Patient presents with fatigue." Step 2: "Fatigue → anaemia, thyroid, depression." Step 3: "Patient also presents with joint pain." Step 4: "Joint pain → arthritis, lupus, fibromyalgia." Steps 2 and 4 are independent branches in a linear chain. The interaction (fatigue + joint pain together = lupus indicator) is invisible to CoT because the topology processes symptoms sequentially. GoT, selected after re-capture, creates a node for each symptom and edges for known co-occurrence patterns, surfacing the lupus indicator at the intersection.

## 5.2 False Selection: Legal Precedent Analysis

**Setting.** A legal research system analyses court precedents for a new case.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L2 (prompted) | Full triple: $P$ = "identify all relevant precedents and their interactions." $\bar{P}$ = "must not treat precedents as independent when they interact." $S$ = "produce a relationship graph of precedent dependencies." $\varphi \approx 0.7$. |
| **Select** | $f(\text{IoT}) \to$ ToT | Selection function weights "identify" and "exploration" signals, choosing tree-of-thought for parallel precedent evaluation. |
| **Execute** | ToT reasoning | Evaluates precedents along independent branches; misses contradictions between concurrent holdings. |
| **Fail** | $\bar{P}$ violated | ToT treated precedents as independent despite the explicit Anti-Purpose constraint. |
| **Judge** | False Selection | $P_{\text{captured}} \approx P_{\text{actual}}$ (intent was correct). $T_{\text{optimal}}$ = GoT (precedents have non-linear relationships). $f$ weighted "exploration" over "interconnection." |
| **Respond** | Level 2 (notify) | Flag to user that topology was misselected; suggest GoT re-execution. |
| **Learn** | Update $f$ | Add training case: "precedent interactions" $\to$ GoT preference. Weight "interconnection" keywords toward graph topologies. |

**Lifecycle trace:** `CAPTURE(L2) → SELECT(ToT) → EXECUTE → FAIL → JUDGE(False Selection) → RESPOND(L2, re-select) → LEARN → SELECT(GoT, improved)`

**Reasoning trace (partial).** ToT Branch A: "Smith v. Jones (2018) establishes duty of care." Branch B: "Brown v. State (2019) limits duty of care in government contexts." Branch C: "Garcia v. County (2020) extends Brown." Branches evaluated independently: each receives a relevance score. The contradiction (Smith establishes broad duty; Brown limits it in exactly the jurisdictional context at issue) is invisible because ToT evaluates branches in isolation. GoT, after re-selection, creates edges between Smith and Brown (CONTRADICTS), Brown and Garcia (EXTENDS), and surfaces the tension that determines the case strategy.

## 5.3 False Execution: Aviation Safety Assessment

**Setting.** An aviation safety system assesses cascading risk factors in maintenance decisions.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L3 (collaborative) | High-fidelity triple ($\varphi \approx 0.9$). $P$ = "assess cascading risk factors in aircraft maintenance decisions." $\bar{P}$ = "must not overlook secondary failure modes or downplay risk severity." $S$ = "produce a risk dependency graph with severity-weighted edges." |
| **Select** | $f(\text{IoT}) \to$ GoT | Correctly selects graph-of-thought for interconnected risk analysis. |
| **Execute** | GoT reasoning | Proceeds correctly through steps 1-6. At step 7, reasoning drifts from risk assessment toward compliance checklist generation. $\delta = 0.72$ (threshold = 0.5). |
| **Fail** | $\delta > \theta$ | Drift detected. Output quality degrading toward lower-risk compliance reporting. |
| **Judge** | False Execution | $P_{\text{captured}} \approx P_{\text{actual}}$. $T_{\text{selected}} \approx T_{\text{optimal}}$. Drift at step 7: execution deviated despite correct intent and topology. |
| **Respond** | Level 4 (escalate) | Aviation safety context. Halt at checkpoint. Escalate to human safety officer. Re-anchor to $\bar{P}$ ("must not downplay risk severity"). Resume from step 6 with doubled checkpoint frequency. Full audit trail logged. |
| **Learn** | Calibrate $\delta$ | Lower drift threshold for safety-critical domains ($\theta = 0.3$ for aviation versus $\theta = 0.5$ default). Add case to benchmark dataset. |

**Lifecycle trace:** `CAPTURE(L3) → SELECT(GoT) → EXECUTE → DRIFT(δ=0.72) → JUDGE(False Execution) → RESPOND(L4, escalate) → LEARN → EXECUTE(GoT, checkpointed)`

**Reasoning trace (partial).** GoT steps 1-6: Node "engine wear" → edge to "hydraulic pressure" (severity 8); node "hydraulic pressure" → edge to "landing gear reliability" (severity 9); node "maintenance interval" → edges to all three (modifier). Step 7 (drift): reasoning shifts from "what fails if hydraulic pressure drops?" to "is the maintenance schedule compliant with FAA 14 CFR Part 43?" The topic is related but the topology output changes from a risk dependency graph to a compliance checklist, violating $S$. Drift detection compares the semantic trajectory of steps 1-6 (risk assessment vocabulary: "failure," "cascade," "severity") against step 7 (compliance vocabulary: "regulation," "schedule," "compliant"). The cosine distance between step 7's embedding and the running mean of steps 1-6 exceeds $\theta = 0.5$.

All three case studies trace the complete lifecycle. The failure mode determines the correction target: capture strategy (Case 1), selection function (Case 2), or execution parameters (Case 3). The governance response scales with intent criticality: Level 3 (medical, re-specify), Level 2 (legal, notify), Level 4 (aviation, escalate).

---

# Section 6: Discussion

## 6.1 Limitations

We acknowledge several limitations of the present work.

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance of lifecycle benefits | Case studies demonstrate lifecycle utility; empirical validation is future work |
| Capture fidelity measurement | The fidelity function $\varphi$ requires empirical calibration | Proposed formally; calibration requires the topology selection benchmark (future Paper 3) |
| Reconstruction accuracy | $P_{\text{reconstructed}}$ may not match $P_{\text{actual}}$ | Acknowledged as upper-bound estimation, not ground truth. Non-identifiability is inherent (Section 4.1) |
| Non-identifiability | Many intents can explain the same failed trajectory | Judgement includes selection principles (minimal change, safety priors, explanatory adequacy) |
| Governance levels are illustrative | Five levels may not fit all domains | Framework allows domain-specific calibration of levels and thresholds |
| Single-model focus | Lifecycle may behave differently across model architectures | Future benchmark will test cross-model generalisation |
| Silent failure | If $S$ is poorly specified (low $\varphi$), system may not detect failure | Learning Loop calibrates $S$ over time; bootstrapping accuracy is a limitation |
| MAPE-K analogy is structural | Must not overclaim formal equivalence | Positioned as structural analogy throughout |
| Kalman regime-limits | State estimation duality does not automatically generalise beyond LQG settings [Todorov, 2009] | Framed as structural analogy; regime-limits named explicitly; predicate-transformer anchor offered as alternative |
| Non-adversarial capture (A12) | The lifecycle assumes intent specification is honest; deceptive capture breaks the governance chain | Scope boundary analogous to ICAO's honest incident reporting assumption |

### Degradation Conditions

The lifecycle is structurally domain-agnostic: the six-phase loop (Capture, Select, Monitor, Judge, Respond, Learn) applies wherever reasoning topology selection matters. However, five conditions degrade its effectiveness without constituting structural breaks:

1. **Latency-critical reasoning**: When reasoning must complete in milliseconds, full capture (L2-L3) is infeasible. Systems must rely on pre-computed capture (L4) or zero-capture (L0) with post-hoc judgement.
2. **Subjective success criteria**: When $S$ is difficult to specify precisely (e.g., creative quality), drift detection reliability decreases and Judgement loses its ground truth.
3. **Adversarial capture**: If intent is deliberately misspecified, the lifecycle operates on false premises. This is a security concern, not a governance concern (A12).
4. **Composable intent**: Tasks with nested sub-intents require recursive lifecycle application, which the present work acknowledges but does not solve (A4).
5. **Multi-stakeholder negotiation**: When no single $P$ exists and intent must be negotiated, the lifecycle requires periodic re-capture as consensus evolves.

### Domain Applicability

Table 4 maps the lifecycle across eleven domains, ranking them by adoption readiness.

| Domain | Capture Mode | Governance Level | Primary Topology | Key Adaptation | Status |
|--------|:------------:|:----------------:|:----------------:|----------------|:------:|
| Clinical Decision Support | L1→L2 | L3-L4 | GoT | Symptom interaction detection | Demonstrated |
| Legal Reasoning | L2 | L2-L3 | GoT/ToT | Precedent relationship mapping | Demonstrated |
| Aviation Safety | L3 | L4-L5 | GoT | Drift threshold calibration | Demonstrated |
| Financial Risk Analysis | L2-L3 | L4-L5 | GoT | Real-time market data integration | Proposed |
| Cybersecurity Incident Response | L1-L2 | L3-L5 | AoT→GoT | Threat classification hierarchy | Proposed |
| Engineering Design | L2-L3 | L2-L3 | ToT/GoT | Constraint satisfaction | Proposed |
| Scientific Research Planning | L2-L3 | L2-L3 | ToT→GoT | Hypothesis interaction | Proposed |
| Regulatory Compliance | L2 | L3-L4 | CoT/GoT | Audit trail requirements | Proposed |
| Judicial AI | L3 | L4-L5 | GoT | Explainability requirements | Proposed |
| Educational Assessment | L1-L2 | L1-L2 | CoT/ToT | Learner model integration | Stretch |
| Creative Applications | L0-L1 | L1 | Any | Subjective $S$ handling | Stretch |

## 6.2 Completing the Research Programme

This paper is the second in a three-paper programme:

- **Paper 1** [Mohamed Kani, 2026]: The IoT framework. Introduced the intent triple, topology selection function, and drift detection. Forward governance: specify, select, monitor.
- **Paper 2** (this paper): The IoT Lifecycle. Introduced intent capture, retrospective judgement, and the learning loop. Backward governance: capture, judge, correct, learn.
- **Paper 3** (future): The Topology Selection Benchmark (TSB). Empirical validation of capture fidelity measurement, judgement accuracy, and cross-model generalisation.

Together, the three papers constitute a complete, testable research programme for intent-governed reasoning.

## 6.3 Broader Implications

The lifecycle pattern, capture $\to$ govern $\to$ execute $\to$ judge $\to$ learn, is domain-general. It mirrors a fundamental pattern in human decision-making: "Why are we discussing this?" before "How should we decide?" before "What went wrong?"

Several directions merit future investigation:

- **Intent compositionality**: nested intents for complex tasks where sub-tasks carry distinct purposes. This addresses the single-task assumption (A4).
- **Multi-agent intent governance**: when multiple agents serve different stakeholders, whose intent governs topology selection? This addresses the single-model assumption (A6).
- **Dynamic context adaptation**: intent that evolves during reasoning as new information arrives. This addresses the static-context assumption (A5).
- **Topology discovery**: automated expansion of the topology space $\mathcal{T}$ beyond the five currently recognised structures. This addresses the known-topology-space assumption (A7).
- **Continuous topology representation**: moving from discrete topology categories to a continuous space where topologies can be blended. This addresses the discrete-topologies assumption (A10).
- **Training-time integration**: fine-tuning models to internalise the lifecycle, enabling L4 capture and model-native judgement capabilities.

The governance-proportional correction mechanism occupies a niche that no existing framework fills: it simultaneously targets the reasoning process, responds proportionally to risk, provides operationally defined response levels, and applies domain-agnostically. The lifecycle's value proposition scales with reasoning stakes: high-consequence domains (medical, legal, financial, safety) benefit most; low-consequence domains (creative, exploratory) benefit least but are not excluded. This suggests potential for standardisation analogous to ICAO's incident severity classifications or Anthropic's ASL tiers, but applied to reasoning governance rather than deployment or organisational safety.

---

# Section 7: Conclusion

We have introduced the IoT Lifecycle, completing the operational cycle for intent-governed reasoning. The Capture Spectrum (Section 3) formalises five modes by which intent enters a reasoning system, producing IoT triples of varying fidelity. Retrospective Judgement (Section 4) introduces backward intent reconstruction that diagnoses failures as False Capture, False Selection, or False Execution, with governance-proportional correction scaling response severity to intent criticality. The Learning Loop feeds judgement outputs into improved capture strategies, updated selection functions, and calibrated drift thresholds, closing the governance cycle.

Three contributions distinguish this work. First, the Capture Spectrum is architecturally distinct from prompt engineering: it produces topology governance inputs consumed by a selection function, not task instructions consumed by an executor. Second, Retrospective Judgement fills a diagnostic gap that existing work does not address: step-level diagnosis asks "which step went wrong?"; structural diagnosis asks "is chain-of-thought faithful?"; intent-level diagnosis asks "was the right reasoning topology selected for this purpose?" Third, the governance-proportional correction mechanism occupies a niche that no existing framework fills, simultaneously targeting reasoning processes, responding proportionally, operating at defined levels, and applying across domains.

The companion paper [Mohamed Kani, 2026] established the "what" of intent-governed reasoning: the triple, the selection function, the topology space. This paper establishes the "how": how intent is captured, how failures are diagnosed, how the system learns. Future work, including the Topology Selection Benchmark, will establish the "how well." No existing framework governs reasoning proportionally across domains. This paper demonstrates that such governance is both formalisable and operational.

---

# Appendices

## Appendix A: Formal Duality Derivation

### A.1 State Estimation Anchor

Consider a latent intent variable $I_t$ at time $t$, observed through a reasoning trace $Y_{1:T}$ and a failure signal $F$. Under a chain-structured generative model with Gaussian noise, the forward filtering distribution (Capture) computes:

$$p(I_t \mid Y_{1:t}) \propto p(Y_t \mid I_t) \int p(I_t \mid I_{t-1}) p(I_{t-1} \mid Y_{1:t-1}) \, dI_{t-1}$$

This forward pass produces causal marginals: estimates of intent conditioned only on evidence available at the time of specification. It corresponds to IoT Capture, where the system infers intent from the information available before reasoning begins.

The backward smoothing pass (Judgement) incorporates future evidence:

$$p(I_t \mid Y_{1:T}, F) \propto p(I_t \mid Y_{1:t}) \int \frac{p(I_{t+1} \mid I_t)}{p(I_{t+1} \mid Y_{1:t})} p(I_{t+1} \mid Y_{1:T}, F) \, dI_{t+1}$$

This produces smoothed posteriors: estimates of intent conditioned on the full evidence set, including the reasoning outcome and failure signal. It corresponds to Retrospective Judgement.

**Regime limitation.** This clean duality is "an artifact of the LQG setting" [Todorov, 2009]. In nonlinear regimes, the forward and backward messages do not combine via simple multiplication. We do not claim mathematical equivalence; we claim structural analogy: Capture and Judgement perform the same inferential operation (intent estimation) under different evidence sets, with the same relationship that prediction and smoothing have in state estimation.

### A.2 Predicate-Transformer Anchor

Dijkstra's [1976] predicate-transformer semantics provides a second, arguably closer formal anchor. For a program $S$ (here, a reasoning topology):

- **Strongest postcondition** $\text{sp}(P, S)$: "Given precondition $P$, what is the strongest statement about states reachable after executing $S$?" This is Capture → Select → Execute: given an intent specification $P$, what outcomes are achievable?

- **Weakest precondition** $\text{wp}(S, Q)$: "Given that we want postcondition $Q$, what is the weakest precondition that guarantees $Q$ after $S$?" This is Judgement: given that we wanted outcome $Q$ but got failure, what was the weakest (most general) intent specification that would have avoided the failure?

The predicate-transformer tradition is explicitly about *specifications*, not physical state. It maps directly to the IoT Lifecycle:

| Predicate Transformer | IoT Lifecycle | Direction |
|----------------------|---------------|-----------|
| Precondition $P$ | Intent specification $(P, \bar{P}, S)$ | Input |
| Program $S$ | Reasoning topology $T$ | Process |
| Postcondition $Q$ | Reasoning outcome $O$ | Output |
| $\text{sp}(P, S) = Q$ | Capture → Select → Execute | Forward |
| $\text{wp}(S, Q) = P$ | Judgement: "What intent was needed?" | Backward |

## Appendix B: Extended Related Work

### B.1 CLIPS Meta-Controller Pattern

CLIPS [Zhi-Xuan et al., AAMAS 2024] performs Bayesian goal inference from observations, distinct from intent *elicitation* (which is interactive). CLIPS' contribution is the formal demonstration that instructions and goals are informationally distinct: a user's instruction ("solve this problem") underdetermines the goal (sequential derivation? parallel exploration? interconnected analysis?). The IoT Capture Spectrum builds on this insight: L0 receives only instructions (CLIPS' problem), L1-L3 progressively elicit the goal/governance triple that CLIPS infers.

### B.2 Kambhampati's Five-Type Failure Taxonomy

Kambhampati et al. [2024] identify five categories of reasoning failure in LLMs: factual errors, logical errors, planning errors, metacognitive errors, and hallucinations. This taxonomy operates within a fixed reasoning topology. IoT Judgement adds a sixth category: *topological errors* (the right topology was not selected for the task). This is orthogonal to the Kambhampati taxonomy: a system can produce factually correct, logically valid reasoning that nonetheless fails because the topology was wrong for the purpose (e.g., CoT producing a valid linear analysis when GoT was needed for interconnected factors).

### B.3 BDI Commitment Semantics

The BDI (Belief-Desire-Intention) architecture [Bratman, 1987; Rao and Georgeff, 1995; Cohen and Levesque, 1990] governs agent *actions* through commitment to intentions. IoT governs *reasoning topology* through commitment to purpose. The structural parallel: BDI's commitment termination conditions (purpose achieved, purpose unachievable, background conditions changed) map directly to IoT's drift detection outputs (success signal satisfied, purpose unreachable, context shift). The key difference: BDI operates at the action level (what the agent does); IoT operates at the reasoning level (how the agent thinks).

### B.4 Framework of Thoughts (FoT) and STELAR

FoT [Ding et al., 2024] provides a meta-architecture for composing reasoning structures dynamically. STELAR-VISION [2025] trains models to select reasoning topologies for vision-language tasks. Both address topology selection but neither formalises *intent* as the selection criterion. FoT composes topologies based on task structure; STELAR learns selection from training data. IoT provides the governance layer that both lack: *why* this topology for *this* purpose, with *these* constraints.

## Appendix C: Domain Implementation Notes

### C.1 Financial Risk Analysis

The IoT Lifecycle maps to financial risk assessment as follows. Capture (L2-L3): elicit the risk analysis purpose. Common purposes include portfolio stress testing ($P$ = "identify correlated failure scenarios"), regulatory compliance ($P$ = "demonstrate capital adequacy under Basel III"), and client advisory ($P$ = "personalise risk tolerance to client profile"). Anti-Purpose is critical: $\bar{P}$ = "must not treat asset classes as independent when they are correlated" (analogous to the clinical triage case). Governance-proportional response maps to financial materiality: Level 1 for informational queries, Level 5 for irreversible trade execution.

### C.2 Cybersecurity Incident Response

The lifecycle naturally maps to NIST's Incident Response phases (Preparation, Detection, Analysis, Containment, Recovery, Lessons Learned). Capture aligns with Detection + Analysis (determine the type and scope of threat). Selection maps to Containment strategy (sequential isolation = CoT, parallel investigation = ToT, threat graph analysis = GoT). Governance levels map directly to NIST severity classifications. The Learning Loop feeds into Lessons Learned.

### C.3 Judicial AI

Judicial reasoning provides the strongest structural parallel to the IoT Lifecycle. A court's purpose ($P$) is explicit in the case filing. Anti-Purpose ($\bar{P}$) corresponds to legal constraints (constitutional rights, procedural rules). Success Signal ($S$) is the judgment standard (preponderance of evidence, beyond reasonable doubt). Retrospective Judgement maps to appellate review: "Given the outcome, was the correct legal reasoning topology applied?" False Capture = incorrect framing of the legal question. False Selection = wrong standard of review. False Execution = correct framing and standard, but reasoning drifted from the evidentiary record.

## Appendix D: RLPG Framework Comparison

We expand Table 1b (Section 2.3) with detailed analysis of each framework across the four properties.

### D.1 Anthropic's ASL (AI Safety Levels)

ASL defines four tiers based on model capabilities (ASL-1 through ASL-4). Each tier prescribes deployment restrictions, evaluation requirements, and containment measures. ASL governs *what models can do*, not *how they reason per-task*. It is proportional to capability risk, not to intent criticality. ASL cannot distinguish between a model reasoning about a low-stakes creative task and a high-stakes medical decision; the same ASL tier applies to both.

### D.2 ICAO Safety Management System

ICAO's SMM (Doc 9859) uses a severity-probability matrix to scale organisational response to aviation incidents. It is the gold standard for governance-proportional response in safety-critical domains. However, it governs *organisations*, not *reasoning processes*. An ICAO incident investigation examines human factors, equipment failure, and procedural deficiencies; it does not examine the reasoning topology that produced a decision.

### D.3 Decision Moment Standard (DMS)

DMS defines an 8-step governance protocol (Octagon) for auditable decisions. It governs *decision moments*: defined points where a commitment is made. DMS does not govern the reasoning process that precedes the decision, nor does it scale response proportionally to reasoning risk. Every decision receives the same 8-step protocol regardless of complexity or consequence.

### D.4 Synthesis: The RLPG Niche

The four properties (reasoning-targeted, risk-proportional, operational, domain-agnostic) define a governance niche that is occupied when the governance object is *reasoning itself* and the response scales with the *criticality of the reasoning purpose*. This niche is distinct from capability governance (ASL), organisational governance (ICAO), decision governance (DMS), and agent governance (TAO). The IoT Lifecycle occupies it.

---

## References

*[Full bibliography to be compiled from inline citations]*

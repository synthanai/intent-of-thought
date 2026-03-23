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

L4 is the most architecturally distinctive capture mode and the most speculative. Where L0 through L3 operate at inference time (the system extracts or elicits intent from the current interaction), L4 operates at training time: the model has internalised intent-topology mappings from prior data, enabling it to auto-generate an IoT triple from a task embedding without explicit elicitation. Training-time tool integration provides a partial precedent: Toolformer [Schick et al., 2023] trains models to decide *when and how* to invoke external tools, and ToolLLM [Qin et al., 2024] extends this to 16,000+ APIs. These demonstrate that models can learn to produce structured pre-action outputs (tool calls) from training data. L4 extends this pattern: instead of learning to produce *tool invocations*, the model learns to produce *governance triples*.

**Relationship to existing training paradigms.** L4 intersects with, but differs from, three established training approaches:

1. **Reinforcement Learning from Human Feedback (RLHF) / AI Feedback (RLAIF)** [Ouyang et al., 2022; Bai et al., 2022]: These train models to produce outputs preferred by humans or AI feedback, but they do not produce governance triples. The model learns to generate better task outputs, not to specify what reasoning topology is appropriate. Zhang et al. [ICLR 2025] show that RLHF actively discourages asking clarifying questions, which means RLHF-trained models are biased toward L0 (zero capture) rather than L4 (learned capture).
2. **Constitutional AI** [Bai et al., 2022]: Embeds principles (a form of Anti-Purpose) into training. Constitutional principles are closest to $\bar{P}$ in the IoT triple: they specify what reasoning must avoid. But they do not produce $P$ (task-specific purpose) or $S$ (success criteria), and they are static across all tasks.
3. **Instruction tuning**: Trains models to follow instructions, which is L0 territory (infer intent from instruction text). L4 goes further: it trains models to *produce* an explicit governance triple as a first-order output before reasoning begins.

**The L4 paradox.** If a model can reliably auto-generate IoT triples from task embeddings, it has internalised the governance layer itself. This raises a bootstrapping question: how do you train L4 without a large corpus of (task, IoT triple, optimal topology, outcome) quadruples? The answer is the Learning Loop (Section 4.5): every correction from Retrospective Judgement produces a training signal. Over time, L0-L3 capture interactions generate the training data that enables L4. The lifecycle is its own training pipeline.

**L4 fidelity is variable.** Unlike L1-L3, where fidelity increases monotonically with capture effort, L4 fidelity depends on training distribution coverage. For task types well-represented in training, L4 may achieve $\varphi > 0.8$. For out-of-distribution tasks, L4 may produce confidently wrong triples (hallucinated intent), making runtime fidelity checking essential even for learned capture.

## 3.6 The Capture Spectrum Visual (Figure 2)

Figure 2 depicts the Capture Spectrum as a fidelity gradient, mapping each mode (L0 through L4) against the fidelity range it typically produces, the capture effort required, and the topology space it can safely govern.

The visual encodes three relationships: (1) the fidelity gradient from L0 (low, fragile) through L3 (high, validated), with L4 as a conditional branch; (2) the governance-proportional threshold $\theta_\text{elevate}$ below which the system should escalate its capture mode; and (3) the safe topology range, showing that low-fidelity capture restricts the system to robust defaults (CoT) while high-fidelity capture unlocks specialised topologies (GoT, Hybrid).


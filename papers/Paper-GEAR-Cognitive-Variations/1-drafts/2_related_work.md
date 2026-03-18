# 2. Background and Related Work

Three distinct literatures bear on the question of cognitive posture: classical cognitive mode frameworks in psychology, the more recent meta-reasoning and thinking disposition research programme, and the rapidly evolving design space of AI agent cognitive architectures. We survey each in turn, then synthesise their collective gap through a differentiation matrix.

## 2.1 Cognitive Mode Frameworks in Psychology

The lineage of cognitive mode thinking begins with Bloom's Taxonomy (1956; revised by Anderson and Krathwohl, 2001), which organises cognitive operations into six hierarchical levels: remember, understand, apply, analyse, evaluate, create. The taxonomy is a *level* model, not a *mode* model: it specifies the complexity of the cognitive operation, not the orientation of the thinker performing it. Two individuals both operating at the "evaluate" level may produce fundamentally different assessments depending on whether they evaluate adversarially (seeking failure modes) or engagingly (seeking structural parallels). Bloom's hierarchy is silent on this distinction.

De Bono's Six Thinking Hats (1985) represents the most widely adopted mode-based framework. Each hat assigns a cognitive orientation: White (information), Red (emotion), Black (caution), Yellow (benefits), Green (creativity), Blue (process management). De Bono's key insight was that thinking has qualitatively different *modes*, not merely different levels. However, each hat is defined by a fixed output type: the Black Hat is caution, the Green Hat is creativity. The modes are *task-coupled*: they specify both what to attend to and how to think about it simultaneously. The framework cannot express "adversarial creativity" (applying oppositional pressure to a brainstorming process) or "reflective information-gathering" (examining past experience to determine what data to collect), because these require the mode and the task to be specified independently.

Kahneman's dual-process framework (2011), building on the foundational synthesis of Evans and Stanovich (2013), distinguishes Type 1 processing (autonomous, independent of working memory) from Type 2 processing (reflective, requiring working memory coupling). Evans and Stanovich (2013) clarify that the distinction is not primarily one of speed but of *architecture*: Type 2 processing supports hypothetical thinking, the ability to reason about counterfactual and suppositional contexts. This is a significant framework, but it describes a single axis: the degree of working memory engagement. All four cognitive postures we propose can operate at both processing levels. An adversarial hunch (Type 1) and a systematic red-team analysis (Type 2) share a cognitive posture while differing in processing depth.

Schon (1983) distinguished reflection-in-action from reflection-on-action, providing the most detailed treatment of what we term the reflective variation. Polanyi (1966) described tacit knowledge, the phenomenon of "knowing more than we can tell," which underpins what we term the generative variation: cognition that occurs *through* the act of making. Both scholars described one variation with considerable depth and precision but did not systematise the space of variations or propose a framework in which variations interact.

## 2.2 Meta-Reasoning and Thinking Dispositions

A more recent body of work addresses the *governance* of cognitive mode: how the mind monitors and adjusts which mode to deploy.

Ackerman and Thompson (2017) propose the most cited meta-reasoning framework, distinguishing object-level processes (the actual thinking) from meta-level processes (monitoring and control of thinking). Their central finding is that mode transitions are governed by fluctuating *feelings of certainty and uncertainty*: processing fluency signals whether the current mode is adequate or whether a shift to more effortful engagement is warranted. This framework explains why mode transitions are largely involuntary and cue-driven, an important constraint for any prescriptive framework that proposes *deliberate* mode selection.

Stanovich (2016) introduces the tripartite model of mind, distinguishing the autonomous mind (Type 1 processing), the algorithmic mind (cognitive capacity for Type 2 processing), and the reflective mind (the *disposition* to engage Type 2 processing). The critical finding is that capacity and deployment are largely independent: having the cognitive ability to reason reflectively does not predict whether one will actually do so. The Comprehensive Assessment of Rational Thinking (CART) measures both. This capacity-deployment independence provides theoretical support for the G.E.A.R. claim that posture is a design variable: it can be selected independently of cognitive ability.

Newton, Feeney, and Pennycook (2023) provide the strongest empirical evidence for multidimensional thinking style. Using 265 items drawn from 15 existing scales and factor-analysing across a large sample, they identify four statistically independent dimensions: Actively Open-Minded Thinking, Close-Minded Thinking, Preference for Intuitive Thinking, and Preference for Effortful Thinking. These four dimensions have differential predictive validity: not all analytic thinkers are open-minded, and not all intuitive thinkers are close-minded. The finding that thinking style is empirically *multidimensional*, with at least four independent factors, lends support to the claim that a four-variation framework is not arbitrary, even though Newton et al.'s dimensions differ from ours.

Mercier and Sperber (2017) offer a complementary perspective through their argumentative theory of reasoning. They propose that human reasoning evolved two distinct cognitive postures: a *producer stance* (generating arguments to persuade, inherently biased toward current beliefs) and an *evaluator stance* (applying epistemic vigilance when assessing others' arguments, more critical and open). The transition between stances is driven by *social role*, not by task content or difficulty. This finding directly supports the G.E.A.R. claim that posture varies independently of task: the same act of reasoning changes its character depending on whether one is producing or evaluating, regardless of the topic.

Hommel (2015) provides the Metacontrol State Model (MSM), which frames cognitive behaviour as emerging from a continual balance between two metacontrol states: *persistence* (strong top-down control, convergent, goal-focused) and *flexibility* (weak top-down control, divergent, associative). Rather than discrete states, these form a continuum dynamically regulated by task context, reward, and dopaminergic neuromodulation. The MSM provides a neurobiological substrate for mode-switching, while suggesting that the underlying reality may be continuous rather than categorical, a point we address in our limitations.

## 2.3 AI Agent Cognitive Architectures

The design of cognitive architectures for language-model-based agents has evolved rapidly from 2022 to 2026, producing a series of frameworks that progressively parameterise more aspects of agent cognition. We trace the trajectory with specific attention to how each framework handles reasoning posture.

The Beliefs-Desires-Intentions (BDI) architecture (Bratman, 1987; Rao and Georgeff, 1995) established the foundational agent model: intentions as committed goals that govern action selection. BDI operates at the *agent-action* level: it specifies what the agent will do, but not how it will reason while doing it.

ReAct (Yao et al., 2023) introduced the interleaved Thought-Action-Observation loop, establishing the canonical baseline for agentic reasoning. Its reasoning posture is fixed and uniform: every step receives the same treatment regardless of task character or intermediate state. This uniformity is both its strength (interpretability, debuggability) and its limitation (no adaptive posture).

Reflexion (Shinn et al., 2023) introduced the first explicit post-hoc reasoning posture in the modern agent literature: after an episode fails, a self-reflection module generates a verbal critique that is stored in episodic memory and used to condition future attempts. This is a *phase-level* mode switch (execution to reflection), not a *within-phase* posture variation.

Generative Agents (Park et al., 2023) added *event-driven* mode transition: agents operate in a fast, reactive mode for moment-to-moment decisions, but shift to a slower reflective mode when the cumulative importance of recent events exceeds a threshold. This makes mode-switching responsive to environmental signals rather than fixed to architectural phases. However, the reflection module itself operates in a single mode.

Tree of Thoughts (Yao et al., 2023) and Language Agent Tree Search (Zhou et al., 2024) parameterise the *structure* of reasoning: branching factor, search depth, and backtracking strategy. These are significant contributions to reasoning architecture, but they control *how much* the agent reasons (the deliberative budget), not the qualitative character of the reasoning itself.

CoALA (Sumers et al., 2024) provides the most systematic attempt to unify agent cognitive architectures, drawing on classical cognitive science (Soar, ACT-R) to propose taxonomies of memory (working, episodic, semantic, procedural), actions (internal reasoning, retrieval, learning; external grounding), and a decision-making loop (proposal, evaluation, selection, execution). CoALA identifies metareasoning as an underexplored direction but does not itself propose a posture parameterisation.

The Talker-Reasoner architecture (Christakopoulou et al., 2024), developed at Google DeepMind, is the most explicit structural separation of cognitive modes in the 2024 literature. Inspired by Kahneman's dual-process framework, it divides the agent into two specialised modules: a Talker (System 1: fast, conversational, reactive) and a Reasoner (System 2: slow, deliberative, tool-using). The modules share a memory store, enabling asynchronous coordination. This is a structural separation of *speed*, not a parameterisation of *posture*: the Reasoner always reasons in the same way, it merely reasons more deeply.

Chain of Mindset (Jiang et al., 2025) represents the closest prior work to our proposal. It defines four "mindsets" (Spatial, Convergent, Divergent, Algorithmic) and uses a meta-agent to select the optimal mindset at each reasoning step. However, each mindset is *task-type-specific*: Spatial is invoked for geometric problems, Algorithmic for computation, Divergent for creative deadlocks. The mindsets are not postures applicable to any task; they are specialised modules triggered by task classification. Additionally, the Chain of Mindset results reveal a critical design principle: mode switching without information gating (their "Context Gate") leads to context pollution, degrading accuracy by 8.24% and increasing token usage by 87%.

ARES (Yang et al., 2026) learns a per-step effort-routing policy, training a small model (Qwen3-1.7B) to predict the minimum sufficient reasoning effort for each step. ARES parameterises *how much* to reason, reducing token usage by up to 52.7% while maintaining accuracy. Notably, ARES demonstrates the "overthinking problem": fixed-high-effort agents *underperform* adaptive-effort agents on web navigation tasks, suggesting that cognitive posture (not just depth) affects output quality.

## 2.4 The Differentiation Matrix

Table 1 synthesises the analysis. For each framework, we assess three properties: whether it is *posture-aware* (does it distinguish qualitatively different ways of thinking about the same task?), whether it is *approximately independent* (does it treat posture as a dimension separable from the task itself?), and whether it includes a *blind spot model* (does it predict systematic omissions from defaulting to a particular posture?).

**Table 1.** Differentiation matrix across cognitive frameworks.

| Framework | What It Describes | Posture-Aware? | Approx. Independent? | Blind Spot Model? |
|-----------|------------------|----------------|----------------------|-------------------|
| Bloom's Taxonomy (1956) | Cognitive levels | No | No | No |
| Six Thinking Hats (1985) | Thinking modes | Partially (6 modes) | No (mode = task) | No |
| Dual-Process Theory (2013) | Processing architecture | No | No | No |
| Reflective Practice (1983) | One variation (reflective) | Partially | No | No |
| Thinking Dispositions (2023) | 4 trait dimensions | No (trait-based) | No | No |
| Argumentative Theory (2017) | Producer/Evaluator | Partially (2 postures) | Partially (social role) | No |
| BDI (1987) | Agent intentions | No | No | No |
| CoALA (2024) | Agent taxonomy | Vocabulary only | No | No |
| Chain of Mindset (2025) | 4 task-specific mindsets | Yes (step-level) | No (mindset = task type) | No |
| Talker-Reasoner (2024) | Fast/slow structural split | Yes (2 modules) | No (speed, not posture) | No |
| **G.E.A.R. [this paper]** | **Cognitive variations** | **Yes (4 gears)** | **Yes** | **Yes (2 blind spot pairs)** |

The matrix reveals a consistent pattern: frameworks that are posture-aware are not independent of task, and frameworks that achieve some independence (Mercier and Sperber's social-role-driven posture) lack a model of the systematic consequences of posture defaulting. G.E.A.R. is the first framework that combines all three properties.

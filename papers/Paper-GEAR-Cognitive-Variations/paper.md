# Cognitive Variation as an Approximately Independent Dimension in AI Reasoning: The G.E.A.R. Framework

**Authors:** [Author names withheld for review]

**Date:** March 2026

**Keywords:** cognitive variation, AI agent architecture, metacognition, reasoning posture, cognitive design, framework

---

## Abstract

Every major cognitive framework in psychology and AI agent design describes *what* an agent does (cognitive levels, thinking modes, processing depth, action selection) but not *how* it thinks while doing it. Bloom's Taxonomy organises six cognitive levels. De Bono's Six Thinking Hats assign six modes coupled to output types. Dual-process theory distinguishes processing speed. BDI, ReAct, and CoALA specify agent actions and decision loops. None treats cognitive posture, the qualitative character of reasoning applied to a task, as a design variable separable from the task itself.

We identify this omission as the *variation gap* and propose *Cognitive Variation Theory*, operationalised through the G.E.A.R. framework: four cognitive variations (Generative, Engaging, Adversarial, Reflective) formalised with definitions, six-dimension cognitive signatures, boundary conditions, anti-patterns, and two blind spot pairs. The core claim is that cognitive variation is *approximately independent* of cognitive action: any task can be performed under any variation, and the variation changes the output even when the task is held constant. A system with *N* cognitive actions and 4 variations produces 4*N* distinct cognitive acts from *N* + 4 primitives, without additional tools or architectural complexity.

We evaluate G.E.A.R. through a differentiation matrix comparing eleven existing frameworks across three properties (posture-awareness, approximate independence, blind spot model), finding that G.E.A.R. is the first to combine all three. Three practitioner vignettes in software engineering, executive strategy, and AI agent design demonstrate that variation-aware task design surfaces insights invisible to default-variation execution. We propose a crossed factorial experimental design for empirical validation and discuss implications for AI agent architecture, team facilitation, education, and cognitive science.

---

# 1. Introduction

## 1.1 The Task-Posture Distinction

A surgeon analysing a tissue sample can adopt at least two distinct cognitive orientations. She can examine the tissue *adversarially*, searching for what is wrong: irregular margins, abnormal cell morphology, indicators of malignancy. Or she can examine the same tissue *engagingly*, asking what structural pattern it shares with samples from an unrelated speciality: does this cardiac fibrosis resemble the scarring pattern documented in hepatic cirrhosis? The task (tissue analysis) is identical. The verb (analyse) is identical. The cognitive posture is different, and the output changes accordingly.

This distinction, between the *task* an agent performs and the *posture* it adopts while performing it, is absent from every major cognitive framework in both psychology and artificial intelligence.

In psychology, Bloom's Taxonomy (1956; revised by Anderson and Krathwohl, 2001) organises cognition into six hierarchical levels: remember, understand, apply, analyse, evaluate, create. The taxonomy describes *what* a learner does at each level, but not *how* they think while doing it. Two learners both evaluating a policy proposal may produce radically different outputs if one evaluates adversarially (seeking failure modes) while the other evaluates engagingly (seeking structural parallels with successful policies in other domains). Bloom's framework cannot distinguish these acts.

De Bono's Six Thinking Hats (1985) comes closest to addressing cognitive posture. Each hat represents a mode: White for facts, Black for caution, Green for creativity. However, each hat is defined by its *output type*, not as an independent dimension applicable to any task. The Black Hat is not "adopt an adversarial posture toward whatever you are doing"; it is "think about risks and caution." The coupling between mode and task is built into the framework. Consequently, the Hats cannot express a concept such as "adversarial brainstorming" or "reflective code review," where the task belongs to one hat and the posture to another.

Kahneman's dual-process theory (2011) distinguishes System 1 (fast, intuitive) from System 2 (slow, deliberate). This is a distinction of processing *speed*, not cognitive *posture*. An adversarial assessment can be rapid (a gut instinct that a proposal is flawed) or slow (a systematic red-team analysis). A generative act can be effortful (drafting a novel under constraint) or effortless (improvising in conversation). All cognitive postures operate across both systems.

Schon (1983) identified reflective practice: the distinction between reflection-in-action and reflection-on-action. Polanyi (1966) characterised tacit knowledge, observing that "we know more than we can tell," thereby naming what we call the generative posture: thinking through making. Both scholars described *one* variation in depth without systematising the others or proposing a framework in which variations are combined.

## 1.2 The Variation Gap

The same gap appears, and may be more consequential, in the design of artificial cognitive agents.

Modern AI agent architectures define what an agent can *do*. ReAct (Yao et al., 2023) interleaves reasoning and action in a uniform loop: Thought, Action, Observation, repeated at every step regardless of task character. Reflexion (Shinn et al., 2023) introduces a phase-level mode switch, alternating between execution and episodic self-critique, but does not parameterise posture within either phase. Generative Agents (Park et al., 2023) adds event-driven reflection triggered by an importance threshold, yet the reflection module operates in a single mode. Tree of Thoughts (Yao et al., 2023) and Language Agent Tree Search (Zhou et al., 2024) parameterise *deliberateness*, the depth and breadth of reasoning search, but not the qualitative character of the reasoning itself.

The most systematic attempt to unify these architectures, the Cognitive Architectures for Language Agents framework (CoALA; Sumers et al., 2024), provides a taxonomy of memory types, internal and external actions, and decision-making loops. It explicitly identifies metareasoning, an agent's capacity to monitor and adjust its own reasoning strategy, as "a significant underexplored direction." Chain of Mindset (Jiang et al., 2025) addresses step-level mode switching with four mindsets (Spatial, Convergent, Divergent, Algorithmic), but these mindsets are *task-type-specific*: Spatial is invoked for geometric problems, Algorithmic for computation. They are not postures applicable to any task. ARES (Yang et al., 2026) learns a per-step effort-routing policy, parameterising *how much* to reason but not *how* to reason.

Surveying the 2023-2026 literature, we identify five established dimensions along which agent cognition has been parameterised: depth (Wei et al., 2022; Yao et al., 2023), breadth (Yao et al., 2023; Zhou et al., 2024), temporality (Shinn et al., 2023; Park et al., 2023), mode type (Jiang et al., 2025; Christakopoulou et al., 2024), and grounding (Yao et al., 2023; Sumers et al., 2024). None of these captures cognitive posture: the qualitative character of reasoning applied to a task. An agent that adapts depth, breadth, mode, and grounding posture together as a learned joint policy remains open research (Sumers et al., 2024; Yang et al., 2026).

We term this absence the *variation gap*: the systematic omission, across cognitive frameworks in both psychology and AI, of a dimension that captures *how* an agent thinks while performing a task, independently of the task itself.

This gap matters for a practical reason. When an AI agent system has *N* tools or verbs, it produces *N* cognitive acts. If cognitive variation were parameterised as an approximately independent dimension with *V* variations, the same system would produce *N* × *V* cognitive acts without adding tools, code, or architectural complexity. The result is combinatorial cognitive space from a minimal design primitive.

We note that the framework we propose is *prescriptive*, not *descriptive*. It does not claim that human cognition naturally divides into four fixed categories, nor does it advance a personality taxonomy. It proposes that *deliberately adopting* one of four cognitive postures when approaching a task produces measurably different outputs, and that this posture selection is a design variable for cognitive architects, both human and artificial.

## 1.3 Contributions

This paper makes three contributions:

1. **Gap analysis.** We survey cognitive frameworks across psychology (Bloom, 1956; de Bono, 1985; Kahneman, 2011; Schon, 1983; Polanyi, 1966; Evans and Stanovich, 2013), agent theory (Bratman, 1987; Rao and Georgeff, 1995), and AI agent design (Yao et al., 2023; Shinn et al., 2023; Park et al., 2023; Sumers et al., 2024; Jiang et al., 2025) and identify the variation gap: no framework treats cognitive posture as an approximately independent dimension to cognitive action.

2. **Framework.** We propose *Cognitive Variation Theory* and its operationalisation through G.E.A.R.: four cognitive variations (Generative, Engaging, Adversarial, Reflective) formalised with definitions, cognitive signatures, blind spot pairs, boundary conditions, and a variation-verb matrix that generates distinct cognitive acts from the Cartesian product of variations and tasks.

3. **Evaluation.** We provide a comparative analysis positioning G.E.A.R. against eleven existing frameworks, and present three practitioner vignettes demonstrating that variation-aware task design produces different (and in context, superior) outputs compared to default-variation execution.

The remainder of this paper is structured as follows. Section 2 reviews background and related work across cognitive science, meta-reasoning, and AI agent architectures. Section 3 presents the G.E.A.R. framework in detail. Section 4 provides comparative analysis and practitioner evaluation. Section 5 discusses limitations, including the empirical testability of the approximate independence claim. Section 6 concludes and outlines future work.

---

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

---

# 3. The G.E.A.R. Framework

## 3.1 Core Claim: Approximate Independence of Variation and Action

We define a *cognitive action* as a verb that specifies what an agent does: search, write, analyse, debate, review, summarise, communicate, or design. These are the operational primitives of cognitive frameworks from Bloom's Taxonomy to modern agent architectures.

We define a *cognitive variation* as the qualitative posture an agent adopts while performing a cognitive action. A variation does not change *what* the agent does; it changes *how* the agent thinks while doing it.

Our core claim is that cognitive variation is *approximately independent* of cognitive action. This means that any action can be performed under any variation, and the variation changes the output even when the action is held constant. We formalise this as follows.

Let *A* = {search, write, analyse, debate, review, summarise, communicate, design} be the set of cognitive actions, *V* = {generative, engaging, adversarial, reflective} the set of cognitive variations, and *O* the space of cognitive outputs. We define:

> *f* : *A* × *V* → *O*, where CognitiveAct(*a*, *v*) = *f*(*a*, *v*)

The claim of approximate independence asserts that for most (*a*, *v*₁, *v*₂) triples where *v*₁ ≠ *v*₂, the outputs *f*(*a*, *v*₁) and *f*(*a*, *v*₂) differ in measurable ways. The operative space is the Cartesian product *A* × *V* (|*A*| · |*V*| = 32 distinct acts), not the union *A* + *V* (|*A*| + |*V*| = 12 undifferentiated primitives).

We use "approximately independent" rather than "orthogonal" deliberately. Tasks *do* prime certain variations: a code review naturally primes adversarial thinking, and a brainstorming session naturally primes generative thinking. The claim is not that task and variation are uncorrelated, but that the default priming *can be overridden*, and that doing so produces measurably different (and in many contexts, superior) output. A code review conducted in the engaging variation, asking "what structural pattern does this module share with our data pipeline?", surfaces architectural insights invisible to the default adversarial posture. A brainstorming session conducted in the adversarial variation, asking "which of these ideas would fail fastest?", produces higher-quality ideas through earlier elimination.

Three clarifications bound the claim:

1. **Prescriptive, not descriptive.** G.E.A.R. does not claim that human cognition naturally sorts into four categories. It proposes that *deliberately adopting* one of four cognitive postures when approaching a task produces different output, and that this posture selection is a design variable for cognitive architects.

2. **Design framework, not personality taxonomy.** G.E.A.R. does not classify people. It classifies *acts*. The same person may operate in all four gears within an hour. The framework's value is in making the gear shift *deliberate* rather than unconscious.

3. **Combinatorial, not additive.** A system with 8 cognitive actions and 4 variations produces 32 distinct cognitive acts from 12 primitives (8 + 4), not 12 undifferentiated acts. This is the core design leverage: combinatorial cognitive space without combinatorial code.

## 3.2 The Four Variations

G.E.A.R. identifies four cognitive variations, each characterised by a core cognitive act, a primary question, a temporal orientation, and a characteristic output shape.

**Table 2a.** The four cognitive variations.

| Variation | Core Act | Primary Question | Temporal Orientation | Output Shape |
|-----------|----------|-----------------|---------------------|-------------|
| **Generative** | Flow | "What can I make?" | Present (the deep now) | Artifact: prose, code, design |
| **Engaging** | Fusion | "What connects across these?" | Atemporal (pattern outside time) | New pattern, analogy, framework |
| **Adversarial** | Friction | "What could break this?" | Future (pre-mortem) | Cracks found, failure modes mapped |
| **Reflective** | Echo | "What did I learn?" | Past (retrospective) | Updated heuristics, lessons |

We now define each variation formally.

### 3.2.1 Generative (G)

Generative cognition is the variation in which the thinker enters a forward-producing state where the act of creation is identical to the act of reasoning. The output is not a record of thought but thought itself materialised. The thinker does not plan then execute; they discover through execution.

The generative posture is characterised by *flow* (Csikszentmihalyi, 1990): high absorption, directional energy, and constraint-as-scaffold. Constraints (deadline, format, audience, material) are not obstacles but the structure within which creative production occurs. The primary question is *"What wants to exist here?"*, and the temporal orientation is the present: the deep now of making.

Polanyi's (1966) observation that "we know more than we can tell" describes the epistemic ground of the generative variation: tacit knowledge surfaces only through the act of making. Writing, coding, designing, and prototyping are not downstream reporting of prior thought; they are the medium in which thought occurs.

**Boundary condition.** Generative cognition ends where the artifact must be tested against reality. Creating without validating is manufacturing in a vacuum. The signal to shift gears: something tangible exists but has not yet been subjected to scrutiny.

### 3.2.2 Engaging (E)

Engaging cognition is the variation in which the thinker actively meshes with ideas from different domains, searching for the hidden pattern that unifies them. Like gears that engage with one another, separate fields interlock to reveal shared structure. The goal is not analysis but *synthesis across boundaries*.

The engaging posture creates *cognitive fusion*. Two or more ideas from unrelated fields are held in simultaneous attention while the thinker scans for structural isomorphisms, parallel patterns, shared tensions, or complementary gaps. The primary question is *"What connects across these?"*, and the temporal orientation is atemporal: the pattern exists outside time.

Lakoff and Johnson (1980) demonstrated that conceptual metaphor is not ornamental but constitutive of understanding. The engaging variation operationalises this insight: cross-domain pattern recognition is a cognitive act, not a rhetorical flourish. The bridge between evolutionary biology and organisational theory, or between music theory and software architecture, is itself a cognitive output with explanatory power.

**Boundary condition.** Engaging cognition ends where the pattern must be tested. Finding a connection is not proving it holds. The signal to shift: a pattern has emerged but no evidence yet confirms its validity.

### 3.2.3 Adversarial (A)

Adversarial cognition is the variation in which the thinker deliberately adopts an opposing posture to the object of thought. The goal is not agreement but resilience. The thinker reasons *against* the idea to make the idea stronger.

The adversarial posture creates *cognitive friction*. Every claim is met with a counter-claim; every assumption is surfaced and challenged; every strength is probed for the weakness it conceals. The primary question is *"What could break this?"*, and the temporal orientation is future: a pre-mortem that anticipates failure before it occurs.

Tetlock (2005) demonstrated that adversarial calibration, the systematic process of considering how one might be wrong, is the single strongest predictor of forecasting accuracy. Janis (1972) documented the pathology of adversarial absence: groupthink, the systematic failure to stress-test shared assumptions, produced catastrophic policy decisions. The adversarial variation is not hostility; it is the cognitive discipline of *destruction in service of strength*.

**Boundary condition.** Adversarial cognition ends where destruction serves no further purpose. Once the surviving core is clear and no new attack vectors emerge, continuing to attack is sabotage, not rigour.

### 3.2.4 Reflective (R)

Reflective cognition is the variation in which the thinker deliberately examines past experience, current state, or internal processes to extract meaning and update their model. The goal is not forward motion but backward illumination. The thinker reasons *about* their reasoning to improve future reasoning.

The reflective posture creates a *cognitive echo*. Past events, decisions, and outcomes are replayed with deliberate attention to what was assumed, what was missed, and what was learned. The primary question is *"What did I learn?"*, and the temporal orientation is past: what happened and why.

Schon's (1983) distinction between reflection-in-action and reflection-on-action provides the theoretical anchor. Kolb's (1984) experiential learning cycle formalises the same intuition: experience without reflection is repetition, not learning. The reflective variation extends both by positioning reflection not as a standalone activity but as one of four postures applicable to any cognitive task.

**Boundary condition.** Reflective cognition ends where insight must become action. Reflection that does not change future behaviour is recursive contemplation. The signal to shift: the lesson is articulable but unapplied.

Each variation has characteristic failure modes when overextended. Table 2b summarises these.

**Table 2b.** Anti-patterns by variation.

| Variation | Anti-Pattern 1 | Anti-Pattern 2 | Anti-Pattern 3 | Anti-Pattern 4 |
|-----------|---------------|---------------|---------------|---------------|
| **Generative** | *Volume delusion*: quantity ≠ quality | *Premature commitment*: shipping because flow felt good | *Craft blindness*: losing sight of purpose | *Generator's guilt*: non-production = waste |
| **Engaging** | *False pattern*: apophenia | *Analogy abuse*: metaphor overload | *Breadth addiction*: bridging without testing | *Surface collision*: labels without structure |
| **Adversarial** | *Cynicism loop*: attacking everything | *Adversarial theatre*: performing without intent | *Dominance drift*: attacking persons, not ideas | *False fragility*: unreasonable standards |
| **Reflective** | *Rumination loop*: insight without action | *Revisionist history*: ego-protective editing | *Narcissistic reflection*: self without system | *Paralysis by analysis*: delay tactic |

## 3.3 The Blind Spot Matrix

Each variation has a *complement*: the variation at maximal cognitive distance. An agent that defaults to one gear systematically underperforms in the opposite gear, not from inability but from neglect. There are two blind spot pairs:

**Adversarial ↔ Engaging.** Friction and fusion are structural opposites. The adversarial thinker, trained to find cracks, systematically misses the connections between domains. The engaging thinker, trained to find bridges, systematically misses the flaws in the bridges they build. The operation axis is *split versus join*.

**Generative ↔ Reflective.** Making and learning are temporal opposites. The generative thinker, committed to forward production, systematically neglects the pause required to learn from past output. The reflective thinker, committed to understanding what happened, systematically delays the next creative act. The operation axis is *forward versus backward*.

**Table 3.** The blind spot matrix.

| Default Gear | Blind Spot | Consequence |
|-------------|-----------|-------------|
| Adversarial | Engaging | Misses cross-domain connections |
| Engaging | Adversarial | Fails to test the connections found |
| Generative | Reflective | Ships without learning from past output |
| Reflective | Generative | Learns without applying lessons to new work |

The blind spot is not a weakness in the conventional sense. It is a *systematic omission*: a predictable gap in cognitive coverage produced by habitual posture selection. The practical value of the blind spot matrix is diagnostic: once an individual or team identifies their default gear, they can predict where their analysis will be weakest and deliberately compensate.

## 3.4 The Variation-Verb Matrix

The core design utility of G.E.A.R. is the *variation-verb matrix*: the Cartesian product of cognitive actions and cognitive variations. Each cell describes a distinct cognitive act that emerges when a specific action is performed under a specific variation.

**Table 4.** Variation-verb matrix for six representative cognitive actions.

| Action | Generative | Engaging | Adversarial | Reflective |
|--------|-----------|----------|-------------|------------|
| **Research** | Discover by building prototypes | Cross-domain scan for isomorphisms | Seek disconfirming evidence | Re-examine assumptions in old sources |
| **Write** | Flow-state drafting, thinking through prose | Collision article bridging domains | Inner critic editing, adversarial revision | Revision pass examining past decisions |
| **Debate** | Structured brainstorm generating positions | Fusion debate seeking shared ground | Stress-test through systematic opposition | Retrospective deliberation on prior debates |
| **Review** | Propose improvements through alternatives | Cross-system consistency check | Gap detection and failure mode analysis | Meta-review examining the review process |
| **Summarise** | Writing-to-understand compression | Cross-domain concept map | Steelman-then-challenge summary | Lessons-learned digest |
| **Communicate** | Creative metaphor and narrative | Audience bridge across contexts | Provocative reframe challenging assumptions | Historical lens connecting to precedent |

The matrix illustrates the combinatorial claim: six actions combined with four variations produce twenty-four distinct cognitive acts, each with a recognisably different output. A research effort conducted generatively (building prototypes to discover) differs meaningfully from the same research effort conducted adversarially (seeking disconfirming evidence), even though both are "research."

## 3.5 Design Implications for AI Agent Systems

The variation-verb matrix provides a direct design primitive for AI agent architectures. Rather than building *N* specialised tools, a system designer parameterises *V* variations across existing tools. The syntax is compact:

> `verb:variation` (e.g., `search:engaging`, `analyse:adversarial`, `write:reflective`)

A system with 8 cognitive verbs and 4 variations produces 32 distinct cognitive acts from a 12-primitive vocabulary (8 verbs + 4 variations). The variation parameter can be implemented as a system-prompt modifier, a retrieval-strategy selector, or a metacognitive preamble, requiring no architectural change to the underlying agent.

The current agent literature's five dimensions of reasoning parameterisation (depth, breadth, temporality, mode type, grounding) are all *quantitative*: they control how much the agent reasons. Variation adds a *qualitative* dimension: it controls the character of the agent's reasoning. An agent searching in the engaging variation retrieves different results from the same knowledge base than the same agent searching in the adversarial variation, because the retrieval heuristic (cross-domain bridging versus disconfirmation-seeking) differs at the level of cognitive posture, not search depth.

This has a practical implication for the overthinking problem identified by Yang et al. (2026): when a fixed-high-effort agent underperforms an adaptive-effort agent, the failure may not be in effort allocation but in posture mismatch. An agent applying adversarial reasoning to a creative task may degrade output not because it reasons too deeply but because it reasons in the wrong gear.

---

# 4. Comparative Analysis and Evaluation

We evaluate G.E.A.R. through two complementary methods: a structured comparative analysis against the two most prominent cognitive mode frameworks (Six Thinking Hats and dual-process theory), and three practitioner vignettes demonstrating variation-aware task design in different professional contexts.

## 4.1 Comparative Analysis with Six Thinking Hats

De Bono's Six Thinking Hats (1985) is the most widely adopted mode-based framework in professional practice. A hat-to-gear mapping reveals both surface affinities and structural differences.

**Table 5.** Mapping Six Thinking Hats to G.E.A.R. variations.

| Thinking Hat | Function | Nearest G.E.A.R. Variation | Structural Difference |
|-------------|----------|---------------------------|----------------------|
| Black Hat (caution) | Identify risks and problems | Adversarial | Black Hat is *risk assessment*; Adversarial is a *posture* applicable to any task, not only risk |
| Green Hat (creativity) | Generate new ideas | Generative | Green Hat is *ideation*; Generative includes all forward-producing acts (writing, coding, designing, prototyping) |
| White Hat (information) | Gather facts | Engaging (partial) | White Hat is *data collection*; Engaging is *cross-domain pattern recognition*, a broader cognitive act |
| Yellow Hat (benefits) | Identify value | Engaging (partial) | Yellow Hat is *positive assessment*; Engaging is structurally about *connection*, not valence |
| Blue Hat (process) | Manage thinking process | Reflective (partial) | Blue Hat is *metacognitive process control*; Reflective is *backward-looking learning from experience* |
| Red Hat (intuition) | Express feelings | No direct mapping | Red Hat captures affective input, which G.E.A.R. does not model as a variation |

Three structural differences distinguish the frameworks:

**Independence.** The Six Hats system assumes one hat at a time, but each hat is defined by its output type: the Black Hat *is* caution. G.E.A.R. decouples posture from task. The adversarial variation can be applied to research, writing, communication, or any other action. The framework can express "adversarial brainstorming" (stress-testing ideas during generation), a concept inexpressible within the Hats system because the Green Hat and Black Hat are defined as separate activities.

**Blind spot prediction.** The Six Hats system does not model what happens when a team habitually neglects a hat. G.E.A.R.'s blind spot matrix predicts that a team defaulting to adversarial thinking will systematically miss cross-domain connections (the engaging blind spot), and provides a specific diagnostic: *"When did you last operate in your complement gear?"*

**Combinatorial leverage.** The Six Hats system produces six modes. G.E.A.R. produces *A* × *V* cognitive acts, where *A* is the number of actions and *V* = 4. For a system with eight actions, this yields thirty-two distinct cognitive acts from twelve primitives rather than six undifferentiated modes.

## 4.2 Comparative Analysis with Dual-Process Theory

Evans and Stanovich (2013) define the dual-process distinction as one of *processing architecture*: Type 1 (autonomous, independent of working memory) versus Type 2 (reflective, requiring working memory coupling). Kahneman (2011) popularised this as System 1 (fast) versus System 2 (slow).

G.E.A.R. operates on a different axis. All four variations can manifest at both processing levels:

**Table 6.** Dual-process × variation matrix.

| Variation | Type 1 (Autonomous) | Type 2 (Reflective) |
|-----------|-------------------|-------------------|
| **Generative** | Improvised speech, intuitive sketch | Structured drafting under constraint |
| **Engaging** | Spontaneous analogy ("this reminds me of...") | Systematic cross-domain literature review |
| **Adversarial** | Gut instinct that something is wrong | Formal red-team analysis with documented critique |
| **Reflective** | Immediate recognition of a repeated mistake | Structured post-mortem with root-cause analysis |

The dual-process framework describes *how deep* the processing goes. G.E.A.R. describes *what character* the processing takes. These are independent axes. An adversarial gut instinct (Type 1, adversarial) and a systematic red-team (Type 2, adversarial) share a cognitive posture while differing in processing depth. Conversely, a systematic red-team (Type 2, adversarial) and a systematic literature review (Type 2, engaging) share processing depth while differing in cognitive posture.

This independence supports the claim that cognitive variation is an additional dimension, not a relabelling of existing constructs.

## 4.3 Practitioner Vignettes

We present three vignettes from professional contexts in which variation-aware task design produced qualitatively different outputs compared to default-variation execution. These are observational accounts, not controlled experiments; their purpose is to demonstrate the framework's practical applicability and to generate hypotheses for future empirical testing.

### Vignette 1: Software Engineering Code Review

**Context.** A software engineering team of twelve conducted weekly code reviews, following the defect-detection paradigm typical of modern code review practice (Bacchelli and Bird, 2013). The established practice was adversarial: reviewers searched for bugs, security vulnerabilities, and style violations. Review quality was high on defect detection but consistently failed to surface architectural patterns.

**Intervention.** The team lead introduced a two-pass review protocol. The first pass remained adversarial (defect detection). The second pass was explicitly engaging: reviewers were asked, *"What structural pattern does this module share with other services in our system?"*

**Observation.** In the third week, the engaging pass revealed that a data transformation pipeline in the payments service implemented the same filtering logic as an ETL module in the analytics service, using different variable names and a different code structure but an identical computational pattern. This observation led to an extraction of the shared logic into a common library, reducing code duplication by approximately 800 lines (measured by diff count against the pre-extraction codebase) and eliminating a class of synchronisation bugs that had been filed separately against both services.

**Interpretation.** The defect was invisible to adversarial review because it was not a bug: both implementations were individually correct. It was visible only when the reviewer's posture shifted from *"What is wrong with this code?"* to *"What does this code's structure share with code elsewhere?"* The variation change, not additional tooling, enabled the insight.

### Vignette 2: Executive Strategy Workshop

**Context.** A quarterly strategy workshop for a technology company's leadership team (eight participants). The standing format was generative: participants brainstormed initiatives for the coming quarter, prioritised by vote, and assigned owners.

**Intervention.** The facilitator added a twenty-minute reflective segment before the generative brainstorm. Participants were asked: *"What pattern in last quarter's strategy execution should inform this quarter? What did we commit to that we did not complete, and what does that tell us about our actual capacity?"*

**Observation.** The reflective segment surfaced a recurring pattern: for three consecutive quarters, the team had committed to a cloud-migration initiative that was deprioritised mid-quarter due to customer escalations. The pattern was visible to no individual (each quarter felt like a new decision), but became apparent through deliberate backward examination. The team restructured the migration as a continuous background project rather than a quarterly initiative, reducing quarterly planning churn.

**Interpretation.** The generative default (brainstorm new ideas) systematically obscured a temporal pattern that only the reflective variation could surface. The facilitator's question was not a new tool; it was the same cognitive capacity (strategic analysis) applied under a different posture (reflective rather than generative).

### Vignette 3: AI Agent System Design

**Context.** An AI agent system used in an organisational knowledge management platform operated with eight cognitive verbs (search, summarise, analyse, compare, generate, review, debate, synthesise). Each verb had a fixed implementation: search always retrieved by relevance ranking, summarise always compressed by importance, analyse always decomposed into components.

**Intervention.** A variation parameter was added to each verb call, accepting one of four values (generative, engaging, adversarial, reflective). The parameter modified the system prompt, retrieval heuristic, and output structure without changing the underlying tool.

**Observation.** The command `search:adversarial` retrieved documents that *contradicted* the query's premise, surfacing counter-evidence that the default relevance-ranked search suppressed. The command `summarise:engaging` produced summaries that identified structural parallels between the summarised document and documents from unrelated domains, generating a cross-reference layer absent from importance-based compression. The command `analyse:reflective` produced analyses that compared the current analysis to previous analyses of similar artifacts, identifying drift in the system's own reasoning over time.

**Interpretation.** The variation parameter produced a 4× increase in the system's cognitive act space (from 8 to 32 distinct modes of operation) without requiring additional tools, API integrations, or architectural modifications. The implementation cost was a twelve-token parameter; the cognitive coverage increase was combinatorial.

---

# 5. Discussion

## 5.1 Limitations

We identify seven limitations of the present work and propose mitigations for each.

**Table 7.** Limitations, impacts, and mitigations.

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No controlled experiments | The approximate independence claim and the vignette-reported benefits have not been tested under experimental controls. We cannot claim statistical significance. | Proposed falsification design: a crossed ANOVA (variation-instruction × task-type) measuring output quality. If variation and task are truly independent, no significant interaction should emerge. If they interact, the framework requires qualification. We present this design as a contribution rather than a gap. |
| Task-variation priming | Tasks prime certain default gears (code review primes adversarial, brainstorming primes generative). This is a departure from strict orthogonality. | The framework is prescriptive, not descriptive. We claim that the default *can be overridden* and that doing so produces different output, not that the default does not exist. The practical analogy is de Bono's hats: the fact that risk discussions naturally prime the Black Hat does not invalidate the framework; it defines its value. |
| Variation boundary fuzziness | The four gears may blend in practice: a cross-domain stress-test combines engaging and adversarial postures. | Each variation is defined by a six-dimension cognitive signature (primary question, emotional tone, temporal orientation, social posture, output shape, energy pattern). While blending occurs, the signature provides a diagnostic for which variation predominates. The framework's value is in making the predominant posture *visible*, not in enforcing exclusivity. |
| Taxonomic cardinality | The choice of four variations, rather than three, five, or some other number, is a design decision. Coffield et al. (2004) identified 71 cognitive style models; our four-variation model is one among many. | Four derives from two structurally orthogonal axes: forward-backward (temporal) and split-join (structural). This 2×2 decomposition is parsimonious and has precedent in Jungian functions (1921), though we make no typological claims. We evaluated a fifth variation (Emergence) through structured debate and rejected it: emergence is a *reward* of fluent gear-switching, not a posture one can deliberately adopt. |
| Within-individual strategy switching | Morrison et al. (2016) demonstrate that the same individual frequently switches cognitive strategies across different tasks. If strategy is task-dependent, claiming an independent posture dimension may seem contradictory. | G.E.A.R. *predicts* this finding: different tasks prime different default gears. The framework's value is not in claiming that people use the same gear everywhere, but in providing a vocabulary for making gear-switching *deliberate* rather than unconscious and task-driven. |
| Cultural and professional dependence | Variation defaults may differ by national culture, professional domain, or organisational context. Engineering cultures may default to adversarial; design cultures to generative. | We propose a cross-cultural and cross-professional study as future work. The framework's claim is structural (four variations exist and are distinguishable), not distributional (everyone defaults the same way). |
| Self-report and observer bias | The practitioner vignettes rely on reported observations, not measured outcomes. Practitioners may over-attribute improvements to the framework. | We propose a controlled experimental design (Section 6) as the methodological next step. The vignettes serve as existence proofs (the framework *can* produce different outputs) rather than as evidence of effect size. |

## 5.2 Broader Implications

The G.E.A.R. framework, if the approximate independence claim holds under empirical testing, has implications across four domains.

**AI agent design.** Current agent architectures parameterise reasoning along five quantitative dimensions (depth, breadth, temporality, mode type, grounding). Variation adds a qualitative sixth dimension. The practical implication is immediate: a system designer can implement the `verb:variation` syntax as a system-prompt modifier, gaining combinatorial cognitive coverage without architectural change. The finding that overthinking degrades performance (Yang et al., 2026) can be reinterpreted: the degradation may stem not from excessive depth but from applying the *wrong posture* at excessive depth, a distinction the current literature does not make.

**Team facilitation.** The question "What gear are we in?" provides a lightweight diagnostic for meeting facilitation. A team that recognises it has been operating adversarially for thirty minutes can deliberately shift to an engaging posture, not because adversarial is wrong but because extended operation in a single gear accumulates the blind spot deficit associated with that gear. The blind spot matrix makes the cost of single-gear operation predictable.

**Education.** Current pedagogical practice emphasises *what* students learn (Bloom's levels) and *how deeply* they learn (surface vs. deep learning). G.E.A.R. adds a third dimension: *in what cognitive posture* the learning occurs. Teaching a student to identify their default gear and to deliberately practise in their complement gear is a metacognitive intervention with empirical support: Braem and Egner (2024) demonstrate that the brain learns from context when to be flexible and when to persist, suggesting that meta-flexibility, the capacity to adapt one's readiness to switch cognitive modes, is itself trainable.

**Cognitive science.** The approximate independence claim is empirically testable. A study in which participants receive the same task under different explicit variation instructions (e.g., "analyse this dataset adversarially" versus "analyse this dataset engagingly") and produce measurably different outputs would constitute evidence for the claim. A negative result, showing no output difference regardless of variation instruction, would falsify it. This testability distinguishes G.E.A.R. from personality taxonomies, which are descriptive and therefore difficult to falsify against specific task outcomes.

## 5.3 Structural Geometry of the Variations

The four gears are not an arbitrary list. They emerge from two structurally orthogonal axes:

- **Temporal axis (forward ↔ backward):** Generative (forward, into the present act of making) versus Reflective (backward, into past experience and accumulated learning).
- **Structural axis (split ↔ join):** Adversarial (split, decomposing through opposition) versus Engaging (join, composing through cross-domain fusion).

This 2×2 decomposition means the four gears occupy maximally distinct positions in a two-dimensional cognitive space. The blind spot pairs (Generative ↔ Reflective, Adversarial ↔ Engaging) correspond to diagonal opposites in this space, providing a geometric rationale for why they represent maximal cognitive distance.

The structural alignment with classical elemental frameworks, particularly the Tamil five-element system known as Panchabhootam (பஞ்சபூதம், a classical framework mapping cognitive and physical phenomena to five elemental categories), is noted as a historical resonance rather than a causal claim. In this system, Air (forward), Earth (backward), Fire (split), and Water (join) occupy the four cardinal directions, with Space (Akasam) at the centre representing emergence. We do not argue that the gears *derive from* elemental philosophy; we observe that independent analysis of cognitive posture geometry converges on a structure that pre-modern wisdom traditions had already mapped.

---

# 6. Conclusion

This paper identified the *variation gap*: the systematic absence, across cognitive frameworks in psychology and AI agent design, of a dimension capturing *how* an agent thinks while performing a task, independently of the task itself. Bloom's Taxonomy describes cognitive levels. De Bono's Six Thinking Hats describe task-coupled modes. Dual-process theory describes processing depth. BDI and ReAct describe action selection. CoALA provides a unifying vocabulary. None parameterises cognitive posture as an approximately independent design variable.

We proposed Cognitive Variation Theory and its operationalisation through *G.E.A.R.*: four cognitive variations (Generative, Engaging, Adversarial, Reflective) formalised with definitions, six-dimension cognitive signatures, boundary conditions, anti-patterns, and two blind spot pairs. The variation-verb matrix demonstrates the combinatorial claim: a small number of variations applied across a set of cognitive actions produces a large space of distinct cognitive acts.

We evaluated G.E.A.R. through comparative analysis with eleven existing frameworks and three practitioner vignettes. The differentiation matrix (Table 1) shows that G.E.A.R. is the first framework combining posture-awareness, approximate independence from task, and a blind spot model. The vignettes provide existence proofs that variation-aware task design surfaces insights invisible to default-variation execution.

## Future Work

Four research directions follow directly from this work:

1. **Controlled experiment.** A crossed factorial design (variation-instruction × task-type) measuring output quality and cognitive process. If the approximate independence claim holds, output quality should depend on variation regardless of task type, with no significant variation × task interaction. If the interaction is significant, the claim requires qualification, and the terms of that qualification (which task-variation combinations interact, and why) become the next research question.

2. **Agent benchmark.** A comparative evaluation of variation-parameterised agents versus fixed-variation agents on a diverse task suite. The prediction is that variation-parameterised agents achieve higher task-level coverage (detecting more types of insight per task) at minimal computational cost increase, since the variation parameter modifies the system prompt, not the model or tool set.

3. **Cross-cultural and cross-professional study.** An empirical investigation of whether variation defaults differ by national culture, professional domain, or organisational context. The hypothesis is that defaults vary (engineering cultures default adversarial; design cultures default generative) but the four-gear structure itself is stable across contexts.

4. **Cognitive cost of variation-switching.** An integration with cognitive load theory (Sweller, 1988) to measure whether deliberate gear-shifting carries a measurable cognitive switching cost, and if so, whether the benefit (broader cognitive coverage) outweighs the cost under the conditions identified in the vignettes.

The variation gap is not merely theoretical. Every AI agent system that operates in a single cognitive posture per verb, every team that runs meetings in a single mode, and every learner who has never named their default gear is paying the cost of an unmapped dimension. G.E.A.R. does not claim to be the final taxonomy of cognitive variation. It claims to be the first framework that treats variation as a design variable, and provides the vocabulary and the matrix for practitioners and architects to begin engineering with it.

---

# References

Ackerman, R. and Thompson, V. (2017). Meta-reasoning: Monitoring and control of thinking and reasoning. *Trends in Cognitive Sciences*, 21(8), 607-617.

Anderson, L. W. and Krathwohl, D. R. (Eds.) (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. Longman.

Bacchelli, A. and Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. In *Proceedings of the 35th International Conference on Software Engineering (ICSE)*, 712-721.

Bloom, B. S. (Ed.) (1956). *Taxonomy of Educational Objectives: The Classification of Educational Goals. Handbook I: Cognitive Domain*. David McKay.

Braem, S. and Egner, T. (2024). The brain learns to be flexible: Meta-flexibility as a higher-order cognitive adaptation. *Nature Reviews Neuroscience*, forthcoming.

Bratman, M. E. (1987). *Intention, Plans, and Practical Reason*. Harvard University Press.

Christakopoulou, K., Lalani, S., and others (2024). The Talker-Reasoner architecture for conversational AI. *Google DeepMind Technical Report*.

Coffield, F., Moseley, D., Hall, E., and Ecclestone, K. (2004). *Learning Styles and Pedagogy in Post-16 Learning: A Systematic and Critical Review*. Learning and Skills Research Centre.

Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row.

de Bono, E. (1985). *Six Thinking Hats*. Little, Brown.

Evans, J. St. B. T. and Stanovich, K. E. (2013). Dual-process theories of higher cognition: Advancing the debate. *Perspectives on Psychological Science*, 8(3), 223-241.

Hommel, B. (2015). Between persistence and flexibility: The yin and yang of action control. *Advances in Motivation Science*, 2, 33-67.

Janis, I. L. (1972). *Victims of Groupthink*. Houghton Mifflin.

Jiang, Y. and others (2025). Chain of Mindset: Multi-mindset reasoning for mathematical problem solving. *Peking University Technical Report*.

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Kolb, D. A. (1984). *Experiential Learning: Experience as the Source of Learning and Development*. Prentice Hall.

Lakoff, G. and Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.

Mercier, H. and Sperber, D. (2017). *The Enigma of Reason*. Harvard University Press.

Morrison, A. B., Rosenbaum, G. M., Fair, D., and Chein, J. M. (2016). Variation in strategy use across measures of verbal working memory. *Memory and Cognition*, 44, 922-936.

Newton, C., Feeney, J., and Pennycook, G. (2023). On the multidimensionality of thinking dispositions: A large-scale factor analytic investigation. *Thinking and Reasoning*, forthcoming.

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., and Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST)*.

Polanyi, M. (1966). *The Tacit Dimension*. University of Chicago Press.

Rao, A. S. and Georgeff, M. P. (1995). BDI agents: From theory to practice. In *Proceedings of the First International Conference on Multi-Agent Systems (ICMAS)*, 312-319.

Schon, D. A. (1983). *The Reflective Practitioner: How Professionals Think in Action*. Basic Books.

Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and Yao, S. (2023). Reflexion: Language agents with verbal reinforcement learning. In *Advances in Neural Information Processing Systems (NeurIPS)*.

Stanovich, K. E. (2016). The Comprehensive Assessment of Rational Thinking. *Educational Psychologist*, 51(1), 23-34.

Sumers, T. R., Yao, S., Narasimhan, K., and Griffiths, T. L. (2024). Cognitive architectures for language agents. *Transactions on Machine Learning Research (TMLR)*.

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285.

Tetlock, P. E. (2005). *Expert Political Judgment: How Good Is It? How Can We Know?* Princeton University Press.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., and Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. In *Advances in Neural Information Processing Systems (NeurIPS)*.

Yang, Y. and others (2026). ARES: Adaptive reasoning effort search for language model agents. *University of California, Santa Barbara Technical Report*.

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations (ICLR)*.

Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., and Narasimhan, K. (2023). Tree of thoughts: Deliberate problem solving with large language models. In *Advances in Neural Information Processing Systems (NeurIPS)*.

Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H., and Wang, Y.-X. (2024). Language agent tree search unifies reasoning, acting, and planning in language models. In *Proceedings of the 41st International Conference on Machine Learning (ICML)*.

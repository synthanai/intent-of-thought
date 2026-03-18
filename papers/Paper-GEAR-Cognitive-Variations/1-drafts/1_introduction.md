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

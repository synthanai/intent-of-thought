## 2. Background and Related Work

We survey the landscape of reasoning topologies (Section 2.1), then examine how intent has been applied at different levels of AI reasoning systems (Sections 2.2-2.3), and conclude with a differentiation matrix that reveals the topology-governance gap (Section 2.4).

### 2.1 X-of-Thought Reasoning Topologies

The X-of-Thought (XoT) family encompasses a growing set of structured reasoning methods for LLMs. We categorise them by their topological structure following the taxonomy of [@besta2025topologies].

**Chain-based topologies.** Chain-of-Thought (CoT; [@wei2022chain]) generates a linear sequence of intermediate reasoning steps. Zero-shot CoT [@kojima2022zero] achieves this without exemplars via the prompt "Let's think step by step." Self-Consistency [@wang2023self] samples multiple chains and selects by majority vote. Program-of-Thought (PoT; [@chen2023program]) generates executable code as its reasoning chain. These methods share a common structural assumption: reasoning proceeds as a linear sequence where each step depends on the previous one.

**Tree-based topologies.** Tree-of-Thought (ToT; [@yao2023tree]) organises reasoning as a search tree, where each node represents a partial solution and branches represent alternative continuations. Evaluation functions score intermediate states, enabling backtracking and parallel exploration. LATS [@zhou2023lats] combines tree search with Monte Carlo Tree Search (MCTS) for more efficient exploration.

**Graph-based topologies.** Graph-of-Thoughts (GoT; [@besta2024graph]) generalises tree structures by allowing reasoning steps to be combined, refined, and looped. This enables operations like merging partial solutions and iterative refinement that are impossible in strictly hierarchical structures.

**Abstraction-based topologies.** Abstraction-of-Thought (AoT; [@hong2024abstraction]) introduces hierarchical problem classification before reasoning, decomposing problems into abstract types before engaging with specifics. This operates at the level of *what type* of problem is being solved, distinct from *how* to solve it.

Additional topologies include Buffer-of-Thought (problem-type libraries), Skeleton-of-Thought (parallel skeleton filling), and Meta-of-Thought (dynamic topology switching). The proliferation is striking: [@besta2025topologies] catalogues fourteen distinct topological structures, each with associated benchmark results. Yet across this entire landscape, a fundamental question remains unexamined: *given a reasoning task, which topology should be selected, and on what basis?*

### 2.2 Intent in AI Reasoning

Recent work has begun to introduce intent as an explicit variable in reasoning processes. We identify three levels at which this has occurred.

**Step-level intent.** Speaking with Intent (SWI; [@yin2025swi]) adds explicit `<INTENT>` tags before each reasoning step, requiring the model to state what it aims to accomplish with each step before executing it. Experimental results demonstrate consistent improvements over standard CoT across multiple benchmarks, providing direct evidence that articulating step-level purpose improves reasoning quality.

**Domain-level intent.** Intention Chain-of-Thought (ICoT; [@li2025icot]) introduces "intention abstraction" for code generation, comprising a specification component (what the code should do) and an algorithmic strategy component (how to approach it). This represents intent at the domain level: specific to code generation, not generalisable across reasoning tasks.

**Retrieval-level intent.** Analyse-Retrieve-Reason (ARR; [@yin2025arr]) adds an intent analysis phase before the retrieval step in question answering. By first analysing the question's purpose, ARR improves retrieval relevance and downstream reasoning quality. This operates at the retrieval stage, governing what to retrieve, not how to reason about it.

These contributions demonstrate that explicit intent improves reasoning outcomes. However, all three operate *within* a fixed topology. SWI improves chain steps but does not question whether a chain is the right structure. ICoT guides code generation but assumes a chain topology. ARR improves retrieval but does not address reasoning structure. The question of which topology to deploy remains outside their scope.

### 2.3 Intent in Agent Theory and Alignment

The concept of intention has a rich history in agent theory and AI alignment, operating at levels distinct from reasoning topology.

**Agent-action intent (BDI).** The Belief-Desire-Intention (BDI) architecture [@bratman1987intention; @cohen1990intention; @rao1995bdi] provides formal semantics for intention as "choice with commitment" [@cohen1990intention]. Intentions in BDI govern agent *actions*: what to do, when to persist, and when to reconsider. Cohen and Levesque's formulation of "relativised persistent goals" provides termination semantics (abandon a goal when it is achieved, believed unachievable, or when background conditions change) that are relevant to our Anti-Purpose primitive. However, BDI intention governs *what an agent does*, not *how an agent reasons*. The distinction between action governance and reasoning-topology governance is central to our contribution.

**Training-level intent (RLHF/DPO).** Reinforcement Learning from Human Feedback (RLHF; [@ouyang2022instructgpt]) and Direct Preference Optimisation (DPO; [@rafailov2023dpo]) align model behaviour with user intent at the training level. These methods shape the model's general disposition toward helpfulness and safety, but they do not provide task-specific topology selection. A model trained with RLHF will default to chain-of-thought reasoning regardless of whether a tree or graph structure would better serve the task's purpose.

**Latent intent.** Tutunov et al. [-@tutunov2024latent] and Jiang [-@jiang2024latent] have independently proposed that intent functions as a latent variable underlying chain-of-thought reasoning. This theoretical perspective suggests that intent is already *present* in reasoning but *implicit*. Our work complements this view: we propose making intent *explicit* and *operational* at the topology-governance level.

### 2.4 The Differentiation Matrix

Table 1 summarises the landscape of intent-in-reasoning across six levels. The topology-governance level (row 6) represents the gap that this paper addresses.

**Table 1: Intent-in-reasoning differentiation matrix.**

| Level | Representative Work | What It Governs | What It Does NOT Govern |
|:------|:-------------------|:----------------|:-----------------------|
| 1. Step | SWI [@yin2025swi] | Individual reasoning step quality | Which topology to use |
| 2. Domain | ICoT [@li2025icot] | Code generation strategy | General-purpose reasoning |
| 3. Retrieval | ARR [@yin2025arr] | Pre-retrieval question analysis | Reasoning structure |
| 4. Agent-action | BDI [@cohen1990intention] | External actions, commitments | Internal reasoning process |
| 5. Training | RLHF/DPO [@ouyang2022instructgpt] | Model behavioural alignment | Per-task topology selection |
| **6. Topology** | **This paper** | **Which reasoning structure to deploy** | **, ** |

The matrix reveals a clear architectural gap. Step-level intent operates *within* a topology. Agent-action intent operates *outside* reasoning entirely. Training-level intent shapes general disposition. None provide a mechanism for connecting the *purpose* of a specific reasoning task to the *selection* of an appropriate reasoning structure.

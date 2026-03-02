# Intent of Thought: A Pre-Reasoning Governance Layer for Topology Selection in LLM Reasoning

**Naveen Riaz Mohamed Kani**
ORCID: [0009-0003-9173-2425](https://orcid.org/0009-0003-9173-2425)

## Abstract

The proliferation of reasoning topologies for large language models, from Chain-of-Thought [@wei2022chain] through Tree-of-Thought [@yao2023tree] to Graph-of-Thoughts [@besta2024graph], has created a rich structural landscape for AI reasoning. Yet across this landscape, a critical question remains unaddressed: *which topology should be deployed for a given reasoning task, and why?* While recent work has introduced intent at the step level (SWI; [@yin2025swi]), the domain level (ICoT; [@li2025icot]), and the retrieval stage (ARR; [@yin2025arr]), no existing framework formalises intent as a governance mechanism for topology selection itself. We survey intent-in-reasoning across five distinct levels and identify this topology-governance gap. We then propose *Intent of Thought* (IoT), a three-primitive pre-reasoning checkpoint comprising Purpose, Anti-Purpose, and Success Signal that governs which reasoning structure to deploy. We formalise IoT with a topology selection function and an intent drift detection mechanism, and demonstrate its utility through three illustrative case studies spanning sequential, exploratory, and interconnected reasoning tasks. We conclude by proposing the Topology Selection Benchmark (TSB) as a community resource for evaluating purpose-governed reasoning.

---

## 1. Introduction

Since the publication of Chain-of-Thought prompting [@wei2022chain], the landscape of structured reasoning for large language models (LLMs) has expanded rapidly. More than thirty distinct reasoning topologies have been proposed in under three years, each offering a different structural approach to the problem of multi-step inference. Tree-of-Thought (ToT; [@yao2023tree]) introduced parallel exploration with state evaluation. Graph-of-Thoughts (GoT; [@besta2024graph]) enabled non-linear reasoning with refinement loops. Abstraction-of-Thought (AoT; [@hong2024abstraction]) added hierarchical problem classification. Buffer-of-Thought, Skeleton-of-Thought, and numerous other variants have followed, each contributing a new structural primitive to the reasoning toolkit.

This explosion of topologies has created a selection problem. When a practitioner or an automated system encounters a reasoning task, which topology should be deployed? Current practice relies on one of three informal mechanisms: researcher intuition (the paper author selects a topology for their benchmark), prompt heuristics (chain for simple tasks, tree for exploration), or fixed assignment (a single topology is baked into the system regardless of the task). None of these mechanisms are grounded in a formal analysis of the task's *purpose*.

Recent work has begun to address the role of intent in reasoning. Speaking with Intent (SWI; [@yin2025swi]) adds explicit `<INTENT>` tags before individual reasoning steps, demonstrating that step-level intent improves performance. Intention Chain-of-Thought (ICoT; [@li2025icot]) introduces intention abstraction for code generation tasks, combining specification and algorithmic strategy into a two-stage intent-guided pipeline. Analyze-Retrieve-Reason (ARR; [@yin2025arr]) incorporates intent analysis before the retrieval step in question answering, improving retrieval relevance and downstream reasoning. These contributions are valuable, but they operate *within* a fixed topology. SWI improves the quality of individual chain steps; it does not determine whether a chain, tree, or graph should have been selected in the first place.

We call this the *topology-governance gap*: the absence of a formal mechanism that connects the *purpose* of a reasoning task to the *selection* of a reasoning structure. This gap is distinct from the well-studied intent constructs in agent theory (BDI architectures govern agent *actions*, not reasoning *topologies*; [@cohen1990intention; @rao1995bdi]) and alignment research (RLHF governs model *training*, not per-task topology selection; [@ouyang2022instructgpt]).

In this paper, we make three contributions:

1. **Gap Analysis.** We survey intent-in-reasoning across five levels (step, domain, retrieval, agent-action, and training) and identify topology-governance as the missing sixth level (Section 2).

2. **Framework.** We propose Intent of Thought (IoT), a three-primitive pre-reasoning checkpoint comprising Purpose, Anti-Purpose, and Success Signal, with a topology selection algorithm and an intent drift detection protocol (Section 3).

3. **Illustrative Evaluation.** We demonstrate IoT on three case studies where purpose-governed topology selection outperforms ad-hoc selection across sequential, exploratory, and interconnected reasoning tasks (Section 4).

We note that the abbreviation "IoT" has been used for "Internet of Things" and for "Iteration of Thought" [@radha2024iteration], an iterative prompting method. Our use refers specifically to *Intent* of Thought, and context disambiguates throughout.[^1]

[^1]: Iteration of Thought [@radha2024iteration] proposes iterative inner dialogue loops within a fixed chain topology. Intent of Thought addresses a different problem: selecting *which* topology to use based on stated purpose.

The remainder of this paper is organised as follows. Section 2 surveys reasoning topologies and intent-in-reasoning at five levels, culminating in a differentiation matrix that reveals the topology-governance gap. Section 3 presents the IoT framework with formal notation. Section 4 demonstrates IoT through three illustrative case studies. Section 5 discusses limitations and proposes the Topology Selection Benchmark, and Section 6 concludes with directions for future work.
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

**Retrieval-level intent.** Analyze-Retrieve-Reason (ARR; [@yin2025arr]) adds an intent analysis phase before the retrieval step in question answering. By first analysing the question's purpose, ARR improves retrieval relevance and downstream reasoning quality. This operates at the retrieval stage, governing what to retrieve, not how to reason about it.

These contributions demonstrate that explicit intent improves reasoning outcomes. However, all three operate *within* a fixed topology. SWI improves chain steps but does not question whether a chain is the right structure. ICoT guides code generation but assumes a chain topology. ARR improves retrieval but does not address reasoning structure. The question of which topology to deploy remains outside their scope.

### 2.3 Intent in Agent Theory and Alignment

The concept of intention has a rich history in agent theory and AI alignment, operating at levels distinct from reasoning topology.

**Agent-action intent (BDI).** The Belief-Desire-Intention (BDI) architecture [@bratman1987intention; @cohen1990intention; @rao1995bdi] provides formal semantics for intention as "choice with commitment" [@cohen1990intention]. Intentions in BDI govern agent *actions*: what to do, when to persist, and when to reconsider. Cohen and Levesque's formulation of "relativised persistent goals" provides termination semantics (abandon a goal when it is achieved, believed unachievable, or when background conditions change) that are relevant to our Anti-Purpose primitive. However, BDI intention governs *what an agent does*, not *how an agent reasons*. The distinction between action governance and reasoning-topology governance is central to our contribution.

**Training-level intent (RLHF/DPO).** Reinforcement Learning from Human Feedback (RLHF; [@ouyang2022instructgpt]) and Direct Preference Optimization (DPO; [@rafailov2023dpo]) align model behaviour with user intent at the training level. These methods shape the model's general disposition toward helpfulness and safety, but they do not provide task-specific topology selection. A model trained with RLHF will default to chain-of-thought reasoning regardless of whether a tree or graph structure would better serve the task's purpose.

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
| **6. Topology** | **This paper** | **Which reasoning structure to deploy** | **—** |

The matrix reveals a clear architectural gap. Step-level intent operates *within* a topology. Agent-action intent operates *outside* reasoning entirely. Training-level intent shapes general disposition. None provide a mechanism for connecting the *purpose* of a specific reasoning task to the *selection* of an appropriate reasoning structure.
## 3. Intent of Thought

We now present Intent of Thought (IoT), a pre-reasoning governance layer that connects the purpose of a reasoning task to the selection of an appropriate topology. IoT comprises three primitives (Section 3.1), a specification format (Section 3.2), a topology selection algorithm (Section 3.3), and an intent drift detection protocol (Section 3.4).

### 3.1 The Three Primitives

IoT specifies the *intent* of a reasoning task through three complementary primitives:

**Purpose ( P ).** The desired outcome of the reasoning process. Purpose answers "WHY are we reasoning?" and specifies the end-state that the agent seeks to achieve. Unlike a task description (which specifies *what* to do), Purpose specifies *why* the reasoning matters and what constitutes a good outcome. For instance, a Purpose might be "identify the optimal investment allocation across three asset classes" rather than "solve this optimisation problem."

**Anti-Purpose ( P-bar ).** The set of outcomes that would render the reasoning worthless. Anti-Purpose answers "what must we AVOID?" and specifies explicit failure conditions, drawing on the BDI tradition of commitment termination [@cohen1990intention]. Anti-Purpose is operationally distinct from constraints: where constraints limit the solution space, Anti-Purpose identifies what would make the entire reasoning episode a waste. For example: "avoid recommending allocations that ignore tax implications" is a constraint, while "reasoning that treats the three asset classes as independent when they are correlated" is an Anti-Purpose.

**Success Signal ( S ).** The criteria by which the agent (or an observer) determines that the reasoning has achieved its Purpose. Success Signal answers "HOW will we know we succeeded?" and provides evaluation criteria that are checkable during and after reasoning. Success Signals may be binary (achieved or not), graded (degree of satisfaction), or multi-dimensional (a set of criteria). For instance: "a ranked allocation with sensitivity analysis showing the impact of correlation assumptions."

These three primitives are complementary. Purpose without Anti-Purpose permits reasoning drift into technically valid but practically useless territory. Purpose without Success Signal provides no mechanism for detecting when reasoning should terminate. Anti-Purpose without Purpose is unconstrained negation. The triad functions as a pre-reasoning checkpoint: before selecting a reasoning topology, the agent must specify all three.

### 3.2 The IoT Specification

We define the IoT specification as a triple:

> **IoT** = (Purpose, Anti-Purpose, Success Signal)

or in shorthand: **IoT = (P, P-bar, S)**.

This triple is the input to the topology selection algorithm described below. It captures the *why* of a reasoning task in a structured form that can be matched against the structural characteristics of available topologies.

### 3.3 Topology Selection Algorithm

The selection algorithm takes the IoT specification and the problem context as input, and produces a ranked list of recommended topologies. The algorithm proceeds in three steps:

**Algorithm 1: Topology Selection**

```
Input:  IoT specification (P, P-bar, S), problem context
Output: Ranked list of recommended topologies

Step 1 — Extract purpose type.
  Analyse the Purpose to identify the dominant reasoning
  requirement: sequential derivation, parallel exploration,
  interconnected analysis, hierarchical classification,
  or multi-phase complex reasoning.

Step 2 — Match purpose type to topology.
  Use Table 2 to identify the topology whose structural
  properties best align with the identified purpose type.

Step 3 — Apply Anti-Purpose constraints.
  Check whether the candidate topology would structurally
  violate the Anti-Purpose. If it does, demote it and
  promote the next candidate.

Output: Ordered list, most aligned topology first.
```

**Table 2: IoT topology selection mapping.**

| Purpose Type | Structural Signal | Recommended Topology | Rationale |
|:-------------|:-----------------|:--------------------|:----------|
| Sequential derivation | Single valid path, step dependencies | CoT | Linear chain; each step builds on the previous |
| Parallel exploration | Multiple viable approaches, uncertain best path | ToT | Branching enables evaluation of alternatives before commitment |
| Interconnected analysis | Non-linear relationships, feedback loops | GoT | Graph structure supports refinement and merging |
| Hierarchical classification | Problem type matters before details | AoT | Abstraction first, then type-specific reasoning |
| Multi-phase complex | Requires multiple reasoning modes | Hybrid | Sequential phases with different structural needs |

The mapping is not deterministic. Purpose determines the general topology class, Anti-Purpose adds constraints (e.g., "avoid premature commitment to a single path" favours ToT over CoT), and Success Signal informs the evaluation mechanism within the selected topology.

### 3.4 Intent Drift Detection

Reasoning drift occurs when a multi-step reasoning process gradually diverges from its stated purpose, producing outputs that are internally coherent but misaligned with the original intent. This phenomenon is well-documented: Reflexion [@shinn2023reflexion] addresses it through episodic feedback signals, and RLHF [@ouyang2022instructgpt] addresses it at the training level. IoT addresses it at the topology-governance level through continuous monitoring.

**Algorithm 2: Intent Drift Detection**

```
Input:  IoT specification (P, P-bar, S), reasoning trace
Output: Continue, correct, switch topology, or terminate

Step 1 — Anchor.
  At the start of reasoning, record the Purpose as the
  reference point for alignment checks.

Step 2 — Monitor.
  At regular intervals during reasoning, compare the
  current direction of reasoning against the stated Purpose.

Step 3 — Check for drift.
  If the reasoning has diverged significantly from Purpose:
    a. Re-read the IoT specification (P, P-bar, S).
    b. Evaluate whether the current topology is still
       appropriate for the stated Purpose.
    c. If topology is mismatched: re-run Algorithm 1
       with updated context.
    d. If topology is appropriate: add a purpose-
       realignment step to the reasoning chain.

Step 4 — Check for Anti-Purpose violation.
  If the reasoning has entered territory explicitly
  identified by Anti-Purpose: trigger immediate correction.

Step 5 — Check for completion.
  If the Success Signal is satisfied: terminate reasoning.
  If the Purpose is believed unachievable: terminate and
  report (following Cohen and Levesque's [-@cohen1990intention]
  termination semantics).
```

This protocol draws on BDI commitment termination but applies it to the reasoning process itself rather than to agent actions. The agent maintains its reasoning commitment until: (a) the Purpose is achieved (Success Signal satisfied), (b) the Purpose is believed unachievable, or (c) background conditions have changed such that the original Purpose is no longer relevant.
## 4. Preliminary Evaluation

We demonstrate IoT through three case studies, each selected to illustrate a distinct topology-governance scenario. For each case, we specify the IoT triple (Purpose, Anti-Purpose, Success Signal), show the topology recommended by the selection algorithm, and contrast it with the outcome of ad-hoc topology selection.

### 4.1 Case Study Design

We selected three reasoning problems that represent distinct topological requirements: sequential derivation (optimal for CoT), parallel exploration (optimal for ToT), and interconnected analysis (optimal for GoT). For each problem, we demonstrate that the IoT specification provides sufficient information to select the correct topology, and that selecting an alternative topology leads to suboptimal reasoning behaviour.

These case studies are illustrative, not statistically evaluated. We present them as evidence that the IoT framework provides a principled basis for topology selection, and we propose a formal benchmark (Section 5.2) for large-scale evaluation.

### 4.2 Case 1: Sequential Derivation (IoT recommends CoT)

**Problem.** A multi-step mathematical proof requiring logical deduction: "Prove that the sum of the first *n* odd numbers equals *n* squared."

**IoT Specification.**
- **Purpose:** "Derive a valid proof through a sequence of logically dependent steps."
- **Anti-Purpose:** "Skipping steps, assuming intermediate results, or exploring alternative proof strategies when a single valid path exists."
- **Success Signal:** "Each step logically follows from the previous; the final step establishes the identity."

**Selection.** The selection algorithm (Algorithm 1) identifies structural signals: single valid path, step dependencies, no need for parallel exploration. It recommends Chain-of-Thought as the primary topology.

**Contrast.** Deploying ToT would generate parallel branches of proof attempts, evaluating intermediate states across multiple paths. For this problem, where only one valid proof path exists (by induction), the branching overhead of ToT is wasted computation. The Anti-Purpose explicitly forbids "exploring alternative proof strategies when a single valid path exists," which a tree topology would inherently do.

### 4.3 Case 2: Parallel Exploration (IoT recommends ToT)

**Problem.** An open-ended design challenge: "Propose three distinct user interface layouts for a mobile banking application, evaluate their usability trade-offs, and recommend one."

**IoT Specification.**
- **Purpose:** "Discover and evaluate multiple viable design alternatives before committing to a recommendation."
- **Anti-Purpose:** "Committing to the first design that comes to mind without evaluating alternatives; producing variations of a single concept rather than genuinely distinct approaches."
- **Success Signal:** "At least three structurally distinct layouts presented, with explicit trade-off analysis across at least two usability dimensions, and a justified recommendation."

**Selection.** The selection algorithm identifies: multiple viable paths, uncertain best solution, evaluation required before commitment. It recommends Tree-of-Thought as the primary topology, with Graph-of-Thoughts as a secondary option.

**Contrast.** Deploying CoT would produce a single linear chain of reasoning, likely generating one design, refining it, and presenting it as the recommendation. The chain topology cannot naturally explore parallel alternatives because each step builds on the previous one. The Anti-Purpose explicitly forbids premature commitment, which a chain topology structurally encourages. The Success Signal requires three distinct layouts, which is naturally supported by ToT's branching structure but would require explicit self-instruction under CoT.

### 4.4 Case 3: Interconnected Analysis (IoT recommends GoT)

**Problem.** A systems analysis task: "Analyse the causal factors contributing to a hospital's increasing patient readmission rates, considering the interrelationships between staffing levels, discharge planning, patient education, and follow-up care coordination."

**IoT Specification.**
- **Purpose:** "Map the causal relationships between all contributing factors, including feedback loops and indirect effects."
- **Anti-Purpose:** "Treating contributing factors as independent variables when they interact; producing a linear causal chain when the reality is a causal network."
- **Success Signal:** "A relationship map showing at least four causal factors with bidirectional dependencies and at least one feedback loop identified."

**Selection.** The selection algorithm identifies: non-linear relationships, feedback loops, interdependencies. It recommends Graph-of-Thoughts as the primary topology, with Tree-of-Thought as a fallback.

**Contrast.** Deploying CoT would linearise the analysis: "staffing affects discharge planning, which affects patient education, which affects readmission." This linear chain misses the feedback loop (readmission rates affect staffing pressure, which affects discharge planning quality). Deploying ToT would explore parallel branches but would not naturally merge insights across branches. GoT's graph structure supports the refinement and merging operations needed to identify bidirectional causal relationships. The Anti-Purpose explicitly forbids treating factors as independent, which chain and tree topologies structurally tend to do.
## 5. Discussion

### 5.1 Limitations

We acknowledge several limitations of the current work.

**Table 3: Limitations and mitigations.**

| Limitation | Impact | Mitigation |
|:-----------|:-------|:-----------|
| No large-scale experiments | Cannot claim statistical significance for topology selection improvements | Case studies demonstrate framework utility; formal benchmark proposed below |
| Intent ambiguity | Users may specify unclear or contradictory Purpose/Anti-Purpose | Iterative refinement: if the selection function cannot rank topologies with confidence below a threshold, prompt for Purpose clarification |
| Goodhart vulnerability | Success Signals may be optimised superficially without achieving genuine Purpose | Multi-metric evaluation: require Success Signals to include at least one process-level and one outcome-level criterion |
| Anti-Purpose overreach | Excessively broad Anti-Purpose specifications may exclude all viable topologies | Priority ordering: rank Anti-Purpose constraints and relax lower-priority constraints when no topology satisfies all |
| Single-model scope | Case studies are model-agnostic illustrations, not tested across LLM families | TSB benchmark will evaluate across model families (open-weight and proprietary) |
| Drift threshold sensitivity | The threshold $\tau$ for intent drift detection is a hyperparameter without established tuning guidance | Propose empirical calibration as part of TSB benchmark, with task-specific thresholds |

### 5.2 Toward a Topology Selection Benchmark (TSB)

The absence of a benchmark for evaluating topology selection quality is, itself, evidence of the topology-governance gap. We propose the **Topology Selection Benchmark (TSB)** as a community resource for future evaluation.

TSB would consist of:

1. **Problem set.** A curated collection of reasoning problems spanning the topology types in Table 2: sequential derivation, parallel exploration, interconnected analysis, hierarchical classification, and multi-phase complex tasks.
2. **Intent specifications.** For each problem, a canonical IoT triple (Purpose, Anti-Purpose, Success Signal) authored by domain experts.
3. **Expert-labelled topologies.** For each problem, the topology or topologies judged optimal by domain experts, with justification.
4. **Evaluation metrics.** Topology selection accuracy (does the system select the expert-labelled topology?), intent drift score (does reasoning stay aligned with Purpose?), anti-purpose violation rate (does reasoning enter the Anti-Purpose space?), and success signal satisfaction (does the output meet the Success Signal criteria?).

We invite the research community to contribute problems, intent specifications, and expert topology labels to accelerate the development of this benchmark.

### 5.3 Concurrent and Related Work

During the preparation of this paper, two related works came to our attention that further validate the topology-governance gap.

**STELAR-VISION** \cite{stelar2025vision} investigates test-time topology selection for Vision-Language Models (VLMs), training models to autonomously select between Chain, Tree, and Graph reasoning structures. While STELAR-VISION addresses topology selection in the vision domain, IoT operates at the general-purpose reasoning level and introduces the governance triple (Purpose, Anti-Purpose, Success Signal) as the selection criterion, rather than learning selection from task-specific training data. The two approaches are complementary: STELAR-VISION's learned selection could serve as the execution layer beneath IoT's intent-governed selection.

**Framework of Thoughts (FoT)** \cite{ding2024fot} proposes a general-purpose foundational framework for building and optimising dynamic reasoning schemes. FoT provides the meta-architecture for composing reasoning structures, but does not address the governance question of *which* structure to deploy for a given purpose. IoT fills this gap: it can serve as the governance layer that informs FoT's dynamic scheme construction.

The emergence of these concurrent works, each addressing adjacent aspects of the topology-governance problem, reinforces our claim that this gap is a recognised need in the field.

### 5.4 Broader Implications

IoT suggests a broader architectural principle: reasoning systems benefit from a layered governance structure where *why* (purpose) informs *what type* (problem classification) informs *how* (step-by-step execution). This layered architecture separates concerns: the purpose layer handles goal specification and drift detection, the classification layer handles problem decomposition, and the execution layer handles step-level reasoning. Each layer can be improved independently.

This three-layer pattern is not unique to LLM reasoning. In human deliberation, effective decisions typically involve articulating direction before committing to process, and process before committing to action. When this sequence is violated (when teams begin executing before clarifying purpose, or commit to a decision method before understanding the problem type), the result is reasoning drift: internally coherent activity that is misaligned with the original intent. IoT formalises this observation for computational reasoning systems, suggesting that the topology-governance gap is not merely an engineering oversight but a reflection of a latent intent structure that is present, though typically implicit, in skilled human reasoning.

A practical consideration for IoT deployment is the question of *how* intent should be captured. We observe that capture mechanisms can range from fully implicit (the system infers intent from context) to fully explicit (the user specifies Purpose, Anti-Purpose, and Success Signal in structured form). The appropriate capture depth should scale with task complexity and consequence: routine queries require no explicit capture, while high-stakes reasoning benefits from full specification of all three primitives. This suggests a spectrum of capture modes that can be adapted to different application domains and user populations.

Finally, we note three failure modes that IoT is specifically designed to prevent, each corresponding to a breakdown in the governance sequence: (1) *false discovery*, where intent is nominally stated but not genuinely examined, leading to unreflective topology selection; (2) *false process*, where problem classification becomes an end in itself without reaching execution; and (3) *false delivery*, where reasoning chains execute fluently but disconnected from their original purpose. Intent drift detection (Section 3.4) addresses failure mode (3); the full IoT checkpoint addresses modes (1) and (2).
## 6. Conclusion

The rapid growth of X-of-Thought reasoning topologies has created a rich structural landscape for LLM reasoning, yet the question of *which topology to deploy for a given task* has remained ad-hoc and informal. We have surveyed intent-in-reasoning across five existing levels, from step-level intent (SWI) through agent-action intent (BDI) to training-level alignment (RLHF), and identified a sixth, unoccupied level: topology-governance.

To fill this gap, we proposed Intent of Thought (IoT), a three-primitive pre-reasoning checkpoint comprising Purpose, Anti-Purpose, and Success Signal. We formalised IoT with a topology selection function that maps intent specifications to appropriate reasoning structures, and an intent drift detection mechanism grounded in BDI termination semantics. Through three illustrative case studies, we demonstrated that purpose-governed topology selection identifies the structurally appropriate reasoning method where ad-hoc selection does not.

Three directions for future work are particularly promising. First, the Topology Selection Benchmark (TSB) proposed in Section 5.2 would enable large-scale empirical evaluation of purpose-governed topology selection across model families and problem domains. Second, training-time integration of IoT specifications (fine-tuning models to internalise the topology selection algorithm) could reduce the need for explicit pre-reasoning checkpoints. Third, the layered architecture implied by IoT (purpose, classification, execution) suggests a broader design pattern for reasoning systems that warrants formal investigation. Fourth, a complementary direction is retrospective intent reconstruction: given a reasoning trace that failed, can we infer what the latent intent should have been and which topology would have better served it? Forward IoT (this paper) governs reasoning before it begins; backward IoT would diagnose reasoning after it concludes.

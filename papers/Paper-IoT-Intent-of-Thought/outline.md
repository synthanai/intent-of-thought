# Paper Outline: Intent of Thought (IoT)

> **Venue**: Arxiv CS.AI + CL cross-list
> **Type**: Survey-framework hybrid with preliminary evaluation
> **Target**: 8-10 pages + references
> **Stealth**: No proprietary branding. Use "we propose" / "the authors."

---

## Contributions

| # | Contribution | Type |
|---|-------------|------|
| C1 | Structured analysis of intent-in-reasoning across 5 levels, identifying the topology-governance gap | Survey/Gap Analysis |
| C2 | IoT three-primitive framework (Purpose, Anti-Purpose, Success Signal) with formal notation and topology selection mechanism | Framework |
| C3 | Three worked case studies demonstrating purpose-governed topology selection | Preliminary Evaluation |

---

## Section 1: Introduction (1.5 pages)

### 1.1 The X-of-Thought Explosion
- Since Wei et al. (2022), 30+ reasoning topologies published: CoT, ToT, GoT, BoT, AoT, SoT, MoT, FoT, etc.
- Each optimises HOW to reason (chain, tree, graph, hybrid)
- Besta et al. (2025) surveys 14+ structures, proposes taxonomy

### 1.2 The Topology-Governance Gap
- All XoT methods assume topology is pre-selected (by researcher, prompt, or heuristic)
- Step-level intent exists (SWI), domain intent exists (ICoT), retrieval intent exists (ARR)
- But NO framework governs WHICH topology to deploy based on stated purpose
- Reasoning drift is a validated pathology (InstructGPT, Reflexion)

### 1.3 Contribution Statement
Three-bullet summary:
1. We survey intent-in-reasoning across 5 levels and identify the topology-governance gap
2. We propose IoT: a three-primitive pre-reasoning checkpoint for topology selection
3. We demonstrate IoT on 3 case studies spanning sequential, exploratory, and interconnected reasoning

### Research Sources
- Perplexity-1: XoT survey (30+ papers)
- Perplexity-2: XoT expanded (taxonomy, comparison)
- Signals: O2 (topology-governance gap confirmation)

---

## Section 2: Background and Related Work (2 pages)

### 2.1 X-of-Thought Reasoning Topologies
- CoT (Wei et al. 2022): linear chain, step-by-step
- ToT (Yao et al. 2023): tree search with state evaluation
- GoT (Besta et al. 2024): graph-structured reasoning with refinement
- AoT (Hong et al. 2024): multi-level abstraction within steps
- Brief coverage of BoT, SoT, MoT, FoT, LATS, PoT

### 2.2 Intent in AI Reasoning
- SWI (Yin et al. 2025): `<INTENT>` tags before each reasoning step → step-level
- ICoT (Zhang et al. 2024): intention abstraction (spec + strategy) → code domain
- ARR (Qi et al. 2024): intent analysis → retrieval stage
- Latent intent (Tutunov et al. 2024; Jiang 2024): intent as latent variable in CoT

### 2.3 Intent in Agent Theory and Alignment
- BDI (Bratman 1987; Cohen & Levesque 1990): intentions as committed goals → agent action
- Goal-conditioned RL: explicit goal variable g → policy training
- RLHF/DPO (Ouyang et al. 2022; Rafailov et al. 2023): aligning with user intent → training level
- Activation Steering (Turner et al. 2023): controllable internal representations

### 2.4 The Differentiation Matrix

**TABLE**: The centrepiece. Shows 5 levels of intent, each with existing work, what it governs, and what it DOESN'T govern.

| Level | Existing Work | Governs | Does NOT Govern |
|-------|--------------|---------|-----------------|
| Step-level | SWI (Yin 2025) | Individual reasoning steps | Topology selection |
| Domain-level | ICoT (Zhang 2024) | Code generation strategy | General reasoning |
| Retrieval-level | ARR (Qi 2024) | Pre-retrieval question analysis | Reasoning structure |
| Agent-action | BDI (Cohen & Levesque 1990) | External actions, commitments | Reasoning process |
| Training-level | RLHF/DPO | Model behaviour alignment | Per-task topology |
| **Topology-level** | **[THIS PAPER]** | **Which reasoning structure to deploy** |: |

### Research Sources
- Perplexity-3: intent prior art (SWI, ICoT, ARR, BDI, RL)
- ChatGPT-1: devil's advocate (SWI, ICoT identified as closest prior art)
- ChatGPT-2: BDI vs IoT deep comparison
- Signals: C1-C2 (clashes with SWI and BDI)

---

## Section 3: Intent of Thought (2.5 pages)

### 3.1 The Three Primitives

| Primitive | Question | Role |
|-----------|----------|------|
| **Purpose** (P) | WHY are we reasoning? | Specifies the desired end-state |
| **Anti-Purpose** (P̄) | What must we AVOID? | Specifies failure conditions, constraints |
| **Success Signal** (S) | HOW will we know we succeeded? | Specifies completion/evaluation criteria |

### 3.2 Formal Notation

Define:
- IoT := ⟨P, P̄, S⟩
- Topology space T := {CoT, ToT, GoT, AoT, Hybrid, ...}
- Selection function: f(IoT, context) → T*  (ordered subset of T)
- Drift detection: δ(reasoning_trace, P) → [0, 1]  (divergence score)
- Correction protocol: if δ > threshold, invoke IoT checkpoint

### 3.3 Topology Selection Mechanism

Map intent characteristics to topology recommendations:

| Purpose Type | Recommended Topology | Rationale |
|-------------|---------------------|-----------|
| Sequential derivation | CoT | Linear dependency chain |
| Parallel exploration | ToT | Multiple viable paths need evaluation |
| Interconnected analysis | GoT | Elements have non-linear relationships |
| Hierarchical classification | AoT | Problem TYPE matters before details |
| Multi-phase complex | Hybrid (IoT-AoT-CoT stack) | Requires multiple reasoning modes |

### 3.4 Intent Drift Detection

- Define Intent Drift Score (IDS): cosine similarity between stated purpose embedding and reasoning step embeddings over time
- Threshold-based correction: when IDS drops below threshold, invoke IoT checkpoint
- Anti-Purpose violation detection: flag when reasoning produces outputs in P̄ space
- Connection to existing drift work (Reflexion feedback signals, InstructGPT alignment)

### Research Sources
- Research.md: Section B (definitions, 3 primitives)
- Research.md: Section C (theoretical foundations, nomological network)
- Signals: V7 (topology-level intent governance is novel)

---

## Section 4: Preliminary Evaluation (1.5 pages)

### 4.1 Case Study Design
- 3 problems selected to demonstrate topology-governance value
- For each: state IoT specification (P, P̄, S), show framework recommending topology, compare against ad-hoc selection
- Stealth: describe reasoning framework generically (no branding)

### 4.2 Case 1: Sequential Problem (IoT → CoT)
- **Problem**: Multi-step arithmetic or logical derivation
- **IoT**: P = "derive the correct answer through valid steps", P̄ = "guessing or skipping steps", S = "each step logically follows from the previous"
- **Framework selects**: CoT (linear dependency, single valid path)
- **Contrast**: ToT would waste computation on parallel branches for a single-solution problem

### 4.3 Case 2: Exploratory Problem (IoT → ToT)
- **Problem**: Creative writing, brainstorming, or Game of 24
- **IoT**: P = "discover multiple viable approaches and select the best", P̄ = "committing to first approach without exploring alternatives", S = "at least 3 approaches evaluated, best one justified"
- **Framework selects**: ToT (multiple viable paths, evaluation needed)
- **Contrast**: CoT would commit to a single linear path, missing better alternatives

### 4.4 Case 3: Interconnected Problem (IoT → GoT)
- **Problem**: Multi-stakeholder decision or systems analysis
- **IoT**: P = "identify all causal connections between factors", P̄ = "treating factors as independent when they interact", S = "relationship graph with bidirectional dependencies mapped"
- **Framework selects**: GoT (non-linear relationships, refinement loops)
- **Contrast**: CoT would linearise inherently non-linear relationships

### Research Sources
- Research.md: Section D (measurement approaches)
- Signals: O5 (no existing topology-selection benchmark)
- NOOL v0.2: execution path Phase 4-5

---

## Section 5: Discussion (1 page)

### 5.1 Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance | Case studies demonstrate framework utility; TSB benchmark is future work |
| Intent ambiguity | Users may specify unclear purposes | Iterative refinement protocol proposed |
| Goodhart vulnerability | Success Signals can be gamed | Multi-metric evaluation recommended |
| Anti-Purpose scope | Unbounded constraints may block all topologies | Priority ordering of constraints |
| Single-model evaluation | Results may not generalise across LLMs | TSB benchmark will test across model families |

### 5.2 Toward a Topology Selection Benchmark (TSB)
- Propose TSB: problems paired with intent specifications and expert-labelled optimal topologies
- Metrics: topology selection accuracy, intent drift score, anti-purpose violation rate, success signal satisfaction
- Call to community: invite contributions to TSB dataset

### 5.3 Broader Implications
- IoT-AoT-CoT as a three-layer reasoning stack (brief, no branding)
- Connection to human decision-making (leaders asking "why are we meeting?" before "how should we decide?")
- Potential for training-time integration (fine-tuning with IoT specifications)

### Research Sources
- Signals: A2 (TSB design), A7 (IDS operationalisation)
- Research.md: Section G (evidence gaps)

---

## Section 6: Conclusion (0.5 pages)

### Summary
- Surveyed intent-in-reasoning across 5 levels
- Identified topology-governance as the missing level
- Proposed IoT: three primitives + selection mechanism + drift detection
- Demonstrated on 3 case studies

### Future Work
- Topology Selection Benchmark (TSB) with community contributions
- Integration of IoT with training-time fine-tuning
- Extension to multi-agent deliberation settings
- The three-layer reasoning stack (IoT-AoT-CoT) as future paper (no branding)

---

## References (~60-80 citations)

### Must-Cite
| Paper | Why |
|-------|-----|
| Wei et al. 2022 (CoT) | Foundation of XoT |
| Yao et al. 2023 (ToT) | Key topology |
| Besta et al. 2024 (GoT) | Key topology |
| Besta et al. 2025 (Topologies survey) | Closest survey |
| Hong et al. 2024 (AoT) | Sister concept |
| Yin et al. 2025 (SWI) | Closest prior art |
| Zhang et al. 2024 (ICoT) | Domain-level intent |
| Qi et al. 2024 (ARR) | Retrieval-level intent |
| Cohen & Levesque 1990 | BDI foundation |
| Rao & Georgeff 1995 | BDI formalisation |
| Bratman 1987 | Intention theory |
| Ouyang et al. 2022 (InstructGPT) | Alignment/intent |
| Shinn et al. 2023 (Reflexion) | Success signals |
| Radha et al. 2024 (Iteration of Thought) | Disambiguation footnote |

---

## Meta

| Dimension | Value |
|-----------|-------|
| Estimated writing time | 2-3 weeks |
| Pages | 9 + references |
| Sections | 6 |
| Tables | ~6 (differentiation matrix, primitives, topology map, case studies, limitations, citations) |
| Figures | 1-2 (IoT-AoT-CoT stack diagram, topology selection flowchart) |
| SPAR source | Deep Ultra, 90% confidence |

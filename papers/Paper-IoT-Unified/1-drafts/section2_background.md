# Section 2: Background and Related Work

This section surveys three research threads that converge on the problem addressed by IoT: reasoning topology design, intent and governance in AI systems, and reasoning failure analysis.

## 2.1 Reasoning Topologies for Large Language Models

Chain-of-thought (CoT) prompting [Wei et al., 2022] demonstrated that instructing language models to "think step by step" substantially improves performance on arithmetic, commonsense, and symbolic reasoning benchmarks. Subsequent work extended this linear structure. Tree-of-thought (ToT) [Yao et al., 2023] introduces branching and backtracking, enabling deliberate exploration of alternative reasoning paths with the ability to prune unpromising branches. Graph-of-thought (GoT) [Besta et al., 2024] generalises further, permitting arbitrary merging and refinement across reasoning nodes, which supports non-linear problem structures where partial solutions interact. Algorithm-of-thought (AoT) [Hong et al., 2024] leverages algorithmic patterns (e.g., depth-first search, dynamic programming) to impose structured exploration within a single generation pass.

Recent advances have shifted from static topology definition to dynamic routing and meta-reasoning. Framework of Thoughts (FoT) [Fricke et al., 2026] provides a foundational framework for dynamically switching between CoT, ToT, and GoT based on task complexity. Intention Chain-of-Thought (ICoT) [Li et al., 2026] introduces dynamic routing specifically for code generation, guided by intention states. Similarly, Meta-Reasoner [Sui et al., 2026] offers dynamic guidance for optimized inference-time reasoning by intervening during the generation process. In multi-agent contexts, AMAS [Leong et al., 2025] adaptively determines communication topologies between agents rather than relying on fixed structures, while STELAR-VISION [Li et al., 2026] applies self-topology-aware learning to efficient vision-language tasks.

Each topology imposes structural commitments. CoT constrains reasoning to a single sequential path. ToT introduces parallelism but requires an evaluation function to select among branches. GoT permits cycles and merges but requires careful state management. The choice of topology is therefore not stylistic; it determines the reasoning architecture's capabilities and failure modes.

Despite these advances in dynamic routing and meta-reasoning, the topology governance problem remains largely open at the architectural level. While frameworks like FoT and Meta-Reasoner optimise topology dynamically during execution, they operate as inference-time optimisers rather than pre-reasoning governance layers. No established mechanism provides a strict, auditable bridge between *why* an agent is reasoning (its formal intent specification) and *how* it structures that reasoning, complete with a lifecycle for detecting and diagnosing structural drift. This is the gap IoT addresses.

## 2.2 Intent and Governance in AI Systems

The notion that AI systems should be governed by explicit intent has precedents across several domains, none of which address reasoning topology governance directly.

**Prompt engineering and instruction tuning** [Brown et al., 2020] provide mechanisms for specifying *what* a model should produce, but do not govern *how* it should reason internally. Similarly, **structured output formats** (e.g., JSON mode) only constrain the final form, not the generative process. 

Broader frameworks like **user intent modelling** in search [Broder, 2002] and **AI safety tiers** (e.g., Anthropic's ASL) operate either too broadly at the dialogue/system level or ignore task-specific reasoning governance entirely. A model at ASL-2 uses the same reasoning topology whether the task is routine or safety-critical.

IoT draws its primary inspiration from **BDI (Belief-Desire-Intention) architectures** [Bratman, 1987; Cohen and Levesque, 1990], which formalise agent commitment. IoT adapts this tradition for LLMs: reasoning persists until the Success Signal is satisfied, the Purpose is judged unachievable, or Anti-Purpose is violated.

The common gap across these precedents is that none ask: "Given this purpose, which reasoning topology should govern the process, and what should we do when it fails?"

## 2.3 Reasoning Failure Analysis

When LLM reasoning fails, existing approaches diagnose failure at different levels of abstraction, none of which address topology-level diagnosis.

When LLMs fail, existing approaches diagnose the failure at the trace level rather than the topology level. **Chain-of-thought error analysis** [Ling et al., 2023] and **process reward models** [Lightman et al., 2023] evaluate the correctness of individual reasoning steps. However, step-correctness does not guarantee topology-correctness: every step may be locally valid while the overall structure is fundamentally misaligned with the intended task.

Self-corrective frameworks like **Reflexion** [Shinn et al., 2023] improve outputs iteratively but reflect inherently on the *result*, not the *topology selection*. An agent using Reflexion may retry endlessly with the wrong structural approach, producing refinements constrained by a flawed architectural commitment. 

None of these approaches ask: "Was the right reasoning topology selected for this purpose?" This is the exact question Retrospective Judgement (Section 4.3) is designed to answer.

## 2.4 Positioning: The Differentiation Table

Table 1 positions IoT relative to existing approaches across four dimensions.

| Dimension | Prompt Engineering | IoT Capture | Failure Analysis | IoT Judgement |
|-----------|-------------------|-------------|------------------|---------------|
| **Input** | Task instructions | Governance triple $(P, \bar{P}, S)$ | Reasoning trace | Trace + original IoT spec |
| **Governs** | Task execution | Topology selection | Step correctness | Topology + intent correctness |
| **Output** | Task result | Selected topology $T^*$ | Error location | Diagnosis + corrective action |
| **Feedback** | None (open loop) | Fidelity gradient $\varphi$ | Debug information | Learning loop ($\to$ better capture) |
| **Operates at** | Instruction level | Governance level | Trace level | Lifecycle level |

*Table 1: Positioning of IoT relative to existing approaches. IoT operates at the governance level (connecting intent to topology) and the lifecycle level (connecting failure to learning). Existing approaches operate at the instruction or trace level.*

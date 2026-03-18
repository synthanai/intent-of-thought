# Section 2: Background and Related Work

This section surveys three research threads that converge on the problem addressed by IoT: reasoning topology design, intent and governance in AI systems, and reasoning failure analysis.

## 2.1 Reasoning Topologies for Large Language Models

Chain-of-thought (CoT) prompting [Wei et al., 2022] demonstrated that instructing language models to "think step by step" substantially improves performance on arithmetic, commonsense, and symbolic reasoning benchmarks. Subsequent work extended this linear structure. Tree-of-thought (ToT) [Yao et al., 2024] introduces branching and backtracking, enabling deliberate exploration of alternative reasoning paths with the ability to prune unpromising branches. Graph-of-thought (GoT) [Besta et al., 2024] generalises further, permitting arbitrary merging and refinement across reasoning nodes, which supports non-linear problem structures where partial solutions interact. Algorithm-of-thought (AoT) [Sel et al., 2023] leverages algorithmic patterns (e.g., depth-first search, dynamic programming) to impose structured exploration within a single generation pass.

Each topology imposes structural commitments. CoT constrains reasoning to a single sequential path. ToT introduces parallelism but requires an evaluation function to select among branches. GoT permits cycles and merges but requires careful state management. The choice of topology is therefore not stylistic; it determines the reasoning architecture's capabilities and failure modes.

Despite this recognition, the topology selection problem remains largely unaddressed. Existing frameworks present topologies as standalone techniques, each evaluated on benchmarks suited to its structure. No established mechanism connects *why* an agent is reasoning (its purpose) to *how* it should structure that reasoning (its topology). This is the gap IoT addresses.

## 2.2 Intent and Governance in AI Systems

The notion that AI systems should be governed by explicit intent has precedents across several domains, none of which address reasoning topology governance directly.

**Prompt engineering and instruction tuning** [Brown et al., 2020; Ouyang et al., 2022] provide mechanisms for specifying *what* a model should produce, but do not govern *how* it should reason internally. A prompt produces a task output $O$ consumed by the user. An IoT Capture, by contrast, produces a governance triple $(P, \bar{P}, S)$ consumed by a topology selection function $f$. Different type signatures entail different architectural roles.

**Structured output formats** (JSON mode, function calling) constrain the *form* of model output but not the *governance* of the reasoning process that produces it.

**User intent modelling in information retrieval** [Broder, 2002; Radlinski and Craswell, 2017] classifies information needs (navigational, informational, transactional) but does not connect these classifications to reasoning topology selection.

**Conversational intent detection** in natural language understanding classifies user actions (booking, searching, asking) but operates at the dialogue level, not the reasoning level.

**AI safety frameworks** (Anthropic's ASL tiers, OpenAI safety levels) provide model-level governance proportional to capability, but do not address task-level reasoning governance. A model at ASL-2 uses the same reasoning topology whether the task is routine or safety-critical.

**BDI (Belief-Desire-Intention) architectures** [Bratman, 1987; Cohen and Levesque, 1990] formalise agent commitment in terms of intentions that persist until achieved, believed unachievable, or superseded. IoT draws on this tradition for its commitment termination semantics: reasoning persists until the Success Signal is satisfied, the Purpose is judged unachievable, or Anti-Purpose is violated.

The common gap across all these precedents is that none of them ask: "Given this reasoning task's purpose, which reasoning topology should govern the process, and what should we do when it fails?"

## 2.3 Reasoning Failure Analysis

When LLM reasoning fails, existing approaches diagnose failure at different levels of abstraction, none of which address topology-level diagnosis.

**Chain-of-thought error analysis** [Ling et al., 2023; Golovneva et al., 2023] catalogues errors at the trace level: arithmetic mistakes, logical gaps, hallucinated facts. These are step-level failures within a fixed topology.

**Process reward models** [Lightman et al., 2023] evaluate the correctness of individual reasoning steps, enabling fine-grained feedback. But step-correctness does not address topology-correctness: every step may be locally valid while the overall reasoning structure is misaligned with the task.

**Reflexion** [Shinn et al., 2023] introduces self-evaluation where an agent reflects on its output and attempts to improve on subsequent trials. The reflection is on the *output*, not on the *topology selection*. An agent using Reflexion may retry with the same (wrong) topology, producing refinements that are structurally constrained by the same architectural commitment.

**Interpretability and attribution methods** [Doshi-Velez and Kim, 2017] explain *what* a model computed, not *why* it chose a particular reasoning strategy.

None of these approaches ask: "Was the right reasoning topology selected for this purpose?" This is the question Retrospective Judgement (Section 4.3) is designed to answer.

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

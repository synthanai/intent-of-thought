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

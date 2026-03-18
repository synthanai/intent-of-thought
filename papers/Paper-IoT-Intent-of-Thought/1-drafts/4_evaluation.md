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

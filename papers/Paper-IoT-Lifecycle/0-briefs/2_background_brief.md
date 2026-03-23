---
thesis: "Intent in AI reasoning has been addressed at step, domain, retrieval, agent-action, and training levels. Failure diagnosis has focused on trace-level debugging and self-evaluation. Governance-proportional response exists in aviation and medicine but has never been applied to reasoning systems. The IoT Lifecycle addresses the intersection of all three gaps."
data_points:
  - point: "Broder (2002) classified web search intent as informational/navigational/transactional"
    source: "research.md A3"
  - point: "MAPE-K (Kephart & Chess 2003) formalises Monitor-Analyse-Plan-Execute-Knowledge for self-adaptive systems"
    source: "research.md A1"
  - point: "PARC (2024) adds premise-augmented reasoning chains for error identification in mathematical reasoning"
    source: "research.md C1"
  - point: "RFF 'Reason from Future' (2024) uses bidirectional reasoning to reduce error accumulation"
    source: "research.md C3"
  - point: "FAA AI Safety Roadmap (2023) advocates risk-based safety assurance and incremental deployment"
    source: "research.md A4"
  - point: "Prompt engineering evolving to 'context engineering' (2025), still instruction-level not governance-level"
    source: "research.md B1, signals.md O5"
  - point: "Kalman filter prediction/estimation duality provides temporal symmetry analogy"
    source: "research.md A2"
gap: "No existing work connects intent elicitation + reasoning failure diagnosis + governance-proportional correction. Each piece has prior art; the lifecycle integration does not."
---

# Section 2: Background and Related Work: Research Brief

## 2.1 Intent Elicitation in AI Systems (~0.5 page)

**Prompt engineering and instruction tuning**:
- Brown et al. (2020, GPT-3): in-context learning via prompts
- Ouyang et al. (2022, InstructGPT): instruction-following via RLHF
- Context engineering (2025 trend): optimising entire context window
- LLM4nl2post (arXiv 2310.01831): NL → formal postconditions (intent as spec source, not prompt)
- STROT (arXiv 2505.01636): analytical intent → structured prompt → analysis plan before execution
- **Key gap**: All capture INSTRUCTIONS (what to do), not GOVERNANCE INPUTS (what reasoning is FOR)

**Pre-reasoning intent capture** (NEW from external research):
- Ask-before-Plan (Zhang et al., EMNLP 2024): 0.1% plan satisfaction without pre-reasoning clarification
- CLIPS (Zhi-Xuan et al., AAMAS 2024): Bayesian goal inference distinguishes instructions from purpose
- Intent Mismatch (Liu et al., 2026): theoretical proof scaling can't fix intent gap, requires architecture
- Active Task Disambiguation (Kobalczyk et al., ICLR 2025): BED for info-gain maximisation before task
- Zhang et al. (ICLR 2025): RLHF trains LLMs to AVOID clarifying questions
- **Key gap**: All capture TASK PURPOSE. None formalise output as TOPOLOGY GOVERNANCE input.

**Critical differentiation** (SPAR #33, kill vector defence):
- CLIPS (Zhi-Xuan et al.) performs Bayesian goal inference from behaviour and language to minimise goal achievement cost. Output: goal estimate consumed by a planner.
- Ask-before-Plan (Zhang et al.) performs pre-reasoning clarification to improve plan satisfaction. Output: refined task instructions consumed by a plan generator.
- IoT Capture performs governance elicitation to produce a topology selection input. Output: (P, P̄, S) triple consumed by the selection function f.
- **Different type signatures, different downstream consumers.** This is not a competing approach but an orthogonal architectural role.

**Intent classification in Information Retrieval**:
- Broder (2002): informational/navigational/transactional taxonomy
- Radlinski & Craswell (2017): conversational search intent
- **Key gap**: Classify USER SEARCH NEEDS, not REASONING TOPOLOGY NEEDS

**Conversational intent detection (NLU)**:
- Classify user actions (book, search, ask)
- **Key gap**: Classify TASK TYPE, not REASONING PURPOSE

## 2.2 Reasoning Failure Analysis (~0.5 page)

**Trace-level debugging**:
- Golovneva et al. (2023): CoT error patterns (mathematical reasoning)
- PARC (2024): premise-augmented reasoning chains, tracing error accumulation
- **Key gap**: Diagnose WHERE a step went wrong, not WHY the topology was wrong

**Self-evaluation and reflection**:
- Shinn et al. (2023, Reflexion): self-evaluation with success/failure signals
- Process reward models (Lightman et al. 2023): step-level correctness verification
- **Key gap**: Self-evaluation within a fixed topology, no topology diagnosis

**Bidirectional reasoning**:
- RFF (2024): "Reason from Future" uses backward reasoning to reduce error accumulation
- **Connection**: RFF reasons forward AND backward at STEP level. IoT Lifecycle captures forward AND judges backward at TOPOLOGY level. Similar temporal pattern, different abstraction layer.

**Interpretability and attribution**:
- Doshi-Velez & Kim (2017): model-level explanation
- **Key gap**: Explain model internals, not intent-topology alignment

## 2.3 Governance and Proportional Response (~0.5 page)

**Tier 1: Model-level governance** (proportional to capabilities, NOT reasoning):
- Anthropic ASL (Responsible Scaling Policy, 2023): defines capability thresholds (autonomy in R&D, cyber, bio, persuasion) that trigger ASL-1 → ASL-2 → ASL-3+. Higher levels require hardened security, evals, red-teaming, monitoring. Some measures (interpretability, eval of dangerous capabilities) touch how models reason, but ASL does not define graded control over the *depth, style, or topology* of reasoning itself.
- OpenAI Preparedness Framework: similar capability-focused tiering.
- **Key gap**: Model-level risk assessment, not per-task reasoning governance.

**Tier 2: Organisational governance** (proportional to operational risk, NOT reasoning):
- ICAO SMS/RBDM: severity x probability risk matrix with acceptable/tolerable/unacceptable regions. Mitigations, monitoring, and escalation scale with risk category. When applied to AI avionics, adjusts certification level and redundancy, not reasoning depth.
- CDS Governance in Healthcare (PMC6371304): classifies CDS artifacts by clinical risk (interruptive vs passive, dosing vs informational). Higher-risk CDS gets stronger validation, change control, monitoring, incident review. Focus on content and workflow impact, not AI internal reasoning.
- Levels of Autonomous Radiology (PMC9773033): levels from decision support to full automation, with human intervention scaling inversely with automation confidence. Governs who is in the loop, not how reasoning proceeds.
- **Key gap**: All govern *organisational processes* and *external controls*, not the structure or intensity of AI reasoning.

**Tier 3: Reasoning-adjacent governance** (closest to per-task reasoning modulation):
- Scalable Oversight (Irving et al. 2018, Christiano et al. 2020): graduated supervision where harder/riskier tasks get multi-agent debate, recursive decomposition, or AI-assisted oversight. Explicitly modulates *how* models reason (debate structure, critique loops). However, framed as research paradigms, not operational governance tiers with clear triggers and levels.
- TAO, Tiered Agentic Oversight (arXiv 2506.12482, 2025): first practical architecture changing agentic reasoning routing based on risk. Dynamically routes healthcare tasks among agent tiers and human physicians based on complexity and safety. Changes reasoning topology per-task. But domain-specific (healthcare) and architectural, not a general governance standard.
- **Key gap**: These touch reasoning in a proportional way, but are not codified as broadly adopted, domain-agnostic governance standards. They function as *design patterns*, not as a mature analogue of ASL or ICAO SMS applied to reasoning.

**The structural gap**: No existing framework achieves all four properties: (1) targets reasoning process, (2) proportional to risk, (3) operationally mature, (4) domain-agnostic. The IoT Lifecycle addresses this by embedding governance-proportional response directly into the Retrospective Judgement phase, scaling correction intensity with intent criticality rather than model capability or deployment context.

**Self-adaptive systems**:
- MAPE-K (Kephart & Chess 2003): Monitor-Analyse-Plan-Execute-Knowledge feedback loop
- **Differentiation**: MAPE-K adapts SYSTEM CONFIGURATION. IoT Learning Loop adapts REASONING GOVERNANCE. Same structural pattern, different domain of adaptation.

**Structural analogy from control theory** (SPAR #32 Enhancement 3, ChatGPT Report 2 refinement):
- Kalman (1960): prediction/estimation duality in state estimation
- "The relationship between forward intent specification (Capture) and backward intent reconstruction (Judgement) mirrors the prediction-estimation duality in control theory, where forward state prediction and backward state smoothing are structurally symmetric operations."
- Position as structural analogy, not mathematical equivalence.
- **Regime-limit caveat** (C9): Todorov shows Kalman duality is "an artifact of the LQG setting." MUST name this limit explicitly.

**Second formal anchor: Predicate Transformers** (ChatGPT Report 2, O18):
- Hoare triples {P}S{Q}: forward = strongest postcondition, backward = weakest precondition
- Dijkstra's predicate-transformer semantics makes the backward operator explicit
- **Arguably CLOSER to IoT than Kalman**: explicitly about SPECIFICATIONS, not physical state
- Capture = strongest postcondition (what spec does this task produce?)
- Judgement = weakest precondition (what spec was needed to avoid this failure?)
- Cite Hoare (1969) and Dijkstra (1976) as second formal tradition

## 2.4 The Differentiation Table (~0.5 page)

**TABLE** (extends Paper 1's Table 1 with lifecycle dimensions):

| Aspect | Prompt Engineering | IoT Capture | Failure Analysis | IoT Judgement |
|--------|-------------------|-------------|------------------|---------------|
| **Input** | Instructions | Governance triple (P, P̄, S) | Reasoning trace | Trace + original IoT spec |
| **Governs** | Task execution | Topology selection | Step correctness | Topology + intent correctness |
| **Output** | Task result | Selected topology | Error location | Reconstructed intent + diagnosis |
| **Feedback** | None | Fidelity gradient | Debug info | Learning loop (→ better capture) |
| **Temporal** | Forward only | Forward (prospective) | Post-hoc | Backward (retrospective) |

## Writing Notes

- **Target**: 2 pages
- **New citations to add**: MAPE-K (Kephart & Chess 2003), Kalman (1960), Broder (2002), PARC (2024), RFF (2024), FAA AI Roadmap (2023), Anthropic RSP (2023), ICAO SMS, PMC6371304 (CDS Governance), PMC9773033 (Autonomous Radiology), TAO (arXiv 2506.12482, 2025), Irving et al. (2018, AI Safety via Debate), Christiano et al. (2020, Scalable Oversight)
- **Carried from Paper 1**: Brown 2020, Ouyang 2022, Golovneva 2023, Lightman 2023, Shinn 2023, Doshi-Velez & Kim 2017
- **Stealth check**: No proprietary terminology. Use "we" and "the authors."
- **RLPG source**: `2-research/concepts/reasoning-level-proportional-governance/research.md`


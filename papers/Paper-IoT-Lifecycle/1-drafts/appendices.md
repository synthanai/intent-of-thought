# Appendices

## Appendix A: Formal Duality Derivation

### A.1 State Estimation Anchor

Consider a latent intent variable $I_t$ at time $t$, observed through a reasoning trace $Y_{1:T}$ and a failure signal $F$. Under a chain-structured generative model with Gaussian noise, the forward filtering distribution (Capture) computes:

$$p(I_t \mid Y_{1:t}) \propto p(Y_t \mid I_t) \int p(I_t \mid I_{t-1}) p(I_{t-1} \mid Y_{1:t-1}) \, dI_{t-1}$$

This forward pass produces causal marginals: estimates of intent conditioned only on evidence available at the time of specification. It corresponds to IoT Capture, where the system infers intent from the information available before reasoning begins.

The backward smoothing pass (Judgement) incorporates future evidence:

$$p(I_t \mid Y_{1:T}, F) \propto p(I_t \mid Y_{1:t}) \int \frac{p(I_{t+1} \mid I_t)}{p(I_{t+1} \mid Y_{1:t})} p(I_{t+1} \mid Y_{1:T}, F) \, dI_{t+1}$$

This produces smoothed posteriors: estimates of intent conditioned on the full evidence set, including the reasoning outcome and failure signal. It corresponds to Retrospective Judgement.

**Regime limitation.** This clean duality is "an artifact of the LQG setting" [Todorov, 2009]. In nonlinear regimes, the forward and backward messages do not combine via simple multiplication. We do not claim mathematical equivalence; we claim structural analogy: Capture and Judgement perform the same inferential operation (intent estimation) under different evidence sets, with the same relationship that prediction and smoothing have in state estimation.

### A.2 Predicate-Transformer Anchor

Dijkstra's [1976] predicate-transformer semantics provides a second, arguably closer formal anchor. For a program $S$ (here, a reasoning topology):

- **Strongest postcondition** $\text{sp}(P, S)$: "Given precondition $P$, what is the strongest statement about states reachable after executing $S$?" This is Capture → Select → Execute: given an intent specification $P$, what outcomes are achievable?

- **Weakest precondition** $\text{wp}(S, Q)$: "Given that we want postcondition $Q$, what is the weakest precondition that guarantees $Q$ after $S$?" This is Judgement: given that we wanted outcome $Q$ but got failure, what was the weakest (most general) intent specification that would have avoided the failure?

The predicate-transformer tradition is explicitly about *specifications*, not physical state. It maps directly to the IoT Lifecycle:

| Predicate Transformer | IoT Lifecycle | Direction |
|----------------------|---------------|-----------|
| Precondition $P$ | Intent specification $(P, \bar{P}, S)$ | Input |
| Program $S$ | Reasoning topology $T$ | Process |
| Postcondition $Q$ | Reasoning outcome $O$ | Output |
| $\text{sp}(P, S) = Q$ | Capture → Select → Execute | Forward |
| $\text{wp}(S, Q) = P$ | Judgement: "What intent was needed?" | Backward |

## Appendix B: Extended Related Work

### B.1 CLIPS Meta-Controller Pattern

CLIPS [Zhi-Xuan et al., AAMAS 2024] performs Bayesian goal inference from observations, distinct from intent *elicitation* (which is interactive). CLIPS' contribution is the formal demonstration that instructions and goals are informationally distinct: a user's instruction ("solve this problem") underdetermines the goal (sequential derivation? parallel exploration? interconnected analysis?). The IoT Capture Spectrum builds on this insight: L0 receives only instructions (CLIPS' problem), L1-L3 progressively elicit the goal/governance triple that CLIPS infers.

### B.2 Kambhampati's Five-Type Failure Taxonomy

Kambhampati et al. [2024] identify five categories of reasoning failure in LLMs: factual errors, logical errors, planning errors, metacognitive errors, and hallucinations. This taxonomy operates within a fixed reasoning topology. IoT Judgement adds a sixth category: *topological errors* (the right topology was not selected for the task). This is orthogonal to the Kambhampati taxonomy: a system can produce factually correct, logically valid reasoning that nonetheless fails because the topology was wrong for the purpose (e.g., CoT producing a valid linear analysis when GoT was needed for interconnected factors).

### B.3 BDI Commitment Semantics

The BDI (Belief-Desire-Intention) architecture [Bratman, 1987; Rao and Georgeff, 1995; Cohen and Levesque, 1990] governs agent *actions* through commitment to intentions. IoT governs *reasoning topology* through commitment to purpose. The structural parallel: BDI's commitment termination conditions (purpose achieved, purpose unachievable, background conditions changed) map directly to IoT's drift detection outputs (success signal satisfied, purpose unreachable, context shift). The key difference: BDI operates at the action level (what the agent does); IoT operates at the reasoning level (how the agent thinks).

### B.4 Framework of Thoughts (FoT) and STELAR

FoT [Ding et al., 2024] provides a meta-architecture for composing reasoning structures dynamically. STELAR-VISION [2025] trains models to select reasoning topologies for vision-language tasks. Both address topology selection but neither formalises *intent* as the selection criterion. FoT composes topologies based on task structure; STELAR learns selection from training data. IoT provides the governance layer that both lack: *why* this topology for *this* purpose, with *these* constraints.

## Appendix C: Domain Implementation Notes

### C.1 Financial Risk Analysis

The IoT Lifecycle maps to financial risk assessment as follows. Capture (L2-L3): elicit the risk analysis purpose. Common purposes include portfolio stress testing ($P$ = "identify correlated failure scenarios"), regulatory compliance ($P$ = "demonstrate capital adequacy under Basel III"), and client advisory ($P$ = "personalise risk tolerance to client profile"). Anti-Purpose is critical: $\bar{P}$ = "must not treat asset classes as independent when they are correlated" (analogous to the clinical triage case). Governance-proportional response maps to financial materiality: Level 1 for informational queries, Level 5 for irreversible trade execution.

### C.2 Cybersecurity Incident Response

The lifecycle naturally maps to NIST's Incident Response phases (Preparation, Detection, Analysis, Containment, Recovery, Lessons Learned). Capture aligns with Detection + Analysis (determine the type and scope of threat). Selection maps to Containment strategy (sequential isolation = CoT, parallel investigation = ToT, threat graph analysis = GoT). Governance levels map directly to NIST severity classifications. The Learning Loop feeds into Lessons Learned.

### C.3 Judicial AI

Judicial reasoning provides the strongest structural parallel to the IoT Lifecycle. A court's purpose ($P$) is explicit in the case filing. Anti-Purpose ($\bar{P}$) corresponds to legal constraints (constitutional rights, procedural rules). Success Signal ($S$) is the judgment standard (preponderance of evidence, beyond reasonable doubt). Retrospective Judgement maps to appellate review: "Given the outcome, was the correct legal reasoning topology applied?" False Capture = incorrect framing of the legal question. False Selection = wrong standard of review. False Execution = correct framing and standard, but reasoning drifted from the evidentiary record.

## Appendix D: RLPG Framework Comparison

We expand Table 1b (Section 2.3) with detailed analysis of each framework across the four properties.

### D.1 Anthropic's ASL (AI Safety Levels)

ASL defines four tiers based on model capabilities (ASL-1 through ASL-4). Each tier prescribes deployment restrictions, evaluation requirements, and containment measures. ASL governs *what models can do*, not *how they reason per-task*. It is proportional to capability risk, not to intent criticality. ASL cannot distinguish between a model reasoning about a low-stakes creative task and a high-stakes medical decision; the same ASL tier applies to both.

### D.2 ICAO Safety Management System

ICAO's SMM (Doc 9859) uses a severity-probability matrix to scale organisational response to aviation incidents. It is the gold standard for governance-proportional response in safety-critical domains. However, it governs *organisations*, not *reasoning processes*. An ICAO incident investigation examines human factors, equipment failure, and procedural deficiencies; it does not examine the reasoning topology that produced a decision.

### D.3 Structured Decision Governance

Structured decision governance frameworks [Mintzberg et al., 1976; Nutt, 1984] define multi-step protocols for auditable decisions. They govern *decision moments*: defined points where a commitment is made. Such frameworks do not govern the reasoning process that precedes the decision, nor do they scale response proportionally to reasoning risk. Every decision receives the same protocol regardless of complexity or consequence.

### D.4 Synthesis: The RLPG Niche

The four properties (reasoning-targeted, risk-proportional, operational, domain-agnostic) define a governance niche that is occupied when the governance object is *reasoning itself* and the response scales with the *criticality of the reasoning purpose*. This niche is distinct from capability governance (ASL), organisational governance (ICAO), structured decision governance [Mintzberg et al., 1976], and agent governance (TAO). The IoT Lifecycle occupies it.

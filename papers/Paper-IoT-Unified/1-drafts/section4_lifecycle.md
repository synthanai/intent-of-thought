# Section 4: The IoT Lifecycle

The framework presented in Section 3 operates under three simplifying assumptions: (i) the intent triple is *given* by a competent specifier, (ii) the triple *correctly* captures the actual reasoning need, and (iii) governance operates *forward only*, from specification through selection to monitoring. This section relaxes all three assumptions by introducing the operational lifecycle that completes the IoT governance layer.

## 4.1 The Capture Spectrum

Intent elicitation for reasoning governance can be formalised as a five-mode hierarchy that produces IoT triples of varying fidelity. We term this the *Capture Spectrum* and frame it as an intent elicitation maturity hierarchy.

**Table 3: The Capture Spectrum.**

| Mode | Level | Mechanism | IoT Triple Fidelity | Example |
|------|:-----:|-----------|:-------------------:|---------|
| Zero | L0 | System infers intent from task context alone | Low: $P$ inferred, $\bar{P}$ absent, $S$ generic | "Solve this problem" $\to$ system defaults to CoT |
| Implicit | L1 | Lightweight extraction from user phrasing and domain | Medium-low: $P$ extracted, $\bar{P}$ partial | "Compare these options carefully" $\to$ implicit ToT signal |
| Prompted | L2 | Structured questions elicit $P$, $\bar{P}$, $S$ explicitly | Medium-high: full triple, user-specified | System asks: "What must this analysis avoid?" |
| Collaborative | L3 | Interactive refinement loop: draft $\to$ feedback $\to$ revise | High: validated triple via dialogue | Multi-turn IoT specification with user correction |
| Learned | L4 | Model has internalised intent-topology mappings from training | Variable: training-dependent | Model auto-generates IoT triple from task embedding |

The hierarchy is not purely ordinal: "higher is always better" does not hold. L0 is appropriate for low-stakes, familiar tasks; L3 introduces interaction cost that may be unwarranted for routine queries. The spectrum describes *available capability*, not prescribed usage. A mature system selects its capture mode based on task criticality, user context, and confidence.

**Formal notation.** Let $\text{IoT}_{\text{capture}}: \text{mode} \times \text{context} \to \text{IoT}_{\text{fidelity}}$ denote the capture function. The fidelity function $\varphi(\text{IoT}_{\text{capture}}) \to [0,1]$ measures confidence in the captured triple. The extended selection function becomes:

$$f(\text{IoT}, \text{context}, \varphi) \to T^*$$

When $\varphi < \theta_{\text{elevate}}$, the system escalates its capture mode (e.g., from L0 to L2), requesting additional intent specification before committing to topology selection. This creates a feedback loop between capture confidence and capture effort.

**Architectural distinction from prompt engineering.** The strongest objection to the Capture Spectrum is that it constitutes "prompt engineering with extra steps." The decisive rebuttal is that the capture modes imply different *control surfaces*, not merely different textual instructions:

1. **Typed artefacts**: intent is materialised as a structured contract, not free-form text.
2. **Policies**: the system follows explicit rules for when to ask versus when to act, governed by fidelity thresholds.
3. **State machines**: capture proceeds through defined phases (draft, clarify, commit) with auditable transitions.
4. **Telemetry**: field-level missingness, correction rates, and capture mode distributions are measurable.

The type signature argument clarifies the distinction: a prompt produces a task output $O$ consumed by the user; an IoT Capture produces a governance triple $(P, \bar{P}, S)$ consumed by the topology selection function $f$.

## 4.2 Capture-Topology Confidence Interaction

The fidelity gradient creates a correspondence between capture quality and topology specialisation:

- **Low-fidelity capture** (L0--L1): the selection function should prefer robust, general-purpose topologies. Our experimental evidence (Section 5) confirms that chain-of-thought serves as a safe default at these fidelity levels, because CoT is empirically robust across task types.
- **High-fidelity capture** (L3--L4): the selection function can recommend specialised topologies (GoT, hybrid strategies), because the governance triple is precise enough to justify the structural commitment and mitigate the risk of misselection.

This interaction implies that topology selection is not merely a function of task content but of *how well the system understands what it is reasoning about*.

## 4.3 Retrospective Judgement

When reasoning fails despite governance, the system must diagnose *why*. Retrospective Judgement is backward intent reconstruction: given a failed reasoning trace and the original IoT specification, reconstruct what the intent *should have been* and classify the failure mode.

**Definition 3 (Retrospective Judgement Function).** Let 

$$
\mathcal{J}: \text{trace} \times \text{IoT}_{\text{original}} \to (\text{failure\_mode}, \text{IoT}_{\text{reconstructed}}, \text{action})
$$ 

denote the judgement function that diagnoses reasoning failure.

The three failure modes form a diagnostic hierarchy:

**False Capture.** The IoT triple was incorrectly specified. The purpose $P$ does not match the actual reasoning need. Example: a clinical triage task specifies $P$ as "identify the most likely diagnosis" when the actual need is "identify the most dangerous diagnosis that must be ruled out." The topology selection was correct *given* the stated purpose, but the stated purpose was wrong.

**False Selection.** The IoT triple was correct, but the selection function chose the wrong topology. Example: an interconnected analysis task correctly specifies $P$ as "identify interactions between factors," but the system selects CoT instead of GoT, producing a linear analysis that misses cross-factor relationships.

**False Execution.** The IoT triple and topology selection were both correct, but reasoning drifted during execution. The drift detection function $\delta$ either failed to trigger or triggered too late.

**Diagnostic algorithm.** Judgement proceeds by comparing the failed trace against the original IoT specification:

```
Algorithm 3: Retrospective Judgement

Input:  Failed trace τ, original IoT = (P, P̄, S), selected T*
Output: Failure mode, reconstructed IoT, corrective action

Step 1. Reconstruct intent from trace.
  Analyse τ to infer what purpose the reasoning was
  actually pursuing. Call this P_actual.

Step 2. Compare P_actual with P.
  If P_actual ≠ P: diagnose False Capture.
    Action: Escalate capture mode (e.g., L0 → L2).
  If P_actual = P: proceed to Step 3.

Step 3. Evaluate topology-purpose alignment.
  Using Table 2, check whether T* was appropriate for P.
  If T* was mismatched: diagnose False Selection.
    Action: Re-run Algorithm 1 with confirmed P.
  If T* was appropriate: diagnose False Execution.
    Action: Lower drift threshold θ, add checkpoints.

Output: (failure_mode, IoT_reconstructed, corrective_action)
```

## 4.4 The Learning Loop

Capture and Judgement are structurally symmetric under epistemic asymmetry: Capture moves from intent to topology (forward), while Judgement moves from failed topology to reconstructed intent (backward). Both operate on the same IoT triple but from opposite temporal positions.

The Learning Loop connects Judgement outputs to improved Capture:

1. **False Capture corrections** feed back into capture policies, updating the system's thresholds for when to escalate from L0 to L2 or L3.
2. **False Selection corrections** feed back into the selection function, refining the topology-purpose mappings in Table 2 based on observed failures.
3. **False Execution corrections** feed back into drift detection, adjusting the threshold $\theta$ and checkpoint frequency.

This feedback loop closes the lifecycle:

$$\text{Capture} \to \text{Select} \to \text{Monitor} \to \text{Judge} \to \text{Learn} \to \text{Capture}$$

The loop is not merely circular; it is adaptive. Each iteration improves the system's ability to capture intent, select topologies, and detect failures. The convergence condition is when Judgement produces no new corrections, a state we term *governance equilibrium*.

## 4.5 L4 Learned Capture: A Future Direction

L4 is the most architecturally distinctive capture mode and the most speculative. Where L0 through L3 operate at inference time, L4 operates at training time: the model has internalised intent-topology mappings from prior data, enabling auto-generation of IoT triples without explicit elicitation.

Training-time tool integration provides a partial precedent: Toolformer [Schick et al., 2023] trains models to decide *when and how* to invoke external tools. L4 extends this: instead of learning to produce *tool invocations*, the model learns to produce *governance triples*. We do not evaluate L4 empirically in this paper and include it as a theoretical contribution that defines the spectrum's upper bound.

With the theoretical lifecycle established—from explicit L0 capture up to speculative L4 internalisation—the architectural question naturally shifts from *how* to govern topologies to *whether* this governance actually yields measurable improvements. Section 5 transitions from this theoretical foundation into a rigorous empirical barrage, explicitly tracking whether forcing these structural constraints successfully prevents the catastrophic cognitive drift predicted by our failure taxonomy.

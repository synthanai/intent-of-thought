# Section 4: The IoT Lifecycle

The framework presented in Section 3 operates under three simplifying assumptions: (i) the intent triple is *given* by a competent specifier, (ii) the triple *correctly* captures the actual reasoning need, and (iii) governance operates *forward only*, from specification through selection to monitoring. This section relaxes all three assumptions by introducing the operational lifecycle that completes the IoT governance layer.

## 4.1 The Capture Spectrum

Intent elicitation for reasoning governance can be organised as a five-mode hierarchy that produces IoT triples of varying fidelity. We term this the *Capture Spectrum* and frame it as an intent elicitation maturity hierarchy.

**Table 3: The Capture Spectrum.**

| Mode | Level | Mechanism | Triple Fidelity | Example |
|------|:-----:|-----------|:-------------------:|---------|
| Zero | L0 | System infers intent from task context alone | Low: Purpose inferred, Anti-Purpose absent, Success Signal generic | "Solve this problem" leads to system defaulting to CoT |
| Implicit | L1 | Lightweight extraction from user phrasing and domain | Medium-low: Purpose extracted, Anti-Purpose partial | "Compare these options carefully" carries an implicit ToT signal |
| Prompted | L2 | Structured questions elicit Purpose, Anti-Purpose, Success Signal explicitly | Medium-high: full triple, user-specified | System asks: "What must this analysis avoid?" |
| Collaborative | L3 | Interactive refinement loop: draft, feedback, revise | High: validated triple via dialogue | Multi-turn IoT specification with user correction |
| Learned | L4 | Model has internalised intent-topology mappings from training | Variable: training-dependent | Model auto-generates IoT triple from task embedding |

The hierarchy is not purely ordinal: "higher is always better" does not hold. L0 is appropriate for low-stakes, familiar tasks; L3 introduces interaction cost that may be unwarranted for routine queries. The spectrum describes *available capability*, not prescribed usage. A mature system selects its capture mode based on task criticality, user context, and confidence.

**How capture confidence drives topology selection.** The system assigns a confidence score (0 to 1) to each captured triple. When this confidence is low, the system either escalates its capture mode (e.g., from L0 to L2) or defaults to a safe, general-purpose topology. When confidence is high, the system can recommend specialised topologies because the governance triple is precise enough to justify the structural commitment.

**Architectural distinction from prompt engineering.** The strongest objection to the Capture Spectrum is that it constitutes "prompt engineering with extra steps." The decisive rebuttal is that the capture modes imply different *control surfaces*, not merely different textual instructions:

1. **Typed artefacts**: intent is materialised as a structured contract, not free-form text.
2. **Policies**: the system follows explicit rules for when to ask versus when to act, governed by fidelity thresholds.
3. **State machines**: capture proceeds through defined phases (draft, clarify, commit) with auditable transitions.
4. **Telemetry**: field-level missingness, correction rates, and capture mode distributions are measurable.

A prompt produces a task output consumed by the user; an IoT Capture produces a governance triple consumed by the topology selection function. Different type signatures entail different architectural roles.

## 4.2 Capture-Topology Confidence Interaction

The confidence score creates a correspondence between capture quality and topology specialisation:

- **Low-fidelity capture** (L0 to L1): the selection function should prefer robust, general-purpose topologies. Our experimental evidence (Section 5) confirms that chain-of-thought serves as a safe default at these fidelity levels, because CoT is empirically robust across task types.
- **High-fidelity capture** (L3 to L4): the selection function can recommend specialised topologies (GoT, hybrid strategies), because the governance triple is precise enough to justify the structural commitment and mitigate the risk of misselection.

This interaction implies that topology selection is not merely a function of task content but of *how well the system understands what it is reasoning about*.

## 4.3 Retrospective Judgement

When reasoning fails despite governance, the system must diagnose *why*. Retrospective Judgement is backward intent reconstruction: given a failed reasoning trace and the original IoT specification, reconstruct what the intent *should have been* and classify the failure mode.

**How Retrospective Judgement works.** When a reasoning episode fails, the judgement function takes the failed trace and the original IoT triple as inputs, and produces three outputs: the diagnosed failure mode, a reconstructed version of what the triple should have been, and a recommended corrective action.

The three failure modes form a diagnostic hierarchy:

**False Capture.** The IoT triple was incorrectly specified. The Purpose does not match the actual reasoning need. Example: a clinical triage task specifies Purpose as "identify the most likely diagnosis" when the actual need is "identify the most dangerous diagnosis that must be ruled out." The topology selection was correct *given* the stated Purpose, but the stated Purpose was wrong.

**False Selection.** The IoT triple was correct, but the selection function chose the wrong topology. Example: an interconnected analysis task correctly specifies Purpose as "identify interactions between factors," but the system selects CoT instead of GoT, producing a linear analysis that misses cross-factor relationships.

**False Execution.** The IoT triple and topology selection were both correct, but reasoning drifted during execution. The drift detection either failed to trigger or triggered too late.

**Diagnostic algorithm.** Judgement proceeds by comparing the failed trace against the original IoT specification:

```
Algorithm 3: Retrospective Judgement

Input:  Failed trace, original IoT = (Purpose, Anti-Purpose, Success Signal), selected topology
Output: Failure mode, reconstructed IoT, corrective action

Step 1. Reconstruct intent from trace.
  Analyse the trace to infer what purpose the reasoning was
  actually pursuing. Call this the "actual purpose."

Step 2. Compare actual purpose with stated Purpose.
  If they differ: diagnose False Capture.
    Action: Escalate capture mode (e.g., L0 to L2).
  If they match: proceed to Step 3.

Step 3. Evaluate topology-purpose alignment.
  Using Table 2, check whether the selected topology was appropriate for Purpose.
  If mismatched: diagnose False Selection.
    Action: Re-run Algorithm 1 with confirmed Purpose.
  If appropriate: diagnose False Execution.
    Action: Lower drift threshold, add checkpoints.

Output: (failure_mode, reconstructed_IoT, corrective_action)
```

## 4.4 The Learning Loop

Capture and Judgement are structurally symmetric: Capture moves from intent to topology (forward), while Judgement moves from failed topology to reconstructed intent (backward). Both operate on the same IoT triple but from opposite temporal positions.

The Learning Loop connects Judgement outputs to improved Capture:

1. **False Capture corrections** feed back into capture policies, updating the system's thresholds for when to escalate from L0 to L2 or L3.
2. **False Selection corrections** feed back into the selection function, refining the topology-purpose mappings in Table 2 based on observed failures.
3. **False Execution corrections** feed back into drift detection, adjusting the threshold and checkpoint frequency.

This feedback loop closes the lifecycle:

> **Capture > Select > Monitor > Judge > Learn > Capture**

The loop is not merely circular; it is adaptive. Each iteration improves the system's ability to capture intent, select topologies, and detect failures. The convergence condition is when Judgement produces no new corrections, a state we term *governance equilibrium*.

## 4.5 L4 Learned Capture: A Future Direction

L4 is the most architecturally distinctive capture mode and the most speculative. Where L0 through L3 operate at inference time, L4 operates at training time: the model has internalised intent-topology mappings from prior data, enabling auto-generation of IoT triples without explicit elicitation.

Training-time tool integration provides a partial precedent: Toolformer [Schick et al., 2023] trains models to decide *when and how* to invoke external tools. L4 extends this: instead of learning to produce *tool invocations*, the model learns to produce *governance triples*. We do not evaluate L4 empirically in this paper and include it as a theoretical contribution that defines the spectrum's upper bound.

With the theoretical lifecycle established, from explicit L0 capture up to speculative L4 internalisation, the architectural question naturally shifts from *how* to govern topologies to *whether* this governance actually yields measurable improvements. Section 5 transitions from this theoretical foundation into the empirical evidence, explicitly tracking whether forcing these structural constraints successfully prevents the catastrophic cognitive drift predicted by our failure taxonomy.

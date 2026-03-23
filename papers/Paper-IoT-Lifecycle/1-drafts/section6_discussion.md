# Section 6: Discussion

## 6.1 Limitations

We acknowledge several limitations of the present work.

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance of lifecycle benefits | Case studies demonstrate lifecycle utility; empirical validation is future work |
| Capture fidelity measurement | The fidelity function $\varphi$ requires empirical calibration | Proposed formally; calibration requires the topology selection benchmark (future Paper 3) |
| Reconstruction accuracy | $P_{\text{reconstructed}}$ may not match $P_{\text{actual}}$ | Acknowledged as upper-bound estimation, not ground truth. Non-identifiability is inherent (Section 4.1) |
| Non-identifiability | Many intents can explain the same failed trajectory | Judgement includes selection principles (minimal change, safety priors, explanatory adequacy) |
| Governance levels are illustrative | Five levels may not fit all domains | Framework allows domain-specific calibration of levels and thresholds |
| Single-model focus | Lifecycle may behave differently across model architectures | Future benchmark will test cross-model generalisation |
| Silent failure | If $S$ is poorly specified (low $\varphi$), system may not detect failure | Learning Loop calibrates $S$ over time; bootstrapping accuracy is a limitation |
| MAPE-K analogy is structural | Must not overclaim formal equivalence | Positioned as structural analogy throughout |
| Kalman regime-limits | State estimation duality does not automatically generalise beyond LQG settings [Todorov, 2009] | Framed as structural analogy; regime-limits named explicitly; predicate-transformer anchor offered as alternative |
| Non-adversarial capture (A12) | The lifecycle assumes intent specification is honest; deceptive capture breaks the governance chain | Scope boundary analogous to ICAO's honest incident reporting assumption |

### Degradation Conditions

The lifecycle is structurally domain-agnostic: the six-phase loop (Capture, Select, Monitor, Judge, Respond, Learn) applies wherever reasoning topology selection matters. However, five conditions degrade its effectiveness without constituting structural breaks:

1. **Latency-critical reasoning**: When reasoning must complete in milliseconds, full capture (L2-L3) is infeasible. Systems must rely on pre-computed capture (L4) or zero-capture (L0) with post-hoc judgement.
2. **Subjective success criteria**: When $S$ is difficult to specify precisely (e.g., creative quality), drift detection reliability decreases and Judgement loses its ground truth.
3. **Adversarial capture**: If intent is deliberately misspecified, the lifecycle operates on false premises. This is a security concern, not a governance concern (A12).
4. **Composable intent**: Tasks with nested sub-intents require recursive lifecycle application, which the present work acknowledges but does not solve (A4).
5. **Multi-stakeholder negotiation**: When no single $P$ exists and intent must be negotiated, the lifecycle requires periodic re-capture as consensus evolves.

### Domain Applicability

Table 4 maps the lifecycle across eleven domains, ranking them by adoption readiness.

| Domain | Capture Mode | Governance Level | Primary Topology | Key Adaptation | Status |
|--------|:------------:|:----------------:|:----------------:|----------------|:------:|
| Clinical Decision Support | L1→L2 | L3-L4 | GoT | Symptom interaction detection | Demonstrated |
| Legal Reasoning | L2 | L2-L3 | GoT/ToT | Precedent relationship mapping | Demonstrated |
| Aviation Safety | L3 | L4-L5 | GoT | Drift threshold calibration | Demonstrated |
| Financial Risk Analysis | L2-L3 | L4-L5 | GoT | Real-time market data integration | Proposed |
| Cybersecurity Incident Response | L1-L2 | L3-L5 | AoT→GoT | Threat classification hierarchy | Proposed |
| Engineering Design | L2-L3 | L2-L3 | ToT/GoT | Constraint satisfaction | Proposed |
| Scientific Research Planning | L2-L3 | L2-L3 | ToT→GoT | Hypothesis interaction | Proposed |
| Regulatory Compliance | L2 | L3-L4 | CoT/GoT | Audit trail requirements | Proposed |
| Judicial AI | L3 | L4-L5 | GoT | Explainability requirements | Proposed |
| Educational Assessment | L1-L2 | L1-L2 | CoT/ToT | Learner model integration | Stretch |
| Creative Applications | L0-L1 | L1 | Any | Subjective $S$ handling | Stretch |

## 6.2 Completing the Research Programme

This paper is the second in a three-paper programme:

- **Paper 1** [Mohamed Kani, 2026]: The IoT framework. Introduced the intent triple, topology selection function, and drift detection. Forward governance: specify, select, monitor.
- **Paper 2** (this paper): The IoT Lifecycle. Introduced intent capture, retrospective judgement, and the learning loop. Backward governance: capture, judge, correct, learn.
- **Paper 3** (future): The Topology Selection Benchmark (TSB). Empirical validation of capture fidelity measurement, judgement accuracy, and cross-model generalisation.

Together, the three papers constitute a complete, testable research programme for intent-governed reasoning.

## 6.3 Broader Implications

The lifecycle pattern, capture $\to$ govern $\to$ execute $\to$ judge $\to$ learn, is domain-general. It mirrors a fundamental pattern in human decision-making: "Why are we discussing this?" before "How should we decide?" before "What went wrong?"

Several directions merit future investigation:

- **Intent compositionality**: nested intents for complex tasks where sub-tasks carry distinct purposes. This addresses the single-task assumption (A4).
- **Multi-agent intent governance**: when multiple agents serve different stakeholders, whose intent governs topology selection? This addresses the single-model assumption (A6).
- **Dynamic context adaptation**: intent that evolves during reasoning as new information arrives. This addresses the static-context assumption (A5).
- **Topology discovery**: automated expansion of the topology space $\mathcal{T}$ beyond the five currently recognised structures. This addresses the known-topology-space assumption (A7).
- **Continuous topology representation**: moving from discrete topology categories to a continuous space where topologies can be blended. This addresses the discrete-topologies assumption (A10).
- **Training-time integration**: fine-tuning models to internalise the lifecycle, enabling L4 capture and model-native judgement capabilities.

The governance-proportional correction mechanism occupies a niche that no existing framework fills: it simultaneously targets the reasoning process, responds proportionally to risk, provides operationally defined response levels, and applies domain-agnostically. The lifecycle's value proposition scales with reasoning stakes: high-consequence domains (medical, legal, financial, safety) benefit most; low-consequence domains (creative, exploratory) benefit least but are not excluded. This suggests potential for standardisation analogous to ICAO's incident severity classifications or Anthropic's ASL tiers, but applied to reasoning governance rather than deployment or organisational safety.

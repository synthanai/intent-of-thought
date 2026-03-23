# Section 4: Retrospective Judgement

When reasoning fails, the question is not merely "what went wrong?" but "why was this the wrong approach?" We introduce Retrospective Judgement as the backward half of the IoT Lifecycle, reconstructing what the intent *should have been* after observing a failed outcome, diagnosing the failure mode, and scaling the corrective response proportionally to intent criticality.

## 4.1 The Backward Problem

Given a reasoning trace $T_{\text{result}}$ that did not satisfy the Success Signal $S$, the original IoT specification $(P, \bar{P}, S)$, and the selected topology $T_{\text{selected}}$, Retrospective Judgement determines:

- $P_{\text{reconstructed}}$: what the intent should have been (was $P$ correctly captured?)
- $T_{\text{optimal}}$: which topology would have served $P_{\text{reconstructed}}$ (was $T_{\text{selected}}$ correct for the actual need?)
- $\delta_{\text{source}}$: where drift originated (capture error, topology mismatch, or execution drift)

**Temporal symmetry.** Capture (Section 3) constructs the IoT triple *before* reasoning begins: forward specification from belief. Judgement reconstructs what the triple *should have been* after failure: backward reconstruction from observation. Both operations perform intent inference, but under epistemic asymmetry: Capture conditions on prior belief $p(I \mid C)$; Judgement conditions on the full evidence set $p(I \mid C, Y_{1:T}, F)$, where $Y_{1:T}$ is the reasoning trace and $F$ the failure signal. Under a sequential generative model, Capture produces forward-only estimates (conditioning only on evidence available at specification time), while Judgement produces estimates conditioned on all evidence, including the outcome and failure signal. The relationship mirrors two-pass inference: forward filtering followed by backward correction.

This structural pattern recurs across multiple formal traditions. In state estimation, it corresponds to Kalman prediction versus Rauch-Tung-Striebel smoothing [Kalman, 1960; Rauch et al., 1965]. In program verification, it corresponds to strongest postconditions (forward execution from precondition) versus weakest preconditions (backward computation from postcondition) [Dijkstra, 1976]. In plan recognition, it corresponds to planning (goals to actions) versus inverse planning (actions to goals) [Baker et al., 2009].

We note two important limitations. First, the clean duality holds under a fixed generative model; in practice, Judgement may revise the hypothesis class itself (e.g., discovering that the original intent space was inadequate), which goes beyond smoothing. Second, backward intent reconstruction is an ill-posed inverse problem: many intents can be consistent with the same failed trajectory, a challenge analogous to the non-uniqueness problem in inverse reinforcement learning [Ng and Russell, 2000]. Todorov [2009] warns that the forward-backward duality is "an artifact of the LQG setting" and does not transfer cleanly to nonlinear regimes. Judgement therefore requires explicit selection principles: minimal change from $P_{\text{captured}}$, safety priors, and explanatory adequacy.

## 4.2 Three Failure Modes

We distinguish three failure modes, each requiring different corrective action.

| Mode | Description | Diagnosis | Correction |
|------|-------------|-----------|------------|
| **False Capture** | Intent was incorrectly specified: $P_{\text{captured}} \neq P_{\text{actual}}$ | $P_{\text{reconstructed}} \neq P_{\text{captured}}$ | Elevate capture mode, re-specify intent |
| **False Selection** | Intent correct, wrong topology selected: $T_{\text{selected}} \neq T_{\text{optimal}}$ for $P$ | $f(\text{IoT}, \text{context})$ produced wrong $T^*$ | Update selection function, add training data |
| **False Execution** | Intent and topology correct, reasoning drifted: $\delta > \theta$ | Drift detected in trace despite correct setup | Re-execute with IoT checkpoints at higher frequency |

These modes are mutually exclusive by construction: the reconstruction algorithm (below) tests them in sequence, and the first satisfied condition determines the diagnosis.

The companion paper [Mohamed Kani, 2026] identified three failure modes in general terms: *false discovery* (intent not genuinely examined), *false process* (problem classification without execution), and *false delivery* (reasoning disconnected from purpose). The present taxonomy refines these into actionable diagnostic categories: False Capture subsumes false discovery (intent was not merely unexamined but incorrectly specified), False Selection captures false process as a topology-level mis-mapping, and False Execution corresponds to false delivery (drift from a correctly specified purpose).

## 4.3 Reconstruction Algorithm

We propose a seven-step reconstruction procedure:

1. Extract the final outcome $O$ from $T_{\text{result}}$.
2. Compare $O$ against $S$ (Success Signal): quantify failure magnitude.
3. Compare $O$ against $\bar{P}$ (Anti-Purpose): check for constraint violations.
4. Reconstruct $P_{\text{actual}}$ from $O$ + context (what purpose would have led to this outcome?).
5. Compare $P_{\text{actual}}$ with $P_{\text{captured}}$: if they diverge, diagnose *False Capture*.
6. Simulate $f(P_{\text{actual}}, \text{context}) \to T_{\text{theoretical}}$: compare with $T_{\text{selected}}$. If they diverge, diagnose *False Selection*.
7. If $P_{\text{actual}} \approx P_{\text{captured}}$ and $T_{\text{theoretical}} \approx T_{\text{selected}}$: diagnose *False Execution* (drift).

Step 4 is the most challenging: it requires an inference from outcome and context to intent, which is the ill-posed inverse problem discussed above. In practice, this can be implemented as a prompted reconstruction ("Given this outcome and this context, what was the user most likely trying to achieve?") with the selection principles serving as regularisation.

### 4.3.1 Worked Example: Clinical Triage Reconstruction

We trace the algorithm on Case Study 1 (Section 5.1) to illustrate its operation, particularly the ill-posedness at Step 4.

**Setup.** $P_{\text{captured}}$ = "list possible diagnoses." $\bar{P}$ absent. $S$ = "produce a list." $T_{\text{selected}}$ = CoT. Outcome $O$ = a linear list of independent diagnoses, missing the interacting cluster (Symptom A + Symptom B).

1. **Extract $O$**: Linear list of 5 diagnoses, no interaction analysis.
2. **Compare $O$ against $S$**: $S$ ("produce a list") is technically satisfied. However, the clinician rejected the output. Failure magnitude: qualitative.
3. **Compare $O$ against $\bar{P}$**: $\bar{P}$ was absent, so no constraint violation is detectable. This is itself diagnostic: the capture was too shallow to specify constraints.
4. **Reconstruct $P_{\text{actual}}$**: This is the ill-posed step. Multiple intents are consistent with the rejected outcome:
   - $P_a$ = "identify interacting symptom clusters" (requires GoT)
   - $P_b$ = "rank diagnoses by probability" (requires CoT with different priors)
   - $P_c$ = "identify the most dangerous diagnosis first" (requires risk-weighted CoT)

   The selection principles resolve the ambiguity: *minimal change from $P_{\text{captured}}$* favours $P_a$ (elevating from "list diagnoses" to "identify interactions" is the smallest semantic shift that explains the rejection). *Safety priors* also favour $P_a$ (in medical contexts, missing interactions is more dangerous than misordering risks). *Explanatory adequacy*: $P_a$ explains why CoT failed (linear listing cannot detect non-linear interactions), while $P_b$ and $P_c$ do not explain the topological mismatch.

   Result: $P_{\text{reconstructed}} = P_a$ = "identify interacting symptom clusters."

5. **Compare $P_a$ with $P_{\text{captured}}$**: $P_a \neq P_{\text{captured}}$. Diagnose **False Capture**.
6. **(Skipped)**: False Capture diagnosed; no need to test False Selection.
7. **(Skipped)**: Sequential testing terminates at first match.

## 4.4 Governance-Proportional Response

Not all failures deserve the same response. We define five intent criticality levels, each mapping to a response severity and a set of corrective actions.

| Intent Criticality | Response Level | Actions | Cross-Domain Analogue |
|-------------------|----------------|---------|----------------------|
| Level 1 (Reversible) | Silent retry | Re-execute with adjusted parameters; log for learning | Minor turbulence (autopilot adjusts) |
| Level 2 (Moderate) | User notification | Flag failure, suggest alternative topology | Moderate event (alert crew) |
| Level 3 (Strategic) | Halt and re-specify | Pause reasoning, elevate capture mode, require explicit IoT re-entry | Significant incident (divert) |
| Level 4 (High) | Human escalation | Route to expert review, log full trace for audit | Serious incident (emergency landing) |
| Level 5 (Irreversible) | Abort with safeguards | Stop all reasoning, require verified human approval, create permanent audit record | Engine failure (manual override) |

This governance structure occupies a niche that no existing framework fills. ASL [Anthropic, 2025] governs model capabilities. ICAO governs organisational incidents. Decision governance frameworks govern decision moments. TAO [2025] governs agent routing in healthcare. None simultaneously target the reasoning process, respond proportionally to risk, provide operationally defined levels with triggers and responses, and apply domain-agnostically. The IoT Lifecycle's governance-proportional correction satisfies all four properties.

## 4.5 The Learning Loop

Judgement outputs feed back into the lifecycle:

- **False Capture** $\to$ improve capture questions (refine L2/L3 elicitation strategies)
- **False Selection** $\to$ update selection function $f$ (new training cases for topology mapping)
- **False Execution** $\to$ calibrate drift threshold $\delta$ (sensitivity tuning)
- **All modes** $\to$ expand benchmark dataset (future empirical validation)

The feedback mechanism shares a structural parallel with the MAPE-K loop in autonomic computing [Kephart and Chess, 2003]: monitoring the managed system (reasoning trace), analysing for faults (Judgement), planning corrective action (governance response), and executing the correction. The key difference is scope. MAPE-K adapts system-level configuration parameters; the IoT Learning Loop adapts reasoning-level governance specifications.

The complete lifecycle is: Capture $\to$ Select $\to$ Monitor $\to$ Judge $\to$ Respond $\to$ Learn $\to$ Capture. This is not a pipeline; it is a cycle (Figure 1).

**Silent failure limitation.** Retrospective Judgement assumes failure is *observable*: the system knows reasoning failed because the outcome did not satisfy $S$. When $S$ is poorly specified (low $\varphi$), the system may not detect failure at all: the output appears plausible but is incorrect. The Learning Loop calibrates $S$ over time, but the first such failure may go undetected. We acknowledge this bootstrapping limitation in Section 6.

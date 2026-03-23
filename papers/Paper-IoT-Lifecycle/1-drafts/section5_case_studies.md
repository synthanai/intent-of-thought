# Section 5: Case Studies

We demonstrate the IoT Lifecycle through three case studies, each tracing a different failure mode through the complete loop: Capture $\to$ Select $\to$ Execute $\to$ Fail $\to$ Judge $\to$ Respond $\to$ Learn $\to$ Capture. To our knowledge, no prior work traces intent governance from initial specification through failure diagnosis through corrective learning in a single worked example.

## 5.1 False Capture: Clinical Decision Support

**Setting.** A clinical decision support system analyses patient symptoms to support triage.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L1 (implicit) | Clinician queries: "Analyse this patient's symptoms." System extracts: $P$ = "list possible diagnoses." $\bar{P}$ absent. $S$ generic. $\varphi \approx 0.3$. |
| **Select** | $f(\text{IoT}) \to$ CoT | Low-fidelity triple selects safe default: chain-of-thought (sequential listing). |
| **Execute** | CoT reasoning | System produces a linear list of diagnoses, processing symptoms independently. |
| **Fail** | $S$ not met | Misses interacting symptom cluster. Symptom A + Symptom B individually benign, jointly diagnostic. |
| **Judge** | False Capture | $P_{\text{reconstructed}}$ = "identify interacting symptom clusters." $P_{\text{reconstructed}} \neq P_{\text{captured}}$: the captured purpose was too shallow. |
| **Respond** | Level 3 (halt) | Medical context warrants re-specification. Elevate to L2 (prompted): "Should this analysis consider symptom interactions?" Re-capture at higher fidelity. GoT selected. |
| **Learn** | Update L1 rules | Medical queries with multiple symptoms default to L2 prompting. $\varphi$ threshold for medical domain adjusted upward. |

**Lifecycle trace:** `CAPTURE(L1) → SELECT(CoT) → EXECUTE → FAIL → JUDGE(False Capture) → RESPOND(L3, re-capture) → LEARN → CAPTURE(L2, improved)`

**Reasoning trace (partial).** CoT step 1: "Patient presents with fatigue." Step 2: "Fatigue → anaemia, thyroid, depression." Step 3: "Patient also presents with joint pain." Step 4: "Joint pain → arthritis, lupus, fibromyalgia." Steps 2 and 4 are independent branches in a linear chain. The interaction (fatigue + joint pain together = lupus indicator) is invisible to CoT because the topology processes symptoms sequentially. GoT, selected after re-capture, creates a node for each symptom and edges for known co-occurrence patterns, surfacing the lupus indicator at the intersection.

## 5.2 False Selection: Legal Precedent Analysis

**Setting.** A legal research system analyses court precedents for a new case.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L2 (prompted) | Full triple: $P$ = "identify all relevant precedents and their interactions." $\bar{P}$ = "must not treat precedents as independent when they interact." $S$ = "produce a relationship graph of precedent dependencies." $\varphi \approx 0.7$. |
| **Select** | $f(\text{IoT}) \to$ ToT | Selection function weights "identify" and "exploration" signals, choosing tree-of-thought for parallel precedent evaluation. |
| **Execute** | ToT reasoning | Evaluates precedents along independent branches; misses contradictions between concurrent holdings. |
| **Fail** | $\bar{P}$ violated | ToT treated precedents as independent despite the explicit Anti-Purpose constraint. |
| **Judge** | False Selection | $P_{\text{captured}} \approx P_{\text{actual}}$ (intent was correct). $T_{\text{optimal}}$ = GoT (precedents have non-linear relationships). $f$ weighted "exploration" over "interconnection." |
| **Respond** | Level 2 (notify) | Flag to user that topology was misselected; suggest GoT re-execution. |
| **Learn** | Update $f$ | Add training case: "precedent interactions" $\to$ GoT preference. Weight "interconnection" keywords toward graph topologies. |

**Lifecycle trace:** `CAPTURE(L2) → SELECT(ToT) → EXECUTE → FAIL → JUDGE(False Selection) → RESPOND(L2, re-select) → LEARN → SELECT(GoT, improved)`

**Reasoning trace (partial).** ToT Branch A: "Smith v. Jones (2018) establishes duty of care." Branch B: "Brown v. State (2019) limits duty of care in government contexts." Branch C: "Garcia v. County (2020) extends Brown." Branches evaluated independently: each receives a relevance score. The contradiction (Smith establishes broad duty; Brown limits it in exactly the jurisdictional context at issue) is invisible because ToT evaluates branches in isolation. GoT, after re-selection, creates edges between Smith and Brown (CONTRADICTS), Brown and Garcia (EXTENDS), and surfaces the tension that determines the case strategy.

## 5.3 False Execution: Aviation Safety Assessment

**Setting.** An aviation safety system assesses cascading risk factors in maintenance decisions.

| Phase | Operation | Detail |
|-------|-----------|--------|
| **Capture** | L3 (collaborative) | High-fidelity triple ($\varphi \approx 0.9$). $P$ = "assess cascading risk factors in aircraft maintenance decisions." $\bar{P}$ = "must not overlook secondary failure modes or downplay risk severity." $S$ = "produce a risk dependency graph with severity-weighted edges." |
| **Select** | $f(\text{IoT}) \to$ GoT | Correctly selects graph-of-thought for interconnected risk analysis. |
| **Execute** | GoT reasoning | Proceeds correctly through steps 1-6. At step 7, reasoning drifts from risk assessment toward compliance checklist generation. $\delta = 0.72$ (threshold = 0.5). |
| **Fail** | $\delta > \theta$ | Drift detected. Output quality degrading toward lower-risk compliance reporting. |
| **Judge** | False Execution | $P_{\text{captured}} \approx P_{\text{actual}}$. $T_{\text{selected}} \approx T_{\text{optimal}}$. Drift at step 7: execution deviated despite correct intent and topology. |
| **Respond** | Level 4 (escalate) | Aviation safety context. Halt at checkpoint. Escalate to human safety officer. Re-anchor to $\bar{P}$ ("must not downplay risk severity"). Resume from step 6 with doubled checkpoint frequency. Full audit trail logged. |
| **Learn** | Calibrate $\delta$ | Lower drift threshold for safety-critical domains ($\theta = 0.3$ for aviation versus $\theta = 0.5$ default). Add case to benchmark dataset. |

**Lifecycle trace:** `CAPTURE(L3) → SELECT(GoT) → EXECUTE → DRIFT(δ=0.72) → JUDGE(False Execution) → RESPOND(L4, escalate) → LEARN → EXECUTE(GoT, checkpointed)`

**Reasoning trace (partial).** GoT steps 1-6: Node "engine wear" → edge to "hydraulic pressure" (severity 8); node "hydraulic pressure" → edge to "landing gear reliability" (severity 9); node "maintenance interval" → edges to all three (modifier). Step 7 (drift): reasoning shifts from "what fails if hydraulic pressure drops?" to "is the maintenance schedule compliant with FAA 14 CFR Part 43?" The topic is related but the topology output changes from a risk dependency graph to a compliance checklist, violating $S$. Drift detection compares the semantic trajectory of steps 1-6 (risk assessment vocabulary: "failure," "cascade," "severity") against step 7 (compliance vocabulary: "regulation," "schedule," "compliant"). The cosine distance between step 7's embedding and the running mean of steps 1-6 exceeds $\theta = 0.5$.

All three case studies trace the complete lifecycle. The failure mode determines the correction target: capture strategy (Case 1), selection function (Case 2), or execution parameters (Case 3). The governance response scales with intent criticality: Level 3 (medical, re-specify), Level 2 (legal, notify), Level 4 (aviation, escalate).

# EXPERIMENTAL PLAN: Paper-IoT-Lifecycle
# "The IoT Lifecycle: Empirical Validation"

**Goal:** Extensive empirical evidence for all three contributions (Capture Spectrum, Retrospective Judgement, Governance-Proportional Response).

---

## Experiment Overview

| # | Experiment | Tests | What It Proves |
|---|-----------|-------|----------------|
| E1 | Capture Fidelity Gradient | Capture Spectrum (L0-L3) | Higher capture fidelity → better topology selection → better reasoning outcomes |
| E2 | Topology Misselection Impact | Selection function + failure | Wrong topology hurts, and the degree depends on task type |
| E3 | Retrospective Judgement Accuracy | 3 failure modes | The reconstruction algorithm correctly identifies WHY reasoning failed |
| E4 | Governance Response Effectiveness | Proportional correction | Lifecycle correction improves outcomes vs. naive retry |
| E5 | End-to-End Lifecycle | Full closed loop | Complete lifecycle outperforms forward-only IoT and no-IoT baselines |
| E6 | Cross-Model Generalisation | Model independence | Results hold across GPT-4o, Claude 3.5, Gemini 1.5, Llama 3 |

---

## E1: Capture Fidelity Gradient

**Hypothesis:** Higher capture fidelity (L0 → L1 → L2 → L3) produces more accurate topology selection and higher reasoning quality.

### Design
- **Tasks:** 60 reasoning tasks across 3 domains (medical, legal, technical), 20 per domain
- **Each task has a ground-truth optimal topology** (expert-labeled: CoT, ToT, or GoT)
- **Conditions:** Each task is run at 4 capture levels:
  - L0: Zero (task text only, no intent specification)
  - L1: Implicit (task text + domain context)
  - L2: Prompted (explicit P, Anti-P, S elicitation)
  - L3: Collaborative (multi-turn refinement of the IoT triple)
- **Measurements:**
  - Topology selection accuracy (did the system select the expert-labeled optimal topology?)
  - IoT triple completeness (is P present? Anti-P? S?)
  - Reasoning outcome quality (0-5 expert rating)
  - Fidelity score φ (computed from triple completeness + specificity)

### Expected Results
| Capture Level | Topology Accuracy | Outcome Quality |
|:-------------:|:-----------------:|:---------------:|
| L0 | ~40% (defaults to CoT) | Low |
| L1 | ~55% | Medium-Low |
| L2 | ~75% | Medium-High |
| L3 | ~90% | High |

### Statistical Analysis
- ANOVA across capture levels for topology accuracy and outcome quality
- Regression: φ → topology accuracy (is fidelity predictive?)
- Per-domain breakdown (does the gradient hold across domains?)

---

## E2: Topology Misselection Impact

**Hypothesis:** Using the wrong topology for a given intent produces measurably worse outcomes, and the degradation varies by mismatch type.

### Design
- **Tasks:** 30 tasks where the optimal topology is known
  - 10 CoT-optimal (sequential, single-path)
  - 10 ToT-optimal (parallel exploration needed)
  - 10 GoT-optimal (interconnected, feedback loops)
- **Conditions:** Each task run with ALL 3 topologies (CoT, ToT, GoT)
  - 30 tasks × 3 topologies = 90 runs
- **Measurements:**
  - Reasoning quality (0-5 expert rating)
  - Completeness (did the answer address all aspects?)
  - Error types (missed interactions, premature convergence, irrelevant exploration)

### Expected Results
- CoT on GoT-optimal tasks: misses interactions (the clinical triage scenario)
- ToT on CoT-optimal tasks: wasteful exploration, slower, no quality gain
- GoT on ToT-optimal tasks: over-connecting independent options

---

## E3: Retrospective Judgement Accuracy

**Hypothesis:** The 7-step reconstruction algorithm correctly diagnoses the failure mode in >80% of cases.

### Design
- **Tasks:** 45 deliberately-failed reasoning tasks (15 per failure mode)
  - 15 False Capture: give wrong intent, let system reason, see if judgement detects the wrong P
  - 15 False Selection: give correct intent, force wrong topology, see if judgement detects T mismatch
  - 15 False Execution: give correct intent + topology, induce drift, see if judgement detects drift
- **Gold standard:** Each task has an expert-labeled failure mode
- **Measurements:**
  - Diagnosis accuracy (correct failure mode identified?)
  - Reconstruction quality (how close is P_reconstructed to P_actual?)
  - False positive rate (does the algorithm misclassify failure modes?)

### The Reconstruction Test
For each failed task:
1. Run the 7-step algorithm
2. Compare diagnosed mode vs. expert label
3. Measure P_reconstructed similarity to P_actual (cosine similarity of embeddings)

### Expected Results
| Failure Mode | Detection Accuracy | P_reconstructed Quality |
|:------------:|:------------------:|:-----------------------:|
| False Capture | ~85% | Medium (ill-posed) |
| False Selection | ~90% | High (P was correct) |
| False Execution | ~95% | High (both P and T were correct) |

---

## E4: Governance Response Effectiveness

**Hypothesis:** Governance-proportional correction (the right response for the right failure) produces better recovery than naive retry.

### Design
- **Tasks:** 30 failed tasks from E3
- **Conditions:**
  - Baseline: naive retry (same parameters, same topology)
  - IoT Correction: apply the governance-appropriate response
    - False Capture → elevate capture mode, re-specify
    - False Selection → re-select topology
    - False Execution → re-execute with tighter drift threshold
- **Measurements:**
  - Recovery success rate (did the corrected run succeed?)
  - Recovery efficiency (runs needed to succeed)
  - Outcome quality after correction

### Expected Results
| Correction Type | Naive Retry Success | IoT Correction Success |
|:---------------:|:-------------------:|:----------------------:|
| False Capture | ~20% (same bad P) | ~75% (elevated capture) |
| False Selection | ~30% (same bad T) | ~85% (corrected T) |
| False Execution | ~50% (drift may or may not recur) | ~90% (tighter θ) |

---

## E5: End-to-End Lifecycle Comparison

**Hypothesis:** The complete IoT Lifecycle (Capture → Select → Monitor → Judge → Respond → Learn) outperforms both no-IoT and forward-only IoT baselines.

### Design
- **Tasks:** 60 tasks from E1 (same tasks, different conditions)
- **3 Conditions:**
  - A: **No IoT** (prompt → reason → output, single topology, no governance)
  - B: **Forward IoT** (Paper 1: specify → select → monitor, but no judgement/correction)
  - C: **Full Lifecycle** (Capture → Select → Monitor → Judge → Respond → Learn)
- **Allow up to 3 reasoning attempts per task** (lifecycle gets correction loops)
- **Measurements:**
  - First-attempt success rate
  - Final success rate (after corrections)
  - Total tokens consumed (efficiency)
  - Time to correct answer

### Expected Results
| Condition | First-Attempt Success | Final Success | Efficiency |
|:---------:|:---------------------:|:-------------:|:----------:|
| No IoT | ~45% | ~45% (no correction) | Baseline |
| Forward IoT | ~65% | ~65% (no correction) | +30% tokens |
| Full Lifecycle | ~65% (same as Forward) | ~88% (with corrections) | +60% tokens |

---

## E6: Cross-Model Generalisation

**Hypothesis:** Results hold across model families.

### Design
- **Subset:** 20 tasks from E5 (balanced across domains)
- **Models:** GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3 70B
- **Run full lifecycle on each model**
- **Measurements:** Same as E5, per model

---

## Implementation Requirements

### Benchmark Dataset (IoT-Bench)
Create a curated dataset of 60 reasoning tasks:

| Domain | Tasks | CoT-Optimal | ToT-Optimal | GoT-Optimal |
|--------|:-----:|:-----------:|:-----------:|:-----------:|
| Medical | 20 | 7 | 6 | 7 |
| Legal | 20 | 7 | 6 | 7 |
| Technical | 20 | 6 | 7 | 7 |
| **Total** | **60** | **20** | **19** | **21** |

Each task includes:
- Task description (the reasoning problem)
- Expert-labeled optimal topology (ground truth)
- Expert-labeled IoT triple (gold standard P, Anti-P, S)
- Domain-specific context
- Expected output characteristics

### Code Modules Needed
1. **iot_capture.py** - Implements L0-L3 capture modes
2. **iot_selector.py** - Topology selection function f(IoT, context, φ)
3. **iot_monitor.py** - Drift detection δ(trace, P)
4. **iot_judge.py** - 7-step reconstruction algorithm
5. **iot_respond.py** - Governance-proportional response
6. **iot_benchmark.py** - Task runner, results collection, statistical analysis
7. **topology_runners/** - CoT, ToT, GoT implementations per model

### Evaluation Metrics
| Metric | Type | Source |
|--------|------|--------|
| Topology Selection Accuracy | Automated | Compare selected vs. expert-labeled |
| Reasoning Quality | Human | 0-5 expert rating (2 raters, inter-rater reliability) |
| Triple Completeness | Automated | Check P, Anti-P, S presence and specificity |
| Fidelity Score φ | Automated | Computed from completeness + specificity |
| Diagnosis Accuracy | Automated | Compare diagnosed vs. expert-labeled failure mode |
| Recovery Success | Automated | Did corrected run satisfy S? |
| Token Efficiency | Automated | Total tokens per successful outcome |

### Expert Raters
- Need 2 domain experts per domain (6 total) for quality ratings
- Or: use strong LLM-as-judge (GPT-4o) with human spot-checks on 20% sample

---

## Paper Structure with Experiments

The paper expands from 10 pages to ~16-18 pages (or 12 + supplementary):

| Section | Content | Pages |
|---------|---------|:-----:|
| 1. Introduction | Framework recap, lifecycle gap, contributions | 1.5 |
| 2. Background | Related work (keep current) | 2 |
| 3. Capture Spectrum | L0-L4 definition (keep current) | 2 |
| 4. Retrospective Judgement | 3 failure modes, algorithm (keep current) | 2.5 |
| 5. **Experimental Setup** | **NEW: IoT-Bench, design, metrics** | **2** |
| 6. **Results** | **NEW: E1-E6 findings** | **3** |
| 7. Discussion | Expanded with empirical insights | 1.5 |
| 8. Conclusion | Updated | 0.5 |
| Appendices | Formal duality, extended results, dataset | 4 |

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Build IoT-Bench (60 tasks) | 1 week | Curated benchmark dataset |
| 2. Implement code modules | 1 week | iot_capture, iot_judge, topology runners |
| 3. Run E1-E4 | 1 week | Core experimental results |
| 4. Run E5-E6 | 1 week | End-to-end and cross-model |
| 5. Write experimental sections | 1 week | Sections 5-6 drafted |
| 6. Revise full paper | 1 week | Integrated draft |
| **Total** | **6 weeks** | **Submission-ready** |

---

## Key Risks

| Risk | Mitigation |
|------|------------|
| Results don't support hypotheses | Report honestly, adjust claims |
| Expert rating is expensive | LLM-as-judge with human spot-checks |
| GoT implementation varies | Use consistent graph construction across models |
| Token costs for 4 models × 60 tasks × multiple conditions | Budget ~$500-1000 API costs |
| Topology selection is subjective | Use 2 independent expert labelers, measure agreement |

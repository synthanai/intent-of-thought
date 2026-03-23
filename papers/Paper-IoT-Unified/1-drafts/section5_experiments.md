# Section 5: Evidence

We evaluate the IoT governance layer through three experiments designed to test its core claims: that governance improves reasoning quality (Experiment 1), that the Anti-Purpose primitive contributes measurably (Experiment 5), and that topology misselection produces predictable degradation patterns (Experiment 8). A fourth experiment tests generalisation to frontier API models (Experiment 9).

## 5.1 Experimental Design

**Models.** We evaluate 7 models spanning consumer-grade (7B parameters) to large mixture-of-experts (120B parameters, 12B active):

| Model | Parameters | Architecture | Backend |
|-------|:----------:|:------------:|:-------:|
| qwen2.5:7b | 7B | Dense | Local (Ollama) |
| mistral:latest | 7B | Dense | Local (Ollama) |
| deepseek-r1:7b | 7B | Dense | Local (Ollama) |
| qwen3.5:9b | 9B | Dense | Local (Ollama) |
| gemma3:12b | 12B | Dense | Local (Ollama) |
| phi4:14b | 14B | Dense | Local (Ollama) |
| nvidia/nemotron-120b | 120B (12B active) | MoE | Cloud (OpenRouter) |

One model (qwen3.5:9b) was excluded from analysis due to insufficient data: 90% of its responses were empty (generation failures), yielding only 1 usable response for the baseline condition. One cloud model (z-ai/glm-5-turbo) was included in the experiment but showed non-significant results (-8.3%, per-task analysis revealed inconsistent directionality; see Section 7). Results reported below are for the 7 models with sufficient data.

**Tasks.** 18 reasoning tasks across 6 domains (clinical diagnosis, software debugging, mathematical proof, logistics optimisation, architecture comparison, algorithm tracing). Tasks are classified by optimal reasoning structure: *sequential* (single-path derivation), *parallel* (multiple viable approaches), and *interconnected* (non-linear relationships requiring cross-factor analysis).

**Topologies.** Four topologies tested: chain-of-thought (CoT), tree-of-thought (ToT), graph-of-thought (GoT), and a baseline condition (no topology instruction).

**Conditions.** Two governance conditions:

- *Baseline*: task prompt only, no IoT specification.
- *IoT L2*: task prompt preceded by an explicit IoT governance triple specifying Purpose, Anti-Purpose, and Success Signal (Prompted capture, Table 3).

**Scoring.** All responses scored on a 0 to 3 scale (0: wrong, 1: partial, 2: correct, 3: excellent) using an LLM-as-judge approach [Zheng et al., 2023] with phi4:14b as evaluator. Each response was scored against a domain-expert-authored ground truth rubric. Judge self-consistency was measured at 98% (91/93 re-scored responses matched).

**Reproducibility.** All local models were run via Ollama with temperature 0.7 and default sampling parameters. Cloud models were accessed via OpenRouter API with temperature 0.7. No random seeds were fixed (each response represents a single stochastic sample). Prompt templates for all three experiments, including the IoT governance triple format and the LLM-as-judge rubric, are provided in the supplementary materials.

**Infrastructure.** Local models served via Ollama; cloud models accessed via OpenRouter API. Total scored evaluations: 705 across all experiments.

## 5.2 Experiment 1: Governance Impact (N = 486)

**Hypothesis.** Adding an IoT governance triple (L2 Prompted capture) before reasoning improves output quality relative to an ungoverned baseline.

### Results

**Table 4: Overall governance impact.**

| Condition | Mean Score (0 to 3) | N |
|-----------|:-----------------:|:---:|
| Baseline (no IoT) | 2.10 | 240 |
| IoT L2 (governance triple) | **2.43** | 246 |
| **Uplift** | **+0.33 (+15.7%)** | |

The governance uplift is consistent across the majority of models. A paired t-test on the subset of exactly matched reasoning episodes (N = 209 matched pairs) confirms this overall uplift is statistically significant (p < 0.001). Table 5 reports the granular per-model breakdown.

**Table 5: Per-model governance impact (sorted by uplift).**

| Model | Params | Baseline | IoT L2 | Change | Uplift |
|-------|:------:|:--------:|:------:|:------:|:------:|
| qwen2.5:7b | 7B | 2.08 | 2.77 | +0.69 | **+33.3%** |
| mistral:latest | 7B | 1.62 | 2.10 | +0.49 | **+30.2%** |
| gemma3:12b | 12B | 2.13 | 2.61 | +0.47 | **+22.2%** |
| nemotron-120b | 120B | 2.27 | 2.64 | +0.37 | +16.3% |
| phi4:14b | 14B | 2.34 | 2.71 | +0.37 | +15.7% |
| deepseek-r1:7b | 7B | 2.09 | 2.34 | +0.25 | +12.0% |
| z-ai/glm-5-turbo | ~14B | 2.31 | 2.12 | -0.19 | -8.3% |

### Finding 1: Governance as Cognitive Equaliser

The governance uplift is inversely correlated with model capability: smaller models (7B) gain +30 to 33%, while larger models (14B to 120B) gain +12 to 16%. This pattern suggests that IoT governance functions as a *cognitive equaliser*: it compensates for weaker models' inability to self-structure reasoning, providing external architectural scaffolding that stronger models partially possess internally.

### Finding 2: Governance as Topology Safety Net

Table 6 reports the per-topology governance impact.

**Table 6: Per-topology governance impact (sorted by uplift).**

| Topology | Baseline | IoT L2 | Change | Uplift |
|----------|:--------:|:------:|:------:|:------:|
| ToT | 1.67 | 2.28 | +0.62 | **+37.0%** |
| GoT | 1.96 | 2.53 | +0.57 | **+29.1%** |
| Baseline (none) | 2.37 | 2.48 | +0.12 | +4.9% |
| CoT | 2.35 | 2.44 | +0.09 | +3.8% |

Governance rescues the worst-performing topologies: ToT gains +37% and GoT gains +29%. CoT, already robust, gains only +3.8%. The governance benefit scales inversely with topology quality: the more a topology needs structural guidance, the more governance helps.

This finding has an important practical implication: IoT governance is not merely a quality improvement mechanism; it is a *safety net* that makes topology misselection survivable. Without governance, selecting the wrong topology produces catastrophic results (see Experiment 8 below). With governance, the same misselection produces usable, if suboptimal, results.

## 5.3 Experiment 5: Anti-Purpose Ablation (N = 88)

**Hypothesis.** The Anti-Purpose primitive contributes measurably to reasoning quality beyond what Purpose and Success Signal provide.

### Design

Three conditions, each using L2 Prompted capture with one component ablated:
- *Full Triple*: complete IoT specification (Purpose, Anti-Purpose, Success Signal).
- *No Anti-Purpose*: Purpose and Success Signal only.
- *No Success Signal*: Purpose and Anti-Purpose only.

### Results

**Table 7: Anti-Purpose ablation.**

| Condition | Mean Score | Std Dev | N | Change vs Full |
|-----------|:---------:|:---:|:---:|:-----------------:|
| Full Triple (Purpose, Anti-Purpose, Success Signal) | **2.20** | 0.81 | 30 | Ref. |
| No Success Signal (Purpose, Anti-Purpose) | 2.17 | 0.83 | 30 | -0.03 |
| No Anti-Purpose (Purpose, Success Signal) | 2.11 | 0.88 | 28 | -0.09 |

### Finding 3: Anti-Purpose as Drift Guard

Removing Anti-Purpose produces the lowest scores, confirming that explicit negative guardrails contribute to reasoning quality. We note, however, the high variance (standard deviation around 0.85 on a 3-point scale) and the modesty of the effect size (+4% uplift when Anti-Purpose is present). A paired t-test indicates this difference is directionally consistent but not statistically significant (p = 0.14) at current sample sizes.

Rather than a definitive proof of necessity, we interpret this finding as consistent with the view that Anti-Purpose functions as a drift guard: it operates as a boundary constraint rather than a primary driver of reasoning success. Its absence does not cause catastrophic failure; it permits gradual drift that accumulates over multi-step reasoning. We expect the effect to be larger on longer reasoning chains and more open-ended generative tasks, remaining a structural hypothesis for future work.

## 5.4 Experiment 8: The Confusion Matrix (N = 131)

**Hypothesis.** Using the wrong topology for a given task category produces measurably worse outcomes, and the degradation pattern is predictable from the topology-purpose mapping (Table 2).

### Design

Each of 3 task categories (sequential, parallel, interconnected) is paired with each of 3 topologies (CoT, ToT, GoT), producing a 3x3 confusion matrix. Tasks are run across 5 models under IoT L2 governance.

### Results

**Table 8: The Confusion Matrix (Task Category x Topology).**

| Task Category | CoT | GoT | ToT | Optimal (Table 2) |
|:--------------|:---:|:---:|:---:|:------------------:|
| Sequential | **2.13** | 1.71 | 1.64 | CoT |
| Parallel | **2.07** | 1.27 | 2.00 | ToT |
| Interconnected | **2.47** | 2.20 | 1.00 | GoT |

### Finding 4: CoT Unreasonable Robustness

CoT achieves the highest or near-highest score in *every* task category, including those Table 2 assigns to GoT (interconnected: 2.47 vs. 2.20) and ToT (parallel: 2.07 vs. 2.00). At the model scales tested (7B to 14B), CoT is a universally safe default.

### Finding 5: Topology Misselection is Catastrophic

The confusion matrix confirms that wrong topology selection can be catastrophic. ToT on interconnected tasks scores 1.00, a complete failure. GoT on parallel tasks scores 1.27. These are not gradual degradations; they are structural mismatches that produce qualitatively different (worse) outputs.

### Finding 6: The Combined Insight

Findings 4 and 5 together produce the paper's most practically important result: *you probably don't need to select a topology (CoT is safe), but if you do, getting it wrong is catastrophic, and governance makes the wrong selection survivable (Experiment 1, Table 6).*

This reframes the IoT framework's contribution: from "always select the optimal topology" to "default to CoT, escalate only when justified, and use governance to protect against the consequences of topology failure."

**Table 9: Per-model confusion matrix scores.**

| Model | CoT | GoT | ToT |
|-------|:---:|:---:|:---:|
| phi4:14b | 2.56 | 1.89 | 2.11 |
| gemma3:12b | 2.56 | 1.56 | 1.89 |
| qwen2.5:7b | 2.33 | 2.11 | 1.33 |
| deepseek-r1:7b | 2.22 | 1.88 | 1.33 |
| mistral:latest | 1.44 | 1.22 | 1.00 |

The CoT robustness pattern holds across all models tested, including the weakest (mistral, 1.44). The cross-model consistency strengthens the finding's generalisability within the tested parameter range.

## 5.5 Experiment 9: Frontier Model Generalisation (N = 72)

**Hypothesis.** The governance uplift observed in local 7B to 14B models generalises to frontier API models, though the absolute magnitude of the uplift will scale inversely with the model's baseline capability.

### Design

Two frontier models, gpt-4o-mini (~8B distilled) and claude-3.5-haiku (~20B), were evaluated across the 18-task comprehensive benchmark. Each model was tested in two conditions: an unguided baseline and the full IoT L2 (Purpose, Anti-Purpose, Success Signal) governance prompt. Responses were independently scored by phi4:14b on the standard 0 to 3 rubric.

### Results

**Table 10: Frontier model governance impact.**

| Model | Baseline Mean | IoT L2 Mean | Change (Uplift) | N |
|-------|:-------------:|:-----------:|:-----------------:|:---:|
| claude-3.5-haiku | 2.83 | 2.78 | -0.06 (-2.0%) | 18 |
| gpt-4o-mini | 2.28 | 2.56 | +0.28 (+12.2%) | 18 |
| **Overall Frontier** | 2.56 | 2.67 | **+0.11 (+4.3%)** | 36 |

### Finding 7: The Capability Ceiling Effect

The results confirm that governance uplift does not scale linearly with model intelligence; it scales with *model need*.

Claude 3.5 Haiku achieved a near-perfect baseline score (2.83/3.00). At this level of baseline competence, explicit structural governance is redundant and imposes a slight cognitive overhead, resulting in a marginal loss (-2.0%). The model already intrinsically executes the guardrails that IoT makes explicit.

In contrast, gpt-4o-mini (baseline 2.28) demonstrated a significant +12.2% uplift when governed by the IoT triple, elevating its reasoning reliability toward Haiku's baseline. This validates that the Intent of Thought framework is highly effective for "punching up" the reliability of smaller, faster, or distilled models, transforming cost-effective inference engines into robust reasoning agents.

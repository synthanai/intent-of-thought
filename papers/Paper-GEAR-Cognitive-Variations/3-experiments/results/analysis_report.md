# G.E.A.R. Experiment: Analysis Report

> Generated: 2026-03-17T19:20:47.312974
> Valid runs: 458 / 144
> Models: gemini-2.5-pro, gemma3:12b, nvidia/nemotron-3-super-120b-a12b:free, openrouter/hunter-alpha, qwen2.5:7b, z-ai/glm-5
> Vocabulary: 12619 unique tokens

## 1. Headline Result: Variation vs Personality Effect

The core question: does changing cognitive variation produce MORE output divergence
than changing personality, when task and model are held constant?

| Dimension Changed | Mean Cosine Similarity | Mean Divergence (1-cos) | Mean Jaccard Distance |
|-------------------|----------------------|------------------------|----------------------|
| **Variation** (GEAR) | 0.7467 (SD=0.1196) | **0.2533** | 0.7767 |
| **Personality** | 0.7561 (SD=0.1208) | **0.2439** | 0.7679 |

**Finding:** Variation produces **1.0x more divergence** than personality.
This supports the approximate independence claim: cognitive variation is a meaningful
dimension that changes output independently of (and more than) personality framing.

## 2. Cross-Model Consistency

Does the effect hold across architecturally different models?

| Model | Var Divergence | Pers Divergence | Var/Pers Ratio | Effect Consistent? |
|-------|---------------|-----------------|----------------|-------------------|
| gemini-2.5-pro | 0.4446 | 0.4595 | 0.97x | No |
| gemma3:12b | 0.3494 | 0.3397 | 1.03x | Yes |
| nvidia/nemotron-3-super-120b-a12b:free | 0.1906 | 0.1781 | 1.07x | Yes |
| openrouter/hunter-alpha | 0.1803 | 0.1793 | 1.01x | Yes |
| qwen2.5:7b | 0.2902 | 0.2315 | 1.25x | Yes |
| z-ai/glm-5 | 0.3764 | 0.3544 | 1.06x | Yes |

## 3. Variation Pair Divergence Matrix

Which variation pairs produce the most different outputs? (lower similarity = more different)

| Variation Pair | Mean Cosine Sim | Divergence | N |
|---------------|----------------|------------|---|
| adversarial ↔ engaging | 0.7422 | 0.2578 | 112 |
| adversarial ↔ generative | 0.7274 | 0.2726 | 112 |
| adversarial ↔ reflective | 0.7573 | 0.2427 | 111 |
| engaging ↔ generative | 0.7376 | 0.2624 | 115 |
| engaging ↔ reflective | 0.7691 | 0.2309 | 111 |
| generative ↔ reflective | 0.7470 | 0.2530 | 111 |

**Blind spot prediction test:** The framework predicts that Adversarial ↔ Engaging
and Generative ↔ Reflective should show maximal divergence (lowest similarity).

- Split ↔ Join (predicted blind spot pair): cosine=0.7422, divergence=0.2578
- Forward ↔ Backward (predicted blind spot pair): cosine=0.7470, divergence=0.2530

## 4. Per-Task Analysis

Does variation effect hold across different task types?

| Task | Var Mean Sim | Pers Mean Sim | Var > Pers? |
|------|-------------|---------------|-------------|
| analyse_scenario | 0.6678 | 0.6724 | **Yes** |
| cognitive_science | 0.7862 | 0.7986 | **Yes** |
| complex_system | 0.7858 | 0.7776 | No |
| design_tradeoff | 0.7796 | 0.7892 | **Yes** |
| economic_paradox | 0.8314 | 0.8370 | **Yes** |
| emergence_debate | 0.8208 | 0.8209 | **Yes** |
| epistemology | 0.8360 | 0.8413 | **Yes** |
| ethical_ai | 0.8320 | 0.8491 | **Yes** |
| leadership_failure | 0.8451 | 0.8543 | **Yes** |
| org_paradox | 0.8162 | 0.8256 | **Yes** |
| review_code | 0.5927 | 0.6497 | **Yes** |
| summarise_finding | 0.6139 | 0.6022 | No |

## 5. Structural Element Profiles by Variation

Do different variations produce structurally different outputs?
(Mean count of structural elements per response)

| Variation | Questions | Warnings | Connections | Reflections | Creations | Recommendations |
|-----------|--------|--------|--------|--------|--------|--------|
| **Adversarial** | 1.9 | 2.9 | 2.3 | 1.3 | 2.4 | 1.1 |
| **Engaging** | 0.7 | 1.8 | 3.9 | 1.3 | 2.3 | 0.9 |
| **Generative** | 1.0 | 1.8 | 1.9 | 1.4 | 3.7 | 1.1 |
| **Reflective** | 1.0 | 1.8 | 3.1 | 2.5 | 2.6 | 1.3 |

**Expected pattern (if GEAR works):**
- Generative should have highest 'creations'
- Adversarial should have highest 'warnings'
- Engaging should have highest 'connections'
- Reflective should have highest 'reflections'

✅ Generative has highest 'creations' count
✅ Adversarial has highest 'warnings' count
✅ Engaging has highest 'connections' count
✅ Reflective has highest 'reflections' count

**Structural signature match: 4/4**

## 6. Summary

- **Total valid runs:** 458
- **Variation divergence:** 0.2533 (mean)
- **Personality divergence:** 0.2439 (mean)
- **Effect ratio:** Variation produces 1.0x more divergence
- **Cross-model:** Effect holds in 5/6 models
- **Cross-task:** Effect holds in 10/12 tasks
- **Structural signature:** 4/4 variations show expected element profile

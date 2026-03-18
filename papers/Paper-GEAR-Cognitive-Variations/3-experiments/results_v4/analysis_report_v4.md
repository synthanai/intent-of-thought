# GEAR v4: Threshold Validation Analysis Report

**Date**: 2026-03-18 16:33
**Total runs**: 192
**Models**: qwen2.5:0.5b, qwen2.5:1.5b, qwen2.5:3b, qwen2.5:7b
**Design**: Same-family gradient (Qwen 2.5), 6 deep tasks, 4 variations, 2 personalities
**Primary metric**: Embedding cosine distance (1 - similarity)

## 1. Basic Stats Per Model

| Model | Size | Runs | Avg Words | Med Words | Avg Time | StDev |
|:------|:-----|:-----|:----------|:----------|:---------|:------|
| qwen2.5:0.5b | 0.5B | 48 | 652 | 611 | 28s | 202 |
| qwen2.5:1.5b | 1.5B | 48 | 572 | 550 | 36s | 140 |
| qwen2.5:3b | 3B | 48 | 634 | 617 | 81s | 98 |
| qwen2.5:7b | 7B | 48 | 627 | 631 | 124s | 69 |

## 2. Embedding-Based Variation Divergence (PRIMARY METRIC)

> Higher cosine distance = more semantic differentiation between cognitive modes

| Model | Size | Var Divergence | Pers Divergence | V/P Ratio | Winner |
|:------|:-----|:---------------|:----------------|:----------|:-------|
| qwen2.5:0.5b | 0.5B | 0.1222 | 0.1241 | 0.98x | PERSONALITY |
| qwen2.5:1.5b | 1.5B | 0.0939 | 0.0884 | 1.06x | VARIATION |
| qwen2.5:3b | 3B | 0.0839 | 0.0921 | 0.91x | PERSONALITY |
| qwen2.5:7b | 7B | 0.0827 | 0.0845 | 0.98x | PERSONALITY |

## 3. Size Gradient: Divergence vs Parameter Count

> This is the KEY test. If the threshold hypothesis holds,
> divergence should increase with model size.

| Model | Size | Embed Var Div | Word Count Var Spread | Embed CoV |
|:------|:-----|:--------------|:----------------------|:----------|
| qwen2.5:0.5b | 0.5B | 0.1222 | 226w | 33.5% |
| qwen2.5:1.5b | 1.5B | 0.0939 | 135w | 29.5% |
| qwen2.5:3b | 3B | 0.0839 | 103w | 36.9% |
| qwen2.5:7b | 7B | 0.0827 | 67w | 45.4% |

**Spearman rank correlation (size vs embedding divergence): ρ = -1.000**
→ **Negative correlation**: smaller models show MORE divergence

## 4. Per-Task Embedding Divergence

| Task | qwen2.5:0.5b (0.5B) | qwen2.5:1.5b (1.5B) | qwen2.5:3b (3B) | qwen2.5:7b (7B) |
|:-----|:------||:------||:------||:------|
| complex_system | 0.1381 | 0.0908 | 0.0701 | 0.0540 |
| emergence_debate | 0.1009 | 0.0839 | 0.0542 | 0.0619 |
| epistemology | 0.1571 | 0.0885 | 0.1101 | 0.1099 |
| ethical_ai | 0.1351 | 0.1030 | 0.0955 | 0.0779 |
| leadership_failure | 0.1032 | 0.1035 | 0.0815 | 0.1011 |
| org_paradox | 0.0986 | 0.0938 | 0.0921 | 0.0914 |

## 5. Falsification Control (Inverted Prompts)

> If model READS instructions: normal vs inverted should differ (low similarity)
> If model IGNORES: normal vs inverted should be the same (high similarity)


### qwen2.5:0.5b (0.5B)
| Label | Actual | Words |
|:------|:-------|:------|
| adversarial | generative | 502w |
| engaging | reflective | 824w |
| generative | adversarial | 787w |
| reflective | engaging | 481w |

**Normal vs Inverted Similarity:**
| Variation | Cosine Sim | Interpretation |
|:----------|:-----------|:---------------|
| adversarial | 0.9010 | AMBIGUOUS |
| engaging | 0.9036 | AMBIGUOUS |
| generative | 0.8552 | AMBIGUOUS |
| reflective | 0.8533 | AMBIGUOUS |

**Average similarity: 0.8783**
→ Model PARTIALLY responds to variation instructions

### qwen2.5:7b (7B)
| Label | Actual | Words |
|:------|:-------|:------|
| adversarial | generative | 586w |
| engaging | reflective | 685w |
| generative | adversarial | 788w |
| reflective | engaging | 675w |

**Normal vs Inverted Similarity:**
| Variation | Cosine Sim | Interpretation |
|:----------|:-----------|:---------------|
| adversarial | 0.9264 | AMBIGUOUS |
| engaging | 0.9319 | AMBIGUOUS |
| generative | 0.9768 | SAME (ignores instruction) |
| reflective | 0.9381 | AMBIGUOUS |

**Average similarity: 0.9433**
→ Model PARTIALLY responds to variation instructions

## 6. Verdict

- Smallest model (0.5B) embedding divergence: 0.1222
- Largest model (7B) embedding divergence: 0.0827
- Ratio: 0.68x

### ❌ THRESHOLD HYPOTHESIS NOT SUPPORTED
Embedding-based analysis does not confirm that larger models are more 
responsive to cognitive variation instructions.
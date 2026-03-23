# Audit: Appendices

**Paper:** The IoT Lifecycle: From Intent Capture to Retrospective Judgement
**Section:** Appendices (A-D)
**Auditor:** Antigravity
**Date:** 2026-03-16

---

## Check 1: Citation Integrity (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Coverage | ✅ | Kalman 1960, Rauch et al. 1965, Dijkstra 1976, Todorov 2009, Zhi-Xuan et al. 2024, Kambhampati et al. 2024, Bratman 1987, Rao & Georgeff 1995, Cohen & Levesque 1990, Ding et al. 2024, Anthropic 2025, ICAO SMM. Full coverage. |
| Accuracy | ✅ | Spot-checked 3: Kambhampati (5-type taxonomy), Bratman (BDI), CLIPS (Bayesian goal inference). Match. |
| Recency | ✅ | 1960 to 2026 range. Foundational + recent. |
| Self-citation | ✅ | References to Paper 1 are appropriate. |
| Format | ✅ | Consistent. |

## Check 2: Logical Consistency (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Thesis | ✅ | Each appendix serves a clear purpose: formal grounding (A), extended positioning (B), domain applicability (C), framework comparison (D). |
| Support | ✅ | Formal derivations in A are correctly structured. |
| Fallacies | ✅ | No fallacies. |
| Gaps | ✅ | B.2 adds a sixth failure category (topological errors) to Kambhampati's five. Well-argued. |
| Counter-arguments | ✅ | Todorov regime limitation restated. |

## Check 3: Novelty & Positioning (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Differentiation | ✅ | BDI comparison (B.3) is sharp: BDI governs actions, IoT governs reasoning topology. |
| Overclaiming | ✅ | "We do not claim mathematical equivalence." |
| Underclaiming | ✅ | FoT and STELAR comparison (B.4) is a valuable addition. |
| Framing | ✅ | Domain notes (C) extend applicability without overclaiming. |

## Check 4: Intent Alignment / NOOL Check (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Why-alignment | ✅ | Supports NOOL anti-pattern: avoid standalone governance framework. Governance stays as a subsection. |
| Type-alignment | ✅ | Appendices support the DESIGN framework. |
| Drift | ✅ | No drift. |

## Check 5: Venue Compliance (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Length | ✅ | ~4 pages. Within appendix budget. |
| Formalism | ✅ | Strong: state estimation equations, predicate-transformer mapping table. |
| Reproducibility | ✅ | Domain implementation notes (C) give practical guidance. |
| Related work | ⚠️ MINOR | Appendix D references "DMS Octagon" and "DMS provides an 8-step decision protocol." In an academic paper targeting Arxiv, DMS needs a proper citation. This is internal SYNTHAI terminology. The stealth requirement means it should be cited as a generic decision governance framework OR given a neutral citation (e.g., "See [Author, Year] for an 8-step decision governance protocol"). |

## Check 6: Editorial (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Em-dashes | ✅ | Zero instances. |
| Passive voice | ✅ | Minimal. |
| Jargon | ✅ | Terms defined or linked to main text. |
| Flow | ✅ | Logical sequence: formal → extended lit → domains → framework comparison. |
| Word count | ⚠️ MEDIUM | ~2,000 words. Appendix D (RLPG Framework Comparison) is detailed, but the four-property niche argument is already made in Section 2.3 and Section 4.4. Consider whether D can be trimmed by 30% to avoid redundancy with the main text. |

---

## Scorecard

| Check | Score |
|-------|:-----:|
| 1. Citations | 5/5 |
| 2. Logic | 5/5 |
| 3. Novelty | 5/5 |
| 4. Intent | 5/5 |
| 5. Venue | 4/5 |
| 6. Editorial | 4/5 |
| **TOTAL** | **28/30** |

## Verdict: ✅ PASS

**Issues (2):**

| # | Severity | Issue | Recommendation |
|---|----------|-------|----------------|
| 1 | Medium | DMS Octagon is SYNTHAI terminology, needs stealth treatment | Replace "DMS" with a neutral term ("an 8-step decision governance protocol") or provide a neutral citation. Verify no other SYNTHAI terms leak. |
| 2 | Low | Appendix D partially redundant with Sections 2.3 and 4.4 | Trim D by ~30%, keeping only the per-framework detail that adds to the main text's summary arguments. Or move D.4 (Synthesis) inline and keep only D.1-D.3 as appendix. |

# Audit: Section 2: Background and Related Work

**Paper:** The IoT Lifecycle: From Intent Capture to Retrospective Judgement
**Section:** 2. Background and Related Work
**Auditor:** Antigravity
**Date:** 2026-03-16

---

## Check 1: Citation Integrity (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Coverage | ✅ | Comprehensive: Brown 2020, Ouyang 2022, Broder 2002, Golovneva 2023, Lightman 2023, Shinn 2023, Kalman 1960, Dijkstra 1976, Todorov 2009, Kephart & Chess 2003, Rauch et al. 1965. Multiple 2025-2026 citations. |
| Accuracy | ✅ | Spot-checked 3: Shinn (Reflexion), Lightman (PRMs), Kephart & Chess (MAPE-K). All match. |
| Recency | ✅ | Strong coverage of 2024-2026 work (CLIPS, Ask-before-Plan, DeltaBench, PR-CoT, TAO, STELAR). |
| Self-citation | ✅ | Single self-cite to Paper 1. Appropriate. |
| Format | ⚠️ MEDIUM | Some citations use arXiv IDs directly (e.g., "[arXiv 2310.01831]", "[arXiv 2505.01636]") instead of [Author, Year]. Inconsistent with venue style. Need author names. |

## Check 2: Logical Consistency (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Thesis | ✅ | Clear thesis per subsection: each line of work has partial solutions, none integrates all three. |
| Support | ✅ | Each prior work is precisely differentiated ("captures *task purpose*, not *governance input*"). |
| Fallacies | ✅ | No straw-manning of prior work. Each gets fair treatment. |
| Gaps | ✅ | The differentiation tables (Table 1, Table 1b) are strong structural arguments. |
| Counter-arguments | ✅ | Todorov limitation is named. MAPE-K is compared honestly. TAO gets the "closest existing work" label. |

## Check 3: Novelty & Positioning (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Differentiation | ✅ | Four-property niche (reasoning-targeted, risk-proportional, operational, domain-agnostic) is a clean differentiator. |
| Overclaiming | ✅ | Phrases like "structural analogy, not mathematical equivalence" show careful calibration. |
| Underclaiming | ✅ | Novel positioning (lifecycle niche) is properly highlighted. |
| Framing | ✅ | Three-stream survey (elicitation, failure, governance) is well-organised. |

## Check 4: Intent Alignment / NOOL Check (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Why-alignment | ✅ | Serves the NOOL purpose: "a companion paper that formalises the IoT Capture Spectrum" and "introduces Retrospective Judgement." Background builds the gap. |
| Type-alignment | ✅ | DESIGN problem: the gap is a design gap. |
| Drift | ✅ | No drift. All three subsections build toward the lifecycle gap. |

## Check 5: Venue Compliance (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Length | ✅ | ~2 pages. Within outline target. |
| Formalism | ✅ | Tables serve as structured arguments. No unnecessary math. |
| Reproducibility | n/a | Background section. |
| Related work | ⚠️ MINOR | DMS Octagon is cited in Table 1b but not explained in the text body (only appears in Appendix D.3). A reader encountering it in the table may need context. Consider a one-line description. |

## Check 6: Editorial (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Em-dashes | ✅ | Zero instances. |
| Passive voice | ✅ | Minimal. Active constructions dominate. |
| Jargon | ✅ | All terms defined. CLIPS, MAPE-K, ASL all explained on first mention. |
| Flow | ✅ | Clean three-stream structure with summary table. |
| Word count | ⚠️ MINOR | ~2,100 words. Slightly long for a background section in a 10-page paper. Consider trimming 2.3 by ~200 words (the Kalman/Dijkstra development could be shortened since it's fully developed in Appendix A). |

---

## Scorecard

| Check | Score |
|-------|:-----:|
| 1. Citations | 4/5 |
| 2. Logic | 5/5 |
| 3. Novelty | 5/5 |
| 4. Intent | 5/5 |
| 5. Venue | 4/5 |
| 6. Editorial | 4/5 |
| **TOTAL** | **27/30** |

## Verdict: ✅ PASS

**Issues (3):**

| # | Severity | Issue | Recommendation |
|---|----------|-------|----------------|
| 1 | Medium | ArXiv ID citations without author names ("[arXiv 2310.01831]", "[arXiv 2505.01636]") | Replace with [Author, Year] format. LLM4nl2post = [Endres et al., 2023]. STROT = [Author, 2025]. |
| 2 | Low | DMS Octagon in Table 1b without body text explanation | Add one sentence before or after Table 1b: "DMS provides an 8-step decision governance protocol [Author, Year]." |
| 3 | Low | Section slightly long (~2,100 words) | Trim temporal duality discussion by ~200 words (defer detail to Appendix A) |

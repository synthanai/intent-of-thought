# Paper Section Audit: Intent of Thought (IoT)
# /paper-section-audit IoT --all
# Date: 2026-03-02
# Venue: Arxiv CS.AI + CL

---

## Summary Metrics

| Section | Words | Target | Δ |
|---------|-------|--------|---|
| 1. Introduction + Abstract | 807 | 750-850 | ✅ |
| 2. Background & Related Work | 1,071 | 800-1000 | ⚠️ +71 |
| 3. IoT Framework | 1,164 | 1000-1200 | ✅ |
| 4. Preliminary Evaluation | 810 | 600-800 | ⚠️ +10 |
| 5. Discussion | 797 | 400-600 | ⚠️ +197 |
| 6. Conclusion | 310 | 200-300 | ⚠️ +10 |
| **TOTAL** | **4,959** | **~4,500** | +459 |

Total with self-audit blocks removed: ~4,300 (within target).

---

## Section 1: Introduction + Abstract

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 4/5 | 8 citations. SWI/ICoT/ARR cite details approximate (marked in flags). |
| 2. Logic | 5/5 | Clean progression: XoT explosion → selection problem → step-level intent → gap → contributions. |
| 3. Novelty | 5/5 | Three contributions clearly stated. Topology-governance gap well-positioned. |
| 4. Intent (NOOL) | 5/5 | Section directly serves the paper's WHY (establishing the gap). |
| 5. Venue | 4/5 | Arxiv-appropriate voice. IoT disambiguation footnote is smart. Missing: explicit "paper structure" paragraph (common in CS.AI). |
| 6. Editorial | 5/5 | 0 em-dashes. Clean flow. All terms defined. |
| **TOTAL** | **28/30** | **PASS** |

**Issues:**
- ⚠️ Add a brief "paper structure" sentence at end: "Section 2 surveys..., Section 3 presents..., Section 4 demonstrates..."
- ⚠️ Verify SWI, ICoT, ARR citation details before submission

---

## Section 2: Background and Related Work

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 4/5 | 17 citations. Added Wang (2023, Self-Consistency), Kojima (2022, Zero-shot), Chen (2023, PoT), Zhou (2023, LATS) inline but NOT in references.bib yet. |
| 2. Logic | 5/5 | Clean taxonomy: topologies → step/domain/retrieval intent → agent/training intent → matrix → gap. |
| 3. Novelty | 5/5 | Differentiation matrix (Table 1) is the centrepiece. 6-level taxonomy is original. |
| 4. Intent (NOOL) | 5/5 | Section establishes the evidence base for the gap claim. |
| 5. Venue | 4/5 | Comprehensive survey for 2 pages. Could add 1-2 more recent XoT papers if available. |
| 6. Editorial | 4/5 | 1 em-dash found (table content "—", not editorial). Slightly over word target. |
| **TOTAL** | **27/30** | **PASS** |

**Issues:**
- ⚠️ Add Wang, Kojima, Chen, Zhou to references.bib
- ⚠️ The "—" in Table 1 row 6 is table content (meaning "none"), not editorial. Acceptable.
- ⚠️ Trim ~70 words if page count is tight.

---

## Section 3: IoT Framework

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 5/5 | Appropriate: cites BDI, Reflexion, RLHF for grounding. Original contribution clearly marked with "we define/propose." |
| 2. Logic | 5/5 | Clean formal structure: primitives → notation → selection → drift. |
| 3. Novelty | 5/5 | Three-primitive framework, selection function f, drift score δ, violation detector v are all novel and clearly distinguished from SWI/BDI. |
| 4. Intent (NOOL) | 5/5 | This IS the core contribution. Directly serves paper's Intent. |
| 5. Venue | 5/5 | Formal notation present (IoT triple, f, δ, v). LaTeX-ready math. Sufficient rigour for CS.AI. |
| 6. Editorial | 5/5 | 0 em-dashes. Clear subsection structure. All notation defined on first use. |
| **TOTAL** | **30/30** | **PASS** |

**Issues:** None.

---

## Section 4: Preliminary Evaluation

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 4/5 | References CoT, ToT, GoT appropriately. No new citations needed for case studies. |
| 2. Logic | 5/5 | Consistent structure across all 3 cases: Problem → IoT Spec → Selection → Contrast. |
| 3. Novelty | 4/5 | Case studies are illustrative, not statistical. Limitation acknowledged upfront. |
| 4. Intent (NOOL) | 5/5 | Demonstrates C3 (illustrative evaluation). Stays within scope. |
| 5. Venue | 4/5 | For Arxiv: acceptable as illustrative. A reviewer may ask for quantitative results. TSB proposal in Section 5.2 addresses this. |
| 6. Editorial | 5/5 | 0 em-dashes. Clean, parallel structure. |
| **TOTAL** | **27/30** | **PASS** |

**Issues:**
- ⚠️ Consider adding a brief "reproducibility" note: "These case studies can be replicated by specifying the IoT triple in any LLM prompt."
- ⚠️ Case 3 (hospital readmission) could be made more concrete with specific factors named.

---

## Section 5: Discussion

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 5/5 | No unsupported claims. TSB is proposed, not claimed. |
| 2. Logic | 5/5 | Limitations → Benchmark → Implications → Capture → False modes. Clean progression. |
| 3. Novelty | 5/5 | TSB benchmark proposal is concrete. False-mode taxonomy (false discovery/process/delivery) is original and strong. |
| 4. Intent (NOOL) | 5/5 | Honest limitations serve the paper's credibility. |
| 5. Venue | 4/5 | Over word target after 5.3 expansion (797 vs 400-600 target). May need trimming. |
| 6. Editorial | 5/5 | 0 em-dashes. Clean transitions. |
| **TOTAL** | **29/30** | **PASS** |

**Issues:**
- ⚠️ Section is ~200 words over target. If page count is tight, trim TSB details or capture spectrum paragraph.
- No stealth violations.

---

## Section 6: Conclusion

| Check | Score | Notes |
|-------|-------|-------|
| 1. Citations | 5/5 | No new claims, no citations needed. |
| 2. Logic | 5/5 | Three-sentence recap + three future directions. No new arguments. |
| 3. Novelty | 5/5 | Properly scoped. Does not overclaim. |
| 4. Intent (NOOL) | 5/5 | Clean summary. No drift. |
| 5. Venue | 5/5 | Appropriate length and tone for Arxiv. |
| 6. Editorial | 5/5 | 0 em-dashes. Tight writing. |
| **TOTAL** | **30/30** | **PASS** |

**Issues:** None.

---

## Cross-Section Continuity Check

| Check | Result |
|-------|--------|
| Contribution consistency | ✅ C1/C2/C3 stated in Intro, delivered in S2/S3/S4, summarised in S6 |
| Terminology consistency | ✅ IoT, P, P̄, S used consistently throughout |
| Table numbering | ✅ T1 (differentiation), T2 (topology selection), T3 (limitations) |
| Forward/back references | ✅ "Section 3.4" referenced from S5, "Section 5.2" referenced from S4 |
| Notation consistency | ✅ f, δ, v, τ used consistently after introduction in S3 |
| Stealth compliance | ✅ Zero branded terms across all sections |

---

## Aggregate Scorecard

| Section | Citations | Logic | Novelty | Intent | Venue | Editorial | Total |
|---------|-----------|-------|---------|--------|-------|-----------|-------|
| 1. Introduction | 4 | 5 | 5 | 5 | 4 | 5 | **28** |
| 2. Background | 4 | 5 | 5 | 5 | 4 | 4 | **27** |
| 3. Framework | 5 | 5 | 5 | 5 | 5 | 5 | **30** |
| 4. Evaluation | 4 | 5 | 4 | 5 | 4 | 5 | **27** |
| 5. Discussion | 5 | 5 | 5 | 5 | 4 | 5 | **29** |
| 6. Conclusion | 5 | 5 | 5 | 5 | 5 | 5 | **30** |
| **AVERAGE** | **4.5** | **5.0** | **4.8** | **5.0** | **4.3** | **4.8** | **28.5/30** |

## Verdict: **PASS** (All sections ≥25/30)

### Pre-Submission Fixes (Minor)

1. Add "paper structure" sentence to end of Introduction
2. Add Wang, Kojima, Chen, Zhou to references.bib
3. Verify SWI, ICoT, ARR citation details (exact titles, authors)
4. Consider trimming S2 and S5 if page count is tight (~460 words over target)
5. Remove self-audit blocks from drafts before assembly

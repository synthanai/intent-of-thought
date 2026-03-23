# Audit: Section 3: The IoT Capture Spectrum

**Paper:** The IoT Lifecycle: From Intent Capture to Retrospective Judgement
**Section:** 3. The IoT Capture Spectrum
**Auditor:** Antigravity
**Date:** 2026-03-16

---

## Check 1: Citation Integrity (4/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Coverage | ⚠️ MEDIUM | Section 3.5 references Ouyang et al. 2022 (RLHF), Bai et al. 2022 (Constitutional AI), and Zhang et al. ICLR 2025 (RLHF discourages clarification). These are well-cited. However, the L4 discussion is a major sub-contribution and lacks citation to relevant training-time intent work (e.g., Hao et al. 2023 on toolformer-style training, or Schick et al. 2023 on tool-augmented LMs). |
| Accuracy | ✅ | Spot-checked 3: Ouyang (RLHF), Bai (constitutional), Zhang ICLR 2025. Match. |
| Recency | ✅ | 2022-2025 range. Appropriate. |
| Self-citation | ✅ | References companion paper for notation. |
| Format | ✅ | Consistent [Author, Year] format. |

## Check 2: Logical Consistency (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Thesis | ✅ | Clear: five-mode hierarchy, architecturally distinct from prompt engineering. |
| Support | ✅ | The six control surfaces (typed artifacts, policies, state machines, security, telemetry, training/runtime) are a strong structural argument. |
| Fallacies | ✅ | The "strongest objection" paragraph (3.4) directly addresses the prompt-engineering conflation, which is intellectually honest. |
| Gaps | ✅ | The L4 paradox and bootstrapping argument (3.5) is novel and well-developed. |
| Counter-arguments | ✅ | "Not purely ordinal" caveat, "confidently wrong triples" for L4 OOD. |

## Check 3: Novelty & Positioning (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Differentiation | ✅ | Type-signature argument is the decisive differentiator. Prompt → task output vs. IoT Capture → governance triple. |
| Overclaiming | ✅ | L4 is correctly positioned as speculative. Fidelity is acknowledged as variable. |
| Underclaiming | ✅ | The six control surfaces are a strong, under-appreciated argument. |
| Framing | ✅ | Explicitly distinguished from maturity models and intent taxonomies. |

## Check 4: Intent Alignment / NOOL Check (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Why-alignment | ✅ | Directly serves NOOL: "Formalises the IoT Capture Spectrum: a 5-mode hierarchy." |
| Type-alignment | ✅ | DESIGN: how should capture be structured? |
| Drift | ✅ | No drift. Tightly scoped. |

## Check 5: Venue Compliance (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Length | ✅ | ~2 pages. Within outline target. |
| Formalism | ✅ | Notation extends Paper 1: IoT_capture, φ, θ_elevate. |
| Reproducibility | ✅ | Five modes are precisely defined in table form. |
| Related work | n/a | (Handled in Section 2) |

## Check 6: Editorial (5/5)

| Sub-check | Status | Notes |
|-----------|:------:|-------|
| Em-dashes | ✅ | Zero instances. |
| Passive voice | ✅ | Minimal. |
| Jargon | ✅ | All terms defined: capture mode, fidelity function, capture spectrum. |
| Flow | ✅ | Table → notation → confidence interaction → differentiation → L4 → visual. Logical progression. |
| Word count | ✅ | ~1,700 words. Appropriate. |

---

## Scorecard

| Check | Score |
|-------|:-----:|
| 1. Citations | 4/5 |
| 2. Logic | 5/5 |
| 3. Novelty | 5/5 |
| 4. Intent | 5/5 |
| 5. Venue | 5/5 |
| 6. Editorial | 5/5 |
| **TOTAL** | **29/30** |

## Verdict: ✅ PASS

**Issues (1):**

| # | Severity | Issue | Recommendation |
|---|----------|-------|----------------|
| 1 | Medium | L4 section lacks citations to training-time tool/intent learning literature | Add 1-2 citations to recent work on training models to produce structured outputs before acting (e.g., Toolformer, Schick et al. 2023, or reasoning-before-acting paradigms). This strengthens the L4 positioning. |

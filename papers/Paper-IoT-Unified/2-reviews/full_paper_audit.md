# Full Paper Audit: Intent of Thought (Unified)

> Combined `/paper-section-audit` (6 checks × 8 sections) + `/audit-readability` (25 dimensions)
> Audit date: 2026-03-18

---

## Part A: Paper-Section Audit (6 Checks × 8 Sections)

### Section 1: Introduction (598 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 3/5 | Claims citing [Wei 2022], [Yao 2024], [Besta 2024] correct. Missing: [Sel 2023] appears in S3 but not in intro topology list. [Radha 2024] cited in footnote but no formal ref entry yet. No references.bib assembled. |
| 2. Logic | 5/5 | Clean argument: gap → consequences → contribution. No fallacies. |
| 3. Novelty | 5/5 | Three contributions clearly stated with numbers. No overclaiming. |
| 4. Intent | 5/5 | Aligns with reframed narrative (governance uplift, not topology selection). |
| 5. Venue | 4/5 | Arxiv-appropriate length and formalism. Could add a figure reference for lifecycle diagram. |
| 6. Editorial | 4/5 | No em-dashes in prose. One compound sentence at line 3 runs 4 lines; could split. |
| **TOTAL** | **26/30** | **PASS** |

---

### Section 2: Background (903 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 3/5 | 13 citations in text but no references.bib. [Broder 2002] and [Radlinski & Craswell 2017] need verification. [Bratman 1987] added but not in Paper 1's refs. |
| 2. Logic | 5/5 | Three threads converge cleanly on the gap. Table 1 is precise. |
| 3. Novelty | 4/5 | Positioning table is strong. Could strengthen the "no existing work asks" claim with a brief search methodology note. |
| 4. Intent | 5/5 | Serves the paper's purpose: establish the gap IoT fills. |
| 5. Venue | 5/5 | Comprehensive for Arxiv. Covers the right prior art. |
| 6. Editorial | 4/5 | Clean prose. "Conversational intent detection in natural language understanding classifies..." is too broad; could cite a specific system. |
| **TOTAL** | **26/30** | **PASS** |

---

### Section 3: Framework (1,080 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 4/5 | [Cohen & Levesque 1990] correctly used. Algorithm pseudocode matches Paper 1 original. |
| 2. Logic | 5/5 | Clean definitions, algorithms, and the critical S3.4 qualification. |
| 3. Novelty | 4/5 | S3.4 (Empirical Qualification) is the key new addition. Handles CoT robustness honestly. |
| 4. Intent | 5/5 | Framework is presented accurately then immediately qualified with empirical reality. |
| 5. Venue | 4/5 | Good formalism. Algorithm pseudocode in code blocks uses em-dash separators ("Step 1: "); acceptable in pseudocode but technically violates the style rule. |
| 6. Editorial | 3/5 | Em-dashes in algorithm steps ("Step 1: "). These are in code blocks so borderline acceptable, but 8 instances. Should use colons or numbers instead. |
| **TOTAL** | **25/30** | **PASS** |

> **Action**: Replace "Step N , " with "Step N:" in pseudocode blocks.

---

### Section 4: Lifecycle (1,258 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 2/5 | [Schick et al., 2023] (Toolformer) mentioned but no others in this section. Capture Spectrum and Retrospective Judgement are novel contributions but could cite relevant intent elicitation literature. |
| 2. Logic | 5/5 | Clean progression: Capture → Confidence Interaction → Judgement → Learning Loop → L4. |
| 3. Novelty | 5/5 | Three failure modes, diagnostic algorithm, and Learning Loop are genuinely novel. |
| 4. Intent | 5/5 | Directly serves the lifecycle contribution. |
| 5. Venue | 4/5 | Algorithm 3 is clear. Formal notation is precise. Could benefit from a lifecycle diagram reference. |
| 6. Editorial | 3/5 | Algorithm 3 uses em-dash separators ("Step 1: "). Line "Capture Spectrum is architecturally distinct from prompt engineering" repeats a claim from S1; could tighten. |
| **TOTAL** | **24/30** | **REVISE** |

> **Actions**: (1) Add citations in Capture Spectrum section. (2) Replace "Step N , " with "Step N:" in Algorithm 3. (3) Remove repeated claim.

---

### Section 5: Experiments (1,431 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 4/5 | [Zheng et al., 2023] for LLM-as-judge is correct. [Mialon, Yao] cited in Discussion but not here. Would benefit from citing [Sel 2023] for AoT. |
| 2. Logic | 5/5 | Clean experimental design → results → findings. No logical gaps. |
| 3. Novelty | 5/5 | Six findings, all empirically supported. Finding 6 (combined insight) is the most practically impactful. |
| 4. Intent | 5/5 | This is the paper's strongest section. Delivers on the empirical promise. |
| 5. Venue | 4/5 | Good reproducibility detail. Missing: random seed info, temperature settings, prompt templates (could go in appendix). |
| 6. Editorial | 4/5 | One em-dash in Table 7 (", " for baseline delta). Replace with "Ref." or "-". Clean otherwise. |
| **TOTAL** | **27/30** | **PASS** |

> **Actions**: (1) Add reproducibility details (temperature, seeds) or reference appendix. (2) Replace ", " in Table 7 with "Ref." or "-".

---

### Section 6: SPAR Case Study (940 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 2/5 | No formal citations. "LOON" is introduced without citation or footnote. The case study references no external systems for comparison. |
| 2. Logic | 5/5 | Five phases map cleanly to IoT lifecycle components. The interpretation boxes are strong. |
| 3. Novelty | 4/5 | Longitudinal case study is strong complement to controlled experiments. Honest about causality limitations. |
| 4. Intent | 5/5 | Directly serves the "self-realised IoT" narrative user requested. |
| 5. Venue | 3/5 | For Arxiv, a case study without external citations or comparison to other debate protocols is weak. Should cite at least [Du et al., 2023] on multi-agent debate and [Liang et al., 2023] on LLM debates. |
| 6. Editorial | 3/5 | "LOON (Looking Outward, Opening Nool)" is SYNTHAI jargon that breaks the "no proprietary branding" rule. Must be described generically. Table header "Failure Mode Addressed" has a trailing ", " em-dash for Phase 1. |
| **TOTAL** | **22/30** | **REVISE** |

> **Actions**: (1) Add citations to multi-agent debate literature. (2) Remove "LOON" acronym, describe generically as "structured retrospection." (3) Replace em-dash in table. (4) Add one comparison to an existing debate protocol.

---

### Section 7: Discussion (816 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 3/5 | [Mialon et al., 2023] and [Yao et al., 2023] cited but not formally referenced. [Zheng et al., 2023] repeated from S5. |
| 2. Logic | 5/5 | Three-response structure for CoT question is strong. Limitations are honest and comprehensive. |
| 3. Novelty | 4/5 | "Governance as cognitive equaliser" implication is novel and well-argued. |
| 4. Intent | 5/5 | Directly addresses the ultimatum's hard gates. |
| 5. Venue | 4/5 | Good Discussion for Arxiv. Could be slightly more concise. |
| 6. Editorial | 3/5 | One em-dash in prose: "experimentally, only L2" (S7.2, L2 capture limitation paragraph). Must fix. |
| **TOTAL** | **24/30** | **REVISE** |

> **Actions**: (1) Fix em-dash: "experimentally, only L2". (2) Ensure all cited references have entries.

---

### Section 8: Conclusion (390 words)

| Check | Score | Issues |
|-------|:-----:|--------|
| 1. Citations | 3/5 | [Schick et al., 2023] cited. No other new citations. |
| 2. Logic | 5/5 | Clean summary. Three future directions are focused. |
| 3. Novelty | 4/5 | Appropriate. No overclaiming. |
| 4. Intent | 5/5 | Honest closing: "we are candid about what this paper does not show." |
| 5. Venue | 5/5 | Good length for Arxiv conclusion. |
| 6. Editorial | 5/5 | Clean. No em-dashes. No passive voice issues. |
| **TOTAL** | **27/30** | **PASS** |

---

### Paper-Section Audit Summary

| Section | Score | Verdict |
|---------|:-----:|:-------:|
| S1 Introduction | 26/30 | **PASS** |
| S2 Background | 26/30 | **PASS** |
| S3 Framework | 25/30 | **PASS** |
| S4 Lifecycle | 24/30 | **REVISE** |
| S5 Experiments | 27/30 | **PASS** |
| S6 Case Study | 22/30 | **REVISE** |
| S7 Discussion | 24/30 | **REVISE** |
| S8 Conclusion | 27/30 | **PASS** |
| **PAPER TOTAL** | **201/240** | **83.8%** |

---

## Part B: Readability Audit (25 Dimensions)

> Evaluator identity: expert editorial evaluator, calibrated scoring (8 = strong, 9 = excellent, 10 = exceptional).

**Word count**: 7,416 words | **Overall**: 7.8/10

| # | Dimension | Score | Note |
|---|-----------|:-----:|------|
| 1 | Clarity | 8 | Clean academic prose. Complex ideas explained without re-reading. |
| 2 | Flow | 8 | Sections connect logically. S3→S4 transition could be smoother. |
| 3 | Hook strength | 9 | S1 opens with ToT catastrophic failure (1.00/3.00). Immediate intellectual tension. |
| 4 | Vulnerability | 7 | Honest about CoT robustness contradicting the framework. S7 "candid" closer helps. |
| 5 | Metaphor coherence | 7 | "Safety net" and "cognitive equaliser" land well. No overextension. |
| 6 | Jargon | 7 | IoT, CoT, ToT, GoT defined. "Fidelity function φ" assumes math literacy (appropriate for Arxiv). |
| 7 | Evidence weight | 9 | 705 scored results. Every claim backed by data or algorithm. |
| 8 | Specificity | 9 | Tables with exact numbers. Per-model, per-topology breakdowns. No vague claims. |
| 9 | Precision | 8 | Tight prose. Few redundancies. S4 repeats the type-signature argument from S1. |
| 10 | Emotional arc | 6 | Academic paper, limited emotional range. S6 case study adds narrative warmth. |
| 11 | Actionability | 8 | Reader knows: use CoT as default, add IoT triple for uplift, use governance for safety net. |
| 12 | Economy | 7 | 7,416 words for 8 sections. Efficient. S4 (1,258w) could be tighter. |
| 13 | Voice consistency | 9 | Consistent academic voice throughout. No tone shifts. |
| 14 | Authority | 8 | 705 empirical results establish credibility. Case study adds practitioner authority. |
| 15 | Audience calibration | 8 | Pitched correctly for CS.AI/CL researchers. Accessible to ML practitioners. |
| 16 | Structure | 9 | 8 sections in logical order. Framework → Lifecycle → Evidence → Case Study → Discussion. |
| 17 | Opening punch | 9 | "ToT on interconnected tasks produced 1.00 out of 3.00" is immediately compelling. |
| 18 | Closing resonance | 7 | Adequate but not memorable. "Ship it" energy from the ultimatum doesn't translate to academic closing. |
| 19 | Intellectual honesty | 9 | Model exclusion explained. CoT robustness acknowledged. LLM-as-judge limitations stated. |
| 20 | Progressive disclosure | 8 | Complexity increases naturally: triple → algorithms → experiments → implications. |
| 21 | Shareability | 7 | "Governance as cognitive equaliser" is quotable. "Safety net" is a good mental model. |
| 22 | Memorability | 8 | Finding: "weaker models benefit 2-3x more" is sticky. Confusion Matrix visual is strong. |
| 23 | Trust-building | 8 | Earns trust by leading with data, then qualifying with limitations. |
| 24 | Uniqueness | 8 | No existing paper connects intent governance to reasoning topology with empirical data. |
| 25 | **Overall** | **7.8** | Strong first draft. Needs citation assembly, S6 jargon cleanup, and em-dash fixes. |

### Top 3 Strengths
1. **Evidence weight (9)**: 705 scored results across 7 models. Rare for a framework paper to have this much data.
2. **Hook strength / Opening punch (9)**: Leading with the catastrophic ToT failure is immediately compelling.
3. **Intellectual honesty (9)**: Acknowledges CoT robustness, model exclusions, LLM-as-judge limitations without defensiveness.

### Top 3 Opportunities
1. **S6 Case Study citations (2/5)**: Must add multi-agent debate literature and remove SYNTHAI jargon ("LOON", "NOOL").
2. **references.bib assembly**: No formal reference list exists. ~25 citations need entries.
3. **Em-dash cleanup**: 13 instances in pseudocode blocks + 2 in prose. Replace with colons.

### Fletch Filter

| Flag | Location | Detected Pattern | Fix |
|------|----------|-----------------|-----|
|: |: |: |: |

✅ **Fletch Filter: Clean.** No AI writing anti-patterns detected.

---

## Part C: Critical Issues (Must Fix Before Submission)

| # | Issue | Section | Priority | Effort |
|---|-------|---------|:--------:|:------:|
| 1 | **No references.bib**: ~25 citations in text, no formal reference entries | All | 🔴 | 2h |
| 2 | **S6 SYNTHAI jargon**: "LOON (Looking Outward, Opening Nool)" breaks stealth rule | S6 | 🔴 | 10min |
| 3 | **S6 missing citations**: No multi-agent debate references | S6 | 🔴 | 30min |
| 4 | **Em-dashes in pseudocode**: 13 instances of "Step N , " | S3, S4 | 🟡 | 10min |
| 5 | **Em-dash in prose**: "experimentally, only L2" | S7 | 🟡 | 1min |
| 6 | **Reproducibility**: Missing temperature, seeds, prompt templates | S5 | 🟡 | 30min |
| 7 | **S4 repeated claim**: Type-signature argument appears in both S1 and S4 | S4 | 🟡 | 5min |
| 8 | **No abstract**: Paper has no abstract | S0 | 🔴 | 15min |
| 9 | **No lifecycle figure**: Referenced in outline but not produced | All | 🟡 | 1h |
| 10 | **Table 7 em-dash**: ", " for baseline delta | S5 | 🟡 | 1min |

### Verdict

| Status | Action |
|--------|--------|
| **REVISE** | Fix the 10 issues above (estimated 4.5h). Then paper is submission-ready. |

**Paper is 83.8% passing the section audit and 7.8/10 on readability. Strong first draft. The bones are solid; the fixes are surface-level and citation-mechanical, not structural.**

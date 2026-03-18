# நூல் / NOOL — Intent of Thought (IoT) Paper

> *The Reasoning Thread: a record of INTENT (why), ABSTRACTION (what type), and CHAIN (how).*

---

## நோக்கம் / Intent (Soul: WHY)

### The Problem

1. **Step-level intent exists, topology-level intent governance does not**: SWI (Yin et al., 2025) adds `<INTENT>` tags before individual reasoning steps. ICoT (Zhang et al., 2024) adds intention abstraction for code generation. ARR (Qi et al., 2024) adds intent analysis before retrieval. But *none* propose that intent should govern WHICH reasoning topology (chain, tree, graph, hybrid) to deploy.
2. **Topology selection is ad-hoc**: When practitioners choose between CoT, ToT, GoT, or other reasoning structures, the choice is made by the researcher/engineer, not by a formal purpose-driven mechanism. Besta et al. (2025) surveys 14+ topologies but offers no intent-based selection framework.
3. **Reasoning drift is a validated pathology**: LLMs and human deliberators routinely lose track of their original intent mid-reasoning, producing technically valid but purpose-misaligned outputs. The alignment literature (InstructGPT, DPO) and the reasoning evaluation literature (Reflexion, IDS) confirm this is a real failure mode.
4. **No formal topology-governance layer exists**: BDI governs agent ACTION. Goal-conditioned RL governs policy TRAINING. System prompts provide instruction STEERING. None of these govern reasoning TOPOLOGY selection based on stated purpose.

### The Purpose

A paper that:
- **Names and formalises** Intent of Thought (IoT) as a pre-reasoning governance layer for topology selection
- **Differentiates precisely** from step-level intent (SWI), domain-specific intent (ICoT), retrieval-stage intent (ARR), agent-action intent (BDI), and reward-signal intent (goal-conditioned RL)
- **Provides a testable framework**: IoT as a 3-component checkpoint (Purpose, Anti-Purpose, Success Signal) that governs which reasoning topology to deploy
- **Proposes a Topology Selection Benchmark (TSB)**: problems paired with intent specifications and expert-labelled optimal topologies
- **Targets Arxiv CS.AI + CL cross-list**: this IS a reasoning architecture contribution
- **Uses neutral framing**: no proprietary branding (stealth mode)

### What We're Avoiding

| Anti-Pattern | Why | How We Prevent It |
|--------------|-----|-------------------|
| **"Intent is missing" claim** | Falsified by SWI, ICoT, ARR | Frame as "topology-level intent governance is missing" (narrower, defensible) |
| **Ignoring BDI lineage** | 40 years of intention formalism | Cite Cohen & Levesque, Rao & Georgeff, position IoT as BDI-for-reasoning-topologies |
| **Ignoring SWI** | Most direct prior art (INLG 2025) | Head-to-head comparison: step-level vs topology-level intent |
| **Overclaiming** | "We invented intentional reasoning" | Frame as formalising what experts do implicitly, at the topology level |
| **No evaluation** | Arxiv standards demand experiments | Design Topology Selection Benchmark + drift detection experiments |
| **Conflating IoT with NOOL** | IoT is one layer, NOOL is the 3-layer stack | Paper focuses solely on IoT, NOOL paper follows as Paper 2 |
| **Goodhart vulnerability** | Success Signals can be gamed | Acknowledge reward misspecification risk, propose multi-metric evaluation |
| **Proprietary branding** | Stealth mode | Use "we propose" / "the authors", no branded terminology |

---

## வடிவம் / Abstraction (Mind: WHAT TYPE)

### Problem Type

**DESIGN**: How should a formal intent-governance layer for reasoning topology selection be structured, differentiated from prior art, and empirically validated?

### Key Dimensions

1. **Prior Art Differentiation Matrix**: Map the landscape of intent-in-reasoning work:
   - Step-level: SWI (per-step `<INTENT>` tags)
   - Domain-level: ICoT (code-generation intention abstraction)
   - Retrieval-level: ARR (pre-retrieval intent analysis)
   - Agent-level: BDI (action commitment governance)
   - Training-level: RLHF/DPO (reward-based alignment)
   - **Gap**: Topology-level governance (NONE)
2. **IoT Framework**: 3-component topology-governance structure:
   - **Purpose**: WHY are we reasoning? What outcome do we seek?
   - **Anti-Purpose**: What would make this reasoning worthless? What must we avoid?
   - **Success Signal**: How will we know the reasoning achieved its purpose?
3. **Topology Selection Mechanism**: Intent specification → topology recommendation (chain for sequential, tree for parallel exploration, graph for interconnected reasoning, hybrid for multi-phase)
4. **Intent Drift Detection**: Ongoing comparison of reasoning trajectory against stated purpose, with correction protocol
5. **Topology Selection Benchmark (TSB)**: Problems paired with intent specifications, expert-labelled optimal topologies, and drift measurement

### Key Relations

- Prior Art Differentiation **ENABLES** novelty claim (topology-level gap is defensible)
- SWI comparison **REQUIRES** head-to-head benchmarking (step vs topology)
- BDI positioning **ENABLES** philosophical depth (40 years of formal semantics)
- TSB benchmark **ENABLES** empirical validation (makes contribution testable)
- IoT paper (Paper 1) **ENABLES** NOOL paper (Paper 2: full three-layer stack)
- Stealth mode **CONSTRAINS** framing (no proprietary references)

---

## சங்கிலி / Chain (Body: HOW)

### Execution Path

| Phase | Activity | Priority | Status |
|-------|----------|----------|--------|
| 0. Capture | External research + /steal protocol | P0 | ✅ Complete |
| 1. Prior Art Matrix | Build SWI/ICoT/ARR/BDI/RL differentiation table | P0 | ⬜ |
| 2. IoT Formalisation | Define 3-component framework with notation | P0 | ⬜ |
| 3. Topology Selection Mechanism | Map intent types → topology recommendations | P0 | ⬜ |
| 4. TSB Design | Create benchmark: problems + intents + optimal topologies | P1 | ⬜ |
| 5. Experiments | IoT+{CoT,ToT,GoT} vs {CoT,ToT,GoT} alone on alignment-sensitive tasks | P1 | ⬜ |
| 6. Drift Measurement | Operationalise Intent Drift Score (IDS) | P1 | ⬜ |
| 7. Paper Drafting | Arxiv-format paper (stealth framing) | P1 | ⬜ |
| 8. Submission | Submit to Arxiv (CS.AI + CL cross-list) | P2 | ⬜ |

### Success Criteria

- [ ] Prior art matrix clearly differentiates IoT from SWI, ICoT, ARR, BDI, RLHF
- [ ] IoT framework formally defined with notation (analogous to CoT's notation)
- [ ] Topology Selection Benchmark produces measurable, reproducible results
- [ ] Experiments show intent-governed topology selection outperforms fixed topology
- [ ] Intent Drift Score is operationalised and validated
- [ ] Paper uses neutral framing throughout (stealth verified)
- [ ] Arxiv submission accepted (preprint available)
- [ ] NOOL paper (Paper 2) can cite this paper as foundational

### Revision Triggers

- A paper formalising "intent-governed topology selection" appears before submission → accelerate timeline
- SWI team extends to topology-level → differentiate on Anti-Purpose + drift detection
- Experiments show no measurable difference → pivot to theoretical contribution (formalism + taxonomy)
- BDI community subsumes the contribution → frame as "BDI adapted for LLM reasoning topologies"

---

## Evolution History

| Version | Date | Layer Changed | What Changed |
|---------|------|---------------|--------------|
| v0.1 | 2026-02-27 | All | Initial NOOL from SPAR #30 verdict and AoT research |
| v0.2 | 2026-03-02 | All | **Major pivot**: thesis reframed from "intent is missing" to "topology-governance gap". Incorporates 6 external reports (4 Perplexity + 2 ChatGPT), 2 SPAR deep ultra verdicts (naming, go/no-go), and /steal research (774-line research.md, 24 signals). Stealth mode flag added. |

---

> *நூல் (nool): the thread that connects, the text that records, the classic that endures.*

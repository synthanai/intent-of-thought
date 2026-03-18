# Research Brief: Section 1 — Introduction

```yaml
thesis: "30+ X-of-Thought reasoning topologies optimise HOW to reason,
  but none provide a formal mechanism for selecting WHICH topology
  based on the PURPOSE of the reasoning task. We call this the
  topology-governance gap and propose Intent of Thought (IoT)
  to fill it."

data_points:
  - point: "30+ XoT papers published since CoT (2022)"
    source: "Perplexity-1 survey, Besta et al. (2025)"
  - point: "Besta et al. (2025) surveys 14+ reasoning topologies but excludes intent governance"
    source: "Perplexity-1, Perplexity-2"
  - point: "SWI (Yin et al. 2025) adds step-level intent, outperforms CoT"
    source: "Perplexity-3, ChatGPT-1"
  - point: "ICoT (Zhang et al. 2024) adds domain-level intent for code"
    source: "Perplexity-3"
  - point: "ARR (Qi et al. 2024) adds retrieval-stage intent analysis"
    source: "Perplexity-3"
  - point: "None propose intent should govern topology SELECTION"
    source: "Signals O2 (gap confirmation)"
  - point: "Reasoning drift is documented (InstructGPT, Reflexion)"
    source: "Research.md Section C, Perplexity-3"

case_studies: []

quotes:
  - text: "Intent is meta-thought/planning that guides analysis and reasoning"
    author: "Yin et al."
    year: 2025

gap: "Step-level intent (SWI), domain-level intent (ICoT), and
  retrieval-level intent (ARR) exist. Topology-level intent
  governance does not. This paper fills that gap."
```

### Writing Notes
- Open with the XoT explosion (eye-catching stat: 30+ papers in 3 years)
- Introduce the gap via a progression: CoT fixed chain → ToT added branching → GoT added graphs → but WHO or WHAT decides which structure to use?
- Three-bullet contribution statement (C1: gap analysis, C2: framework, C3: case studies)
- Stealth: no branding, use "we propose"
- ~1.5 pages, ~500-600 words

# Research Brief: Section 2 — Background and Related Work

```yaml
thesis: "Intent has been applied to AI reasoning at five distinct
  levels (step, domain, retrieval, agent-action, training), but
  never at the topology-governance level. A 6-level differentiation
  matrix makes this gap explicit."

data_points:
  - point: "CoT (Wei et al. 2022): linear chain, step-by-step, most-cited XoT"
    source: "Perplexity-1"
  - point: "ToT (Yao et al. 2023): tree search with BFS/DFS + state evaluation"
    source: "Perplexity-1"
  - point: "GoT (Besta et al. 2024): graph-structured reasoning with refinement"
    source: "Perplexity-1"
  - point: "AoT (Hong et al. 2024): multi-level abstraction within steps, EMNLP"
    source: "Perplexity-1, AoT research.md"
  - point: "SWI adds <INTENT> before steps, outperforms CoT on benchmarks"
    source: "Perplexity-3, ChatGPT-1"
  - point: "ICoT: specification-and-idea intention abstraction for code"
    source: "Perplexity-3"
  - point: "ARR: analyzes question intent before retrieval-reasoning"
    source: "Perplexity-3"
  - point: "BDI: 40 years of formal intention semantics (Bratman, Cohen & Levesque, Rao & Georgeff)"
    source: "ChatGPT-2 (BDI deep dive)"
  - point: "Cohen & Levesque (1990): intention is choice with commitment"
    source: "ChatGPT-2"
  - point: "Goal-conditioned RL: explicit goal variable, reward conditioning"
    source: "ChatGPT-2, Perplexity-3"
  - point: "RLHF/DPO: aligning model behaviour with user intent at training level"
    source: "Perplexity-3"
  - point: "Latent intent (Tutunov et al. 2024): intent as latent variable behind CoT"
    source: "Perplexity-3"
  - point: "Iteration of Thought (Radha et al. 2024): abbreviation collision, different concept"
    source: "Signals O1"
  - point: "OpenAI CoT monitoring: intent visible in traces but fragile under optimisation"
    source: "ChatGPT-1"

case_studies: []

quotes:
  - text: "Intention is choice with commitment"
    author: "Cohen & Levesque"
    year: 1990
  - text: "True intentions and context serve as latent variables behind CoT"
    author: "Tutunov et al."
    year: 2024

gap: "The differentiation matrix establishes that topology-level
  governance is the only level without existing work."
```

### Writing Notes
- 2.1: XoT survey (0.5 pages): CoT, ToT, GoT, AoT, brief others
- 2.2: Intent in reasoning (0.5 pages): SWI, ICoT, ARR, latent intent
- 2.3: Intent in agents/alignment (0.5 pages): BDI, goal-RL, RLHF
- 2.4: Differentiation matrix TABLE (0.5 pages): the centrepiece
- Add footnote disambiguating IoT from Iteration of Thought and Internet of Things
- ~2 pages, ~800-900 words

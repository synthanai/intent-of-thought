# Research Brief: Section 4: Preliminary Evaluation

```yaml
thesis: "Three worked case studies demonstrate that IoT's purpose
  specification correctly selects the optimal reasoning topology,
  while ad-hoc selection leads to suboptimal or wasteful reasoning."

data_points:
  - point: "No existing benchmark measures topology-selection quality"
    source: "Signals O5"
  - point: "ToT excels at Game of 24 (parallel exploration, state evaluation)"
    source: "Yao et al. (2023), Perplexity-1"
  - point: "CoT excels at linear derivation (GSM8K, arithmetic)"
    source: "Wei et al. (2022), Perplexity-1"
  - point: "GoT excels at interconnected problems (refinement, merging)"
    source: "Besta et al. (2024), Perplexity-1"
  - point: "ToT wastes computation on single-solution problems"
    source: "Perplexity-2 (comparison data)"
  - point: "CoT misses alternatives on multi-path problems"
    source: "Yao et al. (2023), ToT paper"

case_studies:
  - name: "Case 1: Sequential derivation"
    relevance: "IoT selects CoT (linear dependency); ToT would over-explore"
  - name: "Case 2: Exploratory problem"
    relevance: "IoT selects ToT (parallel paths); CoT would fixate on first path"
  - name: "Case 3: Interconnected analysis"
    relevance: "IoT selects GoT (non-linear relations); CoT would linearise"

quotes: []

gap: "No prior work demonstrates purpose-driven topology selection
  on concrete problems. These case studies provide the first
  illustrative evidence."
```

### Writing Notes
- 4.1: Case study design (selection criteria, evaluation method) (~0.25 pages)
- 4.2-4.4: One case per subsection, each following the pattern:
  - Problem description
  - IoT specification: P, P_bar, S
  - Framework recommendation: selected topology + rationale
  - Contrast: what ad-hoc selection would produce
- Use concrete, reproducible problems (arithmetic, creative writing, stakeholder analysis)
- Acknowledge limitation: illustrative, not statistical
- ~1.5 pages, ~600-700 words

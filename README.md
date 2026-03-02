# Intent of Thought (IoT)

> A Pre-Reasoning Governance Layer for Topology Selection in LLM Reasoning

[![Paper](https://img.shields.io/badge/Paper-Arxiv-red)](https://arxiv.org/abs/XXXX.XXXXX)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## What is IoT?

When an LLM reasons, it uses a *topology*: Chain-of-Thought (linear), Tree-of-Thought (branching), Graph-of-Thoughts (networked), or others. But **which topology should it use for a given task?**

Current practice: intuition, heuristics, or hardcoded defaults.

**Intent of Thought** proposes a better way: before reasoning begins, state **why** you're reasoning, **what** would make it worthless, and **how** you'll know you succeeded. These three primitives govern which topology gets deployed.

```
IoT = (Purpose, Anti-Purpose, Success Signal)
```

| Primitive | Question | Example |
|-----------|----------|---------|
| **Purpose** | WHY are we reasoning? | "Map causal relationships including feedback loops" |
| **Anti-Purpose** | What must we AVOID? | "Treating factors as independent when they interact" |
| **Success Signal** | HOW will we know we succeeded? | "At least 4 factors with bidirectional dependencies" |

## How It Works

**Algorithm 1: Topology Selection**
```
Input:  IoT specification, problem context
Output: Ranked list of recommended topologies

1. Extract the dominant reasoning requirement from Purpose
2. Match to topology using the selection table
3. Apply Anti-Purpose constraints (demote violating topologies)
4. Output ranked list, most aligned first
```

**Selection Table:**

| Purpose Type | Recommended Topology |
|:-------------|:--------------------|
| Sequential derivation | Chain-of-Thought |
| Parallel exploration | Tree-of-Thought |
| Interconnected analysis | Graph-of-Thoughts |
| Hierarchical classification | Abstraction-of-Thought |
| Multi-phase complex | Hybrid |

**Algorithm 2: Intent Drift Detection**
```
During reasoning, continuously check:
- Is reasoning still aligned with Purpose?
- Has it entered Anti-Purpose territory?
- Is the Success Signal satisfied?

If drift detected: re-evaluate topology.
If Anti-Purpose violated: immediate correction.
If Success Signal met: terminate.
```

## Quick Start

```python
from iot import IntentOfThought, TopologySelector

# Define your intent
iot = IntentOfThought(
    purpose="Map causal relationships between hospital readmission factors",
    anti_purpose="Treating factors as independent when they interact",
    success_signal="Relationship map with bidirectional dependencies and feedback loops"
)

# Select topology
selector = TopologySelector()
recommendation = selector.select(iot, context="systems analysis")
print(recommendation)
# => TopologyRecommendation(primary='GoT', fallback='ToT', rationale='...')
```

## Repository Structure

```
intent-of-thought/
├── README.md                 # This file
├── LICENSE                   # Apache 2.0
├── paper/
│   ├── intent_of_thought.md  # Full paper (readable)
│   └── references.bib        # Bibliography
├── iot/
│   ├── __init__.py
│   ├── specification.py      # IoT triple: Purpose, Anti-Purpose, Success Signal
│   ├── selector.py           # Algorithm 1: Topology Selection
│   └── drift.py              # Algorithm 2: Intent Drift Detection
└── examples/
    ├── case1_sequential.py   # Mathematical proof (IoT -> CoT)
    ├── case2_parallel.py     # UI design challenge (IoT -> ToT)
    └── case3_interconnected.py # Hospital readmission (IoT -> GoT)
```

## Citation

If you use Intent of Thought in your research, please cite:

```bibtex
@article{mohamedkani2026intent,
  title={Intent of Thought: A Pre-Reasoning Governance Layer for
         Topology Selection in LLM Reasoning},
  author={Mohamed Kani, Naveen Riaz},
  journal={arXiv preprint},
  year={2026}
}
```

## Author

**Naveen Riaz Mohamed Kani**
ORCID: [0009-0003-9173-2425](https://orcid.org/0009-0003-9173-2425)

## License

Apache 2.0. See [LICENSE](LICENSE) for details.

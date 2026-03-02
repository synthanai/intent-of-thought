# Intent of Thought (IoT)

> A Pre-Reasoning Governance Layer for Topology Selection in LLM Reasoning

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18836659.svg)](https://doi.org/10.5281/zenodo.18836659)
[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/intent_of_thought.pdf)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

---

## The Problem

LLMs can reason using many structures: chains, trees, graphs, and more. But **how do you pick the right one?**

Current practice relies on researcher intuition, prompt heuristics, or hardcoded defaults. No existing framework connects the *purpose* of a reasoning task to the *selection* of a reasoning structure.

<p align="center">
  <img src="paper/figure3_comparison.svg" alt="Without IoT vs With IoT" width="750"/>
</p>

## The Topology-Governance Gap

We identify six distinct levels at which intent operates in reasoning. The first five are addressed by prior work. The sixth, **topology governance**, is the gap this paper fills.

<p align="center">
  <img src="paper/figure2_gap.svg" alt="The Topology-Governance Gap" width="700"/>
</p>

## How IoT Works

IoT adds a **pre-reasoning checkpoint** that governs which topology to deploy, then monitors for **intent drift** during execution.

<p align="center">
  <img src="paper/figure1_architecture.svg" alt="IoT Architecture" width="850"/>
</p>

## The IoT Triple

Every reasoning task gets a three-part checkpoint before topology selection:

```
IoT = (Purpose, Anti-Purpose, Success Signal)
```

| Primitive | Question | What It Prevents |
|-----------|----------|--------------------|
| **Purpose** | WHY are we reasoning? | Aimless computation |
| **Anti-Purpose** | What must we AVOID? | Technically valid but useless output |
| **Success Signal** | HOW will we know? | Reasoning that never terminates |

## Case Studies

Same algorithm, different intents, different topology selections:

<p align="center">
  <img src="paper/figure4_cases.svg" alt="Case Studies" width="800"/>
</p>

| Case | Task | IoT Recommends | Why |
|------|------|:--------------:|-----|
| 1 | Mathematical proof | 📝 **CoT** | Single valid path, each step depends on previous |
| 2 | UI design challenge | 🌳 **ToT** | Must explore 3+ alternatives before committing |
| 3 | Hospital readmission analysis | 🕸️ **GoT** | Feedback loops between staffing, planning, education |

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
result = selector.select(iot, context="systems analysis")

print(result)
# => Recommended: GoT
#    The Purpose involves interconnected factors with feedback
#    loops, requiring a graph structure for refinement and merging.
```

## Repository Structure

```
intent-of-thought/
├── README.md                 # This file
├── LICENSE                   # Apache 2.0
├── paper/
│   ├── intent_of_thought.md  # Full paper (readable)
│   ├── references.bib        # Bibliography (21 entries)
│   ├── figure1_architecture.svg
│   ├── figure2_gap.svg
│   ├── figure3_comparison.svg
│   └── figure4_cases.svg
├── iot/
│   ├── __init__.py
│   ├── specification.py      # IoT triple: Purpose, Anti-Purpose, Success Signal
│   ├── selector.py           # Algorithm 1: Topology Selection
│   └── drift.py              # Algorithm 2: Intent Drift Detection
└── examples/
    ├── case1_sequential.py   # Mathematical proof → CoT
    ├── case2_parallel.py     # UI design → ToT
    └── case3_interconnected.py # Hospital analysis → GoT
```

## Citation

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

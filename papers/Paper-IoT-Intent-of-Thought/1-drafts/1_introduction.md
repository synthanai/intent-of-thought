# Intent of Thought: A Pre-Reasoning Governance Layer for Topology Selection in LLM Reasoning

**Naveen Riaz Mohamed Kani**
ORCID: [0009-0003-9173-2425](https://orcid.org/0009-0003-9173-2425)

## Abstract

The proliferation of reasoning topologies for large language models, from Chain-of-Thought [@wei2022chain] through Tree-of-Thought [@yao2023tree] to Graph-of-Thoughts [@besta2024graph], has created a rich structural landscape for AI reasoning. Yet across this landscape, a critical question remains unaddressed: *which topology should be deployed for a given reasoning task, and why?* While recent work has introduced intent at the step level (SWI; [@yin2025swi]), the domain level (ICoT; [@li2025icot]), and the retrieval stage (ARR; [@yin2025arr]), no existing framework formalises intent as a governance mechanism for topology selection itself. We survey intent-in-reasoning across five distinct levels and identify this topology-governance gap. We then propose *Intent of Thought* (IoT), a three-primitive pre-reasoning checkpoint comprising Purpose, Anti-Purpose, and Success Signal that governs which reasoning structure to deploy. We formalise IoT with a topology selection function and an intent drift detection mechanism, and demonstrate its utility through three illustrative case studies spanning sequential, exploratory, and interconnected reasoning tasks. We conclude by proposing the Topology Selection Benchmark (TSB) as a community resource for evaluating purpose-governed reasoning.

---

## 1. Introduction

Since the publication of Chain-of-Thought prompting [@wei2022chain], the landscape of structured reasoning for large language models (LLMs) has expanded rapidly. More than thirty distinct reasoning topologies have been proposed in under three years, each offering a different structural approach to the problem of multi-step inference. Tree-of-Thought (ToT; [@yao2023tree]) introduced parallel exploration with state evaluation. Graph-of-Thoughts (GoT; [@besta2024graph]) enabled non-linear reasoning with refinement loops. Abstraction-of-Thought (AoT; [@hong2024abstraction]) added hierarchical problem classification. Buffer-of-Thought, Skeleton-of-Thought, and numerous other variants have followed, each contributing a new structural primitive to the reasoning toolkit.

This explosion of topologies has created a selection problem. When a practitioner or an automated system encounters a reasoning task, which topology should be deployed? Current practice relies on one of three informal mechanisms: researcher intuition (the paper author selects a topology for their benchmark), prompt heuristics (chain for simple tasks, tree for exploration), or fixed assignment (a single topology is baked into the system regardless of the task). None of these mechanisms are grounded in a formal analysis of the task's *purpose*.

Recent work has begun to address the role of intent in reasoning. Speaking with Intent (SWI; [@yin2025swi]) adds explicit `<INTENT>` tags before individual reasoning steps, demonstrating that step-level intent improves performance. Intention Chain-of-Thought (ICoT; [@li2025icot]) introduces intention abstraction for code generation tasks, combining specification and algorithmic strategy into a two-stage intent-guided pipeline. Analyse-Retrieve-Reason (ARR; [@yin2025arr]) incorporates intent analysis before the retrieval step in question answering, improving retrieval relevance and downstream reasoning. These contributions are valuable, but they operate *within* a fixed topology. SWI improves the quality of individual chain steps; it does not determine whether a chain, tree, or graph should have been selected in the first place.

We call this the *topology-governance gap*: the absence of a formal mechanism that connects the *purpose* of a reasoning task to the *selection* of a reasoning structure. This gap is distinct from the well-studied intent constructs in agent theory (BDI architectures govern agent *actions*, not reasoning *topologies*; [@cohen1990intention; @rao1995bdi]) and alignment research (RLHF governs model *training*, not per-task topology selection; [@ouyang2022instructgpt]).

In this paper, we make three contributions:

1. **Gap Analysis.** We survey intent-in-reasoning across five levels (step, domain, retrieval, agent-action, and training) and identify topology-governance as the missing sixth level (Section 2).

2. **Framework.** We propose Intent of Thought (IoT), a three-primitive pre-reasoning checkpoint comprising Purpose, Anti-Purpose, and Success Signal, with a topology selection algorithm and an intent drift detection protocol (Section 3).

3. **Illustrative Evaluation.** We demonstrate IoT on three case studies where purpose-governed topology selection outperforms ad-hoc selection across sequential, exploratory, and interconnected reasoning tasks (Section 4).

We note that the abbreviation "IoT" has been used for "Internet of Things" and for "Iteration of Thought" [@radha2024iteration], an iterative prompting method. Our use refers specifically to *Intent* of Thought, and context disambiguates throughout.[^1]

[^1]: Iteration of Thought [@radha2024iteration] proposes iterative inner dialogue loops within a fixed chain topology. Intent of Thought addresses a different problem: selecting *which* topology to use based on stated purpose.

The remainder of this paper is organised as follows. Section 2 surveys reasoning topologies and intent-in-reasoning at five levels, culminating in a differentiation matrix that reveals the topology-governance gap. Section 3 presents the IoT framework with formal notation. Section 4 demonstrates IoT through three illustrative case studies. Section 5 discusses limitations and proposes the Topology Selection Benchmark, and Section 6 concludes with directions for future work.

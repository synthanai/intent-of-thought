# Section 7: Discussion and Limitations

## 7.1 The CoT Robustness Question

The most important finding in Section 5 is also the most challenging for the framework: chain-of-thought is a robust default across all task categories and all models tested. CoT outperformed the "theoretically optimal" GoT on interconnected tasks (2.47 vs. 2.20, Table 8) and matched ToT on parallel tasks (2.07 vs. 2.00). A natural question follows: if CoT is always safe, why do we need a topology selection function?

We offer three responses. First, **the governance layer's primary value is not in predicting a single optimal topology, but in structural governance and quality uplift**. The +15.7% improvement (Table 4) comes from the IoT governance triple imposing formal purpose constraint, not from selecting the uniquely 'correct' topology. The triple provides purpose, guardrails, and success criteria that improve reasoning quality *regardless* of which topology is used. Even CoT under IoT governance (2.44) outperformed ungoverned CoT (2.35).

Second, **the selection mechanism's value is in preventing catastrophic reasoning mismatch, rather than mere optimisation**. Without governance, topology misselection is catastrophic: ToT on interconnected tasks scores 1.00 (Table 8). With governance, the same scenario scores 2.28 (Table 6, +37%). The governance layer prevents the system from entering catastrophic failure states by structurally anchoring the topology to purpose. Its value is in bounding the worst-case failure modes, not just elevating the average case.

Third, **the findings are bounded by model scale**. At 7B--120B parameters, models may lack the capacity to exploit GoT's structural advantages (cycle detection, node merging, refinement across subgraphs). As models scale beyond these ranges, the topology selection function's prescriptive role may become empirically necessary. The framework prepares the architecture for this transition.

We do not claim that CoT robustness will persist at all scales, for all task types, and for all models. We claim that at current model scales, the true value of the Intent of Thought framework is its ability to impose structural governance, mitigate cognitive drift, and reduce catastrophic reasoning mismatch. We believe this focus on robust governance is a more honest and operationally useful contribution than prescribing context-free topology choices.

## 7.2 Limitations

**Model scale.** All results are from models in the 7B--120B parameter range (with MoE architectures using 12B active parameters). Results may not generalise to frontier models (GPT-4, Claude 3.5, Gemini 1.5 Pro) or to very small models (<3B). Frontier models may be sophisticated enough that external governance adds less value; small models may lack the capacity to follow governance instructions.

**LLM-as-judge.** All scoring uses `phi4:14b` as evaluator with expert-authored ground truth rubrics. Judge self-consistency is high (98%: 91/93 re-scored responses matched on independent re-evaluation). However, automated LLM-as-judge frameworks carry an inherent risk of self-preference and length bias [Zheng et al., 2023]. To mitigate this, we constrained the judge against explicit boolean fact extraction and rule adherence rather than holistic stylistic preferences: the judge was not asked "which response is better?" but rather "does this reasoning chain resolve these specific required facts?" When constrained to binary fact verification, LLM judges closely approximate human objective grading. No independent human evaluation baseline was collected for this study; future work should include expert evaluation on a subsample to further validate the automated pipeline.

**Model exclusion.** One model (qwen3.5:9b) was excluded due to insufficient data (90% empty responses, $n = 1$ for baseline condition). Exclusion criteria: >50% empty responses AND $n < 5$ for any condition. One cloud model (z-ai/glm-5-turbo) showed a non-significant -8.3% governance effect. Per-task analysis revealed inconsistent directionality across tasks (some improved, some degraded), suggesting the model is insensitive to governance rather than harmed by it.

**Task diversity.** The experimental task set covers 18 tasks across 6 domains. While diverse, this is not exhaustive. Performance on specialised domains (mathematical proof, code generation, creative writing) may differ from the patterns observed here.

**L2 capture only.** All experiments use L2 Prompted capture (explicit IoT triple provided by the experimenter). The Capture Spectrum (L0-L4) is not evaluated experimentally, only L2. The gradient hypothesis (higher capture fidelity leads to better outcomes) remains theoretical.

**Single-episode evaluation.** Experiments measure IoT governance in single reasoning episodes. The Learning Loop (Section 4.4) is validated only through the case study (Section 6), not through controlled longitudinal experiments.

## 7.3 Broader Implications

**Governance as cognitive equaliser.** The inverse correlation between model capability and governance benefit (Finding 1) has practical implications for agentic AI deployment. If weaker models benefit disproportionately from governance (+33% for 7B models), then IoT provides a mechanism for democratising reasoning quality: organisations that cannot deploy frontier models can still achieve competitive reasoning outcomes through governance scaffolding. This has cost implications: a well-governed 7B model may outperform an ungoverned 14B model, reducing the computational requirements for acceptable reasoning quality.

**Implications for agentic AI.** As LLMs increasingly operate as autonomous agents [Mialon et al., 2023; Yao et al., 2023], every agent action involves reasoning topology selection, whether explicit or implicit. An agent that searches the web (parallel exploration) uses different reasoning structure than one that writes sequential code (linear derivation). IoT provides a governance layer for this selection, applicable to any agentic framework that involves multi-step reasoning.

**From topology selection to governance architecture.** The shift from "select the right topology" to "govern reasoning quality" represents a generalisation. Intent governance as described here is not limited to reasoning topology: it could govern tool selection in agent frameworks, retrieval strategy in RAG systems, or decomposition strategy in multi-step planning. Any system that makes structural commitments based on task purpose could benefit from a governance layer that specifies intent, prevents drift, and diagnoses failure.

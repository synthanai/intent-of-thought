# Section 6: Case Study: SPAR, A Multi-Agent Debate Protocol as Self-Realised IoT

The evidence in Section 5 evaluates IoT governance in controlled, single-episode reasoning tasks. This section presents a longitudinal case study of IoT governance operating in a production system: SPAR (Structured Persona-Argumentation for Reasoning), a multi-agent debate protocol that evolved through five distinct phases over 75 debates spanning twelve months. The SPAR protocol and its implementation are publicly available at https://github.com/synthanai/spar-kit.

Multi-agent debate, where multiple LLMs argue from different perspectives to improve reasoning quality, has shown promise for fact verification [Du et al., 2023], mathematical reasoning [Liang et al., 2024], and complex decision-making [Chan et al., 2024]. The SPAR case study is notable because IoT governance was not imposed retroactively; the protocol *independently* developed IoT-like governance structures, which we later recognised as a self-realised instance of the lifecycle described in Section 4.

## 6.1 Context: The SPAR Protocol

SPAR orchestrates structured debates between 4 to 8 LLM agents, each assigned a distinct persona and argumentative stance, to produce reasoned decisions on complex questions (e.g., technology selection, strategic priorities, publication strategy). Each debate follows a multi-round structure: agents state positions, challenge each other, synthesise tensions, and converge toward a verdict with explicit dissent recording.

The protocol was initially designed as a flat structure: agents debate, a moderator synthesises. No governance layer existed. Over 75 debates, the protocol evolved iteratively, with each modification motivated by observed failure modes.

## 6.2 The Five Phases of Evolution

**Phase 1: Role-based debate (SPAR v1.0 to v2.0, debates 1 to 12).** Each agent was assigned a role (Advocate, Skeptic, Theorist) and a stance. The only governance was the moderator's prompt. Failure mode observed: agents drifted into tangential arguments that were internally coherent but purposeless. There was no mechanism to detect this drift or to specify what the debate should avoid.

*IoT interpretation*: This is L0 capture (zero mode). No intent triple exists. The system infers purpose from context alone. Drift detection is absent. This pattern is consistent with the "naive debate" condition in [Du et al., 2023], where agents debate without structured governance.

**Phase 2: Purpose-driven debate (SPAR v2.1 to v3.0, debates 13 to 28).** After repeated drift, a Purpose statement was added to the debate prompt: "The goal of this debate is [X]." This reduced drift but introduced a new failure mode: debates would satisfy the stated Purpose through superficial consensus, avoiding genuine tension.

*IoT interpretation*: Partial L2 capture. Purpose is explicit, but Anti-Purpose and Success Signal are absent. Without Anti-Purpose, there is no mechanism to prevent purposeless agreement.

**Phase 3: Anti-Purpose and Success Signal (SPAR v3.1 to v5.0, debates 29 to 50).** Two additions solved the superficial consensus problem. First, Anti-Purpose: "This debate must NOT [Y]" (e.g., "must not reach consensus without addressing the strongest counterargument"). Second, Success Signal: explicit criteria for what constitutes a valid debate output (e.g., "must include dissent record, confidence score, and review date").

*IoT interpretation*: Full L2 capture. The complete IoT triple (Purpose, Anti-Purpose, Success Signal) governs each debate. This is the configuration tested in Experiment 1 (Section 5.2), where it produced a 15.7% quality uplift.

**Phase 4: Topology-aware debate (SPAR v5.1 to v6.0, debates 51 to 65).** With the governance triple established, the protocol began adapting its *reasoning structure* based on the debate's purpose. For tradeoff decisions, agents were instructed to follow tree-of-thought (branch and compare). For interconnected analyses, graph-of-thought (map factors and relationships). The topology selection was governed by the IoT triple: the Purpose determined the reasoning structure, the Anti-Purpose constrained it, and the Success Signal validated the output.

*IoT interpretation*: The topology selection function (Algorithm 1) is now operational. Each debate's structure is chosen based on its governance specification, not by default.

**Phase 5: Retrospective judgement and learning (SPAR v6.1 to v7.4, debates 66 to 75).** The protocol added systematic retrospection: after each debate, a structured reflection document (a LOON, or backward-looking reasoning trace) recorded what went well, what failed, and what should change. Failed debates were diagnosed: Was the Purpose wrong (False Capture)? Was the topology mismatched (False Selection)? Did agents drift despite correct setup (False Execution)? These diagnoses fed back into improved debate templates.

*IoT interpretation*: The full lifecycle is operational. Capture > Select > Monitor > Judge > Learn > Capture. The Learning Loop closed naturally over 75 iterations.

## 6.3 Quantitative Evolution

Table 11 summarises the structural progression across SPAR versions.

| Phase | SPAR Version | Debates | IoT Capture Level | Components Present | Failure Mode Addressed |
|:-----:|:------------:|:-------:|:-----------------:|:------------------:|:----------------------:|
| 1 | v1.0 to v2.0 | 1 to 12 | L0 (Zero) | None | (none) |
| 2 | v2.1 to v3.0 | 13 to 28 | Partial L2 | Purpose only | Drift |
| 3 | v3.1 to v5.0 | 29 to 50 | L2 (Prompted) | Purpose, Anti-Purpose, Success Signal | Superficial consensus |
| 4 | v5.1 to v6.0 | 51 to 65 | L2 + Selection | Full triple + topology function | Topology mismatch |
| 5 | v6.1 to v7.4 | 66 to 75 | L2 + Lifecycle | Full lifecycle | Recurrence of known failures |

## 6.4 What the Case Study Demonstrates

This case study provides three forms of evidence that complement the controlled experiments in Section 5:

1. **Organic emergence**: The IoT lifecycle was not designed top-down and applied to SPAR. It emerged bottom-up: each governance component was added in response to an observed failure mode. This suggests the lifecycle addresses real, recurrent needs rather than theoretical constructs.

2. **Longitudinal validation**: The controlled experiments (Section 5) measure IoT governance in single episodes. The SPAR case study demonstrates governance improving *across* episodes through the Learning Loop, validating the closed-loop lifecycle over sustained use.

3. **Anti-Purpose as the critical inflection point**: The transition from Phase 2 (Purpose only) to Phase 3 (full triple) produced the most noticeable qualitative improvement. This corroborates Experiment 5's finding that Anti-Purpose contributes measurably, and suggests the effect may compound over time as Anti-Purpose accumulates institutional knowledge of failure patterns.

The case study does not claim controlled causality: other factors (prompt refinement, model upgrades, user learning) contributed to the protocol's improvement. The claim is structural: the IoT lifecycle accurately describes the governance evolution that occurred, and the protocol's observed failure modes map cleanly onto the three diagnostic categories (False Capture, False Selection, False Execution) defined in Section 4.3. The full SPAR protocol, including debate templates, persona definitions, and governance configurations, is open-source at https://github.com/synthanai/spar-kit.

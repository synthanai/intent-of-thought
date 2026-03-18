# Section 6: Case Study: A Multi-Agent Debate Protocol as Self-Realised IoT

The experimental results in Section 5 evaluate IoT governance in controlled, single-episode reasoning tasks. This section presents a longitudinal case study of IoT governance operating in a production system: a multi-agent debate protocol that evolved through five distinct phases over 75 debates spanning twelve months. Multi-agent debate, where multiple LLMs argue from different perspectives to improve reasoning quality, has shown promise for fact verification [Du et al., 2023], mathematical reasoning [Liang et al., 2023], and complex decision-making [Chan et al., 2024]. The case study is notable because IoT governance was not imposed retroactively; the protocol *independently* developed IoT-like governance structures, which we later recognised as a self-realised instance of the lifecycle described in Section 4. We present the evolution without proprietary attribution, focusing on the structural progression.

## 6.1 Context: The Multi-Agent Debate Protocol

The protocol orchestrates structured debates between 4--8 LLM agents, each assigned a distinct persona and argumentative stance, to produce reasoned decisions on complex questions (e.g., technology selection, strategic priorities, publication strategy). Each debate follows a multi-round structure: agents state positions, challenge each other, synthesise tensions, and converge toward a verdict with explicit dissent recording.

The protocol was initially designed as a flat structure: agents debate, a moderator synthesises. No governance layer existed. Over 75 debates, the protocol evolved iteratively, with each modification motivated by observed failure modes.

## 6.2 The Five Phases of Evolution

**Phase 1: Role-based debate (debates 1--15).** Each agent was assigned a role (Advocate, Skeptic, Theorist) and a stance. The only governance was the moderator's prompt. Failure mode observed: agents drifted into tangential arguments that were internally coherent but purposeless. There was no mechanism to detect this drift or to specify what the debate should avoid.

*IoT interpretation*: This is L0 capture (zero mode). No intent triple exists. The system infers purpose from context alone. Drift detection ($\delta$) is absent. This pattern is consistent with the "naive debate" condition in [Du et al., 2023], where agents debate without structured governance.

**Phase 2: Purpose-driven debate (debates 16--30).** After repeated drift, a Purpose statement was added to the debate prompt: "The goal of this debate is [X]." This reduced drift but introduced a new failure mode: debates would satisfy the stated Purpose through superficial consensus, avoiding genuine tension.

*IoT interpretation*: Partial L2 capture. Purpose ($P$) is explicit, but Anti-Purpose ($\bar{P}$) and Success Signal ($S$) are absent. Without $\bar{P}$, there is no mechanism to prevent purposeless agreement.

**Phase 3: Anti-Purpose and Success Signal (debates 31--50).** Two additions solved the superficial consensus problem. First, Anti-Purpose: "This debate must NOT [Y]" (e.g., "must not reach consensus without addressing the strongest counterargument"). Second, Success Signal: explicit criteria for what constitutes a valid debate output (e.g., "must include dissent record, confidence score, and review date").

*IoT interpretation*: Full L2 capture. The complete IoT triple $(P, \bar{P}, S)$ governs each debate. This is the configuration tested in Exp1 (Section 5.2), where it produced a 15.7% quality uplift.

**Phase 4: Topology-aware debate (debates 51--65).** With the governance triple established, the protocol began adapting its *reasoning structure* based on the debate's purpose. For tradeoff decisions, agents were instructed to follow tree-of-thought (branch and compare). For interconnected analyses, graph-of-thought (map factors and relationships). The topology selection was governed by the IoT triple: the Purpose determined the reasoning structure, the Anti-Purpose constrained it, and the Success Signal validated the output.

*IoT interpretation*: The topology selection function $f(\text{IoT}, \text{context}) \to T^*$ (Algorithm 1) is now operational. Each debate's structure is chosen based on its governance specification, not by default.

**Phase 5: Retrospective judgement and learning (debates 66-75).** The protocol added systematic retrospection: after each debate, a structured reflection document recorded what went well, what failed, and what should change. Failed debates were diagnosed: Was the Purpose wrong (False Capture)? Was the topology mismatched (False Selection)? Did agents drift despite correct setup (False Execution)? These diagnoses fed back into improved debate templates.

*IoT interpretation*: The full lifecycle is operational. Capture $\to$ Select $\to$ Monitor $\to$ Judge $\to$ Learn $\to$ Capture. The Learning Loop closed naturally over 75 iterations.

## 6.3 Quantitative Evolution

Table 10 summarises the structural progression.

| Phase | Debates | IoT Capture Level | Components Present | Failure Mode Addressed |
|:-----:|:-------:|:-----------------:|:------------------:|:----------------------:|
| 1 | 1-15 | L0 (Zero) | None | (none) |
| 2 | 16--30 | Partial L2 | $P$ only | Drift |
| 3 | 31--50 | L2 (Prompted) | $P, \bar{P}, S$ | Superficial consensus |
| 4 | 51--65 | L2 + Selection | $P, \bar{P}, S$ + $f$ | Topology mismatch |
| 5 | 66-75 | L2 + Lifecycle | Full lifecycle | Recurrence of known failures |

## 6.4 What the Case Study Demonstrates

This case study provides three forms of evidence that complement the controlled experiments in Section 5:

1. **Organic emergence**: The IoT lifecycle was not designed top-down and applied to this system. It emerged bottom-up: each governance component was added in response to an observed failure mode. This suggests the lifecycle addresses real, recurrent needs rather than theoretical constructs.

2. **Longitudinal validation**: The controlled experiments (Section 5) measure IoT governance in single episodes. The case study demonstrates governance improving *across* episodes through the Learning Loop, validating the closed-loop lifecycle over sustained use.

3. **Anti-Purpose as the critical inflection point**: The transition from Phase 2 (Purpose only) to Phase 3 (full triple) produced the most noticeable qualitative improvement. This corroborates Exp5's finding that Anti-Purpose contributes measurably, and suggests the effect may compound over time as $\bar{P}$ accumulates institutional knowledge of failure patterns.

The case study does not claim controlled causality: other factors (prompt refinement, model upgrades, user learning) contributed to the protocol's improvement. The claim is structural: the IoT lifecycle accurately describes the governance evolution that occurred, and the protocol's observed failure modes map cleanly onto the three diagnostic categories (False Capture, False Selection, False Execution) defined in Section 4.3.

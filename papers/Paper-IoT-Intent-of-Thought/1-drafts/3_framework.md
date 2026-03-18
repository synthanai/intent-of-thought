## 3. Intent of Thought

We now present Intent of Thought (IoT), a pre-reasoning governance layer that connects the purpose of a reasoning task to the selection of an appropriate topology. IoT comprises three primitives (Section 3.1), a specification format (Section 3.2), a topology selection algorithm (Section 3.3), and an intent drift detection protocol (Section 3.4).

### 3.1 The Three Primitives

IoT specifies the *intent* of a reasoning task through three complementary primitives:

**Purpose ( P ).** The desired outcome of the reasoning process. Purpose answers "WHY are we reasoning?" and specifies the end-state that the agent seeks to achieve. Unlike a task description (which specifies *what* to do), Purpose specifies *why* the reasoning matters and what constitutes a good outcome. For instance, a Purpose might be "identify the optimal investment allocation across three asset classes" rather than "solve this optimisation problem."

**Anti-Purpose ( P-bar ).** The set of outcomes that would render the reasoning worthless. Anti-Purpose answers "what must we AVOID?" and specifies explicit failure conditions, drawing on the BDI tradition of commitment termination [@cohen1990intention]. Anti-Purpose is operationally distinct from constraints: where constraints limit the solution space, Anti-Purpose identifies what would make the entire reasoning episode a waste. For example: "avoid recommending allocations that ignore tax implications" is a constraint, while "reasoning that treats the three asset classes as independent when they are correlated" is an Anti-Purpose.

**Success Signal ( S ).** The criteria by which the agent (or an observer) determines that the reasoning has achieved its Purpose. Success Signal answers "HOW will we know we succeeded?" and provides evaluation criteria that are checkable during and after reasoning. Success Signals may be binary (achieved or not), graded (degree of satisfaction), or multi-dimensional (a set of criteria). For instance: "a ranked allocation with sensitivity analysis showing the impact of correlation assumptions."

These three primitives are complementary. Purpose without Anti-Purpose permits reasoning drift into technically valid but practically useless territory. Purpose without Success Signal provides no mechanism for detecting when reasoning should terminate. Anti-Purpose without Purpose is unconstrained negation. The triad functions as a pre-reasoning checkpoint: before selecting a reasoning topology, the agent must specify all three.

### 3.2 The IoT Specification

We define the IoT specification as a triple:

> **IoT** = (Purpose, Anti-Purpose, Success Signal)

or in shorthand: **IoT = (P, P-bar, S)**.

This triple is the input to the topology selection algorithm described below. It captures the *why* of a reasoning task in a structured form that can be matched against the structural characteristics of available topologies.

### 3.3 Topology Selection Algorithm

The selection algorithm takes the IoT specification and the problem context as input, and produces a ranked list of recommended topologies. The algorithm proceeds in three steps:

**Algorithm 1: Topology Selection**

```
Input:  IoT specification (P, P-bar, S), problem context
Output: Ranked list of recommended topologies

Step 1 — Extract purpose type.
  Analyse the Purpose to identify the dominant reasoning
  requirement: sequential derivation, parallel exploration,
  interconnected analysis, hierarchical classification,
  or multi-phase complex reasoning.

Step 2 — Match purpose type to topology.
  Use Table 2 to identify the topology whose structural
  properties best align with the identified purpose type.

Step 3 — Apply Anti-Purpose constraints.
  Check whether the candidate topology would structurally
  violate the Anti-Purpose. If it does, demote it and
  promote the next candidate.

Output: Ordered list, most aligned topology first.
```

**Table 2: IoT topology selection mapping.**

| Purpose Type | Structural Signal | Recommended Topology | Rationale |
|:-------------|:-----------------|:--------------------|:----------|
| Sequential derivation | Single valid path, step dependencies | CoT | Linear chain; each step builds on the previous |
| Parallel exploration | Multiple viable approaches, uncertain best path | ToT | Branching enables evaluation of alternatives before commitment |
| Interconnected analysis | Non-linear relationships, feedback loops | GoT | Graph structure supports refinement and merging |
| Hierarchical classification | Problem type matters before details | AoT | Abstraction first, then type-specific reasoning |
| Multi-phase complex | Requires multiple reasoning modes | Hybrid | Sequential phases with different structural needs |

The mapping is not deterministic. Purpose determines the general topology class, Anti-Purpose adds constraints (e.g., "avoid premature commitment to a single path" favours ToT over CoT), and Success Signal informs the evaluation mechanism within the selected topology.

### 3.4 Intent Drift Detection

Reasoning drift occurs when a multi-step reasoning process gradually diverges from its stated purpose, producing outputs that are internally coherent but misaligned with the original intent. This phenomenon is well-documented: Reflexion [@shinn2023reflexion] addresses it through episodic feedback signals, and RLHF [@ouyang2022instructgpt] addresses it at the training level. IoT addresses it at the topology-governance level through continuous monitoring.

**Algorithm 2: Intent Drift Detection**

```
Input:  IoT specification (P, P-bar, S), reasoning trace
Output: Continue, correct, switch topology, or terminate

Step 1 — Anchor.
  At the start of reasoning, record the Purpose as the
  reference point for alignment checks.

Step 2 — Monitor.
  At regular intervals during reasoning, compare the
  current direction of reasoning against the stated Purpose.

Step 3 — Check for drift.
  If the reasoning has diverged significantly from Purpose:
    a. Re-read the IoT specification (P, P-bar, S).
    b. Evaluate whether the current topology is still
       appropriate for the stated Purpose.
    c. If topology is mismatched: re-run Algorithm 1
       with updated context.
    d. If topology is appropriate: add a purpose-
       realignment step to the reasoning chain.

Step 4 — Check for Anti-Purpose violation.
  If the reasoning has entered territory explicitly
  identified by Anti-Purpose: trigger immediate correction.

Step 5 — Check for completion.
  If the Success Signal is satisfied: terminate reasoning.
  If the Purpose is believed unachievable: terminate and
  report (following Cohen and Levesque's [-@cohen1990intention]
  termination semantics).
```

This protocol draws on BDI commitment termination but applies it to the reasoning process itself rather than to agent actions. The agent maintains its reasoning commitment until: (a) the Purpose is achieved (Success Signal satisfied), (b) the Purpose is believed unachievable, or (c) background conditions have changed such that the original Purpose is no longer relevant.

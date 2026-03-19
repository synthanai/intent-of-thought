# Section 3: The IoT Framework

This section presents the core IoT governance layer: the intent triple (Section 3.1), the topology selection function (Section 3.2), and the drift detection protocol (Section 3.3). We then discuss the empirical qualification that situates the selection function's value (Section 3.4).

## 3.1 The Intent Triple

IoT specifies the *intent* of a reasoning task through three complementary primitives:

**Purpose ($P$).** The desired outcome of the reasoning process. Purpose answers "why are we reasoning?" and specifies the end-state that the agent seeks to achieve. Unlike a task description (which specifies *what* to do), Purpose specifies *why* the reasoning matters and what constitutes a good outcome. For instance, a Purpose might be "identify the optimal investment allocation across three asset classes" rather than "solve this optimisation problem."

**Anti-Purpose ($\bar{P}$).** The set of outcomes that would render the reasoning worthless. Anti-Purpose answers "what must we avoid?" and specifies explicit failure conditions. Anti-Purpose is operationally distinct from constraints: where constraints limit the solution space, Anti-Purpose identifies what would make the entire reasoning episode a waste. For example: "avoid recommending allocations that ignore tax implications" is a constraint, while "reasoning that treats the three asset classes as independent when they are correlated" is an Anti-Purpose. This distinction draws on the BDI tradition of commitment termination [Cohen and Levesque, 1990], where an agent abandons a commitment not because the solution is infeasible but because the reasoning has become purposeless.

**Success Signal ($S$).** The criteria by which the agent (or an observer) determines that reasoning has achieved its Purpose. Success Signal answers "how will we know we succeeded?" and provides evaluation criteria that are checkable during and after reasoning. Success Signals may be binary (achieved or not), graded (degree of satisfaction), or multi-dimensional (a set of criteria).

These three primitives are complementary and non-redundant:

- Purpose without Anti-Purpose permits reasoning drift into technically valid but practically useless territory.
- Purpose without Success Signal provides no mechanism for detecting when reasoning should terminate.
- Anti-Purpose without Purpose is unconstrained negation: the system knows what to avoid but not what to achieve.

The triad functions as a pre-reasoning checkpoint: before selecting a reasoning topology, the agent must specify all three components.

**Definition 1 (IoT Specification).** The IoT specification is a triple:

$$\text{IoT} = (P, \bar{P}, S)$$

This triple is the input to the topology selection function defined below.

## 3.2 Topology Selection Function

The selection function takes the IoT specification and the problem context as input and produces a ranked list of recommended topologies from the topology space $\mathcal{T} = \{\text{CoT}, \text{ToT}, \text{GoT}, \text{AoT}, \text{Hybrid}\}$.

**Algorithm 1: Topology Selection**

```
Input:  IoT specification (P, P̄, S), problem context C
Output: Ranked list T* ⊆ T

Step 1. Extract purpose type.
  Analyse P to identify the dominant reasoning requirement:
  sequential derivation, parallel exploration, interconnected
  analysis, hierarchical classification, or multi-phase complex.

Step 2. Match purpose type to topology.
  Use Table 2 to identify the topology whose structural
  properties best align with the identified purpose type.

Step 3. Apply Anti-Purpose constraints.
  Check whether the candidate topology would structurally
  violate P̄. If so, demote it and promote the next candidate.

Output: Ordered list, most aligned topology first.
```

**Table 2: IoT topology selection mapping.**

| Purpose Type | Structural Signal | Recommended Topology | Rationale |
|:-------------|:------------------|:---------|:---------------------------------|
| Sequential derivation | Single valid path, step dependencies | CoT | Linear chain; each step builds on the previous |
| Parallel exploration | Multiple viable approaches, uncertain best path | ToT | Branching enables evaluation of alternatives |
| Interconnected analysis | Non-linear relationships, feedback loops | GoT | Graph structure supports refinement and merging |
| Hierarchical classification | Problem type matters before details | AoT | Abstraction first, then type-specific reasoning |
| Multi-phase complex | Requires multiple reasoning modes | Hybrid | Sequential phases with different structural needs |

The mapping is not deterministic. Purpose determines the general topology class, Anti-Purpose adds constraints (e.g., "avoid premature commitment to a single path" favours ToT over CoT), and Success Signal informs the evaluation mechanism within the selected topology.

## 3.3 Intent Drift Detection

Reasoning drift occurs when a multi-step reasoning process gradually diverges from its stated purpose, producing outputs that are internally coherent but misaligned with the original intent. IoT addresses drift at the topology-governance level through continuous monitoring.

**Definition 2 (Drift Detection Function).** The drift detection function $\delta: \text{trace} \times P \to [0,1]$ measures the alignment between the current reasoning trajectory and the stated Purpose. When $\delta$ exceeds a threshold $\theta$, the system triggers corrective action.

**Algorithm 2: Intent Drift Detection**

```
Input:  IoT specification (P, P̄, S), reasoning trace τ
Output: Continue, correct, switch topology, or terminate

Step 1. Anchor. Record P as the reference point.

Step 2. Monitor. At regular intervals, compute δ(τ, P).

Step 3. Drift check. If δ(τ, P) > θ:
  a. Re-read the IoT specification.
  b. Evaluate whether the current topology is still
     appropriate for P.
  c. If topology is mismatched: re-run Algorithm 1 with
     updated context.
  d. If topology is appropriate: add a purpose-realignment
     step to the reasoning chain.

Step 4. Anti-Purpose violation. If τ enters territory
  identified by P̄: trigger immediate correction.

Step 5. Completion. If S is satisfied: terminate.
  If P is believed unachievable: terminate and report.
```

This protocol draws on BDI commitment termination [Cohen and Levesque, 1990]: reasoning persists until the Purpose is achieved, believed unachievable, or superseded by Anti-Purpose violation.

## 3.4 Empirical Qualification

The topology selection mapping in Table 2 was designed prescriptively: "match topology to task type." Our experimental evaluation (Section 5) reveals that this prescription must be qualified.

At current model scales (7B--120B parameters), chain-of-thought (CoT) is empirically robust across all task types, including those Table 2 assigns to GoT or ToT. CoT scored 2.47 on interconnected tasks where GoT scored 2.20 ($n = 131$, Section 5.4). The selection function's empirical value is therefore not in *optimal* topology recommendation but in *failure protection*: preventing the catastrophic quality loss that occurs when the wrong topology is selected without governance (e.g., ToT on interconnected tasks: 1.00/3.00).

This qualification does not invalidate the selection function. It situates its contribution accurately: governance provides a safety net that makes topology misselection survivable, and an uplift mechanism that improves all topologies. As models scale beyond the ranges tested here, the selection function's prescriptive role may become empirically necessary. At current scales, its value is architectural preparedness combined with measurable quality improvement.

# Section X: SPAR as IoT Routing Implementation

> Draft section for IoT Lifecycle paper. Source: SPAR-IoT architectural analysis (2026-03-17)
> Ready for revision and integration into paper structure.

## X.1 SPAR as a Live Implementation of the IoT Lifecycle

The SPAR protocol (Structured Persona-Argumentation for Reasoning) provides a live implementation of the IoT Lifecycle within a multi-agent debate context. SPAR's Three-Layer Reasoning Stack maps directly to the IoT framework:

| IoT Lifecycle Component | SPAR Implementation |
|------------------------|---------------------|
| **IoT Triple Capture** | NOOL statement at SCOPE (Purpose, Anti-Purpose, Success Signal) |
| **Topology Selection** | AoT problem classification → recommended topology (CoT/ToT/GoT) |
| **Drift Monitoring** | Anti-Purpose (P̄) check after each RUMBLE round |
| **Retrospective Judgement** | RAPS review (30-90 day scheduled retrospective) |
| **Learning Loop** | Protocol evolution driven by failure analysis |

## X.2 Capture Spectrum Application

SPAR's NOOL capture operates at L2 (Prompted) of the Capture Spectrum: the protocol asks structured questions to elicit Purpose, Anti-Purpose, and Success Signal explicitly. The fidelity function $\varphi$ is observable: debates with well-specified NOOLs (high $\varphi$) produce higher-confidence verdicts than those with vague NOOLs (low $\varphi$).

| NOOL Fidelity | Topology Governance | Debate Outcome |
|--------------|---------------------|----------------|
| Low (generic P, no P̄, vague S) | Default CoT, no topology awareness | Higher risk of drift, lower confidence |
| High (specific P, concrete P̄, measurable S) | AoT-informed topology selection | Lower drift, higher confidence, auditable |

This confirms the Capture-Topology Confidence Interaction (Section 3.3): low-fidelity capture restricts the system to robust defaults, while high-fidelity capture unlocks specialised topologies.

## X.3 Topology Routing via AoT Problem Classification

SPAR's POPULATE step classifies the problem type (SEQUENCING, TRADEOFF, ROOT_CAUSE, RESOURCE_ALLOCATION, DESIGN, PREDICTION) and recommends a reasoning topology:

| Problem Type | Recommended Topology | Rationale |
|-------------|---------------------|-----------|
| SEQUENCING | CoT | Linear causal chain; order matters |
| TRADEOFF | ToT | Branch and compare alternatives |
| ROOT_CAUSE | GoT | Map factor relationships and feedback loops |
| RESOURCE_ALLOCATION | ToT | Evaluate allocation strategies as branches |
| DESIGN | GoT | Interconnected design dimensions |
| PREDICTION | CoT or ToT | Sequential forecasting or scenario branching |

The routing is advisory, not mandatory: agents may override the recommended topology if their perspective demands a different reasoning approach. This aligns with the governance-proportional response principle (Section 4.4): the IoT Lifecycle governs without constraining.

## X.4 Retrospective Judgement in Practice

SPAR's RAPS (Review and Periodic Scoring) mechanism implements Retrospective Judgement at the protocol level. Each debate schedules a retrospective review at a tier-appropriate interval:

| RAMP Level | Review Interval | Review Depth |
|-----------|----------------|-------------|
| L1-L2 | 90 days | Lite (did verdict hold?) |
| L3 | 60 days | Standard (was the reasoning sound?) |
| L4-L5 | 30 days | Full (would we decide differently with hindsight?) |

When a RAPS review finds that a verdict did not hold, the failure analysis follows the three-mode taxonomy (Section 4.2): False Capture (the NOOL was wrong), False Selection (the topology was wrong), or False Execution (the reasoning drifted despite correct setup).

## X.5 Evidence from 75 Debates

Across 75 SPAR debates (73 scored), the mean confidence was 88.0% (range: 72-96%). Debates with explicit NOOL statements (IoT capture at L2+) scored 3-5 points higher on average than early debates with implicit or absent NOOLs. The introduction of PROBE (mandatory counter-thesis agent) was the single most impactful quality intervention, corresponding to a governance-proportional correction at the reasoning level: when the system detects potential sycophancy drift, it injects structured opposition.

## X.6 Implications for the IoT Lifecycle

SPAR's operational implementation provides several validation points:

1. **L2 Capture is sufficient for structured reasoning**: prompted elicitation of the IoT triple (rather than learned or collaborative capture) is effective for decision-making contexts
2. **Anti-Purpose as drift guard works**: explicit P̄ checking during reasoning prevents the most common failure mode (consensus without rigor)
3. **AoT→topology routing is advisory, not prescriptive**: the routing recommendation improves reasoning quality without constraining agent flexibility
4. **The Learning Loop is reflexive**: SPAR applies the IoT Lifecycle to itself, evolving its protocol through failure-driven iteration

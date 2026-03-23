# Figure 1: The IoT Lifecycle

> **Purpose**: Visual centrepiece of Paper 2. Referenced in Section 1 (Introduction) and throughout.
> **Format**: Mermaid source + LaTeX TikZ description for production.

---

## Mermaid Source (preview rendering)

```mermaid
flowchart LR
  subgraph FORWARD["Forward Governance (Paper 1)"]
    direction LR
    C["🎯 CAPTURE\n(Section 3)\nElicit IoT Triple\n(P, P̄, S)"]
    S["⚙️ SELECT\n(Paper 1)\nf(IoT, context, φ) → T*"]
    M["📡 MONITOR\nδ(trace, P) → [0,1]\nDrift Detection"]
  end

  subgraph BACKWARD["Backward Governance (Paper 2)"]
    direction LR
    J["🔍 JUDGE\n(Section 4)\nReconstruct P_actual\nDiagnose Failure Mode"]
    R["⚖️ RESPOND\nGovernance-\nProportional\nCorrection"]
    L["🧠 LEARN\nUpdate f, φ, δ\nExpand Benchmarks"]
  end

  C --> S --> M
  M -->|"δ > threshold\n(failure detected)"| J
  J --> R --> L
  L -->|"improved\ncapture"| C

  style FORWARD fill:#e8f4e8,stroke:#2d7d2d,stroke-width:2px
  style BACKWARD fill:#fde8e8,stroke:#c0392b,stroke-width:2px
```

## Dual-Diagram: Temporal Symmetry

```mermaid
flowchart TB
  subgraph FWD["CAPTURE (Forward)"]
    direction TB
    F1["Context C"] --> F2["Belief about Intent\np(I|C)"]
    F2 --> F3["IoT Triple\n(P, P̄, S)"]
    F3 --> F4["Topology Selection\nf(IoT, context, φ) → T*"]
  end

  subgraph BWD["JUDGEMENT (Backward)"]
    direction TB
    B1["Terminal Evidence\n(Y₁:T, F)"] --> B2["Knowledge about Intent\np(I|C, Y₁:T, F)"]
    B2 --> B3["Reconstructed Triple\n(P_actual, P̄_actual, S_actual)"]
    B3 --> B4["Failure Diagnosis\nFalse Capture / Selection / Execution"]
  end

  FWD ~~~ BWD

  style FWD fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
  style BWD fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

---

## LaTeX TikZ Description (for production)

The diagram should be rendered as TWO parts:

### Part A: The Lifecycle Loop (horizontal)

Six nodes arranged in an oval/racetrack layout:
- **Top row** (left to right): CAPTURE → SELECT → MONITOR (green shading, "Forward Governance")
- **Bottom row** (right to left): JUDGE → RESPOND → LEARN (red/orange shading, "Backward Governance")
- Arrow from MONITOR down to JUDGE (labelled "δ > threshold")
- Arrow from LEARN back up to CAPTURE (labelled "improved capture")
- Each node shows: name, section reference, key operation

### Part B: Temporal Symmetry Inset (small, bottom-right)

Two columns side by side:
- Left: "CAPTURE (Forward)" with arrow from Context → Belief → IoT Triple → Topology
- Right: "JUDGEMENT (Backward)" with arrow from Evidence → Knowledge → Reconstructed Triple → Diagnosis
- Label between: "Same operator L(I;E), different evidence"
- Blue shading (forward), orange shading (backward)

### Figure Caption

"Figure 1: The IoT Lifecycle. The forward half (Capture → Select → Monitor) constructs and governs reasoning; the backward half (Judge → Respond → Learn) diagnoses failures and feeds corrections back to capture. Together they complete a closed governance loop. Inset: Capture and Judgement are structurally symmetric, both performing intent inference under epistemic asymmetry, with Capture conditioning on belief (pre-reasoning) and Judgement conditioning on observation (post-failure)."

---

## Key Design Decisions

1. **Racetrack, not circle**: emphasises forward/backward distinction
2. **Colour coding**: green (forward, Paper 1 territory), red/orange (backward, Paper 2 contribution)
3. **Section references**: each node links to paper section for reader navigation
4. **Inset**: temporal symmetry is visually compact, not overemphasised (SPAR #33 constraint)
5. **No MAPE-K labels**: MAPE-K is cited in text, not shown in diagram (avoids direct visual comparison)

# Research Brief: Section 3 — Intent of Thought Framework

```yaml
thesis: "IoT is a three-primitive pre-reasoning checkpoint (Purpose,
  Anti-Purpose, Success Signal) with a topology selection function,
  formal notation, and an intent drift detection mechanism."

data_points:
  - point: "IoT := <P, P_bar, S> — three primitives with distinct roles"
    source: "Research.md Section B (definitions)"
  - point: "Topology selection function f(IoT, context) → T* (ordered topology subset)"
    source: "Research.md Section C (theory), outline.md Section 3.3"
  - point: "Intent Drift Score δ: cosine similarity between purpose embedding and step embeddings"
    source: "Signals A7, Research.md Section D"
  - point: "Anti-Purpose is operationally distinct from BDI constraints: 'what would make this reasoning WORTHLESS'"
    source: "Signals C4"
  - point: "Cohen & Levesque's relativised persistent goals provide termination semantics"
    source: "ChatGPT-2 (BDI comparison)"
  - point: "Sequential → CoT, Exploratory → ToT, Interconnected → GoT mapping"
    source: "Outline.md Section 3.3"
  - point: "Correction protocol: if δ > threshold, invoke IoT checkpoint"
    source: "Research.md Section C (theory)"

case_studies: []

quotes:
  - text: "Intention is choice with commitment, maintained until achieved,
    believed unachievable, or background conditions change"
    author: "Cohen & Levesque"
    year: 1990

gap: "No existing framework provides formal notation for
  intent-governed topology selection with drift detection.
  This is the core theoretical contribution."
```

### Writing Notes
- 3.1: Three Primitives table with examples (~0.5 pages)
- 3.2: Formal notation — keep simple but rigorous: IoT tuple, selection function, drift function (~0.5 pages)
- 3.3: Topology selection mechanism table: purpose type → topology → rationale (~0.75 pages)
- 3.4: Drift detection: IDS definition, threshold, correction protocol (~0.75 pages)
- This is the CORE section. Spend the most care here.
- Must be formally precise enough for CS.AI but accessible enough for CL cross-list
- ~2.5 pages, ~1000-1100 words

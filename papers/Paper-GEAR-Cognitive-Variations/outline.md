# Paper Outline: Cognitive Variation as an Orthogonal Dimension in AI Reasoning — The G.E.A.R. Framework

> **Venue**: SSRN (practitioner-accessible academic voice) + Arxiv CS.AI cross-post
> **Type**: Framework paper with comparative analysis and practitioner evaluation
> **Target**: 8-10 pages + references
> **Stealth**: No proprietary branding. Use "we propose" / "the authors."

---

## Contributions

| # | Contribution | Type |
|---|-------------|------|
| C1 | Structured analysis showing that existing cognitive frameworks (Bloom, de Bono, Kahneman, BDI, AI agent architectures) describe tasks but not postures, identifying the "variation gap" | Survey/Gap Analysis |
| C2 | The G.E.A.R. framework: four cognitive variations (Generative, Engaging, Adversarial, Reflective) formalized as an orthogonal dimension to cognitive action, with definitions, cognitive signatures, blind spot pairs, and the 4xN variation-verb matrix | Framework |
| C3 | Comparative analysis with Six Thinking Hats, dual-process theory, and agent architectures, plus practitioner vignettes demonstrating variation-aware task design | Evaluation |

---

## Section 1: Introduction (1.5 pages)

### 1.1 The Task-Posture Distinction
- Cognitive frameworks describe what you DO: six levels (Bloom 1956), six modes (de Bono 1985), two systems (Kahneman 2011)
- AI agent architectures describe what agents CAN do: verbs, tools, functions
- None address HOW the agent (or human) thinks while performing the task
- A surgeon can analyse tissue adversarially (seeking pathology) or engagingly (seeking cross-speciality patterns): same verb, different cognitive posture, different output

### 1.2 The Variation Gap
- Prior work on cognitive modes exists (de Bono closest) but conflates mode WITH task
- CoALA (Sumers et al. 2024) identifies metareasoning as "significantly underexplored"
- No framework treats variation as an approximately independent dimension to action
- In AI agent design, this means N tools produce N cognitive acts; variation-awareness produces N x V acts from the same tools
- The design implication: combinatorial cognitive space without combinatorial code
- KEY POSITIONING: GEAR is prescriptive (a design framework for cognitive architects), not descriptive (a personality taxonomy). It does not claim people naturally think in four fixed modes; it proposes that deliberately adopting one of four cognitive postures produces measurably different outputs.

### 1.3 Contribution Statement
Three-bullet summary:
1. We survey cognitive frameworks across psychology, AI, and agent theory and identify the variation gap
2. We propose G.E.A.R.: four cognitive variations formalized as an orthogonal dimension with definitions, blind spot pairs, and a variation-verb matrix
3. We demonstrate G.E.A.R. through comparative analysis with existing frameworks and practitioner vignettes

### Key Citations
- Bloom (1956), de Bono (1985), Kahneman (2011), Schon (1983), Polanyi (1966)
- BDI: Bratman (1987), Rao & Georgeff (1995)
- AI Agents: Park et al. (2023), Yao et al. (2023), Wei et al. (2022)

---

## Section 2: Background and Related Work (2 pages)

### 2.1 Cognitive Mode Frameworks
- **Bloom's Taxonomy** (1956, rev. Anderson & Krathwohl 2001): 6 cognitive levels (Remember → Create). Hierarchical, not modal. Does not address posture within levels.
- **de Bono's Six Thinking Hats** (1985): 6 modes (White/facts, Red/feelings, Black/caution, Yellow/optimism, Green/creativity, Blue/process). Closest to variation thinking, but modes are task-coupled, not orthogonal. No blind spot model.
- **Kahneman's Dual Process** (2011): System 1 (fast, intuitive) vs System 2 (slow, deliberate). Binary: cognitive reality has more than two gears. Speed axis only, no posture axis.
- **Schon's Reflective Practice** (1983): reflection-in-action vs reflection-on-action. Names one variation (reflective) but does not formalize the others.
- **Polanyi's Tacit Knowledge** (1966): "We know more than we can tell." Identifies generative cognition (thinking through making) but does not systematize variations.
- **Jung's Four Functions** (1921): Thinking, Feeling, Sensation, Intuition. Typological (identity-based), not situational (posture-based).

### 2.2 Meta-Reasoning and Thinking Dispositions (NEW from research)
- **Evans & Stanovich (2013)**: Type 1 (autonomous) vs Type 2 (reflective). Not fast/slow but working memory coupling. Foundational dual-process.
- **Ackerman & Thompson (2017)**: Meta-reasoning framework. Feelings of certainty/uncertainty drive mode transitions. Most cited work on metacognitive stance selection (~617 citations).
- **Newton, Feeney & Pennycook (2023/2024)**: FOUR independent thinking dimensions empirically identified (AOT, Close-minded, Intuitive Preference, Effortful Preference). Thinking style is multidimensional.
- **Mercier & Sperber (2017)**: Argumentative theory: producer stance (biased toward current beliefs) vs evaluator stance (epistemic vigilance). Social role determines cognitive mode.
- **Hommel (2015)**: Metacontrol State Model: persistence vs flexibility continuum, dynamically regulated by dopamine, context, reward.
- **Stanovich (2016)**: Tripartite model: autonomous mind, algorithmic mind, reflective mind. Capacity != deployment. GEAR is about deployment.

### 2.3 AI Agent Architectures and Cognitive Design (expanded)
- **BDI Architecture** (Bratman 1987, Rao & Georgeff 1995): Beliefs, Desires, Intentions. Agent-action level: governs what to do, not how to think while doing it.
- **ReAct** (Yao et al. 2022/2023): Interleaved Thought-Act-Obs loop. Fixed, uniform posture. Canonical baseline.
- **Reflexion** (Shinn et al. 2023): Phase-level mode switch (execution → reflection). Verbal self-critique as learning signal. 91% pass@1 on HumanEval.
- **Generative Agents** (Park et al. 2023): Event-driven reflection triggered by importance threshold. Memory-driven cognitive depth.
- **ToT/LATS** (Yao et al. 2023, Zhou et al. 2024): Deliberateness as a design variable. Branching, backtracking, search-based reasoning.
- **CoALA** (Sumers et al. 2024): Unifying taxonomy. Memory types (W/E/S/P), action types (internal/external). Identifies metareasoning as underexplored.
- **Talker-Reasoner** (Christakopoulou et al. 2024): Structurally separate fast/slow modules. Cognitive mode as structural design variable.
- **Chain of Mindset** (Jiang et al. 2025): Step-level multi-mindset switching (Spatial, Convergent, Divergent, Algorithmic). Closest to GEAR but mindsets are TASK-SPECIFIC, not task-orthogonal.
- **ARES** (Yang et al. 2026): Per-step effort routing. Learned reasoning-depth policy. Overthinking hurts performance.

### 2.3 The Differentiation Matrix

**TABLE**: Centrepiece comparison showing what each framework addresses and what it misses.

| Framework | What It Describes | Posture-Aware? | Orthogonal? | Blind Spot Model? |
|-----------|------------------|----------------|-------------|-------------------|
| Bloom's Taxonomy | Cognitive levels | No | No | No |
| Six Thinking Hats | Thinking modes | Partially (6 modes) | No (mode = task) | No |
| Dual Process Theory | Processing speed | No | No | No |
| Reflective Practice | One variation | Partially | No | No |
| Four Thinking Dimensions (Newton) | Dispositions | No (trait-based) | No | No |
| Argumentative Theory (Mercier) | Producer/Evaluator | Partially (2 modes) | No | No |
| BDI | Agent intentions | No | No | No |
| CoALA | Agent taxonomy | Vocabulary only | No | No |
| CoM (Chain of Mindset) | 4 task-specific mindsets | Yes (step-level) | No (mindset = task type) | No |
| Talker-Reasoner | Fast/slow structural split | Yes (2 modules) | No (hardwired) | No |
| **G.E.A.R. [this paper]** | **Cognitive variations** | **Yes (4 gears)** | **Yes (variation x action)** | **Yes (2 pairs)** |

---

## Section 3: The G.E.A.R. Framework (2.5 pages)

### 3.1 Core Claim: Approximate Independence of Variation and Action
- Define cognitive action (verb): what the agent does (search, write, analyse, debate)
- Define cognitive variation (gear): how the agent thinks while doing it
- Claim: variation is approximately independent of action. The combinatorial space is V x A, not V + A
- Acknowledge: tasks DO prime certain gears (code review primes adversarial). The claim is that this default CAN be overridden, and doing so produces measurably different output.
- Formalize: CognitiveAct := (Action, Variation) → Output
- GEAR is PRESCRIPTIVE (design framework), not DESCRIPTIVE (personality taxonomy)

### 3.2 The Four Variations

| Variation | Core Act | Primary Question | Temporal Orientation | Output Shape |
|-----------|----------|-----------------|---------------------|-------------|
| **Generative** | Flow | "What can I make?" | Present (deep now) | Artifact: prose, code, design |
| **Engaging** | Fusion | "What engages across these?" | Atemporal (pattern outside time) | New pattern, analogy, framework |
| **Adversarial** | Friction | "What could break this?" | Future (pre-mortem) | Cracks found, failure modes mapped |
| **Reflective** | Echo | "What did I learn?" | Past (retrospective) | Updated heuristics, lessons |

For each variation, provide:
- Formal definition (one paragraph)
- Cognitive signature (6 dimensions: question, tone, temporality, social posture, output, energy)
- Boundary condition (when to exit)
- Anti-patterns (4 failure modes per variation)

### 3.3 The Blind Spot Matrix
- Adversarial ↔ Engaging: friction and fusion are cognitive opposites
- Generative ↔ Reflective: making and learning are temporal opposites
- Your default gear predicts your blind spot: maximal cognitive distance
- The blind spot is not a weakness per se, but a systematic omission

### 3.4 The Variation-Verb Matrix
- Present the 4xN matrix: any verb x any variation = distinct cognitive act
- Worked examples using 6 common cognitive verbs:

| Verb | Generative | Engaging | Adversarial | Reflective |
|------|-----------|----------|-------------|-----------|
| Research | Discover by building | Cross-domain scan | Seek disconfirmation | Re-examine old sources |
| Write | Flow-state drafting | Collision article | Inner critic editing | Revision pass |
| Debate | Structured brainstorm | Fusion debate | Stress-test | Retrospective deliberation |
| Review | Improvement proposals | Cross-system consistency | Gap detection | Meta-review of review |
| Summarise | Writing-to-understand | Cross-domain concept map | Steelman summary | Lessons-learned digest |
| Communicate | Creative metaphor | Audience bridge | Provocative reframe | Historical lens |

### 3.5 Design Implications for AI Agents
- Instead of building N specialised tools, parameterize V variations across existing tools
- Combinatorial space: 4 variations x 8 verbs = 32 cognitive acts from a 12-token parameter
- Syntax: `verb:variation` (e.g., `search:engaging`, `analyse:adversarial`)
- Agent architecture receives a variation parameter that modulates all downstream behaviour

---

## Section 4: Comparative Analysis and Evaluation (1.5 pages)

### 4.1 Comparative Analysis with Six Thinking Hats
- Map de Bono's 6 hats to G.E.A.R.'s 4 gears
- Black Hat ≈ Adversarial, Green Hat ≈ Generative, White+Yellow ≈ Engaging, Blue ≈ Reflective
- Key differences: (1) G.E.A.R. is orthogonal (hats are not), (2) blind spot model, (3) variation-verb matrix
- G.E.A.R. handles the "what hat for what task?" problem by making variation independent of task

### 4.2 Comparative Analysis with Dual Process Theory
- System 1/2 describes processing speed, not cognitive posture
- All four gears can operate in both System 1 and System 2
- Example: adversarial System 1 = gut instinct that something is wrong; adversarial System 2 = systematic red-team

### 4.3 Practitioner Vignettes
Three vignettes from real-world deployment:

**Vignette 1: Software Engineering Team**
- Team running code reviews defaulted to adversarial (bug-hunting)
- Introduced engaging variation: "What pattern does this code share with our data pipeline?"
- Result: architectural insight invisible to pure bug-hunting

**Vignette 2: Strategy Workshop**
- Executive team defaulted to generative (brainstorming)
- Introduced reflective variation: "What did last quarter's strategy teach us?"
- Result: avoided repeating a resource allocation pattern from Q2

**Vignette 3: AI Agent Architecture**
- Agent system with 8 verbs operated in default variation per verb
- Introduced variation parameter: each verb now takes a gear selector
- Result: 4x combinatorial increase in cognitive acts without additional tools

---

## Section 5: Discussion (1 page)

### 5.1 Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| No large-scale experiments | Cannot claim statistical significance | Practitioner vignettes demonstrate utility; ANOVA falsification design proposed as future work |
| Tasks prime certain gears | Approximate independence, not perfect orthogonality | Framework is prescriptive (design tool), not descriptive (personality taxonomy). Priming can be overridden. |
| Variation boundaries are fuzzy | Gears may blend in practice | Cognitive signature provides 6-dimension disambiguation |
| Cultural dependence | Variation defaults may vary by culture | Cross-cultural study proposed as future work |
| Four is a design choice | Why not 3, 5, 6, or 71? (Coffield et al. found 71 style models) | Four derives from two orthogonal axes (Forward/Backward x Split/Join). Parsimonious and actionable. SPAR adjudicated: 5th rejected. |
| Strategy switching within individuals | Morrison et al. (2016): same person switches strategies across tasks | GEAR predicts this: different tasks prime different default gears. The framework's value is making the switch deliberate. |
| Self-report bias in vignettes | Practitioners may over-report impact | Propose Style x Task ANOVA as controlled experiment (from ChatGPT critique) |

### 5.2 Broader Implications
- For AI agent design: variation as a first-class parameter in cognitive architectures
- For team facilitation: "What gear are we in?" as a meeting diagnostic
- For education: teaching learners to name their default and deliberately practice their blind spot gear
- For cognitive science: the orthogonality claim is empirically testable (same task, different variation, measure output difference)

### 5.3 Connection to Elemental Frameworks
- Brief note: the four gears map naturally to two orthogonal axes (Forward↔Backward, Split↔Join)
- This structural alignment suggests the taxonomy is not arbitrary but reflects a deeper cognitive geometry
- Historical resonance with classical elemental systems (without overclaiming cultural universality)

---

## Section 6: Conclusion (0.5 pages)

### Summary
- Identified the variation gap in cognitive frameworks
- Proposed G.E.A.R.: four orthogonal cognitive variations
- Demonstrated through comparative analysis and practitioner vignettes
- Provided the variation-verb matrix as a design primitive

### Future Work
- Large-scale controlled study: same task x different variation instruction → measure output differences
- AI agent benchmark: variation-parameterized agents vs fixed-variation agents on diverse tasks
- Cross-cultural study: do variation defaults differ by national culture, professional domain, or personality type?
- Integration with cognitive load theory: does variation-switching have a measurable cognitive cost?

---

## References (~40-60 citations)

### Must-Cite
| Paper | Why |
|-------|-----|
| Bloom (1956) | Foundational cognitive taxonomy |
| Anderson & Krathwohl (2001) | Revised Bloom's |
| de Bono (1985) | Six Thinking Hats, closest prior art |
| Kahneman (2011) | Dual process theory |
| Schon (1983) | Reflective practice |
| Polanyi (1966) | Tacit knowledge, thinking through making |
| Evans & Stanovich (2013) | Foundational dual-process architecture |
| Ackerman & Thompson (2017) | Meta-reasoning landmark (~617 citations) |
| Newton, Feeney & Pennycook (2023/2024) | Four independent thinking dimensions |
| Mercier & Sperber (2017) | Argumentative theory, producer vs evaluator |
| Hommel (2015) | Metacontrol state model |
| Braver (2012) | Dual mechanisms of control (~1870 citations) |
| Stanovich (2016) | CART / tripartite model |
| De Neys (2022/2023) | DPT revision |
| Morrison et al. (2016) | Strategy variation across tasks |
| Bratman (1987) | Intention theory |
| Rao & Georgeff (1995) | BDI formalization |
| Wei et al. (2022) | Chain-of-Thought |
| Yao et al. (2022/2023) | ReAct + Tree-of-Thought |
| Shinn et al. (2023) | Reflexion |
| Park et al. (2023) | Generative Agents |
| Sumers et al. (2024) | CoALA taxonomy |
| Christakopoulou et al. (2024) | Talker-Reasoner |
| Jiang et al. (2025) | Chain of Mindset |
| Yang et al. (2026) | ARES adaptive effort |
| Csikszentmihalyi (1990) | Flow (generative gear) |
| Kolb (1984) | Experiential learning cycle (reflective gear) |
| Lakoff & Johnson (1980) | Metaphors We Live By (engaging gear) |
| Tetlock (2005) | Superforecasting, adversarial calibration |
| Janis (1972) | Groupthink (adversarial absence pathology) |
| Braem & Egner (2024) | Meta-flexibility |

---

## Meta

| Dimension | Value |
|-----------|-------|
| Estimated writing time | 1-2 weeks |
| Pages | 10 + references |
| Sections | 6 |
| Tables | ~8 (differentiation matrix, 4 variations, blind spot, variation-verb, hat mapping, agent comparison, limitations, citations) |
| Figures | 1-2 (compass diagram, variation-verb matrix visual) |
| External research | 3 documents (Perplexity-1 Agent Architectures, Perplexity-2 Cognitive Modes, ChatGPT-1 Orthogonality Critique) |
| Signals extracted | 7 opportunities, 4 clashes, 4 validations |
| Must-cite papers | ~30 (expanded from 18 to 30 via research) |
| SPAR source | Deep Ultra, 82% confidence |

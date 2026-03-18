# Section X: SPAR as First Variation-Aware Verb

> Draft section for GEAR paper. Source: [SPAR-GEAR-2026-03-17](file:///Users/naveen/.gemini/antigravity/brain/99ed191f-d7cf-4be8-931c-8ffa2b4d992c/spar_gear_into_spar_workflow.md)
> Ready for revision and integration into paper structure.

## X.1 Case Study: Variation vs. Style in Structured Debate

The SPAR protocol (Structured Persona-Argumentation for Reasoning) provides a case study for the orthogonality hypothesis. SPAR's `--style` axis defines interaction dynamics between debate agents (balanced, adversarial, steelman, consensus, premortem, escalation, inversion). The GEAR framework's variations define cognitive postures (Generative, Engaging, Adversarial, Reflective).

An internal SPAR debate (8 agents, 3 rounds, dialectic/steelman preset, 91% confidence) adjudicated whether GEAR variations should replace or augment SPAR's Style axis. The verdict established that they are orthogonal:

| Dimension | GEAR Variation | SPAR Style |
|-----------|---------------|------------|
| Governs | Cognitive posture (how agents think) | Debate dynamics (how agents interact) |
| Scope | Entire debate run | Agent-to-agent within a round |
| Mechanism | `verb:variation` frontmatter | `--style` flag |

A practitioner can steelman (Style) while in any GEAR mode. A debate can apply adversarial interaction (Style) while the overall cognitive posture is Connective (Variation). This confirms the independence hypothesis: variation modulates the *quality* of reasoning, not its *form*.

## X.2 The 3-Axis Model

SPAR's current architecture separates three independent cognitive dimensions:

1. **GEAR (Variation)**: how agents think (set via `verb:variation` frontmatter)
2. **IoT (Intent)**: what agents reason about and what they must avoid (set via AoT→topology mapping at the problem classification step)
3. **Style (Interaction)**: how agents interact with each other (set via `--style` flag)

This three-axis model provides evidence that cognitive variation is a genuine independent dimension, not reducible to interaction style or task specification. The variation axis survived an adversarial debate specifically designed to challenge its distinctiveness.

## X.3 Blind Spot Evidence

The debate surfaced that SPAR's default variation (`spar:adversarial`) systematically neglects the Connective variation's cross-domain pattern detection (the Adversarial↔Connective blind spot pair). When SPAR debates are run with `spar:connective`, the synthesis step produces more cross-domain connections but weaker stress-testing, confirming the complementarity principle.

## X.4 Design Implication

For AI agent systems implementing multi-agent debate, the GEAR framework suggests that variation should be configurable independently of interaction protocol. An agent's cognitive posture (Generative, Engaging, Adversarial, Reflective) is a separate parameter from its debate role (advocate, contrarian, synthesizer) and its interaction mode (adversarial, steelman, consensus).

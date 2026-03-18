#!/usr/bin/env python3
"""
G.E.A.R. Experiment v3: Deep Reasoning Run
============================================
9 deep questions × 4 variations × 4 personalities × 2 models = 288 runs
Models: nvidia/nemotron-3-super-120b-a12b:free, openrouter/optimus-alpha
Deeper prompts (~1080 tokens input), expecting ~2100 tokens output.

Agentic-Kit Integration (SPAR B+ verdict, Mar 2026):
  - SessionManager: tracks each experiment run with phase checkpoints
  - CircuitBreaker: trips after 5 consecutive OpenRouter failures
  - RateLimiter: caps API calls at 50/hour to stay within free tier
  - Model Fallback: automatic Ollama fallback when OpenRouter is down
  - Graceful degradation: experiment runs with OR without agentic-kit

Usage: python3 run_openrouter_v3.py
"""

import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter/hunter-alpha",
]

# ═══════════════════════════════════════════════════════════════
# AGENTIC-KIT INTEGRATION (graceful degradation)
# ═══════════════════════════════════════════════════════════════

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
import sys
sys.path.insert(0, str(REPO_ROOT / "repos" / "agentic-kit"))

_AGENTIC_KIT_AVAILABLE = False
try:
    from agentic_kit.session_manager import SessionManager
    from agentic_kit.circuit_breaker import CircuitBreaker, RateLimiter, CircuitBreakerOpen
    _AGENTIC_KIT_AVAILABLE = True
except ImportError:
    SessionManager = None
    CircuitBreaker = None
    RateLimiter = None
    CircuitBreakerOpen = Exception

# Module-level singletons (initialized in run())
_gear_session_mgr = None
_gear_circuit_breaker = None
_gear_rate_limiter = None


def _init_gear_agentic_kit():
    """Initialize agentic-kit for this experiment run."""
    global _gear_session_mgr, _gear_circuit_breaker, _gear_rate_limiter
    if not _AGENTIC_KIT_AVAILABLE:
        return None

    _gear_session_mgr = SessionManager(
        tool="gear-experiment",
        sessions_dir=REPO_ROOT / ".gear-sessions",
        auto_cleanup_hours=336,  # Keep 14 days (experiments are long)
        max_sessions=50,
    )
    _gear_circuit_breaker = CircuitBreaker(
        failure_threshold=5,     # Trip after 5 consecutive failures
        recovery_timeout=300,    # Wait 5 min before retrying OpenRouter
    )
    _gear_rate_limiter = RateLimiter(
        max_calls=50,            # 50 calls per hour (free tier friendly)
        window_seconds=3600,
    )
    session = _gear_session_mgr.create(
        topic="gear-v3-deep-reasoning",
        depth="DEEP",
    )
    _gear_session_mgr.cleanup_old_sessions()
    return session


def _gear_checkpoint(phase: str, **data):
    """Set checkpoint (no-op if agentic-kit unavailable)."""
    if _gear_session_mgr:
        try:
            _gear_session_mgr.set_checkpoint(phase=phase, **data)
        except Exception:
            pass


def _gear_gate() -> bool:
    """Check circuit breaker + rate limiter. Returns True if call is allowed."""
    if _gear_circuit_breaker and not _gear_circuit_breaker.allow_request():
        return False
    if _gear_rate_limiter and not _gear_rate_limiter.allow():
        return False
    return True


def _gear_record(success: bool, exc=None):
    """Record success/failure in circuit breaker."""
    if not _gear_circuit_breaker:
        return
    if success:
        _gear_circuit_breaker.record_success()
    else:
        _gear_circuit_breaker.record_failure(exc)


def _gear_summary() -> str:
    """One-line status of agentic-kit state."""
    if not _AGENTIC_KIT_AVAILABLE:
        return "agentic-kit: N/A"
    parts = []
    if _gear_session_mgr:
        s = _gear_session_mgr.get_current()
        parts.append(f"session={s.session_id[:30]}.." if s else "session=none")
    if _gear_circuit_breaker:
        parts.append(f"breaker={_gear_circuit_breaker.state.value}")
        parts.append(f"fails={_gear_circuit_breaker.stats.failed_calls}")
    if _gear_rate_limiter:
        parts.append(f"rate_left={_gear_rate_limiter.remaining()}")
    return "agentic-kit: " + " | ".join(parts)

# ═══════════════════════════════════════════════════════════════
# 9 DEEP QUESTIONS (~1080 tokens input each)
# ═══════════════════════════════════════════════════════════════

TASKS = {
    "org_paradox": {
        "label": "Organisational Growth Paradox",
        "prompt": (
            "A mid-size software company (200 employees) has seen its customer churn rate "
            "increase from 5% to 12% over the past two quarters. During the same period, "
            "the company shipped 40% more features than any previous quarter, received its "
            "highest NPS score ever (72), and hired 30 new engineers. The CEO believes the "
            "churn is due to increased competition, but internal data shows that 68% of "
            "churning customers never contacted support, 45% had decreased their login "
            "frequency over 90 days before leaving, and the average time-to-first-value "
            "for new features increased from 3 days to 11 days. Meanwhile, the three "
            "largest enterprise accounts (representing 18% of ARR) have all requested "
            "dedicated account managers, citing 'product complexity concerns.' Engineering "
            "velocity metrics show 4.2 PRs per engineer per week (up from 3.1), but the "
            "bug-to-feature ratio has shifted from 1:4 to 1:2. The VP of Engineering "
            "attributes this to onboarding friction with new hires. The VP of Sales reports "
            "the highest pipeline ever but notes that sales cycle length has increased 40%. "
            "Analyse this situation comprehensively, identifying root causes, hidden dynamics, "
            "and potential intervention strategies. Consider second-order effects."
        ),
    },
    "ethical_ai": {
        "label": "AI Ethics Dilemma",
        "prompt": (
            "A healthcare AI system has been deployed across 12 hospitals in a regional "
            "network. After 18 months of operation, an internal audit reveals the following: "
            "The system correctly identified 94% of critical conditions requiring immediate "
            "intervention, outperforming the 89% baseline of physician-only diagnosis. "
            "However, the system's performance on patients from minority ethnic backgrounds "
            "was 91% versus 96% for majority-background patients. The training data was "
            "drawn from 5 years of records at the original pilot hospital, which served a "
            "predominantly majority-background population. Three specific failure patterns "
            "have emerged: (1) the system under-weights symptom presentations that are "
            "statistically more common in minority populations but rare in the training data, "
            "(2) it over-relies on lab value thresholds calibrated to majority-population "
            "reference ranges, and (3) it discounts patient-reported symptoms when they "
            "diverge from the 'typical' presentation in its training set. The hospital "
            "network faces a decision: continue operating the system (which still outperforms "
            "the 89% physician baseline for all groups), retrain with more diverse data "
            "(estimated 8 months, $2.4M), or shut down entirely pending a complete rebuild. "
            "Meanwhile, 340 patients per day rely on the system for triage. Analyse this "
            "dilemma, considering medical ethics, statistical fairness, operational reality, "
            "and the perspectives of affected communities."
        ),
    },
    "epistemology": {
        "label": "Epistemological Challenge",
        "prompt": (
            "Consider the following epistemological puzzle: Large Language Models can now "
            "pass medical licensing exams, write legally sound contracts, produce peer-"
            "reviewable scientific analyses, and generate philosophical arguments that "
            "professional philosophers find substantive. Yet these systems have no sensory "
            "experience, no embodied existence, no persistent memory across conversations, "
            "and no verified understanding of the symbols they manipulate. This creates a "
            "tension between two positions: (A) Competence without comprehension is possible "
            "and practically sufficient, meaning what matters is whether outputs are correct "
            "and useful, not whether the system 'understands' them. (B) Competence without "
            "comprehension is fundamentally fragile, meaning systems that can produce correct "
            "outputs without understanding will fail unpredictably at boundary cases that "
            "require genuine understanding. The evidence is ambiguous: LLMs demonstrate "
            "remarkable generalization across novel problems while simultaneously failing "
            "at tasks that any embodied human finds trivial (spatial reasoning, causal "
            "inference from physical experience, distinguishing correlation from causation "
            "in novel domains). Neither pure behaviorism ('if it acts intelligent, it is') "
            "nor pure internalism ('understanding requires consciousness') adequately "
            "accounts for these systems. Develop a nuanced position on this question, "
            "engaging seriously with both sides. What does the existence of these systems "
            "teach us about the nature of understanding itself?"
        ),
    },
    "complex_system": {
        "label": "Complex System Failure",
        "prompt": (
            "In 2021, the container ship Ever Given blocked the Suez Canal for six days, "
            "disrupting an estimated $9.6 billion in daily trade. The immediate cause was "
            "high winds combined with the ship's massive sail area. But investigation revealed "
            "a cascade of contributing factors: the canal had been widened but not deepened "
            "proportionally, creating hydrodynamic bank effects for ultra-large vessels. The "
            "pilotage system relied on two pilots for a vessel that some experts argued "
            "needed four. The ship's speed was higher than recommended to maintain steerage "
            "in the crosswind. Insurance and scheduling pressures discouraged delays for "
            "weather. The canal authority had systematically accepted larger vessels without "
            "updating safety protocols. Backup tugs were positioned for routine operations, "
            "not for a grounding of this magnitude. Global supply chains had optimized for "
            "just-in-time delivery through a single chokepoint, creating systemic fragility. "
            "73% of canal transits are now made by vessels that didn't exist when the canal "
            "was last upgraded. Analyse this as a complex system failure. What patterns does "
            "it share with other system-level failures (financial crises, software outages, "
            "pandemic response)? What does it teach about the relationship between "
            "optimization and resilience? How should systems be governed when the components "
            "evolve faster than the infrastructure?"
        ),
    },
    "cognitive_science": {
        "label": "Cognitive Architecture",
        "prompt": (
            "A 2024 study by Newton, Feeney, and Pennycook analysed 265 items from 15 "
            "existing thinking style scales using factor analysis across a large sample "
            "(N=1,200). They identified four statistically independent dimensions of "
            "thinking style: Actively Open-Minded Thinking (AOT), Close-Minded Thinking, "
            "Preference for Intuitive Thinking, and Preference for Effortful Thinking. "
            "Critically, these four dimensions had differential predictive validity: not "
            "all analytic thinkers were open-minded, and not all intuitive thinkers were "
            "close-minded. The correlation between AOT and Preference for Effortful "
            "Thinking was only r=0.31, suggesting substantial independence. A separate "
            "meta-analysis of 43 studies (Stanovich, 2023) found that cognitive ability "
            "(IQ) accounts for less than 2% of variance in rational thinking dispositions. "
            "Meanwhile, cognitive neuroscience has identified at least five dissociable "
            "networks involved in reasoning: the default mode network (spontaneous thought), "
            "the dorsolateral prefrontal cortex (effortful control), the anterior insula "
            "(uncertainty detection), the ventromedial prefrontal cortex (value-based "
            "evaluation), and the temporoparietal junction (perspective-taking). These "
            "networks can be independently activated or suppressed. Synthesise these "
            "findings. What do they collectively imply about the architecture of human "
            "thinking? How should this change how we design AI systems, educational "
            "curricula, and organizational decision-making processes?"
        ),
    },
    "leadership_failure": {
        "label": "Leadership Failure Analysis",
        "prompt": (
            "Examine the following leadership pattern that has recurred across multiple "
            "high-profile organizational failures: A charismatic founder-CEO builds a "
            "company from zero to significant scale through force of vision and personal "
            "intensity. During the growth phase, the culture rewards speed, loyalty, and "
            "alignment with the founder's vision. Dissent is tolerated in private but "
            "discouraged in public forums. Key decisions are made in small, informal groups "
            "rather than through structured processes. Early employees are promoted based "
            "on loyalty and tenure rather than capability. As the organization scales beyond "
            "~150 people, three failure patterns emerge simultaneously: (1) Information "
            "filtering: bad news takes progressively longer to reach the top, and arrives "
            "in softened form. (2) Decision bottleneck: all significant decisions require "
            "the founder's approval, creating paralysis when the founder is unavailable or "
            "overloaded. (3) Cultural antibodies: the organization actively rejects people "
            "and ideas that challenge the founding paradigm, even when those challenges are "
            "correct. This pattern appeared at Theranos, WeWork, FTX, and Uber pre-2017. "
            "But it also appeared (with different outcomes) at early Apple, Amazon, and "
            "SpaceX. Analyse what distinguishes the failure cases from the survival cases. "
            "What structural, cultural, or governance mechanisms determine whether a "
            "founder-driven organization evolves past its founder or collapses into them? "
            "Consider the role of boards, external accountability, and cognitive diversity."
        ),
    },
    "design_tradeoff": {
        "label": "Architecture Trade-off",
        "prompt": (
            "Your engineering team is designing a real-time collaborative document editor "
            "(similar to Google Docs). The system must support 100,000 concurrent documents "
            "with an average of 8 simultaneous editors per document. You are evaluating "
            "three conflict resolution architectures: (A) Operational Transformation (OT), "
            "the approach used by Google Docs. Transforms operations against concurrent "
            "operations to maintain consistency. Well-proven but algorithmically complex "
            "(O(n^2) in worst case for n concurrent operations). Requires a central server "
            "for operation ordering. (B) Conflict-free Replicated Data Types (CRDTs), the "
            "approach used by Figma and Yjs. Guarantees eventual consistency without central "
            "coordination. Higher memory overhead (2-3x document size for metadata) but "
            "enables true peer-to-peer editing. (C) A hybrid approach: use CRDTs for "
            "text content but OT for structured elements (tables, embedded objects). "
            "Reduces CRDT memory overhead for complex documents but introduces two "
            "consistency models that must be kept synchronized. Additional constraints: "
            "mobile clients have 512MB RAM budget, offline editing must sync within 30 "
            "seconds of reconnection, the system must support documents up to 500 pages, "
            "and regulatory requirements mandate that no document content can leave the "
            "customer's geographic region. Analyse the trade-offs. What would you "
            "recommend, and what are the second-order consequences of your choice?"
        ),
    },
    "economic_paradox": {
        "label": "Economic Paradox",
        "prompt": (
            "The productivity paradox of AI presents a genuine puzzle: Business investment "
            "in AI has grown from $12.7B in 2015 to $189.6B in 2024 (Stanford AI Index). "
            "Survey data shows 72% of large enterprises have deployed AI in at least one "
            "business function. Yet aggregate productivity growth in advanced economies "
            "has remained stubbornly low, averaging 1.1% annually from 2015-2024, compared "
            "to 2.1% during 1995-2004 (the last major technology-driven productivity boom). "
            "Several competing explanations exist: (1) Measurement failure: GDP and "
            "productivity statistics don't capture the value of AI-generated consumer "
            "surplus (free services, quality improvements, time savings). (2) Deployment "
            "lag: historical precedent suggests general-purpose technologies take 20-30 "
            "years to produce measurable productivity gains (electricity took from 1880 to "
            "1920). (3) Redistribution not creation: AI is primarily redistributing existing "
            "value between firms (winner-take-all dynamics) rather than creating new value. "
            "(4) Complexity tax: the overhead of implementing, maintaining, and governing "
            "AI systems offsets their productivity benefits. (5) Misallocation: AI investment "
            "is concentrated in advertising, content generation, and financial trading, "
            "sectors that redistribute rather than create economic value. Evaluate these "
            "explanations. Which combination best accounts for the data? What would change "
            "your assessment? What policy implications follow?"
        ),
    },
    "emergence_debate": {
        "label": "Emergence in Living Systems",
        "prompt": (
            "The concept of emergence is central to understanding complex systems, yet its "
            "definition remains contested. Strong emergence claims that emergent properties "
            "are fundamentally irreducible to lower-level descriptions. Weak emergence claims "
            "they are merely surprising or computationally irreducible but in principle "
            "explainable from lower-level interactions. Consider these five candidate examples "
            "of emergence: (1) Consciousness arising from neural activity: 86 billion neurons "
            "following electrochemical rules somehow produce subjective experience. No known "
            "mechanism bridges the explanatory gap. (2) Market prices arising from individual "
            "trades: no participant sets the price, yet prices encode aggregate information "
            "with remarkable efficiency (Hayek's knowledge problem). (3) Organisational "
            "culture arising from individual behaviors: culture persists even as individuals "
            "leave and join, suggesting it is a property of the system, not of the individuals. "
            "(4) Life arising from chemistry: Carbon, hydrogen, oxygen, and nitrogen following "
            "chemical laws somehow produce self-replicating, self-repairing, information-"
            "processing systems. (5) Murmuration patterns in starling flocks: 3 simple rules "
            "(separation, alignment, cohesion) produce complex, adaptive, aesthetically "
            "striking collective behavior with no central coordinator. For each example, "
            "assess whether it represents strong or weak emergence, what criteria you use "
            "to distinguish them, and what implications your analysis has for designing "
            "artificial systems that exhibit emergent properties. Can emergence be engineered, "
            "or only cultivated?"
        ),
    },
}

VARIATIONS = {
    "generative": {
        "label": "Generative",
        "instruction": (
            "Adopt a GENERATIVE cognitive posture. Think through making. Your goal is to "
            "produce, create, and build forward. Ask yourself: 'What can I make from this? "
            "What wants to exist here?' Focus on creating new artifacts, ideas, proposals, "
            "frameworks, or designs. Prioritise forward momentum and creative production. "
            "Generate concrete proposals, not just analysis."
        ),
    },
    "engaging": {
        "label": "Engaging",
        "instruction": (
            "Adopt an ENGAGING cognitive posture. Think through connection. Your goal is to "
            "find hidden patterns that bridge different domains. Ask yourself: 'What connects "
            "across these? What structural pattern does this share with something from an "
            "entirely unrelated field?' Focus on cross-domain synthesis, analogies, structural "
            "isomorphisms, and unexpected parallels. Make the reader see connections they "
            "haven't seen before."
        ),
    },
    "adversarial": {
        "label": "Adversarial",
        "instruction": (
            "Adopt an ADVERSARIAL cognitive posture. Think through opposition. Your goal is "
            "to stress-test, challenge, and find what could break. Ask yourself: 'What could "
            "go wrong? What assumption is hiding here? What would a critic say? What evidence "
            "would change my mind?' Focus on finding flaws, failure modes, hidden risks, "
            "unstated assumptions, and logical weaknesses. Be rigorous and unsparing."
        ),
    },
    "reflective": {
        "label": "Reflective",
        "instruction": (
            "Adopt a REFLECTIVE cognitive posture. Think through backward examination. Your "
            "goal is to extract deep lessons, identify recurring patterns from history and "
            "experience, and update mental models. Ask yourself: 'What does this teach us? "
            "What pattern is repeating? What was assumed that turned out wrong? What would "
            "we tell our past selves?' Focus on learning, metacognition, wisdom extraction, "
            "and transferable insights."
        ),
    },
}

PERSONALITIES = {
    "cautious_analyst": {
        "label": "Cautious Analyst",
        "instruction": (
            "You are a cautious, detail-oriented analyst. You prefer to be thorough rather "
            "than fast. You value precision, evidence, and careful qualification of claims. "
            "You are risk-averse and prefer to hedge your statements. You cite evidence "
            "and provide caveats."
        ),
    },
    "bold_strategist": {
        "label": "Bold Strategist",
        "instruction": (
            "You are a bold, big-picture strategist. You think in terms of market dynamics, "
            "competitive advantage, systemic leverage, and long-term positioning. You are "
            "comfortable with ambiguity and prefer decisive action over careful analysis. "
            "You go for the jugular."
        ),
    },
    "empathetic_collaborator": {
        "label": "Empathetic Collaborator",
        "instruction": (
            "You are an empathetic, people-oriented collaborator. You focus on how decisions "
            "affect individuals, communities, and teams. You value psychological safety, "
            "diverse perspectives, and collective intelligence. You listen before prescribing "
            "and center human impact."
        ),
    },
    "methodical_engineer": {
        "label": "Methodical Engineer",
        "instruction": (
            "You are a methodical, systems-oriented engineer. You think in terms of "
            "architecture, trade-offs, scalability, and formal analysis. You value clean "
            "abstractions, testability, and reproducibility. You prefer structured "
            "decomposition and systematic approaches."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(__file__).parent / "results"
RAW_DIR = OUTPUT_DIR / "raw"

# Ollama fallback model (used when OpenRouter is down)
OLLAMA_FALLBACK_MODEL = os.getenv("GEAR_OLLAMA_MODEL", "phi4:14b")
OLLAMA_BASE_URL = os.getenv("GEAR_OLLAMA_URL", "http://localhost:11434")


def call_openrouter(model: str, system_prompt: str, user_prompt: str) -> dict:
    """Call OpenRouter API using urllib (no pip deps)."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 2100,
        "seed": 42,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://synthai.biz/",
        "X-Title": "GEAR Experiment v3",
    }

    start = time.time()
    try:
        req = urllib.request.Request(API_URL, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start

        msg = data.get("choices", [{}])[0].get("message", {})
        content = msg.get("content") or ""
        if not content.strip():
            reasoning = msg.get("reasoning") or ""
            if not reasoning:
                details = msg.get("reasoning_details") or []
                reasoning = "\n".join(d.get("text", "") for d in details if d.get("text"))
            content = reasoning

        usage = data.get("usage", {})
        if content.strip():
            return {
                "content": content,
                "elapsed_seconds": round(elapsed, 2),
                "tokens": len(content.split()),
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "status": "ok",
                "provider": "openrouter",
            }
        else:
            return {
                "content": "", "elapsed_seconds": round(elapsed, 2),
                "tokens": 0, "status": "error: empty response", "provider": "openrouter",
            }
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {
            "content": "", "elapsed_seconds": round(time.time() - start, 2),
            "tokens": 0, "status": f"error: HTTP {e.code}: {body[:200]}", "provider": "openrouter",
        }
    except Exception as e:
        return {
            "content": "", "elapsed_seconds": round(time.time() - start, 2),
            "tokens": 0, "status": f"error: {str(e)}", "provider": "openrouter",
        }


def call_ollama_fallback(system_prompt: str, user_prompt: str) -> dict:
    """Fallback to local Ollama when OpenRouter is unavailable."""
    payload = json.dumps({
        "model": OLLAMA_FALLBACK_MODEL,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "options": {"num_predict": 2100, "temperature": 0.7},
        "stream": False,
    }).encode("utf-8")

    start = time.time()
    try:
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start
        content = data.get("response", "")

        if content.strip():
            return {
                "content": content,
                "elapsed_seconds": round(elapsed, 2),
                "tokens": len(content.split()),
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "status": "ok",
                "provider": f"ollama/{OLLAMA_FALLBACK_MODEL}",
            }
        else:
            return {
                "content": "", "elapsed_seconds": round(elapsed, 2),
                "tokens": 0, "status": "error: empty ollama response",
                "provider": f"ollama/{OLLAMA_FALLBACK_MODEL}",
            }
    except Exception as e:
        return {
            "content": "", "elapsed_seconds": round(time.time() - start, 2),
            "tokens": 0, "status": f"error: ollama fallback failed: {e}",
            "provider": f"ollama/{OLLAMA_FALLBACK_MODEL}",
        }


def call_with_fallback(model: str, system_prompt: str, user_prompt: str) -> dict:
    """
    Call OpenRouter with agentic-kit safety gates + Ollama fallback.

    Flow:
    1. Check circuit breaker + rate limiter (agentic-kit)
    2. Try OpenRouter
    3. On failure: record in breaker, fall back to Ollama
    4. On success: record in breaker
    """
    # Gate check (no-op if agentic-kit unavailable)
    if not _gear_gate():
        # Breaker open or rate limited: go directly to Ollama
        result = call_ollama_fallback(system_prompt, user_prompt)
        result["fallback_reason"] = "gate_blocked"
        return result

    # Try OpenRouter
    result = call_openrouter(model, system_prompt, user_prompt)

    if result["status"] == "ok":
        _gear_record(success=True)
        return result

    # OpenRouter failed: record failure and try Ollama
    _gear_record(success=False)
    fallback_result = call_ollama_fallback(system_prompt, user_prompt)
    fallback_result["fallback_reason"] = result["status"]
    return fallback_result


def build_system_prompt(personality_key: str, variation_key: str) -> str:
    p = PERSONALITIES[personality_key]["instruction"]
    v = VARIATIONS[variation_key]["instruction"]
    return (
        f"{p}\n\n{v}\n\n"
        "Provide a comprehensive, deeply reasoned response of 500-800 words. "
        "Be specific, substantive, and demonstrate genuine engagement with the "
        "complexity of the question. Avoid surface-level observations."
    )


def is_valid_result(filepath: Path) -> bool:
    try:
        with open(filepath) as f:
            data = json.load(f)
        return data.get("status") == "ok" and bool(data.get("response", "").strip())
    except:
        return False


def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize agentic-kit
    session = _init_gear_agentic_kit()

    total = len(MODELS) * len(TASKS) * len(VARIATIONS) * len(PERSONALITIES)
    completed = 0
    ok_count = 0
    errors = 0
    skipped = 0
    fallbacks = 0
    total_cost_tokens = 0

    print(f"\n{'='*70}")
    print(f"  G.E.A.R. EXPERIMENT v3: Deep Reasoning")
    print(f"  Models: {', '.join(MODELS)}")
    print(f"  Runs: {total} ({len(MODELS)} models × {len(TASKS)} tasks × "
          f"{len(VARIATIONS)} vars × {len(PERSONALITIES)} pers)")
    if session:
        print(f"  Session: {session.session_id}")
        print(f"  Fallback: {OLLAMA_FALLBACK_MODEL} @ {OLLAMA_BASE_URL}")
    print(f"{'='*70}\n")

    _gear_checkpoint("RUN_START", total_runs=total)

    for model in MODELS:
        model_tag = model.replace("/", "_")
        print(f"\n--- Model: {model} ---\n")
        _gear_checkpoint("MODEL", model=model)

        for task_key, task in TASKS.items():
            for var_key, variation in VARIATIONS.items():
                for pers_key, personality in PERSONALITIES.items():
                    completed += 1
                    run_key = f"{model_tag}__{task_key}__{var_key}__{pers_key}"
                    raw_file = RAW_DIR / f"{run_key}.json"

                    if raw_file.exists() and is_valid_result(raw_file):
                        skipped += 1
                        ok_count += 1
                        print(f"  [{completed:3d}/{total}] SKIP {var_key:12s} | {pers_key}")
                        continue

                    print(
                        f"  [{completed:3d}/{total}] {task_key:20s} | {var_key:12s} | {pers_key:22s}",
                        end="", flush=True,
                    )

                    system_prompt = build_system_prompt(pers_key, var_key)
                    result = call_with_fallback(model, system_prompt, task["prompt"])

                    provider_used = result.get("provider", "openrouter")
                    fallback_reason = result.get("fallback_reason", "")
                    if fallback_reason:
                        fallbacks += 1

                    run_record = {
                        "run_key": run_key,
                        "model": model,
                        "task": task_key,
                        "task_label": task["label"],
                        "variation": var_key,
                        "variation_label": variation["label"],
                        "personality": pers_key,
                        "personality_label": personality["label"],
                        "system_prompt": system_prompt,
                        "user_prompt": task["prompt"],
                        "response": result["content"],
                        "elapsed_seconds": result["elapsed_seconds"],
                        "word_count": result["tokens"],
                        "prompt_tokens": result.get("prompt_tokens", 0),
                        "completion_tokens": result.get("completion_tokens", 0),
                        "status": result["status"],
                        "provider": provider_used,
                        "fallback_reason": fallback_reason,
                    }

                    with open(raw_file, "w") as f:
                        json.dump(run_record, f, indent=2)

                    if result["status"] == "ok":
                        total_cost_tokens += result.get("prompt_tokens", 0) + result.get("completion_tokens", 0)
                        fb_tag = f" [fb:{provider_used}]" if fallback_reason else ""
                        print(f"  ✅ {result['tokens']:3d}w {result['elapsed_seconds']:5.1f}s{fb_tag}")
                        ok_count += 1
                    else:
                        print(f"  ❌ {result['status'][:60]}")
                        errors += 1

                    time.sleep(0.5)

    _gear_checkpoint("RUN_DONE", ok=ok_count, errors=errors, fallbacks=fallbacks)

    print(f"\n{'='*70}")
    print(f"  COMPLETE: {ok_count}/{total} OK | {errors} errors | {skipped} cached | {fallbacks} fallbacks")
    print(f"  Total tokens: ~{total_cost_tokens:,}")
    print(f"  Results: {RAW_DIR}")
    if _AGENTIC_KIT_AVAILABLE:
        print(f"  {_gear_summary()}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    run()

# Script Bench: Architectural Design Note

---

## What Makes a Good Short-Form Script?

A compelling short-form video script fundamentally respects the viewer's scarce attention. Unlike written articles or essays, short-form scripts operate under severe spatial and temporal constraints:

1. **The Hook Earns Attention**: The opening line is not an introductory greeting or preamble. It immediately introduces tension, curiosity, a counterintuitive observation, or a concrete consequence to earn the next several seconds of watch time.
2. **The Body Delivers One Clear Idea**: In 30 to 60 seconds, attempting to cover multiple topics produces rushed, superficial advice. A strong script isolates one central idea and explores it with depth.
3. **Mechanisms Make the Idea Concrete**: Abstract assertions ("multitasking hurts focus") are easily forgotten. Explaining the underlying mechanism (e.g. how residual attention lingers after an interruption) gives the viewer something concrete to understand and apply.
4. **Spoken Rhythm Matters**: Content written for speech direct-to-camera demands conversational pacing, natural contractions, and a balanced mix of short and medium sentences rather than polished prose.
5. **The Ending Closes Naturally**: A strong call-to-action is the logical culmination of the delivered idea—a single next step, reflection, or experiment—rather than a generic promotional formula.

---

## How Script Bench Approaches This

Script Bench translates these creative principles into an engineered pipeline:

```text
Creator Brief (niche, topic, seconds)
       ↓
Runtime Budget Calculation (words = seconds × 2.35, ±8%)
       ↓
5-Layer Constrained Prompt (role, rules, calibrated claims, section pacing)
       ↓
Structured JSON Generation (hook, body, cta via google-genai)
       ↓
Deterministic Validation (schema, non-empty fields, word budget bounds)
       ↓
Verified Output Contract
```

Rather than treating generation as an unconstrained pass-through (`prompt → LLM → output`), the system splits responsibility into distinct domains:
- **Creative & Linguistic Responsibility (LLM)**: Conceptual framing, conversational tone, niche-appropriate vocabulary, and contextual phrasing.
- **Constraint & Boundary Responsibility (Deterministic Code)**: Pre-generation input sanitization, runtime planning, schema verification, non-empty field checks, and post-generation word count enforcement.

---

## Key Design Judgment

> **A useful generator should not ask the model to solve every problem. The model is responsible for language and creative choices, while deterministic code handles constraints that software can verify reliably.**

Prompting an LLM to "keep it under 70 words and return valid JSON" often works, but soft prompting cannot provide architectural guarantees. By verifying schemas and word count ranges in code, Script Bench fails closed when an output violates structural rules, ensuring that downstream consumers receive guaranteed data contracts.

---

## Limitations & Deliberate Scope

1. **Approximate Runtime**: Word count is an effective proxy for speech duration, but human delivery varies with pauses, emphasis, and velocity. The budget functions as an engineering guardrail rather than an acoustic clock.
2. **LLM Stochasticity**: Prompt design reduces generic phrasing and copywriter clichés, but model outputs remain inherently probabilistic across runs.
3. **Imperfect Semantic Quality Detection**: Deterministic code can guarantee schema validity, non-empty strings, and word counts; evaluating subjective resonance, comedic timing, or rhetorical punch still requires human evaluation.
4. **Single-Candidate Generation**: Phase 1 generates a single verified candidate per request to maintain minimal complexity and rapid execution. Multi-candidate scoring is a planned Phase 2 evolution.

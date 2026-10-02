"""Tests for prompts.py: verifies prompt assembly, constraint inclusion, and guidance."""

from src.script_bench.models import ScriptRequest
from src.script_bench.planner import plan_runtime
from src.script_bench.prompts import build_prompt


def test_build_prompt_includes_inputs() -> None:
    """Prompt must include creator niche, topic, runtime, and word bounds."""
    request = ScriptRequest(
        niche="personal finance",
        topic="Automating emergency funds before lifestyle inflation hits",
        target_seconds=45,
    )
    plan = plan_runtime(request.target_seconds)
    prompt = build_prompt(request, plan)

    assert "personal finance" in prompt
    assert "Automating emergency funds before lifestyle inflation hits" in prompt
    assert "45 seconds" in prompt
    assert f"{plan.min_words}-{plan.max_words}" in prompt


def test_build_prompt_enforces_anti_cliche_and_spoken_rules() -> None:
    """Prompt must explicitly instruct spoken tone and discourage generic formulas."""
    request = ScriptRequest(
        niche="technology",
        topic="Why distributed systems need idempotency keys",
        target_seconds=60,
    )
    plan = plan_runtime(request.target_seconds)
    prompt = build_prompt(request, plan)

    # Core identity & spoken delivery
    assert "short-form video script writer" in prompt
    assert "Write for spoken delivery" in prompt or "spoken-language" in prompt.lower()

    # Discourages clichés & engagement tricks
    assert "Generic engagement tricks" in prompt or "generic" in prompt.lower()
    assert "Do you ever" in prompt or "cliché" in prompt.lower()
    assert "hook" in prompt.lower()
    assert "body" in prompt.lower()
    assert "cta" in prompt.lower()


def test_build_prompt_enforces_factual_precision_and_calibrated_claims() -> None:
    """Prompt must explicitly discourage universal absolute claims and enforce calibrated language."""
    request = ScriptRequest(
        niche="career",
        topic="Tailoring resumes for technical roles",
        target_seconds=45,
    )
    plan = plan_runtime(request.target_seconds)
    prompt = build_prompt(request, plan)

    # Factual precision & calibrated language guidance
    assert "calibrated" in prompt.lower()
    assert "absolute claims" in prompt.lower() or "universal" in prompt.lower()
    assert "statistics" in prompt.lower()


def test_build_prompt_enforces_cta_discipline() -> None:
    """Prompt must demand a concise single-sentence CTA that avoids re-explanation."""
    request = ScriptRequest(
        niche="productivity",
        topic="Limiting daily top priorities to three items",
        target_seconds=30,
    )
    plan = plan_runtime(request.target_seconds)
    prompt = build_prompt(request, plan)

    # CTA single action & length guidance
    assert "8–15 words" in prompt or "8-15 words" in prompt
    assert "single" in prompt.lower() or "one clear next step" in prompt.lower()


def test_build_prompt_contains_exact_json_shape() -> None:
    """Prompt must demand strict JSON format with hook, body, and cta."""
    request = ScriptRequest(
        niche="career",
        topic="How to showcase impact instead of responsibilities",
        target_seconds=30,
    )
    plan = plan_runtime(request.target_seconds)
    prompt = build_prompt(request, plan)

    assert '"hook": "..."' in prompt
    assert '"body": "..."' in prompt
    assert '"cta": "..."' in prompt
    assert "Return valid JSON only" in prompt or "Return exactly:" in prompt

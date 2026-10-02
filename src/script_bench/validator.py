"""Quality validation for script structure and runtime word budget."""

from typing import Any
from pydantic import ValidationError

from src.script_bench.models import ScriptOutput
from src.script_bench.planner import RuntimePlan


class ScriptValidationError(Exception):
    """Raised when generated script fails structural or word budget checks."""


def validate_script(raw_output: Any, plan: RuntimePlan) -> ScriptOutput:
    """Validate raw output against structure schema and runtime word budget.

    Layer 1 (Structure):
      - raw_output is a dict.
      - hook, body, and cta fields exist.
      - fields are non-empty strings.
      - matches ScriptOutput schema.

    Layer 2 (Runtime):
      - total words = words(hook) + words(body) + words(cta) must be within
        plan.min_words..plan.max_words.

    Args:
        raw_output: Parsed dictionary from LLM.
        plan: RuntimePlan containing word budget guardrails.

    Returns:
        Validated ScriptOutput instance.

    Raises:
        ScriptValidationError: If any structural or word budget constraint fails.
    """
    if not isinstance(raw_output, dict):
        raise ScriptValidationError(
            f"Expected script output to be a dictionary, got {type(raw_output).__name__}."
        )

    required_fields = ("hook", "body", "cta")
    for field in required_fields:
        if field not in raw_output:
            raise ScriptValidationError(f"Missing required field: '{field}'.")
        if not isinstance(raw_output[field], str):
            raise ScriptValidationError(
                f"Field '{field}' must be a string, got {type(raw_output[field]).__name__}."
            )
        if not raw_output[field].strip():
            raise ScriptValidationError(
                f"Field '{field}' must be a non-empty string."
            )

    try:
        output = ScriptOutput.model_validate(raw_output)
    except ValidationError as e:
        raise ScriptValidationError(f"Script output failed schema validation: {e}") from e

    hook_words = len(output.hook.split())
    body_words = len(output.body.split())
    cta_words = len(output.cta.split())
    total_words = hook_words + body_words + cta_words

    if total_words < plan.min_words or total_words > plan.max_words:
        raise ScriptValidationError(
            f"Total word count of {total_words} is outside the allowed range "
            f"[{plan.min_words}, {plan.max_words}] for target runtime of {plan.target_seconds}s "
            f"(hook: {hook_words}, body: {body_words}, cta: {cta_words})."
        )

    return output

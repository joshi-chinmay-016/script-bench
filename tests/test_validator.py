"""Tests for validator.py and model contracts."""

from pydantic import ValidationError
import pytest

from src.script_bench.models import ScriptOutput, ScriptRequest
from src.script_bench.planner import plan_runtime
from src.script_bench.validator import ScriptValidationError, validate_script


def test_invalid_schema() -> None:
    """Empty string fields violate schema requirements."""
    with pytest.raises(ScriptValidationError):
        validate_script({"hook": "", "body": "", "cta": ""}, plan_runtime(30))


def test_missing_field() -> None:
    """Missing required fields in output dictionary raises ScriptValidationError."""
    plan = plan_runtime(30)
    with pytest.raises(ScriptValidationError, match="Missing required field"):
        validate_script({"hook": "This is a hook.", "body": "This is the body."}, plan)


def test_non_string_field() -> None:
    """Non-string field values raise ScriptValidationError."""
    plan = plan_runtime(30)
    with pytest.raises(ScriptValidationError, match="must be a string"):
        validate_script(
            {"hook": 12345, "body": "Valid body text here.", "cta": "Follow for more."},
            plan,
        )


def test_word_count_below_range() -> None:
    """Output with word count below plan min_words raises ScriptValidationError."""
    plan = plan_runtime(30)  # range ~65-77 words
    raw = {
        "hook": "Here is a quick hook.",
        "body": "This is too brief to meet the minimum runtime word budget.",
        "cta": "Check the link.",
    }
    with pytest.raises(ScriptValidationError, match="outside the allowed range"):
        validate_script(raw, plan)


def test_word_count_above_range() -> None:
    """Output with word count exceeding plan max_words raises ScriptValidationError."""
    plan = plan_runtime(30)  # range ~65-77 words
    # Build 85 words
    long_body = " ".join(["word"] * 80)
    raw = {
        "hook": "This is a hook sentence.",
        "body": long_body,
        "cta": "Follow for more tips.",
    }
    with pytest.raises(ScriptValidationError, match="outside the allowed range"):
        validate_script(raw, plan)


def test_valid_output_within_range() -> None:
    """Output matching schema and word count budget succeeds and returns ScriptOutput."""
    plan = plan_runtime(30)  # range 65-77 words
    # 10 words + 55 words + 6 words = 71 words
    hook = "Stop scrolling if you want to fix your savings today."
    body = " ".join([
        "Most people try to save whatever money is left at the end of every single month.",
        "That almost never works because unexpected expenses always pop up.",
        "Instead, set an automatic transfer to move ten percent of your paycheck the day you get paid.",
        "You adapt to what remains and save consistently without thinking about it at all.",
    ])
    cta = "Try this for one month and see."

    total_words = len(hook.split()) + len(body.split()) + len(cta.split())
    assert plan.min_words <= total_words <= plan.max_words

    result = validate_script({"hook": hook, "body": body, "cta": cta}, plan)
    assert isinstance(result, ScriptOutput)
    assert result.hook == hook
    assert result.body == body
    assert result.cta == cta


def test_input_contract_target_seconds_bounds() -> None:
    """Target runtime below 15s or above 180s must be rejected."""
    with pytest.raises(ValidationError):
        ScriptRequest(niche="finance", topic="Saving money easily", target_seconds=14)

    with pytest.raises(ValidationError):
        ScriptRequest(niche="finance", topic="Saving money easily", target_seconds=181)

    # Valid boundaries
    req_min = ScriptRequest(niche="finance", topic="Saving money easily", target_seconds=15)
    assert req_min.target_seconds == 15

    req_max = ScriptRequest(niche="finance", topic="Saving money easily", target_seconds=180)
    assert req_max.target_seconds == 180


def test_input_contract_whitespace_stripping() -> None:
    """Whitespace on niche and topic must be stripped before length checks."""
    req = ScriptRequest(
        niche="  personal finance  ",
        topic="  I automated my savings and forgot about it   ",
        target_seconds=45,
    )
    assert req.niche == "personal finance"
    assert req.topic == "I automated my savings and forgot about it"

    # Whitespace-only string must fail min_length check after stripping
    with pytest.raises(ValidationError):
        ScriptRequest(niche="   ", topic="Valid topic here", target_seconds=30)

    with pytest.raises(ValidationError):
        ScriptRequest(niche="finance", topic="   ", target_seconds=30)

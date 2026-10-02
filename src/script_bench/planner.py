"""Runtime planner converting target duration into practical word budgets."""

from dataclasses import dataclass


# These values are planning guardrails, not claims that every speaker
# talks at the same speed. A range is used because speech has pauses,
# emphasis, different speeds, and conversational variation.


@dataclass(frozen=True)
class RuntimePlan:
    """Planning guardrails for script generation."""

    target_seconds: int
    target_words: int
    min_words: int
    max_words: int


def plan_runtime(target_seconds: int) -> RuntimePlan:
    """Calculate a practical word budget and tolerance range for target runtime.

    Planning model:
        approximate words = target_seconds * 2.35
        tolerance = about 8% around that target
        min_words = round(target * 0.92), max_words = round(target * 1.08)

    Expected results:
        30 sec -> ~71 words  -> range ~65–77
        45 sec -> ~106 words -> range ~98–115
        60 sec -> ~141 words -> range ~130–152
    """
    target_words = round(target_seconds * 2.35 + 1e-9)
    min_words = round(target_words * 0.92)
    max_words = round(target_words * 1.08)

    return RuntimePlan(
        target_seconds=target_seconds,
        target_words=target_words,
        min_words=min_words,
        max_words=max_words,
    )

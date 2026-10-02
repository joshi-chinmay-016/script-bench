"""Tests for planner.py: runtime planning and word budget calculations."""

from src.script_bench.planner import plan_runtime


def test_runtime_plan_30_seconds() -> None:
    """Ensure 30 seconds produces valid target and ascending bounds."""
    plan = plan_runtime(30)
    assert plan.target_seconds == 30
    assert plan.min_words < plan.max_words
    assert plan.min_words <= plan.target_words <= plan.max_words


def test_runtime_plan_ranges_30_45_60() -> None:
    """Verify that 30s, 45s, and 60s conform to the expected planning ranges.

    Expected:
        30 sec -> ~71 words  -> range ~65–77
        45 sec -> ~106 words -> range ~98–115
        60 sec -> ~141 words -> range ~130–152
    """
    plan_30 = plan_runtime(30)
    assert plan_30.target_words == 71
    assert 64 <= plan_30.min_words <= 66
    assert 76 <= plan_30.max_words <= 78

    plan_45 = plan_runtime(45)
    assert plan_45.target_words == 106
    assert 97 <= plan_45.min_words <= 99
    assert 113 <= plan_45.max_words <= 116

    plan_60 = plan_runtime(60)
    assert plan_60.target_words == 141
    assert 129 <= plan_60.min_words <= 131
    assert 151 <= plan_60.max_words <= 153

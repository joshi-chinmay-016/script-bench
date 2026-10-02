"""Orchestrator for the script generation process."""

from src.script_bench.models import ScriptOutput, ScriptRequest
from src.script_bench.planner import plan_runtime
from src.script_bench.prompts import build_prompt
from src.script_bench.provider import LLMProvider
from src.script_bench.validator import validate_script


class ScriptGenerator:
    """Orchestrates script generation: planning, prompting, LLM call, and validation."""

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def generate(self, request: ScriptRequest) -> ScriptOutput:
        """Run the end-to-end generation pipeline."""
        plan = plan_runtime(request.target_seconds)
        prompt = build_prompt(request, plan)
        raw_output = self.provider.generate_json(prompt)
        return validate_script(raw_output, plan)

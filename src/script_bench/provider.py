"""LLM provider abstraction and Gemini implementation."""

from abc import ABC, abstractmethod
import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


class ProviderError(Exception):
    """Raised when an LLM provider encounters an error or returns invalid output."""


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_json(self, prompt: str) -> dict[str, Any]:
        """Generate structured JSON output from a prompt.

        Args:
            prompt: Generation prompt text.

        Returns:
            Parsed dictionary from model response.

        Raises:
            ProviderError: If generation fails or output is not valid JSON.
        """
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Gemini LLM provider using the google-genai SDK."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "GEMINI_API_KEY environment variable is missing. "
                "Please set it in your environment or in a .env file."
            )
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = genai.Client(api_key=self.api_key)

    def generate_json(self, prompt: str) -> dict[str, Any]:
        """Request JSON from Gemini and parse it into a dictionary."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                ),
            )
        except Exception as e:
            raise ProviderError(f"Gemini API generation failed: {e}") from e

        text = response.text
        if not text:
            raise ProviderError("Gemini returned an empty response.")

        cleaned = text.strip()
        # Handle markdown fence stripping if necessary
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ProviderError(f"Failed to parse Gemini response as JSON: {e}") from e

        if not isinstance(parsed, dict):
            raise ProviderError(f"Expected JSON object (dict), but received {type(parsed).__name__}.")

        return parsed

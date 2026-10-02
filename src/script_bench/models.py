"""Data models and input/output contracts for Script Bench."""

from pydantic import BaseModel, Field, field_validator


class ScriptRequest(BaseModel):
    """Input contract for script generation."""

    niche: str = Field(min_length=2, max_length=100)
    topic: str = Field(min_length=5, max_length=500)
    target_seconds: int = Field(ge=15, le=180)

    @field_validator("niche", "topic", mode="before")
    @classmethod
    def strip_whitespace(cls, v: object) -> object:
        """Strip leading and trailing whitespace before length checks."""
        if isinstance(v, str):
            return v.strip()
        return v


class ScriptOutput(BaseModel):
    """Output contract for generated script."""

    hook: str = Field(min_length=1)
    body: str = Field(min_length=1)
    cta: str = Field(min_length=1)

    @field_validator("hook", "body", "cta", mode="before")
    @classmethod
    def strip_whitespace(cls, v: object) -> object:
        """Strip leading and trailing whitespace before length checks."""
        if isinstance(v, str):
            return v.strip()
        return v

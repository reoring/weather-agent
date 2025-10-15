import os
from dataclasses import dataclass, field
from enum import Enum


class ReasoningEffort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReasoningSummary(str, Enum):
    CONCISE = "concise"
    DETAILED = "detailed"


@dataclass
class ModelConfig:
    model_id: str | None = None
    reasoning_effort: ReasoningEffort = ReasoningEffort.LOW  # default to low
    reasoning_summary: ReasoningSummary | None = None

    def resolve_model_id(self) -> str:
        """Return model_id, falling back to environment and a sane default."""
        return (
            self.model_id
            or os.environ.get("OPENAI_RESPONSES_MODEL_ID")
            or os.environ.get("OPENAI_CHAT_MODEL_ID")
            or "gpt-5-nano"
        )

    def build_additional_chat_options(self) -> dict[str, dict[str, str]]:
        """Build additional_chat_options for Responses API, defaulting effort to 'low'."""
        reasoning: dict[str, str] = {"effort": self.reasoning_effort.value}
        if self.reasoning_summary:
            reasoning["summary"] = self.reasoning_summary.value
        return {"reasoning": reasoning}


@dataclass
class AppConfig:
    api_key: str | None = None
    env_file_path: str = ".env"
    model: ModelConfig = field(default_factory=ModelConfig)

    def resolve_api_key(self) -> str | None:
        return self.api_key or os.environ.get("OPENAI_API_KEY")

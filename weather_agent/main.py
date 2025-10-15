import asyncio
import os

from .agent import run_non_streaming, run_streaming
from .config import AppConfig, ModelConfig, ReasoningEffort, ReasoningSummary


async def main() -> None:
    print("=== Basic OpenAI Responses Agent Example ===")

    # Build config from environment (can be overridden by caller)
    model_cfg = ModelConfig(
        model_id=(
            os.environ.get("OPENAI_RESPONSES_MODEL_ID")
            or os.environ.get("OPENAI_CHAT_MODEL_ID")
            or "gpt-5-nano"
        ),
    )
    # Apply optional env overrides without clobbering defaults
    eff = os.environ.get("OPENAI_REASONING_EFFORT")
    if eff:
        try:
            model_cfg.reasoning_effort = ReasoningEffort(eff.lower())
        except ValueError:
            pass  # ignore invalid value, keep default
    summ = os.environ.get("OPENAI_REASONING_SUMMARY")
    if summ:
        try:
            model_cfg.reasoning_summary = ReasoningSummary(summ.lower())
        except ValueError:
            pass
    cfg = AppConfig(
        api_key=os.environ.get("OPENAI_API_KEY"),
        env_file_path=os.environ.get("ENV_FILE_PATH", ".env"),
        model=model_cfg,
    )

    print("=== Non-streaming Response Example (Responses API) ===")
    print("User: What's the weather like in Seattle?")
    result = await run_non_streaming(cfg)
    print(f"Agent: {result}\n")

    print("=== Streaming Response Example (Responses API) ===")
    print("User: What's the weather like in Portland?")
    print("Agent: ", end="", flush=True)
    async for text in run_streaming(cfg):
        print(text, end="", flush=True)
    print("\n")


def main_entry() -> None:
    asyncio.run(main())

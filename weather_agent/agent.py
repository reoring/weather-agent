from collections.abc import AsyncIterator
from random import randint
from typing import Annotated

from agent_framework import AgentRunResponse
from agent_framework.openai import OpenAIResponsesClient
from pydantic import Field

from .config import AppConfig


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return (
        f"The weather in {location} is {conditions[randint(0, 3)]} "
        f"with a high of {randint(10, 30)}°C."
    )


def create_agent(config: AppConfig):
    """Create an OpenAI Responses agent configured for the weather tool."""
    model_id = config.model.resolve_model_id()
    api_key = config.resolve_api_key()
    additional_chat_options = config.model.build_additional_chat_options()

    return OpenAIResponsesClient(
        env_file_path=config.env_file_path,
        model_id=model_id,
        api_key=api_key,
    ).create_agent(
        instructions="You are a helpful weather agent.",
        tools=get_weather,
        additional_chat_options=additional_chat_options,
    )


async def run_non_streaming(config: AppConfig) -> AgentRunResponse:
    agent = create_agent(config)
    query = "What's the weather like in Seattle?"
    result = await agent.run(query)
    return result


async def run_streaming(config: AppConfig) -> AsyncIterator[str]:
    agent = create_agent(config)
    query = "What's the weather like in Portland?"
    async for chunk in agent.run_stream(query):
        if chunk.text:
            yield chunk.text

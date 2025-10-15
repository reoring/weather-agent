## weather-agent

This is a minimal sample that uses the OpenAI Responses client (`agent_framework.openai.OpenAIResponsesClient`). You can run it with `uv`.

### Prerequisites
- Python 3.10+
- `uv` installed (if not installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Setup
```bash
uv sync
cp .env.example .env
# Open .env and set OPENAI_API_KEY and OPENAI_RESPONSES_MODEL_ID
```

Example `.env`:
```env
OPENAI_API_KEY=sk-...
OPENAI_RESPONSES_MODEL_ID=gpt-5-nano
# Optional
# OPENAI_ORG_ID=...
# OPENAI_BASE_URL=...
```

### Run
```bash
# Entry point (console_script)
uv run weather-agent

# Or run as a module
uv run python -m weather_agent.main
```

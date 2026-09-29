# pip install 'openai-agents[litellm]'
import asyncio
import json
import os
import sys
from datetime import datetime

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
import litellm


base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1/")
api_key = os.environ.get("OPENAI_API_KEY") or input(f"Enter your API key for {base_url}: ")
model = os.environ.get("OPENAI_MODEL", "litellm/openrouter/auto")

# The Agents SDK uses the Responses API by default. OpenRouter and many
# OpenAI-compatible gateways usually expose Chat Completions instead.
# Override with OPENAI_AGENTS_API=responses when using a compatible endpoint.
agents_api = os.environ.get("OPENAI_AGENTS_API", "chat_completions")
if agents_api not in {"chat_completions", "responses"}:
    raise ValueError("OPENAI_AGENTS_API must be either 'chat_completions' or 'responses'")

client = AsyncOpenAI(base_url=base_url, api_key=api_key)
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api(agents_api)
# Avoid trace export attempts when using non-OpenAI/proxy endpoints.
# Set OPENAI_AGENTS_TRACING=true to enable tracing explicitly.
set_tracing_disabled(os.environ.get("OPENAI_AGENTS_TRACING", "false").lower() != "true")

litellm._turn_on_debug()

@function_tool
def get_current_time() -> str:
    """Return the current local date and time of the machine running this CLI."""
    now = datetime.now()
    iso = now.isoformat(timespec='seconds')
    print(f"get_current_time called, returning {iso}", file=sys.stderr)
    return json.dumps({
        "iso": iso,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
    })


agent = Agent(
    name="CLI chat assistant",
    model=model,
    instructions=(
        "Just chat with the user, be friendly and helpful. Do not think. Just answer. "
        "When the user asks for the current time or date, call get_current_time. "
        "Do not guess the current time."
    ),
    tools=[get_current_time],
)


async def main() -> None:
    messages = []

    print(f"Using model: {model}")
    print(f"Using Agents API: {agents_api}")
    print("Type '/exit' or '/quit' to stop. Type '/retry' to retry the last message.")

    while True:
        try:
            user_text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_text:
            continue

        cmd = user_text.lower().strip()
        if cmd in {"/exit", "/quit"}:
            break

        if cmd not in {"/retry"}:
            messages.append({"role": "user", "content": user_text})

        try:
            result = await Runner.run(agent, input=messages)
            print(f"assistant> {result.final_output}")

            # Keep the SDK-normalized conversation history, including tool calls and
            # tool results, so follow-up turns have the full context.
            messages = result.to_input_list()
        except Exception as exc:
            print(f"error> {exc}")
            continue

    print("Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())

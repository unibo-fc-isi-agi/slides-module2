# pip install -U langchain langchain-openai

import json
import os
from datetime import datetime
from getpass import getpass
from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


PROVIDER_DEFAULTS: dict[str, dict[str, Any]] = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "model": "openrouter/auto",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
    },
    # Generic OpenAI-compatible endpoint: vLLM, LM Studio, llama.cpp server,
    # a company proxy, etc. Override OPENAI_BASE_URL and OPENAI_MODEL.
    "custom": {
        "base_url": "http://localhost:8000/v1",
        "api_key_env": "OPENAI_API_KEY",
        "model": "openai/gpt-oss-20b",
    },
}


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_json(name: str) -> dict[str, Any] | None:
    value = os.environ.get(name)
    if not value:
        return None
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return parsed


def build_llm() -> ChatOpenAI:
    provider = os.environ.get("LLM_PROVIDER", "openrouter").strip().lower()
    defaults = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["custom"])
    base_url = os.environ.get("OPENAI_BASE_URL", defaults["base_url"])
    model = os.environ.get("OPENAI_MODEL", defaults["model"])

    # Prefer provider-specific keys, but keep OPENAI_API_KEY as a universal fallback.
    provider_key_env = defaults["api_key_env"]
    api_key = (
        os.environ.get(provider_key_env)
        or os.environ.get("OPENAI_API_KEY")
        or getpass(f"Enter API key for {provider} at {base_url}: ")
    )

    kwargs: dict[str, Any] = {
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "temperature": float(os.environ.get("OPENAI_TEMPERATURE", "0.7")),
        "timeout": float(os.environ.get("OPENAI_TIMEOUT", "60")),
        "max_retries": int(os.environ.get("OPENAI_MAX_RETRIES", "2")),
    }

    if env_bool("OPENAI_DISABLE_STREAMING", False):
        kwargs["disable_streaming"] = True

    llm = ChatOpenAI(**kwargs)

    # Store these for startup display only. They are not part of LangChain's API.
    llm._cli_provider = provider  # type: ignore[attr-defined]
    llm._cli_base_url = base_url  # type: ignore[attr-defined]
    llm._cli_model = model  # type: ignore[attr-defined]
    return llm


@tool
def get_current_time() -> str:
    """Return the current local date and time of the machine running this CLI."""
    now = datetime.now()
    return json.dumps(
        {
            "iso": now.isoformat(timespec="seconds"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
        }
    )


def render_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False)


def last_ai_text(result: dict[str, Any]) -> str:
    messages = result.get("messages", [])
    for message in reversed(messages):
        message_type = getattr(message, "type", None)
        if message_type == "ai" or isinstance(message, AIMessage):
            return render_content(getattr(message, "content", ""))
    return render_content(result)


def main() -> None:
    llm = build_llm()
    tools = [get_current_time]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Just chat with the user, be friendly and helpful. Do not expose hidden "
            "reasoning. When the user asks for the current time or date, call "
            "get_current_time. Do not guess the current time."
        ),
    )

    messages: list[BaseMessage] = []

    print(f"Using provider: {getattr(llm, '_cli_provider', 'unknown')}")
    print(f"Using model: {getattr(llm, '_cli_model', 'unknown')}")
    print(f"Using base URL: {getattr(llm, '_cli_base_url', 'unknown')}")
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

        if cmd != "/retry":
            messages.append(HumanMessage(content=user_text))

        try:
            result = agent.invoke({"messages": messages})
            messages = list(result["messages"])
            print(f"assistant> {last_ai_text(result)}")
        except Exception as exc:
            print(f"error> {exc}")
            continue

    print("Goodbye!")


if __name__ == "__main__":
    main()

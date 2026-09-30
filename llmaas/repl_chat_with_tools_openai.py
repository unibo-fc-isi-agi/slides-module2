import json
import os
from datetime import datetime

from openai import OpenAI


base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1/")
api_key = os.environ.get("OPENAI_API_KEY") or input(f"Enter your API key for {base_url}: ")
model = os.environ.get("OPENAI_MODEL", "openrouter/auto")
client = OpenAI(base_url=base_url, api_key=api_key)


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


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time of the machine running this CLI.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    }
]

TOOL_FUNCTIONS = {
    "get_current_time": lambda args: get_current_time(),
}

messages = [
    dict(
        role="system",
        content=(
            "Just chat with the user, be friendly and helpful. Do not think. Just answer. "
            "When the user asks for the current time or date, call get_current_time. "
            "Do not guess the current time."
        ),
    )
]

print(f"Using model: {model}")
print("Type '/exit' or '/quit' to stop. Type '/retry' to retry the last message.")

try:
    while True:
        user_text = input("you> ").strip()
        if not user_text:
            continue
        if (cmd := user_text.lower().strip()) in {"/exit", "/quit"}:
            break
        if cmd not in {"/retry"}:
            messages.append(dict(role="user", content=user_text))

        try:
            while True:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                )
                message = response.choices[0].message
                tool_calls = message.tool_calls or []

                if not tool_calls:
                    answer = message.content or ""
                    print(f"assistant> {answer}")
                    messages.append(dict(role="assistant", content=answer))
                    break

                messages.append(
                    {
                        "role": "assistant",
                        "content": message.content,
                        "tool_calls": [tc.model_dump() for tc in tool_calls],
                    }
                )

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    raw_args = tool_call.function.arguments or "{}"
                    try:
                        args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        args = {}

                    function = TOOL_FUNCTIONS.get(function_name)
                    if function is None:
                        result = json.dumps({"error": f"Unknown tool: {function_name}"})
                    else:
                        result = function(args)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": result,
                        }
                    )
        except Exception as exc:
            print(f"error> {exc}")
            continue
except (EOFError, KeyboardInterrupt):
    pass
print("Goodbye!")
exit(0)

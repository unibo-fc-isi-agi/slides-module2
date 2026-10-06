# pip install langchain langchain-openai
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from simple_tools import instructions, tools

base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1/")
api_key = os.environ.get("OPENAI_API_KEY") or input(f"Enter your API key for {base_url}: ")
model = os.environ.get("OPENAI_MODEL", "openrouter/auto")

llm = ChatOpenAI(base_url=base_url, api_key=api_key, model=model)

agent = create_agent(llm, tools=tools, system_prompt=instructions)


def print_tool_calls(messages) -> None:
    for message in messages:
        for tool_call in getattr(message, "tool_calls", []):
            print(f"    [tool] {tool_call['name']}({tool_call['args']})")


if __name__ == "__main__":
    messages = []
    while True:
        try:
            messages.append(("user", input("You: ")))
        except (EOFError, KeyboardInterrupt):
            break
        result = agent.invoke({"messages": messages}, {"recursion_limit": 20})
        print_tool_calls(result["messages"][len(messages):])
        messages = result["messages"]
        print(f"AI: {messages[-1].content}")

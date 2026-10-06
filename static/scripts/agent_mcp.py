# pip install langchain langchain-openai langchain-mcp-adapters
import asyncio
import os
import pathlib
import sys
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from committee import instructions
from agent_langchain import llm, print_tool_calls

secrets = {k: v for k, v in os.environ.items() if k.startswith("OPENAI_")}  # needed by score_letter

mcp_client = MultiServerMCPClient({
    "committee": dict(
        transport="stdio",  # the server is a sub-process, talking via stdin/stdout
        command=sys.executable,
        args=[str(pathlib.Path(__file__).parent / "committee_mcp_server.py")],
        env=secrets,
    ),
    # more servers here, e.g. "fetch": dict(transport="stdio", command="uvx", args=["mcp-server-fetch"]),
})


async def main():
    tools = await mcp_client.get_tools()  # MCP: tools/list
    print(f"Tools: {[t.name for t in tools]}")
    agent = create_agent(llm, tools=tools, system_prompt=instructions)
    messages = []
    while True:
        try:
            messages.append(("user", input("You: ")))
        except (EOFError, KeyboardInterrupt):
            break
        result = await agent.ainvoke({"messages": messages}, {"recursion_limit": 20})
        print_tool_calls(result["messages"][len(messages):])
        messages = result["messages"]
        print(f"AI: {messages[-1].content}")


if __name__ == "__main__":
    asyncio.run(main())

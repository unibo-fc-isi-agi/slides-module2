# pip install pytest langchain langchain-openai
import functools
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent / "scripts"))  # i.e. <root dir>/scripts/

from agent_langchain import agent


@functools.cache
def trajectory(question: str) -> tuple[list[dict], str]:
    """Runs the agent on a question, returning the tool calls it made (in order) and its final answer."""
    messages = agent.invoke({"messages": [("user", question)]}, {"recursion_limit": 20})["messages"]
    tool_calls = [call for message in messages for call in getattr(message, "tool_calls", [])]
    return tool_calls, messages[-1].content


def test_time_in_tokyo():
    tool_calls, _ = trajectory("What time is it in Tokyo?")
    assert [(call["name"], call["args"]) for call in tool_calls] == [("get_current_time", {"timezone": "Asia/Tokyo"})]


def test_weather_in_bologna():
    tool_calls, _ = trajectory("Is it raining in Bologna right now?")
    assert [call["name"] for call in tool_calls] == ["get_weather"]  # exactly one call, no wasted steps
    assert "bologna" in tool_calls[0]["args"]["location"].lower()


def test_no_tools_when_not_needed():
    tool_calls, _ = trajectory("What is the capital of France?")
    assert tool_calls == []  # well-known facts need no tools


def test_unknown_location():
    _, answer = trajectory("What's the weather like in Xyzzyville?")
    assert not any(char.isdigit() for char in answer), "the agent must not invent temperatures"

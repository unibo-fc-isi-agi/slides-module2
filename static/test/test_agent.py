# pip install pytest langchain langchain-openai
import functools
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent / "scripts"))  # i.e. <root dir>/scripts/

from agent_langchain import agent
from committee import list_candidates

CANDIDATES = list_candidates()


@functools.cache
def trajectory(question: str) -> tuple[list[dict], str]:
    """Runs the agent on a question, returning the tool calls it made (in order) and its final answer."""
    messages = agent.invoke({"messages": [("user", question)]}, {"recursion_limit": 20})["messages"]
    tool_calls = [call for message in messages for call in getattr(message, "tool_calls", [])]
    return tool_calls, messages[-1].content


def test_lists_candidates():
    tool_calls, answer = trajectory("Who applied to the PhD programme?")
    assert [call["name"] for call in tool_calls] == ["list_candidates"]  # exactly one call, no wasted steps
    assert all(name in answer for name in CANDIDATES)


def test_valid_arguments():
    tool_calls, _ = trajectory("Which candidate has the best recommendation letter?")
    assert all(call["args"]["candidate"] in CANDIDATES for call in tool_calls if call["name"] != "list_candidates")


def test_scores_each_candidate_once():
    tool_calls, answer = trajectory("Which candidate has the best recommendation letter?")
    scored = [call["args"]["candidate"] for call in tool_calls if call["name"] == "score_letter"]
    assert sorted(scored) == sorted(CANDIDATES)  # all of them, once each
    assert "Mario Rossi" in answer


def test_focuses_on_one_candidate():
    tool_calls, answer = trajectory("Does the letter of Jean Dupont mention any weakness?")
    assert {call["args"].get("candidate") for call in tool_calls} <= {"Jean Dupont", None}
    assert tool_calls, "the answer must be grounded on some tool call"

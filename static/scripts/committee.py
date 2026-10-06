# Tools of the admission committee assistant: plain Python functions, documented for the LLM
import pathlib
from typing import Annotated
from pydantic import Field
from letter_scoring_langchain import score_letter as score_letter_text

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"  # i.e. <root dir>/data/

instructions = """
You are assisting the admission committee of University of Bologna PhD programmes.
Answer the committee's questions about the candidates, using the available tools.
Ground every claim on the tools' results: never guess candidates' data.
If the tools cannot answer a question, say so.
"""

Candidate = Annotated[str, Field(description="Full name of the candidate, exactly as returned by list_candidates")]


def list_candidates() -> list[str]:
    """List the full names of all candidates who applied to the PhD programme."""
    return [path.stem.removeprefix("letter-").replace("-", " ").title() for path in sorted(DATA_DIR.glob("letter-*.txt"))]


def read_letter(candidate: Candidate) -> str:
    """Read the recommendation letter of a candidate, as plain text."""
    if candidate not in list_candidates():  # never trust the LLM's arguments
        raise ValueError(f"Unknown candidate: {candidate!r}. Call list_candidates to get valid names.")
    return (DATA_DIR / f"letter-{candidate.lower().replace(' ', '-')}.txt").read_text()


def score_letter(candidate: Candidate) -> dict:
    """Score the recommendation letter of a candidate, from 0 (worst) to 5 (best), and extract structured
    information about the applicant and the author of the letter. Slow and costly: call it once per candidate."""
    return score_letter_text(read_letter(candidate)).model_dump()


tools = [list_candidates, read_letter, score_letter]

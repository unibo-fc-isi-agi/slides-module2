# pip install langchain-openai deepeval pytest
# run with: PYTHONPATH=../prompting pytest test_letter_scoring.py   (or: deepeval test run test_letter_scoring.py)
import functools
import os
import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import OpenRouterModel
from deepeval.test_case import LLMTestCase, SingleTurnParams
from golden import GOLDEN, read_letter
from letter_scoring_langchain import score_letter, api_key, base_url

score = functools.cache(score_letter)  # one LLM call per letter, shared by all tests


# 1. deterministic scorers: plain assertions on the fields of the structured output
@pytest.mark.parametrize("golden", GOLDEN, ids=lambda g: g["applicant"])
def test_extracted_fields(golden):
    info = score(read_letter(golden))
    assert golden["applicant"].lower() in info.applicant.name.lower()
    assert golden["author"].lower() in info.author.name.lower()
    assert golden["programme"].lower() in info.application_for.lower()
    assert golden.get("min_score", 0) <= info.score <= golden.get("max_score", 5)
    if "has_weaknesses" in golden:
        assert bool(info.applicant.weaknesses) == golden["has_weaknesses"]


# 2. relational property: holds across inputs, even if single scores may vary
def test_best_letter_is_mario_rossi():
    scores = {g["applicant"]: score(read_letter(g)).score for g in GOLDEN}
    assert scores["Mario Rossi"] == max(scores.values())


# 3. LLM-as-a-judge: a (different) model grades what is hard to check with code
judge = OpenRouterModel(model=os.environ.get("JUDGE_MODEL", "openai/gpt-oss-120b"), api_key=api_key, base_url=base_url)

groundedness = GEval(
    name="Groundedness",
    criteria="Every skill, strength, and weakness listed in the actual output must be explicitly supported by the letter in the input. "
             "Penalise any invented, exaggerated, or misattributed item.",
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    model=judge,
    threshold=0.7,
)

@pytest.mark.parametrize("golden", GOLDEN, ids=lambda g: g["applicant"])
def test_groundedness(golden):
    letter = read_letter(golden)
    info = score(letter)
    assert_test(LLMTestCase(input=letter, actual_output=info.applicant.model_dump_json()), [groundedness])

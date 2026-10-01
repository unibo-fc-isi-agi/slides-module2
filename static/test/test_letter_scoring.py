# pip install langchain-openai deepeval pytest pyyaml
# run with: pytest test/test_letter_scoring.py   (from the project root)
import functools
import os
import pathlib
import sys
import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import OpenRouterModel
from deepeval.test_case import LLMTestCase, SingleTurnParams
from dataset import TEST_CASES, read_letter
sys.path.append(str(pathlib.Path(__file__).parent.parent / "scripts"))  # makes <root dir>/scripts/ importable
from letter_scoring_langchain import score_letter, api_key, base_url

score = functools.cache(score_letter)  # this is the scoring function under test!


# 1. deterministic scorers: plain assertions on the fields of the structured output
@pytest.mark.parametrize("case", TEST_CASES, ids=lambda c: c["expectations"]["applicant"])
def test_extracted_fields(case):
    info, expected = score(read_letter(case)), case["expectations"]
    assert expected["applicant"].lower() in info.applicant.name.lower()
    assert expected["author"].lower() in info.author.name.lower()
    assert expected["programme"].lower() in info.application_for.lower()
    assert expected.get("min_score", 0) <= info.score <= expected.get("max_score", 5)
    if "has_weaknesses" in expected:
        assert bool(info.applicant.weaknesses) == expected["has_weaknesses"]


# 2. relational property: holds across inputs, even if single scores may vary
def test_best_letter_is_mario_rossi():
    scores = {c["expectations"]["applicant"]: score(read_letter(c)).score for c in TEST_CASES}
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

@pytest.mark.parametrize("case", TEST_CASES, ids=lambda c: c["expectations"]["applicant"])
def test_groundedness(case):
    letter = read_letter(case)
    info = score(letter)
    assert_test(LLMTestCase(input=letter, actual_output=info.applicant.model_dump_json()), [groundedness])

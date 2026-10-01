# pip install langchain-openai mlflow pyyaml
# run with: python test/evaluate_mlflow.py   (from the project root), then browse results with: mlflow ui
import os
import pathlib
import sys
from typing import Literal
import mlflow
from mlflow.genai import scorer
from mlflow.genai.judges import make_judge
from dataset import TEST_CASES, read_letter
sys.path.append(str(pathlib.Path(__file__).parent.parent / "scripts"))  # makes <root dir>/scripts/ importable
from letter_scoring_langchain import score_letter, base_url

# 1. the dataset: "inputs" are passed to predict_fn, "expectations" to the scorers
data = [dict(inputs=dict(letter_text=read_letter(c)), expectations=c["expectations"]) for c in TEST_CASES]

# 2. the system under test (outputs must be serialisable)
def predict_fn(letter_text: str) -> dict:
    return score_letter(letter_text).model_dump()

# 3. deterministic scorers
@scorer
def applicant_name(outputs, expectations) -> bool:
    return expectations["applicant"].lower() in outputs["applicant"]["name"].lower()

@scorer
def score_in_range(outputs, expectations) -> bool:
    return expectations.get("min_score", 0) <= outputs["score"] <= expectations.get("max_score", 5)

# 4. LLM-as-a-judge (the API key is read from OPENAI_API_KEY)
groundedness = make_judge(
    name="groundedness",
    instructions="The {{ inputs }} contain a recommendation letter, and the {{ outputs }} the information extracted from it. "
                 "Answer 'yes' if every skill, strength, and weakness in the outputs is explicitly supported by the letter, 'no' otherwise.",
    model=f"openai:/{os.environ.get('JUDGE_MODEL', 'openai/gpt-oss-120b')}",
    base_url=base_url,
    feedback_value_type=Literal["yes", "no"],
    generate_rationale_first=True,
)


if __name__ == "__main__":
    mlflow.set_experiment("letter-scoring")
    results = mlflow.genai.evaluate(data=data, predict_fn=predict_fn, scorers=[applicant_name, score_in_range, groundedness])
    print(results.metrics)

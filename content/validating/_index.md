+++

title = "[AgI] Validating Generative Software"
description = "How to evaluate LLM-based software: golden sets, deterministic scorers, LLM-as-a-Judge, with DeepEval and MLflow"
outputs = ["Reveal"]

+++

# Validating Generative Software

{{% import path="reusable/footer.md" %}}

---

## Outline

1. [The general concept](#/validation): why LLM-based software is hard to test, and what an _evaluation_ is made of
2. [LLM-as-a-Judge](#/llm-as-a-judge), and the [technological landscape](#/eval-frameworks) of evaluation frameworks
3. Examples: testing the letter evaluator with [DeepEval](#/test-deepeval) and [MLflow](#/evaluate-mlflow)
4. Exercise on the running example: [testing infrastructure](#/exercise-id-tests)

> Recall: we assume the reader is familiar with [structured outputs](../prompting/#/structured-output) and with the [running example](../prompting/#/running-example), from the previous lecture

---

{{% section %}}

{{< slide id="validation" >}}

## Validating generative software: the general concept

- LLM-based software is hard to test:
    + outputs are _non-deterministic_ (same input, different outputs)
    + outputs are _open-ended_ (many correct answers, no single expected value)
    + behaviour changes whenever the _prompt_, the _model_, or the _provider_ changes, even silently
- Hence, rather than _unit tests_, we need __evaluations__ (a.k.a. _evals_): measuring _how often_, and _how well_, the system behaves as expected, on a _dataset_ of representative inputs

- Ingredients of an evaluation:
    1. a __dataset__ of inputs, possibly with _expectations_ (a _golden set_, written by humans)
    2. the __system under test__ (prompt + model + code)
    3. __scorers__ (a.k.a. _metrics_), mapping each (input, output, expectation) to a _score_ or a _pass/fail_:
        * __deterministic__ scorers: schema validity, exact match, ranges, regular expressions, invariants and _relations_ among outputs
        * __statistical__ scorers: similarity to a reference (e.g. [BLEU](https://aclanthology.org/P02-1040/), [ROUGE](https://aclanthology.org/W04-1013/), embedding similarity)
        * __LLM-as-a-Judge__: another LLM grades the output, according to a natural language _rubric_
        * __humans__: the most reliable, and the most expensive
    4. an __aggregation__ (e.g. pass rate, mean score), to be compared across _versions_ of the system (_regression testing_)

- Structured outputs make evaluation _much_ easier: most fields can be checked with _code_

---

## Validating generative software: an intuitive example

{{< image src="./evaluation-pipeline.svg" max-h="65vh" alt="An evaluation pipeline: a golden set of three letters with expectations goes through the prompt template and model; outputs are checked by deterministic, relational and LLM-as-a-judge scorers, and the pass/fail report feeds back into the prompt" >}}

---

{{< slide id="llm-as-a-judge" >}}

## LLM-as-a-Judge

- Idea: use a (strong) LLM to _grade_ outputs, according to some _criteria_ (cf. [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685), and the survey by [Gu et al. (2024)](https://arxiv.org/abs/2411.15594))
    + _pointwise_ (grade one output on a scale), or _pairwise_ (which of two outputs is better?), with or without a _reference_ answer
    + the judge's prompt is a _rubric_, and its answer is (ideally) a __structured output__: score + rationale
    + asking for the _rationale first_ helps (cf. [chain-of-thought](../prompting/#/letter-tone)); [G-Eval](https://arxiv.org/abs/2303.16634) goes further, by first generating _evaluation steps_ from the criteria

- Known __biases__ of judges:
    + _position_ bias (preferring the first, or the second, option in pairwise comparisons), cf. [Wang et al. (2023)](https://arxiv.org/abs/2305.17926)
    + _verbosity_ bias (preferring longer answers), and _self-preference_ (preferring outputs of the _same_ model family)

- Good practices:
    + use a _different_ (and possibly stronger) model as judge, with _low_ temperature
    + prefer _narrow_, _binary_ criteria (e.g. "is every strength supported by the letter?") over vague ones (e.g. "is it good?")
    + __validate the judge__: compare its grades with _human_ grades, on a small sample, before trusting it
    + use judges only for what _cannot_ be checked with code

---

{{< slide id="eval-frameworks" >}}

## Evaluation frameworks: the technological landscape

| Tool | Style | Scorers / judges | Results in | Docs |
|---|---|---|---|---|
| [DeepEval](https://github.com/confident-ai/deepeval) | _unit-test_ like, on top of `pytest` | many built-in metrics (G-Eval, hallucination, RAG, agents), custom ones | terminal; optional cloud dashboard | [link](https://deepeval.com/docs/getting-started) |
| [MLflow](https://mlflow.org/) GenAI | _experiment_ tracking: runs, datasets, traces | code scorers (`@scorer`), built-in and custom judges (`make_judge`) | local (or remote) tracking server, with web UI | [link](https://mlflow.org/docs/latest/genai/eval-monitor/) |
| [promptfoo](https://www.promptfoo.dev/) | _declarative_ (YAML), CLI, language-agnostic | assertions, model-graded rubrics, red-teaming | terminal, local web UI | [link](https://www.promptfoo.dev/docs/intro/) |
| [OpenAI Evals](https://github.com/openai/evals) | registry of evals + platform | templates, model-graded | OpenAI dashboard | [link](https://developers.openai.com/api/docs/guides/evals) |
| [Ragas](https://docs.ragas.io/) | library of metrics | focused on _RAG_ and agents | Python objects, dataframes | [link](https://docs.ragas.io/) |
| [Inspect](https://inspect.aisi.org.uk/) | framework for _benchmarks_ and safety evals | solvers + scorers, model-graded | log viewer | [link](https://inspect.aisi.org.uk/) |
| [LangSmith](https://www.langchain.com/langsmith) | tracing + evals, by LangChain | code and LLM evaluators | cloud dashboard | [link](https://docs.langchain.com/langsmith/evaluation) |

- __Same metamodel__ everywhere: _dataset_ $\times$ _system under test_ $\rightarrow$ _outputs_ $\rightarrow$ _scorers_ $\rightarrow$ _report_
- __Differences__: _how_ datasets and scorers are declared (code vs. configuration), _where_ results go (terminal, local UI, cloud), and _batteries included_ (built-in metrics)

{{% /section %}}

---

{{% section %}}

{{< slide id="test-deepeval" >}}

## Example 1: Testing the Letter Evaluator with DeepEval (pt. 1)

> __Goal__: set up a _test suite_ for the [LangChain letter evaluator](../prompting/#/langchain) of Example 1 (bis) of the Prompt Engineering lecture

1. The __golden set__ is written by _humans_, and shared among test suites (full code [here](./golden.py)):

    {{% code path="content/validating/golden.py" from="5" to="17" %}}

    - notice that expectations are _partial_ and _tolerant_: e.g. _ranges_ for scores, "contains" for names

2. Imports: DeepEval runs on top of `pytest`, and the system under test is imported _as is_:

    {{% code path="content/validating/test_letter_evaluator.py" from="1" to="13" %}}

    - `functools.cache` avoids calling the LLM _once per test_: each letter is evaluated once, and outputs are shared

---

## Example 1: Testing the Letter Evaluator with DeepEval (pt. 2)

3. __Deterministic__ scorers are just `pytest` assertions on the _fields_ of the structured output:

    {{% code path="content/validating/test_letter_evaluator.py" from="16" to="25" %}}

4. __Relational__ properties hold _across_ inputs (a.k.a. _metamorphic_ testing): they are robust to the variability of single scores

    {{% code path="content/validating/test_letter_evaluator.py" from="28" to="31" %}}

---

## Example 1: Testing the Letter Evaluator with DeepEval (pt. 3)

5. __LLM-as-a-Judge__, via DeepEval's _G-Eval_ metric: the judge scores (in $[0, 1]$) how much the output satisfies the _criteria_, and the test passes if the score is above the _threshold_

    {{% code path="content/validating/test_letter_evaluator.py" from="34" to="50" %}}

    - the judge is a _different_ model than the one under test (set `JUDGE_MODEL` to change it)
    - `evaluation_params` selects which parts of the test case the judge can _see_

6. Let's run it (full code [here](./test_letter_evaluator.py)):

    ```bash
    pytest test_letter_evaluator.py -v
    ```

    - would the outputs of [Example 1 of the Prompt Engineering lecture](../prompting/#/letter-evaluator) pass? __No__: Mohammed Ali's shallow letter got score 4, whereas the committee expects at most 3
        * a test failure is _information_: fix the _prompt_ (e.g. with [Exercise 1 of the Prompt Engineering lecture](../prompting/#/exercise-checklist)), or the _model_, and re-run
    - run the suite _several times_: which tests are _flaky_? Flakiness is a _measure_ of the system's (in)consistency

{{% /section %}}

---

{{% section %}}

{{< slide id="evaluate-mlflow" >}}

## Example 1 (bis): Evaluating the Letter Evaluator with MLflow (pt. 1)

1. Same golden set, rearranged as MLflow wants it: `inputs` (for the system) + `expectations` (for the scorers)

    {{% code path="content/validating/evaluate_mlflow.py" from="1" to="16" %}}

    - the system under test is a _function_ (`predict_fn`), called with the `inputs` as keyword arguments

2. Deterministic scorers are _functions_ decorated with `@scorer`, whose parameters are _named_ after what they need (`inputs`, `outputs`, `expectations`, `trace`):

    {{% code path="content/validating/evaluate_mlflow.py" from="18" to="25" %}}

---

## Example 1 (bis): Evaluating the Letter Evaluator with MLflow (pt. 2)

3. The judge is created via `make_judge`, with _template variables_ in the instructions, and a _structured_ feedback type:

    {{% code path="content/validating/evaluate_mlflow.py" from="27" to="36" %}}

    - `generate_rationale_first=True`: rationale _before_ verdict (cf. [chain-of-thought](../prompting/#/letter-tone))
    - `model` is a URI (`<provider>:/<model>`); `base_url` redirects it to any OpenAI-compatible API

4. Evaluation is a _single call_, whose results are logged as an MLflow _run_ (full code [here](./evaluate_mlflow.py)):

    {{% code path="content/validating/evaluate_mlflow.py" from="39" to="42" %}}

    ```bash
    python evaluate_mlflow.py   # prints aggregated metrics, e.g. {'score_in_range/mean': 0.67, ...}
    mlflow ui                   # then open http://localhost:5000, to browse runs, traces, and judges' rationales
    ```

    {{< image src="./todo-mlflow-ui.png" max-h="25vh" alt="TODO picture: screenshot of the MLflow UI, 'letter-evaluator' experiment, 'Evaluations' tab of a run: a table with one row per letter (Mario Rossi, Jean Dupont, Mohammed Ali), columns for the inputs (truncated letter text), the outputs (truncated JSON), and one column per scorer (applicant_name, score_in_range, groundedness) with pass/fail or yes/no badges; the groundedness cell of one row is expanded, showing the judge's rationale." >}}

---

## DeepEval vs. MLflow: analogies and differences

| Aspect | DeepEval | MLflow GenAI |
|---|---|---|
| Mental model | _tests_: pass / fail, in CI | _experiments_: runs to be _compared_ over time |
| Dataset | test cases (`LLMTestCase`), or `pytest` parameters | list of dicts (`inputs`, `expectations`), dataframes, or managed datasets |
| System under test | called by you, inside the test | `predict_fn`, called by the framework (and _traced_) |
| Deterministic scorers | plain `assert`s | `@scorer` functions, returning `bool`, numbers, or `Feedback` |
| LLM judges | `GEval(criteria=..., threshold=...)`, plus many ready-made metrics | `make_judge(instructions=..., feedback_value_type=...)`, plus built-in judges |
| Judge model | `DeepEvalBaseLLM` subclasses (OpenAI, OpenRouter, Ollama, ...) | model URIs (`openai:/...`, `anthropic:/...`), plus `base_url` |
| Results | terminal (+ optional cloud platform) | tracking server + web UI (local, self-hosted, or managed) |
| Best for | _regression_ tests in CI pipelines | _comparing_ prompts / models, and _monitoring_ in production |

- Same _concepts_ (golden set, deterministic scorers, judges, aggregation), different _workflows_: the two can _coexist_ in a project

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-id-tests" >}}

## Exercise 1: Testing Infrastructure for ID Document Extraction (pt. 1)

> __Goal__: the committee wants _evidence_ that the extractor of [Exercise 2 of the Prompt Engineering lecture](../prompting/#/exercise-id-documents) is reliable, and wants to be _warned_ whenever a change in prompt or model makes it worse

{{% fragment %}}
### TO-DO List
1. build a __golden set__ from the 3 passports of the [running example](../prompting/#/running-example): for each picture, write down the _expected_ values of all fields (name, date of birth, ID number, expiration date)
2. pick a framework (DeepEval _or_ MLflow), and write __deterministic scorers__:
    + _exact match_ for ID numbers and dates, _normalised_ match for names (case, accents, order of first/family name)
    + _invariants_: date of birth < expiration date, candidate is of age, etc.
3. measure __consistency__: run the extractor $N$ times per picture, and report the _agreement rate_ per field
    + compare single queries vs. _majority voting_ (as in Exercise 2 of the Prompt Engineering lecture): does voting improve _accuracy_?
4. add an __LLM-as-a-Judge__ _only_ where code can't help (e.g. "is the document _legible_ enough to trust the extraction?"), and _validate_ it against your own judgement
5. run the suite with at least __two models__, and write down which one you'd pick, and why (cf. the [Governance lecture](../governance/#/compare-models))
{{% /fragment %}}

---

## Exercise 1: Testing Infrastructure for ID Document Extraction (pt. 2)

### Decision points and hints

- _Where_ should the golden set live? (code, YAML/JSON file, a managed dataset?) Who is allowed to change it?
- _Tolerance_: which fields must be exactly right, and which ones may be _flagged_ for human review instead?
- _Cost_: $N$ samples $\times$ 3 pictures $\times$ $M$ models $\times$ (1 + judge) requests: keep $N$ small while developing, and use `:free` models (cf. [Free Access to LLMs](../free-access/))
- _Flakiness_: a test that fails 1 time out of 10 is telling you something; consider asserting on _rates_ (e.g. "at least 4 out of 5 runs are correct") rather than on single runs
- Do __not__ cache LLM responses while measuring consistency (cf. [Exercise 1 of the LLM-as-a-Service lecture](../llmaas/))

### How to test it?

- deliberately _break_ the system (e.g. remove the field descriptions from the Pydantic class, or use a tiny model) and check that the suite _catches_ it
- run it in CI (e.g. GitHub Actions), with the API key stored as a _secret_

{{% /section %}}

---

## What's next?

- So far, the LLM only _reads_ and _writes_ text (or JSON), and we know how to _measure_ how well it does so
- Next, we'll let it __act__: calling _tools_ (functions) to get data or change the world, i.e. building __agents__
    + structured output is the _enabling_ technology: a tool call is nothing but a structured output, matching the tool's _signature_

---

{{% import path="reusable/back.md" %}}

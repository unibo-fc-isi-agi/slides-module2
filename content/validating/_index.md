+++

title = "[AgI] Validating Generative Software"
description = "How to evaluate LLM-based software: test datasets, deterministic scorers, LLM-as-a-Judge, with DeepEval and MLflow"
outputs = ["Reveal"]

+++

# Validating Generative Software

{{% import path="reusable/footer.md" %}}

---

## Outline

1. [The general concept](#/validation): why LLM-based software is hard to test, and what an _evaluation_ is made of
2. [LLM-as-a-Judge](#/llm-as-a-judge), and the [technological landscape](#/eval-frameworks) of evaluation frameworks
3. Examples: testing the letter-scoring system with [DeepEval](#/test-deepeval) and [MLflow](#/evaluate-mlflow)
4. Exercises on the running example: [complete the test suite of the letter-scoring system](#/exercise-all-fields), [testing infrastructure for ID documents extraction](#/exercise-id-tests)

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
    1. a __test dataset__: _known_ inputs, each with the _expected_ results (a.k.a. _expectations_), designed by _humans_ __before__ testing
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

{{< image src="./evaluation-pipeline.svg" max-h="65vh" alt="An evaluation pipeline: a test dataset of three letters with expectations goes through the prompt template and model; outputs are checked by deterministic, relational and LLM-as-a-judge scorers, and the pass/fail report feeds back into the prompt" >}}

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

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 1)

> __Goal__: set up a _test suite_ for the [LangChain letter-scoring system](../prompting/#/langchain) of Example 1 (bis) of the Prompt Engineering lecture, checking _some_ fields of the `LetterInfo` objects it produces

1. __First__, design the __test dataset__: _known_ inputs (the letters), each with the results _expected_ from a correct scoring
    + written by _humans_ (the committee), as a _data file_ ([`test_data.yml`](../lab-snippets/snippets/lecture_validating/test_data.yml)) shared among test suites

{{% multicol %}}
{{% col class="col-6"%}}
{{% code path="static/lab-snippets/snippets/lecture_validating/test_data.yml" %}}
- _adding_ a test case = adding an entry to the file, no code changes
{{% /col %}}
{{% col class="col-6" %}}
- notice that each expectation is meant for a specific _kind_ of check:
    * __exact__ match: names and emails
    * __tolerant__ match: _ranges_ for scores
    * __LLM-as-a-Judge__: _descriptions_ in natural language (e.g. the author's relationship with the applicant), as there are many correct ways to phrase them
- the file is loaded in Python as a list of `dict`s
    * full code [here](../lab-snippets/snippets/lecture_validating/dataset.py):

{{% code path="static/lab-snippets/snippets/lecture_validating/dataset.py" from="6" to="13" %}}
{{% /col %}}
{{% /multicol %}}

---

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 2)

2. Imports: DeepEval runs on top of `pytest`, and the system under test is imported _as is_:

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py" from="8" to="20" %}}

    - snippets are regular Python _packages_: the system under test is imported from the [prompting lecture's package](../lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py), with no further configuration
    - `functools.cache` accepts a Python function (`score_letter`) and returns a _cached_ version of it (`score`):
        1. each time `score(l)` is called, the cache checks if the same letter `l` has already been scored
        2. if yes, the cached output is returned; if not, the function `score_letter` is called and the output is cached
    - this approach allows to run multiple tests on the same letter without making multiple LLM calls
    - `for_each_case` is a _decorator_ making a test run once per test case (named after the applicant)

---

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 3)

3. __Deterministic__ scorers are just `pytest` assertions on _some_ fields of the structured output:

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py" from="23" to="34" %}}

    - names and emails must match _exactly_; scores may vary within a _range_

4. __Relational__ properties hold _across_ inputs (a.k.a. _metamorphic_ testing): they are robust to the variability of single scores

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py" from="37" to="40" %}}

---

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 4)

5. __LLM-as-a-Judge__, via DeepEval's _G-Eval_ metric: the judge scores (in $[0, 1]$) how much the output satisfies the _criteria_, and the test passes if the score is above the _threshold_

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py" from="43" to="62" %}}

    - the judge is a _different_ model than the one under test (set `JUDGE_MODEL` to change it)
    - `evaluation_params` selects which parts of the test case the judge can _see_:
        * _reference-based_ judge (`relationship`): compares the actual output with the _expected_ one, written by humans
        * _reference-free_ judge (`groundedness`): compares the actual output with the _input_, no expectation needed

---

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 5)

6. Judges are used within tests, via `assert_test`, on _test cases_ (`LLMTestCase`) built from _some_ fields of the structured output:

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py" from="64" to="74" %}}

    - `relationship_with_applicant` is compared with the _expected_ description
    - `skills`, `strengths`, and `weaknesses` are checked against the _letter_ (are they _grounded_ in it?)

---

## Example 1: Testing the Letter Scoring System with DeepEval (pt. 6)

7. Files of this example, in the [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) repository (cf. [how to set it up, and run snippets](../#/lab-snippets)):

    <div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
    ├── data/
    │   ├── <a href="../lab-snippets/data/letter-jean-dupont.txt">letter-jean-dupont.txt</a>               # inputs (running example)
    │   ├── <a href="../lab-snippets/data/letter-mario-rossi.txt">letter-mario-rossi.txt</a>
    │   ├── <a href="../lab-snippets/data/letter-mohammed-ali.txt">letter-mohammed-ali.txt</a>
    │   └── <a href="../lab-snippets/data/__init__.py">__init__.py</a>                          # helpers to locate data files
    ├── snippets/
    │   ├── lecture_prompting/
    │   │   └── example1bis/
    │   │       └── <a href="../lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py">letter_scoring_langchain.py</a>  # system under test
    │   └── lecture_validating/
    │       ├── example1/
    │       │   └── <a href="../lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py">test_letter_scoring.py</a>       # the test suite
    │       ├── <a href="../lab-snippets/snippets/lecture_validating/dataset.py">dataset.py</a>                       # loads the test dataset
    │       └── <a href="../lab-snippets/snippets/lecture_validating/test_data.yml">test_data.yml</a>                    # test dataset
    └── <a href="../lab-snippets/pyproject.toml">pyproject.toml</a>                           # dependencies of all snippets</code></pre></div>

    - set the environment variables `OPENAI_API_KEY` (and, optionally, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `JUDGE_MODEL`), cf. [Free Access to LLMs](../free-access/)

8. Let's run it (full code [here](../lab-snippets/snippets/lecture_validating/example1/test_letter_scoring.py)), from the project's root directory:

    ```bash
    poetry run python -m snippets -l validating -e 1 -v   # runs pytest on the test suite, with any option given
    ```

    - would the outputs of [Example 1 of the Prompt Engineering lecture](../prompting/#/letter-scoring) pass? __No__: Mohammed Ali's shallow letter got score 4, whereas the committee expects at most 3
        * a test failure is _information_: fix the _prompt_ (e.g. with [Exercise 1 of the Prompt Engineering lecture](../prompting/#/exercise-checklist)), or the _model_, and re-run
    - run the suite _several times_: which tests are _flaky_? Flakiness is a _measure_ of the system's (in)consistency

{{% /section %}}

---

{{% section %}}

{{< slide id="evaluate-mlflow" >}}

## Example 1 (bis): Evaluating the Letter Scoring System with MLflow (pt. 1)

1. Same test dataset, rearranged as MLflow wants it: `inputs` (for the system) + `expectations` (for the scorers)

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py" from="9" to="24" %}}

    - the system under test is a _function_ (`predict_fn`), called with the `inputs` as keyword arguments

2. Deterministic scorers are _functions_ decorated with `@scorer`, whose parameters are _named_ after what they need (`inputs`, `outputs`, `expectations`, `trace`):

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py" from="26" to="35" %}}

---

## Example 1 (bis): Evaluating the Letter Scoring System with MLflow (pt. 2)

3. Judges are created via `make_judge`, with _template variables_ in the instructions, and a _structured_ feedback type:

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py" from="37" to="54" %}}

    - `{{ expectations }}` makes the judge _reference-based_ (`relationship`), `{{ inputs }}` makes it _reference-free_ (`groundedness`)
    - `generate_rationale_first=True`: rationale _before_ verdict (cf. [chain-of-thought](../prompting/#/letter-tone))
    - `model` is a URI (`<provider>:/<model>`); `base_url` redirects it to any OpenAI-compatible API

---

## Example 1 (bis): Evaluating the Letter Scoring System with MLflow (pt. 3)

4. Evaluation is a _single call_, whose results are logged as an MLflow _run_ (named after the current date and time, in ISO format):

    {{% code path="static/lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py" from="57" to="64" %}}

    - `results.metrics` reports, for each scorer, the _fraction_ of test cases passing it (judges' `"yes"` count as 1)
    - if some scorer does not pass on _every_ test case, the script fails (non-zero exit code), just like a failing test suite

---

## Example 1 (bis): Evaluating the Letter Scoring System with MLflow (pt. 4)

5. Files of this example, in the [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) repository (cf. [how to set it up, and run snippets](../#/lab-snippets)):

    <div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
    ├── data/
    │   ├── <a href="../lab-snippets/data/letter-jean-dupont.txt">letter-jean-dupont.txt</a>               # inputs (running example)
    │   ├── <a href="../lab-snippets/data/letter-mario-rossi.txt">letter-mario-rossi.txt</a>
    │   ├── <a href="../lab-snippets/data/letter-mohammed-ali.txt">letter-mohammed-ali.txt</a>
    │   └── <a href="../lab-snippets/data/__init__.py">__init__.py</a>                          # helpers to locate data files
    ├── snippets/
    │   ├── lecture_prompting/
    │   │   └── example1bis/
    │   │       └── <a href="../lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py">letter_scoring_langchain.py</a>  # system under test
    │   └── lecture_validating/
    │       ├── example1bis/
    │       │   └── <a href="../lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py">evaluate_mlflow.py</a>           # the evaluation
    │       ├── <a href="../lab-snippets/snippets/lecture_validating/dataset.py">dataset.py</a>                       # loads the test dataset
    │       └── <a href="../lab-snippets/snippets/lecture_validating/test_data.yml">test_data.yml</a>                    # test dataset
    └── <a href="../lab-snippets/pyproject.toml">pyproject.toml</a>                           # dependencies of all snippets</code></pre></div>

    - set the environment variables `OPENAI_API_KEY` (and, optionally, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `JUDGE_MODEL`), cf. [Free Access to LLMs](../free-access/)

6. Let's run it (full code [here](../lab-snippets/snippets/lecture_validating/example1bis/evaluate_mlflow.py)), from the project's root directory:

    ```bash
    poetry run python -m snippets -l validating -e 1bis   # prints metrics, e.g. {'score_in_range/mean': 0.67, ...}, then: Failed scorers: [...]
    poetry run mlflow ui                                  # then open http://localhost:5000, to browse runs, traces, and judges' rationales
    ```

    {{< image src="./todo-mlflow-ui.png" max-h="25vh" alt="TODO picture: screenshot of the MLflow UI, 'letter-scoring' experiment, 'Evaluations' tab of a run: a table with one row per letter (Mario Rossi, Jean Dupont, Mohammed Ali), columns for the inputs (truncated letter text), the outputs (truncated JSON), and one column per scorer (names_and_email, score_in_range, relationship, groundedness) with pass/fail or yes/no badges; the groundedness cell of one row is expanded, showing the judge's rationale." >}}

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

- Same _concepts_ (test dataset, deterministic scorers, judges, aggregation), different _workflows_: the two can _coexist_ in a project

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-all-fields" >}}

## Exercise 1: Complete the Test Suite of the Letter Scoring System (pt. 1)

> __Goal__: the examples above only check _some_ fields of `LetterInfo`; extend _one_ of the two test suites (DeepEval _or_ MLflow, your choice) so that _every_ field is checked

> __Code__: put your solution in [`snippets/lecture_validating/exercise1/`](../lab-snippets/snippets/lecture_validating/exercise1/__init__.py) of [`lab-snippets`](../#/lab-snippets-exercises), and run it via `poetry run python -m snippets -l validating -x 1`

{{% fragment %}}
### TO-DO List
1. start from the [project](#/test-deepeval) of Example 1 (or 1 bis), and list the fields which are _not_ checked yet (cf. the `pydantic` classes in [`letter_scoring_langchain.py`](../lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py)):
    + `ApplicantInfo`: `degree`, `alma_mater`, `attended`
    + `AuthorInfo`: `affiliation`, `position`, `seniority`, `nationality`
    + `LetterInfo`: `application_for`
2. for each field, decide _how_ to check it, and _why_: __exact__ match, __tolerant__ match (normalisation, "contains", ranges, set inclusion, ...), or __LLM-as-a-Judge__ (reference-based or reference-free)
3. read the [letters](../prompting/#/running-example) _yourself_, and extend [`test_data.yml`](../lab-snippets/snippets/lecture_validating/test_data.yml) with the expectations for each field of each letter
4. write the corresponding scorers (tests, or `@scorer` functions, or judges), and run the suite
5. for each failure, decide whether the _system_ or the _expectation_ is wrong, and fix the right one
{{% /fragment %}}

---

## Exercise 1: Complete the Test Suite of the Letter Scoring System (pt. 2)

### Decision points and hints

- _Optional_ fields (e.g. `nationality`, `alma_mater`): what is the expected value when the letter does _not_ mention it? How do you write it in YAML?
- _Normalisation_: "Université de Lyon" vs. "University of Lyon", "Associate Professor" vs. "Assoc. Prof.": are they _the same_ for the committee?
- _Scales_: `seniority` is an integer, defined by the field's description: is the description _unambiguous_ for every letter?
- _Lists_ (e.g. `attended`): should every expected item be there? Should _every_ extracted item be expected? Is the _order_ relevant?
- _Cost_: one judge per field and per letter means many requests; could a _single_ judge check several fields at once? What would you lose?

### How to test it?

- deliberately _break_ an expectation in `test_data.yml` (e.g. a wrong affiliation), and check that the suite _catches_ it

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-id-tests" >}}

## Exercise 2: Testing Infrastructure for ID Document Extraction (pt. 1)

> __Goal__: the committee wants _evidence_ that the extractor of [Exercise 2 of the Prompt Engineering lecture](../prompting/#/exercise-id-documents) is reliable, and wants to be _warned_ whenever a change in prompt or model makes it worse

> __Code__: put your solution in [`snippets/lecture_validating/exercise2/`](../lab-snippets/snippets/lecture_validating/exercise2/__init__.py) of [`lab-snippets`](../#/lab-snippets-exercises), and run it via `poetry run python -m snippets -l validating -x 2`

{{% fragment %}}
### TO-DO List
1. __first__, design a __test dataset__ from the 3 passports of the [running example](../prompting/#/running-example): for each picture, write down the _expected_ values of all fields (name, date of birth, ID number, expiration date)
2. pick a framework (DeepEval _or_ MLflow), and write __deterministic scorers__:
    + _exact match_ for ID numbers and dates, _normalised_ match for names (case, accents, order of first/family name)
    + _invariants_: date of birth < expiration date, candidate is of age, etc.
3. measure __consistency__: run the extractor $N$ times per picture, and report the _agreement rate_ per field
    + compare single queries vs. _majority voting_ (as in Exercise 2 of the Prompt Engineering lecture): does voting improve _accuracy_?
4. add an __LLM-as-a-Judge__ _only_ where code can't help (e.g. "is the document _legible_ enough to trust the extraction?"), and _validate_ it against your own judgement
5. run the suite with at least __two models__, and write down which one you'd pick, and why (cf. the [Governance lecture](../governance/#/compare-models))
{{% /fragment %}}

---

## Exercise 2: Testing Infrastructure for ID Document Extraction (pt. 2)

### Decision points and hints

- _Where_ should the test dataset live? (code, YAML/JSON file, a managed dataset?) Who is allowed to change it?
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

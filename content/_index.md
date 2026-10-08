
+++

title = "About the course"
description = "Presentation of the course 'Intelligent Agents — Module 2'"
outputs = ["Reveal"]
aliases = [
    "/about/"
]

+++

{{% import path="reusable/front.md" %}}

---

{{< slide id="toc" >}}

## Table of Contents

1. [Generative AI 101](genai)
2. [LLM-as-a-Service](llmaas)
3. [Prompt Engineering & Structured Outputs](prompting)
4. [Validating Generative Software](validating)
5. [Tools and Agents](agents)
6. _Retrieval-Augmented Generation (RAG)_ (coming soon)
7. _Agentic Skills_ (coming soon)
8. _Workflows and Agent Orchestration_ (coming soon)
9. [AI Governance 101](governance)

__Appendices__

- [Free Access to LLMs](free-access)
- [Code of examples and exercises](#/lab-snippets): why, where, and how to run them

---

## Teachers

### Prof. Giovanni Ciatto
* email: [`giovanni.ciatto@unibo.it`](mailto:giovanni.ciatto@unibo.it)
* homepage: <https://www.unibo.it/sitoweb/giovanni.ciatto/en>
* office hours: by appointment (send me an email)

---

## Prioritize the {{< forum_general >}}

* All technical question
* Any other non-personal question

<p>

## When using the email
* Include *all* teachers in CC, **always**, there including prof. [Omicini](mailto:andrea.omicini@unibo.it)
* Clarify the _academic year_ and the _name of the course_ in the subject

---

{{< slide id="links" >}}

## Pages of the course

- [Institutional Page of the Course]({{< institutional_page_url >}})
- [Virtuale Page of the Course]({{< vle_url >}})
    + please enroll if you didn't already
- [APICe Page of the Course]({{< apice_url >}})
- [Code of examples and exercises]({{< github-url repo="lab-snippets" >}})
- [These slides](./)

---

{{% section %}}

{{< slide id="lab-snippets" >}}

## The code of examples and exercises: why a repository?

- All examples (and exercises) of the course live in a single repository: [`unibo-fc-isi-agi/lab-snippets`]({{< github-url repo="lab-snippets" >}})
    + slides only show _excerpts_: the repository contains the _full_, _commented_, _runnable_ code

- Why _one_ repository, rather than copy-pasting code from the slides?
    + examples __build upon each other__: the [running example](./prompting/#/running-example) grows across lectures
        * e.g. the letter-scoring system of the [prompting](./prompting/) lecture is the system under test of the [validating](./validating/) lecture
        * e.g. the tools of the [agents](./agents/) lecture are shared by several agents, local or via MCP
    + __one environment__ for all lectures: dependencies are declared once (`pyproject.toml`), and _locked_ (`poetry.lock`), so that everybody runs the _same_ versions of the _same_ libraries
    + __no copy-paste errors__: code on the slides _is_ the code in the repository (excerpts are taken from it)
    + __versioned__: fixes and updates (e.g. for libraries' breaking changes, or deprecated models) reach you via `git pull`
    + __checked__: a CI pipeline verifies that all snippets compile, and can be found by the runner
    + __exercises in place__: each exercise has its own (empty) package, where your solution can _import_ the examples' code

---

## The code of examples and exercises: directory structure

{{% multicol %}}
{{% col class="col-7" %}}
```text
lab-snippets/
├── data/                         # the running example's data
│   ├── __init__.py               # helpers to locate data files
│   ├── letter-<CANDIDATE>.txt
│   ├── passport-<CANDIDATE>.png
│   └── transcript-<CANDIDATE>.png
├── snippets/
│   ├── __init__.py               # utilities shared across lectures
│   ├── __main__.py               # the runner (python -m snippets)
│   └── lecture_<NAME>/           # one package per lecture
│       ├── <UTILITY>.py          # utilities shared within the lecture
│       ├── example<ID>/          # one package per example...
│       │   └── <DESCRIPTION>.py
│       └── exercise<ID>/         # ...and per exercise (placeholder)
├── pyproject.toml                # dependencies (Poetry)
├── poetry.lock                   # exact versions of dependencies
└── README.md                     # suggested order of lectures and exercises
```
{{% /col %}}
{{% col class="col-5" %}}
- `NAME`: the lecture's name, as in the URL of its slides
    + e.g. `llmaas`, `prompting`, `agents` (`free-access` becomes `free_access`)
- `ID`: the example's (or exercise's) number, as in the slides
    + e.g. `1`, `2`, ..., or `1bis` for "Example 1 (bis)"
- `CANDIDATE`: a candidate of the running example
    + e.g. `mario-rossi`, `jean-dupont`, `mohammed-ali`
- e.g. "Example 1 (bis)" of the [prompting](./prompting/) lecture lives in [`snippets/lecture_prompting/example1bis/`](./lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py)
- the [README]({{< github-url repo="lab-snippets" path="README.md" >}}) lists the _suggested order_ of lectures, examples, and exercises (which is _not_ always the order of IDs)
{{% /col %}}
{{% /multicol %}}

---

{{< slide id="lab-snippets-setup" >}}

## The code of examples and exercises: setup

1. Requirements: [Python](https://www.python.org/downloads/) 3.10+, and [Git](https://git-scm.com/downloads)

2. Clone the repository, and install its dependencies _once_, via [Poetry](https://python-poetry.org) (a dependency manager for Python):

    ```bash
    git clone https://github.com/unibo-fc-isi-agi/lab-snippets.git
    cd lab-snippets
    pip install -r requirements.txt  # installs Poetry, if missing
    poetry install                   # creates a virtual environment in .venv/, with all dependencies
    ```

    - _optionally_, [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the repository first, and clone your fork: you will be able to _commit_ (and push) your solutions to the exercises, and still `git pull` updates from the original repository

3. Configure the LLM provider via __environment variables__ (cf. [Free Access to LLMs](./free-access/)):
    + `OPENAI_API_KEY`: your API key (if missing, snippets ask for it interactively)
    + `OPENAI_BASE_URL` (default: `https://openrouter.ai/api/v1/`), `OPENAI_MODEL` (default: `openrouter/auto`)

    ```bash
    export OPENAI_API_KEY="sk-or-v1-..."     # on Windows (PowerShell): $env:OPENAI_API_KEY="sk-or-v1-..."
    ```

4. Open the repository's directory in your IDE (e.g. VS Code), and select the interpreter in `.venv/`

---

{{< slide id="lab-snippets-run" >}}

## The code of examples and exercises: running examples

- Always run snippets _from the root directory_ of the repository, via the __runner__, by lecture `NAME` and example `ID`:

    ```bash
    poetry run python -m snippets --lecture <NAME> --example <ID> [ARGS]
    poetry run python -m snippets -l <NAME> -e <ID> [ARGS]               # same, but shorter
    poetry run python -m snippets -l prompting -e 1bis data/letter-mario-rossi.txt   # e.g.
    ```

    - `ARGS` are passed to the snippet (each example's slides show which ones it accepts)
    - prefer the runner to `python path/to/snippet.py`: same command for every snippet, no paths to remember

- Don't remember the `ID`? List the snippets of a lecture (or all of them, omitting `-l`):

    ```text
    $ poetry run python -m snippets -l llmaas --list
    llmaas/example1: Example 1: Sync CLI Chat, with OpenAI's Chat Completions API.
         snippets/lecture_llmaas/example1/repl_chat_openai.py
    llmaas/example1bis: Example 1 (bis): the same CLI Chat, with Anthropic's Messages API (served by a local Ollama).
         snippets/lecture_llmaas/example1bis/repl_chat_anthropic.py
    llmaas/example2: Example 2: Async CLI Chat with Streaming, with OpenAI's Chat Completions API.
         snippets/lecture_llmaas/example2/repl_chat_openai_async.py
    llmaas/exercise1: Exercise 1: Caching Sync Requests.
    llmaas/exercise2: Exercise 2: Retry and Exponential Backoff.
    ```

- If more files match (e.g. an example made of several runnable files), the runner asks which one to run:

    ```text
    $ poetry run python -m snippets -l agents -e 2
    # Multiple snippets found, pick one:
    #    1) agents/example2/agent_mcp.py: Example 2: Simple Tools as an MCP Server (and an agent using it).
    #    2) agents/example2/simple_tools_mcp_server.py: Example 2: Simple Tools as an MCP Server (and an agent using it).
    # >
    ```

---

{{< slide id="lab-snippets-exercises" >}}

## The code of examples and exercises: working on exercises

- Each exercise has its own _placeholder_ package, e.g. [`snippets/lecture_llmaas/exercise1/`](./lab-snippets/snippets/lecture_llmaas/exercise1/__init__.py)
    + its `__init__.py` recalls the exercise's goal: put your solution in the _same_ directory (as one or more `.py` files)
    + each exercise's slides recall _where_ its solution goes, and _how_ to run it

- Run your solution like an example, but with `--exercise` (or `-x`) instead of `--example`:

    ```bash
    poetry run python -m snippets -l llmaas -x 1        # until you write some code: "Nothing to run in ..."
    ```

    - every `.py` file in the exercise's directory is runnable, except those starting with `_` (e.g. `_helpers.py`): use them for _private_ helpers

- Starting from an example? _Copy_ its file into the exercise's directory, then change the copy
    + the original remains available, for comparison (and for the others' exercises, which may build upon it)

- _Reuse_ the code of other snippets via __absolute imports__ (as snippets are regular Python packages):

    ```python
    from snippets.lecture_agents.simple_tools import tools                                    # a lecture-wide utility
    from snippets.lecture_prompting.example1bis.letter_scoring_langchain import score_letter  # an example
    import data                                                                               # the running example's data
    letter = data.letter("mario-rossi").read_text()
    ```

    - only import _modules_ whose main code is under `if __name__ == "__main__":` (others run as soon as they are imported!)

{{% /section %}}

---

# Lecture is Over

<br>

Compiled on: {{< today >}} --- [<i class="fa fa-print" aria-hidden="true"></i> printable version](?print-pdf&pdfSeparateFragments=false)

[<i class="fa fa-undo" aria-hidden="true"></i> back to ToC](./#/toc)

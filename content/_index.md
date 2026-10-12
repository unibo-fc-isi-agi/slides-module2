
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

{{% small %}}

0. [About the course](./) (this page):
    + [useful links](#/links) · [prerequisites](#/prerequisites) · [exam](#/exam) · [project work rules](#/rules)
1. [Generative AI 101](genai)
    + [check your understanding](genai/#/check-your-understanding)
2. [LLM-as-a-Service](llmaas)
    + exercise 1. [caching](llmaas/#/exercise-caching) ([solution](llmaas/#/exercise-caching-solution))
    · exercise 2. [retry & backoff](llmaas/#/exercise-retry) ([solution](llmaas/#/exercise-retry-solution))
    · [check your understanding](llmaas/#/check-your-understanding)
3. [Prompt Engineering & Structured Outputs](prompting)
    + exercise 1. [checklist scoring](prompting/#/exercise-checklist) ([solution](prompting/#/exercise-checklist-solution))
    · exercise 2. [ID documents](prompting/#/exercise-id-documents) ([solution](prompting/#/exercise-id-documents-solution))
    · [check your understanding](prompting/#/check-your-understanding)
4. [Validating Generative Software](validating)
    + exercise 1. [all fields](validating/#/exercise-all-fields) ([solution](validating/#/exercise-all-fields-solution))
    · exercise 2. [ID extraction tests](validating/#/exercise-id-tests) ([solution](validating/#/exercise-id-tests-solution))
    · [check your understanding](validating/#/check-your-understanding)
5. [Tools and Agents](agents)
    + exercise 1. [inspection tools](agents/#/exercise-inspect) ([solution](agents/#/exercise-inspect-solution))
    · exercise 2. [decision tools](agents/#/exercise-decide) ([solution](agents/#/exercise-decide-solution))
    · exercise 3. [MCP gateway](agents/#/exercise-gateway) ([solution](agents/#/exercise-gateway-solution))
    · [check your understanding](agents/#/check-your-understanding)
6. [Retrieval-Augmented Generation (RAG)](rag)
    + exercise 1. [Q/A about the slides](rag/#/exercise-slides-qa) ([solution](rag/#/exercise-slides-qa-solution))
    · [check your understanding](rag/#/check-your-understanding)
7. [Agentic Skills](skills)
    + exercise 1. [thesis pre-check](skills/#/exercise-thesis-precheck) ([solution](skills/#/exercise-thesis-precheck-solution))
    · [check your understanding](skills/#/check-your-understanding)
8. [Workflows and Agent Orchestration](workflows)
    + exercise 1. [e-mail bot](workflows/#/exercise-email-bot) ([solution](workflows/#/exercise-email-bot-solution))
    · exercise 2. [A2A agent](workflows/#/exercise-a2a) ([solution](workflows/#/exercise-a2a-solution))
9. [AI Governance 101](governance)
    + exercise 1. [comparing models](governance/#/compare-models) ([solution](governance/#/compare-models-solution))
    · exercise 2. [decision record](governance/#/decision-record) ([solution](governance/#/decision-record-solution))

10. \[Appendix] [Free Access to LLMs](free-access)

{{% /small %}}

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
- Support material for the [prerequisites](#/prerequisites):
    + [Python Programming 101](https://matteomagnini.github.io/distributed-systems-python-101/#/)
    + [Git basics](https://unibo-dtm-se.github.io/course-slides/dvcs-basics/#/)
    + [Shell basics](https://unibo-dtm-se.github.io/course-slides/preliminaries/#/)
    + [Free Access to LLMs](./free-access/) (how to get an API key, or run models locally)

---

## Organization of Module 2

- Lectures in lab, with immediate _hands-on_
- Examples and exercises in __Python__, all in the [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) repository
    * each exercise is followed by a (skippable) _walkthrough_ of its solution: try __before__ looking!
- _Optional_ __project work__ in any programming language of your choice (cf. [exam](#/exam) and [rules](#/rules))
    * report must be in English and follow [this LaTeX template]({{% final_report_template %}})

---

## Time—table

* cf. the [official timetable]({{< institutional_page_url >}}/orariolezioni)

Changes will be published on the {{< forum_news >}}

---

{{< slide id="exam" >}}

## Exam

> Detailed rules: [Exam page on APICe]({{% apice_url %}}?mode=data&data=course$&display=Exam)

- __Written test__ (_mandatory_, max __27/30__): closed-book, open-ended questions, in person on campus, on the university's computers
    + assesses the _theoretical_ knowledge (of both modules)
    + a [list of potential questions]({{< vle_url >}}) is available, and updated throughout the course
- __Project work__ (_optional_, max __6/30__): assesses the _practical_ knowledge
    + it should cover, or follow from, a _specific topic_ of the course
    + _theoretical_, _technological_, or _methodological_ (e.g. an analysis, a technology, a methodology)
- __Final score__ = written test + project, _capped_ at 30/30
    + after passing the written test (18/30 or higher), _tell the teachers_ whether you:
        1. _accept_ the result, skipping the project (exam finalised), or
        2. _continue_ with the project (finalisation postponed)

---

{{< slide id="rules" >}}

## Workflow for the project work (pt. 1)

> Detailed rules: [Exam page on APICe]({{% apice_url %}}?mode=data&data=course$&display=Exam)

1. **Propose** your project idea on the {{< forum_projects >}}
    + individual, or 1-3 students per _group_
        - groups must be _declared on [Virtuale]({{< vle_url >}})_ before starting, and stay _unchanged_ until the end
    + open a discussion thread named `[Surname1, Surname2, ...] Project Proposal: <your project name>`
    + please indicate:
        1. names and __email-addresses__ of the members of the group;
        2. the project _vision_, i.e. what you want to realise, eliciting the _functionalities_ of the envisioned system;
        3. a _motivation_ of why/how the project is letting you _explore_ the __topics of the course__ (e.g. structured outputs, tools, RAG, skills, orchestration, validation);
        4. _which technologies_ (programming languages, libraries, LLM providers and _models_) you intend to use and _why_;
        5. which _deliverable(s)_ you intend to produce (application, library, presentation, etc), __aside from the final report__;
        6. some strict _temporal constraint_, if any (e.g., someone in the group is going to graduate soon)

2. Any _subsequent communication_ on the project should be done on the __same thread__
    + use the thread as a _backlog_ of any official communication concerning the administration of your project work
    + if you want to talk _privately_ about your project work, _mention the URL_ of your project's thread in your email

3. __Wait__ for the teachers to _approve_ your proposal
    + the topic is _negotiated_, to ensure its focus on _Intelligent Agents_, and its feasibility in a reasonable time
    + most likely, we'll try to estimate the effort and ask for changes if too much or too little
    + we'll also check for overlaps with other groups

---

## Workflow for the project work (pt. 2)

4. Create a __GitHub repository__ where to develop your project and post the URL onto your project's thread
    + make all the _members_ of the group collaborators on the repository
    + give _full admin_ rights to the teachers:
        - Username: [`gciatto`](https://github.com/gciatto)

5. __Work__ on your project:
    + _commit_ and _push_ your changes often
        - only the `master` or `main` branch will be considered for the evaluation
    + __never__ commit API keys (read them from environment variables, as in [`lab-snippets`](#/lab-snippets-setup))
    + make the project _runnable by the teachers_: document how to install and run it, and which LLM provider/model it needs
        - prefer _free_ providers or _local_ models (cf. [Free Access to LLMs](./free-access/)), or let the model be configurable
    + _validate_ your system (cf. [Validating Generative Software](./validating/)), and report on how well it works
    + in parallel, or later, write a _report_ about your project following [this LaTeX template]({{% final_report_template %}})

6. Once done, post a _message_ on your _project's thread_ to signal the end of the work
    + we'll _clone_ your repository and evaluate the code

7. __Edits__ may be requested by the teachers, to either the code or the report (or both)

8. Once the teachers are satisfied, you'll be requested to __present__ your work to the teachers
    + all members of the group present _together_
    + about half an hour: _presentation_ + _discussion_
    + both the _software_ and the _report_ are evaluated

---

## Goals

- Teach you how to __design__, __develop__, and __validate__ _LLM-based_ agentic software, in practice...
- ... via a _running example_ (namely, an assistant for a [PhD admission committee](./prompting/#/running-example))
- Give you a _reference_ for developing your final __project work__

---

## Topics

- Generative AI and __LLMs__, consumed _as a service_ (APIs, costs, caching, retries)
- __Prompt engineering__ and _structured outputs_
- __Validating__ generative software (testing non-deterministic systems)
- __Tools__ and __agents__ (function calling, MCP)
- __Retrieval-Augmented Generation__ (RAG)
- Agentic __skills__
- __Workflows__ and agent _orchestration_ (A2A)
- AI __governance__ (regulation, model choice, costs)

---

{{< slide id="prerequisites" >}}

## Prerequisites

- Basic knowledge of __Python__ (see [Python Programming 101](https://matteomagnini.github.io/distributed-systems-python-101/#/) if missing)
    + including _type hints_, _virtual environments_, and (ideally) `async`/`await`
- Basic knowledge of __Git__ (see [these slides](https://unibo-dtm-se.github.io/course-slides/dvcs-basics/#/) if missing)
- Basic knowledge of the __Linux shell__ (see [these slides](https://unibo-dtm-se.github.io/course-slides/preliminaries/#/) if missing)
- Basic understanding of __HTTP__ APIs and __JSON__
- Basic notions of _machine learning_ and _neural networks_ (recalled in [Generative AI 101](./genai/))

---

## Software Requirements

### Required

* A working internet connection
* A working [Python](https://www.python.org/downloads/) 3.11+ installation, and [Git](https://git-scm.com/downloads)
* An __API key__ for some LLM provider, or a _local_ LLM runtime (cf. [Free Access to LLMs](./free-access/))

### Recommended

* _Visual Studio Code_ OR PyCharm
* A decent Unix terminal
    * prefer _Git Bash_ on Windows

---

{{% section %}}

{{< slide id="lab-snippets" >}}

## The code of examples and exercises: why a repository?

- All examples (and exercises) of the course live in a single repository: [`unibo-fc-isi-iag/lab-snippets`]({{< github-url repo="lab-snippets" >}})
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

1. Requirements: [Python](https://www.python.org/downloads/) 3.11+, and [Git](https://git-scm.com/downloads)

2. Clone the repository, and install its dependencies _once_, via [Poetry](https://python-poetry.org) (a dependency manager for Python):

    ```bash
    git clone -b exercises https://github.com/unibo-fc-isi-iag/lab-snippets.git   # the `exercises` branch!
    cd lab-snippets
    pip install -r requirements.txt  # installs Poetry, if missing
    poetry install                   # creates a virtual environment in .venv/, with all dependencies
    ```

    - _optionally_, [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the repository first, and clone your fork: you will be able to _commit_ (and push) your solutions to the exercises, and still `git pull` updates from the original repository

    - the `exercises` branch has _placeholders_ for exercises; the `master` branch has their _solutions_ (look at them only _after_ trying!)

3. Configure the LLM provider via __environment variables__ (cf. [Free Access to LLMs](./free-access/)):
    + `OPENAI_API_KEY`: your API key (if missing, snippets ask for it interactively)
    + `OPENAI_BASE_URL` (default: `https://openrouter.ai/api/v1/`), `OPENAI_MODEL` (default: `nvidia/nemotron-3-super-120b-a12b:free`, free)

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

    - `poetry run`: runs the command _inside_ the project's virtual environment (`.venv/`), with all dependencies available
    - `python -m snippets`: runs the `snippets` package as a program (i.e. its `__main__.py`, the runner)
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
    + each exercise's slides are followed by a (skippable) _walkthrough_ of its solution, available on the `master` branch

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

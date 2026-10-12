+++

title = "[IAg] Workflows and Agent Orchestration"
description = "When the code controls the flow: workflows as state machines, state and durable execution, patterns, intermediate representations, multi-agent systems and A2A, streaming and observability, end-to-end evaluation"
outputs = ["Reveal"]

+++

# Workflows and Agent Orchestration

{{% import path="reusable/footer.md" %}}

---

## Outline

1. [Workflows](#/workflows-concept): processes as _state machines_ over a shared state, made of LLM, data, action, and user-input _steps_
2. [State management](#/state): state schemas, checkpoints, _durable execution_, and humans as _interrupts_
3. [The technological landscape](#/workflows-landscape) of workflow engines
4. [A workflow](#/workflow-scratch) for the committee: [from scratch](#/workflow-scratch), then [with LangGraph](#/workflow-langgraph)
5. [Patterns](#/patterns): chaining, routing, parallelisation, orchestrator–workers, evaluator–optimizer, human-in-the-loop, [plan-and-execute](#/plan-and-execute)
6. [Intermediate representations](#/representations): from _intention_ to _execution_, through artefacts that can be _verified_
7. [Multi-agent systems](#/multi-agent): architectures, communication, and the [A2A protocol](#/a2a)
8. [Streaming and observability](#/observability): what is the workflow doing, _right now_, and what _did_ it do?
9. [Evaluating workflows](#/evaluating-workflows) end-to-end
10. Exercises on the [running example](#/running-example): [a bot for candidates' e-mails](#/exercise-email-bot), [the bot as an A2A agent](#/exercise-a2a)

> Recall: we assume the reader is familiar with [the spectrum of autonomy](../agents/#/autonomy-spectrum), [tools and agents](../agents/) (incl. [plan before acting](../agents/#/plan-before-acting)), [RAG](../rag/), [agentic skills](../skills/) (incl. [hooks](../skills/#/hooks)), and [validating generative software](../validating/)

---

{{< slide id="running-example" >}}

{{< import path="reusable/running-example.md" >}}

---

{{% section %}}

{{< slide id="workflows-concept" >}}

## Workflows: the general concept

> Recall: in the [spectrum of autonomy](../agents/#/autonomy-spectrum), __workflows__ orchestrate LLMs and tools along _predefined_ code paths (the _code_ controls the flow), while __agents__ let the LLM direct its own process

- A __workflow__ is a _process_: a set of __steps__, plus the __transitions__ among them, operating on a shared __state__
    + i.e. a _state machine_ (or a _graph_): nodes are steps, edges are transitions, possibly _conditional_ (guards on the state)
    + one _start_, one or more _ends_, possibly _loops_ (bounded!) and _parallel_ branches
- Each step _reads_ the state, does its job, and _updates_ the state; the __engine__ decides which step comes next
    + the LLM fills in _some_ steps (those that need _language_), it does __not__ decide the order
- Old idea, new ingredients: _business process management_ (cf. [BPMN](https://www.omg.org/spec/BPMN/2.0.2/)), _ETL pipelines_, _CI/CD pipelines_, ... now with __LLM steps__ in them
    + cf. [StateFlow](https://arxiv.org/abs/2403.11322) (Wu et al., 2024): modelling LLM-based task solving as state machines improves success rates _and_ reduces costs, w.r.t. ReAct-style agents

---

## Kinds of steps

| Kind | What it does | Deterministic? | Example (running example) |
|---|---|---|---|
| __LLM step__ | extracts, classifies, scores, drafts text | no | score a candidate's letter |
| __Data step__ | validates, computes, aggregates, retrieves (pure code) | yes | compute the GPA percentage, check eligibility |
| __Action step__ | has _side effects_ on the world (tools, APIs, files) | yes, but _irreversible_ | send an e-mail, record a decision |
| __User-input step__ | asks a _human_ to approve, correct, or choose | no (a human) | the committee approves the ranking |

- An __agent__ can be a step too: e.g. a ReAct loop answering an _open_ question, inside an otherwise _fixed_ process
- Rule of thumb: put in __data steps__ whatever code can do; use __LLM steps__ only where _language_ is needed; guard __action steps__ with checks, and (if irreversible or norm-sensitive) with __user-input steps__

---

{{< slide id="workflows-example" >}}

## Workflows: an intuitive example

{{< image src="./admission-workflow.svg" max-h="42vh" alt="The admission workflow as a graph: start, then one read-transcript LLM step per candidate in parallel, then check eligibility (data step: Master's degree, Art. 3); if some candidate is eligible, score letters (LLM step, eligible candidates only), then rank (data step: grade plus letter, Art. 8, top 2 to the interview); if nobody is eligible, straight to the committee approval; the committee approval is a user-input step (an interrupt: the run stops and resumes upon the answer); if approved, notify candidates (action step, idempotent e-mails), otherwise end with nothing sent. Underneath, the state (run, candidates, transcripts, problems, scores, ranking, approved, notified), saved after each step as a checkpoint" >}}

- The _same_ process, as an agent, would be a system prompt saying "_extract, check, score, rank, ask, notify_", hoping the LLM follows it, in that order, every time
- As a workflow (cf. the [spectrum of autonomy](../agents/#/autonomy-spectrum)):
    + __predictable__: same steps, same order, auditable step by step
    + __cheaper__: each LLM step sees _only_ what it needs, possibly with a smaller model
    + __testable__: steps in isolation, paths through the graph enumerable
    + __less flexible__: unforeseen requests need a _new version_ of the workflow
- vs. [skills](../skills/#/skills-vs-others): procedures owned by domain experts (skills) vs. reliable, auditable ones (workflows)

{{% /section %}}

---

{{% section %}}

{{< slide id="state" >}}

## State management (pt. 1): the state

- The __state__ is the workflow's _memory_ for a single run: a _typed_ record (e.g. a `TypedDict`, a dataclass, a Pydantic model)
    + steps return __partial updates__ (only the fields they change), which the engine _merges_ into the state
    + __reducers__ tell _how_ to merge: _overwrite_ (default), _append_ (e.g. lists of messages, of errors), _custom_ (e.g. max, union)
    + reducers matter for __parallel__ steps: two branches updating the same field at once must not _overwrite_ each other
- Keep the state __small__ and __serialisable__ (JSON-friendly): it is _saved_ after each step (see next slide), _logged_, and _shown_ to humans
    + store _references_ (paths, IDs) to large artefacts (pictures, documents), not the artefacts themselves
- The state is _not_ the LLM's context: each LLM step builds its own prompt from (part of) the state
    + cf. [context management](../prompting/#/context-management): workflows are _context engineering_ by construction

---

## State management (pt. 2): checkpoints and durable execution

{{< image src="./checkpoints.svg" max-h="38vh" alt="Checkpoints on a timeline: process A (e.g. Monday) runs read transcripts, check eligibility, score letters, rank, and the approval step, which interrupts; after each step a checkpoint (1 to 5) is saved into the checkpointer (e.g. SQLite) for thread T1, then the process exits and the question goes to the committee. Process B (e.g. Wednesday) resumes the same thread from the last checkpoint with Command(resume=yes): the approval step gets the answer, notify runs, and checkpoint 6 is saved. A crash during rank would resume from checkpoint 3, without processing transcripts and letters again; time travel re-runs from an earlier checkpoint, e.g. checkpoint 2 after fixing the scoring prompt" >}}

- A __checkpoint__ is a snapshot of the state (plus the _next_ steps), saved by a __checkpointer__ after each step, under a __thread__ ID
- __Durable execution__: a run can _pause_ (waiting for a human, for hours) or _crash_, and later __resume__ from its last checkpoint, possibly in another process
    + needs a _persistent_ checkpointer (e.g. SQLite, Postgres), not an in-memory one (cf. `InMemorySaver` in the [agents lecture](../agents/#/exercise-decide-solution))
    + also enables __time travel__: inspect past states, re-run from an earlier checkpoint (e.g. after fixing a prompt), _fork_ alternative runs
- Resuming may __re-execute__ (part of) the step that was running $\Rightarrow$ steps should be __idempotent__, or their side effects _recorded_ before being performed
    + e.g. `send_email` checks an _outbox_ before sending, so that a resumed run does not e-mail the same candidate twice

---

## State management (pt. 3): humans as interrupts

- A __user-input step__ is an _interrupt_: the workflow saves its checkpoint, _stops_, and returns a _question_ to its caller
    + the caller (a CLI, a Web UI, an e-mail, a ticketing system) shows it to a human, possibly much _later_
    + the human's answer __resumes__ the run (same thread ID), and becomes the _result_ of the user-input step
- Typical interrupts: __approve / reject__ an action, __edit__ a draft or the state, __choose__ among options, __provide__ missing information
- The interrupt lives in the __workflow__ (code), not in the prompt: the LLM _cannot_ skip it
    + recall: [human approval in the controller](../agents/#/exercise-decide-solution), for agents
    + cf. [hooks](../skills/#/hooks): both are deterministic code outside the LLM; hooks react to the agent's _events_, interrupts are _steps_ of the graph
- An interrupt is only as good as the human answering it: _over-trust_ (automation bias) turns approvals into rubber stamps (cf. [governance](../governance/#/responsibility))

{{% /section %}}

---

{{< slide id="workflows-landscape" >}}

## Workflows: the technological landscape

{{% small "65%" %}}

| Technology | Metamodel | State and persistence | Human-in-the-loop | Docs |
|---|---|---|---|---|
| [LangGraph](https://www.langchain.com/langgraph) | __graph__ of nodes (functions) and edges (incl. conditional), over a typed state with reducers; Pregel-style supersteps | checkpointers (memory, SQLite, Postgres), threads, time travel | `interrupt()` + `Command(resume=...)` | [link](https://docs.langchain.com/oss/python/langgraph/overview) |
| [LlamaIndex Workflows](https://www.llamaindex.ai/workflows) | __event-driven__: steps consume and emit typed events | `Context` store, serialisable (`to_dict` / `from_dict`) | `InputRequiredEvent` / `HumanResponseEvent` | [link](https://developers.llamaindex.ai/python/llamaagents/workflows/) |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | __graph__ of executors and edges; successor of AutoGen and Semantic Kernel (1.0 in 2026) | checkpoints | requests for human input | [link](https://learn.microsoft.com/en-us/agent-framework/) |
| [Google ADK](https://adk.dev/) | _workflow agents_ (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) composing LLM agents, with no LLM deciding the flow | sessions with shared state | via tools and callbacks | [link](https://adk.dev/agents/workflow-agents/) |
| [Pydantic Graph](https://ai.pydantic.dev/graph/) | __graph__ of nodes as dataclasses, edges as their return types | state persistence (memory, file), snapshots | stop, then resume from persistence | [link](https://ai.pydantic.dev/graph/) |
| [CrewAI Flows](https://docs.crewai.com/en/concepts/flows) | __event-driven__ methods (`@start`, `@listen`, `@router`) | flow state, persistence | [`@human_feedback`](https://docs.crewai.com/en/learn/human-feedback-in-flows) | [link](https://docs.crewai.com/en/concepts/flows) |
| [Temporal](https://temporal.io/), [Prefect](https://www.prefect.io/) | general-purpose __durable workflows__ as code (not LLM-specific) | event history, replay | signals, pauses | [link](https://docs.temporal.io/) |
| [n8n](https://n8n.io/) | __low-code__ visual graph of nodes (incl. LLM and agent nodes) | executions DB | wait / approval nodes | [link](https://docs.n8n.io/) |

{{% /small %}}

- Same _concepts_ (steps, transitions, state, persistence, interrupts), different _metamodels_: __graphs__ (explicit edges) vs. __events__ (implicit edges) vs. __composed agents__
- LLM-specific engines add _LLM-aware_ features (message reducers, token streaming, tool nodes); general-purpose engines (Temporal) bring _battle-tested_ durability, and are often _combined_ with the former

---

{{% section %}}

{{< slide id="workflow-scratch" >}}

## Example 1: a Workflow from Scratch (pt. 1)

> __Goal__: the [admission workflow](#/workflows-example), as a plain-Python _state machine_, with persistence and a human approval, _without_ any framework

1. The __state__ is a `TypedDict` (a `dict` with _declared_ keys and types; `total=False`: keys may be missing), in a module ([`admission.py`](../lab-snippets/snippets/lecture_workflows/admission.py)) shared with [Example 1 (bis)](#/workflow-langgraph):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/admission.py" from="18" to="26" %}}

---

## Example 1: a Workflow from Scratch (pt. 2)

2. __Steps__ are plain functions, taking the state and returning a _partial_ update, e.g. an LLM step and a data step:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/admission.py" from="39" to="40" %}}

    {{% code path="static/lab-snippets/snippets/lecture_workflows/admission.py" from="52" to="61" %}}

    - `extract_transcript(candidate)` and `score_letter(candidate)` call the functions of a lecture-wide module ([`committee.py`](../lab-snippets/snippets/lecture_workflows/committee.py)): a _vision_ LLM extracting degree and final grade from the transcript's picture (cf. [multimodal input](../prompting/#/exercise-id-documents)), and the [letter scoring](../prompting/#/letter-scoring) of the prompting lecture
    - `eligible(state)`: the candidates with no `problems`; letters are scored only for them
    - the second check is a __gate__ on the LLM's output: in one of our runs, a small vision model read "105/110" as 105510/110

---

## Example 1: a Workflow from Scratch (pt. 3)

3. More steps (full code [here](../lab-snippets/snippets/lecture_workflows/admission.py)): `rank` (data: points as in Art. 8, academic record + letter, top 2 invited), `approval_request` (the text shown to the committee), and an __idempotent__ action step:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/admission.py" from="96" to="103" %}}

    - one e-mail per _run_ and candidate: a run resumed after sending (part of) the e-mails does __not__ send them twice
    - `notify(state)` sends one e-mail per candidate (invited, not invited, not eligible), via `send_email`

4. The __user-input__ step _raises_ an `Interrupt` (a custom exception carrying the question), unless the answer is already in the state:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1/admission_scratch.py" from="20" to="29" %}}

---

## Example 1: a Workflow from Scratch (pt. 4)

5. The __graph__, as code: `STEPS` (not shown) maps each step's name onto its function, and a _transition function_ gives the edges (some of which are _conditional_), via Python's `match`:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1/admission_scratch.py" from="42" to="50" %}}

    - the graph is _implicit_ in the code: nothing checks it, nor draws it (cf. [Example 1 (bis)](#/workflow-langgraph))

---

## Example 1: a Workflow from Scratch (pt. 5)

6. The __engine__: run a step, merge its update, pick the next step, save a __checkpoint__ (`save`/`load` write/read a JSON file `{"next": step, "state": state}` per thread):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1/admission_scratch.py" from="64" to="79" %}}

    - `load(thread) or (...)`: _resume_ from the checkpoint, if any, otherwise _start_; `{**a, **b}`: a new `dict`, with `b`'s values overwriting `a`'s
    - an interrupt _saves_ and _returns_ the question: the process may even _exit_, and a later `run(thread, answer=...)` resumes the same step

---

## Example 1: a Workflow from Scratch (pt. 6)

7. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example1/admission_scratch.py)):

    ```bash
    poetry run python -m snippets -l workflows -e 1
    ```

    ```text
    # Thread: demo
        [step] read_transcripts
        [step] check_eligibility
        [step] score_letters
        [step] rank
        [step] approve
    Proposal of the workflow (candidates will be notified accordingly):
      1. mario-rossi: 38.6 points -> interview
      2. jean-dupont: 27.0 points -> interview
      -  mohammed-ali: NOT eligible, a Master's degree is required (Art. 3), found: 'Bachelor of Science'
    Do you approve it? [y/N] y
        [step] approve
        [step] notify
    # Done: final state in [...]/checkpoints/demo.json, e-mails in [...]/outbox
    ```

    (actual run, with `gemma4:e4b` via [Ollama](../llmaas/), for both text and vision, with `--thread demo`; notice `approve` running _twice_: the interrupted step is re-run upon resuming)

8. Things to observe:
    - press Ctrl+D at the approval question: the process _exits_; run again with `--thread <THREAD>`: no LLM call is repeated, the question is asked again
    - kill the process (Ctrl+C) _while_ the letters are being scored, then resume it: which steps are re-run?
    - answer `y`, then run `notify` again for the same thread (e.g. by editing the checkpoint's `"next"`): how many e-mails are in the outbox?
    - look at the checkpoint file after each step: the state is a _readable_ record of the run (cf. [log and trace](#/representations))

---

## Example 1: Project Structure

Files of this example, in the [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) repository (cf. [how to set it up, and run snippets](../#/lab-snippets)):

<div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
├── <a href="../lab-snippets/data/__init__.py">data/</a>                              # letters, transcripts (+ helpers)
├── snippets/
│   ├── lecture_prompting/
│   │   └── example1bis/
│   │       └── <a href="../lab-snippets/snippets/lecture_prompting/example1bis/letter_scoring_langchain.py">letter_scoring_langchain.py</a>  # letter scoring (reused)
│   └── lecture_workflows/
│       ├── <a href="../lab-snippets/snippets/lecture_workflows/committee.py">committee.py</a>               # transcript extraction, letter scoring, actions
│       ├── <a href="../lab-snippets/snippets/lecture_workflows/admission.py">admission.py</a>               # state and steps (shared with Example 1 bis)
│       └── example1/
│           └── <a href="../lab-snippets/snippets/lecture_workflows/example1/admission_scratch.py">admission_scratch.py</a>   # transitions, engine, checkpoints, CLI
└── <a href="../lab-snippets/pyproject.toml">pyproject.toml</a>                     # dependencies of all snippets</code></pre></div>

- set `OPENAI_API_KEY` (and, optionally, `OPENAI_BASE_URL`, `OPENAI_MODEL`), plus `VISION_MODEL` (a model supporting _images_), cf. [Free Access to LLMs](../free-access/)
- outputs (checkpoints, e-mails) go to `output/workflows/` (or wherever `WORKFLOWS_OUTPUT` says)

---

{{< slide id="workflow-langgraph" >}}

## Example 1 (bis): the same Workflow with LangGraph (pt. 1)

> __Goal__: the same workflow, with [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), reusing the same steps; transcripts are read in __parallel__

1. The state _extends_ the one of [Example 1](#/workflow-scratch), adding a __reducer__ for `transcripts`:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py" from="23" to="35" %}}

    - `Annotated[type, reducer]`: how updates of that field are _merged_; `operator.or_` is `|`, i.e. the _union_ of `dict`s
    - `Send(node, arg)`: run `node` on `arg` (its own small state); a list of `Send`s is a __fan-out__, i.e. parallel _branches_
    - `get_stream_writer()` emits _custom_ events (cf. [Example 5](#/observability-example)); here, a no-op unless someone streams them

2. The user-input step calls `interrupt(value)`: the run _stops_ here, `value` goes to the caller; upon resuming, `interrupt` _returns_ the answer

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py" from="38" to="40" %}}

---

## Example 1 (bis): the same Workflow with LangGraph (pt. 2)

3. The graph is _declared_: nodes, edges, and conditional edges (functions of the state returning the next node, plus the _possible_ targets):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py" from="43" to="64" %}}

    - `START`, `END`: the virtual first and last nodes; `compile` checks the graph, and returns a _runnable_ (`invoke`, `stream`, ...)
    - `SqliteSaver`: a __persistent__ checkpointer, saving a checkpoint after each _superstep_ (a set of nodes run in parallel)
    - `"read_transcript" → "check_eligibility"`: the engine waits for _all_ the branches, merging their updates via the reducer

---

## Example 1 (bis): the same Workflow with LangGraph (pt. 3)

4. The CLI: a `thread_id` selects the checkpoints; a thread stopped at an interrupt is _resumed_ via `Command(resume=answer)`:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py" from="81" to="92" %}}

    - `get_state(config)` reads the last checkpoint of the thread; `.interrupts` lists the pending ones
    - a result containing `"__interrupt__"` means: stopped, waiting for an answer (`.value` is what `interrupt` was given)

5. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py)), possibly printing the graph first:

    ```bash
    poetry run python -m snippets -l workflows -e 1bis --mermaid
    poetry run python -m snippets -l workflows -e 1bis
    ```

    the printed graph is shown in the next slide

6. Project structure: as in [Example 1](#/workflow-scratch), with [`example1bis/admission_langgraph.py`](../lab-snippets/snippets/lecture_workflows/example1bis/admission_langgraph.py) in place of `example1/admission_scratch.py`

---

## Example 1 (bis): the graph, as drawn by LangGraph

{{< mermaid >}}
%%{init: {'flowchart': {'htmlLabels': false}}}%%
flowchart LR
    S([start]) -.->|"one Send per candidate"| RT[read_transcript]
    RT --> CE[check_eligibility]
    CE -.-> SL[score_letters]
    CE -.-> A[approve]
    SL --> R[rank]
    R --> A
    A -.-> N[notify]
    N --> E([end])
    A -.-> E
{{< /mermaid >}}

- What `--mermaid` prints (`get_graph().draw_mermaid()`), with fewer styling details: compare it with the [hand-drawn one](#/workflows-example)
- Dashed edges are the _conditional_ ones: their possible targets come from the lists passed to `add_conditional_edges`

---

## From scratch vs. LangGraph: analogies and differences

| Aspect | From scratch | LangGraph |
|---|---|---|
| State | `TypedDict`, merged with `{**state, **update}` | `TypedDict` (or Pydantic), merged by _reducers_ |
| Transitions | a function (`match` on the step) | edges and conditional edges, _declared_ |
| Parallelism | up to you (threads, `asyncio`) | `Send` (fan-out), supersteps, reducers (fan-in) |
| Persistence | a JSON file per thread | checkpointers (memory, SQLite, Postgres), threads, history |
| Human input | an exception + the answer in the state | `interrupt()` + `Command(resume=...)` |
| Visualisation | none | `get_graph().draw_mermaid()` |
| Streaming, tracing | up to you | built-in (cf. [Example 5](#/observability-example)) |

- Same _concepts_ (state, steps, transitions, checkpoints, interrupts), different _effort_: the engine is ~30 lines, yet _durability_, _parallelism_, and _streaming_ are where frameworks pay off
- The _steps_ did not change at all: keep them as plain, testable functions, independent of the engine

{{% /section %}}

---

{{% section %}}

{{< slide id="patterns" >}}

## Workflow patterns: a catalogue

{{< image src="./patterns.svg" max-h="62vh" alt="Seven workflow patterns: prompt chaining (LLM 1, a gate in code, LLM 2; a failing check stops the chain), routing (an LLM router picks one of several routes), parallelisation (split, several LLM calls in parallel, merge or vote), orchestrator-workers (an LLM orchestrator decides how many workers, then a synthesizer combines their results), evaluator-optimizer (a generator and a judge in a bounded loop, until accepted or N rounds), human-in-the-loop (draft, then a human approves, edits, or rejects, before acting), plan-and-execute (plan, validate in code, human approval, execution, then re-planning seeing the results); legend: LLM steps, data steps, user-input steps, action steps, conditional edges" >}}

- A _small_ set of building blocks, which _compose_ (cf. Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))
- We already met some of them: [prompt chaining](../prompting/#/prompting-techniques) and [self-consistency](../prompting/#/prompting-techniques) (voting), [human approval](../agents/#/exercise-decide-solution), [LLM-Modulo](../agents/#/llm-modulo)

---

## Workflow patterns: when to use which

{{% small "70%" %}}

| Pattern | Use when | Costs and risks | Running example |
|---|---|---|---|
| __Prompt chaining__ | the task splits into _fixed_ sub-tasks; _gates_ (checks in code) between them | latency adds up | extract $\rightarrow$ check $\rightarrow$ score |
| __Routing__ | inputs fall into _distinct categories_, each with its own handling (or model) | misrouting: log and test the router | classify candidates' e-mails ([Exercise 1](#/exercise-email-bot)) |
| __Parallelisation__ | sub-tasks are _independent_ (sectioning), or confidence is needed (voting) | cost $\times N$ | read all transcripts at once ([Example 1 bis](#/workflow-langgraph)); vote on extracted fields |
| __Orchestrator–workers__ | sub-tasks are _not known_ in advance: an LLM decides them, workers execute | less predictable | the supervisor of [Example 4](#/multi-agent-example), delegating ad-hoc sub-questions to the documents and regulations workers |
| __Evaluator–optimizer__ | clear _evaluation criteria_, and iterations measurably help | loops: _bound_ them | feedback letters, refined until a judge accepts them |
| __Human-in-the-loop__ | irreversible, norm-sensitive, or high-stakes actions | latency (hours!); [over-trust](../governance/#/responsibility) | committee approval before notifying |
| __Plan-and-execute__ | multi-step tasks whose steps vary, but must be _checked_ before acting | planning errors: _validate_ plans | ad-hoc requests of the committee |

{{% /small %}}

- Rule of thumb: start with the _simplest_ pattern that does the job; add loops, orchestrators, and planners only when evaluations show it is _needed_ (cf. the [technique selection](../rag/#/technique-selection) rule of thumb)
- References: [Self-Refine](https://arxiv.org/abs/2303.17651) (evaluator–optimizer), [Plan-and-Solve](https://arxiv.org/abs/2305.04091), [ReWOO](https://arxiv.org/abs/2305.18323), [LLMCompiler](https://arxiv.org/abs/2312.04511) (plan-and-execute)

---

{{< slide id="patterns-example" >}}

## Example 2: Routing, Parallelisation, and Evaluator–Optimizer (pt. 1)

> __Goal__: after the committee's decisions, write a _personalised_ feedback e-mail to each candidate, good enough to be sent

1. The committee's __decisions__ are the _only_ facts e-mails may mention; __routing__: one set of instructions per decision

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py" from="21" to="31" %}}

2. The state of each __worker__ (one per candidate) keeps _every_ draft and critique (`operator.add` concatenates lists): the process is _auditable_

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py" from="34" to="47" %}}

    - `Verdict` is the judge's structured output: a __checklist__, one boolean per criterion (cf. the [letter-scoring checklist](../prompting/#/exercise-checklist)); the _issues_ and the acceptance are derived by code
    - why not a list of `issues`? In our runs, a small judge filled it with "None", "N/A", or "the e-mail passes all criteria": nothing was ever accepted

---

## Example 2: Routing, Parallelisation, and Evaluator–Optimizer (pt. 2)

3. __Evaluator–optimizer__: the drafter writes (or _fixes_) the e-mail, the judge fills in the checklist; the descriptions of the failed criteria go back to the drafter

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py" from="50" to="71" %}}

    - `drafter(decision)` is a _factory_: it returns a node function, one per decision; `llm` is the chat model of the [agents lecture](../agents/#/agent-langchain)
    - the loop is __bounded__ (`MAX_ROUNDS = 3`): when the judge never accepts, the last draft is returned, flagged as _not accepted_

---

## Example 2: Routing, Parallelisation, and Evaluator–Optimizer (pt. 3)

4. The __worker__ graph: routing at the start, then the draft ⇄ judge loop; the __main__ graph fans out one worker per candidate (__parallelisation__, by _sectioning_):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py" from="74" to="99" %}}

    - a compiled graph is a _runnable_: here, `worker.invoke(...)` runs _inside_ a node of another graph (a __subgraph__)
    - here, the _code_ decides the sub-tasks (one per candidate); in _orchestrator–workers_, an _LLM_ would decide them (cf. the supervisor of [Example 4](#/multi-agent-example))

---

## Example 2: Routing, Parallelisation, and Evaluator–Optimizer (pt. 4)

5. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py)):

    ```bash
    poetry run python -m snippets -l workflows -e 2
    ```

    ```text
    ===== mario-rossi (interview): 1 round(s), accepted: True
        [judge, round 1] no issues
    [...]
    ===== jean-dupont (interview): 1 round(s), accepted: True
        [judge, round 1] no issues
    Dear Jean-Dupont,
    We are writing to you on behalf of the PhD Admission Committee.
    Based on your excellent academic record (14.7/20), and noting the need for close supervision mentioned in your letter,
    we are pleased to invite you to an interview with the committee. [...]
    ===== mohammed-ali (reject): 1 round(s), accepted: True
    [...]
    ```

    (actual run, with `gemma4:e4b` via [Ollama](../llmaas/): the motivation said "_good_ academic record", the e-mail says "_excellent_", and the judge accepted it)

6. Things to observe:
    - how many rounds per candidate? Are the judge's issues _real_ ones, or nitpicks? Does the judge ever accept a _bad_ e-mail? (cf. [LLM-as-a-Judge](../validating/#/llm-as-a-judge) and its biases)
    - do the e-mails ever invent dates, grades, or promises? Would a _code_ check catch some of them (e.g. numbers not in the facts)?
    - try a _weaker_ drafter, or a _stronger_ judge: which one matters more?

7. Project structure: [`example2/feedback_letters.py`](../lab-snippets/snippets/lecture_workflows/example2/feedback_letters.py), plus the chat model of [`agents/example1bis`](../lab-snippets/snippets/lecture_agents/example1bis/agent_langchain.py); env vars as in [Example 1](#/workflow-scratch) (no vision model needed)

---

{{< slide id="plan-and-execute" >}}

## Plan-and-execute

> Recall: [plan before acting](../agents/#/plan-before-acting), and [LLM-Modulo](../agents/#/llm-modulo): the LLM _proposes_, external _critics_ verify

- __Plan-and-execute__ separates _planning_ (one LLM call, producing a whole plan) from _execution_ (steps run by code, or by simpler LLM calls)
    + vs. ReAct: _fewer_ calls to the big model, the plan is _visible before_ any action, and it can be _validated_ and _approved_
    + a __replanner__ step may revise the remaining plan when a step fails, or returns something unexpected
    + a _static_ cousin of orchestrator–workers: the whole plan is fixed and validated before any worker runs
- Recall: plans as [structured outputs](../prompting/#/structured-output), _validated_ in code ([agents](../agents/#/plan-before-acting)); here, validation is a _step_ of the workflow, and __irreversible__ steps trigger a user-input step approving the _whole_ plan

---

## Example 3: Plan-and-Execute for the Committee (pt. 1)

> __Goal__: serve _ad-hoc_ requests of the committee (e.g. "_invite the candidate with the best letter to an interview next Monday at 10:00_"), with plans that are _validated_ and _approved_ before execution

1. The __tools__ are the functions of [`committee.py`](../lab-snippets/snippets/lecture_workflows/committee.py) (cf. [Example 1](#/workflow-scratch)): read-only ones (`list_candidates`, `read_letter`, `read_transcript`, `score_letter`), write-enabled ones (`schedule_interview`, `send_email`, simulated by writing files), plus `get_current_time` (from the [agents lecture](../agents/#/tools-examples)); the __plan__ is a structured output:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example3/plan_execute.py" from="25" to="40" %}}

    - `StructuredTool.from_function(f).args_schema`: the Pydantic model of `f`'s arguments, the same one from which its JSON schema is derived
    - `Literal[tuple(TOOLS)]`: the planner can only name _existing_ tools; `args` is a JSON _string_ (portable across providers), parsed and validated by code
    - `final`: steps of a plan cannot see each other's results, so the planner may ask to _re-plan_ after seeing them

---

## Example 3: Plan-and-Execute for the Committee (pt. 2)

2. The __validator__ is code: arguments match the tools' signatures, candidates exist, and no action about a candidate whose documents were not read (a _precondition_):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example3/plan_execute.py" from="73" to="90" %}}

    - `committee.list_candidates()`: the known candidates; `state["results"]`: the steps executed so far (by previous plans)
    - `after_validate` (not shown, a conditional edge): invalid plans go back to the planner, _with the errors_ (at most `MAX_PLANS = 4` plans per request); valid ones with write steps go to the committee, the others straight to execution

---

## Example 3: Plan-and-Execute for the Committee (pt. 3)

3. __Approval__ of the _whole_ plan, then __execution__ by code, step by step; tool errors become results, so that the planner can _re-plan_:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example3/plan_execute.py" from="100" to="115" %}}

4. The graph: plan → validate → (approve) → execute → plan again, or report:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example3/plan_execute.py" from="131" to="140" %}}

    - `report` (not shown) asks the LLM to summarise the _results_ for the committee, or says the plan was rejected

---

## Example 3: Plan-and-Execute for the Committee (pt. 4)

5. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example3/plan_execute.py)):

    ```bash
    poetry run python -m snippets -l workflows -e 3
    ```

    ```text
    Committee: Invite the candidate with the best recommendation letter to an interview next Monday at 10:00
        [plan 1]
        1. get_current_time({"timezone": "Europe/Paris"})  # To determine the date for 'next Monday'.
        2. list_candidates({})  # To identify the candidate IDs.
        [...]
        8. score_letter({"candidate": "mohammed-ali"})  # To score the recommendation letter for mohammed-ali.
        9. schedule_interview({"candidate": "[best_candidate_id]", "when": "[calculated_iso_date]"})  # [...]  <- WRITE
        10. send_email({"candidate": "[best_candidate_id]", "subject": "Interview Invitation", [...]})  # [...]  <- WRITE
        [validate] step 9 (schedule_interview): invalid arguments {"candidate": "[best_candidate_id]", [...]}: 1 validation error
            for schedule_interview; step 10: unknown candidate '[best_candidate_id]', valid ones are ['jean-dupont', [...]]
        [plan 2] [...]   (same placeholders, rejected again, and so on, up to plan 4)
    AI (4 plan(s)): The attempt to schedule the interview failed at step 6. The `schedule_interview` action returned
    a validation error due to invalid arguments for the "candidate" and "when" fields.
    ```

    (actual run, with `gemma4:12b` via [Ollama](../llmaas/), _before_ we added the "never use placeholders" line to the prompt: the planner wrote _placeholders_ for values it did not know yet; the validator rejected every such plan, so nothing was ever executed, nor submitted to the committee; with `gemma4:e4b`, plans had malformed JSON arguments instead, rejected as well)

---

## Example 3: Plan-and-Execute for the Committee (pt. 5)

6. Things to observe:
    - ask for something _impossible_ (e.g. "_admit the candidate from Mars_"), or for an e-mail to a candidate who does not exist: where is it stopped?
    - compare the number of LLM calls with the ReAct agent of the [agents lecture](../agents/#/exercise-decide): which one is cheaper? Which one is easier to _audit_?
    - reject the plan: is anything written in `output/`?
    - with a _small_ planner (`gemma4:e4b`), we saw plans declared `final` with no scheduling step at all, and a report saying "_Mario Rossi [is] the candidate to be invited to the interview next Monday at 10:00_": nothing was scheduled. Only the _results_ tell what was done: how would you check the report against them?

    - the planner's prompt grows with the results of each step: with a local [Ollama](../llmaas/#/ollama), whose default context window is 4k tokens on machines with less than 24 GiB of VRAM, a run may fail with a _length limit_ error (start the server with a larger `OLLAMA_CONTEXT_LENGTH`)

7. Project structure: [`example3/plan_execute.py`](../lab-snippets/snippets/lecture_workflows/example3/plan_execute.py), plus the tools of [`committee.py`](../lab-snippets/snippets/lecture_workflows/committee.py); env vars as in [Example 1](#/workflow-scratch); outputs go to `output/workflows/`

{{% /section %}}

---

{{% section %}}

{{< slide id="representations" >}}

## Intermediate representations (pt. 1)

{{< image src="./representations.svg" max-h="40vh" alt="From intention to execution: an intention in natural language (invite the two best candidates to an interview on Monday) becomes a representation (a structured artefact: checklist, plan, schema, process model, tool contract), which undergoes verification (code checks first, then critics such as LLM judges and humans); rejected representations go back with the reasons, as in LLM-Modulo; only verified ones reach execution (steps with side effects). Every stage is logged and traced, so humans can inspect, contest, and audit what was meant, checked, and done" >}}

- LLMs turn _intentions_ into __text__; software (and humans) can only _verify_ __structures__
    + hence: make the LLM produce an __intermediate representation__ between what is _meant_ and what is _done_
- Kinds of intermediate representations:
    + __checklists__: what must hold (cf. the [letter-scoring checklist](../prompting/#/letter-scoring))
    + __plans__: which steps, in which order, with which tools (cf. [Example 3](#/plan-and-execute))
    + __schemas__: what the data looks like (cf. [structured outputs](../prompting/#/structured-output))
    + __process models__: which paths are admissible (a workflow graph, a BPMN diagram)
    + __tool contracts__: what each action requires and changes (pre-/post-conditions, idempotency, reversibility)

---

## Intermediate representations (pt. 2): principles

Generalising [plan before acting](../agents/#/plan-before-acting) beyond plans:

1. __Plan before acting__: no side effect before a representation of _what_ will be done exists
2. __Log and trace__: every representation, every verification, every execution is recorded (cf. [observability](#/observability))
3. __Verify and test__: representations are checked by _code_ first, by _critics_ (LLMs, humans) second
4. __Ask humans__ for __irreversible__ (e-mails, payments, decisions) or __norm-sensitive__ (privacy, consent, fairness) actions, showing them the _representation_, not the conversation

- Workflows are themselves intermediate representations: the _process_ is an artefact that domain experts can read, discuss, and _contest_
    + cf. _good enveloping_ in the [governance lecture](../governance/): explicit, contestable representations, rather than silent adaptation

{{% /section %}}

---

{{% section %}}

{{< slide id="multi-agent" >}}

## Multi-agent systems: the general concept

- A __multi-agent system__ (MAS) is a set of _autonomous_ agents which __interact__ (communicate, coordinate, compete) to achieve individual or shared goals
    + a classical topic in AI (cf. [Wooldridge, _An Introduction to MultiAgent Systems_](https://www.wiley.com/en-us/An+Introduction+to+MultiAgent+Systems%2C+2nd+Edition-p-9780470519462)), with agent communication languages such as [FIPA ACL](http://www.fipa.org/specs/fipa00061/) and [KQML](https://www.csee.umbc.edu/csee/research/kqml/)
- With LLMs, "multi-agent" usually means: several LLM-based agents, each with its _own_ system prompt, tools, and context, _orchestrated_ by code or by another agent
- Why split into several agents?
    + __context isolation__: each agent sees only what it needs (smaller, cleaner contexts)
    + __specialisation__: different prompts, tools, models, _permissions_ (least privilege)
    + __parallelism__: independent sub-tasks run at once
    + __organisational boundaries__: agents owned by _different_ teams or organisations (hence: _protocols_, cf. [A2A](#/a2a))

---

## Multi-agent architectures

{{< image src="./multi-agent.svg" max-h="42vh" alt="Four multi-agent architectures: supervisor (one agent delegates questions to worker agents, used as tools, and gets their answers), hierarchical (a supervisor of team leads, each with its agents), handoffs or swarm (triage, regulations, and status agents transferring control to each other, one active at a time), shared state or blackboard (agents reading and writing a common state, while a workflow decides who acts next)" >}}

- __Supervisor__: one agent delegates to _worker_ agents (often exposed to it as _tools_); simplest to reason about
    + e.g. Deep Agents' `task` subagents ([skills lecture](../skills/#/skills-deepagents))
- __Hierarchical__: supervisors of supervisors, for large teams
- __Handoffs__ (or _swarm_): agents _transfer control_ to each other (e.g. triage $\rightarrow$ billing $\rightarrow$ refunds); one agent active at a time
- __Shared state__ (or _blackboard_): agents communicate through a common state, while a _workflow_ decides who acts next
- Communication: via the __shared state__ (same process, same framework) or via __messages__ (possibly across processes and organisations: protocols)

---

## Multi-agent systems: when (not) to use them

- The claims are __contested__:
    + Anthropic reports that its multi-agent research system (a lead agent + parallel sub-agents) outperformed a single agent by ~90% on an internal research benchmark, using ~15$\times$ the tokens of a chat (cf. [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), 2025)
    + Cognition argues the opposite for coding agents: parallel sub-agents make _conflicting_ implicit decisions, as they do not share the full context (cf. [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents), 2025)
    + an analysis of 7 multi-agent frameworks over 1,600+ traces finds failures due to _specification_ issues, _inter-agent misalignment_, and _weak verification_ (cf. [Cemri et al., Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657), 2025)
- Rule of thumb: __more agents = more autonomy__ (cf. the [spectrum of autonomy](../agents/#/autonomy-spectrum))
    + use them for _breadth-first_, _parallelisable_ tasks with _read-only_ sub-agents (e.g. research), or across _organisational_ boundaries
    + avoid them when sub-tasks are _tightly coupled_, or when sub-agents _write_ (conflicting actions)
- Messages from other agents are __untrusted input__: a sub-agent reading a malicious letter can inject instructions into the supervisor (_injection propagates_); treat sub-agent and A2A outputs as _data_, validate structured outputs, and give _least privilege_ per agent (cf. [prompt injection](../agents/#/security))

---

{{< slide id="multi-agent-example" >}}

## Example 4: a Supervisor with Two Sub-Agents (pt. 1)

> __Goal__: split the committee's assistant into a __supervisor__ and two specialised sub-agents: a _documents_ agent (reads letters and transcripts) and a _regulations_ agent (answers questions about the PhD regulations, via [RAG](../rag/))

1. Each sub-agent has its _own_ system prompt, tools, and context ([`subagents.py`](../lab-snippets/snippets/lecture_workflows/subagents.py), shared by later examples and exercises):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/subagents.py" from="30" to="44" %}}

    - `committee.read_only_tools`: the read-only tools of [Example 3](#/plan-and-execute) (candidates, letters, transcripts, scores)
    - `search_regulations(query)` (not shown): a KNN search over the regulations, in the `sqlite-vec` index of the [RAG lecture](../rag/) (built upon first use)

---

## Example 4: a Supervisor with Two Sub-Agents (pt. 2)

2. The supervisor sees the sub-agents as __tools__: it never sees the documents, nor the regulations, only the sub-agents' _answers_ (__context isolation__)

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example4/supervisor.py" from="15" to="35" %}}

    - sub-agents do __not__ see the supervisor's conversation: questions must be _self-contained_ (and the prompt says so)

3. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example4/supervisor.py)):

    ```bash
    poetry run python -m snippets -l workflows -e 4
    ```

    ```text
    You: Is Mohammed Ali's degree enough to be admitted, according to the regulations?
        [regulations agent] "According to the program regulations, is Mohammed Ali's degree sufficient for admission?"
            -> 'The program regulations provide general criteria for admission but do not contain any information ab'...
        [documents agent] "What is the full academic title and field of study for Mohammed Ali's degree, and what is the issuing
            institution?" -> 'Based on the transcript for Mohammed Ali, his full academic title is **Bachelor of Science**. [...]'...
    AI: [...] The program regulations outline a requirement of a Master's degree or an equivalent credential. The documents
    provided indicate that Mohammed Ali possesses a Bachelor of Science degree, which appears to be below the minimum educational
    level mentioned in the regulations. [...]
    ```

    (actual run, with `gemma4:e4b` via [Ollama](../llmaas/): notice the first question, which is _not_ self-contained, as the regulations agent knows nothing about candidates)

---

## Example 4: a Supervisor with Two Sub-Agents (pt. 3)

4. Things to observe:
    - how many tokens does a question cost, compared with a _single_ agent having all the tools?
    - are the supervisor's questions really _self-contained_? What does the supervisor _lose_ by not seeing the documents (e.g. a detail the sub-agent did not report)?
    - ask something requiring the two sub-agents _in sequence_ (the answer of one is needed to ask the other): does the supervisor manage?

5. Project structure:

<div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
├── <a href="../lab-snippets/data/__init__.py">data/</a>                              # documents, regulations (+ helpers)
├── snippets/
│   ├── lecture_rag/                   # embeddings, sqlite-vec index (reused)
│   └── lecture_workflows/
│       ├── <a href="../lab-snippets/snippets/lecture_workflows/committee.py">committee.py</a>               # read-only tools (reused)
│       ├── <a href="../lab-snippets/snippets/lecture_workflows/subagents.py">subagents.py</a>               # the two sub-agents
│       └── example4/
│           └── <a href="../lab-snippets/snippets/lecture_workflows/example4/supervisor.py">supervisor.py</a>          # the supervisor
└── <a href="../lab-snippets/pyproject.toml">pyproject.toml</a></code></pre></div>

- env vars as in [Example 1](#/workflow-scratch), plus the embedding model's ones (`EMBEDDINGS_*`, cf. the [RAG lecture](../rag/))

{{% /section %}}

---

{{% section %}}

{{< slide id="a2a" >}}

## The Agent2Agent (A2A) protocol: the general concept

- [A2A](https://a2a-protocol.org/) is an _open protocol_ for __agents to talk to agents__, possibly built with _different_ frameworks, by _different_ organisations
    + started by Google (2025), donated to the [Linux Foundation](https://linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year), now a project of the [Agentic AI Foundation](https://aaif.io/blog/a2a-joins-aaif) (along with MCP); specification v1.0 released in 2026
- Core concepts (cf. [key concepts](https://a2a-protocol.org/latest/topics/key-concepts/)):
    + __Agent Card__: a JSON document describing an agent (name, skills, endpoints, supported protocol bindings, authentication), for _discovery_ (served at `/.well-known/agent-card.json`)
        * A2A _skills_ are advertised capabilities (ID, description, tags, examples): __not__ the [Agent Skills](../skills/) of the skills lecture (no `SKILL.md`, no instructions)
        * authentication: `securitySchemes` (API key, HTTP bearer, OAuth2, OpenID Connect, mTLS, as in OpenAPI) plus `security` requirements; optional `signatures` (JWS), so that clients can verify who published the card (cf. the [specification](https://a2a-protocol.org/latest/specification/))
    + __Task__: a _stateful_ unit of work, with an ID and a __lifecycle__: _submitted_, _working_, _input-required_ (or _auth-required_), then one of the terminal states _completed_, _failed_, _canceled_, _rejected_
    + __Message__: one turn of communication (role `user` or `agent`), made of __Parts__ (text, files, structured data)
    + __Artifact__: an _output_ of a task (e.g. a document, a JSON object)
    + __Context__: groups related tasks (a conversation)
- Interaction: request/response (with polling), __streaming__ (Server-Sent Events), __push notifications__ (webhooks), over HTTP(S), with three _protocol bindings_: JSON-RPC 2.0, gRPC, and HTTP+JSON (REST)

---

## A2A: an intuitive example

{{< mermaid >}}
%%{init: {'flowchart': {'htmlLabels': false}}}%%
sequenceDiagram
    participant C as Committee's assistant (A2A client)
    participant S as Admissions office's agent (A2A server)
    C->>S: GET /.well-known/agent-card.json
    S-->>C: Agent Card (name, skills, endpoints, auth)
    C->>S: message: "is the transcript of Mohammed Ali authentic?"
    S-->>C: Task T1: submitted, then working (streamed)
    S-->>C: Task T1: input-required ("please send the transcript")
    C->>S: message (task T1): a file Part, the transcript
    S-->>C: Task T1: working
    S-->>C: Task T1: completed, with an Artifact (a JSON verdict)
{{< /mermaid >}}

- The client does __not__ know (nor need to know) _how_ the remote agent works: which LLM, which tools, which prompts
    + the remote agent is __opaque__: it is a _peer_, with its own autonomy, not a function

---

## A2A vs. MCP

| Aspect | [MCP](../agents/#/mcp) | __A2A__ |
|---|---|---|
| Connects | an agent (host) to __tools__ and data (servers) | an agent to other __agents__ |
| The other side is | _transparent_: a function with a schema | _opaque_: an autonomous peer |
| Unit of interaction | a tool call (one request, one result) | a __task__, with a lifecycle (possibly long-running, possibly asking for input) |
| Who holds the state | the host (the conversation) | the remote agent (the task) |
| Discovery | the host is configured with servers | __Agent Cards__ |
| Typical boundary | same application / organisation | across teams and __organisations__ |

- They are __complementary__: an agent can _use_ tools via MCP, and _be used_ by other agents via A2A
- An A2A agent _could_ be wrapped as an MCP tool (and vice versa), losing what does not fit (task lifecycle, opacity)

---

## A2A: the technological landscape

{{% small "70%" %}}

| Technology | Role | Notes | Docs |
|---|---|---|---|
| Official SDKs: [Python](https://github.com/a2aproject/a2a-python) (`a2a-sdk`), JS, Java, Go, .NET | clients and servers | implement spec v1.0 (with a 0.3 compatibility mode); JSON-RPC, gRPC, HTTP+JSON bindings | [link](https://a2a-protocol.org/latest/sdk/) |
| [A2A Inspector](https://github.com/a2aproject/a2a-inspector) | debugging | a Web UI to fetch Agent Cards, and chat with A2A servers | [link](https://github.com/a2aproject/a2a-inspector) |
| [Google ADK](https://adk.dev/) | framework | `to_a2a(agent)` exposes an agent; `RemoteA2aAgent` uses a remote one as a sub-agent | [link](https://adk.dev/a2a/quickstart-exposing/) |
| [LangGraph / LangSmith Agent Server](https://docs.langchain.com/langsmith/server-a2a) | deployment | each deployed graph gets an `/a2a/{assistant_id}` endpoint and an Agent Card | [link](https://docs.langchain.com/langsmith/server-a2a) |
| [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) | framework | A2A agents as clients, and hosting agents as A2A servers | [link](https://learn.microsoft.com/en-us/agent-framework/) |
| [CrewAI](https://docs.crewai.com/en/learn/a2a-agent-delegation) | framework | `A2AClientConfig` (delegate to remote agents), `A2AServerConfig` (expose agents) | [link](https://docs.crewai.com/en/learn/a2a-agent-delegation) |
| [FastA2A](https://github.com/datalayer/fasta2a) | library | framework-agnostic A2A servers; bridge for Pydantic AI (`agent_to_a2a`) | [link](https://pypi.org/project/fasta2a/) |

{{% /small %}}

- Same _metamodel_ everywhere (cards, tasks, messages, parts, artifacts): what differs is how much of the _executor_ the framework writes for you

---

{{< slide id="a2a-example" >}}

## Example 4 (bis): the Regulations Agent, via A2A (pt. 1)

> __Goal__: the _regulations_ agent of [Example 4](#/multi-agent-example) is now run by _another organisation_ (e.g. the PhD school's office), and exposed via A2A; the supervisor talks to it as a _remote peer_

1. The __Agent Card__ (with [`a2a-sdk`](https://github.com/a2aproject/a2a-python)): who the agent is, what it can do (_A2A skills_), where and how to reach it

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example4bis/regulations_server.py" from="23" to="38" %}}

    - `supported_interfaces`: the endpoints, each with its _protocol binding_ (here, JSON-RPC) and protocol version
    - `capabilities`: optional features (here, _streaming_ of task updates)

---

## Example 4 (bis): the Regulations Agent, via A2A (pt. 2)

2. The __executor__ turns A2A requests into runs of the agent, reporting progress as _task events_; the __server__ serves the card and a JSON-RPC endpoint:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example4bis/regulations_server.py" from="41" to="60" %}}

    - `context`: the incoming request (its `message`, and the `current_task`, if the message continues one); `event_queue`: where task events go (to the client)
    - `TaskUpdater`: helpers to publish status updates (`update_status`, `complete`, `reject`, ...) and artifacts (`add_artifact`)
    - `DefaultRequestHandler` implements the protocol (tasks, streaming, ...), keeping tasks in a `TaskStore` (here, in memory); `Starlette` is the Web framework; [`uvicorn`](https://www.uvicorn.org/) runs it

---

## Example 4 (bis): the Regulations Agent, via A2A (pt. 3)

3. The supervisor's `ask_regulations_agent` tool now uses an A2A __client__ (the rest of [Example 4](#/multi-agent-example) is unchanged):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example4bis/supervisor_a2a.py" from="23" to="40" %}}

    - `create_client(url, config)` fetches the Agent Card, and picks a protocol binding supported by both sides; the `httpx` client has a longer timeout, as remote agents call LLMs (slow)
    - events are _protobuf_ messages (the A2A v1.0 data model is defined in Protocol Buffers): `HasField` tells which kind of event it is
    - the tool is `async` (so is the supervisor's loop: `ainvoke`), as the A2A client is

---

## Example 4 (bis): the Regulations Agent, via A2A (pt. 4)

4. Let's try it, in two terminals (full code [here](../lab-snippets/snippets/lecture_workflows/example4bis/)):

    ```bash
    poetry run python -m snippets -l workflows -e 4bis   # pick regulations_server.py
    curl http://localhost:9999/.well-known/agent-card.json   # the Agent Card, as JSON
    poetry run python -m snippets -l workflows -e 4bis   # pick supervisor_a2a.py, in another terminal
    ```

    ```text
    You: Is there an age limit to apply, according to the regulations?
        [regulations agent, task 9eafc25b] TASK_STATE_WORKING
        [regulations agent, task 9eafc25b] TASK_STATE_COMPLETED
    AI: According to the regulations, there is no age limit for admission (Art. 3).
    ```

    (actual run, with `gemma4:e4b` via [Ollama](../llmaas/); the server's Agent Card, as served at `/.well-known/agent-card.json`, is the JSON version of the `AgentCard` above)

5. Things to observe:
    - inspect the server with the [A2A Inspector](https://github.com/a2aproject/a2a-inspector): what does a client learn about the agent? What _not_?
    - what changed for the supervisor? (one tool's body) And for _governance_? (another organisation, a network, _authentication_, which is missing here!)
    - stop the server, and ask again: how does the supervisor cope with a remote agent being _unavailable_?

---

## Example 4 (bis): Project Structure

<div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
└── snippets/
    └── lecture_workflows/
        ├── <a href="../lab-snippets/snippets/lecture_workflows/subagents.py">subagents.py</a>                 # the regulations agent (reused)
        ├── example4/
        │   └── <a href="../lab-snippets/snippets/lecture_workflows/example4/supervisor.py">supervisor.py</a>            # documents agent tool, prompt (reused)
        └── example4bis/
            ├── <a href="../lab-snippets/snippets/lecture_workflows/example4bis/regulations_server.py">regulations_server.py</a>    # Agent Card, executor, server
            └── <a href="../lab-snippets/snippets/lecture_workflows/example4bis/supervisor_a2a.py">supervisor_a2a.py</a>        # the supervisor, as an A2A client</code></pre></div>

- env vars as in [Example 4](#/multi-agent-example), plus `REGULATIONS_AGENT_PORT` (server, default `9999`) and `REGULATIONS_AGENT_URL` (client, default `http://localhost:9999`)

{{% /section %}}

---

{{% section %}}

{{< slide id="observability" >}}

## Streaming and observability: the general concept

- Workflows take _long_ (many LLM calls, human waits): users and developers need to see __what is happening__
- __Streaming__: the engine emits events _while_ running
    + _token_ streaming (an LLM step's output as it is generated, cf. [the LLMaaS lecture](../llmaas/))
    + _step_ streaming (state updates after each step: "_scoring letters... 2/3_")
    + _custom_ events (progress, intermediate results), and _interrupts_
- __Observability__: _after the fact_, reconstruct what happened, why, and at what cost
    + a __trace__ per run, made of nested __spans__ (one per step, LLM call, tool call), with inputs, outputs, tokens, latency, errors
    + the [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) standardise span names and attributes for LLM calls, agents, and tools
- Traces serve _debugging_, _cost control_, _evaluation_ (traces become test cases), and _accountability_ (cf. [log and trace](#/representations))

---

## Observability: the technological landscape

{{% small "75%" %}}

| Technology | Kind | Open source? | Self-hostable? | Docs |
|---|---|---|---|---|
| [LangSmith](https://www.langchain.com/langsmith) | tracing + evaluation platform, by LangChain | no | enterprise plans only | [link](https://docs.langchain.com/langsmith/observability) |
| [Langfuse](https://langfuse.com/) | tracing + evaluation platform, OpenTelemetry-based | yes (MIT core) | yes | [link](https://langfuse.com/docs) |
| [MLflow Tracing](https://mlflow.org/docs/latest/genai/tracing/) | tracing in the MLflow platform (cf. the [validating lecture](../validating/)), OpenTelemetry-compatible | yes (Apache 2.0) | yes | [link](https://mlflow.org/docs/latest/genai/tracing/) |
| [Arize Phoenix](https://phoenix.arize.com/) | tracing + evaluation, on [OpenInference](https://github.com/Arize-ai/openinference) conventions | yes | yes | [link](https://arize.com/docs/phoenix) |
| [OpenLLMetry](https://github.com/traceloop/openllmetry) | instrumentation of LLM libraries, emitting OpenTelemetry spans | yes (Apache 2.0) | n/a (send to any OTel backend) | [link](https://www.traceloop.com/docs/openllmetry/introduction) |
| OTel backends ([Jaeger](https://www.jaegertracing.io/), [Grafana Tempo](https://grafana.com/oss/tempo/), ...) | generic tracing | yes | yes | — |

{{% /small %}}

- Same _metamodel_ (traces of nested spans, with attributes), increasingly on __OpenTelemetry__: instrument once, choose (or change) the backend later
- Traces contain _prompts_ and _documents_, i.e. possibly __personal data__: where they are stored matters (cf. the [governance lecture](../governance/))

---

{{< slide id="observability-example" >}}

## Example 5: Streaming and Tracing the Admission Workflow (pt. 1)

> __Goal__: watch the workflow of [Example 1 (bis)](#/workflow-langgraph) _while_ it runs, and inspect its traces _afterwards_

1. __Tracing__: one line (in the main program), and every run of the graph becomes an MLflow _trace_ (nodes, LLM calls, tool calls are its _spans_)

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example5/observe.py" from="32" to="33" %}}

2. __Streaming__: `stream` yields events _while_ the graph runs; with several `stream_mode`s, events are `(mode, event)` pairs

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example5/observe.py" from="17" to="28" %}}

    - `"updates"`: after each node, `{node: the partial update it returned}` (interrupts, too, show up here)
    - `"custom"`: what nodes emit via `get_stream_writer()`, e.g. `read_transcript`'s progress events (cf. [Example 1 (bis)](#/workflow-langgraph))
    - other modes: `"values"` (the whole state after each step), `"messages"` (LLM tokens, as they are generated)

---

## Example 5: Streaming and Tracing the Admission Workflow (pt. 2)

3. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example5/observe.py)), then browse the traces:

    ```bash
    poetry run python -m snippets -l workflows -e 5
    poetry run mlflow ui   # then open http://localhost:5000, experiment "admission-workflow", tab "Traces"
    ```

    ```text
    # Thread: demo5
        [progress] transcript of mario-rossi read
        [16:58:19] read_transcript done, updated: transcripts
        [progress] transcript of jean-dupont read
        [16:58:52] read_transcript done, updated: transcripts
        [progress] transcript of mohammed-ali read
        [16:59:30] read_transcript done, updated: transcripts
        [16:59:30] check_eligibility done, updated: problems
        [17:03:29] score_letters done, updated: scores
        [17:03:29] rank done, updated: ranking
    Proposal of the workflow (candidates will be notified accordingly): [...]
    Do you approve it? [y/N] y
        [17:03:29] approve done, updated: approved
        [17:03:29] notify done, updated: notified
    ```

    (actual run, with `gemma4:e4b` via a local [Ollama](../llmaas/), with `--thread demo5`: the "parallel" branches did _not_ overlap, as Ollama served one request at a time)

4. Things to observe:
    - which step is the slowest? Which one costs more _tokens_? Do the parallel branches really overlap in time?
    - stop at the approval (Ctrl+D), then resume with `--thread`: how many traces does the run produce?
    - find the prompt of a letter's scoring, inside the trace: would you be allowed to store it, under the [GDPR](../governance/)?

5. Project structure: [`example5/observe.py`](../lab-snippets/snippets/lecture_workflows/example5/observe.py), plus the workflow of [Example 1 (bis)](#/workflow-langgraph); env vars as in [Example 1](#/workflow-scratch)

---

## Example 5: the trace, in MLflow

{{< image src="./mlflow-trace.png" max-h="62vh" alt="The MLflow trace of the admission workflow, up to the committee's approval: on the left, the tree of spans (LangGraph, then read_transcript three times, each with its ChatOpenAI call taking from 32 seconds to 1.7 minutes, then check_eligibility, score_letters, ...), with durations and tokens; on the right, the inputs and outputs of the whole graph, i.e. the state: the transcripts as extracted (Mario Rossi's final grade misread as 1055 out of 110) and the problems found by check_eligibility (an implausible grade, to be checked)" >}}

- One trace per `stream` call (here, up to the interrupt: 3.2 minutes, 5,619 tokens), and another one for the resumed run; spans nest as nodes $\rightarrow$ chains $\rightarrow$ LLM calls
- In this run, the vision model read Mario Rossi's "105/110" as 1055/110 (a different misreading than [the one above](#/workflow-scratch): the error is not reproducible): the [gate](#/workflow-scratch) in `check_eligibility` flagged it, and the trace shows _where_ the wrong value came from

{{% /section %}}

---

{{% section %}}

{{< slide id="evaluating-workflows" >}}

## Evaluating workflows: the general concept

> Recall: [validating generative software](../validating/): datasets, deterministic scorers, LLM-as-a-Judge, and their integration with test frameworks

- Workflows can be tested at __three levels__:
    1. __step__ level: each step in isolation, as a function of the state (LLM steps with [validation datasets](../validating/), data and action steps with ordinary unit tests, _no_ LLM)
    2. __path__ level: given an input, does the run take the _expected_ path (e.g. ineligible candidates never reach approval)? Do invariants hold (e.g. no e-mail without approval)?
        + LLM steps can be replaced by __fakes__ (fixed outputs), to test the _graph_ cheaply and deterministically
    3. __end-to-end__ level: real LLMs, real inputs, assertions on the _final_ state and on _quality_ (judges)
- _Interrupts_ are part of the test: simulate the human (approve, reject, edit), as in the [agents lecture](../agents/#/exercise-decide-solution)
- __Traces__ from [observability](#/observability) feed new test cases (regressions)

---

{{< slide id="evaluating-workflows-example" >}}

## Example 6: Testing the Admission Workflow (pt. 1)

> __Goal__: a `pytest` suite for the admission workflow of [Example 1 (bis)](#/workflow-langgraph), at the three levels, reusing the dataset of the [validating lecture](../validating/)

1. __Fakes__ replace the LLM steps, with outputs written _by hand_ (by looking at the documents), recording the calls:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example6/test_admission.py" from="33" to="46" %}}

    - `monkeypatch.setattr(module, name, value)`: a `pytest` fixture replacing an attribute for the duration of a test; it works since nodes look up `admission.extract_transcript` _at call time_
    - `TRANSCRIPTS`, `SCORES` (not shown): what a _correct_ extraction and scoring return
    - `output_dir` (not shown): an _autouse_ fixture redirecting `admission.OUTPUT_DIR` to a fresh temporary directory, per test

---

## Example 6: Testing the Admission Workflow (pt. 2)

2. __Step__ tests (no LLM, no graph) and __path__ tests (fake LLMs, real graph), e.g.:

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example6/test_admission.py" from="81" to="97" %}}

    - not shown: step tests (eligibility, ranking, idempotent `notify`), and a test where the committee approves (everybody notified)
    - _invariants_ of the process: no e-mail without approval, no letter scored for ineligible candidates, idempotent notifications
    - __durability__ is tested too: a _new_ instance of the workflow resumes the thread from the SQLite checkpoint, with _no_ LLM call

---

## Example 6: Testing the Admission Workflow (pt. 3)

3. One __end-to-end__ test, with real LLMs, checking the final state against expectations written by hand, and the score ranges of the [validating dataset](../validating/) (`TEST_CASES`):

    {{% code path="static/lab-snippets/snippets/lecture_workflows/example6/test_admission.py" from="102" to="109" %}}

4. Let's try it (full code [here](../lab-snippets/snippets/lecture_workflows/example6/test_admission.py)):

    ```bash
    poetry run python -m snippets -l workflows -e 6 -v                     # all tests
    poetry run python -m snippets -l workflows -e 6 -k "not end_to_end"    # no LLM: fast, free, deterministic
    ```

    - the step and path tests run in _milliseconds_, with no API key: they can run at every commit (CI); the end-to-end test is _slow_ and _costly_: run it before releases, or nightly

5. Project structure: [`example6/test_admission.py`](../lab-snippets/snippets/lecture_workflows/example6/test_admission.py), plus [`lecture_validating/dataset.py`](../lab-snippets/snippets/lecture_validating/dataset.py) and [`test_data.yml`](../lab-snippets/snippets/lecture_validating/test_data.yml) (reused); env vars as in [Example 1](#/workflow-scratch)

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-email-bot" >}}

## Exercise 1: a Bot for Candidates' E-mails (pt. 1)

> __Goal__: a _semi-automatic_ assistant for the PhD admission office, which answers the e-mails of the [candidates](#/running-example) (e.g. on requirements, deadlines, documents, the status of their application), drafting replies which a member of the office __approves__ before they are sent

> __Code__: put your solution in [`snippets/lecture_workflows/exercise1/`](../lab-snippets/snippets/lecture_workflows/exercise1/__init__.py) of [`lab-snippets`](../#/lab-snippets-exercises), and run it via `poetry run python -m snippets -l workflows -x 1`

- The office's __inbox__ is in [`data/inbox/`](../lab-snippets/data/inbox/01-age-limit.txt): 8 e-mails, from candidates and strangers (`data.inbox()` returns them as `dict`s, with `id`, `sender`, `subject`, `body`); the office's records of the applications (e-mail addresses, statuses) are in [`data/applications.json`](../lab-snippets/data/applications.json) (`data.applications()`)

{{% fragment %}}
### TO-DO List
1. model the bot as a __LangGraph__ workflow, with (at least):
    + a __routing__ step (LLM, structured output), e.g.: questions on the _regulations_, on the _status_ of the sender's application, _out of scope_, _suspicious_
    + per route: __RAG__ over the [regulations](../rag/) (questions), a _data_ step reading the application's record (status), a _canned_ reply (out of scope), _escalation_ to a human (suspicious)
    + a __drafting__ step and an __evaluator–optimizer__ loop (no invented facts, no data of _other_ candidates, cite the regulations' articles)
    + a __human-in-the-loop__ step (approve / edit / reject) before an __idempotent__ `send_reply` (writing to an `outbox/`)
2. persist runs with a __SQLite checkpointer__: one thread per e-mail, approvals may come _later_ (even after a restart)
3. stream progress to the CLI, and trace runs (e.g. with MLflow)
4. write __tests__ at the three levels (step, path, end-to-end)
{{% /fragment %}}

---

## Exercise 1: a Bot for Candidates' E-mails (pt. 2)

### Decision points and hints

- _Who_ is writing? The sender's address must match a candidate's application before _any_ personal data is used: a __data step__, not the LLM's judgement
- What does the router do with e-mails that fit _two_ routes (a question _and_ a status request)? One route, a _list_ of routes (fan-out), or escalation?
- The e-mail is __untrusted input__ (cf. [prompt injection](../agents/#/security)): which steps see it? Can any of them _act_?
- How many evaluator–optimizer rounds? What happens when the judge never accepts?
- What does the human see when approving: the e-mail, the draft, the judge's critique, the retrieved articles?

### How to test it?

- the inbox _is_ the dataset: write the expected route (and key facts of the reply) per e-mail
- path tests with a _fake_ router: suspicious e-mails never reach `send_reply` without a human; rejected drafts are never sent
- run the injection e-mail many times: no other candidate's data in any draft

> __Solution__: a walkthrough follows in the next (vertical) column — try on your own first!

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-email-bot-solution" >}}

## Exercise 1: a Bot for Candidates' E-mails — Solution

> ⚠️ __Spoiler alert__: the _walkthrough_ of the solution of [Exercise 1](#/exercise-email-bot) is about to start

- __Do not proceed__ until you have _attempted_ the exercise on your own
    + press → to _skip_ the solution, ↓ to see it
- The code of the solution is on the `master` branch of [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) (while you cloned the `exercises` branch, with placeholders only)

---

## Exercise 1 — Solution: the state and the graph

> Every route ends at a __human__, or at an __escalation__: nothing is sent without approval

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="159" to="175" %}}

- The state (not shown) holds the `email` (__untrusted__), the verified `candidate`, the `route`, the `facts` the reply may state, all `drafts` and `critiques` (lists, with `operator.add` as reducer), the human's `decision`, and whether the reply was `sent`
- `out_of_scope` writes a _canned_ draft (no LLM), which goes straight to the human


---

## Exercise 1 — Solution: the graph

{{< mermaid >}}
%%{init: {'flowchart': {'htmlLabels': false}}}%%
flowchart LR
    S([start]) --> I[identify] --> C[classify]
    C -.-> RG[regulations] --> D[draft]
    C -.-> ST[status] --> D
    C -.-> O[out_of_scope] --> RV[review]
    C -.-> ES[escalate] --> E([end])
    D --> J[judge]
    J -.-> D
    J -.-> RV
    RV -.-> SR[send_reply] --> E
    RV -.-> E
{{< /mermaid >}}

- Dashed edges are _conditional_: routing after `classify`, the draft ⇄ judge loop, and the human's decision after `review`

---

## Exercise 1 — Solution: who is writing? (a data step)

> The sender's __identity__ is checked by _code_, against the office's records: personal data only go to the _verified_ owner

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="93" to="95" %}}

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="107" to="112" %}}

- `data.applications()`: candidate's ID → `{"email": ..., "status": ...}`; `by_address` inverts it
- The LLM never decides _whom_ it is talking to: "_this is Mohammed Ali, writing from my personal address_" changes nothing (e-mail `08`)
- `facts` are the __only__ facts the reply may state: retrieved articles, or the sender's _own_ status, or the reason why nothing can be said
    + the `regulations` node (not shown) puts into `facts` the articles found by `search_regulations` (the KNN search of [Example 4](#/multi-agent-example)), with the e-mail as the query

---

## Exercise 1 — Solution: routing untrusted e-mails

> The router's output is a __closed set__ of routes (a `Literal`), each one _defined_ in the prompt

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="40" to="55" %}}

- `reason` comes _before_ `route`: a one-sentence reasoning first; with a small model, this (and the definitions in the prompt, rather than in the schema) took our tests (the 8 routes, plus the citation test) from 3 to 8 passed out of 9, with `gemma4:e4b` (the forgotten CV still goes to `status`)
- The e-mail is _delimited_ (`<email>...</email>`) and declared as __data__: this _mitigates_ prompt injection, with no guarantee (cf. [prompt injection](../agents/#/security))
- Hence, the _graph_ limits the damage of a misrouted e-mail: no route has tools, no route sends anything without a human, and the `status` route discloses only the _verified_ sender's data
- `admission_llm()` imports the chat model of the [agents lecture](../agents/#/agent-langchain) _lazily_: tests can import the bot with no API key

---

## Exercise 1 — Solution: the evaluator–optimizer loop

> An __LLM judge__ for what needs language, plus a __check in code__ for what code can check

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="127" to="140" %}}

- `write_reply(email, facts, previous, issues)` and `judge_reply(email, facts, reply)` (not shown) prompt the LLM: the former to write (or _fix_) the reply from the `facts` only, the latter to fill in a checklist (only facts given, answers the question, cites articles, polite and short), as in [Example 2](#/patterns-example), returning the failed criteria as `issues`
- The loop is __bounded__ (`MAX_DRAFTS = 3`): then, the _human_ decides, seeing the unresolved issues

---

## Exercise 1 — Solution: the human, and idempotent actions

> The human sees __everything__ needed to decide: the e-mail, the facts, the draft, the judge's unresolved issues

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="143" to="156" %}}

- The answer is a `dict`: `{"decision": "approve"}`, `{"decision": "reject"}`, or `{"decision": "edit", "text": ...}`; edits become the _last draft_, which is what gets sent
- `send_reply` writes one file per e-mail, and never overwrites it: re-running the step (e.g. after a crash) sends nothing twice
- `escalate` (not shown) writes suspicious e-mails into `escalations/`, for a human to handle: the bot never replies to them

---

## Exercise 1 — Solution: the CLI, with durable approvals

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/bot.py" from="199" to="213" %}}

- New e-mails are processed (streaming their steps, via `process`, not shown); e-mails whose thread already has a state are _skipped_
- Then, pending drafts are reviewed one by one (`ask_human`, not shown, asks on the terminal): Ctrl+D stops, and the next run picks up the _remaining_ ones, from the SQLite checkpoints
- Traces go to MLflow, as in [Example 5](#/observability-example)

---

## Exercise 1 — Solution: tests (pt. 1), offline

> __Fakes__ for the LLM steps and RAG: the _graph_'s invariants are tested in milliseconds, with no API key (they run in CI)

{{% code path="static/lab-snippets/tests/test_workflows.py" from="23" to="30" %}}

{{% code path="static/lab-snippets/tests/test_workflows.py" from="58" to="70" %}}

- `run(email, decision)` (not shown) processes an e-mail with a fresh graph (`InMemorySaver`), answering every interrupt with `decision`
- Suspicious e-mails are never answered, _even_ with a careless human approving everything; unverified senders never get personal data

---

## Exercise 1 — Solution: tests (pt. 2), end-to-end

> The inbox __is__ the dataset: the expected routes are written by hand

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise1/test_email_bot.py" from="49" to="64" %}}

- `test_routes` (not shown) checks the router against `EXPECTED_ROUTES`: a _set_ of acceptable routes per e-mail (e.g. `{"status", "suspicious"}` for e-mail `08`)
- `run(email)` approves _everything_: the worst case, as in the [agents exercise](../agents/#/exercise-decide-solution); the injection test is _repeated_, as LLMs are not deterministic
- Jean Dupont's TOEFL dates back to 2022, while Art. 5 accepts certificates from 2023 on: does the reply notice? (a _reasoning_ check, not only retrieval)

---

## Exercise 1 — Solution: Project Structure

<div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
├── data/
│   ├── <a href="../lab-snippets/data/inbox/01-age-limit.txt">inbox/</a>                         # the e-mails
│   ├── <a href="../lab-snippets/data/applications.json">applications.json</a>              # the office's records
│   ├── <a href="../lab-snippets/data/regulations-phd.md">regulations-phd.md</a>             # the regulations
│   └── <a href="../lab-snippets/data/__init__.py">__init__.py</a>                    # helpers: inbox(), applications(), ...
├── snippets/
│   ├── lecture_rag/                   # embeddings, sqlite-vec index (reused)
│   └── lecture_workflows/
│       ├── <a href="../lab-snippets/snippets/lecture_workflows/subagents.py">subagents.py</a>               # search_regulations (reused)
│       └── exercise1/
│           ├── <a href="../lab-snippets/snippets/lecture_workflows/exercise1/bot.py">bot.py</a>                 # the workflow, and its CLI
│           └── <a href="../lab-snippets/snippets/lecture_workflows/exercise1/test_email_bot.py">test_email_bot.py</a>      # end-to-end tests
└── tests/
    └── <a href="../lab-snippets/tests/test_workflows.py">test_workflows.py</a>              # offline tests (fakes)</code></pre></div>

- run it via `poetry run python -m snippets -l workflows -x 1 [PYTEST OPTIONS]`, then pick `bot.py` or `test_email_bot.py`
- env vars: `OPENAI_*`, `EMBEDDINGS_*` (cf. [Free Access to LLMs](../free-access/) and the [RAG lecture](../rag/)); outputs (checkpoints, `sent/`, `escalations/`) go to `output/workflows/`

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-a2a" >}}

## Exercise 2: the E-mail Bot as an A2A Agent (pt. 1)

> __Goal__: expose the bot of [Exercise 1](#/exercise-email-bot) as an __A2A agent__, so that _other_ agents (e.g. the university's general help-desk agent) can _delegate_ candidates' questions to it, and follow the _task_ until a human of the admission office has approved the reply

> __Code__: put your solution in [`snippets/lecture_workflows/exercise2/`](../lab-snippets/snippets/lecture_workflows/exercise2/__init__.py) of [`lab-snippets`](../#/lab-snippets-exercises), and run it via `poetry run python -m snippets -l workflows -x 2`

{{% fragment %}}
### TO-DO List
1. write the bot's __Agent Card__ (cf. [Example 4 (bis)](#/a2a-example)): name, description, _A2A skills_ (e.g. "answer candidates' questions on the PhD admission"), input/output modes
2. write an __A2A server__ (with `a2a-sdk`) whose executor runs the workflow of [Exercise 1](#/exercise-email-bot): one A2A __task__ per e-mail, one LangGraph __thread__ per task
3. map the workflow onto the __task lifecycle__: `working` while drafting, then waiting for the office's approval (still `working`, or `input-required`? cf. the decision points), finally `completed` (with the reply as an __artifact__), or `rejected` / `failed`
4. write a small __A2A client__ (the help-desk agent, or just a script) which sends an e-mail and _streams_ the task's status updates
5. test it: an approved e-mail ends `completed` with the reply; a rejected one does not; the injection e-mail never completes without a human
{{% /fragment %}}

---

## Exercise 2: the E-mail Bot as an A2A Agent (pt. 2)

### Decision points and hints

- _Who_ approves: the A2A __client__ (via `input-required`), or the office, _out of band_ (the client just waits)? Which one makes sense across organisations?
- How does the approver avoid _rubber-stamping_? (e.g. show the evidence, require a motivation)
- The A2A client is _another organisation's_ agent: what should the Agent Card _not_ reveal? Which _authentication_ scheme would you declare?
- Long-running tasks: polling, streaming, or push notifications?
- What is the A2A __context__ in this scenario (one per candidate? one per e-mail thread?)

> __Solution__: a walkthrough follows in the next (vertical) column — try on your own first!

{{% /section %}}

---

{{% section %}}

{{< slide id="exercise-a2a-solution" >}}

## Exercise 2: the E-mail Bot as an A2A Agent — Solution

> ⚠️ __Spoiler alert__: the _walkthrough_ of the solution of [Exercise 2](#/exercise-a2a) is about to start

- __Do not proceed__ until you have _attempted_ the exercise on your own
    + press → to _skip_ the solution, ↓ to see it
- The code of the solution is on the `master` branch of [`lab-snippets`]({{< github-url repo="lab-snippets" >}}) (while you cloned the `exercises` branch, with placeholders only)

---

## Exercise 2 — Solution: the Agent Card

> The card says __what__ the agent does, and what it expects, but not __how__ it works (no prompts, models, tools, nor data sources)

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise2/email_bot_server.py" from="27" to="43" %}}

- Input is a __data part__ (structured JSON), not free text: no need to _parse_ e-mails out of natural language
- The description warns that tasks may take _hours_ (a human approves): clients should not wait with a short timeout
- Missing here, and needed across organisations: `security_schemes` (e.g. OAuth2, API keys), to _authenticate_ clients

---

## Exercise 2 — Solution: tasks ↔ threads, steps ↔ status updates

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise2/email_bot_server.py" from="59" to="76" %}}

- Input is __validated__ first (`get_data_parts`: the JSON objects in the message's data parts): malformed requests are _rejected_; `say(text)` (not shown) builds a message of the agent, within the task
- One A2A __task__ = one LangGraph __thread__ (`thread_id = task.id`); `AsyncSqliteSaver`: the asynchronous SQLite checkpointer, as the executor is `async`
- `astream` streams the workflow's steps, which become `working` status updates (the client sees the progress)
- The approval is asked __out of band__, to the office (`self.approve`, by default `ask_human` on the server's terminal), _not_ to the client: the help desk belongs to another organisation, and cannot approve the office's replies
    + hence, the task stays `working` while waiting, rather than `input-required` (which would ask the _client_ for input)

---

## Exercise 2 — Solution: outcomes, and the client

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise2/email_bot_server.py" from="78" to="84" %}}

- __Completed__ with the reply as an _artifact_, or __rejected__ with a message; escalations say _nothing_ of why (the client may be the attacker)

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise2/helpdesk_client.py" from="21" to="35" %}}

- `new_data_message(obj)`: a message with one data part; the rest is as in [Example 4 (bis)](#/a2a-example)

---

## Exercise 2 — Solution: tests, with an in-process server

> No network, no port: the server's ASGI app is plugged _directly_ into the client's HTTP transport

{{% code path="static/lab-snippets/snippets/lecture_workflows/exercise2/test_email_bot_a2a.py" from="28" to="49" %}}

- `httpx.ASGITransport(app=...)`: HTTP requests are handled by the app, in the same process; `app(card, executor)` is the server of [Example 4 (bis)](#/a2a-example)
- The office is _simulated_ (`approve=lambda request: ...`); the same tests run _offline_ in [`tests/test_workflows.py`](../lab-snippets/tests/test_workflows.py), with the fakes of [Exercise 1](#/exercise-email-bot-solution)

---

## Exercise 2 — Solution: Project Structure

<div class="highlight"><pre tabindex="0" style="background-color:#f8f8f8;"><code class="nohighlight" data-noescape>lab-snippets/
├── snippets/
│   └── lecture_workflows/
│       ├── example4bis/
│       │   └── <a href="../lab-snippets/snippets/lecture_workflows/example4bis/regulations_server.py">regulations_server.py</a>    # app(card, executor) (reused)
│       ├── exercise1/
│       │   └── <a href="../lab-snippets/snippets/lecture_workflows/exercise1/bot.py">bot.py</a>                   # the workflow (reused)
│       └── exercise2/
│           ├── <a href="../lab-snippets/snippets/lecture_workflows/exercise2/email_bot_server.py">email_bot_server.py</a>      # Agent Card, executor, server
│           ├── <a href="../lab-snippets/snippets/lecture_workflows/exercise2/helpdesk_client.py">helpdesk_client.py</a>       # a client
│           └── <a href="../lab-snippets/snippets/lecture_workflows/exercise2/test_email_bot_a2a.py">test_email_bot_a2a.py</a>    # end-to-end tests
└── tests/
    └── <a href="../lab-snippets/tests/test_workflows.py">test_workflows.py</a>                # offline tests (fakes)</code></pre></div>

- run the server (`email_bot_server.py`), then the client (`helpdesk_client.py [EMAIL_ID ...]`) in another terminal, via `poetry run python -m snippets -l workflows -x 2`; approve replies on the _server_'s terminal
- env vars as in [Exercise 1](#/exercise-email-bot-solution), plus `EMAIL_BOT_PORT` (server, default `9998`) and `EMAIL_BOT_URL` (client)

{{% /section %}}

---

## What's next?

- Workflows give back _control_ to the engineer: fixed processes, explicit state, human checkpoints, traces
- Yet _choosing_ between prompting, RAG, tools, skills, workflows, and multi-agent systems is a __trade-off__ among quality, cost, control, compliance, and time-to-market
- Next, we'll see __AI Governance 101__: how to take (and _document_) these decisions, in the face of regulations and responsibilities

---

{{% import path="reusable/back.md" %}}

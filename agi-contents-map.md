Coverage legend: `[x]` covered by slides (lecture dir in backticks), `[ ]` not covered yet (notes say what partially exists).

Covered but not in this map: `genai` (Generative AI 101, intro lecture); `llmaas` exercises on request caching and retry with exponential backoff.

0. Programmatic interfaces for LLMaaS
    - Topics:
        * [x] architectural overview — `llmaas`
        * [x] WebAPIs and the programmatic APIs wrapping them (eg Python) — `llmaas`
        * [x] API keys, cost models, service providers (e.g. OR) — `llmaas`
            + [x] analogies and differences among API standards — `llmaas`
        * [x] Ollama and local deployment — `llmaas`
            + [ ] commonly recommended hardware/software requirements (only supported platforms are listed)
                - [ ] quantization (e.g. GGUF) and model size vs. VRAM/RAM
        * [ ] Model zoo (Ollama's and OR's zoos are only browsed in examples)
            + [ ] how to choose a model for a given task
                - [ ] how to evaluate models
            + [ ] italian / european initiatives for open-models (maturity, issues, etc.)
                - [ ] eg. OpenLLM, ALT-EDIC, LLMs4EU, Minerva
            + [ ] open weights vs. open source: licensing of models _(proposed)_
    - Exercises:
        * [x] E0.1: building CLI for LLM — `llmaas` (examples 1 and 2: sync and async/streaming CLI chat)
        * [x] E0.2: extract structured information from pictures with text (`llmaas` exercise 4 does that with ID documents)

1. Prompt engineering & structured outputs
    - Topics:
        * [ ] Fundamentals of prompt engineering (input, context, expected output)
        * [ ] Overview on prompt engineering techniques
            + [ ] few-shot prompting, chain-of-thought
            + [ ] reasoning models (reasoning effort, reasoning tokens)
        * [x] System prompt / user prompt, completion API, conversation — `llmaas` (Chat Completion API, message roles)
        * [x] Structured outputs & related technicalities (pydantic, JSON, etc) — `llmaas`
        * [x] Multimodal input (e.g. images) — `llmaas` (exercise 4)
        * [ ] Context management: context window limits, token budgets, prompt caching, conversation summarization/compaction
        * [ ] Validating generative software (scorers + LLM-as-a-Judge) (LLM-as-a-Judge only named in `genai`)
            + examples on selected tecnologies (e.g. `deepeval`, `mlflow`, etc)
    - Exercises
        * [x] E1.1: Similar to E0.2, but with clear system/user prompt, structured outputs, and multiple queries for precisions (`llmaas` example 3 and exercise 3 do structured scoring of presentation letters instead)
        * [ ] E1.2: Set-up testing infrastructure for E1.1 with target testing framework

2. Tools and agents
    - Topics:
        * [ ] Agentic metaphor: tools for perception&actuation, LLM for deliberation, agents as controllers
            + [ ] excursis classical agents vs. LLM agents: autonomy, BDI-style perceive/deliberate/act, what LLMs actually replace
        * [ ] Functions as tools (importance of documentation) (tool-call messages and `tool_choice` only shown in `llmaas`)
        * [ ] Building an agent that calls a tool from scratch
            + [ ] the ReAct loop (reason + act)
        * [ ] MCP protocol, MCP gateway (MCP only named in `genai`)
        * [ ] Agents with tools with LangChain
        * [ ] Evaluating agents: trajectories, tool-call correctness, regression tests
        * [ ] Security of agentic systems: prompt injection, least privilege for tools, sandboxing tool execution, secrets out of context
    - Exercises:
        * [ ] E2.1: Building an agent that calls a tool from scratch with OpenAI client lib (code exists, not in slides: `content/llmaas/repl_chat_with_tools_openai*.py`)
        * [ ] E2.2: Building an agent that calls a tool via LangChain (precooked agentic lib) (code exists, not in slides: `content/llmaas/repl_chat_with_tools_langchain*.py`)
        * [ ] E2.3: Setup MCP gateway with 2+ tool servers, attaching LLM to it

3. Retrieval augemented generation (RAG)
    - Topics:
        * [ ] Agentic metaphor: memory & focus
        * [ ] Semantic indexing, embeddings, embedding scores
        * [ ] Chunking, metadata, retrieval
        * [ ] LangChain API and database adapters
        * [ ] Evaluating RAG: retrieval metrics (e.g. precision/recall@k), answer groundedness
        * [ ] Prompt injection via retrieved documents
    - Exercises:
        * [ ] E3.1: Q/A about the slides of a course

4. Agentic skills
    - Topics:
        * [ ] Platform-agnostic definition of skill (textally-described reusable functionality)
        * [ ] Context: copilots frameworks (Claude Code, Codex, Cursor, OpenClaw)
        * [ ] Convention for writing skills (SKILL.md, json files, Python scripts, etc.)
            + [ ] allowing tools in skills
            + [ ] skills as a context-loading mechanism (progressive disclosure)
        * [ ] Convention for testing skills
        * [ ] Hooks and events for skills
            + [ ] Analogies and differences among technologies (sorts of events, configuration files, etc)
            + [ ] https://github.com/responsibleai/agent-hooks
        * [ ] Publishing / installing skills
        * [ ] Anatomy of interesting skills: [ponytail](https://github.com/dietrichgebert/ponytail)
        * [ ] Security of skills: trusting third-party skills, tool permissions
    - Exercises:
        * [ ] E4.1: Creating a pre-check skill for student theses

5. Workflows and Agent Orchestration
    - Topics:
        * [ ] Workflows as state machines
        * [ ] LLM steps, Data steps, Action steps, User input steps
        * [ ] State management
        * [ ] Patterns (prompt chaining, master-worker, evaluator-optimizer, routing, human-in-the-loop, etc)
            + [ ] plan-and-execute _(proposed)_
        * [ ] Multi-agent systems: agent communication, A2A protocol (vs. MCP)
        * [ ] Streaming and observability
        * [ ] Evaluating workflows end-to-end (reusing the E1.2 infrastructure)
    - Exercises:
        * [ ] E5.1: Semi-automatic customer support email bot with LangGraph

6. AI governance 101
    - Topics:
        * [ ] AI in cloud vs local providers vs on-premise (cost/control/privacy considerations) (on-premise vs on-cloud trade-offs introduced in `llmaas`)
        * [ ] trade-offs among quality, cost, control, compliance, and time-to-market (e.g. in skills vs ad-hoc workflow with tools+LLM)
            + [ ] regulation: EU AI Act, GDPR, UniBo GenAI policy
        * [ ] guidelines for technology selection upon use case patterns
            + [ ] prompting vs. RAG vs. fine-tuning
        * [ ] detail on model evaluation: model cards and model evaluation (maybe mention ARC-AGI, and other benchmarks?)


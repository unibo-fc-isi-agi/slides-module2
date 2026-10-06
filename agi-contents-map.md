Coverage legend: `[x]` covered by slides (lecture dir in backticks), `[ ]` not covered yet (notes say what partially exists).

Covered but not in this map: `genai` (Generative AI 101, intro lecture; incl. agentic interfaces, "customers buy automation", the 3 ways engineers exploit GenAI — coding assistants / hard-to-code automation / agents in products —, language vs. action); `llmaas` exercises on request caching and retry with exponential backoff; `llmaas` Example 1 bis (Anthropic Messages API via Ollama) + cross-provider API comparison table.

0. Programmatic interfaces for LLMaaS
    - Topics:
        * [x] architectural overview — `llmaas`
        * [x] WebAPIs and the programmatic APIs wrapping them (eg Python) — `llmaas`
        * [x] API keys, cost models, service providers (e.g. OR) — `llmaas`
            + [x] analogies and differences among API standards — `llmaas`
        * [x] Ollama and local deployment — `llmaas`
            + [x] commonly recommended hardware/software requirements — `llmaas`
                - [x] quantization (e.g. GGUF) and model size vs. VRAM/RAM — `llmaas`
        * [x] Model zoo — `llmaas`
            + [x] how to choose a model for a given task — `governance`
                - [x] how to evaluate models — `governance` (benchmarks, leaderboards, task-specific evaluation; exercise 1)
            + [x] italian / european initiatives for open-models (maturity, issues, etc.) — `governance`
                - [x] eg. OpenLLM, ALT-EDIC, LLMs4EU, Minerva — `governance`
            + [x] open weights vs. open source: licensing of models _(proposed)_ — `governance`
    - Exercises:
        * [x] E0.1: building CLI for LLM — `llmaas` (examples 1 and 2: sync and async/streaming CLI chat)
        * [x] E0.2: extract structured information from pictures with text — `prompting` (exercise 2, with ID documents)

1. Prompt engineering & structured outputs
    - Topics:
        * [x] Fundamentals of prompt engineering (input, context, expected output) — `prompting` (anatomy of a prompt, best practices)
        * [x] Overview on prompt engineering techniques — `prompting` (+ self-consistency, prompt chaining; example 2)
            + [x] few-shot prompting, chain-of-thought — `prompting`
            + [x] reasoning models (reasoning effort, reasoning tokens) — `prompting` (example 3)
        * [x] System prompt / user prompt, completion API, conversation — `llmaas` (Chat Completion API, message roles), `prompting` (prompt anatomy)
        * [x] Structured outputs & related technicalities (pydantic, JSON, etc) — `prompting` (example 1 with OpenAI, 1 bis with LangChain, constrained decoding)
        * [x] Multimodal input (e.g. images) — `prompting` (exercise 2)
        * [x] Context management: context window limits, token budgets, prompt caching, conversation summarization/compaction — `prompting` (example 4: CLI chat with compaction)
        * [x] Validating generative software (scorers + LLM-as-a-Judge) — `validating`
            + [x] examples on selected tecnologies (e.g. `deepeval`, `mlflow`, etc) — `validating` (example 1 with DeepEval, 1 bis with MLflow)
    - Exercises
        * [x] E1.1: Similar to E0.2, but with clear system/user prompt, structured outputs, and multiple queries for precisions — `prompting` (exercise 2, field-by-field voting; exercise 1 does checklist scoring of letters)
        * [x] E1.2: Set-up testing infrastructure for E1.1 with target testing framework — `validating` (exercise 2; exercise 1 completes the test suite of the letter-scoring system, field by field)

2. Tools and agents
    - Topics:
        * [x] Agentic metaphor: tools for perception&actuation, LLM for deliberation, agents as controllers — `agents`
            + [x] excursis classical agents vs. LLM agents: autonomy, BDI-style perceive/deliberate/act, what LLMs actually replace — `agents`
            + [x] LLMs are not agents by themselves: agent = controller + LLM + tools + memory + policies; intelligence vs. autonomy vs. agency (Floridi 2025) — `agents` (recalled from `genai`)
        * [x] Spectrum of autonomy: workflows (code controls the flow) vs. agents (LLM controls the flow); least autonomy that does the job (cf. Anthropic's "Building effective agents") — `agents`
        * [x] Functions as tools (importance of documentation) — `agents` (good-tools table, cross-provider landscape)
        * [x] Building an agent that calls a tool from scratch — `agents` (example 1)
            + [x] the ReAct loop (reason + act) — `agents`
        * [x] MCP protocol, MCP gateway — `agents` (example 2: FastMCP server, MCP Inspector, langchain-mcp-adapters)
        * [x] Agents with tools with LangChain — `agents` (example 1 bis, `create_agent`)
        * [x] Evaluating agents: trajectories, tool-call correctness, regression tests — `agents` (example 3, pytest)
            + [x] agentic benchmarks (GAIA, WebArena, AgentBench, SWE-bench, ARC-AGI-3): representation as the bottleneck; success without governance is not trustworthy agency — `agents` (+ τ-bench, harness effect on ARC-AGI-3) (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
        * [x] LLMs can't plan, but can help planning (LLM-Modulo, PlanBench): plans vs. plan-shaped text; LLMs as translators, critics, heuristic sources; external validation — `agents` (+ plan before acting) (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
        * [x] Security of agentic systems: prompt injection, least privilege for tools, sandboxing tool execution, secrets out of context — `agents` (+ lethal trifecta)
            + [x] tools change the risk profile: read-only (information), write-enabled (action), external (dependency), institutional (accountability) risks — `agents` (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
    - Exercises:
        * [x] E2.1: Building an agent that calls a tool from scratch with OpenAI client lib — `agents` example 1
        * [x] E2.2: Building an agent that calls a tool via LangChain (precooked agentic lib) — `agents` example 1 bis
        * [x] E2.3: Setup MCP gateway with 2+ tool servers, attaching LLM to it — `agents` exercise 3 (exercise 1: read-only tools to inspect applications; exercise 2: write tools with human-in-the-loop + prompt injection test)

3. Retrieval augemented generation (RAG)
    - Topics:
        * [ ] Agentic metaphor: memory & focus
            + [ ] memory is not "more context": working/episodic/semantic/procedural memory; memory governance (provenance, staleness, forgetting, privacy) _(proposed)_ (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
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
        * [ ] Context: copilots frameworks (Claude Code, Codex, Cursor, OpenClaw) (introduced in `genai`)
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
        * [ ] Intermediate representations (checklists, plans, schemas, process models, tool contracts): intention → representation → verification → execution _(proposed)_ (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
            + [ ] plan before acting, log & trace, verify & test; ask humans for irreversible / norm-sensitive actions _(proposed)_ (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
        * [ ] Multi-agent systems: agent communication, A2A protocol (vs. MCP)
        * [ ] Streaming and observability
        * [ ] Evaluating workflows end-to-end (reusing the E1.2 infrastructure)
    - Exercises:
        * [ ] E5.1: Semi-automatic customer support email bot with LangGraph

6. AI governance 101
    - Topics:
        * [x] AI in cloud vs local providers vs on-premise (cost/control/privacy considerations) — `governance` (with worked cost example)
        * [x] trade-offs among quality, cost, control, compliance, and time-to-market (e.g. in skills vs ad-hoc workflow with tools+LLM) — `governance`
            + [x] regulation: EU AI Act, GDPR, UniBo GenAI policy — `governance` (+ Italian L. 132/2025)
        * [x] guidelines for technology selection upon use case patterns — `governance`
            + [x] prompting vs. RAG vs. fine-tuning — `governance`
        * [x] detail on model evaluation: model cards and model evaluation (maybe mention ARC-AGI, and other benchmarks?) — `governance`
        * [ ] Enveloping (Floridi): the world adapting to AI; bad (silent adaptation) vs. good (explicit, contestable representations) enveloping _(proposed)_ (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
        * [ ] Responsibility remains human: biases in LLM-agent use (over-trust, artificial salience, false certainty) and countermeasures _(proposed)_ (cf. keynote "From Language to Agency", SKILLED-LLMs 2026)
    - Exercises:
        * [x] E6.1: Comparing models on the running example (quality, consistency, latency, cost) — `governance` exercise 1
        * [x] E6.2: Governance decision record for the running example (AI Act, GDPR, deployment, model, oversight) — `governance` exercise 2


0. Programmatic interfaces for LLMaaS
    - Topics:
        * architectural overview
        * WebAPIs and the programmatic APIs wrapping them (eg Python)
        * API keys, cost models, service providers (e.g. OR)
            + analogies and differences among API standards
        * Ollama and local deployment
            + commonly recommended hardware/software requirements
        * Model zoo
            + how to choose a model for a given task
                - how to evaluate models
                - excursus on model cards and model evaluation (maybe mention ARC-AGI, and other benchmarks?)
            + italian / european initiatives for open-models (maturity, issues, etc.)
                - eg. OpenLLM, ALT-EDIC, LLMs4EU, Minerva
    - Exercises:
        * E0.1: building CLI for LLM
        * E0.2: extract weighted (by ECTS) score in CS-realated courses from the *scan* of a foreigner student's academic records

1. Prompt engineering & structured outputs
    - Topics:
        * Fundamentals of prompt engineering (input, context, expected output)
        * Overview on prompt engineering techniques
        * System prompt / user prompt, completion API, conversation
        * Structured outputs & related technicalities (pydantic, JSON, etc)
        * Validating generative software (scorers + LLM-as-a-Judge)
    - Exercises
        * E1.1: Same of E0.2, but with clear system/user prompt, structured outputs, and multiple queries for precisions
        * E1.2: Set-up testing infrastructure for E1.1 with mlflow

2. Tools and agents
    - Topics:
        * Agentic metaphor: tools for perception&actuation, LLM for deliberation, agents as controllers
        * Functions as tools (importance of documentation)
        * Building an agent that calls a tool from scratch
        * MCP protocol, MCP gateway
        * Agents with tools with LangChain
    - Exercises:
        * E2.1: Building an agent that calls a tool from scratch with OpenAI client lib
        * E2.2: Building an agent that calls a tool via LangChain (precooked agentic lib)
        * E2.3: Setup MCP gateway with 2+ tool servers, attaching LLM to it

3. Retrieval augemented generation (RAG)
    - Topics:
        * Agentic metaphor: memory & focus
        * Semantic indexing, embeddings, embedding scores
        * Chunking, metadata, retrieval
        * LangChain API and database adapters
    - Exercises:
        * E3.1: Q/A about the slides of a course

4. Agentic skills
    - Topics:
        * Platform-agnostic definition of skill (textally-described reusable functionality)
        * Context: copilots frameworks (Claude Code, Codex, Cursor, OpenClaw)
        * Convention for writing skills (SKILL.md, json files, Python scripts, etc.)
            + allowing tools in skills
        * Convention for testing skills
        * Hooks and events for skills
            + Analogies and differences among technologies (sorts of events, configuration files, etc)
            + https://github.com/responsibleai/agent-hooks
        * Publishing / installing skills
        * Anatomy of interesting skills: [ponytail](https://github.com/dietrichgebert/ponytail)
    - Exercises:
        * E4.1: Creating a pre-check skill for student theses

5. Workflows and Agent Orchestration
    - Topics:
        * Workflows as state machines
        * LLM steps, Data steps, Action steps, User input steps
        * State management
        * Patterns (prompt chaining, master-worker, evaluator-optimizer, routing, human-in-the-loop, etc)
        * Streaming and observability
    - Exercises:
        * E5.1: Semi-automatic customer support email bot with LangGraph

6. AI governance 101
    - Topics:
        * AI in cloud vs local providers vs on-premise (cost/control/privacy considerations)
        * trade-offs among quality, cost, control, compliance, and time-to-market (e.g. in skills vs ad-hoc workflow with tools+LLM)
        * guidelines for technology selection upon use case patterns
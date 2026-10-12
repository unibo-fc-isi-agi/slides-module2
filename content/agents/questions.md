+++
title = "Tools and Agents — Questions"
[build]
render = "never"
list = "never"
+++

# Tools and Agents — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of API signatures, protocol versions, or benchmark scores.

## Agents and tools

1. **[notions; theoretical]** What is an agent, and what changes when its deliberation relies on an LLM? Explain the roles of perception, action, goals, state, and the controller.

2. **[reasoning; theoretical]** How do intelligence, autonomy, and agency differ? Give examples showing why improving one does not necessarily improve the others.

3. **[reasoning; theoretical]** When does a task need an agent rather than a single LLM call or a predefined workflow? What costs come with giving the model more control?

4. **[know-how; theoretical]** How would you design a tool that an LLM can use reliably? Explain what its interface should communicate about arguments, results, errors, and side effects.

5. **[reasoning; theoretical]** Does giving an agent more tools always make it more capable? How could you make a large collection of tools available without presenting every definition at every step?

6. **[know-how; theoretical]** How would you implement a ReAct controller? Explain how it associates tool results with calls, handles dependencies and failures, and decides when to stop.

7. **[reasoning; theoretical]** If a tool call conforms to its JSON Schema, is it safe to execute? What checks remain necessary, and where should they happen?

8. **[know-how; practical]** How would you build a tool-using agent with LangChain? Explain what the framework provides compared with a loop written using a provider's SDK, and what policies you still need to implement.

9. **[know-how; theoretical]** How would you design tools for an assistant that answers questions across text documents and images? Discuss where extraction and computation should happen, what to return to the agent, and when caching is appropriate.

## Tool integration and MCP

10. **[notions; practical]** What problem does MCP solve? Explain the roles of hosts, clients, and servers, and distinguish tools, resources, and prompts.

11. **[know-how; practical]** How would you expose existing Python functions through an MCP server and connect an agent to them? Compare local stdio and remote HTTP connections, including how you would diagnose a connection or tool-call failure.

12. **[reasoning; theoretical]** Compare tools executed inside the agent's process, tools accessed through a separate server, and tools executed by the model provider. How do these arrangements affect reuse, control, isolation, and failure handling?

13. **[know-how; practical]** How would you configure an MCP gateway shared by several applications with different permissions? Explain how you would handle tool names, credentials, access checks, and logging, including when a host fails to enforce its own policies.

14. **[reasoning; theoretical]** Does using a standard tool protocol make third-party tools trustworthy? Discuss the risks of tool descriptions as well as executable code, including changes made after a tool was approved.

## Evaluation and planning

15. **[reasoning; theoretical]** Why is checking an agent's final answer insufficient? Explain what its trajectory can reveal, and when requiring an exact sequence of tool calls would be too restrictive.

16. **[know-how; practical]** How would you test an agent's tool selection, arguments, efficiency, and handling of unavailable information? Explain how you would separate agent failures from tool or external-service failures.

17. **[reasoning; theoretical]** What can an agentic benchmark establish about an agent's capabilities? Discuss the influence of the harness, task representation, repeated-run reliability, and the way the goal was achieved.

18. **[reasoning; theoretical]** What distinguishes an executable plan from a plausible description of steps? Explain how explicit states, preconditions, and effects help assess a proposed plan.

19. **[know-how; theoretical]** How could you combine an LLM with external planners or validators to solve a planning task? Explain the generate–test–critique approach and the limits of the guarantees it provides.

## Security and actions with consequences

20. **[reasoning; theoretical]** How does adding tools change an LLM-based system's risks? Is an agent with only read-only tools necessarily harmless?

21. **[know-how; theoretical]** How would you protect an agent that reads untrusted documents, accesses private data, and communicates externally? Explain direct and indirect prompt injection, and distinguish prompt-level mitigations from enforced restrictions.

22. **[know-how; practical]** How would you implement human approval for selected tool calls in an agent framework? Explain what the reviewer must see and how approval, editing, and rejection affect execution.

23. **[reasoning; theoretical]** Why does idempotency matter for tools that change state? Compare recording a decision with sending a notification, and explain what could go wrong after a timeout or retry.

24. **[know-how; theoretical]** How would you test that an agent cannot perform an unauthorised action, even if a document tells it the action was already approved? Distinguish testing the agent's proposals from testing the actual effects and the controls around execution.

## Scope and coverage

| Topic | Questions |
|---|---|
| Classical agents, situated control loops, BDI, artifacts, LLM deliberation, controller, memory and policies | 1 |
| Intelligence, autonomy, agency; least autonomy; workflow versus agent | 2, 3 |
| Tools for perception, computation and actuation; definitions versus calls and execution | 1, 4, 6, 9 |
| Tool names, descriptions, schemas, units, useful results, actionable errors | 4, 7 |
| Tool overload, deferred discovery, selection, tools exposed as code | 5 |
| ReAct, call IDs, history ordering, multiple calls, dependencies, recovery, bounded execution | 6 |
| Strict arguments versus valid values, allow-lists, path/query restrictions | 7, 9, 21 |
| From-scratch controller versus LangChain, schema derivation, middleware, limits, message state | 6, 8 |
| Read-only document tools, extraction inside tools, multimodality, caching, deterministic computations | 9 |
| MCP interoperability, host/client/server, tools/resources/prompts, discovery and invocation | 10, 11 |
| FastMCP, client adapters, Inspector, stdio protocol channel, process environment, HTTP authentication | 11 |
| In-process, MCP, and provider-hosted tools; reuse, isolation, overhead and control | 12 |
| Gateways, aggregation, name clashes, profiles, secrets, logs, server outages, enforcement boundaries | 13 |
| Third-party dependencies, tool poisoning, changing descriptions, pinning and review | 14 |
| Final answers versus trajectories, grounding, forbidden calls, order, strict/unordered/partial matching | 15, 16 |
| Tool isolation, mocked services, regression tests, repeated runs, unavailable or ambiguous information | 16, 24 |
| Agentic benchmarks, task diversity, harness effects, representation, pass^k, saturation and contamination | 17 |
| Classical planning, explicit world models, executable plans versus generated text, formal-domain evaluation | 18 |
| LLM-Modulo, hard/soft/policy critics, translators, heuristics, model drafting, verification before action | 19 |
| Information, action, dependency, institutional and physical risks | 20 |
| Direct/indirect injection, private data plus untrusted content plus external communication | 21 |
| Least privilege, sandboxing, validation, secrets out of context, delimiters, logging | 7, 13, 21 |
| Human approval in the controller, pause/resume, reviewed arguments, rejection handling | 22, 24 |
| Write-enabled tools, idempotent updates, non-idempotent effects, retry hazards | 23 |
| Simulated human decisions, temporary outputs, adversarial documents, deterministic gateway-policy tests | 24 |
| Exercises: document inspection, decision tools, and a shared MCP gateway | 9, 13, 16, 21–24 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Questions concern reusable designs and failure modes, rather than recall of particular tools, candidates, or benchmark results.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Memory types, embeddings, retrieval pipelines, vector stores, RAG-specific evaluation | Retrieval-Augmented Generation |
| Packaged skills, progressive loading of skill content, skill testing and lifecycle | Agentic Skills |
| Durable workflow state, checkpoints in depth, plan-and-execute implementations, multi-agent systems and A2A | Workflows and Agent Orchestration |
| Model-selection studies, deployment economics, regulation and organisational accountability | AI Governance 101 |

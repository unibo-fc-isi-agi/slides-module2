+++
title = "Workflows and Agent Orchestration — Questions"
[build]
render = "never"
list = "never"
+++

# Workflows and Agent Orchestration — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of API names, command lines, or framework catalogues.

## Processes, state, and durability

1. **[notions; theoretical]** What makes a process a workflow? Explain the roles of steps, transitions, and state, and distinguish a workflow from an agent following instructions and from a reusable skill.

2. **[know-how; theoretical]** You must process applications, extract information from documents, check eligibility, obtain a committee's decision, and notify applicants. How would you divide this process into LLM, data, human-input, and action steps? Explain where you would put checks and why.

3. **[reasoning; theoretical]** What should a workflow's state contain, and how does it differ from an LLM's context? Explain why state size, serialisability, and merge rules matter, especially when branches run in parallel.

4. **[reasoning; theoretical]** A workflow sends one e-mail, crashes before saving its next checkpoint, and then resumes. What may happen? Explain how checkpoint boundaries, idempotency, and recorded side effects affect the outcome.

5. **[know-how; practical]** How would you make an approval step survive a process restart in a workflow engine such as LangGraph? Explain what is persisted, how the human's answer reaches the suspended run, and what must be checked before an irreversible action proceeds.

6. **[reasoning; practical]** When would you implement a workflow with plain code, and when would you adopt a workflow engine? Compare explicit graphs, event-driven workflows, and general-purpose durable execution in terms of the capabilities your application actually needs.

## Patterns and verifiable plans

7. **[know-how; theoretical]** Given a task with independent document checks, several kinds of incoming requests, and a final decision, which workflow patterns would you combine? Explain when chaining, routing, parallelisation, or an orchestrator with workers would be appropriate, and where their costs or failure modes arise.

8. **[reasoning; theoretical]** When can an evaluator–optimizer loop improve a draft, and when might it repeatedly approve a bad result or never stop? Explain how you would choose evaluation criteria, a stopping rule, and a fallback.

9. **[know-how; theoretical]** A user asks an assistant to identify the best applicant and schedule an interview. How would you structure a plan-and-execute workflow so that unknown values, invalid tool arguments, failed steps, and write actions are handled before the assistant claims success?

10. **[reasoning; theoretical]** Why create an intermediate representation between a natural-language request and an action? Compare what a checklist, schema, plan, process model, or tool contract lets you verify, and explain what still requires human judgement.

## Multiple agents and communication

11. **[notions; theoretical]** What makes a system multi-agent rather than a workflow with several LLM calls? Compare a supervisor, handoffs, a hierarchy, and shared-state coordination in terms of who controls the next action and how agents exchange information.

12. **[reasoning; theoretical]** Would splitting a tightly coupled task among several agents necessarily improve it? Discuss context isolation, specialisation, parallelism, conflicting decisions, verification, and cost; give a case where multiple agents are justified and one where they are not.

13. **[reasoning; theoretical]** A specialist agent reads an untrusted document and returns advice to a supervisor. What could go wrong if the supervisor treats that advice as instructions? Explain how you would constrain permissions and check information crossing agent boundaries.

14. **[notions; practical]** How does an agent use another agent through A2A? Explain what an Agent Card advertises and how messages, parts, tasks, statuses, artifacts, and contexts fit together. How is this different from calling a tool through MCP or installing an Agent Skill?

15. **[know-how; practical]** An external help-desk agent delegates a candidate's e-mail to an admissions agent, whose reply needs approval by admissions staff. How would you expose and follow this long-running task through A2A? Explain task-to-workflow identity, progress updates, approval ownership, terminal outcomes, and what the remote client should be allowed to see.

## Observing, testing, and applying workflows

16. **[reasoning; theoretical]** What can users learn from streamed progress, and what can developers learn from a trace after a run? Explain why a graph with parallel branches may still execute slowly or sequentially, and what evidence would reveal the cause.

17. **[know-how; practical]** How would you observe a long-running workflow with a tracing system such as MLflow or an OpenTelemetry-compatible backend? Explain which steps and calls should be connected in a trace, how you would use it to diagnose a wrong result, and what sensitive information it might contain.

18. **[know-how; theoretical]** How would you test a workflow at the step, path, and end-to-end levels? Give examples of invariants involving approval, routing, retries, and duplicate actions, and explain where fake LLM outputs help and where real-model tests remain necessary.

19. **[know-how; theoretical]** Design a workflow for answering applicants' e-mails using regulations and private application records. Explain how you would route mixed or suspicious requests, verify the sender before using personal data, bound draft revision, involve a human, and resume safely after an interruption.

20. **[reasoning; theoretical]** A workflow's final report says an interview was scheduled, but the action step failed. How could that discrepancy survive a plausible-looking trace or approval? Explain how you would compare the request, plan, execution record, and final report to detect and prevent it.

## Scope and coverage

| Topic | Questions |
|---|---|
| Workflow concept, autonomy, kinds of steps, admission example | 1–2 |
| State, context, parallel merge, checkpoints, durable execution, interrupts, idempotent actions | 3–5 |
| From-scratch and LangGraph implementations; workflow-engine landscape and metamodels | 5–6 |
| Chaining, routing, parallelisation, orchestrator–workers, evaluator–optimizer, human-in-the-loop | 2, 7–8, 19 |
| Plan-and-execute, validation, re-planning, preconditions, approval | 9, 20 |
| Intermediate representations, verification, logging, human judgement | 10, 20 |
| Multi-agent concept, architectures, benefits, costs, and trust boundaries | 11–13 |
| A2A concepts, A2A versus MCP, remote-agent lifecycle, admissions-bot exercise | 14–15 |
| Streaming, traces, observability technologies, privacy, actual parallelism | 16–17 |
| Step, path, and end-to-end evaluation; e-mail-bot exercise | 18–19 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Framework API spellings, protocol version numbers, benchmark percentages, and the exact details of the running example are not assessment targets.

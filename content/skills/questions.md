+++
title = "Agentic Skills — Questions"
[build]
render = "never"
list = "never"
+++

# Agentic Skills — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of installation commands, metadata limits, or event-name catalogues.

## Designing and using skills

1. **[notions; theoretical]** What is an agentic skill? Explain its relationship to procedural memory, and distinguish it from a system prompt, a tool, an MCP server, and a workflow.

2. **[reasoning; theoretical]** How does progressive disclosure make a collection of skills usable within a limited context? Compare it with loading every procedure upfront and with retrieving documents through RAG.

3. **[know-how; practical]** How would you turn a team's recurring procedure into an Agent Skills package? Explain what belongs in `SKILL.md`, its description, references, and assets, and how you would state when the skill should not be used.

4. **[reasoning; theoretical]** Which parts of a skill should be natural-language instructions, and which should be executable scripts? Explain how the choice affects reliability, flexibility, context use, and testability.

5. **[know-how; theoretical]** How would you add skill support to an existing agent? Distinguish discovery, advertising, loading, and execution, and explain which decisions belong to the model and which to its controller.

6. **[know-how; practical]** How would you use the same skill in a coding-agent harness and in an application built with Deep Agents? What would you check about discovery, file access, script execution, and harness-specific extensions?

7. **[reasoning; practical]** Does a skill's `allowed-tools` declaration or a filesystem backend's root directory provide a security sandbox? Explain what permissions and execution boundaries must actually be checked.

## Testing skills

8. **[notions; theoretical]** What can static validation establish about a skill, and what requires running an agent? Distinguish a valid package, correct scripts, correct activation, and useful outcomes.

9. **[know-how; theoretical]** How would you test whether an agent selects the right skill? Discuss near misses, overlapping descriptions, explicit requests, and how to improve a description without overfitting the test queries.

10. **[know-how; practical]** How would you measure whether a skill improves an agent's work? Describe an evaluation using a skill-testing tool or your own test suite, including the baseline and the evidence you would collect.

## Hooks and enforced behaviour

11. **[notions; theoretical]** What is a hook in an agent harness? Explain the event–callback contract and how a hook differs from an instruction the model is asked to follow.

12. **[know-how; practical]** How would you port a hook between two harnesses? Explain what must be checked beyond matching event names, and how you would separate shared policy logic from harness-specific adapters.

13. **[reasoning; theoretical]** A hook blocks known network tools and shell commands containing `curl`. Does it prevent an agent from leaking private data? Explain how event coverage, alternative execution paths, and sandboxing affect the answer.

14. **[reasoning; theoretical]** What should happen if a policy hook crashes, times out, or returns an invalid response? Compare failing open with failing closed, and explain why a hook intended to improve reliability could itself prevent progress.

15. **[know-how; theoretical]** How would you make a behavioural skill remain available after context compaction and when work is delegated to another agent? Distinguish preserving its instructions from guaranteeing that they are followed.

## Distribution, trust, and application

16. **[know-how; practical]** How would you distribute and maintain a skill for a team? Compare project and personal installation, and explain when a skill folder is sufficient and when a harness-specific plugin is needed.

17. **[know-how; theoretical]** What would you review before installing or updating a third-party skill? Discuss risks in instructions, references, scripts, and bundled hooks, and the limits of registry scanning or user confirmation.

18. **[know-how; theoretical]** How would you design a skill that reviews a long document and reports issues without modifying it? Explain how you would combine automated checks, selective reading, and judgement, and test both its usefulness and its scope boundaries.

## Scope and coverage

| Topic | Questions |
|---|---|
| Skills as procedural memory, reusable procedures, relation to plan libraries and organisational procedures | 1, 3 |
| Skills versus prompts, tools, MCP and workflows; domain ownership and predictability | 1, 4 |
| Metadata, instructions and resources as progressive-disclosure levels; context costs; comparison with RAG | 2 |
| Agent Skills format, YAML metadata, Markdown body, descriptions, relative paths, scripts/references/assets | 3, 8 |
| Authoring practices, scope, degree of freedom, checklists, feedback loops, maintaining instructions | 3, 4, 18 |
| Scripts versus judgement, generic harness tools, execution requirements, outputs entering context | 4, 5 |
| Controller support: discovery, parsing, advertising, loading, script execution | 5 |
| Coding-agent extension points, instruction files, skills, MCP, hooks, subagents, plugins | 1, 6, 11, 15, 16 |
| Shared specification versus harness extensions, locations, activation mechanisms, cross-harness use | 3, 6, 16 |
| From-scratch support versus Deep Agents, dedicated/generic tools, backends, approval | 5–7 |
| Tool pre-approval versus confinement, filesystem access versus shell access | 7, 13 |
| Static package validation, referenced resources, script unit tests | 8 |
| Triggering tests, trajectories, positive/negative/near-miss cases, held-out queries | 9 |
| Outcome tests, baselines, repeated runs, framework support, model/harness dependence | 10 |
| Hooks, lifecycle events, callbacks, inversion of control, payloads and verdicts | 11 |
| Hook registration, event granularity, model/tool interception, differing protocols and semantics | 12 |
| Harness-neutral policy core, adapters, vendor-neutral contracts, cross-harness test matrix | 12 |
| Privacy-guard hook, deterministic tests, path restrictions, deny-list limits, sandboxing | 7, 12, 13 |
| Hook failures, fail-open/fail-closed behaviour, stop hooks and loops | 14 |
| Behavioural skills such as ponytail: persistence, user modes, compaction, subagent context, outcome claims | 10, 15 |
| Publishing, installation scopes, repositories, plugins, marketplaces, versions and updates | 16, 17 |
| Malicious skill instructions and prerequisites, supply-chain risks, excessive permissions | 17 |
| Review, pinning, scanning limits, least privilege, sandbox boundaries, trusted distribution | 7, 13, 17 |
| Exercise: document pre-check, objective versus judgement findings, evidence and report templates | 18 |
| Long-document context management, script-generated sections, user files versus skill resources | 2, 6, 18 |
| Exercise tests: planted defects, unintended rewriting, injected document instructions, portable evaluations | 9, 10, 17, 18 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. The lecture's history, product comparisons, security incidents, and behavioural-skill case study illustrate general design choices. Dates, adoption counts, benchmark percentages, and exhaustive hook-event lists are not assessment targets.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Durable workflow execution, checkpoints in depth, orchestration patterns, multi-agent coordination and A2A | Workflows and Agent Orchestration |
| Organisation-wide technology selection, deployment economics, regulation and accountability | AI Governance 101 |

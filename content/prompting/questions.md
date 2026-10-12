+++
title = "Prompt Engineering & Structured Outputs — Questions"
[build]
render = "never"
list = "never"
+++

# Prompt Engineering & Structured Outputs — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of API signatures or provider-specific limits.

## Designing prompts

1. **[know-how; theoretical]** How would you turn a vague request into a reusable prompt? Discuss how you would distinguish instructions, context, input data, and the expected output.

2. **[reasoning; theoretical]** Should prompts be managed like source code? Explain what should happen when a prompt or its underlying model changes, and why a successful example is insufficient evidence that a prompt works well.

3. **[know-how; theoretical]** When would you use few-shot rather than zero-shot prompting? How would you choose examples, and how could poorly chosen examples make the results worse?

4. **[reasoning; theoretical]** What can asking a model to produce intermediate reasoning steps change about its answer? Discuss the limits of treating a generated explanation as evidence of correct reasoning.

5. **[reasoning; theoretical]** What is self-consistency, and when might it help? Can agreement among repeated answers be interpreted as the probability that the answer is correct?

6. **[know-how; theoretical]** When would you split a task into a chain of prompts rather than use one prompt? Explain how you would choose the intermediate results and deal with errors passed from one step to the next.

## Structured outputs

7. **[reasoning; theoretical]** What is the difference between asking for JSON, obtaining valid JSON, and obtaining an object that conforms to a schema? What does each guarantee about the usefulness and correctness of the result?

8. **[know-how; practical]** How would you use Pydantic to define structured information to extract from a document? Explain how field types, constraints, nesting, and descriptions contribute to the schema sent to the model.

9. **[reasoning; theoretical]** How should an extraction schema represent missing, unknown, or unreadable information? Discuss the difference between a required field, a nullable value, and a default value.

10. **[notions; theoretical]** How can structured output be enforced during generation? Compare constrained decoding, parsing and validation after generation, and using tool-call arguments as the output.

11. **[know-how; practical]** How would you request and consume structured output through an LLM client library? What should your application do if the model does not support the requested schema, refuses the request, or returns an unusable result?

12. **[reasoning; practical]** What does LangChain add to using a provider's client directly? Explain how prompt templates, chat models, and structured outputs can be composed, and what portability this does and does not provide.

13. **[know-how; theoretical]** How would you turn a natural-language scoring policy into an LLM-filled checklist and a deterministic scoring function? Which sources of variability or error would this remove, and which would remain?

## Reasoning and context

14. **[notions; theoretical]** What distinguishes a reasoning model from a model prompted to “think step by step”? Explain the role of reasoning tokens and the trade-off between computation at inference time, cost, latency, and answer quality.

15. **[know-how; practical]** How would you choose and adjust a reasoning budget for an application? What would you measure to decide whether spending more on reasoning is worthwhile?

16. **[reasoning; theoretical]** Is it always beneficial to give an LLM as much context as its window allows? Discuss relevance, position, cost, and the space needed to generate an answer.

17. **[know-how; practical]** How would you keep a long-running chat within a token budget? Compare trimming with summarisation, and explain what you would do if the context still exceeded the budget after compaction.

18. **[reasoning; theoretical]** How does provider-side prompt caching differ from caching complete responses in the client? Explain how prompt layout and context compaction affect the opportunity to reuse cached computation.

## Extracting information from images

19. **[know-how; practical]** How would you extract typed information from an image of a document? Explain how you would supply the image and instructions, and check that the chosen model and API can process them.

20. **[reasoning; theoretical]** Several extractions of the same document disagree. What are the benefits and risks of voting separately on each field? How would you handle failed samples, ties, and a result whose fields are individually plausible but inconsistent together?

## Scope and coverage

| Topic | Questions |
|---|---|
| Prompt anatomy, system/user separation, templates, clarity, context, delimiters, output instructions | 1 |
| Prompt artifacts, version control, registries, empirical improvement, model dependence | 2 |
| Zero-shot, few-shot, example selection, format and label bias | 3 |
| Chain-of-thought, ordering reasoning and answers, post-hoc explanations, format constraints | 4, 7, 14 |
| Self-consistency, sampling diversity, agreement versus correctness, cost of repeated calls | 5, 20 |
| Prompt chaining, task decomposition, intermediate representations, error propagation | 6, 12 |
| Combining prompting techniques; benefits, costs, and limits of prompting recipes | 2–6, 14, 15 |
| Structured output, JSON, JSON Schema, syntactic and semantic correctness | 7–11 |
| Pydantic models, types, descriptions, nested fields, schema generation, serialization | 8, 11 |
| Required versus nullable fields, defaults, unavailable information | 9 |
| Prompt-only formatting, JSON mode, constrained decoding, tool-call argument extraction | 7, 10, 11 |
| Provider support, schema restrictions, parsing, refusals, failure handling | 8, 9, 11 |
| Direct SDK versus LangChain, templates, runnables, composition, invoke/batch/stream | 11, 12, 19 |
| Checklist scoring: criteria, deterministic rules, computed properties, inspectable penalties | 13 |
| Reasoning models, reasoning tokens, effort levels and budgets, provider-specific controls | 14, 15 |
| Context windows, token budgeting, history growth, lost information in long contexts | 16, 17 |
| Trimming, summaries, recent history, repeated compaction, client/server compaction | 17 |
| Prompt caching, stable prefixes, cache expiry, cost and latency, compaction trade-offs | 18 |
| Multimodal input, typed message parts, image encoding, MIME types, provider limits | 19 |
| Document extraction, ambiguous fields, normalisation, field-wise voting, review thresholds | 8, 9, 19, 20 |
| Exercises: checklist scoring and repeated image-based extraction | 13, 19, 20 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Answers should explain design choices rather than reproduce the lecture's particular letters, scores, or code.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Evaluation datasets, scorers, LLM-as-a-Judge, statistical comparisons, evaluation frameworks | Validating Generative Software |
| Tool execution, agent loops, MCP, prompt-injection defences beyond prompt organisation | Tools and Agents |
| Retrieval pipelines, embeddings, vector stores, retrieval-based context selection | Retrieval-Augmented Generation |
| Packaged skills and their lifecycle | Agentic Skills |
| Durable workflows, orchestration, multi-agent systems, tracing | Workflows and Agent Orchestration |
| Broader model/deployment selection, privacy, regulation, organisational oversight | AI Governance 101 |

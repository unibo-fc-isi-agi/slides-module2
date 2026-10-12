+++
title = "LLM-as-a-Service — Questions"
[build]
render = "never"
list = "never"
+++

# LLM-as-a-Service — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of model names, prices, or API signatures.

## Models and deployment

1. **[notions; theoretical]** How does an application access an LLM as a service? Distinguish the model, inference runtime, service provider, Web API, and client library. What changes when inference runs locally?

2. **[know-how; practical]** How would you use a model zoo (catalogue) to find a model that your application can run or access? What can you learn from its name, variants, and model card, and what would you still need to verify?

3. **[notions; theoretical]** What is model quantization? Explain its purpose and trade-offs. Is choosing the smallest available representation always a good idea?

4. **[know-how; theoretical]** How would you estimate whether a model can run on a given machine? Explain why its download size or number of active parameters alone may be misleading, and how the length of a conversation affects the estimate.

5. **[know-how; practical]** How would you make a model available locally through Ollama and connect an application to it? If generation were unexpectedly slow, how would you investigate?

6. **[reasoning; practical]** What does an aggregator such as OpenRouter add to direct access to a provider? Distinguish routing among models from routing among providers, and discuss what changes when you supply your own provider credentials.

## Requests, responses, and portability

7. **[know-how; practical]** How would you configure an LLM client so that it can connect to different services without editing its source code? What precautions are needed when handling API keys?

8. **[know-how; theoretical]** How would you estimate and monitor the cost of a conversation with a hosted LLM? Why might the visible length of its answers be a poor estimate of the bill?

9. **[notions; theoretical]** How can a stateless API support a conversation? Explain the role of message history and message roles, and contrast this with an API that stores conversation state on the server.

10. **[know-how; practical]** How would you control the generation of an LLM response through request parameters? Discuss controls over sampling, repetition, and termination, and explain how you would check which controls a service supports.

11. **[reasoning; theoretical]** A request succeeds, but the returned text is empty or appears incomplete. Does this necessarily indicate a failure? What information besides the text would help you interpret the response?

12. **[reasoning; practical]** A service advertises an OpenAI-compatible API. Is changing the client's base URL, key, and model enough to migrate an application to it? Explain what compatibility does and does not guarantee.

13. **[notions; practical]** Compare two LLM APIs with different request and response structures. What concepts do they share, and what must an application translate between them?

14. **[know-how; theoretical]** How would you implement a command-line chat over a stateless completion API? Distinguish continuing a conversation, retrying a failed request, and asking for an alternative to a successful answer.

## Responsiveness and reliability

15. **[reasoning; theoretical]** What is the difference between asynchronous requests and streamed responses? Can either be used without the other, and what does each improve?

16. **[know-how; practical]** How would you consume a streamed LLM response in a client application? Explain how you would keep the display and conversation history consistent if the stream ended unexpectedly.

17. **[know-how; theoretical]** How would you design a persistent cache of LLM responses? What makes two requests equivalent for caching, and how could you avoid returning an answer from the wrong conversation or service?

18. **[reasoning; theoretical]** What are the benefits and limitations of caching when experimenting with LLMs? Discuss its effect on reproducibility, generating alternative answers, and observing changes to the model.

19. **[know-how; practical]** How would you decide whether to retry a failed API request? Give examples of failures that call for waiting and failures that call for changing the request or configuration.

20. **[reasoning; theoretical]** Why use bounded retries with exponential backoff and jitter? What could go wrong if both the application and its client library independently retry requests?

21. **[know-how; theoretical]** How would you test caching and retry behaviour without spending API credits or waiting through real delays? What cases would distinguish a correct implementation from one that only works on successful requests?

## Scope and coverage

| Topic | Questions |
|---|---|
| Service architecture, local versus hosted inference, Web APIs, native and third-party client libraries | 1, 5, 7, 12, 13 |
| Model zoos, cards, capabilities, licences, naming, base/instruct variants, snapshots | 2, 18 |
| Quantization, precision and quality, formats such as GGUF, runtime compatibility | 2–5 |
| Memory estimates, weights, KV cache, context length, total versus active MoE parameters | 4 |
| GPU/CPU execution, VRAM/unified memory, offloading, drivers, local runtime setup and inspection | 4, 5 |
| Aggregators, model/provider routing, latency versus throughput, BYOK | 6 |
| Client configuration, environment variables, command-line options, credentials, authentication | 7, 14, 19 |
| Input/output/reasoning token usage, growing history, costs, credits, budgets, rate limits | 8, 9, 11, 19 |
| Request–response interaction, role-tagged messages, multimodal content, client/server conversation state | 9, 13, 14 |
| Sampling controls, token limits, stop conditions, alternative completions | 10, 11, 14 |
| Response metadata, finish reasons, non-text content, reported model and usage | 8, 11, 13 |
| Partial API compatibility, provider migration, cloud-specific configuration, adapters | 7, 12, 13 |
| Chat Completions, Responses, Messages, and generateContent as alternative API structures | 9, 12, 13 |
| Synchronous CLI chat, history updates, failures, retry versus regeneration | 14 |
| Asynchronous execution, streaming, perceived latency, chunks/deltas, partial failures | 15, 16 |
| Persistent response caching, request identity, serialization, lookup, reproducibility | 17, 18, 21 |
| HTTP errors and SDK exceptions, transient failures, rate limits, Retry-After | 19, 20 |
| Bounded retries, exponential backoff, jitter, nested retry policies, configurable delays | 19–21 |
| Exercise design and verification: caching and retries | 17–21 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Questions about API differences concern concepts and their representation, not recall of every provider's field names.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Prompt design, structured-output schemas, reasoning strategies, context compaction, provider-side prompt caching | Prompt Engineering & Structured Outputs |
| Assessing the semantic quality of generated answers | Validating Generative Software |
| Implementing tool execution, agent control loops, and MCP | Tools and Agents |
| Embeddings and retrieval | Retrieval-Augmented Generation |
| Task-specific model evaluation, licensing analysis, deployment economics, privacy and regulatory trade-offs | AI Governance 101 |

+++
title = "Generative AI 101 — Questions"
[build]
render = "never"
list = "never"
+++

# Generative AI 101 — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of product names or features.

This introduction assesses foundational understanding and the overall role of generative AI in software. Topics previewed here but developed in later lectures are reserved for those lectures.

## Foundations

1. **[notions; theoretical]** What is generative AI? How are foundation models, large language models, and multimodal models related?

2. **[notions; theoretical]** How does an LLM generate text? What roles do tokens, context, and temperature play?

3. **[reasoning; theoretical]** How does the training of a foundation model affect what it can and cannot do? Why might it perform poorly on recent or uncommon information?

4. **[reasoning; theoretical]** If a chatbot remembers what you told it, has it learned something? Discuss the possible meanings of “learning” in this case.

5. **[reasoning; theoretical]** Why can an LLM produce a convincing but incorrect answer? Would making its output deterministic solve the problem?

6. **[reasoning; theoretical]** What are the benefits and limitations of combining language-based reasoning with symbolic computation? How does this relate to the distinction between intuitive and deliberate thinking?

## Generative AI and software

7. **[know-how; practical]** What kinds of interfaces to generative AI systems are available? Choose examples of existing applications and explain what tasks you would use them for.

8. **[reasoning; practical]** What is the difference between a language model and an application built around it? Using an application you know, discuss which capabilities require more than text generation.

9. **[reasoning; theoretical]** How can generative AI be used in software engineering? Distinguish its use in developing a product from its use within the product.

10. **[know-how; theoretical]** Give an example of a task for which generative AI is useful and another for which ordinary software is preferable. What makes the difference?

11. **[reasoning; theoretical]** Can an AI-text detector establish whether a student wrote an assignment? What would make its result convincing or unconvincing evidence?

12. **[notions; theoretical]** What activities does engineering a generative AI application involve? How does its lifecycle differ from that of ordinary software and of classic machine-learning projects?

## Scope and coverage

| Introductory topic | Questions |
|---|---|
| Generative AI, foundation models, LLMs, multimodality | 1 |
| Next-token prediction, tokens, sampling, context, temperature | 2, 5 |
| Training, generalisation, sampling bias, niche and recent knowledge | 3 |
| Training versus conversation context and stored memory | 4 |
| Natural-language reasoning, hallucinations, symbolic computation, dual-system analogy | 5, 6 |
| Interface types and their uses; model versus application | 7, 8 |
| Development-time and runtime uses of GenAI; hard-to-code tasks and unstructured data | 9, 10 |
| Limits of AI-generated text detection | 11 |
| Overall project lifecycle, optional training, iteration | 12 |

The following previews belong in the question banks of their dedicated lectures. They are not additional questions for this introduction.

| Deferred topic | Lecture |
|---|---|
| APIs, streaming, tokens as a cost measure, service limits, local runtimes | LLM-as-a-Service |
| Prompt templates and patterns, structured outputs, context management | Prompt Engineering & Structured Outputs |
| Evaluation methods, validation sets, deterministic scorers, LLM-as-a-Judge | Validating Generative Software |
| Agent anatomy, intelligence versus agency and autonomy, tools, MCP, permissions, prompt injection | Tools and Agents |
| Embeddings, vector stores, retrieval, grounding | Retrieval-Augmented Generation |
| Skills, project instructions, hooks, agent customisation | Agentic Skills |
| Workflow versus agent design, orchestration, tracing, end-to-end application design | Workflows and Agent Orchestration |
| Deployment trade-offs, model selection, privacy, regulation, human oversight | AI Governance 101 |

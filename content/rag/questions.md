+++
title = "Retrieval-Augmented Generation — Questions"
[build]
render = "never"
list = "never"
+++

# Retrieval-Augmented Generation — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used, without requiring memorisation of API signatures or product specifications.

## Memory and retrieval

1. **[notions; theoretical]** What kinds of memory can an LLM-based agent use? Distinguish knowledge in model weights from working, episodic, semantic, and procedural memory, and explain where retrieval fits.

2. **[notions; theoretical]** How does retrieval-augmented generation work? Distinguish preparing the knowledge base from answering a question, and explain which components need an LLM.

3. **[reasoning; theoretical]** When would you use RAG rather than put all the documents in the prompt, use a live-data tool, or fine-tune a model? What evidence would justify the added retrieval infrastructure?

4. **[notions; theoretical]** How do embeddings support semantic search? Compare cosine similarity, dot product, and Euclidean distance, including the role of vector normalisation.

5. **[reasoning; theoretical]** Does a high embedding similarity mean that a document answers a question correctly? Discuss paraphrases, negation, and the interpretation of scores across different models.

6. **[know-how; practical]** How would you connect an embedding model to a retrieval system? What would you check about document and query encoding, and what would need to change if you replaced the embedding model?

## Building the index

7. **[reasoning; theoretical]** What must a vector store store and support? Compare exact and approximate nearest-neighbour search, and explain whether exact search guarantees that the retrieved documents are relevant.

8. **[know-how; practical]** How would you implement vector search with SQLite, with and without a vector extension such as `sqlite-vec`? Explain what the extension changes and what limitations would remain as the corpus grows.

9. **[know-how; theoretical]** How would you choose a chunking strategy for a document collection? Discuss chunk size, overlap, document structure, and ways to preserve the context needed to understand each chunk.

10. **[know-how; practical]** How would you prepare a collection of PDFs for retrieval? Explain how you would detect problems caused by repeated page elements, tables, diagrams, or text-extraction errors before indexing them.

11. **[reasoning; theoretical]** What metadata should accompany a chunk, and why? Explain how filtering before or after nearest-neighbour search changes the results and the enforcement of access restrictions.

12. **[know-how; theoretical]** How would you keep a retrieval index consistent with a changing document collection? Address additions, revisions, deletions, and interrupted updates without rebuilding everything unnecessarily.

## Retrieving evidence and producing answers

13. **[reasoning; theoretical]** When do keyword search and semantic search fail in different ways? Explain how hybrid search combines them and why fusing ranks can be preferable to adding their raw scores.

14. **[know-how; theoretical]** A retriever returns several similar passages but misses the evidence needed to answer the question. How would you decide whether to change k, rerank, rewrite the query, or encourage more diverse results?

15. **[know-how; practical]** How would you build a RAG pipeline with LangChain? Explain the roles of documents, loaders, splitters, embeddings, vector stores, and retrievers, and what you would recheck when replacing a component.

16. **[reasoning; theoretical]** When is agentic RAG preferable to a fixed retrieval-and-generation pipeline? Discuss questions requiring several searches and the consequences of letting the model decide when and what to retrieve.

17. **[know-how; theoretical]** How would you make a document-based assistant cite its evidence and abstain when evidence is insufficient? Explain what can be checked about a citation mechanically and what requires checking its meaning.

## Evaluation and security

18. **[know-how; theoretical]** How would you construct a gold set and compare retrieval strategies? Explain what precision@k, recall@k, and MRR measure, and what aggregate scores might hide.

19. **[reasoning; theoretical]** How would you distinguish a retrieval failure from a generation failure? Can an answer be faithful to the retrieved material yet irrelevant, incomplete, or false?

20. **[know-how; theoretical]** How would you protect a shared RAG system against unauthorised disclosure and poisoned documents? Discuss where permissions must be enforced and whether storing embeddings instead of text removes privacy concerns.

21. **[reasoning; practical]** What additional responsibilities arise when an agent can write persistent memories as well as retrieve documents? Using a memory store or service as an example, explain how you would handle provenance, stale information, deletion, and malicious memories carried into later sessions.

## Scope and coverage

| Topic | Questions |
|---|---|
| Parametric memory, context as working memory, episodic/semantic/procedural memory, focus | 1 |
| RAG indexing, retrieval, prompt augmentation, generation | 2, 15 |
| RAG versus long context, prompting, tools and fine-tuning; adding complexity based on need | 3 |
| Embeddings, semantic search, cosine/dot product/L2, normalisation | 4 |
| Relative similarity scores, negation, relevance, model dependence, limits of visual projections | 4, 5 |
| Embedding APIs and local libraries, batching, dimensions, query/document prefixes, model compatibility | 6 |
| Vector-store records, CRUD, KNN, metadata filters, exact versus ANN search | 7, 11 |
| In-memory libraries, database extensions, dedicated stores; choosing suitable infrastructure | 3, 7, 8 |
| SQLite from scratch versus sqlite-vec, serialisation, SQL KNN, extension loading, performance and concurrency | 8 |
| Fixed, recursive, structural and semantic chunking; overlap; contextual enrichment | 9 |
| PDF ingestion, repeated headers, empty pages, lossy extraction, layout-aware and image-based alternatives | 10 |
| Source/page/section identifiers, citations, validity, ownership, pre/post-filtering | 11, 17, 20 |
| Incremental indexing, digests, verified downloads, transactions, corpus versions, deletion | 6, 12 |
| Lexical/BM25 versus dense search, hybrid search, reciprocal rank fusion | 13 |
| Top-k, reranking, query rewriting, sub-questions, hypothetical answers, diversity | 14 |
| LangChain abstractions, database adapters, retriever composition, store-specific capabilities | 15 |
| Retrieval as a tool, agent-generated queries, multi-hop questions, empty results, stopping limits | 16 |
| Labelled context, structured answers, abstention, citation IDs, URLs built from metadata | 17 |
| Gold questions and relevant chunks, human review of synthetic questions, version-pinned evidence | 18 |
| Precision@k, recall@k, MRR, per-case misses, regression comparisons | 18 |
| Separate retrieval/generation evaluation, faithfulness, answer relevance, contextual recall, LLM judges | 19 |
| Corpus poisoning, indirect injection, delimiters, retrieval-time access control, query/result logs | 20 |
| Embedding privacy, remote embedding/storage services, sensitive derived data | 6, 20 |
| Writable memory technologies, provenance, staleness, forgetting, cross-session memory poisoning | 21 |
| Exercise: maintained PDF corpus, filtered search, grounded answers, verifiable citations, evaluation | 10–12, 15, 17–20 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Evaluation questions apply the methods of the preceding validation lecture specifically to retrieval and grounded generation. Examples may use any suitable document collection.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Packaging and loading procedural knowledge as skills, skill lifecycle and testing | Agentic Skills |
| Durable workflow state, orchestration patterns, multi-agent systems | Workflows and Agent Orchestration |
| Broader technology-selection trade-offs, model licensing, deployment economics and regulation | AI Governance 101 |

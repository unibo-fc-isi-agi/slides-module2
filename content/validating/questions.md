+++
title = "Validating Generative Software — Questions"
[build]
render = "never"
list = "never"
+++

# Validating Generative Software — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify the technology used and explain how it supports the evaluation, without requiring memorisation of API signatures or built-in metric catalogues.

## Designing evaluations

1. **[notions; theoretical]** What makes generative software difficult to test? Describe the ingredients of an evaluation and explain how evaluations relate to ordinary unit tests.

2. **[know-how; theoretical]** How would you construct a representative test dataset for a document-processing application? Discuss how to establish expectations when the source is ambiguous, incomplete, or internally contradictory.

3. **[reasoning; theoretical]** How would you choose between deterministic checks, similarity metrics, an LLM judge, and human assessment? Give examples where a convenient metric would measure the wrong thing.

4. **[know-how; theoretical]** How would you check extracted facts without rejecting harmless differences in their representation? Explain when exact matching, normalisation, ranges, or set-based comparisons are appropriate, and how excessive tolerance could hide errors.

5. **[notions; theoretical]** What are invariants and relational or metamorphic tests? Give examples useful for generative software, and explain what they can establish when no single expected answer is available.

## Evaluating with LLM judges

6. **[know-how; theoretical]** How would you design an LLM judge for a quality criterion that is difficult to check with code? Explain what evidence it needs and how its rubric and output should be structured.

7. **[reasoning; theoretical]** What changes when a judge grades one answer rather than compares two, or judges with rather than without a reference answer? Discuss how these choices affect the conclusions you can draw.

8. **[know-how; theoretical]** How would you detect and reduce position bias, verbosity bias, and self-preference in an LLM judge? Would using a stronger model or requesting a rationale be enough to trust its verdicts?

9. **[reasoning; theoretical]** How would you validate an LLM judge against human assessments? Explain why raw agreement can be misleading and what a chance-corrected measure such as Cohen's kappa adds.

## Interpreting evidence

10. **[reasoning; theoretical]** An application passes every case in a small test dataset. What can you conclude about its reliability? Discuss uncertainty and the difference between testing more inputs and repeating the same inputs more times.

11. **[know-how; theoretical]** How would you compare two versions of a generative application fairly? Explain why paired results on individual cases can tell you more than comparing two average scores.

12. **[reasoning; theoretical]** What is the difference between accuracy and consistency? How would you establish whether majority voting improves a document extractor rather than merely making it more consistent?

13. **[reasoning; theoretical]** When is caching generated outputs useful during evaluation, and when does it invalidate what you are trying to measure? Distinguish reusing a sample across several checks from treating repeated cache hits as independent runs.

## Evaluation in a software project

14. **[reasoning; practical]** Compare the test-oriented approach of DeepEval with the experiment-tracking approach of MLflow. What concepts do they share, and when might you use either or both in a project?

15. **[know-how; practical]** How would you build an evaluation suite for an application that extracts facts and writes explanations? Using DeepEval or MLflow, describe how you would connect the dataset, system under test, scorers, and report so that failures can be investigated.

16. **[know-how; theoretical]** When an evaluation fails, how would you decide whether the application, the expectation, or the scorer is wrong? How would you check that a suite which always passes can actually detect defects?

17. **[know-how; practical]** How would you use evaluations to detect regressions in CI? Discuss intermittent failures, acceptance thresholds, API costs and credentials, and the information needed to compare runs over time.

## Scope and coverage

| Topic | Questions |
|---|---|
| Non-determinism, open-ended answers, changing prompts/models/providers, evaluations versus unit tests | 1, 10, 11, 17 |
| Dataset, system under test, scorers, aggregation, regression testing | 1, 2, 11, 15, 17 |
| Human-authored expectations, representative inputs, missing information, ambiguity, conflicting source evidence | 2, 4, 16 |
| Deterministic checks, statistical/text-similarity metrics, LLM judges, human assessment | 3 |
| Structured fields, exact/tolerant matching, nulls, normalisation, admissible alternatives, lists and ordering | 4, 15 |
| Invariants, ranges, cross-input relations, metamorphic testing | 4, 5 |
| Judge rubrics, narrow criteria, structured verdicts and rationales, G-Eval | 6, 8, 15 |
| Pointwise/pairwise judging, reference-based/reference-free judging, groundedness | 6, 7 |
| Position, verbosity, and self-preference biases; judge model and temperature | 8 |
| Validating the judge, human agreement, chance agreement, Cohen's kappa | 9 |
| Pass-rate estimates, confidence intervals, small datasets, repeated sampling | 10, 11 |
| Fair comparisons, changing one factor, paired differences, McNemar's test | 11 |
| Accuracy versus consistency, field-wise agreement, single queries versus voting | 12 |
| Shared samples within a run, response caching, variance, evaluation cost | 13, 17 |
| Evaluation framework landscape, tests versus experiments, local/cloud reports | 14 |
| DeepEval: pytest parametrisation, assertions, test cases, G-Eval criteria and thresholds | 14, 15 |
| MLflow: inputs/expectations, prediction function, code scorers, judges, runs, traces, metrics | 14, 15, 17 |
| Checking every field, diagnosing failures, grouping checks versus diagnostic detail | 4, 15, 16 |
| Image-based extraction, exact facts, invariants, voting accuracy, validated legibility judge | 2–6, 9, 12, 15 |
| Deliberately incorrect expectations or outputs, checking the test suite itself | 16 |
| Flaky tests, rate-based assertions, CI, secrets, cost and reproducibility | 10, 13, 17 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Statistical questions concern interpreting evidence and choosing suitable comparisons, rather than memorising formulas. Application examples can be chosen independently of the lecture's letters and identity documents.

The following topics are reserved for their dedicated lectures:

| Deferred topic | Lecture |
|---|---|
| Agent trajectories, tool-call correctness, agentic benchmarks | Tools and Agents |
| Retrieval metrics and evaluation of RAG pipelines | Retrieval-Augmented Generation |
| Skill triggering and outcome tests | Agentic Skills |
| Workflow paths, multi-agent behaviour, end-to-end orchestration tests | Workflows and Agent Orchestration |
| Public benchmarks, broader model selection, deployment and governance decisions | AI Governance 101 |

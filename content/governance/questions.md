+++
title = "AI Governance 101 — Questions"
[build]
render = "never"
list = "never"
+++

# AI Governance 101 — Questions

Answer in your own words, motivating your conclusions and using examples where useful. Questions asking whether something is possible or desirable require more than a yes/no answer. Implementation questions can be answered with an explanation or pseudocode unless executable code is explicitly requested.

Labels identify the primary learning target: **notions** (knowledge), **reasoning** (drawing conclusions), or **know-how** (applying knowledge). **Theoretical** questions are independent of particular technologies; **practical** questions concern their use. Practical answers should identify relevant rules, licenses, or technologies and check their current terms; memorising dates, prices, model rankings, or article numbers is not the goal.

## Making and documenting choices

1. **[notions; theoretical]** What is AI governance in an organisation, and which decisions belong to it? Explain why choosing an architecture or model can be a governance decision even before a legal question arises.

2. **[reasoning; theoretical]** How would you compare two plausible designs when one offers better quality and faster delivery, while the other offers more control and easier compliance? Explain how quality, cost, control, compliance, and time-to-market can conflict, and what evidence would justify your choice.

3. **[know-how; practical]** A university wants to process applicants' documents with an LLM. How would you compare a proprietary API, a third-party host of an open model, and an on-premise deployment? Identify who handles the data and operations in each case, and when a hybrid arrangement would help.

4. **[reasoning; practical]** How would you estimate whether paying per request or running your own model is cheaper for a particular workload? State the assumptions you would need, including volume, token use, hardware utilisation, labour, and maintenance, and explain why the cheapest option may still be unsuitable.

## Rules and responsibilities

5. **[notions; practical]** Which different questions are answered by data-protection law, AI-specific regulation, national law, institutional policy, provider contracts, and model licenses? Explain why satisfying one layer does not settle the others.

6. **[know-how; practical]** Before sending identifiable application documents to an external LLM provider, what would you investigate and document? Discuss purpose and minimisation, the controller–processor relationship, retention and logs, international transfers, impact assessment, and the possibility of significant automated decisions.

7. **[reasoning; practical]** Why can the same model be used in one minimal-risk application and in another application subject to high-risk obligations? Apply this distinction to a system that scores applicants, and explain what changes if its output merely informs a committee rather than automatically rejecting people.

8. **[know-how; practical]** An organisation builds an admission assistant on top of a third-party general-purpose model. How would you identify the model provider, the system provider, the deployer, and affected people? What kinds of duties would you examine for each role, including human oversight, documentation, monitoring, and transparency?

9. **[reasoning; practical]** An AI system seems permissible under a general EU rule, but a national rule or the organisation's policy imposes tighter conditions. How should engineers handle this during design and procurement, and who should help resolve uncertain interpretations?

## Openness, licensing, and sovereignty

10. **[notions; theoretical]** In what different senses can an AI model be called “open”? Explain what weights, code, training recipe, data or data information, documentation, and licenses each let a user inspect or do, and why downloadable weights alone do not establish reproducibility.

11. **[reasoning; practical]** A model is advertised as “open source.” How would you examine that claim for both practical reuse and auditability? Explain why a normative definition of open-source AI and a regulatory exemption for open general-purpose models may set different thresholds.

12. **[know-how; practical]** A team plans to fine-tune, merge, or distil an open-weights model and sell access to the result. What exactly would you check before proceeding? Include the checkpoint and license version, upstream models, training data, outputs, downstream distribution, and the team's possible regulatory role.

13. **[reasoning; theoretical]** What might an organisation mean by “sovereign AI”? Distinguish where a model was developed, where it runs, and how much of its construction can be audited. How would you assess a local-language or nationally developed model without assuming its origin makes it better, more open, or more suitable for production?

## Choosing techniques and models

14. **[know-how; theoretical]** A system fails because it lacks current facts, must perform actions, follows a repeatable procedure, and sometimes produces the wrong style. Which of prompting, RAG, tools or agents, skills, workflows, and fine-tuning might address each problem? Explain how you would add complexity only where evidence warrants it.

15. **[know-how; practical]** How would you form a shortlist of models for a real application? Separate hard constraints from qualities you would rank, and explain what model cards, system cards, dataset documentation, provider terms, and your own tests can and cannot establish.

16. **[reasoning; theoretical]** Why might a model that leads a public benchmark or leaderboard perform poorly in your application? Discuss benchmark saturation, contamination, changing test conditions, task mismatch, and the difference between a reported capability and a dependable workflow outcome.

17. **[know-how; practical]** How would you compare several models for scoring applicants' letters? Design a small evaluation that considers a human reference, repeated runs, disagreement, invalid outputs, latency, and cost, and explain how you would choose a model and know when to revisit the choice.

## Human responsibility and oversight

18. **[reasoning; theoretical]** What does it mean to adapt a process or its users to an AI system? Contrast an explicit, contestable change to an admission procedure with a silent change that favours what the model handles well. Who should be able to notice and challenge such adaptations?

19. **[reasoning; theoretical]** Why can placing a human “in the loop” fail to provide meaningful oversight? Explain the responsibility gap, automation bias, artificial salience, and false certainty, and how a nominal approver can end up bearing blame without real control.

20. **[know-how; practical]** Design the committee's review of AI-extracted facts and suggested scores so that members can exercise independent judgement. Explain what evidence they see, when they see the AI's ranking, how uncertainty and overrides are handled, and how you would detect rubber-stamping over time.

21. **[know-how; practical]** What would you put in a governance decision record before deploying an admission assistant? Explain how a colleague could reconstruct the regulatory classification, alternatives, deployment and model choice, evaluation evidence, human responsibilities, monitoring plan, and conditions that trigger reconsideration.

## Scope and coverage

| Topic | Questions |
|---|---|
| Governance as explicit engineering choices; five trade-off dimensions; decision record | 1–2, 21 |
| Cloud, hosted open models, on-premise and hybrid deployment; cost and data flows | 3–4 |
| GDPR, AI Act, national rules, institutional policies, contracts and their interaction | 5–9 |
| Personal data, provider arrangements, transfers, retention, impact and automated decisions | 6 |
| Use-based AI Act risk, system and model roles, oversight and transparency duties | 7–8 |
| Components and degrees of openness; open-source definitions and regulatory exemptions | 10–11 |
| Exact-checkpoint licensing, derivatives, data and distribution | 12 |
| Sovereignty, European and Italian model initiatives, capability evidence and maintenance | 13 |
| Agentic technique selection and its trade-offs | 14 |
| Model documentation, constraints, benchmarks and task-specific comparison | 15–17 |
| Enveloping, accountability, biases and meaningful human oversight | 18–20 |
| Comparing models and writing a governance decision record (lecture exercises) | 17, 21 |

The coverage guide identifies areas to consider when studying; it is not a required answer outline. Current prices, provider offerings, legal deadlines, model releases, benchmark scores, and initiative names are examples to verify when applying the ideas, not facts to recite from the slides.

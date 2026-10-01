+++

title = "[AgI] AI Governance 101"
description = "Trade-offs, regulation, and technology selection for LLM-based software"
outputs = ["Reveal"]

+++

# AI Governance 101

{{% import path="reusable/footer.md" %}}

---

## Outline

1. What is _AI governance_, and why should engineers care?
2. _Where_ should the model run? (cloud vs. on-premise)
3. _Regulation_: GDPR, EU AI Act, national law, UniBo policy
4. _Open_ models, licensing, and "sovereignty"
5. _Which technique_? Prompting vs. RAG vs. fine-tuning vs. agents
6. _Which model_? Selection, documentation, and evaluation
7. Exercises

---

{{% section %}}

{{< slide id="governance-concept" >}}

## What is _AI governance_?

- __AI governance__ = the set of _decisions_, _policies_, and _controls_ determining
    + _which_ AI systems (models, providers, techniques) an organization uses,
    + _how_ and _where_ they are deployed,
    + _who_ is accountable for their outputs, and
    + how they are _monitored_ over time
- It is __not__ (only) a legal matter: most governance decisions are _engineering_ decisions, taken (often implicitly) while designing the system
    + e.g. choosing a provider, a model, a deployment option, or whether a human reviews the outputs
- Making these decisions _explicit_, _motivated_, and _documented_ is what distinguishes governance from improvisation

---

## The five dimensions of the trade-off

Every choice about an AI-powered system implies a trade-off among:

1. __Quality__: how _good_ (accurate, reliable, consistent) are the outputs for the task at hand?
2. __Cost__: how much do _development_, _operation_ (per request, per month), and _maintenance_ cost?
3. __Control__: how much can we _inspect_, _customize_, _reproduce_, and _keep running_ the system, regardless of third parties?
4. __Compliance__: does the system respect _laws_ (e.g. GDPR, AI Act), _contracts_, and _internal policies_?
5. __Time-to-market__: how quickly can we _ship_ (and _change_) the system?

{{< image src="./tradeoff-radar.svg" max-h="45vh" alt="Radar chart comparing a frontier cloud API and a small open model on-premise on quality, cost, control, compliance and time-to-market: neither dominates" >}}

{{% fragment %}}
> There is __no__ option dominating all the others: governance is about choosing the _right compromise_ for the _use case_ at hand, and __writing down why__
{{% /fragment %}}

---

## Running example: a governance perspective

Recall the [running example](../prompting/#/running-example) (PhD admission committee assistant):

- __Data__: passports, transcripts, and presentation letters of the candidates
    + these are _personal data_ (even _identity documents_!)
- __Task__: extract information, summarize, and _score_ candidates
    + outputs contribute to decisions affecting people's _access to education_
- __Stakeholders__: candidates, committee members, the university (as the responsible organization), the AI provider(s)

{{% fragment %}}
### Governance questions (to be answered throughout this lecture)

- Can we send these documents to a cloud provider? Under which conditions?
- Is this system subject to specific regulations? Which obligations follow?
- Should the committee blindly trust the scores? Who is accountable for them?
- Which model, technique, and deployment option are appropriate? How do we _justify_ the choice?
{{% /fragment %}}

{{% /section %}}

---

{{% section %}}

{{< slide id="deployment-options" >}}

## Where should the model run? The general concept

Three main __deployment options__, differing in _who_ runs the model, and _where_ data goes:

1. __Proprietary cloud API__: the model is owned _and_ run by its provider (e.g. OpenAI, Anthropic, Google)
    + you only get an _API_; data is processed on the provider's infrastructure
2. __Open model, hosted by a third party__: an open-weights model run by a cloud provider or aggregator (e.g. via Open Router, Hugging Face Inference Endpoints, cloud GPU rental)
    + same model could be moved elsewhere; data still leaves your premises
3. __On-premise__ (a.k.a. _self-hosted_, _local_): an open-weights model run on _your own_ hardware (e.g. via Ollama, vLLM)
    + data never leaves your premises; you are responsible for hardware, operation, and updates

(cf. [on-premise vs. on-cloud](../llmaas/) in the LLM-as-a-Service lecture)

---

## Where should the model run? An intuitive example

{{< image src="./deployment-options.svg" max-h="70vh" alt="The same admission pipeline under three deployment options (proprietary cloud API, hosted open model, on-premise): whether the candidates' documents leave the university boundary, who pays for what, and who can see the data" >}}

---

## Deployment options: comparison

| | Proprietary cloud API | Hosted open model | On-premise |
|---|---|---|---|
| __Quality__ | highest (frontier models) | good (best open models lag the frontier) | limited by the hardware (smaller models) |
| __Cost structure__ | pay per token, no fixed costs | pay per token or per GPU-hour | hardware purchase + energy + staff; ~zero marginal cost |
| __Scalability__ | virtually unlimited (within rate limits) | high | bounded by owned hardware |
| __Control__ | low: models may change or be retired; no access to weights | medium: model is portable, provider is replaceable | full: versions pinned, runs offline |
| __Privacy__ | data processed by provider (contracts, retention, jurisdiction matter) | same concerns, possibly with an EU provider | data stays in-house |
| __Lock-in__ | high (proprietary features, prices) | low | low (but lock-in on hardware skills) |
| __Time-to-market__ | minutes | hours | days to weeks (procurement, setup) |

- _Hybrid_ solutions are common: e.g. _on-premise_ for sensitive data, _cloud_ for the rest; or a _gateway_ routing requests according to data sensitivity

---

## Deployment options: a worked cost example

Let's estimate the yearly cost of the running example, under explicit (and rough) __assumptions__:
- 500 applications per year; each one = passport picture + transcript + letter ≈ 6k input tokens, plus ~1k tokens of prompts
- 5 requests per application (extraction, validation, scoring, ...) $\implies$ ~35k _input_ + ~5k _output_ tokens per application
- hence, per year: __17.5M input__ + __2.5M output__ tokens

| Option | Price (USD per 1M input / output tokens) | Yearly cost |
|---|---|---|
| frontier proprietary model (e.g. [Claude Opus 5.5](https://platform.claude.com/docs/en/about-claude/pricing)) | $4 / $20 | 17.5 × 4 + 2.5 × 20 ≈ __$120__ |
| small proprietary model (e.g. [Claude Haiku 4.5](https://platform.claude.com/docs/en/about-claude/pricing)) | $1 / $5 | ≈ __$30__ |
| hosted open model (e.g. [`openai/gpt-oss-120b` on Open Router](https://openrouter.ai/openai/gpt-oss-120b)) | $0.04 / $0.17 | ≈ __$1__ |
| rented GPU, on demand (e.g. 24 GB GPU on [RunPod](https://www.runpod.io/pricing)) | ~$0.35–0.75 per hour | a few hours per year ≈ __$5__ (+ setup effort) |
| on-premise (a 24 GB GPU workstation) | ~€2–2.5k for the GPU alone | __€2.5k+__ upfront, + energy, + maintenance |

(prices as of September 2026: they change every few months, always re-check them)

{{% fragment %}}
> At _this_ scale, __cost is not the deciding factor__: compliance and control are. Things change at scale: e.g. one 80 GB GPU rented 24/7 costs ~$2k/month, which buys ~100M _output_ tokens of a frontier model per month. The __break-even__ depends on _volume_, _utilization_, and _model size_
{{% /fragment %}}

{{% /section %}}

---

# Regulatory framework

---

{{% section %}}

{{< slide id="regulation" >}}

## Regulation: the general picture

AI-powered software is subject to (at least) four _layers_ of rules, each with a different _object_:

1. the __GDPR__ ([Reg. (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)) regulates the processing of __personal data__, whatever the technology
2. the __EU AI Act__ ([Reg. (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)) regulates __AI systems__ (by _risk_ of their _use_) and __general-purpose AI models__
3. __national laws__, e.g. the Italian AI law ([Legge 132/2025](https://www.gazzettaufficiale.it/eli/id/2025/09/25/25G00143/sg))
4. __institutional policies__, e.g. the [UniBo GenAI policy](https://www.unibo.it/it/ateneo/statuto-norme-strategie-bilanci/intelligenza-artificiale)

plus _contracts_ (e.g. providers' terms of service, data processing agreements) and _licenses_ (of models, and of data)

{{< image src="./regulation-layers.svg" max-h="45vh" alt="Nested layers of rules around an LLM-powered application (licenses and terms of service, UniBo policy, Italian Law 132/2025, EU AI Act, GDPR), each paired with the question it answers" >}}

> Disclaimer: this is an _engineer's_ overview, __not__ legal advice: in real projects, involve your organization's _legal office_ and _Data Protection Officer_ (DPO)

---

## GDPR for LLM-powered applications: key concepts

- __Personal data__ = any information about an identified or identifiable person (e.g. names, passports, grades, _letters about someone_)
- __Controller__ (who decides _why_ and _how_ data is processed: e.g. the University) vs. __processor__ (who processes data _on behalf_ of the controller: e.g. the LLM provider)
    + a __Data Processing Agreement__ (DPA, [Art. 28](https://gdpr-info.eu/art-28-gdpr/)) with the provider is _mandatory_
- __Principles__ ([Art. 5](https://gdpr-info.eu/art-5-gdpr/)): lawfulness, purpose limitation, __data minimisation__ (send the LLM only what it needs!), accuracy, storage limitation, security
    + _privacy by design and by default_ ([Art. 25](https://gdpr-info.eu/art-25-gdpr/)): e.g. strip or pseudonymize personal data before sending prompts
- __International transfers__ ([Chapter V](https://gdpr-info.eu/chapter-5/)): data leaving the EU need an _adequacy decision_ (e.g. the [EU–US Data Privacy Framework](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en), upheld by the General Court in 2025, appeal pending) or other safeguards (e.g. standard contractual clauses)
- __Data Protection Impact Assessment__ (DPIA, [Art. 35](https://gdpr-info.eu/art-35-gdpr/)): required for high-risk processing, e.g. new technologies used to _evaluate_ or _score_ people
- __Automated decisions__ ([Art. 22](https://gdpr-info.eu/art-22-gdpr/)): people have the right __not__ to be subject to decisions based _solely_ on automated processing, with legal or similarly significant effects
    + e.g. an admission _rejection_ decided by an LLM alone
- About the __models__ themselves: [EDPB Opinion 28/2024](https://www.edpb.europa.eu/documents/opinion-of-the-board-art-64/opinion-282024-on-certain-data-protection-aspects-related-to_en) states that a model trained on personal data is _anonymous_ only if extracting those data is very unlikely, and that an _unlawfully_ developed model may taint its later use

---

## GDPR in practice: providers and enforcement

### What providers offer (as of September 2026)

| Provider | EU data residency | Zero data retention (ZDR) |
|---|---|---|
| [OpenAI](https://help.openai.com/en/articles/10503543-data-residency-for-the-openai-api) | yes (new projects, EU regional endpoints, surcharge) | for eligible customers, upon agreement |
| [Anthropic](https://platform.claude.com/docs/en/manage-claude/data-residency) | not on the first-party API; yes via cloud partners (AWS Bedrock, Google Vertex) | upon agreement |
| [Google Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency) | yes (EU multi-region) | yes, disabling default caching |
| [Microsoft Azure](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) | yes ("Data Zone EU" deployments) | upon request (modified abuse monitoring) |
| [Mistral](https://docs.mistral.ai/inference/regional-inference) | yes (EU or US regional inference) | upon request (default: 30 days retention for abuse monitoring) |

- _Free tiers_ and _consumer_ apps often allow providers to use your data for _training_: never send personal data there

### The Italian Data Protection Authority (Garante) at work

- [March 2023](https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9870847): ChatGPT temporarily _blocked_ in Italy (lawful basis, transparency, age verification), then reopened under [conditions](https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9874751)
- [December 2024](https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10085432): €15M fine to OpenAI, later _annulled_ by the Court of Rome (March 2026) since the competent authority was the Irish one (_one-stop-shop_ mechanism)
- [January 2025](https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10098477): urgent _limitation_ of processing for DeepSeek

---

## EU AI Act: a risk-based approach

{{% multicol %}}
{{% col %}}

- __Unacceptable risk__ $\rightarrow$ _prohibited_ ([Art. 5](https://artificialintelligenceact.eu/article/5/))
    + e.g. social scoring, manipulative techniques, __emotion recognition__ in workplaces and __education__, untargeted scraping of facial images
- __High risk__ $\rightarrow$ strict _obligations_ ([Art. 6](https://artificialintelligenceact.eu/article/6/) and [Annex III](https://artificialintelligenceact.eu/annex/3/))
    + e.g. CV screening, credit scoring, and __education__: systems to _determine access or admission_ to educational institutions (Annex III, point 3(a)), to _evaluate learning outcomes_ (3(b)), or to _proctor_ exams (3(d))
- __Transparency risk__ $\rightarrow$ _disclosure_ obligations ([Art. 50](https://artificialintelligenceact.eu/article/50/))
    + e.g. chatbots must disclose they are AI; synthetic content must be _marked_; deepfakes must be _labelled_
- __Minimal risk__ $\rightarrow$ no specific obligations
    + e.g. spam filters, AI in video games
- Orthogonally: __general-purpose AI (GPAI) models__, with obligations for their _providers_ ([Art. 53](https://artificialintelligenceact.eu/article/53/), [Art. 55](https://artificialintelligenceact.eu/article/55/))

{{% /col %}}
{{% col %}}

{{< image src="./todo-ai-act-pyramid.png" max-h="60vh" alt="TODO picture: the classic AI Act risk pyramid with four levels (top to bottom): 'Unacceptable — prohibited' (red), 'High — conformity & obligations' (orange), 'Transparency — disclosure' (yellow), 'Minimal — no obligations' (green), with 2 example icons per level. A pin labelled 'our PhD admission assistant (Annex III, 3(a))' placed on the high-risk level. A separate side box labelled 'GPAI models (e.g. GPT, Claude, Gemini, Llama)' with an arrow 'used inside' pointing to the systems in the pyramid." >}}

{{% /col %}}
{{% /multicol %}}

{{% fragment %}}
> Our __running example is high-risk__: it contributes to deciding _admission_ to a PhD programme. The same LLM, used to summarize news, would be _minimal_ risk: the Act regulates the __use__, not the technology
{{% /fragment %}}

---

## EU AI Act: who must do what?

| Role | Who is it? | Main obligations (for high-risk systems) |
|---|---|---|
| __Provider__ | who _develops_ the system and puts it on the market / into service under its name | risk management (Art. 9), data governance (Art. 10), technical documentation (Art. 11), automatic __logging__ (Art. 12), instructions for use (Art. 13), __human oversight by design__ (Art. 14), accuracy & robustness (Art. 15), quality management, conformity assessment, registration, post-market monitoring |
| __Deployer__ | who _uses_ the system under its authority | use it as instructed; assign __human oversight__ to competent, trained people; ensure input data are relevant; __monitor__ it; keep __logs__ for ≥ 6 months; __inform__ affected people (Art. 26); public bodies: __fundamental rights impact assessment__ (Art. 27) |
| __Affected person__ | e.g. the candidate | right to an __explanation__ of decisions based on high-risk AI output (Art. 86) |

- Beware: a deployer __becomes a provider__ if it _substantially modifies_ a system, or puts its _own name_ on it (Art. 25)
    + e.g. a University building its own admission assistant on top of an LLM API is the _provider_ __and__ the _deployer_ of that system
- __GPAI model providers__ (e.g. OpenAI, Mistral) must provide technical documentation to downstream providers, a _copyright policy_, and a public _summary of training data_ (Art. 53); models with _systemic risk_ (> 10<sup>25</sup> FLOPs of training) also need evaluations, adversarial testing, incident reporting (Art. 55)
    + _open-source_ GPAI models are exempted from the documentation duties only, and only if they do not pose systemic risk (Art. 53(2), details [later](#/open-models-ai-act))
    + a voluntary [GPAI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai) (July 2025) details how to comply

---

## EU AI Act: timeline, literacy, penalties

### Timeline (as amended by the _Digital Omnibus on AI_, [Reg. (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng))

| Date | What applies |
|---|---|
| 1 Aug 2024 | entry into force |
| 2 Feb 2025 | prohibitions (Art. 5), AI literacy (Art. 4) |
| 2 Aug 2025 | GPAI model obligations, governance structures |
| 2 Aug 2026 | general application, including transparency (Art. 50; until 2 Dec 2026 for systems already on the market) |
| __2 Dec 2027__ | high-risk systems of _Annex III_ (e.g. education), postponed from 2 Aug 2026 |
| 2 Aug 2028 | high-risk systems of _Annex I_ (safety components of regulated products), postponed from 2 Aug 2027 |

### Other relevant points

- __AI literacy__ (Art. 4): providers and deployers must support the AI literacy of their _staff_ (this course is part of it!)
- __Penalties__ (Art. 99): up to €35M or 7% of worldwide turnover for prohibited practices; up to €15M or 3% for most other violations
- __Transparency__: a [Code of Practice on AI-generated content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) details marking and labelling

---

## National law and institutional policies

### Italy: [Legge 23 settembre 2025, n. 132](https://www.gazzettaufficiale.it/eli/id/2025/09/25/25G00143/sg) (in force since 10 Oct 2025)

- complements the AI Act: [AgID](https://www.agid.gov.it/) and [ACN](https://www.acn.gov.it/) are the national _AI authorities_ (Art. 20)
- _public administration_: AI is only _instrumental_, the human official remains solely _responsible_ for decisions (Art. 14)
- _intellectual professions_: AI only for _supporting_ activities, and clients must be _informed_ (Art. 13)
- _minors_: under 14s need parental consent to use AI (Art. 4)
- _copyright_: only _human_ works are protected (AI-assisted ones are, if they result from the author's intellectual effort); rules on text and data mining (Art. 25)
- new _crime_: unlawful dissemination of AI-generated _deepfakes_ (Art. 26)

### University of Bologna: [GenAI policy for teaching and research](https://www.unibo.it/it/allegati/policy-per-un-uso-etico-e-responsabile-dell2019intelligenza-artificiale-generativa-nelle-attivita-di-didattica-e-ricerca/@@download/file/Policy-Generative-AI.pdf)

- GenAI use is _allowed_: principles of human centrality, transparency, accountability, accuracy, respect for rights
- __substantial__ uses (e.g. AI-written papers, theses, or assessed work) must be __declared__; GenAI cannot be an _author_
- __no substantial use__ where it _affects others_: e.g. _peer review_, _evaluating_ research projects, __grading students__
- __no personal data__ of third parties, confidential or unpublished material in online GenAI tools, without a legal basis and guarantees
- a separate [policy for administrative staff](https://www.unibo.it/it/allegati/PolicyUsoAI_Amministrazione.pdf) exists

{{% fragment %}}
> For the running example: scores must remain _suggestions_ to the committee, candidates' data must not go to consumer chatbots, and the University is accountable for the whole process
{{% /fragment %}}

{{% /section %}}

---

# Open models, licensing, and "sovereignty"

---

{{% section %}}

{{< slide id="open-models" >}}

## What makes a model _"open"_? The general concept

A model release is a __bundle__ of separately _openable_ artifacts: downloading one of them (usually the weights) says little about the others

| Component | What a useful release contains | What it enables |
|---|---|---|
| __Weights__ | final parameters (ideally also intermediate checkpoints) | local inference, fine-tuning, independent hosting |
| __Inference code__ | architecture, tokenizer, generation code, configuration | actually _running_ the weights |
| __Training code & recipe__ | data processing, hyper-parameters, training and post-training (SFT, RL) pipelines | understanding _how_ the weights arose; re-training |
| __Training data__ | the actual training mixture, in training-ready form | data auditing, contamination analysis, exact reproduction |
| __Data information__ | provenance, sources, filtering and selection processes | a (weaker) substitute when data cannot be redistributed |
| __Documentation__ | model card, technical report, evaluations, limitations | auditability, downstream risk assessment |
| __Licenses__ | _separate_ licenses for weights, code, and data | knowing what you may _legally_ do with all the above |

---

## Openness is _graded_, not binary

{{< image src="./openness-bar.svg" max-h="30vh" alt="Openness of seven release components for a closed API model, an open-weights model (Llama 4) and a fully open model (OLMo 3): downloadable weights do not make a model open" >}}

| Framework | Question it answers |
|---|---|
| [Liesenfeld & Dingemanse, FAccT 2024](https://doi.org/10.1145/3630106.3659005) | how open is a release _in practice_? (14 dimensions, 40 text LLMs + 6 text-to-image models) |
| [European Open Source AI Index](https://osai-index.eu/database/) | which open-science artifacts were actually released? (graded score; top ranks in July 2026: YuLan-Mini, BLOOMZ, OLMo 3, Apertus) |
| [Stanford Foundation Model Transparency Index](https://crfm.stanford.edu/fmti/December-2025/index.html) (Dec. 2025) | how _transparent_ are providers? (mean score 41/100, down 17 from 2024; IBM 95, DeepSeek 32, Alibaba 26: open weights $\neq$ transparency) |
| [OSI Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition) | does a system meet a _normative_ definition of "open source AI"? (next slide) |

- __Open-washing__: presenting a model as "open" or "open source" based on _one_ disclosed component (typically the weights), while the artifacts or legal freedoms needed to study, reproduce, modify, or freely use it are missing
    + e.g. _Llama 4_ (downloadable weights, restrictive license), _Gemma 3_ (custom terms with use restrictions), _Mistral 3_ (called ["open-source"](https://mistral.ai/news/mistral-3/) by its vendor: Apache 2.0 weights, undisclosed training data)
    + by contrast, OpenAI calls [gpt-oss](https://openai.com/index/introducing-gpt-oss/) "_open-weight_": the more accurate term

---

## The OSI Open Source AI Definition (OSAID 1.0, Oct. 2024)

- Users must be able, _without asking permission_, to:
    1. __use__ the system for _any_ purpose
    2. __study__ how it works
    3. __modify__ it for any purpose
    4. __share__ it, with or without modifications
- This requires the _preferred form for making modifications_:
    + __data information__: enough detail on training data for a skilled person to build a _substantially equivalent_ system
    + __code__: the _complete_ training and inference pipeline
    + __parameters__: weights and configuration, under open terms
- __Controversy__: OSAID does __not__ require releasing the training data itself (cf. [OSI's FAQ](https://opensource.org/ai/faq))
    + OSI: data may be personal, copyrighted, or confidential, so requiring it would exclude too many systems
    + critics: without the data, exact reproduction and data-level auditing are impossible
- OSI's [initial validation](https://opensource.org/ai/final-board-report) found that _Pythia_, _OLMo_, _Amber_, _CrystalCoder_, and _T5_ passed, while _Llama 2_, _Grok_, _Phi-2_, and _Mixtral_ did not
    + a _snapshot_ of 2024, __not__ a certification registry for later versions

---

## The licensing landscape (as of September 2026)

| Category | Examples | What is open | Main limitation |
|---|---|---|---|
| __Closed__ (API-only) | GPT, Claude, Gemini, Mistral's "Premier" models | API + documentation | no weights; usage governed by _terms of service_ |
| __Open weights, restrictive license__ | [Llama 4](https://www.llama.com/llama4/license/), [Gemma 3](https://ai.google.dev/gemma/terms), [Teuken v0.6](https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6), BLOOM ([RAIL](https://huggingface.co/bigscience/bloom-560m/blob/main/LICENSE)) | weights, inference code | use-based, geographic, commercial, or downstream restrictions: _not_ "any purpose" |
| __Open weights, permissive license__ | [Gemma 4](https://ai.google.dev/gemma/docs/core/model_card_4), [Qwen3](https://huggingface.co/Qwen/Qwen3-8B), [DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1), [gpt-oss](https://huggingface.co/openai/gpt-oss-120b), [Mistral Large 3 / Small 4](https://docs.mistral.ai/getting-started/models/) | weights under Apache 2.0 or MIT | training data and full pipeline _not_ released |
| __Fully (or nearly) open__ | [OLMo 3](https://allenai.org/blog/olmo3), [Apertus](https://www.apertus-ai.org/), [Minerva](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0) | weights + code + data (or data pipeline) + docs | reproduction still needs _enormous_ compute |

---

## The licensing landscape (as of September 2026)

### Licenses change across versions: always check the __exact checkpoint__

| Model | Before | Now |
|---|---|---|
| __Gemma__ | Gemma 3: custom Gemma Terms, with cascading use restrictions | Gemma 4 (2026): __Apache 2.0__ |
| __DeepSeek-V3__ | original V3: custom DeepSeek Model Agreement | V3-0324: [relicensed under __MIT__](https://api-docs.deepseek.com/news/news250325) (March 2025) |
| __Mistral__ | historically mixed | _still_ mixed: Large 3 and Small 4 Apache 2.0, Medium 3.5 "Modified MIT", several models proprietary |
| __Teuken__ | v0.4-commercial: Apache 2.0 | v0.6: __non-commercial__ ("newer" does not mean "more permissive") |
| __iGenius → Domyn__ | Italia 9B: MIT; Italia 10B: [custom, non-open license](https://secure.igenius.ai/legal/iGenius%2BLicense%2BItalia%2B10B.pdf) | [rebranded Domyn](https://www.domyn.com/news/introducing-domyn) (June 2025); [Domyn Small 10B](https://www.domyn.com/news/introducing-domyn-small-an-open-european-reasoning-llm-built-for-ai-ownership) (May 2026): MIT |

---

## What do restrictive licenses mean in practice?

| License | On-premise use | Fine-tuning | Hosted service | Redistribution |
|---|---|---|---|---|
| __Llama 4__ ([license](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE), [AUP](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)) | yes, __except__ multimodal models for individuals/companies _based in the EU_ | yes | yes (EU _end users_ of products are carved out) | _"Built with Llama"_ attribution; derived models named _"Llama..."_; separate license above 700M monthly active users |
| __Gemma 3__ ([terms](https://ai.google.dev/gemma/terms)) | yes, within the prohibited-use policy | yes, derivatives inherit the restrictions | counts as _distribution_ | restrictions must be passed to downstream users; Google may restrict use _"remotely or otherwise"_ (a contractual right, not a kill switch) |
| __OpenRAIL__ ([OpenRAIL-M](https://www.licenses.ai/blog/2022/8/26/bigscience-open-rail-m-license)) | yes, for permitted purposes | yes, for permitted purposes | yes, users bound to use restrictions | use restrictions must be passed on |
| __Apache 2.0 / MIT__ | yes | yes | yes | yes, with attribution/notices (and patent clauses, for Apache) |

{{% fragment %}}
> __Running example__: the admission assistant must read _passport pictures_, hence needs a __multimodal__ model. The University of Bologna is an EU organization: under Llama 4's acceptable use policy, it is __not__ granted the right to use Llama 4's multimodal models. Gemma 4, Qwen3, or Mistral's Apache models raise no such issue
{{% /fragment %}}

---

## Derivatives: fine-tunes, distillation, merges, data, outputs

- __Fine-tunes__ remain subject to the base model's license: easy for Apache/MIT, restrictions _propagate_ for Gemma 3 and Llama
- __Distillation__ is license-specific:
    + Gemma 3 counts models trained on Gemma's _outputs_ (synthetic data) as _Model Derivatives_
    + DeepSeek-R1 (MIT) allows distillation, but its published _distills_ are fine-tunes of other models, and __inherit their licenses__ ([Qwen](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B) → Apache 2.0, [Llama](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) → Llama license)
- __Merges__: a merge of models A and B must (conservatively) satisfy __both__ licenses; a restrictive component is not "washed away"
    + whether weights are copyrightable at all is still legally _unsettled_
- __Training data__ has its _own_ license: e.g. OLMo 3 is Apache 2.0, but its dataset [Dolma 3](https://huggingface.co/datasets/allenai/dolma3_mix-6T) is ODC-By (attribution required), and its sources may carry further terms
- __Outputs__: "the vendor claims no rights on outputs" $\neq$ "outputs are free of restrictions"
    + e.g. using Llama _outputs_ to train a distributed model triggers Llama's _naming_ requirement

---

{{< slide id="open-models-ai-act" >}}

## Open models under the EU AI Act

| GPAI provider duty ([Art. 53](https://artificialintelligenceact.eu/article/53/)) | Ordinary GPAI | Free/open-source GPAI |
|---|---|---|
| (a) technical documentation (for the AI Office) | required | __exempt__ |
| (b) information for downstream providers | required | __exempt__ |
| (c) policy to comply with EU _copyright_ law (incl. text-and-data-mining opt-outs) | required | __still required__ |
| (d) public _summary of training content_ (AI Office template) | required | __still required__ |
| systemic-risk obligations ([Art. 55](https://artificialintelligenceact.eu/article/55/)) | if > 10<sup>25</sup> FLOPs | __no exemption__ |

- To qualify, the model must be released under a license allowing _access, use, modification, and distribution_, with weights, architecture, and usage information _public_
    + this is much __weaker__ than OSAID: no training data or training code needed
- Non-EU providers of open-source GPAI are also exempted from appointing an EU _authorized representative_ ([Art. 54(6)](https://artificialintelligenceact.eu/article/54/)), unless the model poses systemic risk
- cf. the Commission's [AI Act Service Desk FAQ](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source) on open-source GPAI models

> The AI Act gives open-source GPAI a __documentation discount__: __not__ a copyright exemption, __not__ a training-data-summary exemption, and __not__ a systemic-risk exemption

---

{{< slide id="sovereignty" >}}

## "Sovereign AI": a framing, and its limits

- Several European and Italian actors frame open, locally-developed models as a matter of __digital sovereignty__
    + reduce dependency on US and Chinese providers; better support for EU _languages_; compliance with EU _law_
- The framing mixes (at least) three __distinct__ goals, which should _not_ be conflated:
    1. __where__ a model is _developed_ (nationality of the developer)
    2. __where__ it is _executed_, and data are processed (_operational_ control)
    3. whether its making can be _inspected_ and _reproduced_ (_auditability_)
- Goals 2 and 3 do __not__ require goal 1:
    + _any_ open-weights model (e.g. Qwen3, gpt-oss, OLMo 3) can run in an EU data centre
    + the most reproducible models are not necessarily European (e.g. OLMo 3, from the US), and a European vendor may disclose little (e.g. Mistral)

{{% fragment %}}
> Skeptical reading: for an engineer, _where the model runs_ and _what its license allows_ matter much more than _who trained it_. The evidence (next slides) suggests that EU and Italian models are mostly __small__, __late__, and __not competitive__ with the frontier, nor with the best global open-weights models
{{% /fragment %}}

---

## Italian initiatives

| Model | Who | What | License | Status (Sep. 2026) |
|---|---|---|---|---|
| [Minerva](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0) | Sapienza NLP, within the [FAIR](https://fondazione-fair.it/) PNRR project; trained on CINECA's Leonardo | up to __7B__, from scratch; 1.14T Italian + 1.14T English + 200B code tokens | Apache 2.0, open data | 7B presented in Nov. 2024; still the flagship, research-grade |
| [LLaMAntino / ANITA](https://huggingface.co/swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA) | Univ. of Bari | _fine-tunes_ of Llama, Mistral, gpt-oss for Italian (not trained from scratch) | inherited; [ANITA-NEXT](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA)'s metadata says Apache 2.0, its card says "research only" | active research project; license hygiene is weak |
| [Velvet](https://huggingface.co/Almawave/Velvet-14B) | Almawave (private); trained on Leonardo | 2B and 14B, 6 languages (~23% Italian for the 14B) | Apache 2.0 | released Jan.–Feb. 2025, static since |
| [Italia](https://huggingface.co/sapienzanlp/modello-italia-9b) → [Domyn Small](https://huggingface.co/domyn/Domyn-Small-v1.0) | iGenius (private), renamed Domyn in June 2025 | Italia 9B (2024), then 10B; Domyn Small 10B (May 2026), 50+ languages | Italia 9B: MIT; Italia 10B: _custom, non-open_; Domyn Small: MIT | company focus moved to _proprietary_ large models |

- A "__national__" model says nothing about its _openness_: compare Minerva (Apache, open data) with Italia 10B (restrictive license)
- All Italian models are in the __2–24B__ range: one or two orders of magnitude below frontier models

---

## European initiatives

| Initiative | Who | What | License | Status (Sep. 2026) |
|---|---|---|---|---|
| [EuroLLM](https://huggingface.co/utter-project/EuroLLM-22B-2512) | IST Lisbon, Univ. of Edinburgh, Unbabel, et al.; EuroHPC and Horizon Europe funding | 1.7B, 9B, 22B; 35 languages (all 24 EU ones), ~4T tokens | Apache 2.0 | 22B released Feb. 2026 |
| [OpenEuroLLM](https://openeurollm.eu/) | 20 members, led by Charles University and AMD Silo AI; Digital Europe grant (Feb. 2025, 3 years) | "truly open" models for all EU languages | open (planned) | so far only small _reference_ models (e.g. [38 monolingual 2.15B](https://openeurollm.eu/blog/hplt-oellm-38-reference-models), with HPLT); flagship still pending |
| [OpenLLM-France](https://openllm-france.fr/en/main-page-en/) | French consortium, Bpifrance funding | [Lucie-7B](https://huggingface.co/OpenLLM-France/Lucie-7B), then [Luciole](https://huggingface.co/collections/OpenLLM-France/luciole-llm) 1B/8B/23B (~30% French) | open data, weights, code | research project |
| [Teuken / OpenGPT-X](https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html) | Fraunhofer, FZ Jülich, et al.; ~€14M from the German government | 7B, 24 EU languages | v0.4: Apache 2.0; v0.6: non-commercial | project __ended__ in March 2025; models still downloadable |
| [Apertus](https://www.apertus-ai.org/) | ETH Zurich, EPFL, CSCS (Swiss AI Initiative: CHF 20M + 10M GPU-hours) | 8B, 70B; 1.5 (July 2026) adds images, reasoning, tools | Apache 2.0, fully open | the most complete open release in Europe; 2.0 planned for 2027 |
| [Mistral AI](https://docs.mistral.ai/getting-started/models/) | French private company | from small to large MoE models | mixed: Apache 2.0, Modified MIT, proprietary | the European vendor closest to the frontier; little training disclosure |

---

## Infrastructure and policy

- __EuroHPC AI Factories__: supercomputing centres opened to AI training and use
    + [IT4LIA](https://www.hpc.cineca.it/projects/it4lia/), at CINECA in Bologna (with Austria and Slovenia), was among the [first seven](https://eurohpc-ju.europa.eu/selection-first-seven-ai-factories-drive-europes-leadership-ai-2024-12-10_en) selected in Dec. 2024 (€1.5bn in total, EU + national funds)
    + beware: IT4LIA is an AI __Factory__, __not__ an AI _Gigafactory_: the [Gigafactories call](https://www.eurohpc-ju.europa.eu/eurohpc-joint-undertaking-launches-ai-gigafactories-call-2026-07-30_en) (for frontier-scale training) opened only in July 2026, with a Nov. 2026 deadline
- __Data__: [ALT-EDIC](https://www.alt-edic.eu/)'s [LLMs4EU](https://www.alt-edic.eu/projects/llms4eu/) (March 2025, 3 years, 20+ countries) collects language resources for all EU languages, and targets sector-specific models
- __Italian policy__: the [Italian AI Strategy 2024–2026](https://www.agid.gov.it/sites/agid/files/2024-07/Strategia_italiana_per_l_Intelligenza_artificiale_2024-2026.pdf) and [Law 132/2025](#/regulation) call for technology "tailored to the Italian context" and open research artifacts

{{< image src="./europe-timeline.svg" max-h="35vh" alt="Timeline 2023-2026 contrasting global frontier model releases with EU and Italian releases and projects, which are smaller and arrive later" >}}

---

## How good are Italian models?

- Measuring it is hard: translated English benchmarks are _not_ enough
    + [ITA-Bench](https://aclanthology.org/2024.clicit-1.67/) (CLiC-it 2024) mixes translated tasks with native Italian datasets
    + [Evalita-LLM](https://arxiv.org/abs/2502.02289) (2025) uses _native_ Italian tasks, and multiple prompts per task, since rankings are _sensitive_ to prompt wording ([leaderboard](https://huggingface.co/spaces/evalitahf/evalita_llm_leaderboard))
- Published numbers show that small Italian models can be _useful_, e.g. [Velvet-2B](https://huggingface.co/Almawave/Velvet-2B) reports 39.6 on Italian MMLU and 61.9–86.6 on ITA-Bench tasks...
- ... but there is __no robust evidence__ that Italian models outperform large multilingual open models (e.g. Qwen3, Gemma 4), let alone frontier ones, _even on Italian_

{{% fragment %}}
> Leaderboard positions change every few months: when citing a rank, always write the __snapshot date__
{{% /fragment %}}

---

## Recurring issues of European open models

1. __Data__: too little high-quality text in less-resourced languages (the very reason for LLMs4EU and for synthetic data)
2. __Compute__: every project depends on a public supercomputer allocation (Leonardo, MareNostrum 5, JUWELS, Alps); an "open" model is not _reproducible_ by anyone who lacks one
3. __Scale and timing__: models of 2–24B parameters, released _months to years_ after comparable global open models; flagships "planned" or "pending"
4. __Maintenance__: projects have _finite_ funding (e.g. OpenGPT-X ended in 2025): who fixes, updates, and re-evaluates the models afterwards?
5. __Adoption__: public-administration use is mostly _aspirational_ in the sources, not a demonstrated large-scale deployment

{{% fragment %}}
> These initiatives are valuable for __research__, __openness__, and __language coverage__; they are (still) __not__ a production-grade alternative to global models. An EU organization can get operational control by running a _global_ open-weights model on _EU_ infrastructure
{{% /fragment %}}

---

{{< slide id="open-models-checklist" >}}

## Engineering take-aways: pre-adoption checklist

The compliance unit is __checkpoint + license version + code licenses + data licenses + deployment + intended use__, not a brand name

| Question | What to check |
|---|---|
| exactly _which_ artifact? | repository, checkpoint hash, release date, license version |
| commercial use? | Apache/MIT: yes; CC-BY-NC: no; custom licenses: read the use restrictions |
| on-premise use? | the license, not the availability of files (e.g. Llama 4 multimodal in the EU) |
| fine-tuning, distillation, merging? | whether derivatives inherit restrictions; license of _each_ parent model |
| hosted service or redistribution? | whether serving an API counts as distribution (it does for Gemma 3); attribution and naming duties |
| geography or scale limits? | e.g. Llama 4: EU multimodal clause, 700M monthly users |
| training and fine-tuning data? | provenance, licenses (e.g. ODC-By), personal data |
| AI Act role? | are _we_ becoming a GPAI provider (e.g. by fine-tuning and distributing)? does the open-source exemption apply? |
| reproducibility needed? | self-hosting: permissive weights suffice; audit or research: prefer fully open models (OLMo 3, Apertus) |

> Mnemonic: __weights → license → recipe → data → regulatory role__: a model is only as open as the layer that matters for your use

---

## Engineering take-aways: three scenarios

{{% multicol %}}
{{% col %}}

### A UniBo lab, on-premise

- wants: local RAG/chat, fine-tuning on university material, reproducible experiments
- good fits: OLMo 3, Apertus (reproducibility); Gemma 4, Qwen3, gpt-oss, Mistral Apache models (weights only suffice); Minerva (Italian-centric research)
- ruled out: Llama 4 _multimodal_ (EU clause)

{{% /col %}}
{{% col %}}

### An Italian startup reselling a fine-tune

- wants: fine-tune, host, sell the model
- good fits: Apache/MIT weights (Gemma 4, Qwen3, gpt-oss, DeepSeek-R1, Mistral Large 3, OLMo 3, Domyn Small)
- beware: R1 _distills_ (Llama-based ones inherit Llama's license); Gemma 3 (restrictions flow to customers); Teuken v0.6 (non-commercial)

{{% /col %}}
{{% col %}}

### A public administration

- wants: EU-controlled deployment and auditability
- _auditability_: Apertus, OLMo 3, Minerva
- _operational control_: any permissively licensed model on EU infrastructure (incl. Mistral, EuroLLM, Velvet, Domyn Small)
- beware: IT4LIA/CINECA provides _compute_, not a model license

{{% /col %}}
{{% /multicol %}}

{{% /section %}}

---

# Agentic Technique Selection Criteria

---

{{% section %}}

{{< slide id="technique-selection" >}}

## Which technique? The general concept

Given a model, there are several ways to make it _behave_ as your task requires, ordered by increasing _effort_:

1. __Prompting__: instructions, examples, and output formats in the prompt (cf. _prompt engineering_ lecture)
    + changes the model's _behaviour_, at _no_ training cost; limited by what the model already _knows_ and by the _context window_
2. __Tools__ and __agents__: let the model _act_ (call APIs, query databases, run code) and iterate (cf. _tools and agents_ lecture)
    + gives access to _live_ data and _actions_; adds complexity, latency, and _security_ concerns
3. __Retrieval-Augmented Generation__ (RAG): retrieve relevant documents and put them in the prompt ([Lewis et al., 2020](https://arxiv.org/abs/2005.11401); cf. _RAG_ lecture)
    + gives access to _private_ or _up-to-date_ knowledge; adds an indexing pipeline to maintain
4. __Skills__ and __workflows__: package instructions, tools, and steps into reusable procedures (cf. _skills_ and _workflows_ lectures)
    + trade _flexibility_ (skills: the agent decides) for _predictability_ (workflows: the engineer decides)
5. __Fine-tuning__: further _train_ the model on task-specific examples
    + changes _style_, _format_, and _narrow skills_ reliably; costly, needs data, and ties you to a model (and a license allowing it!)

---

## Which technique? An intuitive example

{{< mermaid >}}
%%{init: {'flowchart': {'htmlLabels': false}}}%%
flowchart LR
    Q{"Is prompting good enough
    on your validation set?"} -->|yes| P["Stop: use prompting"]
    Q -->|no| M{"What is missing?"}
    M -->|"knowledge the model lacks
    (private / recent documents)"| R["RAG
    e.g. answer questions
    about the PhD regulations"]
    M -->|"ability to act,
    or live data"| T["Tools / agents
    e.g. check the candidate's
    university in a ranking API"]
    M -->|"a multi-step procedure,
    followed reliably"| S{"Who decides
    when to apply it?"}
    S -->|"the engineer
    (fixed steps)"| W["Workflow
    e.g. extract → validate
    → score → report"]
    S -->|the agent| K["Skill"]
    M -->|"a consistent style, format, or
    narrow skill (+ data, budget, license)"| F["Fine-tuning
    e.g. evaluations in the
    committee's house style"]
{{< /mermaid >}}

(cf. OpenAI's [optimizing LLM accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) guide, and Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))

---

## Which technique? Trade-offs

| Technique | Quality | Cost | Control | Compliance | Time-to-market |
|---|---|---|---|---|---|
| __Prompting__ | good, if the model knows enough | low (but long prompts cost tokens at each request) | high: prompts are versioned text | easy to audit | fastest |
| __Tools / agents__ | high for tasks needing actions or live data | medium (more requests per task) | medium: behaviour is less predictable | needs _least privilege_ and logging | medium |
| __RAG__ | high for knowledge-intensive tasks | medium (indexing + longer prompts) | high: knowledge base is inspectable and updatable | data stays in _your_ store; access control needed | medium |
| __Skills__ | high, if the agent picks the right skill | low–medium | medium: the agent decides when to apply them | depends on the tools the skill allows | fast (write a document) |
| __Workflows__ | high and _consistent_ | medium | highest: steps are fixed by the engineer | easy to audit step by step | slow (more code) |
| __Fine-tuning__ | highest for _narrow_ tasks, if data suffice | high (data, training, re-training at each model update) | low–medium: behaviour baked into weights | training data must be lawful; license must allow it | slowest |

- These options __combine__: e.g. a workflow whose steps use prompting, RAG, and tools
- Empirically, RAG tends to outperform fine-tuning at injecting _new knowledge_ ([Ovadia et al., 2023](https://arxiv.org/abs/2312.05934)), while fine-tuning is better at shaping _form_

{{% fragment %}}
> __Rule of thumb__: start with prompting, measure, and add complexity (tools, RAG, workflows, fine-tuning) only when evaluations show that it is _needed_
{{% /fragment %}}

{{% /section %}}

---

# Model Selection Criteria

---

{{% section %}}

{{< slide id="model-selection" >}}

## Which model? The general concept

- Choosing a model is a _governance_ decision, since it affects all five dimensions at once:
    + _quality_ (capabilities), _cost_ (price per token, or hardware), _control_ (open weights? version pinning? deprecation?), _compliance_ (license, provider's jurisdiction and data policies), _time-to-market_ (availability, ecosystem)
- It requires _information_ about models, which comes from:
    1. their __documentation__ (model cards, system cards, licenses, terms of service)
    2. public __evaluations__ (benchmarks, leaderboards)
    3. __your own__ evaluations on the task at hand
- It is __not__ a one-off decision: models are _updated_, _deprecated_, and _surpassed_ every few months, so the choice must be _re-assessed_ periodically (and made _reproducible_)

(cf. [model zoos](../llmaas/#/model-zoos) in the LLM-as-a-Service lecture)

---

## Model documentation: model cards, system cards, datasheets

- __Model cards__ ([Mitchell et al., 2019](https://arxiv.org/abs/1810.03993)): short documents accompanying a model, reporting
    + _intended uses_ and _out-of-scope_ uses, _training data_ (summary), _evaluation_ results (also _disaggregated_ by groups), _ethical considerations_, _limitations_
    + nowadays standard on model zoos (e.g. [Hugging Face's model card guide](https://huggingface.co/docs/hub/model-cards))
- __Datasheets for datasets__ ([Gebru et al., 2021](https://arxiv.org/abs/1803.09010)): the same idea, for training data (motivation, composition, collection, recommended uses)
- __System cards__: longer reports published by frontier providers for each model release, focusing on _safety_ evaluations, red-teaming, and mitigations
    + e.g. [OpenAI's](https://openai.com/index/gpt-oss-model-card/) and [Anthropic's](https://www.anthropic.com/system-cards) system cards

{{< image src="./model-card-anatomy.svg" max-h="35vh" alt="Anatomy of a model card: eight sections, from model details to license, each tagged with the governance dimensions it informs (quality, compliance, control)" >}}

- __What to look for__, as an engineer: _license_, _languages_, _context window_, _knowledge cut-off_, _intended uses_ (does yours fit?), known _limitations_, and _evaluations_ relevant to your task

---

## Measuring _general_ capabilities: frontier benchmarks

As models _saturate_ classic benchmarks, new ones try to measure what models __cannot__ (yet) do:

- __ARC-AGI__ ([Chollet, 2019](https://arxiv.org/abs/1911.01547)): intelligence as _skill-acquisition efficiency_, measured on visual puzzles that are easy for humans, and require _abstracting_ rules from a few examples
    + [ARC-AGI-2](https://arxiv.org/abs/2505.11831) (2025) raised the difficulty; the [ARC Prize 2025](https://arcprize.org/blog/arc-prize-2025-results-analysis) grand prize went _unclaimed_
    + [ARC-AGI-3](https://arcprize.org/blog/arc-agi-3-launch) (March 2026) is _interactive_: agents must explore game-like environments; at launch, humans solved all of them, frontier models almost none
- __Humanity's Last Exam__ ([Phan et al., 2025](https://arxiv.org/abs/2501.14249)): 2,500 expert-written questions across disciplines, designed to be _un-googleable_
    + best models went from single digits (early 2025) to ~60% (cf. [Artificial Analysis](https://artificialanalysis.ai/evaluations/humanitys-last-exam), September 2026)
- __METR's time horizon__ ([Kwa et al., 2025](https://arxiv.org/abs/2503.14499)): the _length_ of tasks (in human-expert time) that an agent completes with 50% success
    + it has been _doubling_ every ~7 months (cf. [live measurements](https://metr.org/time-horizons))
- __Aggregated views__: the [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report) describes a _jagged frontier_: models winning maths olympiad gold medals, yet failing at reading analog clocks

{{< image src="./benchmark-saturation.png" max-h="40vh" alt="AI Index 2026, Figure 2.1.1: best model performance relative to the human baseline, 2012-2025, on ImageNet, SuperGLUE, MMLU, GPQA Diamond, MATH, MMMU, AIME, SWE-bench Verified, OSWorld and others: each benchmark climbs towards or past the human baseline, newer ones ever faster" >}}

<small>Source: [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report), ch. 2, Figure 2.1.1 ([CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/))</small>

> __Engineering take-away__: frontier benchmarks tell you where the _state of the art_ is, not whether a model is good for __your__ task

---

## How to choose a model for a given task?

{{% multicol %}}
{{% col %}}

### Hard constraints (filter)

1. __Deployment__: on-premise (hardware available?) or on-cloud (budget available?)
2. __Data protection__: can the data leave your premises? which jurisdiction? (cf. GDPR)
3. __License__: is the intended use (e.g. commercial) permitted?
4. __Modalities__: text only? images? audio?
5. __Capabilities__: tool calling? structured output? reasoning?
6. __Context window__: will prompts + documents + history fit?
7. __Languages__: e.g. is Italian supported well enough?

{{% /col %}}
{{% col %}}

### Soft criteria (rank)

- _quality_ on __your__ task (see next slide)
- _latency_ (time to first token, tokens per second)
- _cost_ per request (tokens × price, or hardware amortization)
- _stability_ of the offer (will the model be deprecated soon?)
- _ecosystem_ (client libraries, documentation, community)

{{% fragment %}}
> __Rule of thumb__: start from the _smallest/cheapest_ model satisfying the hard constraints, measure its quality on your task, and move to _bigger_ models only if needed
{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

{{< mermaid >}}
%%{init: {'flowchart': {'htmlLabels': false}}}%%
flowchart LR
    Z[("All models
    in the zoo")] --> D[/"Deployment &
    data protection"\] --> L[/"License"\] --> C[/"Modalities &
    capabilities"\] --> X[/"Context window
    & language"\] --> S["Shortlist
    (3-5 models)"] --> E["Evaluate on
    your own test set"] --> P(["Pick the cheapest one
    above the quality threshold"])
{{< /mermaid >}}

---

## How to evaluate models?

### 1. Public __benchmarks__ and __leaderboards__ (generic, cheap to consult)

- _benchmarks_: fixed datasets + metrics for some capability
    + e.g. knowledge ([MMLU](https://arxiv.org/abs/2009.03300)), expert reasoning ([GPQA](https://arxiv.org/abs/2311.12022)), coding ([SWE-bench](https://www.swebench.com/)), tool use, long context...
    + holistic frameworks like [HELM](https://arxiv.org/abs/2211.09110) evaluate many models on many scenarios and metrics (not just accuracy)
- _leaderboards_: rankings aggregating benchmark results or human preferences
    + e.g. [Arena](https://arena.ai/) (formerly Chatbot Arena / LMArena: humans blindly compare pairs of answers, cf. [Chiang et al., 2024](https://arxiv.org/abs/2403.04132); but see also the critique by [Singh et al., 2025](https://arxiv.org/abs/2504.20879)), [Artificial Analysis](https://artificialanalysis.ai/) (quality vs. price vs. speed)
- __caveats__:
    + _data contamination_: benchmark items may have leaked into training data (cf. [Xu et al., 2024](https://arxiv.org/abs/2406.04244))
    + _saturation_: top models all score near 100%, so benchmarks stop discriminating (e.g. Hugging Face [retired](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135) its Open LLM Leaderboard in 2025)
    + _Goodhart's law_: once a benchmark becomes a target, it stops being a good measure
    + benchmarks measure _generic_ skills, possibly _not_ the ones your task requires

### 2. __Task-specific__ evaluation (the one that really matters)

- build a small _validation set_ of realistic inputs for __your__ task (with expected outputs, when possible)
- run each shortlisted model on it, and _score_ outputs: exact match, schema validity, custom checks, or _LLM-as-a-Judge_
- measure _latency_ and _cost_ too (both reported in the API responses' metadata, e.g. `usage`)
- (systematic infrastructure for this will be discussed in the _prompt engineering_ lecture)

---

{{< slide id="compare-models" >}}

## Exercise 1: Comparing Models on the Running Example (pt. 1)

> __Goal__: the admission committee wants to pick the model to be used for letter scoring (cf. [Example 1 of the Prompt Engineering lecture](../prompting/#/letter-scoring)), based on _evidence_ rather than on hype

### TO-DO List

1. __Shortlist__ 3 models, e.g.:
    + one small _free_ model on Open Router,
    + one larger (possibly free) model on Open Router,
    + one _local_ model via Ollama (if your hardware allows it)
2. Run the letter-scoring system on __all 3 letters__ of the running example, __5 times__ per letter per model
    + the script is already parametric w.r.t. the model: just change `OPENAI_MODEL` (and `OPENAI_BASE_URL` for Ollama)
3. For each model, __collect__:
    + the _scores_ (average, and _variance_ across the 5 runs: is the model _consistent_?)
    + the _agreement_ among models (do they rank candidates in the same way?)
    + the number of _failures_ (e.g. invalid JSON, validation errors)
    + _latency_ (wall-clock time per request) and _tokens_ used (from `response.usage`), hence _cost_
4. Summarize the results in a __table__, and motivate your choice

---

## Exercise 1: Comparing Models on the Running Example (pt. 2)

### Decision points and hints

- How to automate the runs?
    * e.g. a script looping over models × letters × repetitions, writing one row per run in a CSV file
    * reuse the caching mechanism of [Exercise 1 of the LLM-as-a-Service lecture](../llmaas/)? (careful: caching would hide the variance!)
- How to measure time?
    * e.g. `time.perf_counter()` before and after the request
- How to compute costs?
    * `score_letter(...)` only returns the parsed `LetterInfo`: adapt it to also return the whole `response` (or its `usage`)
    * multiply `usage.prompt_tokens` and `usage.completion_tokens` by the prices listed in the zoo (Open Router also reports `usage.cost` directly)
- How to deal with rate limits of free models?
    * reuse the retry mechanism of [Exercise 2 of the LLM-as-a-Service lecture](../llmaas/)
- What if models disagree?
    * which one is _right_? you need a __reference__: e.g. score the letters yourself, and compare each model against your scores

### How to test it?

- the table should contain 3 models × 3 letters × 5 runs = 45 rows (minus failures, which should be _counted_, not hidden)
- re-running the script with a _different temperature_ (e.g. `0` vs. `1`) should visibly affect the variance

---

{{< slide id="decision-record" >}}

## Exercise 2: A Governance Decision Record for the Running Example (pt. 1)

> __Goal__: the University asks the committee to _justify_ the adoption of the admission assistant, before using it on real applications

### TO-DO List

Write a short (2–4 pages) __decision record__, answering:

1. __Regulatory classification__: is the system _high-risk_ under the EU AI Act? Which _obligations_ follow for the University (as _deployer_)? Which GDPR _obligations_ apply to candidates' documents?
2. __Deployment__: cloud API, hosted open model, or on-premise? Support the choice with a _cost estimate_ (number of applications per year × tokens per application × price, vs. hardware) and _privacy_ considerations
3. __Model__: which model? Support the choice with the results of [Exercise 1](#/compare-models), and with the model's _documentation_
    + apply the [pre-adoption checklist](#/open-models-checklist) to the __exact checkpoint__: license, multimodal restrictions, derivatives, AI Act role
4. __Technique__: which parts rely on prompting / structured output / tools / RAG? Why not fine-tuning?
5. __Human oversight__: which outputs are _reviewed_ by humans, how, and who is _accountable_ for the final decision?
6. __Monitoring__: what is _logged_, and when is the decision _re-assessed_ (e.g. model deprecation, new regulations)?

---

## Exercise 2: A Governance Decision Record for the Running Example (pt. 2)

### Decision points and hints

- Take inspiration from _Architecture Decision Records_ (ADRs, cf. <https://adr.github.io/>): _context_, _options considered_, _decision_, _consequences_
- Use the _five dimensions_ (quality, cost, control, compliance, time-to-market) as the evaluation criteria for each option, possibly in a table
- For regulation, cite the __article__ of the law supporting each claim
- For costs, state your _assumptions_ explicitly (e.g. tokens per document), and compute a _break-even_ point
- Be explicit about what the system does __not__ decide: e.g. scores as _suggestions_ to the committee, never automatic rejections

### How to assess it?

- Could a colleague _reproduce_ your choice from the record alone?
- Would the record survive a question from the University's _Data Protection Officer_?
- Does the record say _when_ it should be revised?

{{% /section %}}

---

{{% import path="reusable/back.md" %}}

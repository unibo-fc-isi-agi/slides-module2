+++

title = "[AgI] Free Access to LLMs (Appendix)"
description = "Practical reference: free tiers, credits, grants, and local alternatives for students and researchers"
outputs = ["Reveal"]

+++

# Free Access to LLMs

_(Appendix)_

{{% import path="reusable/footer.md" %}}

---

## Before you start

- This is a _practical reference_ on how to use LLMs __without paying__, for _study_ and _research_
    + for Master's and PhD students, researchers, and teachers
- All figures are a __snapshot as of 30 September 2026__
    + quotas, programs, and even models change _every few months_
    + __always check the linked page__ before relying on an offer
- "Free" here means _no money from your pocket_: someone else pays (a provider, a cloud, a grant, your lab), or you pay in _hardware_

---

## What "free" can mean

1. __Standing free tier__: a _recurring_ zero-price quota (per minute / day / month), no application needed
2. __Trial__: a _one-off_ balance that _expires_ (e.g. $5 for 30 days)
    + a trial is __not__ a free tier: don't build a course or a paper on top of it
3. __Student credits__: cloud credits for enrolled students, renewable while eligible
4. __Research grants__: credits awarded upon _application_, for a specific project
5. __Local open weights__: the API bill is zero, but you pay in _hardware_ and _electricity_

{{% fragment %}}
> Rule of thumb: __grant → student credits → free tier → local model → trials__
{{% /fragment %}}

---

## Which route for me?

| Need | First choice |
|---|---|
| A few hundred calls, prototyping, exercises | [Free tiers](#/free-tiers): Gemini, Mistral, Groq, GitHub Models, OpenRouter |
| Thousands or millions of calls, for a paper | [Research grants](#/grants) or [cloud credits](#/students) |
| Sensitive or personal data | [Local open model](#/local), or a _contracted_ API with suitable data terms |
| A course, repeated every semester | [Department gateway](#/gateway) + local model + free tiers as fallback |
| Reproducible experiments | [Pinned open weights, run locally](#/local) |

---

{{< slide id="free-tiers" >}}

## Free APIs you can use _today_

No application: just sign up, get a key, and stay within the quota

| Provider | What you get for free | Good for |
|---|---|---|
| [Google Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | Zero-price quota on several current models (e.g. Flash, Flash-Lite), model-specific limits | Best overall free frontier-ish API |
| [Mistral](https://mistral.ai/pricing/) (Free plan) | __$10/month__ of API credits | Direct access to Mistral models |
| [Groq](https://console.groq.com/docs/rate-limits) | e.g. `gpt-oss-120b`: 30 req/min, 1,000 req/day, 200k tokens/day | Fast open models |
| [GitHub Models](https://docs.github.com/en/billing/concepts/product-billing/github-models) | Rate-limited access to its catalog, with any GitHub account | Comparing many models, quickly |
| [OpenRouter](https://openrouter.ai/docs/api_reference/limits) `:free` models | 20 req/min, __50 req/day__ | One key, many open models |
| [Cohere](https://docs.cohere.com/docs/rate-limits) (trial key) | 1,000 calls/month | Evaluation, embeddings, rerankers |

---

## One client, _many_ free providers

- All the providers above expose an __OpenAI-compatible__ API: only `base_url`, key, and model name change

{{% code path="content/free-access/free_providers.py" from="5" to="14" %}}

```bash
python free_providers.py groq                               # list the models available now
python free_providers.py groq openai/gpt-oss-20b "Hello!"   # one chat request
```

- Full script [here](./free_providers.py); model IDs are _listed live_, not hard-coded, since they __go stale quickly__
- The same trick works with the [LLM-as-a-Service](../llmaas) scripts: just set `OPENAI_BASE_URL` and `OPENAI_API_KEY`

---

## Don't count on these

| Offer | Reality |
|---|---|
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | __Trial__: $5 expiring after 30 days, then pay |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/pricing) | $0.10/month: smoke tests only |
| [Hugging Face ZeroGPU](https://huggingface.co/docs/hub/spaces-zerogpu) | 5 GPU-minutes/day: fine for _demos_, not for experiments |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | Free GPUs, but type and limits _not guaranteed_ |
| [Replicate](https://replicate.com/docs/pricing) | __No__ standing free tier: pay-as-you-go |

---

{{< slide id="students" >}}

## Students: cloud credits

| Program | What | Who | Notes |
|---|---|---|---|
| [Azure for Students](https://azure.microsoft.com/en-us/free/students) | __$100 / 12 months__, no credit card | Full-time university students | Renewable yearly; includes Azure OpenAI |
| [AWS Cloud Credit for Research](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/) | Up to __$5,000__ (students) | Graduate / PhD students at accredited institutions | Application, 90–120 days review; credits last 1 year |
| [Anthropic, Claude for scientists](https://www.anthropic.com/news/expanding-support-for-scientists) | Free _Claude_ seat for 1 year | Lab members, added by a verified PI | A _subscription_, not API credits |

- Cloud credits can pay for __managed model APIs__ in that cloud (Azure OpenAI, Bedrock, Vertex AI)
- Watch out for the moment credits _run out_: set a __budget alert__, or you will be billed

---

{{< slide id="grants" >}}

## Researchers: grants

| Program | Amount | Who | How |
|---|---|---|---|
| [OpenAI Researcher Access](https://openai.com/form/researcher-access-program/) | Up to __$1,000__, 12 months | Academic / research / nonprofit affiliation | Research question + intended use; reviewed quarterly ([FAQ](https://help.openai.com/en/articles/10139500-researcher-access-program-faq)) |
| [Anthropic AI for Science](https://www.anthropic.com/news/expanding-support-for-scientists) | Up to __$50,000__ / project | _Any_ researcher may apply | Project proposal; selective |
| [Cohere Labs Catalyst](https://cohere.com/research/grants) | Varies | Non-commercial, open-science / public-benefit projects | Rolling [application](https://cohere.com/research/grants/application) |
| [Google Cloud for Researchers](https://cloud.google.com/edu/researchers) | __$5,000__ | Academic researchers | Application |
| [AWS Cloud Credit for Research](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/) | No fixed cap (faculty) | Faculty and research staff | Application, 90–120 days |

- Apply __early__: approval takes weeks to months

---

## Startups _(in brief)_

| Program | Amount |
|---|---|
| [Google for Startups, AI](https://cloud.google.com/startup/ai) | Up to $350,000 over 2 years (Google models only) |
| [Microsoft for Startups](https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview) | Up to $150,000, scaling with progress |
| [AWS Activate](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/) | Up to $200,000 |

- Since May 2026, AWS Activate credits can pay for __third-party models on Bedrock__ (Anthropic, Mistral, Meta, ...) ([source](https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/))
- "Up to" is the _maximum_, not what everybody gets

---

{{< slide id="local" >}}

## Local models: the only _durable_ free API

- Open-weight models + an inference server = an API that __nobody can revoke__ or re-price
    + [`gpt-oss-20b`](https://openai.com/index/introducing-gpt-oss/) (Apache 2.0): about __16 GB__ of memory, a good laptop / workstation baseline
    + `gpt-oss-120b`: about __80 GB__, one large GPU
    + others: [Gemma 4](https://ai.google.dev/gemma/docs/core/model_card_4), [Mistral Small 4](https://mistral.ai/news/mistral-small-4/), [DeepSeek-R1 distills](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B) (check each license!)
- Serve them via [Ollama](https://ollama.com) (easy) or [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) (fast, multi-user): both expose an _OpenAI-compatible_ API
    + i.e. `python free_providers.py ollama` works out of the box
- __Quantization__ (4-bit) cuts memory by ~4×, usually with small quality loss, but __re-evaluate on your task__
    + see the [LLM-as-a-Service](../llmaas) lecture for requirements, quantization, and model zoos
- Pinned weights (exact revision + quantization + engine version) are also the best option for __reproducibility__

---

{{< slide id="gateway" >}}

## Labs and courses: a _gateway_, not a shared key

{{< mermaid >}}
flowchart LR
    U[Users, one virtual key each] --> G[Lab gateway, e.g. LiteLLM]
    G --> B[Per-user budgets + rate limits]
    B --> O[Grant-funded APIs]
    B --> C[Cloud credits]
    B --> F[Free tiers]
    B --> L[Local vLLM]
{{< /mermaid >}}

1. Create provider accounts under the _institution_, and keep the real keys __only on the gateway__
2. Run [LiteLLM](https://docs.litellm.ai/docs/proxy/virtual_keys) and give each user (or project) a _virtual key_ with a hard [budget and rate limit](https://docs.litellm.ai/docs/proxy/users)
3. Keep an _allow-list_ of models; record provider + model ID of each run
4. Clients just point `OPENAI_BASE_URL` to the gateway: __same code__ as above

---

## Don'ts

These _look_ free, but they break Terms of Service, leak data, or ruin reproducibility:

- __Sharing or trading API keys__: no attribution, one leak burns everybody's budget
    + OpenAI [recommends one key per person](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety); Mistral [forbids transferring keys](https://legal.mistral.ai/terms/commercial-terms-of-service/)
- __Multiple accounts__ / cycling trials to multiply quotas: leads to suspension
    + OpenRouter explicitly says [extra accounts do not raise limits](https://openrouter.ai/docs/api_reference/limits)
- __Wrapping consumer chat UIs__ (ChatGPT, Claude.ai) as an API: forbidden by [OpenAI](https://platform.openai.com/terms) and [Anthropic](https://www.anthropic.com/legal/consumer-terms) terms, and breaks at every UI change
- __VPNs__ to bypass regional or eligibility restrictions
- __Unknown free proxies__: the operator sees your prompts, outputs, and keys
- __Distilling__ a free proprietary API into your own model: OpenAI's [terms](https://platform.openai.com/terms) forbid using outputs to build competing models
    + with open teachers (e.g. DeepSeek-R1), check _both_ teacher and student-base licenses

---

## Privacy and reproducibility

{{% multicol %}}
{{% col %}}
### What happens to my data?
- Free tiers may use your prompts for _training_ and _human review_
    + __Gemini__: yes for free tiers in general, __but not__ for users in EEA / Switzerland / UK, where paid-tier rules apply ([terms](https://ai.google.dev/gemini-api/terms))
    + __OpenAI API__: not used for training by default ([source](https://openai.com/enterprise-privacy/))
- Never send _personal_, _confidential_, or _human-subject_ data to a free tier without reading its terms
{{% /col %}}
{{% col %}}
### What to record, for each experiment
- provider, endpoint, and service tier
- exact model ID (not just the family)
- date
- prompts, decoding parameters, seed
- number of calls, retry policy, aggregator (if any)
- local: weights revision, quantization, engine + version

> e.g. Cerebras [removed](https://inference-docs.cerebras.ai/support/change-log) `gemma-4-31b` from public endpoints on 3 Sep 2026
{{% /col %}}
{{% /multicol %}}

---

{{% import path="reusable/back.md" %}}

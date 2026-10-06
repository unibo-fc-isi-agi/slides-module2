+++

title = "[AgI] Generative AI 101"
description = "Gentle Introduction to Generative AI"
outputs = ["Reveal"]

+++

# Generative AI 101

{{% import path="reusable/footer.md" %}}

---

{{< slide id="intro" >}}

## __GenAI__: _Generative_ Artificial Intelligence

<!-- > [Systems based on] <br> -->
_AI_ algorithms capable of __automatically generating__ _content_, e.g.:
- _text_
- images
- audio and/or video
- [source] code
- ...

(cf. [Policy for the ethical and responsible use of Generative Artificial Intelligence in teaching and research activities](https://www.unibo.it/it/allegati/policy-per-un-uso-etico-e-responsabile-dell2019intelligenza-artificiale-generativa-nelle-attivita-di-didattica-e-ricerca/@@download/file/Policy-Generative-AI.pdf))

---

## GenAI through _Foundation Models_ (FM)

+ Large _neural networks_ that learn to _process_, _"understand"_, and _produce_ [not necessarily] __structured__ and __unstructured__ data
+ __trained__ on _large_ amounts of data, and with _large_ computational resources, to __do a bit of everything__
    - with the idea that they can later be __specialized__ for _specific tasks_

<br>
{{< image src="./foundation-models.svg" max-h="60vh" alt="Foundation models concept">}}

---

## __Terminology__: Foundation Models vs. _Large Language Models_

{{< image src="./fm-vs-llm.svg" width="80%" max-h="70vh" alt="Venn diagram explaining how LLMs are a specific case of foundation models" link="https://thebabar.medium.com/essential-guide-to-foundation-models-and-large-language-models-27dab58f7404" >}}

---

## Basic Operation of LLMs

{{< image src="./next-word-prediction.svg" width="100%" max-h="60vh" alt="Next token prediction: the LLM outputs a probability distribution over the next token, from which the next token is sampled">}}

- LLMs have learned to __predict__ the _next word_ (actually, _token_) in a _text_ given the _previous context_
    * similar to the _predictive_ keyboard on mobile phones, but much more _complex_ and _powerful_
    * the next token is __sampled__ from the predicted distribution: the _temperature_ parameter controls how _random_ the choice is
- In other words, LLMs have learned how to use __natural language__
- Foundation models can combine input/output text with other modalities (e.g. images, audio, video)
    * e.g. accepting text + image as input, and producing text + image as output, or any combination of these modalities
- This makes them very good at dealing with __unstructured__ data, either in input or output

---

{{< slide id="tokens" >}}

## About Tokens

- LLMs do not process _characters_ nor _words_, but __tokens__: chunks of text, as defined by the model's [tokenizer](https://huggingface.co/learn/llm-course/chapter2/4)
    + you may think that __token $\approx$ word__, but this actually depends on the specific tokenization algorithm

{{< image src="./tokenization.svg" max-h="45vh" alt="Example of how a sentence is split into tokens" >}}

- Tokens are the __unit of measure__ for LLMs:
    + the _context window_ is the maximum number of tokens a model can process in a single request (cf. [context management](../prompting/#/context-management))
    + the _cost_ of using LLMs as services is commonly _per token_ (cf. [Open Router](../llmaas/#/open-router))

---

## Language and Reasoning

- __Natural language__ helps people _communicate_

- It can be used to express _complex_ or _abstract_ concepts

- It can be used to _reason_ about _problems_ and _solutions_
    - however it admits __imprecisions__, due to _ambiguity_, variable interpretations, subjectivity, etc.



> Natural language allows LLMs to use __intuition__ in _reasoning_, like humans do
> <br> (thus __making mistakes__ like humans do)
- $\implies$ LLMs can be very confident in themselves, while saying _incorrect_, _imprecise_, or _made-up_ things
    + a.k.a. __hallucinations__

- better would be to combine LLMs with __symbolic__ AI tools, to get the best of both worlds

---

{{< slide id="dual-system" >}}

## Analogy with Dual-System theory

{{< image src="./dual-system.svg" width="100%" max-h="90vh" alt="Dual-system theory concept">}}

(cf. [Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow))

---

{{% section %}}

## GenAI with an _as-a-Service_ consumption model

{{< image src="./llm-concept.svg" width="100%" max-h="70vh" alt="'As-a-Service' consumption model for foundation models" >}}

---

## GenAI with an _as-a-Service_ consumption model

- __Cost__ models:
    + __subscription-based__: you pay a fixed monthly/annual _fee_ to access the service
        * it often still includes _usage_ limits
    + __usage-based__: you pay _in proportion_ to the actual use of the service

- __Consumption__ is measured based on the _computational effort_ required to serve the request:
    + processed _tokens_ (for text)
    + number of _requests_ (often also subject to __rate limits__, e.g. max requests per minute or day)
    + _size_ of the processed data (for images, audio, video)
    + _complexity_ of the specific _model_ used to serve the request

- __Generation__ should be considered a _stochastic_ process by construction

{{% fragment %}}
> - The __quality__ of the service is subject to randomness and _fluctuations_ due to:
>    + service _load_
>    + model choice, and its related _updates_
>    + service _limits_ possibly reached in the current _time window_
>    + chance
{{% /fragment %}}

{{% /section %}}

---

{{% section %}}

## GenAI _learning_ cycle

{{< image src="./dataflow.svg" width="100%" max-h="70vh" alt="GenAI learning cycle" >}}

---

## GenAI _learning_ cycle — __Consequences__ (pt. 1)

- __Sampling__ __bias__: GenAI knows _only_ what it has been _trained_ on + the pious hope that it learns to _generalize_

- Learning uses data taken __from the Web__ + possible provider-owned __company data__
    + there is documented use of previous users' _interactions_ as _feedback_ for subsequent training

{{% fragment %}}
##

> - __Niche__ information may <u>not</u> be learned correctly (or at all)
> - It is essential to __avoid sharing__ _sensitive_, _confidential_, or _copyrighted_ information
{{% /fragment %}}

---

## GenAI _learning_ cycle — __Consequences__ (pt. 2)

- Learning cycles are extremely __expensive__ in terms of _money_ and _computational resources_...

- ... performed __periodically__ (weeks? months?) to improve the _quality_ of the service
    + the _as-a-Service_ consumption model gives the user transparent access to the _updated_ service


{{% fragment %}}
##

> - __Recent__ information may <u>not</u> have been _learned_ yet
> - There is a risk of receiving __outdated__ or _incomplete_ answers from GenAI
> - GenAI gives the _impression_ of learning __during the conversation__, but its _weights_ are only updated _offline_
>    + within a conversation, it just re-reads the _whole history_ at each turn (cf. [stateless APIs](../llmaas/#/chat-completion-concept))
>    + "_memory_" features of chat apps store notes about the user, and put them back into the _context_ of later conversations
{{% /fragment %}}

---

## Some technological solutions let you _choose_ (pt. 1)

{{< image src="./logo-chatgpt.svg" height="2em" >}}
<br/>
{{< image src="./chatgpt-settings/no-learn-1.png" width="100%" max-h="50vh" >}}

---

## Some technological solutions let you _choose_ (pt. 2)

{{< image src="./logo-chatgpt.svg" height="2em" >}}
<br/>
{{< image src="./chatgpt-settings/no-learn-2.png" width="100%" max-h="50vh" >}}

---

## Some technological solutions let you _choose_ (pt. 3)

{{< image src="./logo-chatgpt.svg" height="2em" >}}
<br/>
{{< image src="./chatgpt-settings/no-learn-3.png" width="100%" max-h="50vh" >}}

---

## Some technological solutions let you _choose_ (pt. 4)

{{< image src="./logo-chatgpt.svg" height="2em" >}}
<br/>
{{< image src="./chatgpt-settings/no-learn-4.png" width="100%"  max-h="50vh" >}}

{{% /section %}}

---

{{< slide id="interfaces" >}}

# Main __technological__ solutions

## Categorized by type of __interface__

- _Conversational_: e.g. [ChatGPT](https://chatgpt.com/), [Claude](https://claude.ai/login?returnTo=%2F%3F), [Scite](https://scite.ai)
- _Auto-completion_: e.g. [GitHub Copilot](https://github.com/features/copilot)
- _Programmatic_: e.g. [OpenAI Platform](https://openai.com/api/), [Hugging Face](https://huggingface.co/)
- _In-App_: e.g. [Microsoft 365 Copilot](https://www.microsoft.com/en-us/microsoft-365/copilot)
- _Audio/video editing_: e.g. [Suno](https://suno.com/), [Runway](https://runwayml.com/)
- _Inspection of generated material_: e.g. [GPTZero](https://gptzero.me/), [ZeroGPT](https://www.zerogpt.com/)
    + {{% color "red" %}}unreliable{{% /color %}}: OpenAI itself [withdrew](https://techcrunch.com/2023/07/25/openai-scuttles-ai-written-text-detector-over-low-rate-of-accuracy/) its AI-text classifier, due to its low accuracy
- _Agentic_: e.g. [Claude Code](https://code.claude.com/docs), [Codex](https://github.com/openai/codex), [OpenClaw](https://openclaw.ai)

{{% color "red" %}}Non-exhaustive list!{{% /color %}}

---

## __Conversational__ interface

{{% multicol %}}
{{% col %}}
{{< image src="./logo-chatgpt.svg" height="2em" >}}
{{< image src="./interface-conversational.png" width="100%" link="https://chatgpt.com/share/6798dd04-8a98-8008-a751-bc374318bd9e" >}}
{{% /col %}}
{{% col %}}
<br>

- _Textual_ interaction that mimics a (__chat__) _exchange_
    + the user asks, the AI responds _reactively_
- The interface allows entering a __prompt__
    + optionally including _attachments_ (e.g. images, documents)
- Responses are __contextual__
    + i.e., the conversation _history_ affects _future_ responses
- The response contains __text__ (often _formatted_)
    + optionally: _images_, URLs, code

{{% fragment %}}

### Sometimes...

- ... before responding, the AI performs a __Web__ _search_
- important for obtaining _up-to-date_ results

{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

---

## __Auto-completion__ interface

{{% multicol %}}
{{% col %}}
{{< image src="./logo-copilot.svg" height="2em" >}}
{{< image src="./interface-autocompletion.gif" width="100%" >}}
{{% /col %}}
{{% col %}}
<br>

- The AI _suggests_ a __completion__ for the entered text
    + e.g., code, text, URLs
- The user __accepts__ (even partially) or _ignores_ the suggestion
- Used especially for __programming__ _code_

{{% fragment %}}

### Attention...
- ... __subscription__ pricing model (see [here](https://github.com/features/copilot/plans))
- ... potential __leaks__ of _sensitive_ information
- ... non-negligible __lock-in__ risk

{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

---

## __Programmatic__ interface

{{% multicol %}}
{{% col class="col-6" %}}
{{< image src="./logo-openai.svg" height="2em" alt="OpenAI logo" >}}
```python
from openai import OpenAI

client = OpenAI()  # reads the API key from the OPENAI_API_KEY env variable

stream = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        dict(role="user", content="European countries, one by line")
    ],
    stream=True,  # receive the response token by token
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

Output (excerpt, may vary):
```plaintext
Albania
Andorra
Austria
Belarus
Belgium
...
```
{{% /col %}}
{{% col %}}

- __Programming language__ interacting with AI
    + e.g., _Python_, JavaScript

- The interaction remains of the _request-response_ type
    + the __program__ sends a _request_, the AI _responds_

{{% fragment %}}

### Enables

- __Parametric__ prompts, responses processed _automatically_
    + e.g. `list of LOCALITIES in AREA, one by line`
        + where `LOCALITIES` $\in$ {`cities`, `regions`, `states`}
        + and `AREA` $\in$ {`Europe`, `Asia`, `Africa`, `America`, `Oceania`}
        + results _sorted alphabetically_

- Writing __software__ that uses AI as a __service__
    + useful in both _industry_ and _research_

{{% /fragment %}}

{{% fragment %}}

### Attention...
- ... __usage-based__ pricing model (see [here](https://openai.com/api/pricing/))
    + proportional to the number of processed _tokens_
    + prices vary _by model_

{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

---

## __In-app__ interface

{{% multicol %}}
{{% col %}}
{{< image src="./logo-copilot-office.svg" height="2em" >}}
{{< image src="./interface-inapp.gif" width="100%" >}}
{{% /col %}}
{{% col %}}
<br>

- GenAI integrated into __desktop__ or _web_ __applications__
    + e.g., _Microsoft Office_ (Word, Excel, Outlook)

- support for an internal __conversational__ interface
    + a conversation that is intrinsically _contextualized_

- AI __automates__ _complex operations_ (within the app)
    + e.g., draft _writing_
    + e.g., _generation_ of formulas, charts

{{% fragment %}}

### Attention...
- ... __subscription__ pricing model (see [here](https://www.microsoft.com/en-us/microsoft-365/copilot#plans))
- ... potential __leaks__ of _sensitive_ information
- ... non-negligible __lock-in__ risk

{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

---

## Interface for __editing__ audio/video content (e.g. _music_)

{{% multicol %}}
{{% col %}}
{{< image src="./logo-suno.svg" height="2em" >}}
{{< image src="./generate-song-1.png" width="100%" >}}
{{% /col %}}
{{% col %}}
- __One-shot__ interaction to generate content
    + _input_: textual description of the content
    + _output_: content

- The interface then allows
    + _playback_ of the content
    + __editing__ of the content
        + e.g., _cutting_ parts, _changing_ key

{{% fragment %}}

### Example

- ["Song of Bacchus" (Lorenzo de' Medici, 1490)](https://it.wikipedia.org/wiki/Il_trionfo_di_Bacco_e_Arianna_(poesia)), rock
    + <https://suno.com/song/cce33ee7-a581-47ae-b9d1-806902e88e47>

{{% /fragment %}}
{{% /col %}}
{{% /multicol %}}

---

## __Agentic__ interface

{{% multicol %}}
{{% col %}}
{{< image src="./claude-code.png" width="100%" alt="A Claude Code session in a terminal: the agent reads files and runs commands to answer the user's request" >}}
{{% /col %}}
{{% col %}}
<br>

- The user assigns a __goal__ (a _task_), not just a question
- The AI works in a __loop__: _plan_ → _act_ → _observe_ → repeat
    + _reads_ files, _runs_ commands, _edits_ code, _searches_ the Web
- It operates within a __workspace__
    + e.g. a repository, the file system, a shell (_locally_ or in a _cloud sandbox_)
- The user __supervises__
    + _approves_ actions, _interrupts_, _reviews_ the changes
- Many front-ends: _CLI_, _IDE_, _desktop_, _web_, even _messaging apps_

{{% fragment %}}

### Attention...
- ... __side effects__: it acts on _your_ machine (e.g. deleted files, leaked secrets)
- ... __prompt injection__ via the files and Web pages it reads
- ... heavy __token consumption__ (subscription or usage-based pricing)
- ... __review__ burden and risk of _over-reliance_
- ... non-negligible __lock-in__ risk

{{% /fragment %}}

{{% /col %}}
{{% /multicol %}}

---

## __Agentic__ interfaces: the landscape

| | Vendor | Front-ends | Models | License |
|---|---|---|---|---|
| [Claude Code](https://code.claude.com/docs) | Anthropic | CLI, IDE, desktop, web | Claude | proprietary |
| [Codex](https://github.com/openai/codex) | OpenAI | CLI, IDE, desktop, web | GPT | Apache-2.0 (CLI) |
| [OpenClaw](https://github.com/openclaw/openclaw) | OpenClaw Foundation | self-hosted, messaging apps (WhatsApp, Telegram, Slack, ...) | any (hosted or local) | MIT |
| [Cursor](https://cursor.com), [Copilot](https://github.com/features/copilot) (agent mode) | Anysphere, GitHub | IDE | various | proprietary |

{{% fragment %}}

### Common anatomy

- An LLM + __tools__ (shell, files, Web) + a __loop__ $\Rightarrow$ an _agent_
- Project-specific instructions in Markdown files (e.g. `CLAUDE.md`, [`AGENTS.md`](https://agents.md))
- Extensible via [__MCP__](https://modelcontextprotocol.io) servers, __skills__, and __hooks__
- __Permission__ modes: from "ask before every action" to "fully autonomous"

{{% /fragment %}}

{{% fragment %}}

These are themselves __LLM-based agentic software__: the kind of system this module teaches you to _build_

{{% /fragment %}}

---

{{% section %}}

{{< slide id="genai-uses" >}}

## Customers buy __automation__, not agents

> Why do people care about software in the first place? (cf. [Introduction to Software Engineering](https://unibo-dtm-se.github.io/course-slides/se-intro/))

- Most people do _not_ care about algorithms, software, or agents _per se_...
- ... they care about __automating__ the _solutions_ to their _problems_
    + algorithms, software, and now _agents_ are just __means__ to that end

- _Classic_ software automates problems which are _repetitive_ and _structured_ enough to be __coded__
- GenAI __widens__ the set of _automatable_ problems
    + to problems which are _linguistic_, _ill-defined_, or about _unstructured_ data
    + i.e. problems which are __hard to code__ explicitly

{{% fragment %}}

### Corollary

- _Autonomy_ is a __cost__ (risks, testing, governance), not a goal
- Aim for the __least autonomy__ that gets the job done (cf. [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))

{{% /fragment %}}

---

## Three ways engineers exploit GenAI

{{% multicol %}}
{{% col class="col-7" %}}
{{< image src="./genai-uses-venn.svg" width="100%" max-h="75vh" alt="Venn diagram: (1) coding assistants and co-pilots, (2) automating hard-to-code tasks, (3) agents in products; all intersections are possible" >}}
{{% /col %}}
{{% col %}}
1. As __coding assistants__ and _co-pilots_
    + GenAI helps engineers _build_ the software
2. To __automate__ activities which would otherwise be _hard to code_
    + GenAI is a _step_ in a flow decided by the developers
3. To create __agents__ for software _products_
    + GenAI _decides_ (part of) the flow, increasing the product's _autonomy_

{{% fragment %}}

- (1) is about the __process__ (_dev-time_): the product may contain no AI at all
- (2) and (3) are about the __product__ (_run-time_)
    + they are _ends_ of a __spectrum__: _who controls the flow_?
    + the _developer's code_ (__workflow__) vs. the _LLM_ (__agent__)

{{% /fragment %}}

{{% fragment %}}

{{% color "red" %}}Not mutually exclusive!{{% /color %}}

{{% /fragment %}}
{{% /col %}}
{{% /multicol %}}

---

## Each dimension on its own

- (1) only: __coding__ an _ordinary_ Web application (no AI inside) with the help of _Claude Code_
    + cf. [agentic interfaces](#/interfaces)
    + GenAI _speeds up_ development, yet the final product is _classic_ software

- (2) only: a script which __extracts__ _structured_ data from _recommendation letters_
    + the steps are _fixed_ in code (read letter $\rightarrow$ prompt LLM $\rightarrow$ validate output $\rightarrow$ store)
    + the LLM is _one step_ among many: it does _not_ decide what to do next

- (3) only: a customer-support __chatbot__ which _decides_ which tools to call (e.g. look up orders, open tickets)
    + the LLM _chooses_ the next action, based on the conversation
    + the product gains _autonomy_, and so does its _risk profile_

---

## How the dimensions __combine__

| Combination | Example |
|---|---|
| (1) + (2) | the letter-extraction script, written with a _coding assistant_ |
| (2) + (3) | an agent whose _tools_ are themselves LLM-based _workflows_ (e.g. the [tender example](#/genai-workflow)) |
| (1) + (3) | an agentic _product_ built with a _coding agent_ |
| (1) + (2) + (3) | an assistant for a PhD admission committee: _workflows_ to extract data from candidates' documents, an _agent_ to answer the committee's questions, all _coded_ with a coding agent |

{{% fragment %}}

### Twist

- One team's (1) is another team's (3)
    + _Claude Code_ is a __tool__ for its users (1)...
    + ... and an agentic __product__ for Anthropic (3)

{{% /fragment %}}

---

## From __language__ to __action__

- An LLM produces __text__, not _action_
    + action requires _software_ which _maps_ text onto _operations_
    + e.g. `Book the train to Lisbon` is just text...
    + ... until software maps it onto _search_, _booking_, _payment_, and _confirmation_ steps

- Are LLMs _agents_? Not really, not fully, not __by themselves__
    + they do not _perceive_ nor _act_ on environments directly
    + they do not _persistently_ manage _goals_ and _state_

- In both (2) and (3), the "agent" is mostly the __surrounding software__
    + _agent_ $\approx$ _controller_ + _LLM_ + _tools_ + _memory_ + _policies_

{{% fragment %}}

### _Intelligence_ vs. _autonomy_ vs. _agency_ are __separable__ dimensions (cf. [Floridi, 2025](https://doi.org/10.1007/s13347-025-00858-9))

- What can the system __do__? (_agency_)
- Who __controls__ _when_ and _why_ it does it? (_autonomy_)
- What __state__ does it actually _change_?

{{% /fragment %}}

---

## Language is a __weak substrate__ for agency

- Natural language is _expressive_ and _flexible_...
    + useful for _vague_ goals, _exceptions_, _preferences_, and _explanations_
- ... but also _ambiguous_ and _underspecified_
    + _fluent_ text may be plausible but __false__
    + _confident_ text may be __non-executable__
    + e.g. `get approval, then submit` hides _who_ approves, _how_ approval is checked, and _what_ submission changes

{{% fragment %}}

### Hence: LLMs __propose__, software __verifies__

- Treat LLM outputs as __candidate__ artefacts (plans, classifications, explanations)...
- ... to be _checked_ by external components: _validators_, _tests_, _policy checkers_, _humans_
    + cf. the _LLM-Modulo_ framework ([Kambhampati et al., 2024](https://proceedings.mlr.press/v235/kambhampati24a.html))
    + recall the [dual-system](#/dual-system) analogy: fast _intuition_ + slow _checking_

{{% /fragment %}}

{{% /section %}}

---

## What can GenAI do __inside__ software? (dimensions 2–3)

Combine _prompts_, _tools_, _vector stores_, and _agents_ to constrain and govern the behavior of __pre-trained__ (_foundation_) models, in order to:
- __generate__ contents (text, images, code, etc.) for a specific purpose
    * e.g. bring unstructured data into a particular format
    * e.g. produce summaries, reports, highlights
- __interpret__ unstructured data and _grasp information_ from it
    * e.g. extract entities, relations, sentiments
    * e.g. answer questions about a document
- __automate__ data-processing tasks which are _hard to code_ explicitly
    * e.g. the task is ill-defined (`write an evaluation paragraph for each student's work`)
    * e.g. the task requires mining information from unstructured data (`find the parties involved in this contract`)
    * e.g. the task is complex yet too narrow to allow for general purpose coding (`plan a vacation itinerary based on user preferences`)
- __interact__ with users via _natural language_
    * e.g. chatbots, virtual assistants

---

## Let's explain the nomenclature

- __<u>Pre-trained</u> foundation models__ (PFM): large neural-networks trained on massive datasets to learn general skills (e.g. 'understanding' and generating text, images, code), most commonly accessed _as-a-Service_ via API, as provided by third-party companies
    * e.g. GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama (Meta), Mistral, Qwen (Alibaba), etc.
    * some are _proprietary_ (usable only via the provider's API), others are _open-weight_ (downloadable and runnable locally, cf. [on-premise deployment](../llmaas/#/ollama) and [open models](../governance/#/open-models))

- __Prompts__: carefully _crafted textual inputs_ that guide some PFM to produce _desired outputs_
    * prompt __templates__ are prompts with _named placeholders_ to be filled with specific data at runtime
        + e.g. `Write a summary of the following article: {article_text}`

- __Tools__: external _software components_ (e.g. WebAPIs, databases, search engines) that PFMs can _ask_ to invoke (the invocation is performed by the surrounding software), to perform specific tasks or retrieve information
    * e.g. a calculator API, a weather API, a database query interface

- __Vector stores__: specialized databases that store and retrieve _high-dimensional vectors_ (embeddings) for the sake of _information retrieval_ via _similarity search_
    * e.g. to support _retrieval-augmented generation_ (RAG)

- __Agents__: software systems that _orchestrate_ the interaction between PFMs and tools, enabling dynamic decision-making and task execution based on the context and user input
    * e.g. a chatbot that uses a PFM for conversation and invokes a weather API when asked about the weather
    * e.g. an assistant that uses a PFM to understand user requests and a database to fetch relevant information

---

{{% section %}}

## What does an AI-powered application include?

(i.e. a product exploiting GenAI as per dimensions (2) and (3))

1. FM are commonly <u>not</u> produced in-house, but rather _accessed_ via APIs... yet the choice of __what model(s) to use__ is crucial
    * must be available, configured, and most commonly imply _costs_ (per call, per token, etc.)
    * imply the choice of some __client library__, and the related _programmatic interface_
        + e.g. [OpenAI Python SDK](https://github.com/openai/openai-python), [Hugging Face Transformers](https://huggingface.co/docs/transformers/index), etc.

2. A set of __prompt templates__ (text files, or code snippets) that are known to work well for the tasks at hand
    * commonly assessed via semi-automatic _evaluations_ on a _validation set_ of inputs

3. A set of __tools__ that PFMs can _ask_ the application to invoke
    * these may be plain _functions_ in the application's code...
    * ... or _software modules_ exposing tools via the [MCP protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (__MCP servers__), somewhat similar to ordinary Web services

4. A set of __agents__, implementing the logic to orchestrate the interaction between PFMs and tools
    * these are _software modules_, commonly implemented via libraries such as [LangChain](https://docs.langchain.com/oss/python/langchain/overview) or [LlamaIndex](https://developers.llamaindex.ai/python/framework/)

5. A set of __vector stores__ (if needed), populated with relevant data, and accessible by the agents
    * these are _software modules_, somewhat similar to ordinary DBMS, offering CRUD operations on data chunks _indexed by_ their _embeddings_

6. LLM-as-a-Judge __evaluations__ to assess the quality of the outputs produced by the system, and to guide the improvement of prompts, tools, and agents
    * e.g. by comparing the output to a _reference_ answer, and by assigning a score based on some _criterion_

---

## Concept: Prompt Templates

| Technique | Prompt template | Description |
|---|---|---|
| Role playing | `You are an expert in {field} known for {key adjective}. Help me {task}.` | telling the AI to act as a famous expert or celebrity |
| Style unbundling | `Describe the key elements of {expert}'s style/skill in bullet points.` <br> `Do {task} in the following style: {style}.` | describe what you like about a style, rather than copying it directly |
| Emotion prompting | `Help me {task}. Please make sure {attribute}. This task is very important for my career.` | use emotional pressure and persuasion with the AI |
| Few-shot learning | `Here are some examples of {task}. Generate a {task} for {new context}.` | add examples of the completed task to the prompt |
| Synthetic bootstrap | `Generate ten examples of {examples} for {context}. Here are the inputs: {inputs}.` <br> `Generate {task} using {examples}.` | use AI to generate good examples of the completed task |

(source: [Lenny's Newsletter](https://www.lennysnewsletter.com/))

- `{placeholders}` are filled with _actual data_ at runtime

---

## Concept: Agents Calling External Tools

{{< image src="./tools.svg" width="100%" max-h="85vh" alt="Sequence diagram: an agent discovers tools via MCP, the LLM requests a tool call, the agent invokes it via MCP, and the result is fed back to the LLM" >}}

---

## Concept: Model-Context Protocol (MCP)

{{< image src="./mcp.svg" width="100%" max-h="70vh" alt="Model-Context Protocol (MCP) concept">}}

- MCP $\approx$ _standard_ protocol for LLM-based applications to _discover_ and _call_ __external tools__ (cf. [specification](https://modelcontextprotocol.io/specification))
- Allows for _decoupling_ between the agent's logic and the implementation of the tools, thus enabling modularity and interoperability
- Each MCP __server__ exposes its _own_ tools (names, descriptions, input schemas), plus possibly _resources_ (data) and _prompts_ (templates)
- The _host_ application (e.g. Claude Code, or your agent) runs one MCP __client__ per server it connects to
    + optionally, a __gateway__ may _aggregate_ several servers behind a single endpoint

---

## Concept: Retrieval-Augmented Generation (RAG)

{{< image src="./rag.svg" width="100%" max-h="80vh" alt="RAG: indexing pipeline (chunking, embedding, vector store) and retrieval-and-generation pipeline (embedding the question, retrieving chunks, enriched prompt, LLM answer)" >}}

---

## Concept: LLM-as-a-Judge

{{< image src="./llm-as-a-judge.svg" width="100%" max-h="70vh" alt="LLM-as-a-Judge concept">}}

- Exploiting an LLM to _evaluate_ the quality of some other LLM's output...
- ... based on some _informal_ __criterion__ (e.g. _relevance_, _accuracy_, _completeness_, etc.)
- ... by comparing the output to some _reference_ (e.g. a human-written checklist)

(more on this in the [validating](../validating/#/llm-as-a-judge) lecture)

{{% /section %}}

---

{{% section %}}

{{< slide id="genai-workflow" >}}

## The GenAI workflow

(The workflow of engineering products as per dimensions (2) and (3).
Similar to the ML workflow in the sense that the goal is to process data, but different in many details: e.g. training is _optional_, and commonly _not_ performed in-house, as pre-trained models are exploited)

{{< image src="./genai-workflow.svg" width="100%" max-h="40vh" alt="GenAI project lifecycle: scope, select, adapt and align model, application integration" >}}

* there could be __many iterations__ (e.g. for PFM selection, and prompt tuning)
* the whole workflow may be __re-started__ upon _data changes_, or _task changes_, or new _PFM availability_
* the __interplay__ between prompts, models, tasks, and data may need to be _monitored_ and _adjusted_ continuously
* the __data-flow__ between components (agents, PFM, tools, vector stores) may need to be _tracked_ for the sake of _debugging_ and _monitoring_

---

## Peculiar activities in a typical GenAI workflow

1. __Foundation model selection__: choose the most suitable pre-trained model(s) based on task requirements, performance, cost, data protection, and availability
    * implies trying out prompts (even manually) on different models

2. __Prompt engineering__: design, test, and refine prompt templates to elicit the desired responses
    * implies engineering variables, lengths, formats, contents, etc

3. __Evaluations__: establish assertions and metrics to assess PFM responses to prompts (attained by instantiating templates over actual data)
    * somewhat similar to _unit tests_ in ordinary software
    * important when automatic, as they allow quick evaluations on prompt/model combinations

4. __Tracking__ the _data-flow_ between components (agents, PFM, tools, vector stores) to monitor _costs_, _latency_, and to _debug_ unexpected behaviors
    * also useful for the sake of _auditing_ and _governance_
    * commonly performed via _logging_ and _tracing_ tools, e.g. [LangSmith](https://smith.langchain.com/), or [MLflow](https://mlflow.org/)

---

## Example of GenAI workflow (pt. 1)

> Support public officers in managing tenders through a GenAI assistant that understands and compares procurement decisions transparently.

__Scope__

1. __Problem Framing__:
    - _Content Generation_: draft and justify _comparisons_ among suppliers' offers vs. technical specs
    - _Interpretation_: understand regulatory documents and technical language
    - _Automation_: score offers against _check-lists_ derived from the technical specs
    - _Interaction_: enable officers to query and validate results through natural language
    - i.e. a _workflow_ (dimension 2) for scoring, plus an _agent_ (dimension 3) for the officers' questions

2. __Data Collection__: past tenders' technical specifications and acts; regulatory documents; previous evaluations (with the officers' scores)

3. __Data Preparation__:
    - devise useful data schema & extract relevant data from documents
    - anonymize sensitive info (personal data; supplier identities, to reduce bias)
    - segment documents and index by topic (law, SLA, price table, etc.)

__Select__

4. __Foundation Model Selection__: multi-lingual? specialized in legal/technical text? cost constraints? support for tools? where does it run (data protection)?
    * try out candidate prompts on candidate models

---

## Example of GenAI workflow (pt. 2)

__Adapt and align__

5. __Vector stores__: embeddings for tender documents & specs, legal texts & guidelines, previous evaluations, templates
    * choose embedding model and chunking strategy, populate the store, engineer retrieval strategies

6. __Prompt Engineering__: templates for check-list extraction, justification, and Q&A
    * role-based system prompts (`You are a procurement evaluator…`), placeholders for retrieved chunks, iterate on manual tests

7. __Evaluations__: past tenders (with the officers' scores) as validation set
    * exact checks on extracted check-lists and scores; [LLM-as-a-judge](../validating/#/llm-as-a-judge) on justifications (e.g. is every claim backed by a cited document?)
    * re-run at every change of prompts or models

__Application integration__

8. __Tools__: regulation lookup API, tender database query API, report generation out of document templates
    * scores are computed by _deterministic_ code out of the (validated) check-lists: the LLM _proposes_, software _verifies_

9. __Workflow__ + __Agent__:
    * _workflow_: extract check-lists $\rightarrow$ validate $\rightarrow$ score $\rightarrow$ generate comparison report
    * _agent_: answers officers' questions, orchestrating RAG and tool invocations

10. __Tracking__ & __Oversight__:
    * log prompts, retrieved chunks, tool calls, and scores, for traceability and auditing
    * the system _proposes_, the officer _decides_ (and signs off); comply with GDPR and the AI Act (cf. [governance](../governance/#/regulation))

{{% /section %}}

---

{{% import path="reusable/back.md" %}}

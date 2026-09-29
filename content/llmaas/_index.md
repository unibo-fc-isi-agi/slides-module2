+++

title = "[ISE] LLM-as-a-Service"
description = "Background about using LLMs via Service Providers"
outputs = ["Reveal"]

+++

# Using LLMs via Service Providers

{{% import path="reusable/footer.md" %}}

---

## Outline

### Key engineering aspects of LLM-as-a-Service

0. **On-premise** vs. **On-cloud** deployment
    - On-premise: the model is hosted and run on the _user's own infrastructure_, commonly via _containerized solutions_ (e.g. [Ollama](https://ollama.com/), [Docker's Model Runner](https://www.docker.com/products/model-runner/), etc.)
        + implies ad-hoc _hardware requirements_ (e.g. Nvidia GPUs, Apple Silicon) and technical expertise for setup and maintenance
        + the service provider is commonly the company providing the _containerized solution_, and making _models_ available for _download_ and use
        + most commonly, containerized solutions provide the same _API_ as the on-cloud service, to facilitate migration between the two deployment options
    - On-cloud: the model is hosted and run on the _service provider's infrastructure_, and accessed via _API calls_
        + implies _<u>no</u> hardware requirements_ for the user, but a _cost per usage_ (e.g. per token, per request, etc.)

1. **Service Provider**: several exist, with different offerings in terms of models, pricing, and features
    - e.g. [OpenAI](https://openai.com/), [Anthropic](https://www.anthropic.com/), [Google](https://cloud.google.com/vertex-ai), [Microsoft](https://azure.microsoft.com/en-us/services/cognitive-services/), [Hugging Face](https://huggingface.co/inference-api), or aggregators like [OpenRouter](https://openrouter.ai/)
    - the choice of the service provider can depend on several factors, including:
        + the availability of _specific models_ (e.g. GPT-4, Claude, Gemini, etc.)
        + the _pricing model_ and cost structure
        + the _features_ and _capabilities_ offered (e.g. fine-tuning, custom models, MCP support, etc.)

1. **Web API Compatibility**: early providers (e.g. OpenAI, Google) invented _their own APIs_, similar in the spirit, but _different in syntax_
    - some later providers attempted to adopt the _same API_ as the _market leader_ (OpenAI), to facilitate adoption
        * others (e.g. HuggingFace) come with their own API, which may be more or less compatible with OpenAI's API
    - API compatibility is key for _provider interchangeability_, hence allowing migration and __avoiding vendor lock-in__

1. **Client Libraries**, in target _programming languages_ wrap Web API clients and make it easier to use _LLMs programmaticatically_
    - here you may care about which programming languages (e.g. Python, JS, Java, etc.) are supported by some given client library...
        * most commonly, the same provider implements the same meta-model onto different target programming languages (e.g. OpenAI' client is available in Python, JS, Java, etc.)
    - there exist also _third-party_ client libraries, which may support multiple Web APIs, and therefore multiple providers (e.g. [LangChain](https://python.langchain.com/en/latest/))

---

{{% section %}}

## About Ollama (cf. <https://ollama.com/>)

- Ollama is a company that provides a _containerized_ solution for _hosting_ and _running_ LLMs __on-premise__, with a focus on ease of use and accessibility

- It offers a [model zoo](https://ollama.com/models) with several pre-trained models available for _download_ and use
    + plus a _native API_ that is _partially compatible_ with OpenAI's API, to facilitate migration between on-premise and on-cloud deployments

- Ollama's solutions can be used on various __hardware__ & __OS configurations__, including _Nvidia_ GPUs and _Apple Silicon_ as well as _Linux_, _MacOS_, and _Windows_

- Ollama's API supports both a native __CLI conversational interface__ and a __Web API__ for programmatic access, making it versatile for different use cases and user preferences

- Ollama may also be used an [on-cloud service](https://ollama.com/pricing), but here we will focus on the on-premise deployment option alone
    + three levels of premiumships (0€/month, 20€/month, 100€/month) with widening rate limitations

---

## On-premise Example with Ollama pt. 1

0. Ensure you have the __required hardware__ (e.g. Nvidia GPU, Apple Silicon, etc.)
    + details and configuration caveats: <https://docs.ollama.com/gpu>

1. __Install__ Ollama on your machine:

    ```bash
    brew install ollama # For macOS (Apple Silicon)
    curl -fsSL https://ollama.com/install.sh | sh # For Linux
    irm https://ollama.com/install.ps1 | iex # For Windows (PowerShell)
    ```

2. Activate the Ollama __service__ in some shell (alternatively, configure a _deamon_ to run it in background):

    ```bash
    ollama serve
    ```

---

## On-premise Example with Ollama pt. 2

3. Have a look to Ollama's __model zoo__ on <https://ollama.com/models>, and __select__ some model you like among the many variants available
    * notice naming convention: `model:variant`, most commonly the variant denotes the size of the model

    {{< image src="ollama-models.png" alt="Ollama's Model Zoo" max-h="70vh" >}}
    {{< image src="ollama-models-gemma4.png" alt="Available variants for a Model on Ollama's Model Zoo" max-h="70vh" >}}

---

## On-premise Example with Ollama pt. 3

4. Pick one model, e.g. `gemma4:e2b`, and __pull__ it:

    ```bash
    ollama pull gemma4:e2b
    ```

5. You may use Ollama's native __CLI conversational interface__ to try the model out:

    ```bash
    ollama chat gemma4:e2b
    ```

    example of conversation (notice that the model is also showing its _thinking process_):

    ```text
    >>> ciao!
    Thinking...
    Thinking Process:

    1.  **Analyze the input:** The input is "ciao!". This is an informal Italian greeting, meaning "hello!".
    2.  **Determine the appropriate response:** Since the user initiated a friendly greeting, the response
    should also be a greeting, ideally reciprocating the language or offering a friendly follow-up.
    3.  **Formulate the response (in Italian):** The simplest and most common reply is "ciao" (hello/hi) or
    a slightly expanded version.
    4.  **Add a standard conversational element (optional but good practice):** Asking how the user is doing
    is polite. ("Come stai?" / "Come va?")
    5.  **Final selection:** A friendly, standard reply.

    *Self-Correction/Refinement:* Keep it warm and open-ended.

    *Output Generation:* Ciao! Come stai? (Hello! How are you?)
    ...done thinking.

    Ciao! Come stai? 😊
    ```

---

## On-premise Example with Ollama pt. 3

6. Should you ever want to use the model _programmatically_, you can use Ollama's __API__, which is _partially_ compatible with OpenAI's API
    * e.g. it supports the same `/v1/chat/completions` endpoint, but not all the features of OpenAI's API, e.g. fine-tuning, custom models, etc.
    * in the client program, recall to set the __API base URL__ to point to your local Ollama service (by default: <http://localhost:11434>)
    * to prove that the API is working, you can send a test request via `curl`:

        ```bash
        curl -X POST "http://localhost:11434/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -d '{
                "model": "gemma4:e2b",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is the capital of France?"}
                ]
            }'
        ```

        result (converted in YAML for the sake of readability):

        ```yaml
        id: chatcmpl-85
        object: chat.completion
        created: 1779435598
        model: gemma4:e2b
        system_fingerprint: fp_ollama
        choices:
        - index: 0
            message:
            role: assistant
            content: The capital of France is **Paris**.
            reasoning: |-
                Thinking Process:

                1.  **Analyze the Request:** The user is asking a factual question: "What is the capital of France?"
                2.  **Identify the Knowledge Needed:** I need to retrieve the capital city of France.
                3.  **Recall/Retrieve the Fact:** The capital of France is Paris.
                4.  **Formulate the Answer:** Provide a direct and accurate answer.
                5.  **Final Review:** The answer is correct and directly addresses the query. (Capital of France = Paris).
            finish_reason: stop
        usage:
        prompt_tokens: 29
        completion_tokens: 121
        total_tokens: 150
        ```

{{% /section %}}

---

{{% section %}}

## About Open Router (cf. <https://openrouter.ai/>), pt. 1

- Open Router (_OR_) is a company that provides an __on-cloud__ service for using _LLMs as services_, with a focus on _provider interchangeability_

- Its distinguishing feature is that it acts as an _aggregator_ of multiple service providers, allowing users to access a variety of models from different providers via a single API, and helping to avoid vendor lock-in
    + one can use OR for __free__, with _very limited rates_ (20 requests per minute, max 50 per day)
        * one may __buy credits__ to widen the limitations for free models (see <https://openrouter.ai/docs/api/reference/limits> for details), or to use _pay-per-use_ models

- Pretty rich [model zoo](https://openrouter.ai/models), exposing models from <u>many</u> different providers, most notably: OpenAI, Anthropic, Google, xAI, Mistral, etc.
    + notice that models come with __price-per-token__, commonly expressed a `$/1M tokens` (some times the prices is different for _input_ or _output_ tokens)
        * this is very common for on-cloud services, and it is the main reason why we need to be careful when experimenting with them, to avoid unexpected costs

    {{< image src="open-router-models.png" alt="Open Router's Model Zoo" max-h="40vh" >}}

---

## About Tokenization

You may think that __token $\approx$ word__, but this actually depends on the specific [tokenization algorithm](https://huggingface.co/docs/course/it/chapter2/4) (tokenizer) being used by a model

![](tokenization.png)

---

## About Open Router (cf. <https://openrouter.ai/>), pt. 2

- Models in OR's zoo are __named__ according to the following convention: `provider/model` followed by _optional_ `:tier`, where:
    + `provider` is the name of the service provider (e.g. `openai`, `qwen`, `google`, etc.)
    + `model` is the name of the model _variant_ as provided by the provider (e.g. `gpt-oss-120b`, `qwen3-coder`, `gemma-4-26b-a4b-it`, etc.)
    + `tier` is an optional suffix that denotes a specific variant of the model (most commonly `free` for free models)


- To allow for __dynamic routing__ of requests to different providers in a _transparent_ way, OR allows for the following meta-models:
    + `openrouter/auto` ([AutoRouter](https://openrouter.ai/openrouter/auto)): let OR decide which provider/model to use for each request, based on the request's content and the current availability of models
    + `provider/*` (e.g. `anthropic/*`, `google/*`, etc.): OR will serve each request with the best available model from the specified provider, according to the request's content and the current availability of models
    + in general, you can reason like with Unix globs, so for instance `openai/gpt*` will match any OpenAI model whose name starts with `gpt` (as currently provided by OR)
    + in the [routing settings](https://openrouter.ai/workspaces/default/routing) of your OR account, you can set up the __routing strategy__ OR should adopt:
        1. __"Price"__ (cost-first): OR will route requests to the currently _cheapest_ model that can serve them
        2. __"Latency"__: OR will route requests to the model that is _currently quicker_ to respond
        3. __"Throughput"__: OR will route requests to the one that has currently the best stats in terms of _throughput_ (requests per minute)
        4. __"Exacto"__ (quality-first): OR will route requests to the _best available_ model that can serve them (based on model's stats on tools usage)

- __Bring your own API key__ (BYOK): OR allows you to _link_ your account with your API keys from _other providers_ so that you can use OR's API to access models from those providers, and therefore be charged according to the prices of those providers instead of OR's prices
    + this is a great feature to avoid vendor lock-in, and to have more control over the costs and the models you want to use

> Dynamic routing and BYOK are _peculiar_ features of OR, for the rest it's an "ordinary" on-cloud provider

---

## On-cloud Example with Open Router (pt. 1)

1. __Sign up__ & _log in_ for an account on Open Router: <https://openrouter.ai>
    + easier to re-use your GitHub account

2. Optionally add __payment methods__ and _credits_ to your account in <https://openrouter.ai/settings/credits>
    + no credit needed for this lecture
    + recall to set _expense limitation_ to avoid unexpected costs, in case you decide to experiment with actual money

    {{< image src="open-router-credits.png" alt="Open Router's Credits Settings" max-h="40vh" >}}

---

## On-cloud Example with Open Router (pt. 2)

3. From time to time, keep an eye on the __activity dashboard__ of your account, to check the usage and the costs of your requests: <https://openrouter.ai/activity>

    {{< image src="open-router-activity.png" alt="Open Router's Activity Dashboard" max-h="40vh" >}}

---

## On-cloud Example with Open Router (pt. 3)

4. To use OR's models programmatically, you need to create an __API key__ first (to be stored securely, and not shared with anyone else)
    * (i.e. an _authentication token_ to let clients authenticate on your behalf)
    * you can do that for the _default workspace_ at <https://openrouter.ai/workspaces/default/keys>
        + __workspaces__ are OR-wise _administration domains_, inside which configurations rules (e.g. routing rules, cost limits, etc.) apply

    {{< image src="open-router-apikeys.png" alt="Open Router's API Keys Settings" max-h="40vh" >}}

    + an API key is a string of the form: `sk-or-XXXXXXXXXXXXXXXXXXXXXXXX`: it is sufficient to <u>consume your credit</u> and to make requests on your behalf

---

## On-cloud Example with Open Router (pt. 4)

5. You may test your API key with a simple `curl` request:

    ```bash
    curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_API_KEY" \
        -d '{"model": "openrouter/auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
    ```

    answer (converted in YAML for the sake of readability):

    ```yaml
    id: gen-1779447979-077vepCYJjlgJfXKnK2q
    object: chat.completion
    created: 1779447979
    model: openai/gpt-5-nano-2025-08-07
    provider: OpenAI
    system_fingerprint: null
    service_tier: default
    choices:
      - index: 0
        logprobs: null
        finish_reason: stop
        native_finish_reason: completed
        message:
          role: assistant
          content: Paris.
          refusal: null
          reasoning: '**Providing the capital of France**


            The user asked a straightforward question: "What is the capital of France?"
            The answer is simple: Paris. I should respond concisely. My best guess is
            to confirm: "The capital of France is Paris." While adding context could be
            fun, it’s not necessary since the user didn’t request it. If I wanted to be
            helpful, I could mention that Paris is the largest city and home to famous
            landmarks like the Eiffel Tower, but I’ll keep it brief.**Confirming details
            on Paris**


            I can keep my response short and straightforward. The user asked about the
            capital of France, and I can simply say: "Paris." If I want to offer more,
            I could say, "The capital of France is Paris." I think that covers it! But
            if they are interested, I could mention I''m happy to share more details about
            Paris if they''d like. For now, I’ll stick with the essential answer.'
    usage:
      prompt_tokens: 13
      completion_tokens: 243
      total_tokens: 256
      cost: 9.785e-05
      is_byok: false
      prompt_tokens_details:
        cached_tokens: 0
        cache_write_tokens: 0
        audio_tokens: 0
        video_tokens: 0
      cost_details:
        upstream_inference_cost: 9.785e-05
        upstream_inference_prompt_cost: 6.5e-07
        upstream_inference_completions_cost: 9.72e-05
      completion_tokens_details:
        reasoning_tokens: 192
        image_tokens: 0
        audio_tokens: 0

    ```

{{% /section %}}

---

{{% section %}}

## What to expect in general from Web APIs of LLM-as-a-Service providers?

1. __Pick__ among a variety of __models__ (by _name_), with different features, capabilities (and prices)

2. __Provide__ general __instructions__ for the task at hand (e.g. via _system prompts_, or top-level instructions)

3. __Ask__ the __next message__ to produce after a _sequence of messages_ (e.g. via chat completions)
    - input/output messages may include content of _different modalities_ (e.g. text, images, audio, video, files, etc.)
    - messages may also include _tool calls_, _tool results_, _reasoning traces_, etc.
    - input messages may contain instructions about how to _structure the output_ (e.g. via JSON schema, or other constraints)

4. Message __streaming__: receive partial responses as they are generated by the model, instead of waiting for the full response

5. Include __tools descriptions__ somewhere, so that model can ask the outer system to _call_ (a.k.a. _invoke_) them when needed
    - outer system is supposed to react to tool invocation with _tool results_, which are then fed back to the model as part of the conversation
        + so that the model can decide how to use them to complete the task at hand

6. Set the __temperature__ of the model, to control the randomness of the output
    + e.g. higher temperature means more random output, while lower temperature means more deterministic output

---

## About LLMs' Web API Compatibility (pt. 1) – OpenAI family

* **Shape**: _"Chat Completions"_ uses `/chat/completions` end point; _"Responses"_ uses `/responses` endpoint
* **Abstraction**: Chat is role-message based; Responses is typed-item based
    - e.g. chat can be a content (e.g. text, image), provided by a role (e.g. user, assistant); responses can be a tool call, a tool result, a reasoning step, etc.
    - e.g. responses could be messages, or tool call or results
* **Capabilities**:
    - _calling tools_ (implies including tool definitions in the prompt, so that the model can call them)
    - _structured_ output (e.g. constrain model response to match a given JSON schema)
    - _multimodal_ (e.g. include images, audio, video in the prompt and/or response)
    - _streaming_ (e.g. receive partial responses as they are generated by the model, instead of waiting for the full response)
    - _reasoning traces_ (e.g. receive the model's reasoning process as part of the response, to understand how it arrived at its answer)
* **Peculiarities**: "Responses" is more modern; "Chat Completions" is more compatible
* **Portability**: "Chat Completions" is high; "Responses" is mostly OpenAI/Azure-native

---

## About LLMs' Web API Compatibility (pt. 2) – OpenAI-compatible APIs

* **Shape**: mimic `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`
* **Abstraction**: OpenAI-like messages over non-OpenAI models
  - Example: same SDK call, different `base_url`, `api_key`, and `model`
* **Capabilities**: usually chat and streaming; tools/JSON vary substantially
  - Example: text streaming may work, but tool-call parsing may fail or differ
* **Peculiarities**: compatibility is often only wire-level, not behavioral
* **Portability**: good for client reuse; weak for advanced features exploitation

{{% fragment %}}
> It may happen that some providers (e.g. Ollama) offer an OpenAI-compatible API, but with a subset of the features of OpenAI's API, and with some differences in the behavior of the models (e.g. in terms of tool use, reasoning traces, etc.)

when this is the case, the client will fail at run-time, complaining about unsupported features for non-reachable endopoint!
{{% /fragment %}}

---

## About LLMs' Web API Compatibility (pt. 3) – Anthropic Clade API

* **Shape**: `/v1/messages`
* **Abstraction**: messages plus content blocks and top-level system instruction
  - Example: `system: "..."` separate from `messages: [...]`
* **Capabilities**: tool use, streaming, long context, prompt caching, extended thinking
  - Example: cache a long policy document, then ask many follow-up questions
* **Peculiarities**: system prompts, tool results, and streaming events differ from OpenAI
* **Portability**: strong native API; needs adapter for OpenAI-style systems

---

## About LLMs' Web API Compatibility (pt. 4) – Google API

* **Shape**: `generateContent` and `streamGenerateContent`
* **Abstraction**: `contents` made of multimodal `parts`
  - Example: one request can include `text`, `image`, `audio`, or `file` parts
* **Capabilities**: native text, image, audio, video, files, tools, structured output
  - Example: analyze a PDF/image, call a function, return schema-constrained JSON
* **Peculiarities**: multimodality is core, not an add-on to chat
* **Portability**: powerful native API; structurally different from OpenAI/Anthropic

---

## About LLMs' Web API Compatibility (pt. 5) – Cloud-provider APIs

* **Shape**: AWS Bedrock Converse; Azure OpenAI / Azure AI Foundry APIs
* **Abstraction**: provider-managed access to multiple or deployed models
  - Example: Azure calls a deployment name; Bedrock calls a model via AWS runtime
* **Capabilities**: streaming, tools, structured output, governance features
  - Example: IAM-controlled access, content filters, guardrails, regional deployment
* **Peculiarities**: deployment names, API versions, regions, IAM, filters leak into design
* **Portability**: good inside the cloud ecosystem; weaker across ecosystems

---

## About LLMs' Web API Compatibility (pt. 6) – Gateways and routers

* **Shape**: usually OpenAI-compatible proxy APIs
* **Abstraction**: one internal API over many upstream providers
* **Capabilities**: routing, fallback, retries, budgets, logging, observability
* **Peculiarities**: advanced features leak through provider-specific behavior
* **Portability**: strong for application architecture; imperfect for feature exploitation

---

## About LLMs' Web API Compatibility (pt. 7) – Wrap Up

__OpenAI-like__ APIs are becoming the _de-facto_ standard, yet they are currently under active _evolution_

{{<image src="apis.png" alt="LLMs' Web API Compatibility Landscape" max-h="70vh" >}}

{{% /section %}}

---

## About client libraries

- Main providers – especially the ones exposing their own Web APIs – come with their own __client libraries__
    + wrapping those APIs into custom SDKs for target programming languages (e.g. Python, JS, Java, etc.)

- Two major didactical choices here (among the _many_ possible ones):
    1. [OpenAI Client lib](https://developers.openai.com/api/docs/libraries) flavoured for JavaScript, Python, .Net, Java, Go, Ruby, CLI
        + it is the "reference" client, since OpenAI invented the first Web API for LLMs, and many other providers mimicked it
    2. [LangChain](https://python.langchain.com/en/latest/) flavoured for Python and JavaScript
        + it is a _third-party_ client library, which supports [multiple providers](https://docs.langchain.com/oss/python/integrations/providers/overview) and APIs (e.g. OpenAI, Anthropic, Google, Azure, etc.)
        + it is more focused on _orchestrating_ interactions with LLMs and tools, rather than just wrapping Web APIs

---

# Focus on OpenAI's Client Library for Python

---

## OpenAI's Chat Completion API with Python

- This is the simplest and most common way to interact with OpenAI-like API providers, via the [openai-python](https://github.com/openai/openai-python) library
    * just run `pip install openai` to install it, into your (virtual) Python environment
    * in your Python scripts, just import the `openai` module

- API comes with _synchronous_ and _asynchronous_ variants
    * __synchronous__: the model's _response_ is returned as a _whole_, after the model has finished generating it (which may take _time_)
    * __asynchronous__: the model's _response_ is returned as a _stream_ of parts, as they are generated by the model, allowing for a more fluid experience (content shown _ASAP_)

- In both cases, ingredients are essentially the same:
    1. __Env vars__ (or command line arguments): to parametrize your program w.r.t. _API keys_, API providers' _base urls_, _model names_, etc.
    2. __Client__: an object of type `openai.OpenAI` (for _sync_) or `openai.AsyncClient` (for _async_) by which you interact with a model as provided by some provider
        - documented "by example" at <https://github.com/openai/openai-python/blob/main/README.md>
    3. __Conversation history__: literally a _list_ of _dictionaries_, each one having two keys: `role` (e.g. "system", "user", "assistant") and `content` (actual text) 
    4. __Chat completion request__: a call to the `client.chat.completions.create()` method, accepting the conversation hystory as input plus some additional parameters (e.g. `temperature`, `max_tokens`, etc.) and returing either the full response (sync) or a stream of response parts (async), depending the parameter `stream` (respectively `False` or `True`)
        + documented here <https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create>
    5. __Chat completion response__: a dictionary containing the model's response, including the generated content (e.g. in `.choices[0].message.content`), plus some additional metadata (e.g. `usage`, `model`, etc.)
        + in principle, there could be multiple _choices_ in the response (in practice is often just one): the idea is that the model may produce alternative responses at once
        + documented here <https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/retrieve>
    6. The __agent__, i.e. the program exploiting the aformentioned functionalities to accomplish some task
        + in case multiple subsequent request–response interactions are needed, the agent should include also reponses' messages in the chat history
        + this is because the model is _stateless_, and the HTTP API are _ReSTful_, but the "conversation" is _mutable_ entity

---

{{% section %}}

## Example 1: Sync CLI Chat (pt. 1)

1. Let's first create the client out of OR's base URL, API key, and target model:
    
    {{% code path="content/llmaas/repl_chat_openai_chatcompletions.py" from="1" to="9" %}}

    notice that:
    - class `OpenAI(...)` initializes the client in a very customizable way
    - the `base_url` parameter, which commonly defaults to <https://api.openai.com/v1>, is set to OR's base URL <https://openrouter.ai/api/v1>, unless specified otherwise via env vars
    - the `api_key` is not in the source file, but taken from env var, or stdin, to avoid hardcoding it in the source code
    - the `model` parameter must be set to some model available in the provider's model zoo

2. Let's then _initialize_ the _conversation_ history with a __system prompt__, containing _general instructions_ for the LLM, which make sense w.r.t. the task at hand

    {{% code path="content/llmaas/repl_chat_openai_chatcompletions.py" from="10" to="11" %}}

    here one may give additional instructions to be followed in the rest of the conversation

    - e.g. "always answer in english", or "detect the user's langauge and answer in the same language", etc.

---

## Example 1: Sync CLI Chat (pt. 2)

3. Finally, we can enter a loop in which we read the user's input from the command line, send it to the model as a new message in the conversation, and print the model's response back to the command line

    {{% code path="content/llmaas/repl_chat_openai_chatcompletions.py" from="15" to="35" %}}

    notice that:

    1. external `try-except` block is used to catch user's `KeyboardInterrupt` (e.g. Ctrl+C) or `EOFError` (e.g. Ctrl+D) to exit gracefully from the loop
    1. user input is first looked for _sub-commands_ (e.g. `/exit`, `/retry`, etc.) 
    1. _non_-sub-command _input_ is then used to create a new message with role `user`, which is appended to the conversation history (`messages` list)
    1. then, a chat completion _request_ is sent to the `model` via `client.chat.completions.create(...)`, with the conversation history as input
    1. the model's _response_ is supposed to contain a _single choice_ (`response.choices[0]`), whose `.message.content` is what we show to the user

---

## Example 1: Sync CLI Chat (pt. 3)

4. Full code [here](./repl_chat_openai_chatcompletions.py)

5. Example of interaction with the model (start with `python path/to/script.py` in the terminal):

```text
Enter your API key for https://openrouter.ai/api/v1/: sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXX
Using model: openrouter/auto
Type '/exit' or '/quit' to stop. Type '/retry' to retry the last message.

you> hi there, what time is it?

assistant> Hi! I don’t have a real-time clock on my end. Could you tell me your time zone or city, and I’ll give you the current local time? If you’d prefer, I can also give you the current UTC time.

you> it's Cesena, in Italy

assistant> In Cesena, Italy right now it’s Central European Summer Time (CEST), which is UTC+2. I can’t see the exact current time here, but if you tell me the current UTC time (or your device’s time), I’ll convert it to Cesena time for you. 

Example: if UTC is 13:00, then Cesena is 15:00. Want me to convert a specific time? Or you can just check your phone or a world clock for the exact minute and second.

you> ^CGoodbye!
```

7. When you run it, pay attention to:
    - time to get a response from the model (latency)
    - you have no way to know which model is actually serving your request, do you?
    - the model does not have access to real-time information, so it cannot answer questions about (e.g.) the current time
    
{{% /section %}}

---

{{% section %}}

## About Chat Completion API (pt. 1)

### Request parameters which can be passed to `client.chat.completions.create(...)`

(cf. <https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create>)

- `messages` (list of dicts): the conversation history, as a list of messages, each one having a `role` (e.g. "system", "user", "assistant") and `content` (actual text)
    ```python
    messages = [
      dict(role="system", content="When asked about time, ask location if missing, then call the `get_current_time` tool."),
      dict(role="user", content="What time is it?"),
      { "role": "assistant", "content": "What location should I use to check the current time?" },
      { "role": "user", "content": "Cesena Italy" },
      {
        "role": "assistant",
        "content": None,
        "tool_calls": [
          {
            "id": "call_current_time_001",
            "type": "function",
            "function": dict(name="get_current_time", arguments="{\"location\":\"Cesena, Italy\"}")
          }
        ]
      },
      dict(role="tool", tool_call_id="call_current_time_001", content="{\"location\":\"Cesena, Italy\",\"timezone\":\"Europe/Rome\",\"current_time\":\"2026-05-23T14:37:00+02:00\"}"),
      { "role": "assistant", "content": "The current time in Cesena, Italy is 14:37 on May 23, 2026."}
    ]
    ```

    + there could be other fields, especially in messages generated by the model (e.g. tool calls, reasoning traces, etc.)
- `model` (str): the name of the model to use for this request, which must be available in the provider's model zoo
- `temperature` (float in `0 .. 2`): controls the _randomness_ of the output, with higher values leading to more random output, and lower values leading to more deterministic output

---

## About Chat Completion API (pt. 2)

### Request parameters which can be passed to `client.chat.completions.create(...)` (cont.)

- `max_completion_tokens` (int, default: `None`): an upper bound for the number of tokens that can be generated for a completion, including visible _output_ tokens and _reasoning_ tokens.

- `n` (int, default: `1`): the number of alternative completions to generate for each input message. The API will return a list of `choices`, each one containing a different completion.

- `stream` (bool, default: `False`): whether to receive the response as a stream of parts, as they are generated by the model, instead of waiting for the full response. If `True`, the API will return an iterator that yields partial responses.

- `response_format` (str, default: `None`): the format in which the model should return the response
    - value `{ "type": "text" }` (default) means that the model should return a plain text response
    - value `{ "type": "json_object" }` forces the model to produce a JSON outout (assumes the schema of the object is described in the system prompt, or in some previous message)
    - value `{ "type": "json_schema", "description": STRING, "strict": BOOL, "schema": "..." }` forces the model to produce a JSON output matching the provided [JSON schema](https://json-schema.org/), with an optional `description` to better describe the schema to the model, and an optional `strict` flag to control how strictly the model should follow the schema (e.g. whether to allow extra fields or not)
        * this is important to support [structured output](https://developers.openai.com/api/docs/guides/structured-outputs) explained later

- `stop` (str or list of str, default: `None`): one or more sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.

---

## About Chat Completion API (pt. 3)

### Request parameters which can be passed to `client.chat.completions.create(...)` (cont.)

- `tool_choice` controls which tools the model can use to solve the task at hand, and how to use them
    - value `none` means that the model cannot use any tool, and should rely on its own knowledge and capabilities to answer the user's question
    - value `auto` (default) means that the model can decide autonomously which tools to use, if any, based on the conversation history and the task at hand
    - value `required` means that the model must use at least one tool to answer the user's question, and cannot rely solely on its own knowledge and capabilities
    - further variants are available to finely control which tools the model can use 

- `tools` (list of dicts): the list of tools that the model can use, each one described by a dictionary containing at least a `name` and a `description`, and optionally some additional fields (e.g. `parameters_schema` to describe the expected input for the tool, etc.)
    
    ```python

    tools=[
      dict(
        type="custom",
        custom={
          "name": "timezone_lookup_dsl",
          "description": "Resolve a city and country into an IANA timezone. The input must follow the DSL form TIMEZONE(\"City, Country\").",
          "format": {
            "type": "grammar",
            "grammar": { "syntax": "regex", "definition": "^TIMEZONE\\(\"[A-Za-z .'-]+, [A-Za-z .'-]+\"\\)$" }
          }
        }
      ),
      dict(
        type="function",
        function={
          "name": "get_current_time",
          "description": "Get the current local time for a given IANA timezone.",
          "parameters": {
            "type": "object",
            "properties": {
              "timezone": { "type": "string", "description": "An IANA timezone identifier, for example Europe/Rome" }
            },
            "required": [ "timezone" ],
            "additionalProperties": False
          }
        }
      ),
    ]
    ```

    tools descriptions can be of two sorts:
    - `function` tools, which are described by their name, a natural language description of what they do, and a JSON schema describing the expected input for the tool (e.g. the parameters of the function)
    - `custom` tools, which are described by their name, a natural language description of what they do, and a custom format description (e.g. a Regex describing the expected input for the tool)

---

## About Chat Completion API (pt. 4)

### What can you expect in the response of a chat completion request?

Reponses are JSON objects containing many relevant metadata, explanation below in YAML syntax for better readability:

```yaml
object: chat.completion # the type of the returned object, which is "chat.completion" for chat completion requests
id: chatcmpl-abc123 # a unique identifier for this chat completion, which can be used for tracking and debugging purposes
model: gpt-4o-2024-08-06 # the actual model that served this request, which may be different from the one specified in the request due to dynamic routing or other factors
created: 1738960610 # the Unix timestamp of when the chat completion was created, which can be useful for logging and debugging purposes
request_id: req_ded8ab984ec4bf840f37566c1011c417 # a unique identifier for the request that led to this chat completion, which can be used for tracking and debugging purposes
tool_choice: auto # the tool choice mode that was used for this chat completion, which can be "none", "auto", "required", or other variants
usage: # the usage statistics for this chat completion
  prompt_tokens: 13 # input tokens
  completion_tokens: 18 # output tokens
  total_tokens: 31 # total tokens (input + output)
seed: 4944116822809980000 # the random seed used for this chat completion, which can be useful for reproducibility and debugging purposes
top_p: 1 # the top_p value used for this chat completion (settable in the request)
temperature: 1 # the temperature value used for this chat completion (settable in the request)
presence_penalty: 0 # the presence_penalty value used for this chat completion (settable in the request)
frequency_penalty: 0  # the frequency_penalty value used for this chat completion (settable in the request)
system_fingerprint: fp_50cad350e4 # a fingerprint of the system configuration that served this request, which can be used for tracking and debugging purposes
metadata: {} # any additional metadata associated with this chat completion
choices: # list of choices generated by the model for this chat completion, each one containing the same fields
- index: 0 # the index of this choice in the list of choices
  message: # the message generated by the model for this choice, which can contain various fields depending on the content and the features used
    content: "Mind of circuits hum,  \nLearning patterns in silence—  \nFuture's quiet
      spark."
    role: assistant # the role of the message, which can be "assistant", "tool", "system", etc.
    tool_calls: # the list of tool calls made by the model in this message, if any, each one containing at least a `name` and `arguments`, and optionally some additional fields (e.g. `id`, `type`, etc.)
      - name: get_current_time # the name of the tool that was called by the model
        arguments: "{\"timezone\":\"Europe/Rome\"}" # the arguments passed to the tool call, which can be a JSON string or other format depending on the tool's definition
        id: call_current_time_001 # a unique identifier for this tool call, which can
  finish_reason: stop # the reason why the model stopped generating tokens for this choice, which can be "stop" (if the model reached a stop sequence), "length" (if the model reached the max_completion_tokens limit), "tool_call" (if the model made a tool call and stopped), or other reasons
  logprobs: # the log probabilities of the generated tokens for this choice, which can be useful for analyzing the model's confidence and behavior (not always present in the response)
response_format: 
```

- most commonly, one cares about the first choice (`choices[0]`), and in particular about the generated message (`choices[0].message.content`), but the rest of the metadata can be useful for debugging, analysis, and cost control purposes

{{% /section %}}

---

{{% section %}}

## Example 2: Async CLI Chat with Streaming (pt. 1)

1. Client setup is very similar to the sync version, but we use `AsyncOpenAI(...)` and keep the same env-driven configuration style:

  {{% code path="content/llmaas/repl_chat_openai_chatcompletions_async.py" from="1" to="10" %}}

  notice that:
  - `AsyncOpenAI(...)` is the async counterpart of `OpenAI(...)`
  - we need module `asyncio` to run the main async function, and to handle async calls in general

2. As the program is asynchronous, we need to define an `async def main():` function, which will contain the main logic of our program, and then run it with `asyncio.run(main())` at the end of the script

    {{% code path="content/llmaas/repl_chat_openai_chatcompletions_async.py" from="56" to="57" %}}

---

## Example 2: Async CLI Chat with Streaming (pt. 2)

3. The main function is structure more or less like the sync version...

    {{% code path="content/llmaas/repl_chat_openai_chatcompletions_async.py" from="16" to="53" %}}

    with some differences in the way we i. create the completion request, by setting `stream=True` to receive a stream of response parts, and by awaiting the response with `async for` instead of just `for`; and ii. consume the stream of response parts

    ```python
    stream = await client.chat.completions.create(..., stream=True) # create the request + open response stream
    answer_parts = [] # buffer to store the parts of the answer as they arrive
    async for item in stream:
        chunk = item.choices[0].delta.content or "" # get each chuck of the answer as it arrives (if any)
        answer_parts.append(chunk) # store the chunk in the buffer
    messages.append(dict(role="assistant", content="".join(answer_parts))) # reconstract the full answer and store it in the conversation history
    ```

    - notice the `.delta` field in the response parts
    - notice that partial responses should be printed with `print(..., end="", flush=True)` to avoid buffering issues in the terminal

---

## Example 2: Async CLI Chat with Streaming (pt. 3)

4. Full code [here](./repl_chat_openai_chatcompletions_async.py)

5. Example of interaction (start with `python path/to/script_async.py`):

```text
Enter your API key for https://openrouter.ai/api/v1/: sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXX
Using model: openrouter/auto
Type '/exit' or '/quit' to stop. Type '/retry' to retry the last message.

you> hi bro

assistant> Hey! How’s it going? How can I help today? I can answer questions, explain things, help with writing or editing, brainstorm ideas, or assist with code—tell me what you need.

you> can you generate the first 20 verses of the divine comedy, in english?
assistant> Sure—do you want the first 20 lines from Inferno, Canto I in Henry Wadsworth Longfellow’s public-domain English translation, or would you prefer a different translation? I can paste exactly whichever you choose.

you> yeah that's fine

assistant> Here are the first 20 lines of Inferno, Canto I, from Henry Wadsworth Longfellow's translation of Dante Alighieri's *Divine Comedy*:
assistant> 
assistant> Midway upon the journey of our life
assistant> I found myself within a forest dark,
assistant> For the strayed path had filled my soul with strife.
assistant> How hard a thing it is to tell what deep
assistant> And tangled wood this was, how wild and steep,
assistant> Which on my memory leaves so keen a fear!
assistant> So bitter is it, death is slight relief;
assistant> But to set forth the goodness that I found,
assistant> I'll speak of other things that there appeared.
assistant> I know not how I entered it, so deep
assistant> I had become in slumber at that hour
assistant> When I had wandered from the path of truth.
assistant> 
assistant> But after I had reached a hill’s low foot,
assistant> Where the long valley terminating had
assistant> My fear, a place, I say, that any heart
assistant> With dread doth pierce; and when I looked above,
assistant> I saw its highest point already clothed
assistant> With rays of the planet that guides man aright
assistant> On every path. Then was the fear a while
assistant> Abated.
assistant> 
assistant> Let me know if you’d like more!

you> Goodbye!
```

6. When you run it, pay attention to:
    - perceived latency (first token arrives earlier than full-response mode)

{{% /section %}}

---

{{% section %}}

## Exercise 1: Caching Sync Requests

> __Problem__: when experimenting with _programmatic_ LLM interfaces, one does a lot of trial and erros, possibly consuming credits, or wasting attempts w.r.t. rate limits, etc.

> __Idea__: implement a simple _caching_ mechanism for your program, so that you can store the responses of the model for given inputs, and reuse them when the same inputs are encountered again (also good for _reproducibility_ and _debugging_ purposes)

### TO-DO List

1. Implement some caching mechanism for the Sync CLI Chat program, so that Chat Completion requests are cached on the file system before being issued
2. Upon doing a new request to the model, first check if the same request has already been made before, and if so, return the cached response instead of issuing a new request to the model

---

## Exercise 1: Caching Sync Requests (cont.)

### Decision points and hints

- Where to store the cache? 
    * e.g. in local untrucked folder, temp folder, home sub-folder, etc.
- How to index the caches? A.k.a. when a cache is hit? 
    * same last message? same conversation history? same model and parameters? same temperature? same model?
- How to store the cache?
    * e.g. as YAML/JSON files, with a naming convention based on the cache index?
    * how to simply cache lookup then?
- How to restructure the code?

### How to test it?

- run the program, and try to send the same message twice, to see if the second time the response is returned from the cache (e.g. by printing a message like "Cache hit! Returning cached response."), and check that the response is indeed the same as the first time
- try to change the message slightly (e.g. by adding a punctuation mark), and see that the cache is not hit, and a new request is sent to the model, and check that the response is different from the first time

{{% /section %}}

---

{{% section %}}

## Exercise 2: Retry and Exponential Backoff 

> __Problem__: when interacting with LLMs via Web APIs, it may happen that some requests _fail_ due to _transient issues_ (e.g. network errors, <u>rate limits</u>, etc.)

> __Solution__: it is good practice to implement some (configurable) _retry mechanism_ with (configurable) [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff) to handle such cases gracefully

### TO-DO List

1. Implement a retry + delay mechanism for the Sync CLI Chat program, so that 
    - when a request to the model fails, the program _automatically retries_ the request after a _certain delay_, up to a _maximum_ number of _retries_
    - the _delay_ between retries _increases exponentially_ (e.g. 1s, 2s, 4s, 8s, etc.) to avoid overwhelming the server and to give it some time to recover from transient issues
2. Let all these parameters (e.g. number of retries, initial delay, backoff factor, etc.) be configurable via env vars or command line arguments (with smart defaults)

---

## Exercise 2: Retry and Exponential Backoff (cont.)

### Decision points and hints

- How to detect a failed request? 
    * e.g. catch exceptions from the client library, check HTTP status codes, etc.
- How to implement the retry mechanism?
    * e.g. with a simple loop and `try-except` block, or with a more sophisticated library like `tenacity`?
- How to implement the exponential backoff?
    * e.g. with a simple calculation based on the retry count, or with a library like `tenacity` that has built-in support for exponential backoff
- How to make the parameters configurable?
    * e.g. via env vars, command line arguments, or a configuration file? consider using `argparse` for command line arguments, and `os.getenv` for env vars
- How to restructure the code?
    * e.g. separate the retry logic into a decorator or a helper function, to keep the main logic of the program clean and focused on the chat interaction

### How to test it?

- run the program, and simulate a transient failure (e.g. by disconnecting the network, or by sending too many requests to trigger rate limits), and see that the program retries the request with increasing delays, and eventually succeeds or gives up after the maximum number of retries
- try to configure the parameters (e.g. number of retries, initial delay, backoff factor) and see that the retry behavior changes accordingly (e.g. more retries, longer delays, etc.)

{{% /section %}}

---

## About Structured Output

__TL;DR__: forcing the model to _produce output_ in a specific format (e.g. JSON matching a given schema) so that to bring unstructured input data (e.g. natural language) into structured form that can be easily processed by downstream applications (e.g. databases, APIs, etc.)

![](./structured-output.png)

---

## How to represent target structured format to the model?

1. __Natural language description__: describe the target format in natural language
    - e.g. "the output should be a JSON object with the following fields: name (string), age (integer), email (string), etc."

2. __Example-based description__: provide one or more examples of the target format, 
    - e.g. "the output should look like this: `{ "name": "John Doe", "age": 30, "email": "john.doe@example.com" }`

3. __Schema-based description__: provide a formal schema (e.g. JSON Schema) describing the target format, e.g. "the output should match the following JSON Schema (written in YAML for better readability):

    ```yaml
    type: object
    properties:
      name:
        type: string
      age:
        type: integer
      email:
        type: string
    required: [name, age, email]
    additionalProperties: false
    ```

4. In _strongly-typed_ programming languages (e.g. Java), client libraries may _reverse-engineer_ the schema from the _type definitions_ in the code, using __reflection__, or leverage serialization libraries such as [Jackson](https://github.com/FasterXML/jackson)

5. In _Python_, one can use [libraries like `pydantic`](https://docs.pydantic.dev/) to define _data models_ with validation logic, and then __generate__ JSON Schemas from them
    + this is so common, that LLM-aaS Client Libraries (there including `openai`) often have built-in support for `pydantic` models 

---

{{% section %}}

## Pydantic classes with documentation strings (pt. 1)

1. Core idea behind `pydantic` is to define _data models_ as __Python classes__ extending `pydantic.BaseModel`
    + with type __annotations__ for the _fields_, also borrowing types from the Python standard library (e.g. `datetime`, `Optional`, etc.)

    ```python
    from typing import Optional
    from pydantic import BaseModel
    from datetime import datetime

    class User(BaseModel):
        name: str
        age: int
        email: Optional[str] = None

    class Post(BaseModel):
        title: str
        content: str
        author: User
        timestamp: datetime
    ```

    + one may also have nested data models, _optional_ fields, _default_ values, etc.
    + `pydantic` data model $\approx$ data classes with default _validation_ and _serialization_ logic
        - automatically implemented constructurs accepting arguments named after the field, with _type_ checking and validation (e.g. `User(name="John Doe", age=30)`)
        - methods to serialize the model to JSON (e.g. `user.model_dump_json()`) and to generate JSON Schema (e.g. `User.model_json_schema()`)

---

## Pydantic classes with documentation strings (pt. 2)

2. To make the data model understandable to the LLM, one _should_ add __documentation strings__ to the fields, which will be included in the generated JSON Schema as `description` fields—also good for setting _default values_ or default _factories_

    ```python
    from typing import Optional
    from pydantic import BaseModel, Field # <-- notice the import of Field for adding documentation strings
    from datetime import datetime

    class User(BaseModel):
        """Anagraphical and contact information about a user."""

        name: str = Field(..., description="The user's full name")
        age: int = Field(..., description="The user's age in years")
        email: Optional[str] = Field(default=None, description="The user's email address")

    class Post(BaseModel):
        """A blog post created by a user."""

        title: str = Field(..., description="The title of the post")
        content: str = Field(..., description="The content of the post")
        author: User = Field(..., description="The author of the  post")
        created_at: datetime = Field(default_factory=datetime.now, description="The date and time when the post was created")

    ```

3. For instance, the class definitions above would produce the following JSON Schema (formatted in YAML for better readability):

    ```yaml
    title: Post
    type: object
    description: A blog post created by a user.
    properties:
      title:
        description: The title of the post
        title: Title
        type: string
      content:
        description: The content of the post
        title: Content
        type: string
      author:
        "$ref": "#/$defs/User"
        description: The author of the  post
      created_at:
        description: The date and time when the post was created
        format: date-time
        title: Created At
        type: string
    required: [title, content, author]
    "$defs":
      User:
        description: Anagraphical and contact information about a user.
        properties:
          name:
            description: The user's full name
            title: Name
            type: string
          age:
            description: The user's age in years
            title: Age
            type: integer
          email:
            anyOf:
            - type: string
            - type: 'null'
            default: 
            description: The user's email address
            title: Email
        required:
        - name
        - age
        title: User
        type: object
    ```

{{% /section %}}

---

{{< import path="reusable/running-example.md" >}}

---

{{% section %}}

## Example 3: Structured Output with Pydantic Classes (pt. 1)

> __Goal__: let's _extract_ structured information from the candidates' _presentation letters_
- In particular:
    + information about the _applicant_ (name, strengths, weaknesses, etc.), to see whether the letter is actually _positive_
    + information about the _authors_ of the letter (e.g. name, position, relationship with the applicant, etc.), to see whether the letter is actually _credible_
    + give a reproducible and grounded _recipe_ for __scoring__ the letter based on these aspects 

{{% fragment %}}

1. Let's import `openai` and initialize the client as usual:

    {{% code path="content/llmaas/letter_evaluator_openai.py" from="1" to="8" %}}

2. Let's design a system prompt to contain general instructions for the model

    {{% code path="content/llmaas/letter_evaluator_openai.py" from="11" to="16" %}}

{{% /fragment %}}

---

## Example 3: Structured Output with Pydantic Classes (pt. 2)

3. Let's define `pydantic` classes to represent the target format, with _documentation strings_ to complement the specification

    - Imports:

        {{% code path="content/llmaas/letter_evaluator_openai.py" from="31" to="32" %}}

    - A class for the _applicant_'s information:

        {{% code path="content/llmaas/letter_evaluator_openai.py" from="34" to="43" %}}

    - A class for the _author_'s information:

        {{% code path="content/llmaas/letter_evaluator_openai.py" from="45" to="55" %}}

    - A class for the overall _evaluation_ of the letter, including the extracted information and the final score:

        {{% code path="content/llmaas/letter_evaluator_openai.py" from="57" to="61" %}}

        * notice that instructions for scoring are contained in another string

---

## Example 3: Structured Output with Pydantic Classes (pt. 3)

4. _Instructions_ for _scoring_ can be provided as well in _natural language_, yet better to be precise and give the LLM a _"recipe"_ for scoring

    {{% code path="content/llmaas/letter_evaluator_openai.py" from="18" to="28" %}}

6. With these ingredients in mind, the automatic evaluation logic is as simple as a _single request–response interaction_ with the LLM:

    {{% code path="content/llmaas/letter_evaluator_openai.py" from="64" to="76" %}}

    notice that:

    - function `client.chat.completions.`<u>`parse`</u>`(...)` is called in place of `.create(...)`
        + to automatically parse the model's response into an instance of the `LetterInfo` 
    - the `response_format` parameter is set to a _reference_ to the `LetterInfo` class
        + `openai` will automatically generate the corresponding JSON Schema from the class definition, and include it in the request 

---

## Example 3: Structured Output with Pydantic Classes (pt. 4)

7. Full code [here](./letter_evaluator_openai.py)

8. At this point, the logic of the program is trivial (load letter file $\rightarrow$ call `evaluate_letter(...)` $\rightarrow$ print the evaluation):
    
    {{% code path="content/llmaas/letter_evaluator_openai.py" from="79" to="92" %}}

9. Possible results below:

{{% multicol %}}
{{% col class="col-4" %}}
{{% code path="content/llmaas/structured-output-mario-rossi.yml" %}}
{{% /col %}}
{{% col class="col-4" %}}
{{% code path="content/llmaas/structured-output-jean-dupont.yml" %}}
{{% /col %}}
{{% col class="col-4" %}}
{{% code path="content/llmaas/structured-output-mohammed-ali.yml" %}}
{{% /col %}}
{{% /multicol %}}

{{% /section %}}

---

## Exercise 3: Improving Letter Scoring with (even more) Structured Output

> __Problem__: the scoring recipe provided to the model is still quite vague and unstructured, which may lead to _inconsistent_ and _non-reproducible_ scores. Even when good, scores are not _explainable_, as the reasoning behind them is not made explicit.

{{% fragment %}}
### TO-DO List
1. let's turn the scoring recipe into a _checklist_ of criteria
2. let's have a Pydantic class with as many __boolean fields__ as the criterial in the checklist
3. let's ask the _LLM_ to set the boolean fields by analysing the _input letter_
4. let's write down the _algorithm_ to compute the final score based on the boolean fields, as a _function_ in the Pydantic _class_
    + the scoring logic is now _reproducible_ and _explainable_
    + the hallucination margin is reduced, as the model is not asked to directly produce a score, but rather to fill in the boolean fields based on the content of the letter, which is an easier task
{{% /fragment %}}

---

{{% section %}}

## Exercise 4: Extract Structured Information from Pictures (pt. 1)

> __Goal__: let's say the committee wants to extract structured information from the ID documents of the candidates, which are provided as pictures in the application form

{{% fragment %}}
### TO-DO List
1. let's use some LLM with _vision capabilities_ (e.g. [OR model `google/gemma-4-26b-a4b-it:free`](https://openrouter.ai/google/gemma-4-26b-a4b-it:free))
2. let's design a prompt to ask the model to extract structured information from the ID document, such as name, date of birth, ID number, _expiration date_, etc.
3. let's define a Pydantic class to represent the extracted information, with appropriate fields and documentation strings
4. let's call the LLM _with the picture_ of the ID document as input, and get the structured information as output
5. let's test the program with _different ID documents_, and see how well the model can extract the information
{{% /fragment %}}

---

## Exercise 4: Extract Structured Information from Pictures (pt. 2)

### How to pass images to the model?

- Many ways, documented [here](https://developers.openai.com/api/docs/guides/images-vision?format=base64-encoded#giving-a-model-images-as-input), simplest one is passing [base64-encoded](https://en.wikipedia.org/wiki/Base64) image in the `content` field of a message:

- [HOW-TO] Encoding an image in base64 and passing it to the model:

    ```python
    import base64

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    ```

- [HOW-TO] Constructing a message with both _text_ and _image_ content (notice that the `content` field is now a list of _typed_ pieces):

    ```python
    def content_with_image(role, text, image_path):
        return dict(
            role=role,
            content=[
                dict(type="input_text", text=text),           # vvvv  TODO change jpeg with your image format if needed (e.g. png)
                dict(type="input_image", image_url=f"data:image/jpeg;base64,{encode_image(image_path)}"),
            ],
        )
    ```

- [HOW-TO] Define the _Pydantic class_ to represent the expected structured information extracted from the ID document:

    ```python
    from pydantic import BaseModel, Field
    from datetime import date

    class IDDocumentInfo(BaseModel):
        """Structured information extracted from an ID document."""

        name: str = Field(..., description="The full name of the person in the ID document")
        date_of_birth: date = Field(..., description="The date of birth of the person in the ID document")
        id_number: str = Field(..., description="The ID number of the document")
        expiration_date: date = Field(..., description="The expiration date of the document")
    ```

---

## Exercise 4: Extract Structured Information from Pictures (pt. 3)

- [HOW-TO] Call the LLM with the message containing the image, and parse the response as an instance of the `IDDocumentInfo` class:

    ```python
    import base64
    from openai import OpenAI

    client = OpenAI(...)

    response = client.chat.completions.parse(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts structured information from ID documents."},
            content_with_image("user", "Please extract the information from this ID document.", "path/to/id_document.jpg")
        ],
        response_format=IDDocumentInfo
    )

    result = response.choices[0].message.parsed # sopposedly an instance of IDDocumentInfo, but always good to check and validate the output
    ```

- [BEWARE] There are limitations w.r.t. input data [on OpenAI](https://developers.openai.com/api/docs/guides/images-vision#image-input-requirements) (and what about [OR](https://openrouter.ai/docs/guides/overview/multimodal/image-understanding)?)

    <!-- ![](./openai-image-input-limits.png) -->
    {{< image src="./openai-image-input-limits.png" alt="OpenAI image input limits" class="img-fluid" >}}

{{% /section %}}

---

{{% import path="reusable/back.md" %}}

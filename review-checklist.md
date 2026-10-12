# Module 2 review checklist (2026-10-12)

Legend: ✓ = verified by hand; other items come from reviewer agents, re-check before fixing.
Sub-items `Fix:` describe how to fix non-obvious items; `@gciatto` sub-items need a human decision or human work.
Line numbers refer to `content/<lecture>/_index.md` unless a snippet path is given.

## Cross-cutting / structure

- [x] Forward references to `governance` (lecture 9) phrased as "recall": `rag:112`, `skills:84`, `workflows:398`; `llmaas:101` defers model selection to it ✓
    - [x] move _technique selection_ (prompting vs. RAG vs. fine-tuning vs. agents, `governance:594-665`) earlier (end of `prompting` / start of `rag`), keep a recap in governance — done: concept + example moved to `rag` (`#/technique-selection`), trade-offs table kept in governance as `#/which-technique`
    - [x] @gciatto decide which moves to make. Options: (a) move all three (governance shrinks ~400 lines, but Ex. 1 code must move `lecture_governance/exercise1` → e.g. `lecture_validating/exercise3` on both lab-snippets branches, and governance Ex. 2 `decision-record.md` refers to "[Ex. 1]"); (b) keep in governance, just reword the 4 forward refs as "see later, in" instead of "recall". Recommend (a) for technique selection only (short, slides 596-665, no code), (b) for the rest
    - [x] move _model selection & evaluation_ + Exercise 1 (`governance:675-992`) right after `validating` (or merge with `validating` Ex. 2 step 5) — kept in governance (option b)
    - [x] move _frontier benchmarks_ (`governance:706-728`) to `genai` or next to `agents:584` — kept in governance (option b; see agents item on benchmarks)
    - [x] Fix (if moved): `agents:584` already has `agentic-benchmarks`; append the frontier-benchmarks slide after it (needs `benchmark-saturation.png` moved into `content/agents/`), leave in governance a one-line link back — n/a
- [x] Links to other lectures without anchors (add `slide id`s where missing, then link):
    - [x] `genai`: add ids to "From language to action", MCP concept, RAG concept, Prompt Templates slides; use them from `agents:68`, `agents:94`, `agents:418`, `prompting:27`
        - [x] Fix: add `{{< slide id="language-to-action" >}}` (`genai:596`), `mcp-concept` (`:737`), `rag-concept` (`:749`), `prompt-templates` (`:715`) before each `##`; then `../genai/#/<id>`
    - [x] `../llmaas/` → `#/chat-completion-concept` (`agents:26`, `agents:113`), `#/exercise-caching` (`prompting:1158`, `validating:516`, `governance:835`, `governance:901`), `#/exercise-retry` (`governance:842`), `#/ollama` or outline (`governance:101`); `prompting:1196` → Example 1 (needs id)
        - [x] Fix: add `{{< slide id="sync-chat" >}}` before `llmaas:775` (`## Example 1: Sync CLI Chat (pt. 1)`, inside the `section`), link `../llmaas/#/sync-chat`; `governance:101` → `#/ollama` (exists, `llmaas:115`)
    - [x] `../prompting/` → `#/prompting-techniques` (`workflows:378`), `#/exercise-id-documents` (`workflows:176`), `#/chat-compaction` (`skills:907`)
    - [x] `validating:106` links `../prompting/#/langchain` ("About LangChain") instead of Example 1 bis (add id)
        - [x] Fix: add `{{< slide id="letter-scoring-langchain" >}}` before `prompting:449`, link it from `validating:106`
    - [x] `governance:1202` "[countermeasures](#/responsibility)" lands 2 slides early: add id to Countermeasures slide (`:1137`)
        - [x] Fix: add `{{< slide id="countermeasures" >}}` before `governance:1137`; retarget both `#/responsibility` links meant for automation bias: `:1202` and `:1290`
- [x] Running-example slide placed after slides that already use it: `prompting:87` (move right after outline, add to outline), `skills:968` (Example 1 at `:59`, `:287` links forward), `agents:608` (far from its exercises)
    - [x] Fix: prompting — move slide `:85-91` before `## Anatomy` (`:33`), add "0. [Running example](#/running-example)" to outline; skills — move `:966-972` right after the outline (before `skills-example`, `:55`); agents — false positive-ish: it already precedes the exercises, only `planning`/`security` sections sit between; optionally move it to just before `exercise-inspect` (`:724`) — agents left as is
- [x] Running example re-imported in 5 lectures (prompting, agents, rag, skills, workflows): fine as recall, consider a short "recall" variant
    - [x] @gciatto decide: (a) keep full import everywhere (self-contained decks, recommended: each lecture is presented standalone); (b) add `reusable/running-example-recall.md` (1 slide, 3 bullets + link to `../prompting/#/running-example`) for agents/rag/skills/workflows. Either way, fix typo "transccript" in `reusable/running-example.md` — kept (a); typo fixed
- [x] Terminology for coding agents drifts: "agentic interfaces" (`genai:470`), "copilot frameworks" (`skills:18`, `:94`), "harnesses", "coding agents" (`skills:28`): pick one
    - [x] @gciatto pick the term. Recommend: "_coding agent_" for the product (Claude Code, Codex, ...), "_harness_" for the controller+tools+policies around the LLM; keep "agentic interface" in `genai` only as the interface category, adding "a.k.a. coding agents"; rename `skills:18`/`:94` "Copilot frameworks" → "Coding agents (harnesses)" (keep anchor `copilots`)
- [x] OpenAI docs on two domains: developers.openai.com (`agents:178`, `:200`) vs platform.openai.com (`rag:165`); `docs.anthropic.com` links (`llmaas:1128`, `:1191`) → `platform.claude.com`
    - [x] Fix: `rag:165` → `https://developers.openai.com/api/docs/guides/embeddings`; `llmaas:1128`, `:1191` → `https://platform.claude.com/docs/en/api/messages` (both checked 200; old one redirects there)
- [ ] Default model `nvidia/nemotron-3-super-120b-a12b:free` is a reasoning model for _all_ snippets (`prompting:838`): Examples 1–2 spend reasoning tokens, CoT comparison (`prompting:725-731`) runs on a reasoning model; check it honours low/medium/high effort
    - [ ] Fix: OpenRouter lists `reasoning_effort` among the model's supported params, but the smoke report records only pass/fail. In lab-snippets, for prompting Ex. 1/1bis/2 pass `extra_body={"reasoning": {"enabled": False}}` (or effort `"low"`), and say so on the CoT slide (`prompting:725-731`: explicit CoT on a reasoning model is partly redundant, cf. `:897` best-practices link); recheck `code` line ranges — only the CoT-slide caveat added; the `extra_body` code change waits for the verification below
    - [ ] @gciatto verify (needs API key): run `-l prompting -e 3 mario-rossi` and check reasoning tokens grow low < medium < high; if flat, use another default (e.g. `nvidia/nemotron-3-ultra-550b-a55b:free`, also listing `reasoning_effort`) or show a non-free model
- [x] Default judge `google/gemma-4-31b-it:free` is smaller than the system under test, against advice at `validating:72` (also `rag:792`)
    - [x] @gciatto decide. Note: Nemotron 3 Super is 120B MoE with 12B _active_, Gemma 4 31B is dense and of a different family (avoids self-preference; `validating:72` says "possibly stronger"): not clearly weaker. Options: (a) keep, add one line at `validating:170` justifying it (different family, comparable active size, free, sees images); (b) default judge `nvidia/nemotron-3-ultra-550b-a55b:free` (stronger, but same family as SUT). Recommend (a); defaults in `lecture_validating/example1/test_letter_scoring.py:44`, `example1bis/evaluate_mlflow.py:38`, `lecture_rag/example5/test_generation.py:31`, `exercise1/test_slides_qa.py:57`

## `genai` (intro)

- [x] Add a roadmap slide mapping "What does an AI-powered application include?" (`:688`) onto lectures; skills, workflows, governance are missing from that list
    - [x] Fix: extend the list at `:690-711` with 7. _workflows_ (code-controlled flows/state machines → `../workflows/`), 8. _skills_ (packaged instructions/scripts → `../skills/`), 9. _governance_ (deployment, cost, AI Act → `../governance/`); then add a 2-col table slide "Roadmap" (component | lecture link) right after it, covering llmaas, prompting, validating, agents, rag, skills, workflows, governance — list split in two slides (pt. 1–2)
- [x] Concept slides miss structured outputs, skills, workflows/state machines
    - [x] Fix: after `## Concept: Prompt Templates` (`:715`) add 3 short concept slides, each 3–4 bullets + forward link: "Structured Outputs" (JSON schema-constrained answers → `../prompting/#/structured-output`), "Workflows" (code decides the flow, LLM fills steps → `../workflows/#/workflows-concept`), "Agentic Skills" (folders of instructions+scripts loaded on demand → `../skills/#/skills-concept`)
    - [x] @gciatto: text-only slides, or draw small SVG diagrams like the other `Concept:` slides? Recommend text-only now, diagrams later — text-only
- [x] Name and link the running example (row at `:582`) → `../prompting/#/running-example`
- [x] Add a governance teaser (cloud vs. local, cost, AI Act) e.g. near as-a-Service slides (`:115`) — appended as a fragment to the as-a-Service cost slide
    - [x] Fix: append to the cost slide (`:118-128`) a fragment "But: data leaves your premises, costs scale with usage, provider lock-in, and the AI Act/GDPR apply → alternatives: [on-premise](../llmaas/#/ollama), trade-offs in [governance](../governance/#/deployment-options), [regulation](../governance/#/regulation)"
- [x] "The GenAI workflow" (`:773`) = engineering lifecycle, clashes with "workflow" = code-controlled flow (`:545`, `:851`, `workflows`): rename slide "GenAI project lifecycle" (keep anchor `genai-workflow`, linked from `llmaas:62`)
    - [x] Fix: also rename "workflow" → "lifecycle" in `:775` text, `:780-781` bullets, `:786` "Peculiar activities in a typical GenAI lifecycle", `:805` "Example of GenAI lifecycle (pt. N)" (all parts), and link text in `llmaas:62` ("GenAI lifecycle"); `:580` link text "tender example" stays; keep `:851` "Workflow + Agent" (correct usage)
- [x] FM vs. PFM mixed (`:31` vs `:666`, `:692`, `:700`)
    - [x] Fix: define once at `:666` "Pre-trained foundation models (PFM, or simply FM)", then use "FM" everywhere (`:670`, `:674`, `:680-682`, `:692`, `:700`, `:704`, `:780-783`, `:795`, `:799`); "pre-trained" is redundant since all FMs are pre-trained
- [x] Floridi slide (`:612`): heading names intelligence/autonomy/agency, bullets don't map intelligence
    - [x] Fix: make bullets map 1:1 — "How __well__ does it solve problems? (_intelligence_)", "What can it __do__ / what state does it change? (_agency_)", "Who __controls__ when and why? (_autonomy_)"; merge the third bullet ("What state…") into agency
- [x] Prompt Templates table (`:717`, Lenny's) = prompt _patterns_, whereas `prompting` uses "template" = LangChain placeholders; reconcile wording
    - [x] Fix: retitle `:715` "Concept: Prompt Patterns", column header "Pattern template"; keep the closing `{placeholders}` bullet and add "→ prompt _templates_ (cf. [prompting](../prompting/#/langchain))"; `:671` definition of templates is already consistent
- [x] `prompting` never assesses genai's patterns (emotion prompting, style unbundling, synthetic bootstrap); role prompting endorsed without caveat (`prompting:72`; cf. Zheng et al., "Is 'A Helpful Assistant' the Best Role…?")
    - [x] Fix: in `prompting:72` Rationale add "(personas give little/no accuracy gain on factual tasks, cf. [Zheng et al., 2024](https://arxiv.org/abs/2311.10054); useful mostly for tone/context)"; below the `prompting:649` techniques table add a bullet: "Folk patterns (role playing, emotion prompting, …, cf. [genai](../genai/#/...)) have weak/inconsistent evidence (cf. [EmotionPrompt, Li et al. 2023](https://arxiv.org/abs/2307.11760) vs. [The Prompt Report](https://arxiv.org/abs/2406.06608)): measure, don't trust"
    - [x] Fix: add `{{< slide id="prompt-patterns" >}}` to genai `:715` so the link above resolves
- [x] `:710` evaluation = "LLM-as-a-Judge" only: say "deterministic scorers + LLM-as-a-Judge" (as in `validating:75`)
- [x] "Model-Context Protocol" (`:737`) → "Model Context Protocol"; "MCP protocol" (`:702`) redundant
    - [x] Fix: also the image alt at `:739`; `:702` → "via [MCP](…)"
- [x] Hugging Face Transformers listed as client library for as-a-Service models (`:695`): it's for local inference
    - [x] Fix: replace with [LangChain](https://docs.langchain.com/oss/python/langchain/overview) or [Hugging Face `huggingface_hub` InferenceClient](https://huggingface.co/docs/huggingface_hub/guides/inference) (actual aaS client); optionally add "(or local runtimes, e.g. Ollama, Transformers, cf. [llmaas](../llmaas/#/ollama))"
- [x] Four ChatGPT "don't train on my data" screenshots (`:186-214`): move to `governance` (`:204`) or shrink to one
    - [x] Fix: screenshots are also outdated (ChatGPT 4o) and in Italian UI on a UNIBO workspace account; keep only `no-learn-4.png` (the toggle) in one slide titled "Some solutions let you _opt out_ of training", add "(cf. [governance](../governance/#/regulation))", delete the other 3 slides and PNGs — kept pt. 4 only (no retake), deleted the other 3 PNGs
    - [x] @gciatto wants to keep only one screenshot, no need to update
## `llmaas`

### Errors
- [x] Example 2 stores `assistant> ` prefixes in history (`example2/repl_chat_openai_async.py:46-48`) ✓; slide's simplified version (`:1043-1050`) differs from real code
    - [x] Fix: in lab-snippets `master` (and merge to `exercises`), print `chunk.replace("\n", "\nassistant> ")` but append the raw `chunk` to `answer_parts`; same pattern in exercise solutions reusing it. Line count unchanged, so `:1029` range `21-58` stays valid; slide `:1043-1050` then matches
- [x] `ollama chat gemma4:e2b` → `ollama run` (`:176`) ✓
- [x] Ollama base URL needs `/v1` for OpenAI client (`:209`) ✓; also `governance:819`
    - [x] Fix: `:209` → `http://localhost:11434/v1`; `governance:819` → "(and `OPENAI_BASE_URL=http://localhost:11434/v1` for Ollama)"
- [x] `response_format` json_schema shape wrong, typed as str (`:899-902`); correct in `prompting:278`
    - [x] Fix: type `dict`; value `{"type": "json_schema", "json_schema": {"name": STR, "description": STR, "schema": {...}, "strict": BOOL}}` (name required); `strict` = constrained decoding guaranteeing schema adherence, not just "extra fields"
- [x] Response YAML not a real `chat.completion` (`:972-1001`): Responses-API fields, `tool_calls` lacks `type`/`function` nesting, `tool_call` → `tool_calls`, content + tool_calls with `finish_reason: stop`
    - [x] Fix: drop `request_id`, `tool_choice`, `seed`, `top_p`, `temperature`, `*_penalty`, `metadata`, `response_format` (request params, not response fields; move `top_p`/penalties to the request-param slides); keep `id, object, created, model, system_fingerprint, service_tier, choices, usage`
    - [x] Fix: `tool_calls: [{id: call_..., type: function, function: {name: get_current_time, arguments: '{"timezone":"Europe/Rome"}'}}]`, `content: null`, `finish_reason: tool_calls`; comment lists `stop|length|tool_calls|content_filter`; or show two choices (text/stop vs tool call)
- [x] Sync/async conflated with non-streaming/streaming (`:753-755`, `:762`)
    - [x] Fix: two orthogonal axes: sync (`OpenAI`, blocking call) vs async (`AsyncOpenAI`, coroutines, `await`); `stream=False` (whole response) vs `stream=True` (chunks); both clients support both. Say Example 1 = sync/non-stream, Example 2 = async/stream by choice
- [x] Open Router routing described wrongly (`:437-441`): sorting is among providers of a model; throughput = tokens/s; `:exacto` is a model suffix
    - [x] Fix: rewrite as "for a given model, OR picks among the _providers_ serving it; default = load-balanced, price-weighted; override with `provider.sort` = `price` | `latency` | `throughput` (tokens/s), or suffixes `:floor` (price), `:nitro` (throughput), `:exacto` (providers with better tool-calling quality, e.g. `moonshotai/kimi-k2-0905:exacto`)". Cite <https://openrouter.ai/docs/guides/routing/provider-selection>, <https://openrouter.ai/docs/guides/routing/model-variants/exacto>
- [x] Check `provider/*`, `openai/gpt*` wildcards as `model` names (`:435-436`)
    - [x] Fix: wildcards are NOT valid `model` values: they are `allowed_models` patterns of the Auto Router (`model="openrouter/auto"`, `plugins=[{"id": "auto-router", "allowed_models": ["anthropic/*", "openai/gpt-5*"]}]`, or Settings > Plugins). Merge into the `openrouter/auto` bullet; cf. <https://openrouter.ai/docs/guides/routing/routers/auto-router>
- [ ] curl request model ≠ response model/cost (`:492` vs `:505`, `:539`)
    - [ ] Fix: re-run the `:492` curl with `nvidia/nemotron-3-super-120b-a12b:free` and paste real output (cost 0, provider Nvidia/other); don't switch curl to `gpt-5-nano` (paid, clashes with "no credit needed" `:460`) — left for the final re-run with your keys
    - [ ] @gciatto says we will do a finall re-run of all exercises with his keys later
- [x] Ollama response YAML malformed nesting (`:232-249`)
    - [x] Fix: indent `message:` at the same level as `index:` (2 spaces after `- `), its fields +2 under it, `finish_reason` aligned with `message`; indent `prompt_tokens/completion_tokens/total_tokens` under `usage:`
- [x] KV cache description wrong + garbled "the neural has processes" (`:272`)
    - [x] Fix: "the __key-value (KV) cache__ stores, for every layer, the attention _keys_ and _values_ computed for each token processed so far (prompt + generated)..."; size ∝ layers × context length × KV heads × head dim
- [x] Response called "a dictionary" (`:764`): it's a pydantic `ChatCompletion`
- [x] "Responses mostly OpenAI/Azure-native" possibly stale (`:648-649`), contradicts table `:1188`
    - [x] Fix: "Chat Completions: supported nearly everywhere; Responses: native in OpenAI/Azure, increasingly mirrored (OpenRouter beta, Ollama ≥0.13.3 stateless only, vLLM) but often partially" — consistent with `~` in the table
- [x] Ollama unsupported features mis-exemplified (fine-tuning, custom models) (`:208`)
    - [x] Fix: per <https://docs.ollama.com/api/openai-compatibility>: unsupported request fields `tool_choice`, `logit_bias`, `user`, `n`; `/v1/responses` stateless only; no files/batches/fine-tuning endpoints
- [x] Ollama Cloud prices in USD, not € (`:129`)
- [x] Example 2 sample output (`:1080-1102`) is a hallucinated translation: flag it as such or replace
    - [x] @gciatto wants to keep and add a fragment "notice: these are _not_ Longfellow's lines (real l.3: 'For the straightforward pathway had been lost'): a confident _hallucination_" (recommended: free teaching moment). Reference to actual lines: https://en.wikisource.org/wiki/Divine_Comedy_(Longfellow_1867)/Volume_1/Canto_1 as proof

### Inconsistencies
- [x] Open Router limits URL differs: `docs/api/reference/limits` (`:414`) vs `docs/api_reference/limits` (`free-access:66`, `:191`)
    - [x] Fix: use `https://openrouter.ai/docs/api_reference/limits` everywhere (the `:414` one 308-redirects to it)
- [x] API key format `sk-or-XXXX` (`:480`) vs `sk-or-v1-...` (`:823`, landing `:164`)
- [x] Gemini "structurally different" (`:685-691`) but `free-access:14,63,73` relies on its OpenAI-compatible endpoint
    - [x] Fix: add to pt. 4 Portability: "...but Google also exposes an [OpenAI-compatible endpoint](https://ai.google.dev/gemini-api/docs/openai) (`https://generativelanguage.googleapis.com/v1beta/openai/`), with a subset of features"
- [x] Overhead 10–20% (`:276`) vs 10–30% (`:295`)
    - [x] Fix: `:276` is runtime overhead only, `:295` includes KV cache; reword `:295` to "add ~10–20% runtime overhead, plus the KV cache (grows with context: several GB at 32k+ tokens)"
- [x] "2× 80 GB" row understates capacity (`:377`)
    - [x] Fix: "≤ 70B at 16-bit (140 GB, tight), ~120B+ at 8-bit, larger with 4-bit or MoE"
- [x] Deployment options: 2 here (`:19-25`) vs 3 in `governance:92-98` (hosted open weights missing here)
    - [x] Fix: add under on-cloud: "+ incl. _open-weights_ models hosted by third parties (e.g. OR, HF Inference): cf. [three options](../governance/#/deployment-options)"
- [x] `openai.AsyncClient` (`:759`) vs `AsyncOpenAI` in code
- [x] List numbering skips 6 (`:840`); 2-space indentation at `:1015-1021`

### Redundancies / placement
- [x] Capabilities listed 3 times (`:614-632`, `:643-647`, table `:1176-1188`); pt. 1–6 (`:636-713`) vs table
    - [x] @gciatto: (a) keep `:614-632` (generic expectations) + table — done: pt. 1 capabilities reduced to one line linking the table
- [x] Chat Completion concept (`:567-581`) restated in "ingredients" (`:757-769`)
    - [x] Fix: shorten ingredients 3–6 to SDK-specific facts (types, method names, doc links), replacing statelessness prose (`:767-769`) with "(cf. [Chat Completion concept](#/chat-completion-concept))"
- [x] OR free limits duplicated with `free-access:66`: link `../free-access/#/free-tiers`
- [x] LangChain promised in "Reference technologies" (`:729`, `:741-743`) but introduced only in `prompting`
    - [x] Fix: drop LangChain from `:729`; in `:741-743` add "(used from the [next lecture](../prompting/#/...) on)" with the prompting anchor where LangChain is introduced
- [x] `custom` grammar tool example (`:927-938`, `:959`) too advanced / unused later
    - [x] Fix: remove the `custom` dict from the code block and `:959`; replace with one line "OpenAI also supports `custom` tools with free-text/grammar inputs (rarely supported by other providers)"
- [x] "Focus on Anthropic's Client Library" (`:1116`) should be `#`, not `##`

### Holes
- [x] No link to Free Access appendix
    - [x] Fix: in OR pt. 1 (`:413`) and Example 1 setup, add "other free options: [Free Access appendix](../free-access/)"
- [x] Explain `e2b` / effective parameters (`:89-93`), and why `ollama ps` shows 7.2 GB (`:388`)
    - [x] Fix: add to `_size_`: "`e2b`: _effective_ 2B (Gemma 3n/4: 2.3B compute, 5.1B incl. per-layer embeddings)"; at `:388` note size = all weights (5.1B, vision/audio encoders, higher-precision tags: Ollama lists 4.6–7.5 GB) + KV cache
    - [x] @gciatto: output is "illustrative": verify 7.2 GB with a real `ollama ps` on your machine — verified on this Mac: `ollama ps` shows 1.7 GB (7.2 GB is the on-disk size from `ollama list`); slide updated with the real output
- [x] Forward pointer to embeddings endpoint (used in `rag:147`)
    - [x] Fix: in pt. 2 (`:655`) add "(`/v1/embeddings` turns text into vectors: cf. the [RAG lecture](../rag/))"
- [x] How to pick a local model supporting tools / structured output (Ollama tags, OR "supported parameters")
    - [x] Fix: add 2 bullets to Model zoos pt. 2: Ollama zoo `tools`/`thinking`/`vision` badges (filter <https://ollama.com/search?c=tools>); OR models page filter "Supported parameters" (`tools`, `structured_outputs`, `response_format`)
- [x] HTTP 429, `Retry-After`, usage/cost fields before Exercise 2
    - [x] Fix: add one slide before `#/exercise-retry` (or into "About Chat Completion API" pt. 4): status codes 400/401/402/429/5xx, `Retry-After` header, `openai.RateLimitError`/`APIStatusError`, SDK `max_retries`, `usage` + OR `usage.cost` — new slide `#/api-errors` before Exercise 2
## `free-access`

- [ ] Env-var advice (`:86`) omits `OPENAI_MODEL` (default is OR-only)
    - [ ] Fix: reword `:86` to "...just set `OPENAI_BASE_URL`, `OPENAI_API_KEY`, __and__ `OPENAI_MODEL` (the default, `nvidia/nemotron-3-super-120b-a12b:free`, exists only on OpenRouter; pick an ID from the listing above)"
- [ ] `free_providers.py` uses per-provider env vars vs `OPENAI_*` everywhere else: add table provider → `OPENAI_BASE_URL` + suggested `OPENAI_MODEL` (incl. Ollama `http://localhost:11434/v1`)
    - [ ] Fix: base URLs are already in the excerpt (`free_providers.py:12-21`); add one sub-bullet under `:86` with a worked example, e.g. `OPENAI_BASE_URL=http://localhost:11434/v1 OPENAI_API_KEY=unused OPENAI_MODEL=gpt-oss:20b` (Ollama) and `OPENAI_BASE_URL=https://api.groq.com/openai/v1 OPENAI_MODEL=openai/gpt-oss-20b` (Groq)
    - [ ] @gciatto: (a) that one-bullet example (recommended: smallest, no stale model table); (b) full provider→URL+model table slide (model IDs go stale); (c) also make `free_providers.py` print the matching `export OPENAI_*=...` lines after listing models (lab-snippets `master` + merge into `exercises`; recheck `from="12" to="21"`)
- [ ] "4-bit cuts memory ~4×" (`:157`) vs `llmaas:289` (~3.3×)
    - [ ] Fix: `:157` → "cuts memory by ~3× w.r.t. 16-bit (`Q4_K_M` ≈ 4.9 bits/weight, cf. the table in [LLM-as-a-Service](../llmaas))": 16/4.9 ≈ 3.3, consistent with llmaas table (7B: 14 → 4.3 GB)
- [ ] Rule of thumb ranks local below free tiers (`:38`) while `:49`, `:51`, `:149` recommend local; Cohere _trial_ listed as free tier (`:67`) right after saying trials aren't
    - [ ] Fix (Cohere): not a contradiction in substance: Cohere "trial" keys don't expire, they're a recurring 1,000 calls/month, non-commercial quota; add "(despite the name: no expiry, non-commercial use only)" to the `:67` row
    - [ ] @gciatto: rule of thumb at `:38`: (a) state its criterion, "cheapest route _for API-scale volume_: ...", leaving local after free tiers; (b) move local before free tiers (matches `:49`/`:51`/`:149` and "only _durable_ free API"); (c) drop the ranking, keep only the "Which route" table. Recommended: (b) "grant → student credits → local model → free tier → trials"
## `prompting`

### Errors
- [x] "ReAct … agents, in the next lecture" (`:659`): next is `validating` ✓
- [ ] Example 4 "never exceeds the token budget" (`:1196`, alt `:1142`): checked after sending ✓ (`chat_with_compaction.py:51`); `keep_last` alone may exceed it; with `CONTEXT_BUDGET=300` (`:1232`) compacts every turn
    - [ ] Fix: in `chat_with_compaction.py` move the budget check (`:51-53`) *before* `llm.invoke(context())` (after appending the user msg); reword `:1196` to "keeps the context _within_ a token budget (best effort: the last `keep_last` messages are never dropped)"; drop `CONTEXT_BUDGET=300` at `:1232` (default 1000 matches the svg's "compaction every ~3 turns"); re-check `from`/`to` at `:1206`, `:1218`, `:1222`.
- [ ] `User`/`Post` example (`:166-190`, `:221`) uses defaults → not strict-mode compatible; real classes use `Optional` without defaults, unexplained
    - [ ] Fix: partly false positive: the `openai` SDK (`.parse`, also used by LangChain's `with_structured_output`) rewrites the schema making _every_ field `required` and dropping `default: null`, so `User`/`Post` works; still, add 1 bullet under the real classes (Example 1 pt. 2): "strict mode wants every field `required`: optional info is `Optional[...]` _without_ default (= must be present, may be `null`)", and note the YAML at `:221` is pre-rewrite.
- [ ] Token counting "offline via tiktoken" only (`:1175`): mention server-side counting endpoint
    - [ ] Fix: OpenAI cell → "`POST /v1/responses/input_tokens` (`client.responses.input_tokens.count(...)`), or offline via `tiktoken` (text only)", link [token counting guide](https://developers.openai.com/api/docs/guides/token-counting).
- [ ] Docs links: structured output (`:283`) → `with_structured_output` page; "runnables and LCEL" (`:683`) → v1 overview without LCEL
    - [ ] Fix: `:283` → `https://docs.langchain.com/oss/python/langchain/models#structured-output` (current link is about `create_agent(response_format=...)`); `:683` → `https://reference.langchain.com/python/langchain-core/runnables/` (verify both anchors resolve before committing).
- [ ] Typo "commettee" in prompts (`letter_scoring_openai.py:21`, `letter_scoring_langchain.py:22`, shown at `:315`, `:459`)

### Inconsistencies / redundancies / placement
- [ ] Outline (`:23`) order ≠ deck order (exercises interleaved; running example missing)
    - [ ] Fix: rewrite outline as deck order: anatomy → [running example](#/running-example) → structured outputs (Ex 1, 1bis, [Exercise 1](#/exercise-checklist)) → techniques (Ex 2) → reasoning (Ex 3) → [Exercise 2](#/exercise-id-documents) → context mgmt (Ex 4); drop item 6. Redo after deciding the context-mgmt move below.
- [ ] "What's next" overlaps `validating:640-644` (agents announcement): drop from prompting
- [ ] Three overlapping views of format specification (`:95-129`, `:99`, `:254-269`): merge
    - [ ] @gciatto: (a) keep svg TL;DR + collapse "How to represent" items 1-3 into one line (NL / example / schema), keeping 4-5 as lead-in to Pydantic; (b) also delete the svg. Recommend (a): "represent" vs "enforce" (`:254`) are orthogonal, keep both.
- [ ] Generic `User`/`Post` Pydantic (`:135-246`, 3 slides) then repeated on real classes: cut to one slide
    - [ ] Fix: keep pt. 2 code (with `Field(description=...)`), drop pt. 1 and the YAML-schema slide (or shrink the YAML to the `User` part only); `Field(...)`/default explanation stays.
- [ ] `example1bis/letter_scoring_langchain.py:30-74` duplicates Example 1 classes instead of importing (drift risk)
    - [ ] Fix: replace `:20-74` with `from snippets.lecture_prompting.example1.letter_scoring_openai import general_instructions, scoring_instructions, ApplicantInfo, AuthorInfo, LetterInfo` (as `governance/exercise1/compare_models.py` already does; re-export keeps `exercise1` import working); use `general_instructions` in the template (fixes typo once); re-check ranges at `:453`, `:459`, `:472` and `validating` refs.
- [ ] Context management (`:1113-1259`) at the end, after exercises: move after reasoning models (or concept + caching to `llmaas`)
    - [ ] @gciatto: (a) move the whole context-mgmt column + Ex 4 right after Ex 3 (before Exercise 2), so the deck ends on an exercise; (b) move concept + caching to `llmaas`, keep Ex 4 here; (c) leave as is. Recommend (a): cut-and-paste only, no cross-lecture link churn.
- [ ] Example 4 appends summary into system message (`chat_with_compaction.py:27`) → breaks prompt cache: make it explicit; prompt hard-coded
    - [ ] Fix: put the summary in a separate message after the fixed `SystemMessage(instructions)` (e.g. `SystemMessage(f"Summary of the earlier conversation:\n{summary}")` or a user msg), so the instructions prefix stays cacheable; add a sub-bullet at `:1204` saying so; read `instructions` from `SYSTEM_PROMPT` env var (default unchanged) so the ">1024 tokens" caching experiment at `:1238` is doable.

### Holes
- [ ] What happens when a model lacks `json_schema` support; fallback `method="function_calling"` / `"json_mode"`
    - [ ] Fix: bullet on enforcement pt. 2 (`:283` area): "model without `json_schema`? → provider returns 400 or ignores it; in LangChain `with_structured_output(Cls, method="function_calling")` (tool trick) or `method="json_mode"` (schema must then be in the prompt); on OpenRouter filter models by `structured_outputs` support / `provider.require_parameters=true`".
- [ ] Prompt injection (`:73`): forward link to `../agents/#/security`
- [ ] Prompts as artifacts: versioning, files, prompt registries (genai:697 promises "text files")
    - [ ] Fix: one slide after best-practices landscape (`:85`): prompts as code: files (`.md`/Jinja) in git, loaded via `ChatPromptTemplate.from_template(Path(...).read_text())`, versioned + tested (→ `validating`); registries: [LangSmith Prompt Hub](https://docs.smith.langchain.com/prompt_engineering), [Langfuse prompt mgmt](https://langfuse.com/docs/prompt-management), [MLflow Prompt Registry](https://mlflow.org/docs/latest/genai/prompt-registry/).
    - [ ] @gciatto: also refactor lab-snippets to load prompts from `prompts/*.md` files? Recommend no (slide-only): keeps snippets readable as single files.
- [ ] Caching: Anthropic cache writes cost extra; OpenAI discount varies (`:1149`, `:1176`)
    - [ ] Fix: `:1176` already says writes cost extra; fix `:1149` → "cached input tokens cost 10–50% of the price (OpenAI 50–90% off depending on model; Anthropic reads 0.1x but _writes_ 1.25x (5 min) / 2x (1 h) TTL)"; check current pricing pages before committing.
## `validating`

- [ ] Missing image `todo-mlflow-ui.png` (`:303`) ✓
    - [ ] @gciatto take the screenshot yourself (run `-e 1bis`, then `mlflow ui`, open the Evaluations tab of a run, expand one groundedness rationale; the alt text at `:303` describes the shot) and save it as `content/validating/mlflow-ui.png`; then rename the `src`.
- [ ] "Not unit tests but evaluations" (`:36`) vs pytest suite (`:135`, `:311`): clarify (assert on rates)
    - [ ] Fix: reword `:36` to "rather than _only_ unit tests (pass/fail on one run), we need __evaluations__ … they can still _run on_ unit-test frameworks (e.g. `pytest`), if assertions are on _rates_ or _thresholds_, not on single exact outputs". Optionally add a pointer to the flakiness bullet at `:218`.
- [ ] Exercise 2 TODO lists 4 fields, solution has 5 (`nationality`) (`:496`); set-of-words match also used for nationality (`:571`)
    - [ ] Fix: `:496` → "(name, nationality, date of birth, ID number, expiration date)", and `:499` → "_normalised_ match for names and nationality". In lab-snippets `exercise2/test_id_extraction.py`, rename `normalise_name` → `normalise_words` (the docstring stays). Fix `:571` to "names (and nationality): a __set__ of words". The line count is unchanged, so `from`/`to` ranges stay valid.
- [ ] Exercise formatting differs from `prompting` (solution links `:364`, `:523`; ⚠️ only here; pt1/pt2 vs single slide)
    - [ ] Fix: mostly a false positive. `prompting` is the outlier: it is the only lecture with `([here](#/…-solution))` and without ⚠️ (`prompting:549,559,1004,1016`), and every other lecture matches validating's `:364`/`:523` and "(pt. N)" titles. Remaining fix in validating: align `:376`/`:535` to the majority wording "> ⚠️ __Spoiler alert__: the _walkthrough_ of the solution of [Exercise N](#/exercise-…) is about to start". Align prompting in its own section.
- [ ] MLflow judge reads only `OPENAI_API_KEY`, system under test falls back to `input()` (`:254`)
    - [ ] Fix: in lab-snippets `example1bis/evaluate_mlflow.py`, import `api_key` too (line 17) and add `os.environ.setdefault("OPENAI_API_KEY", api_key)` before `judge_options`. Update the line-37 comment and `:254` ("the key is the same as the system under test's"). The new line shifts the ranges at `:244`, `:250`, `:260` (37–54 → 38–55, 57–64 → 58–65).
- [ ] Hole: sample size / repetitions / confidence intervals; comparing two versions fairly
    - [ ] Fix: add one slide after `#/llm-as-a-judge` titled "How much evidence?". With 3 letters, a 3/3 pass rate has a 95% Wilson CI of [0.44, 1], so report CIs ([Miller 2024, "Adding Error Bars to Evals"](https://arxiv.org/abs/2411.00640)). Repeat N runs per case. Compare versions _paired_ on the same cases (McNemar / paired differences), changing one factor at a time.
    - [ ] @gciatto decide placement: (a) a new concept slide (recommended), or (b) two bullets in `:36–49` plus a hint in Exercise 2 pt. 2.
- [ ] Hole: statistical scorers (BLEU, ROUGE, embedding similarity) listed (`:43`) never shown: forward link to `rag:709`
    - [ ] Fix: a forward link won't help, because `rag:709–728` covers recall@k/MRR and judge metrics, not BLEU/ROUGE/embedding similarity. Instead, add a sub-bullet at `:43`: "need a reference text; correlate poorly with human judgement on open-ended outputs (cf. [G-Eval](https://arxiv.org/abs/2303.16634)); not used here".
    - [ ] @gciatto decide: (a) caveat only (recommended), (b) add an embedding-similarity scorer to Example 1 bis for `relationship_with_applicant` (new code plus range bumps), or (c) drop the bullet.
- [ ] Hole: quantify judge agreement (accuracy, Cohen's kappa) (`:74`)
    - [ ] Fix: under "__validate the judge__" (`:74`), add a sub-bullet: "measure _agreement_ with human labels: raw accuracy, plus [Cohen's κ](https://en.wikipedia.org/wiki/Cohen%27s_kappa) = (p_o − p_e)/(1 − p_e), which discounts chance agreement (cf. [Thakur et al. 2024](https://arxiv.org/abs/2406.12624))". Optionally, Exercise 2's solution (`:603`) could print the agreement rate across cases instead of only asserting per case.
- [ ] Step 5 of Exercise 2 (`:503`) ≈ `governance` Exercise 1
    - [ ] @gciatto decide: (a) keep step 5 as a teaser, adding a backward link from `governance` Ex. 1 pt. 2 hints (`governance:829+`) to `../validating/#/exercise-id-tests` (recommended: the tasks differ, ID extraction vs letter scoring); or (b) drop step 5 and the second command at `:631`.
## `agents`

### Errors
- [ ] `create_agent` re-raises non-validation tool exceptions (langchain 1.4.3 / langgraph-prebuilt 1.1.0): fix code (`wrap_tool_call` middleware or `handle_tool_error=True`) or text at `:272`, `:356`, `:384`, `:790`, `:969`
    - [ ] Fix: confirmed (`ToolNode._default_handle_tool_errors` re-raises anything but `ToolInvocationError`), so the `ValueError`s raised by `get_current_time`, `exercise1/committee.py:22,51,86`, `exercise2/decisions.py:52,54` crash the run. `:272` (from scratch) is fine. In lab-snippets, pass `middleware=[ToolErrorMiddleware(on_error=lambda e, req: f"Error: {e}")]` (`langchain.agents.middleware`, already in 1.4.3) in `example1bis/agent_langchain.py:18`, `exercise1/agent_committee.py`, `exercise2/agent_decisions.py:36`; MCP tools (example2, exercise3) are fine, since the adapter turns `isError` into tool messages
    - [ ] Fix: then reword `:356`/`:384` as "fed back via `ToolErrorMiddleware` (by default only _argument_ validation errors are)", add a row/hint about it in the table at `:384`, re-check `code` line ranges in `:352` and `:790`/`:969`; add one offline test in `tests/test_agents.py` (a tool raising `ValueError` yields a `ToolMessage(status="error")`)
- [ ] Exercise 3 "lethal trifecta broken in the gateway" (`:1139`, `:1163`): only `fetch_*` taints (`exercise3/gateway.py:49`) ✓, letters are untrusted too (`:695`, Eve Mallory); taint `applications_read_letter` or soften; `:1081` calls `applications` only "private data"; `committee` profile exposes all three (`:1068`)
    - [ ] @gciatto decide: (a) make `UNTRUSTED = ["fetch_*", "applications_read_letter"]` (match with `any(fnmatch(...))`), add a case to `tests/test_agents.py:94ff`; side effect: every invite after reading a letter is refused, i.e. Exercise 2's flow and "trajectory tests pass unchanged" (`:1087`) break; (b) keep code, soften `:1139`/`:1163` to "broken for _Web_ content; letters remain untrusted, covered only by human approval of `send_email`" and fix `:1081` ("`applications` reads private data _and_ untrusted letters"). Recommend (b): honest, no cascade of changes
    - [ ] Note: MCP spec 2026-07-28 removed protocol-level sessions, so taint keyed on `id(get_context().session)` (`gateway.py:66`) won't survive a stateless SDK; add a code comment + one-line caveat in the slide
- [ ] "All three tools harmless, read-only" (`:170`): `web_search` exfiltrates queries, contradicts `:696`
    - [ ] Fix: reword `:170` to "all three tools are _read-only_ (no side effects on the world), yet `web_search` _sends_ the query to a third party, and brings _untrusted_ text into the context (cf. [security](#/security))"
- [ ] `recursion_limit` ≠ `max_steps` (`:355`, `:383`): 2 supersteps per step; `GraphRecursionError` uncaught (`agent_langchain.py:34`)
    - [ ] Fix: `:355` → "`recursion_limit` bounds graph _supersteps_ (≈ 2 per model+tools round, so 20 ≈ 10 steps); exceeding it raises `GraphRecursionError`"; table `:383` → "`recursion_limit` (≈ 2× steps)"; alternatively use `ModelCallLimitMiddleware(run_limit=10)` to mean real steps. In lab-snippets, wrap `invoke` in `try/except GraphRecursionError` (`example1bis/agent_langchain.py:34`, `example2/agent_mcp.py:34`, `exercise1/agent_committee.py:39`) printing "AI: step limit reached"
- [ ] ARC-AGI-3 "< 1% (March 2026)", "0% alone vs 97% with harness" (`:595`, `:600`): date, source, re-check
    - [ ] Fix: "< 1%" is correct as "at release" (tech report abstract: "as of March 2026, below 1%"; report dated 22 Apr 2026, also [arXiv:2603.24621](https://arxiv.org/abs/2603.24621)); append "; best verified: Claude Opus 5, 30.2% (Jul 2026, [ARC Prize](https://arcprize.org/results/anthropic-claude-opus-5))" and align `governance:714`
    - [ ] Fix: `:600` is accurate but misread: arXiv v2 §4 says "in a variant of TR87, Opus 4.6 scores 0.0% with no harness and 97.1% with the Duke harness, yet in BP35 0.0% under both". Cite arXiv §4, name Opus 4.6/TR87, add the BP35 half, and reword the moral to "a hand-crafted harness can make or break a task, but does not _generalise_" (ARC's own point)

### Inconsistencies / redundancies / placement
- [ ] Tools landscape (`:200`) lacks OpenAI Responses; "Chat Completion" vs "Chat Completions"
    - [ ] Fix: rename to "OpenAI (Chat Completions)"; add row "OpenAI (Responses)": `tools=[{type: "function", name, description, parameters, strict}]` (flat, no `function` wrapper) | output item `{type: "function_call", call_id, name, arguments}` (JSON string) | input item `{type: "function_call_output", call_id, output}` | `tool_choice` as Chat Completions | [link](https://developers.openai.com/api/docs/guides/function-calling) (same page, Responses tab)
- [ ] `:66-78` repeats `genai:597-618` (LLMs not agents, Floridi): one-line recall
- [ ] `:84-95` repeats `genai:516-546` (spectrum, least autonomy): frame as recall
- [ ] `:401-416` MCP concept repeats `genai:737-744`: keep N+M, JSON-RPC, transports
- [ ] `:198-204` duplicates `llmaas:1185` tools row
    - [ ] Fix: keep the agents table (the detailed one); add above it "> Recall the _Tools_ row of the [API comparison](../llmaas/#/...)", and leave `llmaas:1185` as is (one-line teaser forward-linking `../agents/#/tools-examples`)
- [ ] `:584-602` benchmarks overlap `governance:706-728`: one home
    - [ ] @gciatto decide: (a) agents keeps the _agentic_ table (GAIA, WebArena, SWE-bench, τ-bench, ARC-AGI-3), governance keeps only general/saturation + one-line link `../agents/#/agentic-benchmarks` for ARC-AGI-3; (b) move all to governance. Recommend (a): drop ARC-AGI-3 bullet at `governance:714` in favour of the link
- [ ] `:716` repeats `genai:625` "LLMs propose, software verifies": mark as recall
- [ ] `:643-650` plan before acting overlaps `workflows:477ff`; planning section (`:616-650`) placement
    - [ ] @gciatto decide: keep the planning section in agents (workflows `:28` and `:483` already recall `../agents/#/planning`), but shrink `:643-650` to 2 bullets (explicit plan artefact + irreversible steps) ending "→ [plan-and-execute](../workflows/#/plan-and-execute)"; alternatively move `:643-650` wholesale into workflows. Recommend shrink. Either way, add `{{< slide id="plan-before-acting" >}}` and point workflows `:483` to it (now `#/planning` hits "Can LLM agents plan?")

### Holes
- [ ] Strict tool arguments (OpenAI `strict: true`, Anthropic strict tool use) for `:209`
    - [ ] Fix: add sub-bullet under "Different reliability" (`:209`): "_strict_ mode makes arguments _always_ schema-valid via constrained decoding: OpenAI `strict: true` (needs `additionalProperties: false`, all fields `required`), Anthropic `strict: true` on the tool; LangChain `bind_tools(..., strict=True)`; cf. [structured outputs](../prompting/#/structured-output)". Valid ≠ correct: still validate values in code
- [ ] Too many tools: tool search, deferred loading, code-calling MCP (`:182`; link skills' progressive disclosure)
    - [ ] Fix: one new slide after "Writing good tools": problem (dozens of MCP tools ⇒ thousands of tokens, worse choices); remedies: tool search + `defer_loading: true` ([Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool); OpenAI Responses `tool_search`, verify), client-side selection (LangChain `LLMToolSelectorMiddleware`), [code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) (tools as code APIs); "same idea as skills' [progressive disclosure](../skills/)"
- [ ] Provider-hosted (server-side) tools vs client-executed
    - [ ] Fix: add bullet (or 2-column mini-table) after the landscape table: _client_ tools = you execute them (all of this lecture); _server_ tools = provider executes, results come back already in the response: OpenAI Responses `web_search`, `file_search`, `code_interpreter`, remote `mcp`; Anthropic `web_search`, `web_fetch`, code execution; Gemini `google_search`, `code_execution`, `url_context`. Trade-off: no code, but no control on validation/logging, data leaves to provider, lock-in
- [ ] OWASP Top 10 for Agentic Applications (Dec 2025) (`:673`)
    - [ ] Fix: append to `:674`: "and the [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (Dec 2025): goal hijack, tool misuse, identity & privilege abuse, supply chain, unexpected code execution, memory/context poisoning, ..." (ASI01–ASI10; verify wording against the PDF)
- [ ] MCP risks: tool poisoning, rug pull (`:515`); client features (sampling, elicitation, roots); `:714` links `draft` spec
    - [ ] Fix: `:515` Trust cell → add "_tool poisoning_ (malicious instructions in descriptions), _rug pull_ (descriptions change after approval: pin/hash them)". `:714` → `https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices` (current stable is 2026-07-28; redirects fine)
    - [ ] Fix: spec 2026-07-28 _deprecates_ Roots, Sampling, Logging (SEP-2577), removes sessions/`initialize` (stateless), and moves elicitation to Multi Round-Trip Requests: mention only elicitation (human input mid-call) + a one-liner on statelessness at `:401-416`; don't teach sampling/roots ([changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog))
## `rag`

- [ ] "Recall the technique selection of the governance lecture" (`:112`): forward reference ✓
    - [ ] Fix: governance comes after rag, so "Recall" is wrong. Reword to "Cf. the [technique selection](../governance/#/technique-selection) slide of the _governance_ lecture (later in the course): ..." (anchor exists, `governance:594`)
- [ ] Contextual retrieval misdescribed (`:437`): Anthropic's uses LLM-written chunk context
    - [ ] Fix: split the bullet: "prepend the document's title and section (cheap, deterministic); or, as in Anthropic's [contextual retrieval](...), have an _LLM_ write a short (50–100 token) context situating each chunk in its document, prepended before embedding _and_ BM25 indexing (−35% to −49% failed retrievals in their tests; costly: one LLM call per chunk, mitigated by prompt caching)"
- [ ] "with `JUDGE_MODEL` set" (`:792`): has a default, say "optionally"
- [ ] `:78-89` re-explains `genai:749-751`: make it a recall
    - [ ] Fix: retitle `:78` "RAG: the general concept (recall)" and open with "Recall the [RAG concept](../genai/#/...) from the genai lecture" (add a `slide id` to `genai:749` if missing); keep the 3-step list, as it is the lecture's backbone, but cut `:87-89` to one line or move hallucination caveats to `:112` slide
- [ ] Memory governance repeated 3× (`:64-68`, `:445-455`, `:815-820`)
    - [ ] Fix: keep the full list once at `:64-68` (concept); at `:445-455` turn the `→ citations/staleness/access control` arrows into back-links "(cf. [memory governance](#/memory))"; at `:815-820` keep only the security-specific mitigations (access control at retrieval, delimiting, read-only, logging) and drop the provenance restatement into a back-link
- [ ] CoALA memory types (`:52-68`): say episodic/procedural out of scope, or move to `agents`
    - [ ] @gciatto decide: (a) keep in rag, adding one line "this lecture: _semantic_ memory only; procedural → [skills](../skills/), episodic → not covered (cf. hole below)"; (b) move the CoALA slide to `agents` (near `agents:71`, "memory" in the agent equation) and recall it here. Recommend (a): cheapest, and `skills:43` already back-refers to "semantic memory, e.g. RAG"
- [ ] Hole: long-term agent memory (LangGraph `Store`, Mem0/Letta, memory poisoning) never shown
    - [ ] @gciatto decide: (a) one landscape slide after `:68` or before Security: _writable_ episodic/semantic memory — LangGraph `Store` (namespaced KV + semantic search), [Mem0](https://github.com/mem0ai/mem0), [Letta](https://www.letta.com/) (ex-MemGPT, [Packer et al., 2023](https://arxiv.org/abs/2310.08560)) — plus a security bullet on memory poisoning ([AgentPoison, Chen et al., 2024](https://arxiv.org/abs/2407.12784)); (b) a full example in lab-snippets (`lecture_rag/example6`, committee remembers past decisions); (c) leave out. Recommend (a)
- [ ] Hole: multimodal / layout-aware retrieval for PDFs (`:923`)
    - [ ] Fix: after `:923` add a bullet "Better: _layout-aware_ parsers ([Docling](https://github.com/docling-project/docling), [Unstructured](https://github.com/Unstructured-IO/unstructured)) keep titles, tables, links; or skip text extraction and embed page _images_ ([ColPali, Faysse et al., 2024](https://arxiv.org/abs/2407.01449))". Optionally mirror it as a row/bullet in the chunking slide (`:431-435`)
- [ ] Hole: synthetic gold-set generation (`:777`)
    - [ ] Fix: add a sub-bullet at `:777`: "larger gold sets can be _synthesised_ by an LLM from the corpus (e.g. [Ragas test-set generation](https://docs.ragas.io/), DeepEval's [`Synthesizer`](https://deepeval.com/docs/synthesizer-introduction)), then _reviewed_ by humans: generated questions tend to reuse the chunk's own words, inflating recall" (ties to `gold.yml` header line 4)
- [ ] Hole: embeddings invertible; remote embedding APIs = data leaves premises (only Pinecone noted, `:260`)
    - [ ] Fix: add to the embedding-provider slide (near `:166-170`) and/or Security (`:812`): "embeddings are _not_ anonymised: text can be largely reconstructed from them ([Vec2Text, Morris et al., 2023](https://arxiv.org/abs/2310.06816): 92% of 32-token inputs recovered exactly); a remote embedding API (or SaaS store) means the _corpus_ leaves your premises: treat vectors as the documents they encode"
- [ ] "271 slides of 8 lectures" (`:955`): say gold set is pinned to that release
    - [ ] Fix: append "(release `2026.10.08`, the one `gold.yml` is pinned to)" at `:955`; if the default `--tag latest` now yields different counts, rerun `index.py --tag 2026.10.08` to confirm 271/8
## `skills`

- [ ] "MCP server: schemas of all tools, always" (`:77`, `:107`): outdated (deferred loading)
    - [ ] Fix: `:77` cell → "schemas of all its tools, at each step (unless the harness _defers_ them, e.g. Claude Code's tool search: names only, schema fetched on demand)"; `:107` "Loaded" → "always (names; schemas on demand with tool search, default in Claude Code)". Source: https://code.claude.com/docs/en/mcp ("Scale with MCP tool search").
- [ ] "~100 vs ~30" lines (`:512`): Deep Agents version is 56 ✓
    - [ ] Fix: `agent_skills.py` is 112 lines, `agent_deepagents.py` 56: change the row to "~110 | ~55" (or "~2× fewer"), avoiding a misleading 3× ratio.
- [ ] Triggering cases "in agentskills.io format" (`:1094`): `triggers`/`should_trigger` is skill-creator format
    - [ ] Fix: confirmed (agentskills.io defines only `skill_name` + `evals[]` with prompt/expected_output/files/assertions). Reword `:1094`: "…`evals/evals.json` (outcome cases in the [agentskills.io](…) format; triggering cases, under `triggers`, in the style of Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator))".
- [ ] Hook "no writes outside `output/`, whatever the LLM says" (`:787`): bypassable via `Bash`
    - [ ] Fix: `privacy_guard.py` only checks `Write/Edit/MultiEdit/NotebookEdit`; `Bash` with `echo > /x`, `cp`, `python -c` passes (and the network regex misses e.g. `python -c "urllib…"`). Weaken `:787` Goal to "…blocks the agent's _file-writing_ tools outside `output/` and the obvious network routes" and add a bullet on the Example 4 slides: "a deny-list over shell commands is _best effort_: for real confinement, deny `Bash` or use a sandbox (cf. [agents security](../agents/#/security))".
    - [ ] @gciatto: decide whether to also harden the snippet (lab-snippets `example4/privacy_guard.py`: deny `Bash` altogether, or allow-list commands) — recommend keeping the code simple and stating the limit on the slide (teaches "a guard is only as good as its coverage").
- [ ] Hook command uses `$CLAUDE_PROJECT_DIR/snippets/...` (`:848`): requires project root = lab-snippets clone, say so
- [x] "Recall from intro: … Gemini CLI" (`:96`): `genai` never mentions it; Gemini CLI as full column in tables (`:243`, `:678`, `:719`, `:872`) though superseded
    - [x] Fix: `genai:233,477` list Claude Code, Codex, OpenClaw, Cursor, Copilot only; at `:96` drop "Recall from" for the extra ones ("e.g. … (cf. [introductory lecture](../genai/))") or add Gemini CLI/Antigravity CLI to the `genai:474-477` table.
    - [x] @gciatto: Gemini CLI columns/rows — (a) keep as is + the existing `antigravity.md` note, (b) rename to "Gemini CLI / Antigravity CLI" after checking Antigravity's docs for skills/hooks, (c) drop Gemini from tables. Recommend (a) for now (Gemini CLI still exists for enterprise/API users; it is the only one with `BeforeModel`, cited at `:733`, `:746`), revisit next A.Y. — kept (a)
- [ ] Copilot naming drifts (`:242`, `:677`, `:696`)
    - [ ] Fix: use "GitHub Copilot" at first mention (`:96`), then "Copilot CLI" vs. "Copilot (VS Code)" explicitly where they differ: `:242` "Copilot (CLI, VS Code)", `:677` "Copilot CLI" (the linked docs are CLI/coding-agent hooks), `:765`/`:750-755` already say "Copilot CLI" where it matters.
- [x] Rule of thumb "cf. governance" (`:84`): recall `agents#autonomy-spectrum` / `genai#genai-uses` instead
    - [x] Fix: replace "(cf. the [governance lecture](../governance/))" with "(cf. the [autonomy spectrum](../agents/#/autonomy-spectrum))"; optionally add "trade-offs summarised in [governance](../governance/#/…)" once that slide has an anchor (see item on `governance:647-655`).
- [ ] Hooks tables (`:668-686`, `:692-756`, `:775`): same metamodel said 2–3×, merge; per-harness event lists → appendix
    - [ ] @gciatto: structure — (a) keep landscape table (`:668`) + one "similarities/differences" slide, move "events per harness pt. 1–2" (`:692-736`) into a skippable vertical sub-deck or to the end of the lecture as appendix; (b) delete pt. 1–2 and link docs. Recommend (a); then keep "Same metamodel" only once (`:683`) and cut the repeat at `:775`.
- [ ] "One core, many adapters" twice (`:762-777`, `:912-913`)
    - [ ] Fix: keep the full explanation at `:767-770`; at `:912-913` shorten to "a concrete instance of [one core, many adapters](#/…)" (add a `{{< slide id="hooks-agnostic" >}}` anchor to the "Harness-agnostic hooks" slide and link it, instead of `#/hooks`).
- [ ] Skills-vs-alternatives table (`:72-79`) and `governance:647-655` don't link each other
    - [ ] Fix: add `{{< slide id="which-technique" >}}` to governance's "Which technique? Trade-offs" slide; add a bullet under `skills:84` "→ business-level trade-offs (cost, compliance, time-to-market) in [governance](../governance/#/which-technique)"; in governance, link the Skills row to `../skills/#/<anchor of :68 slide>` (add an anchor there, e.g. `skills-vs-others`).
- [ ] Subagents used (`:109`, `:468`, `:702`, `:911`) before `workflows` introduces multi-agent: add pointer/definition
    - [ ] Fix: in the `:109` row ("Subagents") add a one-liner: "an agent the main agent calls _like a tool_, with a fresh context, returning only its result (more in [multi-agent systems](../workflows/#/multi-agent))"; later mentions need no change.
- [ ] Hole: recall LangChain middleware (`agents:368-371`) as library-level hooks; qualify "no way to redact" (`:660`, `:746`)
    - [ ] Fix: on "Hooks are callbacks" add: "libraries have hooks too: LangChain [middleware](../agents/#/…) (before/after model or tool call, incl. PII redaction)"; qualify `:660`/`:746`: "…no way to redact the prompt _in that harness_ (libraries like LangChain/Deep Agents allow it via `before_model` middleware)". Needs an anchor on `agents` "Example 1 (bis) pt. 2" slide.
- [ ] Hole: Deep Agents `write_todos` missing (`:468`)
    - [ ] Fix: `:468` → "…a _planning_ tool (`write_todos`), a _virtual file system_ (…), _subagents_ (`task`), …" (built-in tools per https://docs.langchain.com/oss/python/deepagents/overview).
- [ ] Verify: `mcp_tool` handler, `onFailure: "block"` (`:674`, `:755`); Codex hooks URL (`:675`, `:696`); `metadata.include_tools` (`:245`)
    - [ ] Fix: verified 2026-10-12 — Claude Code handler types `command|http|mcp_tool|prompt|agent` ✓, `onFailure: "block"` ✓ (v2.1.295+, `command`/`http` only: add "for command/http hooks"); Codex `command`, `mcp_tool` ✓; Deep Agents `metadata.include_tools` ✓ (space-separated string). Codex URL `learn.chatgpt.com/docs/hooks` resolves, but use canonical `https://developers.openai.com/codex/hooks` (consistent with `:240` skills link).
## `workflows`

- [ ] `gemma4:12b` (`:556`, `:566`): likely nonexistent tag
    - [ ] Fix: none needed. `gemma4:12b` is listed on ollama.com/library/gemma4/tags (next to e2b, e4b, 26b, 31b)
- [ ] Orchestrator–workers illustrated with Example 3 = plan-and-execute (`:391`, `:440`)
    - [ ] Fix: in the patterns table (`:391`), point the running-example cell to the supervisor of [Example 4](#/multi-agent-example), where an LLM delegates ad-hoc sub-questions to the documents/regulations workers. At `:440`, change "(cf. Example 3)" to "(cf. the supervisor of Example 4)"
    - [ ] Fix: optionally add one line under plan-and-execute: "a static cousin of orchestrator–workers: the whole plan is fixed and validated before any worker runs"
- [ ] Ollama default context 4,096 (`:568`, also `llmaas:388`): check current docs
    - [ ] Fix: the docs (docs.ollama.com/context-length) now set the default by VRAM: <24 GiB → 4k, 24–48 GiB → 32k, ≥48 GiB → 256k. At `:568`, write "whose default context window is 4k tokens on machines with less than 24 GiB of VRAM". At `llmaas:388` the `ollama ps` output showing 4096 is still plausible; add a note with the VRAM rule and a link
- [ ] Misread grade "105510/110" (`:178`, `admission.py:59`) vs "1055/110" (`:979`) ✓
    - [ ] Fix: none needed. These are two different runs, and the slides say so ("in one of our runs" vs "in this run"). If you want, add "(a different misreading than [the one above](#/workflow-scratch))" at `:979` to show that the error is not reproducible
- [ ] A2A Agent Card "skills" ≠ Agent Skills (`:729`, `:802`, `:1270`): disambiguate
    - [ ] Fix: at `:729`, after "skills", add "(A2A _skills_ are advertised capabilities with an ID, a description, tags, and examples: they are __not__ the [Agent Skills](../skills/) of the skills lecture, i.e. no `SKILL.md` and no instructions)". At `:802` and `:1270`, write "A2A skills" instead of "skills"
- [ ] Plan-and-execute (`:479-489`) and IR principles (`:595-600`) restate `agents:643-650`, `:702-720`
    - [ ] Fix: on `:479-489`, keep only what is new (plan-and-execute vs ReAct, replanner) and turn the "structured plan + validation" bullets into a one-line recall: "recall: plans as structured outputs, validated in code ([agents](../agents/#/planning))". On `:595-600`, open with "Generalising [plan before acting](../agents/#/planning) beyond plans:" and keep the 4 principles as a short summary list
- [ ] Workflow vs agent pros/cons (`:76-81`) repeats `agents:86-95`: shorten
    - [ ] Fix: keep the agent-vs-workflow contrast sentence and the 4 bullets, each cut to one line (predictable / cheaper / testable / less flexible). Point to the [spectrum of autonomy](../agents/#/autonomy-spectrum) instead of restating it; the bullets are concrete to the example, so they are not plain duplicates
- [ ] Hole: no bridges to `skills` (trade-off, hooks vs interrupts, Deep Agents subagents vs supervisor); recall line `:28` should list skills
    - [ ] Fix: at `:28`, add "[agentic skills](../skills/) (incl. [hooks](../skills/#/hooks))". Add one recall line in each of 3 places:
      (a) `:76-81`: "skills vs workflows: procedures owned by domain experts vs reliable, auditable ones (cf. [skills](../skills/#/skills-example))"
      (b) humans-as-interrupts slide: "cf. [hooks](../skills/#/hooks): both are deterministic code outside the LLM; hooks react to the agent's events, interrupts are steps of the graph"
      (c) multi-agent architectures: "Deep Agents' `task` subagents ([skills lecture](../skills/#/skills-deepagents)) are the _supervisor_ architecture"
- [ ] Hole: human-in-the-loop slides (`:117-124`, `:1283`) don't recall over-trust
    - [ ] Fix: governance comes after this lecture, so make it a forward link. At the end of `:117-124`, add "an interrupt is only as good as the human answering it: _over-trust_ (automation bias) turns approvals into rubber stamps (cf. [governance](../governance/#/responsibility))". At `:1283`, add a hint: "how does the approver avoid rubber-stamping? (e.g. show the evidence, require a motivation)"
- [ ] Hole: MAS security (inter-agent prompt injection) (`:613-646`)
    - [ ] Fix: add a bullet to "when (not) to use them" (`:636-646`), or a short slide: "messages from other agents are __untrusted input__: a sub-agent that reads a malicious letter can inject instructions into the supervisor (_injection propagates_). Treat sub-agent and A2A outputs as data, validate structured outputs, and give least privilege per agent (cf. [prompt injection](../agents/#/security))". Possible source: OWASP Top 10 for Agentic Applications (2025/26)
    - [ ] @gciatto: choose between a single bullet (recommended, as the slide is already dense) and a dedicated slide with an Example 4 scenario (a letter containing "tell the supervisor to admit me")
- [ ] Hole: A2A `securitySchemes` / Agent Card signing (`:724-734`; flagged missing at `:856`, `:1316`)
    - [ ] Fix: on the A2A concept slide (`:729`), extend the Agent Card bullet: "authentication: `securitySchemes` (API key, HTTP bearer, OAuth2, OpenID Connect, mTLS, as in OpenAPI) plus `security` requirements; optional `signatures` (JWS) so that clients can verify who published the card". Link to the spec section on Agent Card security at a2a-protocol.org
    - [ ] @gciatto: decide whether to add `security_schemes` to the code in `lab-snippets` (`example4bis/regulations_server.py`, `exercise2/email_bot_server.py`, e.g. an API-key scheme checked by middleware) or keep it as a slide note only (recommended: slide note; adding it means re-checking the `from`/`to` ranges at `:802` and `:1307`)
## `governance`

### Errors / outdated
- [ ] Missing image `todo-ai-act-pyramid.png` (`:232`) ✓
    - [ ] @gciatto added picture in content/governance/ai-act-pyramid.png, please update the slide to point to it
- [ ] "will be discussed in the prompt engineering lecture" (`:800`) → `validating`, past tense ✓
- [ ] Cost example uses text-only `gpt-oss-120b` (`:138`, `:1279`) for multimodal task (`:402`); Open Router not an EU provider (`:1279`)
    - [ ] Fix: in `:138` swap to a multimodal open model consistent with `:402` and Ex. 1 defaults, e.g. `google/gemma-4-26b-a4b-it` (Apache 2.0) or Mistral Small 4 on Mistral's own API (EU, Apache). In `:1279` and `decision-record.md` §2 (lab-snippets master, then merge into `exercises`), name an EU host (e.g. Mistral La Plateforme, Scaleway or OVHcloud AI Endpoints) and drop Open Router.
    - [ ] @gciatto: pick the model+host pair (rec.: Mistral Small 4 on La Plateforme, since one EU vendor covers both) and re-check its Sept/Oct 2026 price; recompute "≈ $1" / "$1–10".
- [ ] Timeline misses Omnibus new Art. 5 prohibitions from 2 Dec 2026 (`:261-270`)
    - [ ] Fix: add row `| 2 Dec 2026 | new prohibitions (Art. 5(1)(ba)-(bb)): AI generating non-consensual intimate imagery / CSAM ("nudifiers"); end of Art. 50(2) marking grace period |`; merge it with the existing Art. 50 note (see next item).
- [ ] Art. 50 transitional period (`:268`): check OJ text of Reg. 2026/1744
    - [ ] Fix: per commentary (cypheron.cz, nicfab.eu), Art. 50 applies from 2 Aug 2026; only the Art. 50(2) _marking_ duty has until 2 Dec 2026 for systems placed on the market before 2 Aug 2026. Reword `:268` to "(Art. 50(2) marking: until 2 Dec 2026 for generative systems already on the market)".
    - [ ] @gciatto downloaded the html of the OJ text (Reg. 2026/1744) in content/governance/OJ_L_202601744_EN_TXT.html, so you can inspect it
- [ ] Art. 4 AI literacy amended by Omnibus (`:274`): say so
    - [ ] Fix: `:274` already uses the new wording ("support"); append "(as amended by the Omnibus: previously, they had to _ensure_ a sufficient level of literacy)". Only one secondary source reports the change: check the OJ text.
- [ ] 10²⁵ FLOPs presumption is Art. 51(2), not Art. 55 (`:253`, `:431`)
- [ ] METR "doubling every ~7 months" (`:718`): re-check (~4 months recently)
    - [ ] Fix: "doubling every ~7 months over 2019–2025, and faster (~4 months) since 2023/2024 (cf. live measurements)". Kwa et al. give 212 days; METR's updated post-2023 fits give ~130 days (TH 1.1).
    - [ ] @gciatto added picture screenshots and html from <https://metr.org/time-horizons> in content/governance (see new git files)
- [ ] "All Italian models 2–24B" (`:472`): Minerva 350M/1B/3B; 24B is a Magistral fine-tune
    - [ ] Fix: "Italian models trained from scratch range from 0.35B (Minerva) to 14B (Velvet); larger ones (e.g. ANITA-NEXT 24B) are _fine-tunes_ of foreign models: one or two orders of magnitude below the frontier". Also fix "2–24B" in `:519` (recurring issues) and "up to 7B" in the Minerva row (`:466`).
- [ ] "Medium 3.5 Modified MIT" (`:386`): verify
    - [ ] Fix: none needed. Mistral-Medium-3.5-128B (Apr 2026) is open-weights under a "modified MIT" license on HF, per several sources. Optionally link its HF LICENSE file to match the other rows.

### Inconsistencies / redundancies
- [ ] Ex. 2 Q1 frames University as deployer only (`:1197`) vs provider and deployer (`:1248`, `:252`)
    - [ ] Fix: in `:1197` replace "(as _deployer_)" with "(as _provider_ and/or _deployer_? cf. Art. 25)". The solution (`:1251`, decision-record.md §1) already answers both.
- [ ] Option A discarded for model changes (`:1283`): real issue is retirement (`:118`), snapshots exist
    - [ ] Fix: in `:1283` and decision-record.md §2, change the rationale to "Option A is discarded: pinned snapshots (cf. llmaas, `gpt-4o-2024-08-06`) are _retired_ on the vendor's schedule, forcing re-validation; data also leave the University". In `:1278` change Control to "low: snapshots can be pinned, but are retired by the vendor".
- [x] "Ordered by increasing effort" (`:598-608`) vs table (`:652-653`)
    - [x] Fix: the table rates Skills "fast" and Tools "medium", contradicting the list's order. Drop "ordered by increasing _effort_" and say "roughly in the order of this course". Or reorder: Prompting, Skills, RAG, Tools/agents, Workflows, Fine-tuning.
    - [x] @gciatto: choose wording change (rec.: it keeps the course order) — done while moving the slide to `rag`
- [ ] Ex. 1 rebuilds evaluation by hand instead of reusing DeepEval/MLflow (`:800`)
    - [ ] @gciatto: decide (a) keep plain `compare_models.py` and add one slide line justifying it ("frameworks score one system; here we compare N models × repetitions, with cost/latency"), or (b) port it to MLflow (one run per model in one experiment, reusing `lecture_validating/example1bis` scorers). Rec.: (a), cheaper; mention MLflow as the alternative.
- [ ] `:780-800` re-explains `validating:28-75`
    - [ ] Fix: shrink part 2 ("task-specific evaluation") to 2 bullets linking `../validating/#/` (general concept, LLM-as-a-Judge). Keep the benchmarks/leaderboards part, which `validating` does not cover.
- [ ] Model cards (`:693-695`) repeat `llmaas:58`
    - [ ] Fix: replace the model-card definition bullets with "(cf. [model cards](../llmaas/#/...))". Keep datasheets, system cards, the SVG, and the "what to look for" bullet. Add a slide id in llmaas if none exists.
- [ ] Walkthroughs restate body (`:127-146`, `:1154-1177` vs `:1274-1309`); Ovadia et al. cited twice (`:659`, `rag:114`); free-access local-model notes overlap licensing (`:392-417`)
    - [ ] Fix: in solution `:1274-1290` replace the restated cost numbers with "costs as in the [worked example](#/...)" plus only the decision. Ovadia: keep both (different lectures), fine. Free-access: replace the duplicated licence notes in the appendix with a link to `../governance/#/...` (licenses slide).

### Holes
- [ ] Sovereignty (`:444-525`): hard evidence of EU/Italy lag (AI Index model counts by origin, private investment, compute share, leaderboard ranks with date)
    - [ ] Fix: add one slide "The gap, in numbers", before "Italian initiatives". Use AI Index 2026 ch. 1 (notable models by country: US ≫ China ≫ EU) and ch. 4 (private AI investment by country, US vs EU vs Italy), plus the EU share of global AI compute (e.g. Epoch AI / TOP500). Add the best EU model's Arena / Artificial Analysis rank, with its snapshot date.
    - [ ] @gciatto downloaded the ai_index_report_2026.pdf in root, so you can extract the numbers and charts
- [ ] Art. 6(3) last subparagraph: profiling ⇒ always high-risk (`:1254`)
    - [ ] Fix: in `:1254` (and decision-record.md §1), add "and anyway, scoring candidates is _profiling_, so Art. 6(3) last subparagraph makes the system always high-risk". Optionally mention it on the risk-classification slide too.
- [ ] AI Act logging (Art. 26(6)) vs GDPR storage limitation
    - [ ] Fix: add a sub-bullet near `:182`: "logs kept ≥ 6 months (AI Act Art. 26(6)) contain personal data: GDPR storage limitation still applies. Define a retention period (e.g. the appeal window + 6 months), then delete or pseudonymise". Add the retention period to decision-record.md §6.
- [ ] Standards: CEN-CENELEC JTC 21, ISO/IEC 42001, NIST AI RMF
    - [ ] Fix: one bullet on the AI Act roles/timeline slide: "conformity in practice via _harmonised standards_ (CEN-CENELEC JTC 21, still being drafted, a reason for the Omnibus delay); management systems: ISO/IEC 42001:2023; outside the EU: NIST AI RMF 1.0 (2023) + GenAI profile (NIST AI 600-1, 2024)".
- [ ] L. 132/2025 delegated decrees status; sectoral articles (health Art. 7, work Art. 11)
    - [ ] Fix: on the national-law slide (`:282-290`) add "health: AI supports, the physician decides (Art. 7)" and "work: employers must _inform_ workers about AI use (Art. 11)". Also add "delegated decrees: two drafts approved in preliminary reading on 10 Jun 2026 (authorities' powers, AI training; police biometrics, civil/criminal liability); delegation expires Oct 2026".
    - [ ] @gciatto: check the Gazzetta Ufficiale for final adoption before the lecture.
- [ ] Providers' copyright indemnities / output ownership
    - [ ] Fix: add a sub-bullet under "Outputs" (`:417`): "proprietary vendors offer _copyright indemnities_ for outputs (e.g. Microsoft Copilot Copyright Commitment, Google's generative AI indemnification, OpenAI Copyright Shield, Anthropic's commercial terms), usually only for paid/enterprise tiers and with conditions; open-weights licenses give none". Cross-link to L. 132/2025 Art. 25 on human authorship.
- [ ] Energy / environmental footprint in trade-offs
    - [ ] Fix: add a row or bullet "Footprint" to the deployment comparison (`:110-122`): per-token energy is hidden in API prices; on-premise power use is measurable. Cite e.g. Luccioni et al., 2024 "Power Hungry Processing" (arXiv 2311.16863) and the AI Act Art. 53 / Annex XI energy-reporting duty for GPAI providers.

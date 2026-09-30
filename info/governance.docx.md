# Open Models and Licensing: A Governance Guide for LLM Engineers

**Status: 30 September 2026.** This report uses "open source AI"
narrowly where possible, distinguishing it from **open weights**.
Model/license status is checkpoint-specific: Gemma, DeepSeek, Mistral,
Teuken, and the former iGenius/Domyn portfolio all contain examples
where materially different licenses coexist across generations or
variants. [\[1\]](https://ai.google.dev/gemma/terms)

## Executive summary

- **"Open" is not a binary property of a model.** A released model can
  expose weights while withholding training data, data provenance,
  training code, hyperparameters, intermediate checkpoints, or even the
  exact recipe. Liesenfeld & Dingemanse therefore treat openness as a
  **multidimensional, graded property**, rather than equating
  downloadable weights with open source. The 2026 European Open Source
  AI Index operationalizes essentially the same idea across data, code,
  documentation, hardware, architecture, weights and licensing
  dimensions.
  [\[2\]](https://facctconference.org/static/papers24/facct24-120.pdf)
- **Open weights ≠ open source.** OSI\'s Open Source AI Definition 1.0
  requires the freedoms to use, study, modify and share the system,
  together with the preferred form for making modifications:
  sufficiently detailed **Data Information**, complete
  training/inference code, and model parameters under appropriate open
  licenses. It deliberately does **not** require publication of every
  training example.
  [\[3\]](https://opensource.org/ai/open-source-ai-definition)
- **OSI\'s data compromise remains disputed.** Releasing only
  information sufficient to reconstruct a substantially equivalent
  dataset makes OSAID more practicable when data cannot legally be
  redistributed, but it weakens exact reproducibility and data-level
  auditing. OSI explicitly made this trade-off; it should not be
  paraphrased as "OSI requires open training data."
  [\[4\]](https://opensource.org/ai/faq)
- **A permissive weight license is still not sufficient for full
  openness.** Qwen3, gpt-oss, Gemma 4 and the current Apache-licensed
  Mistral models are excellent examples: their weights can be modified
  and commercially redistributed under Apache 2.0, but the original full
  training datasets and end-to-end model-building pipelines are not
  generally published. OLMo 3 and Apertus go much further by publishing
  data/model-flow artifacts and training machinery.
  [\[5\]](https://huggingface.co/Qwen/Qwen3-14B)
- **The biggest recent licensing change for teaching purposes is Gemma 3
  → Gemma 4.** Gemma 3 remains under Google\'s custom Gemma Terms,
  including prohibited-use restrictions that cascade to downstream
  distributions; Gemma 4 is instead released under **Apache 2.0**.
  [\[6\]](https://ai.google.dev/gemma/terms)
- **Llama 4 remains open-weight, not OSI-open-source.** Redistribution
  requires notices and "Built with Llama"; certain distributed models
  trained using Llama materials or outputs must use a name beginning
  with "Llama"; entities above 700 million monthly active users require
  a separate Meta licence; and, unusually, the Llama 4 licence grants no
  model-use rights for its multimodal models to individuals domiciled or
  companies principally established in the EU, although end users of
  products incorporating them are carved out.
  [\[7\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
- **Derivatives inherit more than engineers often expect.** Gemma 3
  explicitly defines synthetic-output distillation as potentially
  creating a "Model Derivative"; Llama imposes downstream naming/notice
  requirements; and DeepSeek\'s R1 distill checkpoints inherit their
  Qwen or Llama base-model licences even though DeepSeek-R1 itself is
  MIT-licensed. [\[8\]](https://ai.google.dev/gemma/terms)
- **Under the EU AI Act, "free and open source" is an exemption, not a
  blanket exclusion.** For qualifying GPAI models, Article 53(2) removes
  the Article 53(1)(a) technical-documentation and 53(1)(b)
  downstream-information duties. It does **not** remove the Article
  53(1)(c) copyright-policy obligation or 53(1)(d) public
  training-content-summary obligation, and the exemption does not apply
  to GPAI models with systemic risk.
  [\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)
- **Europe now has several distinct sovereignty strategies rather than
  one "European LLM".** They range from highly reproducible public
  efforts such as Apertus and OpenEuroLLM, through multilingual EuroLLM
  and Teuken, to commercially developed Mistral and Domyn models. Italy
  additionally has Minerva, Velvet and the LLaMAntino/ANITA line. Their
  openness levels are substantially different.
  [\[10\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
- **For engineering, "Can I download it?" is the wrong licensing
  question.** Before committing to a model, record at least: exact
  checkpoint and licence version; commercial-use permission;
  fine-tuning/distillation/merging rights; hosted-service and
  redistribution conditions; geographic or scale restrictions;
  attribution/naming obligations; licences of training and fine-tuning
  datasets; data provenance; and the applicable AI Act role and
  model/system classification.
  [\[11\]](https://opensource.org/ai/open-source-ai-definition)

## What makes a model "open"

A useful engineering model is to treat a foundation-model release as a
**bundle of separately openable artifacts**. Downloadability of one
artifact---usually the weights---says little about the others. This is
the central insight behind Liesenfeld & Dingemanse\'s FAccT 2024
analysis and the later European Open Source AI Index.
[\[12\]](https://facctconference.org/static/papers24/facct24-120.pdf)

  -------------------------------------------------------------------------------------------------------------------
  Component            What a genuinely useful        Why engineers/researchers need it
                       release contains               
  -------------------- ------------------------------ ---------------------------------------------------------------
  **Weights /          Final weights; ideally         Allows local inference, fine-tuning, inspection and independent
  parameters**         intermediate checkpoints and   hosting. OSI expressly treats model parameters as part of the
                       optimizer state where useful   preferred form for modification.
                                                      [\[13\]](https://opensource.org/ai/open-source-ai-definition)

  **Inference code**   Architecture implementation,   Weights without compatible executable machinery may be
                       tokenizer/processor,           practically unusable or difficult to reproduce. OSI includes
                       generation/inference code and  inference and architecture code in its required source code.
                       configuration                  [\[14\]](https://opensource.org/ai/open-source-ai-definition)

  **Training code and  Preprocessing/filtering code,  Necessary to understand *how* the weights arose and to retrain
  recipe**             optimizer, schedules,          or materially modify the system; OSI requires complete source
                       hyperparameters,               sufficient for training and running the system.
                       distributed-training           [\[13\]](https://opensource.org/ai/open-source-ai-definition)
                       configuration,                 
                       post-training/RL/SFT recipe,   
                       evaluation                     

  **Training data**    Best case: the actual curated  Enables exact data auditing, deduplication studies,
                       training mixture in            contamination analysis and close reproduction. OLMo/Dolma and
                       training-ready form            OpenLLM-France explicitly emphasize this level of transparency.
                                                      [\[15\]](https://allenai.org/olmo)

  **Data information** At minimum: provenance,        This is the **OSAID 1.0 minimum** where releasing the entire
                       sources, scope,                corpus is impossible; it is deliberately weaker than publishing
                       characteristics,               the dataset.
                       selection/filtering/labeling   [\[13\]](https://opensource.org/ai/open-source-ai-definition)
                       processes, and how obtainable  
                       datasets can be acquired       

  **Documentation**    Model card, technical report,  Supports auditability, reproducibility and downstream risk
                       architecture, limitations,     assessment. Both the European index and Stanford FMTI score
                       evaluations, intended use,     documentation/transparency separately from weight availability.
                       risks, dataset documentation   [\[16\]](https://osai-index.eu/database/)

  **Licences**         Separate, compatible licences  A public artifact is not necessarily legally reusable. The OLMo
                       for model/weights, source code ecosystem illustrates the distinction: model code/weights use
                       and datasets                   Apache 2.0 while Dolma 3 uses ODC-BY and underlying source
                                                      terms can still matter.
                                                      [\[17\]](https://huggingface.co/allenai/Olmo-3-1125-32B)
  -------------------------------------------------------------------------------------------------------------------

### Openness is composite, not binary

Liesenfeld & Dingemanse\'s FAccT 2024 study examines openness along **14
dimensions**, surveying 40 text-generating LLMs and six text-to-image
systems. Its central conclusion is that calling models simply "open" or
"closed" hides large differences: many prominent releases are
essentially **open-weight systems**, while training data and other
resources necessary for reproduction remain unavailable. They describe
misleadingly broad "open" claims as a form of **open-washing**.
[\[18\]](https://facctconference.org/static/papers24/facct24-120.pdf)

The **European Open Source AI Index**, whose current index was generated
in July 2026, goes in the same direction. It independently tracks such
dimensions as base-model and end-user-model data, weights, training
code, code documentation, compute/hardware information, architecture,
papers/preprints, model cards, datasheets and licences. Its upper ranks
include highly documented/reproducible projects such as YuLan-Mini,
BLOOM/BLOOMZ, OLMo 3 and Apertus, whereas prominent permissively
licensed weight releases can rank materially lower because the training
pipeline and data remain unavailable. [\[19\]](https://osai-index.eu/)

Stanford CRFM\'s **latest Foundation Model Transparency Index found in
this review is the December 2025 edition**. It assesses 13 companies
using 100 indicators and reports a mean transparency score of 41, down
17 points from 2024. IBM scored 95; open-weight providers were not
automatically highly transparent---DeepSeek scored 32 and Alibaba
26---and Mistral\'s score fell substantially relative to its previous
evaluation. FMTI is broader than an open-source test: it evaluates
corporate/model transparency, including upstream and downstream
information, rather than deciding whether a licence is "open source."
[\[20\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)

The three frameworks therefore ask related but different questions:

  -----------------------------------------------------------------------------------------------------------------------------------------------
  Framework            Main question                  Important consequence
  -------------------- ------------------------------ -------------------------------------------------------------------------------------------
  **Liesenfeld &       *How open is the complete      Exposes "open-washing" produced by reducing openness to weights.
  Dingemanse, FAccT    release in practice?*          [\[21\]](https://facctconference.org/static/papers24/facct24-120.pdf)
  2024**                                              

  **European Open      *Which                         Produces a **graded openness score**, so two Apache-licensed models can receive very
  Source AI Index,     reproducibility/open-science   different evaluations. [\[19\]](https://osai-index.eu/)
  2026**               artifacts have actually been   
                       released?*                     

  **Stanford FMTI,     *How transparent are major     Transparency is broader than source availability and open licensing.
  Dec. 2025**          foundation-model providers     [\[22\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)
                       across their ecosystem?*       

  **OSI OSAID 1.0**    *Does an AI system satisfy a   Requires the four freedoms plus data information, code and parameters in preferred form for
                       normative definition of "open  modification. [\[14\]](https://opensource.org/ai/open-source-ai-definition)
                       source AI"?*                   
  -----------------------------------------------------------------------------------------------------------------------------------------------

### "Open-washing"

For lecture purposes, a precise definition is:

> **Open-washing is presenting an AI system as "open" or "open source"
> on the basis of a selectively disclosed component---most commonly
> downloadable weights---while material artifacts or legal freedoms
> necessary to study, reproduce, modify or freely use the system remain
> unavailable or restricted.** This is the phenomenon highlighted by
> Liesenfeld & Dingemanse.
> [\[21\]](https://facctconference.org/static/papers24/facct24-120.pdf)

Three contemporary patterns make the idea concrete.

**Llama 4:** the weights are downloadable, but the licence contains use
restrictions, an additional licence requirement above 700 million MAU,
branding/naming obligations, and an EU-specific exclusion for rights to
use Llama 4 multimodal models. It therefore fails OSI\'s "use for any
purpose" criterion. Calling this simply "open source" would collapse
open weights and open-source freedoms.
[\[23\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)

**Gemma 3:** weights are accessible and commercial use is possible, but
use is governed by Google\'s custom terms and incorporated
prohibited-use policy; downstream distributors must contractually pass
those restrictions onward. Again, this is open access to weights, not
OSI-style unrestricted open source.
[\[24\]](https://ai.google.dev/gemma/terms)

**Mistral 3:** Mistral itself calls the Apache-2.0 models "open-source,"
while the European Open Source AI Index explicitly treats Mistral\'s
recent releases as much less open with respect to upstream artifacts
than projects such as OLMo. The Apache licence makes the **released
weight artifact** highly reusable; it does not reconstruct the
undisclosed training corpus or complete model-building process.
[\[25\]](https://mistral.ai/it/news/mistral-3/)

By contrast, OpenAI describes gpt-oss principally as **open-weight** and
releases its weights under Apache 2.0. That terminology is more
technically precise because the release does not purport to provide the
complete original training-data pipeline.
[\[26\]](https://openai.com/index/introducing-gpt-oss/)

## Open weights versus open source

### The OSI Open Source AI Definition

OSAID 1.0, finalized in October 2024, says users of an Open Source AI
system must be able, without requesting permission, to:

1.  use the system **for any purpose**;
2.  study how it works and inspect its components;
3.  modify it for any purpose;
4.  share the system, with or without modifications.
    [\[27\]](https://opensource.org/ai/open-source-ai-definition)

The "preferred form for making modifications" must include three classes
of material. **Data Information** must describe provenance, scope,
characteristics, collection/selection/labeling/filtering/processing and
identify publicly or commercially obtainable training sources
sufficiently for a skilled person to build a substantially equivalent
system. **Code** must cover the complete training and execution
pipeline. **Parameters**---including weights and configuration---must be
available under appropriate open terms.
[\[13\]](https://opensource.org/ai/open-source-ai-definition)

The controversial part is the first one. **OSAID does not require that
every training example itself be released.** OSI argues that datasets
can contain personal, confidential, copyrighted or otherwise
non-redistributable material, so requiring publication of all data would
rule out systems whose development can nevertheless be meaningfully
studied and replicated. Critics reasonably answer that "data
information" does not enable exact data auditing or exact reproduction.
This is a genuine design dispute, not a factual disagreement about what
OSAID says. [\[4\]](https://opensource.org/ai/faq)

OSI\'s initial validation exercise reported **Pythia, OLMo, Amber,
CrystalCoder and T5** as systems that passed its then-current review;
BLOOM, StarCoder2 and Falcon were described as potentially passing with
licensing changes. Llama 2, Grok, Phi-2 and Mixtral lacked required
components. This should be taught as an **initial validation set**, not
as a permanent OSI certification registry for all later model versions.
[\[28\]](https://opensource.org/ai/final-board-report)

Consequently, it is safer to say that OLMo 3 and Apertus are **strongly
aligned with the substantive OSAID criteria** than to claim that their
latest checkpoints have received a formal OSI certification. Both
publish substantially more of their model-production flow than ordinary
open-weight releases. [\[29\]](https://allenai.org/blog/olmo3)

### A practical taxonomy as of September 2026

"Permissive open weights" below means that the released weights have an
OSI-approved software-style licence such as Apache 2.0 or MIT, **not**
that the complete AI system satisfies OSAID.

  -----------------------------------------------------------------------------------------------------------------------------------------------------
  Category        Representative         What is actually   Main limitation
                  models/families        open               
  --------------- ---------------------- ------------------ -------------------------------------------------------------------------------------------
  **Closed /      Proprietary OpenAI GPT API/interface and  No downloadable frontier-model weights; modification and redistribution depend on provider
  API-only**      family other than      documentation      service terms. Stanford FMTI treats these providers as transparency subjects rather than
                  gpt-oss; Anthropic                        open-source systems; Mistral\'s current catalogue explicitly distinguishes open licences
                  Claude family; hosted                     from "Premier."
                  Google Gemini family;                     [\[30\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)
                  Mistral **Premier**                       
                  models                                    

  **Open weights, **Llama 4**; **Gemma 3 Weights, often     Use-based, geographic, commercial or downstream contractual restrictions mean "use for any
  restrictive     / 3n**; Teuken-7B      inference tooling  purpose" is absent.
  licence**       v0.6;                  and model cards    [\[31\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
                  BLOOM/OpenRAIL-style                      
                  releases                                  

  **Open weights, **Gemma 4**;           Weights under      Training corpus and complete original training pipeline are not generally reproduced as
  permissive      **Qwen3**;             Apache 2.0 or MIT; part of the release, so these are usually not "fully open" in the open-science sense.
  licence**       **DeepSeek-R1** and    local/commercial   [\[32\]](https://ai.google.dev/gemma/docs/core/model_card_4)
                  MIT V3 releases;       modification and   
                  **gpt-oss**; **Mistral redistribution     
                  Large 3 / Small 4**    generally allowed  
                                         subject to         
                                         standard notices   

  **Fully /       **OLMo 3**;            Weights +          Reproducibility can still depend on enormous compute and third-party source-data terms;
  near-fully open **Apertus**; **Minerva extensive training "fully open" here describes the artifact bundle, not formal OSI certification.
  model flow**    7B**;                  code/recipes +     [\[33\]](https://allenai.org/blog/olmo3)
                  OpenEuroLLM/open-sci   data or data       
                  reference releases     pipeline +         
                                         documentation;     
                                         often intermediate 
                                         checkpoints        
  -----------------------------------------------------------------------------------------------------------------------------------------------------

Several 2025--26 changes are especially slide-worthy:

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Model                Earlier state                                                                                               Current state relevant to engineers
  -------------------- ----------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------
  **Gemma 3 → Gemma    Gemma 3 uses Google\'s custom Gemma Terms with cascading use restrictions.                                  Gemma 4 is **Apache 2.0**, a major simplification for commercial
  4**                  [\[24\]](https://ai.google.dev/gemma/terms)                                                                 reuse, fine-tuning and redistribution.
                                                                                                                                   [\[34\]](https://ai.google.dev/gemma/docs/core/model_card_4)

  **DeepSeek-V3**      Early V3 releases used a bespoke model licence with use restrictions.                                       DeepSeek announced V3-0324 under **MIT**, matching the permissive R1
                       [\[35\]](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/LICENSE-MODEL?trk=public_post_comment-text)   licensing direction. Do not infer one licence from the family name:
                                                                                                                                   inspect the exact checkpoint.
                                                                                                                                   [\[36\]](https://www.deepseek.com/en/news/v3-0324/)

  **Mistral**          Historically mixed Apache, research and commercial models.                                                  Still mixed: Large 3 and Small 4 are Apache 2.0; current Medium 3.5
                                                                                                                                   uses a **Modified MIT** licence; OCR/Codestral and several service
                                                                                                                                   models are "Premier."
                                                                                                                                   [\[37\]](https://docs.mistral.ai/models?ref=aidatahub)

  **Teuken**           Commercial v0.4 released under Apache 2.0.                                                                  Newer 6T-token v0.6 is **CC-BY-NC-4.0** and explicitly
                       [\[38\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)                               non-commercial. "Newer" therefore does not imply "more permissive."
                                                                                                                                   [\[39\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6)

  **iGenius / Domyn**  Italia was initially announced as MIT/open source; the subsequent Italia 10B licence instead prohibited     iGenius became **Domyn** in June 2025; the separate Domyn Small 10B
                       modification, redistribution and derivatives without written consent.                                       release of May 2026 has MIT-licensed open weights. This is a
                       [\[40\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)     portfolio evolution, not evidence that old Italia checkpoints were
                                                                                                                                   retroactively relicensed.
                                                                                                                                   [\[41\]](https://www.domyn.com/news/introducing-domyn)
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### What restrictive licences mean in practice

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Licence/model   On-premise inference                                                                         Fine-tuning     Hosted service                                                                               Redistributing model / fine-tune                                                       Engineering consequence
  --------------- -------------------------------------------------------------------------------------------- --------------- -------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------- ---------------------------------------------------------------
  **Llama 4       Generally yes, **but the multimodal licence grant is not made to EU-domiciled individuals or Generally       Permitted subject to licence/AUP; EU end-user carve-out does not give an EU company itself   Must provide licence/notice and prominent **"Built with Llama"** attribution. A        **Poor fit for an EU company wanting Llama 4 multimodal on
  Community       EU-principal-place-of-business companies**.                                                  permitted for   the underlying model licence.                                                                distributed AI model trained/fine-tuned/improved using Llama materials or outputs      premises.** It is open-weight but not OSI-open.
  Licence**       [\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)   eligible        [\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)   must, in the specified circumstances, begin its name with **"Llama"**. \>700M MAU      
                                                                                                               licensees.                                                                                                   entities need a separate licence.                                                      
                                                                                                                                                                                                                            [\[43\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)   

  **Gemma 3       Yes, subject to prohibited-use policy. [\[24\]](https://ai.google.dev/gemma/terms)           Yes, but        Explicitly treated as "Distribution" via a Hosted Service.                                   Downstream agreements must include the prohibited-use restrictions as enforceable      Commercially usable, but compliance obligations **flow down**
  Terms**                                                                                                      resulting       [\[44\]](https://ai.google.dev/gemma/terms)                                                  terms; recipients get a copy of the agreement and modified-file notices.               to SaaS customers and redistributions.
                                                                                                               derivatives                                                                                                  [\[24\]](https://ai.google.dev/gemma/terms)                                            
                                                                                                               remain subject                                                                                                                                                                                      
                                                                                                               to                                                                                                                                                                                                  
                                                                                                               restrictions.                                                                                                                                                                                       

  **Gemma 4 /     Yes.                                                                                         Yes.            Yes.                                                                                         Yes, subject principally to Apache notice/patent requirements.                         Much simpler than Gemma 3; still distinguish permissive weights
  Apache 2.0**                                                                                                                                                                                                                                                                                                     from fully open training.
                                                                                                                                                                                                                                                                                                                   [\[34\]](https://ai.google.dev/gemma/docs/core/model_card_4)

  **BigScience    Yes for permitted purposes.                                                                  Yes for         Yes, but end users must respect use restrictions.                                            Use restrictions must be included as enforceable downstream terms for derivatives.     "Open" in the Responsible-AI-Licence vocabulary, **not OSI-open
  OpenRAIL /                                                                                                   permitted                                                                                                    [\[45\]](https://huggingface.co/static/bigscience/license/index.html)                  source**, because field/use restrictions contradict the OSI
  OpenRAIL-M                                                                                                   purposes.                                                                                                                                                                                           freedom to use for any purpose.
  family**                                                                                                                                                                                                                                                                                                         [\[14\]](https://opensource.org/ai/open-source-ai-definition)

  **MIT / Apache  Yes.                                                                                         Yes.            Yes.                                                                                         Generally yes, including commercial redistribution, subject to the licence\'s          Preferred default where a company wants maximum
  open weights**                                                                                                                                                                                                            attribution/notices and, for Apache, patent provisions.                                product/licensing flexibility---while still checking dataset
                                                                                                                                                                                                                                                                                                                   and base-model licences.
                                                                                                                                                                                                                                                                                                                   [\[46\]](https://github.com/openai/gpt-oss/blob/main/LICENSE)
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Google\'s Gemma 3 clause allowing Google, "to the maximum extent
permitted by law," to restrict use **"remotely or otherwise"** where it
reasonably believes the agreement is being violated is noteworthy. It is
a **contractual reservation of a right**, not evidence that every
self-hosted Gemma weight file contains a remotely activatable kill
switch. [\[47\]](https://ai.google.dev/gemma/terms)

### Fine-tunes, distillation, merges, data and outputs

Licensing becomes most error-prone after the first fine-tune.

**Fine-tunes.** A fine-tuned model containing the original parameters
normally remains subject to whatever downstream conditions the original
licence asserts. With permissive Apache/MIT models this is usually
straightforward. Gemma 3 requires its use restrictions to propagate.
Llama carries its notice/naming conditions.
[\[48\]](https://ai.google.dev/gemma/terms)

**Distillation is licence-specific.** Gemma 3\'s definition is unusually
explicit: its "Model Derivatives" include models produced by
transferring patterns from Gemma\'s weights, operations **or outputs**,
including synthetic-output distillation; the raw outputs themselves are
not Model Derivatives. [\[49\]](https://ai.google.dev/gemma/terms)
DeepSeek-R1, by contrast, is MIT and expressly permits
derivatives/distillation. But its published small distills are
**fine-tunes of other base models**: Qwen-based R1 distills retain
Apache 2.0, while the 8B and 70B Llama-based distills remain based on
the applicable Llama 3.1/3.3 licences.
[\[50\]](https://github.com/deepseek-ai/DeepSeek-R1/wiki)

**Merges.** A merge that actually contains parameters from models A and
B should be treated conservatively as needing to comply with **both
applicable licence stacks**. A restrictive component is not "washed
away" by merging it into an Apache model. A difficult underlying legal
question remains: the extent to which model weights themselves attract
copyright or other exclusive rights is not fully settled. OSI
deliberately frames OSAID around the freedoms users must practically
receive rather than resolving every jurisdiction\'s theory of IP
protection for parameters.
[\[51\]](https://opensource.org/ai/drafts/the-open-source-ai-definition-1-0-rc1)

**Training data has its own licence.** OLMo 3 demonstrates the correct
separation. OLMo code/weights are Apache 2.0, but Dolma 3 is distributed
under **ODC-BY**; attribution is therefore required when the dataset or
derivatives of it are redistributed, and Ai2 warns that source material
may itself carry additional source-specific terms. A model licence never
automatically grants rights in its training corpus.
[\[52\]](https://huggingface.co/allenai/Olmo-3-1125-32B)

**Outputs can also be contractually constrained.** Gemma says Google
claims no rights in generated output, yet using the model remains
governed by the agreement. OpenRAIL similarly says the licensor claims
no output ownership while requiring that output use not contravene the
licence\'s restrictions. Llama goes further in one important downstream
case: use of Llama **outputs to train/improve another distributed AI
model** can activate Llama\'s naming requirement. Thus "the vendor does
not own my output" and "I may use the output with no contractual
restrictions" are logically separate propositions.
[\[53\]](https://ai.google.dev/gemma/terms)

### Free/open-source GPAI under the EU AI Act

The operative provision for general-purpose AI is **Article 53**.

  ---------------------------------------------------------------------
  AI Act duty for GPAI        Ordinary GPAI        Qualifying
  provider                                         free/open-source
                                                   GPAI
  --------------------------- -------------------- --------------------
  Art. 53(1)(a): technical    Required             **Exempt under Art.
  documentation                                    53(2)**

  Art. 53(1)(b):              Required             **Exempt under Art.
  information/documentation                        53(2)**
  for downstream AI-system                         
  providers                                        

  Art. 53(1)(c): policy to    Required             **Still required**
  comply with EU copyright                         
  law, including rights                            
  reservations under DSM                           
  Directive Art. 4(3)                              

  Art. 53(1)(d): publicly     Required             **Still required**
  available sufficiently                           
  detailed summary of                              
  training content, using the                      
  AI Office template                               

  Additional systemic-risk    If model qualifies   **No FOSS escape:**
  obligations                 as systemic-risk     Art. 53(2)\'s
                              GPAI                 exemption expressly
                                                   does not apply to
                                                   GPAI with systemic
                                                   risk; Article 55
                                                   duties remain
                                                   relevant.
  ---------------------------------------------------------------------

[\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)

For Article 53(2), the model must be released under a free/open-source
licence permitting **access, use, modification and distribution**, and
its parameters---including weights---plus architecture and usage
information must be publicly available. Importantly, the AI Act does
**not** equate this condition with OSAID\'s much richer preferred-form
requirements. A model can therefore qualify for the EU provision without
publishing its exact training dataset.
[\[54\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)

There is also a related **Article 54** relief concerning the EU
authorized-representative requirement for certain non-EU providers of
genuinely free/open-source GPAI, subject to the statutory conditions and
the systemic-risk exception.
[\[55\]](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)

The **GPAI Code of Practice**, finalized in July 2025 and recognized by
the Commission and AI Board as an adequate voluntary compliance
instrument, operationalizes the Act through Transparency and Copyright
chapters for ordinary GPAI and a Safety & Security chapter for GPAI with
systemic risk. Using the Code is voluntary, but signatories receive a
more structured compliance route and reduced regulatory uncertainty.
[\[56\]](https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf)

A useful lecture sentence is therefore:

> **The AI Act gives genuinely free/open-source GPAI a documentation
> discount, not a copyright exemption, not a training-data-summary
> exemption, and not a systemic-risk exemption.**
> [\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)

## Italian and European open-model initiatives

European "sovereign AI" covers at least three different goals that
should not be conflated: **where a model is developed**, **where it can
be executed and its data processed**, and **whether the full
model-building process can be independently inspected/reproduced**.
Mistral, Apertus and OLMo-style projects illustrate that geographic
sovereignty and open-science openness are distinct dimensions.
[\[57\]](https://docs.mistral.ai/models?ref=aidatahub)

### Italy

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Initiative     Actors / funding                                                                                                                      Language/data profile                                                                                     Licence & data openness                                                                                   Release / current status
  -------------- ------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------
  **Minerva**    Sapienza NLP within FAIR, with CINECA/NVIDIA support; funded through PNRR MUR project PE0000013-FAIR and PRIN research funding.       Minerva-7B: \~2.48T tokens: \~1.14T Italian, 1.14T English and 200B code, i.e. roughly **46% Italian      Apache 2.0 model; team describes Minerva as "truly-open (data and model)" and documents its training      Minerva-7B unveiled Nov. 2024; research-grade downloadable Italian/English model family.
                 [\[58\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)   tokens** before the code component. [\[59\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)     sources/process. [\[59\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)                        [\[60\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)

  **LLaMAntino / University of Bari researchers Marco Polignano, Pierpaolo Basile, Giovanni Semeraro and collaborators; family evolved from Italian    Primarily Italian + English adaptation rather than from-scratch Italian pretraining; recent ANITA-NEXT    **Caution:** the ANITA-NEXT Magistral model\'s HF metadata says Apache-2.0, while model-card prose says   Active family with 2025--26-generation variants; useful research/adaptation project, but licence hygiene is weaker than on the
  ANITA**        adaptation of Llama-family models to ANITA/NEXT derivatives.                                                                          includes Mistral/Magistral-derived models and multimodal variants.                                        "research only purposes." Those statements conflict; a commercial user should obtain clarification rather cleanest releases.
                 [\[61\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)                                    [\[62\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)        than assume the metadata overrides the prose.                                                             
                                                                                                                                                                                                                                                                 [\[61\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)        

  **Italia /     Italian private company iGenius, renamed **Domyn on 5 June 2025**; training has used CINECA Leonardo.                                 Original Italia targeted native Italian data; current Domyn Small supports 50+ languages with particular  Original Italia 9B was announced as MIT; **Italia 10B later used a restrictive custom licence** requiring Domyn Small released May 2026 and is positioned for controlled/on-prem enterprise use. Do not treat all historical
  iGenius →      [\[41\]](https://www.domyn.com/news/introducing-domyn)                                                                                emphasis on major European languages including Italian.                                                   written consent for modification/redistribution/derivatives. Current, separate **Domyn Small 10B is MIT   "Italia/iGenius/Domyn" checkpoints as one licensing lineage.
  Domyn**                                                                                                                                              [\[63\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)   open-weight**.                                                                                            
                                                                                                                                                                                                                                                                 [\[64\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)   

  **Velvet**     Almawave; trained on CINECA Leonardo. [\[65\]](https://huggingface.co/Almawave/Velvet-14B)                                            Velvet-14B trained from scratch on six languages; approximately **23% of training data is Italian**, with Apache 2.0 weights. Public-data sources were curated and documented, but this is not the same as          14B release Jan. 31, 2025; 2B release Feb. 2025. Model cards describe these checkpoints as static models.
                                                                                                                                                       \>4T final training tokens plus 400B+ code tokens. [\[65\]](https://huggingface.co/Almawave/Velvet-14B)   providing the exact complete pretraining mixture in training-ready form.                                  [\[66\]](https://huggingface.co/Almawave/Velvet-14B)
                                                                                                                                                                                                                                                                 [\[65\]](https://huggingface.co/Almawave/Velvet-14B)                                                      
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The interesting governance contrast is **Minerva versus Italia 10B**.
Both were publicly discussed as Italian sovereign/open AI, but
Minerva\'s Apache/data-oriented academic release provides substantially
stronger downstream reuse rights than the restrictive 2025 Italia 10B
licence. "National model" therefore says essentially nothing about
openness.
[\[67\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)

### Europe

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Initiative          Who / funding                                                                                                                  Languages                                                                                                                               Openness & licence                                                                                                                                   Status as of 30 Sep. 2026
  ------------------- ------------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------
  **EuroLLM**         Instituto Superior Técnico, Edinburgh, Instituto de Telecomunicações, Paris-Saclay, Unbabel, Sorbonne, Naver Labs, Amsterdam   Current 22B flagship trained on \>4T tokens across **35 languages including all 24 EU official languages**.                             Project presents models as open source and downloadable. For engineering procurement, verify the exact HF checkpoint licence rather than relying     22B is the current flagship; 9B and 1.7B variants also released, with multimodal extensions in development.
                      and others; supported by EuroHPC, Horizon Europe/UTTER and European research funding. [\[68\]](https://eurollm.io/)            [\[68\]](https://eurollm.io/)                                                                                                           solely on the umbrella site\'s "open source" wording.                                                                                                [\[68\]](https://eurollm.io/)

  **OpenEuroLLM**     20-member European consortium led by Charles University and AMD Silo AI, with CINECA, CSC, SURF, Fraunhofer, BSC, universities EU official languages and additional economically/socially relevant languages.                                                          Explicit project goal is a **truly open stack: data, documentation, training/testing code, evaluation and models**.                                  Began 1 Feb. 2025; active. By 2025--26 it had released reference/scaling models and 38 monolingual 2.15B models and secured major
                      and companies; **Digital Europe grant 101195233**. [\[69\]](https://openeurollm.eu/launch-press-release)                                                                                                                                                               [\[70\]](https://www.openeurollm.eu/)                                                                                                                EuroHPC allocations; the project remains broader than one finished frontier checkpoint. [\[71\]](https://openeurollm.eu/blog)

  **OpenLLM-France:   Nine formal partners plus associates; BPI France-funded research project begun Sept. 2024 for two years.                       Lucie 7B used **\>30% French**; successor Luciole 1B/8B/23B uses roughly 30% French plus major European languages.                      Strong open-science commitment: training-ready datasets, final/intermediate weights, training and preprocessing code. Exact licences should be       Lucie is now complemented/superseded by the newer Luciole line; active research commons rather than merely a single model.
  Lucie → Luciole**   [\[72\]](https://openllm-france.fr/fr/main-page-fr/)                                                                           [\[73\]](https://openllm-france.fr/en/main-page-en/)                                                                                    checked artifact-by-artifact. [\[73\]](https://openllm-france.fr/en/main-page-en/)                                                                   

  **Teuken /          Fraunhofer IAIS/IIS, Jülich, DFKI, TU Dresden and industry; German BMWK funding of about **€14m**; project ran Jan. 2022--Mar. From-scratch model covering all **24 EU languages**, approximately 50% non-English pretraining material.                                Commercial v0.4: Apache 2.0. Newer v0.6: CC-BY-NC-4.0 and therefore non-commercial.                                                                  Project funding has ended; models remain available. This makes Teuken a useful case study in post-project maintenance risk.
  OpenGPT-X**         2025.                                                                                                                          [\[75\]](https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html)   [\[76\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)                                                                        [\[75\]](https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html)
                      [\[74\]](https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text)                                                                                                                                                                                                                                                                                                

  **Apertus**         ETH Zurich, EPFL and CSCS through the Swiss AI Initiative; initial resources included \>10m GPU-hours on Alps and a CHF20m ETH Strongly multilingual; project reports extremely broad language coverage rather than an English-first corpus.                           **Apache 2.0; architecture, code, weights, checkpoints, training process and data information/resources are openly released.** Designed explicitly   1.0: Sep. 2025; smaller distillations 1.1: May 2026; **Apertus 1.5: July 2026**, adding multimodal/tool/reasoning capabilities; 2.0
                      Domain commitment. [\[77\]](https://www.swiss-ai.org/)                                                                         [\[78\]](https://apertus-ai.org/pages/about/)                                                                                           around transparency and European/Swiss legal constraints.                                                                                            planned for 2027. [\[78\]](https://apertus-ai.org/pages/about/)
                                                                                                                                                                                                                                                                                             [\[79\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)   

  **Mistral AI**      French private AI company.                                                                                                     Current Mistral 3 models advertise 40+ languages; company maintains both generalist and specialist models.                              **Mixed portfolio**: Large 3 and Ministral 3 are Apache 2.0; Small 4 Apache 2.0; Medium 3.5 Modified MIT; several current specialist models are      One of Europe\'s strongest commercial model vendors; an example of **open weights and proprietary services coexisting in the same
                                                                                                                                                     [\[80\]](https://mistral.ai/it/news/mistral-3/)                                                                                         Premier/proprietary. Training data are not generally published. [\[37\]](https://docs.mistral.ai/models?ref=aidatahub)                               company**.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Infrastructure and sovereignty policy

A terminology correction matters here: **IT4LIA is an AI Factory, not an
AI Gigafactory.**

The Commission selected **IT4LIA at CINECA in Bologna** in December 2024
as one of the first seven EuroHPC AI Factories, alongside sites in
Barcelona, Finland, Luxembourg, Sweden, Germany and Greece. Austria and
Slovenia participate with the Italian factory. The first seven AI
Factories represented an aggregate €1.5 billion investment, half
EU-financed, and are intended to combine compute, data and talent for
startups, research, industry and public-sector AI.
[\[81\]](https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf)

**AI Gigafactories are a separate, substantially larger initiative.** As
of 30 September 2026 the EuroHPC procurement is still under way: the
tender was published on 30 July 2026 and has a November 2026 submission
deadline. It targets infrastructure capable of the complete lifecycle of
very large frontier models. It is therefore premature to describe
IT4LIA---or any site---as an already selected EU AI Gigafactory.
[\[82\]](https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion)

**ALT-EDIC\'s LLMs4EU** is complementary rather than a compute centre.
The Digital Europe-funded project began in March 2025 for three years,
involves organisations in 20 countries, aims to acquire/create language
resources for all EU languages, and targets energy, telecom, tourism,
public services and science, including support for SMEs fine-tuning
models. [\[83\]](https://www.alt-edic.eu/projects/llms4eu/)

Italy\'s national policy layer now consists of both the **Italian AI
Strategy 2024--2026** and **Law No. 132 of 23 September 2025**, followed
by implementing measures during 2026. The strategy explicitly argues
that Italy should develop technology tailored to its own context rather
than merely import generic systems, promotes open-source research
artifacts, and calls for secure and reliable infrastructure for Public
Administration.
[\[84\]](https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf)

### How good are the Italian models?

This is the part where overclaiming should be avoided.

**ITA-Bench** was designed specifically because translated English
benchmarks alone are not a satisfactory measure of Italian capability:
it combines translated standard tasks with manually curated Italian
datasets such as Italian Word-in-Context and Italy-specific QA.
[\[85\]](https://iris.uniroma1.it/bitstream/11573/1727996/3/Moroni_ITA-Bench_2024.pdf)

**Evalita-LLM**, introduced in 2025, goes further by using **ten
native-Italian tasks**, including both multiple-choice and generative
tasks, and multiple prompt formulations per task because model rankings
can be sensitive to prompt choice. Its published analysis finds that
few-shot prompting usually improves results and, unsurprisingly,
newer/larger models generally perform better.
[\[86\]](https://arxiv.org/html/2502.02289v1)

Concrete public model-card evidence illustrates the scale issue. For
example, **Velvet-2B** reports 39.6 on Italian MMLU, 61.9 on ITA-Bench
WinoGrande, 67.3 on ITA-Bench PIQA and 86.6 on the ITA-Bench SciQ
variant. Those numbers establish that a small Italian-oriented model can
be useful; they do **not** establish frontier-model superiority.
[\[87\]](https://huggingface.co/Almawave/Velvet-2B)

The defensible conclusion from the currently published evidence is
therefore:

> **Italian-specific pretraining improves linguistic representation and
> can provide attractive capability/size trade-offs, but there is no
> robust evidence that today\'s national Italian models collectively
> outperform the largest contemporary multilingual/open or closed
> frontier models.** The evaluation landscape changes faster than
> peer-reviewed Italian benchmark tables, and comparisons across
> ITA-Bench, Evalita-LLM and vendor benchmarks are not interchangeable.
> [\[88\]](https://arxiv.org/html/2502.02289v1)

The public Evalita-LLM leaderboard continues to update, so a slide
containing an exact rank should record the **leaderboard snapshot date**
rather than presenting it as a stable model property.
[\[89\]](https://huggingface.co/spaces/evalitahf/evalita_llm_leaderboard)

### Recurring European problems

**Language data remains the first bottleneck.** OpenLLM-France
explicitly motivates French-focused datasets by the overrepresentation
of English in open corpora; LLMs4EU similarly warns that less-resourced
EU languages risk being left behind because the quantity and quality of
suitable training material are insufficient.
[\[90\]](https://openllm-france.fr/en/main-page-en/)

**Compute dependence is the second.** Minerva depends on Leonardo;
Teuken used JUWELS; EuroLLM used MareNostrum 5; Apertus relies on Alps;
OpenEuroLLM has obtained millions of EuroHPC GPU-hours. "Open model"
therefore does not imply that an independent group can afford to
reproduce its training run.
[\[91\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)

**Maintenance after project funding is structurally difficult.**
OpenGPT-X formally ended in March 2025 even though Teuken remains
downloadable; OpenLLM-France and OpenEuroLLM similarly operate in
funded-project time horizons. This does not mean the artifacts
disappear, but it creates a real engineering question about long-term
checkpoint maintenance, vulnerability fixes, evaluation updates and
ownership of downstream community support. The maintenance-risk
statement is an inference from the projects\' finite funding structures,
not evidence that those projects have abandoned their models.
[\[92\]](https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text)

**Public-administration adoption is still more aspiration than
demonstrated large-scale deployment in the sources reviewed.** FAIR
explicitly positions Minerva as potentially useful for Italian PA;
LLMs4EU includes public services; IT4LIA is intended to make
infrastructure available to public administrations. Those are credible
enabling initiatives, but they should not be turned into a claim that
Italian or European open LLMs have already become the standard
production stack of public administrations.
[\[93\]](https://fondazione-fair.it/en/news/minerva-7b-the-new-frontier-of-italian-language-models-unveiled-by-sapienza/)

## Engineering take-aways

### Pre-adoption checklist

The useful compliance unit is
`model checkpoint + model licence version + code licences + data licences + deployment model + intended use`,
not a brand name.

  ---------------------------------------------------------------------------------------------------------------------------
  Question to record before      What to verify
  architecture freeze            
  ------------------------------ --------------------------------------------------------------------------------------------
  **Exactly what artifact am I   Pin repository, model/checkpoint hash, release date and licence revision. "Gemma,"
  using?**                       "DeepSeek," "Mistral" and "Teuken" are not licence identifiers.
                                 [\[94\]](https://ai.google.dev/gemma/terms)

  **Is commercial use            Apache/MIT usually yes; CC-BY-NC does not permit commercial use; custom community licences
  permitted?**                   may introduce scale, field-of-use or use restrictions.
                                 [\[95\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6)

  **May we run it on premises?** Check the model licence, not merely availability of weight files. For an EU organisation,
                                 Llama 4 multimodal is the clearest current geographic counterexample.
                                 [\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)

  **May we fine-tune it?**       Inspect both licence grant and AUP; decide whether the tuned weights will themselves inherit
                                 use restrictions. [\[96\]](https://ai.google.dev/gemma/terms)

  **May we distil it?**          Check whether output-based distillation is addressed explicitly. Gemma 3 says yes---as a
                                 derivative; DeepSeek-R1 permits distillation, but published R1 distills inherit their
                                 base-model licences. [\[97\]](https://ai.google.dev/gemma/terms)

  **May we merge it with another Build a licence dependency graph for every parent. Satisfy all applicable notice, use and
  checkpoint?**                  distribution conditions.

  **May we redistribute weights  Check attribution, NOTICE requirements, downstream AUP propagation, model-naming clauses and
  or sell a fine-tuned model?**  commercial thresholds.
                                 [\[98\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)

  **Does "serving an API" count  Licence-specific. Gemma 3 explicitly includes hosted/API access in its definition of
  as distribution?**             Distribution. [\[44\]](https://ai.google.dev/gemma/terms)

  **Are there geography or       Llama 4: EU multimodal restriction and \>700M-MAU licence threshold.
  company-size restrictions?**   [\[7\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)

  **What attribution/branding    Apache/MIT notices, Gemma notices, Llama "Built with Llama" and naming requirements are
  survives downstream?**         different obligations.
                                 [\[98\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)

  **What trained the model?**    Ask whether actual data, source list, or only vague categories are known; document copyright
                                 opt-out/provenance information and any personal-data issues. OSAID\'s "Data Information" is
                                 a useful minimum, not a guarantee of full data auditability.
                                 [\[13\]](https://opensource.org/ai/open-source-ai-definition)

  **What licence governs our own Model, code and data licences form separate dependency layers. Dolma/OLMo is a good
  fine-tuning data?**            reference architecture for keeping them distinct.
                                 [\[99\]](https://huggingface.co/allenai/Olmo-3-1125-32B)

  **What about generated         Check model licence/AUP and, for hosted access, service terms. Lack of vendor copyright
  outputs?**                     claims does not imply absence of contractual restrictions.
                                 [\[100\]](https://ai.google.dev/gemma/terms)

  **Does the AI Act FOSS GPAI    Verify that licence and publicly available parameters/architecture/usage info meet Art.
  exemption actually apply?**    53(2); remember that copyright policy and training-content summary remain.
                                 [\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)

  **Are we the GPAI provider,    Fine-tuning and redistributing a model can change the regulatory role. Model-level GPAI
  downstream provider,           obligations and application-level AI-system/high-risk obligations are separate layers.
  deployer---or several at       [\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)
  once?**                        

  **Do we require                For self-hosting, permissive weights may suffice. For scientific reproduction/audit, prefer
  reproducibility or merely      OLMo 3, Apertus or another release exposing the full model flow.
  self-hosting?**                [\[101\]](https://allenai.org/olmo)
  ---------------------------------------------------------------------------------------------------------------------------

### Scenario: a University of Bologna research assistant deployed on premises

Suppose a university laboratory wants a local RAG/chat system, wants to
fine-tune it on university material, and wants students to reproduce
experiments.

**Best category:** fully open or permissively licensed open-weight
models.

**Strong candidates:** **OLMo 3** where reproducibility and
training-data research matter; **Apertus** for a Europe-adjacent,
extensively open model flow; **Minerva** for Italian-centric
experiments; and, where only weights/customization are required, **Gemma
4, Qwen3, gpt-oss or an Apache-licensed Mistral model**.
[\[102\]](https://allenai.org/blog/olmo3)

**Llama 4 multimodal is not an acceptable choice for the university
itself under the standard Llama 4 licence**: an Italian university is an
EU-established organisation and Meta\'s AUP says the relevant multimodal
rights are not granted to an EU-principal-place-of-business
company/organisation. The end-user carve-out does not solve the
university\'s own model-use problem.
[\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)

Gemma 3 is technically usable, but Gemma 4\'s Apache licence removes
substantial downstream licence-management complexity.
[\[6\]](https://ai.google.dev/gemma/terms)

### Scenario: an Italian startup fine-tunes a model and sells the resulting model/SaaS

The startup wants freedom to fine-tune, host commercially, distribute a
customer-specific checkpoint and perhaps later sell the model asset
itself.

**Lowest-friction choices:** **Gemma 4, Qwen3, gpt-oss, DeepSeek-R1,
Mistral Large 3/Small 4, OLMo 3 or Domyn Small**, subject to checking
the exact version and all fine-tuning-data licences. Their weight
licences are Apache 2.0 or MIT rather than use-restricted community
licences. [\[103\]](https://ai.google.dev/gemma/docs/core/model_card_4)

**Do not choose an R1 distill by reading only "DeepSeek-R1 / MIT."** A
Llama-based R1 distill retains the corresponding Llama base licence; a
Qwen2.5-based distill uses the Qwen/Apache base terms.
[\[50\]](https://github.com/deepseek-ai/DeepSeek-R1/wiki)

Gemma 3 remains possible but forces prohibited-use clauses into
downstream contractual arrangements. Llama 4 creates additional
naming/attribution/scale constraints and, for an Italian company\'s use
of the multimodal checkpoints, the EU restriction is decisive. Teuken
v0.6 is unsuitable for a commercial product because it is CC-BY-NC.
[\[104\]](https://ai.google.dev/gemma/terms)

### Scenario: an Italian public administration requires EU-controlled deployment and auditability

Here "sovereignty" should be decomposed into **operational
sovereignty**---the ability to execute the system on infrastructure
under European control---and **epistemic/audit sovereignty**---the
ability to know how the model was made.

For maximum auditability, **Apertus** is especially attractive because
it publishes architecture, weights, code, training process,
datasets/data information and checkpoints under a permissive licence.
**Minerva** is attractive when Italian-language orientation and an
Italian public/research ecosystem dominate the decision. **OLMo 3** is
not European, but it is one of the strongest options when the
procurement criterion is reproducibility rather than developer
nationality.
[\[105\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)

For operational EU sovereignty with potentially stronger production
performance, Apache-licensed **Mistral** models, **EuroLLM**, **Velvet**
and **Domyn Small** are plausible candidates, but procurement should
distinguish "weights can run inside our datacentre" from "we can audit
the original training corpus."
[\[106\]](https://mistral.ai/news/mistral-small-4/)

**IT4LIA/CINECA is infrastructure, not a model licence.** Using an EU AI
Factory can solve compute and data-location requirements while leaving
model provenance/licensing questions completely unchanged.
[\[81\]](https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf)

For a five-slide lecture, the core engineering message can therefore be
compressed to:

**Weights → licence → recipe → data → regulatory role.**\
A model is only as "open" as the layer that matters to the intended use.

## Consolidated references

**Concepts and measurement.** Liesenfeld, A. & Dingemanse, M.,
*Rethinking open source generative AI: open-washing and the EU AI Act*,
FAccT 2024.
[\[18\]](https://facctconference.org/static/papers24/facct24-120.pdf)
European Open Source AI Index, current 2026 index and model database.
[\[19\]](https://osai-index.eu/) Stanford CRFM, *Foundation Model
Transparency Index*, December 2025 edition.
[\[20\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)

**Open Source AI Definition.** Open Source Initiative, *Open Source AI
Definition 1.0*.
[\[14\]](https://opensource.org/ai/open-source-ai-definition) OSI FAQ on
training data and preferred form for modification.
[\[107\]](https://opensource.org/ai/faq) OSI final-definition
announcement and rationale.
[\[108\]](https://opensource.org/blog/the-open-source-initiative-announces-the-release-of-the-industrys-first-open-source-ai-definition)
OSI validation/board report on candidate systems.
[\[28\]](https://opensource.org/ai/final-board-report)

**Llama.** Meta, *Llama 4 Community License Agreement*.
[\[109\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
Meta, *Llama 4 Acceptable Use Policy*, including EU multimodal
restriction.
[\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)
Meta, Llama 4 model card.
[\[110\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md?_bhlid=465b0c8311ac465d0fceabb3634d7a77db379746)

**Gemma.** Google, *Gemma Terms of Use*, revised 1 April 2026.
[\[111\]](https://ai.google.dev/gemma/terms) Google, *Gemma 4 Model
Card*, including Apache-2.0 licence.
[\[34\]](https://ai.google.dev/gemma/docs/core/model_card_4)

**Mistral.** Mistral AI, current model catalogue distinguishing Apache,
Modified MIT and Premier models.
[\[112\]](https://docs.mistral.ai/models?ref=aidatahub) Mistral AI,
*Introducing Mistral 3*. [\[80\]](https://mistral.ai/it/news/mistral-3/)
Mistral AI, *Introducing Mistral Small 4*.
[\[113\]](https://mistral.ai/news/mistral-small-4/) Mistral AI, *Mistral
Medium 3.5*.
[\[114\]](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/)

**Qwen, DeepSeek and gpt-oss.** Qwen team, Qwen3 model cards and
repositories. [\[115\]](https://huggingface.co/Qwen/Qwen3-14B) DeepSeek,
*DeepSeek-R1* repository and licence notes, including licences of
distilled checkpoints.
[\[50\]](https://github.com/deepseek-ai/DeepSeek-R1/wiki) DeepSeek,
V3-0324 MIT relicensing announcement.
[\[36\]](https://www.deepseek.com/en/news/v3-0324/) OpenAI, *Introducing
gpt-oss*. [\[116\]](https://openai.com/index/introducing-gpt-oss/)
OpenAI, gpt-oss Apache-2.0 licence and open-weight documentation.
[\[117\]](https://github.com/openai/gpt-oss/blob/main/LICENSE)

**Responsible-AI licences.** BigScience, BLOOM / OpenRAIL licence text.
[\[118\]](https://huggingface.co/static/bigscience/license/index.html)
BigScience/OpenRAIL-M licence, including cascading use-based
restrictions and output provisions.
[\[119\]](https://scancode-licensedb.aboutcode.org/bigscience-open-rail-m.LICENSE)
CreativeML OpenRAIL++ example.
[\[120\]](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/LICENSE.md)

**OLMo and data licensing.** Ai2, OLMo 3 release and model-flow
documentation. [\[121\]](https://allenai.org/blog/olmo3) Ai2, OLMo-3-32B
model card, Apache 2.0.
[\[122\]](https://huggingface.co/allenai/Olmo-3-1125-32B) Ai2, Dolma 3
and ODC-BY licensing documentation.
[\[123\]](https://huggingface.co/datasets/allenai/dolma3_mix-150B-1025/blob/main/README.md)

**Apertus.** Swiss AI Initiative / Apertus official project site and
release history. [\[78\]](https://apertus-ai.org/pages/about/) Swiss AI
Initiative resource/funding information.
[\[77\]](https://www.swiss-ai.org/) ETH Zurich, Apertus release and
openness documentation.
[\[124\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
Apertus Apache-2.0 model repository.
[\[125\]](https://huggingface.co/swiss-ai/Apertus-70B-2509/blob/main/LICENSE.txt)

**EU AI Act and GPAI Code.** European Commission AI Act Service Desk,
Article 53 GPAI obligations and free/open-source exception.
[\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)
Article 54 open-source/authorized-representative treatment.
[\[55\]](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)
European Commission, *General-Purpose AI Code of Practice*, July 2025
and current signatory information.
[\[56\]](https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf)

**Italian models.** FAIR/Sapienza, Minerva-7B announcement.
[\[126\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)
Sapienza NLP, Minerva model card, training mixture, funding and Apache
licence.
[\[59\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)
Polignano et al., ANITA-NEXT model documentation.
[\[62\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)
iGenius, original Italia announcement.
[\[127\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)
iGenius, Italia 10B licence.
[\[128\]](https://secure.igenius.ai/legal/iGenius%2BLicense%2BItalia%2B10B.pdf)
Domyn, iGenius→Domyn rebranding.
[\[129\]](https://www.domyn.com/news/introducing-domyn) Domyn,
*Introducing Domyn Small*, May 2026.
[\[130\]](https://www.domyn.com/news/introducing-domyn-small-an-open-european-reasoning-llm-built-for-ai-ownership)
Almawave, Velvet-14B and Velvet-2B model cards.
[\[66\]](https://huggingface.co/Almawave/Velvet-14B)

**European models and programmes.** EuroLLM project, current model
family and funding acknowledgments. [\[68\]](https://eurollm.io/)
OpenEuroLLM launch, consortium and Digital Europe funding.
[\[69\]](https://openeurollm.eu/launch-press-release) OpenEuroLLM
progress and reference-model releases.
[\[71\]](https://openeurollm.eu/blog) OpenLLM-France, Lucie/Luciole and
open-data/model commitments.
[\[131\]](https://openllm-france.fr/en/main-page-en/)
Fraunhofer/OpenGPT-X, Teuken release, licensing variants and project
funding/status.
[\[132\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)
ALT-EDIC, LLMs4EU. [\[83\]](https://www.alt-edic.eu/projects/llms4eu/)
European Commission, first seven EuroHPC AI Factories including
IT4LIA/CINECA Bologna.
[\[81\]](https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf)
European Commission/EuroHPC, 2026 AI Gigafactory procurement.
[\[133\]](https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion)

**Italian policy and evaluation.** AgID, *Italian Strategy for
Artificial Intelligence 2024--2026*.
[\[134\]](https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf)
Italian Government, implementation of Law No. 132/2025 during 2026.
[\[135\]](https://www.governo.it/it/search/node/132) Moroni et al.,
*ITA-Bench: Towards a More Comprehensive Evaluation for Italian LLMs*.
[\[85\]](https://iris.uniroma1.it/bitstream/11573/1727996/3/Moroni_ITA-Bench_2024.pdf)
Magnini et al., *Evalita-LLM: Benchmarking Large Language Models on
Italian* and public leaderboard.
[\[136\]](https://arxiv.org/html/2502.02289v1)

------------------------------------------------------------------------

[\[1\]](https://ai.google.dev/gemma/terms)
[\[6\]](https://ai.google.dev/gemma/terms)
[\[8\]](https://ai.google.dev/gemma/terms)
[\[24\]](https://ai.google.dev/gemma/terms)
[\[44\]](https://ai.google.dev/gemma/terms)
[\[47\]](https://ai.google.dev/gemma/terms)
[\[48\]](https://ai.google.dev/gemma/terms)
[\[49\]](https://ai.google.dev/gemma/terms)
[\[53\]](https://ai.google.dev/gemma/terms)
[\[94\]](https://ai.google.dev/gemma/terms)
[\[96\]](https://ai.google.dev/gemma/terms)
[\[97\]](https://ai.google.dev/gemma/terms)
[\[100\]](https://ai.google.dev/gemma/terms)
[\[104\]](https://ai.google.dev/gemma/terms)
[\[111\]](https://ai.google.dev/gemma/terms)
https://ai.google.dev/gemma/terms

<https://ai.google.dev/gemma/terms>

[\[2\]](https://facctconference.org/static/papers24/facct24-120.pdf)
[\[12\]](https://facctconference.org/static/papers24/facct24-120.pdf)
[\[18\]](https://facctconference.org/static/papers24/facct24-120.pdf)
[\[21\]](https://facctconference.org/static/papers24/facct24-120.pdf)
https://facctconference.org/static/papers24/facct24-120.pdf

<https://facctconference.org/static/papers24/facct24-120.pdf>

[\[3\]](https://opensource.org/ai/open-source-ai-definition)
[\[11\]](https://opensource.org/ai/open-source-ai-definition)
[\[13\]](https://opensource.org/ai/open-source-ai-definition)
[\[14\]](https://opensource.org/ai/open-source-ai-definition)
[\[27\]](https://opensource.org/ai/open-source-ai-definition)
https://opensource.org/ai/open-source-ai-definition

<https://opensource.org/ai/open-source-ai-definition>

[\[4\]](https://opensource.org/ai/faq)
[\[107\]](https://opensource.org/ai/faq) https://opensource.org/ai/faq

<https://opensource.org/ai/faq>

[\[5\]](https://huggingface.co/Qwen/Qwen3-14B)
[\[115\]](https://huggingface.co/Qwen/Qwen3-14B)
https://huggingface.co/Qwen/Qwen3-14B

<https://huggingface.co/Qwen/Qwen3-14B>

[\[7\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
[\[23\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
[\[31\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
[\[43\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
[\[98\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
[\[109\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE)
https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE

<https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE>

[\[9\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)
[\[54\]](https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53)
https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53

<https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-53>

[\[10\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
[\[79\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
[\[105\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
[\[124\]](https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html)
https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html

<https://ethz.ch/en/news-and-events/eth-news/news/2025/09/press-release-apertus-a-fully-open-transparent-multilingual-language-model.html>

[\[15\]](https://allenai.org/olmo) [\[101\]](https://allenai.org/olmo)
https://allenai.org/olmo

<https://allenai.org/olmo>

[\[16\]](https://osai-index.eu/database/)
https://osai-index.eu/database/

<https://osai-index.eu/database/>

[\[17\]](https://huggingface.co/allenai/Olmo-3-1125-32B)
[\[52\]](https://huggingface.co/allenai/Olmo-3-1125-32B)
[\[99\]](https://huggingface.co/allenai/Olmo-3-1125-32B)
[\[122\]](https://huggingface.co/allenai/Olmo-3-1125-32B)
https://huggingface.co/allenai/Olmo-3-1125-32B

<https://huggingface.co/allenai/Olmo-3-1125-32B>

[\[19\]](https://osai-index.eu/) https://osai-index.eu/

<https://osai-index.eu/>

[\[20\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)
[\[22\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)
[\[30\]](https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true)
https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true

<https://crfm.stanford.edu/fmti/December-2025/index.html?openLinerExtension=true>

[\[25\]](https://mistral.ai/it/news/mistral-3/)
[\[80\]](https://mistral.ai/it/news/mistral-3/)
https://mistral.ai/it/news/mistral-3/

<https://mistral.ai/it/news/mistral-3/>

[\[26\]](https://openai.com/index/introducing-gpt-oss/)
[\[116\]](https://openai.com/index/introducing-gpt-oss/)
https://openai.com/index/introducing-gpt-oss/

<https://openai.com/index/introducing-gpt-oss/>

[\[28\]](https://opensource.org/ai/final-board-report)
https://opensource.org/ai/final-board-report

<https://opensource.org/ai/final-board-report>

[\[29\]](https://allenai.org/blog/olmo3)
[\[33\]](https://allenai.org/blog/olmo3)
[\[102\]](https://allenai.org/blog/olmo3)
[\[121\]](https://allenai.org/blog/olmo3) https://allenai.org/blog/olmo3

<https://allenai.org/blog/olmo3>

[\[32\]](https://ai.google.dev/gemma/docs/core/model_card_4)
[\[34\]](https://ai.google.dev/gemma/docs/core/model_card_4)
[\[103\]](https://ai.google.dev/gemma/docs/core/model_card_4)
https://ai.google.dev/gemma/docs/core/model_card_4

<https://ai.google.dev/gemma/docs/core/model_card_4>

[\[35\]](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/LICENSE-MODEL?trk=public_post_comment-text)
https://github.com/deepseek-ai/DeepSeek-V3/blob/main/LICENSE-MODEL?trk=public_post_comment-text

<https://github.com/deepseek-ai/DeepSeek-V3/blob/main/LICENSE-MODEL?trk=public_post_comment-text>

[\[36\]](https://www.deepseek.com/en/news/v3-0324/)
https://www.deepseek.com/en/news/v3-0324/

<https://www.deepseek.com/en/news/v3-0324/>

[\[37\]](https://docs.mistral.ai/models?ref=aidatahub)
[\[57\]](https://docs.mistral.ai/models?ref=aidatahub)
[\[112\]](https://docs.mistral.ai/models?ref=aidatahub)
https://docs.mistral.ai/models?ref=aidatahub

<https://docs.mistral.ai/models?ref=aidatahub>

[\[38\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)
[\[76\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)
[\[132\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4)
https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4

<https://huggingface.co/openGPT-X/Teuken-7B-instruct-commercial-v0.4>

[\[39\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6)
[\[95\]](https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6)
https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6

<https://huggingface.co/openGPT-X/Teuken-7B-instruct-v0.6>

[\[40\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)
[\[63\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)
[\[64\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)
[\[127\]](https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf)
https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf

<https://secure.igenius.ai/Website/Media/iGenius%2BAI%2BEnglish%2BPress%2BRelease%2B060624.pdf>

[\[41\]](https://www.domyn.com/news/introducing-domyn)
[\[129\]](https://www.domyn.com/news/introducing-domyn)
https://www.domyn.com/news/introducing-domyn

<https://www.domyn.com/news/introducing-domyn>

[\[42\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md)
https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md

<https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md>

[\[45\]](https://huggingface.co/static/bigscience/license/index.html)
[\[118\]](https://huggingface.co/static/bigscience/license/index.html)
https://huggingface.co/static/bigscience/license/index.html

<https://huggingface.co/static/bigscience/license/index.html>

[\[46\]](https://github.com/openai/gpt-oss/blob/main/LICENSE)
[\[117\]](https://github.com/openai/gpt-oss/blob/main/LICENSE)
https://github.com/openai/gpt-oss/blob/main/LICENSE

<https://github.com/openai/gpt-oss/blob/main/LICENSE>

[\[50\]](https://github.com/deepseek-ai/DeepSeek-R1/wiki)
https://github.com/deepseek-ai/DeepSeek-R1/wiki

<https://github.com/deepseek-ai/DeepSeek-R1/wiki>

[\[51\]](https://opensource.org/ai/drafts/the-open-source-ai-definition-1-0-rc1)
https://opensource.org/ai/drafts/the-open-source-ai-definition-1-0-rc1

<https://opensource.org/ai/drafts/the-open-source-ai-definition-1-0-rc1>

[\[55\]](https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source)
https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source

<https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-does-ai-act-apply-general-purpose-ai-models-released-open-source>

[\[56\]](https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf)
https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf

<https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf>

[\[58\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)
[\[60\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)
[\[126\]](https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/)
https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/

<https://fondazione-fair.it/news/minerva-7b-la-nuova-frontiera-dei-modelli-linguistici-italiani-presentata-dalla-sapienza/>

[\[59\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)
[\[67\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)
[\[91\]](https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0)
https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0

<https://huggingface.co/sapienzanlp/Minerva-7B-base-v1.0>

[\[61\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)
[\[62\]](https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md)
https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md

<https://huggingface.co/m-polignano/ANITA-NEXT-24B-Magistral-2506-ITA/blob/main/README.md>

[\[65\]](https://huggingface.co/Almawave/Velvet-14B)
[\[66\]](https://huggingface.co/Almawave/Velvet-14B)
https://huggingface.co/Almawave/Velvet-14B

<https://huggingface.co/Almawave/Velvet-14B>

[\[68\]](https://eurollm.io/) https://eurollm.io/

<https://eurollm.io/>

[\[69\]](https://openeurollm.eu/launch-press-release)
https://openeurollm.eu/launch-press-release

<https://openeurollm.eu/launch-press-release>

[\[70\]](https://www.openeurollm.eu/) https://www.openeurollm.eu/

<https://www.openeurollm.eu/>

[\[71\]](https://openeurollm.eu/blog) https://openeurollm.eu/blog

<https://openeurollm.eu/blog>

[\[72\]](https://openllm-france.fr/fr/main-page-fr/)
https://openllm-france.fr/fr/main-page-fr/

<https://openllm-france.fr/fr/main-page-fr/>

[\[73\]](https://openllm-france.fr/en/main-page-en/)
[\[90\]](https://openllm-france.fr/en/main-page-en/)
[\[131\]](https://openllm-france.fr/en/main-page-en/)
https://openllm-france.fr/en/main-page-en/

<https://openllm-france.fr/en/main-page-en/>

[\[74\]](https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text)
[\[92\]](https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text)
https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text

<https://www.iais.fraunhofer.de/de/branchen-themen/themen/generative-ki/opengpt-x.html?trk=public_post_comment-text>

[\[75\]](https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html)
https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html

<https://www.iais.fraunhofer.de/en/industries_and_cross-sector_solutions/cross-sector_solutions/generative-ai/opengpt-x.html>

[\[77\]](https://www.swiss-ai.org/) https://www.swiss-ai.org/

<https://www.swiss-ai.org/>

[\[78\]](https://apertus-ai.org/pages/about/)
https://apertus-ai.org/pages/about/

<https://apertus-ai.org/pages/about/>

[\[81\]](https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf)
https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf

<https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_24_6302/IP_24_6302_EN.pdf>

[\[82\]](https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion)
[\[133\]](https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion)
https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion

<https://digital-strategy.ec.europa.eu/en/funding/eu-launches-ai-gigafactories-call-boost-europes-computing-capacity-and-unlock-more-eu30-billion>

[\[83\]](https://www.alt-edic.eu/projects/llms4eu/)
https://www.alt-edic.eu/projects/llms4eu/

<https://www.alt-edic.eu/projects/llms4eu/>

[\[84\]](https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf)
[\[134\]](https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf)
https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf

<https://www.agid.gov.it/sites/default/files/repository_files/05_cs_pubblicazione_strategia_intelligenza_artificiale.pdf>

[\[85\]](https://iris.uniroma1.it/bitstream/11573/1727996/3/Moroni_ITA-Bench_2024.pdf)
https://iris.uniroma1.it/bitstream/11573/1727996/3/Moroni_ITA-Bench_2024.pdf

<https://iris.uniroma1.it/bitstream/11573/1727996/3/Moroni_ITA-Bench_2024.pdf>

[\[86\]](https://arxiv.org/html/2502.02289v1)
[\[88\]](https://arxiv.org/html/2502.02289v1)
[\[136\]](https://arxiv.org/html/2502.02289v1)
https://arxiv.org/html/2502.02289v1

<https://arxiv.org/html/2502.02289v1>

[\[87\]](https://huggingface.co/Almawave/Velvet-2B)
https://huggingface.co/Almawave/Velvet-2B

<https://huggingface.co/Almawave/Velvet-2B>

[\[89\]](https://huggingface.co/spaces/evalitahf/evalita_llm_leaderboard)
https://huggingface.co/spaces/evalitahf/evalita_llm_leaderboard

<https://huggingface.co/spaces/evalitahf/evalita_llm_leaderboard>

[\[93\]](https://fondazione-fair.it/en/news/minerva-7b-the-new-frontier-of-italian-language-models-unveiled-by-sapienza/)
https://fondazione-fair.it/en/news/minerva-7b-the-new-frontier-of-italian-language-models-unveiled-by-sapienza/

<https://fondazione-fair.it/en/news/minerva-7b-the-new-frontier-of-italian-language-models-unveiled-by-sapienza/>

[\[106\]](https://mistral.ai/news/mistral-small-4/)
[\[113\]](https://mistral.ai/news/mistral-small-4/)
https://mistral.ai/news/mistral-small-4/

<https://mistral.ai/news/mistral-small-4/>

[\[108\]](https://opensource.org/blog/the-open-source-initiative-announces-the-release-of-the-industrys-first-open-source-ai-definition)
https://opensource.org/blog/the-open-source-initiative-announces-the-release-of-the-industrys-first-open-source-ai-definition

<https://opensource.org/blog/the-open-source-initiative-announces-the-release-of-the-industrys-first-open-source-ai-definition>

[\[110\]](https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md?_bhlid=465b0c8311ac465d0fceabb3634d7a77db379746)
https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md?\_bhlid=465b0c8311ac465d0fceabb3634d7a77db379746

<https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md?_bhlid=465b0c8311ac465d0fceabb3634d7a77db379746>

[\[114\]](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/)
https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/

<https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/>

[\[119\]](https://scancode-licensedb.aboutcode.org/bigscience-open-rail-m.LICENSE)
https://scancode-licensedb.aboutcode.org/bigscience-open-rail-m.LICENSE

<https://scancode-licensedb.aboutcode.org/bigscience-open-rail-m.LICENSE>

[\[120\]](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/LICENSE.md)
https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/LICENSE.md

<https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/LICENSE.md>

[\[123\]](https://huggingface.co/datasets/allenai/dolma3_mix-150B-1025/blob/main/README.md)
https://huggingface.co/datasets/allenai/dolma3_mix-150B-1025/blob/main/README.md

<https://huggingface.co/datasets/allenai/dolma3_mix-150B-1025/blob/main/README.md>

[\[125\]](https://huggingface.co/swiss-ai/Apertus-70B-2509/blob/main/LICENSE.txt)
https://huggingface.co/swiss-ai/Apertus-70B-2509/blob/main/LICENSE.txt

<https://huggingface.co/swiss-ai/Apertus-70B-2509/blob/main/LICENSE.txt>

[\[128\]](https://secure.igenius.ai/legal/iGenius%2BLicense%2BItalia%2B10B.pdf)
https://secure.igenius.ai/legal/iGenius%2BLicense%2BItalia%2B10B.pdf

<https://secure.igenius.ai/legal/iGenius%2BLicense%2BItalia%2B10B.pdf>

[\[130\]](https://www.domyn.com/news/introducing-domyn-small-an-open-european-reasoning-llm-built-for-ai-ownership)
https://www.domyn.com/news/introducing-domyn-small-an-open-european-reasoning-llm-built-for-ai-ownership

<https://www.domyn.com/news/introducing-domyn-small-an-open-european-reasoning-llm-built-for-ai-ownership>

[\[135\]](https://www.governo.it/it/search/node/132)
https://www.governo.it/it/search/node/132

<https://www.governo.it/it/search/node/132>

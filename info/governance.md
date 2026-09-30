# Open Models and Licensing: A Governance Guide for LLM Engineers

**Status: 30 September 2026.** This report uses “open source AI” narrowly where possible, distinguishing it from **open weights**. Model/license status is checkpoint-specific: Gemma, DeepSeek, Mistral, Teuken, and the former iGenius/Domyn portfolio all contain examples where materially different licenses coexist across generations or variants. citeturn15view2turn20search1turn23search2

## Executive summary

- **“Open” is not a binary property of a model.** A released model can expose weights while withholding training data, data provenance, training code, hyperparameters, intermediate checkpoints, or even the exact recipe. Liesenfeld & Dingemanse therefore treat openness as a **multidimensional, graded property**, rather than equating downloadable weights with open source. The 2026 European Open Source AI Index operationalizes essentially the same idea across data, code, documentation, hardware, architecture, weights and licensing dimensions. citeturn0search0turn0search1turn0search5
- **Open weights ≠ open source.** OSI's Open Source AI Definition 1.0 requires the freedoms to use, study, modify and share the system, together with the preferred form for making modifications: sufficiently detailed **Data Information**, complete training/inference code, and model parameters under appropriate open licenses. It deliberately does **not** require publication of every training example. citeturn0search3turn1search4turn1search6
- **OSI's data compromise remains disputed.** Releasing only information sufficient to reconstruct a substantially equivalent dataset makes OSAID more practicable when data cannot legally be redistributed, but it weakens exact reproducibility and data-level auditing. OSI explicitly made this trade-off; it should not be paraphrased as “OSI requires open training data.” citeturn1search4turn1search6
- **A permissive weight license is still not sufficient for full openness.** Qwen3, gpt-oss, Gemma 4 and the current Apache-licensed Mistral models are excellent examples: their weights can be modified and commercially redistributed under Apache 2.0, but the original full training datasets and end-to-end model-building pipelines are not generally published. OLMo 3 and Apertus go much further by publishing data/model-flow artifacts and training machinery. citeturn7search1turn8search1turn3search1turn20search0turn6search3turn10search6
- **The biggest recent licensing change for teaching purposes is Gemma 3 → Gemma 4.** Gemma 3 remains under Google's custom Gemma Terms, including prohibited-use restrictions that cascade to downstream distributions; Gemma 4 is instead released under **Apache 2.0**. citeturn15view2turn3search1
- **Llama 4 remains open-weight, not OSI-open-source.** Redistribution requires notices and “Built with Llama”; certain distributed models trained using Llama materials or outputs must use a name beginning with “Llama”; entities above 700 million monthly active users require a separate Meta licence; and, unusually, the Llama 4 licence grants no model-use rights for its multimodal models to individuals domiciled or companies principally established in the EU, although end users of products incorporating them are carved out. citeturn5search0turn5search4
- **Derivatives inherit more than engineers often expect.** Gemma 3 explicitly defines synthetic-output distillation as potentially creating a “Model Derivative”; Llama imposes downstream naming/notice requirements; and DeepSeek's R1 distill checkpoints inherit their Qwen or Llama base-model licences even though DeepSeek-R1 itself is MIT-licensed. citeturn15view4turn5search0turn23search2
- **Under the EU AI Act, “free and open source” is an exemption, not a blanket exclusion.** For qualifying GPAI models, Article 53(2) removes the Article 53(1)(a) technical-documentation and 53(1)(b) downstream-information duties. It does **not** remove the Article 53(1)(c) copyright-policy obligation or 53(1)(d) public training-content-summary obligation, and the exemption does not apply to GPAI models with systemic risk. citeturn13view0
- **Europe now has several distinct sovereignty strategies rather than one “European LLM”.** They range from highly reproducible public efforts such as Apertus and OpenEuroLLM, through multilingual EuroLLM and Teuken, to commercially developed Mistral and Domyn models. Italy additionally has Minerva, Velvet and the LLaMAntino/ANITA line. Their openness levels are substantially different. citeturn10search6turn18search0turn18search4turn19search4turn16search1turn17search3turn17search8
- **For engineering, “Can I download it?” is the wrong licensing question.** Before committing to a model, record at least: exact checkpoint and licence version; commercial-use permission; fine-tuning/distillation/merging rights; hosted-service and redistribution conditions; geographic or scale restrictions; attribution/naming obligations; licences of training and fine-tuning datasets; data provenance; and the applicable AI Act role and model/system classification. citeturn0search3turn13view0turn15view4turn23search2

## What makes a model “open”

A useful engineering model is to treat a foundation-model release as a **bundle of separately openable artifacts**. Downloadability of one artifact—usually the weights—says little about the others. This is the central insight behind Liesenfeld & Dingemanse's FAccT 2024 analysis and the later European Open Source AI Index. citeturn0search0turn0search5

| Component | What a genuinely useful release contains | Why engineers/researchers need it |
|---|---|---|
| **Weights / parameters** | Final weights; ideally intermediate checkpoints and optimizer state where useful | Allows local inference, fine-tuning, inspection and independent hosting. OSI expressly treats model parameters as part of the preferred form for modification. citeturn0search3turn1search4 |
| **Inference code** | Architecture implementation, tokenizer/processor, generation/inference code and configuration | Weights without compatible executable machinery may be practically unusable or difficult to reproduce. OSI includes inference and architecture code in its required source code. citeturn0search3 |
| **Training code and recipe** | Preprocessing/filtering code, optimizer, schedules, hyperparameters, distributed-training configuration, post-training/RL/SFT recipe, evaluation | Necessary to understand *how* the weights arose and to retrain or materially modify the system; OSI requires complete source sufficient for training and running the system. citeturn0search3turn1search4 |
| **Training data** | Best case: the actual curated training mixture in training-ready form | Enables exact data auditing, deduplication studies, contamination analysis and close reproduction. OLMo/Dolma and OpenLLM-France explicitly emphasize this level of transparency. citeturn6search7turn9search7turn18search5 |
| **Data information** | At minimum: provenance, sources, scope, characteristics, selection/filtering/labeling processes, and how obtainable datasets can be acquired | This is the **OSAID 1.0 minimum** where releasing the entire corpus is impossible; it is deliberately weaker than publishing the dataset. citeturn0search3turn1search4 |
| **Documentation** | Model card, technical report, architecture, limitations, evaluations, intended use, risks, dataset documentation | Supports auditability, reproducibility and downstream risk assessment. Both the European index and Stanford FMTI score documentation/transparency separately from weight availability. citeturn0search5turn0search2 |
| **Licences** | Separate, compatible licences for model/weights, source code and datasets | A public artifact is not necessarily legally reusable. The OLMo ecosystem illustrates the distinction: model code/weights use Apache 2.0 while Dolma 3 uses ODC-BY and underlying source terms can still matter. citeturn9search0turn9search7turn9search3 |

### Openness is composite, not binary

Liesenfeld & Dingemanse's FAccT 2024 study examines openness along **14 dimensions**, surveying 40 text-generating LLMs and six text-to-image systems. Its central conclusion is that calling models simply “open” or “closed” hides large differences: many prominent releases are essentially **open-weight systems**, while training data and other resources necessary for reproduction remain unavailable. They describe misleadingly broad “open” claims as a form of **open-washing**. citeturn0search0turn0search4

The **European Open Source AI Index**, whose current index was generated in July 2026, goes in the same direction. It independently tracks such dimensions as base-model and end-user-model data, weights, training code, code documentation, compute/hardware information, architecture, papers/preprints, model cards, datasheets and licences. Its upper ranks include highly documented/reproducible projects such as YuLan-Mini, BLOOM/BLOOMZ, OLMo 3 and Apertus, whereas prominent permissively licensed weight releases can rank materially lower because the training pipeline and data remain unavailable. citeturn0search1turn0search5

Stanford CRFM's **latest Foundation Model Transparency Index found in this review is the December 2025 edition**. It assesses 13 companies using 100 indicators and reports a mean transparency score of 41, down 17 points from 2024. IBM scored 95; open-weight providers were not automatically highly transparent—DeepSeek scored 32 and Alibaba 26—and Mistral's score fell substantially relative to its previous evaluation. FMTI is broader than an open-source test: it evaluates corporate/model transparency, including upstream and downstream information, rather than deciding whether a licence is “open source.” citeturn0search2turn0search6

The three frameworks therefore ask related but different questions:

| Framework | Main question | Important consequence |
|---|---|---|
| **Liesenfeld & Dingemanse, FAccT 2024** | *How open is the complete release in practice?* | Exposes “open-washing” produced by reducing openness to weights. citeturn0search0 |
| **European Open Source AI Index, 2026** | *Which reproducibility/open-science artifacts have actually been released?* | Produces a **graded openness score**, so two Apache-licensed models can receive very different evaluations. citeturn0search1turn0search5 |
| **Stanford FMTI, Dec. 2025** | *How transparent are major foundation-model providers across their ecosystem?* | Transparency is broader than source availability and open licensing. citeturn0search2 |
| **OSI OSAID 1.0** | *Does an AI system satisfy a normative definition of “open source AI”?* | Requires the four freedoms plus data information, code and parameters in preferred form for modification. citeturn0search3 |

### “Open-washing”

For lecture purposes, a precise definition is:

> **Open-washing is presenting an AI system as “open” or “open source” on the basis of a selectively disclosed component—most commonly downloadable weights—while material artifacts or legal freedoms necessary to study, reproduce, modify or freely use the system remain unavailable or restricted.** This is the phenomenon highlighted by Liesenfeld & Dingemanse. citeturn0search0

Three contemporary patterns make the idea concrete.

**Llama 4:** the weights are downloadable, but the licence contains use restrictions, an additional licence requirement above 700 million MAU, branding/naming obligations, and an EU-specific exclusion for rights to use Llama 4 multimodal models. It therefore fails OSI's “use for any purpose” criterion. Calling this simply “open source” would collapse open weights and open-source freedoms. citeturn5search0turn5search4turn0search3

**Gemma 3:** weights are accessible and commercial use is possible, but use is governed by Google's custom terms and incorporated prohibited-use policy; downstream distributors must contractually pass those restrictions onward. Again, this is open access to weights, not OSI-style unrestricted open source. citeturn15view2

**Mistral 3:** Mistral itself calls the Apache-2.0 models “open-source,” while the European Open Source AI Index explicitly treats Mistral's recent releases as much less open with respect to upstream artifacts than projects such as OLMo. The Apache licence makes the **released weight artifact** highly reusable; it does not reconstruct the undisclosed training corpus or complete model-building process. citeturn20search2turn0search1

By contrast, OpenAI describes gpt-oss principally as **open-weight** and releases its weights under Apache 2.0. That terminology is more technically precise because the release does not purport to provide the complete original training-data pipeline. citeturn8search1turn8search7

## Open weights versus open source

### The OSI Open Source AI Definition

OSAID 1.0, finalized in October 2024, says users of an Open Source AI system must be able, without requesting permission, to:

1. use the system **for any purpose**;
2. study how it works and inspect its components;
3. modify it for any purpose;
4. share the system, with or without modifications. citeturn0search3turn1search6

The “preferred form for making modifications” must include three classes of material. **Data Information** must describe provenance, scope, characteristics, collection/selection/labeling/filtering/processing and identify publicly or commercially obtainable training sources sufficiently for a skilled person to build a substantially equivalent system. **Code** must cover the complete training and execution pipeline. **Parameters**—including weights and configuration—must be available under appropriate open terms. citeturn0search3turn1search4

The controversial part is the first one. **OSAID does not require that every training example itself be released.** OSI argues that datasets can contain personal, confidential, copyrighted or otherwise non-redistributable material, so requiring publication of all data would rule out systems whose development can nevertheless be meaningfully studied and replicated. Critics reasonably answer that “data information” does not enable exact data auditing or exact reproduction. This is a genuine design dispute, not a factual disagreement about what OSAID says. citeturn1search4turn1search6

OSI's initial validation exercise reported **Pythia, OLMo, Amber, CrystalCoder and T5** as systems that passed its then-current review; BLOOM, StarCoder2 and Falcon were described as potentially passing with licensing changes. Llama 2, Grok, Phi-2 and Mixtral lacked required components. This should be taught as an **initial validation set**, not as a permanent OSI certification registry for all later model versions. citeturn1search0

Consequently, it is safer to say that OLMo 3 and Apertus are **strongly aligned with the substantive OSAID criteria** than to claim that their latest checkpoints have received a formal OSI certification. Both publish substantially more of their model-production flow than ordinary open-weight releases. citeturn6search3turn10search6

### A practical taxonomy as of September 2026

“Permissive open weights” below means that the released weights have an OSI-approved software-style licence such as Apache 2.0 or MIT, **not** that the complete AI system satisfies OSAID.

| Category | Representative models/families | What is actually open | Main limitation |
|---|---|---|---|
| **Closed / API-only** | Proprietary OpenAI GPT family other than gpt-oss; Anthropic Claude family; hosted Google Gemini family; Mistral **Premier** models | API/interface and documentation | No downloadable frontier-model weights; modification and redistribution depend on provider service terms. Stanford FMTI treats these providers as transparency subjects rather than open-source systems; Mistral's current catalogue explicitly distinguishes open licences from “Premier.” citeturn0search2turn20search1turn8search1 |
| **Open weights, restrictive licence** | **Llama 4**; **Gemma 3 / 3n**; Teuken-7B v0.6; BLOOM/OpenRAIL-style releases | Weights, often inference tooling and model cards | Use-based, geographic, commercial or downstream contractual restrictions mean “use for any purpose” is absent. citeturn5search0turn15view2turn19search3turn23search1 |
| **Open weights, permissive licence** | **Gemma 4**; **Qwen3**; **DeepSeek-R1** and MIT V3 releases; **gpt-oss**; **Mistral Large 3 / Small 4** | Weights under Apache 2.0 or MIT; local/commercial modification and redistribution generally allowed subject to standard notices | Training corpus and complete original training pipeline are not generally reproduced as part of the release, so these are usually not “fully open” in the open-science sense. citeturn3search1turn7search1turn23search2turn8search1turn20search0turn20search2 |
| **Fully / near-fully open model flow** | **OLMo 3**; **Apertus**; **Minerva 7B**; OpenEuroLLM/open-sci reference releases | Weights + extensive training code/recipes + data or data pipeline + documentation; often intermediate checkpoints | Reproducibility can still depend on enormous compute and third-party source-data terms; “fully open” here describes the artifact bundle, not formal OSI certification. citeturn6search3turn6search7turn10search6turn16search1turn18search4turn18search10 |

Several 2025–26 changes are especially slide-worthy:

| Model | Earlier state | Current state relevant to engineers |
|---|---|---|
| **Gemma 3 → Gemma 4** | Gemma 3 uses Google's custom Gemma Terms with cascading use restrictions. citeturn15view2 | Gemma 4 is **Apache 2.0**, a major simplification for commercial reuse, fine-tuning and redistribution. citeturn3search1 |
| **DeepSeek-V3** | Early V3 releases used a bespoke model licence with use restrictions. citeturn6search4 | DeepSeek announced V3-0324 under **MIT**, matching the permissive R1 licensing direction. Do not infer one licence from the family name: inspect the exact checkpoint. citeturn8search9 |
| **Mistral** | Historically mixed Apache, research and commercial models. | Still mixed: Large 3 and Small 4 are Apache 2.0; current Medium 3.5 uses a **Modified MIT** licence; OCR/Codestral and several service models are “Premier.” citeturn20search1turn20search0turn20search3 |
| **Teuken** | Commercial v0.4 released under Apache 2.0. citeturn19search0 | Newer 6T-token v0.6 is **CC-BY-NC-4.0** and explicitly non-commercial. “Newer” therefore does not imply “more permissive.” citeturn19search3turn19search4 |
| **iGenius / Domyn** | Italia was initially announced as MIT/open source; the subsequent Italia 10B licence instead prohibited modification, redistribution and derivatives without written consent. citeturn17search5turn16search3 | iGenius became **Domyn** in June 2025; the separate Domyn Small 10B release of May 2026 has MIT-licensed open weights. This is a portfolio evolution, not evidence that old Italia checkpoints were retroactively relicensed. citeturn17search4turn17search8 |

### What restrictive licences mean in practice

| Licence/model | On-premise inference | Fine-tuning | Hosted service | Redistributing model / fine-tune | Engineering consequence |
|---|---|---|---|---|---|
| **Llama 4 Community Licence** | Generally yes, **but the multimodal licence grant is not made to EU-domiciled individuals or EU-principal-place-of-business companies**. citeturn5search4 | Generally permitted for eligible licensees. | Permitted subject to licence/AUP; EU end-user carve-out does not give an EU company itself the underlying model licence. citeturn5search4 | Must provide licence/notice and prominent **“Built with Llama”** attribution. A distributed AI model trained/fine-tuned/improved using Llama materials or outputs must, in the specified circumstances, begin its name with **“Llama”**. >700M MAU entities need a separate licence. citeturn5search0 | **Poor fit for an EU company wanting Llama 4 multimodal on premises.** It is open-weight but not OSI-open. |
| **Gemma 3 Terms** | Yes, subject to prohibited-use policy. citeturn15view2 | Yes, but resulting derivatives remain subject to restrictions. | Explicitly treated as “Distribution” via a Hosted Service. citeturn15view3 | Downstream agreements must include the prohibited-use restrictions as enforceable terms; recipients get a copy of the agreement and modified-file notices. citeturn15view2 | Commercially usable, but compliance obligations **flow down** to SaaS customers and redistributions. |
| **Gemma 4 / Apache 2.0** | Yes. | Yes. | Yes. | Yes, subject principally to Apache notice/patent requirements. | Much simpler than Gemma 3; still distinguish permissive weights from fully open training. citeturn3search1 |
| **BigScience OpenRAIL / OpenRAIL-M family** | Yes for permitted purposes. | Yes for permitted purposes. | Yes, but end users must respect use restrictions. | Use restrictions must be included as enforceable downstream terms for derivatives. citeturn23search1turn23search3 | “Open” in the Responsible-AI-Licence vocabulary, **not OSI-open source**, because field/use restrictions contradict the OSI freedom to use for any purpose. citeturn0search3 |
| **MIT / Apache open weights** | Yes. | Yes. | Yes. | Generally yes, including commercial redistribution, subject to the licence's attribution/notices and, for Apache, patent provisions. | Preferred default where a company wants maximum product/licensing flexibility—while still checking dataset and base-model licences. citeturn8search2turn9search0 |

Google's Gemma 3 clause allowing Google, “to the maximum extent permitted by law,” to restrict use **“remotely or otherwise”** where it reasonably believes the agreement is being violated is noteworthy. It is a **contractual reservation of a right**, not evidence that every self-hosted Gemma weight file contains a remotely activatable kill switch. citeturn15view2turn15view3

### Fine-tunes, distillation, merges, data and outputs

Licensing becomes most error-prone after the first fine-tune.

**Fine-tunes.** A fine-tuned model containing the original parameters normally remains subject to whatever downstream conditions the original licence asserts. With permissive Apache/MIT models this is usually straightforward. Gemma 3 requires its use restrictions to propagate. Llama carries its notice/naming conditions. citeturn15view2turn5search0

**Distillation is licence-specific.** Gemma 3's definition is unusually explicit: its “Model Derivatives” include models produced by transferring patterns from Gemma's weights, operations **or outputs**, including synthetic-output distillation; the raw outputs themselves are not Model Derivatives. citeturn15view4 DeepSeek-R1, by contrast, is MIT and expressly permits derivatives/distillation. But its published small distills are **fine-tunes of other base models**: Qwen-based R1 distills retain Apache 2.0, while the 8B and 70B Llama-based distills remain based on the applicable Llama 3.1/3.3 licences. citeturn23search2turn23search6

**Merges.** A merge that actually contains parameters from models A and B should be treated conservatively as needing to comply with **both applicable licence stacks**. A restrictive component is not “washed away” by merging it into an Apache model. A difficult underlying legal question remains: the extent to which model weights themselves attract copyright or other exclusive rights is not fully settled. OSI deliberately frames OSAID around the freedoms users must practically receive rather than resolving every jurisdiction's theory of IP protection for parameters. citeturn1search8turn0search3

**Training data has its own licence.** OLMo 3 demonstrates the correct separation. OLMo code/weights are Apache 2.0, but Dolma 3 is distributed under **ODC-BY**; attribution is therefore required when the dataset or derivatives of it are redistributed, and Ai2 warns that source material may itself carry additional source-specific terms. A model licence never automatically grants rights in its training corpus. citeturn9search0turn9search7turn9search2turn9search3

**Outputs can also be contractually constrained.** Gemma says Google claims no rights in generated output, yet using the model remains governed by the agreement. OpenRAIL similarly says the licensor claims no output ownership while requiring that output use not contravene the licence's restrictions. Llama goes further in one important downstream case: use of Llama **outputs to train/improve another distributed AI model** can activate Llama's naming requirement. Thus “the vendor does not own my output” and “I may use the output with no contractual restrictions” are logically separate propositions. citeturn15view5turn23search1turn5search0

### Free/open-source GPAI under the EU AI Act

The operative provision for general-purpose AI is **Article 53**.

| AI Act duty for GPAI provider | Ordinary GPAI | Qualifying free/open-source GPAI |
|---|---:|---:|
| Art. 53(1)(a): technical documentation | Required | **Exempt under Art. 53(2)** |
| Art. 53(1)(b): information/documentation for downstream AI-system providers | Required | **Exempt under Art. 53(2)** |
| Art. 53(1)(c): policy to comply with EU copyright law, including rights reservations under DSM Directive Art. 4(3) | Required | **Still required** |
| Art. 53(1)(d): publicly available sufficiently detailed summary of training content, using the AI Office template | Required | **Still required** |
| Additional systemic-risk obligations | If model qualifies as systemic-risk GPAI | **No FOSS escape:** Art. 53(2)'s exemption expressly does not apply to GPAI with systemic risk; Article 55 duties remain relevant. |

citeturn13view0

For Article 53(2), the model must be released under a free/open-source licence permitting **access, use, modification and distribution**, and its parameters—including weights—plus architecture and usage information must be publicly available. Importantly, the AI Act does **not** equate this condition with OSAID's much richer preferred-form requirements. A model can therefore qualify for the EU provision without publishing its exact training dataset. citeturn13view0turn0search3

There is also a related **Article 54** relief concerning the EU authorized-representative requirement for certain non-EU providers of genuinely free/open-source GPAI, subject to the statutory conditions and the systemic-risk exception. citeturn13view1

The **GPAI Code of Practice**, finalized in July 2025 and recognized by the Commission and AI Board as an adequate voluntary compliance instrument, operationalizes the Act through Transparency and Copyright chapters for ordinary GPAI and a Safety & Security chapter for GPAI with systemic risk. Using the Code is voluntary, but signatories receive a more structured compliance route and reduced regulatory uncertainty. citeturn11search1turn11search5

A useful lecture sentence is therefore:

> **The AI Act gives genuinely free/open-source GPAI a documentation discount, not a copyright exemption, not a training-data-summary exemption, and not a systemic-risk exemption.** citeturn13view0

## Italian and European open-model initiatives

European “sovereign AI” covers at least three different goals that should not be conflated: **where a model is developed**, **where it can be executed and its data processed**, and **whether the full model-building process can be independently inspected/reproduced**. Mistral, Apertus and OLMo-style projects illustrate that geographic sovereignty and open-science openness are distinct dimensions. citeturn20search1turn10search6turn6search7

### Italy

| Initiative | Actors / funding | Language/data profile | Licence & data openness | Release / current status |
|---|---|---|---|---|
| **Minerva** | Sapienza NLP within FAIR, with CINECA/NVIDIA support; funded through PNRR MUR project PE0000013-FAIR and PRIN research funding. citeturn16search0turn16search1 | Minerva-7B: ~2.48T tokens: ~1.14T Italian, 1.14T English and 200B code, i.e. roughly **46% Italian tokens** before the code component. citeturn16search1 | Apache 2.0 model; team describes Minerva as “truly-open (data and model)” and documents its training sources/process. citeturn16search1 | Minerva-7B unveiled Nov. 2024; research-grade downloadable Italian/English model family. citeturn16search0 |
| **LLaMAntino / ANITA** | University of Bari researchers Marco Polignano, Pierpaolo Basile, Giovanni Semeraro and collaborators; family evolved from Italian adaptation of Llama-family models to ANITA/NEXT derivatives. citeturn16search2 | Primarily Italian + English adaptation rather than from-scratch Italian pretraining; recent ANITA-NEXT includes Mistral/Magistral-derived models and multimodal variants. citeturn16search2turn16search6 | **Caution:** the ANITA-NEXT Magistral model's HF metadata says Apache-2.0, while model-card prose says “research only purposes.” Those statements conflict; a commercial user should obtain clarification rather than assume the metadata overrides the prose. citeturn16search2 | Active family with 2025–26-generation variants; useful research/adaptation project, but licence hygiene is weaker than on the cleanest releases. |
| **Italia / iGenius → Domyn** | Italian private company iGenius, renamed **Domyn on 5 June 2025**; training has used CINECA Leonardo. citeturn17search4turn17search8 | Original Italia targeted native Italian data; current Domyn Small supports 50+ languages with particular emphasis on major European languages including Italian. citeturn17search5turn17search8 | Original Italia 9B was announced as MIT; **Italia 10B later used a restrictive custom licence** requiring written consent for modification/redistribution/derivatives. Current, separate **Domyn Small 10B is MIT open-weight**. citeturn17search5turn16search3turn17search8 | Domyn Small released May 2026 and is positioned for controlled/on-prem enterprise use. Do not treat all historical “Italia/iGenius/Domyn” checkpoints as one licensing lineage. |
| **Velvet** | Almawave; trained on CINECA Leonardo. citeturn17search3 | Velvet-14B trained from scratch on six languages; approximately **23% of training data is Italian**, with >4T final training tokens plus 400B+ code tokens. citeturn17search3 | Apache 2.0 weights. Public-data sources were curated and documented, but this is not the same as providing the exact complete pretraining mixture in training-ready form. citeturn17search3 | 14B release Jan. 31, 2025; 2B release Feb. 2025. Model cards describe these checkpoints as static models. citeturn17search3turn17search7 |

The interesting governance contrast is **Minerva versus Italia 10B**. Both were publicly discussed as Italian sovereign/open AI, but Minerva's Apache/data-oriented academic release provides substantially stronger downstream reuse rights than the restrictive 2025 Italia 10B licence. “National model” therefore says essentially nothing about openness. citeturn16search1turn16search3

### Europe

| Initiative | Who / funding | Languages | Openness & licence | Status as of 30 Sep. 2026 |
|---|---|---|---|---|
| **EuroLLM** | Instituto Superior Técnico, Edinburgh, Instituto de Telecomunicações, Paris-Saclay, Unbabel, Sorbonne, Naver Labs, Amsterdam and others; supported by EuroHPC, Horizon Europe/UTTER and European research funding. citeturn18search0 | Current 22B flagship trained on >4T tokens across **35 languages including all 24 EU official languages**. citeturn18search0 | Project presents models as open source and downloadable. For engineering procurement, verify the exact HF checkpoint licence rather than relying solely on the umbrella site's “open source” wording. | 22B is the current flagship; 9B and 1.7B variants also released, with multimodal extensions in development. citeturn18search0 |
| **OpenEuroLLM** | 20-member European consortium led by Charles University and AMD Silo AI, with CINECA, CSC, SURF, Fraunhofer, BSC, universities and companies; **Digital Europe grant 101195233**. citeturn18search1turn18search4 | EU official languages and additional economically/socially relevant languages. | Explicit project goal is a **truly open stack: data, documentation, training/testing code, evaluation and models**. citeturn18search4 | Began 1 Feb. 2025; active. By 2025–26 it had released reference/scaling models and 38 monolingual 2.15B models and secured major EuroHPC allocations; the project remains broader than one finished frontier checkpoint. citeturn18search10 |
| **OpenLLM-France: Lucie → Luciole** | Nine formal partners plus associates; BPI France-funded research project begun Sept. 2024 for two years. citeturn18search8 | Lucie 7B used **>30% French**; successor Luciole 1B/8B/23B uses roughly 30% French plus major European languages. citeturn18search5 | Strong open-science commitment: training-ready datasets, final/intermediate weights, training and preprocessing code. Exact licences should be checked artifact-by-artifact. citeturn18search5 | Lucie is now complemented/superseded by the newer Luciole line; active research commons rather than merely a single model. |
| **Teuken / OpenGPT-X** | Fraunhofer IAIS/IIS, Jülich, DFKI, TU Dresden and industry; German BMWK funding of about **€14m**; project ran Jan. 2022–Mar. 2025. citeturn19search6 | From-scratch model covering all **24 EU languages**, approximately 50% non-English pretraining material. citeturn19search4 | Commercial v0.4: Apache 2.0. Newer v0.6: CC-BY-NC-4.0 and therefore non-commercial. citeturn19search0turn19search3 | Project funding has ended; models remain available. This makes Teuken a useful case study in post-project maintenance risk. citeturn19search4 |
| **Apertus** | ETH Zurich, EPFL and CSCS through the Swiss AI Initiative; initial resources included >10m GPU-hours on Alps and a CHF20m ETH Domain commitment. citeturn10search1 | Strongly multilingual; project reports extremely broad language coverage rather than an English-first corpus. citeturn10search0 | **Apache 2.0; architecture, code, weights, checkpoints, training process and data information/resources are openly released.** Designed explicitly around transparency and European/Swiss legal constraints. citeturn10search6turn10search8 | 1.0: Sep. 2025; smaller distillations 1.1: May 2026; **Apertus 1.5: July 2026**, adding multimodal/tool/reasoning capabilities; 2.0 planned for 2027. citeturn10search0 |
| **Mistral AI** | French private AI company. | Current Mistral 3 models advertise 40+ languages; company maintains both generalist and specialist models. citeturn20search2 | **Mixed portfolio**: Large 3 and Ministral 3 are Apache 2.0; Small 4 Apache 2.0; Medium 3.5 Modified MIT; several current specialist models are Premier/proprietary. Training data are not generally published. citeturn20search1turn20search0turn20search3 | One of Europe's strongest commercial model vendors; an example of **open weights and proprietary services coexisting in the same company**. |

### Infrastructure and sovereignty policy

A terminology correction matters here: **IT4LIA is an AI Factory, not an AI Gigafactory.**

The Commission selected **IT4LIA at CINECA in Bologna** in December 2024 as one of the first seven EuroHPC AI Factories, alongside sites in Barcelona, Finland, Luxembourg, Sweden, Germany and Greece. Austria and Slovenia participate with the Italian factory. The first seven AI Factories represented an aggregate €1.5 billion investment, half EU-financed, and are intended to combine compute, data and talent for startups, research, industry and public-sector AI. citeturn21search3

**AI Gigafactories are a separate, substantially larger initiative.** As of 30 September 2026 the EuroHPC procurement is still under way: the tender was published on 30 July 2026 and has a November 2026 submission deadline. It targets infrastructure capable of the complete lifecycle of very large frontier models. It is therefore premature to describe IT4LIA—or any site—as an already selected EU AI Gigafactory. citeturn21search0turn21search6

**ALT-EDIC's LLMs4EU** is complementary rather than a compute centre. The Digital Europe-funded project began in March 2025 for three years, involves organisations in 20 countries, aims to acquire/create language resources for all EU languages, and targets energy, telecom, tourism, public services and science, including support for SMEs fine-tuning models. citeturn21search1

Italy's national policy layer now consists of both the **Italian AI Strategy 2024–2026** and **Law No. 132 of 23 September 2025**, followed by implementing measures during 2026. The strategy explicitly argues that Italy should develop technology tailored to its own context rather than merely import generic systems, promotes open-source research artifacts, and calls for secure and reliable infrastructure for Public Administration. citeturn22search5turn22search0

### How good are the Italian models?

This is the part where overclaiming should be avoided.

**ITA-Bench** was designed specifically because translated English benchmarks alone are not a satisfactory measure of Italian capability: it combines translated standard tasks with manually curated Italian datasets such as Italian Word-in-Context and Italy-specific QA. citeturn22search2turn22search6

**Evalita-LLM**, introduced in 2025, goes further by using **ten native-Italian tasks**, including both multiple-choice and generative tasks, and multiple prompt formulations per task because model rankings can be sensitive to prompt choice. Its published analysis finds that few-shot prompting usually improves results and, unsurprisingly, newer/larger models generally perform better. citeturn21search11turn21search2

Concrete public model-card evidence illustrates the scale issue. For example, **Velvet-2B** reports 39.6 on Italian MMLU, 61.9 on ITA-Bench WinoGrande, 67.3 on ITA-Bench PIQA and 86.6 on the ITA-Bench SciQ variant. Those numbers establish that a small Italian-oriented model can be useful; they do **not** establish frontier-model superiority. citeturn17search7

The defensible conclusion from the currently published evidence is therefore:

> **Italian-specific pretraining improves linguistic representation and can provide attractive capability/size trade-offs, but there is no robust evidence that today's national Italian models collectively outperform the largest contemporary multilingual/open or closed frontier models.** The evaluation landscape changes faster than peer-reviewed Italian benchmark tables, and comparisons across ITA-Bench, Evalita-LLM and vendor benchmarks are not interchangeable. citeturn21search11turn22search2turn17search7

The public Evalita-LLM leaderboard continues to update, so a slide containing an exact rank should record the **leaderboard snapshot date** rather than presenting it as a stable model property. citeturn22search3

### Recurring European problems

**Language data remains the first bottleneck.** OpenLLM-France explicitly motivates French-focused datasets by the overrepresentation of English in open corpora; LLMs4EU similarly warns that less-resourced EU languages risk being left behind because the quantity and quality of suitable training material are insufficient. citeturn18search5turn21search1

**Compute dependence is the second.** Minerva depends on Leonardo; Teuken used JUWELS; EuroLLM used MareNostrum 5; Apertus relies on Alps; OpenEuroLLM has obtained millions of EuroHPC GPU-hours. “Open model” therefore does not imply that an independent group can afford to reproduce its training run. citeturn16search1turn19search3turn18search0turn10search1turn18search10

**Maintenance after project funding is structurally difficult.** OpenGPT-X formally ended in March 2025 even though Teuken remains downloadable; OpenLLM-France and OpenEuroLLM similarly operate in funded-project time horizons. This does not mean the artifacts disappear, but it creates a real engineering question about long-term checkpoint maintenance, vulnerability fixes, evaluation updates and ownership of downstream community support. The maintenance-risk statement is an inference from the projects' finite funding structures, not evidence that those projects have abandoned their models. citeturn19search6turn18search8turn18search4

**Public-administration adoption is still more aspiration than demonstrated large-scale deployment in the sources reviewed.** FAIR explicitly positions Minerva as potentially useful for Italian PA; LLMs4EU includes public services; IT4LIA is intended to make infrastructure available to public administrations. Those are credible enabling initiatives, but they should not be turned into a claim that Italian or European open LLMs have already become the standard production stack of public administrations. citeturn16search4turn21search1turn21search3

## Engineering take-aways

### Pre-adoption checklist

The useful compliance unit is **`model checkpoint + model licence version + code licences + data licences + deployment model + intended use`**, not a brand name.

| Question to record before architecture freeze | What to verify |
|---|---|
| **Exactly what artifact am I using?** | Pin repository, model/checkpoint hash, release date and licence revision. “Gemma,” “DeepSeek,” “Mistral” and “Teuken” are not licence identifiers. citeturn15view2turn20search1turn19search4 |
| **Is commercial use permitted?** | Apache/MIT usually yes; CC-BY-NC does not permit commercial use; custom community licences may introduce scale, field-of-use or use restrictions. citeturn19search3turn5search0 |
| **May we run it on premises?** | Check the model licence, not merely availability of weight files. For an EU organisation, Llama 4 multimodal is the clearest current geographic counterexample. citeturn5search4 |
| **May we fine-tune it?** | Inspect both licence grant and AUP; decide whether the tuned weights will themselves inherit use restrictions. citeturn15view2turn23search1 |
| **May we distil it?** | Check whether output-based distillation is addressed explicitly. Gemma 3 says yes—as a derivative; DeepSeek-R1 permits distillation, but published R1 distills inherit their base-model licences. citeturn15view4turn23search2 |
| **May we merge it with another checkpoint?** | Build a licence dependency graph for every parent. Satisfy all applicable notice, use and distribution conditions. |
| **May we redistribute weights or sell a fine-tuned model?** | Check attribution, NOTICE requirements, downstream AUP propagation, model-naming clauses and commercial thresholds. citeturn5search0turn15view2 |
| **Does “serving an API” count as distribution?** | Licence-specific. Gemma 3 explicitly includes hosted/API access in its definition of Distribution. citeturn15view3 |
| **Are there geography or company-size restrictions?** | Llama 4: EU multimodal restriction and >700M-MAU licence threshold. citeturn5search0turn5search4 |
| **What attribution/branding survives downstream?** | Apache/MIT notices, Gemma notices, Llama “Built with Llama” and naming requirements are different obligations. citeturn5search0turn15view2 |
| **What trained the model?** | Ask whether actual data, source list, or only vague categories are known; document copyright opt-out/provenance information and any personal-data issues. OSAID's “Data Information” is a useful minimum, not a guarantee of full data auditability. citeturn0search3turn1search4 |
| **What licence governs our own fine-tuning data?** | Model, code and data licences form separate dependency layers. Dolma/OLMo is a good reference architecture for keeping them distinct. citeturn9search0turn9search7 |
| **What about generated outputs?** | Check model licence/AUP and, for hosted access, service terms. Lack of vendor copyright claims does not imply absence of contractual restrictions. citeturn15view5turn23search1 |
| **Does the AI Act FOSS GPAI exemption actually apply?** | Verify that licence and publicly available parameters/architecture/usage info meet Art. 53(2); remember that copyright policy and training-content summary remain. citeturn13view0 |
| **Are we the GPAI provider, downstream provider, deployer—or several at once?** | Fine-tuning and redistributing a model can change the regulatory role. Model-level GPAI obligations and application-level AI-system/high-risk obligations are separate layers. citeturn13view0 |
| **Do we require reproducibility or merely self-hosting?** | For self-hosting, permissive weights may suffice. For scientific reproduction/audit, prefer OLMo 3, Apertus or another release exposing the full model flow. citeturn6search7turn10search6 |

### Scenario: a University of Bologna research assistant deployed on premises

Suppose a university laboratory wants a local RAG/chat system, wants to fine-tune it on university material, and wants students to reproduce experiments.

**Best category:** fully open or permissively licensed open-weight models.

**Strong candidates:** **OLMo 3** where reproducibility and training-data research matter; **Apertus** for a Europe-adjacent, extensively open model flow; **Minerva** for Italian-centric experiments; and, where only weights/customization are required, **Gemma 4, Qwen3, gpt-oss or an Apache-licensed Mistral model**. citeturn6search3turn10search6turn16search1turn3search1turn7search1turn8search1turn20search0

**Llama 4 multimodal is not an acceptable choice for the university itself under the standard Llama 4 licence**: an Italian university is an EU-established organisation and Meta's AUP says the relevant multimodal rights are not granted to an EU-principal-place-of-business company/organisation. The end-user carve-out does not solve the university's own model-use problem. citeturn5search4

Gemma 3 is technically usable, but Gemma 4's Apache licence removes substantial downstream licence-management complexity. citeturn15view2turn3search1

### Scenario: an Italian startup fine-tunes a model and sells the resulting model/SaaS

The startup wants freedom to fine-tune, host commercially, distribute a customer-specific checkpoint and perhaps later sell the model asset itself.

**Lowest-friction choices:** **Gemma 4, Qwen3, gpt-oss, DeepSeek-R1, Mistral Large 3/Small 4, OLMo 3 or Domyn Small**, subject to checking the exact version and all fine-tuning-data licences. Their weight licences are Apache 2.0 or MIT rather than use-restricted community licences. citeturn3search1turn7search1turn8search1turn23search2turn20search1turn9search0turn17search8

**Do not choose an R1 distill by reading only “DeepSeek-R1 / MIT.”** A Llama-based R1 distill retains the corresponding Llama base licence; a Qwen2.5-based distill uses the Qwen/Apache base terms. citeturn23search2turn23search6

Gemma 3 remains possible but forces prohibited-use clauses into downstream contractual arrangements. Llama 4 creates additional naming/attribution/scale constraints and, for an Italian company's use of the multimodal checkpoints, the EU restriction is decisive. Teuken v0.6 is unsuitable for a commercial product because it is CC-BY-NC. citeturn15view2turn5search0turn5search4turn19search3

### Scenario: an Italian public administration requires EU-controlled deployment and auditability

Here “sovereignty” should be decomposed into **operational sovereignty**—the ability to execute the system on infrastructure under European control—and **epistemic/audit sovereignty**—the ability to know how the model was made.

For maximum auditability, **Apertus** is especially attractive because it publishes architecture, weights, code, training process, datasets/data information and checkpoints under a permissive licence. **Minerva** is attractive when Italian-language orientation and an Italian public/research ecosystem dominate the decision. **OLMo 3** is not European, but it is one of the strongest options when the procurement criterion is reproducibility rather than developer nationality. citeturn10search6turn16search1turn6search7

For operational EU sovereignty with potentially stronger production performance, Apache-licensed **Mistral** models, **EuroLLM**, **Velvet** and **Domyn Small** are plausible candidates, but procurement should distinguish “weights can run inside our datacentre” from “we can audit the original training corpus.” citeturn20search0turn18search0turn17search3turn17search8

**IT4LIA/CINECA is infrastructure, not a model licence.** Using an EU AI Factory can solve compute and data-location requirements while leaving model provenance/licensing questions completely unchanged. citeturn21search3

For a five-slide lecture, the core engineering message can therefore be compressed to:

**Weights → licence → recipe → data → regulatory role.**  
A model is only as “open” as the layer that matters to the intended use.

## Consolidated references

**Concepts and measurement.** Liesenfeld, A. & Dingemanse, M., *Rethinking open source generative AI: open-washing and the EU AI Act*, FAccT 2024. citeturn0search0turn0search4 European Open Source AI Index, current 2026 index and model database. citeturn0search1turn0search5 Stanford CRFM, *Foundation Model Transparency Index*, December 2025 edition. citeturn0search2turn0search6

**Open Source AI Definition.** Open Source Initiative, *Open Source AI Definition 1.0*. citeturn0search3 OSI FAQ on training data and preferred form for modification. citeturn1search4 OSI final-definition announcement and rationale. citeturn1search6 OSI validation/board report on candidate systems. citeturn1search0

**Llama.** Meta, *Llama 4 Community License Agreement*. citeturn5search0turn5search3 Meta, *Llama 4 Acceptable Use Policy*, including EU multimodal restriction. citeturn5search4 Meta, Llama 4 model card. citeturn5search7

**Gemma.** Google, *Gemma Terms of Use*, revised 1 April 2026. citeturn15view2turn15view3turn15view4turn15view5 Google, *Gemma 4 Model Card*, including Apache-2.0 licence. citeturn3search1

**Mistral.** Mistral AI, current model catalogue distinguishing Apache, Modified MIT and Premier models. citeturn20search1turn20search5 Mistral AI, *Introducing Mistral 3*. citeturn20search2 Mistral AI, *Introducing Mistral Small 4*. citeturn20search0 Mistral AI, *Mistral Medium 3.5*. citeturn20search3

**Qwen, DeepSeek and gpt-oss.** Qwen team, Qwen3 model cards and repositories. citeturn7search1turn7search4 DeepSeek, *DeepSeek-R1* repository and licence notes, including licences of distilled checkpoints. citeturn23search2turn23search6 DeepSeek, V3-0324 MIT relicensing announcement. citeturn8search9 OpenAI, *Introducing gpt-oss*. citeturn8search1 OpenAI, gpt-oss Apache-2.0 licence and open-weight documentation. citeturn8search2turn8search7

**Responsible-AI licences.** BigScience, BLOOM / OpenRAIL licence text. citeturn23search1 BigScience/OpenRAIL-M licence, including cascading use-based restrictions and output provisions. citeturn23search3 CreativeML OpenRAIL++ example. citeturn23search5

**OLMo and data licensing.** Ai2, OLMo 3 release and model-flow documentation. citeturn6search3turn6search7 Ai2, OLMo-3-32B model card, Apache 2.0. citeturn9search0 Ai2, Dolma 3 and ODC-BY licensing documentation. citeturn9search7turn9search2turn9search3

**Apertus.** Swiss AI Initiative / Apertus official project site and release history. citeturn10search0 Swiss AI Initiative resource/funding information. citeturn10search1 ETH Zurich, Apertus release and openness documentation. citeturn10search6 Apertus Apache-2.0 model repository. citeturn10search8

**EU AI Act and GPAI Code.** European Commission AI Act Service Desk, Article 53 GPAI obligations and free/open-source exception. citeturn13view0 Article 54 open-source/authorized-representative treatment. citeturn13view1 European Commission, *General-Purpose AI Code of Practice*, July 2025 and current signatory information. citeturn11search1turn11search5

**Italian models.** FAIR/Sapienza, Minerva-7B announcement. citeturn16search0turn16search4 Sapienza NLP, Minerva model card, training mixture, funding and Apache licence. citeturn16search1 Polignano et al., ANITA-NEXT model documentation. citeturn16search2turn16search6 iGenius, original Italia announcement. citeturn17search5 iGenius, Italia 10B licence. citeturn16search3 Domyn, iGenius→Domyn rebranding. citeturn17search4 Domyn, *Introducing Domyn Small*, May 2026. citeturn17search8 Almawave, Velvet-14B and Velvet-2B model cards. citeturn17search3turn17search7

**European models and programmes.** EuroLLM project, current model family and funding acknowledgments. citeturn18search0 OpenEuroLLM launch, consortium and Digital Europe funding. citeturn18search1turn18search4 OpenEuroLLM progress and reference-model releases. citeturn18search10 OpenLLM-France, Lucie/Luciole and open-data/model commitments. citeturn18search5turn18search8 Fraunhofer/OpenGPT-X, Teuken release, licensing variants and project funding/status. citeturn19search0turn19search3turn19search4turn19search6 ALT-EDIC, LLMs4EU. citeturn21search1 European Commission, first seven EuroHPC AI Factories including IT4LIA/CINECA Bologna. citeturn21search3 European Commission/EuroHPC, 2026 AI Gigafactory procurement. citeturn21search0

**Italian policy and evaluation.** AgID, *Italian Strategy for Artificial Intelligence 2024–2026*. citeturn22search5 Italian Government, implementation of Law No. 132/2025 during 2026. citeturn22search0 Moroni et al., *ITA-Bench: Towards a More Comprehensive Evaluation for Italian LLMs*. citeturn22search2turn22search6 Magnini et al., *Evalita-LLM: Benchmarking Large Language Models on Italian* and public leaderboard. citeturn21search11turn22search3
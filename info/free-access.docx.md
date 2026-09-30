# Free-of-Charge Access to LLM APIs for Research, Study, and Learning

**Research snapshot: 30 September 2026.** This report distinguishes
genuinely free access from promotional credits, temporary trials, cloud
grants, institutional cost-sharing, and practices that merely shift or
evade payment. "Legal risk" below primarily means
contractual/Terms-of-Service risk; it is not a determination that a
practice is unlawful under any particular jurisdiction.

## Executive summary

- **The best legitimate route for academic researchers is increasingly
  provider-funded research credits rather than "hacks."** OpenAI
  currently offers eligible researchers up to **\$1,000 of API credits
  for 12 months** through its Researcher Access Program; Anthropic\'s
  expanded AI for Science program offers selected projects **up to
  \$50,000 in credits**; Cohere\'s rolling Catalyst Grants give
  non-commercial public-benefit/open-science projects free API credits.
  [\[1\]](https://openai.com/form/researcher-access-program/)

- **For students, Microsoft currently has the strongest explicit
  cloud-credit offer:** Azure for Students provides eligible full-time
  university students **\$100 for 12 months**, no credit card required,
  and explicitly advertises access to technologies including Azure
  OpenAI. Students can renew annually while they remain eligible.
  [\[2\]](https://azure.microsoft.com/en-us/free/students)

- **Google provides a genuine zero-price Gemini API tier for several
  current models.** As of 30 September 2026, models including Gemini 3.8
  Flash and 3.5 Flash-Lite have free-of-charge input/output quotas;
  exact availability and limits are model-dependent. Google also
  advertises **\$5,000 research Cloud credits** and up to **\$350,000
  over two years** for qualifying AI startups.
  [\[3\]](https://ai.google.dev/gemini-api/docs/pricing)

- **Mistral\'s current Free plan is unusually useful for individual
  experimentation:** it includes **\$10/month of API credits** and
  access to Mistral Studio. Cohere also gives registered developers a
  free, rate-limited evaluation key, with its documented trial allowance
  capped at **1,000 API calls/month**.
  [\[4\]](https://mistral.ai/pricing/)

- **Several inference platforms offer meaningful legitimate free API
  access to open models.** GitHub Models gives every GitHub account
  rate-limited free access to its supported model catalog; Groq has a
  standing Free Plan, for example currently allowing gpt-oss-120b/20b at
  30 requests/minute, 1,000 requests/day and 200,000 tokens/day;
  OpenRouter exposes designated `:free` models at 20 requests/minute and
  normally 50 free-model requests/day for accounts that have purchased
  less than \$10 of credits.
  [\[5\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)

- **"Free trial" and "free tier" must not be conflated.** Cerebras
  currently gives a **\$5 trial balance expiring after 30 days**, after
  which API access requires purchased credits; Hugging Face gives free
  users only **\$0.10/month** of Inference Providers credits;
  Replicate\'s current official pricing is pay-as-you-go and does **not
  document a standing universal free inference tier**.
  [\[6\]](https://inference-docs.cerebras.ai/support/rate-limits)

- **The best institutional "trick" is a compliant gateway, not a shared
  API key.** A lab can keep provider credentials on a server and issue
  per-user virtual credentials through software such as LiteLLM,
  enforcing individual/team budgets and token/request limits. This is
  materially safer than emailing one API key to 50 students and also
  gives much better accounting.
  [\[7\]](https://docs.litellm.ai/docs/proxy/users)

- **Credential sharing, account pooling, trial cycling and consumer-UI
  wrappers are poor research infrastructure.** OpenAI prohibits
  circumventing rate limits/protective measures and advises individual
  API keys rather than shared keys; Mistral expressly prohibits buying,
  selling or transferring API keys and requires credentials to remain
  confidential; OpenRouter explicitly states that additional
  accounts/API keys do not increase its global rate limits.
  [\[8\]](https://platform.openai.com/terms)

- **Local open-weight inference is often the only genuinely durable
  "free API."** OpenAI\'s Apache-2.0 gpt-oss-20b can run in roughly **16
  GB of memory**, while gpt-oss-120b fits in about **80 GB** because the
  released weights are natively MXFP4-quantized; vLLM can expose local
  models through an OpenAI-compatible HTTP API. The monetary API bill
  becomes zero, although hardware, electricity and administration
  obviously remain costs.
  [\[9\]](https://openai.com/index/introducing-gpt-oss/)

- **For publishable research, free access has a hidden reproducibility
  cost.** Quotas, endpoints and even available models can change:
  Cerebras, for example, removed Gemma 4 31B from its public endpoints
  on **3 September 2026** while retaining it on dedicated endpoints;
  Google, Colab and free inference providers similarly make free
  resources conditional on quotas/capacity. Experiments should therefore
  record exact model IDs, dates, endpoint/provider, parameters and---in
  open-model experiments---weight revisions.
  [\[10\]](https://inference-docs.cerebras.ai/support/change-log)

## Official programs and free tiers

The useful distinction is between four funding mechanisms: **research
grants**, **student/education credits**, **startup credits**, and
**standing developer free tiers**. They behave very differently in
experiments: grants can support serious benchmarking, while most free
tiers are suitable only for coursework, prototypes or small evaluation
sets. [\[11\]](https://openai.com/form/researcher-access-program/)

**Research, education and startup programs**

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Provider /     Cost = free?           Eligibility and application Limits / duration    Legal    Technical     Primary sources
  program                                                                                risk     complexity    
  -------------- ---------------------- --------------------------- -------------------- -------- ------------- -------------------------------------------------------------------------------------------------------------------
  **OpenAI       Yes, if awarded        Active affiliation with an  Up to **\$1,000 API  Low      Low           [\[12\]](https://openai.com/form/researcher-access-program/)
  Researcher                            academic institution/other  credits**; **12                             
  Access                                research organization;      months**; usable on                         
  Program**                             nonprofits conducting       publicly available                          
                                        research are also eligible. API models.                                 
                                        Submit research question    Applications                                
                                        and intended API use        reviewed quarterly                          
                                        through the application     in March, June,                             
                                        portal.                     September, December;                        
                                                                    grant delivery                              
                                                                    normally 4--6 weeks                         
                                                                    after the review.                           

  **Anthropic AI Yes, if awarded        The September 2026 general  Up to **\$50,000 in  Low      Low           [\[13\]](https://www.anthropic.com/news/expanding-support-for-scientists)
  for Science**                         program says **any          credits/project**.                          
                                        researcher may apply** for  General program page                        
                                        project credits.            does not give one                           
                                        Separately, a PI/equivalent universal credit                            
                                        at an academic or nonprofit lifetime; a specific                        
                                        research institution can    2026 rare-disease                           
                                        verify a laboratory for the call gave up to                             
                                        scientists\' team plan.     \$50k over six                              
                                                                    months.                                     

  **Anthropic    Yes for standard seat  PI/equivalent at            **10,000 initial     Low      Low           [\[14\]](https://www.anthropic.com/news/expanding-support-for-scientists)
  Claude team                           academic/nonprofit research seats**; standard                           
  plan for                              institution verifies and    seats free for **one                        
  scientists**                          adds lab members.           year**; premium                             
                                                                    seats \$15/month                            
                                                                    with 5× usage. This                         
                                                                    is primarily a                              
                                                                    Claude subscription                         
                                                                    program, not                                
                                                                    equivalent to                               
                                                                    unrestricted API                            
                                                                    credits.                                    

  **Cohere Labs  Yes, if awarded        Academic partners,          Award size varies;   Low      Low           [\[15\]](https://cohere.com/research/grants)
  Catalyst                              civic/public-impact         credits subject to                          
  Grants**                              organizations; project      API rate limits.                            
                                        should advance public       Cohere reports 250                          
                                        benefit or open-science     grants and \$350k                           
                                        research and be             aggregate API                               
                                        non-commercial. Rolling     credits awarded to                          
                                        application asks for        date.                                       
                                        affiliation, model choices,                                             
                                        estimated calls, timeline                                               
                                        and intended research                                                   
                                        artifact.                                                               

  **Google Cloud Yes, if awarded        Google Cloud\'s current     Advertised grant:    Low      Medium        [\[16\]](https://cloud.google.com/edu/researchers)
  research                              researcher program has an   **\$5,000 Google                            
  credits**                             application route for       Cloud research                              
                                        academic research.          credits**. The                              
                                                                    public landing page                         
                                                                    does not state one                          
                                                                    universal award                             
                                                                    duration or                                 
                                                                    guarantee                                   
                                                                    eligibility of every                        
                                                                    service, so verify                          
                                                                    the award terms for                         
                                                                    the particular                              
                                                                    project.                                    

  **AWS Cloud    Yes, if awarded        Full-time faculty/research  Students: max        Low      Medium        [\[17\]](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/)
  Credit for                            staff or                    **\$5,000**;                                
  Research**                            graduate/postgraduate/PhD   faculty/staff: no                           
                                        students at accredited      fixed program cap.                          
                                        research institutions;      Promotional credits                         
                                        institutional email and AWS last **one year or                          
                                        account required. Global    until exhausted**.                          
                                        except Greater China.       Intended for finite                         
                                        Rolling review, normally    research/cloud                              
                                        90--120 days.               proof-of-concept,                           
                                                                    reusable tools or                           
                                                                    workshops rather                            
                                                                    than ongoing lab                            
                                                                    operations.                                 

  **Azure for    Yes                    Full-time university        **\$100 Azure credit Low      Low--medium   [\[2\]](https://azure.microsoft.com/en-us/free/students)
  Students**                            students; academic          for 12 months**,                            
                                        verification; no credit     plus selected free                          
                                        card.                       services; can renew                         
                                                                    annually while                              
                                                                    eligible. Microsoft                         
                                                                    explicitly                                  
                                                                    references Azure                            
                                                                    OpenAI among                                
                                                                    available                                   
                                                                    technologies.                               

  **Google Cloud Yes, if accepted       VC-funded AI startup;       Up to **\$350,000    Low      Medium        [\[18\]](https://cloud.google.com/startup/ai)
  AI startup                            founded within five years;  over two years**:                           
  program**                             specified                   AI-first startups                           
                                        pre-seed/seed/Series-A      can receive up to                           
                                        timing; generally not       \$250k year one and                         
                                        already \>\$5k Google Cloud 20% coverage up to                          
                                        credits; AI/Gemini central  another \$100k year                         
                                        to product.                 two. Covers Google                          
                                                                    models such as                              
                                                                    Gemini/Gemma, not                           
                                                                    third-party model                           
                                                                    charges.                                    

  **Microsoft    Yes, if                Privately held, for-profit  Credits scale with   Low      Medium        [\[19\]](https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview)
  for Startups** accepted/progressing   software startup;           progress/usage, **up                        
                                        pre-Series-C;               to \$150,000**. "Up                         
                                        Azure-supported country;    to" is important:                           
                                        other eligibility           the maximum is not                          
                                        conditions apply. Direct    an automatic award                          
                                        application; partner-backed to every applicant.                         
                                        startups may unlock                                                     
                                        additional benefits.                                                    

  **Azure for    Yes                    New Azure customers;        **\$1,000            Low      Low--medium   [\[2\]](https://azure.microsoft.com/en-us/free/students)
  Startups entry                        initial access, then        immediately**, up to                        
  offer**                               business verification for   **\$5,000 total**;                          
                                        larger amount.              initial credits 90                          
                                                                    days,                                       
                                                                    post-verification                           
                                                                    credits 180 days.                           

  **AWS          Yes, if eligible       Startups; higher Portfolio  Provider-backed      Low      Medium        [\[20\]](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/)
  Activate**                            tier requires affiliation   startups can receive                        
                                        with an Activate Provider   up to **\$200,000**                         
                                        and additional conditions.  under the current                           
                                                                    program.                                    
                                                                    Importantly,                                
                                                                    Activate credits can                        
                                                                    now pay for                                 
                                                                    third-party                                 
                                                                    foundation models on                        
                                                                    Amazon Bedrock,                             
                                                                    including models                            
                                                                    from Anthropic,                             
                                                                    Mistral, Meta and                           
                                                                    others.                                     
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

A particularly useful 2026 development is **cloud-credit fungibility**.
AWS announced in May 2026 that Activate credits can be spent on
third-party Bedrock models. That means a startup does not necessarily
need a direct Anthropic or Mistral grant to experiment with those
models: eligible AWS promotional credits can fund them indirectly.
[\[21\]](https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/)

**Standing free access and trials**

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Provider / service Cost = free?      Eligibility             Current limits / caveats        Legal    Technical    Primary sources
                                                                                               risk     complexity   
  ------------------ ----------------- ----------------------- ------------------------------- -------- ------------ --------------------------------------------------------------------------------------------------------------------------
  **Google Gemini    **Yes**           Developer account;      Several current models expose   Low      Low          [\[22\]](https://ai.google.dev/gemini-api/docs/pricing)
  Developer API Free                   availability depends on zero-price input/output on free                       
  Tier**                               model/region.           tier. For example Gemini 3.8                          
                                                               Flash and 3.5 Flash-Lite are                          
                                                               listed "free of charge." Quotas                       
                                                               are model-specific.                                   

  **Mistral Free**   **Yes**           Standard free account   Current plan includes           Low      Low          [\[23\]](https://mistral.ai/pricing/)
                                                               **\$10/month API credits**,                           
                                                               plus limited Studio/Vibe                              
                                                               access.                                               

  **Cohere           **Yes**           Registered developer    Free evaluation access;         Low      Low          [\[24\]](https://docs.cohere.com/docs/rate-limits)
  evaluation/trial                                             documented trial allowance                            
  key**                                                        **1,000 API calls/month**, with                       
                                                               endpoint/model rate limits.                           
                                                               Intended for                                          
                                                               evaluation/proofs-of-concept,                         
                                                               not production.                                       

  **GitHub Models**  **Yes**           Any GitHub account      All accounts get rate-limited   Low      Low          [\[25\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
                                                               free access to supported                              
                                                               models; limits vary by                                
                                                               model/Copilot plan and are                            
                                                               aimed at                                              
                                                               prototyping/experimentation.                          

  **GroqCloud Free   **Yes**           Free Groq account       Example as of today:            Low      Low          [\[26\]](https://console.groq.com/docs/rate-limits)
  Plan**                                                       gpt-oss-120b/20b: **30 RPM,                           
                                                               1,000 requests/day, 8k TPM,                           
                                                               200k tokens/day**. Limits are                         
                                                               organization-level.                                   

  **OpenRouter**     **Yes**           OpenRouter account      Designated free variants: **20  Low      Low          [\[27\]](https://openrouter.ai/docs/api_reference/limits)
  `:free` **models**                                           RPM** and normally **50                               
                                                               requests/day** for accounts                           
                                                               with \< \$10 lifetime credit                          
                                                               purchases. Higher 1,000/day                           
                                                               ceiling requires prior credit                         
                                                               purchase, so that tier is not                         
                                                               strictly "zero expenditure."                          

  **Cerebras Free    **Temporarily**   New/eligible account    **\$5 credits, expiring after   Low      Low          [\[28\]](https://inference-docs.cerebras.ai/support/rate-limits)
  Trial**                                                      30 days**. gpt-oss-120b                               
                                                               currently 5 RPM, 30k uncached                         
                                                               TPM and 1M tokens/day. There is                       
                                                               explicitly **no automatically                         
                                                               renewing no-cost tier**.                              

  **Hugging Face     Technically yes,  Any free HF user        **\$0.10/month** of credits,    Low      Low          [\[29\]](https://huggingface.co/docs/inference-providers/main/pricing.md)
  Inference          but tiny                                  explicitly subject to change.                         
  Providers**                                                  Useful for smoke tests, not                           
                                                               substantive LLM experiments.                          

  **Hugging Face     **Yes**,          Any user to consume;    Free account receives **5       Low      Medium       [\[30\]](https://huggingface.co/docs/hub/main/spaces-zerogpu.md)
  ZeroGPU Spaces**   quota-limited     free account in good    GPU-minutes/day** and can host                        
                                       standing, verified      up to **two ZeroGPU Spaces**;                         
                                       email and \>30 days old unauthenticated usage is 2                            
                                       to host                 min/day.                                              

  **Replicate**      **No standing     ---                     Current official pricing says   Low      Low          [\[31\]](https://replicate.com/docs/pricing)
                     free tier                                 pay only for usage, with public                       
                     verified**                                models charged by time or                             
                                                               tokens/output. I found no                             
                                                               current official universal free                       
                                                               inference quota. Promotional                          
                                                               credits may exist case-by-case,                       
                                                               but should not be treated as a                        
                                                               durable program.                                      

  **Aleph Alpha /    **No public free  Enterprise/deployment   Current documentation exposes   Low      Medium       [\[32\]](https://docs.aleph-alpha.com/phariaai-dev-guide/latest/index.html)
  PhariaAI**         program           access appears to be    authenticated PhariaInference                         
                     verified**        the current focus       APIs and token management, but                        
                                                               I could not verify a current                          
                                                               public student/research                               
                                                               free-credit scheme from Aleph                         
                                                               Alpha\'s official 2026                                
                                                               material. **Uncertain negative                        
                                                               finding:** a private                                  
                                                               partnership program may exist.                        
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Two corrections to common online advice are therefore important.
**Replicate should not currently be presented as having a general free
tier**, and **Hugging Face\'s ordinary Inference Providers allowance is
only ten cents per month for free users**; HF\'s materially more useful
free compute mechanism is ZeroGPU rather than the hosted inference
credit. [\[33\]](https://replicate.com/docs/pricing)

## Community and institutional workarounds

There is a sharp distinction between a **workaround that improves
allocation of legitimate credits** and a workaround that **evades the
provider\'s charging or access controls**.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Technique                          Cost = free?        Eligibility              Practical               Limits                Legal / ToS risk     Technical           Primary sources
                                                                                  implementation                                                     complexity          
  ---------------------------------- ------------------- ------------------------ ----------------------- --------------------- -------------------- ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Institutional LLM gateway**      End users can be    Lab/course/institution   Store upstream keys     Overall upstream      **Low**, when        Medium              [\[7\]](https://docs.litellm.ai/docs/proxy/users)
                                     free;               with legitimate provider only on the gateway;    quota/budget still    provider contract                        
                                     institution/grant   account                  authenticate every      applies.              permits the                              
                                     pays                                         researcher/student                            institutional                            
                                                                                  separately; issue                             application/end                          
                                                                                  virtual keys; enforce                         users                                    
                                                                                  per-user/team budgets,                                                                 
                                                                                  TPM and RPM. LiteLLM                                                                   
                                                                                  directly supports these                                                                
                                                                                  controls.                                                                              

  **Cloud-credit → managed-model     Yes until credits   Grant/student/startup    Obtain AWS/Azure/GCP    Grant duration and    **Low**              Medium              [\[34\]](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/)
  API**                              expire              eligibility              credits, create the     eligible services.                                             
                                                                                  managed-model resource                                                                 
                                                                                  under the credited                                                                     
                                                                                  cloud account, and                                                                     
                                                                                  expose it through                                                                      
                                                                                  normal cloud IAM or a                                                                  
                                                                                  lab gateway.                                                                           

  **Organization billing with        Depends on sponsor  Team/institution         Give each user their    Subscription/credit   **Low**              Low--medium         [\[29\]](https://huggingface.co/docs/inference-providers/main/pricing.md)
  individual identities**                                                         own identity/token      pool.                                                          
                                                                                  while centralizing                                                                     
                                                                                  billing. HF, for                                                                       
                                                                                  example, supports                                                                      
                                                                                  organization billing                                                                   
                                                                                  while every user                                                                       
                                                                                  retains an individual                                                                  
                                                                                  access token.                                                                          

  **Sponsored academic partnership** Often               Requires successful      Apply to OpenAI,        Selective;            **Low**              Low                 [\[35\]](https://openai.com/form/researcher-access-program/)
                                                         proposal/relationship    Anthropic, Cohere, AWS, proposal-specific.                         administratively,   
                                                                                  Google or a                                                        medium              
                                                                                  university/cloud                                                   organizationally    
                                                                                  program; place awarded                                                                 
                                                                                  credits in an                                                                          
                                                                                  institutional project.                                                                 

  **Free API aggregators /           Yes within quotas   Usually account          Use documented          Low daily/token       **Low** if used      Low                 [\[5\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
  legitimate free endpoints**                            registration             endpoints such as       ceilings and no SLA.  normally                                 
                                                                                  GitHub Models, Groq or                                                                 
                                                                                  OpenRouter\'s                                                                          
                                                                                  explicitly free model                                                                  
                                                                                  IDs.                                                                                   

  **One shared lab API key passed    Cost may be         Anyone receiving the     Technically trivial,    Poor attribution; one **Medium--high**;    Low                 [\[36\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
  among users**                      centrally funded,   credential               but replace it with a   leak compromises      provider rules often                     
                                     not actually free                            gateway or provider     whole budget.         restrict credential                      
                                                                                  organization/project                          sharing                                  
                                                                                  accounts.                                                                              

  **Account/password sharing**       Superficially       Shared login             Do not use as the       MFA, audit and        **High** where terms Low                 [\[37\]](https://www.anthropic.com/legal/consumer-terms)
                                                                                  access-control          concurrent-use        expressly prohibit                       
                                                                                  mechanism; provision    problems.             shared credentials                       
                                                                                  supported end-user                                                                     
                                                                                  accounts instead.                                                                      

  **API-key/token marketplace or     Sometimes           Access to somebody       No legitimate           Revocation, fraud,    **High**; Mistral    Low                 [\[38\]](https://legal.mistral.ai/terms/commercial-terms-of-service/)
  exchanging tokens with strangers**                     else\'s credential       engineering reason in a uncontrolled billing. explicitly prohibits                     
                                                                                  research environment;                         buying, selling or                       
                                                                                  use BYOK with one\'s                          transferring API                         
                                                                                  own credentials or an                         keys/accounts.                           
                                                                                  authorized gateway                                                                     
                                                                                  instead.                                                                               

  **Cycling trial accounts /         Superficially       Ability to create        Not a sustainable       Detection/account     **High**             Low                 [\[39\]](https://platform.openai.com/terms)
  multi-account quota evasion**                          identities/accounts      access strategy. Use    suspension; poor                                               
                                                                                  multiple providers or   reproducibility.                                               
                                                                                  free models                                                                            
                                                                                  legitimately instead.                                                                  

  **Reverse-engineered API around    Superficially       Consumer                 A wrapper automates a   UI changes, CAPTCHAs, **High** for         Medium--high        [\[40\]](https://platform.openai.com/terms)
  consumer chat UI**                                     subscription/free UI     web UI/session rather   account controls; no  providers whose                          
                                                                                  than the documented     API guarantees.       terms prohibit                           
                                                                                  developer API. I do not                       automated extraction                     
                                                                                  recommend                                     or                                       
                                                                                  implementation                                protective-measure                       
                                                                                  instructions because                          bypass                                   
                                                                                  the central mechanism                                                                  
                                                                                  can itself violate                                                                     
                                                                                  automation/extraction                                                                  
                                                                                  restrictions.                                                                          

  **VPN/geographic/account-control   Superficially       ---                      Not a legitimate        Account termination   **High** when used   Low                 [\[41\]](https://platform.openai.com/terms)
  circumvention**                                                                 research-access         and compliance        to bypass                                
                                                                                  mechanism.              problems.             eligibility/access                       
                                                                                                                                restrictions                             

  **Community-hosted proxy using     Possibly            Proxy operator permits   Technically just an     Availability,         **Variable / often   Low client-side     [\[42\]](https://docs.litellm.ai/docs/proxy/users)
  somebody else\'s upstream                              access                   intermediary HTTP       privacy, provenance   unclear**                                
  credits**                                                                       gateway. Only use where and quota unknown.                                             
                                                                                  the operator explicitly                                                                
                                                                                  offers the service and                                                                 
                                                                                  upstream terms permit                                                                  
                                                                                  it.                                                                                    
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The practical institutional pattern is:

  ------------------------------------------------------------
                   ![Rendered Mermaid diagram
        1](media/rId40.png){width="5.833333333333333in"
                 height="2.556583552055993in"}

  ------------------------------------------------------------

LiteLLM\'s current gateway supports per-user, per-team and per-key
budgets as well as TPM/RPM limits; vLLM can make a locally hosted model
look like an OpenAI-compatible endpoint. Those two properties make this
architecture convenient for courses and labs because application code
can remain largely provider-neutral.
[\[43\]](https://docs.litellm.ai/docs/proxy/users)

A minimal compliant implementation is therefore:

1.  Create the upstream API/cloud accounts under the institution rather
    than an individual student.
2.  Put upstream secrets only on the gateway host or secret manager.
3.  Run a gateway such as LiteLLM and expose only its virtual keys to
    users.
4.  Give every user or project a separate virtual key and assign a hard
    monetary, TPM and RPM budget.
5.  Maintain an allow-list of models for the course/project.
6.  Record upstream provider and model ID with each experimental run,
    while avoiding prompt logging when the research data requires
    stronger confidentiality. LiteLLM provides the budget/rate-control
    primitives required for this design.
    [\[7\]](https://docs.litellm.ai/docs/proxy/users)

This is better than a shared credential even where sharing inside an
organization is technically possible: attribution, revocation and budget
isolation become local administrative operations rather than reasons to
rotate the entire lab\'s upstream secret.

## Technical alternatives

The most robust way to obtain a zero-dollar **API bill** is to stop
depending on a proprietary API. It does not make computation
economically free, but it changes the scarce resource from metered
tokens to hardware time.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Provider /          Cost = free?        Eligibility          Limits / trade-off           Legal risk       Technical      Primary sources
  technique                                                                                                  complexity     
  ------------------- ------------------- -------------------- ---------------------------- ---------------- -------------- --------------------------------------------------------------------------------------------------------------------------
  **gpt-oss-20b       API: yes; compute:  Anyone under model   Apache 2.0; natively MXFP4;  Low              Medium         [\[44\]](https://openai.com/index/introducing-gpt-oss/)
  locally**           no                  license              about **16 GB memory**; 128k                                 
                                                               context. Good                                                
                                                               laptop/workstation-class                                     
                                                               research target where                                        
                                                               supported hardware is                                        
                                                               available.                                                   

  **gpt-oss-120b      API: yes; compute:  Anyone under model   Apache 2.0; about **80 GB    Low              Medium--high   [\[44\]](https://openai.com/index/introducing-gpt-oss/)
  locally**           no                  license              memory**; 128k context;                                      
                                                               practical on one 80-GB                                       
                                                               accelerator according to                                     
                                                               OpenAI.                                                      

  **Mistral           API: yes when       License-dependent    Mistral has continued        Low under        Medium--high   [\[45\]](https://mistral.ai/news/mistral-small-4/)
  open-weight         self-hosted                              releasing Apache-2.0 open    applicable open                 
  models**                                                     models; recent Small 4 is a  license                         
                                                               119B-total/6B-active MoE                                     
                                                               with 256k context, but                                       
                                                               full-weight storage still                                    
                                                               makes deployment                                             
                                                               substantially heavier than                                   
                                                               its active-parameter count                                   
                                                               suggests.                                                    

  **Gemma 4 family**  API: yes when       License/model-card   Current family provides      Low if license   Medium         [\[46\]](https://ai.google.dev/gemma/docs/core/model_card_4)
                      self-hosted         conditions           multiple sizes for           conditions                      
                                                               local/server deployment and  followed                        
                                                               is designed for                                              
                                                               multilingual/multimodal use.                                 
                                                               Hardware requirement varies                                  
                                                               greatly by                                                   
                                                               size/quantization.                                           

  **DeepSeek-R1       API: yes when       Base-model and       1.5B--70B distilled          Low--medium;     Medium         [\[47\]](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)
  distills**          self-hosted         derivative-license   checkpoints provide much     check the                       
                                          conditions apply     smaller reasoning models.    specific base                   
                                                               DeepSeek\'s model card       license                         
                                                               permits                                                      
                                                               modifications/distillation                                   
                                                               but also documents the                                       
                                                               Qwen/Llama base models from                                  
                                                               which specific distills                                      
                                                               derive.                                                      

  **vLLM              Software yes        Local/cloud hardware Exposes `/v1`-style          Low              Medium         [\[48\]](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)
  OpenAI-compatible                                            completion/chat APIs;                                        
  server**                                                     supports several quantized                                   
                                                               load formats and parallel                                    
                                                               deployment.                                                  

  **GPTQ              Software/research   Compatible           3--4-bit post-training       Depends on model Medium--high   [\[49\]](https://arxiv.org/html/2210.17323v2)
  quantization**      method yes          weights/runtime      weight quantization can      license                         
                                                               dramatically cut memory; the                                 
                                                               GPTQ paper reports                                           
                                                               negligible degradation on                                    
                                                               its tested models and                                        
                                                               substantial inference                                        
                                                               speedups, but those results                                  
                                                               must not be generalized                                      
                                                               blindly to every                                             
                                                               architecture/task.                                           

  **AWQ               Software/research   Compatible           Activation-aware low-bit     Depends on model Medium--high   [\[50\]](https://arxiv.org/pdf/2306.00978)
  quantization**      method yes          weights/runtime      quantization; the MLSys work license                         
                                                               reports roughly **4×                                         
                                                               model-size reduction** at                                    
                                                               INT4 with small degradation                                  
                                                               in evaluated settings and                                    
                                                               implements optimized 4-bit                                   
                                                               inference.                                                   

  **Knowledge         Method yes; teacher Teacher/output terms Can transfer capabilities    Potentially high High           [\[51\]](https://arxiv.org/html/1503.02531v1)
  distillation**      inference may cost  must permit intended from a larger teacher to a   with prohibited                 
                      money               use                  smaller deployable student.  teacher-output                  
                                                               It is an optimization        use                             
                                                               technique, **not a license                                   
                                                               bypass**.                                                    

  **Google Colab free Yes                 Google account /     Free notebooks can expose    Low for normal   Low--medium    [\[52\]](https://research.google.com/colaboratory/faq.html)
  runtime**                               service availability GPUs/TPUs, but resources,    notebook use                    
                                                               accelerator type and limits                                  
                                                               are not guaranteed and may                                   
                                                               fluctuate. Free-tier                                         
                                                               anti-abuse rules restrict                                    
                                                               techniques such as using the                                 
                                                               notebook as a generic remote                                 
                                                               desktop/SSH service.                                         

  **Hugging Face      Yes within daily    HF users; stricter   Free users: 5 GPU-min/day;   Low              Medium         [\[30\]](https://huggingface.co/docs/hub/main/spaces-zerogpu.md)
  ZeroGPU**           quota               condition to host    eligible free accounts can                                   
                                                               host two ZeroGPU Spaces.                                     
                                                               Excellent for demos or                                       
                                                               interactive teaching, poor                                   
                                                               for sustained benchmark                                      
                                                               campaigns.                                                   

  **GitHub Models**   Yes within quota    GitHub account       Convenient API playground    Low              Low            [\[25\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
                                                               for comparing multiple                                       
                                                               hosted models; not intended                                  
                                                               as unlimited production                                      
                                                               inference.                                                   

  **Groq free         Yes within quota    Groq account         Fast hosted access to a      Low              Low            [\[26\]](https://console.groq.com/docs/rate-limits)
  inference**                                                  limited catalog; gpt-oss                                     
                                                               free-plan limits currently                                   
                                                               allow meaningful                                             
                                                               experimentation but not                                      
                                                               large-scale evaluation.                                      

  **Cerebras Free     Only temporarily    New/eligible account Very fast hosted inference   Low              Low            [\[28\]](https://inference-docs.cerebras.ai/support/rate-limits)
  Trial**                                                      but \$5/30-day trial rather                                  
                                                               than permanent zero-cost                                     
                                                               compute.                                                     

  **Replicate**       No generic free     Normal account       Excellent managed serving    Low              Low            [\[31\]](https://replicate.com/docs/pricing)
                      allocation verified                      convenience, but current                                     
                                                               public documentation is                                      
                                                               pay-as-you-go.                                               
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Quantization is usually the highest-leverage local-inference trick

For weight storage alone, changing a 16-bit representation to 4 bits
gives an **idealized 4× reduction**. Real runtime memory also contains
KV cache, activations, runtime buffers and sometimes higher-precision
tensors, so total VRAM does not fall by exactly 4×. GPTQ and AWQ provide
empirical evidence that well-designed 3--4-bit post-training
quantization can retain much of the original model\'s quality, although
the size/accuracy/speed result is model-, task-, hardware- and
kernel-dependent. [\[53\]](https://arxiv.org/html/2210.17323v2)

A useful hierarchy for research engineering is therefore:

  -----------------------------------------------------------------------------------------------------------
  Need                 First choice         Why
  -------------------- -------------------- -----------------------------------------------------------------
  A few hundred        Gemini Free, Mistral Almost zero setup; sufficient for prototyping.
  exploratory calls    Free, Groq, GitHub   [\[54\]](https://ai.google.dev/gemini-api/docs/pricing)
                       Models, OpenRouter   
                       free models          

  Thousands/millions   Research grant/cloud Stable billing account and larger allocation are preferable to
  of publishable calls credits              stitching together free tiers.
                                            [\[55\]](https://openai.com/form/researcher-access-program/)

  Sensitive data       Local open model or  Avoids sending data through unknown public proxies; OpenAI\'s API
                       contracted API with  business data is not used for training by default.
                       appropriate data     [\[56\]](https://openai.com/enterprise-privacy/)
                       terms                

  Repeated course      Department gateway + Central quotas, no shared upstream secrets, and less dependence
  every semester       local model + one or on a single provider\'s free-tier policy.
                       more free hosted     [\[57\]](https://docs.litellm.ai/docs/proxy/users)
                       fallbacks            

  Reproducible systems Pinned open weights  Removes endpoint retirement and silent hosted-model replacement
  research             locally              from the main experimental variable. Recent Cerebras endpoint
                                            removals illustrate the issue.
                                            [\[58\]](https://inference-docs.cerebras.ai/support/change-log)
  -----------------------------------------------------------------------------------------------------------

### Distillation has a licensing trap

Distillation itself is a standard compression/knowledge-transfer
technique. Hinton, Vinyals and Dean formalized the now-standard
teacher/student approach, and DeepSeek explicitly used R1-generated
samples to construct smaller R1 distills.
[\[59\]](https://arxiv.org/html/1503.02531v1)

But the technical ability to collect outputs does **not** imply
permission to use them as model-training data. OpenAI\'s current Terms
of Use prohibit using output to develop models that compete with OpenAI;
therefore, a workflow of "use a free proprietary API to generate
millions of examples, then train my own substitute model" can be
precisely the kind of activity the terms restrict.
[\[60\]](https://platform.openai.com/terms)

Conversely, DeepSeek\'s R1 model card expressly says its released
code/weights support modification and derivative works including
distillation, while warning that particular R1 distills inherit ancestry
from Qwen or Llama models whose applicable terms must also be
considered.
[\[47\]](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)

Thus **distillation is a cost-reduction strategy only after the
teacher\'s terms and the student\'s base-model license have been
checked**.

## Ethical, legal and security risks

The highest-risk "free access" techniques are generally not
sophisticated technical exploits. They are ordinary engineering
shortcuts---shared credentials, unidentified proxies, uncontrolled
logging and experimental dependence on ephemeral quotas.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Risk               What can go wrong       Severity for research        Evidence / policy
  ------------------ ----------------------- ---------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Rate-limit /     Account suspension,     High                         OpenAI explicitly prohibits circumventing rate limits/restrictions/protective measures; OpenRouter explicitly says extra accounts/API keys do not increase its global limits. [\[39\]](https://platform.openai.com/terms)
  trial              termination, inability                               
  circumvention**    to reproduce the work                                
                     under the same access                                
                     conditions.                                          

  **Shared or traded Accidental expenditure, High                         OpenAI recommends unique team-member keys; Mistral prohibits key/account transfers and requires credentials to remain confidential.
  credentials**      loss of attribution,                                 [\[61\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
                     compromise of all                                    
                     users, policy breach.                                

  **Automating       Breakage when UI        High                         OpenAI prohibits programmatic extraction and protection bypass; Anthropic\'s consumer terms restrict automated access except through authorized mechanisms. [\[40\]](https://platform.openai.com/terms)
  consumer web       changes; possible                                    
  interfaces**       automation/extraction                                
                     or protective-control                                
                     violation.                                           

  **Sending research Prompts may be          High for                     Google specifically distinguishes unpaid and paid Gemini services, with an important EEA/CH/UK exception described below. [\[62\]](https://ai.google.dev/gemini-api/terms)
  data to free       retained/used under     confidential/human-subject   
  services**         different conditions    data                         
                     from paid enterprise                                 
                     APIs.                                                

  **Unknown          Proxy operator can      High                         This follows architecturally whenever a proxy terminates/authenticates the HTTP request; legitimate gateways such as LiteLLM should therefore be operated by a trusted party. [\[42\]](https://docs.litellm.ai/docs/proxy/users)
  third-party        potentially observe                                  
  proxy**            prompts, outputs and                                 
                     credentials and may                                  
                     itself be violating                                  
                     upstream terms.                                      

  **Model/provider   Results change or       High for publications        Cerebras removed Gemma 4 31B from public endpoints on 3 September 2026; Colab explicitly states resources/limits fluctuate. [\[63\]](https://inference-docs.cerebras.ai/support/change-log)
  drift**            endpoint disappears                                  
                     between experiment and                               
                     replication.                                         

  **"Free" quotas    Accidental charges once Medium--high                 HF distinguishes included credits from pay-as-you-go; Azure distinguishes promotional credits from post-credit paid operation. [\[64\]](https://huggingface.co/docs/inference-providers/main/pricing.md)
  silently turning   free allocation is                                   
  into spend**       exhausted.                                           

  **Free-tier        Research compares       Medium                       This is a methodological inference from the highly heterogeneous free quotas documented by providers. [\[65\]](https://ai.google.dev/gemini-api/docs/pricing)
  availability       models because they                                  
  bias**             were inexpensive rather                              
                     than because they are                                
                     scientifically                                       
                     appropriate.                                         

  **Unlicensed       A student model may     High                         OpenAI currently prohibits using output to develop competing models. [\[60\]](https://platform.openai.com/terms)
  teacher-output     violate provider                                     
  distillation**     contractual                                          
                     restrictions even if                                 
                     training code and                                    
                     resulting weights are                                
                     technically original.                                
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### The Gemini privacy rule has an important European exception

Google\'s March 23, 2026 Gemini API terms say that for ordinary **Unpaid
Services**, Google may use submitted content and generated responses to
provide, improve and develop its products, and may have human reviewers
process data; Google consequently says not to submit sensitive,
confidential or personal information to those unpaid services.
[\[62\]](https://ai.google.dev/gemini-api/terms)

However, the same current terms make an important geographical
carve-out: **for users in the European Economic Area, Switzerland and
the United Kingdom, the "Paid Services" data-handling provisions apply
to all Gemini services, including AI Studio and free API quota**. Under
the Paid Services provision, Google says prompts and responses are not
used to improve its products. This makes older blanket statements that
"Google trains on all free Gemini API traffic" inaccurate for European
users as of September 2026.
[\[62\]](https://ai.google.dev/gemini-api/terms)

OpenAI likewise states that data sent through its API Platform is **not
used to train its models by default**, unless the customer explicitly
opts in to data sharing. Qualifying API customers can also obtain
stronger retention controls, including zero-data-retention
configurations. [\[56\]](https://openai.com/enterprise-privacy/)

The correct research practice is therefore to record **not only the
model and provider but also the service tier, account geography and
data-processing terms that applied at experiment time**.

### Reproducibility is an underrated cost of "free"

A result reported simply as "we evaluated Gemma 4 using a free API" may
become unreproducible within weeks. On 3 September 2026, for example,
Cerebras removed `gemma-4-31b` from its public endpoints while keeping
it available on dedicated endpoints and recommending a different public
model. [\[58\]](https://inference-docs.cerebras.ai/support/change-log)

For an API-based experiment, the artifact should therefore record at
least:

- exact provider and endpoint;
- exact model ID/version, not merely the family name;
- experiment date;
- system/developer prompt;
- decoding parameters and seed where meaningful;
- number of calls and retry policy;
- whether requests were routed through an aggregator;
- service/free-tier type and any provider-side features such as search
  or caching;
- for local inference, exact weight commit/revision, quantization,
  inference engine and engine version.

These fields are a methodological recommendation motivated by the
documented volatility of hosted models and free resources, rather than a
provider requirement.
[\[63\]](https://inference-docs.cerebras.ai/support/change-log)

## Practical checklist

The safest decision process is to treat "free access" as a
resource-allocation problem rather than an account-creation problem.

  ------------------------------------------------------------
                   ![Rendered Mermaid diagram
        2](media/rId60.png){width="5.833333333333333in"
                 height="4.501027996500437in"}

  ------------------------------------------------------------

Before using any route, answer these questions:

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Check                Decision criterion   Preferred action
  -------------------- -------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Is there an        Research             Apply before looking for workarounds. OpenAI, Anthropic, Cohere, AWS, Google and Microsoft all currently provide relevant routes.
  official             affiliation, course  [\[66\]](https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz)
  research/student     enrollment or        
  grant?**             startup eligibility  

  **Is the "free"      Renewable free tier  Treat Cerebras, for example, as a 30-day/\$5 trial; treat Groq/Gemini/Mistral as current recurring/free-plan offerings subject to future policy changes. [\[67\]](https://inference-docs.cerebras.ai/support/rate-limits)
  offer permanent or   versus expiring      
  promotional?**       credit               

  **What is the actual Calls/day,           Calculate benchmark feasibility before implementing against a provider. [\[68\]](https://console.groq.com/docs/rate-limits)
  quota?**             tokens/day, RPM/TPM, 
                       concurrent requests  

  **Can the provider   Sensitive,           Read the tier-specific data terms. In particular, Gemini\'s free-tier rules differ geographically, while OpenAI API data is not used for training by default. [\[69\]](https://ai.google.dev/gemini-api/terms)
  use my               unpublished,         
  inputs/outputs?**    proprietary or       
                       human-subject data   

  **Am I sharing a     More than one person Replace shared keys with individual provider identities or an institutional gateway with virtual keys. [\[70\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
  credential?**        possesses the same   
                       raw upstream secret  

  **Does the approach  Multiple accounts,   Do not make it part of the research methodology; choose another provider or local model. [\[39\]](https://platform.openai.com/terms)
  defeat a quota or    token rotation, UI   
  eligibility rule?**  automation, VPN      
                       restriction bypass   

  **Could I run an     Evaluation does not  gpt-oss-20b is a particularly convenient current baseline because its 4-bit weights require about 16 GB memory and are Apache 2.0. [\[44\]](https://openai.com/index/introducing-gpt-oss/)
  open model           specifically require 
  instead?**           a proprietary        
                       frontier model       

  **Does quantization  Task-sensitive       Re-evaluate after quantization rather than assuming published GPTQ/AWQ results generalize. [\[71\]](https://arxiv.org/pdf/2306.00978)
  preserve the metric  evaluation           
  I care about?**                           

  **Am I distilling    Outputs become       Explicitly verify output/training restrictions first. [\[72\]](https://platform.openai.com/terms)
  from API outputs?**  student-model        
                       training data        

  **Can another        Publication or       Pin open weights where possible; otherwise log provider, exact model/version, date and decoding setup. [\[58\]](https://inference-docs.cerebras.ai/support/change-log)
  researcher reproduce benchmark            
  the endpoint                              
  later?**                                  

  **What happens when  Long-running         Put a hard budget at gateway/provider level and maintain a local/open fallback. LiteLLM supports user/team/key budgets and rate limits. [\[7\]](https://docs.litellm.ai/docs/proxy/users)
  the free allocation  project/course       
  ends?**                                   
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

A simple hierarchy works well in practice:

**official research grant → student/cloud credit → documented recurring
free API → institutional sponsored gateway → local open-weight inference
→ temporary trials**.

Shared credentials, trial-account cycling and unofficial consumer-web
wrappers should sit outside that hierarchy because they do not produce
stable, auditable research infrastructure.
[\[73\]](https://platform.openai.com/terms)

## Case studies

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Scenario            Recommended     Concrete choices              Why
                      safe path                                     
  ------------------- --------------- ----------------------------- --------------------------------------------------------------------------------------------------------------------------
  **University        Apply for       **OpenAI Researcher Access:** Maximizes available compute while retaining per-researcher accounting and avoiding shared credentials. It also separates
  research lab**      research        up to \$1k/12 months.         expensive frontier-model evaluations from bulk experiments that can run locally.
                      credits;        **Anthropic AI for Science:** [\[74\]](https://openai.com/form/researcher-access-program/)
                      aggregate them  up to \$50k/project where     
                      behind a lab    research fits. **Cohere       
                      gateway;        Catalyst:** free credits for  
                      maintain an     open-science/public-benefit   
                      open-model      projects. **AWS Research:**   
                      cluster for     up to \$5k for students,      
                      bulk runs.      uncapped program maximum for  
                                      faculty/staff awards. Deploy  
                                      LiteLLM in front; use local   
                                      gpt-oss through vLLM for      
                                      high-volume baseline          
                                      experiments.                  

  **Independent       Start with      **Gemini API Free Tier**,     OpenAI\'s Researcher Access eligibility currently requires active affiliation with an academic/research organization or
  researcher without  legitimate      **Mistral \$10/month API      eligible nonprofit, making it less suitable for a genuinely unaffiliated individual. Anthropic\'s general AI for Science
  institutional       recurring free  credits**, **GitHub Models**, language is broader. [\[75\]](https://ai.google.dev/gemini-api/docs/pricing)
  affiliation**       APIs and local  **Groq Free**, **OpenRouter** 
                      open weights;   `:free`, plus gpt-oss-20b     
                      apply to        locally. Anthropic\'s current 
                      provider        AI for Science announcement   
                      programs that   says any researcher may apply 
                      do not require  for project credits, although 
                      conventional    selection is not guaranteed.  
                      university                                    
                      affiliation                                   
                      where                                         
                      appropriate.                                  

  **Master\'s-level   Give students   **GitHub Models** for easy    Individual accounts eliminate secret sharing; the common local endpoint gives equal access and reproducibility even if
  university course** individual free multi-model prototyping;      individual free-tier quotas differ or providers change terms mid-semester.
                      accounts where  **Azure for Students** gives  [\[76\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
                      pedagogically   eligible students \$100/12    
                      useful and      months; **Gemini Free** and   
                      provide a       **Mistral Free** provide      
                      department      direct APIs; **Groq Free**    
                      gateway/local   provides gpt-oss. For         
                      endpoint for    assessed coursework, expose   
                      uniform         one department-managed        
                      assignments.    vLLM/gpt-oss endpoint so      
                                      every student has the same    
                                      baseline.                     
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

For a Computer Science course, the last architecture is particularly
robust: students can learn **real commercial API integration** against
GitHub/Gemini/Mistral/Groq while all graded experiments also target a
department-controlled OpenAI-compatible endpoint. Application code can
therefore switch only `base_url`, model ID and credential rather than
being rewritten for every provider. vLLM explicitly implements an
OpenAI-compatible HTTP server, and LiteLLM can provide the corresponding
multi-provider gateway abstraction.
[\[77\]](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)

## Consolidated references

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Source                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Relevance
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------
  **OpenAI --- Researcher Access Program application** [\[78\]](https://openai.com/form/researcher-access-program/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Current program; up to
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             \$1,000, 12-month validity,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             quarterly review.

  **OpenAI --- Researcher Access Program FAQ**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Eligibility, grant timing,
  [\[79\]](https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz)   expiry and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             rate-limit/payment-method
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             details.

  **OpenAI --- Terms of Use** [\[60\]](https://platform.openai.com/terms)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Rate-limit/protection
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             circumvention, automated
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             extraction and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             competitive-model
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             restrictions.

  **OpenAI --- Enterprise Privacy** [\[80\]](https://openai.com/enterprise-privacy/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         API/business data not used for
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             training by default.

  **OpenAI --- Business data privacy, security and compliance** [\[81\]](https://openai.com/business-data/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  API training policy and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             retention controls.

  **OpenAI --- Introducing gpt-oss** [\[44\]](https://openai.com/index/introducing-gpt-oss/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Apache 2.0 gpt-oss-120b/20b,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             MXFP4, memory requirements,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             model architecture.

  **Anthropic --- Expanding our support for scientists, 27 Aug 2026** [\[14\]](https://www.anthropic.com/news/expanding-support-for-scientists)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              10,000 scientist seats,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             one-year access, expanded AI
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             for Science, up to
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             \$50k/project.

  **Anthropic --- AI for Science rare-disease grants** [\[82\]](https://www.anthropic.com/news/rare-disease-research-grants)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Example of \$50k/six-month
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             targeted research grant.

  **Cohere Labs --- Catalyst Grants** [\[83\]](https://cohere.com/research/grants)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           Current rolling
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             public-benefit/open-science
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             grant program.

  **Cohere Labs --- Catalyst Grant application** [\[84\]](https://cohere.com/research/grants/application)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Application fields and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             explicit free API-credit
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             mechanism.

  **Google --- Gemini Developer API pricing** [\[22\]](https://ai.google.dev/gemini-api/docs/pricing)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Current zero-price Gemini API
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             tiers and model-dependent
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             pricing.

  **Google --- Gemini API Additional Terms, effective 23 Mar 2026** [\[62\]](https://ai.google.dev/gemini-api/terms)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Free/paid data rules and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             EEA/Switzerland/UK exception.

  **Google Cloud --- Cloud for Researchers** [\[16\]](https://cloud.google.com/edu/researchers)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Current \$5,000
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             research-credit application.

  **Google Cloud --- AI startup program** [\[18\]](https://cloud.google.com/startup/ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Up to \$350k credits/2 years
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             and eligibility criteria.

  **Microsoft Azure --- Azure for Students** [\[2\]](https://azure.microsoft.com/en-us/free/students)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \$100/12 months,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             full-time-student conditions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             and Azure OpenAI reference.

  **Microsoft --- Microsoft for Startups** [\[19\]](https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Startup eligibility and up to
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             \$150k credits.

  **AWS --- Cloud Credit for Research** [\[17\]](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Eligibility, \$5k student cap,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             one-year credit lifetime and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             global scope.

  **AWS --- Activate credits for third-party Bedrock models** [\[85\]](https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Credits usable for third-party
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             foundation models on Bedrock.

  **AWS --- Activate Credits guide** [\[86\]](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Startup tiers and current
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             maximum credits.

  **Mistral --- Pricing** [\[23\]](https://mistral.ai/pricing/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Current Free plan and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             \$10/month API credits.

  **Mistral --- Commercial Terms of Service** [\[38\]](https://legal.mistral.ai/terms/commercial-terms-of-service/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          API-key transfer, security
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             circumvention and account-use
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             restrictions.

  **Mistral --- Additional Product Terms** [\[87\]](https://legal.mistral.ai/terms/additional-terms/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Credential confidentiality and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             end-user-account rules.

  **Hugging Face --- Inference Providers pricing** [\[29\]](https://huggingface.co/docs/inference-providers/main/pricing.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 \$0.10/month free-user credits
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             and organization billing.

  **Hugging Face --- ZeroGPU documentation** [\[30\]](https://huggingface.co/docs/hub/main/spaces-zerogpu.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Daily free GPU quota and free
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Space-hosting limits.

  **Replicate --- Pricing** [\[31\]](https://replicate.com/docs/pricing)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Current pay-as-you-go model;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             basis for the finding that no
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             standing universal free tier
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             is documented.

  **Aleph Alpha --- PhariaAI Developer Guide / API** [\[32\]](https://docs.aleph-alpha.com/phariaai-dev-guide/latest/index.html)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Current API/deployment
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             documentation; no current
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             public free-credit program was
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             verifiable from these
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             materials.

  **GitHub --- GitHub Models billing** [\[25\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Free rate-limited model access
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             for all GitHub accounts.

  **Groq --- Free Plan rate limits** [\[26\]](https://console.groq.com/docs/rate-limits)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Current per-model free limits,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             including gpt-oss.

  **Cerebras --- Inference rate limits** [\[88\]](https://inference-docs.cerebras.ai/support/rate-limits)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \$5/30-day trial and current
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             free-trial quotas.

  **Cerebras --- Inference change log** [\[58\]](https://inference-docs.cerebras.ai/support/change-log)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Concrete 2026 endpoint/model
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             changes illustrating
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             reproducibility risk.

  **OpenRouter --- API credit and rate limits** [\[27\]](https://openrouter.ai/docs/api_reference/limits)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `:free` limits and explicit
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             statement that additional
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             accounts/keys do not expand
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             quotas.

  **Google --- Colab FAQ** [\[52\]](https://research.google.com/colaboratory/faq.html)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       Free GPU/TPU availability,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             fluctuating limits and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             anti-abuse restrictions.

  **LiteLLM --- budgets and rate limits** [\[42\]](https://docs.litellm.ai/docs/proxy/users)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Per-user/team/key budget and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             quota management for
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             institutional gateways.

  **LiteLLM --- virtual keys** [\[89\]](https://docs.litellm.ai/docs/proxy/virtual_keys)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Virtual credentials and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             budget/rate-control
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             mechanisms.

  **vLLM --- OpenAI-compatible server documentation** [\[48\]](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Local OpenAI-compatible
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             serving and supported
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             quantization/load formats.

  **Frantar et al. --- GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers** [\[49\]](https://arxiv.org/html/2210.17323v2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Primary paper on practical
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             3--4-bit post-training LLM
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             quantization.

  **Lin et al. --- AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration, MLSys 2024** [\[50\]](https://arxiv.org/pdf/2306.00978)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Low-bit weight quantization,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             compression and empirical
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             accuracy results.

  **Hinton, Vinyals & Dean --- Distilling the Knowledge in a Neural Network** [\[90\]](https://arxiv.org/html/1503.02531v1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Foundational
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             knowledge-distillation
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             reference.

  **DeepSeek --- R1 Distill model card** [\[47\]](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           Distillation procedure,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             released checkpoint sizes and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             derivative/base-license notes.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Uncertain or volatile findings.** Free-tier quotas and promotional
programs are especially volatile. The table values above are the values
verifiable from official sources on **30 September 2026**. In
particular, I found no current official universal free tier for
Replicate and no current public free-credit program for Aleph Alpha;
those are **negative search findings rather than proof that private,
partner-specific or newly launched offers do not exist**. Replicate\'s
current official documentation describes metered pay-as-you-go service,
while Aleph Alpha\'s current documentation emphasizes authenticated
PhariaAI deployment/API access.
[\[91\]](https://replicate.com/docs/pricing)

------------------------------------------------------------------------

[\[1\]](https://openai.com/form/researcher-access-program/)
[\[11\]](https://openai.com/form/researcher-access-program/)
[\[12\]](https://openai.com/form/researcher-access-program/)
[\[35\]](https://openai.com/form/researcher-access-program/)
[\[55\]](https://openai.com/form/researcher-access-program/)
[\[74\]](https://openai.com/form/researcher-access-program/)
[\[78\]](https://openai.com/form/researcher-access-program/)
https://openai.com/form/researcher-access-program/

<https://openai.com/form/researcher-access-program/>

[\[2\]](https://azure.microsoft.com/en-us/free/students)
https://azure.microsoft.com/en-us/free/students

<https://azure.microsoft.com/en-us/free/students>

[\[3\]](https://ai.google.dev/gemini-api/docs/pricing)
[\[22\]](https://ai.google.dev/gemini-api/docs/pricing)
[\[54\]](https://ai.google.dev/gemini-api/docs/pricing)
[\[65\]](https://ai.google.dev/gemini-api/docs/pricing)
[\[75\]](https://ai.google.dev/gemini-api/docs/pricing)
https://ai.google.dev/gemini-api/docs/pricing

<https://ai.google.dev/gemini-api/docs/pricing>

[\[4\]](https://mistral.ai/pricing/)
[\[23\]](https://mistral.ai/pricing/) https://mistral.ai/pricing/

<https://mistral.ai/pricing/>

[\[5\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
[\[25\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
[\[76\]](https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models)
https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models

<https://docs.github.com/api/article/body?pathname=%2Fen%2Fbilling%2Fconcepts%2Fproduct-billing%2Fgithub-models>

[\[6\]](https://inference-docs.cerebras.ai/support/rate-limits)
[\[28\]](https://inference-docs.cerebras.ai/support/rate-limits)
[\[67\]](https://inference-docs.cerebras.ai/support/rate-limits)
[\[88\]](https://inference-docs.cerebras.ai/support/rate-limits)
https://inference-docs.cerebras.ai/support/rate-limits

<https://inference-docs.cerebras.ai/support/rate-limits>

[\[7\]](https://docs.litellm.ai/docs/proxy/users)
[\[42\]](https://docs.litellm.ai/docs/proxy/users)
[\[43\]](https://docs.litellm.ai/docs/proxy/users)
[\[57\]](https://docs.litellm.ai/docs/proxy/users)
https://docs.litellm.ai/docs/proxy/users

<https://docs.litellm.ai/docs/proxy/users>

[\[8\]](https://platform.openai.com/terms)
[\[39\]](https://platform.openai.com/terms)
[\[40\]](https://platform.openai.com/terms)
[\[41\]](https://platform.openai.com/terms)
[\[60\]](https://platform.openai.com/terms)
[\[72\]](https://platform.openai.com/terms)
[\[73\]](https://platform.openai.com/terms)
https://platform.openai.com/terms

<https://platform.openai.com/terms>

[\[9\]](https://openai.com/index/introducing-gpt-oss/)
[\[44\]](https://openai.com/index/introducing-gpt-oss/)
https://openai.com/index/introducing-gpt-oss/

<https://openai.com/index/introducing-gpt-oss/>

[\[10\]](https://inference-docs.cerebras.ai/support/change-log)
[\[58\]](https://inference-docs.cerebras.ai/support/change-log)
[\[63\]](https://inference-docs.cerebras.ai/support/change-log)
https://inference-docs.cerebras.ai/support/change-log

<https://inference-docs.cerebras.ai/support/change-log>

[\[13\]](https://www.anthropic.com/news/expanding-support-for-scientists)
[\[14\]](https://www.anthropic.com/news/expanding-support-for-scientists)
https://www.anthropic.com/news/expanding-support-for-scientists

<https://www.anthropic.com/news/expanding-support-for-scientists>

[\[15\]](https://cohere.com/research/grants)
[\[83\]](https://cohere.com/research/grants)
https://cohere.com/research/grants

<https://cohere.com/research/grants>

[\[16\]](https://cloud.google.com/edu/researchers)
https://cloud.google.com/edu/researchers

<https://cloud.google.com/edu/researchers>

[\[17\]](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/)
[\[34\]](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/)
https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/

<https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/>

[\[18\]](https://cloud.google.com/startup/ai)
https://cloud.google.com/startup/ai

<https://cloud.google.com/startup/ai>

[\[19\]](https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview)
https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview

<https://learn.microsoft.com/en-us/startups/microsoft-for-startups/overview>

[\[20\]](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/)
[\[86\]](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/)
https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/

<https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/>

[\[21\]](https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/)
[\[85\]](https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/)
https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/

<https://aws.amazon.com/aws-startups/learn/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/>

[\[24\]](https://docs.cohere.com/docs/rate-limits)
https://docs.cohere.com/docs/rate-limits

<https://docs.cohere.com/docs/rate-limits>

[\[26\]](https://console.groq.com/docs/rate-limits)
[\[68\]](https://console.groq.com/docs/rate-limits)
https://console.groq.com/docs/rate-limits

<https://console.groq.com/docs/rate-limits>

[\[27\]](https://openrouter.ai/docs/api_reference/limits)
https://openrouter.ai/docs/api_reference/limits

<https://openrouter.ai/docs/api_reference/limits>

[\[29\]](https://huggingface.co/docs/inference-providers/main/pricing.md)
[\[64\]](https://huggingface.co/docs/inference-providers/main/pricing.md)
https://huggingface.co/docs/inference-providers/main/pricing.md

<https://huggingface.co/docs/inference-providers/main/pricing.md>

[\[30\]](https://huggingface.co/docs/hub/main/spaces-zerogpu.md)
https://huggingface.co/docs/hub/main/spaces-zerogpu.md

<https://huggingface.co/docs/hub/main/spaces-zerogpu.md>

[\[31\]](https://replicate.com/docs/pricing)
[\[33\]](https://replicate.com/docs/pricing)
[\[91\]](https://replicate.com/docs/pricing)
https://replicate.com/docs/pricing

<https://replicate.com/docs/pricing>

[\[32\]](https://docs.aleph-alpha.com/phariaai-dev-guide/latest/index.html)
https://docs.aleph-alpha.com/phariaai-dev-guide/latest/index.html

<https://docs.aleph-alpha.com/phariaai-dev-guide/latest/index.html>

[\[36\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
[\[61\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
[\[70\]](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class)
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class

<https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.class>

[\[37\]](https://www.anthropic.com/legal/consumer-terms)
https://www.anthropic.com/legal/consumer-terms

<https://www.anthropic.com/legal/consumer-terms>

[\[38\]](https://legal.mistral.ai/terms/commercial-terms-of-service/)
https://legal.mistral.ai/terms/commercial-terms-of-service/

<https://legal.mistral.ai/terms/commercial-terms-of-service/>

[\[45\]](https://mistral.ai/news/mistral-small-4/)
https://mistral.ai/news/mistral-small-4/

<https://mistral.ai/news/mistral-small-4/>

[\[46\]](https://ai.google.dev/gemma/docs/core/model_card_4)
https://ai.google.dev/gemma/docs/core/model_card_4

<https://ai.google.dev/gemma/docs/core/model_card_4>

[\[47\]](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)
https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B

<https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B>

[\[48\]](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)
[\[77\]](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)
https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html

<https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html>

[\[49\]](https://arxiv.org/html/2210.17323v2)
[\[53\]](https://arxiv.org/html/2210.17323v2)
https://arxiv.org/html/2210.17323v2

<https://arxiv.org/html/2210.17323v2>

[\[50\]](https://arxiv.org/pdf/2306.00978)
[\[71\]](https://arxiv.org/pdf/2306.00978)
https://arxiv.org/pdf/2306.00978

<https://arxiv.org/pdf/2306.00978>

[\[51\]](https://arxiv.org/html/1503.02531v1)
[\[59\]](https://arxiv.org/html/1503.02531v1)
[\[90\]](https://arxiv.org/html/1503.02531v1)
https://arxiv.org/html/1503.02531v1

<https://arxiv.org/html/1503.02531v1>

[\[52\]](https://research.google.com/colaboratory/faq.html)
https://research.google.com/colaboratory/faq.html

<https://research.google.com/colaboratory/faq.html>

[\[56\]](https://openai.com/enterprise-privacy/)
[\[80\]](https://openai.com/enterprise-privacy/)
https://openai.com/enterprise-privacy/

<https://openai.com/enterprise-privacy/>

[\[62\]](https://ai.google.dev/gemini-api/terms)
[\[69\]](https://ai.google.dev/gemini-api/terms)
https://ai.google.dev/gemini-api/terms

<https://ai.google.dev/gemini-api/terms>

[\[66\]](https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz)
[\[79\]](https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz)
https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz

<https://help.openai.com/en/articles/10139500-researcher-access-program-faq%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523.svgz>

[\[81\]](https://openai.com/business-data/)
https://openai.com/business-data/

<https://openai.com/business-data/>

[\[82\]](https://www.anthropic.com/news/rare-disease-research-grants)
https://www.anthropic.com/news/rare-disease-research-grants

<https://www.anthropic.com/news/rare-disease-research-grants>

[\[84\]](https://cohere.com/research/grants/application)
https://cohere.com/research/grants/application

<https://cohere.com/research/grants/application>

[\[87\]](https://legal.mistral.ai/terms/additional-terms/)
https://legal.mistral.ai/terms/additional-terms/

<https://legal.mistral.ai/terms/additional-terms/>

[\[89\]](https://docs.litellm.ai/docs/proxy/virtual_keys)
https://docs.litellm.ai/docs/proxy/virtual_keys

<https://docs.litellm.ai/docs/proxy/virtual_keys>

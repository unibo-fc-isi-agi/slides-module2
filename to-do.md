# To-do (pictures)

## Missing pictures

- [ ] `content/validating/_index.md` → `todo-mlflow-ui.png`: screenshot of the MLflow UI
      ("letter-scoring" experiment, Evaluations tab, one groundedness rationale expanded). Needs a real run of the evaluation script.
- [ ] `content/llmaas/_index.md` → `todo-model-card.png`: screenshot of a Hugging Face model card
      (e.g. google/gemma or Qwen). Claude can draw the numbered callouts as an SVG overlay afterwards.
- [ ] `content/governance/_index.md` → `todo-ai-act-pyramid.png`: decide between
      - the EC's official pyramid (521×325 px only, says "limited risk", no pin/GPAI box):
        <https://ec.europa.eu/information_society/newsroom/image/document/2021-17/pyramid_7F5843E5-9386-8052-931F5C4E98C6E5F2_75757.jpg>
      - an SVG drawn by Claude, matching the spec (pin on high risk, GPAI side box)

## To double-check

- [ ] `governance` benchmark chart: `max-h` raised from 30vh to 40vh. Check the slide still fits.
- [ ] `governance` decision tree: the Mermaid CSS limits it to 45vh (the placeholder had 70vh). Check it is readable.
- [ ] `governance/model-card-anatomy.svg`: section → dimension tags (quality/compliance/control) were chosen by Claude.
- [ ] `governance/europe-timeline.svg`: it shows only sizes stated in the lecture, so "EU models are smaller" is weak.
      Add the global models' sizes to the lecture text if you want them in the figure.
- [ ] `validating/evaluation-pipeline.svg`: the report numbers (8/9, 1/1, 3/3) are made up.
- [ ] `prompting/context-growth.svg`: compaction happens after turn 6 (the spec said turn 5), following `chat_with_compaction.py`.
- [ ] Typo "commettee" in `static/scripts/letter_scoring_openai.py`. If you fix it, re-check the `code` shortcode line ranges.
- [ ] SVGs were checked with fallback fonts, not Signika Negative. Give them a quick look in `hugo serve`.

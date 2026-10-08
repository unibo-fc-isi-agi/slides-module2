# AGENTS.md

Guidance for AI agents (and humans) working on this repository.

## What this is

Slides for **Module 2** of the course *Intelligent Agents* ("Agenti Intelligenti", **AgI**),
Master's degree in Computer Science and Engineering, University of Bologna
(mandatory for the *Artificial Intelligence* curriculum). Teacher: Giovanni Ciatto.

Module 2 is about **engineering LLM-based agentic software**: LLM-as-a-Service,
prompt engineering and structured outputs, tools and agents, RAG, agentic skills,
workflows/orchestration, AI governance.

Technically: a [Hugo](https://gohugo.io/) site rendered as [reveal.js](https://revealjs.com/)
presentations via the [reveal-hugo](https://github.com/cric96/reveal-hugo) theme,
published to GitHub Pages at <https://unibo-fc-isi-agi.github.io/slides-module2>.

## Running locally

```bash
git submodule update --init --recursive   # theme, shared-slides, lab-snippets are submodules
hugo serve                                # requires Hugo *extended* (SCSS compilation)
```

Then open <http://localhost:1313/slides-module2/>.
Alternative: `docker compose up` (runs `shared-slides/serve.sh` in a container).
`hugo` alone builds into `build/` (see `publishDir`).

## Layout

| Path | Purpose |
|------|---------|
| `config.toml` | Hugo + reveal.js configuration (1920x1080, theme `league`, custom SCSS, mermaid) |
| `content/_index.md` | Landing presentation: course info, **ToC** (`#/toc`), teachers, links |
| `content/<lecture>/_index.md` | One lecture = one directory = one reveal.js presentation |
| `content/<lecture>/*` | That lecture's pictures, data files, diagrams sources (`.graphml`); no code (see `static/lab-snippets/`) |
| `layouts/shortcodes/` | Custom shortcodes, documented in `layouts/shortcodes/INDEX.md` |
| `layouts/partials/reveal-hugo/{head,body}.html` | Extra CSS/JS injected in every presentation (Bootstrap, FontAwesome, MathJax, QR codes, PlantUML, print-mode tweaks) |
| `assets/custom-theme.scss` | Main stylesheet, compiled by Hugo extended |
| `reusable/` | Markdown snippets imported into slides (see below) |
| `static/` | Resources shared across lectures, served at the site root |
| `static/lab-snippets/` | Git submodule: <https://github.com/unibo-fc-isi-agi/lab-snippets>, the **code of all examples and exercises** (see below); edit it there, not here |
| `themes/reveal-hugo/` | Theme (git submodule, do not edit) |
| `shared-slides/` | Build/serve/PDF scripts shared across courses (git submodule, do not edit) |
| `agi-contents-map.md` | **Desired ToC** of the whole module (topics + exercises per lecture), with coverage tracked as checkboxes (`[x]` + lecture dir) |
| `.github/workflows/build-and-deploy.yml` | CI: preprocess, `hugo`, inline mermaid, deploy to `gh-pages`, build PDFs as release assets |

### Reusable snippets (`reusable/`)

Imported with `{{% import path="reusable/<file>.md" %}}` (path is relative to the repo root):

- `front.md` — title slide of the course (course name, A.Y., teacher); used by `content/_index.md`
- `footer.md` — course/A.Y./teacher block placed under a lecture's `# Title` on its first slide
- `back.md` — closing "Lecture is Over" slide with print link and back-to-ToC link
- `running-example.md` — the **running example** (PhD admission committee assistant: 3 candidates
  with passport, transcript, letter, stored in `static/lab-snippets/data/`); import it with `{{< import ... >}}`
  (`<`, not `%`) since it contains HTML

## Writing a lecture

1. Create `content/<lecture-id>/_index.md` (short, lowercase id, e.g. `genai`, `llmaas`) with front matter:

   ```toml
   +++

   title = "[AgI] <Lecture Title>"
   description = "<one-line description>"
   outputs = ["Reveal"]

   +++
   ```

2. Skeleton:

   ```markdown
   # <Lecture Title>

   {{% import path="reusable/footer.md" %}}

   ---

   ## First slide
   ...

   ---

   {{% import path="reusable/back.md" %}}
   ```

3. Add the lecture to the ToC in `content/_index.md` (`{{< slide id="toc" >}}` slide), and tick the items it covers in `agi-contents-map.md`.

### Slide conventions

- `---` separates horizontal slides; wrap a group in `{{% section %}}` ... `{{% /section %}}` for vertical slides.
- `# Heading` = section title slide, `## Heading` = regular slide title.
- Emphasis style: `_italic_` for key terms, `__bold__` for the central concept, often combined.
- Incremental reveal: `{{% fragment %}}...{{% /fragment %}}`; named anchors: `{{< slide id="..." >}}`.
  (`section`, `fragment`, `slide` come from the reveal-hugo theme.)
- Images: `{{< image src="./pic.png" max-h="60vh" alt="..." >}}`, files stored next to `_index.md`.
- Code: __all__ runnable code (examples, exercise placeholders, running-example data) lives in the
  [`lab-snippets`](https://github.com/unibo-fc-isi-agi/lab-snippets) repository, mounted as the submodule `static/lab-snippets/`
  (Poetry project; see its README for layout, runner, and the suggested order of lectures/exercises):
    + `snippets/lecture_<NAME>/example<ID>/<file>.py` per example (`NAME` = lecture dir, `-` → `_`; `ID` as in the slides, e.g. `1`, `1bis`),
      `snippets/lecture_<NAME>/exercise<ID>/` placeholders per exercise, `snippets/lecture_<NAME>/*.py` lecture-wide utilities,
      `data/` (letters, passports, transcripts, plus pathlib helpers in `data/__init__.py`)
    + change code __in `lab-snippets`__ (commit, push), then bump the submodule here (`git -C static/lab-snippets pull`, commit the new pointer)
    + include excerpts with `{{% code path="static/lab-snippets/snippets/lecture_<NAME>/example<ID>/file.py" from="10" to="20" %}}`
      rather than pasting code, and link full files as `../lab-snippets/snippets/...` (data: `../lab-snippets/data/...`).
      When editing a snippet, **re-check the `from`/`to` line ranges** of every `code` shortcode pointing to it
    + commands are written as run from the repository root, via the runner:
      `poetry run python -m snippets -l <NAME> -e <ID> [ARGS]` (`-x <ID>` for exercises); rationale, structure, setup, and usage
      are explained in the landing deck (`content/_index.md`, slides `#/lab-snippets`, `#/lab-snippets-setup`,
      `#/lab-snippets-run`, `#/lab-snippets-exercises`), which lectures link to as `../#/lab-snippets-run` etc.
    + each example ends with a "Project Structure" slide (a `tree`-like `<pre>` block linking each involved file of `lab-snippets`);
      each exercise has a `> __Code__:` line naming its `exercise<ID>/` package and run command
    + never mention the site's own layout (`content/`, `static/`) in slides; don't run snippets inside `static/lab-snippets/`
      (it would create `__pycache__`/`.venv` there, which get published): use a separate clone
- Resources in `static/` are referenced from lectures with `../<file>` (lectures live one level down).
- Layout in columns: `{{% multicol %}}{{% col %}}...{{% /col %}}{{% col %}}...{{% /col %}}{{% /multicol %}}`.
- Diagrams: mermaid code fences (inlined by CI), or `{{< plantuml >}}`; `.graphml` sources exported to `.svg`/`.png`.
- Slides are in **English**; `goldmark` runs in unsafe mode, so raw HTML is allowed.
- Printable version: append `?print-pdf` to a presentation URL.

## Course-wide values

Academic year, course name, URLs (Virtuale, forums, APICe, institutional page) are hard-coded in
single-line shortcodes in `layouts/shortcodes/` (`academic_year`, `course_name`, `vle_url`, ...).
Update them there, once, at the start of each A.Y. — never hard-code them in slides.

## Don'ts

- Don't edit `themes/reveal-hugo/`, `shared-slides/`, or `static/lab-snippets/` (submodules) in place.
- Don't commit `build/`, `public/`, PDFs (gitignored).
- Don't put any `index.md` / `INDEX.md` under `content/`: Hugo lowercases it and it clashes with `_index.md`
  (build panics); any other `.md` there becomes a page.
- Don't write double curly braces in non-template files under `layouts/`: Hugo parses them as templates.
- Don't rename lecture directories: their names are the public URLs.

---
myst:
  html_meta:
    description: "How this Sphinx site is built and deployed — the staging of notebooks and deck PDFs, live preview, and how to publish it by hand."
---

# Building this documentation

This site is built with [Sphinx](https://www.sphinx-doc.org), writing pages in
Markdown ([MyST](https://myst-parser.readthedocs.io)) and rendering the lab
notebooks with [MyST-NB](https://myst-nb.readthedocs.io).

## Build

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html          # Linux: xdg-open
```

Or, from inside `docs/`:

```bash
cd docs
make html        # make clean, make latexpdf, … also available
```

## Live preview

```bash
pip install sphinx-autobuild
sphinx-autobuild docs docs/_build/html --open-browser
```

Edits to any page reload the browser automatically.

## PDF

```bash
cd docs
make latexpdf    # needs a TeX Live installation
```

## How the build finds the course materials

The materials live outside `docs/`, and Sphinx only reads sources from inside
its source directory. `docs/conf.py` therefore stages them before each build:

| Source | Staged to | Why |
|---|---|---|
| `Chapters/chapter_NN/chapter_NN_lab.ipynb` | `docs/labs/` | MyST-NB renders them as pages |
| `Chapters/Advanced/advanced_NN_topic/advanced_NN_topic_lab.ipynb` | `docs/advanced_labs/` | same, for the four advanced modules |
| `Chapters/chapter_NN/chapter_NN.pdf` | `docs/_extra/slides/` | copied verbatim into the HTML output via `html_extra_path`, so `slides/chapter_NN.pdf` links resolve |
| `Chapters/Advanced/advanced_NN_topic/advanced_NN_topic.pdf` | `docs/_extra/slides/` | same, so the advanced decks are downloadable too |

The mock exams are **not** staged: they are assessment material, kept out of the
repository and off this site. `docs/exams.md` describes them without linking any
file.

Both staging directories are **generated and git-ignored** — never edit anything
in them, and never add a hand-written page under `docs/labs/`: it is wiped and
recreated on every build. If a PDF is missing (for instance because a deck
hasn't been compiled yet), the build prints a note and continues; only that
link breaks.

```{admonition} Notebooks are never executed
:class: important

`nb_execution_mode = "off"` — the notebooks are rendered with the outputs they
were committed with. That keeps the build fast and dependency-free (no `torch`,
no `lifelines`, no network). To refresh outputs, run the notebook in Jupyter and
commit it.
```

## Adding a page

1. Create `docs/<name>.md`.
2. Add `<name>` to the appropriate `toctree` in `docs/index.md`.

Adding a new lecture chapter means appending its number to `SLIDE_CHAPTERS` in
`docs/conf.py` and adding a row to [Lecture slides](slides.md); a new lab is
picked up automatically by the glob in [Lab notebooks](labs.md), but deserves a
row in that page's table too, for the Colab badge.

## Publishing

The site is live at **<https://chrisw09.github.io/Quantitative-Research-Methods/>**.

```{admonition} Publishing is now a manual step
:class: important

The repository has **no GitHub Actions workflows**. The site is not rebuilt on
push — what is published stays published until someone deploys a new build.
```

GitHub Pages for this repository is configured with `build_type: workflow`,
which means a workflow was the thing that uploaded each new version. With the
workflows removed, the last deployment simply remains live. To publish changes
you have two routes:

**Build locally, then deploy from a branch.** Switch Pages to *Deploy from a
branch* in the repository settings, then push the built HTML:

```bash
sphinx-build -b html docs docs/_build/html   # add -W to fail on warnings
touch docs/_build/html/.nojekyll             # keep _static/ from being stripped
git subtree push --prefix docs/_build/html origin gh-pages
```

**Or restore the workflow.** The deleted file is one `git revert` away — it
lived at `.github/workflows/docs.yml` and is in the history if the automatic
route is wanted back.

Whichever route, build with `sphinx-build -W --keep-going` first: **any warning
then fails the build** rather than silently publishing a broken page. That is
how a missing deck PDF or a dead cross-reference gets caught, and it is worth
keeping in the habit now that nothing checks it for you.

The output in `docs/_build/html/` is a self-contained static site, so it can
equally be served from Read the Docs or any static host. The `html_extra_path`
mechanism means the deck PDFs are part of that output — a published site is
enough to teach from. The exams are not staged, so they are never part of it.

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
| `Lab_Notebooks/*.ipynb` | `docs/labs/` | MyST-NB renders them as pages |
| `Lecture_Slides/chapter_NN/chapter_NN.pdf` | `docs/_extra/slides/` | copied verbatim into the HTML output via `html_extra_path`, so `slides/chapter_NN.pdf` links resolve |
| `Mock_Exams/**/*.pdf` | `docs/_extra/exams/` | same, for `exams/*.pdf` links |

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

Deployment is automatic: [`.github/workflows/docs.yml`](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/.github/workflows/docs.yml)
builds the site and publishes it to GitHub Pages on every push to `main` that
touches `docs/`, `Lab_Notebooks/`, or a deck or exam PDF. It can also be run by
hand from the repository's **Actions** tab (*Documentation* → *Run workflow*).

Two things worth knowing about that workflow:

- It builds with `sphinx-build -W --keep-going`, so **any warning fails the
  build** rather than silently publishing a broken page. If a deployment fails,
  read the log before re-running — the warning is real.
- It publishes the artifact directly, without Jekyll, so the `_static/`
  directory survives (a `.nojekyll` file is added as well).

The output in `docs/_build/html/` is a self-contained static site, so it can
equally be served from Read the Docs or any static host. The `html_extra_path`
mechanism means the deck and exam PDFs are part of that output — a published
site is enough to teach from.

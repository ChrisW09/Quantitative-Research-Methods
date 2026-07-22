# Quick start

You don't need to install anything to **read** the slides — the compiled PDFs
are linked from [Lecture slides](slides.md). To *run* a lab you have two
options.

## ▶︎ Google Colab — zero setup (recommended)

Open any notebook in your browser; nothing to install. Every notebook's first
cell detects Colab, quietly installs the few missing packages (`ISLP`, plus
`pygam` / `xgboost` / `lifelines` where a chapter needs them; `torch` is
preinstalled on Colab), and resolves the data automatically — **12 of the 13
datasets load straight from the `ISLP` package**, and the one that isn't in
ISLP (`Advertising`) streams from the book's official site.

One-click links for all fifteen labs are on the [Lab notebooks](labs.md)
page.

```{tip}
The Colab links open straight from the public GitHub repository — you only need
a Google account to *run* a notebook, not any access to this repository.
```

## ⌥ Local Jupyter

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab Lab_Notebooks/chapter_03_lab.ipynb
```

Tested with **Python 3.9+**. Data loads via the `ISLP` package when installed,
with an automatic fallback to the bundled `ALL CSV FILES - 2nd Edition/` folder
— see [Datasets](datasets.md).

## Rebuilding the LaTeX materials

The decks are compiled from LaTeX sources kept in the repository, so anything
can be edited and rebuilt. This needs a TeX Live distribution with `beamer`,
`tcolorbox`, `tikz`, `listings` and `booktabs`.

::::{tab-set}

:::{tab-item} A lecture deck

```bash
cd Lecture_Slides/chapter_03
pdflatex chapter_03.tex
pdflatex chapter_03.tex   # second pass for the navigation bar
```
:::

:::{tab-item} This documentation

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html
```

See [Building the docs](building-docs.md) for live-reload and PDF output.
:::

::::

## Where to go next

- [The course at a glance](course.md) — the 12-lecture plan.
- [Lecture slides](slides.md) — deck-by-deck contents and exercise counts.
- [Lab notebooks](labs.md) — every lab, rendered in full.
- [Python environment](environment.md) — what's pinned and why.

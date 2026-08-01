---
myst:
  html_meta:
    description: "Run any course lab on Google Colab with zero setup, install the local Python environment from week two, and rebuild the LaTeX materials."
---

# Quick start

{.qrm-lead}
You don't need to install anything to **read** the slides — the compiled PDFs
are linked from [Lecture slides](slides.md). To *run* a lab, **start in Colab**.
Install locally later, in your own time, once you know you want to.

## ▶︎ Day one: Google Colab — nothing to install

This is the documented first-session route, and it is the one to use in the
room. Open any notebook in your browser; there is nothing to set up and nothing
to go wrong on a projector.

Every notebook's first cell detects Colab, quietly installs the few missing
packages (`ISLP`, plus `pygam` / `xgboost` / `lifelines` where a chapter needs
them; `torch` is preinstalled on Colab), and resolves the data automatically —
**datasets load straight from the `ISLP` package wherever possible**, and the
four the package does not ship (`Advertising`, `Heart`, `Income1`, `Income2`)
stream from the book's official site.

One-click links for all fifteen notebooks are on the
[Lab notebooks](labs.md) page.

```{tip}
The Colab links open straight from the public GitHub repository — you only need
a Google account to *run* a notebook, not any access to this repository.
```

Colab is enough for every lab in the course, including the Chapter 10 deep
learning lab.

## ⌥ Week two: a local virtual environment

Worth doing once the course is under way, and worth doing properly: a local
environment is faster, works offline, keeps your edits, and is what you will
want for any serious piece of work. It is not a first-session activity — the
install pulls in **around 150 packages and several hundred megabytes**, because
the book companion package `ISLP` hard-requires `torch` (together with
`pytorch_lightning` and `torchmetrics`). On Windows `torch` alone is over
100 MB; on Linux it is several times that, as the wheel bundles the CUDA
libraries. Budget time for it, on a decent connection, outside class.

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab Chapters/chapter_03/chapter_03_lab.ipynb
```

Tested with **Python 3.9+**. Data loads via the `ISLP` package when installed,
with an automatic fallback to the bundled `ALL CSV FILES - 2nd Edition/` folder
— see [Datasets](datasets.md), and [Python environment](environment.md) for what
is pinned and why.

## Rebuilding the LaTeX materials

The decks are compiled from LaTeX sources kept in the repository, so anything
can be edited and rebuilt. This needs a TeX Live distribution with `beamer`,
`tcolorbox`, `tikz`, `listings` and `booktabs`.

::::{tab-set}

:::{tab-item} A lecture deck

```bash
cd Chapters/chapter_03
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

- [For students](for-students.md) — prerequisites, the precourse skip rule, workload, and how to revise.
- [The course at a glance](course.md) — the 15-lecture plan.
- [Lecture slides](slides.md) — deck-by-deck contents, exercise counts, and what sits in each deck's optional appendix.
- [Lab notebooks](labs.md) — every lab, rendered in full.
- [Python environment](environment.md) — what's pinned and why.

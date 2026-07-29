# Python environment

`requirements.txt` pins the packages used by the notebooks and by the code
examples printed on the slides.

| Purpose | Packages |
|---|---|
| Core scientific stack | `numpy>=1.24` · `pandas>=2.0` · `matplotlib>=3.7` · `seaborn>=0.12` · `scipy>=1.10` |
| Statistics & machine learning | `statsmodels>=0.14` · `scikit-learn>=1.3` |
| Book companion (datasets + helpers) | `ISLP>=0.3` |
| Chapter-specific | `pygam>=0.9` (Ch 7) · `xgboost>=2.0` (Ch 8, genuinely optional) · `torch>=2.1` (Ch 10) · `lifelines>=0.27` (Ch 11) |
| Notebook environment | `jupyter>=1.0` |

Only `xgboost` is optional in practice. `pygam`, `torch` and `lifelines` are
pinned here for clarity, but they are also **hard dependencies of `ISLP`** and
arrive whether or not you list them — see
[Why the install is large](#why-the-install-is-large).

## Install

```{important}
For a first session, don't. Use [Colab](quickstart.md) — it needs no install and
runs every lab in the course. A local environment is the week-two route: better
for real work, but not something to attempt with a room waiting.
```

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Tested with **Python 3.9+**. Expect around 150 packages and several hundred
megabytes — see [Why the install is large](#why-the-install-is-large) below.

## Notes on the chapter-specific packages

`pygam`
: Used in the Chapter 7 lab for generalized additive models. `statsmodels`
  covers most of the chapter; `pygam` is what makes the smooth-term plots easy.

`xgboost`
: Optional. Chapter 8 works end-to-end with scikit-learn's
  `GradientBoostingClassifier`; `xgboost` appears only in a side-by-side
  comparison.

`torch`
: Chapter 10 (deep learning). Preinstalled on Colab, so the Colab path needs no
  install; locally, install the build that matches your platform if you want GPU
  support. Note that it arrives whether you ask for it or not — see below.

`lifelines`
: Chapter 11 (survival analysis) — a self-study code reference, so you can skip
  the notebook if you only teach the 12-lecture plan. The package still
  installs, because `ISLP` requires it.

## Why the install is large

There is no useful "minimal install" of this environment, and the reason is
`ISLP` itself. The book companion package does not merely *suggest* the
chapter-specific libraries — it **hard-requires** them. Its declared
dependencies include `torch`, `pytorch_lightning`, `torchmetrics`, `lifelines`
and `pygam` alongside the core scientific stack.

So asking for the datasets and helpers used from Lecture 1 onwards also installs
the deep-learning stack you will not touch until Chapter 10:

- resolving `requirements.txt` pulls in roughly **150 packages**;
- on Windows that is several hundred megabytes of downloads, `torch` alone over
  100 MB;
- on Linux it is substantially more again — the `torch` wheel bundles the CUDA
  libraries and is several hundred megabytes on its own.

Dropping `torch>=2.1` from `requirements.txt` does not help: `pip` reinstates it
as a dependency of `ISLP`. The only genuinely light route is
[Colab](quickstart.md), where `torch` is already present.

## Colab — the recommended route

Every notebook's first cell detects Colab and installs only what's missing, so
you can open a lab in a fresh runtime and run it top to bottom — see
[Quick start](quickstart.md). This is the day-one path for students, and it
covers every lab in the course.

## LaTeX

Rebuilding the [slides](slides.md) or [exams](exams.md) requires a TeX Live
distribution including `beamer`, `tcolorbox`, `tikz`, `listings` and `booktabs`.
Nothing else in the repository depends on LaTeX — the compiled PDFs are
committed.

## Where to go next

- [Quick start](quickstart.md) — Colab in one click on day one, a local venv from week two.
- [For students](for-students.md) — prerequisites, workload, and what to do when your numbers differ.
- [Lab notebooks](labs.md) — what the environment is for.
- [Building the docs](building-docs.md) — the separate, documentation-only requirements.

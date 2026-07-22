# Python environment

`requirements.txt` pins the packages used by the notebooks and by the code
examples printed on the slides.

| Purpose | Packages |
|---|---|
| Core scientific stack | `numpy>=1.24` · `pandas>=2.0` · `matplotlib>=3.7` · `seaborn>=0.12` · `scipy>=1.10` |
| Statistics & machine learning | `statsmodels>=0.14` · `scikit-learn>=1.3` |
| Book companion (datasets + helpers) | `ISLP>=0.3` |
| Chapter-specific | `pygam>=0.9` (Ch 7) · `xgboost>=2.0` (Ch 8, optional) · `torch>=2.1` (Ch 10) · `lifelines>=0.27` (Ch 11) |
| Notebook environment | `jupyter>=1.0` |

## Install

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Tested with **Python 3.9+**.

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
  support.

`lifelines`
: Chapter 11 (survival analysis) — a self-study notebook, so you can skip it if
  you only teach the 12-lecture plan.

```{admonition} Minimal install
:class: tip

If you only need Chapters 1–6, `numpy`, `pandas`, `matplotlib`, `seaborn`,
`scipy`, `statsmodels`, `scikit-learn`, `ISLP` and `jupyter` are enough.
```

## Colab

Every notebook's first cell detects Colab and installs only what's missing, so
you can open a lab in a fresh runtime and run it top to bottom — see
[Quick start](quickstart.md).

## LaTeX

Rebuilding the [slides](slides.md) or [exams](exams.md) requires a TeX Live
distribution including `beamer`, `tcolorbox`, `tikz`, `listings` and `booktabs`.
Nothing else in the repository depends on LaTeX — the compiled PDFs are
committed.

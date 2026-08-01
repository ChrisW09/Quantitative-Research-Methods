---
myst:
  html_meta:
    description: "Four optional advanced modules extending the course — randomised controlled trials, Shapley-value explanations, conformal prediction, and GLMs with penalized splines — each with a full lecture deck and a companion notebook."
---

# Advanced modules

{.qrm-lead}
Four optional, self-study modules that take the course beyond ISLP: causal
inference with randomised experiments, explaining black-box models with Shapley
values, distribution-free uncertainty with conformal prediction, and the
exponential-family machinery that unifies GLMs and penalized splines.

:::{container} qrm-chips
[**4** modules]{.qrm-chip}
[**300** slides]{.qrm-chip}
[**25 + 8** exercises with solutions]{.qrm-chip}
[**4** companion notebooks]{.qrm-chip}
[optional **self-study**]{.qrm-chip}
:::

Each module is built exactly like a course deck — the same colour-coded callout
boxes, every exercise followed immediately by its worked solution, a closing
summary block and an optional appendix — and each is paired with a companion
notebook whose printed numbers match the slides seed-for-seed
(`np.random.default_rng(2024)`). The modules sit **outside** the twelve-lecture
plan: nothing in the course or its exams depends on them.

## The modules

| | Module | What it covers | Slides | Deck | Notebook | Colab |
|:--:|---|---|:--:|:--:|:--:|:--:|
| A1 | Randomised Controlled Trials | Potential outcomes, the selection-bias decomposition, why randomisation works, regression adjustment with HC2 errors, power and sample size, ITT vs per-protocol, the peeking problem | 71 | <a href="slides/advanced_01_rcts.pdf">Open</a> | [Rendered](advanced_labs/advanced_01_rcts_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Advanced/advanced_01_rcts/advanced_01_rcts_lab.ipynb) |
| A2 | Explainable AI with Shapley Values | Cooperative games and the four axioms, the marginal value function, exact Shapley by enumeration, Monte-Carlo sampling, waterfalls and global importance, the correlated-feature and retrain pitfalls | 73 | <a href="slides/advanced_02_shapley.pdf">Open</a> | [Rendered](advanced_labs/advanced_02_shapley_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Advanced/advanced_02_shapley/advanced_02_shapley_lab.ipynb) |
| A3 | Conformal Prediction | Exchangeability, split conformal and the finite-sample quantile, marginal vs conditional coverage, locally weighted scores and CQR, classification prediction sets, the OLS stress test | 74 | <a href="slides/advanced_03_conformal.pdf">Open</a> | [Rendered](advanced_labs/advanced_03_conformal_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Advanced/advanced_03_conformal/advanced_03_conformal_lab.ipynb) |
| A4 | GLMs and Splines | The exponential family, Poisson regression on `Bikeshare`, deviance and LRTs, overdispersion (quasi-Poisson, negative binomial), penalized splines and effective df, a count GAM | 82 | <a href="slides/advanced_04_glms_splines.pdf">Open</a> | [Rendered](advanced_labs/advanced_04_glms_splines_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Advanced/advanced_04_glms_splines/advanced_04_glms_splines_lab.ipynb) |

```{tip}
Everything is implemented **from scratch** — exact Shapley values, split
conformal, P-splines — so the notebooks need nothing beyond the course
environment. The slides name the production tools (`shap`, `MAPIE`, `mgcv`-style
GAM software) once the mechanics are understood.
```

## What each module assumes

Each module bridges back to the course chapters it extends, and assumes them:

| Module | Builds on |
|:--:|---|
| A1 | Ch 0 (standard errors, tests) · Ch 3 (regression) · Ch 5 (simulation) · Ch 13 (multiple testing — the peeking problem) |
| A2 | Ch 0b (counting and the 2ᵖ cost) · Ch 8 (boosting, variable importance) · Ch 10 (black-box models) |
| A3 | Ch 3 (prediction intervals) · Ch 5 (train/validation splits) |
| A4 | Ch 3–4 (linear and logistic regression) · Ch 5–6 (CV, AIC) · Ch 7 (splines and GAMs) |

## How they are built

The sources live in
[`Advanced/`](https://github.com/ChrisW09/Quantitative-Research-Methods/tree/main/Advanced)
— one folder per deck with its LaTeX source, its `make_figures.py` (every
figure is computed from the course datasets or a seeded simulation) and the
compiled PDF; the notebooks ship with stored outputs and run on Colab with one
click, resolving data exactly like the [course labs](labs.md). From the
repository root, `make advanced` rebuilds any deck whose source changed. The
folder also carries the distilled style guides (`STYLE_DECK.md`,
`STYLE_NOTEBOOK.md`) used to author them — the starting point for adding a
module A5.

## All advanced notebooks

```{toctree}
:maxdepth: 1
:glob:

advanced_labs/advanced_*_lab
```

## Where to go next

- [Lecture slides](slides.md) — the twelve course decks these modules extend.
- [Lab notebooks](labs.md) — the course labs, built to the same pattern.
- [The course at a glance](course.md) — where the twelve-lecture plan ends and these begin.
- [Repository layout](repository.md) — where everything lives.

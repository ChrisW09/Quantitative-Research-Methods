# Advanced modules

Twelve optional, self-study modules. Seven extend the taught course beyond ISLP —
causal inference from experiments (A1) and from observational data (A10), model
explanation, distribution-free uncertainty, the GLM/spline machinery behind
Chapters 4 and 7, time series and forecasting (A11), and Bayesian inference
(A12) — and five are ISLP chapters lifted out of the taught sequence: support
vector machines (Ch 9), deep learning (Ch 10), survival analysis (Ch 11),
unsupervised learning (Ch 12) and multiple testing (Ch 13).
Each module is a full Beamer
deck in the course's house style — same box grammar, every exercise followed
immediately by its worked solution, closing summary block, optional appendix —
paired with a companion Jupyter notebook whose numbers match the slides
seed-for-seed. They are **not** part of the taught plan, but two are
**exam-relevant**: the final mock exam is weighted toward modules A7 and A9,
and Short Exam E carries a multiple-testing problem drawn from A7.

| Module | Title | What it covers | Deck | Exercises | Notebook |
|---|---|---|---|---|---|
| A1 | Randomised Controlled Trials | Potential outcomes, selection-bias decomposition, randomisation, regression adjustment (HC2), power/MDE, ITT vs per-protocol, peeking | 77 pages | 6 + 2 extended | `advanced_01_rcts_lab.ipynb` |
| A2 | Explainable AI with Shapley Values | Cooperative games, the Shapley axioms, exact enumeration vs Monte-Carlo, waterfalls, global importance, correlated-feature and retrain pitfalls | 82 pages | 6 + 2 extended | `advanced_02_shapley_lab.ipynb` |
| A3 | Conformal Prediction | Exchangeability, split conformal, the finite-sample quantile, marginal vs conditional coverage, CQR, prediction sets, the OLS stress test | 79 pages | 6 + 2 extended | `advanced_03_conformal_lab.ipynb` |
| A4 | GLMs and Splines | Exponential family, Poisson regression on `Bikeshare`, deviance/LRT/AIC, overdispersion (quasi-Poisson, NB), penalized splines and edf, a count GAM | 94 pages | 7 + 2 extended | `advanced_04_glms_splines_lab.ipynb` |
| A5 | Support Vector Machines *(ISLP Ch 9)* | Maximal-margin classifier, the soft margin and the cost *C*, the support-vector classifier, polynomial and radial kernels, tuning by CV | 94 pages | 7 + 3 | `advanced_05_svm_lab.ipynb` |
| A6 | Survival Analysis *(ISLP Ch 11)* | Censoring, the survival and hazard functions, Kaplan–Meier, the log-rank test, Cox proportional hazards | 96 pages | 7 + 3 | `advanced_06_survival_lab.ipynb` |
| A7 | Multiple Testing *(ISLP Ch 13)* | Why naive testing fails at scale, FWER, Bonferroni and Holm, the false discovery rate, Benjamini–Hochberg, *p*-hacking | 75 pages | 5 + 3 | `advanced_07_multiple_testing_lab.ipynb` |
| A8 | Unsupervised Learning *(ISLP Ch 12)* | No test error to validate against, PCA (loadings, scores, PVE, biplot), scaling, *K*-means and its local optima, dendrograms, linkage and dissimilarity, clusters in pure noise | 102 pages | 6 + 3 | `advanced_08_unsupervised_lab.ipynb` |
| A9 | Deep Learning *(ISLP Ch 10)* | The MLP as adaptive basis functions, activations, training as gradient descent on a loss, epochs and early stopping, dropout and weight decay, when a boosted tree still wins | 93 pages | 6 + 3 | `advanced_09_deep_learning_lab.ipynb` |
| A10 | Causal Inference from Observational Data | Confounders/mediators/colliders, omitted-variable bias (γδ), regression adjustment, stratification, propensity-score matching, difference-in-differences, instrumental variables (Wald) | 58 pages | 5 + 2 extended | *(in preparation — `make_figures.py` is the lab)* |
| A11 | Time Series and Forecasting | Stationarity, the ACF by hand and in code, AR as OLS on lags, baselines (mean, seasonal naive), rolling-origin backtesting vs shuffled-CV leakage, why returns resist forecasting | 55 pages | 5 + 2 extended | *(in preparation — `make_figures.py` is the lab)* |
| A12 | Bayesian Inference | Prior × likelihood ∝ posterior, Beta–binomial updating, credible intervals, precision-weighted shrinkage, ridge as MAP (λ = σ²/τ²), Metropolis from scratch, a Bayesian A/B decision | 53 pages | 4 + 2 extended | *(in preparation — `make_figures.py` is the lab)* |

## Prerequisites, and a suggested reading order

Each module assumes the course chapters it extends:

- **A1** — Ch 0 (standard errors, tests), Ch 3 (regression), Ch 5 (simulation), A7 (multiple testing).
- **A2** — Ch 0b (counting, 2ᵖ), Ch 8 (boosting, variable importance), A9 (black-box models).
- **A3** — Ch 3 (prediction intervals), Ch 5 (train/validation splits).
- **A4** — Ch 3 (linear regression), Ch 4 (logistic regression), Ch 5–6 (CV, AIC), Ch 7 (splines, GAMs).
- **A5** — Ch 4 (classification, ROC/AUC), Ch 5 (cross-validation).
- **A6** — Ch 0 (distributions, tests), Ch 3 (regression), Ch 4 (logistic regression).
- **A7** — Ch 0 (hypothesis testing, *p*-values), Ch 5 (resampling).
- **A8** — Ch 2 (what a test error buys you), Ch 5 (resampling, stability).
- **A9** — Ch 3 (least squares, the linear predictor), Ch 5 (validation, overfitting).
- **A10** — Ch 3 (regression, omitted variables), Ch 4 (logistic → propensity scores), Ch 5 (simulation), A1 (potential outcomes).
- **A11** — Ch 3 (OLS on lagged copies), Ch 4 (`Weekly`), Ch 5 (evaluation, leakage).
- **A12** — Ch 0 (intervals, tests), Ch 3–4 (the likelihood), Ch 6 (ridge, shrinkage).

The numbering is a grouping (A1–A4 and A10–A12 extend the course, A5–A9 are
lifted ISLP chapters), **not** a reading order. Three constraints and one
priority determine a sensible sequence:

1. **A7 and A9 first** — they are the exam-relevant pair (assigned as
   self-study after the Chapter 8 session), and they unlock A1 and A2.
2. **A7 before A1**, **A9 before A2**, and **A1 before A10** — the only
   inter-module dependencies.
3. Everything else — A3, A4, A5, A6, A8, A11, A12 — stands alone on the taught
   chapters and can be read in any order; folder order works.

## Layout

Each module is one self-contained folder holding its deck and its lab together,
the same shape as a chapter folder in [`Chapters/`](../):

```text
Advanced/
├── advanced_0N_topic/
│   ├── advanced_0N_topic.tex        # source (course preamble, self-contained)
│   ├── advanced_0N_topic.pdf        # compiled deck (committed)
│   ├── advanced_0N_topic_lab.ipynb  # companion lab, stored outputs, Colab-ready
│   ├── images/                      # matplotlib figures used by the deck
│   └── make_figures.py              # regenerates every figure from the course data
├── STYLE_DECK.md                    # the house style, distilled (for new modules)
└── STYLE_NOTEBOOK.md
```

## Running a notebook

Every notebook opens with a Colab badge — one click, nothing to install; the
setup cell resolves data via the `ISLP` package, the book's site, or the
bundled `ALL CSV FILES - 2nd Edition/` folder, exactly like the course labs.
Locally: run it from inside its own module folder so the relative CSV path
resolves.
No packages beyond the course `requirements.txt` are needed — Shapley values,
conformal prediction, the P-splines, propensity matching, the ACF/AR machinery
and the Metropolis sampler are implemented from scratch on purpose (`shap`,
`MAPIE`, `linearmodels`, `statsmodels.tsa` and `PyMC` are named on the slides
as the production tools). A10–A12 do not have companion notebooks yet: their
`make_figures.py` doubles as the lab and reproduces every number on the
slides.

## Rebuilding a deck

```bash
cd Chapters/Advanced/advanced_01_rcts
python3 make_figures.py     # regenerate images/ from the course datasets
pdflatex advanced_01_rcts.tex
pdflatex advanced_01_rcts.tex   # second pass for the navigation bar
```

Or, from the repository root, `make advanced` rebuilds every advanced deck
whose source changed. Every figure is computed from the bundled datasets or a
seeded simulation (`np.random.default_rng(2024)`) — nothing is sketched — and
every number quoted on a slide is reproduced by the companion notebook.

# Advanced modules

Seven optional, self-study modules. Four extend the taught course beyond ISLP —
causal inference, model explanation, distribution-free uncertainty, and the
GLM/spline machinery behind Chapters 4 and 7 — and three are ISLP chapters
lifted out of the taught sequence: support vector machines (Ch 9), survival
analysis (Ch 11) and multiple testing (Ch 13). Each module is a full Beamer
deck in the course's house style — same box grammar, every exercise followed
immediately by its worked solution, closing summary block, optional appendix —
paired with a companion Jupyter notebook whose numbers match the slides
seed-for-seed. They are **not** part of the taught plan. Note that the mock exams still carry a
multiple-testing problem, which now draws on module A7.

| Module | Title | What it covers | Deck | Exercises | Notebook |
|---|---|---|---|---|---|
| A1 | Randomised Controlled Trials | Potential outcomes, selection-bias decomposition, randomisation, regression adjustment (HC2), power/MDE, ITT vs per-protocol, peeking | 72 pages | 6 + 2 extended | `advanced_01_rcts_lab.ipynb` |
| A2 | Explainable AI with Shapley Values | Cooperative games, the Shapley axioms, exact enumeration vs Monte-Carlo, waterfalls, global importance, correlated-feature and retrain pitfalls | 75 pages | 6 + 2 extended | `advanced_02_shapley_lab.ipynb` |
| A3 | Conformal Prediction | Exchangeability, split conformal, the finite-sample quantile, marginal vs conditional coverage, CQR, prediction sets, the OLS stress test | 74 pages | 6 + 2 extended | `advanced_03_conformal_lab.ipynb` |
| A4 | GLMs and Splines | Exponential family, Poisson regression on `Bikeshare`, deviance/LRT/AIC, overdispersion (quasi-Poisson, NB), penalized splines and edf, a count GAM | 83 pages | 7 + 2 extended | `advanced_04_glms_splines_lab.ipynb` |
| A5 | Support Vector Machines *(ISLP Ch 9)* | Maximal-margin classifier, the soft margin and the cost *C*, the support-vector classifier, polynomial and radial kernels, tuning by CV | 94 pages | 7 + 3 | `advanced_05_svm_lab.ipynb` |
| A6 | Survival Analysis *(ISLP Ch 11)* | Censoring, the survival and hazard functions, Kaplan–Meier, the log-rank test, Cox proportional hazards | 94 pages | 7 + 3 | `advanced_06_survival_lab.ipynb` |
| A7 | Multiple Testing *(ISLP Ch 13)* | Why naive testing fails at scale, FWER, Bonferroni and Holm, the false discovery rate, Benjamini–Hochberg, *p*-hacking | 70 pages | 5 + 3 | `advanced_07_multiple_testing_lab.ipynb` |

## Prerequisites

Each module assumes the course chapters it extends:

- **A1** — Ch 0 (standard errors, tests), Ch 3 (regression), Ch 5 (simulation), A7 (multiple testing).
- **A2** — Ch 0b (counting, 2ᵖ), Ch 8 (boosting, variable importance), Ch 10 (black-box models).
- **A3** — Ch 3 (prediction intervals), Ch 5 (train/validation splits).
- **A4** — Ch 3 (linear regression), Ch 4 (logistic regression), Ch 5–6 (CV, AIC), Ch 7 (splines, GAMs).
- **A5** — Ch 4 (classification, ROC/AUC), Ch 5 (cross-validation).
- **A6** — Ch 0 (distributions, tests), Ch 3 (regression), Ch 4 (logistic regression).
- **A7** — Ch 0 (hypothesis testing, *p*-values), Ch 5 (resampling).

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
conformal prediction and the P-splines are implemented from scratch on purpose
(`shap` and `MAPIE` are named on the slides as the production tools).

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

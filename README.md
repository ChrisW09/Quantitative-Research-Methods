# Quantitative Research

Lecture slides (LaTeX Beamer) by Prof. Dr. Christoph Weisser, HSBI — Summer Semester 2026.

| Part | Folder | Topic |
|------|--------|-------|
| 1 | `Part_1_Descriptive_Statistics` | Basic concepts, levels of measurement, frequencies, measures of central tendency (incl. trimmed and geometric mean) and dispersion (range, IQR, variance, coefficients of variation) |
| 2 | `Part_2_Graphical_Representations` | Empirical CDF, histogram, boxplot -- constructing, reading and comparing distributions |
| 3 | `Part_3_Statistical_Inference` | Foundations (normal distribution, CLT), confidence intervals, sample size, hypothesis tests, p-values, one-sided tests, types of error (appendix: estimator properties, law of large numbers) |
| 4 | `Part_4_Regression` | Correlation, least squares step by step, goodness of fit, residual analysis and QQ-plot, inference for regression, multiple regression (appendix: minimum property of OLS, interactions, diagnostics, collinearity) |
| 5 | `Part_5_Classification` | Two-way tables and conditional probability, logistic regression, classification rules, confusion matrix, base rates and precision, ROC/AUC (appendix: total probability and Bayes' theorem; Bayes classifiers -- naive Bayes, LDA) |

Every section contains exercises (many adapted from the course *Statistik für
Ökonomen* and its mock exams) with step-by-step solutions.

Each part folder contains

- `Part_k_<Topic>.tex` — the slide deck (compiled PDF next to it),
- `Part_k_<Topic>.py` — Python script that reproduces every number on the slides,
- `make_figures.py` — regenerates the computed figures in `images/` (Parts 2–5),
- `images/` — all figures used by the deck.

All decks share `common/preamble.tex` (theme, colours, boxes, code listings,
course-overview slide). The data sets for Parts 4 and 5 are in `data/`
(Advertising, Credit and Default data from James, Witten, Hastie, Tibshirani:
*An Introduction to Statistical Learning*, www.statlearning.com).

## Building

```sh
cd Part_4_Regression
latexmk -pdf Part_4_Regression.tex
```

Speaker notes (talk tracks in Part 3) can be enabled in `common/preamble.tex`.

## Requirements

- TeX Live (beamer, tikz, pgfplots, listings, booktabs)
- Python 3 with numpy, pandas, scipy, statsmodels, matplotlib (>= 3.8) and
  scikit-learn (Part 5), e.g. via the Anaconda Distribution or
  `pip install numpy pandas scipy statsmodels matplotlib scikit-learn jupyter`

Run a script from its folder, e.g. `cd Part_4_Regression && python3 Part_4_Regression.py`.

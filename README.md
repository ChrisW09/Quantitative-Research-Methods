# Quantitative Research

Lecture slides (LaTeX Beamer) by Prof. Dr. Christoph Weisser, HSBI — Summer Semester 2026.

| Part | Folder | Topic |
|------|--------|-------|
| 1 | `Part_1_Descriptive_Statistics` | Basic concepts, levels of measurement, frequencies, measures of central tendency and dispersion |
| 2 | `Part_2_Graphical_Representations` | Empirical CDF, histogram, boxplot |
| 3 | `Part_3_Statistical_Inference` | Confidence intervals, hypothesis tests, p-values, one-sided tests, types of error |
| 4 | `Part_4_Regression` | Correlation, simple and multiple linear regression, inference for regression (appendix: derivations, interactions, diagnostics, collinearity) |
| 5 | `Part_5_Classification` | Logistic regression, classification rules, confusion matrix, ROC/AUC (appendix: Bayes classifiers -- naive Bayes, LDA) |

Each part folder contains

- `Part_k_<Topic>.tex` — the slide deck (compiled PDF next to it),
- `Part_k_<Topic>.R` — R script that reproduces every number on the slides,
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
- R with the packages `MASS` and `e1071` (Part 5)
- Python 3 with numpy, pandas, matplotlib, scipy, statsmodels (only to regenerate figures)

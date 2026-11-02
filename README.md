# Quantitative Research

Lecture slides (LaTeX Beamer) and a mock exam by Prof. Dr. Christoph Weisser.

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

## Mock exam

`Mock_Exams/Mock_Exam_1/` contains a mock exam on Parts 3–5 (an English
counterpart of the *Statistik für Ökonomen* mock exams):

| Task | Topic | Points |
|------|-------|--------|
| 1 | Part 3 -- Statistical inference (test, p-value, confidence interval) | 20 |
| 2 | Part 4 -- Regression (least squares, R², reading a `statsmodels` output) | 20 |
| 3 | Part 5 -- Classification (odds, logistic regression, confusion matrix) | 20 |

Each task has 10 subtasks worth 2 points (60 points, 120 minutes). Every subtask
asks for exactly **one** result and can be solved on its own, so grading is quick
and an error does not carry over. Three PDFs are provided:

- `Quantitative Research Mock Exam 1.pdf` -- the exam, with the standard normal
  table and the t-table appended,
- `Quantitative Research Mock Exam 1 Solutions.pdf` -- worked solutions, grading
  key (2-point rubric per subtask) and a results overview,
- `Quantitative Research Mock Exam 1 Slides.pdf` -- slides for discussing the
  solutions in class.

All three are generated from one source in `Mock_Exams/_Generator/` -- edit
`spec_qrm1.py` there, never the generated `.tex` files (see
`Mock_Exams/_Generator/README.md`):

```sh
cd Mock_Exams/_Generator
python3 figures.py     # figures
python3 verify.py      # recompute all 30 results
python3 build.py 1     # .tex files, automatic checks, PDFs
```

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

# Quantitative Research

Lecture slides (LaTeX Beamer), companion Jupyter notebooks, a mock exam and a
separate **Python course** by Prof. Dr. Christoph Weisser.

| Part | Folder | Topic |
|------|--------|-------|
| 1 | `Part_1_Descriptive_Statistics` | Basic concepts, levels of measurement, frequencies, measures of central tendency (incl. trimmed and geometric mean) and dispersion (range, IQR, variance, coefficients of variation) |
| 2 | `Part_2_Graphical_Representations` | Empirical CDF, histogram, boxplot -- constructing, reading and comparing distributions |
| 3 | `Part_3_Statistical_Inference` | Foundations (normal distribution, CLT), confidence intervals, sample size, hypothesis tests, p-values, one-sided tests, types of error (appendix: estimator properties, law of large numbers) |
| 4 | `Part_4_Regression` | Correlation, least squares step by step (running exercise "online shop"), goodness of fit, inference for regression, multiple regression (appendix: derivation of the OLS estimators, minimum property, residual analysis, leverage, QQ-plot, interactions, diagnostics, collinearity) |
| 5 | `Part_5_Classification` | Two-way tables and conditional probability, logistic regression, classification rules, confusion matrix, base rates and precision, ROC/AUC (appendix: total probability and Bayes' theorem; Bayes classifiers -- naive Bayes, LDA) |
| Py | `Python_Course` | Separate Python course: a 90-minute introduction (Python basics, pandas, a first chart) and a self-paced track from NumPy, pandas and visualisation to scikit-learn and PyTorch -- see below |

Every section contains exercises (many adapted from the course *Statistik für
Ökonomen* and its mock exams) with step-by-step solutions -- roughly one
exercise every 15--20 minutes of lecture time.

Each part folder contains

- `Part_k_<Topic>.tex` — the slide deck (compiled PDF next to it),
- `Part_k_<Topic>.ipynb` — companion Jupyter notebook: same sections as the
  slides, all Python examples and every exercise (try it yourself, then the
  solution),
- `Part_k_<Topic>.py` — Python script that reproduces every number on the slides,
- `make_figures.py` — regenerates the computed figures in `images/` (Parts 2–5),
- `images/` — all figures used by the deck.

All decks share `common/preamble.tex` (theme, colours, boxes, code listings,
course-overview slide). The data sets for Parts 4 and 5 are in `data/`
(Advertising, Credit and Default data from James, Witten, Hastie, Tibshirani:
*An Introduction to Statistical Learning*, www.statlearning.com).

## Jupyter notebooks and Google Colab

Every part has a companion notebook that follows the slides section by section.
The slides point to it with "Try it yourself" links. Open a notebook locally in
Jupyter / VS Code, or directly in Google Colab (nothing to install):

| Part | Notebook | Colab |
|------|----------|-------|
| 1 -- Descriptive Statistics | [`Part_1_Descriptive_Statistics.ipynb`](Part_1_Descriptive_Statistics/Part_1_Descriptive_Statistics.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Part_1_Descriptive_Statistics/Part_1_Descriptive_Statistics.ipynb) |
| 2 -- Graphical Representations | [`Part_2_Graphical_Representations.ipynb`](Part_2_Graphical_Representations/Part_2_Graphical_Representations.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Part_2_Graphical_Representations/Part_2_Graphical_Representations.ipynb) |
| 3 -- Statistical Inference | [`Part_3_Statistical_Inference.ipynb`](Part_3_Statistical_Inference/Part_3_Statistical_Inference.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Part_3_Statistical_Inference/Part_3_Statistical_Inference.ipynb) |
| 4 -- Regression | [`Part_4_Regression.ipynb`](Part_4_Regression/Part_4_Regression.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Part_4_Regression/Part_4_Regression.ipynb) |
| 5 -- Classification | [`Part_5_Classification.ipynb`](Part_5_Classification/Part_5_Classification.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Part_5_Classification/Part_5_Classification.ipynb) |

The notebooks load the data sets from the local `data/` folder when they run
inside the repository and from GitHub otherwise (e.g. in Colab). Run the cells
from top to bottom; in the exercise sections, try the "Your turn" cell first and
then compare with the solution.

## Python course

`Python_Course/` is a separate, self-contained Python course that comes with the
lecture -- no programming experience needed, every notebook runs in Google Colab.

| Track | Content | Start |
|-------|---------|-------|
| 1 -- Introduction (90 min, live) | Python basics, data structures, control flow, functions, first steps with pandas (+ seaborn bonus) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/01_welcome_to_python.ipynb) |
| 2 -- Advanced & self-learning (~12--14 h) | 15 notebooks: fundamentals in depth, NumPy, pandas, data cleaning, matplotlib, seaborn, EDA, machine learning, scikit-learn, PyTorch, capstone project | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/01_python_basics.ipynb) |

All notebooks with their Colab links, timings and a suggested path alongside
Parts 1--5: [`Python_Course/README.md`](Python_Course/README.md). The course is
adapted from the
[Python for Data Science Workshop](https://github.com/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop)
(MIT License, see `Python_Course/LICENSE`).

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
- Python 3 with numpy, pandas, scipy, statsmodels, matplotlib (>= 3.8),
  scikit-learn (Part 5) and Jupyter, e.g. via the Anaconda Distribution or
  `pip install numpy pandas scipy statsmodels matplotlib scikit-learn jupyter`
  (the Python course additionally uses seaborn and, in one notebook, PyTorch)
  -- or use Google Colab (see above), where everything is preinstalled

Run a script from its folder, e.g. `cd Part_4_Regression && python3 Part_4_Regression.py`.

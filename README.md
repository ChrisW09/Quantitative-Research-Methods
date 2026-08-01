<h1 align="center">Quantitative Research Methods</h1>

<p align="center">
  A complete, ready-to-teach university course in statistical learning —<br>
  twelve slide decks, fifteen Jupyter notebooks, eight mock exams, and the course datasets.
</p>

<p align="center">
  <img alt="Based on ISLP (Springer 2023)" src="docs/badges/based-on-islp.svg">
  <img alt="Python 3.9+" src="docs/badges/python.svg">
  <img alt="Jupyter notebooks" src="docs/badges/jupyter.svg">
  <img alt="Slides: LaTeX Beamer" src="docs/badges/slides.svg">
  <a href="#-lab-notebooks"><img alt="Open in Colab" src="docs/badges/colab.svg"></a>
  <a href="https://chrisw09.github.io/Quantitative-Research-Methods/"><img alt="Documentation" src="https://img.shields.io/badge/docs-online-2ea44f"></a>
</p>

<p align="center">
  <b>1027 core slides</b> (+139 in optional appendices) ·
  <b>127 exercises</b> with worked solutions ·
  <b>12 labs</b> + 3 code references, all running locally &amp; on Colab ·
  <b>3 + 5 mock exams</b> · <b>22 datasets</b>
</p>

<p align="center">
  <b>📖 Read it online: <a href="https://chrisw09.github.io/Quantitative-Research-Methods/">chrisw09.github.io/Quantitative-Research-Methods</a></b>
</p>

> **These materials are based on the textbook** *An Introduction to Statistical
> Learning, with Applications in Python* (James, Witten, Hastie, Tibshirani &
> Taylor, Springer 2023 — "ISLP"). The course structure, topics, notation and
> labs follow the book; please cite it if you reuse these materials
> (see [Citation & licence](#-citation--licence)).

Prepared by **Prof. Dr. Christoph Weisser** (HSBI — Bielefeld University of
Applied Sciences and Arts), Summer Semester 2026.

---

## Start here

| | Where to go | What you get |
|:--:|---|---|
| 🎓 | **Learning it** — [read a deck](#-lecture-slides), then [run its lab](#-lab-notebooks) | The compiled PDFs need no toolchain; every notebook opens in Colab with one click and resolves its own data. |
| 👩‍🏫 | **Teaching it** — [the teaching guide](#-teaching-it) | A thirteen-week plan, per-session runsheets with timings and cut lists, a generated slide index, and one `make` command that keeps them in sync with the decks. |
| 🛠️ | **Adapting it** — [repository layout](#-repository-layout) | LaTeX sources for every deck and exam, figures regenerated from the datasets by script, and a pinned Python environment. |

### What's inside

| Material | Count | Notes |
|---|---|---|
| [Lecture decks](#-lecture-slides) | 12 | Ten ISLP chapters + a two-part precourse · 1027 slides, plus 139 in per-deck appendices |
| Exercises | 86 short + 41 extended | Each with a full worked solution, tagged [Concept] / [Math] / [Python] / [Integrative] |
| [Lab notebooks](#-lab-notebooks) | 12 + 3 | Twelve taught labs, each paired with a deck and carrying worked solutions · three untaught **code references** (SVM, survival, unsupervised): no deck, no solutions |
| [Mock exams](#-mock-exams) | 3 | Each as questions, worked solutions and an in-class review deck — kept out of git |
| [Datasets](#-python-environment--datasets) | 22 CSVs | From [statlearning.com](https://www.statlearning.com), resolved automatically via `ISLP` |
| [Teaching guide](#-teaching-it) | 1 kit | Semester plan, runsheets, slide index, before-class checklist, printable handouts |

---

## 🚀 Quick start

You don't need to install anything to *read* the slides — the compiled PDFs live
right in the repo. To *run* a lab, **start in Colab**; install locally later,
once the course is under way.

### ▶︎ Day one: Google Colab — nothing to install

This is the route to use in the first session and the one to point a cohort at.
Open any notebook from the [lab table](#-lab-notebooks) in your browser; nothing
to install and nothing to debug on a projector. The first cell detects Colab,
installs the few missing packages (`ISLP`, plus `pygam`/`xgboost`/`lifelines`
where a chapter needs them; `torch` is preinstalled), and resolves the data
automatically. A Google account is enough — no account on this repository is
needed, and Colab runs every lab in the course, including the Chapter 10 deep
learning lab.

### ⌥ Week two: a local virtual environment

Faster, works offline, keeps your edits, and what you want for any serious piece
of work — but not a first-session activity. The install pulls in **around 150
packages and several hundred megabytes**, because the book companion package
`ISLP` *hard-requires* `torch` (along with `pytorch_lightning` and
`torchmetrics`): on Windows `torch` alone is over 100 MB, and on Linux the wheel
bundles the CUDA libraries and is several times larger again. Removing `torch`
from `requirements.txt` does not help — `pip` reinstates it as an `ISLP`
dependency. Set aside time for it outside class.

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab Chapters/chapter_03/chapter_03_lab.ipynb
```

Tested with **Python 3.9+**. Data loads via the `ISLP` package when installed,
falling back to the bundled `ALL CSV FILES - 2nd Edition/` folder, so it also
works offline.

---

## 📚 The course at a glance

A 13-session semester (13 × 180 min), **6 ECTS**, graded by a single 120-minute
written exam at the end. The precourse is **taught** in the session that opens
the semester; the twelve chapter lectures keep their numbers, which is what the
exam calendar and the runsheets refer to.

| Session | Chapter | Topic |
|:--:|:--:|--|
| **Precourse** | 0 + 0b | **Taught in one session**, from both precourse decks: descriptive statistics, probability, distributions, inference, simple regression, Python — and reading notation, logs & exponentials, odds & the logit, likelihood and MLE, counting & cost. 157 slides across the two, so the session is a selection and the decks stay the reference |
| 1 | 1 + 2 (part 1) | Introduction; what is statistical learning; prediction vs. inference |
| 2 | 2 (part 2) | Model accuracy; bias–variance trade-off; Bayes classifier; KNN |
| 3–4 | 3 | Linear regression: estimation, inference, dummies, interactions, diagnostics |
| 5–6 | 4 | Classification: logistic regression, the confusion matrix, ROC/AUC (LDA/QDA, naive Bayes and Poisson are in the appendix) |
| 7 | 5 | Resampling: validation set, k-fold CV, LOOCV, bootstrap |
| 8 | 6 | Model selection & regularization: subset selection, ridge, lasso, PCR/PLS |
| 9 | 7 | Beyond linearity: polynomials, splines, smoothing splines, GAMs |
| 10 | 8 | Tree-based methods: trees, bagging, random forests, boosting |
| 11 | 10 | Deep learning: MLPs, CNNs, training, regularization (PyTorch) |
| 12 | 13 | Multiple testing: FWER, Bonferroni/Holm, FDR, Benjamini–Hochberg |

Chapters 2, 3 and 4 each span two lectures, breaking where a session can end
cleanly: Ch 2 after "regression vs. classification" (p. 42), so accuracy,
bias–variance and KNN open Lecture 2; Ch 3 after multiple regression and the
four questions (p. 76); Ch 4 after the logistic-regression section (p. 42), so
evaluation and the lab open Lecture 6.

> Chapters **9 (SVM), 11 (Survival) and 12 (Unsupervised)** aren't part of the
> 12-lecture plan and have **no lecture deck**. They ship only as **code
> references**: notebooks that show how to run the methods in Python, to be read
> alongside the ISLP chapter, which does the teaching. They also ship **without
> worked solutions** — unlike the twelve taught labs, their closing exercises are
> left unanswered.

---

## 🎞️ Lecture slides

Twelve decks in `Chapters/chapter_NN/`, each folder self-contained
(`chapter_NN.tex`, its `images/`, the compiled PDF — and the chapter's
[companion lab](#-lab-notebooks), so everything for one week sits in one place).
Slide counts are given
as **main flow (+ appendix)**: every deck ends with an appendix of optional,
advanced material that the main thread never depends on.

<p align="center">
  <img alt="Four slides from the Chapter 3 deck: a figure computed from the course data with a takeaway box, a worked example with real numbers, an exercise prompt, and its worked solution." src="docs/_static/deck-preview.png" width="820">
  <br><sub>Chapter 3: a computed figure with its takeaway, a worked example, an in-deck exercise, and the solution that follows it.</sub>
</p>

| Ch. | Deck | What it covers | Exercises | Slides | PDF |
|:--:|---|---|:--:|:--:|:--:|
| 0 | Precourse (a) — Statistics refresher *(optional)* | Descriptive statistics, probability and Bayes, distributions, standard errors and CIs, testing and power, simple regression, the Python toolkit | 10 + 4 | 106 (+16) | [PDF](./Chapters/chapter_00/chapter_00.pdf) |
| 0b | Precourse (b) — Toolkit *(optional)* | Reading notation, logs and exponentials, odds and the logit, likelihood, computational cost, the Python patterns the labs use | 6 + 2 | 51 (+9) | [PDF](./Chapters/chapter_00b/chapter_00b.pdf) |
| 1 | Introduction | What statistical learning is, prediction vs. inference, the three motivating data sets, notation and the design matrix | 3 + 1 | 71 (+6) | [PDF](./Chapters/chapter_01/chapter_01.pdf) |
| 2 | Statistical Learning | Estimating *f*, parametric vs. nonparametric, the flexibility trade-off, training vs. test error, bias–variance, Bayes classifier and KNN | 8 + 4 | 107 (+8) | [PDF](./Chapters/chapter_02/chapter_02.pdf) |
| 3 | Linear Regression | Least squares, standard errors and *t*/*F* inference, confidence vs. prediction intervals, dummies and interactions, the four diagnostics | 12 + 6 | 144 (+11) | [PDF](./Chapters/chapter_03/chapter_03.pdf) |
| 4 | Classification | Logistic regression and the odds scale, confounding, confusion matrices, ROC and AUC — LDA, QDA and naive Bayes moved to the appendix | 10 + 6 | 82 (+43) | [PDF](./Chapters/chapter_04/chapter_04.pdf) |
| 5 | Resampling Methods | The validation set and why it wobbles, LOOCV, *k*-fold CV and the trade-off inside the estimate, CV pitfalls, the bootstrap | 6 + 3 | 79 (+7) | [PDF](./Chapters/chapter_05/chapter_05.pdf) |
| 6 | Model Selection & Regularization | Best subset and stepwise selection, Cₚ/AIC/BIC/adjusted R², ridge, the lasso and its sparsity, PCR, the *p* > *n* regime | 7 + 3 | 81 (+11) | [PDF](./Chapters/chapter_06/chapter_06.pdf) |
| 7 | Moving Beyond Linearity | Polynomials and step functions, regression splines and knots, natural splines, smoothing splines, LOESS, GAMs | 6 + 3 | 85 (+7) | [PDF](./Chapters/chapter_07/chapter_07.pdf) |
| 8 | Tree-Based Methods | Recursive binary splitting, pruning, impurity measures, bagging and out-of-bag error, random forests, boosting | 7 + 3 | 83 (+7) | [PDF](./Chapters/chapter_08/chapter_08.pdf) |
| 10 | Deep Learning | Single-layer networks and activations, MLPs and parameter counts, convolutions and pooling, loss and SGD, regularisation | 6 + 3 | 75 (+8) | [PDF](./Chapters/chapter_10/chapter_10.pdf) |
| 13 | Multiple Testing | Why naive testing fails at scale, FWER, Bonferroni and Holm, the false discovery rate, Benjamini–Hochberg, *p*-hacking | 5 + 3 | 63 (+6) | [PDF](./Chapters/chapter_13/chapter_13.pdf) |
| **Total** | | | **86 + 41** | **1027 (+139)** | |

<details>
<summary><b>How a deck is built</b></summary>

1. **Front matter** — course-at-a-glance, chapter contents, and a "Notation in
   this chapter" symbol table.
2. **Teaching flow** — motivation → intuition → formal definition → worked
   example → interpretation, with colour-coded callout boxes: 🟩 takeaway,
   🟦 how-to-read-this, 🟧 worked example, 🟥 pitfall, 🟪 short exercise (🟩 teal
   solution), 🟣 extended exercise, 🩵 "switch to the notebook now".
3. **Exercises** — one short exercise every ~20 minutes and one extended
   exercise every ~45 minutes, each tagged **[Concept] / [Math] / [Python]**
   (short) or **[Math] / [Python] / [Integrative]** (extended). Every prompt is
   followed by its full solution; long ones run across a `(1/2)` / `(2/2)` pair.
4. **Closing summary** — chapter-in-one-slide, key formulas at a glance,
   vocabulary, decision rules and common pitfalls.
5. **Appendix** — the optional, advanced material, opened by a slide that says
   what is in it and why each item is optional.

Throughout: **~100 purpose-built visuals** (65 matplotlib plots computed from
the real course datasets + 39 native TikZ diagrams), commented Python on every
listing, and numeric answers reproduced against the real data.
</details>

<details>
<summary><b>What each appendix holds</b></summary>

The appendix sits outside the timed plan: the runsheets stop where it begins and
the slide index marks it *optional*. Every exercise there keeps its full
solution, so it works as homework.

| Ch. | In its appendix | Pages |
|:--:|---|:--:|
| 0 | χ²/*t*/*F* and LLN vs. CLT · the ANOVA decomposition · linear algebra (with Exercise 0.8) · calculus and gradient descent (with Extended Exercise 0.3) | 16 |
| 0b | least squares as maximum likelihood (with Extended Exercise 0b.1) · counting and the 2ᵖ cost (with Exercise 0b.5) | 9 |
| 1 | the design matrix entry by entry · the two dataset lookup tables | 6 |
| 2 | Extended Exercise 2.1 (bias–variance from first principles) · Extended Exercise 2.3 (the Bayes boundary for two Gaussians) | 8 |
| 3 | squared vs. absolute loss · Extended Exercise 3.L2 (deriving least squares) · the matrix form of multiple regression · Extended Exercise 3.L6 (linear vs. polynomial vs. KNN) | 11 |
| 4 | how logistic regression is actually fitted (deviance, IRLS) · the multinomial softmax · Extended Exercise 4.2 (LDA from Bayes' theorem) · Extended Exercise 4.3 (naive Bayes by hand) · GLMs and Poisson regression | 15 |
| 5 | Exercise 5.2 and Extended Exercise 5.1 — the LOOCV leverage-shortcut drills | 7 |
| 6 | the constraint geometry redrawn · Exercise 6.1 (counting models) · Extended Exercise 6.2 (orthonormal design, soft thresholding) · partial least squares with Exercise 6.6 | 11 |
| 7 | the truncated-power basis and the constraint count · Extended Exercise 7.1 (regression splines by hand) | 7 |
| 8 | the partition picture redrawn · Extended Exercise 8.2 (impurity measures and pruning) · BART | 7 |
| 10 | Extended Exercise 10.2 (CNN architecture arithmetic) · transformers · backpropagation · double descent | 8 |
| 13 | the four outcomes drawn · resampling-based inference · post-selection inference | 6 |
</details>

<details>
<summary><b>The two precourse decks</b></summary>

**Chapter 0 — the statistics refresher.** An optional session (106 slides plus a
16-slide appendix) revisiting what the course assumes: descriptive statistics,
probability and Bayes, the standard distributions, sampling and confidence
intervals, hypothesis testing, simple linear regression, and the
`numpy`/`pandas` toolkit; the matrix algebra and the calculus/gradient-descent
strands sit in its appendix. It opens with a twelve-question self-check so
students can decide whether they need it, and closes with a table mapping every
topic to the chapter that uses it. Eighteen figures — Anscombe's quartet,
Simpson's paradox, the CLT, CI coverage, power, gradient descent — are computed
from the course data by
[`make_figures.py`](./Chapters/chapter_00/make_figures.py); the companion
notebook is [`chapter_00_lab.ipynb`](./Chapters/chapter_00/chapter_00_lab.ipynb).

**Chapter 0b — the toolkit.** A second optional session covering what the later
chapters use but never explain, chosen by counting actual usage across the ten
lecture decks: reading notation (Σ, Π, arg max, indicators, sets — 180 uses),
logs and exponentials (176), odds and the logit (108), likelihood and maximum
likelihood (37), counting and the 2ᵖ cost (13), and the Python patterns every
lab relies on (functions, loops, seeds, `fit`/`predict`, train/test discipline).
Companion notebook:
[`chapter_00b_lab.ipynb`](./Chapters/chapter_00b/chapter_00b_lab.ipynb).
</details>

<details>
<summary><b>Rebuilding a deck</b></summary>

Requires a TeX Live distribution (with `beamer`, `tcolorbox`, `tikz`,
`listings`, `booktabs`):

```bash
cd Chapters/chapter_NN
pdflatex chapter_NN.tex
pdflatex chapter_NN.tex   # second pass for the navigation bar
```

Or run `make` from the repository root: it rebuilds only what changed and
refreshes the slide index.
</details>

---

## 📓 Lab notebooks

Fifteen notebooks, each beside the deck it accompanies at
`Chapters/chapter_NN/chapter_NN_lab.ipynb`: **twelve taught labs**, one per deck
(both precourse sessions included), each ending in worked Python solutions to
that chapter's exercises — plus **three code references** for the untaught
chapters, which have no deck and no solutions (see below). Each runs
**locally or on Google Colab**; data loads via the `ISLP` package with an
automatic fallback to the bundled CSVs, so nothing needs downloading by hand.

| Ch. | Lab | Open in Colab |
|:--:|--|:--:|
| 0 · Precourse (a) — Statistics | `chapter_00_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_00/chapter_00_lab.ipynb) |
| 0b · Precourse (b) — Toolkit | `chapter_00b_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_00b/chapter_00b_lab.ipynb) |
| 1 · Introduction | `chapter_01_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_01/chapter_01_lab.ipynb) |
| 2 · Statistical Learning | `chapter_02_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_02/chapter_02_lab.ipynb) |
| 3 · Linear Regression | `chapter_03_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_03/chapter_03_lab.ipynb) |
| 4 · Classification | `chapter_04_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_04/chapter_04_lab.ipynb) |
| 5 · Resampling Methods | `chapter_05_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_05/chapter_05_lab.ipynb) |
| 6 · Model Selection & Regularization | `chapter_06_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_06/chapter_06_lab.ipynb) |
| 7 · Moving Beyond Linearity | `chapter_07_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_07/chapter_07_lab.ipynb) |
| 8 · Tree-Based Methods | `chapter_08_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_08/chapter_08_lab.ipynb) |
| 10 · Deep Learning | `chapter_10_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_10/chapter_10_lab.ipynb) |
| 13 · Multiple Testing | `chapter_13_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_13/chapter_13_lab.ipynb) |

**Code references — no lecture deck, no worked solutions.** Read the ISLP
chapter first; these three notebooks show how to run the methods in Python, they
do not teach the ideas.

| Ch. | Code reference | Open in Colab |
|:--:|--|:--:|
| 9 | `chapter_09_lab.ipynb` — Support Vector Machines | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_09/chapter_09_lab.ipynb) |
| 11 | `chapter_11_lab.ipynb` — Survival Analysis | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_11/chapter_11_lab.ipynb) |
| 12 | `chapter_12_lab.ipynb` — Unsupervised Learning | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_12/chapter_12_lab.ipynb) |

Every notebook is also
[rendered in full](https://chrisw09.github.io/Quantitative-Research-Methods/labs.html)
on the documentation site, stored outputs included.

---

## 👩‍🏫 Teaching it

[`Teaching_Guide/`](./Teaching_Guide/) holds what you need to walk into a room:

| File | What it is |
|---|---|
| [`semester_plan.md`](./Teaching_Guide/semester_plan.md) | The thirteen weeks on one page, the three split points, and what to sacrifice when you fall behind |
| [`slide_index.md`](./Teaching_Guide/slide_index.md) | Generated from the PDFs: every section with its page range and time budget, every exercise and solution with its page |
| [`before_class.md`](./Teaching_Guide/before_class.md) | The ten-minute checklist for the evening before and the morning of |
| `runsheets/` | One page per session — timings, what to run live, what to cut, what students get wrong. Git-ignored: they map exercises onto exam problems |
| `handouts/` | Printable two-up PDFs of every deck (`make handouts`) |

Runsheet timings cover the **main flow** of a deck; appendix pages are material
to assign, not to teach.

```bash
make            # figures, any deck whose source changed, and the slide index
make check      # page counts, and any slide that overruns its frame
make handouts   # printable 2-up PDFs of every deck
make help       # the rest
```

---

## 📝 Mock exams

Three practice exams matched to the course rhythm, each built from a single
LaTeX source so the paper and its solutions can never diverge. All numeric
answers were verified programmatically. Each ships in three formats:
**questions**, **worked solutions**, and a **Beamer deck** for reviewing the
exam in class.

| Exam | After | Covers | Format |
|--|:--:|--|:--:|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min · 90 pts |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Final Mock Exam | Lecture 12 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |

The final exam also exists in three parallel versions (A / B / C) — same
structure and difficulty, different numbers.

Alongside them, **five 60-minute short exams** (A–E, three problems × 20 points)
form the formative layer, released one at a time as the material each needs is
taught — A after Lecture 6 (Ch 4), B after 7 (Ch 5), C after 8 (Ch 6), D after 10
(Ch 8), E after 12 (Ch 13). They are the papers to give a student who has fallen
behind, and the only ones carrying grading keys and marking tables. They live in
`Mock_Exams/Short_Exams_60min/` and build with their own `./build.sh`, not
`make exams`.

> 🔒 **Not distributed here.** The exams, their solutions and their LaTeX
> sources are assessment material and are deliberately kept out of this
> repository (see [`.gitignore`](./.gitignore)). Instructors can request them
> from the author at [info@profweisser-ai.de](mailto:info@profweisser-ai.de).

---

## 🧭 Advanced modules

Four **optional, self-study** modules extend the course beyond ISLP — same
house style as the twelve decks (every exercise followed by its worked
solution, closing summary, optional appendix), each paired with a companion
notebook whose numbers match the slides seed-for-seed:

| Module | Title | Deck | Notebook |
|:--:|---|:--:|:--:|
| A1 | Randomised Controlled Trials — potential outcomes, selection bias, power, peeking | 71 slides | [`advanced_01_rcts_lab.ipynb`](./Chapters/Advanced/advanced_01_rcts/advanced_01_rcts_lab.ipynb) |
| A2 | Explainable AI with Shapley Values — axioms, exact and Monte-Carlo Shapley, pitfalls | 73 slides | [`advanced_02_shapley_lab.ipynb`](./Chapters/Advanced/advanced_02_shapley/advanced_02_shapley_lab.ipynb) |
| A3 | Conformal Prediction — split conformal, CQR, prediction sets, the OLS stress test | 74 slides | [`advanced_03_conformal_lab.ipynb`](./Chapters/Advanced/advanced_03_conformal/advanced_03_conformal_lab.ipynb) |
| A4 | GLMs and Splines — exponential family, overdispersion, penalized splines, a count GAM | 82 slides | [`advanced_04_glms_splines_lab.ipynb`](./Chapters/Advanced/advanced_04_glms_splines/advanced_04_glms_splines_lab.ipynb) |

Nothing in the twelve-lecture plan or the exams depends on them — see the
[module guide](./Chapters/Advanced/README.md) for prerequisites and build instructions;
`make advanced` rebuilds the decks.

---

## 🎯 Short projects

Six **3–5 hour challenges** in [`Projects/`](./Projects/) where students take a
real decision on real data. Unlike the labs, there is no worked solution: each
brief poses a problem someone actually has, fixes a seeded held-out test set,
gives a baseline to beat, and asks for a **one-page memo with specific numbers**.

| # | Project | The decision | Data | After |
|:--:|---|---|:--:|:--:|
| 1 | Who should we call? | A ranked shortlist of 500 prospects, and how many policies it sells | `Caravan` | Lecture 7 |
| 2 | Five numbers or seventeen? | Whether a board-readable five-variable model is defensible | `College` | Lecture 8 |
| 3 | Can you predict the market? | Whether a fund should trade on last week's returns | `Weekly` | Lecture 7 |
| 4 | A model the brand manager can read | Accuracy versus explainability, and which to deploy | `OJ` | Lecture 10 |
| 5 | What is it worth, and how sure are you? | Five valuations, each with a defensible interval | `Boston` | Lecture 9 |
| 6 | How many managers can actually pick stocks? | One number for a pension trustee — possibly zero | `Fund` | Lecture 12 |

Each has a trap the brief does not reveal, and in several of them **"this cannot
be predicted well enough to act on" is a correct answer**. The projects are
formative — the module is graded by the written exam — and each folder carries a
`SOLUTION_NOTES.md` with expected findings and a marking guide.

---

## 🗂️ Repository layout

| Path | Contents |
|---|---|
| [`Chapters/`](./Chapters/) | **One folder per chapter, holding its deck and its lab together**: `chapter_NN/` contains `chapter_NN.tex`, the compiled `.pdf`, `images/`, and `chapter_NN_lab.ipynb`. Twelve decks and fifteen notebooks — chapters 9, 11 and 12 are notebook-only code references. See its [deck guide](./Chapters/README.md). |
| [`Chapters/Advanced/`](./Chapters/Advanced/) | Four optional self-study modules — RCTs, Shapley values, conformal prediction, GLMs & splines — each a full deck plus companion notebook. See its [module guide](./Chapters/Advanced/README.md). |
| [`Projects/`](./Projects/) | Six short projects (3–5 h): a real decision on real data, with a fixed held-out set, a baseline to beat and a one-page memo as the deliverable. See its [project guide](./Projects/README.md). |
| [`Teaching_Guide/`](./Teaching_Guide/) | Instructor material: semester plan, runsheets, slide index, before-class checklist, printable handouts |
| [`ALL CSV FILES - 2nd Edition/`](./ALL%20CSV%20FILES%20-%202nd%20Edition/) | Course datasets (from [statlearning.com](https://www.statlearning.com)) |
| [`Makefile`](./Makefile) | One-command rebuild of figures, decks, handouts and the index |
| [`docs/`](./docs/) | Sphinx documentation for the whole course — see [Documentation](#-documentation) |
| [`requirements.txt`](./requirements.txt) | Pinned Python environment for the notebooks |
| `Mock_Exams/` | Three exams plus three parallel variants of the final, and five 60-min exams (questions, solutions, review decks) — **excluded from git**: assessment material. `make exams` builds the first group; `Short_Exams_60min/build.sh` the second |
| `Source_Material/` | Copyrighted textbook PDF & figure banks — **excluded from git** (see [`.gitignore`](./.gitignore)) |

---

## 🐍 Python environment & datasets

[`requirements.txt`](./requirements.txt) pins the packages used by the notebooks
and the in-slide code examples:

| Purpose | Packages |
|---|---|
| Core scientific stack | `numpy` · `pandas` · `matplotlib` · `scipy` |
| Statistics & ML | `statsmodels` · `scikit-learn` |
| Book companion (datasets + helpers) | `ISLP` |
| Chapter-specific | `pygam` (Ch 7) · `xgboost` (Ch 8, optional) · `torch` (Ch 10) · `lifelines` (Ch 11) |
| Notebook environment | `jupyter` |

The datasets live in
[`ALL CSV FILES - 2nd Edition/`](./ALL%20CSV%20FILES%20-%202nd%20Edition/) and are
distributed by the textbook authors at
[statlearning.com](https://www.statlearning.com) for use with the book. In the
notebooks, **datasets load straight from the `ISLP` package wherever possible**;
the four the package does not ship (`Advertising`, `Heart`, `Income1`,
`Income2`) stream from the book's official site, and the bundled CSVs act as an
offline fallback. The decks attribute every book
figure to its source.

---

## 📖 Documentation

**📖 <https://chrisw09.github.io/Quantitative-Research-Methods/>**

Everything above — the lecture plan, the decks, all fifteen labs rendered in
full, the teaching guide, the exams and the datasets — is published as a
browsable site. It is **built and published by hand** — the repository carries
no CI — so after changing the materials, rebuild and deploy it (see
[Building the docs](https://chrisw09.github.io/Quantitative-Research-Methods/building-docs.html)).

To build it locally from [`docs/`](./docs/):

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html          # Linux: xdg-open
```

The build stages the notebooks and the deck PDFs into the site automatically, so
the generated `docs/_build/html/` folder is self-contained. Details, including
how the deployment works, are in
[`docs/building-docs.md`](./docs/building-docs.md).

---

## 👤 About

I am Christoph Weisser, Professor of Mathematics, specializing in Business Data
Science at Hochschule Bielefeld (HSBI), and former Technical Lead Analytics &
Artificial Intelligence at BASF. My work focuses on Artificial Intelligence,
Generative AI, Business Data Science, and agentic AI systems that bridge research
with real-world industrial applications.

Before joining academia, I led international AI initiatives at BASF from strategy
through production deployment. Today, I combine research, teaching, open-source
software development, and selected industry collaborations to advance the
practical application of AI.

I hold two master’s degrees from the University of Oxford and the University of
St Andrews and completed the PhD Program in Applied Statistics & Empirical
Methods (summa cum laude) at Georg-August-Universität Göttingen. I was awarded
scholarships by the Studienstiftung des deutschen Volkes, the
Konrad-Adenauer-Stiftung, and the Evangelisches Studienwerk Villigst. I
regularly publish research in leading journals and at international conferences
and contribute to open-source software.

---

## 📄 Citation & licence

The **Quantitative Research Methods** course materials are based on, and follow
the structure of, the textbook *An Introduction to Statistical Learning, with
Applications in Python*. If you reuse them, please cite the source textbook:

> James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J. (2023).
> *An Introduction to Statistical Learning, with Applications in Python.*
> Springer Texts in Statistics. Springer. <https://www.statlearning.com>

BibTeX:

```bibtex
@book{islp2023,
  title     = {An Introduction to Statistical Learning: with Applications in Python},
  author    = {James, Gareth and Witten, Daniela and Hastie, Trevor and Tibshirani, Robert and Taylor, Jonathan},
  year      = {2023},
  publisher = {Springer},
  series    = {Springer Texts in Statistics},
  isbn      = {978-3-031-38746-3},
  doi       = {10.1007/978-3-031-38747-0},
  url       = {https://www.statlearning.com}
}
```

**Attribution.** The slides, exercises, mock exams and notebooks in this
repository were prepared by Prof. Dr. Christoph Weisser (HSBI), Summer Semester
2026. The ISLP textbook, its text and its figures are © the authors / Springer;
the datasets are distributed by the authors at
[statlearning.com](https://www.statlearning.com) for use with the book. The
copyrighted textbook PDF and figure banks are **not** included in this
repository (see [`.gitignore`](./.gitignore)).

<p align="center"><sub>Happy teaching 🎓</sub></p>

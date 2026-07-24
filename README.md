<h1 align="center">Quantitative Research Methods</h1>

<p align="center">
  A complete, ready-to-teach university course in statistical learning —<br>
  twelve polished slide decks, fifteen Jupyter labs, three mock exams, and the course datasets.
</p>

<p align="center">
  <img alt="Based on ISLP (Springer 2023)" src="docs/badges/based-on-islp.svg">
  <img alt="Python 3.9+" src="docs/badges/python.svg">
  <img alt="Jupyter notebooks" src="docs/badges/jupyter.svg">
  <img alt="Slides: LaTeX Beamer" src="docs/badges/slides.svg">
  <a href="#-open-any-notebook-in-colab"><img alt="Open in Colab" src="docs/badges/colab.svg"></a>
  <a href="https://chrisw09.github.io/Quantitative-Research-Methods/"><img alt="Documentation" src="https://img.shields.io/badge/docs-online-2ea44f"></a>
</p>

<p align="center">
  <b>12 Beamer decks · 15 Jupyter labs · 3 mock exams · ~127 exercises with worked solutions · runs locally &amp; on Colab</b>
</p>

<p align="center">
  <b>📖 Read it online: <a href="https://chrisw09.github.io/Quantitative-Research-Methods/">chrisw09.github.io/Quantitative-Research-Methods</a></b>
</p>

<p align="center">
  <a href="#-why-these-materials">⚡ Why</a> &nbsp;·&nbsp;
  <a href="#-quick-start">🚀 Quick start</a> &nbsp;·&nbsp;
  <a href="#-the-course-at-a-glance">📚 Course</a> &nbsp;·&nbsp;
  <a href="#-lecture-slides">🎞️ Slides</a> &nbsp;·&nbsp;
  <a href="#-lab-notebooks">📓 Labs</a> &nbsp;·&nbsp;
  <a href="#-mock-exams">📝 Exams</a> &nbsp;·&nbsp;
  <a href="#-open-any-notebook-in-colab">▶️ Colab</a> &nbsp;·&nbsp;
  <a href="#-about">👤 About</a>
</p>

> **These materials are based on the textbook** *An Introduction to Statistical
> Learning, with Applications in Python* (James, Witten, Hastie, Tibshirani &
> Taylor, Springer 2023 — "ISLP"). The course structure, topics, notation and
> labs follow the book; please cite it if you reuse these materials
> (see [Citation & licence](#-citation--licence)).

Prepared by **Prof. Dr. Christoph Weisser** (HSBI — Bielefeld University of
Applied Sciences and Arts).

---

## Contents

- [Why these materials](#-why-these-materials)
- [Quick start](#-quick-start)
- [The course at a glance](#-the-course-at-a-glance)
- [Repository layout](#-repository-layout)
- [Lecture slides](#-lecture-slides)
- [Lab notebooks](#-lab-notebooks)
- [Mock exams](#-mock-exams)
- [Python environment](#-python-environment)
- [Datasets](#-datasets)
- [Open any notebook in Colab](#-open-any-notebook-in-colab)
- [Documentation](#-documentation)
- [About](#-about)
- [Citation & licence](#-citation--licence)

---

## ⚡ Why these materials

- **A whole course, not a pile of files.** Twelve Beamer decks — ten chapters
  plus a two-part optional precourse — fifteen labs and three mock exams that
  share one notation, one dataset set, and one 12-week rhythm.
- **Slides built for the room.** Every deck moves motivation → intuition →
  formal definition → worked example, with colour-coded callout boxes and
  **~86 short + ~41 extended exercises**, each followed by a full solution. The
  hardest, optional material — formal derivations, side topics, the heaviest
  exercises — is parked in a **per-deck appendix**, so the main thread is
  ~1030 slides that fit the twelve sessions, with ~110 more behind them.
- **Numbers you can trust.** ~40 purpose-built visuals are computed from the
  real course datasets (not sketched), and every mock-exam answer was verified
  programmatically.
- **Labs that run anywhere.** Fifteen Jupyter notebooks run locally *and* on
  Google Colab — data loads from the `ISLP` package with an automatic fallback
  to the bundled CSVs, so a fresh Colab runtime just works.
- **Exam-ready.** Three practice exams matched to the course calendar, each in
  three formats (questions, worked solutions, and an in-class review deck) built
  from a single LaTeX source so paper and solutions can never diverge.
- **Reproducible by design.** LaTeX sources for every deck and exam, a pinned
  Python environment, and datasets that resolve automatically.

---

## 🚀 Quick start

You don't need to install anything to read the slides — the compiled PDFs live
right in the repo. To *run* a lab you have two options:

### ▶︎ Google Colab — zero setup *(recommended)*

Open any notebook in your browser; nothing to install. Every notebook's first
cell detects Colab, quietly installs the few missing packages (`ISLP`, plus
`pygam`/`xgboost`/`lifelines` where a chapter needs them; `torch` is
preinstalled on Colab), and resolves the data automatically — **12 of the 13
datasets load straight from the `ISLP` package**, and the one that isn't in
ISLP (`Advertising`) streams from the book's official site.

Jump to [**Open any notebook in Colab**](#-open-any-notebook-in-colab) for a
one-click link to all fifteen labs.

> 💡 The Colab links open straight from GitHub — no account on this repository
> is needed, only a Google account to run the notebook.

### ⌥ Local Jupyter

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab Lab_Notebooks/chapter_03_lab.ipynb
```

Tested with **Python 3.9+**. Data loads via the `ISLP` package when installed,
with an automatic fallback to the bundled `ALL CSV FILES - 2nd Edition/` folder.

---

## 📚 The course at a glance

A 12-lecture semester (12 × 180 min):

| Lecture | Chapter | Topic |
|:--:|:--:|--|
| 0 *(optional)* | — | **Precourse (a)**: descriptive statistics, probability, distributions, inference, simple regression, Python — matrix algebra and calculus in the appendix |
| 0b *(optional)* | — | **Precourse (b)**: reading notation, logs & exponentials, odds & the logit, likelihood and MLE, counting & cost, the Python patterns of the labs |
| 1 | 1 + 2 (part 1) | Introduction; what is statistical learning; prediction vs. inference |
| 2 | 2 (part 2) | Model accuracy; bias–variance trade-off; Bayes classifier; KNN |
| 3–4 | 3 | Linear regression: estimation, inference, dummies, interactions, diagnostics |
| 5–6 | 4 | Classification: logistic regression, LDA/QDA, naive Bayes, ROC, Poisson |
| 7 | 5 | Resampling: validation set, k-fold CV, LOOCV, bootstrap |
| 8 | 6 | Model selection & regularization: subset selection, ridge, lasso, PCR/PLS |
| 9 | 7 | Beyond linearity: polynomials, splines, smoothing splines, GAMs |
| 10 | 8 | Tree-based methods: trees, bagging, random forests, boosting |
| 11 | 10 | Deep learning: MLPs, CNNs, training, regularization (PyTorch) |
| 12 | 13 | Multiple testing: FWER, Bonferroni/Holm, FDR, Benjamini–Hochberg |

> Chapters **9 (SVM), 11 (Survival) and 12 (Unsupervised)** aren't part of the
> 12-lecture plan but ship as **self-study lab notebooks** for completeness.

---

## 🗂️ Repository layout

| Path | Contents |
|---|---|
| [`Lecture_Slides/`](./Lecture_Slides/) | Twelve Beamer decks (`chapter_NN/chapter_NN.tex` + `.pdf` + images) — the core deliverable, including the `chapter_00` precourse refresher. See its [deck guide](./Lecture_Slides/README.md). |
| [`Lab_Notebooks/`](./Lab_Notebooks/) | Fifteen Jupyter notebooks (`chapter_NN_lab.ipynb`), local- and Colab-ready |
| [`ALL CSV FILES - 2nd Edition/`](./ALL%20CSV%20FILES%20-%202nd%20Edition/) | Course datasets (from [statlearning.com](https://www.statlearning.com)) |
| [`Teaching_Guide/`](./Teaching_Guide/) | Instructor material: semester plan, per-session runsheets, slide index, printable handouts |
| [`Makefile`](./Makefile) | One-command rebuild of figures, decks, handouts and the index |
| [`docs/`](./docs/) | Sphinx documentation for the whole course — see [Documentation](#-documentation) |
| [`requirements.txt`](./requirements.txt) | Pinned Python environment for the notebooks |
| `Mock_Exams/` | Three exams (questions, solutions, review decks) — **excluded from git**: assessment material |
| `Source_Material/` | Copyrighted textbook PDF & figure banks — **excluded from git** (see [`.gitignore`](./.gitignore)) |

---

## 🎞️ Lecture slides

Twelve decks (`Lecture_Slides/chapter_NN/`) share a consistent teaching design:

- **Front matter** — course-at-a-glance, chapter contents, and a "Notation in
  this chapter" symbol table.
- **Teaching flow** — motivation → intuition → formal definition → worked
  example, with colour-coded callout boxes (green takeaway, blue how-to-read,
  orange worked example, red pitfall).
- **~86 short exercises** (~5 min) in purple boxes, each with a full
  step-by-step solution (teal), plus **~41 extended, multi-part exercises**
  (~15 min) in violet boxes with detailed multi-slide solutions.
- **~40 purpose-built visuals** — ≈22 matplotlib plots computed from the real
  course datasets plus ≈18 native TikZ concept diagrams.
- **Commented Python** on every code listing, and a cyan "Companion notebook"
  box marking exactly when to switch to the Jupyter lab.
- **Closing summary** — chapter-in-one-slide, key formulas, vocabulary,
  decision rules, and common pitfalls.
- **An appendix in every deck** — the optional, more advanced material sits
  behind the summary: formal derivations, the heaviest worked exercises, and
  side topics. It opens with a slide saying what is in it and *why* each item is
  optional, and the deck's Contents slide points at it. The main thread never
  depends on the appendix, so a session runs front to back and stops where the
  appendix begins: **1029 slides carry the course, 111 more are there when you
  want them.**

| Ch. | Deck | Short ex. | Extended ex. | Main flow | Appendix | Open |
|:--:|--|:--:|:--:|:--:|:--:|:--:|
| 0 | Precourse (a) — Statistics Refresher *(optional)* | 10 | 4 | 104 | +16 | [PDF](./Lecture_Slides/chapter_00/chapter_00.pdf) |
| 0b | Precourse (b) — Toolkit *(optional)* | 6 | 2 | 48 | +9 | [PDF](./Lecture_Slides/chapter_00b/chapter_00b.pdf) |
| 1 | Introduction | 3 | 1 | 68 | +6 | [PDF](./Lecture_Slides/chapter_01/chapter_01.pdf) |
| 2 | Statistical Learning | 8 | 4 | 105 | +8 | [PDF](./Lecture_Slides/chapter_02/chapter_02.pdf) |
| 3 | Linear Regression | 12 | 6 | 142 | +11 | [PDF](./Lecture_Slides/chapter_03/chapter_03.pdf) |
| 4 | Classification | 10 | 6 | 110 | +15 | [PDF](./Lecture_Slides/chapter_04/chapter_04.pdf) |
| 5 | Resampling Methods | 6 | 3 | 77 | +7 | [PDF](./Lecture_Slides/chapter_05/chapter_05.pdf) |
| 6 | Linear Model Selection & Regularization | 7 | 3 | 79 | +11 | [PDF](./Lecture_Slides/chapter_06/chapter_06.pdf) |
| 7 | Moving Beyond Linearity | 6 | 3 | 83 | +7 | [PDF](./Lecture_Slides/chapter_07/chapter_07.pdf) |
| 8 | Tree-Based Methods | 7 | 3 | 81 | +7 | [PDF](./Lecture_Slides/chapter_08/chapter_08.pdf) |
| 10 | Deep Learning | 6 | 3 | 71 | +8 | [PDF](./Lecture_Slides/chapter_10/chapter_10.pdf) |
| 13 | Multiple Testing | 5 | 3 | 61 | +6 | [PDF](./Lecture_Slides/chapter_13/chapter_13.pdf) |
| **Total** | | **86** | **41** | **1029** | **+111** | |

<details>
<summary><b>What each appendix holds</b></summary>

Every deck ends with a signpost slide and then the optional material below.
Nothing in the main flow depends on it, and the per-session runsheets in
[`Teaching_Guide/`](./Teaching_Guide/) budget no time for it.

| Ch. | In its appendix | Pages |
|:--:|---|:--:|
| 0 | χ²/t/F and LLN vs. CLT · the ANOVA decomposition · linear algebra (with Exercise 0.8) · calculus and gradient descent (with Extended Exercise 0.3) | 16 |
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

> **New: a precourse refresher (Chapter 0).** An optional session — 104 slides
> plus a 16-slide appendix — that revisits the undergraduate material this
> course assumes: descriptive statistics, probability and Bayes, the standard
> distributions, sampling and confidence intervals, hypothesis testing, simple
> linear regression, and the `numpy`/`pandas` toolkit; the matrix algebra and
> the calculus/gradient-descent strands sit in its appendix, for the cohorts
> that need them.
> It opens with a twelve-question self-check so students can decide whether they
> need it, and closes with a table mapping every topic to the chapter that uses
> it. Eighteen figures — Anscombe's quartet, Simpson's paradox, the CLT, CI
> coverage, power, gradient descent — are computed from the course data by
> [`make_figures.py`](./Lecture_Slides/chapter_00/make_figures.py), and the
> whole session has a companion notebook,
> [`chapter_00_lab.ipynb`](./Lab_Notebooks/chapter_00_lab.ipynb).
>
> **Part (b), the toolkit (Chapter 0b).** A second optional session covering
> what the later chapters use but never explain — chosen by counting actual
> usage across the ten lecture decks: reading notation (Σ, Π, argmin,
> indicators, sets — 180 uses), logs and exponentials (176), odds and the logit
> (108), likelihood and maximum likelihood (37), counting and the 2ᵖ cost (13),
> and the Python patterns every lab relies on (functions, loops, seeds,
> `fit`/`predict`, train/test discipline). Also with a companion notebook,
> [`chapter_00b_lab.ipynb`](./Lab_Notebooks/chapter_00b_lab.ipynb).

<details>
<summary><b>Rebuilding a deck</b></summary>

Requires a TeX Live distribution (with `beamer`, `tcolorbox`, `tikz`,
`listings`, `booktabs`):

```bash
cd Lecture_Slides/chapter_NN
pdflatex chapter_NN.tex
pdflatex chapter_NN.tex   # second pass for the navigation bar
```
</details>

---

## 📓 Lab notebooks

Fifteen notebooks (`Lab_Notebooks/chapter_NN_lab.ipynb`) mirror each chapter's
Python Lab — including both precourse sessions and chapters 9, 11 and 12, which
are included for self-study.
Each notebook runs **locally or on Google Colab**; data loads via the `ISLP`
package with an automatic fallback to the bundled CSVs, so nothing needs
downloading by hand.

One-click Colab links for all fifteen are in
[**Open any notebook in Colab**](#-open-any-notebook-in-colab) below.

---

## 📝 Mock exams

Three practice exams matched to the course rhythm, each built from a single
LaTeX source so the paper and its solutions can never diverge. All numeric
answers were verified programmatically. Each exam ships in three formats:
**questions**, **worked solutions**, and a **Beamer deck** for reviewing the
exam in class.

> 🔒 **Not distributed here.** The exams, their solutions and their LaTeX
> sources are assessment material and are deliberately kept out of this
> repository (see [`.gitignore`](./.gitignore)). Instructors can request them
> from the author.

| Exam | After | Covers | Format |
|--|:--:|--|:--:|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min · 90 pts |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Final Mock Exam | Lecture 12 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |

The final exam also exists in three parallel versions (A / B / C) — same
structure and difficulty, different numbers.

---

## 👩‍🏫 Teaching it

[`Teaching_Guide/`](./Teaching_Guide/) holds what you need to walk into a room:
a [semester plan](./Teaching_Guide/semester_plan.md), a
[before-class checklist](./Teaching_Guide/before_class.md), a generated
[slide index](./Teaching_Guide/slide_index.md) (every section and exercise with
its page number, each appendix marked *optional*), and per-session runsheets
with timings, a cut-list for when you are behind, the exercises worth running
live, and the misconceptions to pre-empt. The runsheet timings cover the main
flow only — appendix pages are material to assign, not to teach.

Everything rebuilds with one command:

```bash
make            # figures, any deck whose source changed, and the slide index
make check      # page counts, and any slide that overruns its frame
make handouts   # printable 2-up PDFs of every deck
make help       # the rest
```

> The runsheets and the handouts are git-ignored: runsheets name which exercises
> map onto which exam problems, so they stay off the public repository alongside
> the exams themselves.

---

## 🐍 Python environment

[`requirements.txt`](./requirements.txt) pins the packages used by the
notebooks and the in-slide code examples:

| Purpose | Packages |
|---|---|
| Core scientific stack | `numpy` · `pandas` · `matplotlib` · `scipy` |
| Statistics & ML | `statsmodels` · `scikit-learn` |
| Book companion (datasets + helpers) | `ISLP` |
| Chapter-specific | `pygam` (Ch 7) · `xgboost` (Ch 8, optional) · `torch` (Ch 10) · `lifelines` (Ch 11) |
| Notebook environment | `jupyter` |

```bash
pip install -r requirements.txt
```

---

## 📊 Datasets

The course datasets live in [`ALL CSV FILES - 2nd Edition/`](./ALL%20CSV%20FILES%20-%202nd%20Edition/)
and are distributed by the textbook authors at
[statlearning.com](https://www.statlearning.com) for use with the book. In the
notebooks, **12 of the 13 datasets load straight from the `ISLP` package**; the
one that isn't in ISLP (`Advertising`) streams from the book's official site,
and the bundled CSVs act as an offline fallback. The slide decks attribute
every book figure to its source.

---

## ▶️ Open any notebook in Colab

Click a badge to open a lab in [Google Colab](https://colab.research.google.com/).
Nothing needs installing; a Google account is enough to run them.

### Lecture chapters

| Ch. | Lab | Open |
|:--:|--|:--:|
| 0 · Precourse (a) — Statistics | `chapter_00_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_00_lab.ipynb) |
| 0b · Precourse (b) — Toolkit | `chapter_00b_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_00b_lab.ipynb) |
| 1 · Introduction | `chapter_01_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_01_lab.ipynb) |
| 2 · Statistical Learning | `chapter_02_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_02_lab.ipynb) |
| 3 · Linear Regression | `chapter_03_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_03_lab.ipynb) |
| 4 · Classification | `chapter_04_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_04_lab.ipynb) |
| 5 · Resampling Methods | `chapter_05_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_05_lab.ipynb) |
| 6 · Model Selection & Regularization | `chapter_06_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_06_lab.ipynb) |
| 7 · Moving Beyond Linearity | `chapter_07_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_07_lab.ipynb) |
| 8 · Tree-Based Methods | `chapter_08_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_08_lab.ipynb) |
| 10 · Deep Learning | `chapter_10_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_10_lab.ipynb) |
| 13 · Multiple Testing | `chapter_13_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_13_lab.ipynb) |

### Self-study chapters

| Ch. | Lab | Open |
|:--:|--|:--:|
| 9 · Support Vector Machines | `chapter_09_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_09_lab.ipynb) |
| 11 · Survival Analysis | `chapter_11_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_11_lab.ipynb) |
| 12 · Unsupervised Learning | `chapter_12_lab.ipynb` | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_12_lab.ipynb) |

---

## 📖 Documentation

**📖 <https://chrisw09.github.io/Quantitative-Research-Methods/>**

Everything above — the lecture plan, the decks, all fifteen labs rendered in
full, the exams and the datasets — is published as a browsable site, rebuilt
automatically by [GitHub Actions](./.github/workflows/docs.yml) on every push to
`main` that touches the materials.

To build it locally from [`docs/`](./docs/):

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html          # Linux: xdg-open
```

The build stages the notebooks and the deck/exam PDFs into the site
automatically, so the generated `docs/_build/html/` folder is self-contained.
Details, including how the deployment works, are in
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

# An Introduction to Statistical Learning with Python — Lecture Materials

Complete teaching materials for a 12-lecture university course based on
*An Introduction to Statistical Learning, with Applications in Python*
(James, Witten, Hastie, Tibshirani & Taylor, Springer 2023 — "ISLP"),
prepared by **Prof. Dr. Christoph Weisser** (HSBI — Bielefeld University of
Applied Sciences and Arts).

The package contains ten polished Beamer slide decks with built-in exercises
and solutions, thirteen Jupyter lab notebooks that run locally **and on
Google Colab**, three mock exams with full solutions and in-class review
decks, and the course datasets.

---

## Repository structure

```
.
├── Lecture_Slides/                   Ten Beamer decks — the core deliverable
│   ├── chapter_01 … chapter_13/      chapter_NN.tex, chapter_NN.pdf, images/
│   └── README.md                     Deck guide: 12-lecture plan, exercise index
│
├── Lab_Notebooks/                    13 Jupyter notebooks (chapter_NN_lab.ipynb)
│                                     Run locally or on Google Colab (see below)
│
├── Mock_Exams/
│   ├── Exam_1_after_Lecture_04/      Ch 1–3   (90 min / 90 pts)
│   ├── Exam_2_after_Lecture_08/      Ch 4–6   (90 min / 90 pts)
│   └── Final_Exam_after_Lecture_12/  Comprehensive (120 min / 120 pts)
│                                     Each: exam PDF, solutions PDF, and a
│                                     Beamer solutions deck for in-class review
│
├── ALL CSV FILES - 2nd Edition/      Course datasets (from statlearning.com)
│
├── Source_Material/                  Textbook PDF + original figure banks
│                                     (NOT for public redistribution — see
│                                     "Publishing to GitHub" below)
│
├── requirements.txt                  Python environment for the notebooks
├── .gitignore
└── README.md                         This file
```

---

## The course at a glance (12 × 180 min)

| Lecture | Chapter | Topic |
|--:|--|--|
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

---

## The slide decks

Each deck (`Lecture_Slides/chapter_NN/`) follows a consistent teaching design:

- **Front matter:** course-at-a-glance overview, chapter table of contents, and
  a "Notation in this chapter" symbol table.
- **Teaching flow:** motivation → intuition → formal definition → worked
  example, with color-coded callout boxes (green takeaway, blue how-to-read,
  orange worked example, red pitfall).
- **70 short exercises** (~5 min, roughly every 20 minutes of lecture) in
  purple boxes, each followed by a full step-by-step solution (teal).
- **35 extended exercises** (~15 min, roughly every 45 minutes) in violet
  boxes — integrative multi-part problems with detailed multi-slide solutions.
- **~50 purpose-built visuals:** matplotlib plots computed from the real
  course datasets plus native TikZ concept diagrams — all numbers on these
  slides were generated, not sketched.
- **Commented Python:** every code listing carries line-by-line comments.
- **Lab signposts:** a cyan "Companion notebook" box marks exactly when to
  switch to the Jupyter notebook for a live demo.
- **Closing summary block:** chapter-in-one-slide, key formulas at a glance,
  vocabulary, decision rules, and common pitfalls.

### Rebuilding a deck

Requires a TeX Live distribution (with `beamer`, `tcolorbox`, `tikz`,
`listings`, `booktabs`):

```bash
cd Lecture_Slides/chapter_NN
pdflatex chapter_NN.tex
pdflatex chapter_NN.tex   # second pass for the navigation bar
```

---

## The lab notebooks

Thirteen notebooks (`Lab_Notebooks/chapter_NN_lab.ipynb`) mirror each
chapter's Python Lab section — including chapters 9, 11 and 12, which are not
part of the 12-lecture plan but are included for self-study.

### Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab Lab_Notebooks/chapter_03_lab.ipynb
```

Data loads via the `ISLP` package when installed, with automatic fallback to
the bundled `ALL CSV FILES - 2nd Edition/` folder.

### Run on Google Colab

Every notebook is Colab-ready. Its first cell detects Colab, quietly installs
any missing packages (`ISLP`, plus `pygam`/`xgboost`/`lifelines` where needed;
`torch` is preinstalled on Colab), and resolves the data automatically:
**12 of the 13 datasets load straight from the `ISLP` package**, and the one
that isn't in ISLP (`Advertising`) streams from the book's official site — so
the notebooks run on a fresh Colab runtime **even before this repo is public**.

**Open in Colab (one link per notebook):**

| Lecture chapter | Colab link | | Self-study | Colab link |
|--|--|--|--|--|
| 1 · Introduction | `…/chapter_01_lab.ipynb` | | 9 · SVM | `…/chapter_09_lab.ipynb` |
| 2 · Statistical Learning | `…/chapter_02_lab.ipynb` | | 11 · Survival | `…/chapter_11_lab.ipynb` |
| 3 · Linear Regression | `…/chapter_03_lab.ipynb` | | 12 · Unsupervised | `…/chapter_12_lab.ipynb` |
| 4 · Classification | `…/chapter_04_lab.ipynb` | | | |
| 5 · Resampling | `…/chapter_05_lab.ipynb` | | | |
| 6 · Model Selection | `…/chapter_06_lab.ipynb` | | | |
| 7 · Beyond Linearity | `…/chapter_07_lab.ipynb` | | | |
| 8 · Trees | `…/chapter_08_lab.ipynb` | | | |
| 10 · Deep Learning | `…/chapter_10_lab.ipynb` | | | |
| 13 · Multiple Testing | `…/chapter_13_lab.ipynb` | | | |

Each notebook also carries an **"Open in Colab" badge** in its first cell. The
full link format is:

```
https://colab.research.google.com/github/OWNER/REPO/blob/main/Lab_Notebooks/chapter_NN_lab.ipynb
```

**One-time setup after you create the GitHub repo** (the links use an `OWNER/REPO`
placeholder until then): from the repo root, replace the placeholder everywhere —

```bash
# macOS/BSD sed; use `sed -i` (no '') on Linux. Replace with your real path.
grep -rl 'OWNER/REPO' README.md Lab_Notebooks | \
  xargs sed -i '' 's#OWNER/REPO#your-github-user/your-repo#g'
```

That fixes the badge links, the README table, and the `GITHUB_RAW` data fallback
in every notebook in one step. The Colab badges then become clickable and open
each notebook directly from GitHub.

---

## Mock exams

Three practice exams matched to the course rhythm, each in three formats
built from a single LaTeX source (paper and solutions can never diverge):

| Exam | After | Covers | Format |
|--|--|--|--|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min / 90 pts |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min / 90 pts |
| Final Mock Exam | Lecture 12 | All chapters, weighted to Ch 7/8/10/13 | 120 min / 120 pts |

Per exam: `Mock_Exam_N.pdf` (questions only), `Mock_Exam_N_Solutions.pdf`
(worked solutions), and `Mock_Exam_N_Solutions_Slides.pdf` (Beamer deck for
reviewing the exam in class). All numeric answers were verified
programmatically. To rebuild:

```bash
cd Mock_Exams/Exam_1_after_Lecture_04
pdflatex -jobname=Mock_Exam_1 mock_exam_1.tex
pdflatex -jobname=Mock_Exam_1_Solutions "\def\withsolutions{1}\input{mock_exam_1.tex}"
```

---

## Python environment

`requirements.txt` pins the packages used by the notebooks and the in-slide
code examples: numpy, pandas, matplotlib, scipy, statsmodels, scikit-learn,
ISLP, pygam (ch 7), xgboost (ch 8, optional), torch (ch 10), lifelines
(ch 11), jupyter.

```bash
pip install -r requirements.txt
```

---

## Publishing to GitHub — read before pushing

- **`Source_Material/` must not be pushed to a public repository.** It
  contains the full textbook PDF and per-chapter PDFs, which are copyrighted
  Springer material. The provided `.gitignore` excludes it by default.
- The **datasets** are distributed by the authors at
  <https://www.statlearning.com> for use with the book; the slide decks
  attribute every book figure to its source.
- After pushing, set `GITHUB_RAW` in the notebooks (see above) and consider
  adding per-notebook "Open in Colab" badges:
  `https://colab.research.google.com/github/OWNER/REPO/blob/main/Lab_Notebooks/chapter_NN_lab.ipynb`.

---

## Citation

If you reuse these materials, please cite the source textbook:

> James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J. (2023).
> *An Introduction to Statistical Learning, with Applications in Python.*
> Springer. <https://www.statlearning.com>

Slides, exercises, exams and notebooks prepared by Prof. Dr. Christoph
Weisser (HSBI), Summer Semester 2026.

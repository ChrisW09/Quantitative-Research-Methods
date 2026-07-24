# The course at a glance

A 12-lecture semester (12 × 180 min) covering ten ISLP chapters, optionally
preceded by a two-part precourse: (a) a refresher of the undergraduate
statistics, and (b) the notation, algebra and Python the chapters assume.

:::{container} qrm-chips
**12** sessions × **180 min** · **2** optional precourse sessions ·
**3** decks split across two lectures · **3** mock exams
:::

## Semester plan

| Lecture | Chapter(s) | Content | Exercises |
|:--:|:--:|---|---|
| 0 *(optional)* | Ch 0 | **Precourse (a)**: descriptive statistics; probability and Bayes; distributions; standard errors and confidence intervals; hypothesis testing and power; simple linear regression; the Python toolkit — matrix algebra and gradients in the deck's appendix (with its own [lab notebook](labs.md)) | 0.1–0.10 |
| 0b *(optional)* | Ch 0b | **Precourse (b)**: reading mathematical notation; logs and exponentials; odds, the logit and the sigmoid; likelihood and maximum likelihood; counting and computational cost; the Python patterns the labs use (with its own [lab notebook](labs.md)) | 0b.1–0b.6 |
| 1 | Ch 1 + Ch 2 (part 1) | Introduction; what is statistical learning; prediction vs. inference; parametric vs. non-parametric | 1.1–1.3, 2.1–2.2 |
| 2 | Ch 2 (part 2) | Assessing accuracy; bias–variance trade-off; classification & KNN; lab | 2.3–2.8 |
| 3 | Ch 3 (part 1) | Simple & multiple linear regression; estimation; inference (SE, *t*, *F*) | 3.1–3.6 |
| 4 | Ch 3 (part 2) | Qualitative predictors; interactions; diagnostics; KNN vs. OLS; lab | 3.7–3.12 |
| 5 | Ch 4 (part 1) | Logistic regression; odds; multiple logistic regression; confounding | 4.1–4.4 |
| 6 | Ch 4 (part 2) | LDA, QDA, naive Bayes; confusion matrix; ROC/AUC; lab | 4.5–4.10 |
| 7 | Ch 5 | Validation set, LOOCV, *k*-fold CV, the bootstrap | 5.1–5.6 |
| 8 | Ch 6 | Subset selection; Cₚ/AIC/BIC; ridge; lasso; PCR/PLS | 6.1–6.7 |
| 9 | Ch 7 | Polynomials, step functions, splines, smoothing splines, GAMs | 7.1–7.6 |
| 10 | Ch 8 | Decision trees; bagging & OOB; random forests; boosting | 8.1–8.7 |
| 11 | Ch 10 | Neural nets; forward pass; backprop/GD; CNNs; regularization (PyTorch) | 10.1–10.6 |
| 12 | Ch 13 | Multiple testing; FWER; Bonferroni; Holm; FDR & Benjamini–Hochberg | 13.1–13.5 |

```{admonition} Split lectures
:class: tip

Chapters 2, 3 and 4 each span two lectures. The recommended stopping points are
a natural section boundary, so you can stop and resume cleanly:

- **Ch 2** — after the KNN / bias–variance material
- **Ch 3** — after "Goodness of fit / the four questions"
- **Ch 4** — after multiple logistic regression (before LDA)
```

## Self-study chapters

Chapters **9 (Support Vector Machines)**, **11 (Survival Analysis)** and
**12 (Unsupervised Learning)** are not part of the 12-lecture plan, but ship as
complete [lab notebooks](labs.md) for students who want them.

## Assessment rhythm

Three mock exams are matched to the calendar so students can self-test at the
natural checkpoints — see [Mock exams](exams.md). They are not distributed with
this repository.

Each deck also carries far more exercises than a session can run: the
[runsheets](teaching.md) name the two to four worth live time and leave the rest
as homework.

| Exam | Written after | Covers | Length |
|---|:--:|---|:--:|
| Mock Exam 1 | Lecture 4 | Chapters 1–3 | 90 min · 90 pts |
| Mock Exam 2 | Lecture 8 | Chapters 4–6 (+ light cumulative) | 90 min · 90 pts |
| Final Mock Exam | Lecture 12 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |

## Where to go next

- [Lecture slides](slides.md) — the deck for each week, and how a deck is built.
- [Teaching it](teaching.md) — runsheets, timings and the cut list.
- [Lab notebooks](labs.md) — the companion notebook for each chapter.

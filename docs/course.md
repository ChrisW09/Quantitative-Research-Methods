---
myst:
  html_meta:
    description: "The sixteen-session semester plan — a taught precourse session plus fifteen chapter lectures over thirteen ISLP chapters — with the recommended split points and the assessment calendar."
---

# The course at a glance

{.qrm-lead}
A 16-session semester (16 × 180 min), worth **6 ECTS**: one taught precourse
session covering both precourse decks, then fifteen chapter lectures over
thirteen ISLP chapters.

:::{container} qrm-chips
[**16** sessions × **180 min**]{.qrm-chip}
[**6** ECTS]{.qrm-chip}
[**1** taught precourse session]{.qrm-chip}
[**3** decks split across two lectures]{.qrm-chip}
[**3 + 5** practice exams]{.qrm-chip}
:::

## Semester plan

The precourse opens the semester as a **taught session**; the fifteen chapter
lectures run in ISLP order and keep their numbers 1–15, which is what the exam
calendar and the [runsheets](teaching.md) refer to.

| Session | Chapter(s) | Content | Exercises |
|:--:|:--:|---|---|
| **Precourse** | Ch 0 + Ch 0b | **Taught in one session**, drawing on both precourse decks: descriptive statistics; probability and Bayes; distributions; standard errors and confidence intervals; hypothesis testing; simple linear regression; the Python toolkit — and reading mathematical notation; logs and exponentials; odds, the logit and the sigmoid; likelihood; counting and computational cost (with a [lab notebook](labs.md) each) | 0.1–0.10, 0b.1–0b.6 |
| 1 | Ch 1 + Ch 2 (part 1) | Introduction; what is statistical learning; prediction vs. inference; parametric vs. non-parametric | 1.1–1.3, 2.1–2.2 |
| 2 | Ch 2 (part 2) | Assessing accuracy; bias–variance trade-off; classification & KNN; lab | 2.3–2.8 |
| 3 | Ch 3 (part 1) | Simple & multiple linear regression; estimation; inference (SE, *t*, *F*) | 3.1–3.6 |
| 4 | Ch 3 (part 2) | Qualitative predictors; interactions; diagnostics; KNN vs. OLS; lab | 3.7–3.12 |
| 5 | Ch 4 (part 1) | Logistic regression; odds; multiple logistic regression; confounding | 4.1–4.4 |
| 6 | Ch 4 (part 2) | The confusion matrix; ROC/AUC; lab — the generative models (LDA, QDA, naive Bayes) are appendix material | 4.8–4.10 |
| 7 | Ch 5 | Validation set, LOOCV, *k*-fold CV, the bootstrap | 5.1–5.6 |
| 8 | Ch 6 | Subset selection; Cₚ/AIC/BIC; ridge; lasso; PCR/PLS | 6.1–6.7 |
| 9 | Ch 7 | Polynomials, step functions, splines, smoothing splines, GAMs | 7.1–7.6 |
| 10 | Ch 8 | Decision trees; bagging & OOB; random forests; boosting | 8.1–8.7 |
| 11 | Ch 9 | The maximal-margin classifier; the soft margin and *C*; kernels; SVMs tuned by CV | 9.x |
| 12 | Ch 10 | Neural nets; forward pass; backprop/GD; CNNs; regularization (PyTorch) | 10.1–10.6 |
| 13 | Ch 11 | Censoring; the survival and hazard functions; Kaplan–Meier; the log-rank test; Cox regression | 11.x |
| 14 | Ch 12 | Principal components; *K*-means; hierarchical clustering and linkage | 12.x |
| 15 | Ch 13 | Multiple testing; FWER; Bonferroni; Holm; FDR & Benjamini–Hochberg | 13.1–13.5 |

```{admonition} Split lectures
:class: tip

Chapters 2, 3 and 4 each span two lectures. The recommended stopping points let
you stop and resume cleanly:

- **Ch 2** — after "regression vs. classification" (p. 42); assessing accuracy,
  bias–variance and KNN open Lecture 2
- **Ch 3** — after multiple regression and the four questions (p. 76)
- **Ch 4** — after the logistic-regression section (p. 42); the confusion matrix, ROC/AUC and the lab open Lecture 6
```

```{admonition} One session, two decks — so it is a selection
:class: important

The two precourse decks carry **157 slides** in their main flow (106 + 51). A
single 180-minute session cannot cover them, and is not meant to: the session
sets up the notation, the standard-error material and the Python patterns the
chapters lean on hardest, and both decks stay available in full as the
reference. The tools for closing the rest yourself are built in — the
twelve-question self-check on page 7 of `chapter_00.pdf` and the notation table
on page 5 of `chapter_00b.pdf` — see [For students](for-students.md).
```

```{admonition} All thirteen ISLP chapters are taught, in book order
:class: note

Chapters **9 (Support Vector Machines)**, **11 (Survival Analysis)** and
**12 (Unsupervised Learning)** used to sit outside the plan as code-reference
notebooks without a deck. They are now full lectures — 11, 13 and 14 — each with
its own [deck](slides.md) and a [lab](labs.md) carrying worked solutions like
every other. Lectures 1–10 kept their numbers, so anything pegged to the first
ten sessions is unaffected; deep learning moved to Lecture 12 and multiple
testing to Lecture 15.
```

## Assessment

The module is worth **6 ECTS** and is graded by a **single written exam at the
end of the semester — 120 minutes, 100% of the mark**. The
[Final Mock Exam](exams.md) is built as the rehearsal for that paper: same
length, same structure, weighted to Chapters 7, 8, 10 and 13.

## Practice rhythm

Everything below is **practice, not assessment** — eight papers matched to the
calendar so students can self-test at the natural checkpoints, none of which
counts towards the grade. See [Mock exams](exams.md); none is distributed with
this repository.

Each deck also carries far more exercises than a session can run: the
[runsheets](teaching.md) name the two to four worth live time and leave the rest
as homework.

| Paper | Written after | Covers | Length |
|---|:--:|---|:--:|
| Mock Exam 1 | Lecture 4 | Chapters 1–3 | 90 min · 90 pts |
| Short Exam A | Lecture 6 | Ch 0 + 1–2, Ch 3, **Ch 4** | 60 min · 60 pts |
| Short Exam B | Lecture 7 | Ch 2, Ch 3, **Ch 5** | 60 min · 60 pts |
| Mock Exam 2 | Lecture 8 | Chapters 4–6 (+ light cumulative) | 90 min · 90 pts |
| Short Exam C | Lecture 8 | Ch 0 + 0b, Ch 3, **Ch 6** | 60 min · 60 pts |
| Short Exam D | Lecture 10 | Ch 2 + 5, Ch 2 + 4, **Ch 8** | 60 min · 60 pts |
| Final Mock Exam | Lecture 15 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |
| Short Exam E | Lecture 15 | Ch 0, Ch 5 + 7, **Ch 13** | 60 min · 60 pts |

The three mock exams are the full-length rehearsals; the five 60-minute short
exams are the formative layer, and the bold chapter is where each one's hardest
problem sits — which is why they are released in order, not all at once.

## Where to go next

- [Lecture slides](slides.md) — the deck for each week, and how a deck is built.
- [Teaching it](teaching.md) — runsheets, timings and the cut list.
- [Lab notebooks](labs.md) — the companion notebook for each chapter.
- [For students](for-students.md) — prerequisites, workload and how to revise.

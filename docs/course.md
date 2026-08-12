---
myst:
  html_meta:
    description: "The eleven-session semester plan — a taught precourse session plus eight ISLP chapters — with the recommended split points and the assessment calendar."
---

# The course at a glance

{.qrm-lead}
A 11-session semester (11 × 180 min), worth **6 ECTS**: one taught precourse
session covering both precourse decks, then eight ISLP chapters taught in book
order.

:::{container} qrm-chips
[**11** sessions × **180 min**]{.qrm-chip}
[**6** ECTS]{.qrm-chip}
[**1** taught precourse session]{.qrm-chip}
[**9** ISLP chapters]{.qrm-chip}
[**3 + 5** practice exams]{.qrm-chip}
:::

## Semester plan

The precourse opens the semester as a **taught session**; the chapters follow in
ISLP book order. The plan is keyed to **chapter numbers**, not session numbers —
that is what the decks, the labs, the exercise numbering and the
[runsheets](teaching.md) all refer to. The *Sessions* column says how many
180-minute slots each chapter needs.

| Chapter | Sessions | Content | Exercises |
|:--:|:--:|---|---|
| **Precourse** — Ch 0 + Ch 0b | 1 | **Taught in one session**, drawing on both precourse decks: descriptive statistics; probability and Bayes; distributions; standard errors and confidence intervals; hypothesis testing; simple linear regression; the Python toolkit — and reading mathematical notation; logs and exponentials; odds, the logit and the sigmoid; likelihood; counting and computational cost (with a [lab notebook](labs.md) each) | 0.1–0.10, 0b.1–0b.6 |
| **Ch 1** | ½ | Introduction; prediction vs. inference; the three motivating data sets | 1.1–1.3 |
| **Ch 2** | 1½ | What is statistical learning; parametric vs. non-parametric; assessing accuracy; the bias–variance trade-off; the Bayes classifier and KNN; lab | 2.1–2.8 |
| **Ch 3** | 2 | Simple & multiple linear regression; estimation; inference (SE, *t*, *F*); qualitative predictors; interactions; diagnostics; KNN vs. OLS; lab | 3.1–3.12 |
| **Ch 4** | 2 | Logistic regression; odds; multiple logistic regression; confounding; the confusion matrix; ROC/AUC; lab — the generative models (LDA, QDA, naive Bayes) are appendix material | 4.1–4.10 |
| **Ch 5** | 1 | Validation set, LOOCV, *k*-fold CV, the bootstrap | 5.1–5.6 |
| **Ch 6** | 1 | Subset selection; Cₚ/AIC/BIC; ridge; lasso; PCR/PLS | 6.1–6.6 |
| **Ch 7** | 1 | Polynomials, step functions, splines, smoothing splines, GAMs | 7.1–7.6 |
| **Ch 8** | 1 | Decision trees; bagging & OOB; random forests; boosting | 8.1–8.7 |

Chapter 1 is short and opens the same session as the first half of Chapter 2.

```{admonition} Split chapters
:class: tip

Chapters 2, 3 and 4 each span two sessions. The recommended stopping points let
you stop and resume cleanly:

- **Ch 2** — after "regression vs. classification" (p. 41); assessing accuracy,
  bias–variance and KNN open the second session
- **Ch 3** — after multiple regression and the four questions (p. 79)
- **Ch 4** — after the logistic-regression section (p. 46); the confusion matrix, ROC/AUC and the lab open the second session
```

```{admonition} One session, two decks — so it is a selection
:class: important

The two precourse decks carry **165 slides** in their main flow (112 + 53). A
single 180-minute session cannot cover them, and is not meant to: the session
sets up the notation, the standard-error material and the Python patterns the
chapters lean on hardest, and both decks stay available in full as the
reference. The tools for closing the rest yourself are built in — the
twelve-question self-check on page 7 of `chapter_00.pdf` and the notation table
on page 5 of `chapter_00b.pdf` — see [For students](for-students.md).
```

```{admonition} Four chapters sit outside the taught plan
:class: note

Chapters **9 (Support Vector Machines)**, **11 (Survival Analysis)**,
**12 (Unsupervised Learning)** and **13 (Multiple Testing)** are no longer
taught in the sequence. Each keeps its full deck and its lab, now as a
self-study [advanced module](advanced.md) — A5, A6, A8 and A7 respectively —
under `Chapters/Advanced/`. The remaining eight chapters run in book order, so
nothing else moved.

The mock exams were **not** rewritten: the final papers and Short Exam E still
carry a multiple-testing problem, which now draws on module A7 rather than on a
taught session, and any unsupervised-learning question now draws on module A8.
```

## Assessment

The module is worth **6 ECTS** and is graded by a **single written exam at the
end of the semester — 120 minutes, 100% of the mark**. The
[Final Mock Exam](exams.md) is built as the rehearsal for that paper: same
length, same structure, weighted to Chapters 7, 8, 10 and 13 — the last of which
is now the self-study module [A7](advanced.md). Any unsupervised-learning
question draws on module [A8](advanced.md), for the same reason.

## Practice rhythm

Everything below is **practice, not assessment** — eight papers matched to the
calendar so students can self-test at the natural checkpoints, none of which
counts towards the grade. See [Mock exams](exams.md); none is distributed with
this repository.

Each deck also carries far more exercises than a session can run: the
[runsheets](teaching.md) name the two to four worth live time and leave the rest
as homework.

| Paper | Checkpoint | Covers | Length |
|---|:--:|---|:--:|
| Mock Exam 1 | after Ch 3 | Chapters 1–3 | 90 min · 90 pts |
| Short Exam A | after Ch 4 | Ch 0 + 1–2, Ch 3, **Ch 4** | 60 min · 60 pts |
| Short Exam B | after Ch 5 | Ch 2, Ch 3, **Ch 5** | 60 min · 60 pts |
| Mock Exam 2 | after Ch 6 | Chapters 4–6 (+ light cumulative) | 90 min · 90 pts |
| Short Exam C | after Ch 6 | Ch 0 + 0b, Ch 3, **Ch 6** | 60 min · 60 pts |
| Short Exam D | after Ch 8 | Ch 2 + 5, Ch 2 + 4, **Ch 8** | 60 min · 60 pts |
| Final Mock Exam | after Ch 8 | All chapters (weighted to Ch 7/8 and modules A9 and A7) | 120 min · 120 pts |
| Short Exam E | after Ch 8 | Ch 0, Ch 5 + 7, **Ch 13** *(module A7)* | 60 min · 60 pts |

The three mock exams are the full-length rehearsals; the five 60-minute short
exams are the formative layer, and the bold chapter is where each one's hardest
problem sits — which is why they are released in order, not all at once.

## Where to go next

- [Lecture slides](slides.md) — the deck for each week, and how a deck is built.
- [Teaching it](teaching.md) — runsheets, timings and the cut list.
- [Lab notebooks](labs.md) — the companion notebook for each chapter.
- [For students](for-students.md) — prerequisites, workload and how to revise.

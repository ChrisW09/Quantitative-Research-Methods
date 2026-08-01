---
myst:
  html_meta:
    description: "Three full-length mock exams and five 60-minute short exams matched to the course calendar — what each covers, how they are designed, and how they are built."
---

# Mock exams

```{warning}
The exams, their worked solutions and their LaTeX sources are **assessment
material** and are deliberately kept out of the public repository, so they are
not downloadable from this site. Instructors can request them from the author
at [info@profweisser-ai.de](mailto:info@profweisser-ai.de). This page documents
what exists and how it is built.
```

```{admonition} These are practice papers, not the graded exam
:class: important

The module (**6 ECTS**) is graded by **one written exam at the end of the
semester: 120 minutes, 100% of the mark**. None of the eight papers below counts
towards it — they exist so students can find out where they stand before that
paper. The **Final Mock Exam** is deliberately built to its shape: same length,
same structure, same weighting.
```

Eight practice papers are matched to the course rhythm: **three full-length mock
exams** and **five 60-minute short exams**. Each is built from a **single LaTeX
source** so the paper and its solutions can never diverge, and all numeric
answers were verified programmatically.

Every paper exists in three formats:

- **Questions** — the paper as students see it;
- **Solutions** — the same paper with full worked answers, **handed out together
  with the paper** (so the discipline of working it closed-book first sits with
  the student);
- **Review deck** — a Beamer deck for going through the exam in class, step by
  step.

## The three full-length papers

| Exam | Written after | Covers | Length |
|---|:--:|---|:--:|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min · 90 pts |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Final Mock Exam | Lecture 15 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |

The final exam also exists in three parallel versions (**A / B / C**) — same
structure and difficulty, different numbers — for seating variants or for a
second attempt.

## The five 60-minute short exams

Alongside the three full-length papers there are **five 60-minute exams**
(A–E), each **three problems × 20 points**, with the problems increasing in
difficulty: P1 warm-up, P2 core, P3 advanced. They are the formative layer —
short enough to sit in a spare hour, released one at a time as the material each
needs is taught.

| Short exam | Release after | P1 (warm-up) | P2 (core) | P3 (advanced) |
|:--:|:--:|---|---|---|
| A | Lecture 6 | Learning problems, descriptive statistics (Ch 0 + 1–2) | Simple linear regression by hand (Ch 3) | **Logistic regression, confusion matrix (Ch 4)** |
| B | Lecture 7 | Bias–variance, KNN regression (Ch 2) | Reading multiple regression output (Ch 3) | **Cross-validation and the bootstrap (Ch 5)** |
| C | Lecture 8 | Conditional probability, Bayes, odds (Ch 0 + 0b) | Dummies and interactions (Ch 3) | **Ridge and lasso (Ch 6)** |
| D | Lecture 10 | Honest model evaluation — leakage, splits (Ch 2 + 5) | KNN classification by hand (Ch 2 + 4) | **Trees: Gini, splitting, pruning, forests (Ch 8)** |
| E | Lecture 15 | Reading `describe()` output, SE vs SD (Ch 0) | Polynomial regression, model choice (Ch 5 + 7) | **Multiple testing: Bonferroni, Holm, BH (Ch 13)** |

The bold chapter is where each paper's hardest problem sits, so the five are
**sequenced, not interchangeable**: A needs Chapter 4, B Chapter 5, C
Chapter 6, D Chapter 8, E Chapter 13. Because P1 and P2 reach back to earlier
material, each paper is cumulative-to-date rather than a single-chapter test.
They are also the only papers that touch the **precourse** material: A, C and E
each open on Chapter 0 / 0b, while no problem in the three full-length papers
cites either precourse deck.

Each ships as the paper, a solutions PDF carrying a **grading key per problem**
(marks per sub-step, follow-through rules), and a review deck with a "common
mistake" box per problem and a one-slide marking table. They are built by their
own `build.sh`, not by `make exams` — see
[How they are built](#how-they-are-built) below.

## Question design

- Sub-parts are **independent**: a student who gets part (a) wrong can still
  earn full marks on (b) and (c).
- Papers mix conceptual, mathematical and **Python-interpretation** questions —
  the latter show real output (a `statsmodels` summary, a confusion matrix, a
  CV curve) and ask what it means.
- Each exam references the [lecture slides](slides.md) it draws on, so revision
  can be targeted.

## How they are built

```{note}
`Mock_Exams/` is git-ignored, so it is **absent from every clone of this
repository** — the commands below only work on a machine that already has the
folder from the author. On a fresh clone there is nothing to `cd` into.
```

One source file produces both the paper and the solutions; the `\withsolutions`
flag switches between them.

```bash
cd Mock_Exams/Exam_1_after_Lecture_04     # only if you have the folder
pdflatex -jobname=Mock_Exam_1 mock_exam_1.tex
pdflatex -jobname=Mock_Exam_1_Solutions "\def\withsolutions{1}\input{mock_exam_1.tex}"
```

The review decks are separate Beamer sources in the same folder
(`solutions_slides_*.tex`) and compile with a plain `pdflatex` run — twice, for
the navigation bar.

From the repository root, `make exams` builds the whole set on a machine that
has the folder: **18 PDFs**, namely

- the three papers *and* the three final variants A / B / C, each as questions
  and, via `\withsolutions`, as solutions — 12 PDFs;
- all six review decks, two passes each — 6 PDFs.

The target is incremental: a PDF is rebuilt only when its source is newer, and
`make -j` is safe because every job writes under its own `-jobname`. On a
machine without `Mock_Exams/` — a fresh clone, for instance — it stops with a
one-line message rather than a confusing LaTeX error.

The **five 60-minute exams** are the one exception. They live in
`Mock_Exams/Short_Exams_60min/` and are built by the `build.sh` that ships next
to their sources (15 further PDFs: paper, solutions and review deck for each),
deliberately kept out of the Makefile so that folder stays self-contained:

```bash
cd Mock_Exams/Short_Exams_60min
./build.sh
```

## Where to go next

- [The course at a glance](course.md) — where each exam sits in the calendar.
- [For students](for-students.md) — how to revise, and where the short exams fit.
- [Teaching it](teaching.md) — which exercises rehearse which exam problem.
- [Lecture slides](slides.md) — the material each paper draws on.

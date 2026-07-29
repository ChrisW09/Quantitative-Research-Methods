# Mock exams

```{warning}
The exams, their worked solutions and their LaTeX sources are **assessment
material** and are deliberately kept out of the public repository, so they are
not downloadable from this site. Instructors can request them from the author.
This page documents what exists and how it is built.
```

Three practice exams are matched to the course rhythm, each built from a
**single LaTeX source** so the paper and its solutions can never diverge. All
numeric answers were verified programmatically.

Each exam exists in three formats:

- **Questions** — the paper as students see it;
- **Solutions** — the same paper with full worked answers;
- **Review deck** — a Beamer deck for going through the exam in class, step by
  step.

## The exams

| Exam | Written after | Covers | Length |
|---|:--:|---|:--:|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min · 90 pts |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Final Mock Exam | Lecture 12 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts |

The final exam also exists in three parallel versions (**A / B / C**) — same
structure and difficulty, different numbers — for seating variants or for a
second attempt.

Alongside them, a set of **five 60-minute exams** (A–E, three problems × 20
points) covers shorter practice slots. They live in their own subfolder and are
built separately — see [How they are built](#how-they-are-built) below.

## Question design

- Sub-parts are **independent**: a student who gets part (a) wrong can still
  earn full marks on (b) and (c).
- Papers mix conceptual, mathematical and **Python-interpretation** questions —
  the latter show real output (a `statsmodels` summary, a confusion matrix, a
  CV curve) and ask what it means.
- Each exam references the [lecture slides](slides.md) it draws on, so revision
  can be targeted.

## How they are built

One source file produces both the paper and the solutions; the `\withsolutions`
flag switches between them.

```bash
cd Mock_Exams/Exam_1_after_Lecture_04
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
- [Teaching it](teaching.md) — which exercises rehearse which exam problem.
- [Lecture slides](slides.md) — the material each paper draws on.

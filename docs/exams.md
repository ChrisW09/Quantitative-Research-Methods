# Mock exams

Three practice exams matched to the course rhythm, each built from a **single
LaTeX source** so the paper and its solutions can never diverge. All numeric
answers were verified programmatically.

Each exam ships in three formats:

- **Questions** — the paper as students see it;
- **Solutions** — the same paper with full worked answers;
- **Review deck** — a Beamer deck for going through the exam in class,
  step by step.

## The exams

| Exam | Written after | Covers | Length | Questions | Solutions | Review deck |
|---|:--:|---|:--:|:--:|:--:|:--:|
| Mock Exam 1 | Lecture 4 | Ch 1–3 | 90 min · 90 pts | <a href="exams/Mock_Exam_1.pdf">PDF</a> | <a href="exams/Mock_Exam_1_Solutions.pdf">PDF</a> | <a href="exams/Mock_Exam_1_Solutions_Slides.pdf">PDF</a> |
| Mock Exam 2 | Lecture 8 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts | <a href="exams/Mock_Exam_2.pdf">PDF</a> | <a href="exams/Mock_Exam_2_Solutions.pdf">PDF</a> | <a href="exams/Mock_Exam_2_Solutions_Slides.pdf">PDF</a> |
| Final Mock Exam | Lecture 12 | All chapters (weighted to Ch 7/8/10/13) | 120 min · 120 pts | <a href="exams/Final_Mock_Exam.pdf">PDF</a> | <a href="exams/Final_Mock_Exam_Solutions.pdf">PDF</a> | <a href="exams/Final_Mock_Exam_Solutions_Slides.pdf">PDF</a> |

### Parallel variants of the final

The final exam also exists in three parallel versions (A / B / C) — same
structure and difficulty, different numbers — for seating variants or for a
second attempt.

| Variant | Questions | Solutions |
|:--:|:--:|:--:|
| A | <a href="exams/Final_Mock_Exam_A.pdf">PDF</a> | <a href="exams/Final_Mock_Exam_A_Solutions.pdf">PDF</a> |
| B | <a href="exams/Final_Mock_Exam_B.pdf">PDF</a> | <a href="exams/Final_Mock_Exam_B_Solutions.pdf">PDF</a> |
| C | <a href="exams/Final_Mock_Exam_C.pdf">PDF</a> | <a href="exams/Final_Mock_Exam_C_Solutions.pdf">PDF</a> |

## Question design

- Sub-parts are **independent**: a student who gets part (a) wrong can still
  earn full marks on (b) and (c).
- Papers mix conceptual, mathematical and **Python-interpretation** questions —
  the latter show real output (a `statsmodels` summary, a confusion matrix, a
  CV curve) and ask what it means.
- Each exam references the [lecture slides](slides.md) it draws on, so revision
  can be targeted.

## Rebuilding an exam

One source file produces both the paper and the solutions; the `\withsolutions`
flag switches between them.

```bash
cd Mock_Exams/Exam_1_after_Lecture_04
pdflatex -jobname=Mock_Exam_1 mock_exam_1.tex
pdflatex -jobname=Mock_Exam_1_Solutions "\def\withsolutions{1}\input{mock_exam_1.tex}"
```

The review decks are separate Beamer sources in the same folder
(`solutions_slides_*.tex`) and compile with a plain `pdflatex` run (twice, for
the navigation bar).

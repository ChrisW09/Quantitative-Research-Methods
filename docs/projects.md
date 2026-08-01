---
myst:
  html_meta:
    description: "Six short student projects — a real decision on real data, using the methods of the course. Each takes 3–5 hours, fixes its own held-out test set, and ends in a one-page memo."
---

# Short projects

{.qrm-lead}
Six short projects in which students take a **real decision on real data** using
the methods of the course. Each takes about 3–5 hours, uses one of the bundled
course datasets, and ends in a one-page memo with specific numbers rather than a
notebook full of output.

:::{container} qrm-chips
[**6** projects]{.qrm-chip}
[**3–5 h** each]{.qrm-chip}
[real **decisions**, not exercises]{.qrm-chip}
[held-out set **fixed and sealed**]{.qrm-chip}
[**Colab**-ready starters]{.qrm-chip}
:::

These are deliberately unlike the [lab notebooks](labs.md). A lab is guided,
mirrors one chapter and ends with worked solutions. A project poses a problem
someone actually has, gives no solution, and asks the student to commit to an
answer and defend it — including, in several of them, the answer "this cannot be
predicted well enough to act on."

## The six

| # | Project | The decision the student must make | Data | Methods | After |
|:--:|---|---|:--:|:--:|:--:|
| 1 | Who should we call? | Hand back a ranked shortlist of 500 prospects and say how many policies it will sell | `Caravan` | Ch 4, 5 | Lecture 7 |
| 2 | Five numbers or seventeen? | Decide whether a board-readable five-variable model is defensible, and price the simplicity | `College` | Ch 3, 6 | Lecture 8 |
| 3 | Can you predict the market? | Tell a fund whether to trade on last week's returns — with an interval | `Weekly` | Ch 4, 5 | Lecture 7 |
| 4 | A model the brand manager can read | Choose between the most accurate model and one you can explain | `OJ` | Ch 8 | Lecture 10 |
| 5 | What is it worth, and how sure are you? | Value five neighbourhoods, each with a defensible interval | `Boston` | Ch 3, 7 | Lecture 9 |
| 6 | How many managers can actually pick stocks? | Give a pension trustee one number — it may be zero | `Fund` | Ch 13 | Lecture 15 |

The briefs, starters and notes live in
[`Projects/`](https://github.com/ChrisW09/Quantitative-Research-Methods/tree/main/Projects).
Each project folder holds three files: the **brief** (`README.md`), a
**Colab-ready starter notebook**, and **`SOLUTION_NOTES.md`** — what a good
answer finds, the trap, and a marking guide.

Open a starter in Colab — nothing to install, the data resolves itself:

| | | | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|
| **1** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_1_caravan/project_1_starter.ipynb) | **2** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_2_college/project_2_starter.ipynb) | **3** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_3_weekly/project_3_starter.ipynb) | **4** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_4_oj/project_4_starter.ipynb) | **5** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_5_boston/project_5_starter.ipynb) | **6** [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_6_fund/project_6_starter.ipynb) |

```{admonition} Read the solution notes afterwards
:class: tip

The notes ship alongside the brief, exactly as the practice-exam solutions ship
alongside the paper: the discipline of attempting the work first is the
student's to keep. They are genuinely worth reading *after* an attempt — several
of these projects have a result that surprises people.
```

## What makes them projects rather than exercises

**The test set is fixed and off-limits.**
: Each starter defines the held-out split so that every student's reported number
  is comparable, and so that Chapter 5's honest-evaluation discipline is enforced
  by the scaffolding rather than by trust. Where the data are time-ordered —
  projects 3 and 6 — the split is **chronological rather than random**, because
  randomly splitting a time series trains on the future to predict the past and
  answers an easier question than the one asked.

**There is a baseline to beat, computed for you.**
: Random targeting, the majority class, a mean-only model. A student who cannot
  beat it has learned something real, and the briefs say so.

**Every number needs an interval or a caveat.**
: A point estimate without its uncertainty is not an answer to any of these
  questions — least of all project 3, where the interval is the whole point.

**The obvious approach is often the wrong one.**
: Each project has a trap, named in its solution notes but not in its brief.
  Accuracy is the wrong metric when 6% of customers buy; random cross-validation
  is invalid on time-ordered returns; a confidence interval for a mean is not a
  prediction interval for one house; and of 289 "significant" fund managers out
  of 2,000, about a hundred are what chance alone produces and roughly half are
  significantly *bad*.

## Where they fit in the semester

The module is graded by [one written exam](exams.md), so the projects are
**formative** — none counts towards a mark unless the instructor chooses to use
one. They are keyed to the lecture after which each becomes doable, in the same
"one at a time, when the material is taught" rhythm as the five 60-minute
[short exams](exams.md), and they fill the gap those papers leave: a short exam
tests whether you can answer a question, a project asks whether you can decide
something.

Projects 3 and 6 both end in a judgement call worth arguing about, which makes
them the two best candidates for group work or a seminar discussion.

## Where to go next

- [Lab notebooks](labs.md) — the guided labs these build on.
- [Advanced modules](advanced.md) — several projects name one as a natural extension: Shapley values for explaining a targeting model, conformal prediction for the valuation intervals.
- [Mock exams](exams.md) — the practice papers, and the exam that actually counts.
- [For students](for-students.md) — workload, and how the course is assessed.

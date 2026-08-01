# Short projects

Six short projects in which students take a **real decision on real data** using
the methods of the course. Each takes about **3–5 hours**, uses one of the
bundled course datasets, and ends in a **one-page memo with specific numbers**
rather than a notebook full of output.

They are deliberately unlike the [lab notebooks](../Chapters/). A lab is
guided, mirrors one chapter and ends with worked solutions. A project poses a
problem someone actually has, gives no solution, and asks the student to commit
to an answer and defend it.

## The six

| # | Project | The decision | Data | Methods | After |
|:--:|---|---|---|:--:|:--:|
| 1 | **Who should we call?** | Hand back a ranked shortlist of 500 prospects and say how many policies it will sell | `Caravan` (5,822 × 86) | Ch 4, 5 | Lecture 7 |
| 2 | **Five numbers or seventeen?** | Decide whether a board-readable five-variable model is defensible, and price the simplicity | `College` (777 × 18) | Ch 3, 6 | Lecture 8 |
| 3 | **Can you predict the market?** | Tell a fund whether to trade on last week's returns — with an interval | `Weekly` (1,089 × 9) | Ch 4, 5 | Lecture 7 |
| 4 | **A model the brand manager can read** | Choose between the most accurate model and one you can explain | `OJ` (1,070 × 18) | Ch 8 | Lecture 10 |
| 5 | **What is it worth, and how sure are you?** | Value five neighbourhoods, each with a defensible interval | `Boston` (506 × 13) | Ch 3, 7 | Lecture 9 |
| 6 | **How many managers can actually pick stocks?** | Give a pension trustee one number — it may be zero | `Fund` (50 × 2,000) | Ch 13 | Lecture 15 |

Each folder holds three files:

- **`README.md`** — the brief: the situation, the challenge, the rules, exactly
  which numbers the memo must report, and how the work is judged.
- **`project_N_starter.ipynb`** — a Colab-ready starter that loads the data,
  shows a first look, **fixes the held-out split with a seed**, computes the
  baseline you have to beat, and provides the evaluation helper. Everything in
  it runs; your work goes underneath the numbered headings.
- **`SOLUTION_NOTES.md`** — what a good answer finds, the trap, the common wrong
  turns, and a marking guide. Read it **after** your attempt: like the practice
  exams, it ships alongside the paper and the discipline of trying first is
  yours to keep.

## Three rules that apply to all six

1. **The test set is fixed and off-limits** until your final evaluation. The
   starter defines it so that every student's number is comparable — seeded where
   a random split is appropriate, and **chronological in projects 3 and 6**, where
   the data are time-ordered and a random split would train on the future to
   predict the past. Touching it early does not make your model better; it only
   makes your estimate a lie.
2. **Every number gets an interval or a caveat.** A point estimate presented
   without its uncertainty is not an answer to any of these questions.
3. **A correct negative result beats an overstated positive one.** "This cannot
   be predicted at the accuracy you would need" is a complete, creditable answer
   in several of these projects — provided you show the work that establishes it.

## Running one

Every starter opens in Colab with one click from the badge in its first cell —
nothing to install, and the data resolves automatically. Locally, run it from
inside its own folder so the relative path to
`ALL CSV FILES - 2nd Edition/` resolves:

```bash
cd Projects/project_1_caravan
jupyter lab project_1_starter.ipynb
```

Nothing beyond the course's `requirements.txt` is needed.

## For the instructor

The projects are **formative** — the module is graded by the single written exam
(see [`Teaching_Guide/semester_plan.md`](../Teaching_Guide/semester_plan.md)), so
none of these counts towards a mark unless you choose to use one. They fit three
ways:

- **as a bridge over the mid-semester gap**, released on the schedule in the
  table above, in the same "one at a time, when the material is taught" rhythm as
  the 60-minute short exams;
- **as group work**, since each deliverable is a memo and a recommendation
  rather than a set of answers, which makes disagreement productive;
- **as a seminar seed** — projects 3 and 6 in particular end in a judgement call
  worth arguing about in a room.

Each `SOLUTION_NOTES.md` carries a marking guide if you do decide to grade one.

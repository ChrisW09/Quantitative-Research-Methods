# Project 5 — What is it worth, and how sure are you?

> **The situation.** A municipal valuation office must publish an assessed median house
> value for **five named census tracts** before the appeal window opens. Every one of the
> five figures will be contested in writing — owners' advisers read the file, and a number
> that arrives bare is struck out on procedure alone. So each figure must be accompanied by
> **an interval the office is prepared to defend**: an interval it will stand behind when a
> single tract's actual median value is put to it in a hearing. Being wrong is expensive in
> two directions. An interval that is too wide is useless as a valuation and invites the
> charge that the office does not know what it is doing. An interval that is too narrow
> loses the appeal the first time a real tract falls outside it — and the office's own
> published interval becomes the evidence against it. A point estimate on its own is **not
> an acceptable deliverable.**

**Data:** `Boston.csv` (506 × 13) — one row per census tract in the Boston metropolitan area; `medv` is the tract's median owner-occupied home value in $1,000s.
**Methods:** Chapters 3 and 7, with Chapter 5 for evaluation · **After:** Lecture 9 · **Time:** 3–5 hours
**Deliverable:** a one-page memo with five point estimates, five intervals, and the evidence that your model earns whatever complexity it carries.

---

## The challenge

1. **Reproduce the two reference figures.** The starter computes them for you: with 5-fold
   CV at `random_state=2024` over all 506 tracts, a linear model on all predictors scores
   **CV RMSE $4.92k**, and a cubic-spline basis expansion of the predictors
   (`SplineTransformer(n_knots=5, degree=3)` then least squares) scores **$4.58k** — an
   improvement of about **7%**. Confirm both numbers before you go further; if your
   pipeline disagrees, fix the pipeline, not the number.

2. **Establish that the curvature is real — do not assert it.** A 7% gap is not nothing,
   but it is not much either, and "the relationship is nonlinear" is a claim that needs
   evidence. Produce it. Which predictors carry the curvature, and which do not? A blanket
   spline basis over all twelve predictors spends flexibility everywhere; find out where
   it is actually earned. Chapters 3 (residual diagnostics, nested $F$-tests, polynomial
   terms, transformations) and 7 (polynomials, splines, GAMs) both apply, and the evidence
   you produce may be graphical, inferential, or out-of-sample — best is more than one.

3. **Choose your model** using the training tracts only, and say in one sentence why you
   chose it over the linear baseline.

4. **Value the five tracts.** The starter names them by index — tracts
   **401, 113, 2, 297 and 162** — spanning the cheap end of the market to the very top.
   For each, report a **point estimate** and a **95% interval**. For each interval you must
   also state **what kind of interval it is** and **why that kind is the one the valuation
   office needs**. This last requirement carries more marks than the modelling.

5. **Evaluate once.** Call `evaluate_on_test(...)` from the starter exactly once, at the
   end, on the whole held-out set. It reports accuracy *and* what your intervals actually
   did out of sample. Report what it tells you, including anything unflattering.

6. **Write the memo** as the final markdown cell of your notebook.

## Rules

- **The held-out set is sealed.** The starter defines a fixed 80/20 split with
  `random_state=2024`. `X_test` and `y_test` may not be looked at, plotted, summarised or
  fitted on until Step 5 (Requirement 5). Every model choice — which predictors, which
  transformation, how many knots, how much penalty — is made on the 404 training tracts,
  by cross-validation. This is the discipline of Chapter 5 and the scaffolding enforces it.
- **Allowed:** anything from Chapters 3 through 7. That includes transformations of
  predictors, polynomials, splines, GAMs (`pygam`), and ridge/lasso should you need to
  stabilise a wide basis. **Out of scope:** trees, forests, boosting, and anything from
  Chapter 8 onwards — this project is about intervals, not about squeezing the last
  0.1 of RMSE.
- **Seed everything** with `random_state=2024` (or `np.random.default_rng(2024)`), so your
  numbers are comparable with everyone else's.
- **Beating the baseline is not required; being honest about it is.** The starter prints
  the baseline CV RMSE on the training tracts. If your flexible model does not beat it, say
  so plainly and report the linear model as your recommendation. That is a complete,
  creditable answer.

## What you must report

The memo must contain **all** of the following, each as a number, not as a description.

| # | Quantity |
|---|---|
| 1 | CV RMSE of the linear model on all predictors — the reference figure and your training-set figure |
| 2 | CV RMSE of your flexible model, on the same folds, and the percentage improvement |
| 3 | Your evidence that the curvature is real: name the predictors that carry it and give the statistic that establishes it (a test statistic and $p$-value, a CV gap, or both) |
| 4 | A five-row table: tract index, point estimate, interval lower, interval upper, interval width |
| 5 | One sentence naming **which kind of interval** those are and **why** it is the kind the office needs |
| 6 | The output of `evaluate_on_test(...)`: test RMSE, the coverage your intervals achieved, and their mean width |
| 7 | One sentence on the **range of `medv`** in this data and what it implies for the top end of your intervals |
| 8 | Your recommendation, and the caveat you would attach if the office published it |

## How this is judged

| | Weak | Solid | Strong |
|---|---|---|---|
| **Evidence of curvature** | Asserts nonlinearity, or points only at the 7% CV gap | Shows curvature with a residual plot or a nested test on the right predictors | Localises the curvature to specific predictors, shows where a spline basis is *not* earned, and confirms it out of sample |
| **The intervals** | One interval type, unnamed, taken from whatever the software printed | Correct interval type, correctly named, with the reason stated | Correct type, named, justified, *and* checked — coverage on the held-out set reported and reconciled with the nominal 95% |
| **Honesty** | Reports only the flattering numbers; claims a large win from a small one | Reports the required numbers as they came out | States plainly where the model is weak, which tracts it should not be trusted on, and what would change the recommendation |
| **The memo** | A list of numbers | Numbers plus a recommendation | A recommendation a valuation officer could act on, with the caveat that keeps the office out of trouble |

**A correct negative result beats an overstated positive one.** "The flexible model improves
CV RMSE by 7%, which is real but small, and I recommend the linear model for its defensible
intervals" — argued with evidence — scores above "my GAM is much better" asserted without
it. The office is not buying a model; it is buying a number it can defend.

## Getting started

Open `project_5_starter.ipynb`. It loads the data, shows you the target, computes the
reference figures and the baseline, seals the test set, names the five tracts, and defines
the evaluation helper. Your work begins at the cell marked **Step 1**.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_5_boston/project_5_starter.ipynb)

Worked notes are in `SOLUTION_NOTES.md`. They are published alongside this brief, on the
understanding that you read them **after** your attempt, not instead of one.

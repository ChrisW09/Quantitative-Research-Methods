# Project 3 — Can you predict the market? (and how would you know)

> **The situation.** A small fund has a proposal on the table: a rule that goes long
> for a week whenever last week's index return points the right way. Before any
> money moves, the partners want an honest answer to one question — **can next
> week's direction be predicted at all, and with what confidence?** They are not
> asking for a model. They are asking whether the edge is real, because a
> confident wrong answer here is not an embarrassment on a slide, it is a
> drawdown. Your job is to give them a number they can act on, an interval around
> it, and a recommendation you would defend with your own money.

**Data:** `Weekly.csv` (1,089 × 9) — weekly percentage returns on the S&P 500, 1990–2010: `Year`, `Lag1`–`Lag5` (the previous five weeks' returns), `Volume` (average daily share volume, billions), `Today` (this week's return) and `Direction` (`Up`/`Down`).  
**Methods:** Chapters 4 and 5 · **After:** Lecture 7 · **Time:** 3–5 hours  
**Deliverable:** a one-page memo to the fund, in the final markdown cell of your notebook, containing the required numbers below and a recommendation.

## The challenge

Your target is `Direction`. Your candidate predictors are `Lag1`–`Lag5` and
`Volume` — and **nothing else**.

> ### ⚠️ `Today` is not a predictor. It is the answer.
> `Direction` is, by construction, the sign of `Today`. A model given `Today`
> will score close to 100 %, and it will have learned nothing except that you
> handed it the label. **This is the single most common fatal error on this data
> set, and it voids the submission.** Drop both `Today` and `Direction` from your
> design matrix and check the column list before you fit. If your accuracy is
> above about 70 %, you have leaked something — go and find it.

1. **Read the baseline.** The starter computes the accuracy of the rule "always
   predict `Up`" on the held-out period. Every number you produce afterwards is
   measured against *that*, not against 50 %.
2. **Fit one honest classifier.** Choose a small set of predictors, fit on the
   training years only, and evaluate once on the held-out period. Report the
   accuracy **with a 95 % interval**.
3. **Compare methods.** Put at least three of Chapter 4's classifiers —
   logistic regression, LDA, QDA, KNN — on the same split, with the same
   predictors, and tabulate them. For KNN, say what you did about scaling and
   how you chose $K$ (and where you chose it).
4. **Show what happens as predictors are added.** Report the held-out accuracy of
   your best single-predictor model and of the model using all six predictors.
   Explain the direction of the change in the language of Chapter 2.
5. **Justify your resampling.** If you use cross-validation or the bootstrap
   anywhere — for choosing $K$, for choosing predictors, for anything — you must
   state **in one sentence why your scheme is legitimate for data that arrive in
   time order**, naming which weeks each fold fits on and which it scores. Not
   every resampling scheme in Chapter 5 survives that question on a series. This
   requirement is not decorative; it is marked, and the default answer of
   "10-fold, as in the lab" is not an answer.
6. **Decide whether your rule beats the baseline.** Not whether the point
   estimate is higher — whether the two can be *distinguished*, given the size
   of the held-out sample. Support the claim with an interval or a test.
7. **Write the memo.** One page. What you found, what it means for the proposed
   rule, and what you would tell the partners to do.

## Rules

- **Held out.** The training years are `Year <= 2008`; the held-out period is
  **2009–2010** (n = 104). You may look at the training years as much as you
  like. You touch the held-out period **once**, at the very end, through the
  starter's `evaluate()` helper — so that your number is computed exactly the way
  everyone else's is. Fitting several models and reporting the one that happened
  to do best *on the held-out period* is test-set mining, and it is the same
  error as reporting a training accuracy, only better hidden.
- **Choose on the training years.** Predictor sets, $K$ for KNN, thresholds —
  all of it is decided with the training data, by an argument or a resampling
  scheme you have justified under requirement 5.
- **Never `Today`, never `Direction`.** See the warning above.
- **Every accuracy carries a 95 % interval.** A bare accuracy figure anywhere in
  your memo loses marks, however good the number is. On 104 weeks the interval
  is roughly ±9 percentage points, and that fact *is* the finding.
- **Seed everything** with `2024` (`np.random.default_rng(2024)`, or
  `random_state=2024`), so your numbers reproduce.

## What you must report

The memo must contain all six of these, each with the figure attached:

| # | Quantity | Form |
|---|----------|------|
| 1 | Held-out accuracy of **your chosen rule** | % **and** a 95 % interval |
| 2 | Held-out accuracy of the **majority-class baseline** | % |
| 3 | **Can the two be distinguished?** | yes / no, with the interval or test that settles it |
| 4 | **Method comparison** on the fixed split | small table: method, predictors, accuracy, 95 % interval |
| 5 | **Effect of adding predictors** | one predictor vs all six, both held-out, with the interpretation |
| 6 | **Recommendation to the fund** | one paragraph |

For requirement 6, be aware of the following, and take it literally:
**"do not trade on this" is a fully acceptable answer, and may well be the
correct one.** A memo that reaches that conclusion, and shows the arithmetic
that forces it, scores higher than a memo that finds an edge it cannot defend.
You are not being marked on whether you beat the market.

## How this is judged

| | What it looks like |
|---|---|
| **Weak** | A single accuracy figure with no interval; or a number obtained by scoring on the data the model was fitted to; or `Today` among the predictors; or cross-validated folds drawn at random from a time-ordered series with no comment. Conclusion stated more confidently than the evidence allows. |
| **Solid** | An honest held-out accuracy with a correct 95 % interval, compared against the majority baseline; three or more Chapter 4 methods on the same split; the added-predictors comparison with a sensible bias–variance reading; a resampling scheme whose treatment of time is stated. A clear recommendation. |
| **Strong** | All of the above, plus the recognition that the interval around the held-out accuracy **overlaps the baseline**, and the conclusion that follows from it — stated plainly, without hedging, and with the sample size named as the reason the question cannot be settled more sharply. Notes what evidence *would* settle it (how many weeks, or what other data). Says what the fund should do and what it should not conclude. |

**A correct negative result beats an overstated positive one.** That is the whole
point of Chapter 5, and it is the point of this project. The market-prediction
literature is full of the other kind.

## Getting started

Open `project_3_starter.ipynb`. It loads the data, shows you the one fact about
this series that shapes everything, defines the held-out split, computes the
baseline, and gives you the `evaluate()` helper. Your work begins at
**Step 1**; add code cells beneath the numbered markdown headings.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_3_weekly/project_3_starter.ipynb)

*The notebook runs on Colab as-is — the badge above and the `GITHUB_RAW` line in
its setup cell already point to this repository, so packages install and data
loads automatically.*

**No solution is provided in advance.** `SOLUTION_NOTES.md` in this folder is
published alongside the project; read it **after** you have made a serious
attempt, not before.

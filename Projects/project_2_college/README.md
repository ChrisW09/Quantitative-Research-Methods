# Project 2 — Five numbers or seventeen?

> **The situation.** A consortium of regional universities is preparing a public briefing on why out-of-state tuition varies so sharply across American colleges — from **$2,340** to **$21,700** at institutions in the same file — and the board has asked for a model it can read aloud. A colleague on the consortium's staff has already fitted **every one of the seventeen** available variables, reports a respectable fit, and states that the model "cannot be improved on" and that removing anything would be vandalism. The board's chair disagrees. She will not stand in front of a press conference and defend seventeen coefficients, and she wants **five**. Someone has to decide between them, and the decision has a price: if the small model is materially worse, the consortium publishes a number that is more wrong than it needed to be; if it is not, seventeen coefficients are defended for nothing. Your job is to **put that price in dollars** and make the call.

**Data:** `College.csv` (777 × 18) — statistics on 777 American colleges and universities from the 1995 *US News & World Report* guide.
**Methods:** Chapters 3, 5, 6 · Chapter 7 as an optional extension · **After:** Lecture 8 · **Time:** 3–5 hours
**Deliverable:** a one-page memo in the final markdown cell of your notebook, containing the required numbers, a recommendation, and its caveat.

The target is `Outstate`, out-of-state tuition in dollars. `Private` is recorded as `Yes`/`No` and must be encoded before any model will accept it. Load the file so that the **college name never becomes an eighteenth predictor**:

```python
college = load('College', index_col=0).reset_index(drop=True)   # the first column is a name, not a variable
```

The `reset_index` is there because the name arrives differently depending on where you run. `load()` prefers the `ISLP` package, and `ISLP`'s copy of these 777 rows **does not carry the names at all** — it is indexed `0 … 776`; the bundled CSV does carry them, as its index. Same rows, same order, same eighteen columns either way, so the starter normalises both to a positional index and nothing in this project depends on the name. Report nothing about a college's identity unless you have checked that it is there.

## The challenge

1. **Reproduce the baseline.** The starter notebook computes the test RMSE of a **null model** that predicts the training mean for every college. Confirm it, and say in one sentence what it means for a tuition figure to be wrong by that much.
2. **Fit the colleague's model** — ordinary least squares on all seventeen predictors — and record its test RMSE. This is the number the board has been told cannot be improved on.
3. **Produce the best-predicting model you can honestly evaluate.** Use the tools of Chapter 6: best-subset or stepwise selection, ridge, the lasso, each tuned by cross-validation **on the training data only**. Report what you tried, not merely what won.
4. **Produce a five-variable model for the board.** Exactly five predictors (a `Yes`/`No` variable counts as one). State **which five**, and — this is the part that earns the marks — **how you chose them**, with the evidence.
5. **Price the restriction.** Report the difference in test RMSE between your best model and your five-variable model, **in dollars**, and put it in context: as a fraction of the null model's error, and as a fraction of the improvement the full model buys over the null.
6. **Recommend one model to the board**, with the single caveat that most threatens your recommendation.

## Rules

- **The test set is sealed.** The starter defines a 70/30 split at `random_state=2024`. You may not look at the test set, score against it, or let it influence a choice of variable, penalty or transformation until you have finished modelling. Every comparison you make while deciding must come from cross-validation on the **training** data.
- **Score each model once.** Call the starter's `evaluate()` helper exactly once per final model, so that your number is computed the same way as everyone else's. Four or five calls is a project; twenty calls is a fishing expedition, and the resulting RMSE no longer estimates anything.
- **Allowed:** everything from Chapters 3, 5 and 6 — transformations of predictors, interactions, subset selection, ridge, the lasso, cross-validation. Splines and GAMs (Chapter 7) are a legitimate extension if you want one. Methods from Chapter 8 onwards are out of scope for this project; the point here is not to find the strongest possible learner but to price interpretability inside a class of models the board could be shown.
- **Report dollars.** RMSE in this project is measured in dollars of tuition. Round to the nearest dollar and say so; "0.24" is not an answer anyone on the board can act on.
- A model that **fails to beat the baseline**, honestly reported, is a legitimate result and will be marked as one.

## What you must report

The memo must contain each of these, explicitly and numerically.

| # | Quantity | Form |
|---|----------|------|
| 1 | Test RMSE of the **null** (mean-only) model | dollars |
| 2 | Test RMSE of the **all-seventeen-variable** OLS model | dollars |
| 3 | Test RMSE of **your best** model, and what it is | dollars + one line |
| 4 | Test RMSE of your **five-variable** model | dollars |
| 5 | **Which five** variables, and **how** they were chosen | list + method |
| 6 | The **dollar cost of the restriction** (4 − 3) | dollars, plus one relative framing |
| 7 | Your **recommendation** and its **caveat** | two or three sentences |

## How this is judged

| | Weak | Solid | Strong |
|---|---|---|---|
| **Evaluation discipline** | Test set used during selection; RMSE quoted from whichever fit looked best | Split respected; selection done by cross-validation on the training data | As solid, and the student says what the test RMSE *is* an estimate of, and how uncertain it is |
| **The five variables** | Five picked by eye, by correlation with the target, or by *p*-value from the full fit | Chosen by a stated procedure — stepwise or subset selection under CV — and the procedure is reported | Chosen by a stated procedure **and** checked against a rival five-variable set, with the disagreement explained |
| **The comparison** | "The complex model is better" with no number attached | The dollar cost of the restriction is computed and put in context | The cost is compared against the *uncertainty* in the cost — is $150 of RMSE distinguishable from zero on 234 test colleges? |
| **Regularisation** | Ridge or lasso fitted on unstandardised predictors, or tuned against the test set | Fitted on standardised predictors, penalty chosen by CV, coefficients read correctly | The student explains **why** the regularised fit landed where it did on *this* data, rather than assuming it must win |
| **Honesty** | Overstated conclusion; a result reported as an improvement without evidence that it is one | Conclusions match the numbers | A negative or null finding stated plainly and explained. **This is the highest mark available in this course** — a correct negative result beats an overstated positive one, every time |
| **The memo** | Numbers missing; no recommendation | All seven required numbers, clear recommendation | A recommendation a board could act on, with the caveat that would most embarrass it if ignored |

Two warnings drawn from previous cohorts. First, **report the comparison you actually ran, in the direction it actually came out.** Every method in Chapter 6 has conditions under which it helps and conditions under which it does not; which of those this data set turns out to be is the question, and an answer contradicting what you expected is a result, not a mistake to be tidied away. Second, **a variable with a large coefficient is not the same thing as a variable worth keeping** — test that claim before you build the board's model on it.

## Getting started

Open [`project_2_starter.ipynb`](project_2_starter.ipynb). It loads the data, shows the first look, defines the sealed split, computes the baseline, and gives you two helpers — `cv_rmse()` for honest model selection and `evaluate()` for the single final score. Your work goes under the numbered `## Step` headings at the end.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_2_college/project_2_starter.ipynb)

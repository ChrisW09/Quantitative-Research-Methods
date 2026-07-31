# Project 1 — Who should we call?

> **The situation.** An insurer's marketing team has a list of **1,822 prospects** and the budget to telephone **exactly 500** of them about a caravan policy. A call costs roughly **€10** in agent time; a policy sold is worth roughly **€200** in expected margin. Nobody is asking you which customers will buy — that question has no useful answer when only one prospect in seventeen ever buys anything. They are asking you for a **ranked shortlist of 500 names**, and for a number they can put in a budget request: *how many sales will these 500 calls produce?* Hand back an honest estimate and they will fund the campaign. Hand back a flattering one, and when the campaign returns half of what you promised, you will not be asked again.

**Data:** `Caravan.csv` (5,822 × 86) — anonymised Dutch insurance customers: 85 sociodemographic and product-ownership variables plus `Purchase` (Yes/No), whether the customer bought a caravan policy.  
**Methods:** Chapters 4–5 · **After:** Lecture 7 · **Time:** 3–5 hours  
**Deliverable:** a shortlist of 500 prospect indices, plus a one-page memo in the notebook's final markdown cell.

## The challenge

1. **Build a ranker.** Fit **at least three** classifiers on the training set and use them to order the 1,822 held-out prospects from most to least likely to buy. Logistic regression, LDA, QDA, naive Bayes and KNN are all fair game (Chapter 4); so is anything from Chapter 8 if you have read that far. What matters is the **order**, not a verdict on each customer.
2. **Choose between candidate models honestly.** You may not look at the test set to pick a model. Use the training set and the resampling machinery of Chapter 5 — cross-validation, a validation split, the bootstrap — and say in the memo **which quantity you compared models on, and why that quantity and not another one**.
3. **Commit to exactly 500 prospects.** Not 499, not 501, no ties left unbroken. Save them with the helper the starter provides.
4. **Evaluate once.** Call `evaluate_shortlist()` a single time, at the end. Report what it gives you, including the outcome you did not want if that is what you got.
5. **Attach uncertainty to your headline number.** "Roughly *N* sales" is not a deliverable; "*N* sales, plausibly between *N*−*a* and *N*+*b*, and here is what that interval is an interval *about*" is. Chapter 5 gives you at least two ways to get there, and they do not give the same answer.
6. **Answer the budget question.** One paragraph: what would change if the team could only afford **100** calls instead of 500? Would your shortlist's first 100 names be the right 100? Would the campaign be more or less profitable per call?

## Rules

- **The prospects' outcomes are sealed.** The starter notebook defines the split with a fixed seed. You may use the 1,822 prospects' *predictors* — a real marketing team would have them — but their individual `Purchase` values are off limits until the single evaluation at the end. Do not fit on them, tune on them, or peek. Every choice you make — features, scaling, model, hyperparameters, cut-offs — happens on the 4,000 training rows. The one exception is deliberate and given to you: the **overall purchase rate of the prospect list** is disclosed in the starter, because a marketing team knows its own conversion rate and because publishing it makes every student's lift figure comparable.
- **One evaluation.** The point of a held-out set is that it is spent once. If you evaluate, adjust, and evaluate again, the number you report is no longer an honest estimate of anything, and the memo must say so.
- **The split is fixed for everyone.** Do not change the seed, the ordering, or the 4,000/1,822 sizes. Your number is then directly comparable with every other student's.
- **Preprocessing is part of the model.** All 85 predictors are integer-coded but they are *not* on a common scale. If your method cares about that, handle it inside a pipeline fitted on training data only.
- **You may use** `numpy`, `pandas`, `matplotlib`, `scipy`, `statsmodels`, `scikit-learn`, `pygam`. No `seaborn`.
- **Seed everything.** `np.random.default_rng(2024)` or `random_state=2024`.

## What you must report

The final markdown cell is a memo to the marketing team. It must contain, as explicit numbers:

| # | Quantity | Form |
|---|---|---|
| 1 | The 500 chosen prospects | saved to `shortlist.csv` and referenced by name in the memo |
| 2 | The model you shortlisted with, and why you chose it over the alternatives | one short paragraph naming the comparison quantity and its value |
| 3 | **Expected number of sales** from the 500 calls | a point estimate **with an interval**, and one line on what the interval is an interval *about* |
| 4 | **Top-500 hit rate** | a percentage |
| 5 | **Lift over random selection** | a multiple, with the random baseline restated |
| 6 | Expected campaign profit at €10 per call and €200 per policy | one number, and the break-even hit rate it must clear |
| 7 | The budget-100 paragraph | prose |
| 8 | Caveats | at least two things that could make this estimate wrong in deployment |

## How this is judged

| | Weak | Solid | Strong |
|---|---|---|---|
| **Framing** | Treats the task as "predict who buys"; reports a verdict per customer | Treats it as ranking; reports hit rate and lift | Articulates *why* ranking is the right frame here and what quantity a targeting decision actually depends on |
| **Model choice** | One model, no comparison, or a comparison made on the test set | Two or more candidates compared by cross-validation on the training set | Comparison uses a quantity aligned with the decision (top-*k* performance, not a whole-sample summary) and says why |
| **Discipline** | Test set touched more than once, or before the end | Sealed until the final cell | Sealed, *and* the memo states the pre-registered expectation and compares it with the realised result |
| **Uncertainty** | A single number | An interval, correctly computed | An interval whose meaning is stated precisely — sampling variation in the 500 outcomes is not the same thing as uncertainty about a new list of prospects |
| **Honesty** | Overstates the result; hides the baseline | Reports the baseline alongside the result | Reports a result that undercuts the author's own preferred model, or explains that the campaign is marginal, when that is what the numbers say |

A memo that concludes **"our best ranking gives a 1.1× lift, statistically indistinguishable from calling at random, and here is the evidence"** scores *above* a memo that claims a 3× lift it cannot support. **A correct negative result beats an overstated positive one** — that is the whole point of the course. What is not forgivable is a number that cannot be reproduced from the notebook that produced it.

## Getting started

Open [`project_1_starter.ipynb`](./project_1_starter.ipynb). It loads the data, defines the sealed split, computes the random baseline you must beat, and gives you the two helpers — `save_shortlist()` and `evaluate_shortlist()` — that make your number comparable with everyone else's. Your work begins at the cell marked **Step 1**.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_1_caravan/project_1_starter.ipynb)

Do not read `SOLUTION_NOTES.md` until you have a memo of your own.

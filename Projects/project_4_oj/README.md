# Project 4 — A model the brand manager can read

> **The situation.** The brand manager for Minute Maid has 1 070 purchase records from five stores and one question: **which customers choose Minute Maid over Citrus Hill, and why** — because next quarter she has to decide where to spend a promotion budget. She has also been explicit about a constraint, and she means it: *she will not act on a model she cannot explain to her team.* Your job is therefore not one model but two — the most accurate classifier you can build, and the most explicable one you can defend — and then a recommendation about which of them she should deploy, with the price of that choice stated as a number rather than as a sentiment. If you hand her the accurate model and cannot explain it, nothing happens. If you hand her the readable model and it is materially worse, you have cost her sales. Deciding which of those two risks is the smaller one **is the deliverable**.

**Data:** `OJ.csv` (1 070 × 18) — individual orange-juice purchases: brand bought, both shelf prices, discounts and in-store specials that week, store identity, and a running measure of each customer's brand loyalty to Citrus Hill. 653 purchases of Citrus Hill, 417 of Minute Maid.  
**Methods:** Chapter 8, with Chapters 4–5 for comparison · **After:** Lecture 10 · **Time:** 3–5 hours  
**Deliverable:** a one-page memo to the brand manager, in the starter notebook's final markdown cell, containing the numbers listed below.

## The challenge

1. **Decide what belongs in the model, and say why.** Store identity is recorded three times over (`StoreID`, `STORE`, `Store7`) and is a nominal label rather than a quantity; several price columns are exact arithmetic functions of the others. Neither fact decides itself. Argue your feature set in a paragraph before you fit anything.
2. **Build the most accurate model you can** using Chapter 8: a single tree, **bagging**, a **random forest**, and **gradient boosting** at a minimum. Tune the hyper-parameters that matter by **cross-validation inside the training set** (Chapter 5). Report each candidate's cross-validated accuracy *and* the fold-to-fold spread.
3. **Build the most interpretable model you can defend.** A tree small enough to fit on one slide and be read aloud is the obvious candidate — choose its size by cross-validation and **draw it**, every split legible. Chapter 4 also contains models you can read a coefficient off; fitting one costs two lines and tells you whether the tree is genuinely the best *readable* option you have. Put it in the same table.
4. **Rank the variables — then split the ranking in two.** One list of variables that merely **describe** the customer, one of variables the manager can **change next quarter**. Quantify what happens when something in the second list moves, and **for whom**: the answer is not the same for every customer, and locating the customers for whom the lever does nothing is worth as much to her as locating the ones for whom it works.
5. **Evaluate once, on the held-out set**, and state the accuracy gap between your best model and your interpretable one **in percentage points**.
6. **Recommend one model for deployment** and defend the trade-off. Take a position. "Both have merits" is not a recommendation, and the manager cannot act on it.

## Rules

- **The held-out test set is defined for you** in the starter notebook — a stratified 75/25 split at `random_state=2024`, 268 test purchases. Do not re-split it, do not change the seed, and **do not look at it until requirement 5.** All tuning and model choice happens by cross-validation or a validation split carved out of the *training* data. Every student's headline number is then computed on the same 268 purchases and is directly comparable.
- If your answer to requirement 1 is that columns should be dropped, drop them from **copies** of the supplied `X_train` / `X_test`. Re-splitting breaks the comparability the seed exists to guarantee.
- **Score with the notebook's `evaluate()` helper**, once per model, so that everyone's accuracy is computed identically. Print `results_table()` in the memo.
- The **baseline** — the manager's current rule of thumb, "most people buy Citrus Hill" — is computed for you in the starter. A model that does not beat it earns her nothing, and reporting that clearly is a legitimate result, not a failure.
- Anything in the course is allowed. Anything outside it must be justified in one sentence, and nothing outside `numpy`, `pandas`, `matplotlib`, `statsmodels`, `scikit-learn` and `pygam` is needed.

## What you must report

| # | Required in the memo |
|---|---|
| 1 | The **comparison table**: every model you fitted, with its test accuracy and the share of Minute Maid buyers it finds — baseline row included. |
| 2 | The **cross-validated** accuracy and fold-to-fold spread for the Chapter 8 candidates, from the training set only. |
| 3 | Your interpretable model **drawn or printed in full**, readable as it stands, with the size-selection criterion named. |
| 4 | The **two variable lists** — descriptive and actionable — in importance order, with the evidence for the ranking. |
| 5 | For at least one actionable variable: the **effect size**, and the customers for whom it is largest and smallest. |
| 6 | The **accuracy gap** between your best and your interpretable model, in percentage points, set against the fold-to-fold spread of requirement 2. |
| 7 | The **recommendation** — one model, named — and the accuracy you are knowingly giving up to make it. |
| 8 | **Caveats.** Prices in this data were set by the stores, not assigned by you. Choose your verbs accordingly. |

## How this is judged

| | Weak | Solid | Strong |
|---|---|---|---|
| **Evaluation** | Test set used while choosing models; accuracy reported from the data it was tuned on | One clean final evaluation; baseline included | As solid, plus the gap read against fold-to-fold spread — knows how much of a 3-point difference 268 observations can support |
| **Interpretability** | Asserts a model is "interpretable" without showing it | Tree drawn, size chosen by CV, gap stated in percentage points | Notices that a tree is not the only readable model in the course, and tests the alternative before conceding anything |
| **Variables** | Reports the top of an importance ranking and stops | Separates description from action | States plainly that the strongest predictor is the least useful one to a manager, and re-frames the analysis around what she can actually change |
| **Effect sizes** | "Discounts increase Minute Maid sales" | One quantified effect | Effect quantified *by customer segment*, including a segment where the money is wasted |
| **The recommendation** | Hedges; recommends both | Recommends one, with the cost stated | Recommends one, states the cost, and names the condition under which the answer would flip |
| **Honesty** | Overstates a small difference as a finding; describes an observational association in causal verbs | Caveats present | A **correct negative result is marked above an overstated positive one** — "the expensive model is not reliably better than the simple one, and here is the evidence" is a first-class answer in this course, provided the evidence is there |

## Getting started

Open `project_4_starter.ipynb`. It loads the data, shows the two properties of the columns that shape requirement 1, defines the held-out split, computes the baseline, and provides `evaluate()`. Your work begins at **Step 1**; add code cells under the headings.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_4_oj/project_4_starter.ipynb)

`SOLUTION_NOTES.md` in this folder is published alongside the brief, as this course's policy is. Read it **after** your attempt — reading it first turns a five-hour exercise into a twenty-minute one and teaches you nothing.

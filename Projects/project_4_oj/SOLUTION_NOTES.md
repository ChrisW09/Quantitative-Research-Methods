# Project 4 — solution notes

> **Read this after your attempt.** These notes are published together with the brief, as this course's policy is; the discipline of trying it first is left to you. Reading them before you have fitted anything converts a five-hour exercise into a twenty-minute one and teaches you nothing.

All numbers below were produced on the split the starter defines — stratified 75/25, `random_state=2024`, 802 training and **268 test** purchases, target `Purchase == 'MM'`, predictors one-hot encoded with `drop_first=True`. Model seeds are `random_state=2024` throughout. They are reproducible, not illustrative.

---

## 1. What a good answer finds

### The comparison table

| Model | Test accuracy | MM buyers found | Errors / 268 |
|---|---|---|---|
| Baseline — always Citrus Hill | **61.2 %** | 0.0 % | 104 |
| One split on `LoyalCH` alone (`max_depth=1`) | 82.8 % | 74.0 % | 46 |
| Decision tree, `max_depth=3` | **82.8 %** | 79.8 % | 46 |
| Decision tree, CV-pruned (`ccp_alpha = 0.004`, depth 4, **7 leaves**) | **86.2 %** | 76.0 % | 37 |
| Bagging, 300 trees | 83.6 % | 76.0 % | 44 |
| Random forest, 500 trees (`max_features='sqrt'`) | 83.2 % | 73.1 % | 45 |
| Random forest, 500 trees, `max_features=12` | 84.7 % | 76.9 % | 41 |
| **Gradient boosting, sklearn defaults** | **86.6 %** | 77.9 % | 36 |
| Gradient boosting, store columns dropped | 86.6 % | 77.9 % | 36 |
| Gradient boosting, store one-hot encoded | **87.3 %** | 78.8 % | 34 |
| Gradient boosting, `LoyalCH` dropped | 73.1 % | 51.9 % | 72 |
| Logistic regression (standardised) | **86.6 %** | 75.0 % | 36 |
| Linear discriminant analysis | 86.6 % | 76.0 % | 36 |
| KNN, k = 25 (scaled) | 82.1 % | 67.3 % | 48 |

Bagging is the one row that is seed-sensitive: `random_state=2024` gives 83.6 %, but 0 and 1 give 84.7 % and 42 gives 85.1 %. If a student reports 84–85 % for bagging they have not made an error — they have found the point of §1.3 below.

### The headline result

**A depth-3 tree that fits on one slide reaches 82.8 % against gradient boosting's 86.6 % — a gap of 3.7 percentage points, or ten of 268 purchases.** That is the trade-off the brand manager is being asked to accept, and it is small enough to be worth stating to her honestly rather than managed around.

**And it shrinks to almost nothing if the tree is pruned properly.** Choosing `ccp_alpha` by ten-fold cross-validation on the training set gives a **seven-leaf** tree at **86.2 %** — within **0.4 pp** of the boosted ensemble, thirty-seven errors against thirty-six. A student who fixes `max_depth=3` because the Chapter 8 lab did and never prunes by cross-validation *overstates the cost of interpretability by an order of magnitude*. The seven-leaf tree, in full:

```
|--- LoyalCH <= 0.483
|   |--- LoyalCH <= 0.276                      -> MM
|   |--- LoyalCH >  0.276
|   |   |--- SalePriceMM <= 2.040              -> MM
|   |   |--- SalePriceMM >  2.040              -> CH
|--- LoyalCH >  0.483
|   |--- LoyalCH <= 0.765
|   |   |--- ListPriceDiff <= 0.235
|   |   |   |--- PriceDiff <= 0.015            -> MM
|   |   |   |--- PriceDiff >  0.015            -> CH
|   |   |--- ListPriceDiff >  0.235            -> CH
|   |--- LoyalCH >  0.765                      -> CH
```

That is readable aloud in thirty seconds, and it is 0.4 pp behind the best model in the project. The correct recommendation is to deploy it.

**What separates the strongest answers from the rest is not which model they choose.** It is that they *quantify the trade-off in percentage points* — 3.7 pp at a fixed depth of 3, 0.4 pp once the tree is pruned by cross-validation, against a 2.1 pp standard error — and then **take a position**. Either recommendation can be defended on those numbers. What cannot be defended is the hedge: "the ensemble is more accurate but the tree is more interpretable, so it depends on the manager's priorities" restates the question the manager asked and answers nothing. She has to decide something on Thursday; so must the memo.

### The gap is not statistically distinguishable

Three separate pieces of evidence, any one of which earns the top rubric band:

1. **Binomial standard error.** At 86.6 % on 268 observations the standard error is **2.1 pp**. The 3.7 pp gap to the depth-3 tree is under two standard errors of a single one of the two numbers.
2. **McNemar on the paired predictions.** The depth-3 tree is right where boosting is wrong 10 times; boosting is right where the tree is wrong 20 times. **p = 0.099.** The best ensemble in the project does not significantly outperform a tree you can read aloud.
3. **The ranking does not survive resampling.** Mean test accuracy over twenty stratified 75/25 splits (`random_state = 0…19`):

   | Model | Mean accuracy | SD across splits |
   |---|---|---|
   | Logistic regression | **82.7 %** | 1.6 pp |
   | Gradient boosting | 81.3 % | 2.2 pp |
   | CV-pruned tree | 81.3 % | 1.8 pp |
   | Tree, `max_depth=3` | 80.8 % | 2.0 pp |
   | Bagging, 300 trees | 79.4 % | 2.1 pp |
   | Random forest, 500 trees | 78.6 % | 2.2 pp |

   Five-fold CV *inside* the training set of the project split agrees: logistic regression 81.8 % (± 2.4), depth-3 tree 79.6 % (± 3.4), boosting 79.4 % (± 3.2), random forest 76.7 % (± 2.8). **On average across splits the ensembles do not beat the interpretable models at all, and the random forest and bagging are reliably the worst things in the table.** `random_state=2024` is simply a split on which boosting does well.

So the honest finding is stronger than "the trade-off is small": **on this data there is no reliable trade-off to make.** A student who reaches that conclusion *with this evidence* has written the best possible answer. A student who asserts it without the resampling or the test is guessing correctly, which is not the same thing.

### The actionable finding the memo is really for

Importances from the boosted model: `LoyalCH` **0.757**, `PriceDiff` 0.080, `SalePriceMM` 0.034, `WeekofPurchase` 0.034, `ListPriceDiff` 0.031, then the store columns at 0.014 and below. The random forest agrees on the ordering (`LoyalCH` 0.556) and the standardised logistic coefficients agree on the direction (`LoyalCH` −1.75, then the discount and price-difference terms).

`PriceDiff = SalePriceMM − SalePriceCH`, so it is **negative when Minute Maid is the cheaper of the two on the shelf**. Cutting the full sample at the tree's own loyalty thresholds gives the table the brand manager should actually be shown:

| Customer's `LoyalCH` | n | MM share when CH is cheaper | MM share when **MM is cheaper** | Difference |
|---|---|---|---|---|
| ≤ 0.28 (barely loyal to CH) | 223 | 88.6 % | 85.4 % | **−3.2 pp** |
| 0.28 – 0.48 | 178 | 55.5 % | 80.0 % | **+24.5 pp** |
| 0.48 – 0.77 | 319 | 21.1 % | 54.9 % | **+33.8 pp** |
| > 0.77 (strongly loyal to CH) | 350 | 3.8 % | 6.8 % | **+3.0 pp** |

The lever works in the middle. The 350 strongly loyal Citrus Hill customers — a third of the sample — buy Minute Maid 6.8 % of the time even when it is cheaper; discounting to them is money spent to move three percentage points. The 223 least loyal buy Minute Maid about 87 % of the time whatever the price; discounting to them is a rebate on a sale that was already happening. **The budget belongs to the 497 customers in the middle two bands, where undercutting Citrus Hill moves the Minute Maid share by 25 to 34 points.** The corresponding promotion figures are that the MM share is 58.4 % in weeks with an `SpecialMM` against 35.2 % without, and 48.8 % when `DiscMM > 0` against 34.7 % when it is zero.

That paragraph is the project. It is reachable from the seven-leaf tree alone — the tree's own structure says price matters only in the middle two loyalty bands and is absent from both extremes — which is precisely the argument for deploying the tree.

### The store-identity question

`STORE` is `StoreID` with store 7 relabelled 0, and `Store7` is `StoreID == 7`: three encodings of one nominal label, all treated as numbers by default, so a tree may split on `StoreID <= 2.5` as though store 3 were larger than store 2. Sixteen numeric predictors carry a matrix rank of **12** — four exact linear dependencies among the price columns as well. Dropping all three store columns changes boosting's accuracy by **exactly nothing** (86.6 % either way, the same 36 errors); one-hot encoding `StoreID` properly instead is the only variant that beats the headline model (**87.3 %**). Any of the three positions is defensible if the student measures it. What is not defensible is leaving `StoreID`, `STORE` and `Store7_Yes` in as integers without noticing that they are one variable counted three times, and then reading "store" importances off the result.

---

## 2. The trap

**`LoyalCH` dominates every model, and "brand loyalty predicts brand choice" is true, useless, and very nearly tautological.** The variable is a running measure of the customer's propensity to buy Citrus Hill; using it to predict whether the customer bought Citrus Hill is close to predicting a thing with a smoothed version of itself. The numbers that expose it:

- A **single split** on `LoyalCH` at 0.483 — the whole model is "loyalty above one half, predict Citrus Hill" — scores **82.8 %**, exactly matching the depth-3 tree with all seventeen predictors available, and coming within **two** errors of 300-tree bagging (83.6 %) and **one** error of a 500-tree random forest (83.2 %).
- Dropping `LoyalCH` entirely drops boosting from 86.6 % to **73.1 %** and its MM recall from 77.9 % to 51.9 %.
- `LoyalCH` takes **0.757** of the boosted model's total importance; everything the manager can act on shares about 0.15 between it.

**How to tell whether a student fell in.** They fell in if the memo's finding is "customer loyalty is the strongest predictor of brand choice", with the price and promotion columns mentioned only as also-rans, and with no recommendation the manager could act on. That answer is *arithmetically correct and commercially worthless*: **the manager cannot change a customer's loyalty score next quarter, but she can change a price on Thursday.** They avoided it if the memo separates description from action, and spends its space on `PriceDiff`, `DiscMM` and `SpecialMM` — the small-importance, high-actionability columns — despite their being the *less* impressive part of the importance ranking.

The deeper form of the same point: a model whose accuracy comes almost entirely from `LoyalCH` is a model that describes the market's current state rather than one that predicts a response to intervention. The single split on `LoyalCH` is the honest summary of what 86.6 % accuracy actually contains.

---

## 3. Common wrong turns

1. **Fixing `max_depth=3` because the lab did, and calling the resulting 3.7 pp gap the cost of interpretability.** *Prune by cross-validation before you price interpretability: `ccp_alpha` chosen on the training set gives seven leaves at 86.2 %, and the cost falls from 3.7 pp to 0.4.*
2. **Treating the ranking of the ensembles as a finding.** Boosting beats the forest by 3.4 pp on this split, and loses to plain logistic regression on **15 of 20** other splits. *With 268 test observations a standard error is 2.1 pp, so any gap under about 4 pp needs a resampling argument before it can be called a difference.*
3. **Assuming the ensemble must win because it is the more sophisticated model.** Bagging and the random forest are the *worst* non-trivial models in the twenty-split table (79.4 % and 78.6 %), below a seven-leaf tree. *When one predictor carries three-quarters of the signal, restricting each split to √17 ≈ 4 candidate features throws away the only column that matters in most trees — which is why `max_features` is a hyper-parameter and not a constant: raising it to 12 lifts the forest from 83.2 % to 84.7 % on this split.*
4. **Selecting the model on the test set, then reporting its test accuracy.** Trying nine models and quoting the best one's held-out number makes it a training accuracy with extra steps. *Choose by cross-validation inside the training set; the test set is scored once, for the winner, after the choice has been made.*
5. **Writing "discounting Minute Maid increases its share by 34 points" without qualification.** Prices here were set by the stores, in weeks the stores chose, in stores whose customers differ; the loyalty bands are defined by a variable measured *before* the purchase, but the price variation is not randomised. *Say "purchases where Minute Maid was cheaper show a 34-point-higher Minute Maid share" and then say what would have to be true for the causal reading to hold — that is Chapter 13's discipline and `Chapters/Advanced/` A1's subject.*
6. **Reporting the accuracy of a model fitted with `Purchase` still in the design matrix, or with the `Store7` string un-encoded.** *If your accuracy is above 95 % you have leaked the target; the honest ceiling on this data is around 87 %.*

---

## 4. Marking guide

| Marks | Earned by |
|---|---|
| **25** | One clean final evaluation on the supplied split, baseline included, `evaluate()` used, all four Chapter 8 families fitted, hyper-parameters chosen by CV **inside** the training set with the fold spread reported. |
| **20** | The interpretable model built and **shown in full** — drawn or printed, every split legible — with its size chosen by cross-validation rather than assumed, and the gap to the best model stated in percentage points. |
| **20** | Variables separated into descriptive and actionable, with the explicit statement that the dominant predictor is the one the manager cannot act on, and at least one actionable effect quantified. |
| **15** | A single named recommendation with its accuracy cost, and the condition under which it would change. |
| **10** | Caveats: observational prices, one split's worth of evidence, `LoyalCH`'s near-circularity. Correct verbs. |
| **10** | Evidence that the gap is or is not real — binomial SE, McNemar, repeated splits, or CV spread. Any one suffices. |
| *Bonus 5* | The segment table, or any equivalent that finds a customer group where the promotion budget is wasted. |
| *Deductions* | −10 for a test-set-selected headline number. −10 for "loyalty predicts choice" as the memo's finding. −5 for causal verbs on observational price variation. −5 for a hedged recommendation. |

**A correct negative result outranks an overstated positive one.** A memo concluding "the ensembles are not reliably better than a seven-leaf tree on this data, here is the resampling evidence, deploy the tree" is a full-marks answer. A memo concluding "gradient boosting is the best model at 86.6 %, deploy it" is a lower-marks answer even though 86.6 % is the largest number in the table, because it treats 3.7 pp on 268 observations as a fact and asks the manager to accept an unexplainable model to buy it.

---

## 5. Extensions

1. **Explain individual predictions, not just the model.** The manager's objection — "I cannot explain this to my team" — is not really a request for a global importance ranking; it is a request to know *why this customer was flagged*. That is exactly what **`Chapters/Advanced/` module A2, Shapley values**, provides: a per-purchase decomposition of the boosted model's output into additive contributions from `LoyalCH`, `PriceDiff` and the promotion columns, so the accurate model can be defended one case at a time. Run A2's lab on the boosted model from this project and re-write the recommendation: if individual predictions can be explained, the argument for giving up 0.4 pp weakens considerably. This is the natural sequel to the project and the honest resolution of its central tension.
2. **Attach an honest uncertainty to each prediction** with **A3, conformal prediction** — a set-valued prediction that says "Minute Maid" only when the model is entitled to, and abstains on the middle loyalty band where the tree itself is nearly indifferent. That band is where the promotion budget goes, so knowing where the model declines to commit is commercially useful rather than academic.
3. **Take the causal question seriously.** The segment table is an association. **A1, randomised controlled trials**, is the design that would turn it into an effect: randomise the discount across stores and weeks for customers in the 0.28–0.77 loyalty band and measure the share directly. Write the one-paragraph design, with the sample size the 25-point effect would need.
4. **Fit the loyalty effect as a smooth function** rather than a step. `LoyalCH` enters the tree as three thresholds, but the segment table suggests a genuinely non-linear, saturating relationship. **A4, GLMs and splines**, with a spline in `LoyalCH` plus linear price terms, gives a model that is both smooth and fully interpretable — and on the twenty-split evidence above, a well-specified logistic model is the thing to beat.
5. **Change the loss.** Accuracy weights a lost Minute Maid buyer the same as a misdirected coupon. Ask what a coupon costs and what a converted customer is worth, choose the classification threshold that minimises expected cost instead of error count, and see whether the model ranking survives it.

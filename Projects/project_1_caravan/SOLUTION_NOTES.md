# Project 1 — solution notes

> Read this **after** you have written a memo of your own. The course releases
> worked solutions alongside the papers; the discipline of attempting the problem
> first is left to you, and it is the part that does the teaching.

Every number below was produced on the fixed split defined in the starter —
`np.random.default_rng(2024).permutation(5822)`, first 4,000 rows train, the
remaining 1,822 test — and re-verified before this file was written.

---

## 1. The landscape

| | train | test (prospects) |
|---|---|---|
| rows | 4,000 | 1,822 |
| buyers | 231 | 117 |
| purchase rate | 5.78% | **6.42%** |

Whole data set: 348 buyers out of 5,822 = **5.98%**.

The random baseline is therefore **32.1 expected sales from 500 calls**, sd 5.5,
with 95% of random campaigns landing in **[22, 44]** sales. At €10 per call and
€200 per policy the break-even hit rate is **5.0%**, so a random campaign earns
about **+€1,420** — barely worth the agents' time. Everything of value in this
project is in the ordering.

## 2. What a good answer finds

A standardised, moderately regularised logistic regression is the reference
answer. `Pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=2000))`,
fitted on the 4,000 training rows and used to rank all 1,822 prospects, gives:

| calls | sales | hit rate | lift | profit |
|---|---|---|---|---|
| 100 | 21 | 21.0% | 3.27× | +€3,200 |
| 250 | 46 | 18.4% | 2.87× | +€6,700 |
| **500** | **70** | **14.0%** | **2.18×** | **+€9,000** |

Test AUC 0.728. Against the baseline's 32 sales, the ranking finds **more than
twice as many buyers for the same 500 calls**, and turns a marginal campaign
(+€1,420) into a clearly profitable one (+€9,000).

**A student anywhere in the range 60–80 sales (12–16%, lift 1.9–2.5×) has done
the job.** The exact figure depends on defensible choices, and the spread across
reasonable methods is real:

| ranker | top-500 sales | hit rate | lift | test AUC |
|---|---|---|---|---|
| Gradient boosting (500 trees of depth 2, lr 0.01) | 79 | 15.8% | 2.46× | 0.784 |
| Logistic regression, `C = 0.01` (stronger ridge) | 77 | 15.4% | 2.40× | 0.752 |
| Logistic regression, L1, `C = 0.1` | 74 | 14.8% | 2.30× | 0.755 |
| Gaussian naive Bayes | 71 | 14.2% | 2.21× | 0.717 |
| Random forest (500 trees) | 71 | 14.2% | 2.21× | 0.731 |
| **Logistic regression, `C = 0.1`** | **70** | **14.0%** | **2.18×** | **0.728** |
| LDA | 69 | 13.8% | 2.15× | 0.740 |
| KNN, k = 100, scaled | 69 | 13.8% | 2.15× | 0.713 |
| Logistic regression, `C = 1` (near-unpenalised) | 65 | 13.0% | 2.02× | 0.706 |
| KNN, k = 25, scaled | 57 | 11.4% | 1.78× | 0.667 |
| KNN, k = 5, scaled | 54 | 10.8% | 1.68× | 0.597 |
| KNN, k = 5, **unscaled** | 50 | 10.0% | 1.56× | 0.591 |
| random | 32 | 6.4% | 1.00× | 0.500 |

Two things are worth noticing in that table. **Every** method beats random, so
the project is winnable with almost any honest effort — but the range from KNN-5
to boosting is 50 to 79 sales, a €5,800-versus-€10,800 difference on the same
budget, so the model-selection step is where the marks are. And **more
regularisation helps**: with 85 predictors and 231 training buyers, `C = 1` is
already overfitting relative to `C = 0.01`.

### The cross-validated estimate agrees with the held-out result

This is the part worth dwelling on, because it is Chapter 5's whole claim. Doing
5-fold `StratifiedKFold` on the **training set only**, scoring each fold by the
hit rate in its top 27.4% (= 500/1,822, the same selection depth), gives:

| ranker | CV top-27.4% hit rate | CV lift | realised test lift |
|---|---|---|---|
| Gradient boosting | 13.4% | 2.31× | 2.46× |
| Logistic, `C = 0.01` | 12.4% | 2.14× | 2.40× |
| Logistic, `C = 0.1` | 12.1% | 2.09× | 2.18× |
| Logistic, `C = 1` | 11.7% | 2.03× | 2.02× |
| LDA | 11.7% | 2.03× | 2.15× |
| KNN, k = 100 | 10.3% | 1.78× | 2.15× |
| KNN, k = 5 | 9.1% | 1.57× | 1.68× |

The CV ordering reproduces the test ordering almost exactly, and the CV lift
predicts the test lift to within about 0.2×. A student who cross-validated
properly could have written down, *before* breaking the seal, "expect a lift near
2.1×, so 2.09 × 6.42% × 500 ≈ **67 sales**" — and been right to within three. That pre-registration, compared with
the realised 70, is worth more than either number on its own — say so when
marking.

### The interval

Two routes, and they answer different questions. Both are correct; quoting one
while claiming the other's meaning is not.

- **Route 1 — variation in the outcomes of these 500 calls.** Treat the 500
  called prospects as Bernoulli trials at the realised 14.0%. Clopper–Pearson
  gives **[11.1%, 17.4%]**, i.e. **[55, 87] sales**; a nonparametric bootstrap of
  the 500 outcomes gives **[55, 85]**. This is the interval to quote to a
  marketing team asking "how confident are you in the 70?"
- **Route 2 — variation in the ranking itself.** Bootstrap the 4,000 training
  rows, refit, re-rank the same prospects, recount: mean **66.5** sales, sd
  **3.5**, 95% **[59, 73]**. This is *narrower*, because it holds the prospect
  list fixed and varies only the model.

Neither interval alone answers the question the team will actually ask next
quarter — *how many sales from a different 500 prospects?* — because that
involves both sources of variation plus drift in the population. A strong answer
says so. Route 1 is the safer thing to put in the memo; **[55, 87]** is the
reference interval.

### The budget-100 paragraph

Cutting the budget to 100 calls **raises the hit rate and lowers the total
profit**, and the good answers see both halves:

| | 100 calls | 500 calls |
|---|---|---|
| sales | 21 | 70 |
| hit rate | 21.0% | 14.0% |
| lift | 3.27× | 2.18× |
| total profit | +€3,200 | +€9,000 |
| profit **per call** | +€32.0 | +€18.0 |

Concentration works — the top of the ranking is genuinely richer, and the first
100 names convert at three times the base rate. So the answer to "would the first
100 names be the right 100?" is **yes**: the same ranking, truncated, is the
optimal 100, and no refitting is needed. But the campaign earns €5,800 *less*.
The instructive point is that **the ranking answers "whom to call", not "how many
to call"**: the second question is answered by comparing the *marginal* call's
expected value (the hit rate in the block of prospects around depth *k*, × €200)
against its €10 cost. On the reference ranking, in blocks of 200:

| ranks | marginal hit rate | value per call | cumulative profit at that depth |
|---|---|---|---|
| 1–200 | 19.0% | €38 | +€5,600 at k = 200 |
| 201–400 | 10.5% | €21 | +€8,400 at k = 400 |
| 401–600 | 8.5% | €17 | +€8,800 at k = 600 |
| 601–800 | 5.5% | €11 | +€9,100 at k = 800 |
| 801–1000 | 4.5% | €9 | +€9,200 at k = 1000 |
| 1001–1200 | 4.0% | €8 | +€9,000 at k = 1200 |

The marginal call stops paying for itself somewhere around **rank 800**, and
total profit is essentially flat between 500 and 1,000 calls (+€9,000 to
+€9,200). So an excellent answer notices that **500 was a constraint, not an
optimum** — the budget could be roughly doubled at no loss and a little gain —
while also noting that these block estimates rest on 200 prospects each and are
too noisy to locate the optimum precisely. Cutting to 100 calls, by contrast,
leaves €5,800 of clearly profitable calls unmade.

---

## 3. The trap: **accuracy is a useless metric here**

Predicting "No" for all 1,822 prospects scores **93.58% accuracy** and sells
nothing. That is the trap, and it is not hypothetical — it is what the obvious
pipeline actually does. Take the reference logistic regression and classify at
the default 0.5 threshold:

```
              predicted No   predicted Yes
actual No             1701               4
actual Yes             116               1
```

- accuracy **93.41%** — *worse* than the do-nothing model's 93.58%
- **5** customers predicted to buy, of whom **1** actually did
- sensitivity **0.85%**: the model misses 116 of 117 buyers
- the 500th-highest predicted probability is **0.074** — no sensible threshold
  above 0.5 will ever select 500 people

The model is not broken. It ranks well: its top 500 contains 70 of the 117
buyers. Thresholding at 0.5 simply throws that ranking away, because 0.5 is the
right cut-off only when a false positive and a false negative cost the same
amount — and here a false positive costs €10 while a false negative costs €190 of
forgone margin. **The decision fixes the metric, and the metric here is the hit
rate at depth 500.**

### How to tell whether a student fell in

Look for any of these, in rough order of severity:

1. A confusion matrix at 0.5 accompanied by a sentence like *"the model predicts
   almost no purchases, so it is not useful"*, or *"accuracy is 93%, so the model
   works well"*. Either sentence is the trap, from opposite directions.
2. `cross_val_score(...)` with no `scoring=` argument — that is accuracy — used
   to choose between models. All candidates will score ≈94% and the comparison
   will be noise. This is the commonest form, and it is easy to miss because
   nothing errors.
3. A shortlist shorter than 500 because the student took everyone above a
   threshold rather than the top 500 of a ranking. `evaluate_shortlist()` raises
   on this, so it should not survive to the memo — but the *reasoning* behind it
   often does.
4. No baseline in the memo. Without the 6.4% comparison, "14% of the people we
   called bought a policy" is uninterpretable.
5. Class rebalancing (`class_weight='balanced'`, SMOTE, undersampling) presented
   as *the* fix for the imbalance. It is a fix for a thresholding problem the
   student did not have to have: it shifts the probabilities but barely changes
   their **order**, and the order is all that matters. Concretely, adding
   `class_weight='balanced'` to the reference model raises the number of
   0.5-threshold positives from 5 to **641**, which looks like a dramatic repair
   — while the ranking barely moves (Spearman ρ = **0.97** with the unbalanced
   scores, **452 of the same 500** prospects shortlisted) and the result gets
   marginally *worse*: **68 sales, 13.6%, lift 2.12×**. A student who reports a
   large improvement from rebalancing alone has measured something other than
   what they think.

A student who never computes an accuracy at all, and goes straight from "500-call
budget" to "rank and take the top 500", has understood the project.

## 4. Common wrong turns

**"I used my own `train_test_split(random_state=42)`."**
Then your number is not comparable with anyone else's and the cohort-wide
baseline no longer applies to your list; the seeded split in the starter exists
precisely so that 70 means the same thing in every memo.

**"I standardised before splitting."**
Fitting `StandardScaler` on all 5,822 rows lets the test set's means and standard
deviations into the training procedure; put the scaler inside a `Pipeline` so
that every cross-validation fold rescales using only its own training part.

**"KNN with k = 5 gave me a ranking, so I used it."**
With five neighbours a prospect can only score 0, 0.2, 0.4, 0.6, 0.8 or 1.0 — on
this test set just 479 prospects score above zero, so 21 of your 500 names are
drawn arbitrarily from the 1,343 people tied at exactly 0.0, and re-running with
a different tie-break moves the result between 52 and 58 sales. **A ranking is
only as fine-grained as the scores that produce it**: check `len(np.unique(p))`
before trusting an ordering of 500 people.

**"I compared models by AUC, which is the ranking metric."**
Better than accuracy, and it will get you to roughly the right model — but AUC
summarises the ordering over the *whole* list, including the 1,300 prospects you
will never call, whereas your decision depends only on the top 27%. Here the two
happen to agree; say that you checked, rather than assuming it.

**"I tried several models on the test set and reported the best."**
Then the reported figure is the maximum of several noisy estimates and is biased
upward — the honest quantity is the one you would have got from the model chosen
*before* looking. Choose on the training set with cross-validation, then evaluate
once; if you did evaluate more than once, the memo must say how many times.

**"I reported 70 sales."**
A point estimate with no interval invites a marketing team to treat it as a
promise. **[55, 87]** is the deliverable.

## 5. Marking guide

Suggested weights if the project is graded out of 100.

| | Marks | What earns them |
|---|---|---|
| **Framing the decision** | 15 | States that the deliverable is an ordering, not a classification, and names the quantity the decision depends on (hit rate at depth 500). Full marks require the *reason*: the asymmetry between a €10 call and €190 of forgone margin. |
| **Model construction** | 15 | Three or more Chapter 4 candidates, correctly fitted; scaling handled inside a pipeline; probabilities or scores used, not hard labels. |
| **Honest model selection** | 20 | Cross-validation on the training set only, scored on a criterion aligned with the decision. Deduct heavily for any selection made on the test set; deduct for default-accuracy scoring even where the winning model happens to be right. |
| **Held-out discipline** | 15 | Exactly 500 unique prospects, ties broken explicitly, one evaluation, and — for full marks — a pre-registered expectation from Step 4 compared with the realised result. |
| **Uncertainty** | 15 | An interval, correctly computed. Full marks only if the memo says which of the two sources of variation it captures and which it does not. |
| **The memo** | 20 | All eight required numbers present and mutually consistent; the baseline restated; the budget-100 paragraph gets both the higher hit rate *and* the lower total profit; at least two real deployment caveats. |

**The honesty premium.** A memo reporting a lift of 1.4× that the author's own
interval cannot separate from 1.0×, and which says so plainly, should score above
a memo claiming 2.5× on a number obtained by evaluating six models on the test
set. Reward the reasoning, not the leaderboard position. Conversely, a beautiful
2.4× that cannot be reproduced by re-running the submitted notebook earns
nothing — the number and the code that made it are one deliverable.

Deployment caveats worth credit: the data are a single Dutch cross-section from
the 1990s, so the base rate and the coefficients will both have drifted; the
prospects were not randomly assigned to be called, so the 14% is a hit rate among
*people we chose*, not a causal effect of calling them; a real campaign's contact
rate is well below 100%, so 500 dialled numbers is not 500 conversations; and
several of the strongest predictors are themselves product-ownership variables,
which will look different for a genuinely new prospect than for an existing
customer.

## 6. Extensions

- **Choose the budget, don't accept it.** Plot the marginal hit rate against
  depth *k* and find where the marginal call's expected value crosses €10. It
  happens near **rank 800**, and cumulative profit peaks around **+€9,200 at
  k ≈ 1,000** — so the constraint, not the model, is what limits this campaign.
- **A proper lift/gains curve.** Cumulative buyers captured against prospects
  called, with the random diagonal. It is the standard artefact of marketing
  analytics and it makes the whole memo legible on one axis.
- **Chapter 8 methods.** Boosted depth-2 trees reach 79 sales here (2.46×), the
  best of anything tried. Worth attempting once Lecture 8 is done, as a check on
  whether the extra flexibility survives honest cross-validation — it does,
  marginally.
- **Cost-sensitive learning.** Reformulate the objective as expected profit
  rather than hit rate, and optimise the ranker and the depth jointly instead of
  taking 500 as given.
- **Explaining *why* a prospect was ranked highly — `Advanced/` module A2
  (Shapley values).** This is the natural extension, and not merely a technical
  one: an insurer that targets customers must be able to justify the targeting,
  to a regulator and to the customer. Module A2
  ([`Advanced/advanced_02_shapley/advanced_02_shapley_lab.ipynb`](../../Advanced/advanced_02_shapley/advanced_02_shapley_lab.ipynb))
  gives you the machinery to decompose a single prospect's score into per-feature
  contributions that sum exactly to it, which is what a "reason code" on a call
  sheet has to be. Two warnings the module makes precise apply directly here.
  The `Caravan` predictors are strongly correlated — `PPERSAUT` and `APERSAUT`
  are the premium and the count of the same car policy — and Shapley values
  distribute credit across correlated features in ways that are easy to
  over-interpret. And a large contribution is an explanation of the *model*, not
  evidence about the customer. For the record, the reference model's largest
  standardised coefficients are `PPERSAUT` (+0.64, car-policy premium), `PBRAND`
  (+0.38, fire-policy premium) and `APLEZIER` (+0.32, boat policies) against
  `PLEVEN` (−0.30) and `MOPLLAAG` (−0.28, share of low-education households) —
  a coherent story about affluent multi-policy households with recreational
  vehicles, which is exactly the caravan-owning demographic. That the story is
  coherent is reassuring, not confirmatory.
- **Module A3 (conformal prediction)** is the other honest route to an interval,
  if you want one with finite-sample coverage guarantees rather than an
  asymptotic argument.

# Project 3 — solution notes

> **Read this after you have attempted the project, not before.** It is published
> alongside the brief, in keeping with the course's policy on worked solutions;
> the discipline of trying first is left to you. Every figure below was computed
> on `Weekly.csv` with the starter's split and seed, and can be reproduced.

---

## 1. What a good answer finds

All numbers refer to `Weekly.csv` (1,089 × 9), the split `Year <= 2008` for
training (n = 985) and 2009–2010 held out (n = **104**), predictors drawn only
from `Lag1`–`Lag5` and `Volume`, and 95 % Wald intervals as computed by the
starter's `wald_ci()`.

### The four numbers that carry the whole argument

| | Figure | 95 % interval |
|---|---|---|
| Majority class over the whole series (`Up`) | **55.6 %** (605 / 1,089) | — |
| Logistic regression, all six predictors, **fitted and scored on the same 1,089 weeks** | **56.1 %** (611 / 1,089) | — |
| Majority baseline on the held-out period ("always `Up`") | **58.7 %** (61 / 104) | [49.2 %, 68.1 %] |
| Logistic regression on **`Lag2` only**, trained ≤ 2008, scored 2009–2010 | **62.5 %** (65 / 104) | **[53.2 %, 71.8 %]** |

Read those four rows in order and the project is finished.

- The **56.1 %** is what the obvious approach produces: fit everything on
  everything, score on the same data. It beats the 55.6 % majority rate by
  half a percentage point. Even taken at face value — which it must not be,
  since no held-out data were involved — it is an announcement that there is
  almost nothing here.
- The **62.5 %** looks, at last, like a result: 3.9 points clear of the
  58.7 % baseline, on data the model had never seen.
- And then the interval. **[53.2 %, 71.8 %] contains 58.7 %.** The honest
  conclusion is that the rule **cannot be distinguished from "always predict
  `Up`"**. A binomial test of 65 correct out of 104 against the baseline rate of
  0.587 gives **p = 0.49**; McNemar's exact test against the always-`Up`
  predictions (9 weeks where the model is right and the baseline wrong, 5 the
  other way) gives **p = 0.42**. Two different tests, one answer: no.

### What happens as predictors are added

| Predictors | Held-out accuracy | 95 % interval |
|---|---|---|
| `Lag2` | **62.5 %** | [53.2 %, 71.8 %] |
| `Lag1` + `Lag2` | 57.7 % | [48.2 %, 67.2 %] |
| all six (`Lag1`–`Lag5` + `Volume`) | **46.2 %** | [36.6 %, 55.7 %] |

The six-predictor model is **worse than a coin flip** out of sample, and 16
points below the one-predictor model. This is Chapter 2's variance term made
visible: five of the six predictors carry no signal (on the full data only
`Lag2` reaches significance, p = 0.030; `Lag1` p = 0.118, the rest p > 0.29),
so each one contributes estimation variance and no reduction in bias. `Volume`
is worse than useless — it correlates **0.842** with `Year`, so the fitted
coefficient encodes a level that has moved on by 2009, and a model that
extrapolates a trend into a regime break is not merely noisy but wrong.

### The Chapter 4 comparison, `Lag2` only, on the fixed split

| Method | Held-out accuracy | 95 % interval |
|---|---|---|
| Logistic regression | 62.5 % | [53.2 %, 71.8 %] |
| LDA | **62.5 %** | [53.2 %, 71.8 %] |
| QDA | 58.7 % | [49.2 %, 68.1 %] |
| Gaussian naive Bayes | 58.7 % | [49.2 %, 68.1 %] |
| KNN, K = 25, scaled | 54.8 % | [45.2 %, 64.4 %] |
| KNN, K = 5, scaled | 52.9 % | [43.3 %, 62.5 %] |
| KNN, K = 1, scaled | 50.0 % | [40.4 %, 59.6 %] |

Three observations worth marks:

1. **Logistic regression and LDA agree exactly** — expected, since with one
   predictor both fit a monotone rule in `Lag2` and differ only in how the
   boundary is estimated.
2. **QDA's 58.7 % is not a coincidence: it predicts `Up` for all 104 weeks.**
   It has reproduced the baseline and nothing else. A student who reports QDA at
   58.7 % without noticing this has not looked at the confusion matrix.
3. **KNN degrades monotonically as K falls**, which is the flexibility axis of
   Chapter 2 traversed in a single table: at K = 1 the rule is pure variance and
   lands exactly on 50 %.

The 62.5 % model itself is barely a rule: it predicts `Up` in **90 of 104 weeks**
(confusion: 9 / 34 / 5 / 56 for TN / FP / FN / TP). It is the always-`Up`
baseline with fourteen exceptions, nine of which happen to be right. That is the
entire "edge".

### How much data would settle the question

The observed edge is 3.9 percentage points. Detecting an edge that size against
a 58.7 % baseline at 80 % power needs roughly **n ≈ 1,240 weeks — about 24 years
— of held-out data**, i.e. more out-of-sample history than the whole data set
contains. Note the contrast: tested against 50 %, an edge of 12.5 points needs
only ~120 weeks, which is why choosing the wrong yardstick makes the problem
look tractable when it is not. A strong memo makes this point.

### The recommendation

**Do not trade on this.** Not "the signal is weak" — the estimate is
statistically indistinguishable from a rule that ignores the data entirely, on
the only 104 weeks that were honestly held out. And that is before costs: a rule
that trades on 90 of 104 weeks pays the spread 90 times, against a nominal edge
of four percentage points on a coin-flip-sized payoff. A student who writes that
paragraph has produced the correct answer to the question the fund asked.

---

## 2. The trap

**Random k-fold cross-validation is invalid on this data set, and it is the
first thing a well-trained Chapter 5 student reaches for.**

The rows of `Weekly` are consecutive weeks. `KFold(shuffle=True)` scatters them,
so nine folds' worth of 1990–2010 — including weeks *after* the ones being
scored — train a model that then predicts the tenth. No trader has that
information. Whatever the number is, it is not an estimate of anything anyone
can earn, and the fund would be acting on a quantity that does not exist.

Two things make this trap unusually instructive here.

- The random-CV number is **not** conspicuously flattering, which is exactly why
  it slips through. Random 10-fold CV (seed 2024) reports **55.6 %** for `Lag2`
  and **54.5 %** for the six-predictor model. Neither looks like cheating. A
  student who reports 54.5 % and concludes "a modest signal" has produced a
  defensible-looking number that the honest time split contradicts by **eight
  points** — the same specification earns **46.2 %** in 2009–2010. The leak did
  not inflate the headline; it hid a catastrophic failure.
- The mechanism is visible in the starter's own first-look plot. `Volume` grows
  twentyfold across the series. In a shuffled fold, the model is told what
  `Volume` looks like in 2009 by rows from 2010; in reality it would have to
  extrapolate. The panel is in the starter for precisely this reason, and the
  brief's requirement 5 exists to force the student to connect the two.

**How to tell whether a student fell in.** Look for `KFold`, `cross_val_score`
with an integer `cv=`, `shuffle=True`, or `train_test_split` on `Weekly` with no
`shuffle=False`. Any of these, unremarked, is the trap. `cross_val_score(model,
X, y, cv=10)` is a subtler case: `KFold` does not shuffle by default, so the
folds are contiguous blocks — but folds 1–9 still train on the future when fold 0
is scored, so it is only *less* wrong, not right. The tell-tale sentence is a
reported CV accuracy that is never reconciled with the held-out number.

**What a defensible scheme looks like.** `TimeSeriesSplit`, or any expanding
window, only ever trains on weeks preceding the scored ones. On the training
years it gives **55.1 %** (`Lag2`, 5 splits) and **54.3 %** (all six) — both near
the majority rate, which is the honest signal-strength reading and agrees with
everything else in this document. Choosing K for KNN under `TimeSeriesSplit(5)`
selects K = 27 (held-out 52.9 %); under random 10-fold it selects K = 25
(held-out 54.8 %). The tuning choice barely matters — but only one of the two
procedures is a procedure a fund could have run in 2008.

**The second trap: treating 62.5 % as a win.** It is defused by the brief's hard
requirement that every accuracy carry a 95 % interval, because the interval and
the baseline overlap and there is then nowhere to hide. A student who reports
62.5 % bare, or who compares it with 50 % instead of 58.7 %, has fallen in. The
figure "62.5 % vs 50 %, p = 0.014" is the single most dangerous line a memo can
contain: the test is correct, the null hypothesis is the wrong one, and the
conclusion is false.

---

## 3. Common wrong turns

1. **`Today` among the predictors.** Accuracy jumps to **100 %** on the held-out
   period (99.6 % under random CV). *`Direction` is the sign of `Today`; a model
   given `Today` has been given the label, and the only thing it has learned is
   that you handed it the answer.* The starter's `check_predictors()` raises on
   this, so it should only survive if the student bypassed `evaluate()`.
2. **Scoring on the training data.** The 56.1 % figure. *A training accuracy
   measures how well the model memorised, not how well it will do next week;
   Chapter 5 exists because the two differ, and here the difference is the whole
   result.*
3. **Comparing against 50 %.** *The relevant null is not a coin, it is the
   cheapest rule that ignores the data: always predict `Up`, which is right
   58.7 % of the time in the held-out period. Beating a coin is not an edge when
   the market drifts upwards.*
4. **Reporting the accuracy without an interval.** *On 104 weeks a 95 % interval
   is ±9.6 points wide at each side; quoting a point estimate to three
   significant figures implies a precision the sample size cannot support.*
5. **Mining the held-out period.** Fitting all 63 non-empty predictor subsets and
   reporting the best gives 62.5 % (`Lag2`, `Lag2` + `Lag3`, `Lag2` + `Lag4`, and
   `Lag2` + `Lag3` + `Lag4` + `Lag5` all tie), while the median subset gets
   52.9 % and the worst 41.3 %. *Choosing the specification by its held-out score
   makes the held-out score a training score; the choice has to be made on the
   training years, and the number you report is then the one you get, not the one
   you liked best.*
6. **KNN without scaling.** `Volume` runs to 9.3 while the lags sit in ±5, so
   raw Euclidean distance is essentially the `Volume` axis. It happens not to
   change the story much here (unscaled K = 5 on all six gives 50.0 %, scaled
   51.0 %), *but the reason it does not is luck, and the standardiser must be
   fitted on the training years only — fitting it on all 1,089 weeks leaks the
   held-out period's mean and variance into training.*

---

## 4. Marking guide

Out of 100, if marks are wanted.

| Component | Marks | What earns them |
|---|---|---|
| Honest evaluation | 20 | Fits on the training years, scores 2009–2010 once through `evaluate()`, no leakage of `Today`, no scaler or selection step fitted on the held-out weeks. |
| The interval, and using it | 20 | A correct 95 % interval on every reported accuracy, **and** the recognition that [53.2 %, 71.8 %] contains 58.7 %. Full marks require the second half: the interval must be used, not merely printed. |
| Baseline comparison | 10 | Compares against 58.7 %, not 50 %; supports the verdict with a test or the interval. |
| Method comparison | 15 | Three or more Chapter 4 classifiers on the same split, tabulated with intervals; notices what QDA actually predicts. |
| Adding predictors | 15 | Reports 62.5 % against 46.2 % and explains the direction with the bias–variance decomposition; identifies `Volume`'s trend as the aggravating factor. |
| Resampling justified w.r.t. time | 10 | Either an expanding-window scheme with the reason stated, or an explicit argument that no resampling was used and why. Random shuffled folds with no comment: 0 for this component. |
| The memo | 10 | One page, all six required quantities present, a recommendation that follows from the numbers, at most three caveats. |

**Marking philosophy.** A memo concluding "do not trade" with the arithmetic that
forces it should score in the 80s or 90s. A memo concluding "a 62.5 % edge was
found, we recommend deployment" should not pass the interval component, however
clean the code — the point of the exercise is that the code was never the
difficulty. Conversely, do not penalise a student who *does* recommend a small
paper-traded pilot, provided they state that the evidence cannot distinguish the
rule from the baseline and frame the pilot as the way to collect the missing
1,200 weeks. That is a defensible reading of the same numbers.

---

## 5. Extensions

- **Direction is the wrong target.** Predicting the *sign* throws away the
  magnitude, and a fund is paid in returns, not in hit rates. Regress `Today` on
  the lags, then evaluate the strategy's cumulative return net of a plausible
  spread. The hit rate and the P&L can disagree, and it is instructive when they
  do.
- **The wrong loss function.** Accuracy weights a missed rally and a caught
  crash equally. Re-score with the ROC curve and AUC (Chapter 4.4.3), then pick
  a threshold that reflects the fund's actual asymmetry rather than 0.5.
- **Regime dependence.** Refit on `Year <= 1999` and score 2000–2001, then on
  `Year <= 2004` scoring 2005–2006, and so on. Whether "the" accuracy is stable
  across held-out windows is a more useful question for the fund than its value
  in any one window — and it is the honest version of cross-validation for a
  series.
- **Nonlinearity in the lags.** `Advanced/` module **A4 (GLMs and splines)**
  fits a logistic GAM: replace the linear term in `Lag2` with a smooth and ask
  whether the extra flexibility survives an honest split. It does not, which is
  itself the lesson.
- **Intervals without the normal approximation.** `Advanced/` module **A3
  (conformal prediction)** builds prediction sets with finite-sample validity,
  and raises the question this project only touches: what would it mean to
  abstain on the weeks where the model has no opinion? Compare also the Wilson
  interval for 65 / 104, [52.9 %, 71.2 %], and a 10,000-draw bootstrap,
  [52.9 %, 72.1 %] — all three overlap the baseline, so the conclusion does not
  turn on which interval was chosen.
- **The literature.** This is a miniature of the market-efficiency debate. The
  reason the professional version is hard is not that the models are more
  sophisticated but that the honest evaluation is, and that is what this project
  was about.

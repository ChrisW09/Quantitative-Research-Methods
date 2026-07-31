# Project 5 — Solution notes

> Read this **after** your attempt. The course publishes worked notes alongside the brief and
> leaves the discipline of trying first to you; reading these before you have produced your own
> five intervals costs you the only part of the exercise that transfers.

Every number below was computed on `Boston.csv` (506 × 13, loaded with `index_col=0` and then
re-labelled positionally with `reset_index(drop=True)`, so the index runs 0…505) with
`random_state=2024` throughout: `KFold(n_splits=5, shuffle=True, random_state=2024)` and
`train_test_split(X, y, test_size=0.2, random_state=2024)` — 404 training tracts, 102 held out.
Figures in $1,000s, rounded to the precision the data supports.

**Why the tracts are numbered from 0.** The starter's `load()` helper returns the `ISLP` package's
copy of `Boston` when ISLP is installed — which it is on Colab, because the setup cell installs it
— and the bundled CSV otherwise. The two frames hold the same 506 rows in the same order with the
same 13 columns, but ISLP labels them 0…505 while the CSV labels them 1…506. Naming the five
tracts by CSV label therefore selected *different rows* on Colab than locally, and the starter's
`assert all(t in X_test.index for t in FIVE_TRACTS)` failed outright. The starter now calls
`reset_index(drop=True)` immediately after loading, which makes the label the row's position on
both paths, and the five tracts are quoted by that position throughout. Every figure below is
unchanged by the re-labelling — same rows, so same numbers; only the labels moved (401 → 400,
113 → 112, 2 → 1, 297 → 296, 162 → 161).

---

## 1. What a good answer finds

### The reference figures (all 506 tracts, 5-fold CV)

| Model | CV RMSE | Per fold |
|---|---|---|
| Linear, all 12 predictors | **$4.92k** | 4.61, 5.07, 5.57, 5.25, 4.13 |
| `SplineTransformer(n_knots=5, degree=3)` on all predictors → OLS | **$4.58k** | 3.98, **6.87**, 4.62, 3.63, 3.79 |

Improvement **7.1%**. Both numbers reproduce exactly; a student whose figures differ has changed
the folds or the seed, or — on the CSV path, i.e. without `ISLP` installed — has forgotten
`index_col=0`, which leaves the tract id in as a thirteenth "predictor" (`Unnamed: 0`) and gives
$4.93k instead of $4.92k. That is a discrepancy small enough to be missed and worth catching, and
it is invisible on Colab, where `ISLP` supplies the frame and the id column never appears at all.

The per-fold column already carries the honest reading. The spline wins in **four of five folds**
and loses badly in the fifth (6.87 against 5.07). The mean improvement is real; the model is not
uniformly better. A student who reports only the mean has missed the most decision-relevant fact
in the table.

### Where the curvature lives

Nested $F$-tests against the full linear model (add $x^2$ and $x^3$ for one predictor at a time,
all 506 tracts, $F(2, 491)$):

| Predictor added as a cubic | $F$ | $p$ | $R^2$: 0.7343 → |
|---|---|---|---|
| `rm` | **80.45** | 6.0 × 10⁻³¹ | 0.7999 |
| `lstat` | **60.90** | 2.4 × 10⁻²⁴ | 0.7871 |
| `dis` | 20.53 | 2.7 × 10⁻⁹ | 0.7548 |
| `nox` | 1.20 | 0.30 | 0.7356 |
| `crim` | 0.36 | 0.70 | 0.7347 |

Both together, $F(4, 489) = 55.15$, $p = 2.3 \times 10^{-38}$, $R^2 = 0.8169$. **The curvature is
real and it is local**: overwhelming in `rm` and `lstat`, absent in `crim` and `nox`. That is the
finding the rubric's "strong" column is asking for — the blanket spline basis spends 84 basis
columns to buy what two predictors are responsible for, which is exactly why it collapses on one
fold (the basis matrix has condition number ~10²⁰).

### Model selection on the 404 training tracts (same folds)

| Candidate | CV RMSE (train) | Test RMSE |
|---|---|---|
| Null (training mean) | 9.00 | — |
| **Linear, all predictors — the baseline** | **4.89** | **4.61** |
| `log(lstat)`, rest linear | 4.36 | 4.06 |
| Blanket spline basis, all 12 predictors | 4.16 | 3.98 |
| Blanket spline basis + `RidgeCV` | 3.77 | 4.05 |
| Spline basis in `lstat` and `rm` only, rest linear | **3.83** | **3.86** |
| `log(lstat)` + `rm`, `rm²`, `rm³`, rest linear | 3.83 | 4.38 |

Two things students should notice. First, **targeting the flexibility beats spreading it**: a
spline basis in two predictors does better (3.83) than the same basis on all twelve (4.16), with
a 22-column design instead of 84, and no conditioning problem. Second, and more usefully for the
course's purposes, **a single `log(lstat)` — Chapter 3 material, one line — scores $4.36k on the
full-data folds, beating the entire Chapter 7 spline machine's $4.58k.** The nonlinearity is real;
most of it is one monotone transformation.

A good answer therefore lands at a test RMSE somewhere in **$3.8k–4.1k** against the linear
model's **$4.61k**: a genuine 12–17% improvement out of sample, arrived at with far less
machinery than the reference basis expansion.

### The five tracts

Linear baseline, fitted on the 404 training tracts, `statsmodels` `get_prediction`:

| Tract | Actual | Fit | 95% CI for the **mean** | width | 95% **PI** for one tract | width |
|---|---|---|---|---|---|---|
| 400 | 5.6 | 10.59 | [9.21, 11.96] | 2.75 | [0.92, 20.26] | 19.34 |
| 112 | 18.8 | 20.49 | [19.19, 21.79] | 2.60 | [10.83, 30.15] | 19.32 |
| 1 | 21.6 | 25.10 | [23.97, 26.22] | 2.25 | [15.46, 34.74] | 19.28 |
| 296 | 27.1 | 27.56 | [25.67, 29.45] | 3.78 | [17.80, 37.32] | 19.52 |
| 161 | **50.0** | 36.76 | [34.68, 38.84] | 4.16 | [26.97, 46.56] | 19.59 |

The confidence interval contains the truth for **1 of the 5**. The prediction interval contains it
for **4 of the 5** — and the one it misses is tract 161, the censored one.

A strong answer (spline basis in `lstat` and `rm`, rest linear, fitted with `statsmodels` so the
normal-theory interval comes for free):

| Tract | Actual | Fit | 95% CI | 95% PI | PI covers? |
|---|---|---|---|---|---|
| 400 | 5.6 | 9.04 | [7.19, 10.90] | [1.27, 16.82] | yes |
| 112 | 18.8 | 18.76 | [17.56, 19.96] | [11.11, 26.41] | yes |
| 1 | 21.6 | 23.78 | [22.77, 24.80] | [16.16, 31.41] | yes |
| 296 | 27.1 | 26.39 | [24.77, 28.02] | [18.67, 34.12] | yes |
| 161 | 50.0 | 45.45 | [42.17, 48.74] | [37.22, **53.69**] | yes |

Test RMSE 3.86; prediction intervals cover **97.1%** of the 102 held-out tracts at a mean width of
**$15.61k**; the confidence intervals cover **42.2%** at a mean width of $3.56k.

---

## 2. The trap

**A confidence interval for the mean response is not a prediction interval for one tract, and the
valuation office is asking for the second one.**

The office will be challenged on *tract 161* — a single census tract, whose median value is a
single number. That number is $\hat f(x_0)$ plus the irreducible tract-level noise $\epsilon$. A
confidence interval covers only the first term: it is an interval for $E[Y \mid X = x_0]$, the
average value of *all* tracts with tract 161's characteristics. It answers a question nobody
asked, and it answers it far too confidently.

Chapter 3's closing formula sheet ("Key formulas at a glance") puts the two side by side, and the
whole difference is the leading `1 +` under the square root:

$$\hat y_0 \pm t\,\mathrm{RSE}\sqrt{\tfrac{1}{n} + \tfrac{(x_0-\bar x)^2}{S_{xx}}} \quad\text{(CI, the mean)} \qquad\qquad \hat y_0 \pm t\,\mathrm{RSE}\sqrt{1 + \tfrac{1}{n} + \tfrac{(x_0-\bar x)^2}{S_{xx}}} \quad\text{(PI, one outcome)}$$

That `1 +` is the whole of $\sigma^2$, and here $\sigma$ dominates everything else: the fitted
model's RSE is **$4.87k**, so the prediction interval is essentially $\pm 1.96 \times 4.87 \approx
\pm 9.5$, near enough $19$ wide wherever you evaluate it, while the estimation error contributes
only 2–4. **The prediction interval is about six times wider** (mean 19.41 against 3.11 over the
five tracts; 19.47 against 3.41 over all 102).

### How to tell whether a student fell in

Three tells, in order of reliability.

1. **Width.** Five intervals of width 2–4 are confidence intervals. The correct answer is roughly
   13–19 wide, depending on the model. Nothing legitimate lands in between.
2. **The `evaluate_on_test` coverage line.** It reads **29.4%** for the linear model's confidence
   intervals and **96.1%** for its prediction intervals. A student reporting coverage near 30%
   against a nominal 95% has been handed the diagnosis by the scaffolding; what distinguishes a
   good student from a weak one at this point is whether they *investigated* it or reported it
   without comment. A memo that prints 29% coverage and still calls the interval defensible is the
   worst of the failure modes, and should be marked as such.
3. **The code.** `mean_ci_lower` / `mean_ci_upper` from `summary_frame()` is the CI;
   `obs_ci_lower` / `obs_ci_upper` is the PI. Students almost always take the first two, because
   they come first in the frame.

Note the trap is *seductive*, not silly: the narrow interval looks like a much better deliverable.
It is a more impressive-looking number that answers a question the office did not ask, and the
first appeal hearing exposes it. That is the lesson worth the three hours.

---

## 3. The censoring at $50k

`medv` **tops out at exactly 50.0**, and **16 of the 506 tracts (3.2%) sit precisely there** —
three of them in the held-out set, including tract 161. This is not a coincidence and it is not a
long tail: the variable is **censored (top-coded) at $50,000**, so a tract recorded at 50.0 is a
tract worth *at least* 50, and how much more the data cannot say.

Three consequences a good answer states:

- **The model must under-predict at the top, by construction.** Tract 161 is fitted at 36.8 by the
  linear model and 45.5 by the spline model, against a recorded 50.0. Neither is a modelling
  failure that more flexibility can repair — the training targets themselves were clipped.
- **Any interval whose upper end exceeds 50.0 should be flagged, not published as-is.** The
  strong model's interval for tract 161 is [37.22, 53.69]; 9 of the 102 held-out intervals run
  past 50. Above 50 the data has no information at all, so that part of the interval is an
  extrapolation from a boundary the sample never crosses. The honest wording for the office is
  "at least \$50,000; the data cannot resolve the upper end", not "\$53,700".
- **The linear model's prediction interval for tract 161, [26.97, 46.56], misses the truth
  entirely** — the only one of the five it misses. The censoring bites hardest exactly where the
  valuations are largest, which is where the appeals will come from.

`evaluate_on_test` reports the count of intervals whose upper end exceeds `MEDV_CAP` for this
reason. It is in the output; the marks are for noticing what it means.

---

## 4. Common wrong turns

1. **Reporting the confidence interval.** *The office is not asking what the average tract of this
   description is worth — it is asking what tract 161 is worth, so the interval must carry the
   tract-level noise $\sigma$ as well as the estimation error, which is the `1 +` in Chapter 3's
   prediction-interval formula.*

2. **Concluding "the data is nonlinear" from the 7% CV gap alone, then keeping the blanket
   spline.** *A 7% mean improvement that loses in one of five folds needs localising before it can
   be trusted: test the predictors one at a time, and you find $F = 80$ for `rm` and $F = 0.36$
   for `crim` — the flexibility is earned in two predictors, not twelve.*

3. **A spline basis that explodes, or errors, on the held-out tracts.** Two distinct versions.
   `SplineTransformer` on all twelve correlated predictors gives an 84-column design with
   condition number ~10²⁰, and unpenalised OLS on it is numerically unstable (that fold of 6.87;
   with a slightly different split it reaches 28). Separately, patsy's `bs(lstat, df=5)` raises
   `NotImplementedError: some data points fall outside the outermost knots` the moment you predict
   on test rows outside the training range. *Fix the first with a ridge penalty (Chapter 6) or by
   splining only the predictors that need it; fix the second by passing explicit
   `lower_bound`/`upper_bound` to `bs`, or by using `SplineTransformer`, which extrapolates.*

4. **Selecting the model on the test set.** Usually visible as several `evaluate_on_test` calls, or
   a chosen model that beats the baseline on test but not in training CV. *The held-out set can
   answer one question honestly; every additional look converts it into a validation set and the
   final number stops being an estimate of anything.*

5. **Reporting coverage of 29% without remark, or claiming a large win from a small one.** *The
   coverage line is the audit of your own claim: if you promised 95% and delivered 29%, the
   headline finding of the project is that your interval was the wrong interval, and the memo has
   to say so.*

6. **Treating the spike at 50 as an outlier and deleting it.** *Sixteen tracts at exactly the
   maximum is a top-coded variable, not sixteen data errors; dropping them throws away the
   expensive end of the market the office most needs valued, and biases every prediction there
   downwards even further.*

---

## 5. Marking guide

100 marks, if the professor chooses to grade it.

| Component | Marks | What earns them |
|---|---|---|
| Reference figures reproduced ($4.92k / $4.58k / 7.1%) | 10 | Both numbers, and a comment on the per-fold spread |
| Evidence that curvature is real | 20 | A statistic, not an assertion: nested $F$-test, CV gap, or a fitted smooth. Full marks require **localising** it — `rm` and `lstat` in, `crim` and `nox` out |
| Model selection on training folds only | 15 | A candidate table on shared folds; a sentence justifying the choice over the baseline; per-fold scores inspected |
| Five point estimates | 10 | Five numbers, from a model fitted on the 404 training tracts |
| Five intervals, **correct kind** | 25 | Prediction intervals, **named as such**, with the reason stated. A confidence interval, however well presented, scores at most 8 of the 25 — and 0 if the memo also claims it is defensible in a hearing |
| Held-out evaluation, one call, reported in full | 10 | Test RMSE, achieved coverage, mean width — including if unflattering |
| The censoring at 50.0 | 5 | One sentence identifying it as top-coding and drawing the consequence for the top of the interval |
| The memo | 5 | One page, numbers not adjectives, a recommendation and a caveat an officer could act on |

**Overriding rule.** A memo reporting "the flexible model improves CV RMSE by 7%, which is real but
modest, and I recommend the linear model because its interval is the one I can defend" — argued
with the evidence — outscores an unjustified claim of a large win. Conversely, a beautifully
executed 3.8 test RMSE reported with a 2.75-wide confidence interval called a valuation range
fails the central requirement of the brief, and the mark should show it.

---

## 6. Extensions

- **`Advanced/` module A3 — Conformal Prediction** is the natural next step, and it is a precise
  fit to this problem. The normal-theory prediction interval inherits every assumption of the
  model: homoscedastic, normal errors, and correct specification. None holds here — the errors
  fan out with the fitted value, and the target is censored, so the model is misspecified in a way
  no amount of flexibility repairs. **Split conformal** gives an interval with a *finite-sample,
  distribution-free coverage guarantee* that holds anyway: it needs only exchangeability, not a
  correct model. Calibrating inside the training tracts (a 70/30 split of the 404 — 282 to fit,
  122 to calibrate — gives $\hat q = 7.63$ for the blanket spline) yields intervals of width 15.25 with **96.1%**
  coverage on the held-out set; for the spline in `lstat` and `rm`, $\hat q = 6.61$, width 13.22,
  coverage 93.1%. Same discipline, no distributional promise — which is what a valuation office
  being cross-examined actually wants. A3 also covers **CQR**, which lets the interval widen where
  the market is volatile instead of carrying one width everywhere; here the constant-width normal
  interval is visibly too wide for cheap tracts and too narrow for expensive ones.
- **`Advanced/` module A4 — GLMs and Splines** formalises the Chapter 7 machinery this project
  leans on: penalised splines, effective degrees of freedom, and why a penalty is the principled
  answer to the ill-conditioned basis rather than the ad-hoc ridge used above.
- **The censoring, properly.** A **Tobit** model (or interval regression treating the 50.0 records
  as $[50, \infty)$) is the textbook treatment, and quantile regression at $\tau = 0.5$ is a robust
  alternative that does not assume a symmetric error at all. Either turns "we flag the top end" into
  a model that respects it.
- **Heteroscedasticity.** The errors are not of constant size: grouping the training residuals by
  quartile of fitted value gives residual standard deviations of 4.58, 3.05, 4.71 and **6.07** —
  largest at the expensive end, second-largest at the cheap end, smallest in the middle
  (Breusch–Pagan $p = 6 \times 10^{-6}$). One constant-width interval therefore over-covers the
  middle of the market and under-covers both ends, which is precisely where the five tracts the
  office cares about sit. Modelling $\log(\textit{medv})$ and back-transforming, fitting a variance
  model, or using CQR from A3, produces intervals that are narrow where the market is quiet and
  wide where it is not — more useful to the office than one width for all five tracts.

# Project 2 — solution notes

> **Read this after you have attempted the project.** In line with the course's policy these notes are published together with the brief, but the discipline of trying first is left to you, and there is nothing here you could not have found yourself. Reading it before you have a number of your own converts a three-hour exercise into a twenty-minute one and teaches you nothing.

Every figure below was produced on the exact split the starter defines — `train_test_split(test_size=0.30, random_state=2024)`, 543 training and 234 test colleges — and is reproducible to the dollar. Where a method has its own randomness, `random_state=2024`; `KFold(5, shuffle=True, random_state=2024)` throughout for cross-validation, and `LassoCV(cv=5)` with scikit-learn's default unshuffled folds.

---

## 1. What a good answer finds

### The four required RMSEs

| Model | Test RMSE | vs null | Test R² |
|---|---|---|---|
| Null — predict the training mean ($10,377) for all | **$4,165** | 1.00 | −0.003 |
| OLS, all 17 predictors — *the colleague's model* | **$2,120** | 0.51 | 0.740 |
| `RidgeCV` on standardised predictors (α = 24.2) | $2,140 | 0.51 | 0.735 |
| `LassoCV(cv=5)` on standardised predictors (α = 33.1, **12 non-zero**) | **$2,157** | 0.52 | 0.731 |
| Lasso at the one-standard-error rule (α = 218, 9 non-zero) | $2,229 | 0.54 | 0.713 |
| OLS on the **five** chosen by CV | **$2,255** | 0.54 | 0.706 |
| OLS on the five largest standardised lasso coefficients | $2,447 | 0.59 | 0.654 |
| *Extension:* OLS on all 17 with skewed predictors log-transformed | **$2,013** | 0.48 | 0.766 |
| *Extension:* the five, with `Expend` logged | $2,175 | 0.52 | 0.727 |
| *Extension:* `pygam` GAM on the five (smooths + factor) | $2,171 | 0.52 | 0.728 |

`sd(Outstate) = $4,023` over all 777 colleges. Note that this is **not** the same number as the null model's test RMSE of **$4,165**: the latter scores the *training* mean against a particular 234 held-out colleges, which happen to be a slightly more expensive and more dispersed set. Both figures are worth quoting; conflating them is a small error, but it is an error.

### The five variables

Forward stepwise selection scored by five-fold CV on the training set, and exhaustive best-subset over all C(17,5) = 6,188 five-variable models, **agree exactly**:

| Order added | Variable | Training CV RMSE |
|---|---|---|
| 1 | `Room.Board` | $2,919 |
| 2 | `Expend` | $2,490 |
| 3 | `Private` | $2,221 |
| 4 | `perc.alumni` | $2,098 |
| 5 | `PhD` | $2,014 |

That the greedy path lands on the globally best five is worth remarking on and is not guaranteed — a student who checks it has done real work.

One honest footnote on that table: the four-variable figure is $2,097.4981 here, so it prints as **$2,097** or **$2,098** depending on which BLAS rounds the last digit. Every other entry is stable well inside a dollar. A student reporting either is right; a student whose whole column differs has moved the seed or the split.

Fitted on the training set, in the units the board will read:

| Variable | Coefficient | Read aloud as |
|---|---|---|
| intercept | −3,220 | — |
| `Private` | **+2,831** | private institutions charge $2,831 more, all else equal |
| `Room.Board` | **+1.152** | $1,000 more in room and board goes with **$1,152** more tuition |
| `Expend` | **+0.204** | $1,000 more instructional spend per student goes with **$204** more tuition |
| `perc.alumni` | **+58.8** | each extra percentage point of alumni donating, **+$59** |
| `PhD` | **+44.6** | each extra percentage point of faculty holding doctorates, **+$45** |

All five are positive and all five are explicable to a lay audience without apology. That is not an accident of this data — it is the property that makes the small model publishable, and it is worth stating explicitly as a *finding*, not a convenience.

### The cost of the restriction

$2,255 − $2,120 = **$135** of RMSE. Three framings, all of which a strong answer gives:

- **3.2%** of the null model's error of $4,165.
- The full model closes $2,045 of the null's error; the five-variable model closes $1,910 — so five variables capture **93%** of everything seventeen achieve.
- A paired bootstrap of the test-set squared errors (5,000 resamples of the 234 colleges) puts the 95% interval for that $135 gap at **[−$27, +$299]**. It **includes zero.**

That last line is the answer. On 234 test colleges the penalty for going from seventeen variables to five is not statistically distinguishable from nothing.

### The recommendation

Publish the **five-variable model**. It costs a point estimate of $135 in RMSE — about 3% of the error a board member could make by quoting the national average — and that cost cannot be told apart from zero on the evidence available. In exchange the consortium gets five coefficients that all carry the sign a lay reader expects and can each be stated in one sentence.

**The caveat that must accompany it.** Everything above is *associational and cross-sectional*, from a 1995 snapshot. `Room.Board` is the single strongest predictor and is not a cause of tuition — it is another price set by the same institution in the same budget round, so the model tells the board what tuition *goes with*, not what would happen if a college changed something. A board that reads "+$204 per $1,000 of instructional spend" as a lever to pull has misread it. Any student whose caveat is instead about the sealed split, the sample size, or the age of the data has given a defensible answer; the causal one is the best.

---

## 2. The trap

**Students expect the lasso to win, because the course taught it after OLS. Here it does not.**

`LassoCV(cv=5)` on standardised predictors returns test RMSE **$2,157** against plain OLS's **$2,120** — it is *slightly worse*, and so is ridge ($2,140), and so is the lasso tuned by the one-standard-error rule ($2,229). No amount of careful tuning reverses this, because nothing is wrong with the tuning.

The reason is the bias-variance decomposition, applied honestly rather than recited. Regularisation buys a reduction in variance and pays for it in bias. With **n = 543** training observations and **p = 17** predictors, the least-squares fit has very little variance to give away: the ratio n/p is above 30, the design is well conditioned apart from one correlated block, and OLS is close to unbiased. Shrinkage therefore adds bias against almost no variance saving, and the net is a small loss. Ridge and lasso earn their keep when p approaches or exceeds n, when predictors are severely collinear, or when many coefficients are genuinely zero — none of which describes this data.

So the honest lesson is that **regularisation buys interpretability and stability, not accuracy**. What the lasso actually delivers here is a 12-variable model instead of a 17-variable one, coefficients that will barely move if the sample is redrawn, and an automatic ranking of importance — all for $37 of RMSE. That is a good trade for a consortium that has to explain itself. It is simply not the trade the student came expecting.

**A student who reports "the lasso was worse than OLS, and here is why" has produced the best possible answer to this project and deserves full marks** — better marks than one who reports the lasso winning, because on this split and this seed the lasso does not win, and a positive result that the data do not support is the failure mode this course exists to prevent.

The refinement that separates a very good answer from an excellent one: the same paired bootstrap applied to the lasso's $37 deficit gives a 95% interval of **[−$8, +$86]**, which also includes zero. So the precise claim is not "the lasso is worse" but **"the lasso is no better, and the difference is inside the noise"** — and by symmetry, a student who says the lasso is worse *and states this qualification* has understood the point completely. Note that the whole comparison sits inside a bootstrap interval of [$1,858, $2,415] for the full model's own RMSE: differences of $40 are being read off an estimate whose own uncertainty is ±$280.

### How to tell whether a student fell in

| Symptom | Diagnosis |
|---|---|
| Reports lasso test RMSE of $2,157 **and** OLS $2,120, concludes the lasso is better | Did not read their own table. Marks lost for the conclusion, not the code. |
| Reports only the lasso, having decided in advance it was the right method | Fell in. The all-seventeen OLS was a required number precisely to prevent this. |
| Quietly re-tunes — a different `cv`, a wider `alphas` grid, a shuffled fold seed — until the lasso wins, then reports that fit | Fell in, and worse: this is selection against the test set. The reported RMSE now estimates nothing. |
| Reports the lasso is not better, attributes it to n ≫ p, and quantifies the difference | Did not fall in. Full marks. |
| Concludes "regularisation does not work" | Half-fell in — overgeneralised from one dataset. The correct statement is conditional on n/p and on the conditioning of the design. |

### The second trap, for the strong students

The lasso's five largest standardised coefficients are `Private` (1,103), `Room.Board` (1,017), `Expend` (876), `Accept` (629) and `F.Undergrad` (−565) — with `perc.alumni` (536) a close sixth. It is very tempting to hand those five straight to the board. Do not: OLS on that set scores **$2,447**, some **$192 worse** than the CV-chosen five, and worse than every other model in the table.

Why? `Accept` and `F.Undergrad` correlate at **0.874** and enter with **opposite signs**. They are not two variables; they are one contrast — roughly "how selective is this college *relative to its size*" — and each is nearly useless without the other, while their difference is nearly meaningless on its own. Splitting a collinear pair out of a 12-variable fit and calling the halves "important" is exactly the error the size block in the starter's first look was put there to warn about. **Coefficient magnitude ranks variables inside a given fit; it does not identify the best small subset.** The procedure that answers the question you asked is subset selection under cross-validation, and it gives a different and better five.

A student who runs both procedures, finds the disagreement, and explains it in these terms has done the strongest thing this project admits.

---

## 3. Common wrong turns

1. **Loading without `index_col=0`.** Reading the bundled CSV without it brings the college name in as an `Unnamed: 0` column of strings; either the fit raises, or — if the student drops it silently — an eighteenth column is quietly counted among the seventeen. *The first column of `College.csv` is a label, not a measurement: `load('College', index_col=0)`.*

   The same wrong turn has a second, quieter form: **assuming the name is there.** `load()` prefers the `ISLP` package, whose `College` frame is indexed `0 … 776` and does not carry the names at all — so on Colab, where the setup cell installs `ISLP`, `index_col=0` has nothing to act on and there is no name to print. The rows, their order and the eighteen columns are identical either way, so no number in these notes moves; but any output that names an institution is true in one place and false in the other. *The starter therefore calls `reset_index(drop=True)` unconditionally and reports only what holds on both paths. A student who prints `college.index[:2]` as evidence of anything has written a line whose truth depends on their laptop.*

2. **Penalising unstandardised predictors.** `Lasso()` on the raw columns puts essentially all of the penalty on the variables that happen to be measured in large units and none on `S.F.Ratio` or `perc.alumni`, so the "selection" it reports is a statement about units, not about tuition. *Ridge and the lasso are not scale-invariant: standardise, and do it inside a `Pipeline` so the scaler is refitted within each CV fold rather than leaking the fold's mean into its own validation set.*

3. **Choosing the number of variables by test RMSE.** The temptation is real, because on this split test RMSE keeps drifting down all the way to seventeen ($2,255 at five, $2,206 at six, $2,120 at seventeen) while the training CV curve is *flat* from about six variables onwards — minimum $1,940 at ten, $1,964 at seventeen, a spread of barely 1%. *The flatness is the finding: with n = 543, cross-validation genuinely cannot resolve $50 of RMSE, and reaching for the test set to break the tie destroys the only unbiased estimate you had.* Report the flat curve and choose on parsimony — that is what the flatness licenses.

4. **Picking the five by *p*-value from the full seventeen-variable fit.** Individual *p*-values inside a collinear design answer "does this variable add anything *given all sixteen others*", which is not the question "which five, together, predict best". The size block makes the two answers diverge sharply. *Selection is a search over subsets, not a filter over the coefficients of one fit.*

5. **Quoting the $135 without its uncertainty.** A difference reported as a point estimate invites the board to treat $135 as a fact. *Two hundred and thirty-four colleges support an interval, not a point: bootstrap the test-set errors, and if the interval covers zero, say so — it strengthens your recommendation rather than weakening it.*

6. **Reading `Room.Board` causally.** It is the strongest single predictor ($2,919 CV RMSE on its own, better than the other sixteen), and it is a price the same institution sets in the same budget meeting. *A model whose best predictor is a sibling of the outcome predicts well and explains nothing.*

---

## 4. Marking guide

Out of 100, if the professor chooses to grade it.

| | Marks | What earns them |
|---|---|---|
| **Evaluation discipline** | 20 | The split respected; all selection by training CV; `evaluate()` called a handful of times, not dozens. Full marks require that the student could not have peeked, not merely that they say they did not. |
| **The four required RMSEs** | 15 | All four present, in dollars, matching the table above to within rounding. A number that disagrees with this table means the seed or the split moved — say which. |
| **Model search in Chapter 6** | 15 | Ridge *and* lasso *and* a subset method, all cross-validated on standardised predictors where required; the lasso's non-zero count reported; what was tried reported, not only what won. |
| **The five variables** | 15 | Five chosen by a named procedure with its evidence shown. Deduct if chosen by eye, by marginal correlation, or by *p*-value. **Add up to 5 bonus marks** for running a second procedure and explaining the disagreement. |
| **The cost of the restriction** | 15 | $135 computed and framed relative to the null and to the full model's gain. Full marks need the uncertainty on the gap. |
| **Honesty about the trap** | 20 | The regularised model's failure to improve on OLS, stated plainly and explained in bias-variance terms. **This is the largest single block of marks in the project.** A student who buries it, or who reports the lasso as an improvement when their own numbers say otherwise, forfeits all twenty however elegant the code. |
| **The memo** | 10 | One page, no code, all seven items, a recommendation the board's chair could read aloud, and a caveat that names a real threat. |

Two calibration notes. A student who beats $2,120 with a transformation and says so has done more than the project asked and should be rewarded — but not at the expense of the honesty block. And a student who reports every number correctly and concludes "the extra twelve variables are not worth defending" has arrived, by their own route, at the same place as the model answer; that is a pass with distinction regardless of which model they chose to publish.

---

## 5. Extensions

- **Transform the skewed predictors first.** `P.Undergrad`, `Apps`, `Books`, `Expend` and `Accept` all have skewness above 3.4. Replacing the eight count-and-money columns with `log1p` versions takes the all-seventeen OLS from $2,120 to **$2,013** — a $107 improvement, larger than the entire cost of restricting to five variables, and available from Chapter 3 alone. The lesson for the memo is uncomfortable and true: *the functional form was worth more than the choice of estimator.*

- **Splines and GAMs (Chapter 7).** A GAM on the five chosen variables (`pygam`, smooths on the four continuous predictors and a factor on `Private`) scores **$2,171** against the linear five's $2,255 — recovering roughly 60% of the restriction's cost while keeping the board's five variables. That is the most useful extension here, because it buys accuracy without spending interpretability. See `Advanced/advanced_04_glms_splines/advanced_04_glms_splines_lab.ipynb`. The warning attached: expanding *all seventeen* predictors into cubic spline bases and ridging the result scores **$2,706** — far worse than plain OLS. Flexibility spent where there is no curvature to find is variance bought for nothing, which is the same arithmetic as the main trap seen from the other side.

- **Prediction intervals instead of RMSE.** A board does not want "RMSE $2,255"; it wants "we expect $11,400, and we would not be surprised by anything between $7,000 and $16,000". Split conformal prediction turns the held-out set into exactly that guarantee, distribution-free — `Advanced/advanced_03_conformal/advanced_03_conformal_lab.ipynb`. Presenting the five-variable model *with* calibrated intervals is a materially better deliverable than the one this project asks for.

- **Have both models at once.** The dilemma in the brief is only real if explanation must come from a restricted fit. Shapley values attribute an individual prediction across predictors for *any* model, so the consortium could publish the seventeen-variable fit and still tell each college which five factors drove its own number — `Advanced/advanced_02_shapley/advanced_02_shapley_lab.ipynb`. Worth raising in a memo as the thing you would do with another week; worth being sceptical about too, since a board that cannot see the model cannot audit the explanation.

- **How fragile is "the five"?** Re-run the forward-stepwise selection on 200 bootstrap resamples of the training set and count how often each variable makes the top five. The answer, verified: `Room.Board` **100%**, `Private` **99%**, `Expend` **98%** — then a cliff — `perc.alumni` **78%**, `PhD` **69%**, `Grad.Rate` **25%**, `Terminal` **23%**. Three of the board's five are facts about the data; the other two are the winners of a close contest that the flat CV curve already warned about. Selection stability is a more honest object to hand a board than a single ranked list, and it is Chapter 5 machinery applied to a Chapter 6 question.

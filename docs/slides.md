# Lecture slides

Twelve Beamer decks live in `Lecture_Slides/chapter_NN/`, each folder
self-contained: `chapter_NN.tex`, its `images/`, and the compiled
`chapter_NN.pdf`. The PDFs below are served with this documentation.

:::{container} qrm-chips
**1029** slides in the main flow · **+111** in optional appendices ·
**86** short + **41** extended exercises · **~40** purpose-built figures
:::

```{figure} _static/deck-preview.png
:alt: Four slides from the Chapter 3 deck — a computed figure with a takeaway box, a worked example, an exercise prompt, and its worked solution.
:width: 100%
:align: center

What a deck looks like: a figure computed from the course data with its
takeaway, a worked example with real numbers, an in-deck exercise, and the
worked solution that follows it two slides later.
```

## The decks

Page counts are given as *main flow* and *(appendix)*: every deck ends with an
appendix of optional, more advanced material that the main thread never depends
on — see [what each appendix holds](#what-each-appendix-holds).

| Ch. | Deck | What it covers | Exercises | Slides | PDF |
|:--:|---|---|:--:|:--:|:--:|
| 0 | Precourse (a) — Statistics refresher *(optional)* | Descriptive statistics, probability and Bayes, distributions, standard errors and confidence intervals, testing and power, simple regression, the Python toolkit | 10 + 4 | 104 (+16) | <a href="slides/chapter_00.pdf">Open</a> |
| 0b | Precourse (b) — Toolkit *(optional)* | Reading notation, logs and exponentials, odds and the logit, likelihood, computational cost, the Python patterns the labs use | 6 + 2 | 48 (+9) | <a href="slides/chapter_00b.pdf">Open</a> |
| 1 | Introduction | What statistical learning is, prediction vs. inference, the three motivating data sets, notation and the design matrix | 3 + 1 | 68 (+6) | <a href="slides/chapter_01.pdf">Open</a> |
| 2 | Statistical Learning | Estimating *f*, parametric vs. nonparametric, the flexibility trade-off, training vs. test error, bias–variance, the Bayes classifier and KNN | 8 + 4 | 105 (+8) | <a href="slides/chapter_02.pdf">Open</a> |
| 3 | Linear Regression | Least squares, standard errors and *t*/*F* inference, confidence vs. prediction intervals, dummies and interactions, the four diagnostics, KNN regression | 12 + 6 | 142 (+11) | <a href="slides/chapter_03.pdf">Open</a> |
| 4 | Classification | Logistic regression and the odds scale, multiple predictors and confounding, LDA, QDA, naive Bayes, confusion matrices, ROC and AUC | 10 + 6 | 110 (+15) | <a href="slides/chapter_04.pdf">Open</a> |
| 5 | Resampling Methods | The validation set and why it wobbles, LOOCV, *k*-fold CV and the trade-off inside the estimate, CV pitfalls, the bootstrap | 6 + 3 | 77 (+7) | <a href="slides/chapter_05.pdf">Open</a> |
| 6 | Model Selection & Regularization | Best subset and stepwise selection, Cₚ/AIC/BIC/adjusted R², ridge, the lasso and its sparsity, PCR, the *p* > *n* regime | 7 + 3 | 79 (+11) | <a href="slides/chapter_06.pdf">Open</a> |
| 7 | Moving Beyond Linearity | Polynomials and step functions, regression splines and knots, natural splines, smoothing splines, LOESS, GAMs | 6 + 3 | 83 (+7) | <a href="slides/chapter_07.pdf">Open</a> |
| 8 | Tree-Based Methods | Recursive binary splitting, pruning, classification trees and impurity, bagging and out-of-bag error, random forests, boosting | 7 + 3 | 81 (+7) | <a href="slides/chapter_08.pdf">Open</a> |
| 10 | Deep Learning | Single-layer networks and activations, MLPs and parameter counts, convolutions and pooling, loss and SGD, regularisation and dropout | 6 + 3 | 71 (+8) | <a href="slides/chapter_10.pdf">Open</a> |
| 13 | Multiple Testing | Why naive testing fails at scale, FWER, Bonferroni and Holm, the false discovery rate, Benjamini–Hochberg, *p*-hacking | 5 + 3 | 61 (+6) | <a href="slides/chapter_13.pdf">Open</a> |
| **Total** | | | **86 + 41** | **1029 (+111)** | |

## How a deck is built

Every deck follows the same rhythm, so students always know where they are.

1. **Front matter** — course-at-a-glance, chapter contents, and a "Notation in
   this chapter" symbol table.
2. **Teaching flow** — motivation → intuition → formal definition → worked
   example → interpretation, with colour-coded callout boxes:

   | Box | Meaning |
   |---|---|
   | 🟩 green | Takeaway — the sentence to remember |
   | 🟦 blue | How to read this — a formula explained symbol by symbol |
   | 🟧 orange | Worked example with concrete numbers |
   | 🟥 red | Common pitfall |
   | 🟪 purple | Short exercise (~5 min) · 🟩 teal = its solution |
   | 🟣 violet | Extended exercise (~15 min) |
   | 🩵 cyan | "Companion notebook" — switch to the [Jupyter lab](labs.md) now |

3. **Exercises** — roughly one short exercise every 20 minutes and one extended
   exercise every 45 minutes, each tagged **[Concept] / [Math] / [Python]**
   (short) or **[Math] / [Python] / [Integrative]** (extended), so you can pick
   the right mix for your room. Every prompt is followed by its worked solution;
   long ones run across a clean `(1/2)` / `(2/2)` pair.
4. **Closing summary** — chapter-in-one-slide, key formulas at a glance,
   vocabulary, decision rules and common pitfalls.
5. **Appendix** — the optional, more advanced material, opened by a slide that
   says what is in it and why each item is optional.

Two things hold throughout:

- **~40 purpose-built visuals** — roughly 22 matplotlib plots generated from the
  bundled datasets plus 18 native TikZ concept diagrams. Among them: the
  bias–variance trade-off, the logistic S-curve, ROC and a confusion-matrix
  schematic, *k*-fold and bootstrap diagrams, ridge & lasso coefficient paths
  with the $\ell_1$-vs-$\ell_2$ constraint geometry, spline/GAM fits, a decision
  tree beside its feature-space partition, a neural-network architecture, a
  convolution diagram, and the Benjamini–Hochberg staircase.
- **Verified numbers** — Python listings are commented and runnable against the
  bundled datasets, and every numeric answer was reproduced against the real
  data.

## What each appendix holds

The appendix sits outside the timed plan: the [runsheets](teaching.md) stop where
it begins, and the slide index marks it *optional* rather than budgeting minutes
for it. Every exercise in an appendix keeps its full solution, so it works as
homework.

```{figure} _static/appendix-signpost.png
:alt: The appendix signpost slide of the Chapter 3 deck, listing each optional item and why it is optional.
:width: 80%
:align: center

Every appendix opens with this slide: what is in it, and why each item is
optional.
```

| Ch. | In its appendix | Pages |
|:--:|---|:--:|
| 0 | χ²/*t*/*F* and LLN vs. CLT · the ANOVA decomposition · linear algebra (with Exercise 0.8) · calculus and gradient descent (with Extended Exercise 0.3) | 16 |
| 0b | least squares as maximum likelihood (with Extended Exercise 0b.1) · counting and the 2ᵖ cost (with Exercise 0b.5) | 9 |
| 1 | the design matrix entry by entry · the two dataset lookup tables | 6 |
| 2 | Extended Exercise 2.1 (bias–variance from first principles) · Extended Exercise 2.3 (the Bayes boundary for two Gaussians) | 8 |
| 3 | squared vs. absolute loss · Extended Exercise 3.L2 (deriving least squares) · the matrix form of multiple regression · Extended Exercise 3.L6 (linear vs. polynomial vs. KNN) | 11 |
| 4 | how logistic regression is actually fitted (deviance, IRLS) · the multinomial softmax · Extended Exercise 4.2 (LDA from Bayes' theorem) · Extended Exercise 4.3 (naive Bayes by hand) · GLMs and Poisson regression | 15 |
| 5 | Exercise 5.2 and Extended Exercise 5.1 — the LOOCV leverage-shortcut drills | 7 |
| 6 | the constraint geometry redrawn · Exercise 6.1 (counting models) · Extended Exercise 6.2 (orthonormal design, soft thresholding) · partial least squares with Exercise 6.6 | 11 |
| 7 | the truncated-power basis and the constraint count · Extended Exercise 7.1 (regression splines by hand) | 7 |
| 8 | the partition picture redrawn · Extended Exercise 8.2 (impurity measures and pruning) · BART | 7 |
| 10 | Extended Exercise 10.2 (CNN architecture arithmetic) · transformers · backpropagation · double descent | 8 |
| 13 | the four outcomes drawn · resampling-based inference · post-selection inference | 6 |

## The two precourse decks

Both are optional, both sit before Lecture 1, and both exist because the ten
chapter decks assume their content silently.

### Chapter 0 — the statistics refresher

For students who need the undergraduate material back, and for anyone teaching a
cohort with mixed backgrounds. It covers:

- data and variable types; centre, spread and shape; boxplots and $z$-scores;
- covariance, correlation and what correlation cannot see; confounding;
- probability rules, conditional probability and Bayes' theorem (with the
  base-rate trap that motivates Chapter 4's ROC curves);
- the Bernoulli, binomial, Poisson and normal distributions, and the central
  limit theorem;
- standard errors, confidence intervals, hypothesis tests and the standard
  misreadings of both;
- simple linear regression end to end: least squares, residuals, $R^2$;
- the `numpy` / `pandas` / `matplotlib` / `statsmodels` / `scikit-learn` toolkit
  of the labs.

The linear algebra and the calculus/gradient-descent strands sit in its
appendix, for the cohorts that need them. It opens with a twelve-question
self-check so students can decide whether they need the session at all, and
closes with a table mapping every topic to the chapter that uses it. Eighteen
figures — the boxplot anatomy, a gallery of shapes, Anscombe's quartet,
Simpson's paradox, the CLT, confidence-interval coverage, $p$-values as areas,
power, leverage, and gradient descent on a real loss surface — are computed from
the course data by `Lecture_Slides/chapter_00/make_figures.py`, and every one is
rebuilt in code in the [companion notebook](labs.md).

### Chapter 0b — the toolkit

Covering what the ten lecture decks *use* but never *explain*. Its scope was not
guessed — it comes from counting usage across the decks:

| Topic | Where it bites | Uses |
|---|---|--:|
| `log` and `exp` | Ch. 4 (113), Ch. 10 (31), Ch. 6 (16) | 176 |
| odds and the logit | Ch. 4 (92), Ch. 10 (12) | 108 |
| likelihood and ∏ | Ch. 4 (35), Ch. 2–3 | 37 |
| ∑, arg max, indicators, sets | every chapter from Ch. 2 | 180 |
| counting and the 2ᵖ cost | Ch. 6 (subset selection) | 13 |

It adds a sixth strand the labs depend on and the decks never teach: the Python
patterns themselves — writing a function, looping over candidate settings,
seeding randomness, the `fit`/`predict` contract, and the discipline of scoring
on data the model has not seen. Eight figures, six short and two extended
exercises, and a companion notebook. The maximum-likelihood derivation and the
counting strand live in its appendix.

## Rebuilding a deck

Requires a TeX Live distribution with `beamer`, `tcolorbox`, `tikz`, `listings`
and `booktabs`:

```bash
cd Lecture_Slides/chapter_08
pdflatex chapter_08.tex
pdflatex chapter_08.tex   # second pass for the navigation bar
```

From the repository root, `make` rebuilds every deck whose source changed and
refreshes the slide index, and `make check` reports page counts and any slide
that overruns its frame. Python snippets inside the slides read data from
`../../ALL CSV FILES - 2nd Edition/` or via the `ISLP` package.

```{admonition} Figures from the book
:class: note

Decks that reproduce a textbook figure attribute it to its source. The
copyrighted textbook PDF and figure banks (`Source_Material/`) are **not**
included in the repository.
```

## Where to go next

- [Lab notebooks](labs.md) — the companion notebook for each deck.
- [Teaching it](teaching.md) — runsheets, the slide index, and how the appendix fits a session.
- [The course at a glance](course.md) — which deck goes in which week.

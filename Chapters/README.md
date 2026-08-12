# Chapters — Quantitative Research Methods

The course material, one folder per chapter — for the **Quantitative Research
Methods** course, based on *An Introduction to Statistical Learning, with
Applications in Python* (James, Witten, Hastie, Tibshirani & Taylor, 2023),
prepared by Prof. Dr. Christoph Weisser.

Each chapter folder (`chapter_NN/`) is self-contained and holds **everything for
that chapter**: the deck source `chapter_NN.tex`, its `images/`, the compiled
`chapter_NN.pdf`, and the companion lab `chapter_NN_lab.ipynb`.

Every chapter carries both — ten decks and eleven notebooks, counting the two
precourse sessions. Support vector machines (Ch 9), survival analysis (Ch 11),
unsupervised learning (Ch 12) and multiple testing (Ch 13) are no longer part of
the taught sequence: their decks and labs live on in [`Advanced/`](./Advanced/)
as self-study modules A5, A6, A8 and A7.

`chapter_00/` is the **first half of the taught precourse session**, a refresher of the undergraduate
material the course assumes. It is not an ISLP chapter: it revisits descriptive
statistics, probability and Bayes, the standard distributions, sampling and
confidence intervals, hypothesis testing, simple linear regression and the
`numpy`/`pandas` toolkit — each section ending with where that topic reappears
in the course. The matrix algebra and the derivatives/gradient-descent strands
sit in its appendix, to be taken only by the cohorts that need them. It opens
with a twelve-question self-check so students can judge whether they need it. Its
nineteen figures are regenerated from the bundled data by
[`chapter_00/make_figures.py`](./chapter_00/make_figures.py), and it has a
companion notebook, [`chapter_00_lab.ipynb`](./chapter_00/chapter_00_lab.ipynb), which rebuilds every
one of them in code.

`chapter_00b/` is the **second half of that session**, covering what the later
chapters use but never explain. Its scope was chosen by counting usage across
the nine chapter decks: reading notation (Σ, Π, argmin, indicators, sets — 180
uses), logs and exponentials (176), odds and the logit (108), likelihood and
maximum likelihood (37), counting and the 2ᵖ cost (13), plus the Python
patterns every lab relies on. The maximum-likelihood derivation and the counting
strand are in its appendix. Companion notebook:
[`chapter_00b_lab.ipynb`](./chapter_00b/chapter_00b_lab.ipynb).

## Teaching design

Every deck follows the same flow — motivation → intuition → formal definition →
worked example — in the course house style, with:

- **74 short exercises** (~5 min, roughly one every 20 minutes): a purple prompt
  slide immediately followed by a teal worked-solution slide; long solutions run
  across a clean `(1/2)` / `(2/2)` pair.
- **35 extended exercises** (~15 min, roughly one every 45 minutes) in a violet
  "Extended exercise" box — integrative, multi-part problems with detailed
  multi-slide solutions.
- Every exercise is tagged **[Concept]/[Math]/[Python]** (short) or
  **[Math]/[Python]/[Integrative]** (extended), so you can pick the right mix.
  Python solutions carry runnable snippets against the bundled datasets, and all
  numeric answers were reproduced against the real data.
- **~110 purpose-built visuals** (71 matplotlib plots generated from the bundled
  datasets + 38 native TikZ concept diagrams) — for example the bias–variance
  trade-off, the logistic S-curve, ROC and a confusion-matrix schematic,
  k-fold / bootstrap diagrams, ridge & lasso coefficient paths with the ℓ1-vs-ℓ2
  constraint geometry, spline/GAM fits, a decision tree with its feature-space
  partition, and a neural-network architecture with a convolution diagram.
- A **5–10 slide summary block** closing every deck, including a dedicated
  **"Key formulas at a glance"** slide plus "chapter in one slide", vocabulary,
  decision rules and common pitfalls.
- An **appendix** at the back of every deck holding the optional, more advanced
  material: formal derivations, the heaviest worked exercises and side topics. It
  opens with a slide saying what is in it and why each item is optional, and the
  "Contents" slide points at it. The main thread never depends on the appendix, so
  a session can run front to back and stop where the appendix begins.

## What is in the appendices

The appendix of each deck is outside the timed teaching plan: the runsheets in
`Teaching_Guide/runsheets/` stop where it begins, and `slide_index.md` marks it
*optional*. Every exercise in an appendix still carries its full solution, so it
works as homework.

| Chapter | In its appendix | Pages |
|---|---|:--:|
| 0 | χ²/t/F and LLN vs. CLT · the ANOVA decomposition · linear algebra (with Exercise 0.8) · calculus and gradient descent (with Extended Exercise 0.3) | 20 |
| 0b | least squares as maximum likelihood (with Extended Exercise 0b.1) · counting and the 2ᵖ cost (with Exercise 0b.5) | 14 |
| 1 | the design matrix entry by entry · the two dataset lookup tables | 8 |
| 2 | Extended Exercise 2.1 (bias–variance from first principles) · Extended Exercise 2.3 (the Bayes boundary for two Gaussians) · **the Bayes classifier and KNN in full, with Exercises 2.6, 2.7, E2.2 and E2.4** | 42 |
| 3 | squared vs. absolute loss · Extended Exercise 3.L2 (deriving least squares) · the matrix form of multiple regression · Extended Exercise 3.L6 (linear vs. polynomial vs. KNN) · **linear vs. KNN regression** | 19 |
| 4 | **the generative models in full — Bayes refresher, LDA, QDA, naive Bayes, with Exercises 4.5–4.7** · how logistic regression is actually fitted (deviance, IRLS) · the multinomial softmax · Extended Exercise 4.2 (LDA from Bayes' theorem) · Extended Exercise 4.3 (naive Bayes by hand) · **comparing the classifiers, with Extended Exercise 4.4** · GLMs and Poisson regression | 52 |
| 5 | Exercise 5.2 and Extended Exercise 5.1 — the LOOCV leverage-shortcut drills | 11 |
| 6 | the constraint geometry redrawn · Exercise 6.1 (counting models) · Extended Exercise 6.2 (orthonormal design, soft thresholding) · partial least squares with Exercise 6.6 | 14 |
| 7 | the truncated-power basis and the constraint count · Extended Exercise 7.1 (regression splines by hand) | 9 |
| 8 | the partition picture redrawn · Extended Exercise 8.2 (impurity measures and pruning) · BART | 10 |

## Exercises per chapter

| Chapter | Topic | Short ex. | Extended ex. | Pages (main + appendix) |
|---|---|:--:|:--:|:--:|
| 0  | Precourse (a) — statistics refresher | 13 | 4 | 112 + 20 |
| 0b | Precourse (b) — toolkit | 6 | 2 | 53 + 14 |
| 1  | Introduction | 3 | 1 | 74 + 8 |
| 2  | Statistical Learning | 11 | 4 | 81 + 42 |
| 3  | Linear Regression | 13 | 6 | 149 + 19 |
| 4  | Classification | 13 | 6 | 91 + 52 |
| 5  | Resampling Methods | 6 | 3 | 85 + 11 |
| 6  | Linear Model Selection & Regularization | 6 | 3 | 73 + 14 |
| 7  | Moving Beyond Linearity | 6 | 3 | 93 + 9 |
| 8  | Tree-Based Methods | 7 | 3 | 90 + 10 |
| **Total** | | **80** | **38** | **901 + 199** |

Support vector machines (Ch 9), survival analysis (Ch 11), unsupervised learning
(Ch 12) and multiple testing (Ch 13) are no longer part of the taught sequence —
their decks, labs and appendices moved to [`Advanced/`](./Advanced/) as
self-study modules A5, A6, A8 and A7.

## Suggested plan (11 sessions of 180 min)

Nine ISLP chapters in book order, preceded by the taught precourse session — 12
sessions in all. The plan is keyed to **chapter numbers**, not session numbers,
because that is what the decks, labs and exercise numbering all use. The three
heaviest chapters (2, 3, 4) each span two sessions, splitting at a natural
section boundary so you can stop and resume cleanly.

| Chapter | Sessions | Content | Exercises |
|:--:|:--:|---|---|
| **Precourse** — Ch 0 + Ch 0b | 1 | **Taught in one session**, drawing on both decks: descriptive statistics, probability, distributions, inference, simple regression, Python — and notation, logs and odds, likelihood, counting, the Python of the labs | 0.1–0.10, 0b.1–0b.6 |
| **Ch 1** | ½ | Introduction; prediction vs inference; the three motivating data sets | 1.1–1.3 |
| **Ch 2** | 1½ | What is statistical learning; parametric vs non-parametric; assessing accuracy; bias–variance; the Bayes classifier and KNN; lab | 2.1–2.8 |
| **Ch 3** | 2 | Simple & multiple linear regression; estimation; inference (SE, t, F); qualitative predictors; interactions; diagnostics; KNN vs OLS; lab | 3.1–3.12 |
| **Ch 4** | 2 | Logistic regression; odds; confounding; the confusion matrix; ROC/AUC; lab — generative models are appendix material | 4.1–4.10 |
| **Ch 5** | 1 | Validation set, LOOCV, k-fold CV, the bootstrap | 5.1–5.6 |
| **Ch 6** | 1 | Subset selection; Cp/AIC/BIC; ridge; lasso; PCR/PLS | 6.1–6.6 |
| **Ch 7** | 1 | Polynomials, step functions, splines, smoothing splines, GAMs | 7.1–7.6 |
| **Ch 8** | 1 | Decision trees; bagging & OOB; random forests; boosting | 8.1–8.7 |
| **Ch 10** | 1 | Neural nets; forward pass; backprop/GD; CNNs; regularization | 10.1–10.6 |

Chapter 1 is short and opens the same session as the first half of Chapter 2.

For the split chapters, the recommended stopping points are: **Ch 2** after the
KNN / bias–variance material; **Ch 3** after "Goodness of fit / the four
questions" (p. 75); **Ch 4** after the logistic-regression section (p. 41), so evaluation
and the lab open the second session.

The plan above covers the main flow of each deck. Appendix pages sit outside it
— assign them, or reach for them when a room wants the derivation.

## Rebuilding a deck

Requires a TeX Live distribution (with `beamer`, `tcolorbox`, `tikz`,
`listings`, `booktabs`):

```bash
cd chapter_NN
pdflatex chapter_NN.tex
pdflatex chapter_NN.tex   # second pass for the navigation bar
```

Python exercise snippets read data from `../../ALL CSV FILES - 2nd Edition/` or
via the `ISLP` package.

## Citation

These slides are based on, and follow the structure of, the source textbook —
please cite it if you reuse them:

> James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J. (2023).
> *An Introduction to Statistical Learning, with Applications in Python.*
> Springer Texts in Statistics. Springer. <https://www.statlearning.com>

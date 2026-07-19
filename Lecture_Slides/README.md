# ISLP Lecture Series — Slides with In-Deck Exercises

Enhanced Beamer decks for *An Introduction to Statistical Learning, with
Applications in Python* (James, Witten, Hastie, Tibshirani & Taylor, 2023),
prepared for HSBI by Prof. Dr. Christoph Weisser.

This folder builds on `slides_refined_advanced/` and adds the one feature it
lacked: **formal exercises with detailed, step-by-step solutions**, placed
roughly every 20 minutes of lecture time. Everything else (HSBI house style,
motivation → intuition → definition → worked example flow, roadmaps,
mini-checks) is preserved.

## What was added

- **70 short exercises** (~5 min, roughly one every 20 min), each a prompt
  slide immediately followed by a full worked-solution slide. Purple prompt box,
  teal solution box; long solutions run across a clean `(1/2)` / `(2/2)` pair.
- **35 extended exercises** (~15 min, roughly one every 45 min) in a distinct
  **violet** "Extended exercise" box — integrative, multi-part problems with
  detailed multi-slide solutions. These are the ~45-minute checkpoints; the
  short exercises are the ~20-minute ones.
- Every exercise is tagged **[Concept]/[Math]/[Python]** (short) or
  **[Math]/[Python]/[Integrative]** (extended) so you can pick the right mix.
  Python solutions carry runnable snippets against the bundled datasets, and all
  numeric answers were reproduced against the real data.
- All 10 decks compile cleanly with `pdflatex` (exit 0), with no blank or
  cut-off slides.

## Visuals pass (new teaching graphics)

Each deck gained purpose-built visuals — **~22 Python data plots** generated
from the bundled datasets (matplotlib) and **~18 native TikZ concept diagrams**
— for example: the taxonomy of statistical learning and the bias–variance
trade-off (ch1–2), least-squares residuals and Advertising fits (ch3), the
logistic S-curve, ROC and a confusion-matrix schematic (ch4), k-fold /
bootstrap diagrams and the CV-vs-degree curve (ch5), ridge & lasso coefficient
paths plus the ℓ1-vs-ℓ2 constraint geometry (ch6), spline/GAM fits on Wage
(ch7), a decision tree with its feature-space partition and ensemble error
curves (ch8), a neural-network architecture, activation functions and a
convolution diagram (ch10), and the FWER-growth curve, Benjamini–Hochberg
staircase and p-value histogram (ch13). Every new figure is capped in height so
image plus caption never overflows the slide.

## Summary pass (concepts & formulas)

Every deck ends with a **5–10 slide summary block**, and each now includes a
dedicated **"Key formulas at a glance"** slide collecting the chapter's
essential equations (e.g. the bias–variance decomposition, ridge/lasso
objectives, Gini/entropy, the forward pass and gradient-descent update, the
Benjamini–Hochberg rule), alongside the existing "Chapter in one slide",
vocabulary, decision-rules, pitfalls and "things to remember" slides.

## Layout pass (empty-slide fix)

An earlier version wrapped every solution in an auto-breaking frame. Because a
callout box cannot be split, beamer pushed each box onto a second page and left
the first nearly blank — and the same mechanism split every section `Outline`
and the title `Contents` into a full page plus a near-empty one. This edition
fixes that throughout: box text is set at `\footnotesize`, the spurious page
breaks are removed, table-of-contents slides fit on one page, and any solution
too long for a single slide is split into a clean `(1/2)` / `(2/2)` pair. The
result removed **~107 empty/near-empty pages** (794 → 687) with no loss of
content. Every exercise and solution slide was verified by rendering the page
and checking it is neither blank nor cut off at the bottom.

## Exercises per chapter

| Chapter | Topic | Short ex. | Extended ex. | Pages |
|---|---|---|---|---|
| 1  | Introduction | 3 | 1 | 65 |
| 2  | Statistical Learning | 8 | 4 | 98 |
| 3  | Linear Regression | 12 | 6 | 143 |
| 4  | Classification | 10 | 6 | 108 |
| 5  | Resampling Methods | 6 | 3 | 78 |
| 6  | Linear Model Selection & Regularization | 7 | 3 | 82 |
| 7  | Moving Beyond Linearity | 6 | 3 | 77 |
| 8  | Tree-Based Methods | 7 | 3 | 75 |
| 10 | Deep Learning | 6 | 3 | 71 |
| 13 | Multiple Testing | 5 | 3 | 62 |
| **Total** | | **70** | **35** | **859** |

## Suggested 12-lecture plan (180 min each)

Ten chapters mapped onto twelve 180-minute sessions. The three heaviest
chapters (2, 3, 4) each span two lectures; the split point is a natural
section boundary so you can stop and resume cleanly.

| Lecture | Chapter(s) | Content | Exercises |
|---|---|---|---|
| 1  | Ch 1 + Ch 2 (part 1) | Introduction; what is statistical learning; prediction vs inference; parametric vs non-parametric | 1.1–1.3, 2.1–2.2 |
| 2  | Ch 2 (part 2) | Assessing accuracy; bias–variance trade-off; classification & KNN; lab | 2.3–2.8 |
| 3  | Ch 3 (part 1) | Simple & multiple linear regression; estimation; inference (SE, t, F) | 3.1–3.6 |
| 4  | Ch 3 (part 2) | Qualitative predictors; interactions; diagnostics; KNN vs OLS; lab | 3.7–3.12 |
| 5  | Ch 4 (part 1) | Logistic regression; odds; multiple logistic; confounding | 4.1–4.4 |
| 6  | Ch 4 (part 2) | LDA, QDA, naive Bayes; confusion matrix, ROC/AUC; lab | 4.5–4.10 |
| 7  | Ch 5 | Validation set, LOOCV, k-fold CV, the bootstrap | 5.1–5.6 |
| 8  | Ch 6 | Subset selection; Cp/AIC/BIC; ridge; lasso; PCR/PLS | 6.1–6.7 |
| 9  | Ch 7 | Polynomials, step functions, splines, smoothing splines, GAMs | 7.1–7.6 |
| 10 | Ch 8 | Decision trees; bagging & OOB; random forests; boosting | 8.1–8.7 |
| 11 | Ch 10 | Neural nets; forward pass; backprop/GD; CNNs; regularization | 10.1–10.6 |
| 12 | Ch 13 | Multiple testing; FWER; Bonferroni; Holm; FDR & Benjamini–Hochberg | 13.1–13.5 |

For the split lectures, the recommended stopping points are: **Ch 2** after the
KNN / bias–variance material; **Ch 3** after "Goodness of fit / the four
questions"; **Ch 4** after multiple logistic regression (before LDA).

## Rebuilding a deck

```bash
cd chapter_NN
pdflatex chapter_NN.tex
pdflatex chapter_NN.tex   # second pass for the navigation bar
```

Each chapter folder is self-contained (`chapter_NN.tex`, its `images/`, and the
compiled `chapter_NN.pdf`). Python exercise snippets read data from
`../../ALL CSV FILES - 2nd Edition/` or via the `ISLP` package.

## Citation

> James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J. (2023).
> *An Introduction to Statistical Learning, with Applications in Python.*
> Springer. <https://www.statlearning.com>

# Lecture Slides — Quantitative Research Methods

Ten Beamer decks for the **Quantitative Research Methods** course, based on
*An Introduction to Statistical Learning, with Applications in Python* (James,
Witten, Hastie, Tibshirani & Taylor, 2023), prepared for HSBI by Prof. Dr.
Christoph Weisser.

Each chapter folder (`chapter_NN/`) is self-contained: `chapter_NN.tex`, its
`images/`, and the compiled `chapter_NN.pdf`.

## Teaching design

Every deck follows the same flow — motivation → intuition → formal definition →
worked example — in the HSBI house style, with:

- **70 short exercises** (~5 min, roughly one every 20 minutes): a purple prompt
  slide immediately followed by a teal worked-solution slide; long solutions run
  across a clean `(1/2)` / `(2/2)` pair.
- **35 extended exercises** (~15 min, roughly one every 45 minutes) in a violet
  "Extended exercise" box — integrative, multi-part problems with detailed
  multi-slide solutions.
- Every exercise is tagged **[Concept]/[Math]/[Python]** (short) or
  **[Math]/[Python]/[Integrative]** (extended), so you can pick the right mix.
  Python solutions carry runnable snippets against the bundled datasets, and all
  numeric answers were reproduced against the real data.
- **~40 purpose-built visuals** (≈22 matplotlib plots generated from the bundled
  datasets + ≈18 native TikZ concept diagrams) — for example the bias–variance
  trade-off, the logistic S-curve, ROC and a confusion-matrix schematic,
  k-fold / bootstrap diagrams, ridge & lasso coefficient paths with the ℓ1-vs-ℓ2
  constraint geometry, spline/GAM fits, a decision tree with its feature-space
  partition, a neural-network architecture and a convolution diagram, and the
  Benjamini–Hochberg staircase.
- A **5–10 slide summary block** closing every deck, including a dedicated
  **"Key formulas at a glance"** slide plus "chapter in one slide", vocabulary,
  decision rules and common pitfalls.

## Exercises per chapter

| Chapter | Topic | Short ex. | Extended ex. | Pages |
|---|---|:--:|:--:|:--:|
| 1  | Introduction | 3 | 1 | 73 |
| 2  | Statistical Learning | 8 | 4 | 112 |
| 3  | Linear Regression | 12 | 6 | 152 |
| 4  | Classification | 10 | 6 | 125 |
| 5  | Resampling Methods | 6 | 3 | 83 |
| 6  | Linear Model Selection & Regularization | 7 | 3 | 89 |
| 7  | Moving Beyond Linearity | 6 | 3 | 89 |
| 8  | Tree-Based Methods | 7 | 3 | 87 |
| 10 | Deep Learning | 6 | 3 | 78 |
| 13 | Multiple Testing | 5 | 3 | 67 |
| **Total** | | **70** | **35** | **955** |

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

# Lecture slides

Twelve Beamer decks live in `Lecture_Slides/chapter_NN/`, each folder
self-contained: `chapter_NN.tex`, its `images/`, and the compiled
`chapter_NN.pdf`. The PDFs below are served with this documentation.

Every deck ends with an **appendix** holding the optional, more advanced
material — formal derivations, the heavier worked exercises, and side topics.
Nothing in the main thread depends on it, so a session can ignore it entirely;
the page counts below give the main flow and the appendix separately.

## The decks

| Ch. | Deck | Short ex. | Extended ex. | Pages (main + appendix) | PDF |
|:--:|---|:--:|:--:|:--:|:--:|
| 0 | Precourse (a) — Statistics Refresher *(optional)* | 10 | 4 | 104 + 16 | <a href="slides/chapter_00.pdf">Open</a> |
| 0b | Precourse (b) — Toolkit *(optional)* | 6 | 2 | 48 + 9 | <a href="slides/chapter_00b.pdf">Open</a> |
| 1 | Introduction | 3 | 1 | 68 + 6 | <a href="slides/chapter_01.pdf">Open</a> |
| 2 | Statistical Learning | 8 | 4 | 105 + 8 | <a href="slides/chapter_02.pdf">Open</a> |
| 3 | Linear Regression | 12 | 6 | 142 + 11 | <a href="slides/chapter_03.pdf">Open</a> |
| 4 | Classification | 10 | 6 | 110 + 15 | <a href="slides/chapter_04.pdf">Open</a> |
| 5 | Resampling Methods | 6 | 3 | 77 + 7 | <a href="slides/chapter_05.pdf">Open</a> |
| 6 | Linear Model Selection & Regularization | 7 | 3 | 79 + 11 | <a href="slides/chapter_06.pdf">Open</a> |
| 7 | Moving Beyond Linearity | 6 | 3 | 83 + 7 | <a href="slides/chapter_07.pdf">Open</a> |
| 8 | Tree-Based Methods | 7 | 3 | 81 + 7 | <a href="slides/chapter_08.pdf">Open</a> |
| 10 | Deep Learning | 6 | 3 | 71 + 8 | <a href="slides/chapter_10.pdf">Open</a> |
| 13 | Multiple Testing | 5 | 3 | 61 + 6 | <a href="slides/chapter_13.pdf">Open</a> |
| **Total** | | **86** | **41** | **1029 + 111** | |

## Chapter 0: the precourse refresher

An optional session, added for students who need the undergraduate material
back before Lecture 1 — and for anyone teaching a cohort with mixed
backgrounds. It covers:

- data and variable types; centre, spread and shape; boxplots and $z$-scores;
- covariance, correlation and what correlation cannot see; confounding;
- probability rules, conditional probability and Bayes' theorem (with the
  base-rate trap that motivates Chapter 4's ROC curves);
- the Bernoulli, binomial, Poisson, normal, $t$, $\chi^2$ and $F$
  distributions, and the central limit theorem;
- standard errors, confidence intervals, hypothesis tests and the standard
  misreadings of both;
- simple linear regression end to end: least squares, residuals, $R^2$;
- the linear algebra (matrix products, inverses, norms, eigenvectors) and
  calculus (gradients, convexity, gradient descent) later chapters rely on;
- the `numpy` / `pandas` / `matplotlib` / `statsmodels` / `scikit-learn`
  toolkit of the labs.

It opens with a twelve-question self-check so students can decide whether they
need it, and closes with a table mapping every topic to the chapter that uses
it. Eighteen figures — the boxplot anatomy, a gallery of shapes, Anscombe's
quartet, Simpson's paradox, the CLT, confidence-interval coverage, $p$-values
as areas, power, leverage, and gradient descent on a real loss surface — are
computed from the course data by
`Lecture_Slides/chapter_00/make_figures.py`, and every one of them is rebuilt
in code in the [companion notebook](labs.md).

## Chapter 0b: the precourse toolkit

A second optional session, covering what the ten lecture decks *use* but never
*explain*. Its scope was not guessed — it comes from counting usage across the
decks:

| Topic | Where it bites | Uses |
|---|---|--:|
| `log` and `exp` | Ch. 4 (113), Ch. 10 (31), Ch. 6 (16) | 176 |
| odds and the logit | Ch. 4 (92), Ch. 10 (12) | 108 |
| likelihood and $\prod$ | Ch. 4 (35), Ch. 2–3 | 37 |
| $\sum$, $\arg\max$, indicators, sets | every chapter from Ch. 2 | 180 |
| counting and the $2^p$ cost | Ch. 6 (subset selection) | 13 |

It adds a sixth strand the labs depend on and the decks never teach: the Python
patterns themselves — writing a function, looping over candidate settings,
seeding randomness, the `fit`/`predict` contract, and the discipline of scoring
on data the model has not seen. Eight figures, six short and two extended
exercises, and a companion notebook.

## What's in a deck

- **~40 purpose-built visuals** — roughly 22 matplotlib plots generated from the
  bundled datasets plus 18 native TikZ concept diagrams. Among them: the
  bias–variance trade-off, the logistic S-curve, ROC and a confusion-matrix
  schematic, *k*-fold and bootstrap diagrams, ridge & lasso coefficient paths
  with the $\ell_1$-vs-$\ell_2$ constraint geometry, spline/GAM fits, a decision
  tree beside its feature-space partition, a neural-network architecture, a
  convolution diagram, and the Benjamini–Hochberg staircase.
- **Commented Python** on every code listing, and a cyan "Companion notebook"
  box marking exactly when to switch to the [Jupyter lab](labs.md).
- **Every exercise has a full solution** — short exercises get a teal solution
  slide immediately after the prompt (long ones run across a clean `(1/2)` /
  `(2/2)` pair); extended exercises get detailed multi-slide solutions.
- **Verified numbers** — Python solutions carry runnable snippets against the
  bundled datasets, and all numeric answers were reproduced against the real
  data.

## Rebuilding a deck

Requires a TeX Live distribution with `beamer`, `tcolorbox`, `tikz`, `listings`
and `booktabs`:

```bash
cd Lecture_Slides/chapter_08
pdflatex chapter_08.tex
pdflatex chapter_08.tex   # second pass for the navigation bar
```

Python snippets inside the slides read data from
`../../ALL CSV FILES - 2nd Edition/` or via the `ISLP` package.

```{admonition} Figures from the book
:class: note

Decks that reproduce a textbook figure attribute it to its source. The
copyrighted textbook PDF and figure banks (`Source_Material/`) are **not**
included in the repository.
```

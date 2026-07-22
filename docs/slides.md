# Lecture slides

Ten Beamer decks live in `Lecture_Slides/chapter_NN/`, each folder
self-contained: `chapter_NN.tex`, its `images/`, and the compiled
`chapter_NN.pdf`. The PDFs below are served with this documentation.

## The decks

| Ch. | Deck | Short ex. | Extended ex. | Pages | PDF |
|:--:|---|:--:|:--:|:--:|:--:|
| 1 | Introduction | 3 | 1 | 73 | <a href="slides/chapter_01.pdf">Open</a> |
| 2 | Statistical Learning | 8 | 4 | 112 | <a href="slides/chapter_02.pdf">Open</a> |
| 3 | Linear Regression | 12 | 6 | 152 | <a href="slides/chapter_03.pdf">Open</a> |
| 4 | Classification | 10 | 6 | 125 | <a href="slides/chapter_04.pdf">Open</a> |
| 5 | Resampling Methods | 6 | 3 | 83 | <a href="slides/chapter_05.pdf">Open</a> |
| 6 | Linear Model Selection & Regularization | 7 | 3 | 89 | <a href="slides/chapter_06.pdf">Open</a> |
| 7 | Moving Beyond Linearity | 6 | 3 | 89 | <a href="slides/chapter_07.pdf">Open</a> |
| 8 | Tree-Based Methods | 7 | 3 | 87 | <a href="slides/chapter_08.pdf">Open</a> |
| 10 | Deep Learning | 6 | 3 | 78 | <a href="slides/chapter_10.pdf">Open</a> |
| 13 | Multiple Testing | 5 | 3 | 67 | <a href="slides/chapter_13.pdf">Open</a> |
| **Total** | | **70** | **35** | **955** | |

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

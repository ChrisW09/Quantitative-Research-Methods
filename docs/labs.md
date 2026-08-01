---
myst:
  html_meta:
    description: "Fifteen Jupyter notebooks — one per lecture deck, each closing with worked solutions — rendered in full and runnable on Google Colab with one click."
---

# Lab notebooks

{.qrm-lead}
Fifteen notebooks, one per chapter, each living beside the deck it accompanies
in `Chapters/chapter_NN/chapter_NN_lab.ipynb` — **one lab per lecture deck**,
both precourse sessions included.

Each mirrors its chapter's Python lab and closes with **worked solutions** to
that chapter's exercises. Every chapter, without exception: these are the labs
the course is built around.

Each notebook runs **locally or on Google Colab**; data loads via the `ISLP`
package with an automatic fallback to the bundled CSVs, so nothing needs
downloading by hand. [Colab is the recommended route](quickstart.md) — nothing
to install.

Every notebook is rendered in full below (with its stored outputs — the
documentation build never executes them).

:::{container} qrm-chips
[**15** labs *(with solutions)*]{.qrm-chip}
[**one** lab per deck]{.qrm-chip}
[runs **locally** and on **Colab**]{.qrm-chip}
:::

## The fifteen labs

| Ch. | Lab | Read here | Open in Colab |
|:--:|---|:--:|:--:|
| 0 · Precourse (a) — Statistics | `chapter_00_lab.ipynb` | [Rendered](labs/chapter_00_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_00/chapter_00_lab.ipynb) |
| 0b · Precourse (b) — Toolkit | `chapter_00b_lab.ipynb` | [Rendered](labs/chapter_00b_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_00b/chapter_00b_lab.ipynb) |
| 1 · Introduction | `chapter_01_lab.ipynb` | [Rendered](labs/chapter_01_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_01/chapter_01_lab.ipynb) |
| 2 · Statistical Learning | `chapter_02_lab.ipynb` | [Rendered](labs/chapter_02_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_02/chapter_02_lab.ipynb) |
| 3 · Linear Regression | `chapter_03_lab.ipynb` | [Rendered](labs/chapter_03_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_03/chapter_03_lab.ipynb) |
| 4 · Classification | `chapter_04_lab.ipynb` | [Rendered](labs/chapter_04_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_04/chapter_04_lab.ipynb) |
| 5 · Resampling Methods | `chapter_05_lab.ipynb` | [Rendered](labs/chapter_05_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_05/chapter_05_lab.ipynb) |
| 6 · Model Selection & Regularization | `chapter_06_lab.ipynb` | [Rendered](labs/chapter_06_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_06/chapter_06_lab.ipynb) |
| 7 · Moving Beyond Linearity | `chapter_07_lab.ipynb` | [Rendered](labs/chapter_07_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_07/chapter_07_lab.ipynb) |
| 8 · Tree-Based Methods | `chapter_08_lab.ipynb` | [Rendered](labs/chapter_08_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_08/chapter_08_lab.ipynb) |
| 9 · Support Vector Machines | `chapter_09_lab.ipynb` | [Rendered](labs/chapter_09_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_09/chapter_09_lab.ipynb) |
| 10 · Deep Learning | `chapter_10_lab.ipynb` | [Rendered](labs/chapter_10_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_10/chapter_10_lab.ipynb) |
| 11 · Survival Analysis | `chapter_11_lab.ipynb` | [Rendered](labs/chapter_11_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_11/chapter_11_lab.ipynb) |
| 12 · Unsupervised Learning | `chapter_12_lab.ipynb` | [Rendered](labs/chapter_12_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_12/chapter_12_lab.ipynb) |
| 13 · Multiple Testing | `chapter_13_lab.ipynb` | [Rendered](labs/chapter_13_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/chapter_13/chapter_13_lab.ipynb) |

```{tip}
The Colab badges open straight from the public GitHub repository; a Google
account is all you need to run a notebook.
```

## How the notebooks find their data

Each notebook opens with a setup cell that:

1. detects whether it is running on Colab and installs any missing packages
   (`ISLP`, plus `pygam` / `xgboost` / `lifelines` for the chapters that need
   them — `torch` is preinstalled on Colab);
2. loads each dataset from the `ISLP` package where possible, streams the four
   it does not ship (`Advertising`, `Heart`, `Income1`, `Income2`) from the
   book's official site, and falls back to the bundled
   [`ALL CSV FILES - 2nd Edition/`](datasets.md) folder otherwise.

So a fresh Colab runtime works with no manual downloads, and a local checkout
works offline.

## All notebooks

```{toctree}
:maxdepth: 1
:glob:

labs/chapter_*_lab
```

## Where to go next

- [Lecture slides](slides.md) — the deck each lab accompanies.
- [For students](for-students.md) — how the labs relate to the lectures, and what to do when your numbers differ.
- [Datasets](datasets.md) — what is bundled, and which chapter uses it.
- [Python environment](environment.md) — the pinned packages, and the four chapter-specific ones.

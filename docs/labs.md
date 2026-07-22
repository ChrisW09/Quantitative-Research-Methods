# Lab notebooks

Fourteen notebooks (`Lab_Notebooks/chapter_NN_lab.ipynb`) mirror each chapter's
Python lab — including the precourse refresher and chapters 9, 11 and 12, which
are included for self-study.
Each notebook runs **locally or on Google Colab**; data loads via the `ISLP`
package with an automatic fallback to the bundled CSVs, so nothing needs
downloading by hand.

Every notebook is rendered in full below (with its stored outputs — the
documentation build never executes them).

## Lecture chapters

| Ch. | Lab | Read here | Open in Colab |
|:--:|---|:--:|:--:|
| 0 · Precourse Refresher | `chapter_00_lab.ipynb` | [Rendered](labs/chapter_00_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_00_lab.ipynb) |
| 1 · Introduction | `chapter_01_lab.ipynb` | [Rendered](labs/chapter_01_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_01_lab.ipynb) |
| 2 · Statistical Learning | `chapter_02_lab.ipynb` | [Rendered](labs/chapter_02_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_02_lab.ipynb) |
| 3 · Linear Regression | `chapter_03_lab.ipynb` | [Rendered](labs/chapter_03_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_03_lab.ipynb) |
| 4 · Classification | `chapter_04_lab.ipynb` | [Rendered](labs/chapter_04_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_04_lab.ipynb) |
| 5 · Resampling Methods | `chapter_05_lab.ipynb` | [Rendered](labs/chapter_05_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_05_lab.ipynb) |
| 6 · Model Selection & Regularization | `chapter_06_lab.ipynb` | [Rendered](labs/chapter_06_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_06_lab.ipynb) |
| 7 · Moving Beyond Linearity | `chapter_07_lab.ipynb` | [Rendered](labs/chapter_07_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_07_lab.ipynb) |
| 8 · Tree-Based Methods | `chapter_08_lab.ipynb` | [Rendered](labs/chapter_08_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_08_lab.ipynb) |
| 10 · Deep Learning | `chapter_10_lab.ipynb` | [Rendered](labs/chapter_10_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_10_lab.ipynb) |
| 13 · Multiple Testing | `chapter_13_lab.ipynb` | [Rendered](labs/chapter_13_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_13_lab.ipynb) |

## Self-study chapters

| Ch. | Lab | Read here | Open in Colab |
|:--:|---|:--:|:--:|
| 9 · Support Vector Machines | `chapter_09_lab.ipynb` | [Rendered](labs/chapter_09_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_09_lab.ipynb) |
| 11 · Survival Analysis | `chapter_11_lab.ipynb` | [Rendered](labs/chapter_11_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_11_lab.ipynb) |
| 12 · Unsupervised Learning | `chapter_12_lab.ipynb` | [Rendered](labs/chapter_12_lab) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_12_lab.ipynb) |

```{admonition} Private repository
:class: warning

While the repository is private, the Colab badges open only for Google accounts
that have access to it.
```

## How the notebooks find their data

Each notebook opens with a setup cell that:

1. detects whether it is running on Colab and installs any missing packages
   (`ISLP`, plus `pygam` / `xgboost` / `lifelines` for the chapters that need
   them — `torch` is preinstalled on Colab);
2. loads each dataset from the `ISLP` package where possible (12 of the 13
   datasets used in the labs), streams `Advertising` from the book's official
   site, and falls back to the bundled
   [`ALL CSV FILES - 2nd Edition/`](datasets.md) folder otherwise.

So a fresh Colab runtime works with no manual downloads, and a local checkout
works offline.

## All notebooks

```{toctree}
:maxdepth: 1
:glob:

labs/chapter_*_lab
```

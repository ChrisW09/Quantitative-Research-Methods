# Python for Data Science Workshop

A separate, self-contained **beginner Python course** — not part of the
Quantitative Research Methods (ISLP) course this repository otherwise holds,
and with no prerequisites in common. It is vendored here for convenient local
access; it keeps its own structure, audience and licence, and its own Colab
links (rebased to this repo's copy below).

Two tracks: a 90-minute live introduction, then a self-paced deep dive from
Python fundamentals to a first PyTorch model.

## 🐣 Track 1 — Introduction Session (90 minutes, live)

Five short notebooks, ~75 minutes of content plus ~15 minutes of questions and
discussion, with a sixth optional bonus. Every notebook is Colab-ready — no
installation needed.

| # | Notebook | Time | Covers |
|---|---|:--:|---|
| 1 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/01_welcome_to_python.ipynb) **Welcome to Python** | ~15 min | What Python is and why it matters for Data Science & AI; notebooks; basic syntax; variables; data types; arithmetic; f-strings |
| 2 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/02_data_structures.ipynb) **Data Structures** | ~18 min | Lists, tuples/sequences, dictionaries — what each is for and basic operations |
| 3 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/03_control_flow.ipynb) **Control Flow** | ~12 min | `if / elif / else`, `for` loops, `while` loops — short and conceptual |
| 4 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/04_functions.ipynb) **Functions** | ~12 min | What functions are, defining and calling, parameters, return values, structuring code |
| 5 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/05_pandas_intro.ipynb) **First Steps with Pandas** | ~18 min | DataFrames, loading tabular data, inspection, selecting/filtering, simple manipulation, a first chart |
| ✨ | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/01_introduction/06_seaborn_intro.ipynb) **A First Look at Seaborn** *(bonus, optional)* | ~10 min | The same chart in one line; `hue=` for colour by category; what a seaborn bar chart averages for you |

Session plan with timings and instructor notes:
[`01_introduction/README.md`](./01_introduction/README.md).

## 🚀 Track 2 — Advanced & Self-Learning (self-paced, ~12–14 h)

Fifteen notebooks that build directly on Track 1 and go substantially deeper.

**Python fundamentals — in depth**

| # | Notebook | Time |
|---|---|:--:|
| 1 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/01_python_basics.ipynb) **Python Basics** — types, conversion pitfalls, rounding, float precision | 30–35 min |
| 2 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/02_control_structures.ipynb) **Control Structures** — loops in depth, convergence, `break`/`continue`, `try`/`except` | 35–40 min |
| 3 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/03_lists_data_structures.ipynb) **Lists and Sequences** — slicing, comprehensions, `zip`, tuples, aliasing | 30–40 min |
| 4 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/04_dictionaries_advanced.ipynb) **Dictionaries and Nested Data** — nested structures, counting, JSON | 35–45 min |
| 5 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/05_functions_and_modules.ipynb) **Functions and Modules** — `return` vs `print`, `*args`/`**kwargs`, scope, imports | 35–40 min |

**Data science toolkit**

| # | Notebook | Time |
|---|---|:--:|
| 6 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/06_numpy_fundamentals.ipynb) **NumPy Fundamentals** — arrays, vectorisation, broadcasting, axes | 45–55 min |
| 7 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/07_pandas_essentials.ipynb) **Pandas Essentials** — `loc`/`iloc`, boolean masks, `groupby` | 45–55 min |
| 8 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/08_data_cleaning_preprocessing.ipynb) **Data Cleaning and Preprocessing** — missing values, dtypes, duplicates, outliers, scaling, encoding | 45–55 min |
| 9 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/09_visualization_matplotlib.ipynb) **Visualisation with Matplotlib** — Figure/Axes, choosing the right chart, subplots | 50–60 min |
| 10 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/10_visualization_seaborn.ipynb) **Visualisation with Seaborn** — long data, faceting, distributions, heatmaps, palettes | 50–60 min |
| 11 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/11_exploratory_data_analysis.ipynb) **Exploratory Data Analysis** — the EDA workflow on a real dataset | 50–60 min |

**Machine learning & deep learning**

| # | Notebook | Time |
|---|---|:--:|
| 12 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/12_machine_learning_basics.ipynb) **Machine Learning Basics** — supervised vs unsupervised, features/target, train/test, evaluation, overfitting | 45–55 min |
| 13 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/13_scikit_learn_workflow.ipynb) **The Scikit-Learn Workflow** — classification, regression, pipelines, `GridSearchCV` | 70–85 min |
| 14 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/14_pytorch_basics.ipynb) **PyTorch Basics** — tensors, autograd, a small neural network, the training loop | 50–60 min |

**Capstone**

| # | Notebook | Time |
|---|---|:--:|
| 15 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Python_Course/02_advanced_self_learning/15_capstone_project.ipynb) **Capstone Project** — a full end-to-end analysis | 75–105 min |

Track overview and learning path:
[`02_advanced_self_learning/README.md`](./02_advanced_self_learning/README.md).

## ☁️ Working in Google Colab

Every notebook is fully Colab-ready: no installation, no downloads, no local
files. Click any **Open in Colab** badge above, or the badge in the first cell
of each notebook. Colab opens it read-only from GitHub — use **File → Save a
copy in Drive** once to keep your edits, then **Runtime → Run all**.

## Source

Imported from
[BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop](https://github.com/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop)
at commit `94930a6`, part of the
[Bridging AI & Society Summer Schools](https://bridgingaiandsociety.org).
Licensed under the MIT License (see `LICENSE` in this folder) — copyright the
Python Data Science Course authors, not Prof. Dr. Christoph Weisser.

For updates, issues or the latest version, use the upstream repository linked
above rather than this copy.

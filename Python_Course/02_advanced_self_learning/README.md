<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BridgingAISocietySummerSchools/.github/main/assets/logo-lockup-on-dark.svg">
  <img src="https://raw.githubusercontent.com/BridgingAISocietySummerSchools/.github/main/assets/logo-lockup.svg" alt="Bridging AI & Society Summer Schools" width="320">
</picture>

# 🚀 Track 2 — Advanced & Self-Learning (self-paced)

The depth of the course: **15 notebooks, roughly 12–14 hours** of focused work. It revisits everything from the [90-minute Introduction Session](../01_introduction/) in substantially more detail, then goes far beyond it — data cleaning, visualisation with matplotlib and seaborn, exploratory data analysis, machine learning with scikit-learn, and an introduction to PyTorch, finishing with an end-to-end capstone project.

**Designed for independent study.** Each notebook builds on the previous ones and states what it assumes, so you are never starting from zero — but there is enough explanation and worked example to learn on your own, without an instructor.

> ☁️ **Colab tip:** notebooks open read-only from GitHub — click **File → Save a copy in Drive** once at the start so your exercise solutions persist. **Runtime → Run all** works in every notebook. Each notebook also carries its own *Open in Colab* badge in the first cell.

## 🧱 Python Fundamentals — in depth

Revisits Track 1's foundation and adds the depth a practitioner needs.

| # | Notebook | Time | Covers |
|---|----------|------|--------|
| 1 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/01_python_basics.ipynb) [Python Basics](01_python_basics.ipynb) | 30–35 min | Types and conversion pitfalls, rounding surprises, float precision, strings |
| 2 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/02_control_structures.ipynb) [Control Structures](02_control_structures.ipynb) | 35–40 min | `if/elif/else`, loops, convergence loops, `break/continue`, `try/except` |
| 3 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/03_lists_data_structures.ipynb) [Lists and Sequences](03_lists_data_structures.ipynb) | 30–40 min | Indexing, the slicing model, comprehensions, `zip`, tuples, aliasing |
| 4 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/04_dictionaries_advanced.ipynb) [Dictionaries and Nested Data](04_dictionaries_advanced.ipynb) | 35–45 min | Key-value lookup, nested data, list-of-dicts as a table, counting, JSON |
| 5 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/05_functions_and_modules.ipynb) [Functions and Modules](05_functions_and_modules.ipynb) | 35–40 min | Parameters, defaults, `return` vs `print`, `*args`/`**kwargs`, scope, imports |

## 🧰 Data Science Toolkit

| # | Notebook | Time | Covers |
|---|----------|------|--------|
| 6 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/06_numpy_fundamentals.ipynb) [NumPy Fundamentals](06_numpy_fundamentals.ipynb) | 45–55 min | Arrays, vectorisation, broadcasting, axes, reproducible randomness |
| 7 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/07_pandas_essentials.ipynb) [Pandas Essentials](07_pandas_essentials.ipynb) | 45–55 min | Series, DataFrames, `loc`/`iloc`, boolean masks, `groupby` |
| 8 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/08_data_cleaning_preprocessing.ipynb) [Data Cleaning and Preprocessing](08_data_cleaning_preprocessing.ipynb) | 45–55 min | Missing values, dtypes, duplicates, categories, outliers, scaling, encoding |
| 9 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/09_visualization_matplotlib.ipynb) [Visualisation with Matplotlib](09_visualization_matplotlib.ipynb) | 50–60 min | Figure/Axes model, choosing the right chart, subplots, annotations |
| 10 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/10_visualization_seaborn.ipynb) [Visualisation with Seaborn](10_visualization_seaborn.ipynb) | 50–60 min | Long data, axes- vs figure-level, distributions, categorical plots, faceting, heatmaps, palettes |
| 11 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/11_exploratory_data_analysis.ipynb) [Exploratory Data Analysis](11_exploratory_data_analysis.ipynb) | 50–60 min | The EDA workflow on a real dataset: distributions, relationships, correlation |

## 🤖 Machine Learning & Deep Learning

| # | Notebook | Time | Covers |
|---|----------|------|--------|
| 12 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/12_machine_learning_basics.ipynb) [Machine Learning Basics](12_machine_learning_basics.ipynb) | 45–55 min | What ML is, supervised vs unsupervised, features/target, train/test, evaluation, overfitting |
| 13 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/13_scikit_learn_workflow.ipynb) [The Scikit-Learn Workflow](13_scikit_learn_workflow.ipynb) | 70–85 min | Classification and regression in practice, pipelines, metrics, `GridSearchCV` |
| 14 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/14_pytorch_basics.ipynb) [PyTorch Basics](14_pytorch_basics.ipynb) | 50–60 min | Tensors, autograd, a small neural network, the training loop |

## 🏆 Capstone

| # | Notebook | Time | Covers |
|---|----------|------|--------|
| 15 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/02_advanced_self_learning/15_capstone_project.ipynb) [Capstone Project](15_capstone_project.ipynb) | 75–105 min | End-to-end project: data, EDA, dashboard, regression, executive summary |

## 🧭 Suggested pace

Work through the notebooks **in order** — each assumes the previous ones.

| Pace | Plan |
|------|------|
| 1 notebook / day | Done in about three weeks |
| 3–4 notebooks / weekend | Done in about four weekends |
| Intensive week | The whole track in 4–5 focused days |

If you attended the live session, notebooks 1–7, 9 and 10 will feel partly familiar by design: each opens with a short **"🔗 Building on Track 1"** note telling you what is recap and what is new, so you can move quickly through the parts you know.

## 🧪 What's inside each notebook?

1. **Header** — track position, time estimate, learning objectives, prerequisites.
2. **A "🔗 Building on Track 1" note** where the topic was introduced in the live session.
3. **Intuition first**, then code, then interpretation of what the output means.
4. **Exercises with complete solutions** (collapsed), including a *"Debug me 🐞"* challenge.
5. **Key takeaways**, a **self-assessment checklist**, and a pointer to the next notebook.

## ➡️ After the capstone

Continue with the summer school's [Hands-On-Notebooks](https://github.com/BridgingAISocietySummerSchools/Hands-On-Notebooks) — a visual, intuition-driven collection on linear models, decision trees, random forests, and gradient boosting.

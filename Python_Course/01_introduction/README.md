<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BridgingAISocietySummerSchools/.github/main/assets/logo-lockup-on-dark.svg">
  <img src="https://raw.githubusercontent.com/BridgingAISocietySummerSchools/.github/main/assets/logo-lockup.svg" alt="Bridging AI & Society Summer Schools" width="320">
</picture>

# 🐣 Track 1 — Introduction Session (90 minutes, live)

A single instructor-led session for **complete beginners** — no coding experience assumed. It is the hands-on Python session of the [Bridging AI & Society Summer Schools](https://bridgingaiandsociety.org): accessible, interactive, and connected to questions about data and society.

**This track is a guided tour, not a complete course.** In 90 minutes students meet the whole Python/Data-Science ecosystem at a basic level — variables, data structures, control flow, functions, and pandas — and leave able to read simple code, run a notebook, and continue on their own. Depth is deliberately deferred to [Track 2](../02_advanced_self_learning/).

## 🚀 Open the notebooks in Google Colab

No installation needed — just a Google account.

| # | Notebook | Time | Covers |
|---|----------|------|--------|
| 1 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/01_welcome_to_python.ipynb) [Welcome to Python](01_welcome_to_python.ipynb) | ~15 min | What Python is, how notebooks work, basic syntax, variables, data types, arithmetic, f-strings |
| 2 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/02_data_structures.ipynb) [Data Structures](02_data_structures.ipynb) | ~18 min | Lists, tuples/sequences, dictionaries — and the list-of-dicts "table" shape |
| 3 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/03_control_flow.ipynb) [Control Flow](03_control_flow.ipynb) | ~12 min | `if / elif / else`, `for` loops, `range()`, `while` loops |
| 4 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/04_functions.ipynb) [Functions](04_functions.ipynb) | ~12 min | Why functions, `def`, parameters, `return` values, structuring code |
| 5 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/05_pandas_intro.ipynb) [First Steps with Pandas](05_pandas_intro.ipynb) | ~18 min | DataFrames, `read_csv`, inspecting, selecting, filtering, a computed column, `groupby`, a chart |
| ✨ | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BridgingAISocietySummerSchools/Python-for-Data-Science-Workshop/blob/main/01_introduction/06_seaborn_intro.ipynb) [A First Look at Seaborn](06_seaborn_intro.ipynb) — **bonus, optional** | ~10 min | The same chart in one line, `hue=` for colour by category, and what a seaborn bar chart averages behind your back |

**Content total: ~75 minutes** — the remaining ~15 minutes of the 90 are the questions, discussion, and breathing room that make the session work.

**The seaborn notebook is deliberately outside that budget.** It is a self-contained ten-minute bonus: run it live only if the group is ahead of schedule, and otherwise send everyone home with it. It rebuilds its own data, so nobody who skips it is left behind.

## ⏱️ Suggested session plan (90 minutes)

| Time | Segment |
|------|---------|
| 0:00 – 0:05 | Welcome; everyone opens Notebook 1 in Colab and runs the first cell |
| 0:05 – 0:20 | **Notebook 1 — Welcome to Python** |
| 0:20 – 0:40 | **Notebook 2 — Data Structures** (+ questions) |
| 0:40 – 0:54 | **Notebook 3 — Control Flow** |
| 0:54 – 1:08 | **Notebook 4 — Functions** |
| 1:08 – 1:28 | **Notebook 5 — First Steps with Pandas** (the payoff) |
| 1:28 – 1:30 | Wrap-up: how to continue with Track 2 |
| *(spare)* | *Optional bonus — Notebook 6: A First Look at Seaborn (~10 min), if the group is running early* |

Timings include the built-in **"🎯 Try it (1–2 min)"** micro-exercises and short **"💬 Discuss"** prompts. If the group is slower than planned, the discussion prompts and the later exercises in notebooks 3–4 are the intended things to drop — notebook 5 is the payoff and should not be sacrificed.

## 🧑‍🏫 Instructor notes

- **Live-coding beats slides.** Project the notebook and type along with the group; participants run each cell themselves.
- **Have everyone save a copy first.** Colab opens notebooks read-only from GitHub. Ask participants to click **File → Save a copy in Drive** right at the start so their edits and exercise solutions persist.
- **The Shift+Enter moment matters.** Spend the first minutes making sure *everyone* has executed a cell successfully — the rest of the session depends on it.
- **Resist depth.** Every notebook deliberately stops short: no slicing rules, no `break`/`continue`, no `try/except`, no `*args`, no `loc`/`iloc`. When a sharp question arrives, name the concept, say it is covered in Track 2, and move on — that is the design, not a gap.
- **Use the discussion prompts.** Thirty seconds of pair discussion re-engages non-technical participants and ties the session to the summer school's AI & society theme.
- **Solutions are built in.** Every exercise has a collapsed solution, so participants who fall behind can catch up on their own.
- **The seaborn bonus is a buffer, not a sixth lesson.** Notebook 6 exists so that a fast group has somewhere to go and everyone has a short, satisfying thing to run at home. Never cut into Notebook 5 for it.

## ➡️ After the session

Point participants to the **[Advanced & Self-Learning track](../02_advanced_self_learning/)**: 15 self-paced notebooks that revisit everything from this session in depth, then continue into data cleaning, visualisation with matplotlib and seaborn, exploratory data analysis, machine learning with scikit-learn, and an introduction to PyTorch — finishing with a capstone project.

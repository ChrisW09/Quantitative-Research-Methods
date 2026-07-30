# STYLE_NOTEBOOK.md — How to author a lab notebook in this course's house style

This brief lets you write a Jupyter notebook indistinguishable from the existing
`Lab_Notebooks/chapter_XX_lab.ipynb` files (canonical short example: chapter 13,
18 cells; richer example: chapter 7, 29 cells). Follow it exactly.

---

## 1. Notebook-level metadata

- Kernel: `python3` / "Python 3". Notebook metadata carries a `"title"` key, e.g.
  `"title": "Chapter 13 Lab — Multiple Testing"` (em-dash, not hyphen).
- **Notebooks ship WITH stored outputs.** Execute the whole notebook top-to-bottom
  before committing, so every code cell shows its real output (text, tables, figures).

## 2. The fixed opening sequence (cells 0–4)

**Cell 0 — markdown, Colab badge:**

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Lab_Notebooks/chapter_13_lab.ipynb)

*This notebook runs on Colab as-is. The badge link above and the `GITHUB_RAW` line in the setup cell already point to this repository, so everything installs and loads automatically.*
```

For a notebook living in **`Advanced/Lab_Notebooks/`**, the badge URL path must be
`.../blob/main/Advanced/Lab_Notebooks/chapter_XX_lab.ipynb` (only the path segment
changes; repo stays `ChrisW09/Quantitative-Research-Methods`).

**Cell 1 — markdown, header:**

```markdown
# Chapter 13 — Multiple Testing
## Lab: Bonferroni, Holm, Benjamini–Hochberg, permutation tests

**Course:** Quantitative Research Methods  
**Instructor:** Prof. Dr. Christoph Weisser, HSBI  
**Source:** James, Witten, Hastie, Tibshirani & Taylor (2023), *An Introduction to Statistical Learning, with Applications in Python*, Springer. Companion code at [statlearning.com](https://www.statlearning.com).
```

(H1 = "Chapter N — Title"; H2 = "Lab: " + comma-separated topic list; the three bold
fields end with two trailing spaces for hard line breaks. Cite the publisher/official
site only — never a retailer.)

**Cell 2 — markdown, Goal (one sentence, semicolon-chained):**

```markdown
**Goal.** Run a multiple-testing simulation; compare FWER- and FDR-controlling procedures; build a permutation $p$-value.
```

**Cell 3 — markdown, Setup preamble:**

```markdown
## Setup

Run this cell once. The `ISLP` package can be installed with `pip install ISLP`. As an alternative, the same data sets are available as CSVs in the workspace's `ALL CSV FILES - 2nd Edition` folder.


> **Google Colab:** this notebook also runs on Colab out of the box — the setup cell below installs any missing packages and downloads the data automatically.
```

**Cell 4 — code, THE setup cell.** Copy this VERBATIM from chapter_13 as the template:

```python
# --- Setup: runs locally AND on Google Colab --------------------------------
# Silence only the spurious 'encountered in matmul' RuntimeWarnings that the macOS
# Accelerate BLAS emits; real warnings (deprecations, model caveats) stay visible.
import warnings
warnings.filterwarnings('ignore', message='.*encountered in matmul', category=RuntimeWarning)
import importlib.util, os, subprocess, sys

IN_COLAB = 'google.colab' in sys.modules

def _ensure(pkg, import_name=None):
    """pip-install pkg (quietly) if its import is missing."""
    if importlib.util.find_spec(import_name or pkg) is None:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg], check=False)

if IN_COLAB:  # Colab ships numpy/pandas/sklearn/statsmodels; add course extras
    for _pkg, _imp in [('ISLP', 'ISLP')]:
        _ensure(_pkg, _imp)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(2024)
plt.rcParams['figure.dpi'] = 110

try:
    from ISLP import load_data
    HAVE_ISLP = True
except ImportError:
    HAVE_ISLP = False
    print('ISLP not installed; using CSV / URL fallbacks.')

# Local CSV location (repo layout first, then legacy paths, then a data/ cache).
_CANDIDATES = ['../ALL CSV FILES - 2nd Edition',
               'ALL CSV FILES - 2nd Edition',
               '../../ALL CSV FILES - 2nd Edition', 'data']
CSV = next((p for p in _CANDIDATES if os.path.isdir(p)), 'data')

# GITHUB_RAW lets a fresh Colab runtime fetch any
# CSV that is neither in ISLP nor already local (spaces in the folder -> %20).
GITHUB_RAW = ('https://raw.githubusercontent.com/ChrisW09/Quantitative-Research-Methods/main/'
              'ALL%20CSV%20FILES%20-%202nd%20Edition')

# The four datasets NOT in the ISLP package -> load from the book's official
# site so the notebook works on a fresh Colab even before the repo is published.
KNOWN_URLS = {
    'Advertising': 'https://www.statlearning.com/s/Advertising.csv',
    'Heart':       'https://www.statlearning.com/s/Heart.csv',
    'Income1':     'https://www.statlearning.com/s/Income1.csv',
    'Income2':     'https://www.statlearning.com/s/Income2.csv',
}

def load(name, **read_csv_kwargs):
    """Load a course dataset. Order: ISLP package -> R datasets -> local CSV
    -> official book URL -> your GitHub repo. Works locally and on Colab."""
    if HAVE_ISLP:
        try:
            return load_data(name)
        except Exception:
            pass
    if name == 'USArrests':                       # classic R dataset, not in ISLP
        try:
            import statsmodels.api as sm
            return sm.datasets.get_rdataset('USArrests', 'datasets').data
        except Exception:
            pass
    path = f'{CSV}/{name}.csv'
    if os.path.exists(path):                      # running from the repo (local)
        return pd.read_csv(path, **read_csv_kwargs)
    remotes = ([KNOWN_URLS[name]] if name in KNOWN_URLS else []) + [f'{GITHUB_RAW}/{name}.csv']
    for url in remotes:                           # fresh Colab: stream over https
        try:
            return pd.read_csv(url, **read_csv_kwargs)
        except Exception:
            continue
    raise FileNotFoundError(
        f"Could not load {name!r}. Put the CSV in '{CSV}/' or check your connection for the GITHUB_RAW fallback.")
```

**Adaptations for a notebook in `Advanced/Lab_Notebooks/`:** none inside this cell
except awareness — the `_CANDIDATES` list already contains
`'../../ALL CSV FILES - 2nd Edition'`, which is exactly the relative path from
`Advanced/Lab_Notebooks/` to the repo-root CSV folder, so local loading works as-is.
Only the Colab badge URL in cell 0 changes (see above). If the chapter needs extra
pip packages on Colab (e.g. `pygam`), add them to the `for _pkg, _imp in [...]` list.

## 3. Body structure

- Numbered H2 sections: `## 1. <Topic>`, `## 2. <Topic>`, … Each section is a short
  markdown cell (title, at most a line or two of prose — chapter 7's GAM section adds
  just "Requires `pip install pygam`.") followed by 1–3 code cells.
- Section topics mirror the deck's "Python lab" slide, which lists them as §1, §2, …
  Keep names in sync between deck and notebook.
- Data is loaded through the `load()` helper (`Wage = load('Wage')`) — never a raw
  hard-coded `pd.read_csv` path in body cells.
- Code cells are short (5–20 lines), self-contained steps ending in a `print(...)`,
  a `.summary()` or a `plt.show()`, so every cell produces a visible output.
- Figures: `fig, ax = plt.subplots(figsize=(6, 4))` (or `(7, 4)`, `(10, 4)` for pairs),
  scatter with `s=4..12, alpha=0.3..0.6`, line overlays in matplotlib cycle colours
  `'C1'`, `'C3'`, `ax.set(xlabel=..., ylabel=...)`, end with `plt.show()`.
  Global dpi comes from the setup cell (`plt.rcParams['figure.dpi'] = 110`) — do not
  set dpi per figure.
- Seeding: the setup cell creates `rng = np.random.default_rng(2024)`; body cells use
  that `rng` (functions take `rng=rng` as a default argument). Cells that reproduce a
  slide solution re-seed with the slide's seed (e.g. `rng = np.random.default_rng(0)`)
  so printed numbers match the deck.
- Optional dependencies are guarded with `try: ... except ImportError: print('pyGAM
  not installed; pip install pygam')` and later cells check `if gam is not None:`.
- Markdown tone: compact, didactic, en/em-dashes, LaTeX inline math (`$m = 1000$`,
  `$5\,\%$`). Interpretation paragraphs start with a bold lead-in:
  `**Reading the output.**`, `**How to read the overlay.**`, `**(c) Interpretation.**`
  Code comments: banner style `# (a) ... -------` to bind a cell to an exercise part,
  plus short trailing `#` comments explaining the *why*, not the *what*.

## 4. Closing sections (fixed pattern)

**"Lecture exercises — worked Python solutions"** (H2, after the numbered tutorial
sections) opens with:

```markdown
## Lecture exercises — worked Python solutions

These are the **[Python]-tagged exercises from the lecture slides**, solved step by step. Run each cell and compare with the slide solutions.
```

(Chapter 7's variant adds "...; run them cell by cell. Data loads through the `load()`
helper defined in the Setup cell, so every cell works locally and on Colab.")

Then, per exercise:
- an H3 markdown cell whose title matches the slide exactly, tag included:
  `### Extended Exercise 13.3 — Simulating FDR and power [Python]`, followed by a
  restatement of the task (`**Task (from the slides).**` + numbered list, or a short
  paragraph with the parameters in backticks);
- one or more code cells reproducing the slide's solution code with the same seed and
  the same expected printout (a trailing comment may state
  `# Expected: bh FDR=0.090 power=0.723 ; ...`);
- a markdown interpretation cell (`**Reading the output.** ...`) matching the slide's
  take-away.

**Final cell — open exercises** (markdown, H2, numbered list of 4 short prompts for
self-study; numbered as the next section, e.g. `## 5. Exercises` / `## 6. Exercises`):

```markdown
## 5. Exercises
1. Increase $m$ to 10 000 and re-run. How does power change?
2. Replace `0.6` with `0.3` (smaller effect) and observe how FDR and power respond.
...
```

## 5. Environment constraints on THIS machine (critical)

- **`ISLP` is NOT installed locally.** The setup cell's CSV fallback must carry the
  whole notebook: every dataset you use must exist as
  `ALL CSV FILES - 2nd Edition/<Name>.csv` at the repo root (reachable via the
  `'../../ALL CSV FILES - 2nd Edition'` candidate from `Advanced/Lab_Notebooks/`), or be
  simulated. Expect and keep the printed line `ISLP not installed; using CSV / URL
  fallbacks.` in the stored setup-cell output.
- **`seaborn` is NOT installed.** matplotlib (plus pandas plotting) only.
- **`nbconvert` is NOT installed; `nbclient` IS** (0.10.2). Execute notebooks with
  nbclient, e.g.:
  ```bash
  cd "Advanced/Lab_Notebooks" && python3 - <<'EOF'
  import nbformat
  from nbclient import NotebookClient
  nb = nbformat.read('chapter_XX_lab.ipynb', as_version=4)
  NotebookClient(nb, timeout=600, kernel_name='python3').execute()
  nbformat.write(nb, 'chapter_XX_lab.ipynb')
  EOF
  ```
  Run from the notebook's own directory so the relative CSV candidates resolve.
- Available locally: numpy, pandas, matplotlib, scipy, statsmodels, scikit-learn,
  and pygam. Anything else must still be optional-guarded (try/except ImportError)
  exactly like chapter 7 does with pygam, so the notebook survives a fresh Colab
  or a leaner machine.
- The spurious macOS Accelerate `matmul` RuntimeWarning filter at the top of the setup
  cell is deliberate — keep it.

## 6. Checklist before committing

1. Badge URL points at the notebook's real path under `Advanced/Lab_Notebooks/`.
2. Header cell: title, "Lab:" subtitle, Course / Instructor (Prof. Dr. Christoph
   Weisser, HSBI) / Source lines present.
3. Setup cell verbatim (plus any Colab-only extra packages) and `rng = np.random.default_rng(2024)`.
4. Section numbering contiguous; names match the deck's Python-lab slide.
5. Every `[Python]` exercise from the deck appears under "Lecture exercises — worked
   Python solutions" with matching title, seed and printed numbers.
6. Closing numbered "Exercises" markdown cell present.
7. Executed end-to-end with nbclient on this machine; outputs stored; no error outputs;
   figures render at the default 110 dpi.

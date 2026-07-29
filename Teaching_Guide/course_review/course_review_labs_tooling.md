# Quantitative Research Methods — review of the labs, the tooling, and the student's first week

Prof. Weisser — this covers the fifteen lab notebooks, the install and build
infrastructure, and what a student actually experiences. I did not touch a
single repository file. Everything below is anchored to a `file:line`, a
notebook cell index, or a command I ran; where I am guessing about students
rather than measuring something, I say so explicitly.

Two caveats up front. `Makefile` and `Lab_Notebooks/chapter_03_lab.ipynb` were
being edited by other agents while I worked (`git status --porcelain` showed
both dirty, and HEAD moved from `2e1e1f2` to `1ad1891` mid-session), so treat
my chapter-3 notebook observations as provisional. And `Mock_Exams/` I left
alone entirely.

---

## 1. Where things stand

**The labs are in much better technical shape than the framing of this review
assumed, and the specific defects are narrower and sharper than "loose pins".**
I want to establish that with measurements before recommending anything,
because it changes what is worth doing.

I built two environments and executed the notebooks in both.

*Environment A* — your own interpreter (Python 3.9.6, numpy 2.0.2,
pandas 2.3.3, scikit-learn 1.6.1, statsmodels 0.14.6), with **ISLP deliberately
absent** so the bundled-CSV fallback was exercised. Thirteen notebooks (all but
10 and 11, which need `torch` and `lifelines`) ran top to bottom: **zero
errors**, ~50 s total.

*Environment B* — a realistic 2026 student laptop. `uv venv --python 3.12` plus
`pip install -r requirements.txt` resolved to **numpy 2.5.1, pandas 3.0.5,
scikit-learn 1.9.0, ISLP 0.4.1, torch 2.13.0, pygam 0.12.0, scipy 1.16.3** —
i.e. a stack two to three years ahead of yours, including a pandas *major*
version bump. All **fifteen** notebooks ran top to bottom: **zero errors**,
58 s total.

That is a genuinely strong result and it is not an accident. Every notebook
carries stored outputs with strictly sequential execution counts 1..N and no
error or stderr outputs anywhere (checked programmatically across all 15 —
188 code cells with output, 61 stored figures, 0 errors). The `load()` helper
at cell 4 of every notebook, with its ISLP → R-datasets → local CSV → official
URL → GitHub-raw cascade, is the single best-engineered thing in the repo.

**But the version-drift story is real, and it is concentrated in three places
rather than spread thinly.** I diffed every text output, shipped vs freshly
executed on the 2026 stack: 29 of 202 code cells differ. Most of that is noise
— `statsmodels` prints `Date:`/`Time:` in every summary header, `lifelines`
prints `time fit was run`, and random-forest importances move in the third
decimal. Three findings are not noise:

**(a) `chapter_05_lab.ipynb` cells 8, 10 and 12 now teach the opposite of what
they shipped.** Shipped 10-fold CV MSE by polynomial degree: `19.276, 19.478,
19.137, 19.255, 19.150, 18.962, 19.099, 19.866` — flat, the classic "CV can't
tell these apart" picture. On the 2026 stack: `20.275, 23.057, 26.729, 30.612,
34.376, 37.895, 41.123, 44.040` — a monotone explosion. Same for the
validation-set cell (degree 5: `18.324` → `27.871`) and LOOCV. The plotted
figure in that lab is a different figure.

I found the cause and verified the fix. The pipeline is
`make_pipeline(PolynomialFeatures(degree=d), LinearRegression())` on **raw
`horsepower`** (values 46–230), so degree-10 columns reach ~10²³ and the answer
depends entirely on how `lstsq` handles a catastrophically conditioned design.
I ran both variants in both environments:

```
### py3.9 / sklearn 1.6.1
AS-SHIPPED (raw poly)    [24.208, 19.185, 19.276, 19.478, 19.137, 19.255, 19.150, 18.962, 19.099, 19.866]
SCALED FIRST             [24.208, 19.185, 19.276, 19.478, 19.137, 19.050, 18.822, 18.901, 19.082, 19.890]
### py3.12 / sklearn 1.9.0
AS-SHIPPED (raw poly)    [24.208, 19.185, 20.275, 23.057, 26.729, 30.612, 34.376, 37.895, 41.123, 44.040]
SCALED FIRST             [24.208, 19.185, 19.276, 19.478, 19.137, 19.050, 18.822, 18.901, 19.082, 19.890]
```

Inserting `StandardScaler()` ahead of `PolynomialFeatures` makes the numbers
**identical across a three-year version gap**. It is a one-token edit, it
removes the drift, and it is the pipeline discipline your Chapter 5 lecture
teaches. This is the best-value fix in the whole review. The same pattern
mildly affects `chapter_07_lab.ipynb` cell 25 (degree-5 CV MSE 1598.2 → 1611.9).

**(b) `chapter_08_lab.ipynb` cell 26: single-tree test MSE 26.67 → 16.49.** A
38 % move in an unpruned `DecisionTreeRegressor(random_state=1)` — sklearn
changed splitter tie-breaking. The consequence is in the prose: cell 30 says
"single tree ≈ 26.7 → bagging ≈ 8.5 … Every ensemble cuts the single tree's
error three- to four-fold." On a current stack it is 16.49 → 8.57, a **two-fold**
cut, and the sentence is simply wrong. The interpretive claim was pinned to one
run of one seed on one sklearn.

**(c) `chapter_07_lab.ipynb` cells 15 and 20: pyGAM broke.** Log-likelihood
−24864.6 → −15299.7, AIC 49773.7 → 30643.7, Scale 1585.99 → **39.82**, between
pygam 0.10.1 and 0.12.0. `requirements.txt:16` says `pygam>=0.9`, so students
get 0.12. A student reading your interpretation paragraph alongside their own
summary table sees a 60 % different fit statistic.

**The bigger threat to "my numbers don't match" is not sklearn — it is the
ISLP-vs-CSV branch.** With ISLP absent, the documented fallback path silently
produces *different data*:

- `Auto` from the CSV has 9 columns including `name`, and `horsepower` as
  float. `chapter_02_lab.ipynb` cell 10 prints `(392, 8)` in the shipped
  output and `(392, 9)` on the CSV path. `chapter_05_lab.ipynb` cell 6 shows
  `130` vs `130.0` in the very first data cell of the lab.
- `Bikeshare` from the CSV carries a stray `Unnamed: 0`;
  `chapter_04_lab.ipynb` cell 15 exists purely to print `Bike.columns`, so the
  artefact is on screen.
- `chapter_03_lab.ipynb` cell 18 branches on `HAVE_ISLP` and the two branches
  produce **completely different regression tables** —
  `poly(lstat, degree=2)[0] = -71.4385` (orthogonal basis) versus
  `lstat = -2.2980` (raw), with Cond. No. 1.39e+05 vs 7.09e+03. Both are
  correct; only one matches the slide.
- `NCI60` has **no** fallback. `chapter_01_lab.ipynb` cell 17 and
  `chapter_12_lab.ipynb` cell 16 print "only ships with the ISLP package" and
  the figure never appears.
- `USArrests` is **not** in `ALL CSV FILES - 2nd Edition/` at all, so
  `chapter_12_lab.ipynb` reaches the network via
  `sm.datasets.get_rdataset`. `docs/labs.md:60-61` claims "a local checkout
  works offline". For Chapter 12 that is false.

**The install, not the clone, is the day-one bottleneck.** I measured both.
`git clone` of the public repo: 96 MB, 5.7 s; `--depth 1`: 35 MB, 3.1 s. Fine.
`pip install -r requirements.txt` resolved (dry-run with `--report`, then HEAD
on every wheel URL) to **151 packages, 244 MB** on macOS arm64. The dominant
item is `torch` — and it is **not optional**. `ISLP` 0.4.x declares
`['numpy', 'scipy', 'pandas', 'lxml', 'scikit-learn', 'joblib', 'statsmodels',
'lifelines', 'pygam', 'torch', 'pytorch-lightning', 'torchmetrics']`, so
`requirements.txt:13` alone drags in the whole deep-learning stack. Platform
figures for torch 2.8 cp312 from the PyPI JSON API: macOS arm64 73.6 MB,
**win_amd64 241.3 MB**, **manylinux x86_64 887.9 MB plus twelve `nvidia-cu12`
packages**. Your students are mostly on Windows.

This makes `docs/environment.md:44-49` factually wrong. The "Minimal install"
tip says that for Chapters 1–6, "`numpy`, `pandas`, `matplotlib`, `seaborn`,
`scipy`, `statsmodels`, `scikit-learn`, `ISLP` and `jupyter` are enough" —
implying a small install. Including `ISLP` makes it the *large* install. For
comparison I resolved a core-only file (no ISLP/torch/pygam/xgboost/lifelines):
**114 packages, 126 MB**, and I have already proved 13 of 15 notebooks run
clean without ISLP.

**On pedagogy, the notebooks are excellent explanations and weak exercises.**
The structure is identical in all fifteen: a linear demo (§1…§N), then
"Lecture exercises — worked Python solutions", then a terminal `## Exercises`
list of 3–5 unsolved prompts. The interpretation prose is genuinely first-rate
— `chapter_06_lab.ipynb` cell 26, `chapter_02_lab.ipynb` cell 28 and the
`*Common mistake:*` closers in `chapter_05_lab.ipynb` cell 21 and
`chapter_07_lab.ipynb` cells 22 and 27 are the kind of writing students
actually learn from. But:

- I grepped all fifteen notebooks for `TODO`, `# your code`, `_____`, `<fill`,
  "complete the", "before running", "what do you expect", "guess". **Zero
  hits.** There is no fill-in-the-blank and no predict-then-run anywhere.
- There is exactly **one** deliberately-broken cell in the corpus —
  `chapter_00b_lab.ipynb`'s Exercise 0b.6, "The buggy version, reproduced" —
  and it is shown immediately followed by "The honest version", so the student
  never sits with the bug.
- Every worked solution ships in the same file the student opens, with its
  numeric answer as an inline comment (`# 2.553`, `# testMSE=119064.0`,
  `# best K = 14`) and its output stored. There is no version of
  `chapter_06_lab.ipynb` in which a student can attempt Exercise 6.7 without
  the answer three lines below.
- The three self-study chapters are the thinnest *and* have no worked
  solutions at all: `chapter_09_lab.ipynb` 6 code cells,
  `chapter_11_lab.ipynb` 7, `chapter_12_lab.ipynb` 7 (versus 20 for ch 3, 16
  for ch 8), each ending in a bare four-item `## 5. Exercises` list. The
  students with the least support get the least scaffolding.

**Decks and notebooks reinforce rather than duplicate — but the pointers are
too vague to use.** Measuring code-line overlap between each deck's `Python
Lab` section and its notebook: the deck carries 32–81 code lines, the notebook
113–200, and 32–78 % of deck lines have a notebook twin. The deck is a strict
20–35 % subset. That is a healthy ratio. The problem is the `labnote` boxes.
There are **14 in 22,399 lines of deck source**, and nine decks have exactly
one; the string "Data loads via the `ISLP` package or the bundled CSV files;
the notebook ends with hands-on exercises" appears **nine times byte-identical**.
None of the 14 names a notebook section or cell — even though the anchors
exist (`## 4. Diagnostics`, `## 3. Pruning via cost-complexity`). The one
counter-example, `Lecture_Slides/chapter_00/chapter_00.tex:564` ("Rebuild this
plot yourself in `Lab_Notebooks/chapter_00_lab.ipynb` with
`df["wage"].describe()`"), shows what the other 13 could be.

**Two places model the practice the lectures warn against.** These are worth
naming precisely because everything around them is careful:

- `chapter_06_lab.ipynb` **cell 19**: `Xs = StandardScaler().fit_transform(X)`
  then `cross_val_score(pcr, Xs, y, cv=10)`. **Cell 22**:
  `XH = StandardScaler().fit_transform(X_raw)` then `LassoCV(cv=10).fit(XH, yH)`.
  The scaler sees every fold's held-out data. This is contradicted *inside the
  same notebook*: cells 11 and 15 do it correctly with
  `make_pipeline(StandardScaler(), RidgeCV(...))`, and cell 25 carries the
  comment `# fit scaler on TRAIN only` … `# apply to both -> no leakage`. Two
  cells out of eleven, and they are the two labelled "worked solution".
- `chapter_08_lab.ipynb` **cells 27–28** are headed "tune m = max_features" and
  "tune (learning rate, number of trees, depth)", and select among candidates
  by comparing **test MSE**. Cell 29 then reports importances from "the tuned
  (max_features=6) forest", and cell 30 concludes "tuned boosting … reaches
  ≈ 7.4" — a test score for a configuration chosen on that same test set.
  `GridSearchCV` is already imported and used correctly in cell 12 of the same
  notebook.

  (`chapter_02_lab.ipynb` cell 26 also does `best_K = argmin(te_err)`, but
  there the *purpose* is to draw ISLP Figure 2.17's U-curve, and cell 28
  redeems it with "Cross-validation would pick a K in the flat basin at the
  bottom". I would leave that one alone and add one sentence.)

**CI covers one thing: whether the Sphinx site compiles.** `.github/` contains
exactly one file, `workflows/docs.yml`. Nothing checks that the decks compile,
that the notebooks execute, that the exams build, or that `slide_index.md`
matches the PDFs. And there is a hole in the one check you have:
`docs/conf.py:69-73` prints a bare message when a deck PDF is missing rather
than emitting a Sphinx warning, and `docs/slides.md:30-41` links the PDFs with
raw `<a href=…>` HTML that Sphinx never validates — so `-W` cannot catch it. A
forgotten `make deck-07` ships a green build with a 404ing "Open" button.

For the record, `slide_index.md` **is** byte-identical to what `make_index.py`
regenerates from the committed PDFs, and every quantitative claim in the README
(1057 slides, 111 appendix, 86+41=127 exercises, 1168 pages) cross-checks
against the PDFs. The numbers in this repo are trustworthy.

**Tracked deck PDFs are affordable now and won't stay that way.** 168 tracked
PDFs, 27.7 MB in the working tree. In history, deck PDFs already account for
~175 MB of blob bytes across 42 commits (`chapter_04.pdf` alone: 25.3 MB in
9 versions) because PDFs do not delta-compress. GitHub repacks it down to a
96 MB clone today. At roughly one 12-deck rebuild commit per teaching week,
this grows by ~200 MB per semester and never shrinks. Not urgent; worth a
decision before it is.

**Accessibility: the figures are better than the type.** The two
`make_figures.py` scripts use a disciplined three-colour palette
(`ACCENT #26468C`, `ORANGE #C8641E`, `GREY #7A7A7A` at
`Lecture_Slides/chapter_00/make_figures.py:28-30`); grepping both files for
`jet`, `cmap`, `'red'`, `coolwarm`, `RdYlGn` returns **nothing**, and
multi-series plots pair colour with linestyle and a label. That is genuinely
well done. The problems are elsewhere:

- **Figure text renders at ~5 pt on the slide.** `rcParams` sets
  `font.size: 9` with overrides to `fontsize=8` and `tick_params(labelsize=7.5)`
  (`make_figures.py:33-43`, `:127`, `:329`). `ch00_anscombe.png` is 1399 px =
  9.33 in at 150 dpi, included at `width=0.99\textwidth` where `\textwidth` is
  5.99 in (from `chapter_00.log`) — a 0.64 downscale, so a 7.5 pt tick becomes
  ≈ 4.8 pt, roughly *half* the smallest slide text. The fix is to author
  `figsize` at final on-slide width instead of shrinking a wide figure.
- **`industry` boxes are colour-only.** All eight callout environments define a
  text title, but 344 of 928 call sites override it with a title that drops the
  type word — including **86 of 86** `industry` boxes, whose slate-grey tint is
  the only cue. `takeaway` (`green!4`) vs `solutionbox` (`teal!5`) are adjacent
  hues at 4–5 % tint with no icons and a 2.5 pt vs 3 pt border; 27 solution
  boxes drop the word "Solution". `Lecture_Slides/chapter_04/chapter_04.tex:1631`
  instructs colour-reading directly: "Green cells are correct decisions, red
  cells are the two error types."
- **`chapter_00` shrinks whole slides.** 93 font-shrink commands, 36 of them
  wrapping the *first line of a frame body*. Worst:
  `Lecture_Slides/chapter_00/chapter_00.tex:2269`, `\tiny` on a 20-row table
  (≈ 6 pt projected), and `:194`, a 237-word twelve-item self-check at
  whole-frame `\scriptsize` — which is the entry point for exactly the students
  least confident in the material. There are 46 double-shrinks where
  `\scriptsize` sits inside a box already set to `fontupper=\footnotesize`.
- **PDFs are searchable and bookmarked but not tagged.** pypdf confirms 12–26
  nested outline entries per deck and clean text extraction (`'confounding'`
  hits 6 pages of chapter_03.pdf). But no `/StructTreeRoot`, no `/MarkInfo`, no
  `/Lang` on any deck — no reading order, no alt text on 124 figures and 39
  TikZ diagrams. Separately, code copied out of a deck PDF **loses all
  indentation** and will not run (`chapter_06.pdf` p. 61 extracts
  `for k in range(1, 6):# model sizes` with a flush-left body).
- **No German-language support exists anywhere.** Grepping `Lecture_Slides/`
  for `glossar|german|deutsch|bilingual|translat` yields six hits, all false
  positives ("translation invariance", "Translating notation [Math]"). Not one
  German gloss for `confounding`, `shrinkage` or `overfitting`. The densest
  prose in the corpus is also the smallest type and the only prose with no
  list structure: `chapter_00b.tex:937` is 303 words with zero `\item`s,
  `chapter_00.tex:1992` is 302 words at `\scriptsize` inside a
  `\footnotesize` box.

**The documentation is a portfolio site with a student quickstart bolted on.**
Of ~7,000 words in `docs/`, student-primary is ~22 % (quickstart, labs,
datasets), lecturer/adopter ~57 %, project/recruiter ~21 %. `README.md:4` and
`docs/index.md:3` both open "A complete, **ready-to-teach** university course";
`README.md:380-399` and `docs/citation.md:51-70` carry the author CV twice.
`docs/slides.md` alone (1904 words) outweighs every student page combined.

All seven student needs are absent: no study/revision guide, no glossary, no
errata page or issue channel (`.github/` has no templates and there is no
`CONTRIBUTING.md`), no plain statement of the solutions-access policy, no
"what to do when your numbers don't match", no assessment/deadline/office-hour
information, and no prerequisites page. Three pages promise "request them from
the author" (`README.md:309`, `docs/exams.md:6`, `docs/teaching.md:25`) and
**no contact address exists anywhere**, including `CITATION.cff`.

The frustrating part is that the best student-facing writing in the repository
already exists — in lecturer files. `Teaching_Guide/semester_plan.md:79-84` is
headed "Workload for students" and says "a student who runs every notebook
will pass; one who only reads slides will not". `Teaching_Guide/README.md:64-70`
contains the single most useful diagnostic sentence anyone has written about
this course: "The commonest cause of a struggling student in this course is not
the machine learning — it is a rusty grasp of standard errors." Neither appears
in `docs/`.

And `docs/exams.md` is an 88-line page describing three artefacts a student
cannot reach: `:48-52` gives `cd Mock_Exams/Exam_1_after_Lecture_04`, a
directory that exists in no clone (`.gitignore:13`), and `:61-63` routes the
reader to "which exercises rehearse which exam problem" — a mapping that lives
only in the gitignored runsheets. The withholding is correct
(`Teaching_Guide/runsheets/lecture_13.md:38` really does say "This is Problem
6(a) of the final mock exam almost verbatim"); the gap is that nothing tells a
student what they *can* have. Which is, in fact, a lot: all 127 exercise
solutions are already public inside the committed deck PDFs, and no page says so.

Two live dead links: `Teaching_Guide/README.md:9` and `:12` link `./runsheets/`
and `./handouts/` with no "not published" marker (`docs/teaching.md:17-18` gets
this right), plus `before_class.md:12`. They look fine on your machine because
the directories are on disk.

---

## 2. Recommendations, in priority order

### R1. Make the Colab badge the documented day-one path; demote local install to week two. — 2 h

The review brief I was given said the repo has "no Binder/Colab entry point".
That is not true, and the gap between the reality and that impression is itself
the finding: **the Colab path exists, is wired up, and is nearly invisible.**
Cell 0 of every notebook carries a working badge; `docs/labs.md:22-41` has all
fifteen; `docs/quickstart.md:7` already calls Colab "recommended". I verified
the plumbing: the repo is public at `github.com/ChrisW09/Quantitative-Research-Methods`,
`ALL CSV FILES - 2nd Edition/` is tracked, and every fallback URL returns 200
(`.../ALL%20CSV%20FILES%20-%202nd%20Edition/Boston.csv` → 200, 34309 bytes;
all four `statlearning.com/s/*.csv` → 200).

So the highest-value change to reduce first-day failures is not technical. It
is to stop offering a 244 MB–2 GB install as a co-equal option in session one.
Concretely:

- Put the fifteen Colab badges in a single visible block at the top of
  `README.md` and at the top of `docs/quickstart.md`, above the venv
  instructions, not below them.
- Move the `python -m venv` block (`README.md:74-79`, `docs/quickstart.md:27-32`
  — byte-identical) under a heading that says it is optional and for later.
- Delete the stale line in markdown cell 3 of **13 of 15 notebooks**: "(once
  the repo is on GitHub and `GITHUB_RAW` is set)". It is already set; cell 0
  two cells earlier says so. A student reading cell 3 concludes Colab does not
  work yet.
- Fix "The three datasets NOT in the ISLP package" in the setup cell of **all
  15** notebooks — `KNOWN_URLS` has four entries, and `docs/quickstart.md:13-15`
  correctly says four.

*What it displaces:* nothing. It is editing text you have already written.

*Cost of a Binder path:* I would not add one. Binder cold-starts take 2–5
minutes on a good day and time out on a bad one; a `torch`-bearing environment
makes the image build slow and fragile; and the Colab path already works for
free. If you want a second option, `uv run --with-requirements` is a stronger
bet than Binder.

*Unverified:* I did not launch an actual Colab runtime. I verified every URL
and dependency the bootstrap relies on, but not Google's runtime.

### R2. Scale before you polynomialise, and pin the two genuinely brittle packages. — 3 h

This is the "how should the course handle version drift" answer, and my
recommendation is **none of the three options as stated**. Hard-pinning is
unjustified: I measured ~86 % of outputs stable across a three-year jump
including a pandas major release. Publishing tolerances is busywork for 200
cells. Teaching "this is normal" is a cop-out when the drift is caused by
fragile code.

Instead: **remove the fragility, then pin only what is actually brittle.**

1. Insert `StandardScaler()` ahead of `PolynomialFeatures` in
   `chapter_05_lab.ipynb` cells 8, 10, 12 and `chapter_07_lab.ipynb` cell 25.
   I verified this makes the numbers bit-identical across sklearn 1.6.1 and
   1.9.0. It also models the lesson. Then re-run and re-store outputs.
2. Pin `pygam==0.10.1` in `requirements.txt:16` (was `pygam>=0.9`). The 0.12
   change to the scale-parameter estimate moves AIC by 40 %, and pyGAM is a
   one-maintainer package used in one lab — an upper bound is cheap insurance.
   Pin `ISLP` too: `>=0.3` at `requirements.txt:13` resolves to 0.4.1 today and
   will resolve to something else next year.
3. Re-run `chapter_08_lab.ipynb` and edit the interpretive prose in cell 30 so
   it does not assert "three- to four-fold" about a number that has moved to
   two-fold. Better still, change cell 26's tree to
   `DecisionTreeRegressor(max_depth=8, random_state=1)` so the comparison is
   against a *defensible* tree rather than an unpruned one whose test error is
   an artefact of splitter tie-breaking.
4. Record the reference environment. A `constraints.txt` produced by
   `pip freeze` from the machine that generated the shipped outputs, referenced
   from `docs/environment.md`, lets a student who cares reproduce your exact
   figures without forcing that on everyone. Right now there is **no record
   anywhere** of which versions produced the stored outputs.
5. Add three sentences to `docs/environment.md`: last-digit differences are
   normal and not your fault; if a *ranking* or a *conclusion* differs, that
   is a bug, please report it (see R6 on where); the reference stack is in
   `constraints.txt`.

*What it displaces:* nothing structural. Items 1–3 are notebook edits plus one
re-run each.

### R3. Take `torch` off the default install path and make the data path single-valued. — 4 h

Two problems, one file, one fix each.

**Split `requirements.txt`.** Today it is 114 core packages plus a
deep-learning stack that ships whether the student wants it or not, because
`ISLP` hard-requires `torch`, `pytorch-lightning` and `torchmetrics`.
Measured: 151 packages / 244 MB with, 114 / 126 MB without; `torch` alone is
241 MB on Windows and 888 MB plus twelve CUDA packages on Linux x86_64. Since
13 of 15 notebooks run clean with **no ISLP at all** (I verified this), make
core the default:

- `requirements.txt` → the seven core packages plus `jupyterlab`.
- `requirements-full.txt` → `-r requirements.txt` plus `ISLP`, `xgboost`,
  and pinned `pygam`, for whoever wants Chapters 7, 10, 11.
- Correct `docs/environment.md:44-49`. The "Minimal install" tip currently
  names `ISLP`, which makes it the maximal install. Also add `seaborn` to
  `README.md:337`, which omits it while `requirements.txt:5` requires it for
  the Chapter 2 pairplot.

**Then close the ISLP/CSV divergence.** The dual data path is the real source
of "my numbers don't match", and it is fixable inside `load()`:

- Normalise in the helper: drop `Unnamed: 0`, coerce `Auto.horsepower` to
  float, and decide once whether `Auto.name` is present. That kills the
  ch02/ch04/ch05 diffs at the source, in one function, replicated to 15 cells.
- Add `USArrests.csv` and an `NCI60` extract to
  `ALL CSV FILES - 2nd Edition/`. That removes the only network dependency in
  a local checkout (Chapter 12), un-breaks the `chapter_01` and `chapter_12`
  PCA figures for anyone without ISLP, and makes `docs/labs.md:60-61` true.
- Delete the `if HAVE_ISLP:` branch in `chapter_03_lab.ipynb` cell 18 — pick
  one basis. Two different coefficient tables under one heading is the single
  most confusing thing a student can meet in these notebooks. **(This notebook
  was mid-edit; check the current state first.)**

*What it displaces:* if you split the requirements files, `docs/environment.md`
and the Colab `_ensure` list need a pass for consistency. Budget an extra hour.

### R4. Add notebook execution to CI. It costs 60 seconds. — 3 h to build, ~1 h/semester to maintain

Every one of the three drift bugs in R2 was silent — no exception, no warning,
just different numbers. The only thing that catches that class of bug is
running the notebooks, and I have measured that this is cheap: **58 seconds for
all fifteen** on a 2026 stack, 50 s for thirteen without ISLP.

Minimal plan, in priority order:

1. **`nbclient` executes all fifteen notebooks on push and weekly on a cron.**
   Fail on any error output. With R3's split, install is `requirements.txt` only
   (~126 MB, ~40 s) for thirteen notebooks; run ch 10/11 in a second job with
   the full file, or skip them. The weekly cron is what actually earns its
   keep — it tells you a dependency broke *before* a student does.
2. **Compare numeric outputs against the committed ones, with normalisation.**
   Strip `statsmodels` `Date:`/`Time:` lines and `lifelines` `time fit was run`
   (I confirmed these are the *only* systematic cosmetic diffs), then compare
   text outputs and fail on a change beyond a relative tolerance. This is the
   check that would have flagged ch05 the day it broke. ~1 h on top of step 1.
3. **`make -B decks` on a LaTeX container, plus `make check`.** Compile-only;
   do **not** commit the PDFs from CI. You track built PDFs deliberately and
   that is defensible, but a CI job that commits them would add ~19 MB to
   history per run. Compile, run `check_decks.py`, upload the log as an
   artifact, and let the professor commit. Note `make check` reads gitignored
   `.log` files, so it is meaningless on a fresh clone unless the same job
   compiled first — and five decks are within 2 pt of the 12 pt overfull
   tolerance (chapter_04 at 11.0 pt), so this check is close to firing.
4. **Make a missing deck PDF fail the docs build.** Change
   `docs/conf.py:69-73` from `print()` to a Sphinx warning so `-W` catches it,
   and convert the raw `<a href=…>` links at `docs/slides.md:30-41` to
   `:download:` roles so Sphinx validates them. ~30 min, closes a hole in the
   one check you already have.
5. **A `check_runsheets` target.** Not CI, but the highest-value automation gap
   found: **≥14 stale page references across four runsheets, every one off by
   exactly +2** (e.g. `lecture_03.md:38` says Exercise 3.1 is on p. 28; it is
   on p. 30 — p. 28 is "The same bowl, seen from above"). And
   `lecture_03.md:105` claims these "are refreshed by `make index`", which is
   false — `make index` regenerates only `slide_index.md`. A ~30-line script
   diffing runsheet pages against `slide_index.md` fixes a real recurring
   annoyance. This is lecturer-facing (runsheets are gitignored), so it is
   about your Tuesday morning, not the students'.

I would **not** add a link checker. 15 Colab URLs return 405 to HEAD and 200 to
GET, so a naive checker produces 15 false failures forever. I verified all 31
external URLs by hand: all reachable.

*Honest maintenance cost:* item 1 is near-zero once written — it either passes
or tells you something true. Item 2 will produce occasional false alarms from
float noise; budget an hour a semester to widen a tolerance. Item 3 needs a
TeX Live container, which is a 2 GB image and the one genuinely annoying piece;
if you only do one thing, do item 1.

### R5. Fix the two leakage instances and stop calling test-set search "tuning". — 2 h

Small, cheap, and disproportionately important because the course's own
argument depends on it. A student who reads `chapter_06_lab.ipynb` cell 25's
`# fit scaler on TRAIN only -> no leakage` and then looks up at cell 22 will
either not notice (bad) or notice (worse).

- `chapter_06_lab.ipynb` cells 19 and 22: wrap the scaler in the pipeline, as
  cells 11 and 15 already do. `make_pipeline(StandardScaler(), LassoCV(cv=10, …))`.
- `chapter_08_lab.ipynb` cells 27–28: replace the test-MSE loops with
  `GridSearchCV` on the training set (already imported at cell 12), then report
  **one** test MSE for the selected configuration. Amend cell 30 accordingly.
  If you would rather keep the loops as an illustration, relabel them "test
  error as a function of m" and add one line: *this is not how you would choose
  m; see Chapter 5.*
- `chapter_02_lab.ipynb` cell 26: leave the code, add one sentence noting that
  `argmin` over test error is a picture, not a procedure. Cell 28 half-says
  this already.

### R6. Give students a page of their own. — 4 h

One new file, `docs/for-students.md`, linked first from `README.md:39-46` and
from `docs/index.md`. Most of the content already exists — it is filed where no
student will look:

- Prerequisites and the skip rule, lifted from `Teaching_Guide/README.md:64-70`
  (the twelve-question self-check on slide 7 of chapter_00; nine or more and
  you can skip the precourse; rusty standard errors are what sinks people).
- Workload expectations, lifted verbatim from
  `Teaching_Guide/semester_plan.md:79-84`.
- **The solutions policy, stated plainly for the first time:** every one of the
  127 exercise solutions is in the deck PDFs you already have; the mock exams
  are not distributed. Right now this fact is scattered across
  `README.md:19`, `docs/index.md:121`, `docs/index.md:143`, `docs/slides.md:66`,
  `docs/slides.md:90`, `docs/teaching.md:75` and `docs/teaching.md:90`, and
  stated plainly nowhere.
- "When your numbers don't match" — the three sentences from R2, plus the
  existing `Auto`/`na_values="?"` note at `docs/datasets.md:87-93`, which is
  currently the *only* reproducibility guidance in the docs despite
  `docs/index.md:134` promising "Reproducible by design."
- **A contact address.** Three pages say "request them from the author" and
  none says how.

While you are there: fix `docs/exams.md:48-52`, whose copy-pasteable
`cd Mock_Exams/…` cannot run in any clone, and `:61-63`, which routes students
to a withheld mapping. And add "not published" markers to
`Teaching_Guide/README.md:9`, `:12` and `before_class.md:12`, as
`docs/teaching.md:17-18` already does.

*What it displaces:* nothing, but it will make the imbalance visible —
`docs/slides.md` at 1904 words is longer than everything student-facing
combined, and once there is a student page you may want to trim the catalogue
pages. That is a bigger job; do not start it now.

### R7. Separate solutions from labs, and put scaffolding in. — 12–15 h

I have put this last not because it matters least — pedagogically it is the
largest gap — but because it is the only recommendation that costs real time
and touches all fifteen files. Do it over a summer, not before a semester.

- Split each notebook: `chapter_NN_lab.ipynb` (demo + prompts, **outputs
  cleared** for the exercise sections) and `chapter_NN_solutions.ipynb`. Keep
  the demo outputs — students need something to compare against — but a student
  should be able to attempt Exercise 6.7 without the answer in view.
- Add two or three scaffolded cells per lab. You already have the raw material:
  the `*Common mistake:*` closers in `chapter_05_lab.ipynb` cell 21,
  `chapter_07_lab.ipynb` cells 22 and 27 are diagnoses of errors students
  actually make. Turn each into a *predict-then-run* pair: a cell that makes
  the mistake, a markdown cell asking what will go wrong, then the fix. The
  buggy/honest pair in `chapter_00b_lab.ipynb`'s Exercise 0b.6 is the template
  — it just needs the two cells separated so the student sits with the bug.
  `chapter_08_lab.ipynb` cells 27–28 (R5) are a ready-made "why is this number
  a lie?" exercise.
- Give the three self-study chapters (9, 11, 12) worked solutions. They have
  6–7 code cells each and no solutions at all, and they are precisely the
  chapters worked without a lecturer in the room.

*What it displaces:* this is a fortnight of a summer. It also makes the docs
build heavier (two notebooks per chapter to render) and doubles what CI
executes — still under two minutes, so not a real constraint.

---

## 3. Additions worth considering

**A1. A German-column on the vocabulary slide. — 3 h, 12 files**
There is no German-language support anywhere in the decks. But the hook already
exists: each deck's summary block has a `{Vocabulary check}` slide with a
`Term | One-line meaning` table (`chapter_00.tex:2236`, and the parallel slide
in all twelve). Adding a third column of German equivalents for the 15–20 terms
per chapter is a contained, high-leverage change for an English-medium course at
a German UAS. Caveat: that table is currently at whole-frame `\scriptsize` with
`\arraystretch{0.95}`, so it needs the type fixed first (A2). *Speculative:* I
am inferring the language load from the material, not from student feedback.

**A2. Author figures at final on-slide size; retire whole-frame `\scriptsize`. — 6 h**
Two separate fixes. In `make_figures.py`, set `figsize` to the deck's 5.99 in
`\textwidth` rather than authoring at 9.3 in and downscaling 0.64 — that alone
takes tick labels from ≈ 4.8 pt to ≈ 7.5 pt with no other change. In the decks,
the 36 whole-frame shrinks in `chapter_00` and the 46 double-shrinks are mostly
a symptom of over-full slides; splitting `chapter_00.tex:2269` (a 20-row table
at `\tiny`) and `:194` (237 words, 12 items) across two frames each fixes the
two worst. Note the good news: `handout_template.tex:11` uses `nup=1x2` at
`scale=0.92`, so handouts render each slide 1.07× *larger* than on screen — the
print path does not compound the problem.

**A3. Give the `industry` box a printed label, and stop instructing colour-reading. — 2 h**
Change the `industry` definition so the title always prefixes "In industry: "
even when overridden — 86 boxes currently identify themselves by grey tint
alone. Restore the word "Solution" on the 27 `solutionbox` calls that drop it
(`chapter_10.tex:530`, `:556`, `:585`, `:1303`, `:1326` are the ones most likely
to mislead, titled `[Forward pass]`, `[Code: load / standardise …]`). And
rewrite `chapter_04.tex:1631` and the parallel line at `chapter_13.tex:1156-1157`
so they name the cells rather than the colours. `Lecture_Slides/chapter_05`'s
k-fold diagrams (`:446-463`, `:570-572`) are your own best-practice example:
blue/orange plus printed "Train"/"Test" in every cell.

**A4. Make the fourteen `labnote` boxes name a notebook section. — 2 h**
Nine are byte-identical boilerplate. The notebooks already have numbered
headings; citing them (`→ chapter_08_lab.ipynb §3 "Pruning via cost-complexity"`)
turns a decorative box into a usable instruction. Note `chapter_08.tex:973`
promises pruning and the deck's Python Lab section has no pruning listing —
it exists only in the notebook, which is exactly what a pointer is for. Also
worth catching in the same pass: `chapter_06.tex:1264` calls it "Extended
Exercise 6.3" where the notebook heading is "Extended Exercise 6.2", and
`chapter_06.tex:1218`/`:1272` load data via
`pd.read_csv("../../ALL CSV FILES - 2nd Edition/Hitters.csv")` — a relative
path valid only from a deck directory, printed on a slide for students to copy.

**A5. Tagged PDFs, and an errata channel. — 4 h + ongoing**
No deck has `/StructTreeRoot`, `/MarkInfo` or `/Lang`; adding
`\DocumentMetadata{lang=en-GB, pdfstandard=ua-2}` needs TeX Live ≥ 2024 and one
edit per deck (there is no shared preamble — all twelve duplicate the same
~70 lines, so every preamble change is a 12-file change; extracting a `.sty`
first would be ~2 h well spent). Separately: a `.github/ISSUE_TEMPLATE/` and an
`docs/errata.md` give students somewhere to report the next ch05-style bug. You
currently have no channel and no address.

**A6. Decide about PDF history before it decides for you. — 1 h**
Not urgent — 96 MB clone, 5.7 s. But ~175 MB of the history is already deck-PDF
blobs and it grows ~200 MB a semester. The cheapest option is to keep tracking
them and add `--depth 1` to the documented clone command (35 MB instead of
96 MB, and the gap widens every semester). Note `docs/conf.py:62-65` already
publishes all twelve decks to the Pages site, so students do not need the
tracked copies at all — they are for your convenience, which is a legitimate
reason to keep them, just worth knowing.

**A7. `warnings.filterwarnings('ignore')` in the setup cell of all 15 notebooks. — 30 min**
I checked what this actually hides before recommending anything, and the honest
answer is: almost nothing. Stripping it and re-running chapters 3, 5, 6, 7, 8
and 10 surfaced **three** warnings in total, all in chapter 7. But one of them
is worth seeing: pyGAM's `UserWarning: KNOWN BUG: p-values computed in this
summary are likely much smaller than they should be. Please do not make
inferences based on these values!` — and `chapter_07_lab.ipynb`'s own prose
tells the student "pyGAM prints a caveat that its summary p-values are
approximate", referring to a message the setup cell prevents them from ever
seeing. Narrow the filter to the specific categories you want gone rather than
blanketing, or at least let chapter 7 through. Low priority; listed because it
is thirty minutes.

---

## 4. What I examined and judged sound

Stated plainly so you know where not to spend time.

- **The `load()` helper** (cell 4 of all fifteen notebooks). The ISLP →
  R-datasets → local CSV → official URL → GitHub-raw cascade is the right
  design and it works. I verified every URL in it returns 200. R3 asks you to
  *normalise* what it returns, not to redesign it.
- **Notebook hygiene.** All fifteen have strictly sequential execution counts
  1..N, stored outputs on every code cell, and zero error or stderr outputs.
  Someone re-runs these cleanly before committing. That discipline is why R4 is
  cheap to add.
- **Cross-version robustness, ~86 % of it.** 173 of 202 code cells produce
  byte-identical text output across a jump from numpy 2.0/pandas 2.3/sklearn 1.6
  to numpy 2.5/pandas 3.0/sklearn 1.9. That is unusual and it is why I did not
  recommend hard-pinning.
- **The interpretation prose.** `chapter_06_lab.ipynb` cell 26,
  `chapter_02_lab.ipynb` cell 28, `chapter_05_lab.ipynb` cell 24,
  `chapter_07_lab.ipynb` cell 27 — these explain *what the numbers mean and
  where they stop being trustworthy*, which is the hard part and the part most
  courses skip. Do not touch them except where R2 makes a number stale.
- **Deck/notebook division of labour.** Measured: decks carry 20–35 % of the
  notebook's code, notebooks carry 2–4× more plus 12–28 markdown cells with no
  deck counterpart. That is the right ratio. The pointers need work (A4); the
  split does not.
- **`slide_index.md` and the repo's arithmetic.** Byte-identical to what
  `make_index.py` regenerates from the committed PDFs. 1057 + 111 slides,
  86 + 41 = 127 exercises with zero missing solution pages, 1168 total pages,
  290 min for chapter 3 — every figure quoted in the README and docs
  cross-checks. Do not spend time auditing the numbers; they are right.
- **The `Makefile`'s design.** The figure-stamp mechanism and its comment at
  lines 54–61 (including the honest admission that make cannot handle the
  spaces in the data directory name) is careful work. The directory name is
  worth renaming eventually, but the Makefile already routes around it and
  every notebook quotes the path correctly. *Mid-edit by another agent; I only
  read it.*
- **`Teaching_Guide/` as lecturer material.** `before_class.md`
  ("Nothing here is clever; all of it has gone wrong for somebody"),
  `semester_plan.md` with its three split points and ranked cut list, and the
  runsheets' "What they will get wrong" sections are the best-written material
  in the repository. My only complaint (R6) is that some of it is written for
  students and filed where students cannot find it.
- **The figure palette.** No colormaps, no `jet`, no red/green pairs, colour
  paired with linestyle and label. Only the *sizes* need work.
- **PDF searchability and navigation.** 12–26 nested bookmark entries per deck,
  clean text extraction, `/Title` set correctly. Tagging is missing (A5) but the
  basics are right.
- **The decision to gitignore `Mock_Exams/` and `Teaching_Guide/runsheets/`.**
  Correct, and the `.gitignore:14-16` rationale is accurate — the runsheets
  really do map exercises onto exam problems verbatim. The fix is not to
  publish them; it is to tell students what they can have (R6).

---

## Method, and where I am guessing

**Commands I ran** (all read-only against the repo; work confined to a scratch
directory): `pip install --dry-run --report` against `requirements.txt` on
Python 3.9 and a `uv`-built 3.12, plus HEAD requests on every resolved wheel URL
to get download sizes; `nbclient` execution of all fifteen notebooks in both
environments with `allow_errors=True`; a normalised text-output differ against
the committed notebooks; a standalone probe comparing scaled vs unscaled
`PolynomialFeatures` CV MSE across both stacks; `curl` HEAD/GET on the fallback
data URLs; `git rev-list`/`cat-file --batch-check` for history blob accounting;
`git clone` full and `--depth 1` for clone cost; a re-run with
`filterwarnings` stripped to count what is suppressed; `pypdf` for deck
outlines, text extraction and tagging metadata; and
`python3 Teaching_Guide/check_decks.py`, which I confirmed writes nothing.

**Where I am speculating rather than observing.** Everything about how a
student *feels* is inference from the artefacts: that vague `labnote` pointers
go unused, that inline answers get read instead of attempted, that the language
load is heavy, that a 4.8 pt tick label is unreadable from row twelve. I have
measured the artefacts precisely and inferred the experience. The two claims I
would most want checked against actual students are (i) whether anyone uses the
Colab badges at all, and (ii) whether the terminal `## Exercises` lists in each
notebook are ever attempted, given that the worked solutions sit two cells
above them. Both are answerable with one question in week three.

**What I did not verify:** an actual Google Colab runtime; sklearn versions
between 1.6.1 and 1.9.0 (so I cannot say exactly when chapter 5 broke);
Windows and Linux installs (sizes are from PyPI metadata, not from running
them); and anything in `Mock_Exams/`.

# For students

One page for everyone taking the course: what you are assumed to know, how much
work it is, how the labs fit around the lectures, what to do when your output
does not match the slides, and how to revise.

:::{container} qrm-chips
**12** sessions × **180 min** · **2** optional precourse sessions ·
**12** labs *(with solutions)* · **5** short practice exams ·
**Colab** on day one
:::

## What the course assumes

The course teaches *statistical learning*, not statistics from scratch. From
Lecture 1 onwards the decks assume undergraduate statistics silently: variable
types, means and spreads, correlation, probability and Bayes, the standard
distributions, standard errors, confidence intervals, hypothesis tests, and
simple linear regression. On the Python side it assumes you can open a notebook,
run cells in order, and read `pandas` and `numpy` code — not that you can write
a program from a blank file.

```{admonition} The one thing that catches people out
:class: warning

It is almost never the machine learning. It is a rusty grasp of **standard
errors** — what they are, why they shrink with *n*, and how they differ from a
standard deviation. If that sentence felt uncomfortable, start with the
precourse.
```

## The two precourse decks, and the skip rule

Two optional sessions sit before Lecture 1. They exist because the ten chapter
decks use all of this and explain none of it.

**Precourse (a) — statistics refresher** (`chapter_00`, 106 slides plus a
16-slide appendix). Descriptive statistics, probability and Bayes,
distributions, sampling and confidence intervals, hypothesis testing and power,
simple regression, and the `numpy`/`pandas` toolkit; matrix algebra and
calculus/gradient descent sit in its appendix.

**Precourse (b) — the toolkit** (`chapter_00b`, 51 slides plus a 9-slide
appendix). Reading mathematical notation (Σ, Π, arg max, indicators, sets), logs
and exponentials, odds and the logit, likelihood and maximum likelihood,
counting and computational cost, and the Python patterns every lab relies on.
The topics were chosen by counting how often the later decks use them — slide 4
of that deck shows the count next to each one.

```{admonition} How to tell whether you can skip Precourse (a)
:class: tip

**Page 7 of `chapter_00.pdf` is a twelve-question self-check** — one question per
section, so a wrong answer tells you which section to read. The deck's own
scoring rule:

- **comfortable with 9 or more** — skim the deck and move on;
- **fewer than 6** — work through it *with* the exercises; it pays for itself by
  Lecture 3.

Between 6 and 8, read the sections your wrong answers point at.
```

Precourse (b) has no equivalent self-check. The honest test is page 5, the
notation table: if every symbol on it is one you could read aloud without
hesitating, you can skim the deck.

Either way, the material is **assumed from Lecture 1 onwards**, whether or not
the sessions are taught.

```{admonition} TODO for the professor
:class: caution

Whether the two precourse sessions are **taught** this semester or **set as
self-study** is a per-cohort decision and is not recorded anywhere in the
repository. Please state the intention for this cohort here.
```

## Running the labs

**Day one: use [Google Colab](quickstart.md).** Every notebook has a Colab badge
in its first cell, and one-click links for all fifteen are on the
[Lab notebooks](labs.md) page. There is nothing to install: the first cell
detects Colab, adds the few packages that are missing, and loads the data for
you. A Google account is all you need. Colab runs every lab in the course,
including the Chapter 10 deep learning lab.

**From about week two, a local install is worth it** — faster, works offline,
and it keeps your own edits. Do it in your own time, not in a session: it pulls
in around 150 packages and several hundred megabytes, because the book companion
package `ISLP` hard-requires `torch`. The four commands are in
[Quick start](quickstart.md), and [Python environment](environment.md) explains
what is pinned and why the download is so large.

## How the labs relate to the lectures

Each of the twelve taught chapters has **one deck and one notebook**, and they
are written as a pair:

- the deck moves motivation → intuition → definition → worked example, and drops
  a cyan **"switch to the notebook now"** box at each point where the lab picks
  the thread up;
- the notebook reproduces that chapter's analysis in Python, then closes with
  **worked Python solutions** to the chapter's exercises;
- every exercise *inside* a deck is followed immediately by its own full
  solution slide, so you are never stuck on a prompt with nowhere to go.

Three ISLP chapters — **9 (Support Vector Machines)**, **11 (Survival
Analysis)** and **12 (Unsupervised Learning)** — are outside the twelve-lecture
plan. They have **no deck**, and their notebooks are **code references without
worked solutions**: read the ISLP chapter first, then use the notebook to see
how the methods are run in Python. Do not treat them as labs equivalent to the
twelve.

```{admonition} The labs are the part that matters
:class: important

A student who runs every notebook will pass. One who only reads slides will not.
```

## Workload

Per week, beyond the 180-minute session itself:

| What | How long |
|---|:--:|
| The chapter's lab notebook | 60–90 min |
| The deck's short exercises you did not do in the room | ~30 min |
| Reading the ISLP chapter | varies |

Each deck also carries far more exercises than a session can run — roughly one
short exercise every 20 minutes of teaching and one extended exercise every
45 minutes — so there will always be some left over. Every one of them has a
worked solution behind it.

```{admonition} TODO for the professor
:class: caution

The official workload figure — ECTS credits and the expected total hours for the
module — is not recorded anywhere in the repository, and neither is **how the
module is actually assessed** (the paper that counts towards your grade, as
distinct from the practice papers described below). Please add both.
```

## Solutions: what you get, and when

| Material | Solutions |
|---|---|
| Exercises inside a deck | **Yes, immediately** — the next slide is always the worked solution, including in the appendices |
| The twelve taught lab notebooks | **Yes** — each ends in a *Lecture exercises — worked Python solutions* section |
| The three code-reference notebooks (Ch 9, 11, 12) | **No** — the closing exercises are deliberately left unanswered |
| Mock exams and short exams | Worked solutions exist for every paper, but the papers are **not** published — see below |

The exam papers, their solutions and their LaTeX sources are assessment material
and are kept out of the public repository, so they are not downloadable from
this site. They come from your lecturer.

```{admonition} TODO for the professor
:class: caution

**The distribution policy for the exam solutions is not written down anywhere.**
Please state plainly: do students receive the solutions PDF, and if so, when —
with the paper, after attempting it, or only in the in-class review session?
Students will ask, and at present nothing in the repository answers them.
```

## When your numbers do not match the shipped output

**This is normal, and it is usually not your mistake.** The notebooks ship with
stored outputs, and the slides quote numbers computed when the deck was built.
Small differences are expected because:

- **package versions differ.** Most of `requirements.txt` gives *minimum*
  versions rather than exact ones, so two students installing on different days
  can end up with different `scikit-learn`, `statsmodels` or `numpy` releases —
  and defaults and tie-breaking rules do change between releases;
- **Colab and a local install are not the same environment.** Colab ships its
  own versions, and its `torch` is a different build from the one you would
  install locally;
- **floating-point arithmetic is platform-dependent** in the last few digits,
  and iterative fits (splines, boosting, gradient descent, anything with a
  convergence tolerance) amplify that into the third or fourth decimal;
- **not every source of randomness can be seeded away.** The notebooks are
  careful about this — splits use an explicit `random_state`, bootstrap draws use
  a seeded generator, and the Chapter 10 network calls `torch.manual_seed` — but
  a seeded draw is only reproducible against *the same library version*.

So the question is never "do the digits match?" but **"does the conclusion
change?"**

- A test MSE of 0.0187 where the slide says 0.0189, a *t*-statistic of 4.31
  against 4.29, a coefficient differing in the fourth decimal: ignore it.
- A **sign** flipping, a coefficient losing significance, a different model
  winning the cross-validation comparison, or a difference in the *first*
  significant figure: that is a real difference. Check three things, in order —
  did you run the cells in order from a fresh kernel; is the split the one the
  notebook set; and is the data the same (`df.shape` first).
- If it still differs, bring it to the session. A genuine version-driven
  difference is worth ten minutes of everyone's time.

```{tip}
If you want to settle it yourself, the repository root carries a
`constraints.txt` recording the exact build that reproduces the outputs stored in
the notebooks. Install with `pip install -r requirements.txt -c constraints.txt`
and re-run the cell: if it matches then, the difference was your stack moving,
not your code.
```

## How to revise

1. **Start at the end of the deck, not the beginning.** Every deck closes with a
   summary block: *Chapter N in one slide*, *Key formulas at a glance*, a
   vocabulary checklist, *Decision rules of thumb* and *Common pitfalls*, and
   most decks add self-check questions and a "things to remember" slide. It is
   written to be read alone. If you can answer the self-check, you know the
   chapter; if you cannot, it tells you which section to reopen.
2. **Re-run the lab from a clean kernel** — top to bottom, without looking at
   the stored output. This is the single highest-value revision activity in the
   course, and it is also how the exams test Python: by showing you real output
   and asking what it means.
3. **Do the exercises you skipped**, including the ones in the appendix. All of
   them have full worked solutions, so you can mark yourself.
4. **Then sit a short exam under time**, closed-book, before you look at its
   solutions.
5. If you need to find one specific topic fast, use the generated **slide
   index** (`Teaching_Guide/slide_index.md`, linked from
   [Teaching it](teaching.md)): it lists every section with its page range and
   every exercise with the page of its prompt *and* the page of its solution.

## Where the short exams fit

Five 60-minute practice papers (A–E) run alongside the three full-length mock
exams. Each is three problems × 20 points, increasing in difficulty, and each is
released once the material it needs has been taught:

| Short exam | Available after | The hardest problem is on |
|:--:|:--:|---|
| A | Lecture 6 | Logistic regression and the confusion matrix (Ch 4) |
| B | Lecture 7 | Cross-validation and the bootstrap (Ch 5) |
| C | Lecture 8 | Ridge and the lasso (Ch 6) |
| D | Lecture 10 | Trees: Gini, splitting, pruning, forests (Ch 8) |
| E | Lecture 12 | Multiple testing: Bonferroni, Holm, BH (Ch 13) |

The first two problems of each paper reach back to earlier chapters, so a short
exam is a cumulative check on everything up to that point rather than a test of
one chapter. A, C and E each open on precourse material — these five papers are
the only ones that revisit it.

**If you have fallen behind, these are the papers to use.** One of them takes an
hour, tells you exactly where you stand, and comes with a full worked solution
and a review deck. Full details are on the [Mock exams](exams.md) page; the
papers themselves come from your lecturer.

```{admonition} TODO for the professor
:class: caution

Three places in these docs promise that materials can be **requested from the
author** ([Mock exams](exams.md), [Teaching it](teaching.md), and the repository
`README.md`), but there is **no contact address anywhere in the repository** —
not in the README, not in `CITATION.cff`. Please add one, or change the wording
to name the channel students and instructors should actually use.
```

## Where to go next

- [Quick start](quickstart.md) — Colab in one click, and the local install for later.
- [The course at a glance](course.md) — the twelve-lecture plan and the assessment calendar.
- [Lecture slides](slides.md) — every deck, what it covers, and what is in its appendix.
- [Lab notebooks](labs.md) — all fifteen notebooks, rendered in full.
- [Mock exams](exams.md) — the eight practice papers and what each covers.

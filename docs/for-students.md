---
myst:
  html_meta:
    description: "What the course assumes, how much work it is, how the labs fit around the lectures, and how to revise — the one page every student should read in week one."
---

# For students

{.qrm-lead}
One page for everyone taking the course: what you are assumed to know, how much
work it is, how the labs fit around the lectures, what to do when your output
does not match the slides, and how to revise.

:::{container} qrm-chips
[**16** sessions × **180 min**]{.qrm-chip}
[**6** ECTS]{.qrm-chip}
[graded by **one 120-min exam**]{.qrm-chip}
[**15** labs *(with solutions)*]{.qrm-chip}
[**Colab** on day one]{.qrm-chip}
:::

## What the course assumes

The course teaches *statistical learning*, not statistics from scratch. From
Chapter 1 onwards the decks assume undergraduate statistics silently: variable
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

## The precourse session, and the skip rule

**The precourse is taught.** It opens the semester as a single 180-minute
session drawing on both precourse decks, because the thirteen chapter decks use
all of this material and explain none of it.

One session cannot cover both decks — together they run to 157 slides — so the
session is a **guided selection**, and the two decks stay available in full as
your reference. The skip rule below is what tells you which parts you still
need to read on your own.

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

```{admonition} How to tell which parts of Precourse (a) you still need
:class: tip

**Page 7 of `chapter_00.pdf` is a twelve-question self-check** — one question per
section, so a wrong answer tells you which section to read. The deck's own
scoring rule:

- **comfortable with 9 or more** — skim the deck and move on;
- **fewer than 6** — work through it *with* the exercises; it pays for itself by
  Chapter 3.

Between 6 and 8, read the sections your wrong answers point at.
```

Precourse (b) has no equivalent self-check. The honest test is page 5, the
notation table: if every symbol on it is one you could read aloud without
hesitating, you can skim the deck.

Either way, the material is **assumed from Chapter 1 onwards** — the taught
session gets you started on it, and the decks are there to finish the job.

## Running the labs

**Day one: use [Google Colab](quickstart.md).** Every notebook has a Colab badge
in its first cell, and one-click links for all twelve are on the
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

Every chapter has **one deck and one notebook** — twelve of each, the two
precourse sessions included — and they are written as a pair:

- the deck moves motivation → intuition → definition → worked example, and drops
  a cyan **"switch to the notebook now"** box at each point where the lab picks
  the thread up;
- the notebook reproduces that chapter's analysis in Python, then closes with
  **worked Python solutions** to the chapter's exercises;
- every exercise *inside* a deck is followed immediately by its own full
  solution slide, so you are never stuck on a prompt with nowhere to go.

That holds for **every taught chapter**, and for the three chapters that now sit
outside the sequence as [advanced modules](advanced.md) — support vector
machines (Ch 9), survival analysis (Ch 11) and multiple testing (Ch 13). Each
has its own deck, and each lab closes with worked solutions. There is no chapter
in the course you are expected to teach yourself from the book alone.

```{admonition} The labs are the part that matters
:class: important

A student who runs every notebook will pass. One who only reads slides will not.
```

## Credits, assessment and workload

The module is worth **6 ECTS**, and your grade comes from **one written exam at
the end of the semester: 120 minutes, 100% of the mark**. Everything else on
this page — the mock exams, the five short exams, the deck exercises — is
practice. None of it counts.

```{admonition} What the exam looks like
:class: important

The [Final Mock Exam](exams.md) is built as the rehearsal for the real paper:
same 120 minutes, same structure, weighted towards Chapters 7, 8, 10 and 13.
Sitting it under time, closed-book, is the single best predictor of how the real
one will go.
```

Per week, beyond the 180-minute session itself:

| What | How long |
|---|:--:|
| The chapter's lab notebook | 60–90 min |
| The deck's short exercises you did not do in the room | ~30 min |
| Reading the ISLP chapter | varies |

That comes to roughly 6–8 hours a week including the session — in the range the
6 ECTS implies (on the standard conversion of 25–30 hours per credit, about
150–180 hours across the semester).

Each deck also carries far more exercises than a session can run — roughly one
short exercise every 20 minutes of teaching and one extended exercise every
45 minutes — so there will always be some left over. Every one of them has a
worked solution behind it.

## Solutions: what you get, and when

| Material | Solutions |
|---|---|
| Exercises inside a deck | **Yes, immediately** — the next slide is always the worked solution, including in the appendices |
| The twelve lab notebooks | **Yes, every one** — each ends in a *Lecture exercises — worked Python solutions* section |
| Mock exams and short exams | **Yes — handed out together with the paper**; the papers themselves are not published here, see below |

The practice papers come **with their worked solutions**, distributed at the
same time. That puts the discipline on you: a solution you have already read
tells you nothing about whether you could have produced it. Work the paper
under time and closed-book *first*, then open the solutions — and use the
in-class review deck for the parts that still do not sit.

The papers, their solutions and their LaTeX sources are kept out of the public
repository, so they are not downloadable from this site. They come from your
lecturer.

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
| A | after Ch 4 | Logistic regression and the confusion matrix (Ch 4) |
| B | after Ch 5 | Cross-validation and the bootstrap (Ch 5) |
| C | after Ch 6 | Ridge and the lasso (Ch 6) |
| D | after Ch 8 | Trees: Gini, splitting, pruning, forests (Ch 8) |
| E | end of course | Multiple testing: Bonferroni, Holm, BH (Ch 13 — now module [A7](advanced.md)) |

The first two problems of each paper reach back to earlier chapters, so a short
exam is a cumulative check on everything up to that point rather than a test of
one chapter. A, C and E each open on precourse material — these five papers are
the only ones that revisit it.

**If you have fallen behind, these are the papers to use.** One of them takes an
hour, tells you exactly where you stand, and comes with a full worked solution
and a review deck. Full details are on the [Mock exams](exams.md) page; the
papers themselves come from your lecturer.

## Where to go next

- [Quick start](quickstart.md) — Colab in one click, and the local install for later.
- [The course at a glance](course.md) — the ten-chapter plan and the assessment calendar.
- [Lecture slides](slides.md) — every deck, what it covers, and what is in its appendix.
- [Lab notebooks](labs.md) — all twelve notebooks, rendered in full.
- [Mock exams](exams.md) — the eight practice papers and what each covers.

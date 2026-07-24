# Quantitative Research Methods

A complete, ready-to-teach university course in statistical learning — twelve
Beamer decks, fifteen Jupyter labs, three mock exams and the course datasets,
sharing one notation and one twelve-week rhythm.

:::{container} qrm-chips
**12** decks · **1029** core slides *(+111 optional)* · **127** exercises with
solutions · **15** labs · **3** mock exams · **22** datasets
:::

Prepared by **Prof. Dr. Christoph Weisser**, HSBI — Bielefeld University of
Applied Sciences and Arts, Summer Semester 2026.

```{admonition} Based on ISLP
:class: note

These materials follow *An Introduction to Statistical Learning, with
Applications in Python* (James, Witten, Hastie, Tibshirani & Taylor, Springer
2023 — "ISLP"). The structure, topics, notation and labs follow the book; please
cite it if you reuse them — see [Citation & licence](citation.md).
```

## Start here

::::{grid} 1 3 3 3
:gutter: 3
:class-container: qrm-doors

:::{grid-item-card} 🎓 Learning it
:link: quickstart
:link-type: doc

Read a deck, then run its lab in Colab with zero setup.

+++
Quick start →
:::

:::{grid-item-card} 👩‍🏫 Teaching it
:link: teaching
:link-type: doc

Semester plan, per-session runsheets, slide index, one `make` command.

+++
Teaching guide →
:::

:::{grid-item-card} 🛠️ Adapting it
:link: repository
:link-type: doc

LaTeX sources, generated figures, pinned environment — all editable.

+++
Repository layout →
:::

::::

## The materials

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 📚 The course
:link: course
:link-type: doc

The twelve-lecture plan, chapter map and the three split points.
:::

:::{grid-item-card} 🎞️ Lecture slides
:link: slides
:link-type: doc

Twelve decks: 1029 core slides, 111 more in optional appendices, every exercise
with a worked solution.
:::

:::{grid-item-card} 📓 Lab notebooks
:link: labs
:link-type: doc

Fifteen notebooks, rendered here in full and runnable locally or on Colab.
:::

:::{grid-item-card} 📝 Mock exams
:link: exams
:link-type: doc

Three exams, each in three formats — documented here, distributed on request.
:::

:::{grid-item-card} 📊 Datasets
:link: datasets
:link-type: doc

The 22 ISLP datasets bundled with the course, with sizes and where each is used.
:::

:::{grid-item-card} 🐍 Environment
:link: environment
:link-type: doc

What is pinned, why, and which chapter needs which extra package.
:::

::::

## What makes these materials different

**A whole course, not a pile of files.**
: Decks, labs and exams that share one notation, one dataset set and one
  twelve-week rhythm — ready to teach as-is or adapt.

**Slides built for the room.**
: Every deck moves motivation → intuition → formal definition → worked example,
  with colour-coded callout boxes and ~86 short + ~41 extended exercises, each
  followed by a full solution. The hardest, optional material sits in a per-deck
  [appendix](slides.md), so the main thread fits the twelve sessions.

**Numbers you can trust.**
: ~40 purpose-built visuals are computed from the real course datasets (not
  sketched), and every mock-exam answer was verified programmatically.

**Ready to walk into a room.**
: Timed runsheets, a generated [slide index](teaching.md) with page numbers, a
  ranked cut list for when you are behind, and `make check` to catch a slide that
  overruns its frame.

**Reproducible by design.**
: LaTeX sources for every deck and exam, a pinned Python environment, and
  datasets that resolve automatically — locally *and* on a fresh Colab runtime.

## At a glance

| | |
|---|---|
| Lecture decks | 10 chapters + two precourse sessions · 1029 slides, plus 111 in optional appendices |
| Exercises | ~86 short (~5 min) + ~41 extended (~15 min), all with worked solutions |
| Lab notebooks | 15 (2 precourse + 10 lecture chapters + 3 self-study) |
| Mock exams | 3, each in 3 formats (not distributed publicly) |
| Datasets | 22 CSVs from [statlearning.com](https://www.statlearning.com) |
| Semester shape | 12 lectures × 180 min (+ two optional precourse sessions) |
| Sources | LaTeX (Beamer) · Jupyter · Python 3.9+ · one `make` build |

```{toctree}
:hidden:
:caption: Getting started

quickstart
course
environment
```

```{toctree}
:hidden:
:caption: Materials

slides
labs
exams
datasets
```

```{toctree}
:hidden:
:caption: Teaching

teaching
```

```{toctree}
:hidden:
:caption: Project

repository
building-docs
citation
```

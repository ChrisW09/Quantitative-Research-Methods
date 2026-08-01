---
myst:
  html_meta:
    description: "A complete, ready-to-teach university course in statistical learning based on ISLP — twelve Beamer lecture decks, fifteen Jupyter labs, eight mock exams and the course datasets."
---

# Quantitative Research Methods

{.qrm-lead}
A complete, ready-to-teach university course in statistical learning — twelve
Beamer decks, fifteen Jupyter notebooks, eight mock exams and the course
datasets, sharing one notation and one semester rhythm.

:::{container} qrm-chips
[**12** decks]{.qrm-chip}
[**1027** core slides *(+139 optional)*]{.qrm-chip}
[**127** exercises with solutions]{.qrm-chip}
[**12** labs *(+3 code references)*]{.qrm-chip}
[**3 + 5** mock exams]{.qrm-chip}
[**22** datasets]{.qrm-chip}
:::

::::{container} qrm-cta
:::{button-ref} quickstart
:color: primary

🚀 Get started — a lab in Colab, one click
:::
:::{button-ref} slides
:color: primary
:outline:

🎞️ Browse the lecture decks
:::
::::

Prepared by **Prof. Dr. Christoph Weisser**, HSBI — Bielefeld University of
Applied Sciences and Arts.

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
:link: for-students
:link-type: doc

Prerequisites, workload, the skip rule, how to revise — and Colab on day one.

+++
For students →
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

The 13-session plan, the chapter map, the three split points — and how the
course is graded.
:::

:::{grid-item-card} 🎞️ Lecture slides
:link: slides
:link-type: doc

Twelve decks: 1027 core slides, 139 more in optional appendices, every exercise
with a worked solution.
:::

:::{grid-item-card} 📓 Lab notebooks
:link: labs
:link-type: doc

Twelve taught labs plus three code references, rendered here in full and
runnable on Colab or locally.
:::

:::{grid-item-card} 📝 Mock exams
:link: exams
:link-type: doc

Three full-length papers plus five 60-minute short exams — documented here,
distributed on request.
:::

:::{grid-item-card} 🚀 Quick start
:link: quickstart
:link-type: doc

Run a lab in Colab with zero setup; install locally from week two.
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

:::{grid-item-card} 🧭 Advanced modules
:link: advanced
:link-type: doc

Four optional self-study modules: RCTs, Shapley values, conformal prediction,
GLMs & splines.
:::

:::{grid-item-card} 🎯 Short projects
:link: projects
:link-type: doc

Six 3–5 hour challenges: a real decision on real data, ending in a memo.
:::

::::

## What makes these materials different

**A whole course, not a pile of files.**
: Decks, labs and exams that share one notation, one dataset set and one
  semester rhythm — ready to teach as-is or adapt.

**Slides built for the room.**
: Every deck moves motivation → intuition → formal definition → worked example,
  with colour-coded callout boxes and ~86 short + ~41 extended exercises, each
  followed by a full solution. The hardest, optional material sits in a per-deck
  [appendix](slides.md), so the main thread fits the sessions it has.

**Numbers you can trust.**
: 65 purpose-built figures are computed from the real course datasets (not
  sketched), 39 more are drawn natively in TikZ, and every mock-exam answer was
  verified programmatically.

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
| Lecture decks | 10 chapters + two precourse decks · 1027 slides, plus 139 in optional appendices |
| Exercises | ~86 short (~5 min) + ~41 extended (~15 min), all with worked solutions |
| Lab notebooks | 12 taught labs, each with worked solutions (2 precourse + 10 lecture chapters) · 3 code references for the untaught chapters (no deck, no solutions) |
| Mock exams | 3 full-length papers, each in 3 formats, + 5 sixty-minute short exams (not distributed publicly) |
| Datasets | 22 CSVs from [statlearning.com](https://www.statlearning.com) |
| Advanced modules | 4 optional self-study modules (RCTs, Shapley values, conformal prediction, GLMs & splines) · 300 slides + 4 notebooks |
| Short projects | 6 challenges on real data, 3–5 h each, each with a fixed held-out set, a baseline to beat and a memo as the deliverable |
| Semester shape | 13 × 180 min: a taught precourse session + 12 chapter lectures · **6 ECTS** |
| Assessment | One written exam at the end of the semester (120 min, 100% of the grade); the eight practice papers do not count |
| Sources | LaTeX (Beamer) · Jupyter · Python 3.9+ · one `make` build |

```{toctree}
:hidden:
:caption: Getting started

quickstart
for-students
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
advanced
projects
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

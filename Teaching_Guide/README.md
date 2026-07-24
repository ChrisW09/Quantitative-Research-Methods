# Teaching guide

Everything needed to walk into a room and teach this course without re-reading
a 120-slide deck first.

| File | What it is |
|---|---|
| [`semester_plan.md`](./semester_plan.md) | The 12 weeks on one page: what to teach when, what the assessment rhythm is, what to do if you fall behind |
| [`runsheets/`](./runsheets/) | One page per session: timing blocks, what to cut first, which exercises to run live, the misconceptions to pre-empt |
| [`slide_index.md`](./slide_index.md) | Every deck's sections with page ranges, every exercise with its page, generated from the compiled PDFs; each deck's appendix is listed but marked *optional* rather than given a time budget |
| [`before_class.md`](./before_class.md) | The ten-minute checklist for the morning of a lecture |
| [`handouts/`](./handouts/) | Printable two-up versions of every deck (`make handouts`) |
| `make_index.py`, `check_decks.py` | The generators behind the index and the health check |

## The one command you need

From the repository root:

```bash
make            # regenerate figures, rebuild any deck whose source changed, refresh the index
make check      # page counts, and any slide whose content overruns the frame
make handouts   # printable 2-up PDFs for every deck
```

`make help` lists the rest. Everything is incremental — a deck is only
recompiled if its `.tex` is newer than its `.pdf`.

## How the pieces fit

```
Lecture_Slides/chapter_NN/chapter_NN.tex   the deck you project
        │
        ├─ make ──────────► chapter_NN.pdf        (two pdflatex passes)
        ├─ make handouts ─► Teaching_Guide/handouts/chapter_NN_handout.pdf
        └─ make index ────► Teaching_Guide/slide_index.md   (page numbers)

Lab_Notebooks/chapter_NN_lab.ipynb          what students run
Mock_Exams/                                 assessment (kept out of git)
```

## A note on the appendices

Every deck ends with an appendix holding its optional, more advanced material —
formal derivations, the heaviest worked exercises, side topics. It is deliberately
outside the timed plan: the runsheets stop where the appendix begins, and
`slide_index.md` marks it *optional*. Three ways to use it:

- **Assign it.** Every exercise in an appendix has its full solution behind it,
  so students can work it alone.
- **Reach for it in the room** when a cohort wants the derivation — each runsheet
  has an "In the appendix (optional)" section naming what is there and which
  board moments moved with it.
- **Ignore it.** No slide in the main flow depends on an appendix slide.

## A note on the two precourse sessions

`chapter_00` (statistics refresher) and `chapter_00b` (notation, logs and odds,
likelihood, the Python patterns) are **optional** and sit before Lecture 1.
They exist because the ten chapter decks assume all of it silently. Two ways to
use them:

- **Taught**, as one or two extra sessions in the week before the course
  starts — worth it for a cohort with mixed backgrounds.
- **Set as self-study**, pointing students at the twelve-question self-check on
  slide 7 of `chapter_00`. Students who answer nine or more can skip it.

Either way, tell students the material is assumed from Lecture 1 onwards. The
commonest cause of a struggling student in this course is not the machine
learning — it is a rusty grasp of standard errors.

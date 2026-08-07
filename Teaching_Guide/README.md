# Teaching guide

Everything needed to walk into a room and teach this course without re-reading
a 120-slide deck first.

| File | What it is |
|---|---|
| [`semester_plan.md`](./semester_plan.md) | The twelve sessions on one page: what to teach when, what the assessment rhythm is, what to do if you fall behind |
| [`runsheets/`](./runsheets/) | One page per session (`lecture_NN.md`), plus one per self-study module (`module_aN_*.md`): timing blocks, what to cut first, which exercises to run live, the misconceptions to pre-empt. **Not published** — git-ignored, because they map exercises onto exam problems; instructors request them from the author |
| [`slide_index.md`](./slide_index.md) | Every deck's sections with page ranges, every exercise with its page, generated from the compiled PDFs; each deck's appendix is listed but marked *optional* rather than given a time budget |
| [`before_class.md`](./before_class.md) | The ten-minute checklist for the morning of a lecture |
| [`handouts/`](./handouts/) | Printable two-up versions of every deck. **Not published** — build output, git-ignored; run `make handouts` to generate the folder |
| `make_index.py`, `check_decks.py`, `check_runsheets.py`, `check_notebooks.py` | The generators behind the index, the deck health check, the runsheet page-reference validator, and the notebook re-execution check (`make notebooks`) |

## The one command you need

From the repository root:

```bash
make            # regenerate figures, rebuild any deck whose source changed, refresh the index
make check      # page counts, slides that overrun the frame, and stale runsheet page references
make runsheets  # every runsheet page reference with the slide title it lands on
make handouts   # printable 2-up PDFs for every deck
make advanced   # the eight self-study module decks (kept out of `make all`)
make notebooks  # re-execute all 25 notebooks and diff against their stored outputs
make docs       # build the documentation site locally
```

`make help` lists the rest. Everything is incremental — a deck is only
recompiled if its `.tex` is newer than its `.pdf`, and the two precourse decks
also rebuild when their `make_figures.py` changes.

## How the pieces fit

```
Chapters/chapter_NN/chapter_NN.tex   the deck you project
        │
        ├─ make ──────────► chapter_NN.pdf        (two pdflatex passes)
        ├─ make handouts ─► Teaching_Guide/handouts/chapter_NN_handout.pdf
        └─ make index ────► Teaching_Guide/slide_index.md   (page numbers)

Chapters/chapter_NN/chapter_NN_lab.ipynb    what students run
        └─ make notebooks ► re-executed and diffed against its stored outputs

Chapters/Advanced/advanced_NN_topic/        eight self-study modules (make advanced)
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
likelihood, the Python patterns) are **optional** and sit before Chapter 1.
They exist because the ten chapter decks assume all of it silently. Two ways to
use them:

- **Taught**, as one or two extra sessions in the week before the course
  starts — worth it for a cohort with mixed backgrounds.
- **Set as self-study**, pointing students at the twelve-question self-check on
  slide 7 of `chapter_00`. Students who answer nine or more can skip it.

Either way, tell students the material is assumed from Chapter 1 onwards. The
commonest cause of a struggling student in this course is not the machine
learning — it is a rusty grasp of standard errors.

# Teaching it

Everything needed to walk into a room: a semester plan, a per-session runsheet,
a generated slide index, a before-class checklist, and one `make` command that
keeps all of it in sync with the decks.

The instructor material lives in
[`Teaching_Guide/`](https://github.com/ChrisW09/Quantitative-Research-Methods/tree/main/Teaching_Guide).

## The instructor kit

| File | What it is | On GitHub |
|---|---|:--:|
| `semester_plan.md` | The twelve weeks on one page: what to teach when, where the three split lectures break, what to sacrifice when you fall behind | [open](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/Teaching_Guide/semester_plan.md) |
| `slide_index.md` | Generated from the compiled PDFs: every section with its page range and time budget, every exercise and solution with its page | [open](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/Teaching_Guide/slide_index.md) |
| `before_class.md` | The ten-minute checklist for the evening before and the morning of | [open](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/Teaching_Guide/before_class.md) |
| `runsheets/` | One page per session — timings, what to run live, what to cut, what students get wrong | not published |
| `handouts/` | Printable two-up PDFs of every deck (`make handouts`) | build output |

```{admonition} Why the runsheets are not here
:class: note

They name which exercise rehearses which exam problem, so they are assessment
material and stay out of the public repository alongside the exams themselves.
Instructors can request them from the author.
```

## One command keeps it consistent

From the repository root:

```bash
make            # figures, decks whose source changed, and the slide index
make check      # page counts, and any slide that overruns its frame
make handouts   # printable 2-up PDFs of every deck
make index      # refresh Teaching_Guide/slide_index.md from the PDFs
make docs       # build this documentation locally
make help       # the rest
```

Everything is incremental: a deck is only recompiled when its `.tex` changed,
and the slide index is regenerated from the PDFs, so quoted page numbers cannot
drift away from the slides.

## What a runsheet gives you

Each session has one page, and each page has the same eight parts:

1. **Running order** — timing blocks with page ranges, so a 180-minute session
   has a plan rather than a hope. The blocks add up to the teaching minutes left
   after arrival, breaks and questions.
2. **Run these in the room** — the two to four exercises worth live time, with
   the reason each was chosen.
3. **Set as homework** — the rest, with the page of the prompt and its solution.
4. **If you are running late, cut in this order** — a ranked cut list, written in
   advance so the decision is not made at minute 140.
5. **What they will get wrong** — the misconceptions, each with the sentence that
   fixes it.
6. **Worth doing on the board** — the two or three derivations that land better
   written by hand than projected.
7. **Before you walk in** — the notebook cells to pre-run, the numbers to have on
   screen.
8. **Close on** — the last slide, and the sentence that bridges to next week.

## Where the appendix fits

Every deck ends with an appendix holding its optional, more advanced material —
formal derivations, the heaviest worked exercises, side topics. It sits
**outside** the timed plan: the running orders stop where the appendix begins,
and the slide index marks it *optional* instead of giving it minutes.

Three ways to use it:

- **Assign it.** Every exercise in an appendix keeps its full worked solution, so
  students can do it alone.
- **Reach for it in the room** when a cohort wants the derivation. Each runsheet
  has an "In the appendix (optional)" section naming what is there and which
  board moments moved with it.
- **Ignore it.** Nothing in a deck's main flow depends on an appendix slide.

What each appendix holds is listed in [Lecture slides](slides.md).

## If you are behind

Falling behind is normal — the decks carry more than a session holds. The first
cut is already made: the appendix is outside the plan. After that, in order of
what to sacrifice:

1. **Extended exercises** — set them as homework; the solutions are in the deck.
2. **The second worked example** of a concept, when the deck gives two.
3. **The "where this reappears in the course" slides** — signposting, not content.
4. **The closing summary block** — it is written to be read alone.

Do **not** cut the motivation slide that opens a topic, the pitfall
(`alertblock`) slides, or any exercise the runsheet marks as exam-relevant.

## Where to go next

- [Lecture slides](slides.md) — deck-by-deck contents, and what is in each appendix.
- [The course at a glance](course.md) — the twelve-lecture plan and the split points.
- [Mock exams](exams.md) — the assessment rhythm and how the papers are built.

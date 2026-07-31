# Deck triage — what could become optional or appendix material

*A proposal, not a change. Nothing in `Lecture_Slides/` has been moved. Each
deck was audited independently against its own runsheet; the per-deck detail,
including the "do not move" lists, is summarised below.*

## The headline

The decks are **less bloated than the raw slide counts suggest**, and **more
over-budget than the slide index admits**. Both things are true, for different
reasons.

Only **52% of main-flow pages are core taught content**:

| Kind | Pages | Share |
|---|--:|--:|
| Core taught content | 549 | 52% |
| Exercise + worked-solution pairs | 322 | 30% |
| Front matter (title, contents, notation, objectives, industry) | 94 | 9% |
| Auto-generated `Outline` navigation slides | 92 | 9% |
| **Main flow, total** | **1057** | |

So the "1.7 min per slide" figures are pessimistic — a third of every deck is
exercise pairs the session was never going to run live, and a tenth is
navigation that costs seconds. But the runsheets — your own timed plans — are
the honest measure, and **five of them already exceed their own budget before
any slack**:

| Deck | Runsheet plans | Budget | Verdict |
|---|--:|--:|---|
| Precourse (`chapter_00` + `chapter_00b`) | ~250–264 min | 145 min | the merged session cannot be taught as written |
| `chapter_01` | 80 min | 72 min | over by 8–11% |
| `chapter_03` | 295 min | 290 min | marginally over |
| `chapter_05` | 150 min | 145 min | over by 5 |
| `chapter_08` | 150 min | 145 min | over by 5, before four board-work items |
| `chapter_07` | — | 145 min | "unachievable as written" — the spline block alone runs at 2.9 min/slide |
| `chapter_13` | 145 min | 145 min | fits exactly |

## Per-deck proposal

| Deck | Main now | min/slide | Move | Main after | min/slide after | Highest-confidence candidate |
|---|--:|--:|--:|--:|--:|---|
| `chapter_00` | 106 | 0.92\* | 29 | 77 | 1.27 | Ext 0.1 + Ext 0.4 (pp. 70–72, 94–96) — already homework |
| `chapter_00b` | 51 | 0.92\* | 8 | 43 | 3.4† | *Maximum likelihood outside the classroom* (p. 31) — a second industry slide |
| `chapter_01` | 71 | 1.01 | 9 | 62 | 1.16 | NumPy/pandas/sklearn tours (pp. 48–50) — all three in the lab, duplicated in `00b` |
| `chapter_02` | 107 | 2.03 | 10 | 97 | 2.24 | Ext 2.2 + solutions (pp. 85–87) — siblings 2.1/2.3 already in appendix |
| `chapter_03` | 144 | 2.00 | 14 | 130 | 2.25 | Ext 3.L1 + solutions (pp. 51–54) — siblings 3.L2/3.L6 already in appendix |
| `chapter_04` | 112 | 2.60 | 10 | 102 | 2.84 | four bare lab code slides (pp. 92–95) — byte-identical to notebook cells |
| `chapter_05` | 79 | 1.80 | 10 | 69 | 2.10 | Ext 5.2 + solutions (pp. 52–55) — task-identical to Exercise 5.6 |
| `chapter_06` | 81 | 1.79 | 11 | 70 | 2.07 | four bare code slides (pp. 61–64) — verified self-contained |
| `chapter_07` | 85 | 1.70 | 15 | 70 | 2.10 | four lab code slides (pp. 63–66) — runsheet says "do not read" |
| `chapter_08` | 83 | 1.70 | 15 | 68 | 2.13 | Ext 8.1 + solutions (pp. 33–36) — runsheet says don't open the solutions |
| `chapter_10` | 75 | 1.90 | 7 | 68 | 2.13 | the whole `Sequences` section (pp. 45–48) — see below |
| `chapter_13` | 63 | 2.30 | 10 | 53 | 2.70 | Ext 13.2 + solutions (pp. 45–48) — already set as reading |

\* share of the merged 180-min precourse session.
† standalone; the deck is only overloaded because it now shares a session.

**Total: 148 slides**, main flow 1057 → 909, appendices 111 → 259.

## Six patterns that account for nearly all of it

1. **Extended exercises already set as homework.** A 15-minute exercise cannot
   run in a 180-minute session, and the house convention keeps the full worked
   solution with the prompt — so moving the pair costs students nothing. The
   precedent is already set: Ext 2.1/2.3, 3.L2/3.L6, 6.2, 7.1, 8.2 and 0.3 are
   *already* in appendices. This is the single largest and safest category.
2. **Bare lab code slides** that duplicate the companion notebook line for line
   (`chapter_04` pp. 92–95, `chapter_06` pp. 61–64, `chapter_07` pp. 63–66,
   `chapter_03` pp. 130/132/135). Every runsheet says to run the notebook
   instead.
3. **The same object drawn twice** — an ISLP figure beside a native redraw, or
   two views of one geometry (`chapter_02` p. 76, `chapter_03` pp. 28–29 and
   103/104, `chapter_05` p. 28, `chapter_07` p. 54, `chapter_08` pp. 17 and 19,
   `chapter_10` pp. 14/16 and 52, `chapter_13` p. 29).
4. **"Mini-check" slides** that restate the previous slide at lower density with
   the answers printed (`chapter_06` p. 48, `chapter_07` p. 47, `chapter_08`
   p. 46).
5. **"Connections to the rest of the course"** signposting inside the summary
   (`chapter_05` p. 76, `chapter_06` p. 78, `chapter_07` p. 82, `chapter_13`
   p. 62 *Course-wide summary*).
6. **The industry pair.** Every runsheet ranks it cut #1, but it is house style
   in all 12 decks — so it should be decided once, for the whole course, not
   deck by deck.

## The zero-content-cost lever

**92 pages are auto-generated `Outline` slides** — one per `\section`, produced
by `\AtBeginSection`, already suppressed after `\appendix`, and narrated by no
runsheet. Suppressing them course-wide removes 9% of every deck with no content
loss whatsoever. It also resolves the two over-length summaries for free (see
below). This is one line of LaTeX per deck and a course-wide house-style
decision.

## The two biggest single wins

- **`chapter_10`'s `Sequences` section (pp. 45–48).** The dependency check came
  back clean on all three axes: the lab notebook has no sequence content, no
  file in `Mock_Exams/` mentions RNN, LSTM, transformer, attention or hidden
  state, and `semester_plan.md` states the session as "MLPs, backprop, CNNs".
  The appendix already holds *Transformers (briefly)*, so the RNN slides join
  their companion.
- **The precourse.** 29 slides out of `chapter_00` and 8 out of `chapter_00b`
  gets the merged session from 157 slides to 120 — still not one session's
  worth, which is why `docs/course.md` frames it as a guided selection. Triage
  helps; it does not solve a 250-minutes-into-145 problem on its own.

## What must not move

The audits were asked to name load-bearing slides that *look* optional. The
recurring ones:

- **`chapter_00`:** the notation convention (pp. 4, 16), SD vs SE (p. 58) with
  the CI-coverage pair (59–60), the expectation/variance rules (p. 47 — this is
  Chapter 2's bias–variance algebra), the Type I/II table (p. 63 — Chapter 4's
  confusion matrix and Chapter 13's FWER/FDR), the regression bridge (74–77),
  and the self-check (p. 7), which is the mechanism the documented "selection"
  plan depends on.
- **`chapter_02`:** Ext 2.4 (pp. 96–98) looks exactly like the rank-1 candidate
  but is cited twice by the summary, and its 0.994 coefficient is the narrative
  bridge into Chapter 3.
- **`chapter_04`:** p. 55 is the QDA discriminant — core, and Exercise 4.6
  depends on it. (The runsheet's cut list names it by mistake; see below.)
- **`chapter_07`:** both LOESS slides. LOESS is never examined and appears in no
  later deck, but it is lab §4 run live, Mini-check q3, Self-check q5, a
  methods-comparison row and a stated learning outcome.
- **`chapter_08`:** the partition picture. The main-flow and appendix versions
  *do* duplicate — but the fix is a **swap** (promote the appendix redraw,
  demote the ISLP figure), because moving the main-flow one out leaves the
  taught thread with no partition picture at all.

## Runsheet errata found on the way — worth fixing regardless

Five runsheets name **stale page numbers in their cut lists**. Acting on them
literally would cut the wrong slides:

| Runsheet | Says | Actually |
|---|---|---|
| `lecture_04.md` (Ch 4) cut #2 | pp. 55, 66 | pp. 57, 68 — **p. 55 is the QDA discriminant, p. 66 is an Outline frame** |
| `lecture_01.md` (Ch 1) cut #4 | pp. 27, 31 | pp. 30, 34 — the literal reading deletes two dataset slides |
| `lecture_06.md` (Ch 6) cut #2 | pp. 73, 76–78 | pp. 75, 78, 79, 80 (off by two) |
| `lecture_13.md` (Ch 13) cut #3 | pp. 57, 60–61 | pp. 59, 62, 63 |
| `lecture_08.md` (Ch 8) | three page numbers | stale |

`make check` passes these because the pages *exist*; `make runsheets` flags them
as gloss-vs-title warnings, which is why they are worth reading rather than
ignoring. Separately, `chapter_01`'s runsheet claims p. 40 "carries the whole
convention — n, p, the design matrix, hats and the tr/te subscripts"; p. 40
carries n, p and typography only — the hat convention, residuals and tr/te
subscripts are **appendix-only** (p. 75). Given Chapter 1 has budget room,
promoting that block is worth more than any further trimming.

## The cost of acting, and how to pay it

Moving frames shifts printed page numbers, and page numbers are referenced in:

- **826 hand-written references across the 12 runsheets** (Ch 0's alone has 93);
- **self-check slides inside the decks** — `chapter_02` p. 105 cites six pages,
  `chapter_03` p. 142, `chapter_05` p. 77 (six, including two appendix pages),
  `chapter_07` p. 83 (six), `chapter_08` p. 81 (six), `chapter_00` p. 103
  (eleven). `make index` does **not** fix these; they are inside the slides;
- 9 page references in `docs/` and `README.md`;
- the split-point pages quoted in `docs/course.md` and each deck's p. 2.

The repair is mechanical rather than manual: `Teaching_Guide/check_runsheets.py`
already resolves every page to its frame title, and a page→title snapshot of all
1168 pages was taken before any change. So the sequence is: move → `make index`
→ rewrite references by matching titles to their new pages → `make check` → fix
the in-deck self-check slides by hand (six decks) → recompile.

## Suggested tiers

- **Tier 0 — free, no content decision.** Suppress the 92 `Outline` slides. Fixes
  the two 11-page summaries as a side effect. One line per deck.
- **Tier 1 — safest 60 slides.** Extended-exercise pairs already set as homework,
  plus the bare lab code slides. Both categories have established precedent in
  the appendices, and neither costs students a worked solution.
- **Tier 2 — the duplicate figures and mini-checks.** Needs a look at each pair to
  choose which of the two to keep; three cases are swaps, not moves.
- **Tier 3 — the industry pairs and the signposting slides.** A course-wide style
  decision, best made once rather than twelve times.

Tier 1 alone takes the worst decks from 1.7 to roughly 2.0 min/slide and needs no
figure judgement — it is the recommended starting point.

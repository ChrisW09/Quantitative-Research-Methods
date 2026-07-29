# Quantitative Research Methods — curriculum, coverage and pedagogy review

Prof. Dr. Christoph Weisser, HSBI · ISLP (James et al. 2023) · 12 × 180 min + 2 precourse decks

Reviewed: the twelve `Lecture_Slides/chapter_*/chapter_*.tex` sources (1,168 pages), all fifteen
`Lab_Notebooks/*.ipynb`, `Teaching_Guide/` (semester plan, twelve runsheets, `slide_index.md`,
`before_class.md`, `make_index.py`, `check_decks.py`), `README.md`, `docs/`, and — because the
alignment question cannot be answered without them — the sources in `Mock_Exams/`.

Note: the repository was being edited by another process while I read it (`git status` went from
clean to five modified files mid-review). Line numbers below were re-verified at the end, but a
few may have shifted by a line or two. Page numbers come from `Teaching_Guide/slide_index.md`,
which is generated from the compiled PDFs and is the stable reference.

---

## 1. Where the course actually stands

This is not a course that needs curriculum work. It needs **consistency maintenance** — the
material has outgrown the metadata that describes it, and a handful of promises made on the
objectives slides are no longer true of the decks behind them.

What is unambiguously in good shape:

- **The assessment layer is more complete than the plan admits.** Three long papers, three
  parallel variants of the final, five 60-minute short exams, worked solutions and a review
  deck for each — built from a single source per paper via `\withsolutions`, sub-parts
  independent, "points ≈ minutes", and a per-problem grading key
  (`Mock_Exams/Short_Exams_60min/README.md:22-27`). The blueprint tables
  (`Final_Exam_after_Lecture_12/solutions_slides_final.tex:69-80`) map every problem to a
  chapter. Very few courses at this level have this.
- **The runsheets are the best artifact in the repository.** The "What they will get wrong" and
  "Worth doing on the board" sections are not generic — `lecture_02.md:79` correctly predicts
  that students will read Fig 2.17's x-axis as $K$ rather than $1/K$; `lecture_13.md` builds
  Holm's ladder as a column of six numbers before revealing the slide; `lecture_06.md` has the
  lecturer derive the soft threshold and circle the divide-by-two because "half the room will
  otherwise threshold at $\lambda$". This is hard-won teaching knowledge written down.
- **The appendix mechanism works, and it is honest.** Every deck opens its appendix with an
  "Appendix — what is in here, and why" frame that names the main-flow substitute. Two examples
  of the standard being met: `chapter_06.tex:1486` describes its own appendix geometry slide as
  "a duplicate of the diamond-vs-circle picture that is already in the main deck"; `chapter_07`
  keeps the truncated-power derivation in the appendix but says the main deck retains "the
  picture and the degrees-of-freedom rule, which is what you are asked to apply" — and the
  final exam does indeed ask only for the df count and the basis count
  (`solutions_slides_c.tex:174`).
- **The industry boxes are the strongest recent addition** and they are pitched exactly right
  for HSBI. `chapter_08.tex:727` on impurity importance being biased toward high-cardinality
  variables and risk teams reporting SHAP "because those are the reason codes a declined
  applicant must be given"; `chapter_08.tex:849` on champion/challenger and the observation that
  whether the boosted model *may* take the decision "is a model-governance question, not a
  statistical one". That is business-school content that no ISLP-derived course usually has.

Where it is weaker than it looks:

- **Eleven objectives slides promise things the decks and exams do not deliver** (§R2). This is
  the largest single defect and it is entirely a text problem.
- **`lecture_01.md` and parts of `lecture_02.md` carry stale slide numbers** — a −3 and a −2
  offset respectively, verified against the compiled decks (§R1). The later runsheets are clean,
  which is why this has gone unnoticed.
- **Nothing in the course asks a student to retrieve last week's material.** Not one deck has a
  recap or warm-up frame; `chapter_02`, `chapter_08` and `chapter_10` contain zero cross-chapter
  references of any form; `chapter_06`, `chapter_08` and `chapter_10` have no `[Integrative]`
  exercise at all — and the final is weighted to Ch 7/8/10/13.
- **The three "self-study" chapters are not self-study material.** They are code tours (§R6).
- **The two precourse sessions are wildly unbalanced** — 106 main-flow slides against 51, for
  the same 180 minutes (§R4).

---

## 2. Prioritised recommendations

### R1 — Fix the two stale runsheets, then make staleness impossible · ~5 h · displaces nothing

**What.** `Teaching_Guide/runsheets/lecture_01.md`'s prose is offset by −3 pages throughout;
`lecture_02.md`'s "Worth doing on the board" and "What they will get wrong" sections are offset
by −2. Then extend `make_index.py` to validate every `p. N` in the runsheets against the frame
titles it already extracts from the PDFs.

**Evidence.** In `lecture_01.md`, the running-order *tables* are right and the prose inside them
is wrong:

| Runsheet says | Actual page (`chapter_01.pdf`) |
|---|---|
| "Give 4 minutes on slide 19 … before showing 20-21" (Ex 1.1) | prompt p. 22, solutions 23-24 |
| "Slide 37 now carries the whole convention — $n$, $p$, the design matrix" | p. 40 |
| "Show slide 44 (standard imports)" | p. 47 |
| "Slide 60's six pitfalls deserve a real minute" | p. 63 |
| "Slide 62 is the notebook handoff" | p. 65 |
| "the five-patient table on slide 50 has $p=4$" (×3 in the misconceptions) | Exercise 1.3, p. 53 |
| "The deck only states it formally on slide 65" | p. 68 |
| "finish on 73" | main flow ends at p. 71; 73 is inside the appendix |

Two rows are worse than stale. Cut-list row 3 says cut "27, 31 — the two recreated figures";
pp. 27 and 31 are *"Example 1: Wage"* and *"Example 2: Smarket"*, the two slides that introduce
the examples — the recreated figures are pp. 30 and 34. Cut-list row 4 says cut 67-70 and then
"skip to slide 68", which is inside the range it just cut.

In `lecture_02.md` the same sections drift by −2: "Slide 12 (Reducible vs irreducible error)" is
p. 14; "Slide 51 (The bias-variance decomposition)" is p. 53; "Slide 56 (the trade-off,
schematically)" is p. 58; "Exercise 2.4, slide 59" is p. 61; "Slide 80 (Exercise 2.7)" is p. 82.
The block prose in the same file is correct, so this is an editing-generation artifact, not
sloppiness. And `lecture_02.md:16` says "BREAK GOES HERE, after p.112" in a block covering
pp. 64-66 — p. 112 is deep in the appendix.

I checked `lecture_05.md`, `lecture_06.md`, `lecture_08.md` and `lecture_13.md` against the decks
and they are accurate (two small exceptions in `lecture_08.md`: Extended Ex 8.2 is p. 86 not 84,
Extended Ex 8.3 is p. 71 not 69).

**Why it matters here.** These files exist precisely so you can walk in without re-reading the
deck (`Teaching_Guide/README.md:3-4`), and `before_class.md:11-12` tells you to pick your cut
list from them the evening before. A cut list that deletes the two example-introduction slides
instead of the two redundant figures is worse than no cut list. Lecture 1 is also the session
with the least slack (§R5), so this is where a wrong jump costs most.

**One related risk, cheap to remove.** `Teaching_Guide/runsheets/` is gitignored
(`.gitignore:13-15`, "The runsheets say which exercises map onto which exam problems, so they are
assessment material too"). The reasoning is sound, but the consequence is that ~1,200 lines of the
most valuable and least reproducible teaching material in the project has **no version history and
no backup** — while `before_class.md:52-55` explicitly asks you to keep editing it year after year
("next year's you will be grateful"). A private second repository, a submodule, or an
`--assume-unchanged` local branch would keep it off GitHub and still keep its history. ~1 h.

**Cost.** 2 h to correct the two files. 3 h to add the validator: `make_index.py` already builds
`{page: frame title}` from each PDF (`frame_titles()`), so a `make check-runsheets` that regexes
`p\.\s?(\d+)` out of each runsheet and prints page/title pairs for eyeball confirmation is a
~40-line addition. `check_decks.py` currently only checks page counts and overfull vboxes, so
nothing catches this today.

### R2 — Reconcile the objectives slides with what is taught and examined · ~5 h · displaces nothing

**What.** Edit eleven objectives slides. Every deck opens with a well-formed, verb-first,
Bloom-appropriate list — `\textbf{Estimate}`, `\textbf{Distinguish}`, `\textbf{Diagnose}` — and
they are genuinely better written than most. But several are now false.

**Promised, never examined:**

- `chapter_03.tex:207-209` — "**Distinguish** a confidence interval for the regression line from
  a prediction interval for an individual outcome." No exam in `Mock_Exams/` contains the string
  "prediction interval", in any of the eleven papers. It is also `chapter_03`'s self-check
  question 6. The deck teaches it properly (there is even a dedicated common-mistake note on
  dropping the "$1+$" under the root, `chapter_03.tex:1217`).
- `chapter_03.tex:210-212` — "**Diagnose** … outliers / leverage". "leverage", "Cook" and
  "residual plot" appear in no exam paper. Collinearity and VIF do (`mock_exam_1.tex`,
  `final_mock_exam_c.tex`), so this is a partial gap on the *largest* section of the chapter
  after simple regression (Diagnostics, pp. 100-123, 24 slides / 49 min) — taught the week
  before Exam 1 and then barely tested.
- `chapter_04.tex:161-163` — "**Generalise** to multinomial responses and Poisson regression
  through the GLM framework." The multinomial half is fine (main flow, pp. 37-42). The Poisson
  half lives only in the appendix, where the same deck says of it: "**Not examinable**"
  (`chapter_04.tex:2342`). A learning objective and an appendix note in the same PDF contradict
  each other. No exam mentions Poisson.
- `chapter_06.tex:156-158` — "**Use** principal-components and partial-least-squares
  regression." PCR/PLS is 3 slides (pp. 53-55, 5 min). Its only exercise, 6.6, is in the
  appendix (p. 91). PLS itself is appendix-only, and the deck says so: "PCR is the version that
  appears in the lab and the exam" (`chapter_06.tex:1489`). PCR appears in exactly one of three
  final-exam variants (`final_mock_exam_b.tex`); "partial least squares" in none. "**Use**" is
  not what a student can do here — "**recognise when** dimension reduction is the right response
  to collinearity" is, and that is worth keeping.

**Promised, in optional material:**

- `chapter_00.tex:186` — "**Manipulate** vectors and matrices, and read the matrix form of the
  regression estimator" — and `:188` "**Differentiate** a loss function and take a
  gradient-descent step." Both live entirely in the appendix (pp. 107-122), which
  `lecture_00.md` explicitly moves out of the timed plan ("the algebra and calculus blocks moved
  to the appendix"). Two of nine stated objectives for the refresher are outside the session
  that states them. The same deck then tells students at `chapter_00.tex:2393-2396` that
  "'standard error', 'residual', 'conditional probability' and 'gradient' are used without
  further explanation" from Lecture 1 on — a warning about a word the timed session never
  teaches. Gradient descent is a prerequisite for `chapter_10` and the matrix form for
  `chapter_06`'s ridge slide.
- `chapter_02.tex:170` — "**Derive** and **interpret** the bias-variance decomposition." The
  derivation is Extended Exercise 2.1, appendix pp. 109-112. `lecture_02.md` compensates by
  doing it on the board, which is the right call — but then the objective's Bloom level ("derive")
  is delivered only if the lecturer chooses to, and the exam asks for the numerical
  substitution, not the derivation (Exam 1 P2). Either soften to "**apply** and **interpret**"
  or promote the derivation.

**Taught but not stated:** `chapter_08`'s roadmap lists BART as the fifth ensemble
(`chapter_08.tex:166`) and its self-check asks "In what sense is BART a Bayesian boosting
algorithm?" (`:1257`) — but BART is not an objective, and its only slide is appendix p. 90. The
appendix note handles this correctly ("Random forests and boosting are the two you will be asked
about"); it is the self-check question that is misplaced.

**Why it matters here.** A business cohort reads the objectives slide as the revision contract.
An objective that is not assessed wastes their time; one that is assessed but unstated is a
fairness problem. Also: `Teaching_Guide/README.md:54` asserts "No slide in the main flow depends
on an appendix slide." That claim holds for content, and I checked the cases that looked most at
risk (ch06 geometry, ch07 truncated-power, ch10 backprop are all in the main flow) — but it does
not hold for the *objectives* slides, which are in the main flow and point at the appendix.

**Cost.** ~5 h of careful text editing on eleven slides, plus a decision on each of the four
"promised, never examined" items: soften the objective, or add the exam question. Two lines in
`chapter_00`'s objectives could instead be fixed structurally by R4.

### R3 — Give the self-check slides answers, and make the deck solutions hideable · ~8 h · displaces the current one-PDF-per-deck build

**What.** Two changes to the practice architecture.

*(a) The self-check slides are a dead end.* Every chapter deck closes with a "Self-check
questions" frame — six questions, no answers, no page pointers. Several ask for appendix
material: `chapter_03`'s Q1 "Derive the OLS slope from the normal equations" is Extended Exercise
3.L2 (appendix p. 147); `chapter_05`'s Q6 "derive the LOOCV shortcut formula using leverage" is
appendix Exercise 5.2; `chapter_08`'s Q5 is BART, appendix p. 90. `chapter_05`'s Q2 ("Show that
5-fold CV has lower variance than LOOCV") is not something this cohort can show.

The fix already exists in your own repository: `chapter_00`'s twelve-question self-check says
"Each question maps to one section, so a wrong answer tells you where to read: 1-2 one variable;
3 two variables; 4 probability; …" That is a diagnostic instrument. The other eleven decks have
the same slide without the mapping. Adding `(p. NN)` to each self-check item, in all eleven
decks, is ~3 h and it converts the single most natural landing page for a student who has fallen
behind from a dead end into a route back in.

*(b) Every solution is the adjacent slide, by design.* `slide_index.md` confirms prompt p. N,
solution p. N+1, for all 139 in-deck exercises, and `before_class.md:41` relies on it ("The
solution slide is always the next one"). That is right for the room and wrong for the desk. It is
worse in print: the handout is `nup=1x2` (`handout_template.tex:11`), so a prompt on an odd page
sits on the same physical sheet as its own answer — that is 9 of `chapter_03`'s 18 exercises.

A `\newif\ifsolutions` toggle in each preamble plus a `make decks-nosolutions` target producing
`chapter_NN_student.pdf` costs ~4 h (the exam sources already do exactly this with
`\withsolutions`, so the pattern is in-house). Project the full deck; publish the student
version; keep the solutions PDF for after the seminar. Note the labs are already the inverse of
this and get it right: the taught twelve each have a "Lecture exercises — worked Python
solutions" section *plus* four unsolved exercises at the end
(`chapter_08_lab.ipynb`, cells 19-31 then 31).

*(c) While you are in there,* three sessions have long unpractised stretches against the deck's
own claimed cadence of a short exercise every ~20 min. From the exercise page lists in
`slide_index.md`: `chapter_05` has 19 pages (≈ 35 min) between Ex 5.1 (p. 18) and Ex 5.3 (p. 37),
covering all of LOOCV and most of $k$-fold — the two procedures Exam 2 P4 tests; `chapter_06` has
16 pages between Ex 6.5 (p. 49) and Ex 6.7 (p. 65), covering the end of the lasso, PCR/PLS and
the high-dimensional regime; `chapter_02` has 15 pages between Ex 2.5 (p. 64) and Ex 2.6 (p. 79)
across the whole Bayes-classifier introduction. `chapter_03` (max gap 10 pages) and `chapter_13`
(max gap 8) show what good looks like.

**Cost.** 3 h for the self-check pointers, 4 h for the solutions toggle, 3-4 h if you also add
one short exercise into each of the three gaps. Displaces only build simplicity.

### R4 — Rebalance the two precourse sessions and teach Python once · ~10 h · displaces `chapter_00`'s Python section and two runsheet cut-list rows

**What.** The two precourse decks are pitched well individually — `chapter_00b`'s "Reading
mathematical notation" and "Probability, odds and the logit" sections are exactly the right
bridge for a business cohort, and its "Where each topic reappears in the course" table plus
`chapter_00`'s "Bring with you" takeaway are a genuinely good handoff into Lecture 1. But the
*split between them* is wrong.

**Evidence.** `slide_index.md`: `chapter_00` is 106 main-flow slides in one 180-min session,
≈ 1.4 min per slide — the densest session in the entire course. `chapter_00b` is 51 slides in the
same 180 minutes, ≈ 2.8 min per slide — the loosest, and its runsheet says so outright
("*Total: 125 minutes of teaching — 20 minutes of slack*"). `chapter_00` covers descriptive
statistics, bivariate statistics, probability, six distributions, sampling and CIs, hypothesis
testing, simple linear regression *and* a 14-slide Python toolkit; the linear algebra and
calculus that two of its own objectives promise are pushed to the appendix to make it fit.

There is also fourfold Python redundancy. `chapter_00` pp. 83-96 (14 slides) and `chapter_00b`
pp. 34-42 (9 slides) both teach the toolkit; then `chapter_01` pp. 44-50 does NumPy/pandas/
sklearn tours; then `chapter_02` pp. 90-91 does array syntax again. The runsheets' answer is to
cut two of the four — `lecture_01.md` cut #1 removes pp. 48-50 because "the precourse toolkit
deck already covers Python basics", and `lecture_02.md` cut #3 removes pp. 90-91 because they are
"already covered in the precourse decks (chapter_00 pp.83-96 and chapter_00b pp.33-41)". Teaching
something four times and cutting it twice is a symptom, not a design.

**Proposal.** Move `chapter_00`'s Python toolkit (pp. 83-96) into `chapter_00b`, whose Python
section it belongs beside and which has the 20 minutes of slack to hold it. That frees ~19 min in
`chapter_00`, enough to bring the linear-algebra and gradient-descent material out of the
appendix and into the timed plan — which makes its own objectives (`:186`, `:188`) true and
removes the "gradient is used without further explanation" trap. Then delete `chapter_01`
pp. 48-50 and `chapter_02` pp. 90-91 outright rather than cutting them live every year.

**Why it matters here.** Your own diagnosis is at `Teaching_Guide/README.md:69-70`: "The
commonest cause of a struggling student in this course is not the machine learning — it is a
rusty grasp of standard errors." `chapter_00` is the deck that fixes that, and it is the one
deck that cannot be delivered in its slot.

**Cost.** ~10 h: moving 14 slides between decks (the two decks have separate preambles and
`make_figures.py`, so figure paths need care), rewriting two runsheets, deleting 5 slides.

### R5 — A retrieval opener per session, and mark Lecture 1's break · ~5 h · displaces ~2 min/session of closing revision

**What.** Add one frame at the front of each of the twelve sessions: three questions on last
week, answers on the same slide, 3 minutes, no marks.

**Evidence that nothing does this today.** I grepped all twelve decks for a recap / warm-up /
"where we were" frame: there are none (`chapter_01`'s "Prerequisites" is the only near-miss).
Cross-chapter references are absent from the three decks that most need them: `chapter_02` (6
total, none in `Ch.~N` form), `chapter_08` (5), `chapter_10` (6) — `chapter_10`'s own roadmap
calls single-layer networks "logistic regression in disguise" without pointing at Chapter 4, and
`chapter_08` never sends students back to Chapter 5 although pruning selects $\alpha$ by CV, or to
Chapter 6 although boosting's $\lambda$ is shrinkage. Only `chapter_04` and `chapter_05` have a
"Connections to the rest of the course" frame; `semester_plan.md:58` lists "the *where this
reappears in the course* slides" as a standing cut item, which reads as if they were everywhere —
they exist in four decks out of twelve.

**And a scheduling gap:** `before_class.md:35` says "Say at the start where the break falls."
`lecture_01.md` has no break block. Lecture 1 is 74 min (`chapter_01`) + 72 min (`chapter_02`
blocks 1-3) = **146 minutes of planned teaching, the heaviest single session in the course**, and
the only break marked anywhere in the two runsheets that cover it is placed 75 minutes into
Lecture *2* (`lecture_02.md:16`). Lecture 1 is also 113 pages across two decks, and `chapter_01`
is budgeted at 1.0 min/slide against 2.0 for `chapter_02` and 2.6 for `chapter_04` — the
"half-session" allocation has quietly made Chapter 1 the fastest-paced deck in the course.

**On the "155-page deck".** Worth correcting the premise: `chapter_03` is 155 pages (144 + 11)
but it spans *two* sessions, so at 76 and 68 pages per half it is one of the better-paced decks
in the course. The largest deck in a single 180-minute slot is `chapter_00` at 122 pages, and
the heaviest single *session* is Lecture 1 — 113 pages across two different decks. Both are
addressed above (R4, and the break below).

**Where a lecturer will fall behind.** By the runsheets' own totals: Lecture 1 (146 min),
Lectures 3 and 4 (145 min each, `lecture_03.md` totals 290 for two), Lecture 7 (145) and Lecture
10 (145) are all at or over the 145-minute ceiling `slide_index.md:5` derives from a 180-minute
slot — i.e. **zero contingency**, in a slot where 35 minutes is already the entire allowance for
arrival, break and questions. Lectures 6, 9 and 11 (135, 137, 135) have real slack. The two
sessions to protect are Lecture 1 and Lecture 7.

*(Speculative, flagged as such: I would expect Lecture 2 to be where a business cohort
saturates. Its runsheet puts bias-variance (30 min), reading the U-curve (18), the Bayes
classifier and KNN (30) and KNN-by-hand (22) — 100 minutes of the most abstract material in the
course — into one afternoon, with the break at minute 75. I am inferring this from the block
structure, not observing it.)*

**Cost.** 4 h for twelve opener slides (the content already exists — each is three items lifted
from the previous deck's "Ten things to remember"). 1 h to add a break block to `lecture_01.md`
and rebalance Lecture 1's last block. Displaces 2-3 min per session, taken from the closing
revision block that every runsheet already says to hand out rather than read.

### R6 — Decide the Ch 9 / 11 / 12 question in the artifacts, not in the docs · 2 h or 15 h

**What.** `README.md:112-113`, `docs/course.md:45-46` and `docs/repository.md:46` all state that
the missing decks are intentional and those chapters are self-study. The *intent* is documented
five times. The *artifacts* do not discharge it.

**Evidence.** Measured against the twelve taught notebooks, the three self-study notebooks are
stubs:

| Notebook | cells | code | "Lecture exercises — worked solutions" section |
|---|:--:|:--:|:--:|
| taught chapters (median) | 29 | 11 | yes, all twelve |
| `chapter_09_lab.ipynb` | 16 | 6 | **no** |
| `chapter_11_lab.ipynb` | 17 | 7 | **no** |
| `chapter_12_lab.ipynb` | 18 | 7 | **no** |

`chapter_12_lab.ipynb` introduces PCA, K-means and Ward linkage in seven code cells with no
conceptual markdown whatsoever — `PCA().fit(Xs)`, a biplot, a scree plot, a dendrogram — and then
asks the student, unaided and unanswered, to "Implement the matrix-completion algorithm
(iterative PCA imputation) on a data set with random missing entries" (cell 17). A business
student cannot learn what a principal component is from that. These are excellent *code
references for someone who attended the lecture*, and there is no lecture.

**Two honest options.** (a) 2 h: relabel them in `README.md`, `docs/labs.md` and
`docs/course.md` as "code reference — no lecture provided; read ISLP §9/11/12 first", and stop
calling them self-study. (b) 15 h: bring each up to the standard of the taught twelve — a
concepts section, a worked-solutions section, and four unsolved exercises with the answers in a
companion. I would do (a) now for Ch 9 and 11, and fold Ch 12 into A1 below.

**On the cost of the omissions themselves.** SVMs (Ch 9) are the cheapest to omit and I would not
add them: your own `chapter_08.tex:219` says boosted trees are "today the default choice" for
wide mixed-type tabular data, which is this cohort's whole world, and 180 minutes spent on the
kernel trick buys less than 180 minutes spent on anything else in the list. Survival analysis
(Ch 11) has real business content — time-to-churn, time-to-default, customer lifetime — but it is
the most self-contained chapter in ISLP and can stay self-study without breaking anything.
**Unsupervised learning (Ch 12) is the expensive omission**, and not only because segmentation is
the single most-used technique in commercial analytics. It has structural dependencies inside
your own course: `chapter_06`'s PCR is defined as regression on "the principal components of
$\mathbf{X}$" (`chapter_06.tex:1066`) with PCA itself never taught; `chapter_01`'s third
motivating dataset is *"NCI60: the first two principal components"* (`chapter_01.tex:686`), shown
in week 1 and never explained; and `chapter_00b`'s "Where each topic reappears" table sends
students to "Ch. 12 (clusters)", a chapter with no deck.

---

## 3. Additions worth considering

### A1 — A taught half-session on PCA and clustering, funded by compressing Ch 13 and Ch 10 · 25-35 h

**What to add.** A ~45-slide `chapter_12` deck at half-session length: PCA (loadings, PVE, scree,
biplot), $K$-means, hierarchical clustering, and one honest slide on why cluster counts are not
identifiable. Plus upgrading `chapter_12_lab.ipynb` from 18 to ~28 cells with a worked-solutions
section.

**Why for this audience.** It is the only chapter on the list a marketing or controlling graduate
will be asked to run in their first job, and it closes the three internal dependencies listed in
R6. It also gives `chapter_06`'s PCR objective something real to stand on.

**What it displaces — and this is the honest part.** Two half-sessions have to come out, and the
evidence points at the same two chapters:

- **Ch 13 (Multiple Testing) → half session.** 63 slides, 141 min planned, and the loosest
  budget in the course at 2.3 min/slide. FWER and BH are genuinely valuable for a cohort that
  will run A/B tests, but "The Problem" (8 slides) + FWER (9) + FDR (16) + Practice (6) is a
  90-minute topic delivered in 180. Compressing to a half session costs the resampling-based
  $p$-value material, which is already appendix-flavoured.
- **Ch 10 (Deep Learning) → half session.** 75 slides, 135 min. Six of its nine exercises are
  hand arithmetic ([Math]: 10.1, EE 10.1, 10.3, 10.4, 10.5, EE 10.2) and only one is [Concept] —
  the lowest conceptual share of any deck. The final exam tests it as "Neural networks by hand"
  (20/120). For a business cohort, hand-computing a CNN's output dimensions has almost no
  transfer; deciding *whether* to buy a deep-learning solution has a great deal, and that is the
  one objective (`chapter_10.tex`: "**Reason** about when deep learning is worth it") that no
  exam assesses. Keep single-layer, multilayer, the PyTorch lab and the "worth it" reasoning;
  drop the CNN arithmetic and the 4-slide Sequences section (which the objectives already only
  promise to "**Outline**").

That trade is defensible on the evidence, but it is a real loss of two half-sessions and it is
your call, not mine.

**Cost.** 25-35 h for the deck at the density of the existing ones (they average ~90 pages and
are very dense), 6-10 h for the notebook, 3 h for a runsheet, 2 h for exam questions.

### A2 — Three integrative exercises, for Ch 6, Ch 8 and Ch 10 · ~8 h · displaces one short exercise each

`chapter_06`, `chapter_08` and `chapter_10` contain **zero** `[Integrative]` exercises — verified
both by grep and in `slide_index.md`'s exercise tables. Ch 1, 2, 3, 4, 5, 7 and 13 all have at
least one. The final exam is "weighted to Ch 7/8/10/13", so two of its four focus chapters have
no exercise that asks a student to combine anything. And Problem 7 of the final is "Cumulative
essentials (Ch 2-6)" — a cumulative problem type that nothing in Ch 6 rehearses.

Model them on `chapter_04`'s Extended Exercise 4.4 ("Choosing a classifier: three cases"), which
is the best exercise in the repository for this audience: a stated business situation, and the
student has to pick and justify. Ch 6's should be "given this design (n, p, collinearity,
interpretability requirement), choose subset selection / ridge / lasso and defend it"; Ch 8's
"single tree vs forest vs boosting under a governance constraint" — `chapter_08.tex:402` already
has the industry box for it; Ch 10's "is deep learning worth it here", which is the unassessed
objective.

### A3 — Put the five 60-minute short exams in the calendar · ~2 h · displaces nothing

`Mock_Exams/Short_Exams_60min/` holds five complete parallel papers (A-E, 3 × 20 pts, increasing
difficulty, per-problem grading keys, review decks). `semester_plan.md` mentions them once, in a
*build* note, and its "Assessment rhythm" table lists only the three long exams. `docs/exams.md`
describes them but not when to use them. No runsheet references them.

This is the answer to "what is there for students who fall behind", and it is invisible. Their
coverage maps neatly onto the weeks between the long exams (A: Ch 1-4 · B: Ch 2, 3, 5 · C: Ch 3,
4, 6 · D: Ch 2, 5, 8 · E: Ch 0, 7, 13) and Exam E's P1 ("Reading `describe()` output, SE vs SD")
is the only place the precourse material is ever assessed. Add a column to the semester-plan
table and one line to each runsheet's homework section.

### A4 — Bring back the "worked example" box in the second half · ~10 h · displaces nothing

The `numexample` box ("Worked example", orange) is used 7× in `chapter_00`, 7× in `chapter_03`,
4× in `chapter_02`, 3× in `chapter_04` — and **0× in `chapter_06`, `chapter_07`, `chapter_08` and
`chapter_10`**, 1× in `chapter_05` and `chapter_13`. One of your seven callout types silently
stops existing halfway through the semester. The material is still numeric — `chapter_06` has
$C_p$/BIC arithmetic, `chapter_08` has Gini computations — but it now appears only inside
exercises and solutions, where a student meets it as a test rather than as a demonstration.
Two or three worked examples per second-half deck (~10 h) would restore the see-one-then-do-one
rhythm that makes Ch 3 work.

---

## 4. On the callout-box system (Q7), briefly

Counts per deck, from the `.tex` sources:

| | 00 | 00b | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 10 | 13 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `takeaway` | 47 | 14 | 19 | 27 | 36 | 29 | 19 | 21 | 22 | 20 | 21 | 18 |
| `numexample` | 7 | 4 | 2 | 4 | 7 | 3 | 1 | **0** | **0** | **0** | **0** | 1 |
| `readme` | 16 | **1** | 11 | 12 | 18 | 13 | 8 | 8 | 13 | 10 | 11 | 10 |
| `alertblock` | 7 | 5 | 3 | 3 | 13 | 5 | 5 | 6 | 4 | 3 | **1** | 2 |
| `industry` | 6 | 6 | 8 | 7 | 8 | 7 | 7 | 7 | 7 | 7 | 10 | 6 |
| `labnote` | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Four observations:

- **`takeaway` is over-used and therefore under-read.** 47 boxes across `chapter_00`'s 122
  pages means 4 in every 10 slides carries a green "the thing to remember" box. `before_class.md:36-38`
  calls the colours "a contract with the students — green is the thing to remember". A contract
  invoked 47 times in one session is not a contract. `chapter_13` (18 across 69 pages) is about
  right; `chapter_00` and `chapter_03` should shed a third of theirs.
- **There is no "common mistake" box, and there should be.** There are 133 instances of
  `\textit{Common mistake:}` across the twelve decks (18 in `chapter_03` alone), and every one is
  plain italic text inside a `solutionbox` or `readme` — e.g. `chapter_03.tex:733`, `:929`,
  `:1119`, `:1217`. This is some of the most valuable content in the decks and it has no visual
  identity, cannot be found by flipping, and cannot be extracted into a revision sheet. Defining
  a `\newtcolorbox{mistake}` (red-brown, ~1 h) and converting the 133 instances (~6 h,
  mechanical) would make the single richest layer of the material visible. This is my answer to
  "is a slide type missing": not a slide type — a *box* type, for content you have already
  written.
- **`labnote` is defined but not used as a pacing device.** Exactly one cyan box per 80-page
  deck. `slide_index.md` reports "Notebook cues: 1 in this deck" for ten of the twelve. The
  notebook is therefore a handoff at the end rather than a companion throughout — yet
  `semester_plan.md:84` says "The labs are the part that matters." Three or four cues per deck,
  placed where the notebook actually reproduces the figure on screen, costs ~4 h and matches what
  the runsheets already tell the lecturer to do ("cut to the notebook here and rerun the
  validation cell with random_state = 1, 2, 3", `lecture_05.md:12`).
- **`readme` ("How to read this") is excellent and unevenly deployed.** 18 in `chapter_03`, 13 in
  `chapter_07` — and **1** in `chapter_00b`, the deck whose first section is literally "Reading
  mathematical notation". That deck has the slack (§R4) and the strongest claim on the box.
  `alertblock` at 1 in `chapter_10` is also thin for a chapter full of ways to waste GPU money.

`industry` is well-calibrated at 6-10 per deck and needs no work. `exercise`/`solutionbox`/
`longexercise` are doing their job.

---

## 5. Examined and judged sound — no work needed

- **The three two-session split points** (`semester_plan.md:42-46`). Ch 2 at p. 42 correctly puts
  the whole framing before the break and the whole error analysis after. Ch 3 at p. 76 splits
  76/68 pages, estimation-and-inference against everything-that-complicates-it. Ch 4 at p. 46
  splits 46/66 and lands exactly where LDA begins (I checked the subsection boundaries: LDA
  p. 46, QDA p. 54, naive Bayes p. 61). All three are page-balanced and conceptually clean; I
  looked for a better break in each and did not find one. The rationale column in the semester
  plan is not decoration — it is right.
- **The appendix mechanism.** Twelve "Appendix — what is in here, and why" frames, each naming
  the main-flow substitute for the material it holds. I stress-tested the three cases most likely
  to be quiet burials — `chapter_06`'s lasso geometry, `chapter_07`'s truncated-power basis,
  `chapter_10`'s backpropagation — and in all three the main flow carries what the objectives and
  the exams need, exactly as the appendix note claims. `chapter_06.tex:1486` even labels its own
  appendix slide a duplicate. The only genuine misalignment is `chapter_04`'s Poisson material,
  and the fault there is in the objective (R2), not the appendix.
- **`slide_index.md` and the build.** Generated from the compiled PDFs by `make_index.py` with
  per-section page ranges, proportional time budgets and every exercise's prompt/solution page;
  `check_decks.py` reads the LaTeX logs for overfull vboxes above 12 pt because "below it the eye
  cannot see the overflow". Incremental, cheap, correct. The gap is that neither tool validates
  the runsheets (R1).
- **Exam construction.** Single source for paper and solutions so they cannot diverge, independent
  sub-parts, points ≈ minutes, three parallel finals for seating variants, per-problem grading
  keys with follow-through rules, and every problem tagged with the lecture slides it draws on.
- **The taught labs' shape.** Code tour → worked solutions to the deck's [Python] exercises →
  four unsolved exercises. `chapter_08_lab.ipynb` cells 24 and 30 even discuss *why* boosting
  beats the forest on this particular split rather than just printing the MSE. Colab badge on
  every notebook, and a three-way data fallback (ISLP → bundled CSV → the book's site).
- **Notation discipline.** Every deck opens with a "Notation in this chapter" table, and
  `chapter_01` p. 40 carries $n$, $p$, the design matrix, hats and the tr/te subscripts on one
  slide that later chapters can assume. For a cohort meeting $\sum_i x_{ij}$ seriously for the
  first time, this is the right investment.
- **The "Decision rules of thumb" closer**, present in all ten chapter decks. It is the slide a
  practitioner keeps, and it is in every deck.
- **`before_class.md`.** Fifty-five lines, no filler, and it anticipates the failure modes that
  actually happen — cold kernel, single screen, no wifi, a `\begin{frame}` that overflows in the
  room. I would not change a line.

---

## 6. Summary of effort

| | Recommendation | Hours | Displaces |
|---|---|--:|---|
| R1 | Fix `lecture_01`/`lecture_02`; add runsheet validator | 5 | — |
| R2 | Reconcile eleven objectives slides with decks + exams | 5 | — |
| R3 | Self-check pointers; hideable solutions; three exercise gaps | 8-11 | build simplicity |
| R4 | Rebalance precourse; teach Python once | 10 | ch00 Python §; ch01 pp. 48-50; ch02 pp. 90-91 |
| R5 | Twelve retrieval openers; Lecture 1 break | 5 | ~2 min/session of closing revision |
| R6 | Relabel or rebuild the three self-study notebooks | 2 or 15 | — |
| A1 | Taught Ch 12 half-session (PCA + clustering) | 25-35 | half of Ch 13, half of Ch 10 |
| A2 | Integrative exercises for Ch 6, 8, 10 | 8 | one short exercise each |
| A3 | Schedule the five 60-min exams | 2 | — |
| A4 | Worked-example boxes in the second-half decks | 10 | — |
| — | A `mistake` box + convert 133 instances (§4) | 7 | — |

If only three things get done: **R1** (a wrong cut list is worse than none), **R2** (the
objectives are the students' revision contract and four of them are false), and **R5** (the
course has no retrieval practice at all, and Lecture 1 has no break).

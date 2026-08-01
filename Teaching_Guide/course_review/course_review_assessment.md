# Quantitative Research Methods — assessment review

**For:** Prof. Dr. Christoph Weisser, HSBI
**Scope:** assessment only — the eight papers in `Mock_Exams/`, their solutions and review decks, the 127 in-deck exercises, the 67 student exercises in `Chapters/`, and how `Teaching_Guide/semester_plan.md`, `Teaching_Guide/runsheets/` and `docs/exams.md` position all of it.
**Method:** read-only. Nothing in the repository was modified.

### Two caveats on the state of the files

1. `Mock_Exams/` was being edited while I read it. `final_mock_exam_a.tex` and `solutions_slides_a.tex` had been touched shortly before I started; all main-paper `.tex` files were touched again at 14:39–14:40 during my read. **Where I flag an inconsistency between a paper and its solutions deck, treat it as mid-edit rather than as a defect** — I say so explicitly each time.
2. Every paper in the repository is labelled *mock*. `docs/course.md:51–52` calls them self-test material at the natural checkpoints. **Nothing anywhere in the repository states what the summative instrument actually is** — no ECTS weighting, no grade split, no statement that the real HSBI paper is isomorphic to these. My remarks about "the assessment" therefore describe the rehearsal system and infer the shape of the real paper from it. If the real paper differs materially, several recommendations below change priority.
3. Files outside `Mock_Exams/` were also changing during the review — `git status` showed live modifications to `Teaching_Guide/semester_plan.md`, `docs/exams.md`, `Chapters/chapter_03/chapter_03.tex`, `Chapters/chapter_03/chapter_03_lab.ipynb`, `README.md` and the `Makefile`. I re-verified every line anchor in this document against the files as they stood at the end of the review and corrected two that had drifted. **Line numbers may drift again; the quoted text and the problem/exercise numbers will not.** Where precision matters, search on the quoted string rather than the line.

---

## 1. Honest assessment of the current design

**The engineering is better than the assessment design.** Single-source `\withsolutions` toggles, programmatically verified numerics, three genuinely parallel final variants, per-problem slide cross-references, and runsheets that name which exercise rehearses which exam problem — that infrastructure is unusually good, and I say more about it in §4. The problem is what the infrastructure is used to build.

**The papers are a procedure-rehearsal instrument, and the runsheets say so out loud.** This is not inference. `Teaching_Guide/runsheets/lecture_13.md:14`: "This exact drill is Problem 6(b) of the final mock exam with barely changed numbers." `lecture_06.md:16`: "parts (1) and (2) are verbatim Mock Exam 2 problem 6(c)." `lecture_06.md:39`: "Parts (1) and (2) are Mock Exam 2 problem 6(b) and 6(d) almost word for word." `lecture_13.md:99` gives you the closing line to say to the room: "Problem 6 is exactly the three procedures you did by hand today, so go home and redo Exercises 13.2, 13.3 and 13.5." A student who memorises the twelve or so drilled procedures passes without ever having chosen a method, read an unfamiliar output, or defended a recommendation.

**By marks, the papers are arithmetic.** My classification of all 137 sub-parts across the eight papers (599 marks; primary class per sub-part, conservative — I coded "compute five metrics from a supplied confusion matrix" as hand-computation, not interpretation):

| | RECALL | HAND-COMP | OUTPUT-INTERP | JUDGEMENT | OPEN |
|---|---|---|---|---|---|
| Mock Exam 1 (90) | 26 (28.9%) | 41 (45.6%) | 17 (18.9%) | 6 (6.7%) | 0 |
| Mock Exam 2 (90) | 38 (42.2%) | 36 (40.0%) | 0 | 13 (14.4%) | 3 (3.3%) |
| Final, base (120) | 38 (31.7%) | 59 (49.2%) | 8 (6.7%) | 15 (12.5%) | 0 |
| **three main papers (300)** | **102 (34.0%)** | **136 (45.3%)** | **25 (8.3%)** | **34 (11.3%)** | **3 (1.0%)** |
| five short exams (299) | 39 (13.0%) | 192 (64.2%) | 27 (9.0%) | 41 (13.7%) | 0 |
| **all eight papers (599)** | **141 (23.5%)** | **328 (54.8%)** | **52 (8.7%)** | **75 (12.5%)** | **3 (0.5%)** |

A softer boundary gives the same verdict. Counting every mark whose stem rests on *supplied* printed output or a results table — the most generous possible reading of "interpretation" — gives 160 of 600 marks, 26.7%. But that measure exposes the real problem: it is **6.7% on the final paper** (8 of 120 marks: P4(c) reading a `GradientBoostingRegressor` call, P7(b) reading a `Logit` table). The highest-stakes paper, the one covering chapters 7/8/10/13, is the one that asks least often what a number means.

**Zero figures.** `grep -c 'includegraphics\|tikzpicture\|pgfplots'` over all eight papers returns **0**. Not one paper asks a student to read a plot. The decks are figure-rich — `chapter_03.tex` alone has 16 — and three of the best exercises in the course are plot-reading exercises (`chapter_02.tex:1122` read a flexibility-vs-error curve; `chapter_03.tex:2154` four residual patterns, name the problem and the remedy; `chapter_03.tex:2483` diagnose all four classical problems from four plots plus VIFs). The papers convert these into recall. The clearest instance is `Mock_Exams/Exam_1_after_Lecture_04/mock_exam_1.tex:480–482`, which *describes* the plot — "shows a clear U-shape (positive residuals for small and large fitted values, negative in between)" — and then asks what it indicates. The stem contains the diagnosis. The candidate supplies the label.

**No Python is ever written or debugged.** No question in any paper asks for code. Every `\texttt{scikit-learn}` and `\texttt{statsmodels}` mention is a read of a constructor call or a stylised table. Meanwhile `semester_plan.md:88` states: "The labs are the part that matters — a student who runs every notebook will pass; one who only reads slides will not." Nothing in the assessment tests lab work, and none of the 67 student exercises across the 13 notebooks has a submission mechanism, rubric, point value, `assert`, or nbgrader metadata. The stated centre of gravity of the course carries zero assessment weight. `chapter_00b.tex:852` (Exercise 0b.6 — find the off-by-one and the train-on-train bug in a given CV loop) is the single most useful question type in the whole repository for this cohort, and it is never examined.

**The output that is shown is stylised, not real.** `docs/exams.md:41–43` says the papers "show real output (a `statsmodels` summary, a confusion matrix, a CV curve)". They show four-row extracts with round numbers: `t = 42.000`, `coef = 2.3500`, `std = 12.0`, a confusion matrix of 855/45/40/60. No paper — and no deck — contains `Df Residuals`, `Omnibus`, `Durbin-Watson`, or the `[0.025 0.975]` columns. A student whose entire exposure is a tidy four-row table will not recognise a real `summary()` in an internship.

**Marking documentation is split down the middle, and the wrong half is documented.** The five 60-minute papers each carry three `gradingbox` grading keys with marks allocated inside each sub-part (`mock_exam_A.tex:141–148, 214–220, 294–300`) and a one-slide "Marking at a glance" table (`solutions_slides_A.tex:271`). The three main papers — 300 marks, the ones that mirror the real exam — carry **no grading key at all, no within-part mark allocation, and no marking table**. Their solutions decks contain only four ECF notes, one per problem, on 4 of the 18 problems (`solutions_slides_1.tex:210` P2, `:434` P4; `solutions_slides_2.tex:572` P5; `solutions_slides_final.tex:290` P3). A second marker handed `Mock_Exam_1_Solutions.pdf` gets a model script and a per-part total. Nothing tells them what the 6 marks of P4(a) are 6 marks *of*, or what a candidate who writes the correct formula and fumbles the arithmetic scores.

**The sub-part independence mechanism is being replaced, and the replacement is better.** Independence was previously bought by restating earlier answers in later stems — Exam 1 P2(d) still says "*(Recall the expected test MSEs from part (b): 3.50 for A, 2.60 for B and 4.61 for C.)*" at `mock_exam_1.tex:186`, and P4(b)/(c)/(d)/(e)/(f) at lines 341/344/346/355 still hand back `ŷ = 2.000 + 3.000x`, the residual vector, RSE = 1.155 and RSS = 4.000. The four ECF notes already assert the opposite ("The question paper no longer restates …"), so paper and deck currently disagree. **This is the live edit, not a defect** — the direction is right and §3.4 argues it should go deck-wide.

---

## 2. Constructive alignment: the map

Every deck states objectives (`chapter_00.tex:171`, `00b:177`, `01:151`, `02:157`, `03:198`, `04:147`, `05:148`, `06:146`, `07:141`, `08:141`, `10:136`, `13:137`). Here is what is not assessed.

**Objectives with no examination anywhere in the eight papers.** Verified by grep across all paper stems and solutions:

| Deck | Stated objective | Status |
|---|---|---|
| 03 | "**Distinguish** a confidence interval for the regression line from a prediction interval for an individual outcome" | *prediction interval*: 0 hits in any paper. Taught and drilled (`chapter_03.tex:1126`, Ext 3.L1 computes one). |
| 03 | "**Diagnose** the four classical regression problems — nonlinearity, heteroscedasticity, outliers / leverage, collinearity" | Only nonlinearity and collinearity, both in E1 P5(f). *leverage*, *outlier*: 0 hits. |
| 04 | "**Derive** linear and quadratic discriminant analysis from Bayes' theorem" | E2 P2(a) asks only to *state* the covariance assumption. No discriminant score is ever computed; no LDA boundary is ever derived. Drilled at `chapter_04.tex:1105` (Ex 4.5) and `:2392` (Ext 4.2). |
| 04 | "**Generalise** to multinomial responses and Poisson regression through the GLM framework" | *Poisson*: 0 hits in any paper. |
| 05 | "**Avoid** the common resampling pitfalls (information leakage, naive time-series folds, group-ignoring splits)" | Leakage examined **only** in short exam D P1(c)(d) — never in any of the three main papers. Time-series folds and group splits: 0 hits anywhere. |
| 06 | "**Apply** best-subset and stepwise selection" | *stepwise*: 0 hits. E2 P5 consumes best-subset output without performing a search. |
| 06 | "**Use** principal-components and partial-least-squares regression" | *principal component*, *PLS*: 0 hits in any stem. Deliberate — `lecture_06.md:17` says the section "is not on Mock Exam 2". |
| 07 | "**Fit** polynomial and step-function regressions"; "**Construct** … local regressions" | *step function*, *local regression* / LOESS: 0 hits. Drilled at `chapter_07.tex:357` (Ex 7.2). |
| 08 | "**Choose** between trees, random forests, and boosting for a given tabular problem" | Only as one of four items in the FIN P7(e) matching grid. BART (in the deck's own "Eight things to remember"): 0 hits. |
| 10 | "**Train** a small network with stochastic gradient descent + backpropagation" | *backprop*, *stochastic gradient*, *dropout*, *double descent*, *recurrent*: 0 hits. FIN P5 is forward pass only. |
| 10 | "**Outline** recurrent networks and the basic transformer idea"; "**Reason** about when deep learning is worth it" | Neither examined. |
| 13 | "**Use** resampling-based *p*-values when the null distribution is hard to derive" | *permutation*: 0 hits. Deliberate — `lecture_13.md:31`: "None of it is on the final mock exam." |
| 13 | "**Avoid** the post-selection-inference and *p*-hacking pitfalls" | *p-hacking*, post-selection inference: 0 hits. |
| 00 | "**Differentiate** a loss function and take a gradient-descent step"; "**Manipulate** vectors and matrices … the matrix form of the estimator" | 0 hits. |
| 00b | "**Write down** a likelihood, take its log, explain what maximum likelihood chooses"; "**Count** models and explain why 2^p makes exhaustive search hopeless"; "explain what a coefficient means when the response is logged" | 0 hits. *elasticity* appears in no paper, despite `chapter_00b.tex:228–244` building an entire industry case around it. |
| 01 + 13 | causation vs. association; selection bias; fairness | *causal*, *ethic*, *fair*, *selection bias*: **0 hits in any of the eight papers**, though taught in `chapter_01`, `chapter_03`, `chapter_08`, `chapter_13`, and named as one of the "Five things to remember" at `chapter_00.tex:2341` ("Association is not causation… that question is why multiple regression exists"). |

Some of these gaps are documented and deliberate (PCR/PLS, resampling *p*-values). I would still note the second-order effect: `lecture_06.md:17` tells you to tell the room a section is not on the exam, which in a business-school cohort reliably means it is not learned.

**Examined material with no matching stated objective.** No paper examines anything untaught — everything traces to a deck frame. But three items are examined without an objective behind them:

- **FIN P5(c)+(d), 6 of the 20 chapter-10 marks**: parameter counting and the `(W − F + 2P)/S + 1` convolution-output formula. In the deck (`chapter_10.tex:658`, `:847`, formula at `:853`), but serving none of the five stated ch-10 objectives.
- **FIN P1(a)+(b), 8 of 16 marks**: spline degree-of-freedom counting. The ch-7 objective is "articulate the boundary problem of cubic splines and the fix offered by natural splines"; the paper asks for the arithmetic of `df = K + 4` and `df = K` instead of the articulation. In the deck at `chapter_07.tex:562`, `:602`.
- **Short C P3(b)+(c), 10 of 60 marks**: ridge and lasso closed forms under an orthonormal design. This is **appendix material** — `chapter_06.tex` puts `\appendix` at line 1474 and Extended Exercise 6.2 at 1589, and the deck's own appendix note calls it "the cleanest proof in the chapter — and the hardest algebra". `semester_plan.md:9–13` states that appendix pages are "extra material to assign, not to teach". A sixth of short exam C tests material the semester plan says is not taught in the room.

**Weighting against teaching time** (main-paper marks ÷ sessions, from `semester_plan.md:17–32`):

| Chapter | Sessions | Main-paper marks | Marks / session |
|---|---|---|---|
| 8 (trees) | 1 | 36 | **36** |
| 6 (selection) | 1 | 29 | 29 |
| 2 (stat. learning) | 1.5 | ~43 | ~29 |
| 4 (classification) | 2 | 49 | 24.5 |
| 3 (linear regression) | 2 | 48 | 24 |
| 7 (beyond linearity) | 1 | 24 | 24 |
| 5 (resampling) | 1 | 22 | 22 |
| 10 (deep learning) | 1 | 20 | 20 |
| 13 (multiple testing) | 1 | 20 | 20 |
| 1 (introduction) | 0.5 | ~8 | ~16 |
| 00 / 00b (precourse) | 2 (optional) | **0** | 0 |

Chapter 8 is over-weighted by roughly 1.8× relative to chapters 10 and 13, all three taught in one session each. Chapters 10 and 13 are the *last two sessions* and the two decks with no "N things to remember" and no self-check frame (`chapter_10.tex:1377`, `chapter_13.tex:1020`) — the thinnest closure and the lightest examination, at the point in the semester where attention is scarcest. The precourse decks appear only in short exams A P1, C P1 and E P1 (three of fifteen problems, ~54 of 300 short-exam marks) and nowhere in the main papers.

---

## 3. Prioritised recommendations

### 3.1 Convert one problem per main paper from arithmetic to output interpretation — using the deck exercises you already own
**Effort:** one afternoon per paper. **Displaces:** 8–12 marks of hand arithmetic per paper.

This is the highest-value change and it is nearly free, because the source material exists and is already drilled in class.

- **Exam 1.** P4 is 24 marks — 22 of them pure arithmetic on five points, and 12 of those (parts b, c, e) are re-deriving quantities the stem hands you anyway. Cut P4 to 12 marks (keep a+d: estimate the line, then the *t*-test and CI, which is where the statistical content lives). Spend the freed 12 marks on `chapter_03.tex:2154` (Exercise 3.10 — four residual plots, name the problem and the remedy) **with the four plots actually printed**. You already generate figures for the decks; the same `\includegraphics` works in an `article` paper.
- **Exam 2.** P2 is 12 marks of pure LDA/QDA/naive-Bayes recall — four "state the assumption" parts. Replace 6 of them with `chapter_04.tex:1476` (Extended Exercise 4.4 — choose among logistic/LDA/QDA/NB/KNN for three described datasets, plus the runner-up and why). Same content, forces the choice.
- **Final.** This paper needs it most (8 of 120 marks currently rest on supplied output). P5 is 20 marks of neural-network arithmetic; P5(c)+(d), 6 marks, examine formulas no ch-10 objective mentions. Replace them with `chapter_10.tex:1285` (Extended Exercise 10.3, already in the deck): print the train/validation loss curve, ask where to stop and why, and what `weight_decay` did. That single swap examines three ch-10 objectives that are currently unexamined and one that is over-examined.

**What is lost, honestly.** Hand computation is not worthless here, and I would not strip it out. Computing `SE(β̂₁) = RSE/√Sxx` once by hand is what makes a standard error a quantity rather than a column heading; the Holm and BH chains at FIN P6(b)(c) are worth their 13 marks because the step-down/step-up scan direction is the entire conceptual content and students genuinely invert it. What is *not* worth marks is arithmetic that re-derives a quantity the stem already supplies: Exam 1 P4(b) computes five residuals from a line the stem prints, P4(c) sums five squares the stem prints, P4(e) computes TSS from five numbers. That is 12 marks measuring whether the candidate can subtract. **The test I would apply: keep the hand computation where getting it wrong reveals a conceptual error, cut it where getting it wrong reveals only a slip.** By that test, Exam 1 P4(b)(c)(e) and FIN P5(c)(d) go; FIN P6(b)(c), E1 P4(d), FIN P3(a) and short D P3(a)(b) stay.

### 3.2 Put a grading key in the three main papers
**Effort:** 2–3 hours per paper — the `gradingbox` environment and its five-year-old conventions already exist. **Displaces:** nothing.

Copy `mock_exam_A.tex:31–32` (the `gradingbox` definition) into `mock_exam_1.tex`, `mock_exam_2.tex` and the four final variants, and write one box per problem in the style already established at `mock_exam_A.tex:214–220`:

> (a) 3 P slope formula and value; 1 P for `S_xy/S_xx` structure even if miscomputed; 3 P intercept via `ȳ − β̂₁x̄`; 1 P fitted line written out.

That is exactly the granularity a second marker needs, and note what the second clause does: it awards a method mark for correct structure with wrong arithmetic. Add a "Marking at a glance" frame (`solutions_slides_A.tex:271`) to each main solutions deck. **This is the single change most likely to matter if you ever hand marking to an assistant or face a grade appeal**, and it is the one gap where the fix is pure transcription from work you have already done.

### 3.3 Make the labs count for something
**Effort:** moderate — see §4.1 for the concrete instrument. **Displaces:** one of the two 90-minute mock exams as a *classroom event*, not as material.

`semester_plan.md:88` says the labs are what matters and that lab-runners pass. The assessment contradicts this: 67 student exercises, no submission, no rubric, no marks, and no exam question requiring code. This is also where the AI-era exposure actually sits (§3.5). Until something rewards lab work, the rational student skips the notebooks and drills the twelve exam procedures — and the runsheets tell them exactly which twelve.

### 3.4 Take the ECF convention deck-wide, and finish the leakage removal consistently
**Effort:** small, and partly underway. **Displaces:** nothing.

The four ECF notes are well written — `solutions_slides_1.tex:434` in particular ("Mark every one of them on *method*… Each numerical slip is penalised once only, in the part where it was made… compare the *steps*, not only the numbers") is a correct and complete statement of the convention. Three things follow:

1. **Make it a paper-level instruction, not a per-problem note.** Put one sentence in the `Instructions` block of every paper (`mock_exam_1.tex:75–79`), next to the existing rounding tolerance: *"Later parts may be answered from your own earlier results; a correct method applied to your own incorrect value earns full credit for the later part."* Then candidates know the rule, not just markers. Note that the short exams already do half of this at `mock_exam_A.tex:78` ("the sub-parts within each problem are largely independent, so a wrong (a) does not spoil (b)") — but that promise is currently kept by *restating the answer*, and once the restatements go, the promise needs the ECF sentence to remain true.
2. **Cover all 18 problems, not 4.** Any problem with a chained sub-part needs the note: Exam 1 P2 and P4 (done), Exam 2 P1 (a→b→c chain on the same logistic fit), P3 (a→b), P5 (done), P6(e); FIN P3 (done), P4(a) (ii and iii chain), P5(b), P6(b)→(c), and the corresponding parts of variants a/b/c.
3. **Keep paper and deck in step.** Right now `mock_exam_1.tex:341/344/346/355` still restates what `solutions_slides_1.tex:434` says it no longer restates. That is the live edit; the point is to sweep all six main-paper sources together rather than problem by problem, or the ECF notes will keep describing a paper that has not caught up.

### 3.5 Raise the AI floor where it is actually low — the labs, not the exams
**Effort:** small, once §3.3 exists. **Displaces:** nothing.

Be clear about where the exposure is. The papers are invigilated and closed-book — "non-programmable calculator; one handwritten A4 sheet of notes (both sides)" (`mock_exam_1.tex:55`) — so a language model cannot sit them. Ranked by intrinsic resistance:

- **Least resistant** (a model answers these verbatim, and they are worth 141 of 599 marks): every RECALL sub-part. Exam 2 P2 (12 marks of LDA/QDA/NB assumptions), FIN P1 (16 marks of spline bookwork), FIN P2 (8 marks of GAM bookwork). These are also the sub-parts most exactly reproduced from the deck. As unsupervised homework they are worthless; under invigilation they are merely low-value.
- **Middling**: the hand computations. A model does them flawlessly, but under invigilation that is irrelevant — the risk is that students *prepare* with a model and never do the arithmetic themselves, which the ECF convention (§3.4) mildly discourages by rewarding visible method.
- **Most resistant, and mostly absent**: anything anchored to an artefact the student produced. `chapter_00b.tex:852` (find the bug in *this* CV loop) is resistant in a lab context because the answer must match the code in front of them. `chapter_05.tex:1265` (Extended Exercise 5.3 — explain the leak, design the correct procedure, sketch nested CV) resists because it wants a design, not a fact. A five-minute oral on the student's own submitted analysis (§4.2) is the only thing here that is genuinely resistant.

**What raises the floor without making the assessment worse:** make the graded coursework (§4.1) require the student's *own* dataset choice and their *own* run, and attach a short oral (§4.2). Do not respond by adding more closed-book arithmetic — that raises the floor by lowering the ceiling.

### 3.6 Rebalance chapters 10 and 13 against chapter 8
**Effort:** small. **Displaces:** ~8 marks of chapter-8 arithmetic on the final.

FIN P3 (20 marks) + P4 (16 marks) = 36 marks for one session of trees, against 20 each for deep learning and multiple testing. FIN P3(a) is 8 marks for computing two RSS values by hand and P3(c) is 6 more for one Gini and one entropy. Cut P3 to 12 (a at 6, c at 4, d at 2) and move the 8 marks to whichever of chapters 10 or 13 you would rather strengthen — `chapter_13.tex:836` (Extended Exercise 13.2, FWER vs FDR for a 4-endpoint confirmatory trial against a 20,000-gene screen, with `E[V] = m₀α`) is the strongest unexamined judgement exercise in the deck set and would give chapter 13 a second judgement question instead of one 3-mark part.

---

## 4. Additions worth considering

These are genuinely new instruments, kept separate because they cost more than the recommendations above and because at least one of them requires an examination-regulations conversation, not just a LaTeX edit.

### 4.1 An applied project — the biggest single gap
**Effort:** 2–3 days to author, plus marking load. **Displaces:** Mock Exam 2 as a classroom event (keep the paper as revision material), and ~20% of the summative weight if that is yours to set.

There is no coursework project, case study, group assignment, presentation, peer review, take-home analysis, reproducible-report submission or oral anywhere in the repository. For a *Fachhochschule* — an institution whose entire premise is applied practice — a quantitative methods course assessed exclusively by closed-book written arithmetic is the finding I would most want to defend to a programme accreditor, and I do not think it can be defended on the current evidence.

The good news: the specification is already written, twice, in your own decks.

- `chapter_00.tex:2081` — **Extended Exercise 0.4**: "review a loyalty-programme consultancy report end to end (skew, CI, *p* vs R², r = 0.05, causality, plots)". That is a marking rubric in embryo.
- `chapter_01.tex:1071` — **Extended Exercise 1.1**: the anatomy of a 20,000-record loan-default study — response and predictors, *n* and *p*, task type, prediction vs inference, the meaning of ε, "sketch workflow + model family for the regulator". That is a project brief.

**Concretely, what I would build.** A 2,500-word reproducible analysis on a dataset the student selects from `ALL CSV FILES - 2nd Edition/` (25 datasets are already in the repo, so no data-sourcing overhead), submitted as a notebook plus a four-page memo addressed to a named business stakeholder. Required structure, mapped to objectives that the written papers currently miss:

1. **The question, and whether it is prediction or inference** (ch-1 objective, examined only as 4 marks of recall in E1 P1(a)).
2. **An honest evaluation protocol**, stated before any model is fitted: the split, the folds, and one sentence on the leakage risk specific to *this* dataset (ch-5 objective "avoid the common resampling pitfalls" — currently examined only in short exam D).
3. **A linear or logistic baseline, interpreted with units and the "holding others fixed" clause**, plus a confidence interval *and* a prediction interval with the difference stated (ch-3 objective, `prediction interval`: 0 hits in the current papers).
4. **One flexible alternative** (forest or boosting or a spline/GAM), compared to the baseline on held-out data, with a bias–variance sentence on why it won or lost (ch-8 objective "choose between trees, random forests and boosting for a given tabular problem").
5. **Diagnostics with the plots shown** — residual-vs-fitted, and either a VIF table or a ROC curve, whichever the response type demands (ch-3 objective: leverage and heteroscedasticity currently unexamined).
6. **A recommendation, and its limits** — one paragraph on what a stakeholder should *do*, and one on why the association may not be causal (the `chapter_00.tex:2341` "five things" item that appears in no paper).
7. **Reproducibility**: seeded, runs top-to-bottom on Colab.

Mark it with the same `gradingbox` granularity as short exam A — say 100 points across the seven headings, with the honest-evaluation and limits sections weighted heaviest, because those are the two that a language model writes blandly and a student who ran the analysis writes specifically.

**What it should replace.** Not the final paper — a written invigilated component should survive, both for integrity and because the Holm/BH and *t*-test computations genuinely belong there. Replace **Mock Exam 2 as a classroom event**: it sits after lecture 8, exactly where a project needs to start if it is to be finished by lecture 12, and it is the paper whose content (chapters 4–6) the project would exercise most directly. Keep `Mock_Exam_2.pdf` in circulation as revision material; the marks move to the project.

### 4.2 A five-minute oral on the submitted project
**Effort:** 5 minutes × cohort size, plus a three-question script. **Displaces:** nothing; it is an integrity mechanism, not a content one.

Three questions, asked from the student's own submitted notebook: *why this split?*, *why did the flexible model win or lose?*, *what would change your recommendation?* This is the only instrument in this review that is robustly AI-resistant, and it costs almost nothing per student because the artefact is already in front of you. If examination regulations make a graded oral awkward, run it ungraded as a pass/fail authenticity check on the project.

### 4.3 A plot-reading bank
**Effort:** one day. **Displaces:** nothing — it feeds §3.1.

The papers have no figures because there is no reservoir of exam-ready ones. Build eight: two residual-vs-fitted patterns, a flexibility-vs-error pair of curves, a CV-error-vs-λ curve with a visible minimum, a coefficient path showing lasso zeros against ridge shrinkage, a ROC curve with two classifiers crossing, a train/validation loss curve turning up, and one partial-dependence panel from a GAM. All seven concepts are already plotted in the decks; the work is extracting them as standalone PDFs with axis labels and no captions. Once they exist, swapping described plots for shown plots (§3.1) becomes a one-line edit per question.

### 4.4 One authentic `statsmodels` summary, once per paper
**Effort:** an hour. **Displaces:** nothing.

Paste one real `summary()` block — `Df Residuals`, `Omnibus`, `Durbin-Watson`, the `[0.025 0.975]` columns, ragged decimals and all — into each paper, and ask for one coefficient interpretation and one thing the extra rows tell them. Neither the papers nor the decks currently contain a single one. The point is not the extra rows; the point is that recognition transfers and pattern-matching on a four-row table does not.

### 4.5 Peer review of the project, as a one-session exercise
**Effort:** small. **Displaces:** 45 minutes of lecture 11 or 12.

Swap drafts, mark against the same rubric, hand back. Cheap, and it is the fastest way to make the rubric criteria real to students. I would keep it formative — peer marks in the grade create appeals.

---

## 5. Checked and judged sound

So the record shows what was examined and found not to need changing.

- **Single-source construction.** Every paper and its solutions come from one `.tex` with a `\withsolutions` toggle (`mock_exam_1.tex:6–11`, and the same pattern in all eight). Paper and solutions cannot diverge. This is the right architecture and I would not touch it.
- **Numeric correctness.** I recomputed every arithmetic answer I read. All correct: Exam 1 P2 (3.50/2.60/4.61), P3 distances and the K=1/K=3 disagreement, P4 (β̂ = 3.000/2.000, RSE = 1.155, t = 8.216, CI [1.838, 4.162], R² = 0.957), P5 (69.70/58.10, gap −11.60 = β̂₂ + 10β̂₃); Exam 2 P1 (0.119/0.731, x* = 200, e^0.02 = 1.020, e² = 7.389), P3 (0.915/0.600/0.950/0.571/0.050), P4 (1 − (4/5)⁵ = 0.672, SE_B = 0.100), P5 (Cp 5.080/4.600/4.520/4.560, BIC 5.184/4.808/4.833/4.977); Final P1 (K+4 = 8, K = 4), P3 (RSS 40 vs 4, G = 0.375, D = 0.562), P4 (2.416, floor 2.4, m = 5), P5 (f(x) = 9, softmax 0.665/0.245/0.090, loss 0.408, 23 parameters, 32×32), P6 (FWER 0.6415, Bonferroni 2, Holm 3, BH 4). The `docs/exams.md:12` claim that answers were verified programmatically holds up.
- **The three final variants are genuinely parallel.** Same seven problems, same titles, same mark allocation (16/8/20/16/20/20/20), same cognitive profile; only data, contexts and constants change. `final_mock_exam_c.tex` P7 substitutes elastic net and a correlation-0.95 collinearity item for the base paper's true/false and lasso items — a slightly different mix, but both are taught (`chapter_06.tex:910`, `chapter_03.tex:2393`) and the marks match. Usable for seating variants and resits as claimed at `docs/exams.md:29–31`.
- **The short exams are correctly sequenced and are the right instrument for the job.** The `Short_Exams_60min/README.md:9–15` table is accurate: each paper's P3 sits at the frontier chapter (A→ch 4, B→ch 5, C→ch 6, D→ch 8, E→ch 13) while P1 and P2 revisit earlier material, so they are cumulative-to-date rather than single-chapter — which is better than the README's own framing suggests, and better than five isolated chapter tests would be. Difficulty does increase within each paper as claimed. On over-assessment: no, and there is no case to answer, because all eight papers are self-test material (`docs/course.md:51–52`) with no marks attached. **The five short papers are the formative layer and are the healthiest part of the assessment corpus** — they carry the only grading keys, the only "common mistake" boxes (29 across the five decks), the only marking tables, and short exam D P1 is the best-designed problem in the whole set: 20 marks, four parts, every one a judgement, including the two things students actually get wrong in practice (scaling before splitting, and re-drawing the split until the ranking looks stable). If anything I would build more like D, not fewer.
- **Problem-to-slide cross-references.** Every problem names the deck and lecture it draws on (e.g. `mock_exam_2.tex:433`: "Lecture slides: Chapter 6 — Linear Model Selection and Regularisation (Lecture 8)"). Revision is targetable. Kept.
- **Instructions and aids.** Consistent across all eight papers, with a stated rounding tolerance and the "points ≈ minutes" convention (`mock_exam_1.tex:75–79`). The tolerance sentence — "Small deviations caused by carrying rounded intermediate results are accepted" — is exactly right for papers this arithmetic-heavy, and it is the natural place to hang the ECF sentence from §3.4.
- **Review decks.** Task frame, then step-by-step solution frames split where a single frame would overflow (e.g. `solutions_slides_final.tex:303` and `:325` splitting P3(a) into a.1/a.2). Good pedagogy for going through a paper in a 180-minute room.
- **The short-exam "common mistake" boxes.** 29 of them, and they name the real error rather than restating the answer — `solutions_slides_A.tex` on precision vs sensitivity ("Mixing up the denominators… Write the matrix margins down first") and on the odds ratio ("'2.7 times as *likely*' — the factor applies to the **odds**"). These are worth porting to the three main solutions decks, which have none.
- **Assessment material is correctly kept private.** `.gitignore` excludes `Mock_Exams/` and `Teaching_Guide/runsheets/`, with an accurate comment explaining that the runsheets are assessment material because they map exercises to exam problems. `docs/exams.md:3–8` states the same publicly. Correct, and the reasoning is right.
- **In-deck exercise provision.** 127 exercises across 12 decks (87 short, 40 extended), with 18 in appendices, every one with a worked solution frame. The cognitive mix is *better* than the exams': RECALL 20, HAND-COMP 64, OUTPUT-INTERP 27, JUDGEMENT 12, OPEN 4. The teaching material is not the problem. The four open-reasoning exercises (`chapter_00b.tex:916`, `chapter_01.tex:1071`, `chapter_02.tex:1496`, `chapter_05.tex:1265`) and the two report-critique exercises (`chapter_00.tex:1458`, `:2081`) are the best assessment artefacts in the repository, and every one of §3 and §4's recommendations is really just a proposal to examine what you have already written.

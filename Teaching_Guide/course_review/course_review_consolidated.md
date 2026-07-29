# Quantitative Research Methods — consolidated review

Prof. Dr. Christoph Weisser, HSBI · ISLP (James et al. 2023) · 12 × 180 min + 2 precourse decks
Merged from four independent reviews: **[Cur]** curriculum/pedagogy · **[Ass]** assessment ·
**[Lab]** labs/tooling/docs · **[Ind]** industry relevance/employability. All four read-only.

Disagreements are in §6. Uncertain claims are marked in §7 and nowhere laundered into fact. Nothing
here is a number, regulation or citation that is not in one of the four inputs.

---

## 1. The headline

**All four reviews describe the same course, and they like it.** The engineering is genuinely unusual:
exam papers and solutions from a single `\withsolutions` source so they cannot diverge; every
arithmetic answer in eight papers independently recomputed and correct [Ass]; `slide_index.md`
byte-identical to what `make_index.py` regenerates from the committed PDFs, with every quantitative
claim in the README cross-checking [Lab]; fifteen notebooks running top to bottom with zero errors on
both a 2023 and a 2026 dependency stack [Lab]. All four independently single out the runsheets' "What
they will get wrong" sections as hard-won teaching knowledge written down. The content is complete and
correctly pitched, and [Ind] calls `chapter_01.tex:939–944` on as-of joins and leakage the single most
credible sentence in the 1,168 slides.

**The single biggest structural weakness is that nothing the course cares about is graded, and nothing
that is graded requires judgement.** All four converge on this from different directions. By marks the
assessment is arithmetic: 54.8 % of 599 marks across eight papers are hand computation, 12.5 %
judgement, 0.5 % open; on the highest-stakes paper only 8 of 120 marks rest on supplied output. Grep
over all eight papers returns **zero** figures, **zero** code questions, and zero hits for *causal*,
*fair*, *selection bias*, *permutation*, *prediction interval*, *leverage*, *stepwise*, *backprop*
[Ass]. Meanwhile `semester_plan.md:88` says "the labs are the part that matters" and the 67 lab
exercises have no submission, no rubric, no marks and no exam question behind them [Ass] — and every
worked solution ships in the file the student opens, with its answer as an inline comment [Lab]. The
industry layer (25 frames, 86 callouts) carries zero assessment weight and, before this session, zero
minutes in any runsheet: `grep -rn "industr" Teaching_Guide/ docs/ README.md` returned four hits, all
four in the author biography [Ind]. A student who memorises the twelve drilled procedures passes, and
the runsheets name which twelve — `lecture_13.md:14`: "This exact drill is Problem 6(b) of the final
mock exam with barely changed numbers." That is a rational student strategy, and it routes around
everything the course is for.

**The second-order weakness is that the material has outgrown its own metadata.** Eleven objectives
slides promise what the decks and exams do not deliver [Cur, Ass]; `docs/environment.md:44-49`'s
"minimal install" names the package that makes it the maximal install [Lab]; `docs/exams.md:48-52`
gives students a `cd` into a directory that exists in no clone [Lab]; runsheet page references drift
against re-paginated decks [Cur, Lab]; three pages say "request them from the author" and no contact
address exists anywhere, including `CITATION.cff` [Lab]. None of this is curriculum work. It is
consistency maintenance, it is cheap, and it is where the first block of time should go.

---

## 2. Already done or in flight this session — the leftovers only

| Completed | What the reviews still want on top |
|---|---|
| Industry layer added across 12 decks | It is banked in the decks, not the apparatus: name the frames in `semester_plan.md` and add them to the protected list at `:62–64` (today they are neither protected nor on the cut list); fix the `chapter_04` gap (blocks run pp. 1–14 then resume p. 17 — the two industry frames are pp. 15–16, inside the skip); fix the two `lecture_10.md` blocks that both start at p. 45 [Ind] |
| ~60 correctness bugs; exam leakage removed; ECF notes added | Make ECF a **paper-level** line in the `Instructions` block of every paper (`mock_exam_1.tex:75–79`), not a per-problem note; confirm the sweep hit all 18 problems and all six main-paper sources — [Ass] found `mock_exam_1.tex:341/344/346/355` still restating what `solutions_slides_1.tex:434` says is no longer restated [Ass 3.4] |
| Runsheet page references re-mapped | Add the validator or it drifts again on the next deck edit (row 10). Also `lecture_03.md:105` claims the references "are refreshed by `make index`" — false; `make index` regenerates only `slide_index.md` [Lab] |
| Lab leakage/scaling fixes in ch 05/06/08 (in progress) | **One code remainder, newly created by the fix itself: `chapter_06_lab` cells 11 and 15 — see §6.13.** Then the non-code remainder: pin `pygam==0.10.1` and pin `ISLP` (`requirements.txt:13,16`); re-run ch08 and fix cell 30's prose ("three- to four-fold" is now two-fold); commit a `constraints.txt` recording which versions produced the shipped outputs — there is **no record anywhere** today [Lab] |
| `make exams` 6 → 18 PDFs | Building them was never the gap. Scheduling them is (row 2) |

---

## 3. The merged, prioritised recommendation table

Ordered by **value per hour of your time**. **A** = new addition, detailed in §5. Merged rows say what
was reconciled. Detail and further anchors are in §4.

| # | Recommendation | Why it matters | h | Displaces | From |
|:--:|---|---|:--:|---|:--:|
| 1 | **Give `Teaching_Guide/runsheets/` a version history** — private repo, submodule or local branch; keep it off GitHub | ~1,200 lines of the least reproducible material in the project has no history and no backup, while `before_class.md:52-55` asks you to keep editing it every year | **1** | — | Cur |
| 2 | **Put the five 60-min short exams in the semester calendar** — a column in the `semester_plan.md` rhythm table, one line per runsheet | Five parallel papers holding the *only* grading keys, marking tables and 29 "common mistake" boxes in the corpus are mentioned once, in a build note. Coverage already maps to the gaps between long exams (A: Ch 1-4 · B: 2,3,5 · C: 3,4,6 · D: 2,5,8 · E: 0,7,13); E P1 is the only place precourse material is ever assessed. This is the answer to "what is there for students who fall behind", and it is invisible | **2** | — | Cur, Ass |
| 3 | **A Start the Modulhandbuch / examination-regulation change for a graded project.** Paperwork only, now | Longest lead time in this document; must be in place before the semester starts. Ranked here on lead time, not value per hour. [Ind]: "the pedagogy is the easy part" | **2** | — | Ind, Ass |
| 4 | **Add "where you are likely to sit" to all twelve depth cases** — one line naming the model's *consumer*, not its builder | All twelve name an owner and a sign-off, and all twelve are specialist quant roles. One line converts each from "a job you won't have" to "a number you will have to challenge". Cheapest change in the four reviews | **1.5** | — | Ind |
| 5 | **Make Colab the documented day-one path; demote local install to week two.** Badges in one block atop `README.md` and `docs/quickstart.md`, above the venv block; delete the stale "(once the repo is on GitHub…)" line in cell 3 of **13 of 15** notebooks; fix "three datasets NOT in ISLP" → four in all 15 | The install, not the clone, is day one: 151 packages / 244 MB, and `torch` is not optional because ISLP hard-requires it — 241 MB on Windows, 888 MB plus twelve CUDA packages on Linux x86_64. Your students are mostly on Windows. This is editing text you already wrote | **2** | — | Lab |
| 6 | **Add `(p. NN)` to every self-check item in eleven decks** | The natural landing page for a student who has fallen behind is a dead end — six questions, no answers, several pointing at appendix material (`chapter_03` Q1 = Ext Ex 3.L2, p. 147; `chapter_05` Q6 = appendix Ex 5.2; `chapter_08` Q5 = BART, p. 90). `chapter_00`'s own self-check already does the mapping; the fix is in your repository | **3** | — | Cur |
| 7 | **Make the cost-optimal threshold a computed thing, in euros.** One ch04 exercise pair: derive `p* = c_FP/(c_FP+c_FN)`, apply to a confusion matrix, compare expected cost against flag-nobody and flag-everybody. Then one exam problem | Asserted three times (`chapter_04.tex:1573–1579`, `:1455–1459`, `chapter_10.tex:222–227`); `grep -i "expected cost\|cost matrix"` over 12 decks returns **zero**. Ex 4.4 moves the threshold 0.5 → 0.2 "because the bank now lowers the threshold", with no cost ratio anywhere. Reframes every later chapter: a threshold is a business parameter | **3** | 20 min of the ch04 naive-Bayes block | Ind |
| 8 | **Put a grading key and a "Marking at a glance" frame in the three main papers.** Pure transcription from `mock_exam_A.tex:214–220` | 300 marks — the papers that mirror the real exam — have no grading key, no within-part allocation, no marking table. A second marker gets a model script and a per-part total; nothing says what the 6 marks of P4(a) are 6 marks *of*. The change most likely to matter at a grade appeal or a handover | **6–9** | — | Ass |
| 9 | **Reconcile the objectives slides with what is taught and examined.** *Merged: the two reviews prescribe opposite remedies for one list — reconciled below* | The objectives slide is a business cohort's revision contract. `chapter_04.tex:161-163` promises Poisson via GLM; the same PDF says at `:2342` "**Not examinable**". `chapter_06.tex:156-158` says "**Use** PCR and PLS": 3 slides, only exercise in the appendix, PLS appendix-only, 0 hits in any paper | **5** + a decision per item | — | Cur, Ass |
| 10 | **A One validator, both jobs.** Extend `make_index.py` to (a) regex `p\.\s?(\d+)` out of each runsheet and print page/title pairs against the `{page: title}` map it already builds, and (b) index the industry frames' pages | `check_decks.py` checks page counts and overfull vboxes only; nothing catches page drift, and drift is what made two rows of `lecture_01.md`'s cut list actively wrong (§6.2). Without (b) the industry-frame work you have just done breaks silently the first time a deck gains a slide | **5** | — | Cur, Ind, Lab |
| 11 | **Swap one problem per main paper from arithmetic to output interpretation**, from deck exercises you own: E1 P4 → `chapter_03.tex:2154` (four residual plots, name problem and remedy, **plots printed**); E2 P2 → `chapter_04.tex:1476` (Ext Ex 4.4, choose among five classifiers for three cases); FIN P5(c)(d) → `chapter_10.tex:1285` (Ext Ex 10.3, loss curve, where to stop, what `weight_decay` did) | The test: **keep hand computation where getting it wrong reveals a conceptual error; cut it where it reveals only a slip.** E1 P4(b)(c)(e) is 12 marks measuring whether the candidate can subtract from numbers the stem prints. FIN P5(c)(d) examines a convolution formula no ch-10 objective mentions while three stated ch-10 objectives go unexamined | **~12** | 8–12 marks of hand arithmetic per paper | Ass |
| 12 | **A The 25-minute causal-thinking insert.** *Merged: [Ind] designs it, [Ass] shows it is unexamined.* 15 min after the MMM case (`chapter_03.tex:401`): the ladder of evidence for a coefficient you are about to spend money on — randomise → exploit a policy change (DiD) → control and hope. 10 min in the ch13 p-hacking block: uplift — rank by treatment effect, not propensity. Then examine it | Your own industry frames walk into this wall four times and stop (`chapter_03.tex:396–399`; `chapter_00b.tex:247–253`; `chapter_02.tex:383–388` names the uplift problem and never supplies the fix; `chapter_01.tex:206–210`). Causality appears only as a prohibition; "difference-in-differences" appears **once**, inside a solution in an **optional** deck. No new machinery, no potential-outcomes notation | **6–8** | The §4.4 cuts | Ind, Ass |
| 13 | **A One figure bank, serving both the papers and ch04.** *Merged: [Ass] wants eight exam-ready plots, [Ind] wants a reliability diagram and a gains/lift chart — one job.* Two residual-vs-fitted patterns, a flexibility-vs-error pair, a CV-error-vs-λ curve, a lasso-vs-ridge coefficient path, two crossing ROC curves, a loss curve turning up, a GAM partial-dependence panel, a reliability diagram, a gains/lift chart with the top-decile comparison | Zero figures in eight papers because there is no reservoir of exam-ready ones. `mock_exam_1.tex:480–482` *describes* a U-shaped residual plot then asks what it indicates — the stem contains the diagnosis. Separately "lift curve" is 0 hits and no reliability diagram exists though "calibrat*" appears 14 times and `chapter_04.tex:1455–1459` promises the top-decile comparison. These are the two charts in a real model-review pack, and A1 needs them | **8–10** | — (feeds row 11) | Ass, Ind |
| 14 | **Twelve retrieval openers, plus mark Lecture 1's break.** Three questions on last week, answers on the same slide, 3 min, no marks | **Nothing in the course asks a student to retrieve last week's material** — no recap frame in any deck; ch02, ch08, ch10 have zero cross-chapter references, and the final is weighted to Ch 7/8/10/13. Content exists already: three items from the previous deck's "Ten things to remember". And `before_class.md:35` says to announce the break, while `lecture_01.md` has none — 146 planned minutes, the heaviest session in the course | **5** | 2–3 min/session of closing revision the runsheets already say to hand out | Cur |
| 15 | **A Notebook execution in CI, weekly cron.** `nbclient` on all fifteen, fail on any error output; then a normalised text diff (strip `statsmodels` `Date:`/`Time:` and `lifelines` `time fit was run` — confirmed the only systematic cosmetic diffs) | All three drift bugs were **silent** — no exception, just different numbers — and the whole suite is measured at **58 s**. This is the check that would have flagged ch05 the day it broke | **3** + ~1 h/sem | — | Lab |
| 16 | **A `docs/for-students.md`, and a contact address.** Prerequisites and skip rule (from `Teaching_Guide/README.md:64-70`), workload (`semester_plan.md:79-84`), the solutions policy stated plainly for the first time, "when your numbers don't match" | All seven student needs are absent. Student-primary content is ~22 % of ~7,000 words in `docs/`; `docs/slides.md` alone (1,904 words) outweighs everything student-facing combined; the author CV appears twice. The best student-facing writing already exists — filed in lecturer files. Also fix `docs/exams.md:48-52` (an uncopyable `cd`) and add "not published" markers at `Teaching_Guide/README.md:9,:12`, `before_class.md:12` | **4** | — | Lab |
| 17 | **Re-anchor to Europe, and stop teaching in dollars.** *Merged [Ind] R2+R3.* Keep US anchors as explicit contrasts — "in the US this is ECOA; here it is Art. 22" beats either alone. Do **not** blanket-convert currencies: `Default`, `Credit`, `Carseats`, `Hitters` are US datasets and their dollar figures are facts | Dollars 77 occurrences across the twelve taught decks; euros 27, of which **26 are in `chapter_00`** — money is denominated in euros only in sessions a student may skip. The whole European regulatory footprint of 1,168 slides is ECB ×2, EU ×1, AI Act ×1; zero hits for GDPR, data protection, consent, BaFin, Solvency, EBA, Germany, European. **Every citation carries a confidence marking — §7. Several are `(verify)`** | **11–14** | — (substitution) | Ind |
| 18 | **Split `requirements.txt`; make the data path single-valued.** Core (7 packages + jupyterlab) as default, `requirements-full.txt` adding ISLP/xgboost/pinned pygam. Then in `load()`: drop `Unnamed: 0`, coerce `Auto.horsepower` to float, settle `Auto.name`; add `USArrests.csv` and an `NCI60` extract; delete the `if HAVE_ISLP:` branch in `chapter_03_lab.ipynb` cell 18 | 114 packages / 126 MB without ISLP, and **13 of 15 notebooks verified to run clean with no ISLP at all**. The bigger cause of "my numbers don't match" is the ISLP-vs-CSV branch, not sklearn — see §4.1. `USArrests` is not in the CSV directory at all, so ch12 reaches the network and `docs/labs.md:60-61` ("a local checkout works offline") is false | **4** (+1) | `docs/environment.md` and the Colab `_ensure` list need a consistency pass | Lab |
| 19 | **Rebalance the two precourse sessions; teach Python once.** Move `chapter_00` pp. 83-96 into `chapter_00b`, bring linear algebra and gradient descent out of `chapter_00`'s appendix into the timed plan, delete `chapter_01` pp. 48-50 and `chapter_02` pp. 90-91 | `chapter_00` is 106 main-flow slides in 180 min (≈1.4 min/slide, densest in the course); `chapter_00b` is 51 in the same slot (≈2.8, its runsheet says "20 minutes of slack"). Python is taught **four times** and the runsheets cut two of the four every year — a symptom, not a design. Also makes `chapter_00`'s objectives `:186`/`:188` true and removes the "gradient is used without further explanation" trap. Your own diagnosis (`Teaching_Guide/README.md:69-70`) is that rusty standard errors sink students — and this is the one deck that cannot be delivered in its slot | **10** | ch00's Python §; ch01 pp. 48-50; ch02 pp. 90-91; two cut-list rows | Cur |
| 20 | **Separate solutions from prompts.** *Merged — one defect, two artefacts, one decision.* (a) `\newif\ifsolutions` + `make decks-nosolutions` → `chapter_NN_student.pdf` (**4 h**; the exam sources already do this). (b) Split each notebook into `_lab` (prompts, exercise outputs cleared) and `_solutions` (**12–15 h**) | Every in-deck solution is the adjacent slide, and the handout is `nup=1x2`, so a prompt on an odd page shares a sheet with its own answer — 9 of `chapter_03`'s 18 exercises. In the notebooks every solution ships in the file the student opens with its answer inline (`# 2.553`, `# best K = 14`) and its output stored. **[Cur] and [Lab] disagree about the labs here — §6.4** | **16–19** (do (a) now, (b) over a summer) | Build simplicity; a heavier docs build | Cur, Lab |
| 21 | **Relabel the three self-study notebooks as code references** in `README.md`, `docs/labs.md`, `docs/course.md`: "code reference — no lecture provided; read ISLP §9/11/12 first" | Against the taught twelve (median 29 cells / 11 code / worked solutions in all twelve): ch09 16/6/**no**, ch11 17/7/**no**, ch12 18/7/**no**. `chapter_12_lab` introduces PCA, K-means and Ward linkage in seven code cells with no conceptual markdown, then asks the student to implement matrix completion unaided and unanswered. Excellent references for someone who attended the lecture; there is no lecture | **2** | — | Cur, Lab |
| 22 | **A `mistake` box type, and convert the 133 instances** | 133 instances of `\textit{Common mistake:}` (18 in ch03 alone) are plain italic text inside other boxes. The richest layer of the material has no visual identity, cannot be found by flipping, cannot be extracted into a revision sheet. The answer to "is a slide type missing" is: not a slide type — a *box* type, for content you have already written | **7** | — | Cur |
| 23 | **Three `[Integrative]` exercises, for Ch 6, Ch 8, Ch 10.** Model on `chapter_04`'s Ext Ex 4.4 | These three decks have **zero** (Ch 1,2,3,4,5,7,13 all have at least one), the final is "weighted to Ch 7/8/10/13", and FIN P7 is "Cumulative essentials (Ch 2-6)" — a problem type nothing in Ch 6 rehearses. Ch 10's should be "is deep learning worth it here", the stated objective no exam assesses | **8** | One short exercise each | Cur |
| 24 | **Author figures at final on-slide width; retire whole-frame shrinks** | `ch00_anscombe.png` is 9.33 in at 150 dpi included at `0.99\textwidth` = 5.99 in — a 0.64 downscale, so a 7.5 pt tick projects at **≈4.8 pt**, half the smallest slide text. Setting `figsize` to 5.99 in fixes it alone. Separately ch00 has 93 font-shrink commands, 36 wrapping a frame's first body line; worst are `:2269` (20-row table at `\tiny`) and `:194` (237 words, 12 items, whole-frame `\scriptsize` — the entry point for the least confident students). Handouts render 1.07× *larger* than screen, so print does not compound it | **6** | — | Lab |
| 25 | **Give the `industry` box a printed label; stop instructing colour-reading.** Always prefix "In industry: "; restore "Solution" on the 27 `solutionbox` calls that drop it; rewrite `chapter_04.tex:1631` ("Green cells are correct decisions, red cells are the two error types") and `chapter_13.tex:1156-1157` to name cells | **86 of 86** industry boxes identify themselves by grey tint alone; `takeaway` (`green!4`) and `solutionbox` (`teal!5`) are adjacent hues at 4–5 % tint with no icons. `chapter_05`'s k-fold diagrams (`:446-463`) are your own best-practice example: colour *plus* printed "Train"/"Test" | **2** | — | Lab |
| 26 | **Make the fourteen `labnote` boxes name a notebook section**, and use three or four per deck as a pacing device | 14 boxes in 22,399 lines of deck source; nine decks have exactly one and one sentence appears **nine times byte-identical**; none names a section though the anchors exist (`## 3. Pruning via cost-complexity`). The notebook is a handoff at the end, not a companion, while `semester_plan.md:84` says the labs are what matters. Catch in the same pass: `chapter_06.tex:1264` says "Extended Exercise 6.3" where the notebook says 6.2, and `:1218`/`:1272` print a relative `read_csv` path valid only from a deck directory on a slide for students to copy | **2–4** | — | Lab, Cur |
| 27 | **Rebalance the final: Ch 8 down, Ch 10 or 13 up.** Cut FIN P3 from 20 to 12 and move 8 marks to `chapter_13.tex:836` (Ext Ex 13.2, FWER vs FDR, 4-endpoint trial against a 20,000-gene screen) | Ch 8 gets 36 main-paper marks for one session against 20 each for Ch 10 and 13 — over-weighted ~1.8×. Ch 10 and 13 are the last two sessions and the only two decks with no "N things to remember" and no self-check frame: thinnest closure, lightest examination, where attention is scarcest | **2** | ~8 marks of ch-8 arithmetic | Ass |
| 28 | **One authentic `statsmodels` summary per paper** | `docs/exams.md:41–43` says the papers "show real output". They show four-row extracts with round numbers (`t = 42.000`, `coef = 2.3500`). No paper *and no deck* contains `Df Residuals`, `Omnibus`, `Durbin-Watson` or the `[0.025 0.975]` columns. Recognition transfers; pattern-matching on a tidy table does not | **1** | — | Ass |
| 29 | **Narrow `warnings.filterwarnings('ignore')`, at least for ch07** | It hides three warnings in total across six notebooks — but one is pyGAM's "KNOWN BUG: p-values… are likely much smaller than they should be", and `chapter_07_lab`'s own prose tells the student "pyGAM prints a caveat", referring to a message the setup cell prevents them from seeing | **0.5** | — | Lab |

**If you have one uninterrupted block rather than five gaps**, spend it on rows 8, 9 and 12 (grading
keys, objectives, causal insert) and file row 3's paperwork the same week. Value per hour puts hygiene
on top; that does not make it the most important work here.

### Reconciling row 9

The two reviews reach the same list of false objectives and prescribe **opposite** remedies — [Cur]
soften the text, [Ass] examine the objective. Both are right about different items; decide per item.

- **Soften** where the omission is documented and deliberate: PCR/PLS (`lecture_06.md:17` tells the
  room the section is not on the exam), resampling *p*-values (`lecture_13.md:31` likewise), Poisson
  (the appendix already says "Not examinable"). "**Use** PCR and PLS" → "**recognise when** dimension
  reduction is the right response to collinearity". ch02's "**Derive** the bias-variance
  decomposition" → "**apply** and **interpret**": the derivation is appendix pp. 109-112 and the exam
  asks for the numerical substitution.
- **Examine** where the objective is worth keeping: prediction interval (taught properly, drilled at
  `chapter_03.tex:1126`, self-check Q6, 0 hits in eleven papers); the four classical diagnostics
  (Diagnostics is 24 slides / 49 min, the largest ch-3 section after simple regression, taught the week
  before Exam 1 — *leverage*, *outlier*, *Cook*, *residual plot* all 0 hits; row 13 makes this a
  one-line edit); "**Choose** between trees, forests and boosting" (currently one item in a matching
  grid); "**Reason** about when deep learning is worth it" (unexamined; row 23 gives it an exercise).
- **Structural, not textual:** ch00's matrix-form and gradient-descent objectives are fixed by row 19.
- **One misplaced question:** ch08's self-check asks about BART while its appendix note correctly says
  forests and boosting are the two you will be asked about. Cut the question, not the note.

---

## 4. Detail by theme

### 4.1 Version drift and reproducibility

Do not over-read this. **173 of 202 code cells produce byte-identical text output across a jump from
numpy 2.0/pandas 2.3/sklearn 1.6 to numpy 2.5/pandas 3.0/sklearn 1.9**, a pandas major release
included. That is why [Lab] rejects hard-pinning. Three findings were not noise:

- **ch05 cells 8/10/12 now teach the opposite of what they shipped.** Shipped 10-fold CV MSE by
  degree: `19.276, 19.478, 19.137, 19.255, 19.150, 18.962, 19.099, 19.866` (flat). On the 2026 stack:
  `20.275, 23.057, 26.729, 30.612, 34.376, 37.895, 41.123, 44.040` (monotone explosion). Cause:
  `PolynomialFeatures` on raw `horsepower` (46–230), so degree-10 columns reach ~10²³ and the answer
  depends on how `lstsq` handles a catastrophically conditioned design. Inserting `StandardScaler()`
  first makes the numbers **identical across the three-year gap** — verified in both environments.
  Same pattern mildly at `chapter_07_lab` cell 25 (1598.2 → 1611.9). *In progress this session.*
- **ch08 cell 26: single-tree test MSE 26.67 → 16.49** (sklearn splitter tie-breaking), which makes
  cell 30's "Every ensemble cuts the single tree's error three- to four-fold" simply wrong (two-fold).
  Better than re-running: make cell 26 `DecisionTreeRegressor(max_depth=8, random_state=1)` so the
  comparison is against a defensible tree, not an unpruned one whose test error is an artefact.
- **ch07 cells 15/20: pyGAM broke** between 0.10.1 and 0.12.0 — log-likelihood −24864.6 → −15299.7,
  AIC 49773.7 → 30643.7, Scale 1585.99 → **39.82**. `requirements.txt:16` says `pygam>=0.9`, so
  students get 0.12 and read your interpretation beside a 60 %-different fit statistic.

**The larger "my numbers don't match" cause is the ISLP-vs-CSV branch**, which silently produces
*different data*: `chapter_02_lab` c10 prints `(392, 8)` shipped and `(392, 9)` on the CSV path;
`chapter_05_lab` c6 shows `130` vs `130.0` in the very first data cell; `Bikeshare` from CSV carries a
stray `Unnamed: 0` that `chapter_04_lab` c15 exists purely to print; `chapter_03_lab` c18's two branches
produce completely different regression tables (`poly(lstat,2)[0] = -71.4385` vs `lstat = -2.2980`) —
both correct, only one matching the slide; `NCI60` has no fallback, so the ch01 and ch12 PCA figures
never appear. Row 18 fixes all of it in one function.

### 4.2 Leakage the course teaches against and then models

- `chapter_06_lab` **cell 19** (`Xs = StandardScaler().fit_transform(X)` then `cross_val_score`) and
  **cell 22** (`XH = …fit_transform(X_raw)` then `LassoCV(cv=10).fit`): the scaler sees every fold's
  held-out data, in the two cells labelled "worked solution". **Both were fixed in this session** (cells
  19, 22, 23 now use `GridSearchCV(make_pipeline(StandardScaler(), Lasso()), …, cv=10)`, with a comment
  explaining that GridSearchCV re-fits the scaler per training fold).
  **Correction to [Lab]: cells 11 and 15 are *not* clean, and the fix has widened the gap — see §6.13.**
- `chapter_08_lab` **cells 27–28**, headed "tune m" and "tune (learning rate, trees, depth)", select by
  comparing **test MSE**; cell 30 reports "tuned boosting … reaches ≈ 7.4" — a test score for a
  configuration chosen on that test set. `GridSearchCV` is already imported and used correctly at cell
  12 of the same notebook. If you keep the loops, relabel them and add: *this is not how you would
  choose m; see Chapter 5.*
- `chapter_02_lab` cell 26 (`best_K = argmin(te_err)`) should be **left alone** — its purpose is to
  draw ISLP Fig 2.17's U-curve and cell 28 half-redeems it. Add one sentence.
- Both leakage instances are in progress. What they cost if missed: ch05's "**Avoid** the common
  resampling pitfalls" is examined **only** in short exam D P1(c)(d), never in the three main papers,
  and time-series folds and group splits are 0 hits anywhere.

### 4.3 The industry layer: strong content, no apparatus, wrong geography

- **Declarative throughout.** Cost-priced confusion matrices (`chapter_04.tex:1573–1579`; 0 hits for
  *expected cost*/*cost matrix*); SHAP as the source of reason codes (`chapter_08.tex:727–729`; "SHAP"
  appears twice in the repo, both inside callouts, never computed); top-decile comparison
  (`chapter_04.tex:1455–1459`; "lift curve" 0 hits, "decile" 1 hit — that sentence). And "most of a
  project's time goes into that join", against, across all 15 notebooks: `merge(` **0**, `to_datetime`
  **0**, `isna`/`fillna` **0**, `duplicated` **0**, `SimpleImputer` **0**, `Pipeline` **0** — only `dropna`
  (11 hits). [Ind]: *"A practitioner reading the decks would say: this person knows the job. A practitioner
  watching a graduate would say: they can recite the job."*
- **Sector spread**, 72 table rows: financial services ~35 %, retail/e-commerce ~22 %,
  manufacturing/industrial/energy ~18 %, pharma/health ~11 %, tech ~11 %, **logistics 1 row**,
  **public sector 0**, **professional services 0**, **controlling/FP&A 0**. "automotive" appears once
  in twelve decks; "Mittelstand", "SME", "public sector", "government", "municipal" — zero. The twelve
  depth cases balance better but include **two consecutive banking cases** (ch04 credit scoring, ch05
  credit-risk model validation).
- **Cheapest structural fix (5 h):** re-cast the ch05 depth case as the **walk-forward backtest of a
  demand or load forecast** already sitting in its own table at `chapter_05.tex:243–245` — same
  statistics, removes the double banking case, adds energy/retail at zero conceptual cost. Then rewrite
  ~8 rows to add logistics, public administration, controlling/FP&A and professional services (audit
  sampling, which is genuinely ISO-2859-shaped).
- **Demote NIR/PLS (`chapter_06.tex:256–278`) to the appendix (2 h)** and promote the credit-scorecard
  attribute-shortlisting row at `:229–231`, or a wide customer/SKU table, into the flagship slot. The
  best possible motivation for *p ≫ n*, and no business graduate will ever be within three floors of
  absorbance and % w/w.
- **Keep and protect:** marketing mix modelling (`chapter_03.tex:366–401`, the best case in the set —
  the coefficient *is* the deliverable), price elasticity (`chapter_00b.tex:228–254`, the
  `0.9^{-1.8}-1 ≈ 21 %` calculation is the most immediately usable number in the course), retail demand
  forecasting (`chapter_08.tex:223–234`), the A/B test and experimentation-platform pair.
- **Two dated anchors:** "SR 11-7, ECB TRIM" (`chapter_04.tex:370`) — TRIM concluded in 2021
  *(confident)*, so citing it as the live supervisory anchor dates the deck; and the M5/LightGBM
  citation, accurate *(confident)* but 2020 and the layer's only benchmark. `chapter_05.tex:284–285`
  shows the better pattern: "euro area: ECB supervisory model reviews" is timeless.
- **The AI Act callout is in the wrong chapter.** `chapter_10.tex:1031–1037` is accurate and the best
  paragraph in the layer, but it sits in the deep-learning deck and says the Act "raises the bar for an
  *opaque* model". The Act is technology-neutral: the ch04 logistic scorecard is *equally* high-risk.
  Students will conclude governance is a neural-network problem. Put a sibling at
  `chapter_04.tex:355–377` and at the ch03 pay-equity frame. **Timeline caveat: §7.**

### 4.4 Pacing, and the cuts that fund the additions

By the runsheets' own totals against the 145-min ceiling `slide_index.md:5` derives: **Lecture 1 (146),
Lectures 3 and 4 (145 each), Lecture 7 (145), Lecture 10 (145)** have zero contingency; Lectures 6, 9
and 11 (135, 137, 135) have real slack. Lecture 1 is 113 pages across two decks with `chapter_01`
budgeted at 1.0 min/slide against 2.0 for `chapter_02` — the "half-session" allocation has quietly made
Chapter 1 the fastest-paced deck in the course, and it has no break block.

Three long unpractised stretches against the decks' own ~20-min exercise cadence: `chapter_05` 19 pages
between Ex 5.1 (p. 18) and Ex 5.3 (p. 37), covering all of LOOCV and most of *k*-fold — the two
procedures Exam 2 P4 tests; `chapter_06` 16 pages between Ex 6.5 and Ex 6.7; `chapter_02` 15 pages
across the whole Bayes-classifier introduction. ch03 (max gap 10) and ch13 (max gap 8) show what good
looks like. ~3–4 h to add one exercise to each.

**[Ind] costed five runsheet-anchored cuts totalling ~58 min**, which fund row 12 and the industry-frame
minutes with 8 to spare: backprop by hand on a 2-2-1 net (18 min, "the least employable 18 minutes in
the course"; keep as assigned homework with its deck solution); the third pass at KNN-vs-OLS in
`lecture_03.md` pp. 124-144 (12); a smoothing-splines/LOESS trim (8); Ext Ex 13.1, a fourth repetition
of three procedures on ten *p*-values (10); a naive-Bayes comparison trim (10).

### 4.5 One callout type stops existing halfway through the semester

`numexample` ("Worked example"): 7× ch00, 7× ch03, 4× ch02, 3× ch04 — and **0× in ch06, ch07, ch08 and
ch10**, 1× in ch05 and ch13. The material is still numeric (`C_p`/BIC arithmetic, Gini computations) but
now appears only inside exercises and solutions, where a student meets it as a test rather than a
demonstration. Two or three per second-half deck (~10 h) restores the see-one-then-do-one rhythm that
makes Ch 3 work. Two related imbalances, both cheap: `takeaway` at 47 across ch00's 122 pages means 4
slides in 10 carry a green "the thing to remember" box, while `before_class.md:36-38` calls the colours
"a contract with the students" (ch13's 18 across 69 pages is about right); and `readme` ("How to read
this") appears **once** in `chapter_00b`, the deck whose first section is "Reading mathematical notation".

---

## 5. Additions worth considering

### A1 — The applied project · 12–16 h design + 10–12 h marking per cohort · displaces Mock Exam 2 as a classroom event

Proposed independently and in detail by **two** reviews ([Ass 4.1], [Ind A1]); [Lab] and [Cur] reach the
same underlying diagnosis by other routes (nothing asks a student to produce anything; the labs'
unsolved exercises are undermined by the answers shipped beside them). [Ass] is blunt about the
institutional exposure: for a *Fachhochschule*, a quantitative methods course assessed exclusively by
closed-book written arithmetic is "the finding I would most want to defend to a programme accreditor,
and I do not think it can be defended". The two designs are complementary:

- **[Ind]'s brief is the more concrete and I would use it.** "One decision, one model, one memo": a
  mid-sized German insurer, direct-mail caravan cross-sell, mailer €4.50, policy worth €60 in expected
  contribution. Data: `ALL CSV FILES - 2nd Edition/Caravan.csv` — 5,822 rows, 85 predictors, 348 Yes
  (5.98 %, verified). It works because the economics bite: mailing everyone loses ~€91,000 at 100,000
  customers and break-even response is 7.5 %, *above* the base rate, so the model must find a
  better-than-average segment or there is no campaign. "Predict No for everyone" scores 94 % accuracy
  and is worth nothing — students discover that themselves. And the column names are opaque
  (`MOSTYPE`, `MAANTHUI`, …), so finding and reading a codebook is part of the work.
- **[Ass] supplies the alignment map.** Seven required sections, each discharging an objective the
  papers miss: prediction-vs-inference framing (4 marks of recall today); an evaluation protocol stated
  *before* fitting, with the leakage risk specific to this dataset; a baseline interpreted with units
  and the "holding others fixed" clause plus a CI **and** a prediction interval; one flexible
  alternative compared out-of-sample with a bias-variance sentence; diagnostics **with plots shown**; a
  recommendation and its limits, including why the association may not be causal; reproducibility.
- **Deliverables:** a 4-page decision memo to a named stakeholder (hard page limit, marked by reading
  the memo *only*); a reproducible notebook (Colab, one DuckDB SQL step, threshold from the cost
  ratio); a one-page model card (A3).
- **Marking, 100 points:** decision quality 40, method soundness 25, communication 20,
  reproducibility/documentation 15. "Boosting beating logistic regression earns nothing on its own."
- **Load:** student 18–25 h for a group of three; marker 25–35 min per group, ~10–12 h for 20 groups.
- **What it replaces:** not the final paper. **Mock Exam 2 as a classroom event** — it sits after
  lecture 8, exactly where a project must start to finish by lecture 12, and its chapters (4–6) are what
  the project exercises. Keep the PDF in circulation as revision material.
- **Zero-setup fallback:** `Bikeshare.csv` (8,645 hourly rows) — reposition-and-forecast-error framing,
  with one genuine wrangling step (building a time index from `mnth`/`day`/`hr`).
- **A five-minute oral** on the submitted notebook (*why this split? why did the flexible model win or
  lose? what would change your recommendation?*) is the only genuinely AI-resistant instrument in the
  four reviews and costs almost nothing, because the artefact is already in front of you. Run it
  ungraded as a pass/fail authenticity check if a graded oral is awkward under the regulations.
- **The real constraint is the Modulhandbuch, not the hours** — row 3.

### A2 — A taught half-session on PCA and clustering · 25–35 h deck + 6–10 h notebook + 5 h runsheet/exam · displaces half of Ch 13 and half of Ch 10

**Ch 12 is the expensive omission**, and not only because segmentation is the most-used technique in
commercial analytics. It has dependencies inside your own course: `chapter_06`'s PCR is defined as
regression on "the principal components of **X**" with PCA never taught; `chapter_01`'s third motivating
dataset is "NCI60: the first two principal components", shown in week 1 and never explained;
`chapter_00b`'s "Where each topic reappears" table sends students to "Ch. 12 (clusters)", a chapter with
no deck.

The funding is the honest part and it is your call. **Ch 13 → half session**: 63 slides, 141 min
planned, the loosest budget in the course at 2.3 min/slide; "The Problem" 8 + FWER 9 + FDR 16 +
Practice 6 is a 90-minute topic delivered in 180. **Ch 10 → half session**: six of nine exercises are
hand arithmetic, the lowest conceptual share of any deck; keep single-layer, multilayer, the PyTorch lab
and the "worth it" reasoning, drop the CNN arithmetic and the 4-slide Sequences section the objectives
only promise to "**Outline**". [Ass] independently supports the Ch 10 half by a different route: FIN
P5(c)(d) examines the convolution formula against no stated objective.

### A3 — Cheap additions the reviews agree on

- **A one-page model card template — 2 h.** Target and horizon; scoring population; predictors and
  their availability *at decision time*; validation design; metric and threshold with its cost basis;
  monitoring trigger; owner; legal status. "model card" = 0 hits today, "monitoring" = 6 hits, all
  rhetorical. It operationalises `chapter_01.tex:1130–1134` and the AI Act callout, is a project
  deliverable, and is a document a graduate can show an employer.
- **One data-plumbing lab, self-study, zero contact hours — 6–8 h.** Read two files, parse dates, do an
  **as-of** join that would leak if done naively, handle duplicates and missings, then fit the same
  model with and without an sklearn `Pipeline` and show the CV score change. `Pipeline` is correctly
  explained on slides in three chapters and appears in **zero notebooks** — the mechanism practitioners
  use to prevent leakage is taught as prose only. Ext Ex 5.3 is its conceptual anchor; `Bikeshare.csv`
  plus a hand-made promotions table suffices.
- **DuckDB over the existing CSVs, gated self-study — 3–4 h, zero contact time.** [Ind] calls this "the
  highest-value item in the whole review per hour of *your* effort": SQL is the most requested tool in
  analyst job ads and cannot be taught inside twelve statistics sessions, but
  `duckdb.sql("select … from 'Credit.csv'")` needs no server and one pip line. Gate it by requiring one
  SQL step in the project. Same logic for git: do not teach it, require three commits per group member.
- **LLM verification discipline: 15 minutes and one rule — 3 h.** Attach to the ch00b block "The Python
  you will actually write". The content is *verification*, not prompting: after an LLM drafts your
  pandas you check row counts before and after every join, check dtypes, hand-compute one value — framed
  exactly as the deck already frames vendor models at `chapter_02.tex:811–815`. The rule: LLM use in labs
  and the project is allowed and must be disclosed in a one-line comment. Enforceable, and it protects
  exam integrity precisely because the exams are already closed-book. No RAG, no agents, no fine-tuning.
- **A supplier-risk row and callout — the Mittelstand hook — 1 h.** Imbalanced labels, a cost-asymmetric
  threshold, an audit-trail requirement and a legal driver; also supplies the logistics/procurement
  representation the tables lack (1 row in 72). *Regulatory basis: §7.*
- **A German column on the twelve `{Vocabulary check}` slides — 3 h.** No German-language support exists
  anywhere (grep for `glossar|german|deutsch|bilingual|translat` yields six hits, all false positives).
  The hook exists: every deck's summary block already has a `Term | One-line meaning` table. Row 24
  first — the table is at whole-frame `\scriptsize` today.
- **An annual 60-minute "currency check" — 1 h/year.** Fixed checklist: three regulatory dates, three
  technique defaults, one sweep of the depth-case caveats. Slot it into the `before_class.md` rhythm.
  The only maintenance mechanism in the four reviews I would bet on.
- **A one-page case-sheet template for guest practitioners — 1 h**, ~30 min per case. Mirrors the existing
  six-field depth-case structure, so a guest fills a form rather than writing slides — the difference
  between "yes" and "I don't have time". Give guests a 25-minute slot inside a session, never a whole one.
- **An errata channel** — `.github/ISSUE_TEMPLATE/` plus `docs/errata.md`. No channel and no address exist
  today for the next ch05-style bug.
- **Peer review of project drafts** — displaces 45 min of Lecture 11 or 12; keep it formative, because peer
  marks in the grade create appeals.

---

## 6. Conflicts, corrections and contested claims

**6.1 Colab already exists — the brief was wrong.** [Lab] was told the repo has "no Binder/Colab entry
point" and found the opposite: a working badge in cell 0 of every notebook, all fifteen at
`docs/labs.md:22-41`, and `docs/quickstart.md:7` already calling Colab "recommended". The repo is
public, the CSV directory is tracked, and every fallback URL returns 200. The finding is *invisibility*,
not absence — which is why row 5 costs 2 hours, not a day. **Not verified: an actual Colab runtime was
never launched.** [Lab] also advises against Binder (2–5 min cold starts, fragile with `torch`) and
against a link checker (15 Colab URLs return 405 to HEAD, 200 to GET — permanent false failures).

**6.2 Runsheet page drift — the two reviews disagree, and both may now be stale.** [Cur]:
`lecture_01.md`'s *prose* is 3 pages low throughout while its running-order tables are correct;
`lecture_02.md`'s "Worth doing on the board" and "What they will get wrong" sections are 2 low; and it
checked `lecture_05`, `06`, `08`, `13` and found them accurate (two exceptions in `lecture_08.md`).
[Lab]: "**≥14 stale page references across four runsheets, every one off by exactly +2**", citing
`lecture_03.md:38` (Exercise 3.1 given as p. 28; it is p. 30). The direction agrees — runsheets
under-number the re-paginated decks — but the files and magnitudes do not, and page references were
re-mapped later in this session, so both findings may predate the fix. Verify against the current files,
then add the validator (row 10). Two `lecture_01.md` errors are worse than stale: cut-list row 3 says
cut "27, 31 — the two recreated figures", but pp. 27 and 31 are the two slides that *introduce* the
examples (the figures are pp. 30 and 34); cut-list row 4 says cut 67-70 and then "skip to slide 68".

**6.3 "No slide in the main flow depends on an appendix slide" (`Teaching_Guide/README.md:54`) fails —
in two different directions.** [Cur]: it holds for *content* (ch06 geometry, ch07 truncated-power, ch10
backprop are all main-flow, stress-tested) but not for the *objectives* slides, which are main-flow and
point at the appendix. [Ass] found the harder counter-example: **short exam C P3(b)(c), 10 of 60 marks,
tests ridge and lasso closed forms under an orthonormal design — appendix material** (`\appendix` at
`chapter_06.tex:1474`, Ext Ex 6.2 at `:1589`), while `semester_plan.md:9–13` says appendix pages are
"extra material to assign, not to teach".

**6.4 The labs' exercise design — [Cur] and [Lab] disagree.** [Cur] lists the taught labs' shape as
sound and praises the worked-solutions section *plus* four unsolved exercises. [Lab] says the packaging
defeats the structure: every solution ships in the same file with its numeric answer as an inline
comment and its output stored, so Exercise 6.7 cannot be attempted without the answer three lines below;
and a grep across all fifteen for `TODO`, `# your code`, `_____`, `<fill`, "complete the", "what do you
expect", "guess" returns **zero hits**. Both are true — the architecture is right, the distribution
undermines it — which is why row 20 costs 12–15 h rather than nothing.

**6.5 The verdict on the industry layer differs by lens.** [Cur] examined the `industry` boxes and
judged them "well-calibrated at 6-10 per deck and needs no work". [Ind] judged the same layer "entirely
declarative — and that is the central weakness", with 25 frames carrying zero minutes and zero notes.
[Lab] found **86 of 86** cued by grey tint alone. Not a contradiction — density right, apparatus and
practice missing, labelling inaccessible — but a professor reading [Cur] alone would conclude nothing is
needed here.

**6.6 The "155-page deck" premise was wrong; [Cur] corrected it.** `chapter_03` is 155 pages but spans
**two** sessions, so at 76 and 68 pages per half it is one of the better-paced decks. The largest deck in
a single 180-min slot is `chapter_00` at 122 pages; the heaviest single *session* is Lecture 1, 113 pages
across two decks.

**6.7 Version drift is not a crisis, and hard-pinning would be wrong.** [Lab] explicitly rejects all
three options it was offered (hard-pin, publish tolerances, teach that drift is normal) on measured
evidence of 86 % stability, and pins only `pygam` and `ISLP`.

**6.8 PCR/PLS: defect or deliberate?** [Cur] treats it as a false objective; [Ass] notes it is documented
and deliberate (`lecture_06.md:17`) but flags the second-order effect — telling a business-school room
that a section is not on the exam reliably means it is not learned. Row 9 softens the objective and keeps
the content.

**6.9 Exam sub-part independence: paper and solutions deck currently disagree.**
`mock_exam_1.tex:341/344/346/355` still hands back `ŷ = 2.000 + 3.000x`, the residual vector, RSE = 1.155
and RSS = 4.000, while `solutions_slides_1.tex:434` asserts "The question paper no longer restates…".
[Ass] says treat this as mid-edit, and the direction is right — but note the dependency: once the
restatements go, sub-part independence is only true if the ECF sentence is in the Instructions block (§2).

**6.10 Counting conventions differ; the underlying numbers do not.** In-deck exercises are **127** in
three places (87+40 in [Cur §5] and [Ass]; 86+41 in [Lab], cross-checked against the PDFs) and **139**
once, in [Cur R3(b)]'s reference to `slide_index.md`. I have not resolved which is right — use 127 unless
`slide_index.md` says otherwise. Paper counts: the brief and [Cur] say **11** papers; [Ass] analyses
**8** (Exam 1, Exam 2, the base final, five short), excluding the two parallel final variants. Both are
right under their own convention. Slide counts agree everywhere: 1,057 + 111 = 1,168 pages.

**6.11 The premise nobody could check: what the summative instrument actually is.** [Ass]: every paper is
labelled *mock*, and "**nothing anywhere in the repository states what the summative instrument actually
is**" — no ECTS weighting, no grade split, no statement that the real HSBI paper is isomorphic to these.
Its recommendations therefore describe the rehearsal system and infer the real paper from it. **If the
real paper differs materially, rows 8, 11, 27 and A1's displacement all change priority.** You are the
only person who can settle this, and it should be settled before row 8 starts.

**6.12 What the reviews infer rather than measure.** [Lab]: everything about how a student *feels* is
inferred from artefacts — that vague `labnote` pointers go unused, that inline answers get read instead of
attempted, that a 4.8 pt tick label is unreadable from row twelve. The two claims it would most want
checked — whether anyone uses the Colab badges, and whether the terminal `## Exercises` lists are ever
attempted — are answerable with one question in week three. [Cur] marks as speculative its expectation
that Lecture 2 is where a business cohort saturates (100 min of the most abstract material in one
afternoon, break at minute 75). [Ind]'s claim that the likeliest destination for an HSBI graduate is a
controlling, sales-ops, purchasing, supply-chain or key-account seat in a regional Mittelstand firm is
judgement, not measurement; the OWL industrial base itself it marks *(confident)*.

**6.13 [Lab] certified `chapter_06_lab` cells 11 and 15 as correct. On inspection they are not, and this
session's fix to cells 19/22 has made it visible.** [Lab] wrote that "cells 11 and 15 do it correctly with
`make_pipeline(StandardScaler(), RidgeCV(...))`". That is correct only *relative* to the old cells 19/22,
where scaling happened entirely outside any CV. Read literally, both still leak into hyperparameter
selection: `make_pipeline(StandardScaler(), RidgeCV(...)).fit(X, y)` fits the scaler on all 263 rows
**before** RidgeCV/LassoCV performs its internal split, so every candidate α is scored on data scaled
using statistics drawn from its own held-out fold. The correct nesting is the one cell 22 now uses —
`GridSearchCV(make_pipeline(StandardScaler(), Lasso()), {...}, cv=10)` — where the scaler is re-fit per
training fold.

Verified in the working tree (read-only): cell 11 `RidgeCV(alphas=np.logspace(-2,4,50))`, prints
`best alpha: 3.727593720314938`; cell 15 `LassoCV(alphas=np.logspace(-3,2,50), cv=10, random_state=0)`,
prints `best alpha: 2.9470517025518097`. Cell 22, post-fix, prints `lasso alpha : 2.33` and
`ridge alpha : 2.812` for what a student reads as the same task on the same data.

**Consequence, and it is now the more urgent half of the defect.** §3/§4 of the notebook come *before*
§5, so the pattern students copy is the leaky one, and the notebook currently prints two different α for
one task with no explanation. **But the 2.947 → 2.33 gap cannot be attributed to leakage alone**: cell 15
uses `LassoCV`'s default path scoring while cell 22 uses `scoring='neg_mean_squared_error'`, so part of
the difference is a different CV objective, not the leak. Isolating the leakage effect requires running
cell 15's own grid and CV setting nested vs non-nested — not yet done, and no before/after number should
be quoted until it is. Whoever holds the notebook should also decide whether the two sections are meant
to be the same task at all; if they are, one recipe should win, and if they are not, the notebook needs
one sentence saying why the α differ.

---

## 7. Uncertain factual claims — do not launder these

[Ind] marked every legal instrument **(confident)** or **(verify)**; the distinction is preserved exactly.
**Nothing marked (verify) or "reasonably confident" goes on a slide without checking first.** [Ind] states
it invented nothing and wrote "I could not verify" rather than supplying a detail — treat any citation not
listed here as absent from the inputs.

**(confident)** — usable after a normal proofread: CJEU C-634/21 *SCHUFA Holding*, judgment 7 Dec 2023,
that a credit agency's probability value is a "decision" under GDPR Art. 22(1) where a third party draws
strongly on it; GDPR Art. 22 and the information duties in Arts 13–15; that **§ 31 BDSG** is *the* German
scoring provision; EBA Guidelines on loan origination and monitoring, EBA/GL/2020/06; that MaRisk exists
and is the relevant German circular; DORA, Regulation (EU) 2022/2554, applying from 17 Jan 2025; CJEU
C-236/09 *Test-Achats*, 1 Mar 2011, with unisex premiums required in the EU from 21 Dec 2012; *Typklasse*,
*Regionalklasse*, *Schadenfreiheitsklasse* as the actual German motor rating factors, the first two
published annually by the GDV; Solvency II Directive 2009/138/EC; BetrVG § 87(1) no. 6 and the operative
phrase "suitable for" monitoring; EntgTranspG (2017); that EU Pay Transparency Directive 2023/970 exists,
transposition deadline 7 June 2026; that AI Act Regulation (EU) 2024/1689 Annex III makes creditworthiness
assessment of natural persons and employment/worker-management high-risk, with documentation, logging,
monitoring and human-oversight obligations; ISO 9001, IATF 16949, VDA Band 5, AIAG-VDA FMEA Handbook
(2019); ISO 2859-1; EU MDR Regulation (EU) 2017/745, CE marking via a notified body, Rule 11 of Annex
VIII; ICH E9 and the E9(R1) estimand addendum (2019); that an EMA/CHMP multiplicity guideline exists; LkSG
in force 2023 for ≥3,000 employees and ≥1,000 from 2024; that ECB TRIM concluded with its final report in
2021; that LightGBM-based solutions dominated M5 (2020); the *it's OWL* cluster and OWL's industrial base;
that SMARD.de, DWD Open Data and the ENTSO-E Transparency Platform are real, free and unregistered; that
the Caravan data is COIL 2000 / *Insurance Company Benchmark* with a published UCI codebook, 5,822 rows,
348 Yes (5.98 %, verified); that Bank Marketing, Statlog German Credit, Online Retail II and Bike Sharing
are on UCI; that Destatis GENESIS-Online, Eurostat, Bundesbank, the ECB Data Portal and GovData.de are
free and citable.

**(verify) / not confident** — the review does not stand behind these as written:

| Claim | What is uncertain |
|---|---|
| **§ 31 BDSG** | Confident it is *the* scoring provision; **verify current wording** and the GDPR-compatibility debate the SCHUFA litigation put in play |
| **CJEU C-203/22 *Dun & Bradstreet Austria* (2025)** | **Verify citation and holding.** Recollection only: disclosing the algorithm is not sufficient; the controller must explain the procedure and principles actually applied |
| **ECB Guide to internal models** | Confident it exists; **verify current edition date** |
| **MaRisk section number for model risk** | Explicitly **not confident** — "do not put one on a slide without checking". BaFin's principles on algorithms in decision-making: **verify title and status** |
| **CRR3, Regulation (EU) 2024/1623, applying 1 Jan 2025** | "**Reasonably confident** — verify" |
| **The 2024/25 Solvency II review** | Real, but **not confident of its citation or application date**. EIOPA material on differential pricing: **verify instrument and date** |
| **BetrVG § 90; Betriebsrätemodernisierungsgesetz (2021); § 80(3); § 95** | **Verify the precise provisions** |
| **EU Pay Transparency Directive threshold** | Joint-pay-assessment trigger recollected as **5 %** — **verify threshold and mechanics**. The 7 June 2026 deadline is (confident) |
| **AI Act Annex III application date** | Scheduled from **2 August 2026** ("reasonably confident") — *this semester* — **but simplification/delay proposals were under discussion in late 2025 and the outcome is unknown.** [Ind]'s own slide wording: "from August 2026, subject to the current state of the EU's simplification package". No unqualified date |
| **Ph. Eur. 2.2.40; ICH Q2(R2) / Q14 (adopted 2023)** | "**Reasonably confident on both; verify** the chapter and reference numbers" |
| **EMA/CHMP multiplicity guideline reference number** | **Verify** |
| **German TDDDG** (renamed TTDSG, effective May 2024) | "**Reasonably confident on the rename; verify**" |
| **Machinery Regulation (EU) 2023/1230, applying Jan 2027**, addressing self-evolving behaviour | "**Reasonably confident; verify**" |
| **CSDDD, Directive (EU) 2024/1760** | Confident it exists; **under omnibus revision in 2025 — verify status** |
| **Statlog German Credit's 5:1 cost ratio** | **Verify on the UCI page** before building an exercise on it |
| **`chapter_10.tex:194,745`** "many AI imaging devices are cleared by regulators" | Flagged as the one place the layer "sounds like it is avoiding a fact it does not have"; the MDR anchor above replaces the hedge |

**Non-regulatory items not verified:** an actual Colab runtime; the sklearn version at which ch05 broke
(only 1.6.1 and 1.9.0 tested); Windows and Linux install sizes (PyPI metadata, not runs); anything in
`Mock_Exams/` by [Lab]. And **all four reviews warn that line numbers may have drifted** — the repository
was being edited during every one of them (HEAD moved from `2e1e1f2` to `1ad1891` mid-session). Search on
the quoted string, not the line number.

---

## 8. Already sound — examined, no action needed

- **Exam architecture.** Single `.tex` per paper with a `\withsolutions` toggle, so paper and solutions
  cannot diverge; every problem names its deck and lecture; instructions, rounding tolerance and
  "points ≈ minutes" consistent across all eight; review decks split solution frames before overflow.
- **Exam numeric correctness.** Every arithmetic answer [Ass] read across all eight papers recomputed and
  correct. `docs/exams.md:12`'s claim of programmatic verification holds.
- **The three final variants are genuinely parallel** — same seven problems, same 16/8/20/16/20/20/20
  allocation, same cognitive profile. Usable for seating variants and resits.
- **The five short exams are the healthiest part of the assessment corpus**, correctly sequenced (each P3
  at the frontier chapter, P1/P2 revisiting earlier material). Short D P1 is "the best-designed problem in
  the whole set". No case to answer on over-assessment.
- **`slide_index.md` and the repo's arithmetic** — byte-identical to regeneration from the committed PDFs;
  every figure in README and docs cross-checks. Only gap: nothing validates the runsheets (row 10).
- **The `load()` helper** (cell 4 of all fifteen): ISLP → R-datasets → local CSV → official URL →
  GitHub-raw, every URL verified 200. Row 18 normalises its output; it does not redesign it.
- **Notebook hygiene and cross-version robustness** — sequential execution counts, stored outputs, zero
  error/stderr outputs; 173 of 202 cells byte-identical across a three-year stack jump.
- **The interpretation prose** (`chapter_06_lab` c26, `chapter_02_lab` c28, `chapter_05_lab` c24,
  `chapter_07_lab` c27). Do not touch except where a number went stale.
- **Deck/notebook division of labour** — decks carry 20–35 % of the notebook's code. Right ratio; only the
  pointers need work (row 26).
- **The three two-session split points** (`semester_plan.md:42-46`) — [Cur] looked for a better break in
  each and did not find one.
- **The appendix mechanism** — twelve frames each naming the main-flow substitute; the three likeliest quiet
  burials stress-tested and holding. Two caveats only, at §6.3.
- **Notation discipline** — a "Notation in this chapter" table opening every deck, and `chapter_01` p. 40
  carrying *n*, *p*, the design matrix, hats and the tr/te subscripts on one slide.
- **The "Decision rules of thumb" closer**, in all ten chapter decks — the slide a practitioner keeps.
- **`before_class.md`** — fifty-five lines, no filler, anticipating the failure modes that actually happen.
  [Cur]: "I would not change a line."
- **The depth-case template** (six fields, twelve times, no drift) and especially **the "who signs off"
  field**, which correctly identifies that the analyst is not the decision-maker. The reason the industry
  layer is salvageable rather than rewritable.
- **Out-of-sample and out-of-time discipline**, reinforced five times (`chapter_02.tex:811–815`,
  `chapter_05.tex:287–290`, `:674–678`, `:1425–1429` "never report the tuned CV score to a steering
  committee", `chapter_08.tex:899–901`). The thing most courses get wrong.
- **The tabular reality check** (`chapter_10.tex:176–182`) and the right amount of MLOps for this audience
  (`chapter_10.tex:998–1002`). Add nothing to either.
- **The figure palette** — three disciplined colours, no colormaps, no `jet`, no red/green pairs, colour
  paired with linestyle and label. Only the *sizes* need work (row 24).
- **The `Makefile`'s design** and the figure-stamp mechanism.
- **Gitignoring `Mock_Exams/` and `Teaching_Guide/runsheets/`** — correct, and the rationale accurate. The
  fix is not to publish them; it is row 16.
- **In-deck exercise provision** — 127 exercises, each with a worked solution frame, and a cognitive mix
  *better* than the exams'. [Ass]: "The teaching material is not the problem."

---

## 9. Cut — value does not justify effort

- **Binder** — 2–5 min cold starts, fragile with `torch`, and Colab already works free.
- **A CI link checker** — 15 Colab URLs return 405 to HEAD and 200 to GET; permanent false failures.
- **Hard-pinning the whole stack, or per-cell tolerances** — 86 % of outputs are stable across three years.
- **A taught SVM session / Chapter 9 deck** — your own `chapter_08.tex:219` says boosted trees are the
  default for wide mixed-type tabular data; 180 min on the kernel trick buys less than anything else here.
- **A taught Chapter 11 (survival)** — real business content, but the most self-contained chapter in ISLP;
  self-study breaks nothing.
- **Rebuilding `chapter_09_lab` and `chapter_11_lab` to the taught standard (15 h)** — cut in favour of the
  2-hour relabel (row 21); fold Ch 12 into A2 instead.
- **Power BI / dashboards** — poor fit for a statistics module, expensive to support, competes with nothing
  you teach. Name the CV gap to students and point at where to close it; do not absorb it.
- **Cloud and MLOps** — lowest value per hour for a cohort who will be stakeholders of a pipeline, not
  owners. `chapter_10.tex:998–1002` is already exactly enough. "Resist."
- **Firm data in the graded project** — NDA, GDPR basis, probably a processing agreement, works-council
  involvement if employees are touched, and the data cannot be published, which breaks the open-repo model
  the course is built on. Route it to a single in-class demo you run yourself, or to Bachelor theses.
- **The German electricity-load project variant** (SMARD + DWD) — best data-quality lesson available (the
  DST changeover with its duplicated 02:00–03:00 hour) but you must pin a snapshot and marking variance
  rises. Offer it to two or three ambitious groups, or to the follow-on module.
- **Tagged/accessible PDFs** — deferred, not cut: 4 h, but there is no shared preamble, so every preamble
  change is a 12-file change. Extract a `.sty` first (~2 h, worth doing anyway) and revisit.
- **Untracking the deck PDFs / rewriting history** — deferred: 96 MB clone in 5.7 s, though ~175 MB of
  history is already deck-PDF blobs growing ~200 MB per semester. Cheap move now: add `--depth 1` to the
  documented clone command (35 MB). `docs/conf.py:62-65` already publishes all twelve decks to Pages, so
  students never need the tracked copies.
- **Alumni-sourced case sheets** — keep, but budget 2–3 usable cases a year, each needing a rewrite. Its
  value is not volume: "an HSBI graduate three years out does this" is the most persuasive sentence
  available in Lecture 1.

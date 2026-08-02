# Semester plan

Thirteen sessions of 180 minutes: a **taught precourse session** drawing on both
precourse decks, then **ten ISLP chapters** in book order. The plan is keyed to
chapter numbers, not session numbers. Chapters 9 (support vector machines),
11 (survival analysis) and 13 (multiple testing) are no longer taught in the
sequence — they keep their decks and labs as self-study modules A5, A6 and A7
under [`../Chapters/Advanced/`](../Chapters/Advanced/). The module is 6 ECTS,
graded by one 120-minute written exam at the end of the semester; every paper in
the calendar below is practice.

The precourse decks run to 157 slides in their main flow (106 + 51), so the one
session is a selection — set up notation, standard errors and the lab Python
patterns, and leave both decks with the cohort as the reference.

Slide counts below are live figures from the compiled decks, written
**main flow + appendix**; the per-session detail is in
[`runsheets/`](./runsheets/). For the three decks that span
two sessions the column gives the pages taught in that session instead; their
appendices (`chapter_02` +8, `chapter_03` +11, `chapter_04` +43) sit outside
both halves. Every deck ends with an appendix holding the optional, more
advanced material (formal derivations, the heaviest worked exercises, side
topics); the timed plans in the runsheets cover the main flow only, so the
appendix pages are extra material to assign, not to teach.

## The thirteen sessions

| Chapter | Session | Deck | Slides | Exercises | Notes |
|:--:|---|---|:--:|:--:|---|
| **0 + 0b** | Precourse *(taught, one session)* | `chapter_00` + `chapter_00b` | 106 + 16, 51 + 9 | 10 + 4, 6 + 2 | 157 main-flow slides across the two: teach a selection (notation, standard errors, the lab Python patterns), leave both decks as the cohort's reference |
| **1 + 2** | Introduction + Statistical Learning I | `chapter_01`, `chapter_02` | 71, then pp. 1–42 | 3 + 1, then 2.1–2.2 | Stop after "regression vs. classification" |
| **2** | Statistical Learning II | `chapter_02` | pp. 43–107 | 2.3–2.8 | Accuracy, bias–variance, Bayes classifier, KNN, lab |
| **3** | Linear Regression I | `chapter_03` | pp. 1–76 | 3.1–3.6 | Stop after multiple regression and the four questions |
| **3** | Linear Regression II | `chapter_03` | pp. 77–144 | 3.7–3.12 | **Mock Exam 1 after this week** |
| **4** | Classification I | `chapter_04` | pp. 1–42 | 4.1–4.4 | Logistic regression end to end; stop after the section, before evaluation |
| **4** | Classification II | `chapter_04` | pp. 43–82 | 4.8–4.10 | Confusion matrix, ROC/AUC, lab (LDA/QDA and naive Bayes are appendix material) · **release Short Exam A** |
| **5** | Resampling | `chapter_05` | 79 + 7 | 6 + 3 | Validation set, LOOCV, k-fold, bootstrap · **release Short Exam B** |
| **6** | Model Selection & Regularisation | `chapter_06` | 81 + 11 | 7 + 3 | **Mock Exam 2 after this week** · **release Short Exam C** |
| **7** | Beyond Linearity | `chapter_07` | 85 + 7 | 6 + 3 | Polynomials, splines, GAMs |
| **8** | Tree-Based Methods | `chapter_08` | 83 + 7 | 7 + 3 | Trees, bagging, forests, boosting · **release Short Exam D** |
| **10** | Deep Learning | `chapter_10` | 75 + 8 | 6 + 3 | MLPs, backprop, CNNs (PyTorch) |
| **12** | Unsupervised Learning | `chapter_12` | 91 + 9 | 6 + 3 | PCA, K-means, hierarchical clustering · **final mock exam after this week** · **release Short Exam E** |

Ten ISLP chapters are taught, in book order. Chapters 9, 11 and 13 keep their
full decks and labs but sit outside the plan as advanced modules A5, A6 and A7.
Short Exam E and the final mock still carry a multiple-testing problem, which
now draws on module A7 rather than on a taught session.

## The three splits, and where to break them

Three decks span two sessions. The split points are chosen so you can stop and
resume without a dangling thread:

| Deck | Break after | Because |
|---|---|---|
| `chapter_02` | "regression vs. classification" (p. 42) | Part 1 is the framing — what *f* is, and how flexible to make it; assessing accuracy, bias–variance and KNN open part 2 |
| `chapter_03` | multiple regression and the four questions (p. 76) | Part 1 is estimation and inference; part 2 is everything that complicates it |
| `chapter_04` | the end of the logistic-regression section (p. 42) | Part 1 is the model itself — fitting, interpreting, confounding; part 2 is judging any classifier: confusion matrix, ROC/AUC, and the lab |

## If you are behind

Falling behind is normal — the decks carry more than a session holds. The first
cut has already been made for you: each deck's appendix (formal derivations, the
heaviest exercises, side topics) is outside the timed plan. After that, in order
of what to sacrifice:

1. **Extended exercises.** Set them as homework; the solutions are in the deck,
   so students are not stranded.
2. **The second worked example** of a concept, when the deck gives two.
3. **The "where this reappears in the course" slides.** Valuable, but they are
   signposting, not content.
4. **The closing summary block** (vocabulary, self-check, five things). Tell
   students to read it — it is written to be readable alone.

Do **not** cut: the motivation slide that opens a topic, the pitfalls
(`alertblock`) slides, or any exercise the runsheet marks as exam-relevant.

## Practice rhythm

Two layers. The **three mock exams** are the full-length rehearsals, matched to
the shape of the real paper. The **five 60-minute short exams** in
`Mock_Exams/Short_Exams_60min/` are the formative layer: shorter, sequenced, and
handed out one at a time as the material each needs is taught.

| After | Paper | Covers | Length |
|:--:|---|---|:--:|
| Lecture 4 | Mock Exam 1 | Ch 1–3 | 90 min · 90 pts |
| Lecture 6 | Short Exam A | Ch 0 + 1–2 · Ch 3 · **Ch 4** | 60 min · 60 pts |
| Lecture 7 | Short Exam B | Ch 2 · Ch 3 · **Ch 5** | 60 min · 60 pts |
| Lecture 8 | Mock Exam 2 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Lecture 8 | Short Exam C | Ch 0 + 0b · Ch 3 · **Ch 6** | 60 min · 60 pts |
| Lecture 10 | Short Exam D | Ch 2 + 5 · Ch 2 + 4 · **Ch 8** | 60 min · 60 pts |
| Lecture 15 | Final Mock Exam | All, weighted to Ch 7/8/10/13 | 120 min · 120 pts |
| Lecture 15 | Short Exam E | Ch 0 · Ch 5 + 7 · **Ch 13** | 60 min · 60 pts |

Every paper exists as questions, worked solutions, and a review deck for going
through it in class; the final also comes in three parallel variants
(A / B / C). All of it is **git-ignored**: assessment material stays off the
public repository.

**Distribution:** the worked solutions go out **together with the paper**. Say so
when you hand it over, and say why — the paper is only diagnostic if it is
attempted closed-book first, and once the solutions are open that discipline is
the student's to keep. The review deck is what the session itself runs on.

### The five short exams are sequenced, not interchangeable

Each is three problems × 20 points, increasing in difficulty. The bold chapter
above is where the third and hardest problem sits — so **A cannot be set before
Chapter 4, B before Chapter 5, C before Chapter 6, D before Chapter 8, or E
before Chapter 13.** The first two problems deliberately reach back to earlier
chapters, which makes each paper cumulative-to-date rather than a
single-chapter test. They are also the only papers that assess the **precourse**
material at all: A, C and E each open on Chapter 0 / 0b, whereas no problem in
the three main papers cites either precourse deck.

This is what to give the student who has fallen behind: a 60-minute paper they
can sit alone at the natural checkpoint, with a full worked solution behind it.
The short exams also carry the only **grading keys, per-sub-part mark
allocations and marking tables** in the whole assessment set, so they are the
easiest papers to mark consistently — and the review decks add a "common
mistake" box per problem. The *Before you walk in* checklist in
`runsheets/lecture_04.md`, `lecture_05.md`, `lecture_06.md`, `lecture_08.md` and
`lecture_13.md` names the paper released after that session, and
`Mock_Exams/Short_Exams_60min/README.md` lists what is in each.

`make exams` rebuilds all 18 of the mock-exam PDFs on a machine that has them —
the three papers and the three final variants, each as questions and as
solutions, plus all six review decks (two `pdflatex` passes each, for the
navigation bar). The five short exams are not part of that target: they have
their own `./build.sh` next to the sources, which produces their 15 PDFs
(paper, solutions and review deck for each).

## Workload for students

Per week, beyond the session itself: one lab notebook (60–90 min), the short
exercises from the deck they did not do in the room (30 min), and reading the
chapter. The labs are the part that matters — a student who runs every notebook
will pass; one who only reads slides will not.

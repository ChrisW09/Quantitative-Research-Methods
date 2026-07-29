# Semester plan

Twelve sessions of 180 minutes, plus two optional precourse sessions. Slide
counts are live figures from the compiled decks; the per-session detail is in
[`runsheets/`](./runsheets/).

Slide counts are written **main flow + appendix**. For the three decks that span
two sessions the column gives the pages taught in that session instead; their
appendices (`chapter_02` +8, `chapter_03` +11, `chapter_04` +15) sit outside
both halves. Every deck ends with an appendix holding the optional, more
advanced material (formal derivations, the heaviest worked exercises, side
topics); the timed plans in the runsheets cover the main flow only, so the
appendix pages are extra material to assign, not to teach.

## The twelve weeks

| Week | Session | Deck | Slides | Exercises | Notes |
|:--:|---|---|:--:|:--:|---|
| — | Precourse (a) | `chapter_00` | 106 + 16 | 10 + 4 | Optional. Statistics refresher |
| — | Precourse (b) | `chapter_00b` | 51 + 9 | 6 + 2 | Optional. Notation, logs & odds, likelihood, Python |
| 1 | Introduction + Statistical Learning I | `chapter_01`, `chapter_02` | 71, then pp. 1–42 | 3 + 1, then 2.1–2.2 | Stop after "regression vs. classification" |
| 2 | Statistical Learning II | `chapter_02` | pp. 43–107 | 2.3–2.8 | Accuracy, bias–variance, Bayes classifier, KNN, lab |
| 3 | Linear Regression I | `chapter_03` | pp. 1–76 | 3.1–3.6 | Stop after multiple regression and the four questions |
| 4 | Linear Regression II | `chapter_03` | pp. 77–144 | 3.7–3.12 | **Mock Exam 1 after this week** |
| 5 | Classification I | `chapter_04` | pp. 1–46 | 4.1–4.4 | Stop after the Bayes-theorem framing, before LDA |
| 6 | Classification II | `chapter_04` | pp. 47–112 | 4.5–4.10 | LDA/QDA, naive Bayes, ROC, lab |
| 7 | Resampling | `chapter_05` | 79 + 7 | 6 + 3 | Validation set, LOOCV, k-fold, bootstrap |
| 8 | Model Selection & Regularisation | `chapter_06` | 81 + 11 | 7 + 3 | **Mock Exam 2 after this week** |
| 9 | Beyond Linearity | `chapter_07` | 85 + 7 | 6 + 3 | Polynomials, splines, GAMs |
| 10 | Tree-Based Methods | `chapter_08` | 83 + 7 | 7 + 3 | Trees, bagging, forests, boosting |
| 11 | Deep Learning | `chapter_10` | 75 + 8 | 6 + 3 | MLPs, backprop, CNNs (PyTorch) |
| 12 | Multiple Testing | `chapter_13` | 63 + 6 | 5 + 3 | **Final mock exam after this week** |

Chapters **9 (SVM)**, **11 (Survival)** and **12 (Unsupervised)** are not
taught; they ship as self-study notebooks for students who want them.

## The three splits, and where to break them

Three decks span two sessions. The split points are chosen so you can stop and
resume without a dangling thread:

| Deck | Break after | Because |
|---|---|---|
| `chapter_02` | "regression vs. classification" (p. 42) | Part 1 is the framing — what *f* is, and how flexible to make it; assessing accuracy, bias–variance and KNN open part 2 |
| `chapter_03` | multiple regression and the four questions (p. 76) | Part 1 is estimation and inference; part 2 is everything that complicates it |
| `chapter_04` | the Bayes-theorem framing, before LDA (p. 46) | Part 1 is one method done properly; part 2 is the alternatives and how to compare them |

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

## Assessment rhythm

| After | Exam | Covers | Length |
|:--:|---|---|:--:|
| Lecture 4 | Mock Exam 1 | Ch 1–3 | 90 min · 90 pts |
| Lecture 8 | Mock Exam 2 | Ch 4–6 (+ light cumulative) | 90 min · 90 pts |
| Lecture 12 | Final Mock Exam | All, weighted to Ch 7/8/10/13 | 120 min · 120 pts |

Each exists as questions, worked solutions, and a review deck for going through
it in class; the final also comes in three parallel variants (A / B / C). They
are **git-ignored**: assessment material stays off the public repository.

`make exams` rebuilds all 18 of those PDFs on a machine that has them — the
three papers and the three final variants, each as questions and as solutions,
plus all six review decks (two `pdflatex` passes each, for the navigation bar).
The five 60-minute short exams in `Mock_Exams/Short_Exams_60min/` are not part
of that target: they have their own `./build.sh` next to the sources.

## Workload for students

Per week, beyond the session itself: one lab notebook (60–90 min), the short
exercises from the deck they did not do in the room (30 min), and reading the
chapter. The labs are the part that matters — a student who runs every notebook
will pass; one who only reads slides will not.

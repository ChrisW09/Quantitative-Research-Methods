# Generator for the Quantitative Research mock exams

The files `Mock_Exam_N.tex`, `Mock_Exam_N_Solutions.tex` and `Mock_Exam_N_Slides.tex`
in `Mock_Exam_N/` and the three PDFs next to them are generated from one source.
**Changes made directly in the .tex files are lost on the next run** -- edit
`spec_qrmN.py` instead. (English port of the generator of the course
*Statistik für Ökonomen*.)

## Files

| File | Content |
|---|---|
| `spec_qrm1.py` | Content of Mock Exam 1: scenarios, 3 x 10 subtasks with question, result, grading rubric, worked solution, typical mistakes, slide content |
| `templates.py` | LaTeX preambles (exam, solutions, slides), cover-page rules, $\Phi$-table and $t$-table (computed with SciPy) |
| `build.py` | Writes the three .tex files incl. results overview, runs the checks, compiles the PDFs |
| `figures.py` | All figures (`Mock_Exam_1/qrm1_*.pdf`), matplotlib with the colour palette of the lecture |
| `verify.py` | Recomputes every result independently and compares it with the text of the spec |
| `data_qrm1_cafe60.csv` | The 60 café days behind the `statsmodels` output in Task 2 (Part B) |

## Usage

```bash
cd _Generator
python3 figures.py        # figures
python3 verify.py         # recompute all 30 results (exit code 1 on any mismatch)
python3 build.py          # all mock exams: .tex, checks, PDFs
python3 build.py 1        # only Mock Exam 1
python3 build.py 1 --tex-only   # .tex and checks, no compilation
```

`build.py` compiles with `latexmk -pdf` (aux files in a temporary `_build/`
folder that is removed afterwards) and saves

- `Quantitative Research Mock Exam 1.pdf` (exam),
- `Quantitative Research Mock Exam 1 Solutions.pdf` (solutions and grading key),
- `Quantitative Research Mock Exam 1 Slides.pdf` (Beamer slides for the discussion).

Requirements: Python 3 with numpy, pandas, scipy, statsmodels, matplotlib; TeX Live.

## Conventions

* 3 tasks x 10 subtasks x **2 points** = 60 points, 120 minutes; Task 1 = Part 3
  (statistical inference), Task 2 = Part 4 (regression), Task 3 = Part 5 (classification).
* Every subtask can be solved **independently**: no intermediate result of another
  subtask is needed; all values are stated in the subtask itself.
* Exactly **one** result per subtask. The exam has **no answer boxes**: students write
  working and result on the correction-margin pages after each task. One-sentence answers
  are marked `kind="satz"`; at most 3 per task.
* **Python in every task:** exactly one Python-command subtask (`python=True`, "Give the
  ... command that ...") and one simple code-reading subtask (`pycode=True`, "Which value
  does the following line return / show?"; the line itself goes into the field `code` and is
  printed on its own indented line below the question). Use only commands that appear on
  the lecture slides; `verify.py` runs every one of them, the `code` lines verbatim.
* Notation as in the lecture decks: $N(\mu,\sigma^2)$, $Z_n$, $z_{1-\alpha/2}$,
  $t_{0.975;\,\mathrm{df}}$, $\hat\beta_0$, $\hat\beta_1$, $S_{xx}$, $S_{xy}$, TSS/ESS/RSS,
  $\hat\eta$, odds ratio $e^{\beta_j}$, TP/TN/FP/FN.

## Checks in the build

`build.py` checks every exam and reports

* tasks that do not have exactly 10 subtasks, missing fields
  (`label`, `q`, `short`, `result`, `rubric`, `solution`),
* wording that asks for **more than one result** ("... and give ...",
  "... and explain ...", "... then ...", "commands", "critical values",
  two calculation verbs in one sentence),
* **back-references** to other subtasks ("from part b)", "computed above",
  "your result" ...),
* more than 3 one-sentence answers, more than one Python-command subtask or more than one
  Python code-reading subtask per task,
* LaTeX errors, undefined references and overfull boxes > 1 pt.

A clean run prints `Check OK: 3 x 10 subtasks, one requested result each, no
back-references` and `LaTeX OK: 3 PDFs, 0 errors, no overfull boxes > 1pt`;
otherwise the findings are listed and the script ends with exit code 1.

Deliberate exceptions: the **hypothesis pair** ($H_0$ vs. $H_1$) and the
**confidence interval** ($[a;\ b]$) each count as one result.

---
myst:
  html_meta:
    description: "How the repository is organised — one self-contained folder per chapter holding its deck and its lab, what is committed, what is git-ignored and why, and the naming conventions."
---

# Repository layout

**Everything for one chapter lives in one folder.** The deck, its compiled PDF,
its figures and the companion lab notebook sit side by side, so teaching or
adapting a chapter means opening a single directory rather than tracking one
file across two trees. The advanced modules and the projects follow the same
shape.

```text
.
├── Chapters/                        # one folder per ISLP chapter — deck + lab together
│   ├── README.md                    #   deck guide: design, exercise counts, lecture plan
│   ├── chapter_NN/
│   │   ├── chapter_NN.tex           #   deck source
│   │   ├── chapter_NN.pdf           #   compiled deck (committed)
│   │   ├── chapter_NN_lab.ipynb     #   companion lab, with stored outputs
│   │   ├── images/                  #   matplotlib figures used by the deck
│   │   └── make_figures.py          #   (chapter_00, chapter_00b) regenerates them
│   └── Advanced/                    #   four optional self-study modules, same shape
│       ├── README.md
│       ├── STYLE_DECK.md            #   the house style, distilled, for a new module
│       ├── STYLE_NOTEBOOK.md
│       └── advanced_NN_topic/
│           ├── advanced_NN_topic.tex
│           ├── advanced_NN_topic.pdf
│           ├── advanced_NN_topic_lab.ipynb   #  deck, PDF, lab, figures — as above
│           ├── images/
│           └── make_figures.py
├── Projects/                        # six short projects: a decision on real data
│   ├── README.md
│   └── project_N_slug/
│       ├── README.md                #   the brief the student reads
│       ├── project_N_starter.ipynb  #   Colab-ready scaffolding
│       └── SOLUTION_NOTES.md        #   expected findings, the trap, marking guide
├── Teaching_Guide/                  # instructor kit: plan, index, checklist, handouts
│   ├── semester_plan.md             #   the thirteen weeks on one page
│   ├── slide_index.md               #   generated: sections, exercises, page numbers
│   ├── before_class.md              #   the ten-minute pre-lecture checklist
│   ├── deck_triage_proposal.md      #   audit: what could become appendix material
│   ├── runsheets/                   #   per-session scripts — git-ignored (assessment)
│   └── handouts/                    #   printable 2-up decks — build output
├── Mock_Exams/                      # eight papers — git-ignored (assessment material)
├── ALL CSV FILES - 2nd Edition/     # course datasets (statlearning.com)
├── docs/                            # this documentation (Sphinx)
├── Source_Material/                 # copyrighted book PDFs & figure banks — git-ignored
├── Makefile                         # one-command rebuild: figures, decks, index, handouts
├── requirements.txt                 # pinned Python environment for the notebooks
├── CITATION.cff                     # how to cite these materials
└── README.md
```

```{admonition} Three chapters have a lab but no deck
:class: note

`chapter_09`, `chapter_11` and `chapter_12` (SVM, survival analysis,
unsupervised learning) sit outside the taught plan, so their folders hold a
notebook and nothing else. That is deliberate, not an unfinished build —
`make check` reports them as *no deck (code reference)*.
```

## What is and isn't committed

| | |
|---|---|
| **Committed** | Deck LaTeX sources and compiled PDFs, notebooks with stored outputs, datasets, project briefs and starters, this documentation |
| **Git-ignored** | `Mock_Exams/` and `Teaching_Guide/runsheets/` (assessment material), `Source_Material/` (copyrighted textbook PDF and figure banks), LaTeX build artefacts (`*.aux`, `*.log`, `*.nav`, …), `.venv/`, `.ipynb_checkpoints/`, `Chapters/*/data/`, `docs/_build/`, and the documentation's staged copies (`docs/labs/`, `docs/advanced_labs/`, `docs/_extra/`) |

Compiled deck PDFs *are* committed on purpose: a colleague should be able to
clone the repository and teach from it without a TeX installation. The exams
are the exception — publishing worked solutions to a public repository would
make them useless as assessment.

## Naming conventions

- Chapter numbers always follow **ISLP**, zero-padded to two digits
  (`chapter_04`), so slides, labs and datasets line up. The gaps are intentional:
  chapters 9, 11 and 12 have a notebook but no deck, because they are untaught
  [code references](labs.md) rather than labs.
- Every file in a chapter folder is named for that folder, so a path is
  self-describing and a glob is unambiguous: `chapter_04/chapter_04.tex`,
  `chapter_04/chapter_04_lab.ipynb`. The build scripts rely on this — they find
  decks with `Chapters/chapter_*/chapter_*.tex` and labs with
  `Chapters/chapter_*/chapter_*_lab.ipynb`.
- Exam folders are named for the lecture they follow
  (`Exam_2_after_Lecture_08`), not for a date, so the calendar can shift without
  renaming anything.
- Exam PDFs use `Title_Case`, their LaTeX sources `snake_case` — the `-jobname`
  argument in the build command is what maps one to the other.

## Related reading

- [`Chapters/README.md`](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/Chapters/README.md)
  — the deck guide, with per-chapter exercise counts, the contents of each
  deck's appendix, and the full lecture plan.
- [Teaching it](teaching.md) — the instructor kit and the `make` targets.
- [Building the docs](building-docs.md) — how this site is assembled.

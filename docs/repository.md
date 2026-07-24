# Repository layout

```text
.
├── Lecture_Slides/            # twelve Beamer decks — the core deliverable
│   ├── README.md              #   deck guide: design, exercise counts, 12-lecture plan
│   └── chapter_NN/
│       ├── chapter_NN.tex     #   source
│       ├── chapter_NN.pdf     #   compiled deck (committed)
│       ├── images/            #   matplotlib figures used by the deck
│       └── make_figures.py    #   (chapter_00, chapter_00b) regenerates figures
├── Lab_Notebooks/             # fifteen Jupyter labs, local- and Colab-ready
│   └── chapter_NN_lab.ipynb
├── Teaching_Guide/            # instructor kit: plan, index, checklist, handouts
│   ├── semester_plan.md       #   the twelve weeks on one page
│   ├── slide_index.md         #   generated: sections, exercises, page numbers
│   ├── before_class.md        #   the ten-minute pre-lecture checklist
│   ├── runsheets/             #   per-session scripts — git-ignored (assessment)
│   └── handouts/              #   printable 2-up decks — build output
├── Mock_Exams/                # three exams — git-ignored (assessment material)
├── ALL CSV FILES - 2nd Edition/   # course datasets (statlearning.com)
├── docs/                      # this documentation (Sphinx)
├── Source_Material/           # copyrighted book PDFs & figure banks — git-ignored
├── Makefile                   # one-command rebuild: figures, decks, index, handouts
├── requirements.txt           # pinned Python environment for the notebooks
├── CITATION.cff              # how to cite these materials
└── README.md
```

## What is and isn't committed

| | |
|---|---|
| **Committed** | Deck LaTeX sources and compiled PDFs, notebooks with outputs, datasets, this documentation |
| **Git-ignored** | `Mock_Exams/` (assessment material — exams, solutions and their sources), `Source_Material/` (copyrighted textbook PDF and figure banks), LaTeX build artefacts (`*.aux`, `*.log`, `*.nav`, …), `.venv/`, `.ipynb_checkpoints/`, `Lab_Notebooks/data/`, `docs/_build/`, and the documentation's staged copies (`docs/labs/`, `docs/_extra/`) |

Compiled deck PDFs *are* committed on purpose: a colleague should be able to
clone the repository and teach from it without a TeX installation. The exams
are the exception — publishing worked solutions to a public repository would
make them useless as assessment.

## Naming conventions

- Chapter numbers always follow **ISLP**, zero-padded to two digits
  (`chapter_04`), so slides, labs and datasets line up. The gaps (9, 11, 12 have
  labs but no deck) are intentional — those chapters are self-study.
- Exam folders are named for the lecture they follow
  (`Exam_2_after_Lecture_08`), not for a date, so the calendar can shift without
  renaming anything.
- Exam PDFs use `Title_Case`, their LaTeX sources `snake_case` — the `-jobname`
  argument in the build command is what maps one to the other.

## Related reading

- [`Lecture_Slides/README.md`](https://github.com/ChrisW09/Quantitative-Research-Methods/blob/main/Lecture_Slides/README.md)
  — the deck guide, with per-chapter exercise counts, the contents of each
  deck's appendix, and the full lecture plan.
- [Teaching it](teaching.md) — the instructor kit and the `make` targets.
- [Building the docs](building-docs.md) — how this site is assembled.

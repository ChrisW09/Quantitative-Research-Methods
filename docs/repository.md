# Repository layout

```text
.
├── Lecture_Slides/            # eleven Beamer decks — the core deliverable
│   ├── README.md              #   deck guide: design, exercise counts, 12-lecture plan
│   └── chapter_NN/
│       ├── chapter_NN.tex     #   source
│       ├── chapter_NN.pdf     #   compiled deck (committed)
│       ├── images/            #   matplotlib figures used by the deck
│       └── make_figures.py    #   (chapter_00 only) regenerates its figures
├── Lab_Notebooks/             # fourteen Jupyter labs, local- and Colab-ready
│   └── chapter_NN_lab.ipynb
├── Mock_Exams/                # three exams, each in three formats
│   ├── Exam_1_after_Lecture_04/
│   ├── Exam_2_after_Lecture_08/
│   └── Final_Exam_after_Lecture_12/
├── ALL CSV FILES - 2nd Edition/   # course datasets (statlearning.com)
├── docs/                      # this documentation (Sphinx)
├── Source_Material/           # copyrighted book PDFs & figure banks — git-ignored
├── requirements.txt           # pinned Python environment for the notebooks
├── CITATION.cff              # how to cite these materials
└── README.md
```

## What is and isn't committed

| | |
|---|---|
| **Committed** | LaTeX sources, compiled deck and exam PDFs, notebooks with outputs, datasets, this documentation |
| **Git-ignored** | `Source_Material/` (copyrighted textbook PDF and figure banks), LaTeX build artefacts (`*.aux`, `*.log`, `*.nav`, …), `.venv/`, `.ipynb_checkpoints/`, `Lab_Notebooks/data/`, `docs/_build/`, and the documentation's staged copies (`docs/labs/`, `docs/_extra/`) |

Compiled PDFs *are* committed on purpose: a colleague should be able to clone
the repository and teach from it without a TeX installation.

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
  — the deck guide, with per-chapter exercise counts and the full lecture plan.
- [Building the docs](building-docs.md) — how this site is assembled.

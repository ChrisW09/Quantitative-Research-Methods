"""Sphinx configuration for the Quantitative Research Methods course docs.

The course materials live outside ``docs/`` (notebooks in ``Lab_Notebooks/``,
compiled decks in ``Lecture_Slides/``, exams in ``Mock_Exams/``).  Sphinx can
only read sources from inside the source directory, so before the build starts
we stage what the site needs:

* ``Lab_Notebooks/*.ipynb``   -> ``docs/labs/``     (rendered by myst-nb)
* deck and exam PDFs         -> ``docs/_extra/``   (copied verbatim into the
                                                    HTML output via
                                                    ``html_extra_path``)

Both staging directories are generated and git-ignored; nothing is edited in
place and no source file is ever written back to.
"""

from __future__ import annotations

import shutil
from pathlib import Path

# -- Paths --------------------------------------------------------------------

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent

LABS_SRC = ROOT / "Lab_Notebooks"
LABS_DST = HERE / "labs"

EXTRA = HERE / "_extra"

# Chapters that have a compiled lecture deck ("00" is the precourse refresher).
SLIDE_CHAPTERS = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "10", "13"]

# Exam PDFs: (folder under Mock_Exams/, list of PDF stems).
EXAM_FILES = [
    (
        "Exam_1_after_Lecture_04",
        ["Mock_Exam_1", "Mock_Exam_1_Solutions", "Mock_Exam_1_Solutions_Slides"],
    ),
    (
        "Exam_2_after_Lecture_08",
        ["Mock_Exam_2", "Mock_Exam_2_Solutions", "Mock_Exam_2_Solutions_Slides"],
    ),
    (
        "Final_Exam_after_Lecture_12",
        [
            "Final_Mock_Exam",
            "Final_Mock_Exam_Solutions",
            "Final_Mock_Exam_Solutions_Slides",
            "Final_Mock_Exam_A",
            "Final_Mock_Exam_A_Solutions",
            "Final_Mock_Exam_B",
            "Final_Mock_Exam_B_Solutions",
            "Final_Mock_Exam_C",
            "Final_Mock_Exam_C_Solutions",
        ],
    ),
]


def _copy(src: Path, dst: Path) -> bool:
    """Copy ``src`` to ``dst`` (creating parents). Returns False if missing."""
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def stage_materials(app=None, config=None) -> None:
    """Copy notebooks and PDFs into the source tree before the build."""
    missing: list[str] = []

    # Notebooks -> docs/labs/
    if LABS_DST.exists():
        shutil.rmtree(LABS_DST)
    LABS_DST.mkdir(parents=True, exist_ok=True)
    for nb in sorted(LABS_SRC.glob("chapter_*_lab.ipynb")):
        shutil.copy2(nb, LABS_DST / nb.name)

    # Lecture decks -> docs/_extra/slides/
    if EXTRA.exists():
        shutil.rmtree(EXTRA)
    for ch in SLIDE_CHAPTERS:
        name = f"chapter_{ch}.pdf"
        if not _copy(ROOT / "Lecture_Slides" / f"chapter_{ch}" / name, EXTRA / "slides" / name):
            missing.append(f"Lecture_Slides/chapter_{ch}/{name}")

    # Exams -> docs/_extra/exams/
    for folder, stems in EXAM_FILES:
        for stem in stems:
            if not _copy(
                ROOT / "Mock_Exams" / folder / f"{stem}.pdf", EXTRA / "exams" / f"{stem}.pdf"
            ):
                missing.append(f"Mock_Exams/{folder}/{stem}.pdf")

    EXTRA.mkdir(parents=True, exist_ok=True)  # keep html_extra_path valid

    if missing:
        print(
            "[docs] note: %d PDF(s) not found and will not be linkable: %s"
            % (len(missing), ", ".join(missing[:5]) + (" …" if len(missing) > 5 else ""))
        )


stage_materials()  # also run at import time so `sphinx-build` on a clean tree works


# -- Project information ------------------------------------------------------

project = "Quantitative Research Methods"
author = "Prof. Dr. Christoph Weisser"
copyright = "2026, Christoph Weisser (HSBI). Based on ISLP (Springer, 2023)"
release = "Summer Semester 2026"
version = release

# -- General configuration ----------------------------------------------------

extensions = [
    "myst_nb",            # Markdown sources + notebook rendering
    "sphinx_design",      # grids, cards, tabs
    "sphinx_copybutton",  # copy button on code blocks
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "_extra", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- MyST / MyST-NB -----------------------------------------------------------

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "linkify",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3

# Notebooks are shipped with their outputs; never execute them at build time
# (Chapter 10 needs torch, Chapter 11 lifelines, and several download data).
nb_execution_mode = "off"
nb_merge_streams = True

# -- HTML output --------------------------------------------------------------

html_theme = "furo"
html_title = "Quantitative Research Methods"
html_short_title = "QRM"
html_static_path = ["_static"]
html_extra_path = ["_extra"]
html_css_files = ["custom.css"]
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "source_repository": "https://github.com/ChrisW09/Quantitative-Research-Methods/",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/ChrisW09/Quantitative-Research-Methods",
            "html": (
                '<svg stroke="currentColor" fill="currentColor" stroke-width="0" '
                'viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 '
                "8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01."
                "37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01"
                "1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-."
                "89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.8"
                "2.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.9"
                "2.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.4"
                "8 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.5"
                '8-8-8-8z"></path></svg>'
            ),
            "class": "",
        },
    ],
}

# -- LaTeX / PDF output -------------------------------------------------------

latex_documents = [
    (
        "index",
        "QuantitativeResearchMethods.tex",
        "Quantitative Research Methods",
        author,
        "manual",
    ),
]
latex_elements = {"papersize": "a4paper", "pointsize": "11pt"}


def setup(app):
    """Re-stage materials on every build (including `sphinx-autobuild` reloads)."""
    app.connect("config-inited", stage_materials)
    return {"parallel_read_safe": True, "parallel_write_safe": True}

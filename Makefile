# Quantitative Research Methods — course build
#
#   make            rebuild anything out of date (figures, decks, index)
#   make decks      rebuild every lecture deck that changed
#   make deck-03    rebuild one deck
#   make figures    regenerate the precourse figures from the datasets
#   make handouts   printable 2-up handouts for every deck
#   make index      refresh Teaching_Guide/slide_index.md
#   make docs       build the documentation site locally
#   make exams      rebuild the mock exams (kept out of git)
#   make clean      delete LaTeX build artefacts
#   make check      report page counts and any overfull slides
#
# Requires: TeX Live (beamer, tcolorbox, tikz, listings, booktabs, pdfpages)
# and python3 with the packages in requirements.txt.

CHAPTERS  := 00 00b 01 02 03 04 05 06 07 08 10 13
SLIDEDIR  := Lecture_Slides
GUIDE     := Teaching_Guide
HANDOUTS  := $(GUIDE)/handouts
PYTHON    ?= python3
LATEX     := pdflatex -interaction=nonstopmode -halt-on-error

DECK_PDFS := $(foreach c,$(CHAPTERS),$(SLIDEDIR)/chapter_$(c)/chapter_$(c).pdf)
HANDOUT_PDFS := $(foreach c,$(CHAPTERS),$(HANDOUTS)/chapter_$(c)_handout.pdf)

.PHONY: all decks figures handouts index docs exams clean check help
.DEFAULT_GOAL := all

all: figures decks index

help:
	@sed -n '2,20p' Makefile

# ---------------------------------------------------------------- lecture decks
# A pattern rule may contain only one %, so the per-chapter rules are generated.
# Two LaTeX passes: the second one fills in the section navigation bar.
define DECK_RULE
$(SLIDEDIR)/chapter_$(1)/chapter_$(1).pdf: $(SLIDEDIR)/chapter_$(1)/chapter_$(1).tex
	@echo "  [deck]     chapter_$(1)"
	@cd $(SLIDEDIR)/chapter_$(1) && $(LATEX) chapter_$(1).tex >/dev/null \
	  && $(LATEX) chapter_$(1).tex >/dev/null
endef
$(foreach c,$(CHAPTERS),$(eval $(call DECK_RULE,$(c))))

decks: $(DECK_PDFS)

deck-%:
	@$(MAKE) --no-print-directory $(SLIDEDIR)/chapter_$*/chapter_$*.pdf

# ------------------------------------------------------------- generated figures
# Only the two precourse decks generate their figures from the datasets.
figures:
	@echo "  [figures]  chapter_00, chapter_00b"
	@$(PYTHON) $(SLIDEDIR)/chapter_00/make_figures.py  >/dev/null
	@$(PYTHON) $(SLIDEDIR)/chapter_00b/make_figures.py >/dev/null

# -------------------------------------------------------------------- handouts
define HANDOUT_RULE
$(HANDOUTS)/chapter_$(1)_handout.pdf: $(SLIDEDIR)/chapter_$(1)/chapter_$(1).pdf $(GUIDE)/handout_template.tex
	@echo "  [handout]  chapter_$(1)"
	@mkdir -p $(HANDOUTS)
	@cd $(HANDOUTS) && $(LATEX) -jobname=chapter_$(1)_handout \
	  "\def\deckpath{../../$(SLIDEDIR)/chapter_$(1)/chapter_$(1).pdf}\input{../handout_template.tex}" >/dev/null
endef
$(foreach c,$(CHAPTERS),$(eval $(call HANDOUT_RULE,$(c))))

handouts: $(HANDOUT_PDFS)

# ----------------------------------------------------------------- teaching index
index: $(DECK_PDFS)
	@$(PYTHON) $(GUIDE)/make_index.py

# ------------------------------------------------------------------------- docs
docs:
	@$(PYTHON) -m sphinx -b html -W --keep-going docs docs/_build/html

# ------------------------------------------------------------------------ exams
# Mock_Exams/ is git-ignored; this only works on a machine that has it.
exams:
	@test -d Mock_Exams || { echo "Mock_Exams/ not present (git-ignored)"; exit 1; }
	@cd Mock_Exams/Exam_1_after_Lecture_04 && \
	  $(LATEX) -jobname=Mock_Exam_1 mock_exam_1.tex >/dev/null && \
	  $(LATEX) -jobname=Mock_Exam_1_Solutions "\def\withsolutions{1}\input{mock_exam_1.tex}" >/dev/null
	@cd Mock_Exams/Exam_2_after_Lecture_08 && \
	  $(LATEX) -jobname=Mock_Exam_2 mock_exam_2.tex >/dev/null && \
	  $(LATEX) -jobname=Mock_Exam_2_Solutions "\def\withsolutions{1}\input{mock_exam_2.tex}" >/dev/null
	@cd Mock_Exams/Final_Exam_after_Lecture_12 && \
	  $(LATEX) -jobname=Final_Mock_Exam final_mock_exam.tex >/dev/null && \
	  $(LATEX) -jobname=Final_Mock_Exam_Solutions "\def\withsolutions{1}\input{final_mock_exam.tex}" >/dev/null
	@echo "  [exams]    rebuilt"

# ------------------------------------------------------------------------ checks
check:
	@$(PYTHON) $(GUIDE)/check_decks.py

clean:
	@find $(SLIDEDIR) $(HANDOUTS) -type f \
	  \( -name '*.aux' -o -name '*.log' -o -name '*.nav' -o -name '*.out' \
	  -o -name '*.snm' -o -name '*.toc' -o -name '*.vrb' -o -name '*.fls' \
	  -o -name '*.fdb_latexmk' \) -delete 2>/dev/null || true
	@echo "  [clean]    LaTeX artefacts removed"

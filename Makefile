# Quantitative Research Methods — course build
#
#   make            rebuild anything out of date (figures, decks, index)
#   make decks      rebuild every lecture deck that changed
#   make deck-03    rebuild one deck
#   make figures    regenerate the precourse figures from the datasets
#   make handouts   printable 2-up handouts for every deck
#   make index      refresh Teaching_Guide/slide_index.md
#   make docs       build the documentation site locally
#   make exams      rebuild the mock exam papers, solutions and review decks
#                   (kept out of git; the 60-min set has its own build.sh)
#   make clean      delete LaTeX build artefacts
#   make check      report page counts, overfull slides, and any runsheet whose
#                   slide numbers no longer match its deck
#   make runsheets  the full runsheet report: every page reference in
#                   Teaching_Guide/runsheets/ resolved to its frame title
#                   (kept out of git; skipped if the folder is absent)
#   make notebooks  run all lab notebooks (15 course + 4 advanced) and diff
#                   their output against the outputs stored in them — what CI
#                   does weekly (needs nbclient)
#   make advanced   rebuild the four advanced-module decks (Advanced/)
#
# Requires: TeX Live (beamer, tcolorbox, tikz, listings, booktabs, pdfpages,
# enumitem and mathtools — the last two for the exam papers and review decks)
# and python3 with the packages in requirements.txt. "index", "check" and
# "runsheets" also need Teaching_Guide/requirements.txt (pypdf); "docs" needs
# docs/requirements.txt; "notebooks" needs nbclient, nbformat and ipykernel.

CHAPTERS  := 00 00b 01 02 03 04 05 06 07 08 10 13
SLIDEDIR  := Chapters
GUIDE     := Teaching_Guide
HANDOUTS  := $(GUIDE)/handouts
PYTHON    ?= python3
LATEX     := pdflatex -interaction=nonstopmode -halt-on-error

DECK_PDFS := $(foreach c,$(CHAPTERS),$(SLIDEDIR)/chapter_$(c)/chapter_$(c).pdf)
HANDOUT_PDFS := $(foreach c,$(CHAPTERS),$(HANDOUTS)/chapter_$(c)_handout.pdf)

.PHONY: all decks figures handouts index docs exams clean check runsheets notebooks advanced help
.DEFAULT_GOAL := all

all: figures decks index

# Print the comment header above, however long it grows: line 2 to the first
# blank line. A fixed line range silently starts printing variables instead.
help:
	@sed -n '2,/^$$/p' Makefile

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

# --------------------------------------------------------------- advanced decks
# Four optional self-study modules in Advanced/ — same two-pass LaTeX build,
# kept out of `all` because they are not part of the 12-lecture deliverable.
ADVANCED := advanced_01_rcts advanced_02_shapley advanced_03_conformal advanced_04_glms_splines
ADV_DIR  := Chapters/Advanced
ADV_PDFS := $(foreach a,$(ADVANCED),$(ADV_DIR)/$(a)/$(a).pdf)

define ADV_RULE
$(ADV_DIR)/$(1)/$(1).pdf: $(ADV_DIR)/$(1)/$(1).tex
	@echo "  [deck]     $(1)"
	@cd $(ADV_DIR)/$(1) && $(LATEX) $(1).tex >/dev/null \
	  && $(LATEX) $(1).tex >/dev/null
endef
$(foreach a,$(ADVANCED),$(eval $(call ADV_RULE,$(a))))

advanced: $(ADV_PDFS)

# ------------------------------------------------------------- generated figures
# Only the two precourse decks generate their figures from the datasets. Each
# script writes a whole directory of PNGs at once, so a stamp file stands in for
# them: it keeps the run incremental, and it lets the two decks declare a real
# dependency on their figures. Without that dependency an edited script never
# triggers a rebuild, and `make -j` can compile a deck while a PNG is still
# half-written. (The datasets themselves are not listed: make cannot handle the
# spaces in "ALL CSV FILES - 2nd Edition", and they never change.)
FIG_STAMPS := $(SLIDEDIR)/chapter_00/.figures.stamp \
              $(SLIDEDIR)/chapter_00b/.figures.stamp

$(SLIDEDIR)/chapter_00/.figures.stamp: $(SLIDEDIR)/chapter_00/make_figures.py
	@echo "  [figures]  chapter_00"
	@$(PYTHON) $(SLIDEDIR)/chapter_00/make_figures.py >/dev/null
	@touch $@

$(SLIDEDIR)/chapter_00b/.figures.stamp: $(SLIDEDIR)/chapter_00b/make_figures.py
	@echo "  [figures]  chapter_00b"
	@$(PYTHON) $(SLIDEDIR)/chapter_00b/make_figures.py >/dev/null
	@touch $@

figures: $(FIG_STAMPS)

# Extra prerequisites for the two decks that use generated figures. A rule with
# no recipe only adds prerequisites; the build commands stay in DECK_RULE above.
# The stamp alone is not enough: it only tracks the *script*, so a figure that
# changed by any other route (a hand-tweaked PNG, a half-restored file) would not
# rebuild the deck that includes it. Listing the images as well covers that.
$(SLIDEDIR)/chapter_00/chapter_00.pdf:   $(SLIDEDIR)/chapter_00/.figures.stamp \
                                         $(wildcard $(SLIDEDIR)/chapter_00/images/*)
$(SLIDEDIR)/chapter_00b/chapter_00b.pdf: $(SLIDEDIR)/chapter_00b/.figures.stamp \
                                         $(wildcard $(SLIDEDIR)/chapter_00b/images/*)

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
#
# Two kinds of source live there. A *paper* is a single .tex that produces two
# PDFs: the paper as students see it, and the same paper with \withsolutions set.
# A *review deck* is a separate beamer source and needs the same two passes as a
# lecture deck, for the navigation bar.
#
# Short_Exams_60min/ is deliberately absent: it ships its own build.sh next to
# its sources (see that folder's README) and stays out of this Makefile.
EXAMDIR := Mock_Exams
EXAM_1  := $(EXAMDIR)/Exam_1_after_Lecture_04
EXAM_2  := $(EXAMDIR)/Exam_2_after_Lecture_08
EXAM_F  := $(EXAMDIR)/Final_Exam_after_Lecture_12

# One entry per source, written "directory|source stem|output stem". The output
# stems are the established -jobname values, so no PDF changes its name. A bar
# is the separator because $(word) splits on whitespace, and $(foreach) below
# needs each entry to stay a single word.
EXAM_PAPERS := \
  $(EXAM_1)|mock_exam_1|Mock_Exam_1 \
  $(EXAM_2)|mock_exam_2|Mock_Exam_2 \
  $(EXAM_F)|final_mock_exam|Final_Mock_Exam \
  $(EXAM_F)|final_mock_exam_a|Final_Mock_Exam_A \
  $(EXAM_F)|final_mock_exam_b|Final_Mock_Exam_B \
  $(EXAM_F)|final_mock_exam_c|Final_Mock_Exam_C

EXAM_DECKS := \
  $(EXAM_1)|solutions_slides_1|Mock_Exam_1_Solutions_Slides \
  $(EXAM_2)|solutions_slides_2|Mock_Exam_2_Solutions_Slides \
  $(EXAM_F)|solutions_slides_final|Final_Mock_Exam_Solutions_Slides \
  $(EXAM_F)|solutions_slides_a|Final_Mock_Exam_A_Solutions_Slides \
  $(EXAM_F)|solutions_slides_b|Final_Mock_Exam_B_Solutions_Slides \
  $(EXAM_F)|solutions_slides_c|Final_Mock_Exam_C_Solutions_Slides

exam_dir = $(word 1,$(subst |, ,$(1)))
exam_src = $(word 2,$(subst |, ,$(1)))
exam_out = $(word 3,$(subst |, ,$(1)))

# The paper and its solutions get a rule each rather than one rule with two
# targets: in make 3.81 a multi-target rule is shorthand for one rule per
# target, so under -j the shared recipe would run twice at once and two
# pdflatex processes would fight over the same -jobname. One target per recipe
# keeps every job's aux files (.aux .log .out .nav .snm .toc) distinct, which
# is what makes it safe for several papers to build in the same directory.
define EXAM_PAPER_RULE
$(1)/$(3).pdf: $(1)/$(2).tex
	@echo "  [exam]     $(3)"
	@cd $(1) && $(LATEX) -jobname=$(3) $(2).tex >/dev/null

$(1)/$(3)_Solutions.pdf: $(1)/$(2).tex
	@echo "  [exam]     $(3)_Solutions"
	@cd $(1) && $(LATEX) -jobname=$(3)_Solutions "\def\withsolutions{1}\input{$(2).tex}" >/dev/null
endef
$(foreach p,$(EXAM_PAPERS),$(eval $(call EXAM_PAPER_RULE,$(call exam_dir,$(p)),$(call exam_src,$(p)),$(call exam_out,$(p)))))

define EXAM_DECK_RULE
$(1)/$(3).pdf: $(1)/$(2).tex
	@echo "  [exam]     $(3)"
	@cd $(1) && $(LATEX) -jobname=$(3) $(2).tex >/dev/null \
	  && $(LATEX) -jobname=$(3) $(2).tex >/dev/null
endef
$(foreach d,$(EXAM_DECKS),$(eval $(call EXAM_DECK_RULE,$(call exam_dir,$(d)),$(call exam_src,$(d)),$(call exam_out,$(d)))))

EXAM_PDFS := \
  $(foreach p,$(EXAM_PAPERS),$(call exam_dir,$(p))/$(call exam_out,$(p)).pdf \
                             $(call exam_dir,$(p))/$(call exam_out,$(p))_Solutions.pdf) \
  $(foreach d,$(EXAM_DECKS),$(call exam_dir,$(d))/$(call exam_out,$(d)).pdf)

# The PDFs cannot be prerequisites of "exams" directly: on a fresh clone their
# .tex prerequisites are missing too, and make would abort with "No rule to make
# target" instead of saying why. Guard first, then hand the list to a sub-make.
exams:
	@test -d $(EXAMDIR) || { echo "$(EXAMDIR)/ not present (git-ignored)"; exit 1; }
	@$(MAKE) --no-print-directory $(EXAM_PDFS)
	@echo "  [exams]    $(words $(EXAM_PDFS)) PDFs up to date"
	@echo "             Short_Exams_60min: run its own ./build.sh"

# ------------------------------------------------------------------------ checks
# Two different questions. check_decks.py reads the .log files and asks whether
# the decks compiled cleanly; check_runsheets.py reads the .pdf and .toc files
# and asks whether the runsheets still describe the decks they were written
# against.
#
# --quiet means what it says: wrong numbers, nothing else, plus a count of the
# heuristic warnings it held back. Those warnings are all benign until someone
# edits a deck, and printing 57 of them on every run would train the reader to
# skip the output — which is how the next real one gets missed. `make runsheets`
# shows them, with the page -> frame title listing; --warnings is the middle one.
check:
	@$(PYTHON) $(GUIDE)/check_decks.py
	@echo
	@$(MAKE) --no-print-directory runsheets ARGS=--quiet

# Teaching_Guide/runsheets/ is git-ignored (it maps exercises onto exam
# problems), so a fresh clone has none. Guard the same way "exams" does — but
# with exit 0, because unlike the exams this is part of "check" and its absence
# is normal, not an error.
#
# Deliberately *not* dependent on $(DECK_PDFS): like check_decks.py this only
# reads what a build has already left behind, so it stays cheap and never
# launches pdflatex. It says so itself when a deck is stale or uncompiled.
RUNSHEETDIR := $(GUIDE)/runsheets

# The directory is passed on to the script rather than left to its default, so
# that the guard above and the check below can never disagree about which folder
# is being read — and so `make check RUNSHEETDIR=/tmp/copy` can test the checker.
runsheets:
	@test -d "$(RUNSHEETDIR)" || { echo "  [runsheets] $(RUNSHEETDIR)/ not present (git-ignored)"; exit 0; } \
	  && $(PYTHON) $(GUIDE)/check_runsheets.py $(ARGS) "$(RUNSHEETDIR)"

# The same command .github/workflows/notebooks.yml runs, so the CI failure can
# be reproduced locally. About 2 minutes, and it needs nbclient on top of
# requirements.txt. Deliberately out of "check": "check" reads files, this runs
# 15 notebooks. Nothing is written back to the notebooks.
notebooks:
	@$(PYTHON) .github/scripts/check_notebooks.py $(ARGS)

# Only ever touches LaTeX by-products: no .tex, .pdf or image can match. Note
# that "check" reads the .log files and "index" the .toc files, and a deck whose
# .pdf is already current will not recompile on its own, so both need a forced
# rebuild after a clean.
clean:
	@find $(SLIDEDIR) $(HANDOUTS) -type f \
	  \( -name '*.aux' -o -name '*.log' -o -name '*.nav' -o -name '*.out' \
	  -o -name '*.snm' -o -name '*.toc' -o -name '*.vrb' -o -name '*.fls' \
	  -o -name '*.fdb_latexmk' \) -delete 2>/dev/null || true
	@echo "  [clean]    LaTeX artefacts removed"
	@echo "             run 'make -B decks' before 'make check' or 'make index'"

# =====================================================================
# R code from: Part_2_Graphical_Representations.tex
# Translated from: Statistik_für_Ökonomen_Teil_2.R
# Translated on: 2026-05-03
# Quantitative Research -- Part 2: Graphical Representations
# Prof. Dr. Christoph Weisser (HSBI), Summer Semester 2026
# Generated/updated on: 2026-05-03
#
# Overview (Slide -> Frame title -> Section / Subsection):
#   Slide 14 : "Empirical distribution function with R"
#                 Section "Graphical displays" /
#                 Subsection "Empirical distribution function"
#   Slide 23 : "Histograms with R"
#                 Section "Graphical displays" / Subsection "Histogram"
#   Slide 28 : "R commands: Histogram"
#                 Section "Graphical displays" / Subsection "Histogram"
#   Slide 29 : "R commands: Classified frequencies"
#                 Section "Graphical displays" / Subsection "Histogram"
#   Slide 57 : "R commands: Frequencies and measures of location"
#                 Section "Graphical displays" / Subsection "R"
#   Slide 58 : "R commands: Measures of dispersion"
#                 Section "Graphical displays" / Subsection "R"
#   Slide 59 : "R commands: Empirical distribution function"
#                 Section "Graphical displays" / Subsection "R"
#   Slide 60 : "R commands: Histogram"
#                 Section "Graphical displays" / Subsection "R"
#   Slide 61 : "R commands: Classified frequencies"
#                 Section "Graphical displays" / Subsection "R"
#   Slide 62 : "R commands: Boxplot"
#                 Section "Graphical displays" / Subsection "R"
#
# Required packages:
#   qboxplot   (only for SLIDE 62 -- boxplot with our quartile definition)
#
# How to navigate this file:
#   - Search for "SLIDE <n>" (e.g. "SLIDE 28") to jump to a slide's code.
#   - Each slide block is wrapped between
#         # --- begin SLIDE <n> ---
#     and
#         # --- end SLIDE <n> ---
#     to make it easy to grep in either direction (LaTeX <-> R).
# =====================================================================


# ---------------------------------------------------------------------
# DATA SETUP -- not from a particular slide.
# The presentation uses the variable name `fussball` (shoe sizes of a
# football team, n = 11). We define it here once so that every R
# snippet on the slides below is runnable as-is.
# ---------------------------------------------------------------------
fussball <- c(40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39)
length(fussball)   # n = 11
sort(fussball)     # sorted


# ---------------------------------------------------------------------
# SLIDE 14: "Empirical distribution function with R"
# Section:  Graphical displays / Empirical distribution function
# ---------------------------------------------------------------------
# --- begin SLIDE 14 ---

# Compute
Fn.fussball <- ecdf(fussball)

# Output
# Returns the value of the empirical
# distribution function at x = 39
Fn.fussball(39)

# Plot
plot(ecdf(fussball),
     verticals = TRUE,
     do.points = FALSE)

# --- end SLIDE 14 ---


# ---------------------------------------------------------------------
# SLIDE 23: "Histograms with R"
# Section:  Graphical displays / Histogram
# ---------------------------------------------------------------------
# --- begin SLIDE 23 ---

# Class width 2
hist(fussball, breaks = c(37, 39, 41, 43, 45, 47), prob = TRUE)
hist(fussball, breaks = seq(37, 47, 2), prob = TRUE)  # alternative

# Different class widths
hist(fussball, breaks = c(37, 39, 40, 41, 46), prob = TRUE)

# --- end SLIDE 23 ---


# ---------------------------------------------------------------------
# SLIDE 28: "R commands: Histogram"
# Section:  Graphical displays / Histogram
# ---------------------------------------------------------------------
# --- begin SLIDE 28 ---

# Histogram with uniform class width (here: 2)
hist(fussball, breaks = c(37, 39, 41, 43, 45, 47), prob = TRUE)
hist(fussball, breaks = seq(37, 47, 2), prob = TRUE)

# Histogram with different class widths
hist(fussball, breaks = c(37, 39, 40, 41, 46), prob = TRUE)

# Note: prob=TRUE displays the density f_j instead of the absolute
# frequencies. The class boundaries are set with `breaks`.

# --- end SLIDE 28 ---


# ---------------------------------------------------------------------
# SLIDE 29: "R commands: Classified frequencies"
# Section:  Graphical displays / Histogram
# ---------------------------------------------------------------------
# --- begin SLIDE 29 ---

# The slide shows the syntax with placeholders (daten/xd, Wert1,...,Wertn).
# Here is the identical syntax as a comment plus a concrete, runnable
# variant with our data `fussball`.

# --- Slide text (schema): ------------------------------------------
# Class assignment
# cut(daten, breaks = c(Wert1, Wert2, ..., Wertn), include.lowest = TRUE)
#
# Absolute classified frequencies
# table(cut(xd, breaks = c(Wert1, ..., Wertn), include.lowest = TRUE))
#
# Relative classified frequencies
# prop.table(table(cut(xd, breaks = c(Wert1, ..., Wertn), include.lowest = TRUE)))
# -------------------------------------------------------------------

# Concrete example with `fussball` and class boundaries 37,39,41,43,45,47
cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE)
table(cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE))
prop.table(table(cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE)))

# --- end SLIDE 29 ---


# ---------------------------------------------------------------------
# SLIDE 57: "R commands: Frequencies and measures of location"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 57 ---

# Absolute frequencies
tab.fussball <- table(fussball)
(tab.fussball <- table(fussball))  # print directly

# Arithmetic mean
mean(fussball)

# Median and quantiles
median(fussball)  # Note: not our definition!
# Better with quantile (type = 1 = our definition):
# Slide text uses `daten`; here directly with `fussball`:
quantile(fussball, 0.8, type = 1)                      # 80% quantile
quantile(fussball, c(0.25, 0.5, 0.75), type = 1)        # quartiles

# --- end SLIDE 57 ---


# ---------------------------------------------------------------------
# SLIDE 58: "R commands: Measures of dispersion"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 58 ---

# Sample variance and standard deviation
var(fussball)
sd(fussball)

# Coefficient of variation
(v <- sd(fussball) / mean(fussball))

# Normalized coefficient of variation
(vstar <- v / sqrt(length(fussball)))

# --- end SLIDE 58 ---


# ---------------------------------------------------------------------
# SLIDE 59: "R commands: Empirical distribution function"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 59 ---

# Compute and evaluate
Fn.fussball <- ecdf(fussball)
Fn.fussball(39)  # function value at x = 39

# Plot
plot(ecdf(fussball), verticals = TRUE, do.points = FALSE)

# --- end SLIDE 59 ---


# ---------------------------------------------------------------------
# SLIDE 60: "R commands: Histogram"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 60 ---

# Uniform class width (here: 2)
hist(fussball, breaks = c(37, 39, 41, 43, 45, 47), prob = TRUE)
hist(fussball, breaks = seq(37, 47, 2), prob = TRUE)

# Different class widths
hist(fussball, breaks = c(37, 39, 40, 41, 46), prob = TRUE)

# --- end SLIDE 60 ---


# ---------------------------------------------------------------------
# SLIDE 61: "R commands: Classified frequencies"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 61 ---

# Absolute frequencies
table(fussball)

# --- Slide text (schema): ------------------------------------------
# Class assignment
# cut(fussball, breaks = c(Wert1, Wert2, ..., Wertn), include.lowest = TRUE)
#
# Absolute and relative classified frequencies
# table(cut(fussball, breaks = c(Wert1, ..., Wertn), include.lowest = TRUE))
# prop.table(table(cut(fussball, breaks = c(Wert1, ..., Wertn), include.lowest = TRUE)))
# -------------------------------------------------------------------

# Concrete example with class boundaries 37,39,41,43,45,47
cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE)
table(cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE))
prop.table(table(cut(fussball, breaks = c(37, 39, 41, 43, 45, 47), include.lowest = TRUE)))

# --- end SLIDE 61 ---


# ---------------------------------------------------------------------
# SLIDE 62: "R commands: Boxplot"
# Section:  Graphical displays / R
# ---------------------------------------------------------------------
# --- begin SLIDE 62 ---

# Standard boxplot (after Tukey)
boxplot(fussball, horizontal = TRUE, range = 1.5)
# `range` can be omitted for k = 1.5.

# Boxplot with our quartiles (type = 1)
# Note: The package `qboxplot` is not part of the standard R installation
# and may need to be installed once:
#   install.packages("qboxplot")
if (requireNamespace("qboxplot", quietly = TRUE)) {
  library(qboxplot)
  qboxplot(fussball ~ 1, qtype = 1, horizontal = TRUE)
} else {
  message("Package 'qboxplot' not installed -- ",
          "Slide 62 (qboxplot) is being skipped. ",
          "If needed: install.packages('qboxplot').")
}

# --- end SLIDE 62 ---

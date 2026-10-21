# =====================================================================
# R code from: Part_1_Descriptive_Statistics.tex
# Title:       Quantitative Research – Part 1: Descriptive Statistics
# Author:      Prof. Dr. Christoph Weisser (HSBI)
# Translated from: Statistik_für_Ökonomen_Teil_1.R
# Translated on:   2026-05-03
# Updated on:      2026-05-03
#
# Description:
#   Slide code for the lecture "Quantitative Research – Part 1".
#   Each code section is tagged with a SLIDE marker that uniquely
#   identifies the corresponding slide of the Beamer presentation.
#   The SLIDE markers are greppable: e.g. "SLIDE 28" finds the code
#   for the slide "Frequencies with R".
#
# Table of contents (slide -> content):
#   Setup                                 -> SETUP block (data of the 11 players)
#   Section 2 "Descriptive Statistics":
#     Subsection "Frequencies":
#       SLIDE 28  "Frequencies with R"
#       SLIDE 29  "Column chart"                 (code for the figure)
#       SLIDE 30  "Bar chart"                    (code for the figure)
#       SLIDE 31  "Pie chart"                    (code for the figure)
#       SLIDE 32  "Empirical distribution function" (code for the figure)
#     Subsection "Measures of location":
#       SLIDE 39  "Measures of location with R 1"
#       SLIDE 40  "Measures of location with R 2"
#       SLIDE 48  "Quantiles with R"
#     Subsection "Measures of dispersion":
#       SLIDE 61  "Measures of dispersion with R"
#       SLIDE 68  "Exercise – Computing measures of dispersion" (handball team)
#       SLIDE 69  "Exercise – Results"
#   Section 3 "Summary":
#       SLIDE 74  "Summary: Important R commands (1/2)"
#       SLIDE 75  "Summary: Important R commands (2/2)"
#
# Reproducibility note:
#   The shoe-size vector `daten` is defined once in the SETUP block and
#   reused by all subsequent slide blocks.
# =====================================================================


# =====================================================================
# SETUP – Data
# Source: slide "The data – an example 2"
# Used from: SLIDE 28 onwards
# =====================================================================
# Football team – read in the shoe sizes of the 11 players
daten <- c(40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39)
daten


# ---------------------------------------------------------------------
# SLIDE 28: "Frequencies with R"
# Section: Descriptive Statistics > Frequencies
# ---------------------------------------------------------------------
# Frequency table (absolute frequencies)
table(daten)

# Relative frequencies
prop.table(table(daten))

# Cumulative (relative) frequencies
cumsum(prop.table(table(daten)))
# --- end SLIDE 28 ---


# ---------------------------------------------------------------------
# SLIDE 29: "Column chart"
# Section: Descriptive Statistics > Frequencies
# Note: The LaTeX slide only shows the image (chart_slide_19.png);
# the corresponding R code is documented here.
# ---------------------------------------------------------------------
barplot(table(daten),
        main = "Column chart – Shoe sizes",
        xlab = "Shoe size",
        ylab = "Absolute frequency")
# --- end SLIDE 29 ---


# ---------------------------------------------------------------------
# SLIDE 30: "Bar chart"
# Section: Descriptive Statistics > Frequencies
# Note: only image on the slide (chart_slide_20.png).
# ---------------------------------------------------------------------
barplot(table(daten),
        horiz = TRUE,
        main  = "Bar chart – Shoe sizes",
        xlab  = "Absolute frequency",
        ylab  = "Shoe size")
# --- end SLIDE 30 ---


# ---------------------------------------------------------------------
# SLIDE 31: "Pie chart"
# Section: Descriptive Statistics > Frequencies
# Note: only image on the slide (chart_slide_21.png).
# ---------------------------------------------------------------------
pie(table(daten), main = "Pie chart – Shoe sizes")
# --- end SLIDE 31 ---


# ---------------------------------------------------------------------
# SLIDE 32: "Empirical distribution function"
# Section: Descriptive Statistics > Frequencies
# Note: only image on the slide (image_004.png).
# ---------------------------------------------------------------------
# Create the empirical distribution function as an R function
Fn <- ecdf(daten)

# Value of the distribution function at 39: F(39)
Fn(39)

# Plot the empirical distribution function
plot(ecdf(daten),
     main      = "Empirical distribution function – Shoe sizes",
     xlab      = "Shoe size",
     ylab      = "F(x)",
     verticals = TRUE,
     do.points = TRUE)
# --- end SLIDE 32 ---


# ---------------------------------------------------------------------
# SLIDE 39: "Measures of location with R 1"
# Section: Descriptive Statistics > Measures of location
# ---------------------------------------------------------------------
# Sum
sum(daten)

# Arithmetic mean
mean(daten)

# Geometric mean
# Step 1: Compute the product of all values
product <- prod(daten)
# Step 2: Determine the number of observations
n <- length(daten)
# Step 3: Take the n-th root
gmean <- product^(1/n)
gmean
# --- end SLIDE 39 ---


# ---------------------------------------------------------------------
# SLIDE 40: "Measures of location with R 2"
# Section: Descriptive Statistics > Measures of location
# ---------------------------------------------------------------------
# Sum
sum(daten)

# Trimmed mean: 10% of the extreme values are removed
mean(daten, trim = 0.10)

# Median
median(daten)  # Note: the R definition differs from the lecture
               # definition (position ceil(n/2))!

# Mode – supplementary helper function (not included in the LaTeX slide,
# added by the author since R does not provide a direct mode command)
modus <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}
print(modus(daten))
# --- end SLIDE 40 ---


# ---------------------------------------------------------------------
# SLIDE 48: "Quantiles with R"
# Section: Descriptive Statistics > Measures of location
# Note: type = 1 corresponds to the discrete definition
#       x_p = x_{ceil(n*p)} from the lecture.
# ---------------------------------------------------------------------
# All standard quantiles at once (type = 1: discrete)
quantile(daten, type = 1)

# 1st quartile (25% quantile)
quantile(daten, 0.25, type = 1)

# 3rd quartile (75% quantile) – supplementary
quantile(daten, 0.75, type = 1)

# 17% quantile – supplementary (cf. table on slide "Quantiles – Computation example")
quantile(daten, 0.17, type = 1)

# 80% quantile
quantile(daten, 0.80, type = 1)
# --- end SLIDE 48 ---


# ---------------------------------------------------------------------
# SLIDE 61: "Measures of dispersion with R"
# Section: Descriptive Statistics > Measures of dispersion
# ---------------------------------------------------------------------
# Variant 1: slide code directly on `daten` (shoe-size team)
# Variance
var(daten)

# Standard deviation
sd(daten)

# Coefficient of variation
v <- sd(daten) / mean(daten)
v

# Normalized coefficient of variation
vstar <- v / sqrt(length(daten))
vstar

# Variant 2: comparison of Vierer A vs. Vierer B (slides 47-57)
vierer_a <- c(34, 37, 40, 41)
vierer_b <- c(36, 37, 39, 40)

# Sample variance
print(var(vierer_a))   # 10
print(var(vierer_b))   # 3.333...

# Standard deviation
print(sd(vierer_a))    # 3.1623
print(sd(vierer_b))    # 1.8257

# Coefficient of variation
print(sd(vierer_a) / mean(vierer_a))   # 0.0832
print(sd(vierer_b) / mean(vierer_b))   # 0.0481

# Normalized coefficient of variation
print((sd(vierer_a) / mean(vierer_a)) / sqrt(length(vierer_a)))  # 0.0416
print((sd(vierer_b) / mean(vierer_b)) / sqrt(length(vierer_b)))  # 0.0240
# --- end SLIDE 61 ---


# ---------------------------------------------------------------------
# SLIDE 68 / SLIDE 69: "Exercise – Computing measures of dispersion" /
#                      "Exercise – Results"
# Section: Descriptive Statistics > Measures of dispersion
# Data:     shoe sizes of the handball team (n = 13)
# Expected: x̄ = 39.8462, s² = 5.1410, s = 2.2674,
#           v = 0.0569, v* = 0.0158
# ---------------------------------------------------------------------
handball <- c(40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39, 40, 42)
length(handball)   # 13

# Mean
mean(handball)

# Sample variance
var(handball)

# Standard deviation
sd(handball)

# Coefficient of variation
v_h <- sd(handball) / mean(handball)
v_h

# Normalized coefficient of variation
vstar_h <- v_h / sqrt(length(handball))
vstar_h
# --- end SLIDE 68/69 ---


# ---------------------------------------------------------------------
# SLIDE 74: "Summary: Important R commands (1/2)"
# Section: Summary
# ---------------------------------------------------------------------
# Frequencies
table(daten)                        # Absolute frequencies
prop.table(table(daten))            # Relative frequencies
cumsum(prop.table(table(daten)))    # Cumulative frequencies

# Measures of location
mean(daten)                         # Arithmetic mean
mean(daten, trim = 0.10)            # Trimmed mean (10%)
median(daten)                       # Median
quantile(daten, 0.25, type = 1)     # Quantiles (e.g. Q1)
# --- end SLIDE 74 ---


# ---------------------------------------------------------------------
# SLIDE 75: "Summary: Important R commands (2/2)"
# Section: Summary
# ---------------------------------------------------------------------
# Measures of dispersion
var(daten)                                        # Sample variance
sd(daten)                                         # Standard deviation
sd(daten) / mean(daten)                           # Coefficient of variation
sd(daten) / mean(daten) / sqrt(length(daten))     # Norm. coeff. of variation
# --- end SLIDE 75 ---

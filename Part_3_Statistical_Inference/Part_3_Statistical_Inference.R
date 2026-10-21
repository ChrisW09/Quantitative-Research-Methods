# =====================================================================
# R code from: Part_3_Statistical_Inference.tex
# Quantitative Research -- Part 3: Statistical Inference
# Translated from: Statistik für Ökonomen Teil 6.R
# Translated on: 2026-05-03
#
# Description:
#   This script collects all R code that appears in the LaTeX Beamer
#   presentation "Quantitative Research -- Part 3: Statistical Inference" (confidence
#   intervals, hypothesis tests, p-value, one-sided tests, error types,
#   contingency and chi-squared test). Every snippet is wrapped with a
#   greppable SLIDE marker so the same code can be located in both
#   directions (frame title in .tex <--> SLIDE tag in .R).
#
# Required R packages:
#   Only base R + 'stats' (loaded by default). No external packages
#   are required.
#
# Required data objects (defined in the SETUP section below):
#   - milch : c(1005, 1001, 997, 1000, 1001, 998, 999, 999, 1009)
#   - sahne : c(251, 248, 248, 249, 250, 251, 247, 246, 252,
#               251, 248, 247, 246, 249, 248, 252)
#   The presentation uses these two example data vectors throughout.
#   They appear in the text/exercise blocks of the slides but are NOT
#   re-defined inside every R-code lstlisting -- so we set them once
#   here so every snippet below is runnable as-is.
#
# Overview (slide -> topic):
#   SETUP                                      -> data definitions
#   Section "Hypothesis tests / Hypothesis test with R":
#     SLIDE 39 : Hypothesis test with R        -> t.test() (two-sided)
#     SLIDE 40 : Hypothesis test with R -- Output (console output)
#   Section "p-value" (R commands):
#     SLIDE 54 : R commands with known variance -- Milk
#     SLIDE 55 : R commands with known variance -- Cream
#     SLIDE 56 : R commands with unknown variance -- Milk
#     SLIDE 57 : R commands with unknown variance -- Cream
#   Section "One-sided tests":
#     SLIDE 68 : One-sided test with R
#     SLIDE 69 : One-sided test with R -- Milk example (output)
#     SLIDE 70 : One-sided test with R -- Cream exercise (output)
#     SLIDE 77 : One-sided CI in R -- known variance
#   Section "Analysis of categorical data / Chi^2-test":
#     SLIDE 106: Test of independence -- R code and example
#   Section "Summary":
#     SLIDE 107: Summary 1 -- Confidence intervals
#     SLIDE 108: Summary 2 -- Hypothesis test, two-sided
#     SLIDE 109: Summary 3 -- p-value
#     SLIDE 110: Summary 4 -- One-sided tests & error types
#     SLIDE 111: Summary 5 -- Contingency & Chi^2-test
# =====================================================================


# ---------------------------------------------------------------------
# SETUP: example data vectors used throughout the presentation
# Section: (used by all R-code slides below)
# Source: data values are stated in the LaTeX problem descriptions
#   - "milch" : Milk example (slide 11, frame "Milk example: Calculation")
#   - "sahne" : Cream exercise (slide 21, frame "Exercise -- Cream filling")
# These are NOT inside lstlisting blocks in the .tex; they are added
# here so every snippet below is self-contained and runnable.
# ---------------------------------------------------------------------
milch <- c(1005, 1001, 997, 1000, 1001, 998, 999, 999, 1009)
sahne <- c(251, 248, 248, 249, 250, 251, 247, 246, 252,
           251, 248, 247, 246, 249, 248, 252)
# --- end SETUP ---


# ---------------------------------------------------------------------
# SLIDE 39: "Hypothesis test with R"
# Section: Hypothesis tests / Hypothesis test with R
# ---------------------------------------------------------------------
milch <- c(1005, 1001, 997, 1000, 1001, 998, 999, 999, 1009)

t.test(milch, mu = 1000)
# --- end SLIDE 39 ---


# ---------------------------------------------------------------------
# SLIDE 40: "Hypothesis test with R -- Output"
# Section: Hypothesis tests / Hypothesis test with R
# Note: This slide shows ONLY the R console output of the t.test() from
#       SLIDE 39 (no new R commands). It is reproduced here as a comment
#       block so the script faithfully mirrors the slide deck.
# ---------------------------------------------------------------------
# Console output (reference -- not executable):
#         One Sample t-test
#
# data:  milch
# t = 0.79472, df = 8, p-value = 0.4497
# alternative hypothesis: true mean is not equal to 1000
# 95 percent confidence interval:
#   998.0983 1003.9017
# sample estimates:
# mean of x
#      1001
# --- end SLIDE 40 ---


# ---------------------------------------------------------------------
# SLIDE 54: "R commands with known variance -- Milk"
# Section: p-value
# ---------------------------------------------------------------------
alpha <- 0.05
mu0.milch   <- 1000
sigma.milch <- 3

(Zn.milch <- (mean(milch) - mu0.milch) /
             (sigma.milch / sqrt(length(milch))))

(ki.n.milch <- mean(milch) +
               c(-1, 1) * qnorm(1 - alpha/2) *
               sigma.milch / sqrt(length(milch)))
# --- end SLIDE 54 ---


# ---------------------------------------------------------------------
# SLIDE 55: "R commands with known variance -- Cream"
# Section: p-value
# ---------------------------------------------------------------------
alpha <- 0.05
mu0.sahne   <- 250
sigma.sahne <- 2

(Zn.sahne <- (mean(sahne) - mu0.sahne) /
             (sigma.sahne / sqrt(length(sahne))))

(ki.n.sahne <- mean(sahne) +
               c(-1, 1) * qnorm(1 - alpha/2) *
               sigma.sahne / sqrt(length(sahne)))
# --- end SLIDE 55 ---


# ---------------------------------------------------------------------
# SLIDE 56: "R commands with unknown variance -- Milk"
# Section: p-value
# ---------------------------------------------------------------------
alpha <- 0.05
mu0.milch <- 1000

(Tn.milch <- (mean(milch) - mu0.milch) /
             (sd(milch) / sqrt(length(milch))))

(ki.t.milch <- mean(milch) +
               c(-1, 1) * qt(1 - alpha/2, length(milch) - 1) *
               sd(milch) / sqrt(length(milch)))
# --- end SLIDE 56 ---


# ---------------------------------------------------------------------
# SLIDE 57: "R commands with unknown variance -- Cream"
# Section: p-value
# ---------------------------------------------------------------------
alpha <- 0.05
mu0.sahne <- 250

(Tn.sahne <- (mean(sahne) - mu0.sahne) /
             (sd(sahne) / sqrt(length(sahne))))

(ki.t.sahne <- mean(sahne) +
               c(-1, 1) * qt(1 - alpha/2, length(sahne) - 1) *
               sd(sahne) / sqrt(length(sahne)))
# --- end SLIDE 57 ---


# ---------------------------------------------------------------------
# SLIDE 68: "One-sided test with R"
# Section: One-sided tests
# ---------------------------------------------------------------------
# left-sided (H1: mu < mu0)
t.test(milch, mu = 1000, alternative = "less")

# right-sided (H1: mu > mu0)
t.test(milch, mu = 1000, alternative = "greater")
# --- end SLIDE 68 ---


# ---------------------------------------------------------------------
# SLIDE 69: "One-sided test with R -- Milk example"
# Section: One-sided tests
# Note: The slide shows the console output of the left-sided test
#       on the milch data. The command itself is repeated below; the
#       expected output is reproduced as a comment.
# ---------------------------------------------------------------------
t.test(milch, mu = 1000, alternative = "less")
# Console output (reference -- not executable):
# > t.test(milch, mu = 1000, alternative = "less")
#
#         One Sample t-test
#
# data:  milch
# t = 0.7947, df = 8, p-value = 0.7751
# alternative hypothesis: true mean is less than 1000
# 95 percent confidence interval:
#       -Inf 1003.338
# sample estimates:
# mean of x
#      1001
# --- end SLIDE 69 ---


# ---------------------------------------------------------------------
# SLIDE 70: "One-sided test with R -- Cream exercise"
# Section: One-sided tests
# Note: Slide shows the console output of the left-sided test on the
#       sahne data. Command is reproduced below; expected output as
#       comment.
# ---------------------------------------------------------------------
t.test(sahne, mu = 250, alternative = "less")
# Console output (reference -- not executable):
# > t.test(sahne, mu = 250, alternative = "less")
#
#         One Sample t-test
#
# data:  sahne
# t = -2.1086, df = 15, p-value = 0.02606
# alternative hypothesis: true mean is less than 250
# 95 percent confidence interval:
#       -Inf 249.7849
# sample estimates:
# mean of x
#  248.9375
# --- end SLIDE 70 ---


# ---------------------------------------------------------------------
# SLIDE 77: "One-sided CI in R -- known variance"
# Section: One-sided tests / One-sided confidence intervals
# Note: The original .tex snippet uses generic placeholders 'daten' and
#       'sigma.daten'. To make the snippet runnable we apply it to the
#       milch data (left-sided) and the sahne data (right-sided). The
#       generic form is preserved as a comment.
# ---------------------------------------------------------------------
# Original (generic) form from the slide:
#   # upper bound of the left-sided CI
#   (ki.n <- mean(daten) +
#            qnorm(1 - alpha) * sigma.daten /
#            sqrt(length(daten)))
#   # lower bound of the right-sided CI
#   (ki.n <- mean(daten) -
#            qnorm(1 - alpha) * sigma.daten /
#            sqrt(length(daten)))

alpha <- 0.05

# upper bound of the left-sided CI (Milk, sigma = 3)
daten <- milch
sigma.daten <- 3
(ki.n <- mean(daten) +
         qnorm(1 - alpha) * sigma.daten /
         sqrt(length(daten)))

# lower bound of the right-sided CI (Milk, sigma = 3)
(ki.n <- mean(daten) -
         qnorm(1 - alpha) * sigma.daten /
         sqrt(length(daten)))
# --- end SLIDE 77 ---


# ---------------------------------------------------------------------
# SLIDE 106: "Test of independence -- R code and example"
# Section: Analysis of categorical data / Chi^2-test
# ---------------------------------------------------------------------
kontingenz <- matrix(c(10, 8, 7,
                        6,12, 7), nrow = 2, byrow = TRUE)
rownames(kontingenz) <- c("m","w")  # TODO: confirm if row labels "m"/"w" (male/female) should be translated -- they are data identifiers used as factor-like labels
colnames(kontingenz) <- c("1V","2V","3V")

chisq.test(kontingenz)
# --- end SLIDE 106 ---


# ---------------------------------------------------------------------
# SLIDE 107: "Summary 1 -- Confidence intervals"
# Section: Summary
# Note: The snippet again uses the generic placeholders 'daten' /
#       'sigma'. We bind them to milch / sigma=3 so the snippet runs.
# ---------------------------------------------------------------------
daten <- milch
sigma <- 3
alpha <- 0.05

# unknown variance: t.test returns the CI directly
t.test(daten, conf.level = 0.95)$conf.int

# known variance: manually
mean(daten) + c(-1, 1) * qnorm(1 - alpha/2) *
              sigma / sqrt(length(daten))
# --- end SLIDE 107 ---


# ---------------------------------------------------------------------
# SLIDE 108: "Summary 2 -- Hypothesis test, two-sided"
# Section: Summary
# ---------------------------------------------------------------------
# Standard case: two-sided t-test with unknown sigma
t.test(milch, mu = 1000)
# Output: t, df, p-value, 95% CI, sample mean
# --- end SLIDE 108 ---


# ---------------------------------------------------------------------
# SLIDE 109: "Summary 3 -- p-value"
# Section: Summary
# Note: The snippet uses generic 'Zn', 'Tn', 'n'. We bind these to the
#       Milk example values (n = 9) so the snippet is runnable.
# ---------------------------------------------------------------------
n  <- length(milch)
Zn <- (mean(milch) - 1000) / (3        / sqrt(n))   # known variance
Tn <- (mean(milch) - 1000) / (sd(milch)/ sqrt(n))   # unknown variance

2 * pnorm(-abs(Zn))           # known variance, two-sided
2 * pt(-abs(Tn), df = n-1)    # unknown, two-sided
pt(Tn, n-1);  1 - pt(Tn, n-1) # left- or right-sided respectively
# --- end SLIDE 109 ---


# ---------------------------------------------------------------------
# SLIDE 110: "Summary 4 -- One-sided tests & error types"
# Section: Summary
# ---------------------------------------------------------------------
t.test(milch, mu = 1000, alternative = "less")     # left-sided
t.test(milch, mu = 1000, alternative = "greater")  # right-sided
# --- end SLIDE 110 ---


# ---------------------------------------------------------------------
# SLIDE 111: "Summary 5 -- Contingency & Chi^2-test"
# Section: Summary
# ---------------------------------------------------------------------
tab <- matrix(c(11,24,  3,0,  2,0), nrow = 3, byrow = TRUE)
chisq.test(tab)        # X-squared, df, p-value
# --- end SLIDE 111 ---

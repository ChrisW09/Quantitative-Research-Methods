# =====================================================================
# Python code for: Part_1_Descriptive_Statistics.tex
# Title:  Quantitative Research - Part 1: Descriptive Statistics
# Author: Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 1. The script is
# organised like the deck (sections / slide titles in the comments) and
# prints all results. Run it with:   python3 Part_1_Descriptive_Statistics.py
#
# Packages: numpy, pandas, scipy, matplotlib
# (Anaconda: already included; otherwise: pip install numpy pandas scipy matplotlib)
# =====================================================================

import math

import matplotlib
matplotlib.use("Agg")            # headless: figures are created, not shown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

pd.set_option("display.precision", 4)


def header(title):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70)


def course_quantile(x, p):
    """Course definition: x_(ceil(n*p)) of the sorted data
    (identical to np.quantile(x, p, method="inverted_cdf"))."""
    return np.quantile(x, p, method="inverted_cdf")


# =====================================================================
# SETUP - Data (slide "The Data -- an Example (2)")
# Shoe sizes of the 11 players of a soccer team
# =====================================================================
data = pd.Series([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39])
n = len(data)

# =====================================================================
# SECTION "Descriptive Statistics" > SUBSECTION "Frequencies"
# =====================================================================

# ---------------------------------------------------------------------
# Slide "Frequency Table"  /  Slide "Frequencies with Python"
# ---------------------------------------------------------------------
header('Slides "Frequency Table" / "Frequencies with Python"')
abs_freq = data.value_counts().sort_index()                # h_j
rel_freq = data.value_counts(normalize=True).sort_index()  # f_j
cum_freq = rel_freq.cumsum()                               # F(x)

table = pd.DataFrame({
    "absolute": abs_freq,
    "relative": rel_freq.round(4),
    "relative in %": (100 * rel_freq).round(1),
    "fraction": [f"{h}/{n}" for h in abs_freq],
    "cumulative": cum_freq.round(4),
    "cum. fraction": [f"{h}/{n}" for h in abs_freq.cumsum()],
})
print(table.T)
print("Total absolute frequency:", abs_freq.sum())         # 11
print("Total relative frequency:", rel_freq.sum())         # 1.0

# ---------------------------------------------------------------------
# Slides "Column Chart", "Bar Chart", "Pie Chart",
#        "Empirical Distribution Function"
# (the slides only show the images; this is the corresponding code)
# ---------------------------------------------------------------------
header('Slides "Column Chart" / "Bar Chart" / "Pie Chart" / "Empirical '
       'Distribution Function"')
fig, ax = plt.subplots()
ax.bar(abs_freq.index.astype(str), abs_freq.values)
ax.set(title="Column chart - Shoe sizes", xlabel="Shoe size",
       ylabel="Absolute frequency")
plt.close(fig)

fig, ax = plt.subplots()
ax.barh(abs_freq.index.astype(str), abs_freq.values)
ax.set(title="Bar chart - Shoe sizes", xlabel="Absolute frequency",
       ylabel="Shoe size")
plt.close(fig)

fig, ax = plt.subplots()
ax.pie(abs_freq.values, labels=abs_freq.index)
ax.set(title="Pie chart - Shoe sizes")
plt.close(fig)

fig, ax = plt.subplots()
ax.ecdf(data)                                   # step function F(x)
ax.set(title="Empirical distribution function - Shoe sizes",
       xlabel="Shoe size", ylabel="F(x)")
plt.close(fig)

print("F(39) =", round((data <= 39).mean(), 4))   # 0.6364 = 7/11
print("Figures created (not shown, headless mode).")

# =====================================================================
# SUBSECTION "Measures of Central Tendency"
# =====================================================================

# ---------------------------------------------------------------------
# Slide "Measures of Central Tendency -- Example"
# Slides "Measures of Central Tendency with Python (1)" and "(2)"
# ---------------------------------------------------------------------
header('Slides "Measures of Central Tendency -- Example" / "... with Python"')
print("Sum:                ", data.sum())                          # 436
print("Arithmetic mean:    ", round(data.mean(), 4))               # 39.6364

# Geometric mean in three steps (as on the slide) ...
product = np.prod(data)
gmean = product ** (1 / n)
print("Geometric mean:     ", round(gmean, 4))                     # 39.5755
# ... and in one step
print("stats.gmean:        ", round(stats.gmean(data), 4))         # 39.5755

print("Trimmed mean (10%): ", round(stats.trim_mean(data, 0.10), 4))  # 39.2222
print("Median (np.median): ", np.median(data))                     # 39.0
print("Median (course):    ", course_quantile(data, 0.5))          # 39
print("Mode:               ", data.mode().tolist())                # [39]

# ---------------------------------------------------------------------
# Slides "Median" (alternative definition) - NumPy averages for even n
# ---------------------------------------------------------------------
even = [34, 37, 40, 41]
print("Even n: np.median =", np.median(even),
      "| course x_(ceil(n/2)) =", course_quantile(even, 0.5))      # 38.5 | 37

# ---------------------------------------------------------------------
# Slides "Quantiles -- Computation", "Quantiles -- Computation Example",
#        "Quantiles -- Worked Example"
# ---------------------------------------------------------------------
header('Slides "Quantiles -- Computation (Example)" / "Worked Example"')
print("Sorted data:", sorted(data))  # 37, 38, 38, 39, 39, 39, 39, 40, 40, 41, 46
xs = np.sort(data.to_numpy())
rows = []
for name, p in [("1st quartile", 0.25), ("2nd quartile", 0.50),
                ("3rd quartile", 0.75), ("17%-quantile", 0.17),
                ("80%-quantile", 0.80), ("5%-quantile", 0.05)]:
    pos = math.ceil(round(n * p, 10))           # round avoids 8.8000000001
    rows.append([name, p, round(n * p, 2), pos, xs[pos - 1],
                 course_quantile(data, p)])
print(pd.DataFrame(rows, columns=["quantile", "p", "n*p", "position",
                                  "value x_(pos)", "np.quantile(inverted_cdf)"])
      .to_string(index=False))
# Expected values: 38, 39, 40, 38, 40, 37

# ---------------------------------------------------------------------
# Slide "Quantiles with Python"
# ---------------------------------------------------------------------
header('Slide "Quantiles with Python"')
p = [0, 0.25, 0.50, 0.75, 1]
print("Standard quantiles:", course_quantile(data, p))         # [37 38 39 40 46]
print("Q1 (25%):          ", course_quantile(data, 0.25))      # 38
print("80%-quantile:      ", course_quantile(data, 0.80))      # 40
print("Pitfall - default (linear) np.quantile(data, 0.25):",
      np.quantile(data, 0.25),                                 # 38.5
      "| data.quantile(0.25):", data.quantile(0.25))           # 38.5

# =====================================================================
# SUBSECTION "Measures of Dispersion"
# =====================================================================
four_a = np.array([34, 37, 40, 41])
four_b = np.array([36, 37, 39, 40])


def dispersion(x):
    x = np.asarray(x, dtype=float)
    s2 = np.var(x, ddof=1)                 # sample variance (n-1)
    s = np.std(x, ddof=1)                  # standard deviation
    v = s / np.mean(x)                     # coefficient of variation
    vstar = v / np.sqrt(len(x))            # normalized coeff. of variation
    return {"Mean": np.mean(x), "Median (course)": course_quantile(x, 0.5),
            "Sample variance": s2, "Standard deviation": s,
            "Coefficient of variation": v,
            "Normalized coefficient of variation": vstar}


# ---------------------------------------------------------------------
# Slides "Measures of Dispersion -- Why?", "Sample Variance -- Worked
# Example", "Standard Deviation -- Worked Example", "Coefficient of
# Variation -- Worked Example", "Normalized Coefficient of Variation --
# Worked Example", "Overview of Measures of Dispersion"
# ---------------------------------------------------------------------
header('Slide "Overview of Measures of Dispersion" (Four A vs. Four B)')
overview = pd.DataFrame({"Four A": dispersion(four_a),
                         "Four B": dispersion(four_b)})
print(overview.round(4))
# Expected: mean 38/38, median 37/37, s^2 10/3.3333, s 3.1623/1.8257,
#           v 0.0832/0.0480, v* 0.0416/0.0240
print("Sum of squares A:", np.sum((four_a - 38) ** 2),             # 30
      "| B:", np.sum((four_b - 38) ** 2))                          # 10

# Slide "Coefficient of Variation": mixed signs -> mean close to 0
print("Mean of -10, -5, 5, 11:", np.mean([-10, -5, 5, 11]))        # 0.25

# ---------------------------------------------------------------------
# Slide "Measures of Dispersion with Python"
# ---------------------------------------------------------------------
header('Slide "Measures of Dispersion with Python"')
print("np.var(four_a, ddof=1):", np.var(four_a, ddof=1))           # 10.0
print("np.std(four_a, ddof=1):", round(np.std(four_a, ddof=1), 4)) # 3.1623
v = np.std(four_a, ddof=1) / np.mean(four_a)
vstar = v / np.sqrt(len(four_a))
print("v =", round(v, 4), "| v* =", round(vstar, 4))               # 0.0832 | 0.0416
print("Pitfall - np.var(four_a) with default ddof=0:", np.var(four_a))  # 7.5
print("pandas .var() / .std() (ddof=1):", pd.Series(four_a).var(),
      round(pd.Series(four_a).std(), 4))                           # 10.0 3.1623

# ---------------------------------------------------------------------
# Slides "Exercise -- Calculate Measures of Dispersion" / "Exercise -- Results"
# Shoe sizes of the handball team (n = 13)
# ---------------------------------------------------------------------
header('Slides "Exercise -- Calculate Measures of Dispersion" / "Results"')
handball = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39, 40, 42])
res = dispersion(handball)
print("n =", len(handball))                                         # 13
for key in ["Mean", "Sample variance", "Standard deviation",
            "Coefficient of variation", "Normalized coefficient of variation"]:
    print(f"{key:37s} {res[key]:.4f}")
# Expected: 39.8462, 5.1410, 2.2674, 0.0569, 0.0158

# =====================================================================
# SECTION "Summary" - Slides "Summary 4: Key Python Commands (1)" / "(2)"
# =====================================================================
header('Slides "Summary 4: Key Python Commands (1)" / "(2)"')
print(data.value_counts().sort_index())                     # Absolute frequencies
print(data.value_counts(normalize=True).sort_index())       # Relative frequencies
print(data.value_counts(normalize=True).sort_index().cumsum())  # Cumulative
print("mean:", np.mean(data))                               # Arithmetic mean
print("gmean:", stats.gmean(data))                          # Geometric mean
print("trim_mean:", stats.trim_mean(data, 0.10))            # Trimmed mean (10%)
print("median:", np.median(data))                           # Median
print("Q1:", np.quantile(data, 0.25, method="inverted_cdf"))  # Quantiles (e.g. Q1)
print("var:", np.var(data, ddof=1))                         # Sample variance
print("std:", np.std(data, ddof=1))                         # Standard deviation
print("v:", np.std(data, ddof=1) / np.mean(data))           # Coefficient of variation
print("v*:", np.std(data, ddof=1) / np.mean(data) / np.sqrt(len(data)))  # Norm. coeff.

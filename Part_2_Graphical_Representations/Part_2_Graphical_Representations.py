#!/usr/bin/env python3
# =====================================================================
# Quantitative Research -- Part 2: Graphical Representations
# Prof. Dr. Christoph Weisser (HSBI)
#
# Python companion to Part_2_Graphical_Representations.tex.
# Reproduces every number shown on the slides and draws the graphics
# (empirical CDF, histograms, boxplots).
#
# Organisation (search for "SLIDE:" to jump to the code of a slide):
#   0. Data and helper functions
#   1. Section "Empirical Cumulative Distribution Function"
#   2. Section "Histogram"
#   3. Section "Boxplot"
#   4. Section "Exercise" (body heights)
#   5. Section "Python Commands"
#
# Requirements: numpy, pandas, statsmodels, matplotlib.
# The script runs headless (matplotlib backend "Agg"); figures are closed
# after drawing. Run with  python3 Part_2_Graphical_Representations.py --save DIR
# to store all figures as PNG files in DIR.
# =====================================================================
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

pd.set_option("display.width", 120)
SAVE_DIR = sys.argv[sys.argv.index("--save") + 1] if "--save" in sys.argv else None


def finish(fig, name):
    """Save the figure (only with --save DIR) and close it."""
    if SAVE_DIR:
        os.makedirs(SAVE_DIR, exist_ok=True)
        fig.savefig(os.path.join(SAVE_DIR, name), dpi=120, bbox_inches="tight")
    plt.close(fig)


def header(title):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70)


# ---------------------------------------------------------------------
# 0. DATA AND HELPER FUNCTIONS
# ---------------------------------------------------------------------
# Shoe sizes of the soccer team (n = 11), the running example of Parts 1-2.
shoe = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39])
n = len(shoe)


def quantile(x, p):
    """Course definition: x_(ceil(n*p)) = numpy method "inverted_cdf"
    (smallest x with F(x) >= p)."""
    return np.quantile(x, p, method="inverted_cdf")


def class_table(x, breaks):
    """Classified frequencies with classes [b0,b1], (b1,b2], ..., (b_{k-1},b_k].

    pd.cut(right=True, include_lowest=True) implements exactly the course
    convention. (np.histogram / plt.hist would use [a,b) instead!)
    """
    breaks = np.asarray(breaks, dtype=float)
    cls = pd.cut(x, breaks, right=True, include_lowest=True)
    h = pd.Series(cls).value_counts(sort=False)        # absolute frequencies
    labels = [f"[{breaks[0]:g},{breaks[1]:g}]"] + [
        f"({a:g},{b:g}]" for a, b in zip(breaks[1:-1], breaks[2:])]
    tab = pd.DataFrame({"width": np.diff(breaks), "abs": h.to_numpy()}, index=labels)
    tab["rel"] = tab["abs"] / len(x)                   # relative frequencies f_j
    tab["density"] = tab["rel"] / tab["width"]         # f_j / class width
    return tab


def density_hist(ax, tab, breaks, **kw):
    """Draw a density histogram from a class table (bars start at the left boundary)."""
    ax.bar(np.asarray(breaks[:-1], dtype=float), tab["density"].to_numpy(),
           width=np.diff(breaks), align="edge", edgecolor="black", **kw)
    ax.set_ylabel("Density")


def boxplot_stats(x, k=1.5):
    """Quartiles, IQR, whisker bounds, whiskers and outliers (course definition)."""
    q1, med, q3 = quantile(x, [0.25, 0.5, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    inside = x[(x >= lo) & (x <= hi)]
    return dict(q1=q1, med=med, q3=q3, iqr=iqr, lower_bound=lo, upper_bound=hi,
                whislo=inside.min(), whishi=inside.max(),
                fliers=np.sort(x[(x < lo) | (x > hi)]))


def print_box(st):
    print(f"Q1 = {st['q1']}, median = {st['med']}, Q3 = {st['q3']}, IQR = {st['iqr']}")
    print(f"lower bound = {st['lower_bound']}, upper bound = {st['upper_bound']}")
    print(f"lower whisker = {st['whislo']}, upper whisker = {st['whishi']}, "
          f"outliers = {st['fliers'].tolist()}")


def draw_course_boxplot(ax, st):
    """Boxplot with the course quartiles: matplotlib's bxp() draws given statistics."""
    ax.bxp([{k: st[k] for k in ("q1", "med", "q3", "whislo", "whishi", "fliers")}],
           vert=False)


# =====================================================================
# 1. SECTION "EMPIRICAL CUMULATIVE DISTRIBUTION FUNCTION"
# =====================================================================
header("1. Empirical CDF -- shoe sizes")

# SLIDE: "Frequency Table"
values, h = np.unique(shoe, return_counts=True)
freq = pd.DataFrame({"abs": h, "rel": h / n, "rel_%": 100 * h / n,
                     "cum": np.cumsum(h) / n}, index=values)
freq.index.name = "shoe size"
print(freq.round(4))
print("Total:", freq["abs"].sum(), "| sum of rel. frequencies:", freq["rel"].sum())

# SLIDE: "Empirical CDF in Python"
F = ECDF(shoe)
print("F(39) =", round(F(39), 4), "(= 7/11)")
print("F at 37, 38, 39, 40, 41, 46:", F([37, 38, 39, 40, 41, 46]).round(4))

# SLIDE: "Empirical CDF -- Reading Off Quantiles": median = smallest x with F(x) >= 0.5
print("Median from the ECDF:", values[np.argmax(F(values) >= 0.5)])

fig, ax = plt.subplots()
ax.ecdf(shoe)                           # step function incl. vertical jumps
ax.set_xlabel("Shoe size")
ax.set_ylabel("F(x)")
finish(fig, "ecdf_shoe.png")

# =====================================================================
# 2. SECTION "HISTOGRAM"
# =====================================================================
header("2. Histogram -- shoe sizes")

# SLIDES: "Histogram -- Construction (Table)" (class width 2, appears twice)
breaks2 = [37, 39, 41, 43, 45, 47]          # = np.arange(37, 48, 2)
tab2 = class_table(shoe, breaks2)
print("Class width 2:\n", tab2.round(4))
# expected densities: 0.3182, 0.1364, 0, 0, 0.0455

# SLIDE: "Histogram -- Alternative Classes (Class Width 3)"
breaks3 = [37, 40, 43, 46]
tab3 = class_table(shoe, breaks3)
print("\nClass width 3:\n", tab3.round(4))
# expected densities: 0.2727, 0.0303, 0.0303

# SLIDE: "Histogram -- Unequal Class Widths"
breaks_u = [37, 39, 40, 41, 46]
tab_u = class_table(shoe, breaks_u)
print("\nUnequal class widths:\n", tab_u.round(4))
# expected densities: 0.3182, 0.1818, 0.0909, 0.0182

# SLIDES: "Histograms in Python" / "Python Commands: Histogram"
fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
for ax, tab, br, title in zip(axes, (tab2, tab3, tab_u), (breaks2, breaks3, breaks_u),
                              ("Class width 2", "Class width 3", "Unequal widths")):
    density_hist(ax, tab, br)
    ax.set_title(title)
    ax.set_xlabel("Shoe size")
finish(fig, "hist_shoe.png")

# Area of every histogram = 1 (density * width = relative frequency)
for tab in (tab2, tab3, tab_u):
    assert np.isclose((tab["density"] * tab["width"]).sum(), 1)

# The trap: numpy / matplotlib use classes [a,b) (only the last one is [a,b]).
# 39 and 41 lie on class boundaries and end up in the wrong class:
wrong = np.histogram(shoe, bins=breaks2, density=True)[0]
print("\nnp.histogram (classes [a,b)) gives densities:", wrong.round(4),
      "<- NOT the slide values")
print("pd.cut (classes (a,b], first [a,b]) gives:     ",
      tab2["density"].to_numpy().round(4))

# SLIDE: "Python Commands: Classified Frequencies"
cls = pd.cut(shoe, breaks2, right=True, include_lowest=True)
print("\nClass of each observation:\n", [str(c) for c in cls])
print(pd.Series(cls).value_counts(sort=False))
print(pd.Series(cls).value_counts(normalize=True, sort=False).round(4))

# =====================================================================
# 3. SECTION "BOXPLOT"
# =====================================================================
header("3. Boxplot -- shoe sizes")

# SLIDE: "Boxplot -- Construction (Data)"
print("Sorted:", np.sort(shoe).tolist(), "| sum =", shoe.sum())

# SLIDE: "Boxplot -- Construction (Quartiles)": position ceil(n*p)
for p in (0.25, 0.50, 0.75):
    pos = int(np.ceil(n * p))
    print(f"p = {p:.2f}: n*p = {n * p:.2f}, position {pos}, value {np.sort(shoe)[pos - 1]}"
          f" | np.quantile(..., 'inverted_cdf') = {quantile(shoe, p)}")

# SLIDES: "Lower/Upper Whisker -- Computation / Step by Step"
st_shoe = boxplot_stats(shoe)
print_box(st_shoe)
# expected: Q1 38, median 39, Q3 40, IQR 2, bounds 35 / 43,
#           whiskers 37 / 41, outlier 46

# SLIDE: "Python Commands: Boxplot" -- matplotlib's own quartiles are interpolated
print("matplotlib/numpy default quartiles:", np.quantile(shoe, [0.25, 0.75]),
      "(Q1 = 38.5 instead of 38!)")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4), sharex=True)
ax1.boxplot(shoe, vert=False, whis=1.5)       # Tukey boxplot, interpolated quartiles
ax1.set_title("plt.boxplot (interpolated quartiles)")
draw_course_boxplot(ax2, st_shoe)              # course quartiles
ax2.set_title("Course definition (inverted_cdf)")
ax2.set_xlabel("Shoe size")
finish(fig, "boxplot_shoe.png")

# =====================================================================
# 4. SECTION "EXERCISE" -- BODY HEIGHTS
# =====================================================================
header("4. Exercise -- body heights")

heights = np.array([164, 162, 168, 198, 166, 166, 192, 160, 151, 175,
                    180, 160, 168, 175, 168])
m = len(heights)

# SLIDE: "Exercise: Body Heights -- Problem Statement"
print("Sorted:", np.sort(heights).tolist())

# SLIDE: "Exercise: Body Heights -- The Data"
hv, hh = np.unique(heights, return_counts=True)
print(pd.DataFrame({"abs": hh, "rel": hh / m, "cum": np.cumsum(hh) / m},
                   index=hv).round(4))
print("Sum of heights:", heights.sum())

# SLIDES: "Mean (Step by Step)", "Median and Mode", "Quartiles and Quantile"
mean = heights.mean()
print(f"\nMean = {heights.sum()} / {m} = {mean:.1f}")
print("Median (position ceil(15*0.5) = 8):", quantile(heights, 0.5))
print("Mode:", pd.Series(heights).mode().tolist())
print("17% quantile (position 3):", quantile(heights, 0.17))
print("Quartiles x_0.25, x_0.75 (positions 4, 12):", quantile(heights, [0.25, 0.75]))

# SLIDE: "Range and IQR"
print("Range R =", heights.max() - heights.min())
print("IQR =", quantile(heights, 0.75) - quantile(heights, 0.25))

# SLIDE: "Variance and Standard Deviation"
dev2 = (heights - mean) ** 2
print("(151 - 170.2)^2 =", round((151 - mean) ** 2, 2),
      "| (160 - 170.2)^2 =", round((160 - mean) ** 2, 2))
print("Sum of squared deviations =", round(dev2.sum(), 2))
s2 = heights.var(ddof=1)                       # ddof=1: divide by n - 1
s = heights.std(ddof=1)
print(f"s^2 = {s2:.2f}, s = {s:.4f}")

# SLIDE: "Coefficient of Variation"
v = s / mean
vstar = v / np.sqrt(m)
print(f"v = {v:.4f}, sqrt(15) = {np.sqrt(m):.4f}, v* = {vstar:.4f}")

# SLIDE: "Whisker Computation"
st_h = boxplot_stats(heights)
print_box(st_h)
# expected: bounds 142.5 / 194.5, whiskers 151 / 192, outlier 198

# SLIDE: "Exercise: Body Heights -- Results" (overview)
results = pd.Series({
    "Sum": heights.sum(), "Arithmetic mean": mean, "Median": st_h["med"],
    "Mode": pd.Series(heights).mode()[0], "1st quartile": st_h["q1"],
    "3rd quartile": st_h["q3"], "17% quantile": quantile(heights, 0.17),
    "Lower whisker": st_h["whislo"], "Lower bound": st_h["lower_bound"],
    "Upper whisker": st_h["whishi"], "Upper bound": st_h["upper_bound"],
    "Sample variance": s2, "Standard deviation": s,
    "Coefficient of variation": v, "Normalised coeff. of variation": vstar})
print("\nResults overview:\n", results.round(4).to_string())

# SLIDE: "Exercise: Body Heights -- Empirical CDF"
Fh = ECDF(heights)
print("\nF(168) =", round(Fh(168), 4), "-> first value with F >= 0.5: median 168")
fig, ax = plt.subplots()
ax.ecdf(heights)
ax.set_xlabel("Body height (cm)")
ax.set_ylabel("F(x)")
finish(fig, "ecdf_body_heights.png")

# SLIDE: "Exercise: Body Heights -- Classified Data (Class Width 10 cm)"
breaks_h = [150, 160, 170, 180, 190, 200]
tab_h = class_table(heights, breaks_h)
tab_h["midpoint"] = (np.asarray(breaks_h[:-1]) + np.asarray(breaks_h[1:])) / 2
tab_h["cum"] = tab_h["rel"].cumsum()
print(tab_h.round(4))
# expected: h_j = 3, 7, 3, 0, 2; F(a_j) = 0.2, 0.667, 0.867, 0.867, 1

# SLIDE: "Exercise: Body Heights -- Empirical CDF of the Classified Data"
# all observations of a class are placed at the class midpoint
classified = np.repeat(tab_h["midpoint"].to_numpy(), tab_h["abs"].to_numpy())
Fc = ECDF(classified)
print("Classified ECDF at the midpoints:", Fc(tab_h["midpoint"].to_numpy()).round(4))
print("Classified ECDF first reaches 0.5 at", quantile(classified, 0.5),
      "(exact median: 168)")
fig, ax = plt.subplots()
ax.ecdf(classified)
ax.set_xlabel("Body height (class midpoints, cm)")
finish(fig, "ecdf_body_heights_classified.png")

# SLIDE: "Exercise: Body Heights -- Histogram (Class Width 10 cm)"
fig, ax = plt.subplots()
density_hist(ax, tab_h, breaks_h)
ax.set_xlabel("Body height (cm)")
finish(fig, "hist_body_heights.png")
print("Densities:", tab_h["density"].round(4).tolist())

# SLIDE: "Exercise: Body Heights -- Boxplot"
fig, ax = plt.subplots()
draw_course_boxplot(ax, st_h)
ax.set_xlabel("Body height (cm)")
finish(fig, "boxplot_body_heights.png")

# =====================================================================
# 5. SECTION "PYTHON COMMANDS" -- shoe sizes
# =====================================================================
header("5. Python commands -- shoe sizes")

# SLIDE: "Python Commands: Frequencies and Measures of Central Tendency"
print(pd.Series(shoe).value_counts().sort_index())
print("mean =", round(np.mean(shoe), 4))
print("np.median =", np.median(shoe), "(averages the two middle values for even n)")
print("80% quantile =", quantile(shoe, 0.8))
print("quartiles =", quantile(shoe, [0.25, 0.5, 0.75]))

# SLIDE: "Python Commands: Measures of Dispersion"
s2_shoe = np.var(shoe, ddof=1)
s_shoe = np.std(shoe, ddof=1)
v_shoe = s_shoe / np.mean(shoe)
vstar_shoe = v_shoe / np.sqrt(len(shoe))
print(f"s^2 = {s2_shoe:.4f}, s = {s_shoe:.4f}, v = {v_shoe:.4f}, v* = {vstar_shoe:.4f}")
print(f"np.var without ddof (divides by n): {np.var(shoe):.4f}")

# SLIDES: "Python Commands: Empirical CDF / Histogram / Classified
# Frequencies / Boxplot" -- see sections 1-3 above (same commands).
print("\nDone.")

#!/usr/bin/env python3
# =====================================================================
# Quantitative Research -- Part 2: Graphical Representations
# Prof. Dr. Christoph Weisser
#
# Python companion to Part_2_Graphical_Representations.tex.
# Reproduces every number shown on the slides and draws the graphics
# (empirical CDF, histograms, boxplots).
#
# Organisation (search for "SLIDE:" to jump to the code of a slide):
#   0. Data and helper functions
#   1. Section "Empirical Cumulative Distribution Function"
#      1b. Exercise "Complaints per Day"
#   2. Section "Histogram"
#      2a. Quick exercise "Car Park" (reading a given histogram, with Python)
#      2b. Exercises "Histogram (Handball Team)" and "Mobile Phone Costs"
#   3. Section "Boxplot"
#      3a. Quick exercise "Daily Revenues" (whiskers by hand, even n)
#      3b. Exercise "Processing Times of Two Teams"
#   4. Section "Exercises" -- body heights
#      4b. Exercise "Cafe Chain (Exam Style)" (adapted from mock exam 3, task 1)
#   5. Section "Python Commands"
#
# The figures of the slides are drawn by make_figures.py (same folder).
# Companion notebook (same folder, also openable in Google Colab):
# Part_2_Graphical_Representations.ipynb -- its sections follow the slides.
# Requirements: numpy, pandas, scipy, statsmodels, matplotlib.
# The script runs headless (matplotlib backend "Agg"); figures are closed
# after drawing. Run with  python3 Part_2_Graphical_Representations.py --save DIR
# to store all figures as PNG files in DIR.
# =====================================================================
import math
import os
import sys
from fractions import Fraction

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
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


def quantile_exact(x, p):
    """The same definition computed with exact fractions: position ceil(n*p).

    np.quantile(..., method="inverted_cdf") works with floating-point numbers,
    so n*p can come out as e.g. 7.000000000000001 and the position is rounded
    up once too often (it happens e.g. for n = 25, p = 0.28). Every quantile on
    the slides is therefore checked against this exact version (check_q).
    """
    xs = np.sort(np.asarray(x))
    pos = max(1, math.ceil(len(xs) * Fraction(str(p))))
    return xs[pos - 1]


def check_q(x, ps):
    """Course quantiles for the probabilities ps -- asserts numpy == exact."""
    ps = np.atleast_1d(ps)
    q_np = quantile(x, ps)
    q_ex = np.array([quantile_exact(x, p) for p in ps])
    assert np.array_equal(q_np, q_ex), (q_np, q_ex)
    return q_ex


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
    q1, med, q3 = check_q(x, [0.25, 0.5, 0.75])
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

# SLIDE: "Empirical CDF -- Definition": F(x) = (number of observations <= x) / n
assert np.isclose(F(39), np.sum(shoe <= 39) / n)

# SLIDE: "Empirical CDF -- Reading Off Quantiles": x_p = min{x | F(x) >= p}
def quantile_from_ecdf(values, Fvals, p):
    """Smallest observed value whose ECDF value reaches p."""
    return values[np.argmax(Fvals >= p - 1e-12)]


print("F(38) =", round(F(38), 4), "< 0.5 <= F(39) =", round(F(39), 4))
print("Median from the ECDF:", quantile_from_ecdf(values, F(values), 0.5))
# SLIDE: "Empirical CDF -- Reading Off Quantiles Graphically" (80 % quantile)
print("F(39) =", round(F(39), 4), "< 0.8 <= F(40) =", round(F(40), 4),
      "-> x_0.8 =", quantile_from_ecdf(values, F(values), 0.8))
for a in (0.5, 0.8):                    # same as the position rule ceil(n*a)
    print(f"  p = {a}: position ceil({n}*{a}) = {math.ceil(n * a)},",
          "value", check_q(shoe, a)[0])
    assert quantile_from_ecdf(values, F(values), a) == check_q(shoe, a)[0]

fig, ax = plt.subplots()
ax.ecdf(shoe)                           # step function incl. vertical jumps
ax.set_xlabel("Shoe size")
ax.set_ylabel("F(x)")
finish(fig, "ecdf_shoe.png")

# ---------------------------------------------------------------------
# 1b. EXERCISE "COMPLAINTS PER DAY" (from SfOe Teil 2, "Reklamationen")
# ---------------------------------------------------------------------
header("1b. Exercise -- complaints per day")
compl = np.array([2, 0, 3, 1, 2, 5, 1, 3, 2, 6])

# SLIDE: "Solution (1/4) -- Complaints: Frequency Table and Empirical CDF"
print("Sorted:", np.sort(compl).tolist())
cv, ch = np.unique(compl, return_counts=True)
tab_c = pd.DataFrame({"h_j": ch, "f_j": ch / len(compl),
                      "F(x)": np.cumsum(ch) / len(compl)}, index=cv)
print(tab_c.round(4))                   # F: 0.1 0.3 0.6 0.8 0.9 1.0

# SLIDE: "Solution (2/4) -- Complaints: Reading Off Shares"
Fc = ECDF(compl)
print("F(2) =", Fc(2), "| F(4) = F(3) =", Fc(4), "| F(3) - F(1) =",
      round(Fc(3) - Fc(1), 4))          # 0.6, 0.8, 0.5

# SLIDE: "Solution (3/4) -- Complaints: Reading Off Quantiles"
print("Median and 80 % quantile:", check_q(compl, [0.5, 0.8]),
      "| positions:", math.ceil(10 * 0.5), "and", math.ceil(10 * 0.8))   # 2 3; 5, 8
assert quantile_from_ecdf(cv, Fc(cv), 0.5) == 2 and quantile_from_ecdf(cv, Fc(cv), 0.8) == 3

# SLIDE: "Solution (4/4) -- Complaints: Python" (exact code and output of the slide)
print(Fc(2), Fc(4), Fc(3) - Fc(1))                              # 0.6 0.8 0.5
print(np.quantile(compl, [0.5, 0.8], method="inverted_cdf"))    # [2 3]
fig, ax = plt.subplots()
ax.ecdf(compl)
ax.set_xlabel("Complaints per day")
finish(fig, "ecdf_complaints.png")

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
# key takeaway: (41,46] holds as many players as (40,41] (one each), but its
# bar is five times lower (width 5 instead of 1)
assert tab_u["abs"].iloc[3] == tab_u["abs"].iloc[2] == 1
print("density (40,41] / density (41,46] =",
      round(tab_u["density"].iloc[2] / tab_u["density"].iloc[3], 4))   # 5

# ---------------------------------------------------------------------
# 2a. QUICK EXERCISE "CAR PARK" (after "Histogram -- Alternative Class
#     Partition"): reading shares off a given histogram -- area = share.
#     Only the densities of the first three bars are given; the last one
#     follows from "all areas add up to 1".
# ---------------------------------------------------------------------
header("2a. Quick exercise -- car park (reading a histogram)")
n_park = 200
edges_p = np.array([0, 1, 2, 4, 10])                 # parking duration in hours
w_p = np.diff(edges_p)                               # class widths 1 1 2 6
dens_p3 = np.array([0.25, 0.3, 0.15])                # labels of the first three bars

# SLIDE: "Solution (1/3) -- Car Park: Shares from Areas"
f_p3 = dens_p3 * w_p[:3]                             # area = density * width = f_j
f_p4 = 1 - f_p3.sum()                                # all areas add up to 1
f_p = np.round(np.r_[f_p3, f_p4], 10)
tab_p = pd.DataFrame({"width": w_p, "density": np.round(f_p / w_p, 10), "f_j": f_p,
                      "h_j": np.round(f_p * n_park).astype(int)},
                     index=["[0,1]", "(1,2]", "(2,4]", "(4,10]"])
print(tab_p)         # f_j 0.25 0.3 0.3 0.15 | h_j 50 60 60 30 | last density 0.025
print(f"f_4 = 1 - {f_p3.sum():.2f} = {f_p4:.2f} | h_4 = {f_p4 * n_park:.0f}"
      f" | missing height = {f_p4:.2f} / {w_p[3]} = {f_p4 / w_p[3]:.4f}")
assert np.isclose(tab_p["f_j"].sum(), 1) and tab_p["h_j"].sum() == n_park

# SLIDE: "Solution (2/3) -- Car Park: Heights versus Areas"
print("height (1,2] / height (2,4] =", round(tab_p["density"].iloc[1] / tab_p["density"].iloc[2], 4),
      "| tickets:", tab_p["h_j"].iloc[1], "vs", tab_p["h_j"].iloc[2])      # 2.0 | 60 vs 60
free = tab_p["f_j"].iloc[0] + tab_p["f_j"].iloc[1]     # durations <= 2 h
print("share of tickets <= 2 h (free):", round(free, 4), "->",
      round(free * n_park), "tickets")                                      # 0.55 -> 110

# SLIDE: "Solution (3/3) -- Car Park: Python" (exact code and output of the slide)
w = np.diff([0, 1, 2, 4, 10])          # class widths: 1 1 2 6
dens = np.array([0.25, 0.3, 0.15])     # heights of the first three bars
f = dens * w[:3]                       # areas = shares: 0.25 0.3 0.3
f4 = 1 - f.sum()                       # all areas add up to 1: f4 = 0.15
print(round(f4 / w[3], 4), np.round(np.r_[f, f4] * 200), round(f[0] + f[1], 4))
# -> 0.025 [50. 60. 60. 30.] 0.55

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

# SLIDES: "Classified Frequencies in Python" / "Python Commands: Classified Frequencies"
cls = pd.cut(shoe, breaks2, right=True, include_lowest=True)
print("\nClass of each observation:\n", [str(c) for c in cls])
print(pd.Series(cls).value_counts(sort=False))
print(pd.Series(cls).value_counts(normalize=True, sort=False).round(4))

# ---------------------------------------------------------------------
# 2b. EXERCISES OF THE HISTOGRAM SECTION
# ---------------------------------------------------------------------
header("2b. Exercises -- histogram")

# SLIDES: "Exercise -- Histogram (Handball Team)", "Solution (1/2), (2/2)":
# shoe sizes of the handball team of Part 1 (n = 13), classes shifted by one size
handball = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39, 40, 42])
breaks_hb = [36, 38, 40, 42, 44, 46]
tab_hb = class_table(handball, breaks_hb)
print(tab_hb.round(4))                  # h_j 3 7 2 0 1; densities 0.1154 0.2692 0.0769 0 0.0385
print("Values on a class boundary:", int(np.isin(handball, breaks_hb).sum()), "of", len(handball))
# Task 3: the classes of the worked example give a different shape
tab_hb_alt = class_table(handball, [37, 39, 41, 43, 45, 47])
print("Classes [37,39], (39,41], ...: h_j =", tab_hb_alt["abs"].tolist(),   # 7 4 1 0 1
      "| densities", tab_hb_alt["density"].round(4).tolist())

# Exercise "Mobile Phone Costs" (from SfOe Teil 2, "Mobilfunkkosten")
costs = np.array([12, 25, 6, 38, 15, 60, 9, 19, 32, 18])
breaks_c = [0, 10, 20, 40, 80]

# SLIDE: "Solution (1/4) -- Mobile Phone Costs: Class Frequencies"
print("Sorted:", np.sort(costs).tolist())
tab_c = class_table(costs, breaks_c)
tab_c["values"] = [np.sort(costs[pd.cut(costs, breaks_c, include_lowest=True).codes == j]).tolist()
                   for j in range(len(breaks_c) - 1)]
print(tab_c)                            # h_j 2 4 3 1, f_j 0.2 0.4 0.3 0.1

# SLIDE: "Solution (2/4) -- Mobile Phone Costs: Densities and Histogram"
print("densities:", tab_c["density"].tolist())          # 0.02 0.04 0.015 0.0025
print("area of (20,40]: 0.015 * 20 =", round(0.015 * 20, 4),
      "| sum of all areas:", round((tab_c["density"] * tab_c["width"]).sum(), 4))

# SLIDE: "Solution (3/4) -- Mobile Phone Costs: Interpretation"
# wrong heights f_j would give the areas f_j * width:
print("areas with height f_j (wrong!):", (tab_c["rel"] * tab_c["width"]).round(4).tolist())
print("most densely populated class:", tab_c["density"].idxmax(),
      "with density", tab_c["density"].max())          # (10,20], 0.04

# SLIDE: "Solution (4/4) -- Mobile Phone Costs: Python" (code and output of the slide)
cls_c = pd.cut(costs, breaks_c, right=True, include_lowest=True)
h_c = pd.Series(cls_c).value_counts(sort=False).to_numpy()
print(h_c, h_c / len(costs) / np.diff(breaks_c))         # [2 4 3 1] [0.02 0.04 0.015 0.0025]
print("np.histogram gives the same here (no value on a boundary):",
      np.histogram(costs, bins=breaks_c, density=True)[0])
fig, ax = plt.subplots()
density_hist(ax, tab_c, breaks_c)
ax.set_xlabel("Monthly costs (EUR)")
finish(fig, "hist_phone_costs.png")

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

# ---------------------------------------------------------------------
# 3a. QUICK EXERCISE "DAILY REVENUES" (after "Upper Whisker -- Step by Step";
#     from SfOe Teil 2, "Tagesumsaetze"): even n, outlier at the bottom.
#     Same online shop and days as the exercise "Complaints per Day" (compl).
# ---------------------------------------------------------------------
header("3a. Quick exercise -- daily revenues of the online shop")
revenue = np.array([15, 18, 12, 22, 17, 13, 14, 20, 17, 4])   # 1000 EUR, days 1-10

# SLIDE: "Solution (1/2) -- Daily Revenues: Quartiles and Bounds"
print("Sorted:", np.sort(revenue).tolist())
for p in (0.25, 0.5, 0.75):              # n*p = 5 is an integer -> position 5
    print(f"  p = {p}: n*p = {len(revenue) * p:g} -> position "
          f"{math.ceil(len(revenue) * Fraction(str(p)))}")
st_rev = boxplot_stats(revenue)
print("1.5 * IQR =", 1.5 * st_rev["iqr"])
print_box(st_rev)
# expected: Q1 13, median 15, Q3 18, IQR 5, 1.5*IQR 7.5, bounds 5.5 / 25.5,
#           whiskers 12 / 22, outlier 4
rev = revenue                            # footnote of the slide
print(np.quantile(rev, [0.25, 0.5, 0.75], method="inverted_cdf"), np.median(rev))  # [13 15 18] 16.0

# SLIDE: "Solution (2/2) -- Daily Revenues: Whiskers, Outlier and Boxplot"
day_out = int(np.flatnonzero(revenue == st_rev["fliers"][0])[0]) + 1
print("outlier", st_rev["fliers"].tolist(), "on day", day_out, "| complaints that day:",
      compl[day_out - 1], "| most complaints of all days:", compl.max())   # day 10, 6, 6
fig, ax = plt.subplots()
draw_course_boxplot(ax, st_rev)
ax.set_xlabel("Daily revenue (in 1000 EUR)")
finish(fig, "boxplot_revenues.png")

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

# SLIDE: "Boxplot -- Interpretation (3/3)": both whiskers 1 unit from the box
print("whisker lengths:", st_shoe["q1"] - st_shoe["whislo"], st_shoe["whishi"] - st_shoe["q3"])

# ---------------------------------------------------------------------
# 3b. EXERCISE "PROCESSING TIMES OF TWO TEAMS" (from SfOe Teil 2,
#     "Bearbeitungszeiten")
# ---------------------------------------------------------------------
header("3b. Exercise -- processing times of two teams")
team_a = np.array([7, 4, 9, 6, 18, 8, 5, 10, 6, 9, 7])
team_b = np.array([12, 8, 15, 5, 14, 10, 16, 8, 11, 14, 7])

# SLIDES: "Solution (1/5) -- Team A", "Solution (2/5) -- Team B",
#         "Solution (3/5) -- Boxplots" (table)
st_team = {}
for name, x in (("A", team_a), ("B", team_b)):
    print(f"Team {name}, sorted:", np.sort(x).tolist(), "| positions",
          [math.ceil(len(x) * p) for p in (0.25, 0.5, 0.75)])
    st_team[name] = boxplot_stats(x)
    print_box(st_team[name])
# expected A: 6 7 9, IQR 3, bounds 1.5 / 13.5, whiskers 4 / 10, outlier 18
# expected B: 8 11 14, IQR 6, bounds -1 / 23, whiskers 5 / 16, no outlier

# SLIDE: "Solution (4/5) -- Processing Times: Comparison"
for name in ("A", "B"):
    st = st_team[name]
    print(f"Team {name}: median - Q1 = {st['med'] - st['q1']}, Q3 - median = "
          f"{st['q3'] - st['med']} | lower whisker {st['q1'] - st['whislo']}, "
          f"upper whisker {st['whishi'] - st['q3']}")
# A: 1 vs 2 (median in the left half) and outlier 18 on the right -> right-skewed,
#    although the upper whisker (1) is shorter than the lower one (2)
# B: 3 vs 3 (median in the middle), whiskers 3 and 2 -> roughly symmetric
# (The German source deck claimed "both whiskers 3 minutes" for B -- wrong: 3 and 2.)

# SLIDE: "Solution (5/5) -- Processing Times: Python" (code of the slide)
def box_stats(x, k=1.5):                    # course quartiles + 1.5 IQR rule
    q1, med, q3 = np.quantile(x, [0.25, 0.5, 0.75], method="inverted_cdf")
    lo, hi = q1 - k * (q3 - q1), q3 + k * (q3 - q1)
    inside = x[(x >= lo) & (x <= hi)]
    return dict(q1=q1, med=med, q3=q3, whislo=inside.min(), whishi=inside.max(),
                fliers=x[(x < lo) | (x > hi)])


stats_teams = [box_stats(team_a), box_stats(team_b)]
for st in stats_teams:                      # A: 4 6 7 9 10 [18]   B: 5 8 11 14 16 []
    print(st["whislo"], st["q1"], st["med"], st["q3"], st["whishi"], st["fliers"])
fig, ax = plt.subplots()
ax.bxp(stats_teams, vert=False)             # both boxplots above a common axis
ax.set_yticks([1, 2], ["Team A", "Team B"])
ax.set_xlabel("Processing time (minutes)")
finish(fig, "boxplot_teams.png")
# plt.boxplot interpolates -- for these data by chance with the same quartiles:
print("numpy default quartiles A:", np.quantile(team_a, [0.25, 0.75]),
      "B:", np.quantile(team_b, [0.25, 0.75]))

# =====================================================================
# 4. SECTION "EXERCISES" -- BODY HEIGHTS
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
print("Median (position ceil(15*0.5) = 8):", check_q(heights, 0.5)[0])
print("Mode:", pd.Series(heights).mode().tolist())
for p in (0.17, 0.25, 0.5, 0.75):      # rule: position = ceil(n*p)
    print(f"  p = {p}: n*p = {m * p:.2f} -> position {math.ceil(m * Fraction(str(p)))}")
print("17% quantile (position 3):", check_q(heights, 0.17)[0])
print("Quartiles x_0.25, x_0.75 (positions 4, 12):", check_q(heights, [0.25, 0.75]))

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
# Why 0 <= v* <= 1: for non-negative data v is at most sqrt(n); the maximum is
# attained when all values but one are 0, e.g. (1, 0, ..., 0):
extreme = np.r_[1.0, np.zeros(m - 1)]
v_max = extreme.std(ddof=1) / extreme.mean()
print(f"largest v for n = {m}: {v_max:.4f} = sqrt({m}) = {np.sqrt(m):.4f}")
assert np.isclose(v_max, np.sqrt(m))

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

# SLIDE: "Exercise: Body Heights -- Empirical CDF" (quantiles read off the ECDF)
Fh = ECDF(heights)
print("\nF(168) =", round(Fh(168), 4), "-> first value with F >= 0.5: median 168")
print("F at 151, 160, 162, 166, 168, 175:", Fh([151, 160, 162, 166, 168, 175]).round(4))
for a in (0.17, 0.25, 0.5, 0.75):       # x_p = min{x | F(x) >= p}
    xa = quantile_from_ecdf(hv, Fh(hv), a)
    print(f"  x_{a}: F({xa}) = {Fh(xa):.4f} >= {a} -> {xa}")
    assert xa == check_q(heights, a)[0]   # same as the position rule
fig, ax = plt.subplots()
ax.ecdf(heights)
ax.set_xlabel("Body height (cm)")
ax.set_ylabel("F(x)")
finish(fig, "ecdf_body_heights.png")

# SLIDE: "Exercise: Body Heights -- Histogram (Table)" and
#        "Exercise: Body Heights -- Classified Data (Class Width 10 cm)"
breaks_h = [150, 160, 170, 180, 190, 200]
tab_h = class_table(heights, breaks_h)
# boundary values: 160 (twice) belongs to [150,160], 180 to (170,180];
# np.histogram / plt.hist with classes [a,b) would count them in the next class
print("values of class (160,170]:", np.sort(heights[(heights > 160) & (heights <= 170)]).tolist())
print("np.histogram counts (classes [a,b)):", np.histogram(heights, bins=breaks_h)[0],
      "<- NOT 3 7 3 0 2")
tab_h["midpoint"] = (np.asarray(breaks_h[:-1]) + np.asarray(breaks_h[1:])) / 2
tab_h["cum"] = tab_h["rel"].cumsum()
print(tab_h.round(4))
# expected: h_j = 3, 7, 3, 0, 2; F(a_j) = 0.2, 0.667, 0.867, 0.867, 1

# SLIDE: "Exercise: Body Heights -- Empirical CDF of the Classified Data"
# all observations of a class are placed at the class midpoint
classified = np.repeat(tab_h["midpoint"].to_numpy(), tab_h["abs"].to_numpy())
Fc = ECDF(classified)
print("Classified ECDF at the midpoints:", Fc(tab_h["midpoint"].to_numpy()).round(4))
print("Classified ECDF first reaches 0.5 at", check_q(classified, 0.5)[0],
      "(exact median: 168)")
print("number of steps: raw", len(hv), "| classified", int((tab_h["abs"] > 0).sum()))
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

# SLIDE: "Exercise: Body Heights -- Python" (code of the slide)
print(np.quantile(heights, [0.17, 0.25, 0.5, 0.75], method="inverted_cdf"))  # 160 162 168 175
cls_h = pd.cut(heights, breaks_h, right=True, include_lowest=True)
h_h = pd.Series(cls_h).value_counts(sort=False).to_numpy()
print(h_h, (h_h / m / np.diff(breaks_h)).round(4))       # 3 7 3 0 2 | densities
classified2 = np.repeat([155, 165, 175, 185, 195], h_h)
print(classified2, np.quantile(classified2, 0.5, method="inverted_cdf"))   # ... 165
assert np.array_equal(classified, classified2)

# ---------------------------------------------------------------------
# 4b. EXERCISE "CAFE CHAIN (EXAM STYLE)" -- adapted from mock exam 3, task 1
#     (Statistik fuer Oekonomen); Part B uses the classes of the variant in
#     Aufgaben_Auswahl.docx, turned into a reading task.
# ---------------------------------------------------------------------
header("4b. Exercise -- cafe chain (exam style)")

# Part A: only the boxplot is given (n = 60 daily revenues, in 100 EUR)
cafe = dict(whislo=15, q1=24, med=28, q3=36, whishi=50, fliers=[62])
n_cafe = 60

# SLIDE: "Solution (1/5) -- Cafe Chain: Reading Off the Boxplot"
iqr_cafe = cafe["q3"] - cafe["q1"]
print("IQR =", iqr_cafe)                                  # 12 (= 1200 EUR)

# SLIDE: "Solution (2/5) -- Cafe Chain: Share of Days and Fences"
print("median position ceil(60 * 0.5) =", math.ceil(n_cafe * 0.5),
      "-> at least 30 days with revenue <= 28")           # 30
lo_c = cafe["q1"] - 1.5 * iqr_cafe
hi_c = cafe["q3"] + 1.5 * iqr_cafe
print("fences:", lo_c, hi_c)                              # 6.0 54.0
assert cafe["fliers"][0] > hi_c                           # 62 is an outlier
assert cafe["whishi"] <= hi_c and cafe["whislo"] >= lo_c  # whiskers inside the fences

# SLIDE: "Solution (3/5) -- Cafe Chain: Skewness"
print("median - Q1 =", cafe["med"] - cafe["q1"], "| Q3 - median =", cafe["q3"] - cafe["med"])
print("lower whisker =", cafe["q1"] - cafe["whislo"], "| upper whisker =",
      cafe["whishi"] - cafe["q3"])                        # 4 vs 8, 9 vs 14 -> right-skewed

# Part B: histogram of n = 50 order values, classes [0,5], (5,10], (10,20], (20,40]
# SLIDE: "Solution (4/5) -- Cafe Chain: Reading the Histogram"
edges_o = np.array([0, 5, 10, 20, 40])
dens_o = np.array([0.04, 0.06, 0.04, 0.005])             # read off the bars
tab_o = pd.DataFrame({"width": np.diff(edges_o), "density": dens_o})
tab_o["f_j"] = (tab_o["density"] * tab_o["width"]).round(10)   # area = rel. frequency
tab_o["h_j"] = (tab_o["f_j"] * 50).round(10)
tab_o.index = ["[0,5]", "(5,10]", "(10,20]", "(20,40]"]
print(tab_o)                                              # f 0.2 0.3 0.4 0.1, h 10 15 20 5
assert np.isclose(tab_o["f_j"].sum(), 1) and tab_o["h_j"].sum() == 50
print("highest bar:", tab_o["density"].idxmax(), "| most orders:", tab_o["h_j"].idxmax())
print("share of orders > 10 EUR:", tab_o["f_j"].iloc[2:].sum())   # 0.5 (25 orders)

# Part C: repair times of the espresso machine (minutes)
# SLIDE: "Solution (5/5) -- Cafe Chain: Robust Measures of Location"
rep = np.array([2, 3, 3, 4, 5, 6, 26])
print("sum =", rep.sum(), "| mean =", rep.mean())        # 49, 7.0
print("median (position ceil(3.5) = 4):", check_q(rep, 0.5)[0])            # 4
print("trimmed mean (min and max removed):", np.sort(rep)[1:-1].mean(),
      "| scipy:", stats.trim_mean(rep, 0.15))            # 4.2 (cuts int(0.15*7) = 1 per end)
st_rep = boxplot_stats(rep)
print_box(st_rep)                                         # Q1 3, Q3 6, IQR 3, fence 10.5 -> 26
print("values above the mean:", int((rep > rep.mean()).sum()), "of", len(rep))
print(rep.mean(), np.quantile(rep, 0.5, method="inverted_cdf"), np.sort(rep)[1:-1].mean())

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

# SLIDE: "Python Commands: Empirical CDF"
print("F(40) - F(38) =", round(F(40) - F(38), 4), "(= 6/11)")
print("quantiles 0.5, 0.8:", np.quantile(shoe, [0.5, 0.8], method="inverted_cdf"))  # 39 40

# SLIDE: "Python Commands: Boxplots of Several Groups" -- box_stats() from 3b;
# box_stats(shoe) reproduces the shoe-size boxplot:
st_check = box_stats(shoe)
assert all(np.all(st_check[k] == st_shoe[k]) for k in ("q1", "med", "q3", "whislo", "whishi"))
assert np.array_equal(st_check["fliers"], st_shoe["fliers"])

# SLIDES: "Python Commands: Histogram / Classified Frequencies / Boxplot"
# -- see sections 2-3 above (same commands).

# Sanity check of the exact quantile helper: numpy's inverted_cdf can be off by
# one position because of floating-point rounding (not for any data set of
# this deck, see check_q above), e.g.
x25 = np.arange(1, 26)
print("n = 25, p = 0.28: numpy", quantile(x25, 0.28), "| exact", quantile_exact(x25, 0.28),
      "(25 * 0.28 =", 25 * 0.28, ")")
print("\nDone.")

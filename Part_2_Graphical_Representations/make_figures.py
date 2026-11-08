#!/usr/bin/env python3
"""Figures for Part 2 (English labels, decimal point).

Writes into images/:

  Section "Empirical CDF"
    ecdf_shoe_quantiles.png          shoe sizes: reading off median and 80 % quantile
    ecdf_complaints.png              exercise "complaints per day"
  Section "Histogram"
    hist_parking.png                 quick exercise "car park" (reading a given
                                     histogram, last label missing; task figure)
    hist_phone_costs.png             exercise "mobile phone costs" (unequal widths)
    hist_handball.png                exercise "histogram (handball team)"
  Section "Boxplot"
    boxplot_shoe_labelled.png        shoe sizes, boxplot with labels
    boxplot_revenues.png             quick exercise "daily revenues" (even n,
                                     outlier at the bottom; solution figure)
    boxplot_teams.png                exercise "processing times" (two teams)
  Section "Exercises" -- body heights
    ecdf_body_heights.png            empirical CDF of the raw data
    ecdf_body_heights_classified.png empirical CDF of the classified data
                                     (stand-alone; the slides show the comparison)
    ecdf_body_heights_comparison.png both side by side
    hist_body_heights.png            density histogram, class width 10 cm
  Section "Exercises" -- cafe chain (exam style)
    boxplot_cafe.png                 boxplot of n = 60 daily revenues (task figure)
    boxplot_cafe_solution.png        the same boxplot with all values and fences
    hist_cafe_orders.png             histogram of n = 50 order values (task figure)

All boxplots use the course quartiles x_(ceil(n*p)) (drawn with Axes.bxp from
exactly these statistics, not with plt.boxplot, which interpolates).
The remaining images of the deck (image_004.png, hist_kb2.png,
hist_andere_klassen.png, boxplot_schuhgroessen_clean.png,
boxplot_koerpergroesse.png) were created earlier and are not redrawn here;
boxplot_schuhgroessen.png is superseded by boxplot_shoe_labelled.png.
Requires numpy and matplotlib.
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
BLUE = "#3366B8"        # lines (ECDF)
BAR = "#4472C4"         # histogram bars (as in hist_kb2.png)
BOX = "#3B6FB6"         # boxplot boxes (as in boxplot_koerpergroesse.png)
ORANGE = "#E69F00"      # hsbiorange: second group / second quantile
RED = "#C0392B"         # hsbirot: outliers, fences, quantile levels p
GREY = "#6B6B6B"

plt.rcParams.update({"font.size": 13, "axes.titlesize": 15, "axes.labelsize": 14,
                     "axes.grid": True, "grid.alpha": 0.35})


def save(fig, fname):
    """Write images/<fname> (dpi 150, as all figures of this deck) and close."""
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    plt.close(fig)
    print("wrote", fname)


def course_quantile(x, p):
    """Course definition x_(ceil(n*p)) -- computed exactly (no floating-point
    trouble with n*p), identical to np.quantile(..., method="inverted_cdf")."""
    xs = np.sort(np.asarray(x))
    pos = max(1, math.ceil(round(len(xs) * p, 9)))
    return xs[pos - 1]


def course_box_stats(x, k=1.5):
    """Statistics for Axes.bxp with the course quartiles and Tukey's 1.5*IQR rule."""
    x = np.asarray(x)
    q1, med, q3 = (course_quantile(x, p) for p in (0.25, 0.5, 0.75))
    lo, hi = q1 - k * (q3 - q1), q3 + k * (q3 - q1)
    inside = x[(x >= lo) & (x <= hi)]
    return dict(q1=q1, med=med, q3=q3, whislo=inside.min(), whishi=inside.max(),
                fliers=x[(x < lo) | (x > hi)])


def class_counts(x, edges):
    """Absolute frequencies of the classes [e0,e1], (e1,e2], ..., (e_{k-1},e_k]
    (course convention: first class closed, all others open on the left)."""
    x = np.asarray(x)
    out = [np.sum((x >= edges[0]) & (x <= edges[1]))]
    out += [np.sum((x > a) & (x <= b)) for a, b in zip(edges[1:-1], edges[2:])]
    return np.array(out)


def tidy(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def draw_ecdf(ax, values, weights, xlim, levels=(0.5,)):
    """Step function with dots at the observed values (style of this deck)."""
    order = np.argsort(values)
    v, w = np.asarray(values, dtype=float)[order], np.asarray(weights)[order]
    F = np.cumsum(w) / w.sum()
    xs = np.concatenate([[xlim[0]], v, [xlim[1]]])
    Fs = np.concatenate([[0], F, [1]])
    ax.step(xs, Fs, where="post", color=BLUE, lw=2.2)
    ax.plot(v, F, "o", color=BLUE, ms=6)
    ax.vlines(v, np.concatenate([[0], F[:-1]]), F, colors=BLUE, linestyles="dotted", lw=1.2)
    for a in levels:
        ax.axhline(a, color=RED, lw=1, ls="--")
        ax.text(xlim[0] + 0.015 * (xlim[1] - xlim[0]), a + 0.02, f"{a:g}", color=RED,
                fontsize=11)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.03, 1.05)
    ax.set_ylabel(r"$F(x)$")
    tidy(ax)


def ecdf_plot(values, weights, title, fname, xlim=(145, 205), xlabel="Body height (cm)",
              levels=(0.5,), figsize=(8, 4.6)):
    fig, ax = plt.subplots(figsize=figsize)
    draw_ecdf(ax, values, weights, xlim, levels)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    fig.tight_layout()
    save(fig, fname)


def density_bars(ax, edges, dens, labels=True, fmt="{:g}", fontsize=12):
    edges = np.asarray(edges, dtype=float)
    ax.bar(edges[:-1], dens, width=np.diff(edges), align="edge",
           color=BAR, edgecolor="black", lw=1.2, zorder=3)
    if labels:
        for a, b, d in zip(edges[:-1], edges[1:], dens):
            ax.text((a + b) / 2, d, fmt.format(d), ha="center", va="bottom",
                    fontsize=fontsize, color="black", zorder=4)
    ax.grid(axis="x", visible=False)
    ax.set_xticks(edges)


# =====================================================================
# Section "Empirical CDF"
# =====================================================================
# Shoe sizes (running example): reading off the median and the 80 % quantile
shoe = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39])
sv, sc = np.unique(shoe, return_counts=True)
fig, ax = plt.subplots(figsize=(8, 4.6))
draw_ecdf(ax, sv, sc, (35, 48), levels=())
# label positions chosen in free areas next to the arrows
for a, col, lab, (tx, ty, ha) in (
        (0.5, RED, r"$\tilde{x} = x_{0.5} = 39$", (-0.15, 0.37, "right")),
        (0.8, ORANGE, r"$x_{0.8} = 40$", (0.15, 0.70, "left"))):
    q = course_quantile(shoe, a)
    ax.hlines(a, 35, q, colors=col, linestyles="--", lw=1.6)
    ax.annotate("", xy=(q, 0), xytext=(q, a),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, ls="--"))
    ax.text(35.2, a + 0.025, f"{a:g}", color=col, fontsize=12)
    ax.text(q + tx, ty, lab, color=col, fontsize=13, ha=ha)
ax.set_xlabel("Shoe size")
ax.set_title("Reading Off Quantiles from the Empirical CDF")
fig.tight_layout()
save(fig, "ecdf_shoe_quantiles.png")

# Exercise "complaints per day" (n = 10)
complaints = np.array([2, 0, 3, 1, 2, 5, 1, 3, 2, 6])
cv, cc = np.unique(complaints, return_counts=True)
ecdf_plot(cv, cc, "Empirical CDF – Complaints per Day", "ecdf_complaints.png",
          xlim=(-1, 7.5), xlabel="Complaints per day", levels=(0.5, 0.8),
          figsize=(6.4, 4.8))

# =====================================================================
# Section "Histogram"
# =====================================================================
# Quick exercise "car park": histogram of the parking durations of n = 200
# tickets, classes [0,1], (1,2], (2,4], (4,10] (hours). Only the densities of the
# first three bars are printed; the last bar is drawn at its true height 0.025
# (students get it from "all areas add up to 1").
edges_p = np.array([0, 1, 2, 4, 10])
f_p = np.array([0.25, 0.30, 0.30, 0.15])                # areas = shares
dens_p = f_p / np.diff(edges_p)                          # 0.25 0.3 0.15 0.025
fig, ax = plt.subplots(figsize=(6.4, 4.4))
density_bars(ax, edges_p, dens_p, labels=False)
for a, b, d, lab in zip(edges_p[:-1], edges_p[1:], dens_p, ("0.25", "0.3", "0.15", "?")):
    ax.text((a + b) / 2, d + 0.004, lab, ha="center", va="bottom", fontsize=15,
            color=RED if lab == "?" else "black", zorder=4)
ax.set_ylim(0, 0.35)
ax.set_xlim(-0.3, 10.3)
ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.set_xlabel("Parking duration (hours)")
ax.set_ylabel(r"Density $f_j/\Delta x_j$")
ax.set_title("Histogram – Car Park (n = 200 tickets)")
tidy(ax)
fig.tight_layout()
save(fig, "hist_parking.png")

# Exercise "mobile phone costs" (n = 10), classes [0,10], (10,20], (20,40], (40,80]
costs = np.array([12, 25, 6, 38, 15, 60, 9, 19, 32, 18])
edges_c = np.array([0, 10, 20, 40, 80])
h_c = class_counts(costs, edges_c)                     # 2 4 3 1
dens_c = h_c / len(costs) / np.diff(edges_c)            # 0.02 0.04 0.015 0.0025
fig, ax = plt.subplots(figsize=(6.4, 4.8))
density_bars(ax, edges_c, dens_c)
ax.set_ylim(0, 0.046)
ax.set_xlabel("Monthly costs (EUR)")
ax.set_ylabel(r"Density $f_j/\Delta x_j$")
ax.set_title("Histogram – Mobile Phone Costs")
tidy(ax)
fig.tight_layout()
save(fig, "hist_phone_costs.png")

# Exercise "histogram (handball team)": shoe sizes of Part 1's handball team
# (n = 13), classes [36,38], (38,40], ..., (44,46]
handball = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39, 40, 42])
edges_h = np.array([36, 38, 40, 42, 44, 46])
h_h = class_counts(handball, edges_h)                   # 3 7 2 0 1
dens_h = h_h / len(handball) / np.diff(edges_h)         # 0.1154 0.2692 0.0769 0 0.0385
fig, ax = plt.subplots(figsize=(6.4, 4.6))
density_bars(ax, edges_h, dens_h, labels=False)
for a, b, d in zip(edges_h[:-1], edges_h[1:], dens_h):
    ax.text((a + b) / 2, d, f"{d:.4f}" if d > 0 else "0", ha="center",
            va="bottom", fontsize=12, zorder=4)
ax.set_ylim(0, 0.30)
ax.set_xlabel("Shoe size")
ax.set_ylabel(r"Density $f_j/\Delta x_j$")
ax.set_title("Histogram – Handball Team")
tidy(ax)
fig.tight_layout()
save(fig, "hist_handball.png")

# =====================================================================
# Section "Boxplot"
# =====================================================================
# Shoe sizes with labels (terms as on the slides: lower/upper whisker)
st = course_box_stats(shoe)                    # 37 38 39 40 41, outlier 46
fig, ax = plt.subplots(figsize=(12.8, 4.6))
ax.bxp([st], vert=False, widths=0.5, patch_artist=True,
       boxprops=dict(facecolor=BOX, edgecolor="black", lw=1.2),
       medianprops=dict(color="black", lw=1.6),
       whiskerprops=dict(lw=1.2), capprops=dict(lw=1.2),
       flierprops=dict(marker="o", markerfacecolor="none", markeredgecolor="black",
                       markersize=9, mew=1.6))
for x, txt, col in ((st["whislo"], "Lower whisker\n37", GREY),
                    (st["whishi"], "Upper whisker\n41", GREY),
                    (46, "Outlier\n46", RED)):
    ax.annotate(txt, xy=(x, 1.3 if col == GREY else 1.07), xytext=(x, 1.75),
                ha="center", va="bottom", color=col, fontsize=15,
                arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
for x, txt in ((38, r"$Q_1 = 38$"), (39, "Median\n39"), (40, r"$Q_3 = 40$")):
    ax.text(x, 0.6, txt, ha="center", va="top", fontsize=15)
ax.set_ylim(0.0, 2.2)
ax.set_xlim(35.5, 47)
ax.set_yticks([])
ax.grid(False)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.set_xlabel("Shoe size", fontsize=16)
ax.tick_params(axis="x", labelsize=16)
fig.tight_layout()
save(fig, "boxplot_shoe_labelled.png")

# Quick exercise "daily revenues" of the online shop (n = 10 days, in 1000 EUR):
# even n, outlier at the bottom (day 10)
revenue = np.array([15, 18, 12, 22, 17, 13, 14, 20, 17, 4])
st_r = course_box_stats(revenue)               # 12 13 15 18 22, outlier 4
lo_r = st_r["q1"] - 1.5 * (st_r["q3"] - st_r["q1"])      # 5.5
hi_r = st_r["q3"] + 1.5 * (st_r["q3"] - st_r["q1"])      # 25.5
fig, ax = plt.subplots(figsize=(6.2, 3.9))
ax.bxp([st_r], vert=False, widths=0.5, patch_artist=True,
       boxprops=dict(facecolor=BOX, edgecolor="black", lw=1.2),
       medianprops=dict(color="black", lw=2.2),
       whiskerprops=dict(lw=1.2), capprops=dict(lw=1.2),
       flierprops=dict(marker="o", markerfacecolor="none", markeredgecolor=RED,
                       markersize=9, mew=1.8))
for fence, txt in ((lo_r, "Lower bound\n5.5"), (hi_r, "Upper bound\n25.5")):
    ax.axvline(fence, color=RED, ls=":", lw=1.6)
    ax.text(fence, 0.42, txt, ha="center", va="bottom", fontsize=13, color=RED,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
# whisker labels just above the caps, box labels above the box (staggered,
# so that 12 and 13 do not collide)
for x, y, txt in ((st_r["whislo"], 1.14, "12"), (st_r["q1"], 1.29, "13"),
                  (st_r["med"], 1.29, "15"), (st_r["q3"], 1.29, "18"),
                  (st_r["whishi"], 1.14, "22")):
    ax.text(x, y, txt, ha="center", va="bottom", fontsize=14)
ax.text(4, 1.12, "Outlier 4\n(day 10)", ha="center", va="bottom", fontsize=13, color=RED)
ax.set_ylim(0.35, 1.75)
ax.set_xlim(2, 27)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.grid(axis="y", visible=False)
ax.grid(axis="x", which="both", alpha=0.3)
ax.set_yticks([])
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.set_xlabel("Daily revenue (in 1000 EUR)")
ax.set_title("Boxplot – Daily Revenues (n = 10)")
fig.tight_layout()
save(fig, "boxplot_revenues.png")

# Exercise "processing times" (two teams, n = 11 each)
team_a = np.array([7, 4, 9, 6, 18, 8, 5, 10, 6, 9, 7])
team_b = np.array([12, 8, 15, 5, 14, 10, 16, 8, 11, 14, 7])
fig, ax = plt.subplots(figsize=(6.6, 3.6))
bp = ax.bxp([course_box_stats(team_a), course_box_stats(team_b)], vert=False,
            widths=0.55, patch_artist=True,
            medianprops=dict(color="black", lw=2.4),
            flierprops=dict(marker="o", markerfacecolor="none", markeredgecolor="black",
                            markersize=8, mew=1.5))
for patch, col in zip(bp["boxes"], (BOX, ORANGE)):
    patch.set_facecolor(col)
ax.set_yticks([1, 2], ["Team A", "Team B"])
ax.xaxis.set_major_locator(MultipleLocator(2))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.grid(axis="y", visible=False)
ax.grid(axis="x", which="both", alpha=0.3)
ax.set_xlim(3, 19)
ax.set_xlabel("Processing time (minutes)")
ax.set_title("Processing Times – Team A vs. Team B")
fig.tight_layout()
save(fig, "boxplot_teams.png")

# =====================================================================
# Section "Exercises" -- body heights
# =====================================================================
heights = np.array([164, 162, 168, 198, 166, 166, 192, 160, 151, 175,
                    180, 160, 168, 175, 168])
vals, counts = np.unique(heights, return_counts=True)
ecdf_plot(vals, counts, "Empirical CDF – Body Heights", "ecdf_body_heights.png")

# classes [150,160], (160,170], (170,180], (180,190], (190,200] -> midpoints
mids = np.array([155, 165, 175, 185, 195])
cls_counts = class_counts(heights, np.arange(150, 201, 10))   # 3 7 3 0 2
keep = cls_counts > 0
ecdf_plot(mids[keep], cls_counts[keep],
          "Empirical CDF – Classified Data (Class Midpoints)",
          "ecdf_body_heights_classified.png")

# both empirical CDFs side by side (same axes)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.0), sharey=True)
draw_ecdf(axes[0], vals, counts, (145, 205))
draw_ecdf(axes[1], mids[keep], cls_counts[keep], (145, 205))
axes[0].set_title("Raw data (10 different values)")
axes[1].set_title("Classified data (class midpoints)")
for ax in axes:
    ax.set_xlabel("Body height (cm)")
axes[1].set_ylabel("")
fig.tight_layout()
save(fig, "ecdf_body_heights_comparison.png")

# density histogram, classes [150,160], (160,170], ..., (190,200]
edges = np.arange(150, 201, 10)
dens = cls_counts / cls_counts.sum() / np.diff(edges)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(edges[:-1], dens, width=np.diff(edges), align="edge",
       color=BAR, edgecolor="black", lw=1.2, zorder=3)
ax.grid(axis="x", visible=False)
ax.set_xticks(edges)
ax.set_xlabel("Body height (cm)")
ax.set_ylabel(r"Density $f_j/\Delta x_j$")
ax.set_title("Histogram (Class Width 10 cm)")
fig.tight_layout()
save(fig, "hist_body_heights.png")

# =====================================================================
# Section "Exercises" -- cafe chain (exam style, adapted from mock exam 3)
# =====================================================================
# Only the five boxplot values and the outlier are given (n = 60 days).
cafe = dict(whislo=15, q1=24, med=28, q3=36, whishi=50, fliers=[62])


def cafe_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    # light box fill and grid lines drawn on top, so that every value can be
    # read off to the unit (exam figure)
    ax.bxp([cafe], vert=False, widths=0.5, patch_artist=True,
           boxprops=dict(facecolor="#CFE0F0", edgecolor="black", lw=1.4),
           medianprops=dict(color=BLUE, lw=3),
           whiskerprops=dict(lw=1.4), capprops=dict(lw=1.4),
           flierprops=dict(marker="o", markerfacecolor="none", markeredgecolor="black",
                           markersize=9, mew=1.6))
    ax.set_axisbelow(False)
    ax.set_xlim(4, 66)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(axis="x", which="major", color="#888888", alpha=0.6, lw=0.9)
    ax.grid(axis="x", which="minor", color="#AAAAAA", alpha=0.45, lw=0.5)
    ax.grid(axis="y", visible=False)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("Daily revenue (in 100 EUR)")
    return fig, ax


fig, ax = cafe_axes((8, 2.0))
ax.set_ylim(0.6, 1.4)
fig.tight_layout()
save(fig, "boxplot_cafe.png")

fig, ax = cafe_axes((8, 3.2))
ax.set_ylim(0.35, 1.65)
WHITE = dict(facecolor="white", edgecolor="none", pad=1.5)   # opaque label background
for fence in (6, 54):
    ax.axvline(fence, color=RED, ls=":", lw=1.8)
for x, y, txt in ((15, 1.33, "Lower whisker\n15"), (24, 1.33, r"$Q_1 = 24$"),
                  (36, 1.33, r"$Q_3 = 36$"), (50, 1.33, "Upper whisker\n50")):
    ax.text(x, y, txt, ha="center", va="bottom", fontsize=12, color=BLUE, bbox=WHITE)
ax.text(28, 0.67, "Median 28", ha="center", va="top", fontsize=12, color=BLUE, bbox=WHITE)
ax.text(62, 1.12, "Outlier 62", ha="center", va="bottom", fontsize=12, color=RED, bbox=WHITE)
for fence, txt in ((6, "Lower fence 6"), (54, "Upper fence 54")):
    ax.text(fence + 0.6, 0.45, txt, ha="left", va="bottom", fontsize=12, color=RED,
            bbox=WHITE)
fig.tight_layout()
save(fig, "boxplot_cafe_solution.png")

# Histogram of the order values (n = 50): classes [0,5], (5,10], (10,20], (20,40]
edges_o = np.array([0, 5, 10, 20, 40])
h_o = np.array([10, 15, 20, 5])
dens_o = h_o / h_o.sum() / np.diff(edges_o)              # 0.04 0.06 0.04 0.005
# compact figure without title (the slide shows it in a narrow column, so the
# densities written on the bars must stay large enough to be read off)
fig, ax = plt.subplots(figsize=(5.0, 2.8))
density_bars(ax, edges_o, dens_o, fontsize=15)
ax.set_ylim(0, 0.072)
ax.set_xlim(-1.5, 41)
ax.yaxis.set_major_locator(MultipleLocator(0.02))
ax.tick_params(labelsize=13)
ax.set_xlabel("Order value (EUR)", fontsize=13)
ax.set_ylabel("Density", fontsize=13)
tidy(ax)
fig.tight_layout()
save(fig, "hist_cafe_orders.png")

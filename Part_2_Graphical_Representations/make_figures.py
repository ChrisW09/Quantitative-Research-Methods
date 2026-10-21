#!/usr/bin/env python3
"""Figures for the body-heights exercise of Part 2 (English labels).

Writes images/ecdf_body_heights.png and images/ecdf_body_heights_classified.png:
the empirical CDF of the raw data and of the classified data (class
midpoints, class width 10 cm), and images/hist_body_heights.png: the
density histogram with class width 10 cm. Requires numpy and matplotlib.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
BLUE = "#3366B8"

heights = np.array([164, 162, 168, 198, 166, 166, 192, 160, 151, 175,
                    180, 160, 168, 175, 168])

plt.rcParams.update({"font.size": 13, "axes.titlesize": 15, "axes.labelsize": 14,
                     "axes.grid": True, "grid.alpha": 0.35})


def ecdf_plot(values, weights, title, fname, annotate=None):
    order = np.argsort(values)
    v, w = np.asarray(values)[order], np.asarray(weights)[order]
    F = np.cumsum(w) / w.sum()
    fig, ax = plt.subplots(figsize=(8, 4.6))
    xs = np.concatenate([[145], v, [205]])
    Fs = np.concatenate([[0], F, [1]])
    ax.step(xs, Fs, where="post", color=BLUE, lw=2.2)
    ax.plot(v, F, "o", color=BLUE, ms=6)
    ax.vlines(v, np.concatenate([[0], F[:-1]]), F, colors=BLUE, linestyles="dotted", lw=1.2)
    ax.axhline(0.5, color="#C0392B", lw=1, ls="--")
    ax.text(146, 0.52, "0.5", color="#C0392B", fontsize=11)
    if annotate:
        for x, y, txt in annotate:
            ax.annotate(txt, (x, y), textcoords="offset points", xytext=(6, -16), fontsize=10)
    ax.set_xlim(145, 205)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel("Body height (cm)")
    ax.set_ylabel(r"$F(x)$")
    ax.set_title(title)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    plt.close(fig)
    print("wrote", fname)


vals, counts = np.unique(heights, return_counts=True)
ecdf_plot(vals, counts, "Empirical CDF – Body Heights", "ecdf_body_heights.png")

# classes [150,160], (160,170], (170,180], (180,190], (190,200] -> midpoints
mids = np.array([155, 165, 175, 185, 195])
cls_counts = np.array([3, 7, 3, 0, 2])
keep = cls_counts > 0
ecdf_plot(mids[keep], cls_counts[keep],
          "Empirical CDF – Classified Data (Class Midpoints)",
          "ecdf_body_heights_classified.png")


# density histogram, classes [150,160], (160,170], ..., (190,200]
edges = np.arange(150, 201, 10)
dens = cls_counts / cls_counts.sum() / np.diff(edges)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(edges[:-1], dens, width=np.diff(edges), align="edge",
       color="#4472C4", edgecolor="black", lw=1.2, zorder=3)
ax.grid(axis="x", visible=False)
ax.set_xticks(edges)
ax.set_xlabel("Body height (cm)")
ax.set_ylabel(r"Density $f_j/\Delta x_j$")
ax.set_title("Histogram (Class Width 10 cm)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "hist_body_heights.png"), dpi=150)
plt.close(fig)
print("wrote hist_body_heights.png")

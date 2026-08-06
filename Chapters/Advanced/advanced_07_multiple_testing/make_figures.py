"""Generate the computed matplotlib figures for advanced module A7 (Multiple Testing).

Everything is computed exactly or from a clearly labelled, seeded simulation
--- nothing is sketched by hand. Run from anywhere:

    python Chapters/Advanced/advanced_07_multiple_testing/make_figures.py

Output: images/ch13_*.png at 150 dpi, matching the other decks. The
ISLP-sourced figures (13_5.pdf, 13_6.pdf) are not touched.

Figures ch13_fwer, ch13_thresholds, ch13_bh and ch13_pval_hist are drawn in
the slightly different house style of the original (now lost) draft script:
white background, no grid except on the threshold panel, ink colour #2A2A2A.
Their data is either closed-form (FWER curves, the six worked p-values of
Exercises 13.2/13.3/13.5) or, for the two simulated panels, the exact values
read back off the published figures, so the pictures are unchanged; only a
few annotation anchors were moved off the curves they used to sit on.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
RNG = np.random.default_rng(2024)

# Palette of the four slide panels below (draft-script house style).
GREEN_D = "#2E7D32"
ORANGE_D = "#E08214"
RED_D = "#C62828"
GREY_D = "#999999"
GREY_M = "#808080"   # open "not rejected" markers
INK = "#2A2A2A"

DRAFT_STYLE = {
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 12.5,
    "axes.titlesize": 14.5,
    "axes.labelsize": 13.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
}

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.6,
    }
)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def fig_min_p():
    """What p-hacking harvests: the distribution of the smallest of m = 20
    p-values when every null is true. 20,000 simulated 'studies'."""
    m = 20
    min_p = RNG.uniform(size=(20_000, m)).min(axis=1)
    frac = (min_p <= 0.05).mean()
    theory = 1 - 0.95 ** m

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    bins = np.linspace(0, 0.4, 57)
    ax.hist(min_p[min_p > 0.05], bins=bins, color=ACCENT, alpha=0.75,
            edgecolor="white", linewidth=0.4)
    ax.hist(min_p[min_p <= 0.05], bins=bins, color=ORANGE,
            edgecolor="white", linewidth=0.4)
    ax.axvline(0.05, color=GREY, lw=1.1, ls="--")

    ax.text(0.052, 1550, f"min $p \\leq 0.05$ in {frac:.0%} of studies\n"
            f"(theory: $1-0.95^{{{m}}} = {theory:.3f}$)",
            fontsize=9, color="#8A4513")
    ax.text(0.185, 700, "the smallest of $m=20$\np-values, all nulls true\n"
            "(20,000 simulated studies)", fontsize=8.5, color=ACCENT)

    ax.set_xlabel("smallest p-value in the study")
    ax.set_ylabel("simulated studies")
    ax.set_xlim(0, 0.4)
    save(fig, "ch13_min_p.png")
    print(f"ch13_min_p: simulated {frac:.4f}, theory {theory:.4f}")


def fig_fwer():
    """FWER = 1 - (1 - alpha)^m for three per-test levels. Closed form."""
    m = np.arange(1, 101)
    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7, 4.2))
        for a, colour in [(0.01, GREEN_D), (0.05, ACCENT), (0.10, ORANGE_D)]:
            ax.plot(m, 1 - (1 - a) ** m, color=colour, lw=2.5,
                    label=rf"$\alpha={a:.2f}$")
        ax.axhline(0.5, color=RED_D, ls="--", lw=1.5)
        # Label parked between the curves: at m = 34 the alpha = 0.05 curve is
        # already at 0.82 and the alpha = 0.01 curve still at 0.29.
        ax.text(34, 0.515, "FWER $= 0.5$", color=RED_D, fontsize=12.5,
                va="bottom")
        ax.set_title("Family-wise error rate explodes with $m$")
        ax.set_xlabel("number of tests $m$")
        ax.set_ylabel(r"FWER $= 1-(1-\alpha)^m$")
        ax.legend(loc="lower right", frameon=False)
        save(fig, "ch13_fwer.png")


def fig_thresholds():
    """Bonferroni / Holm / BH thresholds on the six worked p-values."""
    p = np.array([0.001, 0.008, 0.012, 0.030, 0.040, 0.600])
    m, alpha, q = 6, 0.05, 0.05
    i = np.arange(1, m + 1)
    style = dict(DRAFT_STYLE)
    style.update({"axes.spines.top": True, "axes.spines.right": True,
                  "axes.grid": True, "grid.color": "#EEEEEE",
                  "grid.linewidth": 1.0, "grid.alpha": 1.0,
                  "font.size": 12, "axes.titlesize": 14, "axes.labelsize": 13})
    with plt.rc_context(style):
        fig, ax = plt.subplots(figsize=(7.7, 4.3))
        ax.plot(i, np.full(m, alpha / m), "o-", color="#1F77B4", lw=2.0, ms=7,
                label=r"Bonferroni  $\alpha/m$   (2 rejections)")
        ax.plot(i, alpha / (m - i + 1), "s-", color=ORANGE_D, lw=2.0, ms=7,
                label=r"Holm  $\alpha/(m-i+1)$   (3 rejections)")
        ax.plot(i, i * q / m, "^-", color="#2CA02C", lw=2.0, ms=8,
                label=r"BH  $iq/m$   (5 rejections)")
        ax.vlines(i, 0, np.minimum(p, 0.05), color=GREY_D, lw=1.0)
        ax.scatter(i[:-1], p[:-1], s=90, color="black", zorder=5,
                   label=r"sorted $p_{(i)}$")
        # Ranks 2, 3 and 5 are labelled below the dot: above it the Holm and
        # BH curves pass within a label height of the point.
        offsets = [0.0012, -0.0028, -0.0028, 0.0012, -0.0028]
        for k, dy in enumerate(offsets):
            ax.annotate(f"{p[k]:.3f}", (i[k] + 0.06, p[k] + dy), fontsize=11)
        ax.annotate("", xy=(6.25, 0.0525), xytext=(5.75, 0.0495),
                    arrowprops=dict(arrowstyle="->", color=GREY_D, lw=1.5))
        ax.text(4.05, 0.0455, "$p_{(6)}=0.60$\n(off-scale, never rejected)",
                color=GREY_D, fontsize=11)
        ax.set_title("Same six p-values, three multiplicity thresholds",
                     color=ACCENT, fontweight="bold")
        ax.set_xlabel("rank $i$  (sorted p-values)")
        ax.set_ylabel("threshold / p-value")
        ax.set_xlim(0.6, 6.4)
        ax.set_ylim(0, 0.055)
        ax.legend(loc="upper left", fontsize=11)
        save(fig, "ch13_thresholds.png")


# The 30 sorted p-values of the BH staircase panel, recovered from the
# published figure (the draft script that simulated them is lost).
P_BH = np.array([0.0005, 0.0010, 0.0055, 0.0060, 0.0165, 0.0210, 0.0240,
                 0.0810, 0.1150, 0.1610, 0.2150, 0.2240, 0.2550, 0.2780,
                 0.3000, 0.3020, 0.4440, 0.4660, 0.5050, 0.5520, 0.6210,
                 0.6240, 0.7740, 0.7920, 0.7970, 0.8190, 0.8730, 0.8960,
                 0.9870, 0.9910])


def fig_bh():
    """Benjamini-Hochberg step-up rule drawn as a staircase, m = 30, q = 0.10."""
    m, q = len(P_BH), 0.10
    rank = np.arange(1, m + 1)
    line = rank * q / m
    L = int(np.where(P_BH <= line)[0].max() + 1)
    rejected = rank <= L
    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.plot(rank, line, color=RED_D, lw=2.0,
                label=r"BH line $y=(i/m)\,q$, $q=0.10$")
        ax.scatter(rank[~rejected], P_BH[~rejected], s=45, color=GREY_D,
                   label="not rejected")
        ax.scatter(rank[rejected], P_BH[rejected], s=45, color=ACCENT,
                   label="rejected")
        ax.scatter([L], [P_BH[L - 1]], s=260, facecolors="none",
                   edgecolors=RED_D, lw=1.8)
        # Text sits in the empty wedge above the crossing; the sorted p-values
        # only reach y = 0.50 beyond rank 19, well right of the label.
        ax.annotate(rf"largest $i$ below line ($L={L}$)",
                    xy=(L + 0.35, 0.045), xytext=(6.4, 0.50),
                    color=RED_D, fontsize=11.5,
                    arrowprops=dict(arrowstyle="-", color=RED_D, lw=1.2))
        ax.set_title("Benjamini-Hochberg step-up procedure")
        ax.set_xlabel("rank $i$ of sorted $p$-value")
        ax.set_ylabel("$p_{(i)}$")
        ax.legend(loc="upper left", frameon=False, fontsize=11.5)
        save(fig, "ch13_bh.png")


# Bin counts of the p-value histogram panel, recovered from the published
# figure: 20 equal bins on [0, 1], 3000 tests, 2400 of them true nulls.
COUNTS_PVAL = np.array([664, 170, 124, 122, 134, 142, 111, 96, 142, 111,
                        131, 105, 102, 111, 113, 119, 120, 124, 104, 108])


def fig_pval_hist():
    """Histogram of 3000 p-values: uniform bulk plus a spike of true effects."""
    edges = np.linspace(0, 1, len(COUNTS_PVAL) + 1)
    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.bar(edges[:-1], COUNTS_PVAL, width=0.05, align="edge", color=ACCENT,
               alpha=0.85, edgecolor="white", linewidth=1.2)
        ax.axhline(120, color=RED_D, ls="--", lw=2.0)
        ax.annotate("spike near 0:\ntrue effects", xy=(0.045, 655),
                    xytext=(0.36, 600), color=GREEN_D, fontsize=11.5,
                    arrowprops=dict(arrowstyle="->", color=GREEN_D, lw=1.5))
        # Both captions live in the empty band above the bulk (max bar 170,
        # dashed level 120), so neither is crossed by the dashed line.
        ax.text(0.60, 245, r"flat bulk: nulls $\sim U(0,1)$", color=GREY_D,
                fontsize=11.5, ha="center")
        ax.text(0.47, 180, r"uniform null level $m_0$/bins", color=RED_D,
                fontsize=11.5)
        ax.set_title("Distribution of $p$-values across 3000 tests")
        ax.set_xlabel("$p$-value")
        ax.set_ylabel("count")
        save(fig, "ch13_pval_hist.png")


if __name__ == "__main__":
    fig_min_p()
    fig_fwer()
    fig_thresholds()
    fig_bh()
    fig_pval_hist()

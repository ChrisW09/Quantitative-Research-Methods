#!/usr/bin/env python3
"""Figures of the Quantitative Research mock exams (replaces figures.R of the
course "Statistik fuer Oekonomen").

Colours and style follow the make_figures.py scripts of the lecture (colour
palette of common/preamble.tex). Every number drawn is computed here from the
inputs of the specification; verify.py checks the results independently.

    python3 figures.py        # writes Mock_Exam_1/qrm1_*.pdf
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from scipy import stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT1 = os.path.join(os.path.dirname(HERE), "Mock_Exam_1")

BLUE = "#3333B2"        # hsbiblau
BLUE_DARK = "#1C1C6E"   # hsbiblaudunkel
ORANGE = "#E69F00"      # hsbiorange
GRAY = "#9A9A9A"        # hsbigrau
RED = "#C0392B"         # hsbirot
GREEN = "#2E8B57"       # hsbigruen
WBOX = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 12,
    "axes.labelsize": 11, "axes.edgecolor": "#444444", "axes.linewidth": 1.0,
    "axes.grid": True, "grid.color": "#CFCFCF", "grid.linewidth": 0.8,
    "grid.alpha": 0.7, "axes.axisbelow": True, "xtick.color": "#222222",
    "ytick.color": "#222222", "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "legend.framealpha": 0.95, "legend.edgecolor": "#BBBBBB",
    "pdf.fonttype": 42,
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, metadata={"CreationDate": None})
    plt.close(fig)
    print("wrote", path)


# ======================================================================== Mock Exam 1
# Task 1: two-sided z-test, sigma known
MU0, SIGMA, N, XBAR, ALPHA = 80.0, 12.0, 36, 84.30, 0.05
SE = SIGMA / np.sqrt(N)
Z = (XBAR - MU0) / SE
ZC = round(stats.norm.ppf(1 - ALPHA / 2), 2)           # 1.96 (table value)
CI = (XBAR - ZC * SE, XBAR + ZC * SE)


def fig_t1_ztest():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    x = np.linspace(-4, 4, 800)
    y = stats.norm.pdf(x)
    mid = (x >= -ZC) & (x <= ZC)
    ax.fill_between(x[mid], y[mid], color=BLUE, alpha=0.15, lw=0)
    for sel in (x <= -ZC, x >= ZC):
        ax.fill_between(x[sel], y[sel], color=ORANGE, alpha=0.85, lw=0)
    ax.plot(x, y, color=BLUE_DARK, lw=2.2)
    for v in (-ZC, ZC):
        ax.axvline(v, ls="--", color=RED, lw=1.4)
    ax.axvline(Z, color=GREEN, lw=2.4)
    ax.text(-ZC + 0.08, 0.425, "%.2f" % -ZC, color=RED, ha="left", fontsize=10, bbox=WBOX)
    ax.text(ZC - 0.08, 0.425, "%.2f" % ZC, color=RED, ha="right", fontsize=10, bbox=WBOX)
    ax.annotate(r"$Z_n = %.2f$" % Z, xy=(Z, 0.20), xytext=(3.05, 0.27), color=GREEN,
                fontsize=11, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.text(0, 0.16, "keep $H_0$\n(acceptance region)", ha="center", va="center",
            color=BLUE_DARK, fontsize=10)
    ax.text(-3.0, 0.075, r"$\alpha/2 = 0.025$", ha="center", color="#9A6A00", fontsize=10)
    ax.text(3.0, 0.075, r"$\alpha/2 = 0.025$", ha="center", color="#9A6A00", fontsize=10)
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.47)
    ax.set_xlabel(r"$Z_n$ under $H_0$:  $N(0,1)$")
    ax.set_ylabel("Density")
    handles = [Patch(facecolor=ORANGE, alpha=0.85, label="rejection region"),
               Line2D([], [], color=RED, ls="--", lw=1.4, label=r"critical values $\pm z_{0.975}$"),
               Line2D([], [], color=GREEN, lw=2.4, label="test statistic")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3,
              frameon=False, fontsize=9.5)
    style(ax)
    return fig


def fig_t1_ci():
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    lo, hi = CI
    ax.plot([lo, hi], [0, 0], color=BLUE, lw=9, alpha=0.55, solid_capstyle="butt")
    ax.plot([XBAR], [0], "o", color=BLUE_DARK, ms=8, zorder=3)
    ax.text(XBAR, 0.22, r"$\bar x = %.2f$" % XBAR, ha="center", color=BLUE_DARK, fontsize=11)
    for v in (lo, hi):
        ax.text(v, -0.30, "%.2f" % v, ha="center", va="top", color=BLUE, fontsize=11)
    ax.plot([MU0, MU0], [-0.17, 0.17], color=RED, lw=2.6)
    ax.text(MU0, 0.22, r"$\mu_0 = %d$" % MU0, ha="center", color=RED, fontsize=11)
    ax.text((lo + hi) / 2, -0.62, r"95 %% confidence interval  [%.2f ; %.2f]" % (lo, hi),
            ha="center", va="top", color=BLUE, fontsize=10.5)
    ax.set_xlim(77.5, 90.5)
    ax.set_ylim(-0.95, 0.5)
    ax.set_yticks([])
    ax.set_xticks(range(78, 91, 2))
    ax.set_xlabel("mean order value (EUR)")
    ax.grid(False)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    return fig


# Task 2: simple regression, five days
X2 = np.array([20, 22, 24, 26, 28], dtype=float)
Y2 = np.array([46, 54, 62, 70, 68], dtype=float)


def fig_t2_scatter():
    xb, yb = X2.mean(), Y2.mean()
    b1 = np.sum((X2 - xb) * (Y2 - yb)) / np.sum((X2 - xb) ** 2)
    b0 = yb - b1 * xb
    yh = b0 + b1 * X2
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    xs = np.array([19, 29])
    ax.plot(xs, b0 + b1 * xs, color=BLUE, lw=2.2,
            label=r"$\hat y = %g + %g\,x$" % (b0, b1))
    for xi, yi, fi in zip(X2, Y2, yh):
        if yi != fi:
            ax.plot([xi, xi], [yi, fi], ls="--", color=GRAY, lw=1.3)
        u = yi - fi
        # label on the side of the point that faces away from the line
        if u > 0:
            pos, txt = (xi, yi + 2.3), r"$\hat u = +%d$" % u
        elif u < 0:
            pos, txt = (xi, yi - 2.3), r"$\hat u = %d$" % u
        else:
            pos, txt = (xi + 0.9, yi - 2.3), r"$\hat u = 0$"
        ax.text(pos[0], pos[1], txt, fontsize=9.5, color="#555555", ha="center",
                va="center", bbox=WBOX)
    ax.plot(X2, Y2, "o", color=BLUE_DARK, ms=7, zorder=3, label="observed days")
    ax.plot([xb], [yb], "s", color=ORANGE, ms=8, zorder=3,
            label=r"centroid $(\bar x, \bar y) = (%g;\ %g)$" % (xb, yb))
    ax.set_xlim(19, 29.6)
    ax.set_ylim(40, 78)
    ax.set_xticks(range(20, 29, 2))
    ax.set_xlabel(u"Maximum temperature x (°C)")
    ax.set_ylabel("Iced coffees sold y")
    ax.legend(loc="upper left", fontsize=9.5)
    style(ax)
    return fig


# Task 3: logistic regression
B0, B1 = -3.0, 0.5


def phat(x):
    eta = B0 + B1 * np.asarray(x, dtype=float)
    return np.exp(eta) / (1 + np.exp(eta))


def fig_t3_logistic():
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    xs = np.linspace(0, 14, 400)
    ax.plot(xs, phat(xs), color=BLUE_DARK, lw=2.4, label=r"$\hat p(x)$,  $\hat\eta = -3 + 0.5\,x$")
    ax.axhline(0.5, color=RED, ls="--", lw=1.7, label=r"threshold $t = 0.5$  ($x \geq 7$ flagged)")
    ax.axhline(0.3, color=ORANGE, ls="--", lw=1.7, label=r"threshold $t = 0.3$  ($x \geq 5$ flagged)")
    xb5 = -B0 / B1
    xb3 = (np.log(0.3 / 0.7) - B0) / B1
    ax.axvline(xb5, color=RED, ls=":", lw=1.2)
    ax.axvline(xb3, color=ORANGE, ls=":", lw=1.2)
    for xv, col, dx, ha in ((2, GREEN, 0.35, "left"), (7, RED, 0.35, "left")):
        pv = float(phat(xv))
        ax.plot([xv], [pv], "o", color=col, ms=8, zorder=4)
        ax.text(xv + dx, pv - 0.06, r"$x = %d$: $\hat p = %.4f$" % (xv, pv), color=col,
                fontsize=10, ha=ha, va="center", bbox=WBOX)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 1.0)
    ax.set_xticks(range(0, 15, 2))
    ax.set_xlabel("Hotline calls x (last six months)")
    ax.set_ylabel(r"Estimated churn probability $\hat p(x)$")
    ax.legend(loc="upper left", fontsize=9)
    style(ax)
    return fig


def main():
    save(fig_t1_ztest(), OUT1, "qrm1_t1_ztest.pdf")
    save(fig_t1_ci(), OUT1, "qrm1_t1_ci.pdf")
    save(fig_t2_scatter(), OUT1, "qrm1_t2_scatter.pdf")
    save(fig_t3_logistic(), OUT1, "qrm1_t3_logistic.pdf")
    print("All figures written.")


if __name__ == "__main__":
    main()

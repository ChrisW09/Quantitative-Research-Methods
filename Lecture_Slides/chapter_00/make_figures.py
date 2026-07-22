"""Generate the matplotlib figures for the Chapter 0 refresher deck.

All figures are computed from the bundled course datasets (or from clearly
labelled simulations); nothing is sketched by hand. Run from anywhere:

    python Lecture_Slides/chapter_00/make_figures.py

Output: Lecture_Slides/chapter_00/images/ch00_*.png at 150 dpi, matching the
figure size and resolution used by the other decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
RNG = np.random.default_rng(0)

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
    print("wrote", name)


wage = pd.read_csv(DATA / "Wage.csv", index_col=0)
adv = pd.read_csv(DATA / "Advertising.csv", index_col=0)


# 1 -- Centre and spread on a skewed variable ---------------------------------
def fig_center_spread():
    x = wage["wage"].to_numpy()
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(6.8, 4.0), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.hist(x, bins=40, color=ACCENT, alpha=0.75, edgecolor="white", linewidth=0.4)
    ax1.axvline(x.mean(), color=ORANGE, lw=2, label=f"mean = {x.mean():.1f}")
    ax1.axvline(
        np.median(x), color="black", lw=2, ls="--", label=f"median = {np.median(x):.1f}"
    )
    ax1.set_ylabel("frequency")
    ax1.set_title("Wage (n = 3000): a right-skewed distribution")
    ax1.legend(frameon=False)

    ax2.boxplot(
        x,
        vert=False,
        widths=0.5,
        patch_artist=True,
        boxprops={"facecolor": ACCENT, "alpha": 0.35},
        medianprops={"color": "black", "lw": 2},
        flierprops={"marker": "o", "ms": 3, "mfc": "none", "mec": GREY},
    )
    ax2.set_yticks([])
    ax2.set_xlabel("wage (thousands of dollars)")
    ax2.grid(axis="y", visible=False)
    save(fig, "ch00_center_spread.png")


# 2 -- Anatomy of a boxplot ---------------------------------------------------
def fig_boxplot_anatomy():
    x = wage["wage"].to_numpy()
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    iqr = q3 - q1
    lo = x[x >= q1 - 1.5 * iqr].min()
    hi = x[x <= q3 + 1.5 * iqr].max()

    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    ax.boxplot(
        x,
        vert=False,
        widths=0.35,
        patch_artist=True,
        boxprops={"facecolor": ACCENT, "alpha": 0.30},
        medianprops={"color": "black", "lw": 2},
        flierprops={"marker": "o", "ms": 3.5, "mfc": "none", "mec": ORANGE},
    )

    # Labels sit above the box on two staggered rows so nothing collides.
    ann = [
        (lo, f"lower whisker\n$Q_1 - 1.5\\,\\mathrm{{IQR}}$ = {lo:.0f}", 1.42),
        (q1, f"$Q_1$ = {q1:.0f}", 1.24),
        (med, f"median = {med:.0f}", 1.42),
        (q3, f"$Q_3$ = {q3:.0f}", 1.24),
        (hi, f"upper whisker\n$Q_3 + 1.5\\,\\mathrm{{IQR}}$ = {hi:.0f}", 1.42),
    ]
    for xv, label, ytext in ann:
        ax.annotate(
            label,
            xy=(xv, 1.10),
            xytext=(xv, ytext),
            ha="center",
            va="bottom",
            fontsize=8,
            arrowprops={"arrowstyle": "-", "color": GREY, "lw": 0.8},
        )

    ax.annotate(
        "",
        xy=(q1, 0.80),
        xytext=(q3, 0.80),
        arrowprops={"arrowstyle": "<->", "color": ACCENT, "lw": 1.2},
    )
    ax.text(
        (q1 + q3) / 2, 0.72, f"IQR = {iqr:.0f}", ha="center", fontsize=8, color=ACCENT
    )
    ax.annotate(
        "outliers: beyond the whiskers",
        xy=(x.max() * 0.97, 1.0),
        xytext=(x.max() * 0.97, 0.70),
        ha="right",
        fontsize=8,
        color=ORANGE,
        arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 0.8},
    )

    ax.set_ylim(0.60, 1.68)
    ax.set_yticks([])
    ax.set_xlabel("wage (thousands of dollars)")
    ax.set_title("The five-number summary, read off a boxplot")
    ax.grid(axis="y", visible=False)
    save(fig, "ch00_boxplot_anatomy.png")


# 3 -- What the correlation coefficient does and does not capture -------------
def fig_correlation():
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.6))

    panels = [
        (adv["TV"], adv["sales"], "TV budget vs. sales", "TV"),
        (adv["radio"], adv["sales"], "radio budget vs. sales", "radio"),
        (adv["newspaper"], adv["sales"], "newspaper budget vs. sales", "newspaper"),
    ]
    for ax, (xv, yv, title, xlabel) in zip(axes, panels):
        r = np.corrcoef(xv, yv)[0, 1]
        ax.scatter(xv, yv, s=8, color=ACCENT, alpha=0.6, edgecolors="none")
        b, a = np.polyfit(xv, yv, 1)
        xs = np.linspace(xv.min(), xv.max(), 50)
        ax.plot(xs, a + b * xs, color=ORANGE, lw=1.6)
        ax.set_title(f"{title}\n$r = {r:.2f}$", fontsize=9)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("sales" if ax is axes[0] else "")

    # A strong but non-linear relationship that r cannot see.
    xq = RNG.uniform(-3, 3, 200)
    yq = xq**2 + RNG.normal(0, 0.8, 200)
    r = np.corrcoef(xq, yq)[0, 1]
    axes[3].scatter(xq, yq, s=8, color=GREY, alpha=0.7, edgecolors="none")
    axes[3].axhline(yq.mean(), color=ORANGE, lw=1.6)
    axes[3].set_title(f"simulated: $y = x^2 + \\varepsilon$\n$r = {r:.2f}$", fontsize=9)
    axes[3].set_xlabel("x")

    save(fig, "ch00_correlation.png")


# 4 -- The central limit theorem in action ------------------------------------
def fig_clt():
    pop = wage["wage"].to_numpy()
    mu = pop.mean()
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.5), sharey=False)

    axes[0].hist(pop, bins=40, color=GREY, alpha=0.75, edgecolor="white", linewidth=0.3)
    axes[0].axvline(mu, color=ORANGE, lw=1.8)
    axes[0].set_title(f"population\n(Wage, $\\mu$ = {mu:.0f})", fontsize=9)
    axes[0].set_ylabel("frequency")

    for ax, n in zip(axes[1:], (2, 10, 50)):
        means = RNG.choice(pop, size=(4000, n), replace=True).mean(axis=1)
        ax.hist(means, bins=40, color=ACCENT, alpha=0.8, edgecolor="white", linewidth=0.3)
        ax.axvline(mu, color=ORANGE, lw=1.8)
        ax.set_title(
            f"means of samples, $n = {n}$\nSD = {means.std(ddof=1):.1f}", fontsize=9
        )
        ax.set_xlim(20, 220)

    fig.suptitle(
        "Whatever the population looks like, the sample mean becomes normal — and narrower",
        fontsize=9.5,
    )
    save(fig, "ch00_clt.png")


# 5 -- The four reference distributions of this course ------------------------
def fig_reference_dists():
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.6))

    z = np.linspace(-4, 4, 400)
    axes[0].plot(z, stats.norm.pdf(z), color=ACCENT, lw=1.8, label="$N(0,1)$")
    axes[0].plot(z, stats.t.pdf(z, 3), color=ORANGE, lw=1.6, ls="--", label="$t_{3}$")
    axes[0].plot(z, stats.t.pdf(z, 30), color=GREY, lw=1.4, ls=":", label="$t_{30}$")
    axes[0].set_title("normal vs. $t$: heavier tails,\nsmaller df", fontsize=9)
    axes[0].legend(frameon=False, fontsize=8)

    c = np.linspace(0.01, 20, 400)
    for df, ls in ((2, "-"), (5, "--"), (10, ":")):
        axes[1].plot(c, stats.chi2.pdf(c, df), lw=1.6, ls=ls, label=f"$\\chi^2_{{{df}}}$")
    axes[1].set_title("$\\chi^2$: sums of squares\n(variance, LR tests)", fontsize=9)
    axes[1].legend(frameon=False, fontsize=8)

    f = np.linspace(0.01, 5, 400)
    for d1, d2, ls in ((2, 20, "-"), (5, 20, "--"), (10, 20, ":")):
        axes[2].plot(
            f, stats.f.pdf(f, d1, d2), lw=1.6, ls=ls, label=f"$F_{{{d1},{d2}}}$"
        )
    axes[2].set_title("$F$: ratios of variances\n(the $F$-test in Ch. 3)", fontsize=9)
    axes[2].legend(frameon=False, fontsize=8)

    save(fig, "ch00_reference_dists.png")


# 6 -- What "95% confidence" actually means -----------------------------------
def fig_ci_coverage():
    pop = wage["wage"].to_numpy()
    mu = pop.mean()
    n, reps = 40, 25
    # Own seed: this draw happens to miss twice in 25, which is the point of
    # the slide — "95%" is a property of the procedure, not of one interval.
    rng = np.random.default_rng(3)

    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    n_miss = 0
    for i in range(reps):
        s = rng.choice(pop, size=n, replace=True)
        half = stats.t.ppf(0.975, n - 1) * s.std(ddof=1) / np.sqrt(n)
        lo, hi = s.mean() - half, s.mean() + half
        covers = lo <= mu <= hi
        n_miss += not covers
        ax.plot(
            [lo, hi], [i, i], color=ACCENT if covers else ORANGE, lw=1.8, alpha=0.85
        )
        ax.plot(s.mean(), i, "o", ms=3, color=ACCENT if covers else ORANGE)

    ax.axvline(mu, color="black", lw=1.6, ls="--", label=f"true $\\mu$ = {mu:.0f}")
    ax.set_yticks([])
    ax.set_xlabel("wage (thousands of dollars)")
    ax.set_title(
        f"{reps} samples of $n$ = {n}, one 95% CI each — {n_miss} miss $\\mu$",
        fontsize=10,
    )
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="y", visible=False)
    save(fig, "ch00_ci_coverage.png")


# 7 -- Simple linear regression: fit and residuals ----------------------------
def fig_slr():
    x = adv["TV"].to_numpy()
    y = adv["sales"].to_numpy()
    b1, b0 = np.polyfit(x, y, 1)
    fitted = b0 + b1 * x
    resid = y - fitted
    r2 = 1 - (resid**2).sum() / ((y - y.mean()) ** 2).sum()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.2))

    ax1.scatter(x, y, s=10, color=ACCENT, alpha=0.65, edgecolors="none")
    for xi, yi, fi in zip(x[::6], y[::6], fitted[::6]):
        ax1.plot([xi, xi], [yi, fi], color=GREY, lw=0.7, alpha=0.8)
    xs = np.linspace(x.min(), x.max(), 50)
    ax1.plot(xs, b0 + b1 * xs, color=ORANGE, lw=2)
    ax1.set_xlabel("TV budget (thousands of dollars)")
    ax1.set_ylabel("sales (thousands of units)")
    ax1.set_title(
        f"$\\hat y = {b0:.2f} + {b1:.4f}\\,x$   ($R^2 = {r2:.2f}$)", fontsize=9.5
    )

    ax2.scatter(fitted, resid, s=10, color=ACCENT, alpha=0.65, edgecolors="none")
    ax2.axhline(0, color=ORANGE, lw=1.6)
    ax2.set_xlabel("fitted value $\\hat y$")
    ax2.set_ylabel("residual $y - \\hat y$")
    ax2.set_title("residuals vs. fitted: a pattern means trouble", fontsize=9.5)

    save(fig, "ch00_slr.png")


if __name__ == "__main__":
    fig_center_spread()
    fig_boxplot_anatomy()
    fig_correlation()
    fig_clt()
    fig_reference_dists()
    fig_ci_coverage()
    fig_slr()

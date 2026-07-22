"""Generate the matplotlib figures for the Chapter 0b toolkit deck.

Companion to Lecture_Slides/chapter_00/make_figures.py: same conventions
(150 dpi, the deck's colours, everything computed from the bundled course data
or from a clearly labelled construction). Run from anywhere:

    python Lecture_Slides/chapter_00b/make_figures.py
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

ACCENT = "#26468C"
ORANGE = "#C8641E"
GREEN = "#2E7D5B"
GREY = "#7A7A7A"

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


boston = pd.read_csv(DATA / "Boston.csv", index_col=0)
default = pd.read_csv(DATA / "Default.csv")


# 1 -- exp and log, and the property that matters ------------------------------
def fig_exp_log():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.0))

    x = np.linspace(-2, 3, 300)
    ax1.plot(x, np.exp(x), color=ACCENT, lw=1.9, label=r"$e^{x}$")
    ax1.axhline(1, color=GREY, lw=0.8)
    ax1.axvline(0, color=GREY, lw=0.8)
    ax1.plot(0, 1, "o", color=ORANGE, ms=5)
    ax1.annotate(r"$e^{0}=1$", xy=(0, 1), xytext=(-1.8, 8), fontsize=8.5,
                 arrowprops={"arrowstyle": "->", "color": GREY, "lw": 0.8})
    ax1.set_ylim(-1, 20)
    ax1.set_title("$e^{x}$: always positive, and it explodes", fontsize=9.5)
    ax1.legend(frameon=False)

    u = np.linspace(0.05, 20, 300)
    ax2.plot(u, np.log(u), color=ACCENT, lw=1.9, label=r"$\log u$")
    ax2.axhline(0, color=GREY, lw=0.8)
    ax2.plot(1, 0, "o", color=ORANGE, ms=5)
    ax2.annotate(r"$\log 1 = 0$", xy=(1, 0), xytext=(6, -2.2), fontsize=8.5,
                 arrowprops={"arrowstyle": "->", "color": GREY, "lw": 0.8})
    # the multiplication -> addition property, drawn
    for a, b in [(2, 4)]:
        ax2.plot([a, a], [0, np.log(a)], color=ORANGE, ls=":", lw=1.2)
        ax2.plot([b, b], [0, np.log(b)], color=ORANGE, ls=":", lw=1.2)
        ax2.plot([a * b, a * b], [0, np.log(a * b)], color=GREEN, ls=":", lw=1.2)
        ax2.text(a * b + 0.4, np.log(a * b) - 0.1,
                 r"$\log 8 = \log 2 + \log 4$", fontsize=8.5, color=GREEN)
    ax2.set_ylim(-3.2, 3.6)
    ax2.set_title(r"$\log u$: turns $\times$ into $+$", fontsize=9.5)
    ax2.legend(frameon=False, loc="lower right")
    save(fig, "ch00b_exp_log.png")


# 2 -- a log scale straightens a curved relationship ---------------------------
def fig_log_scale():
    x, y = boston["lstat"], boston["medv"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.1))

    for ax, yy, lab in ((ax1, y, "medv"), (ax2, np.log(y), "log(medv)")):
        ax.scatter(x, yy, s=9, color=ACCENT, alpha=0.55, edgecolors="none")
        b1, b0 = np.polyfit(x, yy, 1)
        xs = np.linspace(x.min(), x.max(), 50)
        ax.plot(xs, b0 + b1 * xs, color=ORANGE, lw=1.8)
        r = np.corrcoef(x, yy)[0, 1]
        ax.set_title(f"{lab} vs. lstat   ($r = {r:.2f}$)", fontsize=9.5)
        ax.set_xlabel("lstat (% lower-status population)")
        ax.set_ylabel(lab)
    save(fig, "ch00b_log_scale.png")


# 3 -- probability, odds and log-odds ------------------------------------------
def fig_odds_logit():
    p = np.linspace(0.001, 0.999, 500)
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9))

    axes[0].plot(p, p / (1 - p), color=ACCENT, lw=1.9)
    axes[0].axhline(1, color=GREY, ls=":", lw=1)
    axes[0].axvline(0.5, color=GREY, ls=":", lw=1)
    axes[0].set_ylim(0, 10)
    axes[0].set_xlabel("probability $p$")
    axes[0].set_ylabel("odds $p/(1-p)$")
    axes[0].set_title("odds: $0$ to $\\infty$,\nasymmetric around $p = 0.5$", fontsize=9)

    axes[1].plot(p, np.log(p / (1 - p)), color=ACCENT, lw=1.9)
    axes[1].axhline(0, color=GREY, ls=":", lw=1)
    axes[1].axvline(0.5, color=GREY, ls=":", lw=1)
    axes[1].set_xlabel("probability $p$")
    axes[1].set_ylabel("log-odds (logit)")
    axes[1].set_title("logit: $-\\infty$ to $\\infty$,\nsymmetric around $0$", fontsize=9)

    z = np.linspace(-6, 6, 500)
    axes[2].plot(z, 1 / (1 + np.exp(-z)), color=ORANGE, lw=1.9)
    axes[2].axhline(0.5, color=GREY, ls=":", lw=1)
    axes[2].axvline(0, color=GREY, ls=":", lw=1)
    axes[2].set_xlabel("logit $z$")
    axes[2].set_ylabel("probability")
    axes[2].set_title("the inverse: the logistic\n(sigmoid) curve", fontsize=9)
    save(fig, "ch00b_odds_logit.png")


# 4 -- why a straight line cannot model a probability --------------------------
def fig_sigmoid_fit():
    x = default["balance"].to_numpy()
    y = (default["default"] == "Yes").astype(float).to_numpy()

    # logistic fit by plain gradient ascent on the log-likelihood (no sklearn
    # needed, and it shows the machinery of Chapter 4 in five lines).
    xs_std = (x - x.mean()) / x.std()
    def sigmoid(z):                      # clipped: no overflow warnings
        return 1 / (1 + np.exp(-np.clip(z, -35, 35)))

    b = np.zeros(2)
    X = np.column_stack([np.ones_like(xs_std), xs_std])
    for _ in range(4000):                # gradient ascent on the log-likelihood
        b += 0.001 * X.T @ (y - sigmoid(X @ b))
    grid = np.linspace(x.min(), x.max(), 300)
    gstd = (grid - x.mean()) / x.std()
    fitted = sigmoid(b[0] + b[1] * gstd)
    lin_b1, lin_b0 = np.polyfit(x, y, 1)

    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.scatter(x, y + np.random.default_rng(0).normal(0, 0.012, len(y)),
               s=4, color=GREY, alpha=0.25, edgecolors="none")
    ax.plot(grid, fitted, color=ORANGE, lw=2.2, label="logistic fit")
    ax.plot(grid, lin_b0 + lin_b1 * grid, color=ACCENT, lw=1.6, ls="--",
            label="straight line (OLS)")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.axhline(1, color=GREY, lw=0.8)
    ax.set_ylim(-0.15, 1.15)
    ax.set_xlabel("credit-card balance ($)")
    ax.set_ylabel("P(default)")
    ax.set_title("Default: a probability must stay in $[0,1]$ — a line does not")
    ax.legend(frameon=False, loc="upper left")
    save(fig, "ch00b_sigmoid_fit.png")
    print(f"    (fitted logit: {b[0]:.3f} + {b[1]:.3f} * z(balance)"
          f" -- statsmodels gives the same to 3 dp)")


# 5 -- the likelihood of a coin, and why we take its log -----------------------
def fig_likelihood_coin():
    n, k = 10, 7
    p = np.linspace(0.001, 0.999, 500)
    lik = stats.binom.pmf(k, n, p)
    loglik = np.log(lik)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.0))
    ax1.plot(p, lik, color=ACCENT, lw=1.9)
    ax1.axvline(k / n, color=ORANGE, lw=1.6, ls="--")
    ax1.set_xlabel(r"candidate value of $\pi$")
    ax1.set_ylabel(r"likelihood $L(\pi)$")
    ax1.set_title(f"7 heads in 10 tosses\nmaximised at $\\hat\\pi = {k/n:.1f}$", fontsize=9.5)
    ax1.annotate(r"$\hat\pi$ = 0.7", xy=(0.7, lik.max()), xytext=(0.28, lik.max()*0.95),
                 fontsize=8.5, arrowprops={"arrowstyle": "->", "color": GREY, "lw": 0.8})

    ax2.plot(p, loglik, color=ACCENT, lw=1.9)
    ax2.axvline(k / n, color=ORANGE, lw=1.6, ls="--")
    ax2.set_ylim(-12, 0)
    ax2.set_xlabel(r"candidate value of $\pi$")
    ax2.set_ylabel(r"log-likelihood $\ell(\pi)$")
    ax2.set_title("the log has its maximum in the\nsame place — and adds instead of multiplies",
                  fontsize=9.5)
    save(fig, "ch00b_likelihood_coin.png")


# 6 -- least squares IS maximum likelihood under normal errors -----------------
def fig_likelihood_normal():
    rng = np.random.default_rng(4)
    data = rng.normal(50, 5, 12)
    mus = np.linspace(42, 58, 400)
    loglik = np.array([stats.norm.logpdf(data, m, 5).sum() for m in mus])
    rss = np.array([((data - m) ** 2).sum() for m in mus])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.0))
    ax1.plot(mus, loglik, color=ACCENT, lw=1.9)
    ax1.axvline(data.mean(), color=ORANGE, lw=1.6, ls="--")
    ax1.set_xlabel(r"candidate mean $\mu$")
    ax1.set_ylabel(r"log-likelihood $\ell(\mu)$")
    ax1.set_title(f"maximised at $\\bar x = {data.mean():.2f}$", fontsize=9.5)

    ax2.plot(mus, rss, color=GREEN, lw=1.9)
    ax2.axvline(data.mean(), color=ORANGE, lw=1.6, ls="--")
    ax2.set_xlabel(r"candidate mean $\mu$")
    ax2.set_ylabel(r"residual sum of squares")
    ax2.set_title("minimised in exactly the same place", fontsize=9.5)
    fig.suptitle("With normal errors, maximising the likelihood IS minimising squared error",
                 fontsize=9.5)
    save(fig, "ch00b_likelihood_normal.png")


# 7 -- why exhaustive search dies: 2^p -----------------------------------------
def fig_subset_growth():
    p = np.arange(1, 41)
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.semilogy(p, 2.0**p, color=ACCENT, lw=2, label=r"$2^{p}$ subsets")
    ax.semilogy(p, p * (p + 1) / 2 + 1, color=GREEN, lw=2, ls="--",
                label=r"$\approx p^{2}/2$ models (stepwise)")
    for pp, dx, dy in ((10, 1.5, 0.02), (20, 1.5, 0.02), (40, -12, 0.02)):
        ax.plot(pp, 2.0**pp, "o", color=ORANGE, ms=6)
        ax.annotate(f"$p={pp}$: {2**pp:,} models".replace(",", " "),
                    xy=(pp, 2.0**pp), xytext=(pp + dx, 2.0**pp * dy),
                    fontsize=8.5, color=ORANGE)
    ax.set_ylim(1, 1e14)
    ax.set_xlabel("number of predictors $p$")
    ax.set_ylabel("models to fit (log scale)")
    ax.set_title("Best-subset selection is impossible; stepwise is merely expensive")
    ax.legend(frameon=False, loc="lower right")
    save(fig, "ch00b_subset_growth.png")


# 8 -- the sampling discipline every lab uses ----------------------------------
def fig_split():
    fig, ax = plt.subplots(figsize=(7.6, 2.3))
    ax.axis("off")

    def bar(y, parts, labels, colours, title):
        left = 0.0
        for frac, lab, c in zip(parts, labels, colours):
            ax.add_patch(plt.Rectangle((left, y), frac, 0.42, facecolor=c,
                                       edgecolor="white", lw=1.5))
            ax.text(left + frac / 2, y + 0.21, lab, ha="center", va="center",
                    fontsize=8.5, color="white", weight="bold")
            left += frac
        ax.text(-0.02, y + 0.21, title, ha="right", va="center", fontsize=9)

    bar(0.60, [1.0], ["all $n$ observations"], [GREY], "the data")
    bar(0.05, [0.7, 0.3], ["training set — fit here", "test set — score here"],
        [ACCENT, ORANGE], "split once,\nat random")
    ax.annotate("", xy=(0.5, 0.50), xytext=(0.5, 0.59),
                arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 1.6})
    ax.text(0.52, 0.545, "with a fixed seed, so it is reproducible",
            fontsize=8.5, va="center")
    ax.set_xlim(-0.32, 1.02)
    ax.set_ylim(-0.02, 1.12)
    ax.set_title("Every model in this course is scored on data it has never seen",
                 fontsize=10)
    save(fig, "ch00b_split.png")


if __name__ == "__main__":
    fig_exp_log()
    fig_log_scale()
    fig_odds_logit()
    fig_sigmoid_fit()
    fig_likelihood_coin()
    fig_likelihood_normal()
    fig_subset_growth()
    fig_split()

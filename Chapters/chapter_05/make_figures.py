"""Generate the computed matplotlib figures for the Chapter 5 deck (Resampling).

Every figure is either computed exactly or drawn from a clearly labelled,
seeded simulation --- nothing is sketched by hand, and every number quoted on
the slide comes out of this file. Run from anywhere:

    python Chapters/chapter_05/make_figures.py

Output: Chapters/chapter_05/images/ch05_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The ISLP-sourced figures
(``5_2.pdf`` etc.) are not touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"

# The three cross-validation / bootstrap figures share their own accents:
# CVTEST is the second series (10-fold CV, variance), RED marks a minimum and
# GREEN marks the point estimate / sweet spot.
CVTEST = "#E08214"
RED = "#C62828"
GREEN = "#2E7D32"

# Those three figures are set one notch larger than the deck default so the
# tick labels stay readable inside their (rather small) LaTeX boxes.
BIG_RC = {"font.size": 13, "axes.titlesize": 14}

RNG = np.random.default_rng(2024)

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


def fig_inclusion_probability():
    """The Exercise 5.5 result drawn: P(row included in a bootstrap resample).

    Theory is exact, 1 - (1 - 1/n)^n; the dots check it by simulation
    (20,000 resamples per n, seeded), the same experiment the chapter 5 lab
    runs in its 'What is actually in a bootstrap sample?' section.
    """
    n_grid = np.unique(np.round(np.logspace(np.log10(2), 3, 60)).astype(int))
    theory = 1 - (1 - 1 / n_grid) ** n_grid

    n_sim = np.array([2, 3, 5, 10, 20, 50, 100, 300, 1000])
    simulated = []
    for n in n_sim:
        draws = RNG.integers(0, n, size=(20_000, n))
        simulated.append((draws == 0).any(axis=1).mean())

    limit = 1 - np.exp(-1)

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.axhline(limit, color=GREY, lw=1.2, ls="--", zorder=1)
    ax.plot(n_grid, theory, color=ACCENT, lw=2, zorder=3)
    ax.plot(n_sim, simulated, "o", color=ORANGE, ms=5,
            mec="white", mew=0.8, zorder=4)

    # direct labels instead of a legend box
    ax.text(3.2, 0.715, r"theory: $1-(1-1/n)^n$", color=ACCENT, fontsize=9)
    ax.text(120, 0.658, "simulation\n(20{,}000 resamples per $n$)".replace("{,}", ","),
            color=ORANGE, fontsize=8.5, ha="left")
    ax.text(950, limit + 0.0025, r"$1-1/e \approx 0.632$", color=GREY,
            fontsize=9, ha="right", va="bottom")

    ax.set_xscale("log")
    ax.set_xlabel(r"sample size $n$")
    ax.set_ylabel("P(a given row is in the resample)")
    ax.set_ylim(0.615, 0.775)
    ax.set_xlim(1.8, 1100)
    ax.set_xticks([2, 5, 10, 50, 100, 1000])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    save(fig, "ch05_inclusion_probability.png")
    print("ch05_inclusion_probability.png:",
          f"n=5 -> {1 - (1 - 1/5)**5:.4f}, n=1000 -> {1 - (1 - 1/1000)**1000:.4f},",
          f"limit {limit:.4f}")


def _auto():
    """Auto.csv with the five ``?`` horsepower rows dropped --- n = 392."""
    auto = pd.read_csv(DATA / "Auto.csv", na_values="?").dropna()
    return auto["horsepower"].to_numpy(float), auto["mpg"].to_numpy(float)


def _poly_test_mse(x_tr, y_tr, x_te, y_te, degree):
    """Fit an OLS polynomial of ``degree`` on the training fold, score the rest.

    ``horsepower`` runs to 230, so a raw Vandermonde matrix of degree 10 is
    hopelessly ill-conditioned; standardising with the *training* mean/sd
    (the design span is unchanged, only the conditioning) keeps the least
    squares solve honest at every degree.
    """
    mu, sd = x_tr.mean(), x_tr.std()
    design = np.vander((x_tr - mu) / sd, degree + 1)
    beta = np.linalg.lstsq(design, y_tr, rcond=None)[0]
    pred = np.vander((x_te - mu) / sd, degree + 1) @ beta
    return float(np.mean((y_te - pred) ** 2))


def fig_cv_degree():
    """LOOCV and 10-fold CV test MSE against polynomial degree on Auto.

    Both curves are computed from ``Auto.csv`` (n = 392, mpg ~ poly(horsepower, d)).
    LOOCV uses the exact hat-matrix shortcut, so it is deterministic; the
    10-fold curve uses ``KFold(10, shuffle=True, random_state=0)``.
    """
    from sklearn.model_selection import KFold

    x, y = _auto()
    degrees = np.arange(1, 11)

    loocv = []
    # errstate only silences spurious FP flags raised by the platform BLAS on
    # these matmuls; the values below are exact (checked against the lab).
    with np.errstate(all="ignore"):
        for d in degrees:
            design = np.vander((x - x.mean()) / x.std(), d + 1)
            q, r = np.linalg.qr(design)
            resid = y - design @ np.linalg.solve(r, q.T @ y)
            leverage = (q ** 2).sum(axis=1)
            loocv.append(np.mean((resid / (1 - leverage)) ** 2))
    loocv = np.array(loocv)

    folds = KFold(n_splits=10, shuffle=True, random_state=0)
    kfold = np.array([
        np.mean([_poly_test_mse(x[tr], y[tr], x[te], y[te], d)
                 for tr, te in folds.split(x)])
        for d in degrees
    ])

    best = int(degrees[np.argmin(loocv)])

    with plt.rc_context(BIG_RC):
        fig, ax = plt.subplots(figsize=(7.00, 4.20))
        ax.grid(False)
        ax.plot(degrees, loocv, "-o", color=ACCENT, lw=2.5, ms=6, label="LOOCV")
        ax.plot(degrees, kfold, "-s", color=CVTEST, lw=2.5, ms=6, label="10-fold CV")
        ax.plot([best], [loocv.min()], "o", mfc="none", mec=RED, ms=14, mew=2,
                zorder=5)
        ax.annotate("min", xy=(best, loocv.min()), xytext=(6, 5),
                    textcoords="offset points", color=RED, ha="left", va="bottom")
        ax.set_xticks(degrees)
        ax.set_xlabel("Polynomial degree of horsepower")
        ax.set_ylabel("Estimated test MSE")
        ax.set_title("Cross-validated test MSE vs polynomial degree (Auto)")
        ax.legend(frameon=False, loc="upper right")
        save(fig, "ch05_cv_degree.png")

    print("ch05_cv_degree.png:",
          f"LOOCV d=1 {loocv[0]:.2f} -> d=2 {loocv[1]:.2f},",
          f"10-fold d=1 {kfold[0]:.2f} -> d=2 {kfold[1]:.2f},",
          f"LOOCV min at degree {best} ({loocv.min():.2f}),",
          f"10-fold min at degree {int(degrees[np.argmin(kfold)])} ({kfold.min():.2f})")


def fig_cv_bias_variance():
    """Schematic: why the mean-squared error of the CV estimate bottoms out at k ~ 5-10.

    There is no data set behind this one --- it is the textbook argument drawn
    to scale. The two components are written down explicitly:
    bias^2 = 0.9 / (k - 1) (more folds -> larger training sets -> less bias)
    and variance = 0.086 + 0.00167 (k - 2)^2 (more folds -> training sets that
    overlap more -> more correlated errors). The total is their sum, and the
    marked sweet spot is simply its minimum over the plotted grid.
    """
    k = np.linspace(2, 20, 361)
    bias2 = 0.9 / (k - 1)
    variance = 0.086 + 0.00167 * (k - 2) ** 2
    total = bias2 + variance
    k_star = float(k[np.argmin(total)])
    total_star = float(total.min())

    with plt.rc_context({**BIG_RC, "grid.alpha": 0.15}):
        fig, ax = plt.subplots(figsize=(8.19, 4.18))
        ax.axvline(k_star, color=GREEN, lw=1.8, ls="--", zorder=1)
        ax.plot(k, bias2, color=ACCENT, lw=2.4,
                label=r"Bias$^2$  (shrinks as $k\uparrow$)")
        ax.plot(k, variance, color=CVTEST, lw=2.4,
                label=r"Variance  (grows as $k\uparrow$)")
        ax.plot(k, total, color=RED, lw=3.2, label="Total error of the estimate")
        ax.plot([k_star], [total_star], "o", color=GREEN, ms=9, zorder=5)

        ax.text(2.15, 0.965, "validation set\n$(k = 2)$", color=ACCENT,
                ha="left", va="top")
        ax.text(16.7, 0.955, "LOOCV\n$(k = n)$", color=CVTEST,
                ha="left", va="top")
        ax.annotate("sweet spot\n$k \\approx 5$–$10$",
                    xy=(k_star, total_star), xytext=(9.6, 0.665),
                    color=GREEN, ha="left", va="top",
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6))

        ax.set_xlim(2, 20.8)
        ax.set_ylim(0, 1.08)
        ax.set_xticks([2, 5, 10, 15, 20])
        ax.set_xlabel("Number of folds $k$")
        ax.set_ylabel("Error of the test-error estimate")
        ax.set_title("Cross-validation bias–variance trade-off in $k$")
        ax.legend(frameon=False, loc="upper center")
        save(fig, "ch05_cv_bias_variance.png")

    print("ch05_cv_bias_variance.png:",
          f"total error minimised at k = {k_star:.2f} (value {total_star:.3f});",
          f"k=2 {total[0]:.3f}, k=20 {total[-1]:.3f}")


def fig_x_bootstrap_alpha_hist():
    """The Portfolio bootstrap: B = 1000 resampled values of alpha-hat.

    Straight out of ``Portfolio.csv`` (n = 100) with the ISLP estimator
    alpha = (var Y - cov XY) / (var X + var Y - 2 cov XY). Rows are resampled
    as *pairs* via one shared index vector, seeded with ``default_rng(0)``.
    """

    def alpha_hat(x, y):
        cov = np.cov(x, y)
        return (cov[1, 1] - cov[0, 1]) / (cov[0, 0] + cov[1, 1] - 2 * cov[0, 1])

    port = pd.read_csv(DATA / "Portfolio.csv")
    x, y = port["X"].to_numpy(), port["Y"].to_numpy()
    n, B = len(x), 1000

    point = alpha_hat(x, y)
    rng = np.random.default_rng(0)
    boot = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)          # whole rows, one shared index vector
        boot[b] = alpha_hat(x[idx], y[idx])
    se = boot.std(ddof=1)

    with plt.rc_context({**BIG_RC, "axes.titlesize": 13}):
        fig, ax = plt.subplots(figsize=(7.20, 4.00))
        ax.grid(False)
        ax.hist(boot, bins=32, color=ACCENT, alpha=0.8,
                edgecolor="white", linewidth=0.8)
        ax.axvline(point, color=GREEN, lw=2,
                   label=rf"$\hat\alpha = {point:.3f}$")
        for edge in (point - se, point + se):
            ax.axvline(edge, color=CVTEST, lw=2, ls="--",
                       label=rf"$\hat\alpha \pm 1$ SE  (SE $= {se:.3f}$)"
                       if edge < point else None)
        ax.set_ylim(bottom=0)
        ax.set_xlabel(r"$\hat\alpha^*$ from bootstrap resample")
        ax.set_ylabel("Count")
        ax.set_title(rf"$B = {B}$ bootstrap resamples of Portfolio ($n = {n}$)")
        ax.legend(frameon=False, loc="upper right")
        save(fig, "ch05_x_bootstrap_alpha_hist.png")

    lo, hi = np.quantile(boot, [0.025, 0.975])
    print("ch05_x_bootstrap_alpha_hist.png:",
          f"alpha-hat {point:.4f}, bootstrap SE {se:.4f},",
          f"95% percentile interval [{lo:.3f}, {hi:.3f}],",
          f"+-2 SE [{point - 2 * se:.2f}, {point + 2 * se:.2f}]")


if __name__ == "__main__":
    fig_inclusion_probability()
    fig_cv_degree()
    fig_cv_bias_variance()
    fig_x_bootstrap_alpha_hist()

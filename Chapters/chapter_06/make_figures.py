"""Generate the computed matplotlib figures for the Chapter 6 deck (Selection).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_06/make_figures.py

Output: Chapters/chapter_06/images/ch06_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The textbook scans (images/6_*.pdf)
are not touched.
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

# the palette the coefficient-path and criterion figures are drawn in
PATH_BLUE = "#26468c"
PATH_ORANGE = "#e08214"
PATH_GREEN = "#2e7d32"
PATH_RED = "#c62828"
PATH_PURPLE = "#6a1b9a"
PATH_GREY = "#cccccc"

DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition" / "Hitters.csv"

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


def hitters():
    """Hitters with the salary rows dropped, factors dummy-coded --- n=263, p=19."""
    import pandas as pd

    df = pd.read_csv(DATA).dropna(subset=["Salary"])
    X = pd.get_dummies(df.drop(columns=["Salary"]), drop_first=True).astype(float)
    return X, df["Salary"].to_numpy()


def fig_search_space():
    """Models fitted by best subset (2^p) vs forward stepwise (1 + p(p+1)/2)."""
    p = np.arange(1, 41)
    best = 2.0 ** p
    fwd = 1 + p * (p + 1) / 2

    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot(p, best, color=ACCENT, lw=2, zorder=3)
    ax.plot(p, fwd, color=ORANGE, lw=2, zorder=3)

    # the two worked cases: the deck's p = 10 and the Hitters p = 19
    for pp, note_xy in [(10, (10.6, 2.2e2)), (19, (19.6, 2.0e4))]:
        ax.plot([pp, pp], [1 + pp * (pp + 1) / 2, 2.0 ** pp],
                color=GREY, lw=0.9, ls=":", zorder=2)
        ax.plot(pp, 2.0 ** pp, "o", color=ACCENT, ms=5, mec="white", mew=0.8, zorder=4)
        ax.plot(pp, 1 + pp * (pp + 1) / 2, "o", color=ORANGE, ms=5, mec="white", mew=0.8, zorder=4)
    ax.annotate("$p=10$: $1{,}024$ vs $56$", xy=(10, 2**10), xytext=(4.3, 6e4),
                fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate("Hitters, $p=19$:\n$524{,}288$ vs $191$", xy=(19, 2**19), xytext=(13.5, 4e7),
                fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.text(26.5, 1.2e9, "best subset: $2^p$", color=ACCENT, fontsize=9.5,
            ha="right")
    ax.text(33, 18, r"forward stepwise: $1+\frac{p(p+1)}{2}$", color=ORANGE,
            fontsize=9.5, ha="center")

    ax.set_yscale("log")
    ax.set_xlabel("number of candidate predictors $p$")
    ax.set_ylabel("models that must be fitted")
    ax.set_xlim(1, 40)
    ax.set_ylim(1, 1e13)

    save(fig, "ch06_search_space.png")
    print("ch06_search_space.png:",
          f"p=10: {2**10:,} vs {1 + 10*11//2} | p=19: {2**19:,} vs {1 + 19*20//2} |",
          f"p=40: {2**40:,.0f} vs {1 + 40*41//2}")


def fig_selection_criteria():
    """C_p, BIC and adjusted R^2 along the forward-stepwise path on Hitters."""
    import statsmodels.api as sm

    X, y = hitters()
    n, p = len(y), X.shape[1]
    Xv = X.to_numpy()
    s2 = sm.OLS(y, sm.add_constant(Xv)).fit().ssr / (n - p - 1)

    chosen, rss, rest = [], [], list(range(p))
    for _ in range(p):
        best = min(
            (sm.OLS(y, sm.add_constant(Xv[:, chosen + [j]])).fit().ssr, j) for j in rest
        )
        rss.append(best[0])
        chosen.append(best[1])
        rest.remove(best[1])

    rss = np.array(rss)
    d = np.arange(1, p + 1)
    tss = ((y - y.mean()) ** 2).sum()
    cp = (rss + 2 * d * s2) / n
    bic = (rss + np.log(n) * d * s2) / n
    adj = 1 - (rss / (n - d - 1)) / (tss / (n - 1))

    with plt.rc_context({"font.size": 10.5, "axes.titlesize": 12, "axes.grid": False}):
        fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.5))
        panels = [
            (cp, PATH_BLUE, r"$C_p$", "min"),
            (bic, PATH_ORANGE, "BIC", "min"),
            (adj, PATH_GREEN, r"Adjusted $R^2$", "max"),
        ]
        for ax, (v, colour, title, kind) in zip(axes, panels):
            ax.plot(d, v, "o-", color=colour, ms=4, lw=1.4)
            i = v.argmin() if kind == "min" else v.argmax()
            ax.plot(d[i], v[i], "o", mfc="none", mec=PATH_RED, ms=11, mew=1.6)
            # label the winner clear of the curve and of the panel title: the
            # adjusted-R^2 peak sits at the top of its panel, so its label goes below
            offset = (0, 12) if kind == "min" else (0, -14)
            ax.annotate(
                str(d[i]), xy=(d[i], v[i]), xytext=offset, textcoords="offset points",
                color=PATH_RED, fontsize=9.5, ha="center", va="center",
            )
            ax.set_title(title)
            ax.set_xlabel("Number of predictors")
        axes[0].set_ylabel("Criterion value")
        fig.suptitle("Forward-stepwise selection criteria (Hitters)", fontsize=12)
        save(fig, "ch06_selection_criteria.png")

    print("ch06_selection_criteria.png:",
          f"Cp picks d={d[cp.argmin()]} | BIC picks d={d[bic.argmin()]} |",
          f"adj R^2 picks d={d[adj.argmax()]}")


def fig_ridge_path():
    """Ridge coefficient paths on standardised Hitters, five largest highlighted."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler

    X, y = hitters()
    Xs = StandardScaler().fit_transform(X)
    alphas = np.logspace(-1, 5.5, 120)
    coefs = np.array(
        [Ridge(alpha=a, solver="cholesky").fit(Xs, y).coef_ for a in alphas]
    )
    top = np.argsort(-np.abs(coefs[0]))[:5]

    with plt.rc_context({"font.size": 11, "axes.titlesize": 12, "axes.grid": False}):
        fig, ax = plt.subplots(figsize=(6.9, 4.1))
        for j in range(coefs.shape[1]):
            if j not in top:
                ax.plot(np.log10(alphas), coefs[:, j], color=PATH_GREY, lw=0.9, zorder=1)
        colours = [PATH_BLUE, PATH_ORANGE, PATH_GREEN, PATH_RED, PATH_PURPLE]
        for colour, j in zip(colours, top):
            ax.plot(np.log10(alphas), coefs[:, j], color=colour, lw=2, zorder=3,
                    label=X.columns[j])
        ax.set_title("Ridge coefficient paths (Hitters)")
        ax.set_xlabel(r"$\log_{10}(\alpha)$")
        ax.set_ylabel("Standardized coefficient")
        # upper right is the one corner every path has left empty
        ax.legend(fontsize=9, frameon=False, loc="upper right")
        save(fig, "ch06_ridge_path.png")

    print("ch06_ridge_path.png:", ", ".join(X.columns[j] for j in top))


def fig_ridge_cv():
    """10-fold CV curve for ridge on standardised Hitters, with the dip marked.

    The slide quotes lambda* ~ 1.6 and CV MSE ~ 114,000. Note this is a
    *10-fold* CV curve over a log grid; the companion notebook's LOO search
    over its own grid lands on alpha ~ 2.8 instead. Both are correct for the
    procedure they run --- the divergence is deliberate, so the fold split
    here is pinned (KFold(10, shuffle=True, random_state=1)) and must not be
    changed without re-checking the number on the slide.
    """
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X, y = hitters()
    alphas = np.logspace(-2, 5, 141)
    cv = KFold(n_splits=10, shuffle=True, random_state=1)
    # The scaler goes *inside* the pipeline so it is re-fitted on each training
    # fold. Scaling X once up front lets every validation fold contribute its
    # mean and standard deviation to the transform -- the exact leak this
    # chapter's own CV-pitfalls slide warns about. (It moves the curve by well
    # under the precision the slide quotes, so the numbers are unchanged.)
    mse = np.array([
        -cross_val_score(
            make_pipeline(StandardScaler(), Ridge(alpha=a, solver="cholesky")),
            X, y, cv=cv, scoring="neg_mean_squared_error",
        ).mean()
        for a in alphas
    ])
    i = mse.argmin()

    with plt.rc_context({"font.size": 13, "axes.titlesize": 13, "axes.grid": False}):
        fig, ax = plt.subplots(figsize=(7.0, 4.0))
        ax.axvline(np.log10(alphas[i]), color=PATH_ORANGE, ls="--", lw=1.8, zorder=2)
        ax.plot(np.log10(alphas), mse / 1e3, color=PATH_BLUE, lw=2.4, zorder=3)
        ax.plot(np.log10(alphas[i]), mse[i] / 1e3, "o", color=PATH_ORANGE, ms=9,
                zorder=4)
        # the flat left arm of the curve leaves this pocket empty, so the label
        # sits clear of the dashed line, the curve and the axis labels
        ax.text(
            0.762, 127.2,
            f"$\\lambda^{{*}} \\approx {alphas[i]:.1f}$\n"
            f"CV MSE $\\approx {mse[i] / 1e3:.0f}$k",
            fontsize=12, color="#333333", ha="left", va="center",
        )
        ax.set_title(r"Ridge on Hitters: cross-validation picks $\lambda$")
        ax.set_xlabel(r"$\log_{10}(\lambda)$")
        ax.set_ylabel(r"10-fold CV MSE ($\times 10^{3}$)")
        save(fig, "ch06_x_ridge_cv.png")

    print("ch06_x_ridge_cv.png:",
          f"lambda* = {alphas[i]:.3f} (log10 = {np.log10(alphas[i]):.2f}),",
          f"CV MSE = {mse[i]:,.0f}")


def fig_lasso_path():
    """Lasso coefficient paths on standardised Hitters, five largest highlighted.

    Companion to fig_ridge_path: same data, same standardisation, same
    'highlight the five largest coefficients at the weakest penalty' rule, so
    the two slides can be read side by side. The grid stops at the smallest
    alpha that zeroes everything, max_j |x_j'(y - ybar)| / n.
    """
    from sklearn.linear_model import Lasso
    from sklearn.preprocessing import StandardScaler

    X, y = hitters()
    Xs = StandardScaler().fit_transform(X)
    alphas = np.logspace(-0.6, 2.4, 120)
    # the coordinate-descent default tol=1e-4 stops short here and leaves the
    # weakest-penalty end visibly off; tighten it so the path is the converged one
    coefs = np.array(
        [Lasso(alpha=a, max_iter=200000, tol=1e-7).fit(Xs, y).coef_ for a in alphas]
    )
    top = np.argsort(-np.abs(coefs[0]))[:5]

    with plt.rc_context({"font.size": 13, "axes.titlesize": 14, "axes.grid": False}):
        fig, ax = plt.subplots(figsize=(7.0, 4.2))
        # the zero line is the point of the figure here: paths land on it
        ax.axhline(0, color="black", lw=0.8, zorder=2)
        for j in range(coefs.shape[1]):
            if j not in top:
                ax.plot(np.log10(alphas), coefs[:, j], color=PATH_GREY, lw=0.9, zorder=1)
        colours = [PATH_BLUE, PATH_ORANGE, PATH_GREEN, PATH_RED, PATH_PURPLE]
        for colour, j in zip(colours, top):
            ax.plot(np.log10(alphas), coefs[:, j], color=colour, lw=2, zorder=3,
                    label=X.columns[j])
        ax.set_title("Lasso coefficient paths (Hitters)")
        ax.set_xlabel(r"$\log_{10}(\alpha)$")
        ax.set_ylabel("Standardized coefficient")
        # upper right is the one corner every path has left empty
        ax.legend(fontsize=10, frameon=False, loc="upper right")
        save(fig, "ch06_lasso_path.png")

    nz = (coefs != 0).sum(axis=1)
    print("ch06_lasso_path.png:", ", ".join(X.columns[j] for j in top),
          f"| nonzero coefficients: {nz[0]} at alpha={alphas[0]:.2f}",
          f"-> {nz[-1]} at alpha={alphas[-1]:.0f}")


def fig_ridge_bias_variance():
    """Schematic: variance falls and squared bias rises as the penalty grows."""
    x = np.linspace(-2, 4, 600)
    variance = 2.8 / (1 + np.exp(2.1 * (x - 0.9)))
    bias2 = 3.4 / (1 + np.exp(-2.3 * (x - 1.6)))
    sigma2 = 1.0
    mse = variance + bias2 + sigma2
    i = mse.argmin()

    with plt.rc_context({"font.size": 11, "axes.titlesize": 12, "axes.grid": True,
                         "grid.color": "#f3f3f3", "grid.alpha": 1.0,
                         "grid.linewidth": 1.0}):
        fig, ax = plt.subplots(figsize=(8.0, 3.9))
        ax.axhline(sigma2, color="#666666", ls=":", lw=2.0, zorder=1)
        ax.text(3.95, sigma2 + 0.12, r"irreducible error $\sigma^2$",
                color="#666666", fontsize=10, ha="right")
        ax.axvline(x[i], color=PATH_GREEN, ls="--", lw=1.8, zorder=2)
        ax.plot(x, variance, color=PATH_ORANGE, lw=2.4, label="Variance", zorder=3)
        ax.plot(x, bias2, color=PATH_BLUE, lw=2.4, label=r"Bias$^2$", zorder=3)
        ax.plot(x, mse, color=PATH_RED, lw=2.8, zorder=4,
                label=r"Test MSE (= Bias$^2$+Var+$\sigma^2$)")
        ax.plot(x[i], mse[i], "o", color=PATH_GREEN, ms=9, zorder=5)
        ax.annotate("best $\\lambda$\n(min test MSE)", xy=(x[i], mse[i]),
                    xytext=(1.72, 4.35), color=PATH_GREEN, fontsize=11, ha="left",
                    arrowprops=dict(arrowstyle="->", color=PATH_GREEN, lw=1.4))
        # the OLS marker sits below the variance plateau, not across it
        ax.text(-1.93, 2.42, "OLS\n$(\\lambda=0)$", color=PATH_RED, fontsize=10,
                ha="left", va="top")
        ax.set_ylim(0, 7.2)
        ax.set_yticks(range(8))
        ax.set_xlabel(r"$\log_{10}\lambda$  (penalty strength $\rightarrow$)")
        ax.set_ylabel("Error")
        ax.set_title(r"Ridge: bias, variance and test error vs $\lambda$")
        ax.legend(loc="upper left", frameon=False, fontsize=11)
        save(fig, "ch06_ridge_bias_variance.png")

    print("ch06_ridge_bias_variance.png:",
          f"test MSE bottoms at log10 lambda = {x[i]:.2f}, MSE = {mse[i]:.2f}")


if __name__ == "__main__":
    fig_search_space()
    fig_selection_criteria()
    fig_ridge_path()
    fig_ridge_cv()
    fig_lasso_path()
    fig_ridge_bias_variance()

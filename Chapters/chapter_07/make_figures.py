"""Generate the computed matplotlib figures for the Chapter 7 (Beyond Linearity) deck.

Everything is computed exactly or from a seeded simulation --- nothing is
sketched by hand. Run from anywhere:

    python Chapters/chapter_07/make_figures.py

Output: Chapters/chapter_07/images/ch07_*.png at 150 dpi, matching the other decks. Existing figures are not
touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

HERE = Path(__file__).parent
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)
DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition" / "Wage.csv"

# Some BLAS builds raise divide/overflow/invalid flags on ordinary dense
# matmuls whose operands and results are entirely finite. Left alone they print
# a dozen RuntimeWarnings per rebuild that mean nothing; the one computation
# where a real NaN would matter (the smoother matrix) asserts finiteness itself.
np.seterr(all="ignore")

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D32"
RED = "#C62828"

# The three Wage figures below all use the age quartiles the lab cuts on.
KNOTS = [33.75, 42.0, 51.0]


def wage():
    """The Wage data, straight from the bundled CSV — no ISLP dependency."""
    return pd.read_csv(DATA)


def natural_basis(x, knots):
    """Natural cubic spline basis (ESL 5.2.1): K knots give K columns.

    Columns are 1, x, then N_{k+2} = d_k - d_{K-1}, which forces the fit to be
    linear beyond the boundary knots — that is the whole point of the natural
    spline, and why its edges behave where the raw cubic's do not.
    """
    x = np.asarray(x, float)
    xi = np.asarray(knots, float)
    K = len(xi)

    def d(k):
        num = np.clip(x - xi[k], 0, None) ** 3 - np.clip(x - xi[-1], 0, None) ** 3
        return num / (xi[-1] - xi[k])

    cols = [np.ones_like(x), x] + [d(k) - d(K - 2) for k in range(K - 2)]
    return np.column_stack(cols)

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


def fig_spline_basis():
    """The truncated-power basis of a cubic spline with three knots.

    Exercise 7.3's counting argument drawn: the four global polynomial terms
    plus one local truncated cubic per knot = K + 4 = 7 basis functions,
    knots at the age quartiles the lab uses (33.8, 42, 51).
    """
    knots = [33.75, 42.0, 51.0]           # Wage age quartiles, as in the lab
    x = np.linspace(18, 80, 400)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))

    ax = axes[0]
    xs = (x - 18) / 62                     # scale to [0,1] so the powers fit one panel
    labelled = [(np.ones_like(xs), "$1$", 40, 1.03), (xs, "$x$", 48, 0.52),
                (xs**2, "$x^2$", 60, 0.40), (xs**3, "$x^3$", 71, 0.56)]
    for term, lab, lx, ly in labelled:
        ax.plot(x, term, color=GREY, lw=1.4, alpha=0.85)
        ax.text(lx, ly, lab, color=GREY, fontsize=9.5)
    ax.set_title("four global polynomial terms", fontsize=9, color=GREY)
    ax.set_xlabel("age"); ax.set_xlim(18, 82); ax.set_ylim(-0.05, 1.12)
    ax.set_yticks([0, 0.5, 1])

    ax = axes[1]
    for k, xi in enumerate(knots):
        b = (np.clip(x - xi, 0, None) / (80 - xi)) ** 3   # each reaches 1 at age 80
        ax.plot(x, b, color=ACCENT, lw=1.8)
        ax.axvline(xi, color=ORANGE, lw=0.9, ls=":")
        ax.annotate(rf"$\xi_{k+1}$", (xi, 1.03), color=ORANGE,
                    fontsize=9.5, ha="center")
    clear = dict(facecolor="white", edgecolor="none", pad=1.5)   # keep labels off the curves/knot lines
    ax.text(56, 0.52, r"$(x-\xi_k)_+^3$", color=ACCENT, fontsize=10, bbox=clear)
    ax.text(20, 0.86, "zero left of its knot ---\neach term acts locally", color="#333333",
            fontsize=8, bbox=clear)
    ax.set_title("one truncated cubic per knot", fontsize=9, color=ACCENT)
    ax.set_xlabel("age"); ax.set_xlim(18, 82); ax.set_ylim(-0.05, 1.12)
    ax.set_yticks([0, 0.5, 1])

    save(fig, "ch07_spline_basis.png")
    print("ch07_spline_basis.png: 4 +", len(knots), "= 7 basis functions (K+4 with K=3)")


def fig_wage_fits():
    """Four ways to bend a line, fitted to the same Wage/age scatter.

    The point of the slide is the *edges*: the degree-4 polynomial turns down,
    the step function is blocky, the cubic spline drops off past the last knot,
    and only the natural spline stays calm where the data runs out.
    """
    df = wage()
    age, y = df["age"].to_numpy(float), df["wage"].to_numpy(float)
    grid = np.linspace(age.min(), age.max(), 400)

    fig, axes = plt.subplots(2, 2, figsize=(9.6, 6.2))
    fig.suptitle("Wage vs. Age: four ways to model curvature", fontsize=12)

    def panel(ax, title, colour):
        ax.scatter(age, y, s=6, color="#444444", alpha=0.16, edgecolors="none")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Age"); ax.set_ylabel("Wage")
        ax.grid(False)
        return ax

    # 1 -- degree-4 polynomial: one global formula, so the tails are driven by
    # the bulk of the data in the middle.
    ax = panel(axes[0, 0], "Degree-4 polynomial", ACCENT)
    ax.plot(grid, np.polyval(np.polyfit(age, y, 4), grid), color=ACCENT, lw=2.2)

    # 2 -- step function: the age quartiles as cut points, mean wage per bin.
    ax = panel(axes[0, 1], "Step function (4 bins)", ORANGE)
    edges = [age.min()] + KNOTS + [age.max()]
    for lo, hi in zip(edges[:-1], edges[1:]):
        inside = (age >= lo) & (age < hi) if hi != edges[-1] else (age >= lo)
        ax.plot([lo, hi], [y[inside].mean()] * 2, color=ORANGE, lw=2.2)
    for k in KNOTS:
        ax.axvline(k, color=GREY, ls=":", lw=0.9)

    # 3 -- cubic spline: truncated-power basis, the one drawn in fig_spline_basis.
    ax = panel(axes[1, 0], "Cubic spline (3 knots)", GREEN)
    def cubic(v):
        v = np.asarray(v, float)
        return np.column_stack([v**p for p in range(4)]
                               + [np.clip(v - k, 0, None) ** 3 for k in KNOTS])
    beta, *_ = np.linalg.lstsq(cubic(age), y, rcond=None)
    ax.plot(grid, cubic(grid) @ beta, color=GREEN, lw=2.2)
    for k in KNOTS:
        ax.axvline(k, color=GREY, ls=":", lw=0.9)

    # 4 -- natural spline, df = 5: five knots at evenly spaced age quantiles.
    ax = panel(axes[1, 1], "Natural spline (df=5)", RED)
    ns_knots = np.quantile(age, [0.10, 0.30, 0.50, 0.70, 0.90])
    beta, *_ = np.linalg.lstsq(natural_basis(age, ns_knots), y, rcond=None)
    ax.plot(grid, natural_basis(grid, ns_knots) @ beta, color=RED, lw=2.2)

    save(fig, "ch07_wage_fits.png")
    print("ch07_wage_fits.png: n =", len(age), "· step-function bin means",
          np.round([y[(age >= lo) & (age < hi)].mean()
                    for lo, hi in zip(edges[:-1], edges[1:])], 1))


def fig_gam_components():
    """The fitted f_j of wage ~ s(age) + s(year) + education, each centred.

    One least-squares fit on a block design matrix rather than backfitting: the
    model is additive and linear in its coefficients, so the two agree, and this
    way the partial effects come straight out of one coefficient vector.
    """
    df = wage()
    age = df["age"].to_numpy(float)
    year = df["year"].to_numpy(float)
    y = df["wage"].to_numpy(float)
    levels = sorted(df["education"].unique())
    edu = df["education"].to_numpy()

    age_k = np.quantile(age, [0.10, 0.30, 0.50, 0.70, 0.90])
    year_k = np.quantile(year, [0.15, 0.50, 0.85])

    B_age = natural_basis(age, age_k)[:, 1:]      # drop each block's intercept;
    B_year = natural_basis(year, year_k)[:, 1:]   # one shared intercept below
    B_edu = np.column_stack([(edu == lv).astype(float) for lv in levels[1:]])
    X = np.column_stack([np.ones_like(y), B_age, B_year, B_edu])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)

    n_a, n_y = B_age.shape[1], B_year.shape[1]
    b_age = beta[1:1 + n_a]
    b_year = beta[1 + n_a:1 + n_a + n_y]
    b_edu = np.concatenate([[0.0], beta[1 + n_a + n_y:]])

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.4))
    fig.suptitle("GAM component functions: wage ~ s(age) + s(year) + education",
                 fontsize=12)

    g = np.linspace(age.min(), age.max(), 300)
    f = natural_basis(g, age_k)[:, 1:] @ b_age
    f -= (natural_basis(age, age_k)[:, 1:] @ b_age).mean()   # centre on the data
    axes[0].plot(g, f, color=ACCENT, lw=2.4)
    axes[0].set_title("f(age)", fontsize=11); axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Partial effect on wage")

    g = np.linspace(year.min(), year.max(), 300)
    f = natural_basis(g, year_k)[:, 1:] @ b_year
    f -= (natural_basis(year, year_k)[:, 1:] @ b_year).mean()
    axes[1].plot(g, f, color=GREEN, lw=2.4)
    axes[1].set_title("f(year)", fontsize=11); axes[1].set_xlabel("Year")

    eff = b_edu - b_edu.mean()
    short = ["< HS", "HS", "Some Coll", "Coll", "Adv Deg"]
    axes[2].vlines(range(len(eff)), 0, eff, color=ORANGE, alpha=0.55, lw=2.4)
    axes[2].scatter(range(len(eff)), eff, color=ORANGE, s=55, zorder=3)
    axes[2].set_xticks(range(len(eff)))
    axes[2].set_xticklabels(short, rotation=30, ha="right", fontsize=9)
    axes[2].set_title("f(education)", fontsize=11)

    for ax in axes:
        ax.axhline(0, color=GREY, lw=0.8, alpha=0.5)
        ax.grid(False)

    save(fig, "ch07_gam_components.png")
    print("ch07_gam_components.png: education effects",
          dict(zip(short, np.round(eff, 1))))


def smoothing_spline(x, y, lam):
    """Natural cubic smoothing spline by the Reinsch algorithm.

    Returns (unique ages, fitted values, effective df). The penalty is
    lam * integral f''(t)^2 dt with t in years, so lam is on the raw age scale —
    which is what the slide's lambda values refer to.
    """
    xs, inverse = np.unique(x, return_inverse=True)
    counts = np.bincount(inverse).astype(float)
    ybar = np.bincount(inverse, weights=y) / counts        # duplicate ages collapse
    n = len(xs)
    h = np.diff(xs)

    Q = np.zeros((n, n - 2))
    R = np.zeros((n - 2, n - 2))
    for j in range(n - 2):
        Q[j, j] = 1 / h[j]
        Q[j + 1, j] = -1 / h[j] - 1 / h[j + 1]
        Q[j + 2, j] = 1 / h[j + 1]
        R[j, j] = (h[j] + h[j + 1]) / 3
        if j < n - 3:
            R[j, j + 1] = R[j + 1, j] = h[j + 1] / 6

    K = Q @ np.linalg.solve(R, Q.T)
    W = np.diag(counts)
    S = np.linalg.solve(W + lam * K, W)                    # the smoother matrix
    fit = S @ ybar
    assert np.isfinite(S).all() and np.isfinite(fit).all()
    return xs, fit, np.trace(S)


def fig_smooth_spline():
    """Two smoothing splines on the same 300-point Wage subsample.

    lambda is the only thing that changes between the two curves, so the slide
    can point at one dial rather than at a change of method.
    """
    df = wage()
    sub = df.sample(300, random_state=0)
    age = sub["age"].to_numpy(float)
    y = sub["wage"].to_numpy(float)

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.scatter(age, y, s=14, color=GREY, alpha=0.35, edgecolors="none",
               label="Wage subsample (n=300)")

    for lam, colour, lw, word in [(0.1, ORANGE, 1.6, "wiggly"),
                                  (10_000, ACCENT, 2.6, "smooth")]:
        xs, fit, edf = smoothing_spline(age, y, lam)
        # The solution is a natural cubic spline through the fitted values, so
        # draw it as one — joining the knots with straight lines would make the
        # wiggly fit look like a polyline and lose the point of the slide.
        grid = np.linspace(xs.min(), xs.max(), 600)
        curve = CubicSpline(xs, fit, bc_type="natural")(grid)
        lam_txt = f"{lam:g}"
        ax.plot(grid, curve, color=colour, lw=lw,
                label=rf"$\lambda={lam_txt}$ ({word}, df $\approx$ {edf:.1f})")
        print(f"ch07_x_smooth_spline.png: lambda={lam_txt} -> {edf:.2f} effective df")

    ax.set_title(r"Smoothing splines on Wage: $\lambda$ is the flexibility dial",
                 fontsize=12)
    ax.set_xlabel("Age"); ax.set_ylabel("Wage ($1000s)")
    ax.legend(frameon=False, fontsize=9.5)
    ax.grid(False)
    save(fig, "ch07_x_smooth_spline.png")


if __name__ == "__main__":
    fig_spline_basis()
    fig_wage_fits()
    fig_gam_components()
    fig_smooth_spline()

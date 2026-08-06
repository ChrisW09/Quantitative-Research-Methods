"""Generate the computed matplotlib figures for the Chapter 2 deck (Statistical Learning).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_02/make_figures.py

Output: Chapters/chapter_02/images/ch02_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. Existing figures are not touched.
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
GREEN = "#2E7D5B"
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




CRIMSON = "#B03030"

def fig_knn_by_hand():
    """Exercise 2.7 drawn: six labelled points, the query, and the K=1 / K=3 circles."""
    P = np.array([[2, 4], [1, 2], [3, 2], [4, 4], [1, 5], [4, 1]], dtype=float)
    labels = ["Blue", "Red", "Red", "Blue", "Blue", "Red"]
    x0 = np.array([2.0, 3.0])
    d = np.sqrt(((P - x0) ** 2).sum(axis=1))

    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    for r, ls, lab, lxy in [(d.min(), "-", "$K=1$: only $P_1$", (3.62, 2.52)),
                            (np.sort(d)[2], "--", "$K=3$: adds $P_2,P_3$", (2.1, 4.68))]:
        circ = plt.Circle(x0, r + 0.02, fill=False, color=GREY, lw=1.1, ls=ls)
        ax.add_patch(circ)
        ax.annotate(lab, lxy, fontsize=8.5, color=GREY)

    # per-point label offsets: P_2 and P_3 sit exactly on the K=3 circle, so
    # their labels are pushed outwards instead of onto the dashed line
    offs = [(0.13, 0.13), (-0.10, -0.45), (0.16, -0.45),
            (0.13, 0.13), (0.13, 0.13), (0.13, 0.13)]
    for i, (pt, lab) in enumerate(zip(P, labels)):
        c = ACCENT if lab == "Blue" else CRIMSON
        m = "o" if lab == "Blue" else "s"      # shape doubles the colour coding
        ax.plot(*pt, m, color=c, ms=9, mec="white", mew=1.0, zorder=4)
        ax.annotate(f"$P_{i+1}$", pt,
                    xytext=(pt[0] + offs[i][0], pt[1] + offs[i][1]),
                    fontsize=9, color=c)
    ax.plot(*x0, "*", color=ORANGE, ms=15, mec="white", mew=0.8, zorder=5)
    ax.annotate("$x_0=(2,3)$", x0, xytext=(x0[0] - 0.80, x0[1] - 0.50),
                fontsize=9, color=ORANGE)

    ax.set_xlim(0.2, 5.4); ax.set_ylim(0.4, 5.6)
    ax.set_aspect("equal")
    ax.set_xlabel("$X_1$"); ax.set_ylabel("$X_2$")
    save(fig, "ch02_knn_by_hand.png")
    order = np.argsort(d, kind="stable")
    print("ch02_knn_by_hand.png: nearest", [f"P{j+1}={d[j]:.3f}" for j in order[:3]])


def fig_param_vs_nonparam():
    """Parametric (straight line) vs.\\ nonparametric (kernel smoother) on one predictor.

    Seeded simulation --- ``RNG = np.random.default_rng(0)`` at the top of this
    file. The truth is the smooth, deliberately non-linear

        f(x) = 0.25 + 2x - 0.11 x^2 + 2.4 sin(0.9 x),   x ~ U(0, 10),

    observed with Gaussian noise of standard deviation 1.25 at n = 50 points.
    The parametric fit is ordinary least squares on (1, x); the nonparametric
    fit is a Nadaraya--Watson kernel smoother with a Gaussian kernel of
    bandwidth h = 1.0. The slide quotes no numbers --- it makes the qualitative
    point that the line underfits the curvature while the smoother tracks it.
    """
    rng = np.random.default_rng(0)
    f = lambda t: 0.25 + 2.0 * t - 0.11 * t ** 2 + 2.4 * np.sin(0.9 * t)
    n, sd, h = 50, 1.25, 1.0
    x = np.sort(rng.uniform(0.0, 10.0, n))
    y = f(x) + rng.normal(0.0, sd, n)

    grid = np.linspace(0.0, 10.0, 400)
    b1, b0 = np.polyfit(x, y, 1)                     # parametric: two parameters
    w = np.exp(-0.5 * ((grid[:, None] - x[None, :]) / h) ** 2)
    smooth = (w * y).sum(axis=1) / w.sum(axis=1)      # nonparametric: no fixed form

    fig, ax = plt.subplots(figsize=(7.5, 4.25))
    ax.plot(x, y, "o", color=GREY, ms=5, alpha=0.7, mec="none",
            label="observed sample")
    ax.plot(grid, f(grid), "--", color="black", lw=1.8, label="true $f$ (unknown)")
    ax.plot(grid, b0 + b1 * grid, color=ORANGE, lw=2.0,
            label="parametric fit (linear)")
    ax.plot(grid, smooth, color=ACCENT, lw=2.0,
            label="nonparametric fit (kernel smoother)")

    ax.set_xlabel("$X$ (single predictor)")
    ax.set_ylabel("$Y$ (response)")
    ax.set_title("Same data, two strategies for estimating $f$", fontweight="bold")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
    save(fig, "ch02_param_vs_nonparam.png")
    print(f"  parametric fit: y = {b0:.2f} + {b1:.2f} x;  "
          f"RMSE(line, f) = {np.sqrt(np.mean((b0 + b1 * grid - f(grid)) ** 2)):.2f}, "
          f"RMSE(smoother, f) = {np.sqrt(np.mean((smooth - f(grid)) ** 2)):.2f}")


def fig_knn_boundary():
    """KNN decision boundaries at K = 1 and K = 100 on the same simulated sample.

    Seeded simulation --- ``np.random.default_rng(0)``. Two overlapping,
    unit-variance Gaussian clouds of 100 points each that differ only in $X_1$:
    class ``blue`` centred at (0, 0) and class ``orange`` at (1.5, 0), so the
    Bayes boundary is the vertical line $X_1 = 0.75$ and the Bayes error rate is
    $\\Phi(-0.75) \\approx 0.227$. Nothing is drawn by hand: both boundaries are
    the 0.5 contour of scikit-learn's ``KNeighborsClassifier`` over a fine grid.
    """
    from sklearn.neighbors import KNeighborsClassifier

    rng = np.random.default_rng(0)
    n_per = 100
    X = np.vstack([rng.normal([0.0, 0.0], 1.0, (n_per, 2)),
                   rng.normal([1.5, 0.0], 1.0, (n_per, 2))])
    y = np.r_[np.zeros(n_per), np.ones(n_per)]

    pad = 0.75
    xs = np.linspace(X[:, 0].min() - pad, X[:, 0].max() + pad, 400)
    ys = np.linspace(X[:, 1].min() - pad, X[:, 1].max() + pad, 400)
    gx, gy = np.meshgrid(xs, ys)
    grid = np.c_[gx.ravel(), gy.ravel()]

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.5), sharey=True)
    for ax, K in zip(axes, (1, 100)):
        p = KNeighborsClassifier(n_neighbors=K).fit(X, y).predict(grid).reshape(gx.shape)
        ax.contourf(gx, gy, p, levels=[-0.5, 0.5, 1.5],
                    colors=[ACCENT, ORANGE], alpha=0.15)
        ax.contour(gx, gy, p, levels=[0.5], colors="black", linewidths=1.0)
        for cls, colour in ((0, ACCENT), (1, ORANGE)):
            ax.plot(X[y == cls, 0], X[y == cls, 1], "o", color=colour,
                    ms=3.4, mec="none")
        ax.set_title(f"KNN, K = {K}")
        ax.set_xlabel("$X_1$")
        ax.set_xticks([]); ax.set_yticks([])
        ax.grid(False)
        ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1])
    axes[0].set_ylabel("$X_2$")
    save(fig, "ch02_knn_boundary.png")
    for K in (1, 100):
        m = KNeighborsClassifier(n_neighbors=K).fit(X, y)
        print(f"  K={K:3d}: training error {1 - m.score(X, y):.3f}")


def fig_flexibility_mse():
    """The bias--variance U-curve: training vs.\\ test MSE against polynomial degree.

    Seeded simulation --- ``np.random.default_rng(0)``. The truth is
    ``f(x) = 3 sin(x) + 0.15 x^2`` on ``x ~ U(0, 8)``, observed with Gaussian
    noise of standard deviation ``sigma = 1.6``, so the irreducible error is
    ``Var(eps) = sigma^2 = 2.56`` --- the dashed floor on the plot. Each of 300
    replications draws a fresh training set of 44 points and a fresh test set of
    1000 points, fits polynomials of degree 1..8 by least squares, and records
    both MSEs; the curves are the averages, which is why they are smooth.

    Training MSE falls monotonically towards ``sigma^2 (1 - (d+1)/n)``; test MSE
    is U-shaped with its minimum at degree 4.
    """
    from numpy.polynomial import Polynomial

    rng = np.random.default_rng(0)
    f = lambda t: 3.0 * np.sin(t) + 0.15 * t ** 2
    n_train, n_test, sigma, reps = 44, 1000, 1.6, 300
    degrees = np.arange(1, 9)

    train = np.zeros(degrees.size)
    test = np.zeros(degrees.size)
    for _ in range(reps):
        xt = rng.uniform(0.0, 8.0, n_train); yt = f(xt) + rng.normal(0.0, sigma, n_train)
        xe = rng.uniform(0.0, 8.0, n_test); ye = f(xe) + rng.normal(0.0, sigma, n_test)
        for i, d in enumerate(degrees):
            fit = Polynomial.fit(xt, yt, d)
            train[i] += np.mean((fit(xt) - yt) ** 2)
            test[i] += np.mean((fit(xe) - ye) ** 2)
    train /= reps
    test /= reps
    best = int(np.argmin(test))

    fig, ax = plt.subplots(figsize=(6.9, 4.09))
    ax.plot(degrees, train, "o-", color=GREY, lw=2.0, ms=5, label="Training MSE")
    ax.plot(degrees, test, "o-", color=ORANGE, lw=2.0, ms=5, label="Test MSE")
    ax.axhline(sigma ** 2, ls="--", color=GREEN, lw=1.8,
               label="Irreducible error $\\sigma^2$")
    ax.plot(degrees[best], test[best], "o", mfc="none", mec=ACCENT, ms=13, mew=1.8)
    ax.annotate("min test MSE", xy=(degrees[best] + 0.08, test[best] + 0.25),
                xytext=(degrees[best] + 0.75, test[best] + 2.1),
                color=ACCENT, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.9))

    ax.set_xlabel("Flexibility (polynomial degree)")
    ax.set_ylabel("Mean squared error")
    ax.set_title("Training vs. test MSE as flexibility grows")
    ax.set_xticks(degrees)
    ax.set_ylim(0, max(test.max(), train.max()) * 1.06)
    ax.legend(loc="upper center", fontsize=9, frameon=False)
    save(fig, "ch02_flexibility_mse.png")
    print("  degree :", list(degrees))
    print("  train  :", np.round(train, 3).tolist())
    print("  test   :", np.round(test, 3).tolist())
    print(f"  min test MSE at degree {degrees[best]} = {test[best]:.3f}; "
          f"floor Var(eps) = {sigma ** 2:.2f}")


if __name__ == "__main__":
    fig_knn_by_hand()
    fig_param_vs_nonparam()
    fig_knn_boundary()
    fig_flexibility_mse()

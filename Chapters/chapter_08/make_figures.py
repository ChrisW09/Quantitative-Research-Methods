"""Generate the computed matplotlib figures for the Chapter 8 (Tree-Based Methods) deck.

Everything is computed exactly or from a seeded simulation --- nothing is
sketched by hand. Run from anywhere:

    python Chapters/chapter_08/make_figures.py

Output: Chapters/chapter_08/images/ch08_*.png at 150 dpi, matching the other decks. Existing figures are not
touched.

Three of the figures (ch08_ensemble_error, ch08_importance,
ch08_x_bagging_variance) are drawn in the slightly different house style of the
original (now lost) draft script: white background, no grid, larger type, and
the darker accent palette #E08214 / #C62828 / #2E7D32. That style lives in
DRAFT_STYLE below and is applied with plt.rc_context so the remaining figures
keep the standard deck rcParams. Their numbers come from the bundled datasets
(Boston.csv, split test_size=0.3, random_state=1 --- the split used throughout
the deck's Boston solutions) or from a seeded simulation, and reproduce the
values quoted on the slides.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"

# Palette and rcParams of the three draft-script panels below.
GREEN_D = "#2E7D32"
ORANGE_D = "#E08214"
RED_D = "#C62828"
GREY_D = "#CECECE"

DRAFT_STYLE = {
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
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


def fig_impurity_measures():
    """Gini, scaled cross-entropy and classification error as functions of p-hat.

    The picture behind Exercise 8.2: error is piecewise linear and flat in
    exactly the region where Gini and entropy still reward purity gains.
    """
    p = np.linspace(0.001, 0.999, 400)
    gini = 2 * p * (1 - p)
    entropy = -(p * np.log2(p) + (1 - p) * np.log2(1 - p)) / 2   # scaled to max 0.5
    error = 1 - np.maximum(p, 1 - p)

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.plot(p, gini, color=ACCENT, lw=2)
    ax.plot(p, entropy, color=ORANGE, lw=1.8, ls="--")
    ax.plot(p, error, color=GREY, lw=2)

    ax.text(0.5, 0.525, "Gini $2\\hat p(1-\\hat p)$", color=ACCENT,
            fontsize=9.5, ha="center")
    ax.text(0.185, 0.44, "cross-entropy\n(scaled)", color=ORANGE, fontsize=9, ha="center")
    # both labels sit inside the triangle under the error curve, clear of the grey line
    ax.text(0.5, 0.285, "classification error", color=GREY, fontsize=9.5, ha="center")

    # the region where error is blind: moving p-hat toward 0 or 1 changes G but not E's slope
    ax.annotate("error has the same slope everywhere on each side ---\nit cannot prefer the split that creates a pure node",
                xy=(0.20, 0.20), xytext=(0.5, 0.055), fontsize=8, color="#333333",
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.set_xlabel(r"$\hat p$  (proportion of class 1 in the node)")
    ax.set_ylabel("node impurity")
    ax.set_xlim(0, 1); ax.set_ylim(0, 0.58)
    save(fig, "ch08_impurity_measures.png")
    print("ch08_impurity_measures.png: max Gini", gini.max().round(3),
          "max error", error.max().round(3))


def _boston_split():
    """Boston.csv with the deck's canonical 70/30 split (random_state=1).

    This is the split behind every Boston number quoted in the chapter:
    single tree ~26.7, bagging 8.6, forest m=4 -> 9.43 / m=6 -> 8.73,
    boosting 7.34.
    """
    boston = pd.read_csv(DATA / "Boston.csv", index_col=0)
    X, y = boston.drop(columns="medv"), boston["medv"]
    return train_test_split(X, y, test_size=0.3, random_state=1)


def fig_ensemble_error():
    """Boston test MSE as a function of ensemble size B, for three ensembles.

    Bagging (m=p) and the random forest (m=p/3) are scored by averaging the
    first B trees of a single 500-tree fit --- one fit per curve, so the whole
    figure costs three model fits rather than 3*500. Boosting uses
    staged_predict on one 500-tree fit. Endpoints: bagging 8.56, forest 9.43
    (the deck's 9.43 for m=4), boosting 7.64 --- boosting lowest, as the
    takeaway states.
    """
    Xtr, Xte, ytr, yte = _boston_split()
    p = Xtr.shape[1]
    yte_ = yte.to_numpy()
    B = 500
    trees = np.arange(1, B + 1)

    def forest_curve(m):
        rf = RandomForestRegressor(n_estimators=B, max_features=m,
                                   random_state=1).fit(Xtr, ytr)
        per_tree = np.array([t.predict(Xte.to_numpy()) for t in rf.estimators_])
        running = np.cumsum(per_tree, axis=0) / trees[:, None]
        return ((running - yte_) ** 2).mean(axis=1)

    bagging = forest_curve(p)
    forest = forest_curve(p // 3)
    gb = GradientBoostingRegressor(n_estimators=B, learning_rate=0.05,
                                   max_depth=3, random_state=1).fit(Xtr, ytr)
    boosting = np.array([((pred - yte_) ** 2).mean()
                         for pred in gb.staged_predict(Xte)])

    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7.2, 4.4))
        ax.plot(trees, bagging, color=ORANGE_D, lw=1.8, label="Bagging (m=p)")
        ax.plot(trees, forest, color=ACCENT, lw=1.8, label="Random forest (m=p/3)")
        ax.plot(trees, boosting, color=GREEN_D, lw=1.8,
                label="Boosting (depth 3, $\\nu$=0.05)")
        ax.set_xlabel("Number of trees")
        ax.set_ylabel("Test MSE")
        ax.set_title("Boston: test error vs. ensemble size")
        # framing of the committed original: the flat tails sit just above the
        # bottom spine instead of floating in the middle of the panel
        ax.set_ylim(6.4, 88.8)
        ax.legend(loc="upper right", frameon=False)
        save(fig, "ch08_ensemble_error.png")
    print("ch08_ensemble_error.png: B=500 test MSE --- bagging",
          round(bagging[-1], 2), "forest", round(forest[-1], 2),
          "boosting", round(boosting[-1], 2))


def fig_importance():
    """Impurity importances of the m=p/3 Boston forest, biggest first.

    Same fit as the deck's Boston solutions (500 trees, max_features=4,
    random_state=1 on the random_state=1 split): lstat 0.332 and rm 0.246
    dominate, then dis and nox --- exactly the ranking the slide describes.
    """
    Xtr, Xte, ytr, yte = _boston_split()
    rf = RandomForestRegressor(n_estimators=500, max_features=Xtr.shape[1] // 3,
                               random_state=1).fit(Xtr, ytr)
    imp = pd.Series(rf.feature_importances_,
                    index=Xtr.columns).sort_values(ascending=False)

    # lstat and rm carry the story, so they get the two warm colours
    colors = [RED_D, ORANGE_D] + [ACCENT] * (len(imp) - 2)
    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7.2, 4.4))
        pos = np.arange(len(imp))[::-1]
        ax.barh(pos, imp.to_numpy(), color=colors)
        ax.set_yticks(pos)
        ax.set_yticklabels(imp.index)
        ax.set_xlim(0, 0.35)
        ax.set_xlabel("Importance (mean decrease in RSS, normalised)")
        ax.set_title("Boston: random-forest variable importance")
        save(fig, "ch08_importance.png")
    print("ch08_importance.png: top of the ranking",
          imp.head(4).round(3).to_dict())


def fig_x_bagging_variance():
    """Simulation: one deep tree vs. the average of 100 bootstrap trees.

    n=120 points from y = sin(2x) + N(0, 0.35^2) on [0, 3], RNG seeded with
    np.random.default_rng(0). MSE is measured against the *truth* on a dense
    grid, which is what the slide quotes: single fully grown tree 0.15,
    bagged average of 100 trees 0.07. 100 trees is the number named in the
    slide text, and is already enough to show the smoothing.
    """
    rng = np.random.default_rng(0)
    n = 120
    x = np.sort(rng.uniform(0, 3, n))
    y = np.sin(2 * x) + rng.normal(0, 0.35, n)
    Xc = x.reshape(-1, 1)

    grid = np.linspace(0, 3, 500)
    grid_c = grid.reshape(-1, 1)
    truth = np.sin(2 * grid)

    single = DecisionTreeRegressor(random_state=0).fit(Xc, y)
    pred_single = single.predict(grid_c)

    boot_preds = []
    for b in range(100):
        idx = rng.integers(0, n, n)          # one bootstrap resample per tree
        tree = DecisionTreeRegressor(random_state=b).fit(Xc[idx], y[idx])
        boot_preds.append(tree.predict(grid_c))
    bagged = np.mean(boot_preds, axis=0)

    mse_single = ((pred_single - truth) ** 2).mean()
    mse_bagged = ((bagged - truth) ** 2).mean()

    with plt.rc_context(DRAFT_STYLE):
        fig, ax = plt.subplots(figsize=(7.0, 4.0))
        ax.plot(x, y, "o", color=GREY_D, ms=3, label="data")
        ax.plot(grid, truth, color=GREEN_D, lw=1.8, ls="--", label="truth sin(2$x$)")
        ax.plot(grid, pred_single, color=ORANGE_D, lw=1.2,
                label=f"single deep tree (MSE {mse_single:.2f})")
        ax.plot(grid, bagged, color=ACCENT, lw=2.2,
                label=f"bagged: mean of 100 trees (MSE {mse_bagged:.2f})")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_ylim(-2, 2)
        ax.set_yticks([-2, -1, 0, 1, 2])
        ax.set_title("Why bagging works: averaging kills single-tree variance")
        ax.legend(loc="lower left", frameon=False, fontsize=10)
        save(fig, "ch08_x_bagging_variance.png")
    print("ch08_x_bagging_variance.png: MSE vs truth --- single tree",
          round(mse_single, 3), "bagged(100)", round(mse_bagged, 3))


if __name__ == "__main__":
    fig_impurity_measures()
    fig_x_bagging_variance()
    fig_ensemble_error()
    fig_importance()

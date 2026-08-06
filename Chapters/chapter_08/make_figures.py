"""Generate the computed matplotlib figures for the Chapter 8 (Tree-Based Methods) deck.

Everything is computed exactly or from a seeded simulation --- nothing is
sketched by hand. Run from anywhere:

    python Chapters/chapter_08/make_figures.py

Output: Chapters/chapter_08/images/ch08_*.png at 150 dpi, matching the other decks. Existing figures are not
touched.
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


if __name__ == "__main__":
    fig_impurity_measures()

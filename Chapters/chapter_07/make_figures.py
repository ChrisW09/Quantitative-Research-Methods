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


if __name__ == "__main__":
    fig_spline_basis()

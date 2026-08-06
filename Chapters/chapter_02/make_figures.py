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


if __name__ == "__main__":
    fig_knn_by_hand()

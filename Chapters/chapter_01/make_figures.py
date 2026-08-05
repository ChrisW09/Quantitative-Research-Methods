"""Generate the computed matplotlib figures for the Chapter 1 deck (Introduction).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_01/make_figures.py

Output: Chapters/chapter_01/images/ch01_*.png at 150 dpi, matching the figure
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



def fig_n_vs_p():
    """The course's data sets on the n-vs-p map, with the p = n boundary.

    The chapter 1 lab closes on the same table; this is it drawn. Everything
    below the diagonal is the comfortable regime; NCI60 sits far above it.
    """
    data = [   # (name, n, p)
        ("Wage", 3000, 10), ("Smarket", 1250, 8), ("Auto", 392, 8),
        ("Default", 10000, 3), ("Hitters", 263, 19), ("Boston", 506, 13),
        ("Caravan", 5822, 85), ("NCI60", 64, 6830),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    lim = np.array([1, 3e4])
    ax.plot(lim, lim, color=GREY, lw=1.2, ls="--")
    ax.text(2.2e3, 1.4e3, "$p = n$", color=GREY, fontsize=9, rotation=31)

    offsets = {"Wage": (1.2, 1.0), "Smarket": (1.2, 1.0), "Auto": (0.82, 0.55),
               "Default": (1.2, 0.95), "Hitters": (0.9, 1.7), "Boston": (1.25, 1.15),
               "Caravan": (1.2, 1.0), "NCI60": (1.35, 0.9)}
    for name, n, p in data:
        special = name == "NCI60"
        ax.plot(n, p, "o", ms=7 if special else 6,
                color=ORANGE if special else ACCENT, mec="white", mew=0.8, zorder=4)
        dx, dy = offsets[name]
        ax.annotate(name, (n, p), xytext=(n * dx, p * dy),
                    fontsize=8.5, color=ORANGE if special else ACCENT, va="center")

    ax.text(230, 1.6e3, "$p \\gg n$: no unique\nleast-squares fit exists", color="#333333",
            fontsize=8, ha="left")
    ax.text(60, 1.6, "$n \\gg p$: the comfortable regime\n(Chapters 2\u20138)", color="#333333",
            fontsize=8)

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("observations $n$"); ax.set_ylabel("predictors $p$")
    ax.set_xlim(40, 3e4); ax.set_ylim(1, 3e4)
    save(fig, "ch01_n_vs_p.png")
    print("ch01_n_vs_p.png:", len(data), "datasets, NCI60 p/n =", round(6830/64, 1))


if __name__ == "__main__":
    fig_n_vs_p()

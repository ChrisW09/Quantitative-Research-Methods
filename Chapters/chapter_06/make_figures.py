"""Generate the computed matplotlib figures for the Chapter 6 deck (Selection).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_06/make_figures.py

Output: Chapters/chapter_06/images/ch06_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. Existing figures are not touched.
"""

from math import comb
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


if __name__ == "__main__":
    fig_search_space()

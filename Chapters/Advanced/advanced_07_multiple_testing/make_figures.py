"""Generate the computed matplotlib figures for advanced module A7 (Multiple Testing).

Everything is computed exactly or from a clearly labelled, seeded simulation
--- nothing is sketched by hand. Run from anywhere:

    python Chapters/Advanced/advanced_07_multiple_testing/make_figures.py

Output: images/ch13_*.png at 150 dpi, matching the other decks. The
ISLP-sourced figures (13_5.pdf, 13_6.pdf) and the pre-existing ch13_*.png
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


def fig_min_p():
    """What p-hacking harvests: the distribution of the smallest of m = 20
    p-values when every null is true. 20,000 simulated 'studies'."""
    m = 20
    min_p = RNG.uniform(size=(20_000, m)).min(axis=1)
    frac = (min_p <= 0.05).mean()
    theory = 1 - 0.95 ** m

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    bins = np.linspace(0, 0.4, 57)
    ax.hist(min_p[min_p > 0.05], bins=bins, color=ACCENT, alpha=0.75,
            edgecolor="white", linewidth=0.4)
    ax.hist(min_p[min_p <= 0.05], bins=bins, color=ORANGE,
            edgecolor="white", linewidth=0.4)
    ax.axvline(0.05, color=GREY, lw=1.1, ls="--")

    ax.text(0.052, 1550, f"min $p \\leq 0.05$ in {frac:.0%} of studies\n"
            f"(theory: $1-0.95^{{{m}}} = {theory:.3f}$)",
            fontsize=9, color="#8A4513")
    ax.text(0.185, 700, "the smallest of $m=20$\np-values, all nulls true\n"
            "(20,000 simulated studies)", fontsize=8.5, color=ACCENT)

    ax.set_xlabel("smallest p-value in the study")
    ax.set_ylabel("simulated studies")
    ax.set_xlim(0, 0.4)
    save(fig, "ch13_min_p.png")
    print(f"ch13_min_p: simulated {frac:.4f}, theory {theory:.4f}")


if __name__ == "__main__":
    fig_min_p()

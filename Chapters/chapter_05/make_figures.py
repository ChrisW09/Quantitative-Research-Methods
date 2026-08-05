"""Generate the computed matplotlib figures for the Chapter 5 deck (Resampling).

Every figure is either computed exactly or drawn from a clearly labelled,
seeded simulation --- nothing is sketched by hand, and every number quoted on
the slide comes out of this file. Run from anywhere:

    python Chapters/chapter_05/make_figures.py

Output: Chapters/chapter_05/images/ch05_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The ISLP-sourced figures
(``5_2.pdf`` etc.) are not touched.
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


def fig_inclusion_probability():
    """The Exercise 5.5 result drawn: P(row included in a bootstrap resample).

    Theory is exact, 1 - (1 - 1/n)^n; the dots check it by simulation
    (20,000 resamples per n, seeded), the same experiment the chapter 5 lab
    runs in its 'What is actually in a bootstrap sample?' section.
    """
    n_grid = np.unique(np.round(np.logspace(np.log10(2), 3, 60)).astype(int))
    theory = 1 - (1 - 1 / n_grid) ** n_grid

    n_sim = np.array([2, 3, 5, 10, 20, 50, 100, 300, 1000])
    simulated = []
    for n in n_sim:
        draws = RNG.integers(0, n, size=(20_000, n))
        simulated.append((draws == 0).any(axis=1).mean())

    limit = 1 - np.exp(-1)

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.axhline(limit, color=GREY, lw=1.2, ls="--", zorder=1)
    ax.plot(n_grid, theory, color=ACCENT, lw=2, zorder=3)
    ax.plot(n_sim, simulated, "o", color=ORANGE, ms=5,
            mec="white", mew=0.8, zorder=4)

    # direct labels instead of a legend box
    ax.text(3.2, 0.715, r"theory: $1-(1-1/n)^n$", color=ACCENT, fontsize=9)
    ax.text(120, 0.658, "simulation\n(20{,}000 resamples per $n$)".replace("{,}", ","),
            color=ORANGE, fontsize=8.5, ha="left")
    ax.text(950, limit + 0.0025, r"$1-1/e \approx 0.632$", color=GREY,
            fontsize=9, ha="right", va="bottom")

    ax.set_xscale("log")
    ax.set_xlabel(r"sample size $n$")
    ax.set_ylabel("P(a given row is in the resample)")
    ax.set_ylim(0.615, 0.775)
    ax.set_xlim(1.8, 1100)
    ax.set_xticks([2, 5, 10, 50, 100, 1000])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    save(fig, "ch05_inclusion_probability.png")
    print("ch05_inclusion_probability.png:",
          f"n=5 -> {1 - (1 - 1/5)**5:.4f}, n=1000 -> {1 - (1 - 1/1000)**1000:.4f},",
          f"limit {limit:.4f}")


if __name__ == "__main__":
    fig_inclusion_probability()

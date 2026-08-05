"""Generate the computed matplotlib figures for the Chapter 3 deck (Linear Regression).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_03/make_figures.py

Output: Chapters/chapter_03/images/ch03_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. Existing figures are not touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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




DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition"

def fig_ci_vs_pi():
    """95% confidence band vs 95% prediction band for mpg ~ horsepower on Auto.

    Computed with statsmodels' exact formulas; the same fit the lab runs.
    """
    import statsmodels.api as sm
    df = pd.read_csv(DATA / "Auto.csv", na_values="?").dropna()
    x = df["horsepower"].astype(float).values
    y = df["mpg"].values
    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit()

    grid = np.linspace(x.min(), x.max(), 120)
    pred = res.get_prediction(sm.add_constant(grid)).summary_frame(alpha=0.05)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.scatter(x, y, s=7, alpha=0.30, color=GREY, edgecolors="none", zorder=2)
    ax.fill_between(grid, pred["obs_ci_lower"], pred["obs_ci_upper"],
                    color=ORANGE, alpha=0.18, zorder=1)
    ax.fill_between(grid, pred["mean_ci_lower"], pred["mean_ci_upper"],
                    color=ACCENT, alpha=0.45, zorder=3)
    ax.plot(grid, pred["mean"], color=ACCENT, lw=2, zorder=4)

    ax.annotate("95% confidence band:\nwhere the average mpg lies", xy=(60, 30.2),
                xytext=(46, 6.5), fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate("95% prediction band:\nwhere a single car lies", xy=(170, 15.5),
                xytext=(150, 34), fontsize=8.5, color="#8A4513",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.set_xlabel("horsepower"); ax.set_ylabel("mpg")
    save(fig, "ch03_ci_vs_pi.png")
    i = 60  # report widths mid-range
    print("ch03_ci_vs_pi.png: CI width", round(pred["mean_ci_upper"][i]-pred["mean_ci_lower"][i], 2),
          "PI width", round(pred["obs_ci_upper"][i]-pred["obs_ci_lower"][i], 2),
          "at hp", round(grid[i]))


if __name__ == "__main__":
    fig_ci_vs_pi()

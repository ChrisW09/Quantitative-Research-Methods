"""Generate the computed matplotlib figures for the Chapter 1 deck (Introduction).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_01/make_figures.py

Output: Chapters/chapter_01/images/ch01_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The two appendix figures
(ch01_wage_overview, ch01_x_smarket_lag_boxplots) read the bundled CSVs from
"ALL CSV FILES - 2nd Edition"; the ISLP PDFs shipped in images/ are untouched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
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

# The two appendix figures are shown at 0.98\textwidth on a 16:9 slide, so they
# are drawn wide, ungridded and with larger type than the in-text figures. The
# override is local (rc_context) so the module defaults above stay in force.
APPENDIX_RC = {"font.size": 13, "axes.titlesize": 13, "axes.grid": False}
APPENDIX_SIZE = (10.01, 3.61)
# Scatter style shared by panels (a) and (b) of the Wage overview: 3000 points
# in a third of the figure, so small and faint enough to read as a cloud.
DOTS = {"s": 9, "color": GREY, "alpha": 0.21, "linewidths": 0}


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


def fig_wage_overview():
    """Wage.csv up close: wage against age, against year, and by education.

    The appendix slide "Wage data up close" claims wage rises then dips with
    age, drifts gently upward over the years, and climbs steeply with
    education. All three panels are computed from the raw file:

      (a) grey scatter of all n = 3000 workers plus a LOWESS smooth
          (frac = 0.45) --- the peak sits near age 44 at about $112k and the
          curve falls away on both sides, so the age effect is nonlinear;
      (b) the same wages against year, jittered horizontally by a seeded
          uniform +/- 0.25 so the seven yearly columns are readable, plus the
          least-squares line: it runs from $107.9k in 2003 to $116.0k in 2009,
          a drift of about $1.35k per year;
      (c) box-and-whisker of wage by education level (outliers hidden). The
          medians climb monotonically: 81.3, 94.1, 104.9, 118.9, 141.8.

    The horizontal jitter in (b) is the only randomness; it is cosmetic and
    seeded with the house RNG = np.random.default_rng(0).
    """
    w = pd.read_csv(DATA / "Wage.csv")
    age = w["age"].to_numpy(float)
    year = w["year"].to_numpy(float)
    wage = w["wage"].to_numpy(float)

    with plt.rc_context(APPENDIX_RC):
        fig, axes = plt.subplots(1, 3, figsize=APPENDIX_SIZE)

        ax = axes[0]
        ax.scatter(age, wage, **DOTS)
        smooth = lowess(wage, age, frac=0.45, return_sorted=True)
        ax.plot(smooth[:, 0], smooth[:, 1], color=ACCENT, lw=2.8,
                solid_capstyle="round")
        ax.set_title("(a) Wage vs. age")
        ax.set_xlabel("Age")
        ax.set_ylabel("Wage (\\$k)")

        ax = axes[1]
        jitter = RNG.uniform(-0.25, 0.25, size=year.size)
        ax.scatter(year + jitter, wage, **DOTS)
        slope, intercept = np.polyfit(year, wage, 1)
        ends = np.array([year.min(), year.max()])
        ax.plot(ends, intercept + slope * ends, color=ORANGE, lw=2.4,
                solid_capstyle="round")
        ax.set_title("(b) Wage vs. year")
        ax.set_xlabel("Year")
        ax.set_xticks([2003, 2005, 2007, 2009])

        ax = axes[2]
        levels = sorted(w["education"].unique())
        groups = [w.loc[w["education"] == lv, "wage"].to_numpy() for lv in levels]
        bp = ax.boxplot(groups, widths=0.6, showfliers=False, patch_artist=True)
        for patch in bp["boxes"]:
            patch.set_facecolor(ACCENT)
            patch.set_alpha(0.55)
            patch.set_edgecolor("black")
            patch.set_linewidth(1.0)
        for line in bp["whiskers"] + bp["caps"]:
            line.set_color("black")
            line.set_linewidth(1.0)
        for line in bp["medians"]:
            line.set_color("black")
            line.set_linewidth(1.8)
        ax.set_title("(c) Wage by education")
        ax.set_xlabel("Education")
        # Two-line labels at 9 pt: the five levels have to sit side by side
        # inside one third of the figure without touching.
        ax.set_xticklabels(["<HS", "HS", "Some\ncoll.", "Coll.\ngrad",
                            "Adv.\ndeg."], fontsize=9)

        save(fig, "ch01_wage_overview.png")

    peak = smooth[np.argmax(smooth[:, 1])]
    print("ch01_wage_overview.png: n =", len(w),
          "| LOWESS peak at age", round(peak[0], 1), "->", round(peak[1], 1),
          "| year line", round(intercept + slope * 2003, 1), "->",
          round(intercept + slope * 2009, 1),
          "| education medians",
          [round(float(np.median(g)), 1) for g in groups])


def fig_x_smarket_lag_boxplots():
    """Figure 1.2 rebuilt from Smarket.csv: Lag1 and Lag2 by today's direction.

    The appendix slide quotes the median Lag1 before Down days (+0.10 %)
    against the median before Up days (-0.05 %) --- a 0.15-point gap set
    against boxes that span roughly +/- 0.6 %. Both come straight out of the
    file: median Lag1 is +0.1035 for Down and -0.0480 for Up, and the quartiles
    are -0.580/+0.662 (Down) and -0.678/+0.532 (Up).

    Boxes are standard Tukey boxes (whiskers at 1.5 IQR, outliers drawn as
    faint dots), so nothing here is smoothed or simulated.
    """
    s = pd.read_csv(DATA / "Smarket.csv")

    with plt.rc_context(APPENDIX_RC):
        fig, axes = plt.subplots(1, 2, figsize=APPENDIX_SIZE, sharey=True)
        panels = (("Lag1", "Yesterday (Lag1)"), ("Lag2", "Two days ago (Lag2)"))
        for ax, (lag, title) in zip(axes, panels):
            groups = [s.loc[s["Direction"] == d, lag].to_numpy()
                      for d in ("Down", "Up")]
            ax.axhline(0.0, color=GREY, ls=":", lw=1.0, zorder=0)
            bp = ax.boxplot(groups, widths=0.55, patch_artist=True)
            for patch, colour in zip(bp["boxes"], (ACCENT, ORANGE)):
                patch.set_facecolor(colour)
                patch.set_alpha(0.75)
                patch.set_edgecolor("#555555")
                patch.set_linewidth(1.0)
            for line in bp["whiskers"] + bp["caps"]:
                line.set_color("#555555")
                line.set_linewidth(1.0)
            for line in bp["medians"]:
                line.set_color("black")
                line.set_linewidth(2.0)
            for flier in bp["fliers"]:
                flier.set(marker="o", markersize=4, markerfacecolor=GREY,
                          markeredgecolor="none", alpha=0.35)
            ax.set_title(title)
            ax.set_xticklabels(["Down", "Up"])
            ax.set_xlabel("Today's market direction")
        axes[0].set_ylabel("Percentage return")

        save(fig, "ch01_x_smarket_lag_boxplots.png")

    med = s.groupby("Direction")["Lag1"].median()
    print("ch01_x_smarket_lag_boxplots.png: median Lag1 before Down =",
          round(med["Down"], 4), "| before Up =", round(med["Up"], 4),
          "| gap =", round(med["Down"] - med["Up"], 4))


if __name__ == "__main__":
    fig_n_vs_p()
    fig_wage_overview()
    fig_x_smarket_lag_boxplots()

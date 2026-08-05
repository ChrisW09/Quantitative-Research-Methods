"""Generate the computed matplotlib figures for the Chapter 4 deck (Classification).

Every figure is computed from the bundled course data (``Default.csv``) with a
seeded split --- nothing is sketched by hand, and every number quoted on the
slide comes out of this file. The split, scaler and model match the chapter 4
lab exactly (test_size=0.3, random_state=0), so the deck and the notebook
print the same numbers. Run from anywhere:

    python Chapters/chapter_04/make_figures.py

Output: Chapters/chapter_04/images/ch04_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The ISLP-sourced figures
(``4_2.pdf`` etc.) are not touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition"
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


def fig_threshold_tradeoff():
    """Sensitivity, specificity and precision as functions of the threshold.

    Identical pipeline to the chapter 4 lab's 'the threshold is a business
    decision' section: logistic regression on balance, income, student on the
    same seeded 70/30 split, so the numbers printed here are the numbers the
    notebook prints.
    """
    df = pd.read_csv(DATA / "Default.csv")
    df["student_d"] = (df["student"] == "Yes").astype(int)
    y = (df["default"] == "Yes").astype(int).values
    X = df[["balance", "income", "student_d"]].values

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
    scaler = StandardScaler().fit(Xtr)
    model = LogisticRegression(max_iter=2000).fit(scaler.transform(Xtr), ytr)
    proba = model.predict_proba(scaler.transform(Xte))[:, 1]

    ts = np.linspace(0.005, 0.9, 300)
    sens, spec, prec = [], [], []
    for t in ts:
        pred = proba >= t
        tp = (pred & (yte == 1)).sum()
        fn = (~pred & (yte == 1)).sum()
        fp = (pred & (yte == 0)).sum()
        tn = (~pred & (yte == 0)).sum()
        sens.append(tp / (tp + fn))
        spec.append(tn / (tn + fp))
        prec.append(tp / (tp + fp) if tp + fp else np.nan)

    def counts_at(t):
        pred = proba >= t
        return (pred & (yte == 1)).sum(), (yte == 1).sum()

    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    for t in (0.10, 0.50):
        ax.axvline(t, color=GREY, lw=1.0, ls=":", zorder=1)
    ax.plot(ts, sens, color=ACCENT, lw=2, zorder=3)
    ax.plot(ts, prec, color=ORANGE, lw=2, zorder=3)
    ax.plot(ts, spec, color=GREY, lw=1.6, zorder=2)

    ax.text(0.55, 0.44, "sensitivity", color=ACCENT, fontsize=9.5)
    ax.text(0.40, 0.60, "precision", color=ORANGE, fontsize=9.5)
    ax.text(0.62, 1.035, "specificity", color=GREY, fontsize=9)

    tp10, pos = counts_at(0.10)
    tp50, _ = counts_at(0.50)
    ax.annotate(f"$t=0.10$: catches {tp10}/{pos}\ndefaulters",
                xy=(0.10, np.interp(0.10, ts, sens)), xytext=(0.145, 0.87),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate(f"$t=0.50$: catches {tp50}/{pos}",
                xy=(0.50, np.interp(0.50, ts, sens)), xytext=(0.33, 0.18),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.set_xlabel(r"decision threshold $t$   (predict default when $\hat p \geq t$)")
    ax.set_ylabel("value on the held-out 30%")
    ax.set_xlim(0, 0.9)
    ax.set_ylim(0, 1.06)

    save(fig, "ch04_threshold_tradeoff.png")
    i10 = np.argmin(np.abs(ts - 0.10)); i50 = np.argmin(np.abs(ts - 0.50))
    print("ch04_threshold_tradeoff.png:",
          f"t=0.10 sens {sens[i10]:.3f} prec {prec[i10]:.3f} |",
          f"t=0.50 sens {sens[i50]:.3f} prec {prec[i50]:.3f} |",
          f"caught {tp10}/{pos} vs {tp50}/{pos}")


if __name__ == "__main__":
    fig_threshold_tradeoff()

"""Generate the computed matplotlib figures for the Chapter 10 (Deep Learning) deck.

Everything is computed exactly or from a seeded simulation --- nothing is
sketched by hand. Run from anywhere:

    python Chapters/chapter_10/make_figures.py

Output: Chapters/chapter_10/images/ch10_*.png at 150 dpi, matching the other decks. Existing figures are not
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


def fig_conv_vs_dense():
    """Parameters of one conv layer vs a dense layer reaching the same outputs.

    Exercise 10.4 as a curve: a 16-filter 5x5 convolution costs 1,216
    parameters whatever the image size; a dense layer to the same output
    volume grows with the fourth power of the image side.
    """
    W = np.arange(8, 129)
    conv = np.full_like(W, 16 * (5 * 5 * 3 + 1), dtype=float)     # 1,216
    out_units = (W - 4) ** 2 * 16
    dense = (W ** 2 * 3).astype(float) * out_units + out_units

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(W, dense, color=ACCENT, lw=2)
    ax.plot(W, conv, color=ORANGE, lw=2)

    i32 = np.where(W == 32)[0][0]
    ax.plot([32, 32], [conv[i32], dense[i32]], color=GREY, lw=0.9, ls=":")
    ax.plot(32, dense[i32], "o", color=ACCENT, ms=5, mec="white", mew=0.8)
    ax.plot(32, conv[i32], "o", color=ORANGE, ms=5, mec="white", mew=0.8)
    ax.annotate("$32\\times32\\times3$ image:\n$38.5$M vs $1{,}216$\n($31{,}700\\times$)",
                xy=(32, dense[i32]), xytext=(40, 2e5), fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.text(88, 1.5e8, "dense layer to the\nsame output volume", color=ACCENT,
            fontsize=9, ha="center")
    ax.text(95, 3.2e3, "one conv layer: $1{,}216$ parameters,\nwhatever the image size",
            color=ORANGE, fontsize=9, ha="center", va="bottom")

    ax.set_yscale("log")
    ax.set_xlabel("image side $W$  (input $W\\times W\\times 3$, 16 filters of $5\\times5$)")
    ax.set_ylabel("trainable parameters")
    ax.set_xlim(8, 128)
    save(fig, "ch10_conv_vs_dense.png")
    print("ch10_conv_vs_dense.png: at W=32 dense", f"{dense[i32]:,.0f}", "conv 1,216",
          f"ratio {dense[i32]/1216:,.0f}x")


if __name__ == "__main__":
    fig_conv_vs_dense()

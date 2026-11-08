#!/usr/bin/env python3
"""Abbildungen für das Archiv-Deck "Statistik für Ökonomen – Teil 3: Regression"
(presentation.tex, images/image_020–029.png).

Beim Layout-Review (2026-10-30) neu erzeugt wurden nur die Grafiken, deren
Beschriftung auf der Folie zu klein war:

* image_021.png (Folie 27): Streuungsdiagramm mit Regressionsgerade – gleiche
  Geometrie und Schriftgrößen wie image_020.png, Legende größer und im
  deutschen Zahlenformat (ŷ = 54,667 − 0,447·x).
* image_022.png (Folie 37): vier typische Residuenmuster (2×2) – gleiche Daten
  (numpy-Seed 42, Erzeugung wie ursprünglich), Größe und Schrift passend zur
  Darstellung auf der Folie.

Jede Funktion fig_<name>() schreibt genau eine Datei images/<name>.png.
Daten: Preis-Absatz-Beispiel der Folien (vgl. Statistik_für_Ökonomen_Teil_3.R).

Aufruf:
    python3 generate_figures.py                 # alle Abbildungen dieses Skripts
    python3 -c "import generate_figures as g; g.fig_image_021()"

Benötigt: numpy, matplotlib
"""
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

IMGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")  # ../images
DPI = 300

PREIS = np.arange(80, 121, 5)                         # Preis x_i (Euro)
MENGE = np.array([20, 17, 15, 9, 11, 8, 4, 4, 2])     # Absatzmenge y_i

BLUE = "#2166ac"
RED = "#b2182b"
SPINE = "#333333"


def _save(fig, name):
    path = os.path.join(IMGDIR, name + ".png")
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("geschrieben:", path)


def _de(v, nd):
    """Zahl mit Dezimalkomma."""
    return f"{v:.{nd}f}".replace(".", ",")


def fig_image_021():
    """Folie 27: Streuungsdiagramm mit Regressionsgerade (Preis-Absatz).

    Leinwand, Achsenposition und Schriftgrößen (Titel 22, Achsen 20, Ticks 16 pt
    bei 7,75 × 5,68 in) wie image_020.png; die Legende hatte 12 pt (auf der Folie
    ≈ 5 pt) und hat jetzt 16 pt.
    """
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    w_px, h_px = 2324, 1703
    fig = plt.figure(figsize=(w_px / DPI, h_px / DPI))
    ax = fig.add_axes([304 / w_px, 1 - 1481 / h_px,
                       (2266 - 304) / w_px, (1481 - 125) / h_px])
    b1, b0 = np.polyfit(PREIS, MENGE, 1)          # 54,667 und −0,447
    ax.scatter(PREIS, MENGE, s=70, color=BLUE, edgecolor="white", linewidth=0.8,
               zorder=3)
    xx = np.linspace(75, 125, 200)
    label = "ŷ = " + _de(b0, 3) + " − " + _de(-b1, 3) + "·x"
    ax.plot(xx, b0 + b1 * xx, color=RED, lw=2.0, label=label)
    ax.set_xlim(75, 125)
    ax.set_ylim(0, 22)
    ax.grid(True, alpha=0.3)
    for s in ax.spines.values():
        s.set_color(SPINE)
    ax.tick_params(labelsize=16)
    ax.set_title("Streuungsdiagramm mit Regressionsgerade", fontsize=22)
    ax.set_xlabel("Preis (€)", fontsize=20)
    ax.set_ylabel("Absatzmenge", fontsize=20)
    ax.legend(fontsize=16, loc="upper right")
    _save(fig, "image_021")


def fig_image_022():
    """Folie 37: typische Muster im Residuenplot (a)–(d).

    Daten wie ursprünglich: np.random.seed(42), x = linspace(0, 10, 50),
    (a) N(0, 1), (b) 0,2·(x−5)² + N(0; 0,5), (c) N(0, 1)·x/3, (d) 2·sin(1,2x) + N(0; 0,3).
    Größe 3,75 × 2,59 in = Darstellung auf der Folie (Höhe 0,8\\textheight).
    """
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    res_a = np.random.normal(0, 1, 50)
    res_b = 0.2 * (x - 5) ** 2 + np.random.normal(0, 0.5, 50)
    res_c = np.random.normal(0, 1, 50) * x / 3
    res_d = 2 * np.sin(1.2 * x) + np.random.normal(0, 0.3, 50)
    panels = [("(a) Zufällig (korrekt)", res_a),
              ("(b) U-Form (falsches Modell)", res_b),
              ("(c) Trichterform (Heteroskedastizität)", res_c),
              ("(d) Wellenmuster (Autokorrelation)", res_d)]

    yticks = [[-2, -1, 0, 1, 2], [0, 2, 4], [-4, -2, 0, 2, 4], [-2, -1, 0, 1, 2]]
    fig = plt.figure(figsize=(3.75, 2.59), layout="constrained")
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, wspace=0.06, hspace=0.08)
    axes = fig.subplots(2, 2)
    for ax, (title, res), yt in zip(axes.flat, panels, yticks):
        ax.scatter(x, res, s=5, color=BLUE, alpha=0.7, linewidths=0, zorder=3)
        ax.axhline(0, color=RED, linestyle="--", linewidth=0.6, zorder=2)
        for s in ax.spines.values():
            s.set_color(SPINE)
            s.set_linewidth(0.6)
        ax.set_xticks([0, 2.5, 5, 7.5, 10])
        ax.set_yticks(yt)
        ax.tick_params(labelsize=6.5, length=2, width=0.6, pad=1.5)
        ax.set_title(title, fontsize=6.5, pad=3)
        ax.set_xlabel("Geschätzte Werte", fontsize=6.5, labelpad=1.5)
        ax.set_ylabel("Residuen", fontsize=6.5, labelpad=1.5)
    _save(fig, "image_022")


ALL = [fig_image_021, fig_image_022]


def main():
    for f in ALL:
        f()


if __name__ == "__main__":
    main()

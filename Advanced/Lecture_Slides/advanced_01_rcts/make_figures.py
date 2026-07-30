"""Generate the matplotlib figures for the Advanced Module A1 deck (RCTs).

All figures are computed from the bundled course datasets (Wage.csv) or from
clearly labelled simulations seeded with np.random.default_rng(2024); nothing
is sketched by hand. Run from anywhere:

    python "Advanced/Lecture_Slides/advanced_01_rcts/make_figures.py"

Output: Advanced/Lecture_Slides/advanced_01_rcts/images/cha1_*.png at 150 dpi,
matching the figure size and resolution used by the course decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"

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
    print("wrote", name)


# Wage.csv has no index column.
wage = pd.read_csv(DATA / "Wage.csv")


def training_population():
    """The simulated training-programme population used throughout the deck.

    1000 workers; low-skill workers are steered into training (p = 0.8 vs 0.2);
    the true effect of training is +4 on average (heterogeneous ITEs, sd 2).
    Same draw order as the slide computations: high, D, y0, tau.
    """
    rng = np.random.default_rng(2024)
    n = 1000
    high = rng.random(n) < 0.5
    p_treat = np.where(high, 0.2, 0.8)
    D = rng.random(n) < p_treat
    y0 = 40 + 20 * high + rng.normal(0, 5, n)
    tau = 4 + rng.normal(0, 2, n)
    y1 = y0 + tau
    return rng, high, D, y0, tau, y1


def fig_simpson():
    """Simpson-style confounding: naive comparison vs within-stratum comparisons."""
    _, high, D, y0, tau, y1 = training_population()
    y = np.where(D, y1, y0)

    groups = [
        ("All workers", np.ones_like(D, bool)),
        ("Low-skill", ~high),
        ("High-skill", high),
    ]
    fig, ax = plt.subplots(figsize=(7.6, 3.1))
    xpos = np.arange(3)
    w = 0.34
    for j, (label, mask) in enumerate(groups):
        mt = y[D & mask].mean()
        mc = y[~D & mask].mean()
        b1 = ax.bar(xpos[j] - w / 2, mt, w, color=ACCENT,
                    label="Trained" if j == 0 else None)
        b0 = ax.bar(xpos[j] + w / 2, mc, w, color=ORANGE,
                    label="Not trained" if j == 0 else None)
        for b, v in [(b1, mt), (b0, mc)]:
            ax.text(b[0].get_x() + b[0].get_width() / 2, v + 0.8, f"{v:.1f}",
                    ha="center", fontsize=8)
        diff = mt - mc
        ax.text(xpos[j], 72.5, f"diff = {diff:+.1f}", ha="center", fontsize=9,
                fontweight="bold", color=(GREEN if diff > 0 else "#B03A2E"))
    ax.set_xticks(xpos)
    ax.set_xticklabels([g[0] for g in groups])
    ax.set_ylabel("Mean wage ($1000s)")
    ax.set_ylim(0, 78)
    ax.set_title("Training looks harmful overall, helpful in every skill stratum "
                 "(simulated, true ATE $=+4.1$)")
    ax.legend(frameon=False, loc="upper left")
    save(fig, "cha1_simpson.png")


def fig_po_table():
    """God's-eye potential-outcomes table for 10 units; counterfactuals greyed."""
    rng = np.random.default_rng(2024)
    y0 = rng.integers(50, 80, 10).astype(float)
    tau = rng.integers(0, 9, 10).astype(float)
    y1 = y0 + tau
    D = np.zeros(10, bool)
    D[np.argsort(y0)[-5:]] = True   # 'selection': the five highest Y(0) get treated

    fig, ax = plt.subplots(figsize=(7.8, 3.4))
    ax.set_axis_off()
    cols = ["Unit $i$", "$Y_i(1)$", "$Y_i(0)$", r"$\tau_i$", "$D_i$", "$Y_i$ observed"]
    ncol = len(cols)
    for j, c in enumerate(cols):
        ax.text(j + 0.5, 10.6, c, ha="center", va="center", fontsize=10,
                fontweight="bold")
    for i in range(10):
        yrow = 9.5 - i
        obs1, obs0 = D[i], not D[i]
        vals = [f"{i + 1}", f"{y1[i]:.0f}", f"{y0[i]:.0f}", f"{tau[i]:+.0f}",
                f"{int(D[i])}", f"{(y1[i] if D[i] else y0[i]):.0f}"]
        shades = ["none",
                  ACCENT if obs1 else "0.92",
                  ORANGE if obs0 else "0.92",
                  "0.92", "none", "none"]
        for j in range(ncol):
            face = shades[j]
            if face == "none":
                fc, txtc, alpha = "white", "black", 1.0
            elif face == "0.92":
                fc, txtc, alpha = "0.93", "0.55", 1.0
            else:
                fc, txtc, alpha = face, "white", 0.85
            ax.add_patch(plt.Rectangle((j, yrow - 0.5), 1, 1, facecolor=fc,
                                       alpha=alpha, edgecolor="0.75", lw=0.6))
            style = "italic" if face == "0.92" else "normal"
            ax.text(j + 0.5, yrow, vals[j], ha="center", va="center",
                    fontsize=9, color=txtc, style=style)
    ax.set_xlim(0, ncol)
    ax.set_ylim(-1.4, 11.3)
    ax.text(ncol / 2, -0.6,
            "Grey italic cells are counterfactuals: never observed. "
            f"God's-eye ATE $= {tau.mean():.2f}$;  naive difference "
            f"$= {y1[D].mean():.1f} - {y0[~D].mean():.1f} = +{y1[D].mean() - y0[~D].mean():.1f}$ "
            "because treatment went to the five highest $Y_i(0)$.",
            ha="center", va="center", fontsize=8.5, color="0.25")
    ax.set_title("The fundamental problem: each unit reveals only one potential outcome")
    ax.grid(False)
    save(fig, "cha1_po_table.png")


def fig_sampling():
    """Sampling distribution of the difference in means: randomised vs self-selected."""
    n, reps = 1000, 2000
    rng = np.random.default_rng(2024)
    high = rng.random(n) < 0.5
    p = np.where(high, 0.2, 0.8)
    _ = rng.random(n) < p                      # the one observational draw (unused here)
    y0 = 40 + 20 * high + rng.normal(0, 5, n)
    tau = 4 + rng.normal(0, 2, n)
    y1 = y0 + tau
    est_r, est_s = [], []
    for _ in range(reps):
        perm = rng.permutation(n)
        Dr = np.zeros(n, bool)
        Dr[perm[:500]] = True
        yr = np.where(Dr, y1, y0)
        est_r.append(yr[Dr].mean() - yr[~Dr].mean())
        Ds = rng.random(n) < p
        ys = np.where(Ds, y1, y0)
        est_s.append(ys[Ds].mean() - ys[~Ds].mean())
    est_r, est_s = np.array(est_r), np.array(est_s)

    fig, ax = plt.subplots(figsize=(7.8, 3.0))
    bins = np.arange(-10.5, 7.5, 0.25)
    ax.hist(est_s, bins=bins, color=ORANGE, alpha=0.75,
            label=f"self-selected (mean {est_s.mean():.2f})")
    ax.hist(est_r, bins=bins, color=ACCENT, alpha=0.75,
            label=f"randomised (mean {est_r.mean():.2f}, sd {est_r.std():.2f})")
    ax.axvline(tau.mean(), color=GREEN, lw=1.8, ls="--",
               label=f"true SATE = {tau.mean():.2f}")
    ax.set_xlabel(r"difference in means  $\bar Y_1 - \bar Y_0$")
    ax.set_ylabel("count over 2000 replications")
    ax.set_title("Randomisation centres the estimator on the truth; "
                 "self-selection never does")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "cha1_sampling.png")
    print("   sampling: rand mean %.3f sd %.3f | sel mean %.3f sd %.3f | SATE %.3f"
          % (est_r.mean(), est_r.std(), est_s.mean(), est_s.std(), tau.mean()))


def fig_power():
    """Analytic power curve vs simulated power (resampling Wage wages), delta = 5."""
    sigma = wage.wage.std()
    delta = 5.0
    za = stats.norm.ppf(0.975)
    ns = np.arange(50, 2001, 10)
    analytic = (stats.norm.cdf(delta / (sigma * np.sqrt(2 / ns)) - za)
                + stats.norm.cdf(-delta / (sigma * np.sqrt(2 / ns)) - za))

    rng = np.random.default_rng(2024)
    w = wage.wage.values
    n_dots = np.arange(200, 2001, 200)
    sim = []
    for npa in n_dots:
        rej = 0
        for _ in range(1000):
            yc = rng.choice(w, npa)
            yt = rng.choice(w, npa) + delta
            se = np.sqrt(yt.var(ddof=1) / npa + yc.var(ddof=1) / npa)
            if abs((yt.mean() - yc.mean()) / se) > za:
                rej += 1
        sim.append(rej / 1000)

    n80 = 2 * (za + stats.norm.ppf(0.80)) ** 2 * sigma ** 2 / delta ** 2
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.plot(ns, analytic, color=ACCENT, lw=1.8, label="analytic power")
    ax.plot(n_dots, sim, "o", color=ORANGE, ms=4.5,
            label="simulated (1000 draws from Wage, effect +5)")
    ax.axhline(0.80, color=GREY, lw=1.0, ls=":")
    ax.axvline(n80, color=GREEN, lw=1.4, ls="--",
               label=f"80% power at n = {np.ceil(n80):.0f} per arm")
    ax.set_xlabel("n per arm")
    ax.set_ylabel("power (reject at $\\alpha=0.05$)")
    ax.set_ylim(0, 1.02)
    ax.set_title(r"Power to detect $\delta = 5$ against $\sigma = 41.7$ (Wage data)")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    save(fig, "cha1_power.png")
    print("   power dots:", dict(zip(n_dots.tolist(), sim)))


def fig_peeking():
    """False-positive rate of an A/A test when peeking after every 100 obs per arm."""
    rng = np.random.default_rng(2024)
    reps, looks, step = 4000, 20, 100
    rej_at = np.zeros(looks)
    for _ in range(reps):
        a = rng.normal(0, 1, looks * step)
        b = rng.normal(0, 1, looks * step)
        for k in range(1, looks + 1):
            na = k * step
            z = (a[:na].mean() - b[:na].mean()) / np.sqrt(2 / na)
            if abs(z) > 1.96:
                rej_at[k - 1] += 1
                break
    cum = np.cumsum(rej_at) / reps

    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ks = np.arange(1, looks + 1)
    ax.plot(ks, cum, "-o", color=ACCENT, ms=4)
    ax.axhline(0.05, color=GREEN, lw=1.4, ls="--", label="nominal $\\alpha = 0.05$")
    for k in (5, 10, 20):
        ax.annotate(f"{cum[k - 1]:.1%}", (k, cum[k - 1]),
                    textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=8, color=ORANGE, fontweight="bold")
    ax.set_xlabel("number of interim looks taken (every 100 obs per arm)")
    ax.set_ylabel("cumulative false-positive rate")
    ax.set_ylim(0, 0.30)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_title("A/A experiment (no true effect): stop-at-first-significant "
                 "inflates the Type I error")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    save(fig, "cha1_peeking.png")
    print("   peeking cum FPR: look1 %.3f look5 %.3f look10 %.3f look20 %.3f"
          % (cum[0], cum[4], cum[9], cum[19]))


def fig_balance():
    """Standardised mean differences for the Wage semi-synthetic experiment."""
    rng = np.random.default_rng(2024)
    D = rng.random(len(wage)) < 0.5
    covs = {"age": wage.age.values.astype(float),
            "year": wage.year.values.astype(float)}
    for lev in sorted(wage.education.unique()):
        covs[lev.replace(". ", ": ")] = (wage.education == lev).values.astype(float)
    names, smds = [], []
    for name, x in covs.items():
        sp = np.sqrt((x[D].var(ddof=1) + x[~D].var(ddof=1)) / 2)
        smds.append((x[D].mean() - x[~D].mean()) / sp)
        names.append(name)

    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ypos = np.arange(len(names))[::-1]
    ax.axvspan(-0.1, 0.1, color=GREEN, alpha=0.10)
    ax.axvline(0, color=GREY, lw=1.0)
    ax.axvline(-0.1, color=GREEN, lw=1.0, ls=":")
    ax.axvline(0.1, color=GREEN, lw=1.0, ls=":")
    ax.plot(smds, ypos, "o", color=ACCENT, ms=6)
    for y, s in zip(ypos, smds):
        ax.text(s + (0.012 if s >= 0 else -0.012), y, f"{s:+.3f}",
                va="center", ha="left" if s >= 0 else "right", fontsize=8)
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=8.5)
    ax.set_xlim(-0.16, 0.16)
    ax.set_xlabel("standardised mean difference (treated $-$ control)")
    ax.set_title("Balance check after coin-flip randomisation on Wage (n = 3000)")
    save(fig, "cha1_balance.png")
    print("   balance SMDs:", {n_: round(s, 3) for n_, s in zip(names, smds)})


if __name__ == "__main__":
    fig_simpson()
    fig_po_table()
    fig_sampling()
    fig_power()
    fig_peeking()
    fig_balance()

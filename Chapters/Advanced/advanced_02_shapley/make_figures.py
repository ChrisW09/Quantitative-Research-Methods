"""Generate the matplotlib figures for the Advanced module A2 deck (Shapley values).

All figures are computed from the bundled course datasets (or from clearly
labelled, seeded simulations); nothing is sketched by hand. The model is a
sklearn GradientBoostingRegressor fitted to log Salary on the Hitters data
(NA salaries dropped), and every Shapley value is computed from scratch ---
exact enumeration over all 2^6 coalitions with a marginal (interventional)
value function over a 100-row background sample. Run from anywhere:

    python "Advanced/advanced_02_shapley/make_figures.py"

Output: Advanced/advanced_02_shapley/images/a2_*.png at
150 dpi, matching the figure size and resolution used by the other decks.
"""

import itertools
from math import factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import permutation_importance

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


# ---------------------------------------------------------------------
# Model and exact Shapley machinery (identical to the deck's numbers)
# ---------------------------------------------------------------------
hitters = pd.read_csv(DATA / "Hitters.csv").dropna().reset_index(drop=True)
FEATS = ["Years", "CHits", "CRBI", "Walks", "Hits", "PutOuts"]
P = len(FEATS)
X = hitters[FEATS].to_numpy(dtype=float)
y = np.log(hitters["Salary"].to_numpy())
N = len(hitters)

gbr = GradientBoostingRegressor(random_state=2024).fit(X, y)

rng = np.random.default_rng(2024)
BG = X[rng.choice(N, size=100, replace=False)]  # background sample
B = len(BG)
BASE = gbr.predict(BG).mean()                   # v(emptyset) = E_b f(b)
PRED = gbr.predict(X)

I_STAR = 188          # the 24-season career-hits record holder (Pete Rose's 1986 line)
WEIGHT = {s: factorial(s) * factorial(P - s - 1) / factorial(P) for s in range(P)}


def coalition_values(Xv):
    """v_i(S) for every instance i and coalition S: dict tuple(S) -> (len(Xv),)."""
    m = len(Xv)
    vals = {}
    for r in range(P + 1):
        for S in itertools.combinations(range(P), r):
            Z = np.repeat(BG[None, :, :], m, axis=0)          # (m, B, P)
            if S:
                Z[:, :, S] = Xv[:, None, S]
            vals[S] = gbr.predict(Z.reshape(m * B, P)).reshape(m, B).mean(axis=1)
    return vals


def exact_shapley(Xv):
    """Exact Shapley matrix (len(Xv), P) by enumeration of all 2^P coalitions."""
    vals = coalition_values(Xv)
    phi = np.zeros((len(Xv), P))
    for j in range(P):
        others = [k for k in range(P) if k != j]
        for r in range(P):
            for S in itertools.combinations(others, r):
                Sj = tuple(sorted(S + (j,)))
                phi[:, j] += WEIGHT[len(S)] * (vals[Sj] - vals[S])
    return phi


print("computing exact Shapley values for all", N, "players ...")
PHI = exact_shapley(X)
resid = np.abs(PHI.sum(axis=1) - (PRED - BASE)).max()
print("efficiency residual (max over players):", resid)


def v_of(S, x):
    """Marginal value function for one instance: mean_b f(x_S, b_{-S})."""
    Z = BG.copy()
    if S:
        Z[:, list(S)] = x[list(S)]
    return gbr.predict(Z).mean()


def mc_shapley(x, m, rng_):
    """Monte-Carlo permutation-sampling estimate of the Shapley values."""
    est = np.zeros(P)
    for _ in range(m):
        perm = rng_.permutation(P)
        S, v_prev = [], BASE
        for j in perm:
            v_new = v_of(tuple(S) + (int(j),), x)
            est[j] += v_new - v_prev
            v_prev = v_new
            S.append(int(j))
    return est / m


# ---------------------------------------------------------------------
# Figure 1: Monte-Carlo convergence to the exact Shapley values
# ---------------------------------------------------------------------
def fig_convergence():
    exact = PHI[I_STAR]
    x_star = X[I_STAR]
    ms = [10, 25, 50, 100, 200, 400]
    rng_ = np.random.default_rng(2024)
    mean_err = []
    for m in ms:
        errs = [np.abs(mc_shapley(x_star, m, rng_) - exact).mean() for _ in range(10)]
        mean_err.append(np.mean(errs))
        print(f"  m={m:4d}  mean abs error = {mean_err[-1]:.4f}")

    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    ax.loglog(ms, mean_err, "o-", color=ACCENT, lw=1.6, ms=5,
              label="mean $|\\hat\\varphi_j - \\varphi_j|$ (10 repeats)")
    ref = mean_err[0] * np.sqrt(ms[0] / np.asarray(ms, float))
    ax.loglog(ms, ref, "--", color=GREY, lw=1.2, label="$c/\\sqrt{m}$ reference")
    for m, e in zip(ms, mean_err):
        ax.annotate(f"{e:.4f}", (m, e), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7, color=ACCENT)
    ax.set_xlabel("number of sampled permutations $m$ (log scale)")
    ax.set_ylabel("mean abs. error (log)")
    ax.set_title("Permutation sampling converges to the exact Shapley values at rate $1/\\sqrt{m}$")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "a2_convergence.png")


# ---------------------------------------------------------------------
# Figure 2: local attribution (waterfall) for the veteran instance
# ---------------------------------------------------------------------
def fig_local_waterfall():
    phi = PHI[I_STAR]
    x_star = X[I_STAR]
    order = np.argsort(np.abs(phi))[::-1]        # biggest first, top of chart
    labels = [f"{FEATS[j]} = {x_star[j]:.0f}" for j in order]
    vals = phi[order]

    fig, ax = plt.subplots(figsize=(7.8, 3.1))
    lefts = BASE + np.concatenate(([0.0], np.cumsum(vals)[:-1]))
    ypos = np.arange(len(vals))[::-1]            # top-down
    colors = [ACCENT if v > 0 else ORANGE for v in vals]
    ax.barh(ypos, vals, left=lefts, color=colors, height=0.62)
    for yp, lf, v in zip(ypos, lefts, vals):
        if abs(v) > 0.09:
            ax.annotate(f"{v:+.3f}", (lf + v / 2, yp), ha="center", va="center",
                        fontsize=8, color="white", fontweight="bold")
        else:
            edge = lf + v if v < 0 else lf
            ax.annotate(f"{v:+.3f}", (edge, yp), ha="right", va="center",
                        fontsize=8, color="black", xytext=(-4, 0),
                        textcoords="offset points")
    ax.axvline(BASE, color=GREY, lw=1.0, ls="--")
    ax.axvline(PRED[I_STAR], color=GREEN, lw=1.0, ls="--")
    ax.set_xlim(5.53, 7.17)
    ax.set_ylim(-0.55, 6.45)
    ax.annotate(f"baseline $E[f]$ = {BASE:.3f}\n($\\approx$ \\$349k)",
                (BASE, 5.6), fontsize=8, color=GREY, ha="right",
                va="bottom", xytext=(-5, 0), textcoords="offset points")
    ax.annotate(f"$f(x)$ = {PRED[I_STAR]:.3f}\n($\\approx$ \\$743k)",
                (PRED[I_STAR], 5.6), fontsize=8, color=GREEN, ha="left",
                va="bottom", xytext=(5, 0), textcoords="offset points")
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("log salary")
    ax.set_title("Exact Shapley attributions for the 24-season veteran: "
                 "from baseline 5.854 to prediction 6.610")
    save(fig, "a2_local_waterfall.png")


# ---------------------------------------------------------------------
# Figure 3: global importance --- mean |phi| vs permutation importance
# ---------------------------------------------------------------------
def fig_global_importance():
    gimp = np.abs(PHI).mean(axis=0)
    perm = permutation_importance(gbr, X, y, n_repeats=20, random_state=2024)
    order = np.argsort(gimp)                      # ascending: biggest on top
    ypos = np.arange(P)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 2.9), sharey=True)
    axes[0].barh(ypos, gimp[order], color=ACCENT, height=0.6)
    axes[0].set_yticks(ypos)
    axes[0].set_yticklabels([FEATS[j] for j in order], fontsize=8)
    axes[0].set_xlabel("mean $|\\varphi_j|$ (log-salary units)")
    axes[0].set_title("Global Shapley importance")
    for yp, v in zip(ypos, gimp[order]):
        axes[0].annotate(f"{v:.3f}", (v, yp), xytext=(3, 0),
                         textcoords="offset points", va="center", fontsize=7.5)
    axes[1].barh(ypos, perm.importances_mean[order], color=ORANGE, height=0.6)
    axes[1].set_xlabel("permutation importance (drop in $R^2$)")
    axes[1].set_title("Permutation importance (Ch. 8 style)")
    for yp, v in zip(ypos, perm.importances_mean[order]):
        axes[1].annotate(f"{v:.3f}", (v, yp), xytext=(3, 0),
                         textcoords="offset points", va="center", fontsize=7.5)
    axes[1].set_xlim(0, perm.importances_mean.max() * 1.18)
    save(fig, "a2_global_importance.png")


# ---------------------------------------------------------------------
# Figure 4: dependence-style scatter --- phi_j against x_j
# ---------------------------------------------------------------------
def fig_dependence():
    chits, years = X[:, FEATS.index("CHits")], X[:, FEATS.index("Years")]
    phi_ch, phi_yr = PHI[:, FEATS.index("CHits")], PHI[:, FEATS.index("Years")]
    med_y, med_c = np.median(years), np.median(chits)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0))
    hi = years > med_y
    axes[0].scatter(chits[~hi], phi_ch[~hi], s=12, color=ACCENT, alpha=0.65,
                    label=f"Years $\\leq$ {med_y:.0f}")
    axes[0].scatter(chits[hi], phi_ch[hi], s=12, color=ORANGE, alpha=0.65,
                    label=f"Years $>$ {med_y:.0f}")
    axes[0].axhline(0, color=GREY, lw=0.8)
    axes[0].set_xlabel("CHits (career hits)")
    axes[0].set_ylabel("$\\varphi_{\\mathrm{CHits}}$")
    axes[0].set_title("Monotone: career hits always help")
    axes[0].legend(frameon=False, fontsize=7.5, loc="lower right")

    hi = chits > med_c
    axes[1].scatter(years[~hi], phi_yr[~hi], s=12, color=ACCENT, alpha=0.65,
                    label=f"CHits $\\leq$ {med_c:.0f}")
    axes[1].scatter(years[hi], phi_yr[hi], s=12, color=ORANGE, alpha=0.65,
                    label=f"CHits $>$ {med_c:.0f}")
    axes[1].axhline(0, color=GREY, lw=0.8)
    axes[1].set_xlabel("Years (seasons played)")
    axes[1].set_ylabel("$\\varphi_{\\mathrm{Years}}$")
    axes[1].set_title("Hump-shaped: seasons help, until they don't")
    axes[1].legend(frameon=False, fontsize=7.5, loc="lower left")
    save(fig, "a2_dependence.png")


# ---------------------------------------------------------------------
# Figure 5: why marginal sampling leaves the data manifold (simulation)
# ---------------------------------------------------------------------
def fig_offmanifold():
    """Seeded simulation: two features with correlation 0.95, as CHits/CRBI."""
    rng_ = np.random.default_rng(2024)
    cov = np.array([[1.0, 0.95], [0.95, 1.0]])
    Z = rng_.multivariate_normal([0, 0], cov, size=300)
    x_inst = np.array([2.0, 1.9])                 # instance being explained
    bg2 = Z[rng_.choice(300, 40, replace=False)]  # background draws
    mixed = np.column_stack([np.full(40, x_inst[0]), bg2[:, 1]])  # S = {1}

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.scatter(Z[:, 0], Z[:, 1], s=10, color=ACCENT, alpha=0.45,
               label="training data ($\\rho = 0.95$)")
    ax.scatter(mixed[:, 0], mixed[:, 1], marker="x", s=26, color=ORANGE,
               label="evaluation points for $v(\\{1\\})$: $(x_1, X_2^{(b)})$")
    ax.scatter(*x_inst, marker="*", s=150, color=GREEN, zorder=5,
               label="instance $x$ being explained")
    ax.set_xlabel("$x_1$ (e.g. CHits, standardised)")
    ax.set_ylabel("$x_2$ (e.g. CRBI, standardised)")
    ax.set_title("Marginal sampling asks the model about points the data never produces")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    save(fig, "a2_offmanifold.png")



def fig_orders():
    """Player A's marginal contribution in each of the 3! arrival orders of the
    consultancy game --- the histogram whose mean IS the Shapley value."""
    v = {frozenset(): 0, frozenset("A"): 120, frozenset("B"): 60, frozenset("C"): 0,
         frozenset("AB"): 270, frozenset("AC"): 150, frozenset("BC"): 90,
         frozenset("ABC"): 300}
    import itertools
    orders, contribs = [], []
    for perm in itertools.permutations("ABC"):
        before = frozenset(perm[:perm.index("A")])
        contribs.append(v[before | frozenset("A")] - v[before])
        orders.append("".join(perm))
    phi_A = sum(contribs) / len(contribs)

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.bar(range(6), contribs, color=ACCENT, width=0.62, zorder=3)
    ax.axhline(phi_A, color=ORANGE, lw=2, zorder=4)
    ax.text(5.42, phi_A + 6, rf"mean $= \varphi_A = {phi_A:.0f}$", color=ORANGE,
            fontsize=10, ha="right")
    for i, cv in enumerate(contribs):
        ax.text(i, cv + 5, str(cv), ha="center", fontsize=9, color=ACCENT)
    ax.set_xticks(range(6), orders)
    ax.set_xlabel("arrival order")
    ax.set_ylabel("A's marginal contribution (k\u20ac)")
    ax.set_ylim(0, 245)
    save(fig, "a2_orders.png")
    print("a2_orders: contribs", contribs, "mean", phi_A)


if __name__ == "__main__":
    fig_convergence()
    fig_local_waterfall()
    fig_global_importance()
    fig_dependence()
    fig_offmanifold()
    fig_orders()

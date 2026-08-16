"""Generate the matplotlib figures for the Advanced Module A10 deck
(Causal Inference from Observational Data).

All figures are computed from the bundled course datasets (Wage.csv) or from
clearly labelled simulations seeded with np.random.default_rng(2024); nothing
is sketched by hand. Run from anywhere:

    python "Advanced/advanced_10_causal_observational/make_figures.py"

Output: Advanced/advanced_10_causal_observational/images/cha10_*.png at
150 dpi, matching the figure size and resolution used by the course decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#C62828"
RNG = np.random.default_rng(2024)

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 9,
    "axes.titlesize": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def ols(X, y):
    """Least-squares coefficients with an intercept prepended."""
    X1 = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    return beta


# ------------------------------------------------------------------
# The module's running simulation: a job-training programme.
# Ability U confounds both take-up D and earnings Y. True effect = 1.0.
# ------------------------------------------------------------------
N = 2000
TRUE_EFFECT = 1.0
U = RNG.normal(0, 1, N)                       # unobserved-ish confounder (we observe a proxy)
X_prox = U + RNG.normal(0, 0.5, N)            # observed covariate: noisy measure of U
D = (0.9 * U + RNG.normal(0, 1, N) > 0).astype(int)
Y = 2.0 + TRUE_EFFECT * D + 1.5 * U + RNG.normal(0, 1, N)

naive = Y[D == 1].mean() - Y[D == 0].mean()
adj = ols(np.column_stack([D, X_prox]), Y)[1]
print(f"[sim] naive difference in means      = {naive:.2f}  (truth {TRUE_EFFECT})")
print(f"[sim] regression-adjusted (on proxy) = {adj:.2f}")


def fig_confounding():
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0))
    bins = np.linspace(Y.min(), Y.max(), 40)
    for ax, title in zip(axes, ["What we see", "Why we see it"]):
        ax.set_title(title)
    axes[0].hist(Y[D == 0], bins=bins, alpha=0.65, color=GREY, label="untrained")
    axes[0].hist(Y[D == 1], bins=bins, alpha=0.65, color=ACCENT, label="trained")
    axes[0].axvline(Y[D == 0].mean(), color="k", lw=1, ls=":")
    axes[0].axvline(Y[D == 1].mean(), color="k", lw=1, ls=":")
    axes[0].set_xlabel("earnings $Y$")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].text(0.02, 0.93, f"gap = {naive:.2f}\n(truth = {TRUE_EFFECT:.1f})",
                 transform=axes[0].transAxes, fontsize=8, va="top")
    axes[1].scatter(U[D == 0], Y[D == 0], s=4, alpha=0.35, color=GREY, label="untrained")
    axes[1].scatter(U[D == 1], Y[D == 1], s=4, alpha=0.35, color=ACCENT, label="trained")
    axes[1].set_xlabel("ability $U$ (confounder)")
    axes[1].set_ylabel("earnings $Y$")
    axes[1].legend(frameon=False, fontsize=8)
    save(fig, "cha10_confounding.png")


def fig_ovb():
    gammas = np.linspace(0, 2.5, 26)
    naive_coefs = []
    for g in gammas:
        Yg = 2.0 + TRUE_EFFECT * D + g * U + RNG.standard_normal(N) * 0.2
        naive_coefs.append(ols(D.reshape(-1, 1), Yg)[1])
    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    ax.plot(gammas, naive_coefs, color=ORANGE, lw=2, label="naive estimate")
    ax.axhline(TRUE_EFFECT, color=ACCENT, lw=1.5, ls="--", label="true effect (1.0)")
    ax.set_xlabel(r"confounder strength $\gamma$ (effect of $U$ on $Y$)")
    ax.set_ylabel("estimated effect of $D$")
    ax.legend(frameon=False, fontsize=8)
    slope = np.polyfit(gammas, naive_coefs, 1)[0]
    print(f"[ovb] bias grows linearly in gamma; fitted slope = {slope:.2f} "
          f"= delta from the auxiliary regression")
    save(fig, "cha10_ovb.png")


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def logistic_fit(X, y, iters=50):
    """Plain Newton-Raphson logistic regression (intercept included),
    with the linear predictor clipped so W never underflows."""
    X1 = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(X1.shape[1])
    for _ in range(iters):
        eta = np.clip(X1 @ b, -30, 30)
        p = sigmoid(eta)
        W = np.maximum(p * (1 - p), 1e-6)
        H = X1.T @ (X1 * W[:, None]) + 1e-9 * np.eye(X1.shape[1])
        step = np.linalg.solve(H, X1.T @ (y - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


b_ps = logistic_fit(X_prox.reshape(-1, 1), D)
ps = sigmoid(np.column_stack([np.ones(N), X_prox]) @ b_ps)


def fig_propensity():
    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    bins = np.linspace(0, 1, 32)
    ax.hist(ps[D == 1], bins=bins, alpha=0.6, color=ACCENT, label="trained")
    ax.hist(ps[D == 0], bins=bins, alpha=0.6, color=GREY, label="untrained")
    ax.set_xlabel(r"estimated propensity score $\hat e(x)$")
    ax.set_ylabel("count")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "cha10_propensity.png")


def smd(x, d):
    """Standardised mean difference between groups d==1 and d==0."""
    s = np.sqrt(0.5 * (x[d == 1].var(ddof=1) + x[d == 0].var(ddof=1)))
    return (x[d == 1].mean() - x[d == 0].mean()) / s


def match_indices():
    """1:1 nearest-neighbour matching on the propensity score, WITH
    replacement (the ATT estimator): every treated unit gets the closest
    control, and a good control may serve several treated units."""
    treated = np.where(D == 1)[0]
    controls = np.where(D == 0)[0]
    ctrl_ps = ps[controls]
    pairs = []
    for t in treated:
        j = int(np.argmin(np.abs(ctrl_ps - ps[t])))
        pairs.append((t, controls[j]))
    return pairs


PAIRS = match_indices()
t_idx = np.array([p[0] for p in PAIRS])
c_idx = np.array([p[1] for p in PAIRS])
match_est = (Y[t_idx] - Y[c_idx]).mean()
smd_before = smd(X_prox, D)
d_m = np.concatenate([np.ones(len(t_idx)), np.zeros(len(c_idx))]).astype(int)
x_m = np.concatenate([X_prox[t_idx], X_prox[c_idx]])
smd_after = smd(x_m, d_m)
print(f"[match] pairs = {len(PAIRS)}, estimate = {match_est:.2f}")
print(f"[match] SMD of proxy before = {smd_before:.2f}, after = {smd_after:.2f}")


def fig_balance():
    fig, ax = plt.subplots(figsize=(6.6, 2.4))
    labels = ["ability proxy $X$"]
    ax.scatter([abs(smd_before)], [0], color=ORANGE, s=60, label="before matching", zorder=3)
    ax.scatter([abs(smd_after)], [0], color=GREEN, s=60, label="after matching", zorder=3)
    ax.axvline(0.1, color=GREY, ls=":", lw=1)
    ax.text(0.1, 0.35, "0.1 rule of thumb", fontsize=8, color=GREY, ha="center")
    ax.set_yticks([0])
    ax.set_yticklabels(labels)
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlim(-0.02, max(abs(smd_before), 0.12) * 1.25)
    ax.set_xlabel("|standardised mean difference|")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    save(fig, "cha10_balance.png")


# ------------------------------------------------------------------
# Difference-in-differences: clean two-group, two-period simulation.
# ------------------------------------------------------------------
DID = dict(c0=20.0, c1=24.0, t0=22.0, t1=30.0)   # group means used on the slides
did_est = (DID["t1"] - DID["t0"]) - (DID["c1"] - DID["c0"])
print(f"[did] treated change {DID['t1']-DID['t0']:.0f}, control change "
      f"{DID['c1']-DID['c0']:.0f}, DiD = {did_est:.0f}")


def fig_did():
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.plot([0, 1], [DID["c0"], DID["c1"]], "-o", color=GREY, label="control")
    ax.plot([0, 1], [DID["t0"], DID["t1"]], "-o", color=ACCENT, label="treated")
    cf = DID["t0"] + (DID["c1"] - DID["c0"])
    ax.plot([0, 1], [DID["t0"], cf], "--o", color=ACCENT, alpha=0.45,
            label="treated counterfactual\n(parallel trends)")
    ax.annotate("", xy=(1, DID["t1"]), xytext=(1, cf),
                arrowprops=dict(arrowstyle="<->", color=RED))
    ax.text(1.02, (DID["t1"] + cf) / 2, f"DiD = {did_est:.0f}", color=RED, fontsize=9)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["before", "after"])
    ax.set_ylabel("outcome")
    ax.set_xlim(-0.15, 1.35)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "cha10_did.png")


# ------------------------------------------------------------------
# Instrumental variables: Z shifts D, U confounds D and Y.
# ------------------------------------------------------------------
RNG_IV = np.random.default_rng(7)             # own stream: stable numbers
N_IV = 5000
U_iv = RNG_IV.normal(0, 1, N_IV)
Z = RNG_IV.binomial(1, 0.5, N_IV)
D_iv = (0.9 * U_iv + 1.4 * Z + RNG_IV.normal(0, 1, N_IV) > 0.7).astype(int)
Y_iv = 2.0 + TRUE_EFFECT * D_iv + 1.5 * U_iv + RNG_IV.normal(0, 1, N_IV)
ols_iv = ols(D_iv.reshape(-1, 1), Y_iv)[1]
wald = (Y_iv[Z == 1].mean() - Y_iv[Z == 0].mean()) / \
       (D_iv[Z == 1].mean() - D_iv[Z == 0].mean())
first_stage = D_iv[Z == 1].mean() - D_iv[Z == 0].mean()
print(f"[iv] OLS = {ols_iv:.2f}, Wald/IV = {wald:.2f}, first stage = {first_stage:.2f}")


def fig_iv():
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    names = ["true effect", "naive OLS", "IV (Wald)"]
    vals = [TRUE_EFFECT, ols_iv, wald]
    cols = [ACCENT, ORANGE, GREEN]
    ax.bar(names, vals, color=cols, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
    ax.axhline(TRUE_EFFECT, color=ACCENT, lw=1, ls="--")
    ax.set_ylabel("estimated effect of $D$")
    ax.set_ylim(0, max(vals) * 1.25)
    save(fig, "cha10_iv.png")


def fig_wage():
    wage = pd.read_csv(DATA / "Wage.csv")
    edu = wage["education"].str.slice(0, 1).astype(int)
    college = (edu >= 4).astype(int)          # college grad or higher
    naive_gap = wage.loc[college == 1, "wage"].mean() - \
        wage.loc[college == 0, "wage"].mean()
    Xw = np.column_stack([college, wage["age"], wage["year"]])
    adj_gap = ols(Xw, wage["wage"].values)[1]
    print(f"[wage] naive college gap = {naive_gap:.1f}, "
          f"age/year-adjusted = {adj_gap:.1f}")
    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    means = wage.groupby("education")["wage"].mean()
    ax.bar(range(len(means)), means.values, color=ACCENT, width=0.6)
    ax.set_xticks(range(len(means)))
    ax.set_xticklabels([s.split(". ")[1].replace(" ", "\n") for s in means.index],
                       fontsize=7)
    ax.set_ylabel("mean wage (\\$1000s)")
    ax.set_title("Wage by education — an association, not (yet) an effect")
    save(fig, "cha10_wage_educ.png")


if __name__ == "__main__":
    fig_confounding()
    fig_ovb()
    fig_propensity()
    fig_balance()
    fig_did()
    fig_iv()
    fig_wage()

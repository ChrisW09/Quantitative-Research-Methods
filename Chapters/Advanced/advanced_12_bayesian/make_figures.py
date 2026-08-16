"""Generate the matplotlib figures for the Advanced Module A12 deck
(Bayesian Inference).

All figures are computed from the bundled course datasets (Advertising.csv,
Default.csv) or from clearly labelled simulations seeded with
np.random.default_rng(2024); nothing is sketched by hand. Run from anywhere:

    python "Advanced/advanced_12_bayesian/make_figures.py"

Output: Advanced/advanced_12_bayesian/images/cha12_*.png at 150 dpi,
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

ACCENT = "#26468C"
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


# ------------------------------------------------------------------
# 1. Beta-binomial updating: a conversion rate with true p = 0.3.
# ------------------------------------------------------------------
TRUE_P = 0.3
flips = RNG.binomial(1, TRUE_P, 200)
grid = np.linspace(0, 1, 400)


def fig_beta_update():
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    a0, b0 = 2, 2
    stages = [0, 10, 50, 200]
    colors = [GREY, ORANGE, GREEN, ACCENT]
    for n, c in zip(stages, colors):
        yheads = int(flips[:n].sum())
        a, b = a0 + yheads, b0 + n - yheads
        lab = (f"prior Beta({a0},{b0})" if n == 0
               else f"n={n}, y={yheads}: Beta({a},{b})")
        ax.plot(grid, stats.beta.pdf(grid, a, b), color=c, lw=1.8, label=lab)
        if n:
            print(f"[beta] n={n}: y={yheads}, posterior Beta({a},{b}), "
                  f"mean {a/(a+b):.3f}, 95% CrI "
                  f"[{stats.beta.ppf(0.025,a,b):.3f}, {stats.beta.ppf(0.975,a,b):.3f}]")
    ax.axvline(TRUE_P, color=RED, lw=1, ls=":")
    ax.text(TRUE_P + 0.008, ax.get_ylim()[1] * 0.9, "true $p$", color=RED, fontsize=8)
    ax.set_xlabel("$p$")
    ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "cha12_beta_update.png")


def fig_priors():
    n, yy = 20, 6
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.8), sharey=True)
    priors = [(1, 1, "flat Beta(1,1)"), (2, 2, "mild Beta(2,2)"),
              (30, 10, "confident Beta(30,10)")]
    for a0, b0, lab in priors:
        axes[0].plot(grid, stats.beta.pdf(grid, a0, b0), lw=1.6, label=lab)
        a, b = a0 + yy, b0 + n - yy
        axes[1].plot(grid, stats.beta.pdf(grid, a, b), lw=1.6,
                     label=f"posterior mean {a/(a+b):.2f}")
        print(f"[priors] {lab}: posterior Beta({a},{b}), mean {a/(a+b):.3f}")
    axes[0].set_title("three priors")
    axes[1].set_title(f"three posteriors after y={yy} of n={n}")
    for ax in axes:
        ax.set_xlabel("$p$")
        ax.legend(frameon=False, fontsize=7.5)
    axes[0].set_ylabel("density")
    save(fig, "cha12_priors.png")


# ------------------------------------------------------------------
# 2. Gaussian mean, known sigma: precision-weighted shrinkage.
# ------------------------------------------------------------------
def fig_gauss_shrink():
    mu0, tau = 100, 15          # prior belief about a mean (e.g. an IQ-like score)
    sigma = 20                  # known sd of one observation
    truth = 130
    xs = np.linspace(80, 150, 500)
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.plot(xs, stats.norm.pdf(xs, mu0, tau), color=GREY, lw=1.6,
            label=f"prior N({mu0}, {tau}$^2$)")
    for n, c in [(2, ORANGE), (10, GREEN), (50, ACCENT)]:
        xbar = truth + RNG.normal(0, sigma / np.sqrt(n))
        post_prec = 1 / tau**2 + n / sigma**2
        post_var = 1 / post_prec
        w = (n / sigma**2) / post_prec
        post_mean = w * xbar + (1 - w) * mu0
        ax.plot(xs, stats.norm.pdf(xs, post_mean, np.sqrt(post_var)), color=c,
                lw=1.6, label=f"n={n}: mean {post_mean:.1f}, weight on data {w:.2f}")
        print(f"[gauss] n={n}: xbar={xbar:.1f}, posterior mean {post_mean:.1f}, "
              f"sd {np.sqrt(post_var):.1f}, data weight {w:.2f}")
    ax.axvline(truth, color=RED, lw=1, ls=":")
    ax.set_xlabel(r"$\mu$")
    ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "cha12_gauss_shrink.png")


# ------------------------------------------------------------------
# 3. Metropolis from scratch: posterior of the mean TV budget effect?
#    Simpler: posterior of (mu, log sigma) for Advertising sales.
# ------------------------------------------------------------------
adv = pd.read_csv(DATA / "Advertising.csv", index_col=0)
sales = adv["sales"].to_numpy(float)
print(f"[adv] n = {len(sales)}, sales mean = {sales.mean():.2f}, "
      f"sd = {sales.std(ddof=1):.2f}")


def log_post_mu(mu, x, sigma, mu0=0.0, tau=100.0):
    """Log posterior of mu under N(mu0, tau^2) prior, known sigma."""
    return (-0.5 * np.sum((x - mu) ** 2) / sigma**2
            - 0.5 * (mu - mu0) ** 2 / tau**2)


def fig_metropolis():
    sigma = sales.std(ddof=1)
    B, step = 20000, 0.5
    chain = np.empty(B)
    cur = sales.mean() + 5          # deliberately bad start
    lp_cur = log_post_mu(cur, sales, sigma)
    acc = 0
    for i in range(B):
        prop = cur + RNG.normal(0, step)
        lp_prop = log_post_mu(prop, sales, sigma)
        if np.log(RNG.uniform()) < lp_prop - lp_cur:
            cur, lp_cur = prop, lp_prop
            acc += 1
        chain[i] = cur
    burn = 2000
    kept = chain[burn:]
    # analytic posterior for comparison (tau large => approx N(xbar, sigma^2/n))
    post_sd = sigma / np.sqrt(len(sales))
    print(f"[mcmc] acceptance = {acc/B:.2f}, posterior mean = {kept.mean():.2f} "
          f"(analytic {sales.mean():.2f}), sd = {kept.std(ddof=1):.3f} "
          f"(analytic {post_sd:.3f})")
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.8))
    axes[0].plot(chain[:1500], color=ACCENT, lw=0.6)
    axes[0].axhline(sales.mean(), color=RED, lw=1, ls=":")
    axes[0].set_xlabel("iteration")
    axes[0].set_ylabel(r"$\mu$")
    axes[0].set_title("trace: the walk finds the posterior")
    axes[1].hist(kept, bins=50, density=True, color=ACCENT, alpha=0.6)
    xs = np.linspace(kept.min(), kept.max(), 300)
    axes[1].plot(xs, stats.norm.pdf(xs, sales.mean(), post_sd), color=RED, lw=1.5,
                 label="analytic posterior")
    axes[1].set_xlabel(r"$\mu$")
    axes[1].set_title("histogram of kept draws")
    axes[1].legend(frameon=False, fontsize=8)
    save(fig, "cha12_metropolis.png")


# ------------------------------------------------------------------
# 4. Bayesian simple regression: sales ~ TV, conjugate with known sigma2.
# ------------------------------------------------------------------
def fig_bayes_reg():
    x = adv["TV"].to_numpy(float)
    yv = sales
    X = np.column_stack([np.ones(len(x)), x])
    bhat, res, *_ = np.linalg.lstsq(X, yv, rcond=None)
    s2 = np.sum((yv - X @ bhat) ** 2) / (len(x) - 2)
    tau2 = 10.0**2                                  # weak N(0, 10^2) prior
    prior_prec = np.eye(2) / tau2
    post_cov = np.linalg.inv(X.T @ X / s2 + prior_prec)
    post_mean = post_cov @ (X.T @ yv / s2)
    print(f"[reg] OLS slope = {bhat[1]:.4f}; posterior slope mean = "
          f"{post_mean[1]:.4f}, sd = {np.sqrt(post_cov[1,1]):.4f}")
    draws = RNG.multivariate_normal(post_mean, post_cov, 4000)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.9))
    xs = np.linspace(0, 300, 100)
    Xs = np.column_stack([np.ones(100), xs])
    lines = draws @ Xs.T
    lo, hi = np.percentile(lines, [2.5, 97.5], axis=0)
    axes[0].scatter(x, yv, s=5, alpha=0.35, color=GREY)
    axes[0].plot(xs, Xs @ post_mean, color=ACCENT, lw=1.6, label="posterior mean line")
    axes[0].fill_between(xs, lo, hi, color=ACCENT, alpha=0.25,
                         label="95% credible band")
    axes[0].set_xlabel("TV budget")
    axes[0].set_ylabel("sales")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].hist(draws[:, 1], bins=60, density=True, color=GREEN, alpha=0.65)
    axes[1].axvline(bhat[1], color=RED, lw=1.2, ls=":", label="OLS slope")
    axes[1].set_xlabel(r"slope $\beta_1$")
    axes[1].set_title("posterior of the slope")
    axes[1].legend(frameon=False, fontsize=8)
    save(fig, "cha12_bayes_reg.png")


# ------------------------------------------------------------------
# 5. Ridge = MAP with a Gaussian prior: the lambda <-> tau dictionary.
# ------------------------------------------------------------------
def fig_ridge_map():
    x = (adv["TV"] - adv["TV"].mean()).to_numpy() / adv["TV"].std()
    yv = (sales - sales.mean())
    n = len(x)
    s2 = 5.0                            # noise variance held fixed for the picture
    taus = np.logspace(-2.5, 1.2, 60)
    ols_slope = np.sum(x * yv) / np.sum(x * x)
    map_slopes = [np.sum(x * yv) / (np.sum(x * x) + s2 / t**2) for t in taus]
    lambdas = s2 / taus**2
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.semilogx(taus, map_slopes, color=ACCENT, lw=2,
                label=r"MAP slope under $\beta \sim N(0, \tau^2)$")
    ax.axhline(ols_slope, color=ORANGE, lw=1.4, ls="--",
               label=f"OLS slope ({ols_slope:.2f})")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel(r"prior sd $\tau$  (small $\tau$  =  large ridge $\lambda = \sigma^2/\tau^2$)")
    ax.set_ylabel("estimated slope")
    ax.legend(frameon=False, fontsize=8)
    print(f"[map] OLS slope (standardised) = {ols_slope:.2f}; "
          f"tau=0.1 -> lambda = {s2/0.01:.0f}, MAP slope = "
          f"{np.sum(x*yv)/(np.sum(x*x)+s2/0.01):.2f}")
    save(fig, "cha12_ridge_map.png")


# ------------------------------------------------------------------
# 6. Bayesian A/B test (ties to module A1): P(pB > pA | data).
# ------------------------------------------------------------------
def fig_ab():
    nA, yA, nB, yB = 1000, 50, 1000, 63
    postA = stats.beta(1 + yA, 1 + nA - yA)
    postB = stats.beta(1 + yB, 1 + nB - yB)
    draws = postB.rvs(200000, random_state=42) - postA.rvs(200000, random_state=43)
    p_better = (draws > 0).mean()
    print(f"[ab] A: {yA}/{nA}, B: {yB}/{nB}; P(pB > pA | data) = {p_better:.3f}")
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.8))
    ps = np.linspace(0.02, 0.10, 400)
    axes[0].plot(ps, postA.pdf(ps), color=GREY, lw=1.6, label=f"A: {yA}/{nA}")
    axes[0].plot(ps, postB.pdf(ps), color=ACCENT, lw=1.6, label=f"B: {yB}/{nB}")
    axes[0].set_xlabel("conversion rate")
    axes[0].set_ylabel("posterior density")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].hist(draws, bins=80, density=True, color=GREEN, alpha=0.65)
    axes[1].axvline(0, color=RED, lw=1.2)
    axes[1].set_xlabel(r"$p_B - p_A$")
    axes[1].set_title(f"P($p_B > p_A$ | data) = {p_better:.2f}")
    save(fig, "cha12_ab.png")


if __name__ == "__main__":
    fig_beta_update()
    fig_priors()
    fig_gauss_shrink()
    fig_metropolis()
    fig_bayes_reg()
    fig_ridge_map()
    fig_ab()

"""Generate the matplotlib figures for Advanced module A3 (Conformal Prediction).

All figures are computed from the bundled course datasets (Wage.csv) or from
clearly labelled simulations seeded with np.random.default_rng(2024); nothing
is sketched by hand. Run from anywhere:

    python "Advanced/advanced_03_conformal/make_figures.py"

Output: images/a3_*.png at 150 dpi, matching the figure size and resolution
used by the other decks.  matplotlib only -- seaborn is NOT installed.
"""

from math import ceil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#B03A3A"

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


ALPHA = 0.10


def conformal_k(n_cal, alpha=ALPHA):
    """Index k of the split-conformal quantile: ceil((n+1)(1-alpha))."""
    return ceil((n_cal + 1) * (1 - alpha))


def poly(x):
    return np.column_stack([x, x**2])


# ---------------------------------------------------------------------------
# Shared Wage split (seed 2024): 2000 train / 500 calibration / 500 test
# ---------------------------------------------------------------------------
wage = pd.read_csv(DATA / "Wage.csv")          # Wage.csv has no index column
x_all = wage["age"].to_numpy(dtype=float)
y_all = wage["wage"].to_numpy()

rng = np.random.default_rng(2024)
perm = rng.permutation(len(wage))
TR, CAL, TE = perm[:2000], perm[2000:2500], perm[2500:]

MODEL = LinearRegression().fit(poly(x_all[TR]), y_all[TR])
SCORES = np.abs(y_all[CAL] - MODEL.predict(poly(x_all[CAL])))
K = conformal_k(len(CAL))                       # 451
QHAT = np.sort(SCORES)[K - 1]                   # 56.14
RES_TE = np.abs(y_all[TE] - MODEL.predict(poly(x_all[TE])))
COVERED = RES_TE <= QHAT                        # test coverage 0.926


# 1 -- Calibration scores + the conformal band on Wage -----------------------
def fig_scores_band():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.3))

    ax1.hist(SCORES, bins=35, color=ACCENT, alpha=0.75,
             edgecolor="white", linewidth=0.4)
    ax1.axvline(QHAT, color=ORANGE, lw=2,
                label=rf"$\hat q$ = {QHAT:.1f} (score #{K} of {len(CAL)})")
    ax1.set_xlabel(r"calibration score  $s_i = |y_i - \hat f(x_i)|$")
    ax1.set_ylabel("count")
    ax1.set_title(f"Calibration scores on Wage (n = {len(CAL)})")
    ax1.legend(frameon=False, fontsize=8)

    grid = np.linspace(18, 80, 200)
    fhat = MODEL.predict(poly(grid))
    ax2.scatter(x_all[TE], y_all[TE], s=8, color=GREY, alpha=0.45,
                linewidths=0, label="test points (500)")
    ax2.plot(grid, fhat, color=ACCENT, lw=2, label=r"$\hat f(x)$ (quadratic)")
    ax2.fill_between(grid, fhat - QHAT, fhat + QHAT, color=ACCENT, alpha=0.18,
                     label=rf"$\hat f(x)\pm\hat q$: covers {COVERED.mean():.1%}")
    ax2.set_xlabel("age")
    ax2.set_ylabel("wage ($1000s)")
    ax2.set_title("Split-conformal 90% band on the test set")
    ax2.legend(frameon=False, fontsize=8, loc="upper right")

    save(fig, "a3_scores_band.png")


# 2 -- Coverage histogram over 200 repeated splits ---------------------------
def fig_coverage_hist():
    rng2 = np.random.default_rng(2024)
    covs = []
    for _ in range(200):
        p = rng2.permutation(len(wage))
        tr, ca, te = p[:2000], p[2000:2500], p[2500:]
        m = LinearRegression().fit(poly(x_all[tr]), y_all[tr])
        q = np.sort(np.abs(y_all[ca] - m.predict(poly(x_all[ca]))))[K - 1]
        covs.append((np.abs(y_all[te] - m.predict(poly(x_all[te]))) <= q).mean())
    covs = np.array(covs)

    fig, ax = plt.subplots(figsize=(7.6, 3.1))
    ax.hist(covs, bins=24, color=ACCENT, alpha=0.75,
            edgecolor="white", linewidth=0.4)
    ax.axvline(0.90, color=RED, lw=2, ls="--", label="nominal $1-\\alpha$ = 0.90")
    ax.axvline(covs.mean(), color=ORANGE, lw=2,
               label=f"mean over splits = {covs.mean():.3f}")
    ax.set_xlabel("empirical test coverage of one split (500 test points)")
    ax.set_ylabel("number of splits")
    ax.set_title("Wage: coverage of the split-conformal interval over 200 random splits "
                 r"($\alpha=0.1$)")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "a3_coverage_hist.png")
    print("  coverage over splits: mean=%.4f sd=%.4f min=%.3f max=%.3f"
          % (covs.mean(), covs.std(), covs.min(), covs.max()))


# 3 -- Marginal vs subgroup coverage on Wage ---------------------------------
def fig_subgroup():
    bands = [("age < 30", x_all[TE] < 30),
             ("30--59", (x_all[TE] >= 30) & (x_all[TE] < 60)),
             (r"age $\geq$ 60", x_all[TE] >= 60)]
    labels = [f"{name}\n(n = {m.sum()})" for name, m in bands] + \
             [f"all\n(n = {len(TE)})"]
    heights = [COVERED[m].mean() for _, m in bands] + [COVERED.mean()]

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    cols = [ACCENT, ACCENT, ACCENT, ORANGE]
    bars = ax.bar(labels, heights, color=cols, alpha=0.8, width=0.55)
    for b, h in zip(bars, heights):
        ax.text(b.get_x() + b.get_width() / 2, h + 0.012, f"{h:.3f}",
                ha="center", fontsize=8)
    ax.axhline(0.90, color=RED, lw=1.6, ls="--", label="nominal 0.90")
    ax.set_ylim(0.75, 1.03)
    ax.set_ylabel("empirical coverage")
    ax.set_title("Same interval, one split: coverage by age group vs overall (marginal)")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    save(fig, "a3_subgroup.png")


# 4 -- Constant-width vs locally weighted vs CQR on Wage ---------------------
def fig_cqr():
    X = x_all.reshape(-1, 1)

    # locally weighted: scale = fitted mean absolute residual (quadratic in age)
    mad = LinearRegression().fit(
        poly(x_all[TR]), np.abs(y_all[TR] - MODEL.predict(poly(x_all[TR]))))
    sig_cal = np.clip(mad.predict(poly(x_all[CAL])), 1e-6, None)
    q_lw = np.sort(SCORES / sig_cal)[K - 1]

    # CQR: gradient boosting at the 5% and 95% quantiles
    gb = dict(n_estimators=200, max_depth=2, learning_rate=0.05, random_state=0)
    lo = GradientBoostingRegressor(loss="quantile", alpha=0.05, **gb).fit(X[TR], y_all[TR])
    hi = GradientBoostingRegressor(loss="quantile", alpha=0.95, **gb).fit(X[TR], y_all[TR])
    s_cqr = np.maximum(lo.predict(X[CAL]) - y_all[CAL],
                       y_all[CAL] - hi.predict(X[CAL]))
    q_cqr = np.sort(s_cqr)[K - 1]

    Lc = lo.predict(X[TE]) - q_cqr
    Uc = hi.predict(X[TE]) + q_cqr
    cov_cqr = ((y_all[TE] >= Lc) & (y_all[TE] <= Uc)).mean()

    grid = np.linspace(18, 80, 200)
    G = grid.reshape(-1, 1)
    fhat = MODEL.predict(poly(grid))
    glo = lo.predict(G) - q_cqr
    ghi = hi.predict(G) + q_cqr
    gsig = np.clip(mad.predict(poly(grid)), 1e-6, None)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.3))

    ax1.scatter(x_all[TE], y_all[TE], s=7, color=GREY, alpha=0.4, linewidths=0)
    ax1.fill_between(grid, fhat - QHAT, fhat + QHAT, color=ACCENT, alpha=0.15,
                     label=rf"absolute residual ($\pm${QHAT:.1f})")
    ax1.plot(grid, glo, color=ORANGE, lw=1.8)
    ax1.plot(grid, ghi, color=ORANGE, lw=1.8, label=f"CQR (covers {cov_cqr:.1%})")
    ax1.set_xlabel("age")
    ax1.set_ylabel("wage ($1000s)")
    ax1.set_title("Two conformal 90% bands on Wage")
    ax1.legend(frameon=False, fontsize=8, loc="upper right")

    ax2.plot(grid, np.full_like(grid, 2 * QHAT), color=ACCENT, lw=2,
             label=f"absolute residual (width {2 * QHAT:.0f})")
    ax2.plot(grid, 2 * q_lw * gsig, color=GREEN, lw=2, label="locally weighted")
    ax2.plot(grid, ghi - glo, color=ORANGE, lw=2, label="CQR")
    ax2.set_xlabel("age")
    ax2.set_ylabel("interval width ($1000s)")
    ax2.set_title("Interval width as a function of age")
    ax2.set_ylim(0, 165)
    ax2.legend(frameon=False, fontsize=8, loc="lower right")

    save(fig, "a3_cqr.png")
    w_te = Uc - Lc
    for a, b in [(18, 30), (30, 60), (60, 81)]:
        m = (x_all[TE] >= a) & (x_all[TE] < b)
        print(f"  CQR width age [{a},{b}): {w_te[m].mean():.1f} (n={m.sum()})")
    print(f"  q_lw={q_lw:.3f} q_cqr={q_cqr:.2f} cov_cqr={cov_cqr:.3f}")


# 5 -- Heteroskedastic simulation: OLS PI vs conformal vs CQR ----------------
def fig_hetero():
    import statsmodels.api as sm

    rng3 = np.random.default_rng(2024)
    N = 4000
    xs = rng3.uniform(0, 10, N)
    ys = 1 + 2 * xs + xs * rng3.normal(0, 1, N)     # sd(y|x) = x
    tr, ca, te = np.arange(0, 2000), np.arange(2000, 3000), np.arange(3000, 4000)
    Xs = xs.reshape(-1, 1)
    k = conformal_k(len(ca))                        # 901 of 1000

    # OLS 90% prediction interval with the pooled residual variance
    ols = sm.OLS(ys[tr], sm.add_constant(xs[tr])).fit()
    half = stats.norm.ppf(0.95) * np.sqrt(ols.scale)
    pred = ols.params[0] + ols.params[1] * xs[te]
    cov_ols = np.abs(ys[te] - pred) <= half

    # split conformal, absolute residuals
    m = LinearRegression().fit(Xs[tr], ys[tr])
    q = np.sort(np.abs(ys[ca] - m.predict(Xs[ca])))[k - 1]
    cov_cp = np.abs(ys[te] - m.predict(Xs[te])) <= q

    # CQR
    gb = dict(n_estimators=200, max_depth=2, learning_rate=0.05, random_state=0)
    lo = GradientBoostingRegressor(loss="quantile", alpha=0.05, **gb).fit(Xs[tr], ys[tr])
    hi = GradientBoostingRegressor(loss="quantile", alpha=0.95, **gb).fit(Xs[tr], ys[tr])
    sc = np.maximum(lo.predict(Xs[ca]) - ys[ca], ys[ca] - hi.predict(Xs[ca]))
    qc = np.sort(sc)[k - 1]
    cov_cqr = (ys[te] >= lo.predict(Xs[te]) - qc) & (ys[te] <= hi.predict(Xs[te]) + qc)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.3))

    order = np.argsort(xs[te])
    xo = xs[te][order]
    ax1.scatter(xs[te], ys[te], s=6, color=GREY, alpha=0.35, linewidths=0)
    ax1.plot(xo, pred[order] - half, color=ACCENT, lw=1.8)
    ax1.plot(xo, pred[order] + half, color=ACCENT, lw=1.8,
             label=rf"OLS 90% PI ($\pm${half:.1f})")
    ax1.plot(xo, lo.predict(Xs[te])[order] - qc, color=ORANGE, lw=1.8)
    ax1.plot(xo, hi.predict(Xs[te])[order] + qc, color=ORANGE, lw=1.8, label="CQR")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title(r"Simulated data: $y = 1 + 2x + x\,\varepsilon$, "
                  r"$\varepsilon \sim \mathcal{N}(0,1)$")
    ax1.legend(frameon=False, fontsize=8, loc="upper left")

    edges = np.linspace(0, 10, 6)                   # five x-bins
    mids = 0.5 * (edges[:-1] + edges[1:])
    for cov, col, lab in [(cov_ols, ACCENT, "OLS 90% PI"),
                          (cov_cp, GREEN, "split conformal (abs. residual)"),
                          (cov_cqr, ORANGE, "CQR")]:
        binned = [cov[(xs[te] >= a) & (xs[te] < b)].mean()
                  for a, b in zip(edges[:-1], edges[1:])]
        ax2.plot(mids, binned, "o-", color=col, lw=1.8, ms=4,
                 label=f"{lab}: marginal {cov.mean():.3f}")
    ax2.axhline(0.90, color=RED, lw=1.4, ls="--")
    ax2.set_ylim(0.55, 1.03)
    ax2.set_xlabel("x (bin midpoint)")
    ax2.set_ylabel("coverage within bin")
    ax2.set_title("Conditional coverage by x-bin (nominal 0.90 dashed)")
    ax2.legend(frameon=False, fontsize=7.5, loc="lower left")

    save(fig, "a3_hetero.png")
    hi_bin = cov_ols[xs[te] > 8].mean()
    print(f"  OLS PI: marginal {cov_ols.mean():.3f}, x>8 bin {hi_bin:.3f}; "
          f"conformal marginal {cov_cp.mean():.3f}; CQR marginal {cov_cqr.mean():.3f}")


# 6 -- Three-class simulation: data + prediction-set sizes -------------------
def classification_setup():
    rng6 = np.random.default_rng(2024)
    n_per = 1000
    means = np.array([[0.0, 0.0], [2.2, 0.0], [1.1, 1.9]])
    Xc = np.vstack([rng6.normal(mu, 1.0, size=(n_per, 2)) for mu in means])
    yc = np.repeat([0, 1, 2], n_per)
    p = rng6.permutation(3 * n_per)
    Xc, yc = Xc[p], yc[p]
    tr, ca, te = np.arange(0, 1500), np.arange(1500, 2250), np.arange(2250, 3000)
    clf = LogisticRegression(max_iter=1000).fit(Xc[tr], yc[tr])
    p_cal = clf.predict_proba(Xc[ca])
    s_cal = 1 - p_cal[np.arange(len(ca)), yc[ca]]   # score: 1 - prob of true class
    return Xc, yc, tr, ca, te, clf, s_cal


def fig_three_class():
    Xc, yc, tr, ca, te, clf, s_cal = classification_setup()
    k = conformal_k(750)                            # 676
    q = np.sort(s_cal)[k - 1]
    p_te = clf.predict_proba(Xc[te])
    sets = p_te >= 1 - q
    cov = sets[np.arange(len(te)), yc[te]].mean()
    sizes = sets.sum(axis=1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.3))

    cols = [ACCENT, ORANGE, GREEN]
    for cl in range(3):
        m = yc[te] == cl
        ax1.scatter(Xc[te][m, 0], Xc[te][m, 1], s=8, color=cols[cl],
                    alpha=0.45, linewidths=0, label=f"class {cl}")
    ax1.set_xlabel(r"$x_1$")
    ax1.set_ylabel(r"$x_2$")
    ax1.set_title("Simulated 3-class problem (test set, 750 points)")
    ax1.legend(frameon=False, fontsize=8)

    fracs = [(sizes == s).mean() for s in range(4)]
    bars = ax2.bar([str(s) for s in range(4)], fracs, color=ACCENT,
                   alpha=0.8, width=0.55)
    for b, h in zip(bars, fracs):
        ax2.text(b.get_x() + b.get_width() / 2, h + 0.012, f"{h:.1%}",
                 ha="center", fontsize=8)
    ax2.set_xlabel("prediction-set size")
    ax2.set_ylabel("fraction of test points")
    ax2.set_ylim(0, 0.85)
    ax2.set_title(rf"Set sizes at $\alpha=0.1$: coverage {cov:.1%}, "
                  rf"average size {sizes.mean():.2f}")
    save(fig, "a3_three_class.png")
    print(f"  classification: qhat={q:.4f} cov={cov:.4f} "
          f"avg size={sizes.mean():.3f} sizes={fracs}")


# 7 -- Coverage vs average set size trade-off --------------------------------
def fig_tradeoff():
    Xc, yc, tr, ca, te, clf, s_cal = classification_setup()
    p_te = clf.predict_proba(Xc[te])
    alphas = [0.20, 0.15, 0.10, 0.05, 0.02, 0.01]
    covs, sizes = [], []
    for a in alphas:
        q = np.sort(s_cal)[conformal_k(750, a) - 1]
        st = p_te >= 1 - q
        covs.append(st[np.arange(len(te)), yc[te]].mean())
        sizes.append(st.sum(axis=1).mean())

    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.plot(covs, sizes, "o-", color=ACCENT, lw=2, ms=5)
    for a, c, s in zip(alphas, covs, sizes):
        ax.annotate(rf"$\alpha$={a}", (c, s), textcoords="offset points",
                    xytext=(6, -11 if a in (0.10, 0.02) else 6), fontsize=8)
    ax.set_xlabel("empirical coverage on the test set")
    ax.set_ylabel("average set size")
    ax.set_title("The price of certainty: coverage vs average prediction-set size")
    save(fig, "a3_tradeoff.png")
    print("  tradeoff:", [f"a={a}: cov={c:.3f} size={s:.2f}"
                          for a, c, s in zip(alphas, covs, sizes)])


if __name__ == "__main__":
    fig_scores_band()
    fig_coverage_hist()
    fig_subgroup()
    fig_cqr()
    fig_hetero()
    fig_three_class()
    fig_tradeoff()
    print("done; qhat =", round(QHAT, 2), "k =", K,
          "test coverage =", round(COVERED.mean(), 4))

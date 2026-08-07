"""
Figures for Advanced module A4 --- GLMs and Splines.

Every figure is computed from the bundled course datasets
("ALL CSV FILES - 2nd Edition": Bikeshare.csv, Wage.csv) or from a
clearly seeded simulation (np.random.default_rng(2024)).  matplotlib
only --- seaborn is NOT installed.

Run from the deck directory:
    python3 make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.interpolate import BSpline

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

# Apple's Accelerate BLAS raises spurious overflow/divide/invalid flags on
# matmuls whose operands and results are entirely finite, printing dozens of
# meaningless RuntimeWarnings per rebuild. Same guard as chapter_07.
np.seterr(all="ignore")

ACCENT = "#26468C"
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150,
    "font.size": 9, "axes.titlesize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ------------------------------------------------------------------
# Shared model fits on Bikeshare
# ------------------------------------------------------------------
bike = pd.read_csv(DATA / "Bikeshare.csv", index_col=0)
bike["hr"] = bike["hr"].astype(int)
FORM = "bikers ~ C(hr) + temp + workingday + C(weathersit)"
LM = smf.ols(FORM, data=bike).fit()
POIS = smf.glm(FORM, data=bike, family=sm.families.Poisson()).fit()


def fig_lm_vs_glm():
    """LM on counts: negative fitted values vs the Poisson GLM."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.1))

    # (a) histogram of LM fitted values, negative mass highlighted
    fv = LM.fittedvalues.values
    bins = np.linspace(fv.min(), fv.max(), 60)
    neg = fv < 0
    ax1.hist(fv[~neg], bins=bins, color=ACCENT, alpha=0.85)
    ax1.hist(fv[neg], bins=bins, color=ORANGE, alpha=0.95)
    ax1.axvline(0, color="black", lw=1)
    ax1.annotate(f"{neg.mean()*100:.1f}% of fitted\ncounts are $<0$",
                 xy=(-60, 250), fontsize=8.5, color=ORANGE, ha="center")
    ax1.set_xlabel("fitted bikers (linear model)")
    ax1.set_ylabel("hours")
    ax1.set_title("(a) Linear model fitted values, all 8 645 hours")

    # (b) predictions across the day for one cold rainy non-working day
    grid = pd.DataFrame({"hr": np.arange(24), "temp": 0.2, "workingday": 0,
                         "weathersit": "light rain/snow"})
    lm_p = LM.predict(grid)
    po_p = POIS.predict(grid)
    ax2.axhline(0, color="black", lw=1)
    ax2.plot(grid.hr, lm_p, color=ORANGE, lw=2, marker="o", ms=3.5,
             label="linear model")
    ax2.plot(grid.hr, po_p, color=ACCENT, lw=2, marker="o", ms=3.5,
             label="Poisson GLM")
    ax2.annotate("LM: $-105$ bikers at 4 a.m.", xy=(4, lm_p[4]),
                 xytext=(7.0, -95), fontsize=8.5, color=ORANGE,
                 arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax2.set_xlabel("hour of day")
    ax2.set_ylabel("predicted bikers")
    ax2.set_title("(b) Cold, light rain, non-working day (temp $=0.20$)")
    ax2.legend(frameon=False, loc="upper left", fontsize=8)
    ax2.set_xticks(range(0, 24, 4))
    save(fig, "adv04_lm_vs_glm.png")


def fig_varfun():
    """Variance functions of the three canonical exponential-family members."""
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.5))
    mu = np.linspace(0.001, 5, 200)
    axes[0].plot(mu, np.ones_like(mu), color=ACCENT, lw=2)
    axes[0].set_title(r"Gaussian: $V(\mu)=1$")
    axes[0].set_ylim(0, 5.2)
    mub = np.linspace(0, 1, 200)
    axes[1].plot(mub, mub * (1 - mub), color=ORANGE, lw=2)
    axes[1].set_title(r"Bernoulli: $V(\mu)=\mu(1-\mu)$")
    axes[2].plot(mu, mu, color=GREEN, lw=2)
    axes[2].set_title(r"Poisson: $V(\mu)=\mu$")
    for ax in axes:
        ax.set_xlabel(r"mean $\mu$")
    axes[0].set_ylabel(r"variance $V(\mu)\,a(\phi)$")
    save(fig, "adv04_varfun.png")


def fig_meanvar():
    """Observed cell mean vs cell variance on Bikeshare: overdispersion."""
    g = bike.groupby(["hr", "workingday", "weathersit"])["bikers"].agg(
        ["mean", "var", "count"])
    g = g[g["count"] >= 20].dropna()
    phi = POIS.pearson_chi2 / POIS.df_resid          # 30.90
    alpha = 0.3049                                   # NB MLE on same formula
    m = np.linspace(g["mean"].min(), g["mean"].max(), 300)

    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.scatter(g["mean"], g["var"], s=16, color=GREY, alpha=0.75,
               edgecolor="white", linewidth=0.4, label="cells (hr $\\times$ day type $\\times$ weather)")
    ax.plot(m, m, color=ACCENT, lw=2, label=r"Poisson: $\mathrm{Var}=\mu$")
    ax.plot(m, phi * m, color=ORANGE, lw=2,
            label=rf"quasi-Poisson: $\mathrm{{Var}}=\hat\varphi\,\mu$, $\hat\varphi={phi:.1f}$")
    ax.plot(m, m + alpha * m**2, color=GREEN, lw=2, ls="--",
            label=rf"neg. binomial: $\mathrm{{Var}}=\mu+\hat\alpha\mu^2$, $\hat\alpha={alpha:.2f}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"cell mean $\bar y$ (log scale)")
    ax.set_ylabel(r"cell variance $s^2$ (log scale)")
    ax.set_title("Bikeshare: within-cell variance vs mean, 119 cells with $n\\geq 20$")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "adv04_meanvar.png")


def bspline_design(x, xl, xr, nseg, deg=3):
    """P-spline design: equally spaced knots, cubic B-splines."""
    dx = (xr - xl) / nseg
    # linspace, not arange: an arange with a float step lands exactly on the
    # endpoint here, so one ULP either way adds or drops a knot and silently
    # changes K -- and with it every P-spline fit and GCV number in the deck.
    knots = np.linspace(xl - deg * dx, xr + deg * dx, nseg + 2 * deg + 1)
    K = len(knots) - deg - 1
    B = np.empty((len(x), K))
    for j in range(K):
        c = np.zeros(K); c[j] = 1.0
        B[:, j] = BSpline(knots, c, deg)(x)
    return B, knots, K


def fig_bspline_basis():
    """Cubic B-spline basis functions on the age range of Wage."""
    xg = np.linspace(18, 80, 500)
    B, knots, K = bspline_design(xg, 18, 80, nseg=10)   # K = 13 basis functions
    fig, ax = plt.subplots(figsize=(7.8, 2.9))
    for j in range(K):
        ax.plot(xg, B[:, j], color=ACCENT, lw=1.2, alpha=0.45)
    jstar = 6
    ax.plot(xg, B[:, jstar], color=ORANGE, lw=2.4,
            label=r"one basis function $B_7(x)$")
    inner = knots[(knots >= 18) & (knots <= 80)]
    ax.plot(inner, np.zeros_like(inner) - 0.03, marker="|", ms=8,
            color=GREY, lw=0, label="knots (equally spaced)")
    ax.set_xlabel("age")
    ax.set_ylabel(r"$B_j(x)$")
    ax.set_title(f"Cubic B-spline basis on age 18--80: {K} local, overlapping bumps")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_ylim(-0.08, 0.85)
    save(fig, "adv04_bspline_basis.png")


def fig_pspline_lambda():
    """Penalized-spline fits on Wage across lambda + the GCV curve."""
    wage = pd.read_csv(DATA / "Wage.csv")
    x = wage.age.values.astype(float)
    y = wage.wage.values
    B, knots, K = bspline_design(x, x.min(), x.max(), nseg=20)  # K = 23
    D = np.diff(np.eye(K), n=2, axis=0)
    S = D.T @ D

    def fit(lam):
        A = B.T @ B + lam * S
        beta = np.linalg.solve(A, B.T @ y)
        edf = np.trace(np.linalg.solve(A, B.T @ B))
        rss = np.sum((y - B @ beta) ** 2)
        gcv = len(y) * rss / (len(y) - edf) ** 2
        return beta, edf, gcv

    xg = np.linspace(x.min(), x.max(), 400)
    Bg, _, _ = bspline_design(xg, x.min(), x.max(), nseg=20)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.3),
                                   gridspec_kw={"width_ratios": [1.6, 1]})
    ax1.scatter(x, y, s=5, color=GREY, alpha=0.25, edgecolor="none")
    for lam, col, ls, lab in [
            (1e-4, ORANGE, "-", None),
            (261.0, ACCENT, "-", None),
            (1e7, GREEN, "--", None)]:
        beta, edf, _ = fit(lam)
        # edf is interpolated, not typed: it was unpacked here and then ignored
        # while the labels carried hand-copied numbers, one of which (6.3) had
        # already drifted from what this code computes (6.2).
        if lam == 1e-4:
            lab = rf"$\lambda=10^{{-4}}$, edf $={edf:.1f}$ (wiggly)"
        elif lam == 261.0:
            lab = rf"$\lambda_{{\rm GCV}}=261$, edf $={edf:.1f}$"
        else:
            lab = rf"$\lambda=10^{{7}}$, edf $={edf:.1f}$ (linear)"
        ax1.plot(xg, Bg @ beta, color=col, lw=2, ls=ls, label=lab)
    ax1.set_xlabel("age"); ax1.set_ylabel("wage (\\$1 000)")
    ax1.set_title("(a) Penalized-spline fits, Wage data ($n=3\\,000$)")
    ax1.legend(frameon=False, fontsize=8, loc="upper right")
    ax1.set_ylim(0, 340)

    lams = 10 ** np.linspace(-2, 8, 121)
    res = np.array([fit(l)[1:] for l in lams])       # edf, gcv
    ax2.plot(lams, res[:, 1], color=ACCENT, lw=2)
    i = int(np.argmin(res[:, 1]))
    ax2.scatter([lams[i]], [res[i, 1]], color=ORANGE, zorder=5, s=28)
    ax2.annotate(rf"$\lambda={lams[i]:.0f}$, edf$={res[i,0]:.1f}$",
                 xy=(lams[i], res[i, 1]), xytext=(2e2, 1615),
                 fontsize=8.5, color=ORANGE)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"$\lambda$ (log scale)"); ax2.set_ylabel("GCV score")
    ax2.set_title("(b) GCV chooses $\\lambda$")
    save(fig, "adv04_pspline_lambda.png")


def fig_gam_partial():
    """GAM partial effects on Bikeshare: smooth of hour and of temperature."""
    from statsmodels.gam.api import GLMGam, BSplines

    xs = bike[["hr", "temp"]].astype(float)
    bs = BSplines(xs, df=[12, 6], degree=[3, 3])
    Xpar = pd.DataFrame({
        "const": 1.0,
        "workingday": bike.workingday.astype(float),
        "w_cloudy": (bike.weathersit == "cloudy/misty").astype(float),
        "w_light": (bike.weathersit == "light rain/snow").astype(float),
        "w_heavy": (bike.weathersit == "heavy rain/snow").astype(float),
    })
    ALPHA = [0.319, 0.00423]        # from GLMGam.select_penweight()
    res = GLMGam(bike.bikers, exog=Xpar, smoother=bs,
                 family=sm.families.Poisson(), alpha=ALPHA).fit()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.2))
    for k, ax, var, ttl in [(0, ax1, "hr", "(a) Smooth of hour of day"),
                            (1, ax2, "temp", "(b) Smooth of temperature")]:
        vals, se = res.partial_values(k)
        xv = bike[var].values.astype(float)
        o = np.argsort(xv)
        xo, vo, so = xv[o], vals[o], se[o]
        ax.fill_between(xo, vo - 2 * so, vo + 2 * so, color=ACCENT, alpha=0.18,
                        edgecolor="none")
        ax.plot(xo, vo, color=ACCENT, lw=2)
        ax.set_title(ttl)
        ax.set_ylabel(r"partial effect on $\log \mu$")
    ax1.set_xlabel("hour of day"); ax1.set_xticks(range(0, 24, 4))
    ax1.annotate("trough 3 a.m.", xy=(3, 1.25), xytext=(5.2, 1.45),
                 fontsize=8.5, color=GREY,
                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax1.annotate("peaks 8 a.m., 5--6 p.m.", xy=(17.6, 4.75), xytext=(7.5, 4.85),
                 fontsize=8.5, color=GREY,
                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax2.set_xlabel("temp (normalised, 1 = 41$^{\\circ}$C)")
    ax2.annotate("flattens, then dips\nabove temp $\\approx 0.75$",
                 xy=(0.85, 4.05), xytext=(0.42, 3.2), fontsize=8.5, color=GREY,
                 arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    save(fig, "adv04_gam_partial.png")



def fig_rate_ratios():
    """The rate-ratio table, drawn: exp(beta) with 95% CIs for the Bikeshare
    Poisson fit. Same model as the deck's statsmodels slide, so the numbers
    match the table (temp 4.79, light rain 0.603, heavy rain 0.260, ...)."""
    import statsmodels.formula.api as smf
    import statsmodels.api as sm

    df = pd.read_csv(DATA / "Bikeshare.csv")
    df["weathersit"] = pd.Categorical(
        df["weathersit"], categories=["clear", "cloudy/misty", "light rain/snow",
                                      "heavy rain/snow"])
    df["hr"] = pd.Categorical(df["hr"])
    fit = smf.glm("bikers ~ hr + workingday + temp + weathersit",
                  data=df, family=sm.families.Poisson()).fit()

    rows = [("temp (full unit)", "temp"),
            ("workingday", "workingday"),
            ("cloudy/misty", "weathersit[T.cloudy/misty]"),
            ("light rain/snow", "weathersit[T.light rain/snow]"),
            ("heavy rain/snow", "weathersit[T.heavy rain/snow]"),
            ("hr = 8 (vs midnight)", "hr[T.8]"),
            ("hr = 17 (vs midnight)", "hr[T.17]"),
            ("hr = 4 (vs midnight)", "hr[T.4]")]
    labels = [r[0] for r in rows]
    est = np.array([fit.params[r[1]] for r in rows])
    se = np.array([fit.bse[r[1]] for r in rows])
    rr = np.exp(est); lo = np.exp(est - 1.96 * se); hi = np.exp(est + 1.96 * se)

    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    y = np.arange(len(rows))[::-1]
    ax.axvline(1.0, color=GREY, lw=1.1, ls="--", zorder=1)
    for yi, l, h, r, name in zip(y, lo, hi, rr, labels):
        flag = name == "heavy rain/snow"
        col = ORANGE if flag else ACCENT
        ax.plot([l, h], [yi, yi], color=col, lw=1.6, zorder=3)
        ax.plot(r, yi, "o", color=col, ms=6, mec="white", mew=0.8, zorder=4)
        txt = f"{r:.3f}" if abs(r - 1) < 0.1 else f"{r:.3g}"
        ax.annotate(txt, (r, yi), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=8, color=col)
    ax.annotate("one observation wide \u2014\nthe deck's warning, visible",
                xy=(np.exp(est[4] - 1.96 * se[4]), y[4]),
                xytext=(0.145, y[4] - 0.95), va="bottom",
                fontsize=8, color="#8A4513",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_yticks(y, labels, fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xticks([0.125, 0.25, 0.5, 1, 2, 4, 8],
                  ["0.125", "0.25", "0.5", "1", "2", "4", "8"])
    ax.set_xlabel(r"rate ratio $e^{\hat\beta}$ (log scale), with 95% CI")
    save(fig, "adv04_rate_ratios.png")
    print("adv04_rate_ratios:", {n: round(v, 3) for n, v in zip(labels, rr)})


if __name__ == "__main__":
    fig_lm_vs_glm()
    fig_varfun()
    fig_meanvar()
    fig_bspline_basis()
    fig_pspline_lambda()
    fig_gam_partial()
    print("all figures written to", OUT)
    fig_rate_ratios()

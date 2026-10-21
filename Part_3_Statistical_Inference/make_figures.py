#!/usr/bin/env python3
# =====================================================================
# make_figures.py
# Regenerates the figures of "Quantitative Research -- Part 3:
# Statistical Inference" (confidence intervals, hypothesis tests,
# p-values, one-sided tests, types of error) with the HSBI colour palette.
#
# Output: images/*.png  (referenced by Part_3_Statistical_Inference.tex)
#
# Requires: numpy, scipy, matplotlib
#   pip install numpy scipy matplotlib
#
# Each function reproduces one slide figure. (conditional_bars,
# observed_vs_expected and chi2_distribution belong to the former
# categorical-data section and are not used in this deck.)
# =====================================================================
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy import stats

# --------------------------------------------------------------------
# HSBI colour palette (matches the LaTeX \definecolor commands)
# --------------------------------------------------------------------
BLUE       = "#3333B2"   # hsbiblau
BLUE_DARK  = "#1C1C6E"   # hsbiblaudunkel
ORANGE     = "#E69F00"   # hsbiorange
GRAY       = "#9A9A9A"   # hsbigrau
RED        = "#C0392B"   # hsbirot
GREEN      = "#2E8B57"

CURVE      = BLUE_DARK   # outline colour for density curves
FILL_BLUE  = BLUE        # acceptance / confidence shading

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUTDIR, exist_ok=True)

DPI = 200

# white label background used to keep text readable on top of curves/lines
WBOX = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85)

# --------------------------------------------------------------------
# global style
# --------------------------------------------------------------------
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "font.size":         14,
    "axes.titlesize":    15,
    "axes.labelsize":    14,
    "axes.edgecolor":    "#444444",
    "axes.linewidth":    1.0,
    "axes.grid":         True,
    "grid.color":        "#CFCFCF",
    "grid.linewidth":    0.8,
    "grid.alpha":        0.7,
    "axes.axisbelow":    True,
    "xtick.color":       "#222222",
    "ytick.color":       "#222222",
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "savefig.facecolor": "white",
    "legend.framealpha": 0.95,
    "legend.edgecolor":  "#BBBBBB",
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", path)


# ====================================================================
# 1. mean_distribution.png   (was ki_normal.png)
#    Standard normal: central 95% confidence band, alpha/2 tails.
# ====================================================================
def fig_mean_distribution():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x)
    zc = 1.96
    ax.plot(x, y, color=CURVE, lw=2.6)
    # central confidence region
    xc = x[(x >= -zc) & (x <= zc)]
    ax.fill_between(xc, stats.norm.pdf(xc), color=FILL_BLUE, alpha=0.22)
    # tails
    xl = x[x <= -zc]; xr = x[x >= zc]
    ax.fill_between(xl, stats.norm.pdf(xl), color=ORANGE, alpha=0.85)
    ax.fill_between(xr, stats.norm.pdf(xr), color=ORANGE, alpha=0.85)
    ax.axvline(-zc, ls="--", color=CURVE, lw=1.4)
    ax.axvline(zc,  ls="--", color=CURVE, lw=1.4)

    ax.text(0, 0.15, r"$1-\alpha = 0.95$", ha="center", va="center",
            fontsize=17, fontweight="bold", color=BLUE_DARK)
    ax.text(-2.75, 0.085, r"$\alpha/2$" + "\n" + r"$= 0.025$",
            ha="center", va="center", fontsize=12.5, color="#B07A00")
    ax.text(2.75, 0.085, r"$\alpha/2$" + "\n" + r"$= 0.025$",
            ha="center", va="center", fontsize=12.5, color="#B07A00")

    ax.set_xticks([-zc, 0, zc])
    ax.set_xticklabels([r"$-z_{1-\alpha/2}$" + "\n" + r"$-1.96$", "0",
                        r"$z_{1-\alpha/2}$" + "\n" + r"$1.96$"])
    ax.set_ylim(0, 0.45)
    ax.set_xlim(-4, 4)
    ax.set_ylabel("Density")
    ax.set_xlabel(r"standardized deviation  $Z_n=(\bar{X}-\mu)/(\sigma/\sqrt{n})$")
    legend = [Patch(facecolor=FILL_BLUE, alpha=0.30, label=r"confidence region $1-\alpha$"),
              Patch(facecolor=ORANGE, alpha=0.85, label=r"error $\alpha/2$ each side")]
    ax.legend(handles=legend, loc="upper right", fontsize=12)
    style(ax)
    save(fig, "mean_distribution.png")


# ====================================================================
# 2. ci_20_simulation.png   (was ki_20_simulation.png)
# ====================================================================
def fig_ci_20_simulation():
    mu_true, sigma, n = 1000.0, 3.0, 9
    half = 1.96 * sigma / np.sqrt(n)
    seed, means, miss = None, None, None
    for s in range(5000):
        rng = np.random.default_rng(s)
        m = mu_true + rng.normal(0, sigma / np.sqrt(n), 20)
        ms = (m - half > mu_true) | (m + half < mu_true)
        if ms.sum() == 1 and m[ms][0] < mu_true:
            seed, means, miss = s, m, ms
            break
    if means is None:                      # fallback
        rng = np.random.default_rng(0)
        means = mu_true + rng.normal(0, sigma / np.sqrt(n), 20)
        miss = (means - half > mu_true) | (means + half < mu_true)

    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    for i, (m, bad) in enumerate(zip(means, miss), start=1):
        col = ORANGE if bad else BLUE
        ax.plot([m - half, m + half], [i, i], color=col, lw=3, solid_capstyle="round")
        ax.plot(m, i, "o", color=col, ms=5)
    ax.axvline(mu_true, color=RED, lw=2.2, label=r"true value $\mu=1000$")
    ax.set_xlabel("Fill quantity (ml)")
    ax.set_ylabel("Sample no.")
    ax.set_title(r"20 samples $\rightarrow$ 20 confidence intervals (95%)",
                 color=BLUE_DARK, fontweight="bold")
    n_cover = int((~miss).sum())
    ax.text(0.02, 0.96, f"{n_cover} of 20 contain " + r"$\mu$",
            transform=ax.transAxes, va="top", ha="left", fontsize=12.5,
            bbox=dict(boxstyle="round", fc="white", ec="#888888"))
    ax.legend(loc="lower right", fontsize=12)
    style(ax)
    save(fig, "ci_20_simulation.png")


# ====================================================================
# 3. ci_length.png   (was ki_laenge.png)
# ====================================================================
def fig_ci_length():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    n = np.linspace(2, 60, 400)
    sigma = 3.0
    for z, c, lab in [(1.645, GRAY, "90%  (z = 1.645)"),
                      (1.96,  BLUE, "95%  (z = 1.96)"),
                      (2.576, ORANGE, "99%  (z = 2.576)")]:
        ax.plot(n, 2 * z * sigma / np.sqrt(n), color=c, lw=3, label=lab)
    ax.axvline(9, ls=":", color=BLUE_DARK, lw=1.6)
    ax.text(9.6, 6.0, "n = 9\n(milk)", color=BLUE_DARK, fontsize=12)
    ax.set_xlabel("Sample size n")
    ax.set_ylabel(r"Length of CI  $L = 2z\sigma/\sqrt{n}$")
    ax.set_xlim(0, 62)
    leg = ax.legend(title="Confidence level", fontsize=12, loc="upper right")
    leg.get_title().set_fontsize(12.5)
    style(ax)
    save(fig, "ci_length.png")


# ====================================================================
# 4. t_vs_normal.png
# ====================================================================
def fig_t_vs_normal():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    x = np.linspace(-4.3, 4.3, 1000)
    ax.plot(x, stats.norm.pdf(x), color=BLUE_DARK, lw=2.6, label=r"$N(0,1)$")
    ax.plot(x, stats.t.pdf(x, 8), color=ORANGE, lw=2.6, label=r"$t_8\ (n=9)$")
    ax.plot(x, stats.t.pdf(x, 2), color=BLUE, lw=2.2, ls="--", label=r"$t_2\ (n=3)$")
    ax.set_xlabel("t  or  z")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 0.43)
    ax.legend(loc="upper left", fontsize=12)
    # inset: heavier tails
    axin = ax.inset_axes([0.60, 0.42, 0.38, 0.50])
    xx = np.linspace(1.5, 3.6, 200)
    axin.plot(xx, stats.norm.pdf(xx), color=BLUE_DARK, lw=2)
    axin.plot(xx, stats.t.pdf(xx, 8), color=ORANGE, lw=2)
    axin.plot(xx, stats.t.pdf(xx, 2), color=BLUE, lw=1.8, ls="--")
    axin.set_title("heavier tails", fontsize=11, color="#666666")
    axin.grid(True, alpha=0.5)
    axin.tick_params(labelsize=9)
    style(ax)
    save(fig, "t_vs_normal.png")


# ====================================================================
# 5. ci_vs_fluctuation.png   (was ki_vs_fluktuation.png)
# ====================================================================
def fig_ci_vs_fluctuation():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    mu, sigma, n = 1000.0, 3.0, 9
    se = sigma / np.sqrt(n)
    x = np.linspace(mu - 12, mu + 12, 1000)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color=GRAY, lw=2.6,
            label=r"single values $X_i \sim N(\mu,\sigma^2)$")
    ax.fill_between(x, stats.norm.pdf(x, mu, sigma), color=GRAY, alpha=0.18)
    ax.plot(x, stats.norm.pdf(x, mu, se), color=BLUE, lw=2.8,
            label=r"mean $\bar{X} \sim N(\mu,\sigma^2/n)$")
    ax.fill_between(x, stats.norm.pdf(x, mu, se), color=BLUE, alpha=0.18)
    ax.axvline(mu, ls="--", color=BLUE_DARK, lw=1.3)

    yk = 0.075
    ax.annotate("", xy=(mu + 1.96 * se, yk), xytext=(mu - 1.96 * se, yk),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=2))
    ax.text(mu, yk + 0.012, "confidence interval (narrow)", color=BLUE,
            ha="center", fontsize=11.5, bbox=WBOX)
    yf = 0.05
    ax.annotate("", xy=(mu + 1.96 * sigma, yf), xytext=(mu - 1.96 * sigma, yf),
                arrowprops=dict(arrowstyle="<->", color="#6E6E6E", lw=2))
    ax.text(mu, yf - 0.016, "fluctuation interval (wide)", color="#5A5A5A",
            ha="center", fontsize=11.5, bbox=WBOX)

    ax.set_xlabel("Fill quantity (ml)")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 0.43)
    ax.legend(loc="upper right", fontsize=11.5)
    style(ax)
    save(fig, "ci_vs_fluctuation.png")


# ====================================================================
# 6. p_value_twosided.png   (was p_wert_zweiseitig.png)
# ====================================================================
def fig_p_value_twosided():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    x = np.linspace(-4, 4, 1000)
    ax.plot(x, stats.norm.pdf(x), color=CURVE, lw=2.6)
    zobs = 2.125
    xl = x[x <= -zobs]; xr = x[x >= zobs]
    ax.fill_between(xl, stats.norm.pdf(xl), color=ORANGE, alpha=0.85)
    ax.fill_between(xr, stats.norm.pdf(xr), color=ORANGE, alpha=0.85)
    ax.axvline(-zobs, ls="--", color=CURVE, lw=1.3)
    ax.axvline(zobs, ls="--", color=CURVE, lw=1.3)
    ax.text(-2.55, 0.055, "p/2", color="#B07A00", fontsize=14, ha="center")
    ax.text(2.55, 0.055, "p/2", color="#B07A00", fontsize=14, ha="center")
    ax.text(0, 0.13, "p-value = sum of\nboth tail areas", color=BLUE_DARK,
            ha="center", va="center", fontsize=13)
    ax.annotate("observed:\n" + r"$|Z_n| = 2.125$",
                xy=(zobs, 0.045), xytext=(3.05, 0.26),
                color=BLUE_DARK, fontsize=12, ha="center",
                arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.set_xlabel(r"$Z$ under $H_0$")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 0.42)
    ax.set_xlim(-4, 4)
    style(ax)
    save(fig, "p_value_twosided.png")


# ====================================================================
# 7. p_value_comparison.png   (was p_wert_vergleich.png) -- 2 panels
# ====================================================================
def fig_p_value_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(8.9, 4.21))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x)
    crit = 1.96

    # left: keep H0
    ax = axes[0]
    ax.plot(x, y, color=CURVE, lw=2.4)
    obs = 1.0
    xr = x[x >= obs]
    ax.fill_between(xr, stats.norm.pdf(xr), color=BLUE, alpha=0.30)
    for c in (-crit, crit):
        ax.axvline(c, ls="--", color=GRAY, lw=1.3)
    # reference alpha tails
    xa = x[x >= crit]; xb = x[x <= -crit]
    ax.fill_between(xa, stats.norm.pdf(xa), color=GRAY, alpha=0.25)
    ax.fill_between(xb, stats.norm.pdf(xb), color=GRAY, alpha=0.25)
    ax.axvline(obs, color=BLUE, lw=2.4)
    ax.text(crit + 0.1, 0.345, "crit. value", color="#777777", fontsize=11,
            bbox=WBOX)
    ax.annotate("p large\n(value not extreme)", xy=(obs, 0.25), xytext=(1.25, 0.26),
                color=BLUE, fontsize=11.5, ha="left", bbox=WBOX,
                arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.set_title(r"p > $\alpha$  $\rightarrow$  keep $H_0$", color=BLUE_DARK)
    ax.set_xlabel(r"$Z$"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.43); style(ax)

    # right: reject H0
    ax = axes[1]
    ax.plot(x, y, color=CURVE, lw=2.4)
    obs = 2.5
    xr = x[x >= obs]
    ax.fill_between(xr, stats.norm.pdf(xr), color=ORANGE, alpha=0.85)
    for c in (-crit, crit):
        ax.axvline(c, ls="--", color=GRAY, lw=1.3)
    xa = x[x >= crit]; xb = x[x <= -crit]
    ax.fill_between(xa, stats.norm.pdf(xa), color=GRAY, alpha=0.22)
    ax.fill_between(xb, stats.norm.pdf(xb), color=GRAY, alpha=0.22)
    ax.axvline(obs, color=ORANGE, lw=2.6)
    ax.text(crit - 0.1, 0.345, "crit. value", color="#777777", fontsize=11,
            ha="right", bbox=WBOX)
    ax.annotate("p small\n(value extreme)", xy=(obs, 0.02), xytext=(2.7, 0.27),
                color="#B07A00", fontsize=11.5, ha="left", bbox=WBOX,
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.set_title(r"p < $\alpha$  $\rightarrow$  reject $H_0$", color=BLUE_DARK)
    ax.set_xlabel(r"$Z$"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.43); style(ax)

    fig.tight_layout()
    save(fig, "p_value_comparison.png")


# ====================================================================
# 8. onesided_vs_twosided.png   (was einseitig_vs_zweiseitig.png)
# ====================================================================
def fig_onesided_vs_twosided():
    fig, axes = plt.subplots(1, 2, figsize=(8.9, 4.21))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x)

    ax = axes[0]
    ax.plot(x, y, color=CURVE, lw=2.4)
    zc = 1.96
    xc = x[(x >= -zc) & (x <= zc)]
    ax.fill_between(xc, stats.norm.pdf(xc), color=FILL_BLUE, alpha=0.20)
    xl = x[x <= -zc]; xr = x[x >= zc]
    ax.fill_between(xl, stats.norm.pdf(xl), color=ORANGE, alpha=0.85)
    ax.fill_between(xr, stats.norm.pdf(xr), color=ORANGE, alpha=0.85)
    ax.axvline(-zc, ls="--", color=CURVE, lw=1.2)
    ax.axvline(zc, ls="--", color=CURVE, lw=1.2)
    ax.text(zc, 0.012, "1.96", color=BLUE_DARK, fontsize=11, ha="center",
            va="bottom", bbox=WBOX)
    ax.text(-zc, 0.012, "-1.96", color=BLUE_DARK, fontsize=11, ha="center",
            va="bottom", bbox=WBOX)
    ax.text(-2.75, 0.05, "0.025", color="#B07A00", fontsize=12, ha="center")
    ax.text(2.75, 0.05, "0.025", color="#B07A00", fontsize=12, ha="center")
    ax.set_title(r"two-sided: $\alpha/2$ each side", color=BLUE_DARK)
    ax.set_xlabel(r"$Z$ under $H_0$"); ax.set_ylabel("Density"); ax.set_ylim(0, 0.43); style(ax)

    ax = axes[1]
    ax.plot(x, y, color=CURVE, lw=2.4)
    zc = -1.645
    xc = x[x >= zc]
    ax.fill_between(xc, stats.norm.pdf(xc), color=FILL_BLUE, alpha=0.20)
    xl = x[x <= zc]
    ax.fill_between(xl, stats.norm.pdf(xl), color=ORANGE, alpha=0.85)
    ax.axvline(zc, ls="--", color=CURVE, lw=1.2)
    ax.text(zc, 0.012, "-1.645", color=BLUE_DARK, fontsize=11, ha="center",
            va="bottom", bbox=WBOX)
    ax.text(-2.6, 0.05, "0.05", color="#B07A00", fontsize=12, ha="center")
    ax.set_title(r"one-sided (left): full $\alpha$", color=BLUE_DARK)
    ax.set_xlabel(r"$Z$ under $H_0$"); ax.set_ylabel("Density"); ax.set_ylim(0, 0.43); style(ax)

    fig.tight_layout()
    save(fig, "onesided_vs_twosided.png")


# ====================================================================
# 9. error_alpha_beta.png   (was fehler_alpha_beta.png)
# ====================================================================
def fig_error_alpha_beta():
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    x = np.linspace(-4.3, 6.7, 1200)
    mu0, mu1 = 0.0, 2.6
    crit = 1.645
    y0 = stats.norm.pdf(x, mu0)
    y1 = stats.norm.pdf(x, mu1)
    ax.plot(x, y0, color=BLUE_DARK, lw=2.6, label=r"$H_0$ true  ($\mu=\mu_0$)")
    ax.plot(x, y1, color=BLUE, lw=2.4, label=r"$H_1$ true  ($\mu=\mu_1$)")
    # beta: left of crit under H1 (lavender)
    xb = x[x <= crit]
    ax.fill_between(xb, stats.norm.pdf(xb, mu1), color=BLUE, alpha=0.28)
    # alpha: right tail under H0 (orange)
    xa = x[x >= crit]
    ax.fill_between(xa, stats.norm.pdf(xa, mu0), color=ORANGE, alpha=0.80)
    ax.axvline(crit, color=RED, lw=2.0)
    ax.text(crit, 0.43, "critical value", color=RED, fontsize=11.5, ha="center",
            va="bottom", bbox=WBOX)
    ax.annotate(r"$\beta$  (Type II error)", xy=(1.05, 0.07), xytext=(-2.55, 0.265),
                color=BLUE, fontsize=12.5, ha="center",
                arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.annotate(r"$\alpha$  (Type I error)", xy=(2.0, 0.02), xytext=(5.35, 0.20),
                color="#B07A00", fontsize=12.5, ha="center",
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.set_xlabel("Test statistic")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 0.46)
    ax.legend(loc="upper left", fontsize=11.5)
    style(ax)
    save(fig, "error_alpha_beta.png")


# ====================================================================
# 10. power_curve.png   (was power_kurve.png)
# ====================================================================
def fig_power_curve():
    # Power as a function of the standardized effect size d = |mu1-mu0|/SE.
    # Two-sided test at alpha = 0.05. Quadrupling n halves SE => doubles d.
    fig, ax = plt.subplots(figsize=(7.425, 4.21))
    alpha = 0.05
    z = stats.norm.ppf(1 - alpha / 2)
    d = np.linspace(-0.3, 4.2, 400)

    def power(eff):
        return 1 - (stats.norm.cdf(z - eff) - stats.norm.cdf(-z - eff))

    ax.plot(d, power(d),     color=BLUE,   lw=3, label="sample n")
    ax.plot(d, power(2 * d), color=ORANGE, lw=3, label=r"sample 4$\cdot$n")
    ax.axhline(0.80, ls="--", color=RED, lw=1.6)
    ax.text(2.55, 0.84, "target power 0.80", color=RED, fontsize=11, bbox=WBOX)
    ax.axhline(alpha, ls=":", color=GRAY, lw=1.6)
    ax.text(0.85, 0.085, r"level $\alpha = 0.05$", color="#777777", fontsize=11,
            bbox=WBOX)
    ax.set_xlabel(r"true deviation  $|\mu_1-\mu_0|$  (in standard errors)")
    ax.set_ylabel(r"Power $1-\beta$")
    ax.set_ylim(0, 1.03)
    ax.set_xlim(-0.35, 4.3)
    leg = ax.legend(title="Power function", loc="lower right", fontsize=12)
    leg.get_title().set_fontsize(12.5)
    style(ax)
    save(fig, "power_curve.png")


# ====================================================================
# 11. conditional_bars.png   (was bedingte_balken.png)
#     f(V|m) = (0.40, 0.32, 0.28) ; f(V|f) = (0.24, 0.48, 0.28)
# ====================================================================
def fig_conditional_bars():
    fig, ax = plt.subplots(figsize=(7.0, 4.19))
    cats = ["1st attempt", "2nd attempt", "3rd attempt"]
    male = [0.40, 0.32, 0.28]
    female = [0.24, 0.48, 0.28]
    xpos = np.arange(3)
    w = 0.38
    ax.bar(xpos - w / 2, male, w, color=BLUE, label="male (m)")
    ax.bar(xpos + w / 2, female, w, color=ORANGE, label="female (f)")
    for xp, v in zip(xpos - w / 2, male):
        ax.text(xp, v + 0.01, f"{v:.2f}", ha="center", fontsize=10.5, color=BLUE_DARK)
    for xp, v in zip(xpos + w / 2, female):
        ax.text(xp, v + 0.01, f"{v:.2f}", ha="center", fontsize=10.5, color="#B07A00")
    ax.set_xticks(xpos)
    ax.set_xticklabels(cats)
    ax.set_ylabel("Relative frequency")
    ax.set_ylim(0, 0.58)
    ax.set_title("Conditional distribution of attempt given gender", color=BLUE_DARK)
    ax.legend(fontsize=12)
    style(ax)
    save(fig, "conditional_bars.png")


# ====================================================================
# 12. observed_vs_expected.png   (was beobachtet_vs_erwartet.png)
# ====================================================================
def fig_observed_vs_expected():
    fig, ax = plt.subplots(figsize=(7.43, 4.21))
    cells = ["m,1st", "m,2nd", "m,3rd", "f,1st", "f,2nd", "f,3rd"]
    obs = [10, 8, 7, 6, 12, 7]
    exp = [8, 10, 7, 8, 10, 7]
    xpos = np.arange(6)
    w = 0.40
    ax.bar(xpos - w / 2, obs, w, color=BLUE, label=r"observed $n_{ij}$")
    ax.bar(xpos + w / 2, exp, w, color=ORANGE, label=r"expected $\hat{n}_{ij}$")
    for xp, o, e in zip(xpos, obs, exp):
        delta = o - e
        if delta != 0:
            ax.text(xp, max(o, e) + 0.3, f"$\\Delta$={delta:+d}",
                    color=RED, fontsize=11, ha="center")
    ax.set_xticks(xpos)
    ax.set_xticklabels(cells)
    ax.set_ylabel("Frequency")
    ax.set_ylim(0, 14)
    ax.set_title("Observed vs. expected under independence", color=BLUE_DARK)
    ax.legend(fontsize=12, loc="upper right")
    style(ax)
    save(fig, "observed_vs_expected.png")


# ====================================================================
# 13. chi2_distribution.png   (was chi2_verteilung.png)
# ====================================================================
def fig_chi2_distribution():
    fig, ax = plt.subplots(figsize=(7.43, 4.21))
    x = np.linspace(0.01, 12, 1000)
    df = 2
    y = stats.chi2.pdf(x, df)
    ax.plot(x, y, color=CURVE, lw=2.6)
    crit = 5.991
    xr = x[x >= crit]
    ax.fill_between(xr, stats.chi2.pdf(xr, df), color=ORANGE, alpha=0.80)
    obs = 1.8
    ax.axvline(obs, color=BLUE, lw=2.4)
    ax.axvline(crit, color=RED, lw=2.0)
    ax.annotate("observed\n" + r"$\chi^2 = 1.8$", xy=(obs, 0.205),
                xytext=(3.0, 0.30), color=BLUE, fontsize=12, ha="center",
                arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.annotate("critical value\n" + r"$\chi^2_{0.95;2}=5.991$", xy=(crit, 0.03),
                xytext=(8.6, 0.20), color=RED, fontsize=12, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(8.4, 0.055, "rejection\nregion ($\\alpha$)", color="#B07A00",
            fontsize=11.5, ha="center")
    ax.set_xlabel(r"$\chi^2$  (df = 2)")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 0.5)
    ax.set_xlim(0, 14)
    style(ax)
    save(fig, "chi2_distribution.png")


# ====================================================================
# 14. critical_value_onesided.png  (teaching aid: left & right rejection regions)
#     SYMMETRIC t-distribution (df=12) -- never F-shaped.
# ====================================================================
def fig_critical_value_onesided():
    v = 12; xc = 1.7
    x = np.linspace(-4, 4, 1000)
    y = stats.t.pdf(x, v)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.35))

    # left-sided
    ax = axes[0]
    ax.plot(x, y, color=BLUE_DARK, lw=2.8)
    keep = x[x >= -xc]; ax.fill_between(keep, stats.t.pdf(keep, v), color=BLUE, alpha=0.18)
    rej = x[x <= -xc]; ax.fill_between(rej, stats.t.pdf(rej, v), color=ORANGE, alpha=0.85)
    ax.axvline(-xc, ls="--", color=RED, lw=2.0)
    ax.text(-xc, 0.012, r"$-t_{1-\alpha,\,n-1}$", color=RED, fontsize=12.5,
            ha="center", va="bottom", bbox=WBOX)
    ax.annotate("REJECT $H_0$\n(area $=\\alpha$)", xy=(-2.8, 0.008), xytext=(-2.95, 0.30),
                color="#B07A00", fontsize=12.5, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
    ax.text(0, 0.13, "KEEP $H_0$\n(area $=1-\\alpha$)", color=BLUE_DARK, fontsize=12,
            ha="center", va="center", fontweight="bold")
    ax.set_title(r"left-sided:  reject if $T_n < -t_{1-\alpha,\,n-1}$", color=BLUE_DARK, fontsize=13.5)
    ax.set_xlabel(r"$T_n$ under $H_0$  (symmetric $t$)"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.42); ax.set_xlim(-4, 4); style(ax)

    # right-sided
    ax = axes[1]
    ax.plot(x, y, color=BLUE_DARK, lw=2.8)
    keep = x[x <= xc]; ax.fill_between(keep, stats.t.pdf(keep, v), color=BLUE, alpha=0.18)
    rej = x[x >= xc]; ax.fill_between(rej, stats.t.pdf(rej, v), color=ORANGE, alpha=0.85)
    ax.axvline(xc, ls="--", color=RED, lw=2.0)
    ax.text(xc, 0.012, r"$t_{1-\alpha,\,n-1}$", color=RED, fontsize=12.5,
            ha="center", va="bottom", bbox=WBOX)
    ax.annotate("REJECT $H_0$\n(area $=\\alpha$)", xy=(2.8, 0.008), xytext=(2.95, 0.30),
                color="#B07A00", fontsize=12.5, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
    ax.text(0, 0.13, "KEEP $H_0$\n(area $=1-\\alpha$)", color=BLUE_DARK, fontsize=12,
            ha="center", va="center", fontweight="bold")
    ax.set_title(r"right-sided:  reject if $T_n > t_{1-\alpha,\,n-1}$", color=BLUE_DARK, fontsize=13.5)
    ax.set_xlabel(r"$T_n$ under $H_0$  (symmetric $t$)"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.42); ax.set_xlim(-4, 4); style(ax)

    fig.tight_layout()
    save(fig, "critical_value_onesided.png")


# ====================================================================
# 15. cv_pvalue_link.png  (critical value <-> p-value: nested tail areas)
# ====================================================================
def fig_cv_pvalue_link():
    x = np.linspace(-1, 4.2, 1000); zc = 1.645
    fig, axes = plt.subplots(1, 2, figsize=(9.7, 4.35))
    # reject: p-tail nested inside alpha-tail
    ax = axes[0]; zo = 2.45
    ax.plot(x, stats.norm.pdf(x), color=BLUE_DARK, lw=2.6)
    ra = x[x >= zc]; ax.fill_between(ra, stats.norm.pdf(ra), color=ORANGE, alpha=0.30)
    rp = x[x >= zo]; ax.fill_between(rp, stats.norm.pdf(rp), color=ORANGE, alpha=0.95)
    ax.axvline(zc, ls="--", color=RED, lw=2.0); ax.axvline(zo, ls="-", color=BLUE, lw=2.4)
    ax.text(zc - 0.06, 0.435, "critical value", color=RED, fontsize=10.5, ha="right", va="top")
    ax.text(zo + 0.06, 0.435, "observed", color=BLUE, fontsize=10.5, ha="left", va="top")
    ax.annotate(r"$\alpha$", xy=(1.95, 0.02), xytext=(1.5, 0.135), color="#9C7A00",
                fontsize=15, fontweight="bold", bbox=WBOX)
    ax.annotate(r"$p$", xy=(2.95, 0.006), xytext=(3.3, 0.10), color="#7A4F00",
                fontsize=15, fontweight="bold", bbox=WBOX,
                arrowprops=dict(arrowstyle="->", color="#7A4F00"))
    ax.set_title(r"reject: statistic past the bar $\Rightarrow p<\alpha$", color=BLUE_DARK, fontsize=12.5)
    ax.set_xlabel("test statistic"); ax.set_ylabel("Density"); ax.set_ylim(0, 0.48); ax.set_xlim(-1, 4.2); style(ax)
    # keep: alpha-tail nested inside p-tail
    ax = axes[1]; zo = 1.0
    ax.plot(x, stats.norm.pdf(x), color=BLUE_DARK, lw=2.6)
    rp = x[x >= zo]; ax.fill_between(rp, stats.norm.pdf(rp), color=ORANGE, alpha=0.30)
    ra = x[x >= zc]; ax.fill_between(ra, stats.norm.pdf(ra), color=ORANGE, alpha=0.95)
    ax.axvline(zc, ls="--", color=RED, lw=2.0); ax.axvline(zo, ls="-", color=BLUE, lw=2.4)
    ax.text(zo - 0.06, 0.435, "observed", color=BLUE, fontsize=10.5, ha="right", va="top")
    ax.text(zc + 0.06, 0.435, "critical value", color=RED, fontsize=10.5, ha="left", va="top")
    ax.annotate(r"$\alpha$", xy=(2.15, 0.012), xytext=(2.6, 0.11), color="#7A4F00",
                fontsize=15, fontweight="bold", bbox=WBOX,
                arrowprops=dict(arrowstyle="->", color="#7A4F00"))
    ax.annotate(r"$p$", xy=(1.35, 0.06), xytext=(1.15, 0.18), color="#9C7A00",
                fontsize=15, fontweight="bold", bbox=WBOX)
    ax.set_title(r"keep: statistic short of the bar $\Rightarrow p>\alpha$", color=BLUE_DARK, fontsize=12.5)
    ax.set_xlabel("test statistic"); ax.set_ylabel("Density"); ax.set_ylim(0, 0.48); ax.set_xlim(-1, 4.2); style(ax)
    fig.tight_layout(); save(fig, "cv_pvalue_link.png")


# ====================================================================
# 16. t_crit_convergence.png  (t critical value -> z as df grows)
# ====================================================================
def fig_t_crit_convergence():
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    dfs = np.arange(1, 41)
    ax.plot(dfs, stats.t.ppf(0.975, dfs), "o-", color=BLUE, lw=2.2, ms=4, label=r"$t_{0.975,\,df}$ (two-sided 95%)")
    ax.plot(dfs, stats.t.ppf(0.95, dfs), "s-", color=ORANGE, lw=2.2, ms=4, label=r"$t_{0.95,\,df}$ (one-sided 95%)")
    ax.axhline(1.96, ls="--", color=BLUE_DARK, lw=1.6); ax.axhline(1.645, ls="--", color="#9C7A00", lw=1.6)
    ax.text(40, 1.875, r"$z_{0.975}=1.96$", color=BLUE_DARK, fontsize=11,
            ha="right", va="top", bbox=WBOX)
    ax.text(40, 1.625, r"$z_{0.95}=1.645$", color="#9C7A00", fontsize=11,
            ha="right", va="top", bbox=WBOX)
    ax.set_xlabel(r"degrees of freedom  df $=n-1$"); ax.set_ylabel("critical value")
    ax.set_ylim(1.5, 4.4); ax.set_xlim(0, 41); ax.legend(loc="upper right", fontsize=11.5); style(ax)
    fig.tight_layout(); save(fig, "t_crit_convergence.png")


# ====================================================================
# 17. p_value_onesided.png  (one-sided p-value: ONE tail, in the H1 direction)
#     Left panel = cream example (T_n = -2.1086, df = 15, p = 0.026).
# ====================================================================
def fig_p_value_onesided():
    v = 15
    x = np.linspace(-4, 4, 1000)
    y = stats.t.pdf(x, v)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.35))

    # left-sided: p = area BELOW the observed statistic
    ax = axes[0]
    tobs = -2.1086
    ax.plot(x, y, color=BLUE_DARK, lw=2.8)
    tail = x[x <= tobs]
    ax.fill_between(tail, stats.t.pdf(tail, v), color=ORANGE, alpha=0.85)
    ax.axvline(tobs, color=BLUE, lw=2.4)
    ax.text(tobs + 0.15, 0.40, "observed\n" + r"$T_n=-2.11$", color=BLUE,
            fontsize=11.5, ha="left", va="bottom")
    ax.annotate(r"$p =$" + "\n" + r"$F_{t,15}(T_n)$" + "\n" + r"$= 0.026$",
                xy=(-2.6, 0.018), xytext=(-3.05, 0.17),
                color="#B07A00", fontsize=12.5, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
    ax.set_title(r"left-sided ($H_1:\mu<\mu_0$): area $\bf below$ $T_n$",
                 color=BLUE_DARK, fontsize=13)
    ax.set_xlabel(r"$T_n$ under $H_0$"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.48); ax.set_xlim(-4, 4); style(ax)

    # right-sided: p = area ABOVE the observed statistic
    ax = axes[1]
    tobs = 2.1086
    ax.plot(x, y, color=BLUE_DARK, lw=2.8)
    tail = x[x >= tobs]
    ax.fill_between(tail, stats.t.pdf(tail, v), color=ORANGE, alpha=0.85)
    ax.axvline(tobs, color=BLUE, lw=2.4)
    ax.text(tobs - 0.15, 0.40, "observed\n" + r"$T_n=+2.11$", color=BLUE,
            fontsize=11.5, ha="right", va="bottom")
    ax.annotate(r"$p = 1-$" + "\n" + r"$F_{t,15}(T_n)$" + "\n" + r"$= 0.026$",
                xy=(2.6, 0.018), xytext=(3.05, 0.17),
                color="#B07A00", fontsize=12.5, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
    ax.set_title(r"right-sided ($H_1:\mu>\mu_0$): area $\bf above$ $T_n$",
                 color=BLUE_DARK, fontsize=13)
    ax.set_xlabel(r"$T_n$ under $H_0$"); ax.set_ylabel("Density")
    ax.set_ylim(0, 0.48); ax.set_xlim(-4, 4); style(ax)

    fig.tight_layout()
    save(fig, "p_value_onesided.png")


# ====================================================================
# 18. test_milk_cream.png  (the two running examples in one picture:
#     milk keeps H0, cream rejects -- two-sided test, known sigma)
# ====================================================================
def fig_test_milk_cream():
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x)
    zc = 1.96
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.35))

    def base(ax):
        ax.plot(x, y, color=BLUE_DARK, lw=2.6)
        xc = x[(x >= -zc) & (x <= zc)]
        ax.fill_between(xc, stats.norm.pdf(xc), color=BLUE, alpha=0.16)
        for s in (-1, 1):
            tail = x[s * x >= zc]
            ax.fill_between(tail, stats.norm.pdf(tail), color=ORANGE, alpha=0.80)
            ax.axvline(s * zc, ls="--", color=RED, lw=1.8)
        ax.text(0, 0.06, "keep $H_0$", color=BLUE_DARK, fontsize=12,
                ha="center", fontweight="bold")
        ax.set_xticks([-zc, 0, zc])
        ax.set_xticklabels([r"$-1.96$", "0", r"$1.96$"])
        ax.set_xlabel(r"$Z_n$ under $H_0$"); ax.set_ylabel("Density")
        ax.set_ylim(0, 0.47); ax.set_xlim(-4, 4); style(ax)

    # milk: Zn = 1.00 -> keep
    ax = axes[0]; base(ax)
    ax.axvline(1.0, color=GREEN, lw=3)
    ax.annotate("milk:\n" + r"$Z_n = 1.00$", xy=(1.0, 0.30), xytext=(3.05, 0.385),
                color=GREEN, fontsize=12, ha="center", fontweight="bold", bbox=WBOX, zorder=5,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.set_title(r"milk: $|Z_n|<1.96$ $\rightarrow$ keep $H_0$",
                 color=BLUE_DARK, fontsize=13)

    # cream: Zn = -2.125 -> reject
    ax = axes[1]; base(ax)
    ax.axvline(-2.125, color=RED, lw=3)
    ax.annotate("cream:\n" + r"$Z_n =$" + "\n" + r"$-2.125$", xy=(-2.125, 0.20), xytext=(-3.15, 0.34),
                color=RED, fontsize=12, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax.set_title(r"cream: $|Z_n|>1.96$ $\rightarrow$ reject $H_0$",
                 color=BLUE_DARK, fontsize=13)

    fig.tight_layout()
    save(fig, "test_milk_cream.png")


# ====================================================================
def main():
    fig_mean_distribution()
    fig_ci_20_simulation()
    fig_ci_length()
    fig_t_vs_normal()
    fig_ci_vs_fluctuation()
    fig_p_value_twosided()
    fig_p_value_comparison()
    fig_onesided_vs_twosided()
    fig_error_alpha_beta()
    fig_power_curve()
    fig_conditional_bars()
    fig_observed_vs_expected()
    fig_chi2_distribution()
    fig_critical_value_onesided()
    fig_cv_pvalue_link()
    fig_t_crit_convergence()
    fig_p_value_onesided()
    fig_test_milk_cream()
    print("\nAll figures written to", OUTDIR)


if __name__ == "__main__":
    main()

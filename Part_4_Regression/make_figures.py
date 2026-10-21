#!/usr/bin/env python3
"""Computed figures for Part 4 (Regression) of the lecture "Quantitative Research".

Every number shown in a figure is computed here from the lecture data
(lamp example, ../data/Advertising.csv, ../data/Credit.csv); simulated
figures use a fixed seed. The colours are the HSBI palette of the shared
preamble. Run from anywhere:

    python3 make_figures.py

Output: images/reg_*.png. The images taken over from the original decks
(image_0xx_en.png, 3_3.pdf, 3_5.pdf) are not touched.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
DATA = os.path.join(HERE, "..", "data")

BLUE = "#3333B2"        # hsbiblau
BLUE_DARK = "#1C1C6E"   # hsbiblaudunkel
ORANGE = "#E69F00"      # hsbiorange
GRAY = "#9A9A9A"        # hsbigrau
RED = "#C0392B"         # hsbirot
GREEN = "#2E8B57"       # hsbigruen
POINT = "#1F4E79"       # point colour of the original regression figures

WBOX = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13, "axes.titlesize": 14,
    "axes.labelsize": 13, "axes.grid": True, "grid.color": "#CFCFCF",
    "grid.alpha": 0.7, "axes.axisbelow": True, "legend.framealpha": 0.95,
    "legend.edgecolor": "#BBBBBB", "figure.facecolor": "white",
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=170, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", name)


# --------------------------------------------------------------------------
# lamp example (running story of Part 4)
# --------------------------------------------------------------------------
price = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120], dtype=float)
qty = np.array([20, 17, 15, 9, 11, 8, 4, 4, 2], dtype=float)
lamp = pd.DataFrame({"price": price, "quantity": qty})
fit_lamp = smf.ols("quantity ~ price", lamp).fit()
b0, b1 = fit_lamp.params
sigma_hat = np.sqrt(fit_lamp.scale)
n = len(price)
sxx = np.sum((price - price.mean()) ** 2)
se_b1 = sigma_hat / np.sqrt(sxx)


def fig_sampling_lines():
    """Different samples -> different lines; sampling distribution of b1."""
    rng = np.random.default_rng(2026)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
    ax = axes[0]
    slopes = []
    for r in range(5000):
        y = b0 + b1 * price + rng.normal(0, sigma_hat, n)
        c1 = np.sum((price - price.mean()) * (y - y.mean())) / sxx
        c0 = y.mean() - c1 * price.mean()
        slopes.append(c1)
        if r < 25:
            xx = np.array([78, 122])
            ax.plot(xx, c0 + c1 * xx, color=GRAY, lw=1, alpha=0.75)
        if r == 0:
            ax.scatter(price, y, color=POINT, s=36, zorder=3, label="one simulated sample")
    xx = np.array([78, 122])
    ax.plot(xx, b0 + b1 * xx, color=RED, lw=2.6, label="population line (fixed)")
    ax.plot([], [], color=GRAY, lw=1, label="OLS lines of 25 samples")
    ax.set_xlabel("Price (Euro)")
    ax.set_ylabel("Sales quantity")
    ax.set_title("(a) Every sample gives its own line")
    ax.legend(loc="upper right", fontsize=10.5)
    style(ax)

    ax = axes[1]
    slopes = np.array(slopes)
    ax.hist(slopes, bins=45, density=True, color=BLUE, alpha=0.35, edgecolor="white")
    g = np.linspace(b1 - 4.2 * se_b1, b1 + 4.2 * se_b1, 300)
    ax.plot(g, stats.norm.pdf(g, b1, se_b1), color=BLUE_DARK, lw=2.2,
            label=r"$N\!\left(\beta_1,\ \mathrm{SE}(\hat\beta_1)^2\right)$")
    ax.axvline(b1, color=RED, lw=2)
    ax.annotate(r"true $\beta_1$", (b1, 0), xytext=(b1 + 0.045, 7.5), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED), fontsize=12)
    ax.annotate("", xy=(b1 - se_b1, 5.2), xytext=(b1, 5.2),
                arrowprops=dict(arrowstyle="<->", color=BLUE_DARK, lw=1.5))
    ax.text(b1 - se_b1 / 2, 5.7, r"SE$\,=0.040$", ha="center", fontsize=11, color=BLUE_DARK, bbox=WBOX)
    ax.set_xlabel(r"estimated slope $\hat\beta_1$ (5000 simulated samples)")
    ax.set_ylabel("Density")
    ax.set_title(r"(b) Sampling distribution of $\hat\beta_1$")
    ax.legend(loc="upper left", fontsize=10.5)
    style(ax)
    fig.tight_layout()
    save(fig, "reg_sampling_lines.png")


def fig_slope_tests():
    """t-test for the lamp slope: H0 beta1 = 0 and H0 beta1 = -0.5."""
    df = n - 2
    tc = stats.t.ppf(0.975, df)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.3))
    cases = [(fit_lamp.tvalues["price"], r"(a) $H_0:\beta_1=0$", (-12.5, 4.5)),
             ((b1 + 0.5) / se_b1, r"(b) $H_0:\beta_1=-0.5$", (-4.5, 4.5))]
    for ax, (tval, title, xl) in zip(axes, cases):
        g = np.linspace(xl[0], xl[1], 800)
        dens = stats.t.pdf(g, df)
        ax.plot(g, dens, color=BLUE_DARK, lw=2)
        ax.fill_between(g, dens, where=np.abs(g) <= tc, color=BLUE, alpha=0.22)
        ax.fill_between(g, dens, where=g <= -tc, color=ORANGE, alpha=0.8)
        ax.fill_between(g, dens, where=g >= tc, color=ORANGE, alpha=0.8)
        for v in (-tc, tc):
            ax.axvline(v, color=RED, lw=1.4, ls="--")
        ax.text(tc + 0.1, 0.33, r"$t_{0.975;7}=2.365$", fontsize=10.5, color=RED, bbox=WBOX)
        ax.axvline(tval, color=GREEN, lw=2.6)
        ax.text(tval + (0.25 if tval < 0 else 0.15), 0.25,
                r"$T=%.2f$" % tval, color=GREEN, fontsize=12.5, bbox=WBOX)
        ax.set_xlim(*xl)
        ax.set_ylim(0, 0.42)
        ax.set_xlabel(r"test statistic $T$ under $H_0$ ($t_7$-distribution)")
        ax.set_title(title)
        style(ax)
    axes[0].set_ylabel("Density")
    axes[0].text(-10.75, 0.37, "reject $H_0$", color=ORANGE, fontsize=12, fontweight="bold")
    axes[1].text(-4.3, 0.37, "keep $H_0$", color=BLUE_DARK, fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "reg_slope_tests.png")


def fig_lamp_ci_pi():
    grid = pd.DataFrame({"price": np.linspace(75, 125, 200)})
    pr = fit_lamp.get_prediction(grid).summary_frame(alpha=0.05)
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.fill_between(grid.price, pr.obs_ci_lower, pr.obs_ci_upper, color=ORANGE, alpha=0.22,
                    label="95% prediction interval (single store)")
    ax.fill_between(grid.price, pr.mean_ci_lower, pr.mean_ci_upper, color=BLUE, alpha=0.30,
                    label="95% confidence interval (mean sales)")
    ax.plot(grid.price, pr["mean"], color=RED, lw=2.4,
            label=r"$\hat y = 54.67 - 0.4467\,x$")
    ax.scatter(price, qty, color=POINT, s=55, zorder=3, label="observations")
    ax.axvline(price.mean(), color=GRAY, lw=1, ls=":")
    ax.text(price.mean() + 0.6, 22.3, r"$\bar x = 100$", color="#555555", fontsize=11)
    ax.set_xlabel("Price (Euro)")
    ax.set_ylabel("Sales quantity")
    ax.set_xlim(75, 125)
    ax.legend(loc="lower left", fontsize=10.5)
    ax.set_title("Lamp example: confidence band vs. prediction band")
    style(ax)
    save(fig, "reg_lamp_ci_pi.png")


# --------------------------------------------------------------------------
# Advertising data (multiple regression)
# --------------------------------------------------------------------------
ad = pd.read_csv(os.path.join(DATA, "Advertising.csv"), index_col=0)


def fig_ad_three():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2), sharey=True)
    for ax, var, col in zip(axes, ["TV", "radio", "newspaper"], [BLUE, ORANGE, GRAY]):
        f = smf.ols(f"sales ~ {var}", ad).fit()
        ax.scatter(ad[var], ad.sales, s=14, color=col, alpha=0.75, edgecolor="none")
        xx = np.linspace(ad[var].min(), ad[var].max(), 2)
        ax.plot(xx, f.params.iloc[0] + f.params.iloc[1] * xx, color=RED, lw=2.4)
        ax.set_xlabel(f"{var} budget (1000 \\$)")
        ax.set_title(r"slope $\hat\beta_1=%.4f$,  $r=%.2f$" % (f.params.iloc[1], np.corrcoef(ad[var], ad.sales)[0, 1]),
                     fontsize=12.5)
        style(ax)
    axes[0].set_ylabel("sales (1000 units)")
    fig.tight_layout()
    save(fig, "reg_ad_three_predictors.png")


def fig_ad_confounding():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.5))
    ax = axes[0]
    ax.scatter(ad.radio, ad.newspaper, s=16, color=BLUE, alpha=0.7, edgecolor="none")
    f = smf.ols("newspaper ~ radio", ad).fit()
    xx = np.array([0, 50])
    ax.plot(xx, f.params.iloc[0] + f.params.iloc[1] * xx, color=RED, lw=2.2)
    ax.set_xlabel("radio budget (1000 $)")
    ax.set_ylabel("newspaper budget (1000 $)")
    ax.set_title(r"(a) Budgets move together: $r(\mathrm{radio},\mathrm{newspaper})=%.2f$"
                 % np.corrcoef(ad.radio, ad.newspaper)[0, 1], fontsize=12.5)
    style(ax)

    ax = axes[1]
    simple = smf.ols("sales ~ newspaper", ad).fit()
    multi = smf.ols("sales ~ TV + radio + newspaper", ad).fit()
    est = [simple.params["newspaper"], multi.params["newspaper"]]
    ci = [simple.conf_int().loc["newspaper"].values, multi.conf_int().loc["newspaper"].values]
    labels = ["simple regression\nsales ~ newspaper", "multiple regression\nsales ~ TV + radio + newspaper"]
    for k, (e, c) in enumerate(zip(est, ci)):
        ax.errorbar(k, e, yerr=[[e - c[0]], [c[1] - e]], fmt="o", ms=9, capsize=8, lw=2.2,
                    color=[ORANGE, BLUE][k])
        ax.text(k + 0.08, e, r"$%.4f$" % e, va="center", fontsize=12, bbox=WBOX)
    ax.axhline(0, color=RED, lw=1.5, ls="--")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_xlim(-0.5, 1.6)
    ax.set_ylabel(r"newspaper slope with 95% CI")
    ax.set_title("(b) The newspaper effect disappears", fontsize=12.5)
    style(ax)
    fig.tight_layout()
    save(fig, "reg_ad_confounding.png")


def fig_f_distribution():
    d1, d2 = 3, 196
    fc = stats.f.ppf(0.95, d1, d2)
    g = np.linspace(0, 5, 600)
    dens = stats.f.pdf(g, d1, d2)
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    ax.plot(g, dens, color=BLUE_DARK, lw=2.2)
    ax.fill_between(g, dens, where=g <= fc, color=BLUE, alpha=0.22)
    ax.fill_between(g, dens, where=g >= fc, color=ORANGE, alpha=0.85)
    ax.axvline(fc, color=RED, ls="--", lw=1.5)
    ax.text(fc + 0.08, 0.55, r"$F_{0.95;\,3,\,196}=%.2f$" % fc, color=RED, fontsize=12, bbox=WBOX)
    ax.text(3.3, 0.18, r"rejection region ($\alpha=0.05$)", color="#A06A00", fontsize=11.5)
    ax.annotate(r"observed $F=570$" "\n" r"(far off the chart)", xy=(5, 0.02), xytext=(3.75, 0.36),
                fontsize=12, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 0.8)
    ax.set_xlabel(r"$F$ under $H_0$: $F_{3,196}$-distribution")
    ax.set_ylabel("Density")
    ax.set_title(r"$F$-test for $H_0:\beta_1=\beta_2=\beta_3=0$ (Advertising)")
    style(ax)
    save(fig, "reg_f_distribution.png")


def fig_ad_residuals():
    add = smf.ols("sales ~ TV + radio", ad).fit()
    inter = smf.ols("sales ~ TV * radio", ad).fit()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4), sharey=True)
    for ax, f, title in zip(axes, [add, inter],
                            ["(a) sales ~ TV + radio", "(b) sales ~ TV + radio + TV:radio"]):
        ax.scatter(f.fittedvalues, f.resid, s=16, color=POINT, alpha=0.75, edgecolor="none")
        ax.axhline(0, color=RED, ls="--", lw=1.5)
        order = np.argsort(f.fittedvalues.values)
        xs = f.fittedvalues.values[order]
        ys = f.resid.values[order]
        k = 25
        smooth = np.convolve(ys, np.ones(k) / k, mode="valid")
        ax.plot(xs[k // 2: k // 2 + len(smooth)], smooth, color=ORANGE, lw=2.6, label="moving average")
        ax.set_xlabel("fitted values")
        ax.set_title(title + r"   ($R^2=%.3f$)" % f.rsquared, fontsize=12.5)
        ax.legend(loc="lower right", fontsize=10.5)
        style(ax)
    axes[0].set_ylabel("residuals")
    fig.tight_layout()
    save(fig, "reg_ad_residuals.png")


def fig_ad_interaction():
    inter = smf.ols("sales ~ TV * radio", ad).fit()
    add = smf.ols("sales ~ TV + radio", ad).fit()
    tv = np.linspace(0, 300, 50)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.3), sharey=True)
    for ax, f, title in zip(axes, [add, inter], ["(a) without interaction: parallel lines",
                                                  "(b) with interaction: lines fan out"]):
        for r, col in zip([10, 40], [BLUE, ORANGE]):
            pred = f.predict(pd.DataFrame({"TV": tv, "radio": r}))
            ax.plot(tv, pred, color=col, lw=2.6, label=f"radio = {r}")
        ax.set_xlabel("TV budget (1000 $)")
        ax.set_title(title, fontsize=12.5)
        ax.legend(loc="upper left", fontsize=11)
        style(ax)
    axes[0].set_ylabel("predicted sales")
    fig.tight_layout()
    save(fig, "reg_ad_interaction.png")


# --------------------------------------------------------------------------
# Credit data (dummy variables, collinearity)
# --------------------------------------------------------------------------
cr = pd.read_csv(os.path.join(DATA, "Credit.csv"))


def fig_credit_dummy():
    f = smf.ols("Balance ~ Income + C(Student)", cr).fit()
    a, bi, bs = f.params["Intercept"], f.params["Income"], f.params["C(Student)[T.Yes]"]
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for lev, col, mk in [("No", BLUE, "o"), ("Yes", ORANGE, "^")]:
        d = cr[cr.Student == lev]
        ax.scatter(d.Income, d.Balance, s=18, color=col, alpha=0.6, marker=mk, edgecolor="none",
                   label=f"Student = {lev}")
    xx = np.array([0, 190])
    ax.plot(xx, a + bi * xx, color=BLUE_DARK, lw=2.6, label=r"non-students: $%.1f + %.2f\,x$" % (a, bi))
    ax.plot(xx, a + bs + bi * xx, color="#A06A00", lw=2.6,
            label=r"students: $(%.1f + %.1f) + %.2f\,x$" % (a, bs, bi))
    ax.annotate("", xy=(170, a + bs + bi * 170), xytext=(170, a + bi * 170),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text(173, a + bi * 170 + bs / 2, r"$\hat\beta_2=%.1f$" % bs, color=RED, fontsize=12, va="center")
    ax.set_xlabel("Income (1000 $)")
    ax.set_ylabel("Balance ($)")
    ax.set_xlim(0, 200)
    ax.legend(loc="upper left", fontsize=10.5)
    ax.set_title("Credit data: a dummy variable shifts the intercept")
    style(ax)
    save(fig, "reg_credit_dummy.png")


def fig_credit_collinearity():
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
    for ax, (xv, yv) in zip(axes, [("Limit", "Age"), ("Limit", "Rating")]):
        ax.scatter(cr[xv], cr[yv], s=16, color=BLUE, alpha=0.65, edgecolor="none")
        r = np.corrcoef(cr[xv], cr[yv])[0, 1]
        ax.set_xlabel(xv)
        ax.set_ylabel(yv)
        ax.set_title(r"$r(\mathrm{%s},\mathrm{%s})=%.3f$" % (xv, yv, r), fontsize=12.5)
        style(ax)
    axes[0].text(0.03, 0.93, "(a) no collinearity", transform=axes[0].transAxes, fontsize=12, color=GREEN)
    axes[1].text(0.03, 0.93, "(b) almost perfect collinearity", transform=axes[1].transAxes, fontsize=12, color=RED)
    fig.tight_layout()
    save(fig, "reg_credit_collinearity.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig_sampling_lines()
    fig_slope_tests()
    fig_lamp_ci_pi()
    fig_ad_three()
    fig_ad_confounding()
    fig_f_distribution()
    fig_ad_residuals()
    fig_ad_interaction()
    fig_credit_dummy()
    fig_credit_collinearity()

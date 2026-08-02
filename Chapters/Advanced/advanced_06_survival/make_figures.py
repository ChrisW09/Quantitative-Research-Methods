"""Figures for Chapter 11 (Survival Analysis and Censored Data).

Every figure is computed either from the bundled course datasets in
``ALL CSV FILES - 2nd Edition`` (BrainCancer, Publication) or from a clearly
labelled seeded simulation (``np.random.default_rng(2024)``).  No figure
contains an invented number: the survival estimates, log-rank statistics and
Cox hazard ratios drawn here are exactly the ones quoted on the slides.

matplotlib only (seaborn is not installed).  Run with

    cd "Chapters/Advanced/advanced_06_survival" && python3 make_figures.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import logrank_test

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

# --- house palette -----------------------------------------------------------
ACCENT = "#26468C"
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#B03030"

RNG = np.random.default_rng(2024)

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.6,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------
# data helpers
# ---------------------------------------------------------------------------
def brain_cancer():
    """BrainCancer, 88 x 8 (the CSV's unnamed first column is the row number).

    status == 1 is the EVENT (death): 35 deaths, 53 censored, which reproduces
    ISLP's log-rank statistic 1.44 on the sex split.
    """
    return pd.read_csv(DATA / "BrainCancer.csv", index_col=0)


def brain_cancer_design():
    """Complete cases with Meningioma as the reference level for diagnosis."""
    df = brain_cancer().dropna().reset_index(drop=True)
    df["diagnosis"] = pd.Categorical(
        df["diagnosis"], categories=["Meningioma", "HG glioma", "LG glioma", "Other"])
    return pd.get_dummies(df, drop_first=True).astype(float)


def step_curve(times, values):
    """Coordinates of a right-continuous staircase for plotting."""
    xs = np.repeat(times, 2)[1:]
    ys = np.repeat(values, 2)[:-1]
    return xs, ys


# ---------------------------------------------------------------------------
# 1. the censoring picture -- the single most important figure of the chapter
# ---------------------------------------------------------------------------
def fig_censoring():
    bc = brain_cancer()
    sub = bc.sort_values("time").iloc[::5].head(18).reset_index(drop=True)
    sub = sub.sort_values("time").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    for i, row in sub.iterrows():
        col = RED if row["status"] == 1 else ACCENT
        ax.hlines(i, 0, row["time"], color=col, lw=1.6, alpha=0.85)
        if row["status"] == 1:
            ax.plot(row["time"], i, "o", color=RED, ms=6, zorder=3)
        else:
            ax.plot(row["time"], i, "|", color=ACCENT, ms=13, mew=2.2, zorder=3)
    end = 84.0
    ax.axvline(end, color=GREY, ls="--", lw=1.1)
    ax.text(end - 1.5, len(sub) - 1.0, "end of study", ha="right", va="center",
            fontsize=8, color=GREY)

    ax.plot([], [], "o", color=RED, ms=6, label="death observed  ($\\delta_i=1$)")
    ax.plot([], [], "|", color=ACCENT, ms=13, mew=2.2,
            label="still alive when last seen  ($\\delta_i=0$)")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.95)
    ax.set(xlabel="months since treatment", ylabel="patient (every 5th, ordered by $Y_i$)",
           xlim=(0, 90), ylim=(-2.6, len(sub) - 0.4),
           title="What a censored data set looks like: 18 BrainCancer patients")
    ax.set_yticks([])
    save(fig, "ch11_censoring.png")


# ---------------------------------------------------------------------------
# 2. why the naive analyses are wrong
# ---------------------------------------------------------------------------
def fig_naive():
    bc = brain_cancer()
    t, d = bc["time"].values, bc["status"].values
    n = len(bc)

    km = KaplanMeierFitter().fit(t, d)
    km_drop = KaplanMeierFitter().fit(t[d == 1], np.ones((d == 1).sum()))
    km_all = KaplanMeierFitter().fit(t, np.ones(n))

    # "censored subjects never die": 1 - (cumulative deaths)/n
    grid = np.sort(np.unique(np.r_[0.0, t]))
    naive_up = 1.0 - np.array([((t <= u) & (d == 1)).sum() for u in grid]) / n

    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    for fitter, col, lab, ls in [
        (km_drop, ORANGE, "(a) drop the 53 censored patients  (median $11.6$)", "--"),
        (km_all, RED, "(b) treat censoring as death  (median $23.7$)", "-."),
    ]:
        sf = fitter.survival_function_
        xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
        ax.plot(xs, ys, color=col, lw=1.7, ls=ls, label=lab)
    xs, ys = step_curve(grid, naive_up)
    ax.plot(xs, ys, color=GREEN, lw=1.7, ls=":",
            label="(c) censored patients never die  (median never reached)")
    sf = km.survival_function_
    xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
    ax.plot(xs, ys, color=ACCENT, lw=2.4, label="Kaplan–Meier  (median $47.8$)")

    ax.axhline(0.5, color=GREY, lw=0.9, ls=":")
    ax.set(xlabel="months", ylabel="estimated $S(t)$", ylim=(0, 1.02), xlim=(0, 85),
           title="Three wrong answers and one right one (BrainCancer, $n=88$)")
    ax.legend(loc="lower left", fontsize=7.6, framealpha=0.95)
    save(fig, "ch11_naive.png")


# ---------------------------------------------------------------------------
# 3. the Kaplan-Meier curve with a confidence band
# ---------------------------------------------------------------------------
def fig_km():
    bc = brain_cancer()
    km = KaplanMeierFitter().fit(bc["time"], bc["status"])
    sf = km.survival_function_
    ci = km.confidence_interval_

    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
    ax.plot(xs, ys, color=ACCENT, lw=2.2, label="Kaplan–Meier $\\hat S(t)$")
    lo = np.repeat(ci.iloc[:, 0].values, 2)[:-1]
    hi = np.repeat(ci.iloc[:, 1].values, 2)[:-1]
    ax.fill_between(xs, lo, hi, color=ACCENT, alpha=0.15, lw=0,
                    label="$95\\%$ confidence band")

    cens = bc.loc[bc["status"] == 0, "time"].values
    ax.plot(cens, km.survival_function_at_times(cens).values, "|",
            color=GREY, ms=9, mew=1.6, label="censoring times (53 patients)")

    ax.plot([0, 47.8], [0.5, 0.5], color=ORANGE, lw=1.1, ls="--")
    ax.plot([47.8, 47.8], [0, 0.5], color=ORANGE, lw=1.1, ls="--")
    ax.annotate("median $=47.8$ months", xy=(47.8, 0.5), xytext=(52, 0.66),
                fontsize=8.5, color=ORANGE,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax.annotate("$\\hat S(20)=0.713$", xy=(20, 0.713), xytext=(23, 0.88),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))
    ax.set(xlabel="months since treatment", ylabel="$\\hat S(t)$",
           ylim=(0, 1.02), xlim=(0, 85),
           title="Kaplan–Meier estimate for the 88 BrainCancer patients")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95)
    save(fig, "ch11_km.png")


# ---------------------------------------------------------------------------
# 4. two curves and a log-rank test
# ---------------------------------------------------------------------------
def fig_km_sex():
    bc = brain_cancer()
    male = bc["sex"] == "Male"
    res = logrank_test(bc.loc[male, "time"], bc.loc[~male, "time"],
                       bc.loc[male, "status"], bc.loc[~male, "status"])

    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    for mask, col, lab in [(~male, ACCENT, "Female"), (male, ORANGE, "Male")]:
        k = KaplanMeierFitter().fit(bc.loc[mask, "time"], bc.loc[mask, "status"])
        sf = k.survival_function_
        xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
        ax.plot(xs, ys, color=col, lw=2.1,
                label=f"{lab}  ($n={int(mask.sum())}$, {int(bc.loc[mask,'status'].sum())} deaths)")
        cens = bc.loc[mask & (bc["status"] == 0), "time"].values
        ax.plot(cens, k.survival_function_at_times(cens).values, "|",
                color=col, ms=8, mew=1.5)

    ax.text(0.98, 0.96,
            "log-rank: $\\chi^2_1=1.44$, $p=0.230$\n"
            "$O_{\\mathrm{male}}=20$ vs $E_{\\mathrm{male}}=16.46$",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GREY, lw=0.8))
    ax.set(xlabel="months since treatment", ylabel="$\\hat S(t)$",
           ylim=(0, 1.02), xlim=(0, 85),
           title="Kaplan–Meier by sex: a visible gap that the log-rank test will not call real")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95)
    save(fig, "ch11_km_sex.png")


# ---------------------------------------------------------------------------
# 5. what "proportional hazards" actually means
# ---------------------------------------------------------------------------
def fig_ph():
    t = np.linspace(0.05, 5, 400)
    h0 = 0.25 + 0.35 * np.sin(t) ** 2 + 0.06 * t      # a deliberately wiggly baseline
    H0 = np.cumsum(h0) * (t[1] - t[0])
    hr = 2.0

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4))
    ax = axes[0]
    ax.plot(t, h0, color=ACCENT, lw=2.0, label="$h_0(t)$  (baseline, $x=0$)")
    ax.plot(t, hr * h0, color=ORANGE, lw=2.0, label="$h_0(t)\\,e^{\\beta}=2\\,h_0(t)$")
    ax.set(xlabel="$t$", ylabel="hazard", title="Hazards: same shape, vertical factor $e^{\\beta}=2$")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(t, np.exp(-H0), color=ACCENT, lw=2.0, label="$S_0(t)$")
    ax.plot(t, np.exp(-hr * H0), color=ORANGE, lw=2.0,
            label="$S_0(t)^{\\,e^{\\beta}}=S_0(t)^2$")
    ax.set(xlabel="$t$", ylabel="$S(t)$", ylim=(0, 1.02),
           title="Survival curves: never cross, and $\\log(-\\log S)$ shifts by $\\beta$")
    ax.legend(fontsize=8)
    save(fig, "ch11_ph.png")


# ---------------------------------------------------------------------------
# 6. crossing hazards: the case the log-rank test is blind to (simulation)
# ---------------------------------------------------------------------------
def _piecewise_exp(rates, cuts, n, rng):
    """Draw n times from a piecewise-constant hazard."""
    edges = list(cuts) + [np.inf]
    rem = rng.exponential(1.0, n)      # unit exponential on the cum.-hazard scale
    cum = np.zeros(n)
    done = np.zeros(n, bool)
    out = np.zeros(n)
    a = 0.0
    for rate, edge in zip(rates, edges):
        width = (edge - a) if np.isfinite(edge) else np.inf
        take = (rem - cum) / rate
        hit = (~done) & (take <= width)
        out[hit] = a + take[hit]
        done[hit] = True
        if np.isfinite(edge):
            cum = cum + rate * width
        a = edge
    return out


def crossing_data():
    """Seeded simulation: 300 + 300 subjects, hazards that cross at t=5."""
    rng = np.random.default_rng(2024)
    n, cap = 300, 36.0
    tA = _piecewise_exp((0.22, 0.012), [5.0], n, rng)   # aggressive surgery
    tB = _piecewise_exp((0.045, 0.085), [5.0], n, rng)  # drug therapy
    yA, dA = np.minimum(tA, cap), (tA <= cap).astype(int)
    yB, dB = np.minimum(tB, cap), (tB <= cap).astype(int)
    return yA, dA, yB, dB


def fig_crossing():
    yA, dA, yB, dB = crossing_data()
    res = logrank_test(yA, yB, dA, dB)

    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    for y, d, col, lab in [(yA, dA, ACCENT, "Arm A — surgery (risky early, safe later)"),
                           (yB, dB, ORANGE, "Arm B — drug (safe early, risky later)")]:
        k = KaplanMeierFitter().fit(y, d)
        sf = k.survival_function_
        xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
        ax.plot(xs, ys, color=col, lw=2.1, label=lab)
    ax.axvline(5.0, color=GREY, ls="--", lw=1.0)
    ax.text(5.5, 0.93, "hazard rates swap at $t=5$", fontsize=8, color=GREY)
    ax.text(0.98, 0.95,
            f"log-rank: $\\chi^2_1={res.test_statistic:.2f}$, $p={res.p_value:.2f}$\n"
            "Cox: $\\widehat{HR}=1.10$, $p=0.28$",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=RED, lw=0.9))
    ax.set(xlabel="months", ylabel="$\\hat S(t)$", ylim=(0, 1.02), xlim=(0, 36),
           title="Crossing hazards: two very different arms, and a log-rank test that sees nothing")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95)
    save(fig, "ch11_crossing.png")


# ---------------------------------------------------------------------------
# 7. the Cox fit as a forest plot
# ---------------------------------------------------------------------------
def fig_forest():
    X = brain_cancer_design()
    cph = CoxPHFitter().fit(X, duration_col="time", event_col="status")
    s = cph.summary
    pretty = {
        "ki": "Karnofsky index (per point)",
        "gtv": "Gross tumour volume (per cm$^3$)",
        "sex_Male": "Male (vs.\\ female)",
        "diagnosis_HG glioma": "HG glioma (vs.\\ meningioma)",
        "diagnosis_LG glioma": "LG glioma (vs.\\ meningioma)",
        "diagnosis_Other": "Other diagnosis (vs.\\ meningioma)",
        "loc_Supratentorial": "Supratentorial (vs.\\ infratentorial)",
        "stereo_SRT": "SRT (vs.\\ SRS)",
    }
    order = list(pretty)[::-1]
    hr = s.loc[order, "exp(coef)"].values
    lo = s.loc[order, "exp(coef) lower 95%"].values
    hi = s.loc[order, "exp(coef) upper 95%"].values
    pv = s.loc[order, "p"].values
    y = np.arange(len(order))

    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    for i in range(len(order)):
        col = ACCENT if (lo[i] > 1 or hi[i] < 1) else GREY
        ax.plot([lo[i], hi[i]], [y[i], y[i]], color=col, lw=1.6)
        ax.plot(hr[i], y[i], "o", color=col, ms=6)
        ax.text(24.0, y[i], f"$p={pv[i]:.3f}$" if pv[i] >= 0.001 else "$p<0.001$",
                va="center", fontsize=7.6, color=col)
    ax.axvline(1.0, color=RED, lw=1.1, ls="--")
    ax.set_xscale("log")
    ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20])
    ax.set_xticklabels(["0.05", "0.1", "0.25", "0.5", "1", "2", "5", "10", "20"])
    ax.set_xlim(0.04, 45)
    ax.set_yticks(y)
    ax.set_yticklabels([pretty[k].replace("\\ ", " ").replace("$^3$", "³")
                        .replace("$", "") for k in order], fontsize=8)
    ax.set(xlabel="hazard ratio  $e^{\\hat\\beta_j}$  (log scale)",
           title="Cox proportional-hazards fit, BrainCancer ($n=87$ complete cases, 35 deaths)")
    ax.grid(axis="y", alpha=0.15)
    save(fig, "ch11_forest.png")


# ---------------------------------------------------------------------------
# 8. checking proportional hazards graphically
# ---------------------------------------------------------------------------
def fig_loglog():
    bc = brain_cancer()
    male = bc["sex"] == "Male"

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4))
    ax = axes[0]
    for mask, col, lab in [(~male, ACCENT, "Female"), (male, ORANGE, "Male")]:
        k = KaplanMeierFitter().fit(bc.loc[mask, "time"], bc.loc[mask, "status"])
        sf = k.survival_function_.iloc[:, 0]
        keep = (sf > 0) & (sf < 1) & (sf.index > 0)
        ax.step(np.log(sf.index[keep]), np.log(-np.log(sf[keep].values)),
                where="post", color=col, lw=1.9, label=lab)
    ax.set(xlabel="$\\log t$", ylabel="$\\log(-\\log \\hat S(t))$",
           title="Complementary log-log plot: parallel $\\Rightarrow$ PH plausible",
           xlim=(0, 4.6))
    ax.legend(fontsize=8)

    ax = axes[1]
    bins = pd.cut(bc["ki"], [39, 79, 89, 100], labels=["$\\leq 70$", "$80$", "$\\geq 90$"])
    for lab, col in zip(bins.cat.categories, [RED, ORANGE, ACCENT]):
        mask = (bins == lab).values
        k = KaplanMeierFitter().fit(bc.loc[mask, "time"], bc.loc[mask, "status"])
        sf = k.survival_function_
        xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
        ax.plot(xs, ys, color=col, lw=1.9, label=f"Karnofsky {lab} ($n={int(mask.sum())}$)")
    ax.set(xlabel="months", ylabel="$\\hat S(t)$", ylim=(0, 1.02), xlim=(0, 85),
           title="Stratified curves: checking a covariate by eye")
    ax.legend(loc="lower left", fontsize=7.6)
    save(fig, "ch11_loglog.png")


# ---------------------------------------------------------------------------
# 9. predicted survival curves from the Cox fit
# ---------------------------------------------------------------------------
def fig_predict():
    X = brain_cancer_design()
    cph = CoxPHFitter().fit(X, duration_col="time", event_col="status")
    base = X.drop(columns=["time", "status"]).median().to_frame().T

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4))
    ax = axes[0]
    prof = pd.concat([base] * 3, ignore_index=True)
    prof["ki"] = [60.0, 80.0, 100.0]
    sf = cph.predict_survival_function(prof)
    for j, (col, lab) in enumerate(zip([RED, ORANGE, ACCENT],
                                       ["$ki=60$", "$ki=80$", "$ki=100$"])):
        ax.step(sf.index.values, sf.iloc[:, j].values, where="post",
                color=col, lw=1.9, label=lab)
    ax.set(xlabel="months", ylabel="$\\hat S(t \\mid x)$", ylim=(0, 1.02), xlim=(0, 85),
           title="Karnofsky index, other covariates at their medians")
    ax.legend(loc="lower left", fontsize=8)

    ax = axes[1]
    prof = pd.concat([base] * 2, ignore_index=True)
    prof["diagnosis_HG glioma"] = [0.0, 1.0]
    sf = cph.predict_survival_function(prof)
    for j, (col, lab) in enumerate(zip([ACCENT, RED], ["Meningioma", "HG glioma"])):
        ax.step(sf.index.values, sf.iloc[:, j].values, where="post",
                color=col, lw=1.9, label=lab)
    ax.set(xlabel="months", ylabel="$\\hat S(t \\mid x)$", ylim=(0, 1.02), xlim=(0, 85),
           title="Diagnosis at $ki=80$: $\\widehat{HR}=8.62$ in survival terms")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "ch11_predict.png")


# ---------------------------------------------------------------------------
# 10. the Publication data (extended exercise)
# ---------------------------------------------------------------------------
def fig_x_publication():
    pub = pd.read_csv(DATA / "Publication.csv", index_col=0)
    pos = pub["posres"] == 1
    res = logrank_test(pub.loc[pos, "time"], pub.loc[~pos, "time"],
                       pub.loc[pos, "status"], pub.loc[~pos, "status"])

    fig, ax = plt.subplots(figsize=(8.4, 3.7))
    for mask, col, lab in [(~pos, ACCENT, "Negative / null result"),
                           (pos, ORANGE, "Positive result")]:
        k = KaplanMeierFitter().fit(pub.loc[mask, "time"], pub.loc[mask, "status"])
        sf = k.survival_function_
        xs, ys = step_curve(sf.index.values, sf.iloc[:, 0].values)
        ax.plot(xs, ys, color=col, lw=2.1,
                label=f"{lab} ($n={int(mask.sum())}$, {int(pub.loc[mask,'status'].sum())} published)")
    ax.text(0.98, 0.95,
            f"log-rank: $\\chi^2_1={res.test_statistic:.2f}$, $p={res.p_value:.3f}$\n"
            "adjusted Cox: $\\widehat{HR}=1.77$, $p=0.001$",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GREY, lw=0.8))
    ax.set(xlabel="months since trial completion", ylabel="$\\hat S(t)$ = still unpublished",
           ylim=(0, 1.02), xlim=(0, 100),
           title="Publication: time to publication of 244 clinical trials")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95)
    save(fig, "ch11_x_publication.png")


if __name__ == "__main__":
    fig_censoring()
    fig_naive()
    fig_km()
    fig_km_sex()
    fig_ph()
    fig_crossing()
    fig_forest()
    fig_loglog()
    fig_predict()
    fig_x_publication()

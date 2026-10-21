#!/usr/bin/env python3
"""Computed figures for Part 5 (Classification) of the lecture "Quantitative Research".

All model-based figures use the full Default data (../data/Default.csv) and
maximum-likelihood logistic regression -- deterministic, so the numbers agree
with glm() in R (see Part_5_Classification.R). Simulated or sub-sampled
figures use a fixed seed. Colours: HSBI palette of the shared preamble.

    python3 make_figures.py

Output: images/cls_*.png. The ISLR figures 4_6.pdf and 4_8.pdf are not touched.
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

BLUE = "#3333B2"
BLUE_DARK = "#1C1C6E"
ORANGE = "#E69F00"
GRAY = "#9A9A9A"
RED = "#C0392B"
GREEN = "#2E8B57"

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


df = pd.read_csv(os.path.join(DATA, "Default.csv"))
df["y"] = (df["default"] == "Yes").astype(int)
g1 = smf.logit("y ~ balance", df).fit(disp=0)
g3 = smf.logit("y ~ balance + income + C(student)", df).fit(disp=0)
p3 = g3.predict(df)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def fig_default_data():
    rng = np.random.default_rng(1)
    no = df[df.y == 0].sample(1500, random_state=1)
    yes = df[df.y == 1]
    fig = plt.figure(figsize=(13, 4.6))
    ax = fig.add_axes([0.05, 0.12, 0.47, 0.8])
    ax.scatter(no.balance, no.income / 1000, s=12, color=BLUE, alpha=0.45, label="default = No")
    ax.scatter(yes.balance, yes.income / 1000, s=22, marker="+", color=ORANGE, linewidths=1.3,
               label="default = Yes")
    ax.set_xlabel("balance (\\$)")
    ax.set_ylabel("income (1000 \\$)")
    ax.set_title("(a) Balance and income (all 333 defaulters, 1500 others)")
    ax.legend(loc="upper right", fontsize=10.5)
    style(ax)
    for k, (var, lab, sc) in enumerate([("balance", "balance (\\$)", 1), ("income", "income (1000 \\$)", 1000)]):
        ax = fig.add_axes([0.6 + 0.205 * k, 0.12, 0.17, 0.8])
        data = [df.loc[df.y == 0, var] / sc, df.loc[df.y == 1, var] / sc]
        bp = ax.boxplot(data, widths=0.55, patch_artist=True, medianprops=dict(color="black"))
        for patch, col in zip(bp["boxes"], [BLUE, ORANGE]):
            patch.set_facecolor(col)
            patch.set_alpha(0.55)
        ax.set_xticks([1, 2])
        ax.set_xticklabels(["No", "Yes"])
        ax.set_xlabel("default")
        ax.set_title(["(b)", "(c)"][k] + " " + lab, fontsize=12.5)
        style(ax)
    save(fig, "cls_default_data.png")


def fig_linear_vs_logistic():
    lpm = smf.ols("y ~ balance", df).fit()
    xs = np.linspace(0, 2700, 300)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.3), sharey=True)
    rng = np.random.default_rng(2)
    jitter = rng.uniform(-0.015, 0.015, len(df))
    for ax, title in zip(axes, ["(a) Linear regression", "(b) Logistic regression"]):
        ax.scatter(df.balance, df.y + jitter, s=4, color=ORANGE, alpha=0.35, edgecolor="none")
        ax.axhline(0, color=GRAY, lw=1, ls=":")
        ax.axhline(1, color=GRAY, lw=1, ls=":")
        ax.set_xlabel("balance (\\$)")
        ax.set_title(title)
        style(ax)
    axes[0].plot(xs, lpm.params.iloc[0] + lpm.params.iloc[1] * xs, color=BLUE, lw=2.6)
    axes[0].fill_between(xs, -0.2, 0, where=lpm.params.iloc[0] + lpm.params.iloc[1] * xs < 0,
                         color=RED, alpha=0.12)
    axes[0].text(40, -0.165, 'negative "probabilities"', color=RED, fontsize=11.5)
    axes[1].plot(xs, g1.predict(pd.DataFrame({"balance": xs})), color=BLUE, lw=2.6)
    axes[0].set_ylabel("P(default = Yes)")
    axes[0].set_ylim(-0.2, 1.08)
    save(fig, "cls_linear_vs_logistic.png")


def fig_sigmoid():
    z = np.linspace(-6, 6, 400)
    p = np.linspace(0.002, 0.998, 400)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.0))
    ax = axes[0]
    ax.plot(z, sigmoid(z), color=BLUE, lw=2.6)
    ax.axhline(0.5, color=GRAY, ls="--", lw=1)
    ax.axvline(0, color=GRAY, ls="--", lw=1)
    ax.set_xlabel(r"log-odds $\eta=\beta_0+\beta_1x$")
    ax.set_ylabel(r"probability $p$")
    ax.set_title(r"(a) logistic function $p=\dfrac{e^{\eta}}{1+e^{\eta}}$")
    ax.text(0.3, 0.42, r"$\eta=0 \Leftrightarrow p=0.5$", fontsize=11.5, bbox=WBOX)
    style(ax)
    ax = axes[1]
    ax.plot(p, np.log(p / (1 - p)), color=ORANGE, lw=2.6)
    ax.axhline(0, color=GRAY, ls="--", lw=1)
    ax.axvline(0.5, color=GRAY, ls="--", lw=1)
    ax.set_xlabel(r"probability $p$")
    ax.set_ylabel(r"log-odds $\log\frac{p}{1-p}$")
    ax.set_title(r"(b) logit: maps $(0,1)$ onto $(-\infty,\infty)$")
    style(ax)
    fig.tight_layout()
    save(fig, "cls_sigmoid.png")


def fig_student_paradox():
    xs = np.linspace(500, 2650, 300)
    inc = df.income.mean()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1.6, 1]})
    ax = axes[0]
    for lev, col, lab in [("No", BLUE, "non-students"), ("Yes", ORANGE, "students")]:
        pr = g3.predict(pd.DataFrame({"balance": xs, "income": inc, "student": lev}))
        ax.plot(xs, pr, color=col, lw=2.6, label=f"{lab}: P(default | balance)")
        rate = df.loc[df.student == lev, "y"].mean()
        ax.axhline(rate, color=col, lw=2, ls="--", label=f"{lab}: overall rate {100 * rate:.2f}%")
    ax.set_xlabel("balance (\\$)")
    ax.set_ylabel("default rate")
    ax.text(1450, 0.42, "overall default rates:\nstudents 4.31% > non-students 2.92%",
            fontsize=11, bbox=WBOX)
    ax.set_title("(a) At the same balance, students default less")
    ax.legend(loc="upper left", fontsize=10)
    style(ax)
    ax = axes[1]
    bp = ax.boxplot([df.loc[df.student == "No", "balance"], df.loc[df.student == "Yes", "balance"]],
                    widths=0.55, patch_artist=True, medianprops=dict(color="black"))
    for patch, col in zip(bp["boxes"], [BLUE, ORANGE]):
        patch.set_facecolor(col)
        patch.set_alpha(0.55)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["non-students", "students"])
    ax.set_ylabel("balance (\\$)")
    ax.set_title("(b) ... but carry larger balances")
    style(ax)
    fig.tight_layout()
    save(fig, "cls_student_paradox.png")


def rates(t):
    pred = p3 > t
    tp = np.sum(pred & (df.y == 1)); fp = np.sum(pred & (df.y == 0))
    fn = np.sum(~pred & (df.y == 1)); tn = np.sum(~pred & (df.y == 0))
    return tp / (tp + fn), tn / (tn + fp), (fp + fn) / len(df)


def fig_threshold():
    ts = np.linspace(0.01, 0.9, 200)
    r = np.array([rates(t) for t in ts])
    fig, ax = plt.subplots(figsize=(10, 4.3))
    ax.plot(ts, r[:, 0], color=ORANGE, lw=2.6, label="sensitivity (defaulters caught)")
    ax.plot(ts, r[:, 1], color=BLUE, lw=2.6, label="specificity (non-defaulters left alone)")
    ax.plot(ts, r[:, 2], color=RED, lw=2.2, ls="--", label="error rate")
    for t in (0.2, 0.5):
        ax.axvline(t, color=GRAY, lw=1.2, ls=":")
        ax.text(t + 0.008, 0.12, f"t = {t}", color="#555555", fontsize=11, bbox=WBOX)
    ax.set_xlabel(r'threshold $t$  (predict "default" if $\hat p>t$)')
    ax.set_ylabel("rate")
    ax.set_ylim(0, 1.02)
    ax.legend(loc="center right", fontsize=10.5)
    ax.set_title("Default data, logistic regression (balance + income + student)")
    style(ax)
    save(fig, "cls_threshold_tradeoff.png")


def fig_roc():
    y = df.y.values
    order = np.argsort(-p3.values)
    ys = y[order]
    tpr = np.concatenate([[0], np.cumsum(ys) / ys.sum()])
    fpr = np.concatenate([[0], np.cumsum(1 - ys) / (1 - ys).sum()])
    auc = float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2))
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    ax.plot(fpr, tpr, color=BLUE, lw=2.6, label=f"logistic regression (AUC = {auc:.3f})")
    ax.plot([0, 1], [0, 1], color=GRAY, ls="--", lw=1.4, label="random guessing (AUC = 0.5)")
    for t, mk in [(0.5, "o"), (0.2, "s"), (0.1, "^")]:
        se, sp, _ = rates(t)
        ax.plot(1 - sp, se, mk, color=ORANGE, ms=9, mec="black")
        ax.annotate(f"t = {t}", (1 - sp, se), xytext=(12, -14), textcoords="offset points", fontsize=11)
    ax.set_xlabel("1 - specificity (false positive rate)")
    ax.set_ylabel("sensitivity (true positive rate)")
    ax.set_title("ROC curve -- Default data")
    ax.legend(loc="lower right", fontsize=10)
    ax.set_xlim(-0.01, 1)
    ax.set_ylim(0, 1.01)
    style(ax)
    save(fig, "cls_roc.png")
    print("AUC", auc)


def fig_lda_1d():
    x = np.linspace(-3.5, 5.5, 500)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.0), sharey=True)
    for ax, (pi0, pi1), title in zip(axes, [(0.5, 0.5), (0.8, 0.2)],
                                     [r"(a) equal priors $\pi_0=\pi_1=0.5$", r"(b) priors $\pi_0=0.8$, $\pi_1=0.2$"]):
        f0 = pi0 * stats.norm.pdf(x, 0, 1)
        f1 = pi1 * stats.norm.pdf(x, 2, 1)
        ax.plot(x, f0, color=BLUE, lw=2.6, label=r"$\pi_0 f_0(x)$, $\mu_0=0$")
        ax.plot(x, f1, color=ORANGE, lw=2.6, label=r"$\pi_1 f_1(x)$, $\mu_1=2$")
        ax.fill_between(x, np.minimum(f0, f1), color=GRAY, alpha=0.3)
        xb = 1 - np.log(pi1 / pi0) / 2
        ax.axvline(xb, color=RED, lw=2, ls="--")
        ax.text(xb + 0.12, 0.24, r"$x^\star=%.3f$" % xb, color=RED, fontsize=12, bbox=WBOX)
        ax.set_xlabel("x")
        ax.set_title(title)
        ax.legend(loc="upper left", fontsize=10.5)
        style(ax)
    axes[0].set_ylabel("prior-weighted density")
    fig.tight_layout()
    save(fig, "cls_lda_1d.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig_default_data()
    fig_linear_vs_logistic()
    fig_sigmoid()
    fig_student_paradox()
    fig_threshold()
    fig_roc()
    fig_lda_1d()
    print("g1", g1.params.values, "g3", g3.params.values)

"""Generate the computed matplotlib figures for the Chapter 4 deck (Classification).

Every figure is computed from the bundled course data (``Default.csv``) with a
seeded split --- nothing is sketched by hand, and every number quoted on the
slide comes out of this file. The split, scaler and model match the chapter 4
lab exactly (test_size=0.3, random_state=0), so the deck and the notebook
print the same numbers. Run from anywhere:

    python Chapters/chapter_04/make_figures.py

Output: Chapters/chapter_04/images/ch04_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. The ISLP-sourced figures
(``4_2.pdf`` etc.) are not touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
RED = "#C0392B"
GREEN = "#2E7D32"

SEED = 0  # simulated figures reseed from here, so call order never matters

# The five figures reconstructed below were originally drawn one notch larger
# than the deck default so they stay readable at the small \includegraphics
# widths they are given (0.33--0.6 \textheight). Applied through rc_context so
# the module-level house rcParams stay authoritative everywhere else.
LARGE = {"font.size": 13, "axes.titlesize": 15.5, "axes.labelsize": 14,
         "legend.fontsize": 12, "xtick.labelsize": 13, "ytick.labelsize": 13}

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


def fig_threshold_picture():
    """Schematic of the two score distributions cut by a moving threshold.

    Two equal-sized classes whose predicted scores are Gaussian; everything
    right of the threshold is predicted positive, so the four confusion-matrix
    cells appear as the four areas TN / FN / FP / TP. The label row (``actual
    -`` / ``actual +``) is kept clear of the arrow row above it, so the arrows
    never strike through the text.
    """
    mu_neg, mu_pos, sd, t = 0.0, 2.6, 1.05, 1.55
    x = np.union1d(np.linspace(-4.2, 6.8, 1101), [t])
    dens = lambda m: np.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    neg, pos = dens(mu_neg), dens(mu_pos)
    lo, hi = x <= t, x >= t

    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    ax.grid(False)
    ax.fill_between(x, 0, neg, where=lo, color=ACCENT, alpha=0.10, lw=0)
    ax.fill_between(x, 0, pos, where=hi, color=GREEN, alpha=0.28, lw=0)
    ax.fill_between(x, 0, pos, where=lo, facecolor=ORANGE, edgecolor=ORANGE,
                    alpha=0.33, hatch="//", lw=0)
    ax.fill_between(x, 0, neg, where=hi, facecolor=RED, edgecolor=RED,
                    alpha=0.30, hatch="xx", lw=0)
    ax.plot(x, neg, color=ACCENT, lw=2.0, zorder=3)
    ax.plot(x, pos, color=RED, lw=2.0, zorder=3)
    ax.axvline(t, color="black", ls=(0, (4, 3)), lw=2.2, zorder=4)

    # three well-separated horizontal bands: decision row, arrow row, curve row
    y_top, y_arrow, y_curve = 0.484, 0.452, 0.4065

    ax.text(-3.87, y_top, "predict $-$", color=GREY, fontsize=10)
    ax.text(t + 0.09, y_top, "threshold $t$", fontsize=10)
    ax.text(6.0, y_top, "predict $+$", color=GREY, fontsize=10, ha="right")

    ax.annotate("", xy=(-0.25, y_arrow), xytext=(1.41, y_arrow),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=2.0,
                                mutation_scale=16))
    ax.text(-0.40, y_arrow, r"lower $t$: sensitivity $\uparrow$", color=ACCENT,
            fontsize=9, ha="right", va="center")
    ax.annotate("", xy=(3.37, y_arrow), xytext=(1.70, y_arrow),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.0,
                                mutation_scale=16))
    ax.text(3.52, y_arrow, r"raise $t$: specificity $\uparrow$", color=GREEN,
            fontsize=9, ha="left", va="center")

    ax.text(mu_neg, y_curve, "actual $-$", color=ACCENT, fontsize=10, ha="center")
    ax.text(mu_pos, y_curve, "actual $+$", color=RED, fontsize=10, ha="center")

    ax.text(-1.35, 0.058, "TN", color=ACCENT, fontsize=11, fontweight="bold",
            ha="center")
    ax.text(0.87, 0.029, "FN", color=ORANGE, fontsize=11, fontweight="bold",
            ha="center")
    ax.text(3.57, 0.079, "TP", color=GREEN, fontsize=11, fontweight="bold",
            ha="center")
    ax.annotate("FP", xy=(2.30, 0.052), xytext=(2.90, 0.139), color=RED,
                fontsize=11, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))

    ax.set_title("Sliding the threshold trades sensitivity against specificity")
    ax.set_xlabel(r"predicted score  $\hat p$  (higher $\Rightarrow$ more positive)")
    ax.set_yticks([])
    ax.set_ylim(0, 0.52)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)

    save(fig, "ch04_x_threshold.png")


def fig_threshold_tradeoff():
    """Sensitivity, specificity and precision as functions of the threshold.

    Identical pipeline to the chapter 4 lab's 'the threshold is a business
    decision' section: logistic regression on balance, income, student on the
    same seeded 70/30 split, so the numbers printed here are the numbers the
    notebook prints.
    """
    df = pd.read_csv(DATA / "Default.csv")
    df["student_d"] = (df["student"] == "Yes").astype(int)
    y = (df["default"] == "Yes").astype(int).values
    X = df[["balance", "income", "student_d"]].values

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
    scaler = StandardScaler().fit(Xtr)
    model = LogisticRegression(max_iter=2000).fit(scaler.transform(Xtr), ytr)
    proba = model.predict_proba(scaler.transform(Xte))[:, 1]

    ts = np.linspace(0.005, 0.9, 300)
    sens, spec, prec = [], [], []
    for t in ts:
        pred = proba >= t
        tp = (pred & (yte == 1)).sum()
        fn = (~pred & (yte == 1)).sum()
        fp = (pred & (yte == 0)).sum()
        tn = (~pred & (yte == 0)).sum()
        sens.append(tp / (tp + fn))
        spec.append(tn / (tn + fp))
        prec.append(tp / (tp + fp) if tp + fp else np.nan)

    def counts_at(t):
        pred = proba >= t
        return (pred & (yte == 1)).sum(), (yte == 1).sum()

    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    for t in (0.10, 0.50):
        ax.axvline(t, color=GREY, lw=1.0, ls=":", zorder=1)
    ax.plot(ts, sens, color=ACCENT, lw=2, zorder=3)
    ax.plot(ts, prec, color=ORANGE, lw=2, zorder=3)
    ax.plot(ts, spec, color=GREY, lw=1.6, zorder=2)

    ax.text(0.55, 0.44, "sensitivity", color=ACCENT, fontsize=9.5)
    ax.text(0.40, 0.60, "precision", color=ORANGE, fontsize=9.5)
    ax.text(0.62, 1.035, "specificity", color=GREY, fontsize=9)

    tp10, pos = counts_at(0.10)
    tp50, _ = counts_at(0.50)
    ax.annotate(f"$t=0.10$: catches {tp10}/{pos}\ndefaulters",
                xy=(0.10, np.interp(0.10, ts, sens)), xytext=(0.145, 0.87),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate(f"$t=0.50$: catches {tp50}/{pos}",
                xy=(0.50, np.interp(0.50, ts, sens)), xytext=(0.33, 0.18),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.set_xlabel(r"decision threshold $t$   (predict default when $\hat p \geq t$)")
    ax.set_ylabel("value on the held-out 30%")
    ax.set_xlim(0, 0.9)
    ax.set_ylim(0, 1.06)

    save(fig, "ch04_threshold_tradeoff.png")
    i10 = np.argmin(np.abs(ts - 0.10)); i50 = np.argmin(np.abs(ts - 0.50))
    print("ch04_threshold_tradeoff.png:",
          f"t=0.10 sens {sens[i10]:.3f} prec {prec[i10]:.3f} |",
          f"t=0.50 sens {sens[i50]:.3f} prec {prec[i50]:.3f} |",
          f"caught {tp10}/{pos} vs {tp50}/{pos}")


def _default_full():
    """Default.csv with the three predictors used all through the chapter.

    The whole 10,000 rows, no split: the confusion matrix quoted on the
    'Extended Exercise 4.5' slide (TN 9627 / FP 40 / FN 228 / TP 105) and the
    AUC 0.950 on the ROC slide are both in-sample numbers on the full file.
    """
    df = pd.read_csv(DATA / "Default.csv")
    df["student_d"] = (df["student"] == "Yes").astype(int)
    y = (df["default"] == "Yes").astype(int).values
    X = df[["balance", "income", "student_d"]].values
    return df, X, y


def fig_sigmoid():
    """Schematic: the logistic curve and its inverse, the logit.

    Pure mathematics --- no data. Left panel is sigma(z) = e^z/(1+e^z) on
    z in [-6, 6] with the symmetry point sigma(0) = 0.5 marked; right panel is
    logit(p) = log[p/(1-p)] on p in (0, 1), which stretches the unit interval
    onto the whole real line. Both quantities the slide's takeaway names.
    """
    with plt.rc_context({**LARGE, "font.size": 12, "axes.titlesize": 14.5,
                         "axes.labelsize": 13.5, "xtick.labelsize": 12,
                         "ytick.labelsize": 12, "axes.spines.top": True,
                         "axes.spines.right": True}):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.16, 3.67))

        z = np.linspace(-6, 6, 801)
        s = 1.0 / (1.0 + np.exp(-z))
        ax1.axhline(0.0, color=GREY, ls=":", lw=1.1, zorder=1)
        ax1.axhline(1.0, color=GREY, ls=":", lw=1.1, zorder=1)
        ax1.plot(z, s, color=ACCENT, lw=2.8, zorder=3)
        ax1.plot([0], [0.5], "o", color=ORANGE, ms=9, zorder=4)
        ax1.annotate(r"$\sigma(0) = 0.5$", xy=(0.20, 0.505), xytext=(1.55, 0.66),
                     color=ORANGE, fontsize=12,
                     arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6,
                                     mutation_scale=13))
        ax1.text(-5.55, 0.775, r"$\sigma(z) = \dfrac{e^{z}}{1 + e^{z}}$",
                 color=ACCENT, fontsize=15)
        # "asymptote 1" sits on the LEFT, where the curve is flat at 0 --- on the
        # right it would be struck through by the rising curve.
        ax1.text(-5.75, 1.025, "asymptote 1", color=GREY, fontsize=11)
        ax1.text(5.75, 0.035, "asymptote 0", color=GREY, fontsize=11, ha="right")
        ax1.set_title("Sigmoid squashes the line into (0,1)", color=ACCENT)
        ax1.set_xlabel(r"linear predictor  $z = \beta_0 + \beta^\top x$")
        ax1.set_ylabel(r"probability  $p = \sigma(z)$")
        ax1.set_xlim(-6, 6)
        ax1.set_ylim(-0.081, 1.122)
        ax1.set_xticks(np.arange(-6, 6.1, 2))
        ax1.set_yticks(np.arange(0, 1.01, 0.2))

        p = np.linspace(0.005, 0.995, 801)
        lo = np.log(p / (1 - p))
        ax2.axhline(0.0, color=GREY, ls=":", lw=1.1, zorder=1)
        ax2.axvline(0.5, color=GREY, ls=":", lw=1.1, zorder=1)
        ax2.plot(p, lo, color=GREEN, lw=2.8, zorder=3)
        ax2.plot([0.5], [0.0], "o", color=GREEN, ms=9, zorder=4)
        # sized and placed to finish left of the dotted p = 0.5 rule
        ax2.text(0.030, 3.45, r"$\mathrm{logit}(p) = \log\dfrac{p}{1 - p}$",
                 color=GREEN, fontsize=13)
        ax2.text(0.60, 4.35, r"$\rightarrow +\infty$", color=GREY, fontsize=11)
        ax2.text(0.035, -5.05, r"$\rightarrow -\infty$", color=GREY, fontsize=11)
        ax2.set_title("Log-odds scale is linear & unbounded", color=GREEN)
        ax2.set_xlabel(r"probability  $p$")
        ax2.set_ylabel(r"log-odds  $\log[p/(1-p)]$")
        ax2.set_xlim(0, 1)
        ax2.set_ylim(-5.6, 5.6)
        ax2.set_yticks(np.arange(-4, 4.1, 2))

        save(fig, "ch04_x_sigmoid.png")
    print("ch04_x_sigmoid.png: sigma(0) =", 1 / (1 + np.exp(-0.0)),
          "| logit(0.5) =", np.log(0.5 / 0.5))


def fig_roc():
    """ROC curve for logistic regression on the full Default data.

    In-sample fit on all 10,000 rows of ``default ~ balance + income +
    student`` --- the same model the 'Extended Exercise 4.5' slide tabulates,
    so the marked 0.5 operating point is exactly the TP 105 / FN 228 /
    FP 40 / TN 9627 row: sensitivity 0.315 and 1-specificity 0.004. The AUC
    printed in the legend is the 0.950 the slide quotes.
    """
    _, X, y = _default_full()
    # Unscaled predictors and max_iter=10000, exactly as the solution slide's
    # code listing --- scaling shifts the fit enough to move one borderline
    # case and break the quoted 9627 / 40 split.
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        model = LogisticRegression(max_iter=10000).fit(X, y)
    proba = model.predict_proba(X)[:, 1]

    fpr, tpr, thr = roc_curve(y, proba)
    auc = roc_auc_score(y, proba)
    pred = proba >= 0.5
    tp = int((pred & (y == 1)).sum()); fn = int((~pred & (y == 1)).sum())
    fp = int((pred & (y == 0)).sum()); tn = int((~pred & (y == 0)).sum())
    sens, fpr50 = tp / (tp + fn), fp / (fp + tn)

    with plt.rc_context(LARGE):
        fig, ax = plt.subplots(figsize=(7.00, 4.21))
        ax.grid(False)
        ax.plot([0, 1], [0, 1], ls="--", color=GREY, lw=1.5,
                label="random (AUC=0.50)")
        ax.plot(fpr, tpr, color=ACCENT, lw=2.8, label=f"logistic ROC (AUC={auc:.3f})")
        ax.plot([fpr50], [sens], "o", color=RED, ms=11, label="threshold = 0.5")
        # the caption sits above the 45-degree chance line, which would
        # otherwise run straight through "1-spec=0.00"
        ax.annotate(f"0.5 cutoff\nsens={sens:.2f}, 1-spec={fpr50:.2f}",
                    xy=(fpr50 + 0.012, sens + 0.015), xytext=(0.032, 0.405),
                    color=RED, fontsize=11.5, va="bottom",
                    arrowprops=dict(arrowstyle="-", color=RED, lw=0.9))
        ax.set_title(r"ROC curve: default $\sim$ balance + income + student")
        ax.set_xlabel("1 - specificity (false positive rate)")
        ax.set_ylabel("sensitivity (true positive rate)")
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.03, 1.03)
        ax.legend(loc="lower right", frameon=False, handlelength=2.4)

        save(fig, "ch04_roc.png")
    print("ch04_roc.png:", f"TN {tn} FP {fp} FN {fn} TP {tp} |",
          f"acc {(tn + tp) / len(y):.3f} sens {sens:.3f} 1-spec {fpr50:.3f} |",
          f"AUC {auc:.4f} | thresholds {len(thr)}")


def fig_logistic_vs_linear():
    """ISLP Figure 4.2 recreated on Default: straight line vs.\\ logistic curve.

    Both panels regress the 0/1 default indicator on ``balance`` over all
    10,000 rows. The OLS line dips below zero for small balances (the shaded
    wedge) --- the point the slide's takeaway makes --- while the logistic fit
    is confined to [0, 1] by construction.
    """
    df, _, y = _default_full()
    bal = df["balance"].values.reshape(-1, 1)

    lin = LinearRegression().fit(bal, y)
    log = LogisticRegression(max_iter=2000).fit(bal / 1000.0, y)
    grid = np.linspace(0, bal.max(), 600)
    yhat_lin = lin.predict(grid.reshape(-1, 1))
    yhat_log = log.predict_proba(grid.reshape(-1, 1) / 1000.0)[:, 1]
    zero_at = -lin.intercept_ / lin.coef_[0]

    with plt.rc_context(LARGE):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.82), sharey=True)
        fig.suptitle("Modelling P(default) from balance", fontsize=13.5)

        for ax, yhat, title in ((ax1, yhat_lin, "Linear regression"),
                                (ax2, yhat_log, "Logistic regression")):
            ax.grid(False)
            ax.axhline(0.0, color=GREY, ls=":", lw=1.1, zorder=1)
            ax.axhline(1.0, color=GREY, ls=":", lw=1.1, zorder=1)
            ax.plot(bal[y == 0], np.full((y == 0).sum(), -0.022), "|",
                    color=ORANGE, alpha=0.18, ms=8, mew=1.0, zorder=2)
            ax.plot(bal[y == 1], np.full((y == 1).sum(), 1.022), "|",
                    color=ORANGE, alpha=0.45, ms=8, mew=1.0, zorder=2)
            ax.plot(grid, yhat, color=ACCENT, lw=3.0, zorder=4)
            ax.set_title(title)
            ax.set_xlabel(r"balance (\$)")
            ax.set_xticks(np.arange(0, 2501, 500))

        ax1.fill_between(grid, yhat_lin, 0, where=yhat_lin < 0, color=RED,
                         alpha=0.16, lw=0, zorder=3)
        ax1.text(70, 0.225, "predictions\n$<0$", color=RED, fontsize=12,
                 va="top")
        ax1.set_ylabel("P(default)")
        ax1.set_ylim(-0.17, 1.14)
        ax1.set_yticks([0.0, 0.5, 1.0])

        save(fig, "ch04_logistic_vs_linear.png")
    print("ch04_logistic_vs_linear.png:",
          f"OLS intercept {lin.intercept_:.4f} slope {lin.coef_[0]:.3e} |",
          f"OLS prediction is negative below balance {zero_at:.0f} |",
          f"logistic range [{yhat_log.min():.4f}, {yhat_log.max():.4f}]")


def fig_lda_1d_densities():
    """Schematic: one-predictor LDA as two Gaussians cut by a threshold.

    No data --- the two class densities are exactly the N(-1.5, 1) and
    N(+1.5, 1) the slide names. The equal-prior boundary is the midpoint 0;
    raising pi_2 to 0.8 moves it by log(0.8/0.2) sigma^2/(mu_2 - mu_1)
    = log(4)/3 = 0.46 toward the rarer class, i.e. to x = -0.46, both of which
    the takeaway quotes. The shaded area is min(f_1, f_2), the irreducible
    Bayes overlap.
    """
    mu1, mu2, sigma = -1.5, 1.5, 1.0
    pi2 = 0.8
    shift = np.log(pi2 / (1 - pi2)) * sigma**2 / (mu2 - mu1)
    b_equal = 0.5 * (mu1 + mu2)
    b_tilt = b_equal - shift

    x = np.linspace(-5, 5, 1201)
    dens = lambda m: np.exp(-0.5 * ((x - m) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    f1, f2 = dens(mu1), dens(mu2)

    with plt.rc_context(LARGE):
        fig, ax = plt.subplots(figsize=(7.28, 4.01))
        ax.grid(False)
        ax.fill_between(x, 0, np.minimum(f1, f2), color="0.82", lw=0, zorder=1)
        ax.plot(x, f1, color=ACCENT, lw=2.8, zorder=3)
        ax.plot(x, f2, color=ORANGE, lw=2.8, zorder=3)
        # the two cutoffs stop short of the caption row above them
        ax.plot([b_equal, b_equal], [0, 0.408], color=GREEN, lw=2.6, zorder=4)
        ax.plot([b_tilt, b_tilt], [0, 0.408], color=GREEN, lw=2.6, ls="--",
                zorder=4)
        ax.annotate("", xy=(b_tilt, 0.285), xytext=(b_equal, 0.285),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8,
                                    mutation_scale=13), zorder=4)
        ax.text(0.0, 0.443,
                r"raising $\pi_2$ to 0.8 shifts the cutoff by "
                rf"$\ln(0.8/0.2)\,\sigma^2/(\mu_2{{-}}\mu_1) = {shift:.2f}$"
                " toward the rarer class",
                color=GREEN, fontsize=10.5, ha="center", va="baseline")

        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"class density $f_k(x)$")
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 0.478)
        ax.set_xticks(np.arange(-4, 4.1, 2))
        ax.set_yticks(np.arange(0, 0.41, 0.1))
        # column-major fill: classes + equal-prior cutoff left, the rest right
        handles = [
            Line2D([], [], color=ACCENT, lw=2.8, label=r"class 1:  $N(-1.5,\,1)$"),
            Line2D([], [], color=ORANGE, lw=2.8, label=r"class 2:  $N(+1.5,\,1)$"),
            Line2D([], [], color=GREEN, lw=2.6,
                   label=r"boundary, $\pi_1 = \pi_2 = 0.5$:  $x = 0$"),
            Line2D([], [], color=GREEN, lw=2.6, ls="--",
                   label=rf"boundary, $\pi_2 = 0.8$:  $x = {b_tilt:.2f}$"),
            Patch(facecolor="0.82", label="overlap: unavoidable errors"),
        ]
        ax.legend(handles=handles, ncol=2, loc="lower center",
                  bbox_to_anchor=(0.5, 1.005), frameon=False, fontsize=11.0,
                  handlelength=2.0, columnspacing=1.6, borderaxespad=0.0)

        save(fig, "ch04_x_lda_1d_densities.png")
    print("ch04_x_lda_1d_densities.png:",
          f"equal-prior boundary {b_equal:.2f} | shift {shift:.4f} |",
          f"tilted boundary {b_tilt:.2f} | crossing density {np.min(np.abs(f1 - f2)):.4f}")


def fig_lda_qda():
    """LDA's line vs.\\ QDA's conic on two simulated two-class problems.

    Simulation, seeded with ``np.random.default_rng(0)``: 250 points per class.
    Each cloud is drawn normally and then affinely corrected so its *sample*
    mean and covariance equal the target exactly. That correction is what makes
    the left panel say what the takeaway says: with the two sample covariances
    genuinely identical, QDA's quadratic term cancels and its conic collapses
    onto LDA's line, instead of wandering off in the corners on 250 points of
    estimation noise. On the right the two targets differ, so the fitted QDA
    conic is the population-optimal boundary and LDA cannot follow it. Both
    boundaries are the zero level set of the fitted scikit-learn
    discriminants, not hand-drawn.
    """
    n = 250
    rng = np.random.default_rng(SEED)

    def draw(mean, cov):
        """Gaussian cloud whose sample mean/covariance are exactly mean/cov."""
        z = rng.standard_normal((n, 2))
        z -= z.mean(axis=0)
        z = z @ np.linalg.inv(np.linalg.cholesky(np.cov(z, rowvar=False))).T
        return z @ np.linalg.cholesky(np.asarray(cov)).T + np.asarray(mean)

    def rotated(sd_major, sd_minor, angle):
        c, s = np.cos(angle), np.sin(angle)
        R = np.array([[c, -s], [s, c]])
        return R @ np.diag([sd_major**2, sd_minor**2]) @ R.T

    eq_cov = rotated(1.12, 0.92, 0.35)
    left = (draw([-1.5, -1.4], eq_cov), draw([1.6, 1.6], eq_cov))

    right = (draw([-0.1, 0.0], rotated(1.15, 1.04, 0.0)),
             draw([2.4, 0.7], rotated(1.80, 0.40, -0.50)))

    # explicit windows: the legend corner has to stay clear of the QDA conic
    # windows leave an empty band at the bottom left for the legend: both
    # boundaries sweep across the top left, so a legend there gets struck through
    panels = ((r"Equal covariance $\rightarrow$ LDA optimal", left,
               (-5.0, 5.2), (-6.2, 4.7)),
              (r"Unequal covariance $\rightarrow$ QDA optimal", right,
               (-4.6, 7.3), (-6.0, 5.4)))

    with plt.rc_context(LARGE):
        fig, axes = plt.subplots(1, 2, figsize=(10.1, 3.91))
        for ax, (title, (A, B), xlim, ylim) in zip(axes, panels):
            X = np.vstack([A, B])
            yy = np.r_[np.zeros(n), np.ones(n)]
            ax.grid(False)
            ax.scatter(A[:, 0], A[:, 1], s=13, color=ACCENT, alpha=0.55, lw=0)
            ax.scatter(B[:, 0], B[:, 1], s=13, color=ORANGE, alpha=0.70, lw=0)

            (x0, x1), (y0, y1) = xlim, ylim
            gx, gy = np.meshgrid(np.linspace(x0, x1, 600), np.linspace(y0, y1, 600))
            mesh = np.c_[gx.ravel(), gy.ravel()]

            lda = LinearDiscriminantAnalysis().fit(X, yy)
            qda = QuadraticDiscriminantAnalysis(store_covariance=True).fit(X, yy)
            ax.contour(gx, gy, lda.decision_function(mesh).reshape(gx.shape),
                       levels=[0], colors=[RED], linewidths=2.6)
            ax.contour(gx, gy, qda.decision_function(mesh).reshape(gx.shape),
                       levels=[0], colors=[GREEN], linewidths=2.6,
                       linestyles="--")

            ax.set_xlim(x0, x1)
            ax.set_ylim(y0, y1)
            ax.set_title(title)
            ax.set_xlabel(r"$X_1$")
            ax.legend(handles=[Line2D([], [], color=RED, lw=2.6, label="LDA (linear)"),
                               Line2D([], [], color=GREEN, lw=2.6, ls="--",
                                      label="QDA (curved)")],
                      loc="lower left", frameon=False, fontsize=12,
                      handlelength=2.0, borderaxespad=0.3)
        axes[0].set_ylabel(r"$X_2$")

        save(fig, "ch04_lda_qda.png")

    for name, (A, B) in (("equal", left), ("unequal", right)):
        X = np.vstack([A, B]); yy = np.r_[np.zeros(n), np.ones(n)]
        lda = LinearDiscriminantAnalysis().fit(X, yy)
        qda = QuadraticDiscriminantAnalysis().fit(X, yy)
        print(f"ch04_lda_qda.png [{name}]:",
              f"LDA train acc {lda.score(X, yy):.3f}",
              f"QDA train acc {qda.score(X, yy):.3f}",
              f"| disagreement {np.mean(lda.predict(X) != qda.predict(X)):.3f}")


if __name__ == "__main__":
    fig_threshold_picture()
    fig_threshold_tradeoff()
    fig_sigmoid()
    fig_roc()
    fig_logistic_vs_linear()
    fig_lda_1d_densities()
    fig_lda_qda()

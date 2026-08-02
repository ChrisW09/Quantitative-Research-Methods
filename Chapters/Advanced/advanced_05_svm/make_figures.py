"""Generate the matplotlib figures for the Chapter 9 deck (Support Vector Machines).

Every figure is computed either from the bundled course dataset
``ALL CSV FILES - 2nd Edition/Heart.csv`` or from a clearly labelled, seeded
simulation (``np.random.default_rng(2024)`` for the separable geometry data,
``np.random.default_rng(2025)`` for the overlapping data, and scikit-learn's
``make_circles(..., random_state=0)`` for the non-linear data).  Nothing is
sketched by hand.  Run from anywhere:

    python3 "Chapters/Advanced/advanced_05_svm/make_figures.py"

Output: Chapters/Advanced/advanced_05_svm/images/ch09_*.png at 150 dpi, matching the figure
size and resolution used by the other decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import make_circles
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#B03030"

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


# ------------------------------------------------------------------
# Shared, seeded data
# ------------------------------------------------------------------
def sim_separable(seed=2024, n=20, shift=2.5):
    """Two linearly separable Gaussian clouds in the plane."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 2))
    y = np.repeat([-1, 1], n // 2)
    X[y == 1] += shift
    return X, y


def sim_overlap(seed=2025, n=60, shift=1.6):
    """Two overlapping Gaussian clouds -- no separating hyperplane exists."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 2))
    y = np.repeat([-1, 1], n // 2)
    X[y == 1] += shift
    return X, y


def scatter2(ax, X, y, s=34, legend=False, loc="upper left"):
    for cls, col, mk, lab in [(-1, ACCENT, "o", "$y=-1$"), (1, ORANGE, "s", "$y=+1$")]:
        m = y == cls
        ax.scatter(X[m, 0], X[m, 1], c=col, marker=mk, s=s, edgecolor="white",
                   linewidth=0.6, zorder=3, label=lab)
    if legend:
        ax.legend(loc=loc, fontsize=7, framealpha=0.9)


def line_from_w(ax, w, b, xlim, style="-", col="k", lw=1.6, label=None):
    """Draw {x : b + w.x = 0} clipped to xlim."""
    xs = np.array(xlim)
    if abs(w[1]) < 1e-9:
        ax.axvline(-b / w[0], ls=style, color=col, lw=lw, label=label)
    else:
        ax.plot(xs, -(b + w[0] * xs) / w[1], ls=style, color=col, lw=lw, label=label)


def boundary(ax, model, X, pad=0.6, ngrid=300, levels=(0,), fill=True):
    """Shade the two half-spaces and draw the decision boundary of `model`."""
    x0, x1 = X[:, 0].min() - pad, X[:, 0].max() + pad
    y0, y1 = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.linspace(x0, x1, ngrid), np.linspace(y0, y1, ngrid))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    if fill:
        ax.contourf(xx, yy, Z, levels=[-1e9, 0, 1e9],
                    colors=[ACCENT, ORANGE], alpha=0.13, zorder=0)
    ax.contour(xx, yy, Z, levels=list(levels), colors="k", linewidths=1.5, zorder=2)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    return Z


# ------------------------------------------------------------------
# 1. What a hyperplane is
# ------------------------------------------------------------------
def fig_hyperplane():
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    xs = np.linspace(-2.6, 2.6, 200)
    xx, yy = np.meshgrid(np.linspace(-2.6, 2.6, 400), np.linspace(-2.6, 2.2, 400))
    Z = 1 + 2 * xx + 3 * yy
    ax.contourf(xx, yy, Z, levels=[-1e9, 0, 1e9], colors=[ACCENT, ORANGE],
                alpha=0.16, zorder=0)
    ax.plot(xs, -(1 + 2 * xs) / 3, color="k", lw=1.8, zorder=2)
    ax.annotate(r"$1+2X_1+3X_2>0$", xy=(0.35, 1.55), fontsize=9, color=ORANGE)
    ax.annotate(r"$1+2X_1+3X_2<0$", xy=(-2.45, -1.9), fontsize=9, color=ACCENT)
    # the normal vector beta = (2,3), drawn from a point on the line
    p = np.array([0.0, -1 / 3])
    n = np.array([2.0, 3.0]) / np.linalg.norm([2.0, 3.0])
    ax.annotate("", xy=p + 0.9 * n, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
    ax.text(*(p + 0.95 * n + np.array([0.06, 0.02])), r"$\beta=(2,3)$",
            color=GREEN, fontsize=9)
    for pt, lab in [((0, 0), "(0,0)"), ((-1, 1), "(-1,1)"), ((2, -2), "(2,-2)")]:
        ax.scatter(*pt, c="k", s=26, zorder=4)
        ax.annotate(lab, pt, textcoords="offset points", xytext=(7, -3), fontsize=8)
    ax.set(xlabel="$X_1$", ylabel="$X_2$",
           title=r"The hyperplane $1+2X_1+3X_2=0$ splits the plane in two")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.2)
    ax.set_aspect("equal")
    save(fig, "ch09_hyperplane.png")


# ------------------------------------------------------------------
# 2. Infinitely many separating hyperplanes
# ------------------------------------------------------------------
def fig_many_hyperplanes():
    X, y = sim_separable()
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    xlim = (X[:, 0].min() - 0.6, X[:, 0].max() + 0.6)
    scatter2(ax, X, y, legend=True)
    # Three hyperplanes at different angles, each offset to a point strictly inside
    # the gap between the two classes -- so each one separates the data perfectly.
    for k, (deg, t) in enumerate([(8.0, 0.5), (42.0, 0.2), (68.0, 0.8)]):
        w = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
        s = X @ w
        lo, hi = s[y == -1].max(), s[y == 1].min()
        b = -(lo + t * (hi - lo))
        assert np.all(np.sign(b + s) == y), "candidate does not separate"
        line_from_w(ax, w, b, xlim, style=["-", "--", ":"][k], col=GREY, lw=1.5)
    ax.set_xlim(*xlim)
    ax.set_ylim(X[:, 1].min() - 0.6, X[:, 1].max() + 0.6)
    ax.set(xlabel="$X_1$", ylabel="$X_2$",
           title="Three of infinitely many hyperplanes that separate these 20 points perfectly")
    save(fig, "ch09_many_hyperplanes.png")


# ------------------------------------------------------------------
# 3. The maximal margin classifier
# ------------------------------------------------------------------
def fig_maxmargin():
    X, y = sim_separable()
    m = SVC(kernel="linear", C=1e6).fit(X, y)
    w, b = m.coef_[0], m.intercept_[0]
    width = 2 / np.linalg.norm(w)
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    boundary(ax, m, X, levels=(-1, 0, 1))
    scatter2(ax, X, y)
    sv = X[m.support_]
    ax.scatter(sv[:, 0], sv[:, 1], s=170, facecolors="none", edgecolors=GREEN,
               linewidths=2.0, zorder=5,
               label=f"support vectors ($n={len(sv)}$)")
    # margin arrow along the normal direction, from the boundary to the margin
    n = w / np.linalg.norm(w)
    foot = -b * n / np.linalg.norm(w)
    ax.annotate("", xy=foot + n * width / 2, xytext=foot - n * width / 2,
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.6))
    ax.annotate("$2M$", xy=foot, xytext=(-24, 4), textcoords="offset points",
                color=RED, fontsize=9)
    ax.legend(loc="upper left", fontsize=7, framealpha=0.92)
    ax.set_aspect("equal")
    ax.set(xlabel="$X_1$", ylabel="$X_2$",
           title=f"Maximal margin: {len(sv)} support vectors\n"
                 f"$M=1/\\|\\beta\\|={width / 2:.3f}$, width $2M={width:.3f}$")
    save(fig, "ch09_maxmargin.png")


# ------------------------------------------------------------------
# 4. Fatal flaw 1: overlapping classes
# ------------------------------------------------------------------
def fig_nonseparable():
    X, y = sim_overlap()
    hard = SVC(kernel="linear", C=1e6).fit(X, y)
    acc = hard.score(X, y)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    boundary(ax, hard, X)
    scatter2(ax, X, y, s=28, legend=True)
    wrong = hard.predict(X) != y
    ax.scatter(X[wrong, 0], X[wrong, 1], s=150, facecolors="none",
               edgecolors=RED, linewidths=1.8, zorder=6)
    ax.set(xlabel="$X_1$", ylabel="$X_2$",
           title=f"No separating hyperplane exists: the best linear rule still "
                 f"misclassifies {wrong.sum()} of {len(y)} points "
                 f"(training accuracy {acc:.3f})")
    save(fig, "ch09_nonseparable.png")


# ------------------------------------------------------------------
# 5. Fatal flaw 2: one point rules the hyperplane
# ------------------------------------------------------------------
def fig_instability():
    X, y = sim_separable()
    Xp = X.copy()
    Xp[10] = [1.9, -1.0]
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.5), sharex=True, sharey=True)
    for ax, D, ttl in [(axes[0], X, "original data"), (axes[1], Xp, "one point moved")]:
        m = SVC(kernel="linear", C=1e6).fit(D, y)
        w = m.coef_[0]
        ang = np.degrees(np.arctan2(w[1], w[0]))
        wid = 2 / np.linalg.norm(w)
        boundary(ax, m, X, levels=(-1, 0, 1))
        scatter2(ax, D, y, s=28, legend=(ax is axes[0]))
        sv = D[m.support_]
        ax.scatter(sv[:, 0], sv[:, 1], s=150, facecolors="none", edgecolors=GREEN,
                   linewidths=1.8, zorder=5)
        ax.set(xlabel="$X_1$",
               title=f"{ttl}: $\\beta$ points at ${ang:.1f}^\\circ$, width $={wid:.3f}$")
    axes[1].annotate("", xy=(1.9, -1.0), xytext=(3.40, 1.02),
                     arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5, ls="--",
                                     shrinkA=3, shrinkB=11))
    axes[1].text(2.65, 0.35, "moved", color=RED, fontsize=8, rotation=-35)
    axes[0].set_ylabel("$X_2$")
    fig.suptitle("Moving ONE observation swings the maximal margin hyperplane",
                 fontsize=10)
    save(fig, "ch09_instability.png")


# ------------------------------------------------------------------
# 6. The soft margin across sklearn's C
# ------------------------------------------------------------------
def fig_soft_C():
    X, y = sim_overlap()
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 5.4), sharex=True, sharey=True)
    for ax, C in zip(axes.ravel(), [0.01, 0.1, 1.0, 10.0]):
        m = SVC(kernel="linear", C=C).fit(X, y)
        w = m.coef_[0]
        wid = 2 / np.linalg.norm(w)
        slack = np.maximum(0.0, 1 - y * m.decision_function(X)).sum()
        boundary(ax, m, X, levels=(-1, 0, 1))
        scatter2(ax, X, y, s=22)
        sv = X[m.support_]
        ax.scatter(sv[:, 0], sv[:, 1], s=95, facecolors="none", edgecolors=GREEN,
                   linewidths=1.2, zorder=5)
        ax.set_title(f"sklearn $C={C:g}$:  {len(sv)} SVs,  width $={wid:.2f}$,  "
                     f"$\\sum\\xi_i={slack:.1f}$", fontsize=9)
    for ax in axes[1]:
        ax.set_xlabel("$X_1$")
    for ax in axes[:, 0]:
        ax.set_ylabel("$X_2$")
    fig.suptitle("Support vector classifier: raising sklearn's $C$ NARROWS the margin",
                 fontsize=10)
    save(fig, "ch09_soft_C.png")


# ------------------------------------------------------------------
# 7. Anatomy of the slacks
# ------------------------------------------------------------------
def fig_slack_anatomy():
    X, y = sim_overlap()
    m = SVC(kernel="linear", C=0.3).fit(X, y)
    f = m.decision_function(X)
    xi = np.maximum(0.0, 1 - y * f)
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    boundary(ax, m, X, levels=(-1, 0, 1))
    cats = [(xi == 0, "$\\xi_i=0$: outside the margin", "o", 26),
            ((xi > 0) & (xi <= 1), "$0<\\xi_i\\leq 1$: inside, right side", "^", 44),
            (xi > 1, "$\\xi_i>1$: misclassified", "X", 60)]
    for msk, lab, mk, s in cats:
        ax.scatter(X[msk, 0], X[msk, 1], marker=mk, s=s, zorder=4,
                   c=[ACCENT if t == -1 else ORANGE for t in y[msk]],
                   edgecolor="k", linewidth=0.5)
        # legend proxy in neutral grey: the marker means the slack, colour the class
        ax.scatter([], [], marker=mk, s=s, c=GREY, edgecolor="k", linewidth=0.5,
                   label=f"{lab} ($n={msk.sum()}$)")
    ax.legend(loc="upper left", fontsize=7, framealpha=0.92,
              title="marker $=$ slack, colour $=$ class", title_fontsize=7)
    ax.set(xlabel="$X_1$", ylabel="$X_2$",
           title=f"Three kinds of observation at sklearn $C=0.3$: "
                 f"$\\sum_i \\xi_i = {xi.sum():.1f}$")
    save(fig, "ch09_slack_anatomy.png")


# ------------------------------------------------------------------
# 8. A linear kernel cannot do this
# ------------------------------------------------------------------
def _circles():
    return make_circles(n_samples=300, factor=0.4, noise=0.15, random_state=0)


def fig_nonlinear_fail():
    X, y0 = _circles()
    y = np.where(y0 == 0, -1, 1)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6), sharey=True)
    # Both kernels are given their best 5-fold-CV hyperparameters, so the
    # comparison is fair: the linear kernel is not being handicapped.
    grids = [("linear", {"svc__C": np.logspace(-2, 2, 9)}),
             ("rbf", {"svc__C": np.logspace(-2, 2, 5), "svc__gamma": np.logspace(-3, 1, 5)})]
    for ax, (kern, grid) in zip(axes, grids):
        gs = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel=kern)),
                          grid, cv=5).fit(X, y)
        boundary(ax, gs.best_estimator_, X, pad=0.4)
        scatter2(ax, X, y, s=14, legend=(ax is axes[0]), loc="lower left")
        sym = {"C": "C", "gamma": r"\gamma"}
        bp = {k.replace("svc__", ""): v for k, v in gs.best_params_.items()}
        extra = ", ".join(f"${sym[k]}={v:g}$" for k, v in sorted(bp.items()))
        ax.set(xlabel="$X_1$",
               title=f"{kern} kernel, CV-tuned ({extra}):\nbest 5-fold CV accuracy "
                     f"{gs.best_score_:.3f}")
    axes[0].set_ylabel("$X_2$")
    fig.suptitle("Concentric classes: the linear kernel is near-useless, the radial "
                 "kernel is near-perfect", fontsize=10)
    save(fig, "ch09_nonlinear_fail.png")


# ------------------------------------------------------------------
# 9. Polynomial kernel: the degree d
# ------------------------------------------------------------------
def fig_poly_degree():
    X, y0 = _circles()
    y = np.where(y0 == 0, -1, 1)
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.2), sharey=True)
    for ax, d in zip(axes, [1, 2, 3]):
        pipe = make_pipeline(StandardScaler(),
                             SVC(kernel="poly", degree=d, coef0=1.0, C=1.0))
        cv = cross_val_score(pipe, X, y, cv=5).mean()
        pipe.fit(X, y)
        boundary(ax, pipe, X, pad=0.4)
        scatter2(ax, X, y, s=12)
        ax.set(xlabel="$X_1$", title=f"degree $d={d}$: CV {cv:.3f}")
    axes[0].set_ylabel("$X_2$")
    fig.suptitle(r"Polynomial kernel $K(x,x')=(1+\langle x,x'\rangle)^d$ on the "
                 "concentric data", fontsize=10)
    save(fig, "ch09_poly_degree.png")


# ------------------------------------------------------------------
# 10. Radial kernel: what gamma does
# ------------------------------------------------------------------
def fig_gamma():
    X, y0 = _circles()
    y = np.where(y0 == 0, -1, 1)
    fig, axes = plt.subplots(1, 4, figsize=(9.4, 2.9), sharey=True)
    for ax, g in zip(axes, [0.01, 0.1, 1.0, 100.0]):
        pipe = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma=g))
        cv = cross_val_score(pipe, X, y, cv=5).mean()
        pipe.fit(X, y)
        boundary(ax, pipe, X, pad=0.4)
        scatter2(ax, X, y, s=9)
        ax.set(xlabel="$X_1$",
               title=f"$\\gamma={g:g}$\nCV {cv:.3f}, train {pipe.score(X, y):.3f}")
    axes[0].set_ylabel("$X_2$")
    fig.suptitle(r"Radial kernel: small $\gamma$ = smooth and global, large $\gamma$ "
                 "= local islands round each point", fontsize=10)
    save(fig, "ch09_gamma.png")


# ------------------------------------------------------------------
# Heart data, prepared once
# ------------------------------------------------------------------
def heart_split():
    H = pd.read_csv(DATA / "Heart.csv", index_col=0).dropna().reset_index(drop=True)
    y = (H["AHD"] == "Yes").astype(int).values
    X = pd.get_dummies(H.drop(columns="AHD"), drop_first=True).astype(float).values
    return train_test_split(X, y, test_size=0.3, random_state=0)


HEART_C = np.array([0.01, 0.1, 1.0, 10.0, 100.0])
HEART_G = np.array([1e-4, 1e-3, 1e-2, 1e-1, 1.0])


# ------------------------------------------------------------------
# 11. Cross-validation heatmap over (C, gamma)
# ------------------------------------------------------------------
def fig_cv_heatmap():
    Xtr, Xte, ytr, yte = heart_split()
    gs = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel="rbf")),
                      {"svc__C": HEART_C, "svc__gamma": HEART_G}, cv=5).fit(Xtr, ytr)
    S = gs.cv_results_["mean_test_score"].reshape(len(HEART_C), len(HEART_G))
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.grid(False)
    im = ax.imshow(S, origin="lower", cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(HEART_G)), [f"$10^{{{int(np.log10(g))}}}$" for g in HEART_G])
    ax.set_yticks(range(len(HEART_C)), [f"$10^{{{int(np.log10(c))}}}$" for c in HEART_C])
    for i in range(len(HEART_C)):
        for j in range(len(HEART_G)):
            ax.text(j, i, f"{S[i, j]:.3f}", ha="center", va="center", fontsize=7.5,
                    color="white" if S[i, j] < S.max() - 0.12 else "black")
    bi, bj = np.unravel_index(S.argmax(), S.shape)
    ax.add_patch(plt.Rectangle((bj - 0.5, bi - 0.5), 1, 1, fill=False,
                               edgecolor=RED, lw=2.4))
    fig.colorbar(im, ax=ax, label="5-fold CV accuracy")
    ax.set(xlabel=r"$\gamma$", ylabel="sklearn $C$",
           title=f"Heart training set ($n={len(ytr)}$): CV accuracy, best "
                 f"$C={HEART_C[bi]:g}$, $\\gamma={HEART_G[bj]:g}$ at {S.max():.3f}")
    save(fig, "ch09_cv_heatmap.png")


# ------------------------------------------------------------------
# 12. Heart: gamma turns training AUC into overfitting
# ------------------------------------------------------------------
def fig_heart_gamma_auc():
    Xtr, Xte, ytr, yte = heart_split()
    gammas = np.logspace(-4, 0, 9)
    tr, te = [], []
    for g in gammas:
        m = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma=g)).fit(Xtr, ytr)
        tr.append(roc_auc_score(ytr, m.decision_function(Xtr)))
        te.append(roc_auc_score(yte, m.decision_function(Xte)))
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.semilogx(gammas, tr, "o-", color=ORANGE, label="training AUC")
    ax.semilogx(gammas, te, "s--", color=ACCENT, label="test AUC")
    j = int(np.argmax(te))
    ax.axvline(gammas[j], color=GREY, ls=":", lw=1.2)
    ax.annotate(f"best test AUC {te[j]:.3f}\nat $\\gamma={gammas[j]:.2g}$",
                xy=(gammas[j], te[j]), xytext=(8, -30), textcoords="offset points",
                fontsize=8, color=ACCENT)
    ax.legend(fontsize=8)
    ax.set(xlabel=r"radial kernel $\gamma$ (log scale)", ylabel="ROC AUC",
           title="Heart data, radial SVM at $C=1$: training AUC rises to 1, test AUC falls")
    save(fig, "ch09_heart_gamma_auc.png")


# ------------------------------------------------------------------
# 13. ROC: SVM vs logistic regression vs random forest
# ------------------------------------------------------------------
def fig_roc():
    Xtr, Xte, ytr, yte = heart_split()
    gs = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel="rbf")),
                      {"svc__C": HEART_C, "svc__gamma": HEART_G}, cv=5).fit(Xtr, ytr)
    svm_rbf = gs.best_estimator_
    gl = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel="linear")),
                      {"svc__C": HEART_C}, cv=5).fit(Xtr, ytr)
    svm_lin = gl.best_estimator_
    logit = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)).fit(Xtr, ytr)
    rf = RandomForestClassifier(n_estimators=500, random_state=0).fit(Xtr, ytr)
    curves = [
        ("radial SVM (CV-tuned)", svm_rbf.decision_function(Xte), ORANGE, "-"),
        (f"linear SVM (CV-tuned, $C={gl.best_params_['svc__C']:g}$)",
         svm_lin.decision_function(Xte), GREEN, "--"),
        ("logistic regression", logit.predict_proba(Xte)[:, 1], ACCENT, "-"),
        ("random forest (500)", rf.predict_proba(Xte)[:, 1], GREY, ":"),
    ]
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    for lab, score, col, ls in curves:
        fpr, tpr, _ = roc_curve(yte, score)
        ax.plot(fpr, tpr, ls, color=col, lw=1.7,
                label=f"{lab}  AUC $={roc_auc_score(yte, score):.3f}$")
    ax.plot([0, 1], [0, 1], color="k", lw=0.8, ls=":", alpha=0.6)
    ax.legend(loc="lower right", fontsize=7.5)
    ax.set(xlabel="false positive rate", ylabel="true positive rate",
           title=f"Heart test set ($n={len(yte)}$): ranking quality is a near tie")
    save(fig, "ch09_roc.png")


# ------------------------------------------------------------------
# 14. Hinge loss vs logistic loss
# ------------------------------------------------------------------
def fig_losses():
    t = np.linspace(-3, 3, 601)
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.plot(t, np.maximum(0, 1 - t), color=ORANGE, lw=2.0,
            label=r"hinge  $\max(0,\,1-y f)$   (SVM)")
    ax.plot(t, np.log(1 + np.exp(-t)), color=ACCENT, lw=2.0, ls="--",
            label=r"logistic  $\log(1+e^{-y f})$   (Ch. 4)")
    ax.plot(t, (t <= 0).astype(float), color=GREY, lw=1.2, ls=":",
            label=r"0/1 loss  $\mathbf{1}\{y f\leq 0\}$")
    ax.axvline(1, color=GREEN, lw=1.0, ls="-.")
    ax.annotate("hinge is exactly 0\nfor $yf\\geq 1$", xy=(1.05, 0.55), fontsize=8,
                color=GREEN)
    ax.legend(fontsize=8, loc="upper right")
    ax.set(xlabel=r"margin $y\,f(x)$", ylabel="loss", ylim=(-0.05, 3.2),
           title="The honest comparison: SVMs and logistic regression differ in their loss")
    save(fig, "ch09_losses.png")


# ------------------------------------------------------------------
# 15. Appendix: distance from a point to a hyperplane
# ------------------------------------------------------------------
def fig_x_margin_geometry():
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    w = np.array([1.0, 2.0])
    b = -2.0
    xs = np.linspace(-1, 4, 100)
    ax.plot(xs, -(b + w[0] * xs) / w[1], color="k", lw=1.8)
    ax.text(3.2, -(b + w[0] * 3.2) / w[1] + 0.12, r"$\beta_0+\beta^\top x=0$", fontsize=9)
    x0 = np.array([3.0, 2.2])
    n = w / np.linalg.norm(w)
    d = (b + w @ x0) / np.linalg.norm(w)
    foot = x0 - d * n
    ax.scatter(*x0, c=ORANGE, s=48, zorder=4)
    ax.annotate(r"$x_0$", x0, textcoords="offset points", xytext=(6, 4), fontsize=9)
    ax.plot([x0[0], foot[0]], [x0[1], foot[1]], color=RED, lw=1.6)
    ax.annotate("", xy=foot + 0.8 * n, xytext=foot,
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
    ax.text(*(foot + 0.85 * n), r"$\beta/\|\beta\|$", color=GREEN, fontsize=9)
    ax.text(*((x0 + foot) / 2 + np.array([0.12, -0.05])),
            r"$\dfrac{|\beta_0+\beta^\top x_0|}{\|\beta\|}=%.3f$" % abs(d),
            color=RED, fontsize=9)
    ax.set(xlabel="$X_1$", ylabel="$X_2$", xlim=(-1, 4.2), ylim=(-0.6, 3.2),
           title="Signed distance: divide the score by the norm of the coefficients")
    ax.set_aspect("equal")
    save(fig, "ch09_x_margin_geometry.png")


# ------------------------------------------------------------------
# 16. Appendix: epsilon-insensitive loss (support vector regression)
# ------------------------------------------------------------------
def fig_x_svr():
    r = np.linspace(-3, 3, 601)
    eps = 1.0
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.plot(r, np.maximum(0, np.abs(r) - eps), color=ORANGE, lw=2.0,
            label=r"$\epsilon$-insensitive, $\epsilon=1$")
    ax.plot(r, r ** 2, color=ACCENT, lw=1.4, ls="--", label="squared error (Ch. 3)")
    ax.axvspan(-eps, eps, color=GREEN, alpha=0.12)
    ax.text(0, 1.6, "free tube: zero loss", ha="center", fontsize=8, color=GREEN)
    ax.legend(fontsize=8)
    ax.set(xlabel=r"residual $y-f(x)$", ylabel="loss", ylim=(-0.1, 3.0),
           title="Support vector regression swaps squared error for a tolerance tube")
    save(fig, "ch09_x_svr.png")


if __name__ == "__main__":
    fig_hyperplane()
    fig_many_hyperplanes()
    fig_maxmargin()
    fig_nonseparable()
    fig_instability()
    fig_soft_C()
    fig_slack_anatomy()
    fig_nonlinear_fail()
    fig_poly_degree()
    fig_gamma()
    fig_cv_heatmap()
    fig_heart_gamma_auc()
    fig_roc()
    fig_losses()
    fig_x_margin_geometry()
    fig_x_svr()

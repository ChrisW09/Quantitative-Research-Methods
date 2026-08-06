"""Generate the matplotlib figures for the Chapter 12 deck (Unsupervised Learning).

Every figure is computed from the bundled course datasets (``USArrests.csv``,
``Ch12Ex13.csv``) or from a clearly labelled, seeded simulation --- nothing is
sketched by hand, and every number quoted on a slide comes out of this file.
Run from anywhere:

    python Chapters/chapter_12/make_figures.py

Output: Chapters/chapter_12/images/ch12_*.png at 150 dpi, matching the figure
size and resolution used by the other decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
CRIMSON = "#B03030"
RNG = np.random.default_rng(2024)

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


# ---------------------------------------------------------------- data ------
# USArrests.csv carries the state names in the first column.
USA = pd.read_csv(DATA / "USArrests.csv", index_col=0)
XS = StandardScaler().fit_transform(USA)          # standardised: each var. var = 1
XC = (USA - USA.mean()).to_numpy()                # centred only

PCS = PCA().fit(XS)                               # scaled PCA
ZS = PCS.transform(XS)
PCU = PCA().fit(XC)                               # unscaled PCA
ZU = PCU.transform(XC)

# Ch12Ex13: 1000 genes (rows) x 40 tissue samples (columns), no header row.
GENE = pd.read_csv(DATA / "Ch12Ex13.csv", header=None).to_numpy()
GX = GENE.T                                       # 40 samples x 1000 genes
GTRUTH = np.array([0] * 20 + [1] * 20)            # first 20 healthy, last 20 diseased


# 1 -- PC1 as the direction of maximum variance -------------------------------
def fig_pc1_direction():
    x = XS[:, 0]                                   # Murder (standardised)
    y = XS[:, 3]                                   # Rape (standardised)
    A = np.column_stack([x, y])
    p = PCA().fit(A)
    v1, v2 = p.components_[0], p.components_[1]
    z1 = A @ v1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.6))

    ax1.scatter(x, y, s=14, color=ACCENT, alpha=0.75)
    for v, c, lab, s in [(v1, ORANGE, "PC1 direction", 2.6), (v2, GREEN, "PC2 direction", 1.6)]:
        ax1.annotate("", xy=(s * v[0], s * v[1]), xytext=(-s * v[0], -s * v[1]),
                     arrowprops=dict(arrowstyle="<->", color=c, lw=2))
        ax1.text(s * v[0] * 1.08, s * v[1] * 1.08, lab, color=c, fontsize=8,
                 ha="center", va="center")
    # projection segments onto PC1
    proj = np.outer(z1, v1)
    for i in range(0, len(x), 2):
        ax1.plot([x[i], proj[i, 0]], [y[i], proj[i, 1]], color=GREY, lw=0.5, alpha=0.7)
    ax1.set(xlabel="Murder (standardised)", ylabel="Rape (standardised)",
            title="Two standardised variables and the two component directions")
    ax1.set_aspect("equal")

    ax2.hist(z1, bins=14, color=ORANGE, alpha=0.8, edgecolor="white", linewidth=0.4,
             label=f"PC1 scores, var = {z1.var(ddof=1):.2f}")
    z2 = A @ v2
    ax2.hist(z2, bins=14, color=GREEN, alpha=0.55, edgecolor="white", linewidth=0.4,
             label=f"PC2 scores, var = {z2.var(ddof=1):.2f}")
    ax2.set(xlabel="score", ylabel="count",
            title="PC1 spreads the data out; PC2 keeps what is left")
    ax2.legend(fontsize=7.5, frameon=False)

    save(fig, "ch12_pc1_direction.png")


# 2 -- The biplot -------------------------------------------------------------
def fig_biplot():
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.scatter(ZS[:, 0], ZS[:, 1], s=10, color=ACCENT, alpha=0.6)
    for i, name in enumerate(USA.index):
        ax.annotate(name, (ZS[i, 0], ZS[i, 1]), fontsize=5.2, color=GREY,
                    xytext=(2, 2), textcoords="offset points")
    scale = 2.6
    for j, var in enumerate(USA.columns):
        dx, dy = scale * PCS.components_[0, j], scale * PCS.components_[1, j]
        ax.annotate("", xy=(dx, dy), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
        ax.text(dx * 1.24, dy * 1.24, var, color=ORANGE, fontsize=9, fontweight="bold",
                ha="center", va="center")
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.set(xlabel="PC1 score  (62.0% of variance)", ylabel="PC2 score  (24.7%)",
           title="USArrests biplot: standardised data, PC1--PC2")
    ax.set_xlim(-3.6, 3.9)
    ax.set_ylim(-3.0, 3.1)          # room for the UrbanPop label, clear of the title
    save(fig, "ch12_biplot.png")


# 3 -- Scree plot and cumulative PVE -----------------------------------------
def fig_scree():
    pve = PCS.explained_variance_ratio_
    k = np.arange(1, len(pve) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.3))

    ax1.plot(k, pve, "o-", color=ACCENT, lw=1.8, ms=6)
    for i, v in enumerate(pve):
        ax1.annotate(f"{v:.3f}", (k[i], v), fontsize=8, xytext=(4, 5),
                     textcoords="offset points", color=ACCENT)
    ax1.set(xlabel="principal component $m$", ylabel="PVE$_m$",
            title="Scree plot: proportion of variance explained", xticks=k,
            ylim=(0, 0.72))

    ax2.plot(k, np.cumsum(pve), "s-", color=ORANGE, lw=1.8, ms=6)
    for i, v in enumerate(np.cumsum(pve)):
        ax2.annotate(f"{v:.3f}", (k[i], v), fontsize=8, xytext=(4, -12),
                     textcoords="offset points", color=ORANGE)
    ax2.axhline(0.9, color=GREY, ls="--", lw=1)
    ax2.text(1.05, 0.915, "90% reference line", color=GREY, fontsize=8)
    ax2.set(xlabel="number of components $M$", ylabel="cumulative PVE",
            title="Cumulative PVE: 2 components carry 86.8%", xticks=k,
            ylim=(0.5, 1.04))
    save(fig, "ch12_scree.png")


# 4 -- Scaled vs unscaled PCA: the most important figure in the chapter -------
def fig_scaling():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0))

    for ax, Z, comps, pve, title, scale in [
        (ax1, ZS, PCS.components_, PCS.explained_variance_ratio_,
         "Standardised (each variable variance 1)", 2.6),
        (ax2, ZU, PCU.components_, PCU.explained_variance_ratio_,
         "Raw units (no scaling)", 150.0),
    ]:
        ax.scatter(Z[:, 0], Z[:, 1], s=9, color=ACCENT, alpha=0.55)
        for j, var in enumerate(USA.columns):
            dx, dy = scale * comps[0, j], scale * comps[1, j]
            ax.annotate("", xy=(dx, dy), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
            ax.text(dx * 1.10, dy * 1.10, var, color=ORANGE, fontsize=8.5,
                    fontweight="bold", ha="center", va="center")
        ax.axhline(0, color=GREY, lw=0.6)
        ax.axvline(0, color=GREY, lw=0.6)
        ax.set(xlabel=f"PC1  ({100 * pve[0]:.1f}% of variance)",
               ylabel=f"PC2  ({100 * pve[1]:.1f}%)", title=title)

    ax1.set_xlim(-3.6, 3.9)
    ax1.set_ylim(-3.0, 2.9)
    ax2.set_xlim(-190, 210)
    ax2.set_ylim(-115, 165)
    save(fig, "ch12_scaling.png")


# 5 -- Variable variances in raw units (why Assault wins) ---------------------
def fig_variances():
    v = USA.var().to_numpy()
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    bars = ax.bar(USA.columns, v, color=[ORANGE if c == "Assault" else ACCENT
                                         for c in USA.columns], alpha=0.85)
    ax.set_yscale("log")
    for b, val in zip(bars, v):
        ax.annotate(f"{val:,.1f}", (b.get_x() + b.get_width() / 2, val), fontsize=8.5,
                    ha="center", va="bottom")
    ax.set(ylabel="sample variance (log scale)",
           title="USArrests in raw units: Assault has 366x the variance of Murder")
    ax.set_ylim(5, 40000)
    save(fig, "ch12_variances.png")


# 6 -- K-means at K = 2, 3, 4 ------------------------------------------------
def fig_kmeans_K():
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.2), sharex=True, sharey=True)
    cols = [ACCENT, ORANGE, GREEN, CRIMSON]
    for ax, K in zip(axes, [2, 3, 4]):
        km = KMeans(n_clusters=K, n_init=50, random_state=0).fit(XS)
        for k in range(K):
            m = km.labels_ == k
            ax.scatter(ZS[m, 0], ZS[m, 1], s=18, color=cols[k], alpha=0.8,
                       label=f"$n_{k + 1}$ = {m.sum()}")
        ax.set(xlabel="PC1 score",
               title=f"$K$ = {K}:  $W$ = {km.inertia_:.1f}   ({1 - km.inertia_ / 200:.0%} of SS)")
        ax.legend(fontsize=7, frameon=False, loc="lower right")
    axes[0].set(ylabel="PC2 score")
    save(fig, "ch12_kmeans_K.png")


# 7 -- Local optima: same K, different starts --------------------------------
def fig_local_optima():
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.4), sharex=True, sharey=True)
    cols = [ACCENT, ORANGE, GREEN, CRIMSON]
    for ax, seed in zip(axes, [1, 18]):     # best and worst of seeds 0..19
        km = KMeans(n_clusters=4, n_init=1, random_state=seed).fit(XS)
        sizes = np.bincount(km.labels_, minlength=4)
        for k in range(4):
            m = km.labels_ == k
            ax.scatter(ZS[m, 0], ZS[m, 1], s=20, color=cols[k], alpha=0.85)
            ax.scatter(*(km.cluster_centers_[k] - XS.mean(0)) @ PCS.components_[:2].T,
                       marker="X", s=90, color=cols[k], edgecolor="black", linewidth=0.6)
        ax.set(xlabel="PC1 score",
               title=f"random_state={seed}, n_init=1:  $W$ = {km.inertia_:.3f}\n"
                     f"cluster sizes {sizes.tolist()}")
    axes[0].set(ylabel="PC2 score")
    save(fig, "ch12_local_optima.png")


# 8 -- Choosing K: within-cluster SS and silhouette, data vs pure noise -------
def fig_choose_K():
    noise = np.random.default_rng(2024).normal(size=(200, 2))
    Ks = np.arange(1, 9)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.3))
    for X, lab, col in [(XS, "USArrests (standardised)", ACCENT),
                        (noise, "pure Gaussian noise, $n$=200", CRIMSON)]:
        w = np.array([KMeans(n_clusters=K, n_init=50, random_state=0).fit(X).inertia_
                      for K in Ks])
        ax1.plot(Ks, w / w[0], "o-", color=col, lw=1.7, ms=5, label=lab)
        s = [silhouette_score(X, KMeans(n_clusters=K, n_init=50, random_state=0)
                              .fit_predict(X)) for K in Ks[1:]]
        ax2.plot(Ks[1:], s, "s-", color=col, lw=1.7, ms=5, label=lab)
    ax1.set(xlabel="$K$", ylabel="$W(K)\\,/\\,W(1)$",
            title="Within-cluster SS always falls --- and bends in noise too")
    ax1.legend(fontsize=7.5, frameon=False)
    ax2.set(xlabel="$K$", ylabel="mean silhouette width",
            title="Silhouette: no honest warning that noise has no clusters",
            ylim=(0, 0.5))
    ax2.legend(fontsize=7.5, frameon=False)
    save(fig, "ch12_choose_K.png")


# 9 -- Clusters in pure noise vs clusters that are really there ---------------
def fig_noise_clusters():
    rng = np.random.default_rng(2024)
    noise = rng.normal(size=(200, 2))
    mu = np.array([[-2.5, 0.0], [2.5, 0.0], [0.0, 2.5]])
    lab = rng.integers(0, 3, 200)
    real = mu[lab] + rng.normal(size=(200, 2))

    cols = [ACCENT, ORANGE, GREEN]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    for ax, X, name in [(ax1, noise, "Pure noise: one distribution, no clusters"),
                        (ax2, real, "Three real clusters")]:
        km = KMeans(n_clusters=3, n_init=50, random_state=0).fit(X)
        for k in range(3):
            m = km.labels_ == k
            ax.scatter(X[m, 0], X[m, 1], s=14, color=cols[k], alpha=0.8)
        sil = silhouette_score(X, km.labels_)
        ax.set(xlabel="$x_1$", ylabel="$x_2$",
               title=f"{name}\n$K$=3: $W$ = {km.inertia_:.1f}, silhouette = {sil:.3f}")
    save(fig, "ch12_noise_clusters.png")


# 10 -- One data set, two linkages ------------------------------------------
def fig_dendro_linkage():
    labels = USA.index.tolist()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for ax, method in [(ax1, "complete"), (ax2, "single")]:
        Z = linkage(XS, method=method)
        dendrogram(Z, labels=labels, leaf_font_size=3.6, ax=ax,
                   color_threshold=0.7 * Z[-1, 2], above_threshold_color=GREY)
        sizes = np.bincount(fcluster(Z, 3, "maxclust"))[1:]
        ax.set(title=f"{method} linkage --- cut into 3: sizes {sizes.tolist()}",
               ylabel="merge height (Euclidean)")
        ax.grid(False)
        ax.tick_params(axis="x", length=0)
    save(fig, "ch12_dendro_linkage.png")


# 11 -- Cutting the tree ------------------------------------------------------
def fig_dendro_cut():
    Z = linkage(XS, method="complete")
    fig, ax = plt.subplots(figsize=(9.4, 3.5))
    dendrogram(Z, labels=USA.index.tolist(), leaf_font_size=4.4, ax=ax,
               color_threshold=4.4, above_threshold_color=GREY)
    for h, k, col in [(4.9, 2, ORANGE), (4.2, 3, GREEN)]:
        ax.axhline(h, color=col, ls="--", lw=1.4)
        sizes = np.bincount(fcluster(Z, k, "maxclust"))[1:]
        ax.text(0.4, h + 0.08, f"cut at {h} -> {k} clusters, sizes {sizes.tolist()}",
                color=col, fontsize=8,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8))
    ax.set(ylabel="merge height (Euclidean)",
           title="Complete linkage on standardised USArrests: the cut chooses $K$")
    ax.grid(False)
    ax.tick_params(axis="x", length=0)
    save(fig, "ch12_dendro_cut.png")


# 12 -- Horizontal position carries no information ---------------------------
def fig_dendro_swap():
    rng = np.random.default_rng(7)
    X = np.vstack([rng.normal([-2, 0], 0.45, (4, 2)),
                   rng.normal([2, 0], 0.45, (4, 2))])
    names = list("ABCDEFGH")
    Z = linkage(X, method="complete")
    Zflip = Z.copy()
    Zflip[:, [0, 1]] = Zflip[:, [1, 0]]     # same tree, every pair of children swapped
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.0))
    for ax, Zi, title in [
        (ax1, Z, "Default leaf order"),
        (ax2, Zflip, "Same tree, every branch pair swapped"),
    ]:
        d = dendrogram(Zi, labels=names, ax=ax, leaf_font_size=9,
                       color_threshold=0.6 * Zi[-1, 2], above_threshold_color=GREY)
        ax.set(title=f"{title}\nleaves: {' '.join(d['ivl'])}",
               ylabel="merge height")
        ax.grid(False)
        ax.tick_params(axis="x", length=0)
    save(fig, "ch12_dendro_swap.png")


# 13 -- The dissimilarity measure matters more than the algorithm ------------
def fig_corr_vs_eucl():
    names = [f"H{i + 1}" for i in range(20)] + [f"D{i + 1}" for i in range(20)]
    Dcorr = 1 - np.corrcoef(GX)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    for ax, Z, name in [
        (ax1, linkage(GX, method="complete"), "Euclidean distance"),
        (ax2, linkage(squareform(Dcorr, checks=False), method="complete"),
         "correlation-based, $1-r$"),
    ]:
        dendrogram(Z, labels=names, leaf_font_size=4.6, ax=ax,
                   color_threshold=0.999 * Z[-1, 2], above_threshold_color=GREY)
        lab = fcluster(Z, 2, "maxclust")
        ari = adjusted_rand_score(GTRUTH, lab)
        ax.set(title=f"complete linkage, {name}\ncut into 2: sizes "
                     f"{np.bincount(lab)[1:].tolist()}, ARI vs truth = {ari:.3f}",
               ylabel="merge height")
        ax.grid(False)
        ax.tick_params(axis="x", length=0)
    save(fig, "ch12_corr_vs_eucl.png")


# 14 -- PCA in p >> n: the gene data ----------------------------------------
def fig_gene_pca():
    p = PCA().fit(GX - GX.mean(0))
    Z = p.transform(GX - GX.mean(0))
    pve = p.explained_variance_ratio_
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.3))
    ax1.scatter(Z[:20, 0], Z[:20, 1], s=26, color=ACCENT, alpha=0.85, label="healthy")
    ax1.scatter(Z[20:, 0], Z[20:, 1], s=26, color=CRIMSON, alpha=0.85, marker="^",
                label="diseased")
    ax1.set(xlabel=f"PC1  ({100 * pve[0]:.1f}%)", ylabel=f"PC2  ({100 * pve[1]:.1f}%)",
            title="40 tissue samples, 1000 genes: PC1 finds the group split")
    ax1.legend(fontsize=8, frameon=False)
    k = np.arange(1, 21)
    ax2.bar(k, pve[:20], color=ACCENT, alpha=0.85)
    ax2.set(xlabel="principal component $m$", ylabel="PVE$_m$", xticks=[1, 5, 10, 15, 20],
            title=f"No dominant components: first 20 carry only "
                  f"{100 * pve[:20].sum():.0f}%")
    save(fig, "ch12_gene_pca.png")


# 15 -- Exercise figure: two local optima on four points ---------------------
def fig_x_rectangle():
    X = np.array([[0.0, 0.0], [0.0, 1.0], [4.0, 0.0], [4.0, 1.0]])
    inits = [np.array([[0.0, 0.5], [4.0, 0.5]]), np.array([[2.0, 0.0], [2.0, 1.0]])]
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 2.9), sharex=True, sharey=True)
    cols = [ACCENT, ORANGE]
    for ax, init, tag in zip(axes, inits, ["vertical split", "horizontal split"]):
        km = KMeans(n_clusters=2, init=init, n_init=1).fit(X)
        for k in range(2):
            m = km.labels_ == k
            ax.scatter(X[m, 0], X[m, 1], s=90, color=cols[k], zorder=3)
            ax.scatter(*km.cluster_centers_[k], marker="X", s=120, color=cols[k],
                       edgecolor="black", linewidth=0.7, zorder=4)
        ax.set(xlabel="$x_1$", xlim=(-1.2, 5.2), ylim=(-0.8, 1.8),
               title=f"{tag}:  $W$ = {km.inertia_:.1f}")
    axes[0].set(ylabel="$x_2$")
    for ax, txt in zip(axes, ["global optimum", "stable, but 16x worse"]):
        ax.text(2.0, 1.5, txt, ha="center", fontsize=8.5, color=GREY)
    save(fig, "ch12_x_rectangle.png")


# 16 -- Exercise / practice figure: one outlier hijacks a cluster ------------
def fig_x_outlier():
    rng = np.random.default_rng(2024)
    X = np.vstack([rng.normal([-2, 0], 0.6, (60, 2)), rng.normal([2, 0], 0.6, (60, 2))])
    Xo = np.vstack([X, [[9.0, 7.0]]])
    cols = [ACCENT, ORANGE, GREEN]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.2))
    for ax, D, name in [(ax1, X, "Clean data"), (ax2, Xo, "One outlier added")]:
        km = KMeans(n_clusters=3, n_init=50, random_state=0).fit(D)
        for k in range(3):
            m = km.labels_ == k
            ax.scatter(D[m, 0], D[m, 1], s=14, color=cols[k], alpha=0.85,
                       label=f"$n$ = {m.sum()}")
        ax.set(xlabel="$x_1$", ylabel="$x_2$",
               title=f"{name}, $K$=3: sizes "
                     f"{np.bincount(km.labels_).tolist()}")
        ax.legend(fontsize=7, frameon=False)
    save(fig, "ch12_x_outlier.png")


# 17 -- Appendix: the silhouette ---------------------------------------------
def fig_x_silhouette():
    from sklearn.metrics import silhouette_samples
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.2), sharex=True)
    cols = [ACCENT, ORANGE, GREEN, CRIMSON]
    for ax, K in zip(axes, [2, 4]):
        km = KMeans(n_clusters=K, n_init=50, random_state=0).fit(XS)
        s = silhouette_samples(XS, km.labels_)
        y = 0
        for k in range(K):
            v = np.sort(s[km.labels_ == k])
            ax.barh(np.arange(y, y + len(v)), v, height=1.0, color=cols[k], alpha=0.85)
            y += len(v) + 3
        ax.axvline(s.mean(), color=GREY, ls="--", lw=1.2)
        ax.set(xlabel="silhouette width $s_i$",
               title=f"$K$ = {K}: mean $s$ = {s.mean():.3f}")
        ax.set_yticks([])
    axes[0].set(ylabel="observations, grouped by cluster")
    save(fig, "ch12_x_silhouette.png")




def fig_method_agreement():
    """K-means and complete-linkage on scaled USArrests: do they agree?

    A 4x4 crosstab of cluster labels, the same validation move the lab makes
    on NCI60 (clusters against cancer types). ARI quantifies the agreement.
    """
    df = pd.read_csv(DATA / "USArrests.csv", index_col=0)
    X = StandardScaler().fit_transform(df.values)

    km = KMeans(n_clusters=4, n_init=20, random_state=2024).fit_predict(X)
    hc = fcluster(linkage(X, method="complete"), t=4, criterion="maxclust") - 1

    tab = np.zeros((4, 4), dtype=int)
    for a, b in zip(km, hc):
        tab[a, b] += 1
    ari = adjusted_rand_score(km, hc)

    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    im = ax.imshow(tab, cmap=plt.cm.Blues, vmin=0, vmax=tab.max())
    for i in range(4):
        for j in range(4):
            ax.text(j, i, tab[i, j], ha="center", va="center", fontsize=10,
                    color="white" if tab[i, j] > tab.max() * 0.6 else "#333333")
    ax.set_xticks(range(4), [f"H{j+1}" for j in range(4)])
    ax.set_yticks(range(4), [f"K{i+1}" for i in range(4)])
    ax.set_xlabel("complete linkage, cut at 4 clusters")
    ax.set_ylabel("$K$-means, $K=4$")
    ax.set_title(f"states per label pair — ARI = {ari:.2f}", fontsize=9)
    ax.grid(False)
    save(fig, "ch12_method_agreement.png")
    print("ch12_method_agreement: ARI =", round(ari, 3), "| row sums", tab.sum(1).tolist())


if __name__ == "__main__":
    fig_pc1_direction()
    fig_biplot()
    fig_scree()
    fig_scaling()
    fig_variances()
    fig_kmeans_K()
    fig_local_optima()
    fig_choose_K()
    fig_noise_clusters()
    fig_dendro_linkage()
    fig_dendro_cut()
    fig_dendro_swap()
    fig_corr_vs_eucl()
    fig_gene_pca()
    fig_x_rectangle()
    fig_x_outlier()
    fig_x_silhouette()
    fig_method_agreement()

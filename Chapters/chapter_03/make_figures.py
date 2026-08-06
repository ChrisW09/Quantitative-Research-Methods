"""Generate the computed matplotlib figures for the Chapter 3 deck (Linear Regression).

Everything is computed exactly --- nothing is sketched by hand, and every
number quoted on the slide comes out of this file. The counts match the
chapter 6 lab's 'How many models did we skip?' section. Run from anywhere:

    python Chapters/chapter_03/make_figures.py

Output: Chapters/chapter_03/images/ch03_*.png at 150 dpi, matching the figure
size and resolution used by the other decks. Existing figures are not touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#C62828"

# The figures below are shown at 0.9-0.96\textwidth on a 16:9 slide, so their
# text is set a few points larger than the module default; applied per figure
# with plt.rc_context so the other figures keep the house rcParams.
SLIDE_RC = {"font.size": 13, "axes.titlesize": 14}

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




DATA = HERE.parents[1] / "ALL CSV FILES - 2nd Edition"

def fig_ci_vs_pi():
    """95% confidence band vs 95% prediction band for mpg ~ horsepower on Auto.

    Computed with statsmodels' exact formulas; the same fit the lab runs.
    """
    import statsmodels.api as sm
    df = pd.read_csv(DATA / "Auto.csv", na_values="?").dropna()
    x = df["horsepower"].astype(float).values
    y = df["mpg"].values
    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit()

    grid = np.linspace(x.min(), x.max(), 120)
    pred = res.get_prediction(sm.add_constant(grid)).summary_frame(alpha=0.05)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.scatter(x, y, s=7, alpha=0.30, color=GREY, edgecolors="none", zorder=2)
    ax.fill_between(grid, pred["obs_ci_lower"], pred["obs_ci_upper"],
                    color=ORANGE, alpha=0.18, zorder=1)
    ax.fill_between(grid, pred["mean_ci_lower"], pred["mean_ci_upper"],
                    color=ACCENT, alpha=0.45, zorder=3)
    ax.plot(grid, pred["mean"], color=ACCENT, lw=2, zorder=4)

    ax.annotate("95% confidence band:\nwhere the average mpg lies", xy=(60, 30.2),
                xytext=(46, 6.5), fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate("95% prediction band:\nwhere a single car lies", xy=(170, 15.5),
                xytext=(150, 34), fontsize=8.5, color="#8A4513",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.set_xlabel("horsepower"); ax.set_ylabel("mpg")
    save(fig, "ch03_ci_vs_pi.png")
    i = 60  # report widths mid-range
    print("ch03_ci_vs_pi.png: CI width", round(pred["mean_ci_upper"][i]-pred["mean_ci_lower"][i], 2),
          "PI width", round(pred["obs_ci_upper"][i]-pred["obs_ci_lower"][i], 2),
          "at hp", round(grid[i]))


def _advertising():
    """Advertising.csv --- 200 markets, index column is the market id."""
    return pd.read_csv(DATA / "Advertising.csv", index_col=0)


def fig_three_predictors():
    """Three simple regressions of sales on each medium (Advertising).

    Slide 'The raw data: sales against each medium'. The panel titles are the
    fitted slope and R^2 of each *simple* regression, printed below so the
    numbers on the figure can be checked against the deck.
    """
    import statsmodels.api as sm
    ad = _advertising()
    panels = [("TV", "TV budget (\\$1k)", ACCENT),
              ("radio", "radio budget (\\$1k)", GREEN),
              ("newspaper", "newspaper budget (\\$1k)", ORANGE)]

    with plt.rc_context(SLIDE_RC):
        fig, axes = plt.subplots(1, 3, figsize=(10.0, 3.83), sharey=True)
        for ax, (col, xlab, colour) in zip(axes, panels):
            x = ad[col].values
            res = sm.OLS(ad["sales"].values, sm.add_constant(x)).fit()
            b0, b1 = res.params
            ax.scatter(x, ad["sales"], s=20, color=colour, alpha=0.55,
                       edgecolors="none", zorder=2)
            grid = np.linspace(x.min(), x.max(), 50)
            ax.plot(grid, b0 + b1 * grid, color=RED, lw=2.2, zorder=3)
            ax.set_title(f"sales ~ {col}\nslope={b1:.3f}, $R^2$={res.rsquared:.2f}",
                         fontsize=13)
            ax.set_xlabel(xlab)
            ax.grid(False)
            print(f"ch03_three_predictors.png: {col} slope {b1:.4f} "
                  f"R2 {res.rsquared:.3f}")
        axes[0].set_ylabel("sales (1,000s)")
        fig.suptitle("Simple linear regressions: sales on each medium",
                     fontsize=14)
        save(fig, "ch03_three_predictors.png")


def fig_ols_residuals():
    """ISLP Figure 3.1 recreated: sales ~ TV with every residual drawn.

    Appendix slide 'Recreating Figure 3.1 on the Advertising data'. The legend
    quotes the fitted line, which must read yhat = 7.03 + 0.0475 x.
    """
    import statsmodels.api as sm
    ad = _advertising()
    x, y = ad["TV"].values, ad["sales"].values
    res = sm.OLS(y, sm.add_constant(x)).fit()
    b0, b1 = res.params
    fitted = b0 + b1 * x

    with plt.rc_context(SLIDE_RC):
        fig, ax = plt.subplots(figsize=(7.0, 4.2))
        ax.vlines(x, np.minimum(y, fitted), np.maximum(y, fitted),
                  color=RED, lw=0.9, alpha=0.55, zorder=2)
        ax.scatter(x, y, s=22, color=ACCENT, edgecolors="white", linewidths=0.5,
                   label="markets", zorder=4)
        grid = np.linspace(x.min(), x.max(), 50)
        ax.plot(grid, b0 + b1 * grid, color=ORANGE, lw=3.0, zorder=3,
                label=f"OLS fit: $\\hat y = {b0:.2f} + {b1:.4f}\\,x$")
        ax.set_xlabel("TV advertising budget (\\$1,000s)")
        ax.set_ylabel("sales (1,000s units)")
        ax.set_title("Sales vs. TV: least-squares fit and residuals")
        ax.legend(loc="lower right", frameon=False, fontsize=12)
        ax.grid(False)
        save(fig, "ch03_ols_residuals.png")
    print(f"ch03_ols_residuals.png: intercept {b0:.4f} slope {b1:.4f} "
          f"RSS {res.ssr:.1f}")


def fig_residual_diag():
    """Residuals vs fitted for the straight-line mpg ~ horsepower fit (Auto).

    Slide 'Residuals vs. fitted on the Auto data'. The red curve is a lowess
    smoother; the slide only claims that it dips and then rises, which is
    verified numerically below.
    """
    import statsmodels.api as sm
    from statsmodels.nonparametric.smoothers_lowess import lowess
    au = pd.read_csv(DATA / "Auto.csv", na_values="?").dropna()
    x = au["horsepower"].astype(float).values
    res = sm.OLS(au["mpg"].values, sm.add_constant(x)).fit()
    fit, resid = res.fittedvalues, res.resid
    sm_fit = lowess(resid, fit, frac=0.5, return_sorted=True)

    with plt.rc_context(SLIDE_RC):
        fig, ax = plt.subplots(figsize=(7.0, 4.2))
        ax.axhline(0, color=GREY, lw=1.0, ls="--", zorder=1)
        ax.scatter(fit, resid, s=18, color=ACCENT, alpha=0.55,
                   edgecolors="none", zorder=2)
        ax.plot(sm_fit[:, 0], sm_fit[:, 1], color=RED, lw=2.8, zorder=3,
                label="smoothed trend")
        ax.text(0.02, 0.06, "U-shaped pattern\n$\\Rightarrow$ missing curvature",
                transform=ax.transAxes, color=RED, fontsize=12, va="bottom")
        ax.set_xlabel("fitted value  $\\hat y$")
        ax.set_ylabel("residual  $e_i = y_i - \\hat y_i$")
        ax.set_title("Residuals vs. fitted: linear mpg ~ horsepower")
        ax.legend(loc="upper right", frameon=False, fontsize=12)
        ax.grid(False)
        save(fig, "ch03_residual_diag.png")
    lo = sm_fit[:, 1]
    print(f"ch03_residual_diag.png: smoother starts {lo[0]:.2f}, dips to "
          f"{lo.min():.2f}, ends {lo[-1]:.2f} (U-shape)")


def fig_x_tv_radio_interaction():
    """sales ~ TV + radio + TV:radio --- the TV slope at two radio levels.

    Slide 'Seeing the interaction: the TV slope depends on radio'. The
    takeaway quotes radio = 10.0 / 36.5 (25th / 75th percentile) and TV
    slopes 0.030 / 0.059 with p_interaction ~ 1e-51.
    """
    import statsmodels.api as sm
    ad = _advertising()
    X = np.column_stack([ad["TV"], ad["radio"], ad["TV"] * ad["radio"]])
    res = sm.OLS(ad["sales"].values, sm.add_constant(X)).fit()
    b0, b_tv, b_ra, b_ix = res.params
    p_ix = res.pvalues[3]
    q25, q75 = ad["radio"].quantile(0.25), ad["radio"].quantile(0.75)

    grid = np.linspace(ad["TV"].min(), ad["TV"].max(), 60)
    with plt.rc_context(SLIDE_RC):
        fig, ax = plt.subplots(figsize=(7.22, 4.02))
        ax.scatter(ad["TV"], ad["sales"], s=18, color=GREY, alpha=0.35,
                   edgecolors="none", zorder=1)
        for radio, colour, tag in [(q25, ACCENT, "25th"), (q75, ORANGE, "75th")]:
            slope = b_tv + b_ix * radio
            ax.plot(grid, b0 + b_ra * radio + slope * grid, color=colour, lw=2.8,
                    zorder=3,
                    label=f"radio = {radio:.1f} ({tag} pct):  slope {slope:.3f}")
            print(f"ch03_x_tv_radio_interaction.png: radio {radio:.1f} "
                  f"({tag} pct) TV slope {slope:.4f}")
        ax.text(0.53, 0.62, "slopes differ $\\Rightarrow$ interaction",
                transform=ax.transAxes, color=GREEN, fontsize=12, style="italic")
        ax.set_xlabel("TV advertising budget (\\$1000s)")
        ax.set_ylabel("Sales (1000s of units)")
        ax.legend(loc="upper left", frameon=False, fontsize=12,
                  title="sales ~ TV + radio + TV$\\times$radio",
                  title_fontsize=12, handlelength=1.6)
        ax.grid(False)
        save(fig, "ch03_x_tv_radio_interaction.png")
    print(f"ch03_x_tv_radio_interaction.png: interaction coef {b_ix:.5f}, "
          f"p = {p_ix:.2e}")


def fig_x_collinearity():
    """Credit: a collinear predictor pair vs an uncorrelated one.

    Slide 'Collinearity, seen: two predictors that move together'. The panel
    titles carry r = 0.997 (Limit, Rating) and r = 0.101 (Limit, Age), and the
    takeaway repeats r = 0.997.
    """
    cr = pd.read_csv(DATA / "Credit.csv")
    pairs = [("Rating", "Rating  (credit score)", RED, "Collinear",
              "points hug a line\n$\\Rightarrow$ redundant predictors"),
             ("Age", "Age  (years)", GREEN, "Not collinear",
              "cloud fills the plane\n$\\Rightarrow$ independent info")]

    with plt.rc_context(SLIDE_RC):
        fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.32))
        for ax, (col, ylab, colour, verdict, note) in zip(axes, pairs):
            x, y = cr["Limit"].values, cr[col].values
            r = np.corrcoef(x, y)[0, 1]
            ax.scatter(x, y, s=22, color=ACCENT, alpha=0.55, edgecolors="none",
                       zorder=2)
            b1, b0 = np.polyfit(x, y, 1)
            grid = np.linspace(x.min(), x.max(), 50)
            ax.plot(grid, b0 + b1 * grid, color=colour, lw=2.4, zorder=3)
            ax.set_title(f"{verdict}:  Limit vs {col}   (r = {r:.3f})",
                         color=colour)
            ax.text(0.04, 0.93, note, transform=ax.transAxes, color=colour,
                    fontsize=12, va="top")
            ax.set_xlabel("Limit  (credit limit, \\$)")
            ax.set_ylabel(ylab)
            ax.set_xticks(np.arange(2000, 14001, 2000))
            ax.spines["top"].set_visible(True)
            ax.spines["right"].set_visible(True)
            ax.grid(False)
            print(f"ch03_x_collinearity.png: corr(Limit, {col}) = {r:.3f}")
        save(fig, "ch03_x_collinearity.png")


def fig_x_rss_surface():
    """The RSS bowl for sales ~ TV on Advertising: contour plus 3-D surface.

    Appendix slide 'The RSS surface: what least squares is minimising'. The
    grid is centred on the OLS solution (7.03, 0.0475); RSS is evaluated
    exactly on every grid point, so the single minimum is a computed fact.
    """
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers '3d')
    import statsmodels.api as sm
    ad = _advertising()
    x, y = ad["TV"].values, ad["sales"].values
    res = sm.OLS(y, sm.add_constant(x)).fit()
    b0h, b1h = res.params

    g0 = np.linspace(b0h - 3.0, b0h + 3.0, 220)
    g1 = np.linspace(b1h - 0.02, b1h + 0.02, 220)
    B0, B1 = np.meshgrid(g0, g1)
    rss = ((y[:, None, None] - B0[None] - B1[None] * x[:, None, None]) ** 2).sum(0)
    rss_k = rss / 1000.0
    levels = np.linspace(2.0, 10.0, 17)

    with plt.rc_context(SLIDE_RC):
        fig = plt.figure(figsize=(10.5, 4.48))
        ax = fig.add_subplot(1, 2, 1)
        cf = ax.contourf(B0, B1, rss_k, levels=levels, cmap="Blues_r")
        ax.contour(B0, B1, rss_k, levels=levels, colors="white", linewidths=0.7)
        cb = fig.colorbar(cf, ax=ax, ticks=np.arange(2, 11))
        cb.set_label("RSS  ($\\times 10^3$)", fontsize=12)
        cb.ax.tick_params(labelsize=12)
        ax.plot([b0h], [b1h], marker="*", ms=22, color=RED, mec="#7B1414",
                mew=1.0, ls="none", label="OLS minimum", zorder=5)
        ax.annotate("$(\\hat\\beta_0, \\hat\\beta_1)$", xy=(b0h, b1h),
                    xytext=(b0h - 0.95, b1h + 0.0090), color=RED, fontsize=12,
                    arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
        ax.legend(loc="upper right", fontsize=12, framealpha=0.92)
        ax.set_xlabel("$\\beta_0$  (intercept)")
        ax.set_ylabel("$\\beta_1$  (slope)")
        ax.set_title("RSS contour: one clear minimum")
        ax.grid(False)

        ax3 = fig.add_subplot(1, 2, 2, projection="3d", computed_zorder=False)
        step = 4
        ax3.plot_surface(B0[::step, ::step], B1[::step, ::step],
                         rss_k[::step, ::step], cmap="Blues_r", vmin=2, vmax=10,
                         rstride=1, cstride=1, linewidth=0.1,
                         edgecolors="white", antialiased=True, zorder=1)
        # computed_zorder=False lets the marker sit on top of the surface
        ax3.scatter([b0h], [b1h], [rss.min() / 1000.0], color="#1B2E5C",
                    s=45, depthshade=False, zorder=5)
        ax3.set_xlabel("$\\beta_0$", labelpad=-2)
        ax3.set_ylabel("$\\beta_1$", labelpad=2)
        # mplot3d z-labels are not counted by bbox_inches="tight", so the
        # label is drawn as a plain Text artist that the crop does see.
        ax3.text2D(1.04, 0.52, "RSS  ($\\times 10^3$)", transform=ax3.transAxes,
                   rotation=90, va="center", ha="left", fontsize=12)
        ax3.set_box_aspect((4, 4, 3), zoom=0.90)
        ax3.set_zticks(np.arange(2, 11, 2))
        ax3.tick_params(labelsize=11, pad=-1)
        ax3.view_init(elev=26, azim=-58)
        ax3.set_title("The RSS 'bowl'")

        fig.suptitle("Least squares minimises RSS$(\\beta_0,\\beta_1)"
                     "=\\sum_i (y_i - \\beta_0 - \\beta_1 x_i)^2$   "
                     "[Advertising: sales on TV]", fontsize=13)
        save(fig, "ch03_x_rss_surface.png")
    print(f"ch03_x_rss_surface.png: min RSS {rss.min():.1f} at "
          f"({b0h:.4f}, {b1h:.4f}); grid max {rss.max():.1f}")


if __name__ == "__main__":
    fig_ci_vs_pi()
    fig_three_predictors()
    fig_ols_residuals()
    fig_residual_diag()
    fig_x_tv_radio_interaction()
    fig_x_collinearity()
    fig_x_rss_surface()

"""Generate the matplotlib figures for the Advanced Module A11 deck
(Time Series and Forecasting).

All figures are computed from the bundled course datasets (Bikeshare.csv,
Weekly.csv) or from clearly labelled simulations seeded with
np.random.default_rng(2024); nothing is sketched by hand. Run from anywhere:

    python "Advanced/advanced_11_time_series/make_figures.py"

Output: Advanced/advanced_11_time_series/images/cha11_*.png at 150 dpi,
matching the figure size and resolution used by the course decks.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
DATA = ROOT / "ALL CSV FILES - 2nd Edition"
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"
ORANGE = "#C8641E"
GREY = "#7A7A7A"
GREEN = "#2E7D5B"
RED = "#C62828"
RNG = np.random.default_rng(2024)

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 9,
    "axes.titlesize": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def acf(x, max_lag):
    """Sample autocorrelation function, the plain estimator."""
    x = np.asarray(x, float)
    x = x - x.mean()
    denom = np.sum(x * x)
    return np.array([np.sum(x[k:] * x[:-k]) / denom if k else 1.0
                     for k in range(max_lag + 1)])


bike = pd.read_csv(DATA / "Bikeshare.csv", index_col=0)
y = bike["bikers"].to_numpy(float)
print(f"[bike] {len(y)} hourly observations, mean = {y.mean():.0f}, "
      f"max = {y.max():.0f}")


def fig_series():
    n = 24 * 21                      # first three weeks
    fig, ax = plt.subplots(figsize=(9.0, 2.7))
    ax.plot(np.arange(n) / 24, y[:n], color=ACCENT, lw=0.8)
    ax.set_xlabel("day")
    ax.set_ylabel("bikers per hour")
    ax.set_title("Bikeshare, first three weeks — the daily cycle is the structure")
    save(fig, "cha11_series.png")


def fig_profiles():
    hr = bike["hr"].astype(int)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.7))
    for w, col, lab in [(1, ACCENT, "working day"), (0, ORANGE, "weekend/holiday")]:
        prof = bike[bike["workingday"] == w].groupby(hr[bike["workingday"] == w])[
            "bikers"].mean()
        axes[0].plot(prof.index, prof.values, "-o", ms=2.5, color=col, label=lab)
    axes[0].set_xlabel("hour of day")
    axes[0].set_ylabel("mean bikers")
    axes[0].legend(frameon=False, fontsize=8)
    months = ["Jan", "Feb", "March", "April", "May", "June",
              "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    prof_m = bike.groupby("mnth")["bikers"].mean().reindex(months)
    axes[1].plot(range(12), prof_m.values, "-o", ms=3, color=GREEN)
    axes[1].set_xticks(range(12))
    axes[1].set_xticklabels([m[0] for m in months])
    axes[1].set_xlabel("month")
    axes[1].set_ylabel("mean bikers")
    peak_h = bike[bike["workingday"] == 1].groupby(hr)["bikers"].mean().idxmax()
    print(f"[profiles] working-day peak at hour {peak_h}")
    save(fig, "cha11_profiles.png")


def fig_acf():
    r = acf(y, 48)
    noise = RNG.normal(size=len(y))
    r_noise = acf(noise, 48)
    band = 1.96 / np.sqrt(len(y))
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.7), sharey=True)
    axes[0].stem(range(49), r, basefmt=" ", linefmt=ACCENT, markerfmt=" ")
    axes[0].set_title("hourly bikers")
    axes[1].stem(range(49), r_noise, basefmt=" ", linefmt=GREY, markerfmt=" ")
    axes[1].set_title("white noise, same length")
    for ax in axes:
        ax.axhline(band, color=RED, lw=0.8, ls=":")
        ax.axhline(-band, color=RED, lw=0.8, ls=":")
        ax.set_xlabel("lag (hours)")
    axes[0].set_ylabel("autocorrelation")
    print(f"[acf] r1 = {r[1]:.2f}, r24 = {r[24]:.2f}, "
          f"white-noise band = ±{band:.3f}")
    save(fig, "cha11_acf.png")


def fig_lagscatter():
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 2.9))
    for ax, k in zip(axes, [1, 24]):
        ax.scatter(y[:-k], y[k:], s=2, alpha=0.25, color=ACCENT)
        rk = np.corrcoef(y[:-k], y[k:])[0, 1]
        ax.set_xlabel(f"$y_{{t-{k}}}$")
        ax.set_ylabel("$y_t$")
        ax.set_title(f"lag {k}: r = {rk:.2f}")
        print(f"[lag] corr(y_t, y_t-{k}) = {rk:.2f}")
    save(fig, "cha11_lagscatter.png")


# ------------------------------------------------------------------
# AR(p) by least squares on lagged copies — Chapter 3 machinery.
# ------------------------------------------------------------------
def make_lags(x, lags):
    p = max(lags)
    X = np.column_stack([x[p - k:len(x) - k] for k in lags])
    return X, x[p:]


LAGS = [1, 2, 24, 25, 168]
split = len(y) - 24 * 7                     # last week held out
X_all, y_all = make_lags(y, LAGS)
off = len(y) - len(y_all)                   # first usable index
X_tr, y_tr = X_all[: split - off], y_all[: split - off]
X_te, y_te = X_all[split - off:], y_all[split - off:]
X1 = np.column_stack([np.ones(len(X_tr)), X_tr])
beta_ar, *_ = np.linalg.lstsq(X1, y_tr, rcond=None)
pred_ar = np.column_stack([np.ones(len(X_te)), X_te]) @ beta_ar
mae_ar = np.mean(np.abs(y_te - pred_ar))
mae_naive = np.mean(np.abs(y_te - y[split - 24:len(y) - 24]))   # seasonal naive
mae_mean = np.mean(np.abs(y_te - y_tr.mean()))
print(f"[ar] coefs on lags {LAGS}: "
      + ", ".join(f"{b:.2f}" for b in beta_ar[1:]))
print(f"[ar] held-out MAE: AR = {mae_ar:.1f}, seasonal naive = {mae_naive:.1f}, "
      f"global mean = {mae_mean:.1f}")


def fig_ar_forecast():
    fig, ax = plt.subplots(figsize=(9.0, 2.8))
    t = np.arange(len(y_te)) / 24
    ax.plot(t, y_te, color=GREY, lw=1.0, label="actual (held-out week)")
    ax.plot(t, pred_ar, color=ORANGE, lw=1.0, label=f"AR on lags 1,2,24,25,168 (MAE {mae_ar:.0f})")
    ax.set_xlabel("day of held-out week")
    ax.set_ylabel("bikers per hour")
    ax.legend(frameon=False, fontsize=8)
    save(fig, "cha11_ar.png")


def knn_time(train_t, train_y, query_t, k=5):
    """k-nearest-neighbours regression on the time index alone."""
    preds = np.empty(len(query_t))
    for i, q in enumerate(query_t):
        d = np.abs(train_t - q)
        nn = np.argpartition(d, k)[:k]
        preds[i] = train_y[nn].mean()
    return preds


# Daily totals: one value per calendar day (a new day starts when hr resets).
day_id = np.cumsum(bike["hr"].astype(int).diff().fillna(0) < 0)
daily = bike.groupby(day_id)["bikers"].sum().to_numpy(float)
print(f"[daily] {len(daily)} days, mean = {daily.mean():.0f} bikers/day")


def fig_backtest():
    """The leak, demonstrated on daily totals: 3-NN on the day index scored
    by shuffled 5-fold CV (neighbouring days leak across folds) vs an honest
    forecast of the final 60 days. The AR-on-lags comparison shows the CV
    number can miss in either direction — it answers a different question."""
    n = len(daily)
    t = np.arange(n, dtype=float)
    sp = n - 60

    idx = RNG.permutation(sp)
    cv_maes = []
    for f in np.array_split(idx, 5):
        mask = np.ones(sp, bool)
        mask[f] = False
        pf = knn_time(t[:sp][mask], daily[:sp][mask], t[:sp][f], k=3)
        cv_maes.append(np.mean(np.abs(daily[:sp][f] - pf)))
    knn_cv = float(np.mean(cv_maes))
    knn_fc = float(np.mean(np.abs(
        daily[sp:] - knn_time(t[:sp], daily[:sp], t[sp:], k=3))))

    # the AR comparison on hourly data: shuffled CV vs the honest week
    cv_ar = []
    for f in np.array_split(RNG.permutation(len(y_tr)), 5):
        mask = np.ones(len(y_tr), bool)
        mask[f] = False
        Xf = np.column_stack([np.ones(mask.sum()), X_tr[mask]])
        bf, *_ = np.linalg.lstsq(Xf, y_tr[mask], rcond=None)
        pf = np.column_stack([np.ones(len(f)), X_tr[f]]) @ bf
        cv_ar.append(np.mean(np.abs(y_tr[f] - pf)))
    ar_cv = float(np.mean(cv_ar))

    print(f"[backtest] 3-NN on daily totals: shuffled CV MAE = {knn_cv:.0f}, "
          f"forecast of final 60 days = {knn_fc:.0f}")
    print(f"[backtest] AR on hourly lags:    shuffled CV MAE = {ar_cv:.1f}, "
          f"forecast of final week = {mae_ar:.1f}")

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 2.9))
    for ax, vals, title, unit in [
        (axes[0], [knn_cv, knn_fc], "3-NN on the day index\n(daily totals)",
         "MAE (bikers per day)"),
        (axes[1], [ar_cv, mae_ar], "AR on lags 1,2,24,25,168\n(hourly)",
         "MAE (bikers per hour)"),
    ]:
        ax.bar(["shuffled\n5-fold CV", "honest\nforecast"], vals,
               color=[ORANGE, GREEN], width=0.5)
        for i, v in enumerate(vals):
            ax.text(i, v * 1.02, f"{v:.0f}", ha="center", fontsize=9)
        ax.set_title(title, fontsize=9)
        ax.set_ylabel(unit)
        ax.set_ylim(0, max(vals) * 1.22)
    save(fig, "cha11_backtest.png")


def fig_weekly_acf():
    weekly = pd.read_csv(DATA / "Weekly.csv")
    r = acf(weekly["Today"].to_numpy(), 20)
    r_vol = acf(weekly["Volume"].to_numpy(), 20)
    band = 1.96 / np.sqrt(len(weekly))
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.7))
    axes[0].stem(range(21), r, basefmt=" ", linefmt=ACCENT, markerfmt=" ")
    axes[0].set_title("Weekly returns (Today)")
    axes[1].stem(range(21), r_vol, basefmt=" ", linefmt=ORANGE, markerfmt=" ")
    axes[1].set_title("Weekly trading volume")
    for ax in axes:
        ax.axhline(band, color=RED, lw=0.8, ls=":")
        ax.axhline(-band, color=RED, lw=0.8, ls=":")
        ax.set_xlabel("lag (weeks)")
        ax.set_ylim(-0.3, 1.05)
    axes[0].set_ylabel("autocorrelation")
    print(f"[weekly] returns r1 = {r[1]:.3f}, volume r1 = {r_vol[1]:.3f}, "
          f"band = ±{band:.3f}")
    save(fig, "cha11_weekly_acf.png")


def fig_ar1_paths():
    """Three simulated AR(1) paths: phi = 0.5, 0.95, 1.0 (random walk)."""
    T = 300
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 2.5), sharex=True)
    for ax, phi in zip(axes, [0.5, 0.95, 1.0]):
        for _ in range(3):
            e = RNG.normal(size=T)
            x = np.zeros(T)
            for t in range(1, T):
                x[t] = phi * x[t - 1] + e[t]
            ax.plot(x, lw=0.8, alpha=0.8)
        ax.set_title(rf"$\phi = {phi}$" + ("  (random walk)" if phi == 1 else ""))
        ax.set_xlabel("t")
    axes[0].set_ylabel("$y_t$")
    save(fig, "cha11_ar1_paths.png")


if __name__ == "__main__":
    fig_series()
    fig_profiles()
    fig_acf()
    fig_lagscatter()
    fig_ar_forecast()
    fig_backtest()
    fig_weekly_acf()
    fig_ar1_paths()

"""Generate the computed matplotlib figures for the A9 (Deep Learning) module deck.

Everything is computed exactly or from a seeded simulation --- nothing is
sketched by hand. Run from anywhere:

    python Chapters/Advanced/advanced_09_deep_learning/make_figures.py

Output: Chapters/Advanced/advanced_09_deep_learning/images/ch10_*.png at 150 dpi, matching the other decks. Existing figures are not
touched.
"""

import functools
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "images"
OUT.mkdir(parents=True, exist_ok=True)

ACCENT = "#26468C"   # matches \definecolor{accent}{RGB}{38,70,140}
ORANGE = "#C8641E"
GREY = "#7A7A7A"

# Secondary palette of the activation / training / descent figures.  These three
# were authored with a slightly brighter amber and with a green and a red for the
# third and fourth series; the constants below reproduce them exactly.
AMBER = "#E08214"
GREEN = "#2E7D32"
RED = "#C62828"
GREY_MID = "#9E9E9E"   # contour lines
GREY_LT = "#BFBFBF"    # zero reference lines

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


# The activation / training / descent figures are wide two-panel plots that sit on a
# slide at 0.88--0.92\textwidth, so they were authored one step up from the module's
# label sizes; this context reproduces the committed PNGs' typography exactly.
BIG_LABELS = {"font.size": 12.8, "axes.titlesize": 14.0, "legend.fontsize": 10.0}


def big_labels(fn):
    """Run *fn* under BIG_LABELS instead of the module's default label sizes."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with plt.rc_context(BIG_LABELS):
            return fn(*args, **kwargs)

    return wrapper


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def fig_conv_vs_dense():
    """Parameters of one conv layer vs a dense layer reaching the same outputs.

    Exercise 10.4 as a curve: a 16-filter 5x5 convolution costs 1,216
    parameters whatever the image size; a dense layer to the same output
    volume grows with the fourth power of the image side.
    """
    W = np.arange(8, 129)
    conv = np.full_like(W, 16 * (5 * 5 * 3 + 1), dtype=float)     # 1,216
    out_units = (W - 4) ** 2 * 16
    dense = (W ** 2 * 3).astype(float) * out_units + out_units

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(W, dense, color=ACCENT, lw=2)
    ax.plot(W, conv, color=ORANGE, lw=2)

    i32 = np.where(W == 32)[0][0]
    ax.plot([32, 32], [conv[i32], dense[i32]], color=GREY, lw=0.9, ls=":")
    ax.plot(32, dense[i32], "o", color=ACCENT, ms=5, mec="white", mew=0.8)
    ax.plot(32, conv[i32], "o", color=ORANGE, ms=5, mec="white", mew=0.8)
    ax.annotate("$32\\times32\\times3$ image:\n$38.5$M vs $1{,}216$\n($31{,}700\\times$)",
                xy=(32, dense[i32]), xytext=(40, 2e5), fontsize=8.5, color="#333333",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))

    ax.text(88, 1.5e8, "dense layer to the\nsame output volume", color=ACCENT,
            fontsize=9, ha="center")
    ax.text(95, 3.2e3, "one conv layer: $1{,}216$ parameters,\nwhatever the image size",
            color=ORANGE, fontsize=9, ha="center", va="bottom")

    ax.set_yscale("log")
    ax.set_xlabel("image side $W$  (input $W\\times W\\times 3$, 16 filters of $5\\times5$)")
    ax.set_ylabel("trainable parameters")
    ax.set_xlim(8, 128)
    save(fig, "ch10_conv_vs_dense.png")
    print("ch10_conv_vs_dense.png: at W=32 dense", f"{dense[i32]:,.0f}", "conv 1,216",
          f"ratio {dense[i32]/1216:,.0f}x")


@big_labels
def fig_activations():
    """The three activation functions and their derivatives, in closed form.

    Nothing is fitted or simulated: sigmoid $1/(1+e^{-z})$, $\\tanh z$ and
    $\\max(0,z)$ are evaluated on a dense grid, and the derivatives are the exact
    analytic ones --- $\\sigma(1-\\sigma)$, $1-\\tanh^2$, and the $0/1$ step.  The
    slide's takeaway reads the two numbers straight off the right panel: the
    sigmoid derivative peaks at $\\sigma'(0)=0.25$ and never exceeds it, while
    ReLU' is exactly $1$ on the active region.
    """
    z = np.linspace(-5, 5, 2001)
    sig = 1.0 / (1.0 + np.exp(-z))
    tanh = np.tanh(z)
    relu = np.maximum(0.0, z)

    d_sig = sig * (1.0 - sig)
    d_tanh = 1.0 - tanh ** 2
    d_relu = (z > 0).astype(float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.60))

    for ax in (ax1, ax2):
        ax.grid(False)
        ax.axhline(0, color=GREY_LT, lw=0.9, zorder=0)
        ax.axvline(0, color=GREY_LT, lw=0.9, zorder=0)
        ax.set_xlabel("$z$")

    ax1.plot(z, sig, color=ACCENT, lw=2, label="sigmoid $1/(1+e^{-z})$")
    ax1.plot(z, tanh, color=AMBER, lw=2, label="tanh")
    ax1.plot(z, relu, color=GREEN, lw=2, label="ReLU $\\max(0, z)$")
    ax1.set_ylim(-1.4, 3.0)          # clips ReLU at z = 3 so the S-curves stay readable
    ax1.set_ylabel("$g(z)$")
    ax1.set_title("Activation functions")
    ax1.legend(loc="upper left", frameon=False)

    ax2.plot(z, d_sig, color=ACCENT, lw=2, label="sigmoid$'$  ($\\leq 0.25$)")
    ax2.plot(z, d_tanh, color=AMBER, lw=2, label="tanh$'$")
    ax2.plot(z, d_relu, color=GREEN, lw=2, label="ReLU$'$  ($0$ or $1$)")
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_ylabel("$g'(z)$")
    ax2.set_title("Derivatives (gradient flow)")
    ax2.legend(loc="upper left", frameon=False)

    save(fig, "ch10_activations.png")
    print("wrote ch10_activations.png:  max sigmoid' =", round(d_sig.max(), 4),
          " ReLU' on the active region =", round(d_relu[z > 0].min(), 4))


@big_labels
def fig_training():
    """Gradient descent on a convex loss (left) and an overfitting run (right).

    Left panel --- exact, deterministic.  Loss $L(w)=(w-2)^2+1$, start $w_0=-3$
    (so $L=26$), learning rate $\\eta=0.16$, i.e. $w_{t+1}-2 = 0.68\\,(w_t-2)$;
    eight iterates are drawn, with the tangent (the gradient actually used) shown
    at the first four.

    Right panel --- a *schematic* learning curve, not a re-run of a network.  The
    deck ties no number to this panel (the slide's takeaway is qualitative, and
    the Default-data MLP of Extended Exercise 10.3 reports quite different values
    --- val-min 0.10 at epoch 16, val-final 0.93 --- on its own text slide).  The
    two trends here are the exponential/linear curves fitted to the original
    figure, train $=0.15+2.23e^{-t/8.94}$ and val $=0.47+1.90e^{-t/6.58}+0.0093t$,
    plus seeded Gaussian jitter; the validation trend is minimised at epoch 23,
    which is where the early-stopping marker sits.  No deep-learning framework is
    needed or used.
    """
    # ---- left: gradient descent on L(w) = (w - 2)^2 + 1 ------------------
    def L(w):
        return (w - 2.0) ** 2 + 1.0

    def dL(w):
        return 2.0 * (w - 2.0)

    eta, w0, n_steps = 0.16, -3.0, 7
    path = [w0]
    for _ in range(n_steps):
        path.append(path[-1] - eta * dL(path[-1]))
    path = np.array(path)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.60))
    ax1.grid(False)
    ax2.grid(False)

    grid = np.linspace(-3.9, 4.2, 400)
    ax1.plot(grid, L(grid), color=GREY, lw=1.6, zorder=1)

    # the tangent at each of the first four iterates: the slope the step uses
    for w in path[:4]:
        seg = np.array([w - 0.7, w + 0.7])
        ax1.plot(seg, L(w) + dL(w) * (seg - w), color=AMBER, lw=2.2, zorder=2)

    ax1.plot(path, L(path), color=ACCENT, lw=1.5, zorder=3)
    ax1.plot(path, L(path), "o", color=ACCENT, ms=7, zorder=4)
    for t in range(5):
        ax1.annotate("", xy=(path[t + 1], L(path[t + 1])), xytext=(path[t], L(path[t])),
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.4), zorder=5)

    ax1.text(path[0], L(path[0]) + 1.4, "start", color=ACCENT, ha="center",
             va="bottom", fontsize=9)
    ax1.plot(2, 1, "*", color=RED, ms=18, zorder=6)
    ax1.annotate("minimum", xy=(2.25, 1.2), xytext=(2.75, 4.3), color=RED,
                 fontsize=9, va="center",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax1.set_xlabel("parameter $w$")
    ax1.set_ylabel("loss $L(w)$")
    ax1.set_title("Gradient descent on a convex loss")

    # ---- right: training vs validation loss (schematic, seeded) ----------
    rng = np.random.default_rng(93)   # seed chosen so the validation minimum lands on epoch 23
    ep = np.arange(1, 61)
    ramp = 1.0 - np.exp(-ep / 4.0)          # curves start smooth, jitter later
    train = 0.15 + 2.23 * np.exp(-ep / 8.94) + 0.013 * ramp * rng.standard_normal(ep.size)
    val = (0.47 + 1.90 * np.exp(-ep / 6.58) + 0.0093 * ep
           + 0.045 * ramp * rng.standard_normal(ep.size))

    best = int(ep[val.argmin()])
    ax2.plot(ep, train, color=ACCENT, lw=1.8, label="training loss")
    ax2.plot(ep, val, color=AMBER, lw=1.8, label="validation loss")
    ax2.axvline(best, color=RED, lw=1.5, ls="--")
    ax2.plot(best, val[best - 1], "o", color=RED, ms=9, zorder=5)
    ax2.annotate("best model\n(early stopping)", xy=(best + 0.7, val[best - 1] + 0.02),
                 xytext=(best + 4.5, val[best - 1] + 0.68), color=RED, fontsize=9,
                 ha="left", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax2.set_xlabel("epoch")
    ax2.set_ylabel("loss")
    ax2.set_title("Training vs. validation loss")
    ax2.legend(loc="upper right", frameon=False)

    save(fig, "ch10_training.png")
    print("wrote ch10_training.png:  left L(-3) =", L(path[0]),
          "-> L(w_7) =", round(L(path[-1]), 3),
          "| right val-min", round(val.min(), 3), "at epoch", best,
          "val-final", round(val[-1], 3), "train-final", round(train[-1], 3))


@big_labels
def fig_x_gradient_descent():
    """Gradient descent on the anisotropic quadratic $(1.5-w_1)^2 + 8(w_2-1)^2$.

    Fully deterministic: fixed start $(-1.5,-0.5)$, exact gradient
    $(2(w_1-1.5),\\, 16(w_2-1))$, 25 steps at each of the two learning rates.
    Because the problem is separable the iterates are known in closed form,
    $w_1-1.5 = (1-2\\eta)^t(w_1^{(0)}-1.5)$ and $w_2-1 = (1-16\\eta)^t(w_2^{(0)}-1)$,
    which is what makes the appendix slide's numbers exact:

      * $L(-1.5,-0.5) = 9 + 18 = 27$;
      * $\\eta = 0.05$ gives contraction factors $0.9$ and $0.2$, so after 25 steps
        $L = 9\\cdot0.9^{50} + 18\\cdot0.2^{50} = 0.046 \\approx 0.05$ --- fast down
        the steep $w_2$ axis, then a crawl along the flat valley;
      * $\\eta = 0.115$ gives $0.77$ and $-0.84$: the $w_2$ factor is negative, so
        the path overshoots and zigzags in the steep direction.
    """
    w_star = np.array([1.5, 1.0])
    curv = np.array([1.0, 8.0])            # L = curv . (w - w_star)^2

    def loss(w1, w2):
        return (1.5 - w1) ** 2 + 8.0 * (w2 - 1.0) ** 2

    def descend(eta, n=25, start=(-1.5, -0.5)):
        w = np.array(start, dtype=float)
        out = [w.copy()]
        for _ in range(n):
            w = w - eta * 2.0 * curv * (w - w_star)
            out.append(w.copy())
        return np.array(out)

    slow = descend(0.05)
    fast = descend(0.115)

    fig, ax = plt.subplots(figsize=(6.82, 4.00))
    ax.grid(False)

    g1 = np.linspace(-2.3, 3.4, 400)
    g2 = np.linspace(-1.3, 2.5, 400)
    G1, G2 = np.meshgrid(g1, g2)
    cs = ax.contour(G1, G2, loss(G1, G2), levels=[0.15, 1.5, 4, 9, 18, 30, 45],
                    colors=GREY_MID, linewidths=0.9)
    ax.clabel(cs, inline=True, fontsize=7.5, fmt="%g", colors=GREY_MID)

    ax.plot(fast[:, 0], fast[:, 1], "-o", color=AMBER, lw=1.1, ms=3.2, alpha=0.9,
            zorder=3, label="$\\eta = 0.115$: zigzags in steep direction")
    ax.plot(slow[:, 0], slow[:, 1], "-o", color=ACCENT, lw=2.0, ms=3.6,
            zorder=4, label="$\\eta = 0.05$: 25 smooth steps")
    ax.plot(*w_star, "*", color=GREEN, ms=16, zorder=5,
            label="minimum $(1.5,\\,1)$")
    ax.plot(-1.5, -0.5, "s", color="black", ms=6, zorder=5)
    ax.text(-1.85, -1.02, "start", color="#2A2A2A", ha="center", va="center")

    ax.set_yticks([-1, 0, 1, 2])
    ax.set_xlabel("$w_1$")
    ax.set_ylabel("$w_2$")
    ax.set_title("Gradient descent on $(1.5-w_1)^2 + 8(w_2-1)^2$")
    ax.legend(loc="upper left", frameon=False,
              handlelength=1.6, borderaxespad=0.2)

    save(fig, "ch10_x_gradient_descent.png")
    print("wrote ch10_x_gradient_descent.png:  L(start) =",
          round(float(loss(*slow[0])), 3),
          "| eta=0.05 after 25 steps L =", round(float(loss(*slow[-1])), 4),
          "| eta=0.115 after 25 steps L =", round(float(loss(*fast[-1])), 4))


if __name__ == "__main__":
    fig_conv_vs_dense()
    fig_activations()
    fig_training()
    fig_x_gradient_descent()

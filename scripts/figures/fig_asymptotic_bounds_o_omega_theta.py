"""Three-panel geometric view of the O / Omega / Theta definitions (ram_model.md SS7.4)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np

from _style import GRAY, INK, LIGHT, apply_style, save

# f(n) = n * (1 + a*exp(-d*n)*sin(w*n)): a near-linear function whose relative
# wiggle decays, so it visibly violates each constant-multiple bound of
# g(n) = n for small n and then stays strictly inside the bound forever.
A, D, W = 1.5, 0.3, 2.1
C1, C2 = 0.55, 1.35  # f = Theta(n) with c1*n <= f(n) <= c2*n past n0

X_MAX = 7.5
DASH = (0, (5, 3))


def f(x):
    return x * (1.0 + A * np.exp(-D * x) * np.sin(W * x))


def last_crossing(x, violated):
    """Smallest x past which `violated` is False forever (midpoint of flip)."""
    i = np.where(violated)[0][-1]
    return 0.5 * (x[i] + x[i + 1])


x = np.linspace(0.0, X_MAX, 2000)
fx = f(x)

n0_o = last_crossing(x, fx > C2 * x)  # last time f pokes above c*g
n0_w = last_crossing(x, fx < C1 * x)  # last time f dips below c*g
n0_t = max(n0_o, n0_w)  # Theta needs both bounds to hold

apply_style()
fig, axes = plt.subplots(1, 3, figsize=(6.0, 2.5), sharey=True)

panels = [
    (axes[0], r"$f(n) = O(g(n))$", n0_o, [(C2, r"$c \cdot g(n)$", True)]),
    (axes[1], r"$f(n) = \Omega(g(n))$", n0_w, [(C1, r"$c \cdot g(n)$", False)]),
    (
        axes[2],
        r"$f(n) = \Theta(g(n))$",
        n0_t,
        [(C2, r"$c_2 \cdot g(n)$", True), (C1, r"$c_1 \cdot g(n)$", False)],
    ),
]

for ax, title, n0, bounds in panels:
    if len(bounds) == 2:  # Theta: shade the trap band, but only past n0
        m = x >= n0
        ax.fill_between(x[m], C1 * x[m], C2 * x[m], color=LIGHT, zorder=0)
    ax.axvline(n0, ls=":", lw=0.9, color=GRAY, zorder=1)
    for c, label, above in bounds:
        ax.plot(x, c * x, ls=DASH, lw=1.1, color=INK, zorder=2)
        # Below-line labels need extra drop so the rising dashed line
        # does not slope up through the text box.
        ax.annotate(
            label,
            xy=(X_MAX, c * X_MAX),
            xytext=(-2, 6 if above else -11),
            textcoords="offset points",
            ha="right",
            va="bottom" if above else "top",
            fontsize=8.5,
            color=INK,
        )
    ax.plot(x, fx, lw=1.8, color=INK, zorder=3)
    ax.annotate(
        r"$f(n)$",
        xy=(X_MAX, fx[-1]),
        xytext=(-2, -7),
        textcoords="offset points",
        ha="right",
        va="top",
        fontsize=8.5,
        color=INK,
    )

    ax.set_title(title)
    ax.set_xlim(0, X_MAX)
    ax.set_ylim(0, 11.0)
    ax.set_xticks([n0])
    ax.set_xticklabels([r"$n_0$"])
    ax.set_yticks([])
    ax.annotate(
        r"$n$",
        xy=(1.0, 0.0),
        xycoords="axes fraction",
        xytext=(0, -11),
        textcoords="offset points",
        ha="center",
        va="top",
        fontsize=9.5,
        color=INK,
    )

# State the rule once: the bound is only required to hold right of n0.
for text, side in [("bound may fail", -1), ("bound holds", +1)]:
    axes[0].annotate(
        text,
        xy=(n0_o + side * 0.38, 10.55),
        ha="left" if side > 0 else "right",
        va="top",
        fontsize=7.5,
        style="italic",
        color=GRAY,
    )

fig.subplots_adjust(wspace=0.16)
save(fig, "asymptotic-bounds-o-omega-theta")

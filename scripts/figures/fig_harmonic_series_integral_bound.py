"""Integral bound for the harmonic series (§15.3): unit-width 1/i rectangles hug y = 1/x, squeezing H_n between ln(n+1) and ln(n) + 1."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np

from _style import GRAY, INK, LIGHT, apply_style, save

N = 15  # bars cover x in [1, N+1]; total bar area is H_N


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.0, 3.1))

    i = np.arange(1, N + 1)

    # Unit-width rectangles: bar i spans [i, i+1] with height 1/i (left-endpoint
    # rule), so the total bar area is exactly H_N.
    ax.bar(i, 1.0 / i, width=1.0, align="edge",
           facecolor=LIGHT, edgecolor=INK, linewidth=0.7, zorder=2)

    # Slivers between each bar top and the curve; together they sum to
    # H_N - ln(N+1) < 1.
    for k in i:
        xs_k = np.linspace(k, k + 1, 40)
        ax.fill_between(xs_k, 1.0 / xs_k, 1.0 / k,
                        facecolor=GRAY, edgecolor="none", zorder=3)

    xs = np.linspace(1, N + 1, 600)
    ax.plot(xs, 1.0 / xs, color=INK, lw=2.0, zorder=4)

    # --- annotations -------------------------------------------------------
    ax.text(1.5, 0.33, "area\n$1$", ha="center", va="center",
            fontsize=9, color=INK, linespacing=1.1, zorder=5)
    ax.text(4.5, 0.105, "area\n$1/4$", ha="center", va="center",
            fontsize=8.5, color=INK, linespacing=1.1, zorder=5)

    ax.annotate(
        "$y = 1/x$\n$\\int_1^{\\,n+1} dx/x = \\ln(n{+}1)$",
        xy=(5.45, 1 / 5.45), xytext=(6.3, 0.42),
        ha="left", va="center", fontsize=9, color=INK, zorder=5,
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8,
                        shrinkA=4, shrinkB=2),
    )

    ax.annotate(
        "dark gaps sum to\n$H_n - \\ln(n{+}1) < 1$",
        xy=(2.35, 0.465), xytext=(3.35, 0.76),
        ha="left", va="center", fontsize=9, color=INK, zorder=5,
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8,
                        shrinkA=4, shrinkB=2),
    )

    ax.text(11.5, 0.24,
            "total bar area $= 1 + 1/2 + \\cdots + 1/n = H_n$",
            ha="center", va="center", fontsize=9, color=INK, zorder=5)

    ax.text(0.985, 0.95,
            "$\\ln(n{+}1) \\,\\leq\\, H_n \\,\\leq\\, \\ln n + 1$\n"
            "$\\Rightarrow\\; H_n = \\Theta(\\log n)$",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9.5, color=INK, linespacing=1.5, zorder=5,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=INK, linewidth=0.7))

    # --- axes --------------------------------------------------------------
    ax.set_xlim(0.6, N + 1.4)
    ax.set_ylim(0, 1.08)
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["$0$", "$1/2$", "$1$"])
    ax.set_xlabel("$i$")
    ax.set_ylabel("$1/i$", rotation=0, labelpad=12)

    save(fig, "harmonic-series-integral-bound")


if __name__ == "__main__":
    main()

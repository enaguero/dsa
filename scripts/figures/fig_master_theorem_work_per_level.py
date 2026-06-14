"""Per-level work in the recursion tree for the three Master Theorem cases (§17.1)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save

N = 64
B = 2
K = int(np.log2(N))  # deepest level; k = 0..K
LEVELS = np.arange(K + 1)


def level_work(a: int, f) -> np.ndarray:
    """Non-recursive work a^k * f(n/b^k) at each level k of the recursion tree."""
    return np.array([a**k * f(N / B**k) for k in LEVELS], dtype=float)


PANELS = [
    {
        "work": level_work(4, lambda m: m),  # T(n) = 4T(n/2) + n
        "title": "Case 1: $f \\prec n^{c^*}$,  ratio $2$",
        "recurrence": "$T(n) = 4\\,T(n/2) + n$",
        "dominant": [K],
        "ratio_label": "$\\times\\, 2$",
        "ratio_gaps": [1, 2, 3],
    },
    {
        "work": level_work(2, lambda m: m),  # T(n) = 2T(n/2) + n
        "title": "Case 2: $f \\asymp n^{c^*}$,  ratio $1$",
        "recurrence": "$T(n) = 2\\,T(n/2) + n$",
        "dominant": list(LEVELS),
        "ratio_label": None,
        "ratio_gaps": [],
    },
    {
        "work": level_work(2, lambda m: m * m),  # T(n) = 2T(n/2) + n^2
        "title": "Case 3: $f \\succ n^{c^*}$,  ratio $\\frac{1}{2}$",
        "recurrence": "$T(n) = 2\\,T(n/2) + n^2$",
        "dominant": [0],
        "ratio_label": "$\\times\\, 1/2$",
        "ratio_gaps": [0, 1, 2],
    },
]


def draw_bars(ax, panel):
    work = panel["work"]
    bars = ax.barh(LEVELS, work, height=0.66, zorder=3)
    for k, bar in enumerate(bars):
        if k in panel["dominant"]:
            bar.set_facecolor(NAVY)
            bar.set_edgecolor("white")
            bar.set_linewidth(0)
            bar.set_hatch("//")
        else:
            bar.set_facecolor(LIGHT)
            bar.set_edgecolor(GRAY)
            bar.set_linewidth(0.7)
    for gap in panel["ratio_gaps"]:
        x = (work[gap] + work[gap + 1]) / 2
        ax.text(x, gap + 0.5, panel["ratio_label"], fontsize=8.5, color=ORANGE,
                ha="center", va="center", zorder=4)


def main():
    apply_style()
    mpl.rcParams["hatch.linewidth"] = 0.7

    fig, axes = plt.subplots(1, 3, figsize=(6.0, 3.0), sharey=True,
                             constrained_layout=True)

    for ax, panel in zip(axes, PANELS):
        draw_bars(ax, panel)
        ax.set_title(panel["title"] + "\n" + panel["recurrence"], fontsize=9.5)
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks(LEVELS)

    ax1, ax2, ax3 = axes
    wmax = PANELS[0]["work"].max()

    ax1.set_xlim(0, wmax * 1.08)
    ax2.set_xlim(0, N * 2.6)
    ax3.set_xlim(0, wmax * 1.08)

    ylabels = [str(k) for k in LEVELS]
    ylabels[0] = "0 (root)"
    ylabels[-1] = f"{K} (leaves)"
    ax1.set_yticklabels(ylabels)
    ax1.set_ylabel("recursion-tree level $k$")
    ax2.set_xlabel("work at level $k\\; = \\;a^k \\cdot f(n/b^k)$"
                   "\n($n = 64$; each panel on its own scale)")

    # Panel 1: leaves dominate.
    ax1.annotate("leaves dominate:\n$\\Theta(n^{c^*}) = \\Theta(n^2)$",
                 xy=(wmax * 0.74, K - 0.16), xytext=(wmax * 1.0, 1.6),
                 ha="right", va="center", fontsize=8.5, color=INK,
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8,
                                 connectionstyle="arc3,rad=-0.25"))

    # Panel 2: bracket spanning all equal levels.
    xb = N * 1.18
    tick = N * 0.10
    ax2.plot([xb, xb], [-0.33, K + 0.33], color=INK, lw=0.9, zorder=4)
    ax2.plot([xb - tick, xb], [-0.33, -0.33], color=INK, lw=0.9, zorder=4)
    ax2.plot([xb - tick, xb], [K + 0.33, K + 0.33], color=INK, lw=0.9, zorder=4)
    ax2.text(xb + N * 0.14, K / 2,
             "$\\log_2 n + 1 = 7$\nequal levels:\n$\\Theta(n^{c^*}\\log n)$",
             fontsize=8.5, color=INK, ha="left", va="center")

    # Panel 3: root dominates.
    ax3.annotate("root dominates:\n$\\Theta(f(n)) = \\Theta(n^2)$",
                 xy=(wmax * 0.96, 0.40), xytext=(wmax * 1.02, 4.0),
                 ha="right", va="center", fontsize=8.5, color=INK,
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8,
                                 connectionstyle="arc3,rad=0.35"))

    save(fig, "master-theorem-work-per-level")


if __name__ == "__main__":
    main()

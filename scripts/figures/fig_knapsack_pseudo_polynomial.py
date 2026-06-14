"""Same Theta(nW) knapsack runtimes vs the value W and vs the bit length of W (§26.6)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np

from _style import INK, NAVY, ORANGE, apply_style, save

N_ITEMS = 100  # fixed number of items n
BITS = np.arange(1, 21)  # b = bit length of W, so W = 2^b
HIGHLIGHT_BITS = [10, 15, 20]  # the three runs marked on both panels

M = 1e6  # plot operations in millions


def main() -> None:
    apply_style()

    # The DP table has n*W entries, each O(1): runtime proxy = n * W = n * 2^b.
    capacities = 2.0**BITS
    operations = N_ITEMS * capacities

    hi = np.isin(BITS, HIGHLIGHT_BITS)

    fig, (ax_val, ax_bit) = plt.subplots(
        1, 2, figsize=(6.0, 3.5), sharey=True, gridspec_kw={"wspace": 0.10}
    )
    fig.subplots_adjust(top=0.80)

    # ---- left panel: x = the VALUE of W (linear axis) ------------------
    w_line = np.linspace(0, 1.1e6, 200)
    ax_val.plot(w_line / M, N_ITEMS * w_line / M, color=NAVY, zorder=2)
    ax_val.plot(
        capacities / M,
        operations / M,
        "o",
        color=INK,
        markersize=3.2,
        linestyle="none",
        zorder=3,
    )
    ax_val.set_xlim(0, 1.1)
    ax_val.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_val.set_xlabel("capacity $W$ (millions)")
    ax_val.set_ylabel("DP table entries $n \\cdot W$ (millions)")
    ax_val.set_title("against the value $W$:\na straight line, $\\Theta(nW)$", fontsize=10)

    ax_val.annotate(
        "every run sits on\nthe line $100\\,W$",
        xy=(0.62, 62),
        xytext=(0.60, 22),
        fontsize=8.5,
        color=NAVY,
        ha="center",
        arrowprops=dict(arrowstyle="-|>", color=NAVY, linewidth=0.7, shrinkA=2, shrinkB=3),
    )

    # ---- right panel: x = the SIZE of the input (bits of W) ------------
    b_line = np.linspace(1, 20, 400)
    ax_bit.plot(b_line, N_ITEMS * 2.0**b_line / M, color=NAVY, zorder=2)
    ax_bit.plot(BITS, operations / M, "o", color=INK, markersize=3.2, linestyle="none", zorder=3)
    ax_bit.set_xlim(0.5, 21)
    ax_bit.set_xticks([1, 5, 10, 15, 20])
    ax_bit.set_xlabel("input size: bits $b$ of $W$  ($W = 2^b$)")
    ax_bit.set_title("against the input size $b$:\nexponential, $\\Theta(n \\cdot 2^b)$", fontsize=10)

    ax_bit.annotate(
        "one more bit doubles\nthe runtime",
        xy=(19.0, N_ITEMS * 2.0**19.0 / M),
        xytext=(12.6, 70),
        fontsize=8.5,
        color=NAVY,
        ha="center",
        arrowprops=dict(
            arrowstyle="-|>",
            color=NAVY,
            linewidth=0.7,
            shrinkA=2,
            shrinkB=3,
            connectionstyle="arc3,rad=-0.2",
        ),
    )

    # ---- the same three runs, marked identically on both panels --------
    for ax, x in ((ax_val, capacities / M), (ax_bit, BITS.astype(float))):
        ax.plot(
            x[hi],
            operations[hi] / M,
            "o",
            markersize=7,
            markerfacecolor="white",
            markeredgecolor=ORANGE,
            markeredgewidth=1.4,
            linestyle="none",
            zorder=4,
            clip_on=False,
        )
        ax.set_ylim(0, 115)
        ax.grid(True, axis="y", zorder=0)

    leader = dict(arrowstyle="-", color=ORANGE, linewidth=0.7, linestyle=(0, (1, 2)))
    ax_val.annotate(
        "the same three runs\n$b = 10, 15, 20$",
        xy=(1.0486, 104.9),
        xytext=(0.30, 92),
        fontsize=8.5,
        color=ORANGE,
        ha="center",
        arrowprops=dict(**leader, shrinkA=4, shrinkB=5),
    )
    ax_val.annotate(
        "", xy=(0.033, 3.3), xytext=(0.21, 86), arrowprops=dict(**leader, shrinkA=2, shrinkB=5)
    )
    ax_bit.annotate(
        "the same three runs\n$b = 10, 15, 20$",
        xy=(20, 104.9),
        xytext=(6.5, 92),
        fontsize=8.5,
        color=ORANGE,
        ha="center",
        arrowprops=dict(**leader, shrinkA=4, shrinkB=6),
    )
    ax_bit.annotate(
        "", xy=(15, 3.3), xytext=(7.5, 85), arrowprops=dict(**leader, shrinkA=2, shrinkB=5)
    )
    ax_bit.annotate(
        "", xy=(10, 0.2), xytext=(6.5, 85), arrowprops=dict(**leader, shrinkA=2, shrinkB=5)
    )

    fig.suptitle(
        "Pseudo-polynomial: the same $\\Theta(nW)$ measurements ($n = 100$ items),"
        " only the $x$-axis changes",
        fontsize=10.5,
        y=0.985,
    )

    save(fig, "knapsack-pseudo-polynomial")


if __name__ == "__main__":
    main()

"""Per-push cost of a doubling dynamic array vs. its flat running average (§19.2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np

from _style import GRAY, INK, LIGHT, NAVY, apply_style, save

N = 50  # number of pushes shown


def push_costs(n: int) -> tuple[np.ndarray, np.ndarray]:
    """Simulate n pushes into a dynamic array that doubles capacity when full.

    Returns (costs, is_realloc): cost of push i is 1 element write, plus
    `size` copies when the push triggers a reallocation.
    """
    costs = np.empty(n)
    is_realloc = np.zeros(n, dtype=bool)
    size, capacity = 0, 1
    for i in range(n):
        if size == capacity:
            capacity *= 2
            costs[i] = size + 1  # copy `size` elements, then write the new one
            is_realloc[i] = True
        else:
            costs[i] = 1
        size += 1
    return costs, is_realloc


def main() -> None:
    apply_style()

    costs, is_realloc = push_costs(N)
    i = np.arange(1, N + 1)
    running_avg = np.cumsum(costs) / i

    fig, ax = plt.subplots(figsize=(6.0, 3.4))

    # Actual cost of each push: ordinary pushes in light gray, reallocating
    # pushes darker so the doubling spikes read even in grayscale.
    h_plain = ax.bar(
        i[~is_realloc],
        costs[~is_realloc],
        width=0.8,
        facecolor=LIGHT,
        edgecolor=GRAY,
        linewidth=0.5,
        label="actual cost $c_i$ of push $i$",
    )
    h_realloc = ax.bar(
        i[is_realloc],
        costs[is_realloc],
        width=0.8,
        facecolor="#c5c5cf",
        edgecolor=INK,
        linewidth=0.7,
        label="push triggering reallocation",
    )

    # Amortized bound from the aggregate analysis: total <= 3n.
    h_bound = ax.axhline(
        3, color=INK, linestyle=(0, (5, 3)), linewidth=1.1, label="amortized bound: 3 per push"
    )

    # Running average — the punchline: it never escapes the bound.
    (h_avg,) = ax.plot(
        i, running_avg, color=NAVY, linewidth=2.0, solid_capstyle="round", label="running average"
    )

    # --- annotations ---------------------------------------------------
    ax.annotate(
        "reallocation at $i=33$:\ncopy 32 elements + write 1",
        xy=(33, 33),
        xytext=(36.5, 31.5),
        fontsize=8.5,
        color=INK,
        ha="left",
        va="top",
        arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.7, shrinkA=2, shrinkB=2),
    )
    ax.annotate(
        "ordinary push: $c_i = 1$",
        xy=(25, 1),
        xytext=(20.5, 7.5),
        fontsize=8.5,
        color=INK,
        ha="center",
        arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.7, shrinkA=2, shrinkB=2),
    )
    ax.annotate(
        "running average stays $O(1)$:\ntotal $\\leq 3n$, so average $\\leq 3$",
        xy=(44, running_avg[43]),
        xytext=(47, 11),
        fontsize=8.5,
        color=NAVY,
        ha="center",
        arrowprops=dict(
            arrowstyle="-|>",
            color=NAVY,
            linewidth=0.7,
            shrinkA=2,
            shrinkB=1,
            connectionstyle="arc3,rad=-0.15",
        ),
    )

    ax.set_xlabel("push number $i$")
    ax.set_ylabel("cost (element writes)")
    ax.set_xlim(0, N + 1)
    ax.set_ylim(0, 36)
    ax.set_xticks([1, 10, 20, 30, 40, 50])
    ax.set_yticks([0, 3, 10, 20, 30])
    ax.set_title("Dynamic array doubling: spikes are rare enough that the average is constant")
    ax.legend(
        handles=[h_plain, h_realloc, h_avg, h_bound],
        loc="upper left",
        handlelength=1.8,
        borderaxespad=0.2,
    )

    save(fig, "dynamic-array-amortized-cost")


if __name__ == "__main__":
    main()

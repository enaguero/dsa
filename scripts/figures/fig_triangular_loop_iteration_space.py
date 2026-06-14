"""Iteration space of the triangular nested loop (§14.3): half the rectangular grid."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from _style import GRAY, INK, NAVY, apply_style, save

N = 12


def main() -> None:
    apply_style()

    # Full rectangular grid (§14.2) and the subset the triangular loop executes.
    all_points = [(i, j) for i in range(1, N + 1) for j in range(1, N + 1)]
    executed = [(i, j) for i in range(1, N + 1) for j in range(i, N + 1)]
    assert len(executed) == N * (N + 1) // 2

    fig, ax = plt.subplots(figsize=(4.5, 4.8))
    ax.set_aspect("equal")

    # All n^2 points of the rectangular loop: small open circles.
    xs = [j for _, j in all_points]
    ys = [i for i, _ in all_points]
    ax.scatter(xs, ys, s=14, facecolors="white", edgecolors=GRAY,
               linewidths=0.7, zorder=2)

    # Points actually executed by the triangular loop (j >= i): filled dots.
    xs_t = [j for _, j in executed]
    ys_t = [i for i, _ in executed]
    ax.scatter(xs_t, ys_t, s=28, facecolors=NAVY, edgecolors="white",
               linewidths=0.6, zorder=3)

    # Dotted square outlining the full n x n grid.
    ax.add_patch(plt.Rectangle((0.5, 0.5), N, N, fill=False, edgecolor=GRAY,
                               linestyle=(0, (1.5, 2)), linewidth=0.9, zorder=1))

    # Diagonal j = i separating executed from skipped points; label placed
    # just past the line's lower end, outside the grid.
    ax.plot([0.5, N + 0.5], [0.5, N + 0.5], color=INK, linewidth=0.9, zorder=1)
    ax.text(N + 1.0, N + 0.85, "$j = i$", rotation=-45,
            rotation_mode="anchor", ha="left", va="center",
            fontsize=9, color=INK)

    # Rectangular-loop annotation outside the top edge of the grid.
    ax.text((N + 1) / 2, -0.35, "rectangular loop (§14.2): $n^2$ iterations",
            ha="center", va="bottom", fontsize=9, color=GRAY)

    # Triangular-loop annotation in the empty lower-left triangle,
    # with an arrow into the middle of the filled region.
    ax.annotate(
        "triangular loop (§14.3):\n$n(n+1)/2 \\approx n^2/2$ iterations",
        xy=(8.5, 5.2), xytext=(3.5, 9.5),
        ha="center", va="center", fontsize=9, color=NAVY,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none"),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, linewidth=0.9,
                        shrinkA=16, shrinkB=6),
    )

    # Axes: i = 1 at the top so the picture reads in loop-execution order.
    ax.set_xlim(-0.2, N + 2.0)
    ax.set_ylim(N + 1.6, -1.1)
    ax.set_xticks([1, N], labels=["$1$", "$n$"])
    ax.set_yticks([1, N], labels=["$1$", "$n$"])
    ax.set_xlabel("$j$ (inner)")
    ax.set_ylabel("$i$ (outer)", rotation=0, ha="right", va="center")
    ax.spines["left"].set_bounds(1, N)
    ax.spines["bottom"].set_bounds(1, N)

    save(fig, "triangular-loop-iteration-space")


if __name__ == "__main__":
    main()

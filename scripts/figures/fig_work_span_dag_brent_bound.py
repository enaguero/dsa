"""Computation DAG (work vs. span) and Brent's bound T_p = max(W/p, S) — §31.2."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save


LEVEL_DY = 0.36  # vertical distance between DAG levels (equal-aspect coords)


def build_dag():
    """Fork-join DAG: 12 nodes in 6 levels; returns positions, edges, critical path."""
    levels = [["s"], ["a", "b"], ["c", "d", "e", "f"], ["g", "h"], ["i", "j"], ["t"]]
    spread = {1: [0.5], 2: [0.27, 0.73], 4: [0.08, 0.36, 0.64, 0.92]}
    pos = {}
    for depth, names in enumerate(levels):
        for name, x in zip(names, spread[len(names)]):
            pos[name] = (x, -depth * LEVEL_DY)
    edges = [
        ("s", "a"), ("s", "b"),
        ("a", "c"), ("a", "d"), ("b", "e"), ("b", "f"),
        ("c", "g"), ("d", "g"), ("e", "h"), ("f", "h"),
        ("g", "i"), ("h", "j"),
        ("i", "t"), ("j", "t"),
    ]
    critical = ["s", "a", "c", "g", "i", "t"]
    return pos, edges, critical


def draw_dag(ax):
    pos, edges, critical = build_dag()
    crit_edges = set(zip(critical, critical[1:]))
    r = 0.055

    for u, v in edges:
        on_path = (u, v) in crit_edges
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        # shrink endpoints to the circle boundary
        d = np.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / d, (y1 - y0) / d
        ax.annotate(
            "",
            xy=(x1 - ux * r * 1.15, y1 - uy * r * 1.15),
            xytext=(x0 + ux * r * 1.15, y0 + uy * r * 1.15),
            arrowprops=dict(
                arrowstyle="->",
                lw=2.2 if on_path else 0.9,
                color=NAVY if on_path else GRAY,
                shrinkA=0,
                shrinkB=0,
            ),
        )

    for name, (x, y) in pos.items():
        on_path = name in critical
        ax.add_patch(
            Circle(
                (x, y),
                r,
                facecolor=NAVY if on_path else "white",
                edgecolor=NAVY if on_path else INK,
                lw=1.6 if on_path else 0.9,
                zorder=3,
            )
        )

    y_bottom = -5 * LEVEL_DY
    ax.text(
        0.5, y_bottom - 0.22,
        "$W$ = total nodes = 12",
        ha="center", va="top", fontsize=9.5, color=INK,
    )
    ax.text(
        0.5, y_bottom - 0.40,
        "$S$ = longest path = 6  (filled)",
        ha="center", va="top", fontsize=9.5, color=NAVY,
    )
    ax.set_title("Computation DAG: work and span")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(y_bottom - 0.58, 0.12)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_brent(ax):
    W, S = 1024, 16
    p = np.logspace(0, np.log2(1024), 200, base=2)
    knee = W / S

    ax.loglog(p, W / p, ls="--", lw=1.2, color=GRAY,
              label=r"$W/p$ (perfect speedup)")
    ax.loglog(p, np.full_like(p, S), ls=":", lw=1.4, color=ORANGE,
              label=r"$S$ (critical path)")
    ax.loglog(p, np.maximum(W / p, S), lw=2.6, color=NAVY,
              label=r"$T_p = \max(W/p,\, S)$")

    ax.axvline(knee, ls=(0, (2, 3)), lw=0.9, color=GRAY)
    ax.annotate(
        "knee: $p = W/S = 64$\n(parallelism)",
        xy=(knee, S * 1.25), xytext=(knee * 1.9, 130),
        fontsize=8.5, color=INK, ha="left",
        arrowprops=dict(arrowstyle="->", lw=0.8, color=INK,
                        connectionstyle="arc3,rad=-0.3"),
    )
    ax.text(6, 420, "work-limited:\nmore processors help",
            fontsize=8, color=INK, ha="center", style="italic")
    ax.text(400, 33, "span-limited: extra\nprocessors are wasted",
            fontsize=8, color=INK, ha="center", style="italic")

    ax.set_xlabel("processors $p$")
    ax.set_ylabel("time $T_p$")
    ax.set_title(r"Brent's bound  ($W = 1024$, $S = 16$)")
    ticks = [1, 4, 16, 64, 256, 1024]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.set_yticks([1, 16, 64, 256, 1024])
    ax.set_yticklabels(["1", "16", "64", "256", "1024"])
    ax.minorticks_off()
    ax.set_xlim(1, 1024)
    ax.set_ylim(6, 1400)
    ax.grid(True, which="major", color=LIGHT, lw=0.6)
    ax.set_axisbelow(True)
    leg = ax.legend(loc="lower left", frameon=True, borderpad=0.4)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_edgecolor("none")


def main():
    apply_style()
    fig, (ax_dag, ax_plot) = plt.subplots(
        1, 2, figsize=(6.0, 3.1), gridspec_kw={"width_ratios": [1, 1.25]}
    )
    draw_dag(ax_dag)
    draw_brent(ax_plot)
    fig.tight_layout(w_pad=1.5)
    save(fig, "work-span-dag-brent-bound")


if __name__ == "__main__":
    main()

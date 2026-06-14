"""Why build-heap is Theta(n): per-level node counts vs sift costs for n=127 (section 24.5)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

from _style import GRAY, INK, LIGHT, NAVY, apply_style, save

# Concrete full heap: n = 127, h = 6.
H = 6
depths = np.arange(H + 1)
nodes = 2**depths  # nodes at depth d
cost = H - depths  # sift-down swaps per node at depth d
naive_level = nodes * H  # naive charge: every node pays h
true_level = nodes * cost  # true charge: node at depth d pays h - d
n = int(nodes.sum())

apply_style()

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(6.0, 3.5), gridspec_kw={"width_ratios": [1.0, 1.25], "wspace": 0.08}
)

BAR_H = 0.58
ys = -depths.astype(float)

# ---------------------------------------------------------------- panel (a)
# The heap, level by level: bar widths proportional to node counts.
TRI_CENTER, TRI_HALF = 0.54, 0.31
for d in depths:
    w = max(2 * TRI_HALF * nodes[d] / nodes[-1], 0.018)
    ax1.add_patch(
        Rectangle(
            (TRI_CENTER - w / 2, ys[d] - BAR_H / 2),
            w,
            BAR_H,
            facecolor=LIGHT,
            edgecolor=INK,
            linewidth=0.8,
        )
    )
    ax1.text(0.17, ys[d], f"{nodes[d]}", ha="right", va="center", fontsize=9, color=INK)
    ax1.text(0.91, ys[d], f"{cost[d]}", ha="left", va="center", fontsize=9, color=INK)

# Column headers.
ax1.text(0.17, 0.92, "nodes\n$2^d$", ha="right", va="bottom", fontsize=8.5, color=GRAY)
ax1.text(0.91, 0.92, "cost\n$h-d$", ha="left", va="bottom", fontsize=8.5, color=GRAY)

# Callouts: expensive-but-rare root, cheap-but-plentiful leaves.
ax1.annotate(
    "cost 6, but\nonly 1 node",
    xy=(TRI_CENTER - 0.015, -0.1),
    xytext=(0.35, -0.85),
    ha="center",
    va="center",
    fontsize=8,
    color=INK,
    arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.7, "shrinkB": 3},
)
ax1.annotate(
    "half of all nodes —\nsift cost 0",
    xy=(TRI_CENTER, ys[-1] - BAR_H / 2),
    xytext=(TRI_CENTER, -7.45),
    ha="center",
    va="top",
    fontsize=8,
    color=INK,
    arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.7, "shrinkB": 2},
)

ax1.set_xlim(0, 1.04)
ax1.set_yticks(ys)
ax1.set_yticklabels([f"{d}" for d in depths])
ax1.set_ylabel("depth $d$")
ax1.set_xticks([])
ax1.spines["bottom"].set_visible(False)
ax1.set_title("(a)  the heap, level by level", fontsize=9.5)

# ---------------------------------------------------------------- panel (b)
# Total swaps per level: naive charge (hatched outline) vs true cost (solid).
ax2.barh(
    ys,
    naive_level,
    height=BAR_H,
    facecolor="none",
    edgecolor=GRAY,
    hatch="/////",
    linewidth=0.8,
    zorder=2,
)
ax2.barh(ys, true_level, height=BAR_H, facecolor=NAVY, edgecolor=NAVY, linewidth=0.5, zorder=3)

# Per-level true values; naive values where the gap is dramatic.
LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "pad": 1.0}
for d in depths:
    if true_level[d] > 0:
        ax2.text(
            true_level[d] + 5,
            ys[d],
            f"{true_level[d]}",
            ha="left",
            va="center",
            fontsize=7.5,
            color=NAVY,
            zorder=4,
            bbox=LABEL_BOX,
        )
ax2.text(5, ys[-1], "0", ha="left", va="center", fontsize=7.5, color=NAVY, bbox=LABEL_BOX)
for d in (5, 6):
    ax2.text(
        naive_level[d] - 8,
        ys[d],
        f"{naive_level[d]}",
        ha="right",
        va="center",
        fontsize=7.5,
        color=GRAY,
        zorder=4,
        bbox=LABEL_BOX,
    )

legend = ax2.legend(
    handles=[
        Patch(facecolor="none", edgecolor=GRAY, hatch="/////", linewidth=0.8),
        Patch(facecolor=NAVY, edgecolor=NAVY),
    ],
    labels=["naive: every node pays $h$", "true: depth $d$ pays $h-d$"],
    loc="upper right",
    bbox_to_anchor=(1.0, 1.0),
    handlelength=1.4,
    handleheight=1.1,
    labelspacing=0.45,
)

ax2.text(
    378,
    -2.45,
    f"$\\sum$ naive $= n\\,h = {int(naive_level.sum())} \\approx n\\log n$",
    ha="right",
    va="center",
    fontsize=8.5,
    color=GRAY,
)
ax2.text(
    378,
    -3.15,
    f"$\\sum$ true $= {int(true_level.sum())} < 2n = {2 * n} \\;\\Rightarrow\\; \\Theta(n)$",
    ha="right",
    va="center",
    fontsize=8.5,
    color=NAVY,
)

ax2.set_xlim(0, 392)
ax2.set_xticks([0, 96, 192, 288, 384])
ax2.set_xlabel("swaps at depth $d$  (nodes $\\times$ cost)")
ax2.set_yticks([])
ax2.spines["left"].set_visible(False)
ax2.xaxis.grid(True, zorder=0)
ax2.set_axisbelow(True)
ax2.set_title("(b)  total swaps per level", fontsize=9.5)

for ax in (ax1, ax2):
    ax.set_ylim(-7.95, 1.55)

fig.suptitle(f"Building a heap on $n = {n}$ ($h = 6$)", fontsize=10.5, y=1.0)

save(fig, "build-heap-linear-level-work")

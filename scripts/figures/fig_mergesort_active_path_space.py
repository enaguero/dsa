"""Mergesort recursion tree (n=16) with one live root-to-leaf path on the call stack, showing Theta(n) auxiliary space — section 20.3."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt

from _style import GRAY, INK, LIGHT, NAVY, apply_style, save

# ------------------------------------------------------------------ recursion
N = 16
DEPTH = N.bit_length()  # 5 levels: subproblem sizes 16, 8, 4, 2, 1

# subproblem size at each level, straight from the recurrence n -> n/2
level_size = [N >> d for d in range(DEPTH)]
assert level_size[-1] == 1

# scratch arrays alive on one root-to-leaf path: one merge active per level
path_scratch = sum(level_size)
assert path_scratch < 2 * N  # 16 + 8 + 4 + 2 + 1 = 31 < 2n = 32

# ------------------------------------------------------------------- layout
TREE_X0, TREE_X1 = 0.025, 0.665
YS = [0.845, 0.705, 0.565, 0.425, 0.285]  # y of levels 0..4


def node_x(d: int, i: int) -> float:
    return TREE_X0 + (i + 0.5) / (1 << d) * (TREE_X1 - TREE_X0)


def is_active(d: int, i: int) -> bool:
    return i == (1 << d) - 1  # rightmost node of its level


apply_style()
fig = plt.figure(figsize=(6.0, 4.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ---------------------------------------------------------------- tree edges
for d in range(DEPTH - 1):
    for i in range(1 << d):
        for child in (2 * i, 2 * i + 1):
            live = is_active(d, i) and is_active(d + 1, child)
            ax.plot(
                [node_x(d, i), node_x(d + 1, child)], [YS[d], YS[d + 1]],
                color=NAVY if live else GRAY,
                lw=2.2 if live else 0.8,
                ls="-" if live else (0, (2.5, 2.5)),
                zorder=3 if live else 2,
            )

# ---------------------------------------------------------------- tree nodes
for d in range(DEPTH):
    leaf = d == DEPTH - 1
    for i in range(1 << d):
        live = is_active(d, i)
        ax.text(
            node_x(d, i), YS[d], f"{level_size[d]}",
            ha="center", va="center",
            fontsize=6.5 if leaf else 9,
            fontweight="bold" if live else "normal",
            color=NAVY if live else GRAY, zorder=5,
            bbox=dict(
                boxstyle="square,pad=0.18" if leaf else "round,pad=0.3",
                fc="white",
                ec=NAVY if live else GRAY,
                lw=1.5 if live else 0.7,
                ls="-" if live else (0, (3, 2)),
            ),
        )

# gray annotation: everything off the active path takes no memory right now
ax.annotate(
    "already returned, or\nnot yet called",
    xy=(node_x(2, 1) + 0.008, YS[2] - 0.032), xytext=(0.13, 0.155),
    ha="center", va="center", fontsize=8.5, color=GRAY, style="italic",
    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9,
                    connectionstyle="arc3,rad=0.22"),
    zorder=5,
)

# ----------------------------------------------------------- call stack panel
STACK_X = 0.852
FRAME_W = 0.105  # half-width of a stack frame box (via pad below)

ax.text(STACK_X, 0.935, "call stack right now", ha="center", va="center",
        fontsize=9.5, color=INK, style="italic")

for d in range(DEPTH):
    # connector from the live tree node to its stack frame
    ax.plot([node_x(d, (1 << d) - 1) + 0.022, STACK_X - FRAME_W], [YS[d], YS[d]],
            color=NAVY, lw=0.7, ls=(0, (1, 2)), zorder=1)
    ax.text(STACK_X, YS[d], f"merge_sort(n={level_size[d]})",
            ha="center", va="center", fontsize=8, family="monospace",
            color=INK, zorder=5,
            bbox=dict(boxstyle="square,pad=0.42", fc=LIGHT, ec=NAVY, lw=1.1))

# square bracket spanning the frames: depth = Theta(log n)
bx, tick = 0.978, 0.008
ax.plot([bx, bx], [YS[-1], YS[0]], color=INK, lw=1.0)
ax.plot([bx - tick, bx], [YS[0], YS[0]], color=INK, lw=1.0)
ax.plot([bx - tick, bx], [YS[-1], YS[-1]], color=INK, lw=1.0)
ax.text(0.997, (YS[0] + YS[-1]) / 2, r"depth $= \Theta(\log n)$ frames",
        ha="center", va="center", fontsize=8.5, color=INK, rotation=90)

# ------------------------------------------------------------ title + payoff
ax.text(0.5, 0.995, r"Why $S(n) = S(n/b) + g(n)$: only one branch is live at a time",
        ha="center", va="center", fontsize=11, color=INK)

sum_str = "+".join(str(s) for s in level_size)
ax.text(0.5, 0.05,
        rf"scratch arrays on the active path: ${sum_str} = {path_scratch} < 2n$"
        r"$\;\Rightarrow\;\Theta(n)$ auxiliary space — not $\Theta(n\,\log n)$",
        ha="center", va="center", fontsize=9.5, color=INK, zorder=6,
        bbox=dict(boxstyle="round,pad=0.45", fc=LIGHT, ec=NAVY, lw=0.9))

save(fig, "mergesort-active-path-space")

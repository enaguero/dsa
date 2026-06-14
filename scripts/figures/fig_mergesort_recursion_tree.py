"""Recursion tree for T(n) = 2 T(n/2) + n (ram_model.md §16.2).

The canonical mergesort recursion: every level of the tree contributes
exactly n units of non-recursive work, the tree has log_2 n + 1 levels,
so T(n) = n * (log_2 n + 1) = Theta(n log n). Each level is annotated
with its subproblem size, its node count, and its per-level sum.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyBboxPatch, Rectangle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    ax.set_xlim(0.0, 12.0)
    ax.set_ylim(0.0, 8.6)
    ax.set_aspect("auto")
    ax.axis("off")

    # ---- tree layout ------------------------------------------------------
    # Levels 0..3 drawn explicitly, then ... , then leaves.
    LEFT, RIGHT = 1.6, 8.4  # the canvas x-span used by the tree itself
    TOP_Y = 7.7
    DY = 1.15  # row spacing
    NODE_W, NODE_H = 0.80, 0.50

    # Spans for child centers in each level
    def centers(level):
        n = 2 ** level
        # Spread n nodes evenly across [LEFT, RIGHT]
        if n == 1:
            return [(LEFT + RIGHT) / 2]
        step = (RIGHT - LEFT) / (n - 1)
        return [LEFT + i * step for i in range(n)]

    sizes = [r"$n$", r"$n/2$", r"$n/4$", r"$n/8$"]

    def draw_node(cx, cy, label, hot=False):
        x0 = cx - NODE_W / 2
        y0 = cy - NODE_H / 2
        ax.add_patch(FancyBboxPatch(
            (x0, y0), NODE_W, NODE_H,
            boxstyle="round,pad=0.01,rounding_size=0.10",
            fc=to_rgba(NAVY, 0.10) if hot else "white",
            ec=NAVY if hot else INK, lw=1.0,
        ))
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=10, color=INK)

    # Draw levels 0..3 (drawing inner subset only when n > 4 to avoid clutter)
    level_ys = [TOP_Y - k * DY for k in range(4)]
    level_centers = [centers(k) for k in range(4)]

    # Connect parents -> children with line segments
    for k in range(3):
        parent_ys = level_ys[k]
        child_ys = level_ys[k + 1]
        for j, pcx in enumerate(level_centers[k]):
            lcx = level_centers[k + 1][2 * j]
            rcx = level_centers[k + 1][2 * j + 1]
            ax.plot([pcx, lcx], [parent_ys - NODE_H / 2, child_ys + NODE_H / 2],
                    color=INK, lw=0.9)
            ax.plot([pcx, rcx], [parent_ys - NODE_H / 2, child_ys + NODE_H / 2],
                    color=INK, lw=0.9)

    # Draw the nodes at each level
    for k in range(4):
        for cx in level_centers[k]:
            draw_node(cx, level_ys[k], sizes[k])

    # ---- middle dots row ('...') ----------------------------------------
    mid_y = level_ys[3] - DY * 0.85
    for cx in level_centers[3]:
        ax.text(cx, mid_y, r"$\vdots$", ha="center", va="center",
                fontsize=11, color=GRAY)

    # ---- leaves row (1's) ----------------------------------------------
    leaf_y = mid_y - DY
    # Pretend there are many leaves; show a row of small squares.
    # Keep the row a little inside the level columns so the left "Level..."
    # label has clear breathing room.
    n_leaves_draw = 14
    leaf_left, leaf_right = LEFT + 0.30, RIGHT - 0.30
    leaf_w = (leaf_right - leaf_left) / (n_leaves_draw - 1) * 0.55
    for j in range(n_leaves_draw):
        cx = leaf_left + j * (leaf_right - leaf_left) / (n_leaves_draw - 1)
        ax.add_patch(Rectangle((cx - leaf_w / 2, leaf_y - 0.16),
                               leaf_w, 0.32,
                               fc=to_rgba(ORANGE, 0.16),
                               ec=ORANGE, lw=0.8))
        ax.text(cx, leaf_y, "1", ha="center", va="center",
                fontsize=7.5, color=INK)

    # ---- left-hand level labels and right-hand sums ---------------------
    LBL_X = 0.10
    SUM_X = 9.6

    def level_text(y, label, sum_text):
        ax.text(LBL_X, y, label, ha="left", va="center",
                fontsize=9, color=INK)
        ax.text(SUM_X, y, sum_text, ha="left", va="center",
                fontsize=10, color=NAVY, weight="bold")

    level_text(level_ys[0], "Level $0$:",
               r"sum $= n$")
    level_text(level_ys[1], "Level $1$:",
               r"sum $= 2 \cdot (n/2) = n$")
    level_text(level_ys[2], "Level $2$:",
               r"sum $= 4 \cdot (n/4) = n$")
    level_text(level_ys[3], "Level $3$:",
               r"sum $= 8 \cdot (n/8) = n$")
    ax.text(LBL_X, mid_y, r"$\vdots$", ha="left", va="center",
            fontsize=11, color=GRAY)
    ax.text(SUM_X, mid_y, r"$\vdots$", ha="left", va="center",
            fontsize=11, color=NAVY)
    level_text(leaf_y, r"Level  $\log_{2} n$:",
               r"sum $= n \cdot \Theta(1) = n$")

    # Vertical brace on the right showing 'log_2 n + 1 levels'
    brace_x = 11.55
    brace_top = level_ys[0]
    brace_bot = leaf_y
    ax.annotate("",
                xy=(brace_x, brace_top), xytext=(brace_x, brace_bot),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(brace_x + 0.10, (brace_top + brace_bot) / 2,
            r"$\log_2 n + 1$" + "\nlevels",
            ha="left", va="center", fontsize=8.5, color=INK,
            linespacing=1.15)

    # ---- bottom-line conclusion box --------------------------------------
    box_y0, box_y1 = 0.10, 0.95
    box_x0, box_x1 = 1.4, 10.6
    ax.add_patch(FancyBboxPatch(
        (box_x0, box_y0), box_x1 - box_x0, box_y1 - box_y0,
        boxstyle="round,pad=0.04,rounding_size=0.14",
        fc=LIGHT, ec=NAVY, lw=1.0,
    ))
    ax.text((box_x0 + box_x1) / 2, (box_y0 + box_y1) / 2 + 0.13,
            r"$(\log_2 n + 1)$ levels   $\times$   work $n$ per level",
            ha="center", va="center", fontsize=10.5, color=INK)
    ax.text((box_x0 + box_x1) / 2, (box_y0 + box_y1) / 2 - 0.20,
            r"$T(n) \;=\; n \cdot (\log_2 n + 1) \;=\; \Theta(n \log n)$",
            ha="center", va="center", fontsize=11.5, color=NAVY,
            weight="bold")

    save(fig, "mergesort-recursion-tree")


if __name__ == "__main__":
    main()

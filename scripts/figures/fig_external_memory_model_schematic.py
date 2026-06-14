"""The Aggarwal-Vitter external memory model (§29.1): fast internal memory of size M holding M/B blocks of B items, an unbounded disk, and the cost model that charges only for block transfers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, Rectangle

from _style import GRAY, INK, NAVY, ORANGE, TEAL, apply_style, save

# Model instance drawn: B items per block, M/B slots internally, disk strip.
B = 4                 # items per block
SLOTS = 4             # M/B block slots -> M = 16
DISK_BLOCKS = 8       # blocks shown on disk before the ellipsis
CW, CH = 0.36, 0.60   # cell width/height in data units

INT_X0, INT_Y0 = 6.0, 3.9     # internal memory strip origin
DSK_X0, DSK_Y0 = 0.35, 0.8    # external memory strip origin

# (slot index, disk block index, hatch, color) for the two resident blocks
RESIDENT = (0, 2, "////", NAVY)
IN_TRANSIT = (2, 5, "\\\\\\\\", TEAL)


def strip(ax, x0, y0, n_cells, n_per_block, loaded):
    """Row of cells with heavy block boundaries; `loaded` maps block -> (hatch, color)."""
    for b, (hatch, color) in loaded.items():
        ax.add_patch(Rectangle((x0 + b * n_per_block * CW, y0), n_per_block * CW, CH,
                               fc=to_rgba(color, 0.10), ec=color, hatch=hatch, lw=0))
    for i in range(1, n_cells):
        x = x0 + i * CW
        ax.plot([x, x], [y0, y0 + CH], color=INK, lw=0.45)
    for b in range(0, n_cells + 1, n_per_block):
        x = x0 + b * CW
        ax.plot([x, x], [y0, y0 + CH], color=INK, lw=1.5)
    w = n_cells * CW
    ax.plot([x0, x0 + w], [y0, y0], color=INK, lw=1.5)
    ax.plot([x0, x0 + w], [y0 + CH, y0 + CH], color=INK, lw=1.5)


def brace(ax, x0, x1, y, depth, pointing="up", color=INK):
    """Curly brace spanning [x0, x1], flat ends at y, tip at y +/- depth."""
    n = 257
    x = np.linspace(x0, x1, n)
    beta = 36.0 / (x1 - x0)
    xh = x[: n // 2 + 1]
    yh = 1.0 / (1 + np.exp(-beta * (xh - x0))) + 1.0 / (1 + np.exp(-beta * (xh - xh[-1])))
    yh = (yh - yh[0]) / (yh[-1] - yh[0])           # 0 at ends, 1 at tip
    yc = np.concatenate((yh, yh[-2::-1]))
    sign = 1 if pointing == "up" else -1
    ax.plot(x, y + sign * depth * yc, color=color, lw=1.0, solid_capstyle="round")


def block_center(x0, b):
    return x0 + (b + 0.5) * B * CW


def main():
    apply_style()
    fig, ax = plt.subplots(figsize=(6.0, 2.85))
    ax.set_xlim(-0.1, 12.9)
    ax.set_ylim(-0.6, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")

    s_res, d_res, h_res, c_res = RESIDENT
    s_tr, d_tr, h_tr, c_tr = IN_TRANSIT

    # ------------------------------------------------ internal memory strip --
    strip(ax, INT_X0, INT_Y0, SLOTS * B, B,
          {s_res: (h_res, c_res), s_tr: (h_tr, c_tr)})
    int_w = SLOTS * B * CW
    brace(ax, INT_X0, INT_X0 + int_w, INT_Y0 + CH + 0.10, 0.22, pointing="up")
    ax.text(INT_X0 + int_w / 2, INT_Y0 + CH + 0.52,
            "internal memory (fast): size $M$  =  $M/B$ block slots",
            fontsize=8.5, color=INK, ha="center", va="bottom")
    ax.text(INT_X0 + int_w / 2, INT_Y0 + CH + 0.38,
            "(drawn: $M=16$, $B=4$, so $M/B=4$ slots)",
            fontsize=7, style="italic", color=GRAY, ha="center", va="top")

    # brace under one slot: a block of B items
    bx0 = INT_X0 + s_res * B * CW
    brace(ax, bx0, bx0 + B * CW, INT_Y0 - 0.10, 0.22, pointing="down")
    ax.text(bx0 + B * CW / 2, INT_Y0 - 0.44, "one block $=$ $B$ items",
            fontsize=7.5, color=INK, ha="center", va="top")

    # ------------------------------------------------ external memory strip --
    strip(ax, DSK_X0, DSK_Y0, DISK_BLOCKS * B, B,
          {d_res: (h_res, c_res), d_tr: (h_tr, c_tr)})
    dsk_w = DISK_BLOCKS * B * CW
    ax.text(DSK_X0 + dsk_w + 0.22, DSK_Y0 + CH / 2, r"$\cdots$",
            fontsize=12, color=INK, ha="left", va="center")
    ax.text(DSK_X0, DSK_Y0 - 0.18,
            "external memory (disk): unbounded — $N$ items in $N/B$ blocks",
            fontsize=8.5, color=INK, ha="left", va="top")

    # ------------------------------------------------------------- CPU box --
    ax.add_patch(Rectangle((1.1, 3.8), 1.6, 0.8, fc="white", ec=INK, lw=1.2))
    ax.text(1.9, 4.2, "CPU", fontsize=10, weight="bold", color=INK,
            ha="center", va="center")

    # CPU <-> internal memory: free
    ax.add_patch(FancyArrowPatch((2.78, 4.2), (INT_X0 - 0.08, 4.2),
                                 arrowstyle="<|-|>", mutation_scale=9,
                                 lw=1.0, color=INK))
    ax.text(4.35, 4.34, "compute: free", fontsize=8, style="italic",
            color=INK, ha="center", va="bottom")
    ax.text(4.35, 4.06, "(touches internal memory only)", fontsize=6.8,
            style="italic", color=GRAY, ha="center", va="top")

    # ------------------------- resident block: same hatching, dashed tie ----
    ax.plot([block_center(INT_X0, s_res), block_center(DSK_X0, d_res)],
            [INT_Y0 - 0.70, DSK_Y0 + CH + 0.06],
            color=c_res, lw=0.9, ls=(0, (4, 3)))
    ax.text(block_center(DSK_X0, d_res) - 0.15, 2.42,
            "already loaded\n(same hatching)", fontsize=7, style="italic",
            color=c_res, ha="right", va="center", linespacing=1.2)

    # ------------------- the key arrow: one block transfer costs one I/O ----
    ax.add_patch(FancyArrowPatch((block_center(INT_X0, s_tr), INT_Y0 - 0.08),
                                 (block_center(DSK_X0, d_tr), DSK_Y0 + CH + 0.08),
                                 arrowstyle="<|-|>", mutation_scale=14,
                                 lw=2.6, color=ORANGE))
    lx = block_center(INT_X0, s_tr) + 0.35
    ax.text(lx, 2.85, "block transfer $=$ 1 I/O", fontsize=9.5,
            weight="bold", color=ORANGE, ha="left", va="center")
    ax.text(lx, 2.47, "the only operation that costs", fontsize=8,
            style="italic", color=INK, ha="left", va="center")

    # ------------------------------------------------------------- footer ---
    ax.text(6.4, -0.55, "Cost model: count block transfers (I/Os);"
            " CPU computation on data in internal memory is free.",
            fontsize=8, style="italic", color=INK, ha="center", va="top")

    save(fig, "external-memory-model-schematic")


if __name__ == "__main__":
    main()

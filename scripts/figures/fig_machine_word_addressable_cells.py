"""Machine word as both an integer and a memory address (ram_model.md §3.3).

A w-bit word `R[j]` simultaneously names a non-negative integer in
[0, 2^w - 1] and a cell index into memory. The figure stacks both readings
vertically and uses an orange arrow to mark "this same w-bit pattern is
also an address" — the indirect-addressing arrow from the RAM model.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save

W = 8                       # word width for the picture
BITS = [0, 1, 0, 0, 1, 1, 0, 1]  # = 77 base-10
ADDR = sum(b << (W - 1 - i) for i, b in enumerate(BITS))   # 77
N_CELLS = 1 << W            # 2^w = 256
SHOW_HEAD_CELLS = 5         # how many low-address cells to draw before the hot one
SHOW_TAIL_CELLS = 4         # how many tail cells to draw after the hot one


# ------------------------------------------------------------- layout --------
BIT_X0, BIT_W, BIT_H = 1.2, 0.66, 0.78  # word-cell geometry
WORD_TOP = 7.4

MEM_X0, MEM_X1 = 0.6, 11.0
MEM_TOP = 2.6
MEM_CH = 0.62


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.set_xlim(-0.1, 11.7)
    ax.set_ylim(0.0, 8.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---------- title strip for "one machine word: w bits  (here w = 8)" ----
    ax.text(
        BIT_X0 + W * BIT_W / 2,
        WORD_TOP + 0.95,
        r"one machine word: $w$ bits   (here $w = 8$)",
        ha="center",
        va="bottom",
        fontsize=9.5,
        style="italic",
        color=INK,
    )

    # ---------- row of bit cells ------------------------------------------
    for i, b in enumerate(BITS):
        x0 = BIT_X0 + i * BIT_W
        ax.add_patch(Rectangle((x0, WORD_TOP), BIT_W, BIT_H,
                               fc=to_rgba(NAVY, 0.10) if b else "white",
                               ec=INK, lw=1.0))
        ax.text(x0 + BIT_W / 2, WORD_TOP + BIT_H / 2,
                str(b), ha="center", va="center",
                fontsize=12, color=NAVY if b else INK,
                weight="bold" if b else "normal",
                family="monospace")

    # left tag "R[j] ="
    ax.text(BIT_X0 - 0.18, WORD_TOP + BIT_H / 2,
            r"$R[j] \;=\;$", ha="right", va="center", fontsize=11, color=INK)
    # right tag "= 77"
    ax.text(BIT_X0 + W * BIT_W + 0.18, WORD_TOP + BIT_H / 2,
            rf"$=\; {ADDR}$", ha="left", va="center", fontsize=11, color=INK)

    # bit-place exponents under each cell
    for i in range(W):
        x0 = BIT_X0 + i * BIT_W
        ax.text(x0 + BIT_W / 2, WORD_TOP - 0.18,
                rf"$2^{{{W - 1 - i}}}$",
                ha="center", va="top", fontsize=7.5, color=GRAY)

    # ---------- "interpreted as address" arrow ----------------------------
    arrow_top_x = BIT_X0 + W * BIT_W / 2
    # Compute where on the memory strip the hot cell sits, in axes coords.
    # We'll align the arrow tip with the hot cell drawn below.
    n_drawn = SHOW_HEAD_CELLS + 1 + SHOW_TAIL_CELLS  # 0..4, ADDR, last-4
    cell_w = (MEM_X1 - MEM_X0 - 0.6) / (n_drawn + 2)  # 2 gaps for dots
    hot_idx_in_strip = SHOW_HEAD_CELLS + 1   # one gap before the hot cell
    hot_center_x = MEM_X0 + 0.3 + (hot_idx_in_strip + 0.5) * cell_w

    ax.add_patch(FancyArrowPatch(
        (arrow_top_x, WORD_TOP - 0.42),
        (hot_center_x, MEM_TOP + MEM_CH + 0.04),
        arrowstyle="-|>", mutation_scale=14, lw=1.6, color=ORANGE,
        connectionstyle="arc3,rad=-0.12",
    ))
    ax.text(arrow_top_x + 0.55, (WORD_TOP - 0.42 + MEM_TOP + MEM_CH) / 2 + 0.45,
            "interpreted as an address:",
            ha="left", va="center", fontsize=8.5, color=INK)
    ax.text(arrow_top_x + 0.55, (WORD_TOP - 0.42 + MEM_TOP + MEM_CH) / 2 + 0.15,
            r"$w$ bits can name $2^{w}$ distinct cells",
            ha="left", va="center", fontsize=8.5, style="italic", color=INK)

    # ---------- memory strip ----------------------------------------------
    ax.text(MEM_X0, MEM_TOP + MEM_CH + 0.22,
            "memory  $M$:", ha="left", va="bottom", fontsize=9, style="italic",
            color=INK)

    def draw_cell(slot, label, hot=False):
        x0 = MEM_X0 + 0.3 + slot * cell_w
        fc = to_rgba(ORANGE, 0.18) if hot else "white"
        ax.add_patch(Rectangle((x0, MEM_TOP), cell_w * 0.92, MEM_CH,
                               fc=fc, ec=INK, lw=0.9))
        ax.text(x0 + cell_w * 0.46, MEM_TOP + MEM_CH / 2,
                label, ha="center", va="center",
                fontsize=8.0, color=ORANGE if hot else INK,
                weight="bold" if hot else "normal", family="monospace")

    # head cells [0] [1] [2] [3] [4]
    for k in range(SHOW_HEAD_CELLS):
        draw_cell(k, f"[{k}]")
    # gap with dots
    gap_x1 = MEM_X0 + 0.3 + SHOW_HEAD_CELLS * cell_w
    ax.text(gap_x1 + cell_w * 0.5, MEM_TOP + MEM_CH / 2,
            r"$\cdots$", ha="center", va="center", fontsize=10, color=GRAY)
    # hot cell [77]
    draw_cell(hot_idx_in_strip, f"[{ADDR}]", hot=True)
    # gap with dots
    gap_x2 = MEM_X0 + 0.3 + (hot_idx_in_strip + 1) * cell_w
    ax.text(gap_x2 + cell_w * 0.5, MEM_TOP + MEM_CH / 2,
            r"$\cdots$", ha="center", va="center", fontsize=10, color=GRAY)
    # tail cells: last few addresses approaching 255
    tail_start = hot_idx_in_strip + 2
    tail_labels = [N_CELLS - SHOW_TAIL_CELLS + i for i in range(SHOW_TAIL_CELLS)]
    for j, lab in enumerate(tail_labels):
        draw_cell(tail_start + j, f"[{lab}]")

    # bracket spanning the whole memory strip
    last_x = MEM_X0 + 0.3 + (tail_start + SHOW_TAIL_CELLS) * cell_w - cell_w * 0.08
    brace_y = MEM_TOP - 0.10
    brace_low = MEM_TOP - 0.42
    ax.add_patch(FancyBboxPatch(
        (MEM_X0 + 0.30, brace_low),
        last_x - (MEM_X0 + 0.30),
        brace_y - brace_low,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        fc="none", ec=INK, lw=0.8,
    ))
    ax.text((MEM_X0 + 0.30 + last_x) / 2, brace_low - 0.30,
            rf"$2^{{w}} = {N_CELLS}$ addressable cells",
            ha="center", va="top", fontsize=9, color=INK)

    # ---------- transdichotomous assumption box ---------------------------
    box_x0, box_x1 = 0.6, 11.0
    box_y0, box_y1 = 0.20, 1.30
    ax.add_patch(FancyBboxPatch(
        (box_x0, box_y0), box_x1 - box_x0, box_y1 - box_y0,
        boxstyle="round,pad=0.04,rounding_size=0.14",
        fc=LIGHT, ec=NAVY, lw=1.0,
    ))
    cx = (box_x0 + box_x1) / 2
    ax.text(cx, box_y1 - 0.32,
            "transdichotomous assumption",
            ha="center", va="center", fontsize=9, style="italic", color=NAVY)
    ax.text(cx, box_y1 - 0.66,
            r"$n \;\leq\; 2^{w}$   $\Longleftrightarrow$   $w \;\geq\; \log_{2} n$",
            ha="center", va="center", fontsize=10.5, color=INK)
    ax.text(cx, box_y0 + 0.18,
            "(one word must be able to point anywhere in the input)",
            ha="center", va="center", fontsize=7.8, style="italic", color=GRAY)

    save(fig, "machine-word-addressable-cells")


if __name__ == "__main__":
    main()

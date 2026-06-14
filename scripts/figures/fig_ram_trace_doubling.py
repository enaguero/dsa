"""RAM configuration trace for the doubling program on input x = 3 (§2.3).

A four-line program is shown on the left; the right-hand table traces the
five configurations C_0, ..., C_4 in (pc, R[0], R[1], output) coordinates,
with the freshly-changed cell highlighted at each step.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save

PROGRAM = [
    "1: READ  R[0]",
    "2: ADD   R[1], R[0], R[0]",
    "3: WRITE R[1]",
    "4: HALT",
]

# Each row: (label, pc, R0, R1, output, fired-cell index 1..4 (or None))
TRACE = [
    (r"$C_0$",  1, "0", "0", "—",     None),
    (r"$C_1$",  2, "3", "0", "—",     1),   # after line 1 (READ R[0])
    (r"$C_2$",  3, "3", "6", "—",     2),   # after line 2 (ADD)
    (r"$C_3$",  4, "3", "6", "$6$",   3),   # after line 3 (WRITE)
    (r"$C_4$",  "—", "3", "6", "$6$", 4),  # after HALT
]


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    fig.subplots_adjust(bottom=0.12, top=0.96, left=0.04, right=0.98)
    ax.set_xlim(0.0, 12.4)
    ax.set_ylim(0.4, 6.0)
    ax.set_aspect("auto")
    ax.axis("off")

    # ---------- left: program listing ------------------------------------
    PROG_X0, PROG_X1 = 0.20, 4.30
    PROG_Y0, PROG_Y1 = 1.10, 5.40
    ax.add_patch(FancyBboxPatch(
        (PROG_X0, PROG_Y0), PROG_X1 - PROG_X0, PROG_Y1 - PROG_Y0,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        fc="white", ec=INK, lw=1.0,
    ))
    ax.text((PROG_X0 + PROG_X1) / 2, PROG_Y1 - 0.32,
            "Program $P$  (doubles its input)",
            ha="center", va="center", fontsize=9, style="italic", color=INK)
    line_ys = [PROG_Y1 - 0.80 - i * 0.70 for i in range(len(PROGRAM))]
    for txt, y in zip(PROGRAM, line_ys):
        ax.text(PROG_X0 + 0.20, y, txt,
                family="monospace", fontsize=9, color=INK,
                ha="left", va="center")

    ax.text((PROG_X0 + PROG_X1) / 2, PROG_Y0 - 0.34,
            "input tape: $x = 3$",
            ha="center", va="top", fontsize=8.5, color=GRAY)

    # ---------- right: trace table ---------------------------------------
    TAB_X0 = 5.10
    col_xs = [TAB_X0 + 0.30,           # label
              TAB_X0 + 1.20,           # pc
              TAB_X0 + 2.10,           # R0
              TAB_X0 + 3.20,           # R1
              TAB_X0 + 4.40]           # output
    HEADERS = [r"$C_t$", r"$\ell$ (pc)", r"$R[0]$", r"$R[1]$", "output"]
    TOP_Y = 5.10
    DY = 0.68

    # Header strip
    ax.add_patch(Rectangle((TAB_X0, TOP_Y - 0.12),
                           (col_xs[-1] - TAB_X0) + 1.6, 0.50,
                           fc=LIGHT, ec="none"))
    for x, h in zip(col_xs, HEADERS):
        ax.text(x, TOP_Y + 0.12, h, ha="center", va="center",
                fontsize=9.0, color=INK, weight="bold")
    ax.axhline = None  # no-op — separator drawn below
    ax.plot([TAB_X0 - 0.10, col_xs[-1] + 1.55],
            [TOP_Y - 0.20, TOP_Y - 0.20],
            color=INK, lw=0.9)

    # Rows
    for j, (lbl, pc, r0, r1, out, fired) in enumerate(TRACE):
        y = TOP_Y - 0.65 - j * DY
        vals = [lbl, str(pc), r0, r1, out]
        # subtle banding
        if j % 2 == 0:
            ax.add_patch(Rectangle((TAB_X0 - 0.10, y - 0.30),
                                   col_xs[-1] - TAB_X0 + 1.65, 0.60,
                                   fc=to_rgba(NAVY, 0.05), ec="none"))
        for x, val in zip(col_xs, vals):
            ax.text(x, y, val, ha="center", va="center",
                    fontsize=9.5, color=INK)

        # mark the "just-fired line" with an orange tag at the end
        if fired is not None:
            ax.text(col_xs[-1] + 1.40, y,
                    rf"line {fired} fired",
                    ha="right", va="center", fontsize=7.8,
                    color=ORANGE, style="italic")

    # ---------- arrow from program to trace ------------------------------
    ax.add_patch(FancyArrowPatch(
        (PROG_X1 + 0.04, 3.30), (TAB_X0 - 0.20, 3.30),
        arrowstyle="-|>", mutation_scale=12, lw=1.4, color=ORANGE,
    ))
    ax.text((PROG_X1 + TAB_X0) / 2, 3.50,
            "execute", ha="center", va="bottom",
            fontsize=8.0, style="italic", color=ORANGE)

    # ---------- bottom caption -------------------------------------------
    fig.text(0.5, 0.04,
             "Running time $= 4$ transitions   |   "
             "Space $= O(1)$ registers, no memory touched",
             ha="center", va="bottom", fontsize=9, style="italic", color=INK)

    save(fig, "ram-trace-doubling")


if __name__ == "__main__":
    main()

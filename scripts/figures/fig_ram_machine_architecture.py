"""Architecture of the Random Access Machine (§2.1): input/output tapes, fixed program with program counter, O(1) registers, unbounded memory, and the indirect-addressing step that gives the model its name."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from _style import GRAY, INK, LIGHT, ORANGE, apply_style, save

HI_FILL = to_rgba(ORANGE, 0.16)  # shaded register/cell pair (grayscale-safe: bold text too)

# ---------------------------------------------------------------- geometry --
TAPE_X0, TAPE_CW, TAPE_CH = 2.2, 0.78, 0.78
IN_TOP, OUT_TOP = 9.6, 1.4
PROG_X0, PROG_X1, PROG_Y0, PROG_Y1 = 0.9, 4.7, 4.6, 7.4
REG_X0, REG_W, REG_CH = 5.9, 1.65, 0.62
MEM_X0, MEM_W, MEM_TOP, MEM_CH, MEM_N = 10.0, 1.65, 7.6, 0.52, 8

PROGRAM = [
    "1: READ  R[0]",
    "2: JZERO R[0], 5",
    "3: ADD   R[1],R[1],R[0]",
    "4: JUMP  1",
    "5: HALT",
]
PC_LINE = 2  # program counter points at line 2 (READ already executed)
ADDR = 7     # address held in R[2]; selects M[7]

# R[2] aligned with M[ADDR] so the indirect-addressing arrow is horizontal
M_HOT_CY = MEM_TOP - (ADDR + 0.5) * MEM_CH
REG_TOP = M_HOT_CY + 2.5 * REG_CH  # R[2] is the third (bottom) register


def tape(ax, y_top, labels, shade_idx=None):
    """Row of square tape cells; returns list of cell centre x's."""
    centers = []
    for i, lab in enumerate(labels):
        x = TAPE_X0 + i * TAPE_CW
        fc = LIGHT if i == shade_idx else "white"
        ax.add_patch(Rectangle((x, y_top - TAPE_CH), TAPE_CW, TAPE_CH,
                               fc=fc, ec=INK, lw=0.9))
        if lab:
            ax.text(x + TAPE_CW / 2, y_top - TAPE_CH / 2, lab,
                    ha="center", va="center", fontsize=8.5, color=INK)
        centers.append(x + TAPE_CW / 2)
    return centers


def main():
    apply_style()
    fig, ax = plt.subplots(figsize=(6.0, 5.1))
    ax.set_xlim(-0.45, 11.9)
    ax.set_ylim(-0.15, 10.25)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------- input tape ----
    in_labels = ["$x_1$", "$x_2$", "$x_3$", "$x_4$", "$x_5$", r"$\cdots$", "$x_n$"]
    in_centers = tape(ax, IN_TOP, in_labels, shade_idx=1)  # head over x_2
    ax.text(TAPE_X0, IN_TOP + 0.12, "read-only input tape",
            fontsize=8, style="italic", color=INK, ha="left", va="bottom")

    head_x = in_centers[1]
    ax.annotate("", xy=(head_x, PROG_Y1 + 0.06), xytext=(head_x, IN_TOP - TAPE_CH - 0.04),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(head_x + 0.2, 8.32, "READ", family="monospace", fontsize=7.2,
            color=INK, ha="left", va="center")
    ax.text(head_x + 0.2, 8.0, "head advances right only",
            fontsize=7, style="italic", color=GRAY, ha="left", va="center")

    # ----------------------------------------------------- program box -----
    ax.add_patch(FancyBboxPatch((PROG_X0, PROG_Y0), PROG_X1 - PROG_X0, PROG_Y1 - PROG_Y0,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="white", ec=INK, lw=1.1))
    ax.text((PROG_X0 + PROG_X1) / 2, PROG_Y1 - 0.3, "program $P$  (fixed, finite)",
            fontsize=8, style="italic", color=INK, ha="center", va="center")
    line_ys = [6.72 - 0.44 * i for i in range(len(PROGRAM))]
    pc_y = line_ys[PC_LINE - 1]
    ax.add_patch(Rectangle((PROG_X0 + 0.12, pc_y - 0.17), PROG_X1 - PROG_X0 - 0.24, 0.34,
                           fc=LIGHT, ec="none"))
    for txt, y in zip(PROGRAM, line_ys):
        ax.text(PROG_X0 + 0.26, y, txt, family="monospace", fontsize=7.0,
                color=INK, ha="left", va="center")

    # program counter: bold arrow at the current line
    ax.annotate("", xy=(PROG_X0 - 0.06, pc_y), xytext=(0.06, pc_y),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0,
                                mutation_scale=14))
    ax.text(0.3, pc_y + 0.24, r"$\ell$", fontsize=10, color=INK,
            ha="center", va="bottom")
    ax.text(0.3, pc_y - 0.26, "program\ncounter", fontsize=6.6, color=GRAY,
            ha="center", va="top", linespacing=1.1)

    # -------------------------------------------------------- registers ----
    reg_cx = REG_X0 + REG_W / 2
    ax.text(reg_cx, REG_TOP + 0.14, "registers ($O(1)$ of them)",
            fontsize=7.5, style="italic", color=INK, ha="center", va="bottom")
    reg_vals = {0: ("$x_1$", False), 1: ("0", False), 2: (str(ADDR), True)}
    reg_cy = {}
    for i in range(3):
        y0 = REG_TOP - (i + 1) * REG_CH
        reg_cy[i] = y0 + REG_CH / 2
        val, hot = reg_vals.get(i, (None, False))
        ax.add_patch(Rectangle((REG_X0, y0), REG_W, REG_CH,
                               fc=HI_FILL if hot else "white", ec=INK, lw=0.9))
        ax.text(REG_X0 + 0.1, reg_cy[i], f"R[{i}]", family="monospace",
                fontsize=6.4, color=GRAY, ha="left", va="center")
        if val:
            ax.text(REG_X0 + REG_W * 0.66, reg_cy[i], val,
                    fontsize=8.5, color=INK, ha="center", va="center",
                    weight="bold" if hot else "normal",
                    family="monospace" if hot else None)

    # program <-> registers: instructions act on registers only
    arr_y = PROG_Y0 + 0.16
    ax.add_patch(FancyArrowPatch((PROG_X1 + 0.06, arr_y), (REG_X0 - 0.06, arr_y),
                                 arrowstyle="<|-|>", mutation_scale=9,
                                 lw=1.2, color=INK))
    ax.text(4.2, 4.3, "ADD, SUB, MUL, DIV,", family="monospace",
            fontsize=6.5, color=INK, ha="center", va="center")
    ax.text(4.2, 4.02, "MOVE, JZERO", family="monospace",
            fontsize=6.5, color=INK, ha="center", va="center")
    ax.text(4.2, 3.72, "operate on registers only",
            fontsize=7, style="italic", color=GRAY, ha="center", va="center")

    # ----------------------------------------------------------- memory ----
    mem_cx = MEM_X0 + MEM_W / 2
    ax.text(mem_cx, MEM_TOP + 0.14, "memory $M$", fontsize=8,
            style="italic", color=INK, ha="center", va="bottom")
    for k in range(MEM_N):
        y0 = MEM_TOP - (k + 1) * MEM_CH
        hot = k == ADDR
        ax.add_patch(Rectangle((MEM_X0, y0), MEM_W, MEM_CH,
                               fc=HI_FILL if hot else "white", ec=INK, lw=0.9))
        ax.text(mem_cx, y0 + MEM_CH / 2, f"M[{k}]", family="monospace",
                fontsize=6.8, color=ORANGE if hot else GRAY,
                weight="bold" if hot else "normal", ha="center", va="center")
    dots_y0 = MEM_TOP - (MEM_N + 1) * MEM_CH
    ax.add_patch(Rectangle((MEM_X0, dots_y0), MEM_W, MEM_CH,
                           fc="white", ec=INK, lw=0.9))
    ax.text(mem_cx, dots_y0 + MEM_CH / 2, r"$\vdots$", fontsize=8,
            color=INK, ha="center", va="center")
    ax.text(mem_cx, dots_y0 - 0.14, "(unbounded)", fontsize=7,
            style="italic", color=GRAY, ha="center", va="top")

    # ------------------------- the key arrow: indirect addressing ----------
    ax.add_patch(FancyArrowPatch((REG_X0 + REG_W + 0.05, M_HOT_CY),
                                 (MEM_X0 - 0.05, M_HOT_CY),
                                 arrowstyle="<|-|>", mutation_scale=12,
                                 lw=2.0, color=ORANGE))
    lx = REG_X0 + 0.1
    ax.text(lx, M_HOT_CY - 0.46, "LOAD / STORE", family="monospace",
            fontsize=7.5, weight="bold", color=ORANGE, ha="left", va="center")
    ax.text(lx, M_HOT_CY - 0.8, f"address ${ADDR}$ in R[2] selects $M[{ADDR}]$,",
            fontsize=7, color=INK, ha="left", va="center")
    ax.text(lx, M_HOT_CY - 1.12, "any cell in one step:", fontsize=7,
            color=INK, ha="left", va="center")
    ax.text(lx, M_HOT_CY - 1.44, "this arrow is the “random access”",
            fontsize=7, style="italic", color=INK, ha="left", va="center")

    # ------------------------------------------------------ output tape ----
    tape(ax, OUT_TOP, [""] * 7)
    ax.text(TAPE_X0, OUT_TOP - TAPE_CH - 0.14, "write-only output tape",
            fontsize=8, style="italic", color=INK, ha="left", va="top")
    wx = TAPE_X0 + TAPE_CW / 2
    ax.annotate("", xy=(wx, OUT_TOP + 0.04), xytext=(wx, PROG_Y0 - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(wx + 0.2, 3.0, "WRITE", family="monospace", fontsize=7.2,
            color=INK, ha="left", va="center")
    ax.text(wx + 0.2, 2.68, "results only", fontsize=7, style="italic",
            color=GRAY, ha="left", va="center")

    save(fig, "ram-machine-architecture")


if __name__ == "__main__":
    main()

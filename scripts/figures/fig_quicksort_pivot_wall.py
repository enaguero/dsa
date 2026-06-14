"""Pivot-wall argument from section 21.1: the first pivot drawn from
{z_i,...,z_j} either is a middle element and walls the pair into different
partitions forever, or is an endpoint and compares them — 2 of j-i+1 equally
likely outcomes, so Pr[z_i and z_j compared] = 2/(j-i+1)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyBboxPatch

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, apply_style, save

# ------------------------------------------------------------------- layout
# Seven slots on the shared number line: five drawn circles + two ellipses
# standing in for the elided elements of {z_i, ..., z_j}.
SLOT_X = np.linspace(1.0, 9.0, 7)
LABELS = [r"$z_i$", r"$z_{i+1}$", r"$\cdots$", r"$z_m$", r"$\cdots$",
          r"$z_{j-1}$", r"$z_j$"]
ELEM = [0, 1, 3, 5, 6]  # slots drawn as circles
DOTS = [2, 4]           # slots elided to an ellipsis
END = {0, 6}            # the endpoints z_i and z_j
MID = 3                 # z_m, the in-between pivot of case 1
MS = 15                 # circle marker size (points)

Y_ROW1, Y_ROW2 = 7.62, 2.95  # circle-row baselines of the two panels

apply_style()
fig = plt.figure(figsize=(6.0, 5.3))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10)
ax.set_ylim(-0.35, 10.35)
ax.axis("off")


def draw_row(y: float, pivot: int, mask_pivot_label: bool = False) -> None:
    """One row of elements; `pivot` is the slot drawn as the solid pivot.

    `mask_pivot_label` puts a white box behind the pivot's label so the
    wall line of case 1 does not strike through it.
    """
    for s in DOTS:
        ax.text(SLOT_X[s], y, r"$\cdots$", ha="center", va="center",
                fontsize=11, color=GRAY, zorder=4)
    for s in ELEM:
        if s == pivot:
            mfc, mec, mew = INK, INK, 1.6
        elif s in END:
            mfc, mec, mew = "white", INK, 1.6
        else:
            mfc, mec, mew = LIGHT, GRAY, 1.0
        ax.plot([SLOT_X[s]], [y], "o", ms=MS, mfc=mfc, mec=mec, mew=mew,
                zorder=4)
        lab_color = INK if (s in END or s == pivot) else GRAY
        bbox = (dict(boxstyle="round,pad=0.1", fc="white", ec="none")
                if (mask_pivot_label and s == pivot) else None)
        ax.text(SLOT_X[s], y - 0.62, LABELS[s], ha="center", va="center",
                fontsize=9.5, color=lab_color, zorder=5, bbox=bbox)


def panel_title(y: float, tag: str, title: str, prob: str, prob_color) -> None:
    ax.text(0.55, y, tag, ha="left", va="center", fontsize=8, color="white",
            zorder=5, bbox=dict(boxstyle="round,pad=0.32", fc=INK, ec="none"))
    ax.text(1.62, y, title, ha="left", va="center", fontsize=9.5, color=INK,
            zorder=5)
    ax.text(9.45, y, prob, ha="right", va="center", fontsize=10,
            color=prob_color, zorder=5)


def emphasized(y: float, plain: str, strong: str, color, x_split: float) -> None:
    """Centered-looking annotation whose tail phrase is bold and colored."""
    ax.text(x_split, y, plain, ha="right", va="center", fontsize=9,
            color=INK, zorder=5)
    ax.text(x_split, y, strong, ha="left", va="center", fontsize=9,
            color=color, fontweight="bold", zorder=5)


# ------------------------------------- case 1: a middle element drawn first
panel_title(9.8, "Case 1",
            r"first pivot drawn from $\{z_i,\ldots,z_j\}$ is a middle element",
            r"$\mathrm{Pr}=\frac{j-i-1}{j-i+1}$", GRAY)

# the two partitions the pivot z_m creates
for x0, x1, name in [(0.55, 4.12, r"left partition  $({<}\,z_m)$"),
                     (5.88, 9.45, r"right partition  $({>}\,z_m)$")]:
    ax.add_patch(FancyBboxPatch(
        (x0, 6.62), x1 - x0, 1.76,
        boxstyle="round,pad=0,rounding_size=0.22",
        fc="#f4f4f8", ec=GRAY, lw=0.8, zorder=1))
    ax.text((x0 + x1) / 2, 8.12, name, ha="center", va="center",
            fontsize=8, color=GRAY, zorder=2)

# the wall: the in-between pivot permanently separates z_i from z_j
ax.plot([SLOT_X[MID]] * 2, [6.22, 8.78], color=ORANGE, lw=1.6,
        ls=(0, (5, 3)), zorder=3)
ax.text(SLOT_X[MID], 9.0, "the wall", ha="center", va="center", fontsize=8.5,
        color=ORANGE, style="italic", zorder=5)

draw_row(Y_ROW1, pivot=MID, mask_pivot_label=True)
ax.text(SLOT_X[MID], 6.5, "pivot", ha="center", va="center", fontsize=8,
        color=ORANGE, style="italic", zorder=5,
        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

emphasized(5.85, r"$z_i$ and $z_j$ land in different partitions — ",
           "never compared", ORANGE, 6.45)

# ------------------------------------------ case 2: an endpoint drawn first
panel_title(5.25, "Case 2",
            r"first pivot drawn from $\{z_i,\ldots,z_j\}$ is $z_i$ or $z_j$",
            r"$\mathrm{Pr}=\frac{2}{j-i+1}$", NAVY)

# the pivot is compared with every element of the range
for s in ELEM[1:] + DOTS:
    d = SLOT_X[s] - SLOT_X[0]
    h = 0.32 + 0.155 * d  # apex height grows with span so the arcs nest
    big = s == 6
    ax.add_patch(Arc((SLOT_X[0] + d / 2, Y_ROW2), d, 2 * h,
                     theta1=0, theta2=180,
                     color=NAVY if big else GRAY,
                     lw=2.2 if big else 0.9,
                     ls="-" if s in ELEM else (0, (2, 2)),
                     zorder=2))
    if big:
        ax.text(SLOT_X[0] + d / 2, Y_ROW2 + h, "compared", ha="center",
                va="center", fontsize=8.5, color=NAVY, fontweight="bold",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

draw_row(Y_ROW2, pivot=0)
ax.text(SLOT_X[0], 1.93, "pivot", ha="center", va="center", fontsize=8,
        color=NAVY, style="italic", zorder=5)

emphasized(1.35, r"$z_i$ is compared with every element in the range — ",
           "including the other endpoint", NAVY, 6.55)

# ------------------------------------------------------------------- payoff
ax.text(5.0, 0.32,
        r"each of the $j-i+1$ elements is equally likely to be the first"
        r" pivot drawn  $\Rightarrow$  "
        r"$\mathrm{Pr}\left[\,z_i,\,z_j\ \mathrm{compared}\,\right]"
        r"=\frac{2}{j-i+1}$",
        ha="center", va="center", fontsize=9, color=INK, zorder=5,
        bbox=dict(boxstyle="round,pad=0.45", fc=LIGHT, ec=NAVY, lw=0.9))

save(fig, "quicksort-pivot-wall")

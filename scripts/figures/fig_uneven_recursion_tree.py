"""Recursion tree for T(n) = T(n/3) + T(2n/3) + n (section 18.1): uneven splits
make the tree lopsided, but every full level still sums to n, giving
Theta(n log n) — the Akra-Bazzi p = 1 picture the Master Theorem cannot draw."""

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt

from _style import GRAY, INK, LIGHT, NAVY, apply_style, save

# ---------------------------------------------------------------- recurrence
# T(n) = T(n/3) + T(2n/3) + n: a node reached by L lefts and R rights has
# size (1/3)^L (2/3)^R n.  Compute every shown subproblem size from the
# recurrence and verify the key fact: each full level sums to exactly n.
SPLITS = {"L": Fraction(1, 3), "R": Fraction(2, 3)}

size = {}  # path string ("" = root) -> fraction of n
for depth in range(4):
    for bits in product("LR", repeat=depth):
        path = "".join(bits)
        frac = Fraction(1)
        for b in path:
            frac *= SPLITS[b]
        size[path] = frac

for depth in range(4):
    level_sum = sum(f for p, f in size.items() if len(p) == depth)
    assert level_sum == 1, f"level {depth} must sum to n, got {level_sum}"


def node_label(frac: Fraction) -> str:
    if frac == 1:
        return "$n$"
    num = "" if frac.numerator == 1 else str(frac.numerator)
    return f"${num}n/{frac.denominator}$"


# ------------------------------------------------------------------- layout
YS = [0.92, 0.755, 0.59, 0.425]  # y of levels 0..3
Y_LEAF_L, Y_LEAF_R = 0.315, 0.165  # left edge bottoms out sooner

X = {  # hand-tuned x for each drawn node (lopsided toward the 2n/3 side)
    "": 0.40,
    "L": 0.22, "R": 0.58,
    "LL": 0.115, "LR": 0.30, "RL": 0.49, "RR": 0.70,
    "LLL": 0.065, "RRR": 0.775,
}
SOLID_EDGES = [
    ("", "L"), ("", "R"),
    ("L", "LL"), ("L", "LR"), ("R", "RL"), ("R", "RR"),
    ("LL", "LLL"), ("RR", "RRR"),
]
# children omitted in favor of the ellipsis get short dotted stubs
STUBS = [("LL", +1), ("LR", -1), ("LR", +1), ("RL", -1), ("RL", +1), ("RR", -1)]

apply_style()
fig = plt.figure(figsize=(5.85, 4.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# dotted leaders from each level toward the per-level sums on the right
for y in [*YS, Y_LEAF_R]:
    ax.plot([0.46, 0.872], [y, y], ls=(0, (1, 3)), lw=0.7, color=GRAY, zorder=1)

# edges, then dotted stubs toward the elided level-3 nodes
for parent, child in SOLID_EDGES:
    ax.plot([X[parent], X[child]], [YS[len(parent)], YS[len(child)]],
            color=INK, lw=0.9, zorder=2)
for parent, sign in STUBS:
    ax.plot([X[parent], X[parent] + 0.038 * sign], [YS[2], YS[2] - 0.10],
            color=GRAY, lw=0.9, ls=(0, (2, 2)), zorder=2)
ax.text(0.40, YS[3], r"$\cdots$", ha="center", va="center", fontsize=13,
        color=GRAY, zorder=3,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

# nodes
for path, x in X.items():
    ax.text(x, YS[len(path)], node_label(size[path]), ha="center", va="center",
            fontsize=9.5, color=INK, zorder=5,
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=INK, lw=0.8))

# the two extreme root-to-leaf paths continue down to size-1 leaves;
# the left edge (divide by 3) terminates visibly sooner than the right.
for x, y_leaf, lx, ha in [(X["LLL"], Y_LEAF_L, 0.095, "left"),
                          (X["RRR"], Y_LEAF_R, 0.748, "right")]:
    ax.plot([x, x], [YS[3] - 0.025, y_leaf + 0.015],
            color=INK, lw=0.9, ls=(0, (1, 2.5)), zorder=2)
    ax.plot([x], [y_leaf], marker="s", ms=4.5, color=INK, zorder=5)
    ax.text(lx, y_leaf, "size 1", ha=ha, va="center", fontsize=8,
            color=GRAY, style="italic", zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

ax.text(0.145, Y_LEAF_L - 0.052, r"shortest path: $\log_3 n$ levels",
        ha="center", va="center", fontsize=8.5, color=INK)
ax.text(X["RRR"], Y_LEAF_R - 0.052, r"longest path: $\log_{3/2} n$ levels",
        ha="center", va="center", fontsize=8.5, color=INK)

# ----------------------------------------------- per-level sums (the insight)
ax.text(0.945, YS[0] + 0.062, "level sum", ha="right", va="center",
        fontsize=8, color=GRAY)
sums = [(YS[0], r"$\boldsymbol{n}$"), (YS[1], r"$\boldsymbol{n}$"),
        (YS[2], r"$\boldsymbol{n}$"), (YS[3], r"$\leq n$"), (Y_LEAF_R, r"$\leq n$")]
for y, s in sums:
    bold = "boldsymbol" in s
    ax.text(0.945, y, s, ha="right", va="center", fontsize=10.5 if bold else 9.5,
            color=NAVY if bold else GRAY, zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

# square bracket spanning the three full levels, labelled vertically
bx, tick = 0.964, 0.008
ax.plot([bx, bx], [YS[2], YS[0]], color=NAVY, lw=1.0)
ax.plot([bx - tick, bx], [YS[0], YS[0]], color=NAVY, lw=1.0)
ax.plot([bx - tick, bx], [YS[2], YS[2]], color=NAVY, lw=1.0)
ax.text(0.987, (YS[0] + YS[2]) / 2, "each full level sums to $n$",
        ha="center", va="center", fontsize=8.5, color=NAVY, rotation=90)

# ------------------------------------------------------------ title + payoff
ax.text(0.42, 1.005, r"$T(n) = T(n/3) + T(2n/3) + n$", ha="center",
        va="center", fontsize=11.5, color=INK)
ax.text(0.42, 0.965, "unequal subproblems — the Master Theorem does not apply",
        ha="center", va="center", fontsize=8, color=GRAY)
ax.text(0.5, 0.045,
        r"$\Theta(n)$ per level $\times\ \Theta(\log n)$ levels"
        r"$\;=\;\Theta(n \log n)$    (Akra–Bazzi: $p = 1$)",
        ha="center", va="center", fontsize=9.5, color=INK, zorder=5,
        bbox=dict(boxstyle="round,pad=0.45", fc=LIGHT, ec=NAVY, lw=0.9))

save(fig, "uneven-recursion-tree")

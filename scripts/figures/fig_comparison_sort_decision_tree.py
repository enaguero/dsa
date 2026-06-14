"""Decision tree for comparison-sorting [a, b, c] (n = 3), illustrating the
information-theoretic lower bound of section 24.1: 3! = 6 leaves force height
ceil(log2 6) = 3."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch

from _style import GRAY, INK, LIGHT, apply_style, save


class _Branch(Exception):
    """Raised when insertion sort hits a comparison undecided by the path."""

    def __init__(self, pair):
        self.pair = pair


def _trace(path):
    """Run insertion sort on [a, b, c], replaying the comparison outcomes in
    `path` (a tuple of ((x, y), bool) meaning "x < y is bool"). Returns either
    ('leaf', sorted_order) or ('cmp', (x, y)) for the next undecided question.
    """
    decided = dict(path)

    def less(x, y):
        if (x, y) in decided:
            return decided[(x, y)]
        if (y, x) in decided:
            return not decided[(y, x)]
        raise _Branch((x, y))

    arr = ["a", "b", "c"]
    try:
        for i in range(1, len(arr)):
            j = i
            while j > 0 and less(arr[j], arr[j - 1]):
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
    except _Branch as exc:
        return ("cmp", exc.pair)
    return ("leaf", tuple(arr))


def build(path=()):
    """Build the decision tree as nested dicts. Questions are canonicalized to
    alphabetical order ("a < b?"), with the yes-branch meaning the question is
    true."""
    kind, payload = _trace(path)
    if kind == "leaf":
        return {"leaf": payload, "depth": len(path)}
    x, y = payload
    lo, hi = sorted(payload)
    raw_when_yes = (x, y) == (lo, hi)  # raw outcome if "lo < hi?" answers yes
    return {
        "cmp": (lo, hi),
        "depth": len(path),
        "yes": build(path + (((x, y), raw_when_yes),)),
        "no": build(path + (((x, y), not raw_when_yes),)),
    }


def layout(node, next_slot=[0], spacing=2.0):
    """Tidy layout: leaves get consecutive slots left-to-right; an internal
    node sits at the midpoint of its children. Sets node['x'], node['y']."""
    node["y"] = -node["depth"]
    if "leaf" in node:
        node["x"] = next_slot[0] * spacing
        next_slot[0] += 1
    else:
        layout(node["yes"], next_slot, spacing)
        layout(node["no"], next_slot, spacing)
        node["x"] = (node["yes"]["x"] + node["no"]["x"]) / 2


def draw(ax, node):
    if "cmp" in node:
        for branch, label in (("yes", "yes"), ("no", "no")):
            child = node[branch]
            ax.plot(
                [node["x"], child["x"]],
                [node["y"], child["y"]],
                color=INK,
                lw=0.9,
                zorder=1,
            )
            mx = (node["x"] + child["x"]) / 2
            my = (node["y"] + child["y"]) / 2
            left = child["x"] < node["x"]
            ax.text(
                mx + (-0.14 if left else 0.14),
                my,
                label,
                ha="right" if left else "left",
                va="center",
                fontsize=7.8,
                style="italic",
                color=GRAY,
                zorder=2,
            )
            draw(ax, child)
        lo, hi = node["cmp"]
        ax.add_patch(
            Ellipse(
                (node["x"], node["y"]),
                width=1.55,
                height=0.62,
                facecolor="white",
                edgecolor=INK,
                lw=0.9,
                zorder=3,
            )
        )
        ax.text(
            node["x"],
            node["y"],
            f"${lo} < {hi}$?",
            ha="center",
            va="center",
            fontsize=9,
            color=INK,
            zorder=4,
        )
    else:
        w, h = 1.66, 0.56
        ax.add_patch(
            FancyBboxPatch(
                (node["x"] - w / 2, node["y"] - h / 2),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                facecolor=LIGHT,
                edgecolor=INK,
                lw=0.9,
                zorder=3,
            )
        )
        a, b, c = node["leaf"]
        ax.text(
            node["x"],
            node["y"],
            f"$[{a},{b},{c}]$",
            ha="center",
            va="center",
            fontsize=9,
            color=INK,
            zorder=4,
        )


def main():
    apply_style()
    tree = build()
    layout(tree)

    fig, ax = plt.subplots(figsize=(6.0, 3.45))
    ax.set_axis_off()

    x_left, x_right = -0.95, 10.95
    max_depth = 3

    # Depth ruler: dashed gridlines with labels in the left margin.
    for d in range(max_depth + 1):
        ax.plot(
            [x_left, x_right],
            [-d, -d],
            ls=(0, (4, 3)),
            lw=0.7,
            color=GRAY,
            alpha=0.55,
            zorder=0,
        )
        ax.text(
            x_left - 0.25,
            -d,
            f"depth {d}",
            ha="right",
            va="center",
            fontsize=8,
            color=GRAY,
        )

    draw(ax, tree)

    # Height arrow in the right margin, spanning depth 0 to depth 3.
    ax_x = x_right + 0.55
    ax.annotate(
        "",
        xy=(ax_x, -max_depth),
        xytext=(ax_x, 0),
        arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9, shrinkA=0, shrinkB=0),
    )
    ax.text(
        ax_x + 0.75,
        -max_depth / 2,
        "worst case $=$ height\n$= \\lceil \\log_2 3! \\rceil = 3$",
        rotation=90,
        ha="center",
        va="center",
        fontsize=8.2,
        color=INK,
    )

    # The punchline.
    ax.text(
        (x_left + x_right) / 2,
        -max_depth - 0.95,
        "$6$ leaves $= 3!$ permutations $\\;\\Rightarrow\\;$ "
        "height $\\geq \\lceil \\log_2 6 \\rceil = 3$ comparisons",
        ha="center",
        va="center",
        fontsize=9.5,
        color=INK,
        bbox=dict(
            boxstyle="round,pad=0.45", facecolor="white", edgecolor=GRAY, lw=0.8
        ),
    )

    ax.set_xlim(x_left - 1.7, ax_x + 1.45)
    ax.set_ylim(-max_depth - 1.55, 0.55)
    save(fig, "comparison-sort-decision-tree")


if __name__ == "__main__":
    main()

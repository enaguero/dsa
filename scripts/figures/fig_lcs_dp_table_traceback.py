"""Filled LCS DP table with predecessor arrows and traceback path (§26.2): time = #subproblems x work each."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from _style import GRAY, INK, NAVY, apply_style, save

X = "ABCBDAB"  # rows,    i = 1..n
Y = "BDCABA"   # columns, j = 1..m
N, M = len(X), len(Y)

SHADE_BOUNDARY = "0.93"
SHADE_PATH = "0.80"
GLYPH = {"d": r"$\nwarrow$", "u": r"$\uparrow$", "l": r"$\leftarrow$"}


def compute_table():
    """Fill the LCS table and the predecessor move for every interior cell."""
    val = [[0] * (M + 1) for _ in range(N + 1)]
    mov = [[None] * (M + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if X[i - 1] == Y[j - 1]:
                val[i][j] = val[i - 1][j - 1] + 1
                mov[i][j] = "d"
            elif val[i - 1][j] >= val[i][j - 1]:
                val[i][j] = val[i - 1][j]
                mov[i][j] = "u"
            else:
                val[i][j] = val[i][j - 1]
                mov[i][j] = "l"
    return val, mov


def traceback(mov):
    """Walk the stored moves from (n, m) back to the boundary."""
    path, matches = [], []
    i, j = N, M
    while i > 0 and j > 0:
        path.append((i, j))
        if mov[i][j] == "d":
            matches.append((i, j))
            i, j = i - 1, j - 1
        elif mov[i][j] == "u":
            i -= 1
        else:
            j -= 1
    return set(path), matches


def main() -> None:
    apply_style()
    val, mov = compute_table()
    path, matches = traceback(mov)
    lcs = "".join(X[i - 1] for i, _ in reversed(matches))
    assert lcs == "BCBA" and val[N][M] == 4

    fig, ax = plt.subplots(figsize=(6.0, 5.45))
    ax.set_aspect("equal")
    ax.axis("off")

    # --- cells: shading, value, predecessor glyph -------------------------
    for i in range(N + 1):
        for j in range(M + 1):
            face = "white"
            if (i, j) in path:
                face = SHADE_PATH
            elif i == 0 or j == 0:
                face = SHADE_BOUNDARY
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=face,
                                       edgecolor="0.62", linewidth=0.6))
            on_path = (i, j) in path
            ax.text(j + 0.56, i + 0.58, str(val[i][j]), ha="center",
                    va="center", fontsize=11, color=INK,
                    fontweight="bold" if on_path else "normal")
            if mov[i][j] is not None:
                ax.text(j + 0.17, i + 0.22, GLYPH[mov[i][j]], ha="center",
                        va="center", fontsize=8 if on_path else 6.5,
                        color=INK if on_path else GRAY)

    # circles around the diagonal (match) cells of the path; read bottom-up
    # they spell the LCS itself
    for i, j in matches:
        ax.add_patch(plt.Circle((j + 0.56, i + 0.58), 0.30, fill=False,
                                edgecolor=INK, linewidth=1.5))
        ax.text(j + 0.91, i + 0.90, X[i - 1], ha="center", va="center",
                fontsize=7, color=INK, fontweight="bold")

    # outer frame
    ax.add_patch(plt.Rectangle((0, 0), M + 1, N + 1, fill=False,
                               edgecolor=INK, linewidth=1.1))

    # --- headers ----------------------------------------------------------
    for j in range(M + 1):
        ax.text(j + 0.5, -1.18, f"$j={j}$", ha="center", va="center",
                fontsize=7, color=GRAY)
        if j >= 1:
            ax.text(j + 0.5, -0.45, Y[j - 1], ha="center", va="center",
                    fontsize=10.5, color=INK, fontweight="bold")
    for i in range(N + 1):
        ax.text(-1.25, i + 0.5, f"$i={i}$", ha="center", va="center",
                fontsize=7, color=GRAY)
        if i >= 1:
            ax.text(-0.45, i + 0.5, X[i - 1], ha="center", va="center",
                    fontsize=10.5, color=INK, fontweight="bold")
    ax.text(-0.45, -0.45, "$Y\\!:$", ha="center", va="center",
            fontsize=9, color=GRAY)
    ax.text(-1.25, -0.45, "$X\\!:$", ha="center", va="center",
            fontsize=9, color=GRAY)

    # --- Theta(1)-per-cell annotation: one cell + its three inputs -------
    ti, tj = 3, 6  # off-path interior cell whose inputs are also off-path
    assert all((i, j) not in path
               for i, j in [(ti, tj), (ti - 1, tj - 1), (ti - 1, tj), (ti, tj - 1)])
    ax.add_patch(plt.Rectangle((tj, ti), 1, 1, fill=False,
                               edgecolor=NAVY, linewidth=1.6, zorder=4))
    for ni, nj in [(ti - 1, tj - 1), (ti - 1, tj), (ti, tj - 1)]:
        ax.add_patch(plt.Rectangle((nj + 0.05, ni + 0.05), 0.9, 0.9,
                                   fill=False, edgecolor=NAVY, linewidth=1.0,
                                   linestyle=(0, (2, 2)), zorder=4))
    ax.annotate(
        "filling one cell: one compare\n+ one max, reads $\\leq 3$ filled\n"
        "neighbors (dashed)\n$\\Rightarrow\\ \\Theta(1)$ per cell",
        xy=(tj + 1.02, ti + 0.5), xytext=(7.9, 2.6),
        ha="left", va="center", fontsize=8, color=NAVY,
        arrowprops=dict(arrowstyle="-|>", color=NAVY, linewidth=0.9,
                        shrinkA=2, shrinkB=2),
    )

    # --- traceback note ---------------------------------------------------
    ax.annotate(
        "traceback follows the stored\narrows back from $L[7][6]=4$;\n"
        "circled matches, read bottom-\nup, spell the LCS: B C B A.\n"
        "It needs the full table kept:\n$\\Theta(nm)$ space to reconstruct.",
        xy=(M + 1.02, N + 0.5), xytext=(7.9, 6.55),
        ha="left", va="center", fontsize=8, color=INK,
        arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=0.9,
                        shrinkA=2, shrinkB=2),
    )

    # --- bracket under the grid: cell count = total time ------------------
    yb = N + 1.42
    ax.plot([0, 0, M + 1, M + 1], [yb - 0.16, yb, yb, yb - 0.16],
            color=INK, linewidth=0.9)
    ax.text((M + 1) / 2, yb + 0.42,
            "$(n{+}1)(m{+}1) = 8 \\times 7 = 56$ cells, $\\Theta(1)$ each"
            " $\\;\\Rightarrow\\; \\Theta(nm)$ total time",
            ha="center", va="center", fontsize=8.5, color=INK)

    ax.set_xlim(-1.75, 12.55)
    ax.set_ylim(yb + 0.95, -1.75)

    save(fig, "lcs-dp-table-traceback")


if __name__ == "__main__":
    main()

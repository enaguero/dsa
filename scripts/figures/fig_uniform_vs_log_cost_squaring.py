"""Repeated squaring under uniform vs logarithmic cost: the bit length of R[0]
doubles per MUL while the uniform criterion charges one step (ram_model.md, section 4.2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, TEAL, apply_style, save

W = 64  # word size in bits; R[0] starts holding a full 64-bit value
K_MAX = 10  # number of MUL R[0],R[0],R[0] instructions executed

# Simulate the program: each MUL squares R[0]. Under the logarithmic
# criterion the instruction costs ceil(log2(operand + 1)) = bit length
# of the operand (section 4.2); under the uniform criterion it costs 1.
v = 2**W - 1
bits = [v.bit_length()]  # bits needed to store R[0] after k MULs
log_cum = [0]  # cumulative logarithmic cost after k MULs
for _ in range(K_MAX):
    log_cum.append(log_cum[-1] + v.bit_length())
    v *= v
    bits.append(v.bit_length())
uniform_cum = list(range(K_MAX + 1))  # cumulative uniform cost = k
ks = list(range(K_MAX + 1))

apply_style()
fig, ax = plt.subplots(figsize=(6.0, 3.9))
ax.set_yscale("log", base=2)

# Shade the gap between what uniform cost charges and the work performed.
ax.fill_between(ks[1:], uniform_cum[1:], log_cum[1:], color=LIGHT, alpha=0.6, lw=0, zorder=1)

# One machine word, for scale.
ax.axhline(W, color=GRAY, lw=0.8, zorder=2)
ax.text(0.05, 50, f"$w = {W}$ bits (one machine word)", color=GRAY, fontsize=8, va="top")

# Series 1: bits needed to store R[0] (solid, circles at even k).
ax.plot(ks, bits, color=NAVY, ls="-", marker="o", ms=3.8, markevery=2, zorder=4)
# Series 3: cumulative logarithmic cost (dotted, open triangles at odd k).
ax.plot(ks[1:], log_cum[1:], color=ORANGE, ls=(0, (1, 1.4)), lw=1.8,
        marker="^", mfc="white", ms=4.8, markevery=2, zorder=5)
# Series 2: cumulative uniform cost (dashed, open squares).
ax.plot(ks[1:], uniform_cum[1:], color=TEAL, ls="--", marker="s",
        mfc="white", ms=3.6, zorder=4)

# Direct series labels (no legend box).
ax.annotate("bits stored in $R[0]$:  $64 \\cdot 2^k$",
            xy=(2.15, 64 * 2**2.15), xytext=(0.55, 1100), color=NAVY, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.7, shrinkB=3))
ax.annotate("cumulative logarithmic cost:  $64\\,(2^k - 1)$",
            xy=(3, log_cum[3]), xytext=(5.0, 800), color=ORANGE, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7, shrinkB=5))
ax.text(9.85, 16.5, "cumulative uniform cost $= k$:  10 steps charged",
        color=TEAL, fontsize=8.5, ha="right", va="bottom")

# The two endpoints of the story.
ax.annotate("after 10 “unit-cost” MULs:\n$65{,}536$ bits $= 1{,}024$ words",
            xy=(10, bits[-1]), xytext=(5.2, 42000), fontsize=8.5, color=INK,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, shrinkA=4, shrinkB=4))
ax.text(6.6, 165, "work performed but never charged —\nthe gap the logarithmic criterion closes",
        fontsize=8, color=INK, ha="center", va="center", style="italic")

ax.set_xlim(-0.35, 10.55)
ax.set_ylim(0.7, 1.7e5)
ax.set_xticks(ks)
yticks = [4**i for i in range(9)]
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t:,}" for t in yticks])
ax.yaxis.set_minor_locator(NullLocator())
ax.set_xlabel("$k$ — number of MUL instructions executed")
ax.set_ylabel("count (log scale)")
ax.grid(axis="y", zorder=0)
ax.set_title("One MUL can double the bit length: uniform vs. logarithmic cost", pad=22)
ax.text(0.5, 1.025, "start with a full 64-bit value in $R[0]$; repeat "
        "$\\mathtt{MUL\\ R[0],R[0],R[0]}$ — each squaring doubles the bit length",
        transform=ax.transAxes, ha="center", fontsize=8, color=GRAY, style="italic")

save(fig, "uniform-vs-log-cost-squaring")

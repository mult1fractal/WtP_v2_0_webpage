#!/usr/bin/env python3
"""Generate the What the Phage v2.0 pipeline flow chart (PNG), vertical layout.

Matches the website design system: pink accent #ff1d6c, slate text #1e293b,
light surface, dark report sink.

Flow: FASTA input -> Input validation -> (bus) -> 7 parallel modules ->
      Interactive report.  Run:  python3 tools/make_flowchart.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ------------------------------------------------------------------ palette
PINK      = "#ff1d6c"
PINK_DIM  = "#ff8fb5"
PINK_SOFT = "#fff0f5"
TEXT      = "#1e293b"
MUTED     = "#64748b"
BORDER    = "#e2e8f0"
SURFACE   = "#ffffff"
DARK      = "#0b1220"
DARK_SOFT = "#cbd5e1"

# ------------------------------------------------------------------ modules
MODULES = [
    ("Identification", "16 tools\nviral scores", False),
    ("Quality control", "CheckV\ncompleteness", False),
    ("Annotation", "Prodigal · Pharokka\nGeNomad · PhaBox2", True),
    ("Taxonomy", "Sourmash · GeNomad\nPhaGCN · taxmyphage", True),
    ("Prophage", "GeNomad · PhaBox2\nVirSorter2 · Phigaro", True),
    ("Host prediction", "iPHoP · CHERRY", True),
    ("Lifecycle", "BACPHLIP · PhaTYP\nconsensus", True),
]

W, H = 10.5, 9.0
fig, ax = plt.subplots(figsize=(W, H), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# vertical axis positions
INPUT_Y    = 88.0
VALID_Y    = 74.0
BUS_Y      = 62.0
MOD_TOP    = 54.0
MOD_BOT    = 34.0
REP_TOP    = 26.0
REP_Y      = 16.0

# 7 module boxes across width
N = len(MODULES)
MOD_W = 11.0
span = 84.0                      # from x=8 to x=92
step = span / N
CX = [8.0 + MOD_W / 2 + i * step for i in range(N)]


def node(cx, cy, w, h, title, sub, fill=SURFACE, edge=BORDER, tcol=TEXT,
         scol=MUTED, radius=2.4, lw=1.6, tsize=10.5, ssize=7.2):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0.2,rounding_size={radius}",
        fc=fill, ec=edge, lw=lw, zorder=2,
    ))
    ax.text(cx, cy + 1.6, title, ha="center", va="center",
            fontsize=tsize, fontweight="bold", color=tcol, zorder=3)
    ax.text(cx, cy - 2.4, sub, ha="center", va="center",
            fontsize=ssize, color=scol, linespacing=1.35, zorder=3)


def v_arrow(y0, y1, x=50.0, lw=2.6, color=PINK):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>",
                                 mutation_scale=16, lw=lw, color=color, zorder=1))


# ------------------------------------------------------------ title
ax.text(50.0, 97.5, "What the Phage v2.0", ha="center", va="center",
        fontsize=17, fontweight="bold", color=TEXT, zorder=3)
ax.text(50.0, 93.0, "one command  ·  end_to_end  ·  every module optional",
        ha="center", va="center", fontsize=9, color=MUTED, zorder=3)

# ------------------------------------------------------------ FASTA input
node(50, INPUT_Y, 36, 9.5, "FASTA input", ".fa / .fasta / .fna / .gz",
     fill=PINK_SOFT, edge=PINK, tcol=PINK, scol=PINK, lw=2.0, tsize=11.5)
v_arrow(INPUT_Y - 4.75 - 1.0, VALID_Y + 4.75 + 1.0)

# ------------------------------------------------------------ validation
node(50, VALID_Y, 46, 9.5, "Input validation",
     "header sanitizing + length filter (1500 bp)", tsize=11.5)
v_arrow(VALID_Y - 4.75 - 1.0, BUS_Y)

# ------------------------------------------------------------ bus
ax.plot([8, 92], [BUS_Y, BUS_Y], color=PINK_DIM, lw=2.2, zorder=1)
for cx in CX:
    ax.plot([cx, cx], [BUS_Y, MOD_TOP + 0.4], color=PINK_DIM, lw=1.6,
            zorder=1)
ax.text(50.0, BUS_Y + 2.6, "distributed to all modules in parallel",
        ha="center", va="center", fontsize=7.6, color=MUTED, zorder=3,
        style="italic")

# ------------------------------------------------------------ modules
for i, (t, s, new) in enumerate(MODULES):
    cy = (MOD_TOP + MOD_BOT) / 2
    node(CX[i], cy, MOD_W, MOD_BOT - MOD_TOP, t, s,
         tsize=8.1, ssize=6.2)
    if new:
        ax.text(CX[i], MOD_TOP - 2.0, "new", ha="center", va="center",
                fontsize=6.0, fontweight="bold", color="#ffffff",
                bbox=dict(boxstyle="round,pad=0.18", fc=PINK, ec="none"),
                zorder=4)

# ------------------------------------------------------------ converge
v_arrow(MOD_BOT - 0.4 - 1.0, REP_TOP + 0.6, x=50.0)

# ------------------------------------------------------------ report
ax.add_patch(FancyBboxPatch(
    (8.0, REP_Y - 9.5), 84.0, 19.0,
    boxstyle="round,pad=0.3,rounding_size=3.2",
    fc=DARK, ec="#24304a", lw=1.8, zorder=2,
))
ax.text(50.0, REP_Y + 3.2, "Interactive report", ha="center", va="center",
        fontsize=13.5, fontweight="bold", color="#ffffff", zorder=3)
ax.text(50.0, REP_Y - 2.6, "tabs · genome viewer · per-sample JSON",
        ha="center", va="center", fontsize=8.6, color=DARK_SOFT, zorder=3)

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
out = "assets/img/wtp-pipeline-flowchart.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURFACE)
print("wrote", out)
#!/usr/bin/env python3
"""
generate_hero.py — Genera nortiqa-hero.svg
TECHSPEC-NL-README-001 v1.0
Agente-A: Edson Albea Dobernack — territorial, operativo, contacto (warm/crimson)
Agente-B: Gio — estratega, laboratorio, sistema (cool/steel)
"""
from pathlib import Path

# ── Canvas ─────────────────────────────────────────────────────────────────────
W, H = 640, 460
CELL = 7

# ── Paleta §9 ──────────────────────────────────────────────────────────────────
BG         = "#0d121d"
BORDER     = "#222b3c"
METAL_D    = "#192030"
METAL_F    = "#3a475d"
METAL_L    = "#586c88"

WARM_OUT   = "#7e1622"
WARM_MID   = "#cf3127"
WARM_HOT   = "#ff6a39"
WARM_CORE  = "#ffe6b8"

COOL_OUT   = "#14324f"
COOL_MID   = "#1f6aa8"
COOL_HOT   = "#3fa9ff"
COOL_CORE  = "#cfeaff"

TEXT_DIM   = "#9aa6b8"
TEXT_MID   = "#cfd8e8"
TEXT_BRT   = "#e8edf5"

# Color map: int → hex  (0=transparent, 1=metal-dark, 2=metal-frame, 3=metal-light,
#                        4=eye-outer, 5=eye-mid, 6=eye-hot, 7=eye-core, 8=glyph/mid)
def palette(warm: bool) -> dict:
    e_out  = WARM_OUT  if warm else COOL_OUT
    e_mid  = WARM_MID  if warm else COOL_MID
    e_hot  = WARM_HOT  if warm else COOL_HOT
    e_core = WARM_CORE if warm else COOL_CORE
    return {1: METAL_D, 2: METAL_F, 3: METAL_L,
            4: e_out, 5: e_mid, 6: e_hot, 7: e_core, 8: e_mid}

# ── Figuras pixel-art (24 × 28) ────────────────────────────────────────────────
# Convención: figura mira a la DERECHA (hacia el centro para Agente-A).
# Agente-B se flippea horizontalmente.
# Glifo A (Edson, territorial): dos columnas + barra = contacto, vínculo.
# Glifo B (Gio, sistema): cuadrícula hexagonal = estructura, laboratorio.

WARRIOR_A = [
 #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 helm-top
 [0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
 [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 2 helm-wide
 [0, 0, 1, 1, 2, 2, 1, 4, 5, 6, 7, 6, 5, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 3 ojos
 [0, 0, 1, 1, 2, 2, 1, 4, 5, 6, 7, 6, 5, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 4 ojos
 [0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 5 visor
 [0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 6 mentón
 [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 7 cuello
 [0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0],  # 8 hombros
 [0, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 3, 3, 0, 0],  # 9 pauldrons + brazo extendido inicio
 [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 2, 0],  # 10 pecho-sup + brazo
 [0, 1, 1, 1, 1, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 1, 1, 1, 1, 2, 3, 3, 3, 0],  # 11 glifo A fila1 + brazo
 [0, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 2, 3, 3, 3, 0],  # 12 glifo A barra + brazo
 [0, 1, 1, 1, 1, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 1, 1, 1, 1, 2, 3, 2, 0, 0],  # 13 glifo A fila3 + brazo
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 14 torso-bajo
 [0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 15 cinturón
 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 16 cadera
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 17 muslos
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
 [0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # 20 rodilla
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 21 espinilla
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 22
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 23
 [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 24 pies
 [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 25
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # 26
 [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # 27 base
]

WARRIOR_B = [
 #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
 [0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
 [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
 [0, 0, 1, 1, 2, 2, 4, 4, 5, 6, 7, 6, 5, 4, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 3 ojos hex
 [0, 0, 1, 1, 2, 2, 4, 5, 6, 7, 7, 7, 6, 5, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 4 ojos hex
 [0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 5
 [0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 6
 [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
 [0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0],  # 8
 [0, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 3, 3, 0, 0],  # 9
 [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 2, 0],  # 10
 [0, 1, 1, 1, 1, 8, 8, 1, 8, 1, 8, 1, 8, 1, 8, 8, 1, 1, 1, 2, 3, 3, 3, 0],  # 11 glifo B
 [0, 1, 1, 1, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 1, 1, 2, 3, 3, 3, 0],  # 12 glifo B cuadrícula
 [0, 1, 1, 1, 1, 8, 8, 1, 8, 1, 8, 1, 8, 1, 8, 8, 1, 1, 1, 2, 3, 2, 0, 0],  # 13 glifo B
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 14
 [0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # 15
 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 16
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
 [0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # 20
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 21
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 22
 [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 23
 [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 24
 [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 25
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # 26
 [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # 27
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def r(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" shape-rendering="crispEdges"{extra}/>'

def t(x, y, text, anchor="middle", size=9, fill=TEXT_DIM, spacing="0", weight="normal"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="monospace" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{spacing}">'
            f'{_esc(text)}</text>')

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(grid, pal, ox, oy, flip=False):
    cols = len(grid[0])
    out = []
    for ri, row in enumerate(grid):
        for ci, v in enumerate(row):
            if v == 0:
                continue
            dc = (cols - 1 - ci) if flip else ci
            out.append(r(ox + dc * CELL, oy + ri * CELL, CELL, CELL, pal.get(v, "#ff00ff")))
    return out

def cordillera(base_y, cx):
    peaks = [(cx, 9), (cx - 110, 6), (cx + 110, 6), (cx - 190, 4), (cx + 190, 4)]
    out = []
    for px, ph in peaks:
        for row in range(ph):
            frac = row / ph
            half = max(1, int((ph - row) * 1.4))
            x = px - half * CELL // 2
            w = half * CELL
            shade = METAL_F if row < 2 else METAL_D
            out.append(r(x, base_y - (ph - row) * CELL, w, CELL, shade))
    return out

def clash(cx, cy):
    out = []
    # expanding rings (outer → inner for correct z-order)
    rings = [(6, WARM_OUT), (5, COOL_OUT), (4, WARM_MID), (3, COOL_MID),
             (2, WARM_HOT), (1, COOL_HOT), (0, WARM_CORE)]
    for rad, col in rings:
        s = (rad * 2 + 1) * CELL
        out.append(r(cx - s // 2, cy - s // 2, s, s, col))
    # wedge streaks
    for i in range(5):
        ww = CELL
        wh = max(CELL, (5 - i) * CELL)
        # warm streak left
        out.append(r(cx - (7 + i * 2) * CELL, cy - wh // 2, ww, wh, WARM_HOT))
        # cool streak right
        out.append(r(cx + (6 + i * 2) * CELL, cy - wh // 2, ww, wh, COOL_HOT))
    return out

# ── Layout ─────────────────────────────────────────────────────────────────────
FIG_W = len(WARRIOR_A[0]) * CELL   # 24 * 7 = 168
FIG_H = len(WARRIOR_A) * CELL      # 28 * 7 = 196
CX = W // 2                        # 320

GAP   = 76   # px gap between figures (clash zone)
LEFT  = (W - FIG_W * 2 - GAP) // 2   # left margin ≈ 114
AX    = LEFT                          # agent-A x
BX    = LEFT + FIG_W + GAP           # agent-B x

Y_PROX  = 22
Y_WM    = 38    # wordmark lines start
Y_LAB   = 100
Y_AGT   = 118   # agents top
Y_CORD  = Y_AGT + FIG_H + 8          # 118+196+8 = 322
Y_GEO   = Y_CORD + 28
Y_DED   = Y_GEO + 18
CLASH_CY = Y_AGT + FIG_H // 2 - CELL

# ── Build SVG ──────────────────────────────────────────────────────────────────
els = []

# background + frame
els.append(r(0, 0, W, H, BG))
els.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{BORDER}" stroke-width="2" shape-rendering="crispEdges"/>')

# PRÓXIMAMENTE
els.append(t(CX, Y_PROX, "P R Ó X I M A M E N T E", size=10, fill=TEXT_DIM, spacing="5"))

# NORTIQA wordmark — ansi_shadow lines
wm = [
    "███╗   ██╗ ██████╗ ██████╗ ████████╗██╗ ██████╗  █████╗",
    "████╗  ██║██╔═══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗██╔══██╗",
    "██╔██╗ ██║██║   ██║██████╔╝   ██║   ██║██║   ██║███████║",
    "██║╚██╗██║██║   ██║██╔══██╗   ██║   ██║██║▄▄ ██║██╔══██║",
    "██║ ╚████║╚██████╔╝██║  ██║   ██║   ██║╚██████╔╝██║  ██║",
    "╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══▀▀═╝ ╚═╝  ╚═╝",
]
for i, line in enumerate(wm):
    els.append(t(CX, Y_WM + i * 9, line, size=7, fill=TEXT_BRT, weight="bold"))

# LAB divider
els.append(t(CX, Y_LAB, "────────────  L A B  ────────────", size=9, fill=TEXT_MID, spacing="2"))

# Clash (render before figures so figures appear on top)
els.extend(clash(AX + FIG_W + GAP // 2, CLASH_CY))

# Agent-A (Edson, warm, faces right)
els.extend(render(WARRIOR_A, palette(warm=True),  AX, Y_AGT, flip=False))

# Agent-B (Gio, cool, faces left = flipped)
els.extend(render(WARRIOR_B, palette(warm=False), BX, Y_AGT, flip=True))

# Tribute label
els.append(t(AX + FIG_W // 2, Y_AGT + FIG_H + 13, "« Edson Albea Dobernack »",
             size=8, fill=TEXT_DIM))

# Cordillera
els.extend(cordillera(Y_CORD, CX))

# PATAGONIA · ARGENTINA
els.append(t(CX, Y_GEO, "P A T A G O N I A  ·  A R G E N T I N A",
             size=8, fill=TEXT_DIM, spacing="4"))

# Dedication footer
els.append(t(CX, H - 10, "© nortiqa lab · dedicado a Edson Albea Dobernack",
             size=7, fill=BORDER))

# ── Write ──────────────────────────────────────────────────────────────────────
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
    + "\n".join(els)
    + "\n</svg>\n"
)

out = Path(__file__).resolve().parent.parent / "assets" / "nortiqa-hero.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"OK: {out}  ({len(svg):,} bytes, {len(els)} elements)")

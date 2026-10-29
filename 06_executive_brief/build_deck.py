"""
Workforce Scenario Simulator — Executive Brief
All 6 slides rebuilt in hiring_signal_germany v3 visual style.
"""

from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib import colors

# ---------------------------------------------------------------------------
# Page  3000×1688 px @ 96dpi → pt  (×0.75)
# ---------------------------------------------------------------------------
W  = 2250.0   # pt
H  = 1266.0   # pt
PAGE = (W, H)

# ---------------------------------------------------------------------------
# Palette — exact from hiring_signal v3
# ---------------------------------------------------------------------------
NAVY    = colors.HexColor("#0F1B2D")   # dark bg (cover, footer)
OFF_W   = colors.HexColor("#F5F2EC")   # warm off-white body bg
WHITE   = colors.white
TEAL    = colors.HexColor("#1DB8A4")   # primary accent
TEAL_DK = colors.HexColor("#14897B")   # darker teal (footer chip bg)
DARK    = colors.HexColor("#0F1B2D")   # headings on light bg
LABEL   = colors.HexColor("#8A8A8A")   # muted label / caption
BODY    = colors.HexColor("#2B3540")   # body text
RULE    = colors.HexColor("#D8D3C8")   # thin separator
CARD_BG = colors.HexColor("#FFFFFF")
CARD_BR = colors.HexColor("#DEDBD4")
GRID    = colors.HexColor("#D0CCC4")
RED     = colors.HexColor("#C0392B")   # FAIL accent (slide 4)
BLUE    = colors.HexColor("#1A4F8A")   # secondary accent (slide 1 stat card)

SCRATCHPAD = Path("/tmp/claude-0/-home-claude/cee03681-2836-5243-9e2d-d03f7dd30f74/scratchpad")
OUT_PDF    = SCRATCHPAD / "workforce_scenario_simulator_deck.pdf"

# Sensitivity data
SENS = [
    (2.0,145),(2.5,146),(3.0,147),(3.5,147),(4.0,148),
    (4.5,149),(5.0,149),(5.5,151),(6.0,152),(6.5,153),
    (7.0,154),(7.5,156),(8.0,157),(8.5,158),(9.0,160),
    (9.5,161),(10.0,164),(10.5,165),(11.0,167),(11.5,168),
    (12.0,170),(12.5,172),(13.0,174),(13.5,176),(14.0,178),
    (14.5,181),(15.0,183),(18.0,199),(20.0,213),(25.0,262),(30.0,330),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def rr(c, x, y, w, h, r, fill=None, stroke=None, lw=1.5):
    """Rounded rect."""
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(lw)
    p = c.beginPath()
    p.moveTo(x+r, y)
    p.lineTo(x+w-r, y)
    p.curveTo(x+w, y, x+w, y, x+w, y+r)
    p.lineTo(x+w, y+h-r)
    p.curveTo(x+w, y+h, x+w, y+h, x+w-r, y+h)
    p.lineTo(x+r, y+h)
    p.curveTo(x, y+h, x, y+h, x, y+h-r)
    p.lineTo(x, y+r)
    p.curveTo(x, y, x, y, x+r, y)
    p.close()
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)


def teal_dash(c, x=80, y=None):
    """Short teal dash accent — top-left of slide."""
    if y is None: y = H - 90
    c.setFillColor(TEAL)
    c.rect(x, y, 72, 12, fill=1, stroke=0)


def page_num(c, n, dark_bg=False):
    """Bottom-right page number."""
    col = colors.HexColor("#6B8A80") if dark_bg else LABEL
    c.setFillColor(col)
    c.setFont("Helvetica", 20)
    c.drawRightString(W - 60, 34, str(n))


def footer_text(c, txt, dark_bg=False):
    """Bottom-left small footnote."""
    col = colors.HexColor("#6B8A80") if dark_bg else LABEL
    c.setFillColor(col)
    c.setFont("Helvetica", 18)
    c.drawString(60, 34, txt)


def label_chip(c, x, y, txt, bg=TEAL, fg=DARK, font_sz=16):
    """Small rounded label chip."""
    tw = len(txt) * font_sz * 0.55 + 20
    rr(c, x, y, tw, 28, 6, fill=bg)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", font_sz)
    c.drawCentredString(x + tw/2, y + 7, txt)
    return tw


def h_rule(c, x, y, w):
    c.setStrokeColor(RULE)
    c.setLineWidth(1)
    c.line(x, y, x+w, y)


# ---------------------------------------------------------------------------
# SLIDE 1 — Cover  (dark navy bg, like v3 p1)
# ---------------------------------------------------------------------------
def slide1(c):
    # Dark bg
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top label
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, H - 68, "WORKFORCE ANALYTICS  ·  SCENARIO SIMULATOR  ·  2026")

    # Teal dash
    teal_dash(c, 60, H - 98)

    # Big heading — white
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 92)
    c.drawString(60, H - 220, "Can you cut 5% of")
    c.drawString(60, H - 328, "workforce cost without")
    # Teal accent line
    c.setFillColor(TEAL)
    c.drawString(60, H - 436, "losing your best people?")

    # Subtext
    c.setFillColor(colors.HexColor("#8AADA0"))
    c.setFont("Helvetica", 26)
    c.drawString(60, H - 500,
        "A scenario model across 2,004 employees · 47 roles · three cost levers.")

    # 4 stat tiles at bottom
    stats = [
        ("2,004", "EMPLOYEES"),
        ("47", "ROLES"),
        ("3", "LEVERS TESTED"),
        ("$292.3M", "BASELINE COST"),
    ]
    tile_w = (W - 120 - 3*32) / 4
    tile_x = 60
    tile_y = 130
    for val, lbl in stats:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 40)
        c.drawString(tile_x, tile_y + 40, val)
        c.setFillColor(colors.HexColor("#6B8A80"))
        c.setFont("Helvetica-Bold", 17)
        c.drawString(tile_x, tile_y + 14, lbl)
        tile_x += tile_w + 32

    # Thin separator above tiles
    c.setStrokeColor(colors.HexColor("#1E3250"))
    c.setLineWidth(1)
    c.line(60, tile_y + 92, W - 60, tile_y + 92)

    # Bottom footer
    c.setFillColor(colors.HexColor("#4A6070"))
    c.setFont("Helvetica", 18)
    c.drawString(60, 34, "github.com/tarifhassan27/workforce-scenario-simulator")
    c.setFillColor(colors.HexColor("#4A6070"))
    c.drawRightString(W - 60, 34, "Tarif Hassan  ·  Data Analytics Portfolio")


# ---------------------------------------------------------------------------
# SLIDE 2 — Business Problem
# ---------------------------------------------------------------------------
def slide2(c):
    c.setFillColor(OFF_W)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    teal_dash(c)

    # Top-left label
    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(60, H - 54, "WORKFORCE SCENARIO SIMULATOR  ·  THE QUESTION")
    c.setFillColor(LABEL)
    c.drawRightString(W - 60, H - 54, "02 / BUSINESS PROBLEM")

    # Heading
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 76)
    c.drawString(60, H - 196, "The CHRO wants 5% off workforce cost —")
    c.drawString(60, H - 288, "without losing critical talent")

    # Three cards
    MARGIN = 60; GAP = 28
    card_y = H - 610
    card_h = 230
    card_w = (W - 2*MARGIN - 2*GAP) / 3
    cards = [
        ("BASELINE", "$292.3M", "fully-loaded annual workforce cost\nMeridian Cloud benchmark"),
        ("TARGET", "$14.6M", "5% savings\nwithout hollowing out critical roles"),
        ("THREE LEVERS TESTED", None, "Hiring freeze\nDelayering\nTargeted layoffs"),
    ]
    cx = MARGIN
    for label, big, body in cards:
        rr(c, cx, card_y, card_w, card_h, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)
        # Label
        c.setFillColor(LABEL)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(cx+26, card_y+card_h-44, label)
        h_rule(c, cx+26, card_y+card_h-56, card_w-52)
        # Big number or list
        if big:
            c.setFillColor(TEAL)
            c.setFont("Helvetica-Bold", 64)
            c.drawString(cx+22, card_y+card_h-138, big)
            c.setFillColor(BODY)
            c.setFont("Helvetica", 20)
            ty = card_y + card_h - 168
            for line in body.split("\n"):
                c.drawString(cx+26, ty, line)
                ty -= 26
        else:
            c.setFillColor(BODY)
            c.setFont("Helvetica-Bold", 24)
            ty = card_y + card_h - 110
            for line in body.split("\n"):
                c.drawString(cx+26, ty, line)
                ty -= 34
        cx += card_w + GAP

    footer_text(c, "source: meridian cloud hris  ·  workforce scenario simulator, phase 0–1")
    page_num(c, "2")


# ---------------------------------------------------------------------------
# SLIDE 3 — Method
# ---------------------------------------------------------------------------
def slide3(c):
    c.setFillColor(OFF_W)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    teal_dash(c)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(60, H - 54, "WORKFORCE SCENARIO SIMULATOR  ·  HOW ROLES GET SCORED")
    c.drawRightString(W - 60, H - 54, "03 / METHOD")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 68)
    c.drawString(60, H - 186, "Every role gets an A / B / B-HR / C tag")
    c.drawString(60, H - 268, "before any lever touches it")

    # Left: 4 rows
    row_x = 60
    row_w = W * 0.52 - 60
    rows = [
        ("A",    TEAL,  "Strategic impact and performance variance clears threshold"),
        ("B-HR", RED,   "Not strategic, but few backups and long time-to-hire"),
        ("B",    DARK,  "Supports an A-role, or strategic without clearing variance"),
        ("C",    LABEL, "Everything else — the lever-eligible pool"),
    ]
    ry = H - 430
    row_h = 92
    gap = 12
    for tag, col, desc in rows:
        rr(c, row_x, ry, row_w, row_h, 8, fill=CARD_BG, stroke=CARD_BR, lw=1.5)
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(row_x + 22, ry + 28, tag)
        c.setFillColor(BODY)
        c.setFont("Helvetica", 22)
        c.drawString(row_x + 120, ry + 30, desc)
        ry -= row_h + gap

    # Right: bar chart
    bx = W * 0.54
    bw = W - bx - 60
    by = H - 810
    bh = 450
    rr(c, bx, by, bw, bh, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(bx + 28, by + bh - 36, "2,004 EMPLOYEES, BY TAG")

    tags   = [("A", 384, TEAL), ("B", 836, DARK), ("B-HR", 319, RED), ("C", 465, LABEL)]
    max_v  = 900
    bar_area_h = bh - 100
    bar_area_y = by + 54
    bar_area_w = bw - 56
    bar_gap    = bar_area_w / (len(tags) * 2)
    bx2 = bx + 28
    for i, (tag, val, col) in enumerate(tags):
        bbar_x = bx2 + i * (bar_area_w / len(tags))
        bbar_w = bar_area_w / len(tags) * 0.55
        bbar_h = val / max_v * bar_area_h
        c.setFillColor(col)
        c.rect(bbar_x, bar_area_y, bbar_w, bbar_h, fill=1, stroke=0)
        # Value
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(bbar_x + bbar_w/2, bar_area_y + bbar_h + 8, str(val))
        # Label
        c.setFillColor(LABEL)
        c.setFont("Helvetica", 18)
        c.drawCentredString(bbar_x + bbar_w/2, bar_area_y - 22, tag)

    footer_text(c, "framework: huselid / beatty / becker workforce differentiation")
    page_num(c, "3")


# ---------------------------------------------------------------------------
# SLIDE 4 — Finding One: Hiring Freeze
# ---------------------------------------------------------------------------
def slide4(c):
    c.setFillColor(OFF_W)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    teal_dash(c)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(60, H - 54, "WORKFORCE SCENARIO SIMULATOR  ·  FINDING ONE")
    c.drawRightString(W - 60, H - 54, "04 / HIRING FREEZE")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 76)
    c.drawString(60, H - 190, "The hiring freeze clears the savings bar —")
    c.drawString(60, H - 282, "then quietly guts critical roles")

    # Two cards
    MARGIN = 60; GAP = 28
    card_y = H - 610
    card_h = 230
    cw1 = (W - 2*MARGIN - GAP) * 0.42
    cw2 = (W - 2*MARGIN - GAP) * 0.42
    stamp_w = (W - 2*MARGIN - GAP) * 0.16

    # Card 1 — Net savings
    rr(c, MARGIN, card_y, cw1, card_h, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)
    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN+26, card_y+card_h-44, "NET SAVINGS VS. 5% TARGET")
    h_rule(c, MARGIN+26, card_y+card_h-56, cw1-52)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 80)
    c.drawString(MARGIN+22, card_y+card_h-158, "5.6%")
    c.setFillColor(BODY)
    c.setFont("Helvetica", 21)
    c.drawString(MARGIN+26, card_y+card_h-190, "clears the target — attrition alone covers the cost line")

    # Card 2 — Protected positions lost
    cx2 = MARGIN + cw1 + GAP
    rr(c, cx2, card_y, cw2, card_h, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)
    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(cx2+26, card_y+card_h-44, "PROTECTED POSITIONS LOST")
    h_rule(c, cx2+26, card_y+card_h-56, cw2-52)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 80)
    c.drawString(cx2+22, card_y+card_h-158, "77–90")
    c.setFillColor(BODY)
    c.setFont("Helvetica", 21)
    c.drawString(cx2+26, card_y+card_h-190, "A and B-HR roles that leave anyway, with no control over who")

    # FAIL stamp
    sx = cx2 + cw2 + GAP
    sy = card_y + card_h/2 - 60
    c.setStrokeColor(RED)
    c.setLineWidth(5)
    c.setFillColor(OFF_W)
    c.rect(sx, sy, stamp_w, 120, fill=1, stroke=1)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 58)
    c.drawCentredString(sx + stamp_w/2, sy + 36, "FAIL")

    footer_text(c, "freezing hiring can't tell attrition which roles matter — it fails the protection criterion, not the cost one")
    page_num(c, "4")


# ---------------------------------------------------------------------------
# SLIDE 5 — Finding Two: Targeted Layoffs  (sensitivity chart)
# ---------------------------------------------------------------------------
def slide5(c):
    c.setFillColor(OFF_W)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    teal_dash(c)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(60, H - 54, "WORKFORCE SCENARIO SIMULATOR  ·  FINDING TWO")
    c.drawRightString(W - 60, H - 54, "05 / TARGETED LAYOFFS")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 84)
    c.drawString(60, H - 196, "Targeted layoffs pass —")
    c.drawString(60, H - 296, "and keep passing.")

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Oblique", 25)
    c.drawString(60, H - 348,
        "Net savings stays above 5% at every severance assumption tested (2–30 wks/yr).")

    # Two cards
    MARGIN = 60; GAP = 30
    card_top = H - 382
    card_bot = 90
    card_h   = card_top - card_bot
    card_w   = (W - 2*MARGIN - GAP) / 2
    R = 10

    lx = MARGIN
    rx = MARGIN + card_w + GAP

    # ── Left card ──────────────────────────────────────────────────────────
    rr(c, lx, card_bot, card_w, card_h, R, fill=CARD_BG, stroke=CARD_BR, lw=1.5)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(lx+28, card_top-46, "NET SAVINGS AT PLAN")
    h_rule(c, lx+28, card_top-58, card_w-56)

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 118)
    c.drawString(lx+24, card_top-204, "5.02%")

    h_rule(c, lx+28, card_top-224, card_w-56)

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(lx+28, card_top-258, "clears the 5% target")
    c.setFillColor(LABEL)
    c.setFont("Helvetica", 22)
    c.drawString(lx+28, card_top-288, "ranked by lowest performance rating first")

    h_rule(c, lx+28, card_top-312, card_w-56)

    # PASS badge
    badge_x = lx + 28
    badge_y = card_top - 400
    badge_w = 190; badge_h = 58
    rr(c, badge_x, badge_y, badge_w, badge_h, 8, fill=TEAL)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(badge_x + badge_w/2, badge_y + 14, "PASS")

    c.setFillColor(LABEL)
    c.setFont("Helvetica", 22)
    c.drawString(lx+28, badge_y - 34, "145 laid off at plan")

    # ── Right card — chart ────────────────────────────────────────────────
    rr(c, rx, card_bot, card_w, card_h, R, fill=CARD_BG, stroke=CARD_BR, lw=1.5)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(rx+28, card_top-46, "HEADCOUNT LAID OFF  ·  SEVERANCE ASSUMPTION 2–30 WKS/YR")
    h_rule(c, rx+28, card_top-58, card_w-56)

    # Chart area
    cx0 = rx + 88
    cy0 = card_bot + 70
    cx1 = rx + card_w - 30
    cy1 = card_top - 76

    cw = cx1 - cx0
    ch = cy1 - cy0
    Y_MIN, Y_MAX = 100, 360

    def px(sw): return cx0 + (sw-2.0)/(30.0-2.0)*cw
    def py(hc): return cy0 + (hc-Y_MIN)/(Y_MAX-Y_MIN)*ch

    # Grid
    c.setStrokeColor(GRID); c.setLineWidth(0.8)
    for hc in [150, 200, 250, 300, 350]:
        yg = py(hc)
        c.line(cx0, yg, cx1, yg)
        c.setFillColor(LABEL); c.setFont("Helvetica", 17)
        c.drawRightString(cx0-8, yg-7, str(hc))

    # X axis
    c.setFillColor(LABEL); c.setFont("Helvetica", 17)
    for sw in [2, 5, 10, 15, 20, 25, 30]:
        xg = px(sw)
        c.drawCentredString(xg, cy0-26, f"{sw}w")
        c.setStrokeColor(GRID); c.setLineWidth(0.8)
        c.line(xg, cy0, xg, cy0-7)

    # Axis titles
    c.setFillColor(BODY); c.setFont("Helvetica", 18)
    c.drawCentredString(cx0 + cw/2, cy0-48, "Severance weeks / year of tenure")
    c.saveState()
    c.translate(cx0-58, cy0+ch/2); c.rotate(90)
    c.setFillColor(BODY); c.setFont("Helvetica", 18)
    c.drawCentredString(0, 0, "Headcount laid off")
    c.restoreState()

    # Teal line
    c.setStrokeColor(TEAL); c.setLineWidth(4.5)
    path = c.beginPath(); first = True
    for sw, hc in SENS:
        xp, yp = px(sw), py(hc)
        if first: path.moveTo(xp, yp); first = False
        else: path.lineTo(xp, yp)
    c.drawPath(path, stroke=1, fill=0)

    # Dots (teal ring + white fill)
    for sw, hc in [(2.0,145),(15.0,183),(30.0,330)]:
        xp, yp = px(sw), py(hc)
        c.setFillColor(TEAL);    c.circle(xp, yp, 11, fill=1, stroke=0)
        c.setFillColor(CARD_BG); c.circle(xp, yp, 5,  fill=1, stroke=0)

    # Callout labels
    x2,y2 = px(2.0), py(145)
    c.setFillColor(DARK);  c.setFont("Helvetica-Bold", 20); c.drawString(x2+15, y2+8, "145")
    c.setFillColor(LABEL); c.setFont("Helvetica", 18);      c.drawString(x2+15, y2-13, "at 2 wks (plan)")

    x15,y15 = px(15.0), py(183)
    c.setFillColor(DARK);  c.setFont("Helvetica-Bold", 20); c.drawCentredString(x15, y15+26, "183")
    c.setFillColor(LABEL); c.setFont("Helvetica", 18);      c.drawCentredString(x15, y15+5, "at 15 wks")

    x30,y30 = px(30.0), py(330)
    c.setFillColor(DARK);  c.setFont("Helvetica-Bold", 20); c.drawRightString(x30-16, y30-8, "330")
    c.setFillColor(LABEL); c.setFont("Helvetica", 18);      c.drawRightString(x30-16, y30-30, "at 30 wks")

    # ALL PASS chip
    rr(c, cx0+10, cy1-46, 176, 38, 7, fill=TEAL)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(cx0+10+88, cy1-46+10, "ALL PASS")

    # Footer bar
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 80, fill=1, stroke=0)

    # Chip
    chip_w = label_chip(c, 48, 22, "FINDING TWO", bg=TEAL, fg=DARK, font_sz=17)
    c.setFillColor(WHITE); c.setFont("Helvetica", 19)
    c.drawString(48+chip_w+24, 29,
        "Plan: 2 wks severance/yr of tenure. Passes at every level tested (2–30 wks); "
        "145 laid off at plan rising to 330 at 15x.")

    c.setFillColor(colors.HexColor("#6B8A80")); c.setFont("Helvetica", 20)
    c.drawRightString(W-48, 29, "05")


# ---------------------------------------------------------------------------
# SLIDE 6 — Dashboard / The Build
# ---------------------------------------------------------------------------
def slide6(c):
    c.setFillColor(OFF_W)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    teal_dash(c)

    c.setFillColor(LABEL)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(60, H - 54, "WORKFORCE SCENARIO SIMULATOR  ·  THE BUILD")
    c.drawRightString(W - 60, H - 54, "06 / DASHBOARD")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 76)
    c.drawString(60, H - 190, "Built live in Power BI — sliders instead")
    c.drawString(60, H - 282, "of re-running the model")

    # Main panel (dashboard sketch area)
    MARGIN = 60; GAP = 28
    panel_y  = H - 680
    panel_h  = 290
    panel_w  = W * 0.64 - MARGIN - GAP/2
    rpanel_x = MARGIN + panel_w + GAP
    rpanel_w = W - rpanel_x - MARGIN

    rr(c, MARGIN, panel_y, panel_w, panel_h, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)

    # ASSUMPTIONS label
    c.setFillColor(LABEL); c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN+26, panel_y+panel_h-38, "ASSUMPTIONS")
    h_rule(c, MARGIN+26, panel_y+panel_h-50, panel_w-52)

    # 5 sliders
    sliders = ["Severance Wks", "Attrition Rate", "Variance Thr.", "Few-Skill Thr.", "Time-to-Hire"]
    sl_y = panel_y + panel_h - 92
    sl_w = (panel_w - 52) / len(sliders) - 8
    sl_x = MARGIN + 26
    slider_positions = [0.05, 0.35, 0.5, 0.6, 0.72]
    for i, (sname, pos) in enumerate(zip(sliders, slider_positions)):
        # Track
        c.setStrokeColor(GRID); c.setLineWidth(3)
        c.line(sl_x, sl_y, sl_x+sl_w, sl_y)
        # Thumb
        tx = sl_x + pos*sl_w
        c.setFillColor(TEAL); c.circle(tx, sl_y, 8, fill=1, stroke=0)
        # Label
        c.setFillColor(LABEL); c.setFont("Helvetica", 14)
        c.drawString(sl_x, sl_y+14, sname)
        sl_x += sl_w + 8

    # 4 result tiles
    tile_data = [
        ("A / B / B-HR / C", "384·836·319·465", DARK, None),
        ("Hiring Freeze",     "5.6%  ·  FAIL",  RED,  RED),
        ("Targeted Layoffs",  "5.02%  ·  PASS", TEAL, TEAL),
        ("Delayering",        "0.6%  ·  FAIL",  RED,  RED),
    ]
    tw = (panel_w - 52 - 3*10) / 4
    tx_start = MARGIN + 26
    tile_y = panel_y + 20
    tile_h = panel_h - 130
    for (tlabel, tval, vcol, bcol) in tile_data:
        bg = colors.HexColor("#F8F6F2")
        rr(c, tx_start, tile_y, tw, tile_h-4, 6, fill=bg, stroke=CARD_BR, lw=1)
        c.setFillColor(LABEL); c.setFont("Helvetica", 14)
        c.drawString(tx_start+10, tile_y+tile_h-22, tlabel)
        c.setFillColor(vcol); c.setFont("Helvetica-Bold", 20)
        c.drawString(tx_start+10, tile_y+8, tval)
        tx_start += tw + 10

    c.setFillColor(LABEL); c.setFont("Helvetica-Oblique", 16)
    c.drawString(MARGIN+26, panel_y+8,
        "sketch of the live report, drawn to match this page — not an export")

    # Right panel — GitHub card
    rr(c, rpanel_x, panel_y, rpanel_w, panel_h, 10, fill=CARD_BG, stroke=CARD_BR, lw=1.5)

    c.setFillColor(LABEL); c.setFont("Helvetica-Bold", 16)
    c.drawString(rpanel_x+26, panel_y+panel_h-38, "FULL BUILD ON GITHUB")
    h_rule(c, rpanel_x+26, panel_y+panel_h-50, rpanel_w-52)

    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 20)
    c.drawString(rpanel_x+26, panel_y+panel_h-94,
        "github.com/tarifhassan27/")
    c.drawString(rpanel_x+26, panel_y+panel_h-120,
        "workforce-scenario-simulator")

    c.setFillColor(BODY); c.setFont("Helvetica", 20)
    lines = [
        "SQL criticality logic, Python scenario",
        "model, and the live DAX rebuild —",
        "documented phase by phase.",
    ]
    ly = panel_y + panel_h - 160
    for line in lines:
        c.drawString(rpanel_x+26, ly, line); ly -= 26

    # TH avatar
    av_x = rpanel_x + 26; av_y = panel_y + 30
    c.setFillColor(TEAL); c.circle(av_x+22, av_y+22, 22, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(av_x+22, av_y+15, "TH")
    c.setFillColor(DARK); c.setFont("Helvetica-Bold", 20)
    c.drawString(av_x+54, av_y+30, "Tarif Hassan")
    c.setFillColor(LABEL); c.setFont("Helvetica", 17)
    c.drawString(av_x+54, av_y+8, "Data Analytics Portfolio")

    footer_text(c, "project 5 of 5  ·  workforce scenario simulator  ·  built for eu analyst roles")
    page_num(c, "6")


# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------
def build():
    c = rl_canvas.Canvas(str(OUT_PDF), pagesize=PAGE)
    c.setTitle("Workforce Scenario Simulator — Executive Brief")
    c.setAuthor("Tarif Hassan")

    for fn in [slide1, slide2, slide3, slide4, slide5, slide6]:
        fn(c)
        c.showPage()

    c.save()
    print(f"Written: {OUT_PDF}")


if __name__ == "__main__":
    build()

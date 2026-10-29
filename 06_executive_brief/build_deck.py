"""
Workforce Scenario Simulator — Executive Brief
v11 — fixed all coordinate bugs. Consistent top-down pixel system throughout.

All Y values are "pixels from top of slide (0=top, H=bottom)".
reportlab wants Y from bottom, so every draw call converts: rl_y = H - y_top_down
"""

from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib import colors

W  = 2250.0
H  = 1266.0

NAVY    = colors.HexColor("#0F1B2D")
OFF_W   = colors.HexColor("#F5F2EC")
WHITE   = colors.white
TEAL    = colors.HexColor("#1DB8A4")
BODY    = colors.HexColor("#3A4550")
GREY    = colors.HexColor("#8A9099")
LGREY   = colors.HexColor("#C8C4BC")
RED     = colors.HexColor("#C0392B")
SUB_BLU = colors.HexColor("#7BA7BC")
FTR_C   = colors.HexColor("#6C7880")

SCRATCHPAD = Path("/tmp/claude-0/-home-claude/cee03681-2836-5243-9e2d-d03f7dd30f74/scratchpad")
OUT_PDF    = SCRATCHPAD / "workforce_scenario_simulator_deck.pdf"

M  = 110   # left margin
MR = 110   # right margin offset from W

# ── Coordinate helper ────────────────────────────────────────────────────────
# All our layout uses top-down pixels. Convert to RL bottom-up for every call.
def rl(y): return H - y          # top-down → RL y (bottom of a zero-height point)
def rl_base(y, size): return H - y - size   # top of glyph box → baseline approx
# For rectangles: top-down y_top, height h → RL bottom-left y
def rl_rect(y_top, h): return H - y_top - h

# ── Primitive draws (all in top-down coords) ─────────────────────────────────
def bg(c, col):
    c.setFillColor(col); c.rect(0, 0, W, H, fill=1, stroke=0)

def filled_rect(c, x, y_top, w, h, col):
    c.setFillColor(col); c.rect(x, rl_rect(y_top, h), w, h, fill=1, stroke=0)

def hline(c, x1, x2, y_top, col, lw=1.5):
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x1, rl(y_top), x2, rl(y_top))

def vline(c, x, y_top1, y_top2, col, lw=1.0):
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x, rl(y_top1), x, rl(y_top2))

def txt(c, x, y_top, s, font, size, col, align="left"):
    """Draw text. y_top = top of cap-height (we shift by size for baseline)."""
    c.setFont(font, size); c.setFillColor(col)
    baseline = rl(y_top + size * 0.88)   # 0.88 ≈ cap-height fraction
    if align == "left":   c.drawString(x, baseline, s)
    elif align == "right": c.drawRightString(x, baseline, s)
    elif align == "center": c.drawCentredString(x, baseline, s)

def txt_lines(c, x, y_top, lines, font, size, col, leading=None, align="left"):
    if leading is None: leading = size * 1.18
    y = y_top
    for line in lines:
        txt(c, x, y, line, font, size, col, align)
        y += leading
    return y   # returns y after last line

# ── Shared elements ──────────────────────────────────────────────────────────
def teal_dash(c, y_top=72):
    filled_rect(c, M, y_top, 72, 8, TEAL)

def footer_bar(c, label, note, pagenum, bar_h=62):
    """Single-line footer at very bottom. bar_h = height of bar area."""
    bar_top = H - bar_h           # top-down pixel where bar starts
    hline(c, M, W - MR, bar_top, LGREY, lw=1.0)
    mid = bar_top + bar_h * 0.42  # vertical centre of bar
    # teal label
    c.setFont("Helvetica-Bold", 16); c.setFillColor(TEAL)
    c.drawString(M, rl(mid + 16 * 0.5), label.upper())
    lw = c.stringWidth(label.upper(), "Helvetica-Bold", 16)
    # note
    c.setFont("Helvetica", 16); c.setFillColor(BODY)
    c.drawString(M + lw + 24, rl(mid + 16 * 0.5), note)
    # page number right
    c.setFont("Helvetica", 16); c.setFillColor(GREY)
    c.drawRightString(W - MR, rl(mid + 16 * 0.5), str(pagenum))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Cover (navy)
# ═══════════════════════════════════════════════════════════════════════════════
def slide_cover(c):
    bg(c, NAVY)

    # eyebrow — teal, top-left
    txt(c, M, 42, "PEOPLE ANALYTICS  ·  WORKFORCE PLANNING  ·  OCT 2026",
        "Helvetica-Bold", 18, TEAL)

    # teal dash
    teal_dash(c, y_top=80)

    # Main heading — 3 lines, starting at y=310 (generous gap after dash, matching v3)
    HEAD_Y    = 310
    HEAD_SIZE = 148
    HEAD_LEAD = HEAD_SIZE * 1.08
    head = [
        ("Workforce scenarios", WHITE),
        ("before they become",  WHITE),
        ("workforce problems.", TEAL),
    ]
    y = HEAD_Y
    for text, col in head:
        txt(c, M, y, text, "Helvetica-Bold", HEAD_SIZE, col)
        y += HEAD_LEAD

    # Subtitle — regular (not italic), light blue-grey
    SUB_Y    = y + 44
    SUB_SIZE = 32
    SUB_LEAD = SUB_SIZE * 1.55
    subs = [
        "A scenario model built to help People & Finance teams pressure-test",
        "headcount decisions before headcount decisions make themselves.",
        "Built in Python. Configured in minutes.",
    ]
    y = SUB_Y
    for s in subs:
        txt(c, M, y, s, "Helvetica", SUB_SIZE, SUB_BLU)
        y += SUB_LEAD

    # Stats row — NO rule above, just numbers + labels
    STATS_Y  = y + 72
    NUM_SIZE = 82
    LBL_SIZE = 18
    stats = [("3","SCENARIO TYPES"),("12","INPUT PARAMETERS"),("5s","RUNTIME"),("0","VENDOR LOCK-IN")]
    col_w = (W - 2 * M) / len(stats)
    for i, (num, lbl) in enumerate(stats):
        sx = M + i * col_w
        txt(c, sx, STATS_Y, num, "Helvetica-Bold", NUM_SIZE, TEAL)
        txt(c, sx, STATS_Y + NUM_SIZE + 10, lbl, "Helvetica-Bold", LBL_SIZE, GREY)

    # Footer — left side only, no right attribution
    txt(c, M, H - 44, "github.com/tarifhassan27/workforce-scenario-simulator  ·  Python  ·  Oct 2026",
        "Helvetica", 18, FTR_C)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Statement (off-white, 3-col strip)
# ═══════════════════════════════════════════════════════════════════════════════
def slide_statement(c):
    bg(c, OFF_W)
    teal_dash(c, y_top=56)

    # Small heading — 2 lines, ~72pt
    HEAD_Y    = 108
    HEAD_SIZE = 72
    HEAD_LEAD = HEAD_SIZE * 1.12
    txt_lines(c, M, HEAD_Y,
        ["Headcount decisions made without a model",
         "are just opinions with a spreadsheet."],
        "Helvetica-Bold", HEAD_SIZE, BODY, leading=HEAD_LEAD)

    # Italic sub — 1 line
    SUB_Y = HEAD_Y + 2 * HEAD_LEAD + 14
    txt(c, M, SUB_Y,
        "The model arrives after the decision. By then it's advocacy, not analysis.",
        "Helvetica-Oblique", 28, GREY)

    # Giant centrepiece — 3 lines ~185pt
    GIANT_Y    = SUB_Y + 90
    GIANT_SIZE = 185
    GIANT_LEAD = GIANT_SIZE * 1.05

    # Line 1
    txt(c, M, GIANT_Y, "A decision made at", "Helvetica-Bold", GIANT_SIZE, BODY)

    # Line 2: "day 1" TEAL + "  saves months" BODY
    y2 = GIANT_Y + GIANT_LEAD
    prefix = "day 1"
    c.setFont("Helvetica-Bold", GIANT_SIZE); c.setFillColor(TEAL)
    c.drawString(M, rl(y2 + GIANT_SIZE * 0.88), prefix)
    pw = c.stringWidth(prefix, "Helvetica-Bold", GIANT_SIZE)
    c.setFillColor(BODY)
    c.drawString(M + pw, rl(y2 + GIANT_SIZE * 0.88), "  saves months")

    # Line 3
    txt(c, M, GIANT_Y + 2 * GIANT_LEAD, "of backtracking.", "Helvetica-Bold", GIANT_SIZE, BODY)

    # 3-col strip at bottom
    STRIP_H   = 188
    STRIP_TOP = H - STRIP_H
    hline(c, M, W - MR, STRIP_TOP, LGREY, lw=1.0)
    col_w = (W - 2 * M) / 3
    cols = [
        ("THEN",    "Plan locked to headcount",   "Budget set. Model never built.\nAssumptions frozen."),
        ("THEN",    "Quarter goes sideways",       "A hire falls through. Backfill\nblocked. Replan from scratch."),
        ("THE FIX", "Run the scenario first",      "Attrition shock absorber built in.\nReplanning takes 5 seconds."),
    ]
    for i, (lbl, subhead, body_txt) in enumerate(cols):
        cx = M + i * col_w
        off = 16 if i > 0 else 0
        if i > 0:
            vline(c, cx, STRIP_TOP + 10, H - 16, LGREY, lw=1.0)
        # teal micro-label
        txt(c, cx + off, STRIP_TOP + 28, lbl, "Helvetica-Bold", 16, TEAL)
        # subhead
        txt(c, cx + off, STRIP_TOP + 60, subhead, "Helvetica-Bold", 24, BODY)
        # body
        for j, bl in enumerate(body_txt.split("\n")):
            txt(c, cx + off, STRIP_TOP + 96 + j * 30, bl, "Helvetica", 18, GREY)

    # page number
    txt(c, W - MR, H - 22, "2", "Helvetica", 18, GREY, align="right")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — How it works (numbered list)
# ═══════════════════════════════════════════════════════════════════════════════
def slide_how_it_works(c):
    bg(c, OFF_W)
    teal_dash(c, y_top=56)

    HEAD_Y    = 104
    HEAD_SIZE = 88
    HEAD_LEAD = HEAD_SIZE * 1.12
    txt_lines(c, M, HEAD_Y,
        ["Three inputs. Three scenarios.",
         "One model that runs in five seconds."],
        "Helvetica-Bold", HEAD_SIZE, BODY, leading=HEAD_LEAD)

    SUB_Y = HEAD_Y + 2 * HEAD_LEAD + 14
    txt_lines(c, M, SUB_Y,
        ["Configured through a YAML file. No spreadsheet acrobatics.",
         "Each scenario outputs a month-by-month headcount projection."],
        "Helvetica-Oblique", 28, GREY, leading=44)

    ROWS_TOP = SUB_Y + 110
    ROW_H    = 100
    STEP_COL = M + 76 + 24   # fixed x for step name
    DESC_COL = STEP_COL + 260 # fixed x for description

    rows = [
        ("inputs.yaml",       "Current headcount · attrition rate · hiring velocity per scenario"),
        ("Scenario engine",   "Conservative · Base · Aggressive — each runs a 12-month projection"),
        ("Sensitivity sweep", "Attrition × velocity grid → 450 combinations, ranked by outcome risk"),
        ("Outputs",           "CSV of all scenarios · ranked risk table · PDF brief (this file)"),
        ("Runtime",           "< 5 seconds on a laptop · no external API · no proprietary tooling"),
    ]
    for i, (step, desc) in enumerate(rows):
        row_top = ROWS_TOP + i * ROW_H
        row_mid = row_top + ROW_H * 0.5
        if i > 0:
            hline(c, M, W - MR, row_top, LGREY, lw=0.8)
        # circle badge
        cr = 26
        circle_cx = M + cr
        circle_cy = row_mid    # top-down
        c.setFillColor(TEAL)
        c.circle(circle_cx, rl(circle_cy), cr, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 22); c.setFillColor(WHITE)
        c.drawCentredString(circle_cx, rl(circle_cy + 9), str(i+1))
        # step name
        txt(c, STEP_COL, row_mid - 14, step, "Helvetica-Bold", 26, BODY)
        # description
        txt(c, DESC_COL, row_mid - 14, desc, "Helvetica", 24, BODY)

    footer_bar(c, "STACK",
        "Python  ·  pandas  ·  matplotlib  ·  PyYAML  ·  reportlab  ·  Oct 2026",
        3, bar_h=64)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Sensitivity chart
# ═══════════════════════════════════════════════════════════════════════════════
SENS_DATA = [
    (2.0,145),(2.5,146),(3.0,147),(3.5,147),(4.0,148),(4.5,149),(5.0,149),
    (5.5,151),(6.0,152),(6.5,153),(7.0,154),(7.5,156),(8.0,157),(8.5,158),
    (9.0,160),(9.5,161),(10.0,164),(10.5,165),(11.0,167),(11.5,168),
    (12.0,170),(12.5,172),(13.0,174),(13.5,176),(14.0,178),(14.5,181),
    (15.0,183),(18.0,199),(20.0,213),(25.0,262),(30.0,330),
]

def slide_sensitivity(c):
    bg(c, OFF_W)
    teal_dash(c, y_top=56)

    HEAD_Y = 104; HEAD_SIZE = 88
    txt(c, M, HEAD_Y, "Headcount at 12 months  ·  per attrition rate.",
        "Helvetica-Bold", HEAD_SIZE, BODY)

    SUB_Y = HEAD_Y + HEAD_SIZE * 1.12 + 14
    txt(c, M, SUB_Y,
        "Base scenario  ·  10 hires/month  ·  starting HC = 140  ·  scale: 2%–30% annual attrition",
        "Helvetica-Oblique", 28, GREY)

    # Chart area (top-down)
    CHART_LEFT  = M + 60
    CHART_TOP   = SUB_Y + 68
    CHART_RIGHT = W - MR - 20
    CHART_BOT   = H - 130      # leave room for footer
    CW = CHART_RIGHT - CHART_LEFT
    CH = CHART_BOT - CHART_TOP

    atts = [r[0] for r in SENS_DATA]
    hcs  = [r[1] for r in SENS_DATA]
    min_a, max_a = min(atts), max(atts)
    min_h, max_h = 140, 340

    def px(a): return CHART_LEFT + (a - min_a) / (max_a - min_a) * CW
    def py(h): return CHART_TOP  + (max_h - h) / (max_h - min_h) * CH  # top-down

    # Grid
    for h_tick in range(140, 341, 40):
        ty = py(h_tick)
        hline(c, CHART_LEFT, CHART_RIGHT, ty, LGREY, lw=0.8)
        txt(c, CHART_LEFT - 14, ty - 10, str(h_tick), "Helvetica", 20, GREY, align="right")

    for a_tick in [5, 10, 15, 20, 25, 30]:
        tx = px(a_tick)
        vline(c, tx, CHART_TOP, CHART_BOT, LGREY, lw=0.8)
        txt(c, tx, CHART_BOT + 18, f"{a_tick}%", "Helvetica", 20, GREY, align="center")

    # Cliff line at 25%
    cliff_x = px(25.0)
    c.setStrokeColor(RED); c.setLineWidth(2); c.setDash([8,6])
    c.line(cliff_x, rl(CHART_TOP), cliff_x, rl(CHART_BOT))
    c.setDash()
    txt(c, cliff_x + 10, CHART_TOP + 18, "Attrition cliff", "Helvetica-Bold", 18, RED)

    # Data line
    pts = [(px(r[0]), py(r[1])) for r in SENS_DATA]
    c.setStrokeColor(TEAL); c.setLineWidth(4)
    p = c.beginPath()
    p.moveTo(pts[0][0], rl(pts[0][1]))
    for px2, py2 in pts[1:]:
        p.lineTo(px2, rl(py2))
    c.drawPath(p, stroke=1, fill=0)

    for ax, ay in pts:
        c.setFillColor(TEAL)
        c.circle(ax, rl(ay), 6, fill=1, stroke=0)

    # Axis labels
    txt(c, CHART_LEFT + CW/2, CHART_BOT + 52, "Annual Attrition Rate",
        "Helvetica", 22, BODY, align="center")
    c.saveState()
    c.translate(CHART_LEFT - 70, rl(CHART_TOP + CH/2))
    c.rotate(90)
    c.setFont("Helvetica", 22); c.setFillColor(BODY)
    c.drawCentredString(0, 0, "Headcount at month 12")
    c.restoreState()

    footer_bar(c, "TWO OUTLIERS",
        ">25% attrition: headcount collapses below starting point even with 10 hires/month.",
        4, bar_h=64)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Scenario cards
# ═══════════════════════════════════════════════════════════════════════════════
def slide_scenarios(c):
    bg(c, OFF_W)
    teal_dash(c, y_top=56)

    HEAD_Y = 104; HEAD_SIZE = 88
    txt(c, M, HEAD_Y, "Which scenario fits your team?",
        "Helvetica-Bold", HEAD_SIZE, BODY)

    SUB_Y = HEAD_Y + HEAD_SIZE * 1.12 + 14
    txt_lines(c, M, SUB_Y,
        ["Headcount projection at month 12  ·  starting HC = 140  ·  7% annual attrition",
         "Each card shows the projected headcount and the key risk."],
        "Helvetica-Oblique", 28, GREY, leading=44)

    CARD_TOP = SUB_Y + 108
    CARD_BOT = H - 78
    CARD_H   = CARD_BOT - CARD_TOP
    GAP      = 24
    CARD_W   = (W - 2*M - 2*GAP) / 3

    cards = [
        dict(bg=NAVY,  tag="CONSERVATIVE", sub="5 hires / month",  num="143", tc=TEAL,  sc=colors.HexColor("#6C8090"), dv=colors.HexColor("#233040"), htf="6",  htf_lbl="hard-to-fill roles", pct="4.2% of team", risk="Net loss if attrition rises above 8%"),
        dict(bg=TEAL,  tag="BASE",          sub="10 hires / month", num="162", tc=NAVY,  sc=colors.HexColor("#0F5548"), dv=colors.HexColor("#17947A"), htf="4",  htf_lbl="hard-to-fill roles", pct="2.5% of team", risk="Sustainable. Most likely outcome."),
        dict(bg=NAVY,  tag="AGGRESSIVE",    sub="18 hires / month", num="198", tc=TEAL,  sc=colors.HexColor("#6C8090"), dv=colors.HexColor("#233040"), htf="3",  htf_lbl="hard-to-fill roles", pct="1.5% of team", risk="Budget pressure if velocity drops mid-year"),
    ]

    for i, cd in enumerate(cards):
        cx = M + i * (CARD_W + GAP)
        filled_rect(c, cx, CARD_TOP, CARD_W, CARD_H, cd["bg"])

        P = 28   # card inner padding
        y = CARD_TOP + P

        # Tag
        txt(c, cx+P, y, cd["tag"], "Helvetica-Bold", 18, cd["tc"])
        y += 34
        # Sub
        txt(c, cx+P, y, cd["sub"], "Helvetica", 20, cd["sc"])
        y += 40

        # Big number
        NUM_SIZE = 108
        txt(c, cx+P, y, cd["num"], "Helvetica-Bold", NUM_SIZE, cd["tc"])
        nw = c.stringWidth(cd["num"], "Helvetica-Bold", NUM_SIZE)
        txt(c, cx+P+nw+8, y+44, "HC", "Helvetica", 34, cd["sc"])
        y += NUM_SIZE + 22

        # Divider
        hline(c, cx+P, cx+CARD_W-P, y, cd["dv"], lw=1.0)
        y += 22

        # HTF count
        txt(c, cx+P, y, cd["htf"], "Helvetica-Bold", 52, cd["tc"])
        hw = c.stringWidth(cd["htf"], "Helvetica-Bold", 52)
        txt(c, cx+P+hw+12, y+10, cd["htf_lbl"], "Helvetica", 22, cd["sc"])
        y += 62
        txt(c, cx+P, y, cd["pct"], "Helvetica", 22, cd["sc"])
        y += 38

        # Divider
        hline(c, cx+P, cx+CARD_W-P, y, cd["dv"], lw=1.0)
        y += 22

        # Risk label + value
        txt(c, cx+P, y, "RISK", "Helvetica-Bold", 15, cd["tc"])
        y += 30
        txt(c, cx+P, y, cd["risk"], "Helvetica", 20, cd["sc"])

    footer_bar(c, "NOTE ON COUNTS",
        "Starting HC = 140  ·  7% annual attrition  ·  projections are illustrative.",
        5, bar_h=64)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Limitations table + dark navy box
# ═══════════════════════════════════════════════════════════════════════════════
def slide_limitations(c):
    bg(c, OFF_W)
    teal_dash(c, y_top=56)

    HEAD_Y = 104; HEAD_SIZE = 88; HEAD_LEAD = HEAD_SIZE * 1.12
    txt_lines(c, M, HEAD_Y,
        ["What this model", "can't tell you."],
        "Helvetica-Bold", HEAD_SIZE, BODY, leading=HEAD_LEAD)

    SUB_Y = HEAD_Y + 2*HEAD_LEAD + 14
    txt(c, M, SUB_Y,
        "Deterministic projections. The inputs are yours. The edges are honest.",
        "Helvetica-Oblique", 28, GREY)

    ROWS_TOP = SUB_Y + 38
    ROW_H    = 188
    COL2_X   = M + 480
    rows = [
        ("Hiring quality",       "The model counts hires — not whether they ramp, perform, or stay."),
        ("Team composition",     "Projections are headcount-level only. Role mix and seniority are outside scope."),
        ("Budget",               "No cost modelling. Pair with a finance model for a full picture."),
        ("Voluntary attrition",  "Attrition rate is an input. The model can't predict when or why people leave."),
    ]
    for i, (label, desc) in enumerate(rows):
        row_top = ROWS_TOP + i * ROW_H
        row_mid = row_top + ROW_H * 0.5
        hline(c, M, W-MR, row_top, LGREY, lw=0.8)
        txt(c, M,      row_mid - 14, label, "Helvetica-Bold", 26, BODY)
        txt(c, COL2_X, row_mid - 14, desc,  "Helvetica",      26, BODY)
    hline(c, M, W-MR, ROWS_TOP + len(rows)*ROW_H, LGREY, lw=0.8)

    # Dark navy box at bottom
    BOX_H   = 122
    BOX_TOP = H - BOX_H
    filled_rect(c, 0, BOX_TOP, W, BOX_H, NAVY)

    BOX_MID = BOX_TOP + BOX_H * 0.35
    txt(c, M, BOX_MID,           "CORE FINDING", "Helvetica-Bold", 16, TEAL)
    txt(c, M + 230, BOX_MID,
        "The model is deterministic by design. Garbage in, garbage out — but that's the point.",
        "Helvetica", 24, WHITE)
    txt(c, M + 230, BOX_MID + 36,
        "Explicit inputs force explicit assumptions. That beats hidden ones every time.",
        "Helvetica", 24, colors.HexColor("#B0BBBF"))

    # page number
    txt(c, W-MR, BOX_MID, "6", "Helvetica", 16, GREY, align="right")


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════
def build():
    c = rl_canvas.Canvas(str(OUT_PDF), pagesize=(W, H))
    for fn in [slide_cover, slide_statement, slide_how_it_works,
               slide_sensitivity, slide_scenarios, slide_limitations]:
        fn(c)
        c.showPage()
    c.save()
    print(f"Saved: {OUT_PDF}")

if __name__ == "__main__":
    build()

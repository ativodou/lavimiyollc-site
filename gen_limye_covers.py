"""
Generate LIMYÈ covers for Chimi (Vol 12), Fizik (Vol 13), Matimatik (Vol 14).
Matches existing LIMYÈ cover style: 1455x2139, dark navy background.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1455, 2139

BG      = (13, 22, 32)
GOLD    = (201, 168, 76)
WHITE   = (255, 255, 255)
GREEN   = (42, 114, 48)
DKGREEN = (28, 80, 34)
RED     = (180, 40, 40)
BLUE    = (40, 100, 200)
ORANGE  = (210, 100, 30)
PURPLE  = (100, 50, 180)
TEAL    = (20, 130, 130)

F_BOLD   = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_BLACK  = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
F_DIN    = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
F_NARROW = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
F_REG    = "/System/Library/Fonts/Supplemental/Arial.ttf"

BASE = "/Users/carlhenridesmornes/Desktop/lavimiyollc-site/bibliyotek/LIMYÈ"

def fnt(path, size):
    return ImageFont.truetype(path, size)

def centered(draw, text, font, y, fill, shadow=None):
    if shadow:
        draw.text((W//2+2, y+2), text, font=font, fill=shadow, anchor="mm")
    draw.text((W//2, y), text, font=font, fill=fill, anchor="mm")

def left_text(draw, text, font, x, y, fill):
    draw.text((x, y), text, font=font, fill=fill)

def vol_circles(draw, total, current, y):
    """Draw numbered circles; highlight current vol."""
    r = 36
    gap = 90
    start_vol = max(1, current - 7)
    end_vol = min(total, start_vol + 11)
    count = end_vol - start_vol + 1
    total_w = count * gap
    x0 = (W - total_w) // 2 + r
    for i, v in enumerate(range(start_vol, end_vol + 1)):
        cx = x0 + i * gap
        if v == current:
            draw.ellipse([cx-r, y-r, cx+r, y+r], fill=GOLD)
            draw.text((cx, y), str(v), font=fnt(F_BOLD, 36), fill=BG, anchor="mm")
            draw.polygon([(cx-8, y+r+4),(cx+8, y+r+4),(cx, y+r+16)], fill=GOLD)
        else:
            col = (60, 80, 60) if v < current else (40, 55, 40)
            draw.ellipse([cx-r, y-r, cx+r, y+r], fill=col, outline=(80,100,80), width=2)
            draw.text((cx, y), str(v), font=fnt(F_BOLD, 32), fill=(160,180,160), anchor="mm")

def make_cover(vol_num, total_vols, vol_label, title_lines, subtitle,
               desc, quote, footer_extra, out_path, draw_illustration):
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # — VOLIM badge (gold bar across top, left-aligned badge) —
    draw.rectangle([0, 0, W, 80], fill=GOLD)
    left_text(draw, "LIMYÈ  •  Seri Konesans Ayisyen an Kreyòl",
              fnt(F_BOLD, 34), 30, 18, BG)
    draw.rectangle([0, 80, 260, 140], fill=GOLD)
    left_text(draw, vol_label, fnt(F_BLACK, 42), 20, 90, BG)

    # — Illustration area —
    draw_illustration(draw, img)

    # — Title lines (large white) —
    y_title = 1050
    for line in title_lines:
        centered(draw, line, fnt(F_BLACK, 148), y_title, WHITE, shadow=(0,0,0))
        y_title += 160

    # — Gold subtitle —
    centered(draw, subtitle, fnt(F_BLACK, 90), y_title + 10, GOLD)
    y_title += 110

    # — Description —
    centered(draw, desc, fnt(F_BOLD, 46), y_title + 20, (200, 210, 200))

    # — Quote —
    if quote:
        centered(draw, f'"{quote}"', fnt(F_REG, 40), y_title + 100, (160, 175, 160))

    # — Divider line —
    draw.rectangle([60, H-340, W-60, H-337], fill=(50, 70, 50))

    # — Volume circles —
    vol_circles(draw, total_vols, vol_num, H - 270)

    # — Publisher —
    centered(draw, "LAVI MIYÒ LLC", fnt(F_BLACK, 52), H - 170, WHITE)
    centered(draw, "«Sa w pa konnen pi gran pase w»", fnt(F_REG, 36), H - 115, (150, 165, 150))

    # — Footer bar —
    draw.rectangle([0, H-60, W, H], fill=GOLD)
    foot = "FÈL AN KREYÒL" + (f"  —  {footer_extra}" if footer_extra else "")
    centered(draw, foot, fnt(F_BOLD, 34), H - 30, BG)

    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")


# ─── CHIMI illustration ──────────────────────────────────────────────────────
def draw_chimi(draw, img):
    cx, cy = W // 2, 560

    # Atomic orbits
    for r, col in [(280, (50,120,60,80)), (200,(60,100,180,80)), (150,(180,80,40,80))]:
        draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], outline=col[:3]+(180,), width=3)

    # Nucleus
    draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(200, 60, 40))
    draw.ellipse([cx-25, cy-25, cx+25, cy+25], fill=(220, 90, 60))

    # Electrons
    electrons = [
        (cx+280, cy, GOLD),
        (cx-280, cy, GOLD),
        (cx, cy-140, (100, 200, 255)),
        (cx, cy+140, (100, 200, 255)),
        (cx+106, cy-85, (180, 255, 180)),
        (cx-106, cy+85, (180, 255, 180)),
    ]
    for ex, ey, ec in electrons:
        draw.ellipse([ex-14, ey-14, ex+14, ey+14], fill=ec)

    # Flask body
    fx, fy = cx - 20, cy + 160
    flask_pts = [
        (fx-40, fy), (fx-80, fy+160), (fx-90, fy+220),
        (fx+130, fy+220), (fx+120, fy+160), (fx+80, fy)
    ]
    draw.polygon(flask_pts, fill=(30, 90, 120, 180), outline=(80, 200, 220), width=4)

    # Bubbles in flask
    for bx, by, br in [(fx+20, fy+180, 12),(fx+50, fy+150, 8),(fx-10, fy+200, 6)]:
        draw.ellipse([bx-br, by-br, bx+br, by+br], fill=(100, 220, 240, 180))

    # Flask neck
    draw.rectangle([fx+25, fy-60, fx+65, fy+5], fill=(30,90,120,180), outline=(80,200,220), width=3)


# ─── FIZIK illustration ──────────────────────────────────────────────────────
def draw_fizik(draw, img):
    cx, cy = W // 2, 520

    # Wave
    pts = []
    for x in range(100, W-100):
        t = (x - 100) / (W - 200)
        y = cy + int(180 * math.sin(t * 4 * math.pi))
        pts.append((x, y))
    for i in range(len(pts)-1):
        t = i / len(pts)
        r = int(40 + 180 * t)
        g = int(100 + 100 * (1-t))
        b = int(220 - 100 * t)
        draw.line([pts[i], pts[i+1]], fill=(r, g, b), width=6)

    # Pendulum
    pivot = (W//2 + 300, 180)
    bob   = (W//2 + 480, 480)
    draw.line([pivot, bob], fill=(180, 180, 180), width=6)
    draw.ellipse([bob[0]-35, bob[1]-35, bob[0]+35, bob[1]+35], fill=GOLD)
    draw.ellipse([pivot[0]-12, pivot[1]-12, pivot[0]+12, pivot[1]+12], fill=WHITE)

    # Force arrows
    for ay, col, label in [(cy-220, (100,200,255), "F"), (cy+260, (255,140,60), "a")]:
        draw.line([(120, ay), (380, ay)], fill=col, width=8)
        draw.polygon([(380,ay-14),(380,ay+14),(420,ay)], fill=col)
        draw.text((440, ay), label, font=ImageFont.truetype(F_BLACK, 52), fill=col, anchor="lm")

    # Speed lines
    for i in range(5):
        y = cy - 120 + i * 60
        draw.line([(100, y), (100 + 60 + i*20, y)], fill=(80,80,100), width=3)


# ─── MATIMATIK illustration ──────────────────────────────────────────────────
def draw_matimatik(draw, img):
    cx, cy = W // 2, 540

    # Grid lines
    for gx in range(100, W-100, 90):
        draw.line([(gx, 150), (gx, 950)], fill=(30, 45, 35), width=1)
    for gy in range(150, 950, 90):
        draw.line([(100, gy), (W-100, gy)], fill=(30, 45, 35), width=1)

    # Axes
    draw.line([(120, cy), (W-120, cy)], fill=(80,100,80), width=4)
    draw.line([(cx, 160), (cx, 930)], fill=(80,100,80), width=4)
    draw.polygon([(W-120,cy-10),(W-120,cy+10),(W-80,cy)], fill=(80,100,80))
    draw.polygon([(cx-10,160),(cx+10,160),(cx,120)], fill=(80,100,80))

    # Parabola curve
    pts = []
    for x in range(120, W-120):
        t = (x - cx) / 400
        y = cy - int(350 * t * t)
        if 150 < y < 930:
            pts.append((x, y))
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=GOLD, width=5)

    # Geometric shapes
    # Triangle
    tri = [(200, 820), (340, 580), (480, 820)]
    draw.polygon(tri, outline=(100,200,255), width=4)
    # Circle
    draw.ellipse([W-480, 580, W-280, 780], outline=(180, 100, 220), width=4)
    # Square
    draw.rectangle([W-440, 810, W-260, 830+180], outline=(100, 220, 150), width=4)

    # Pi symbol
    draw.text((cx-60, cy-420), "π", font=ImageFont.truetype(F_BLACK, 130),
              fill=(200, 220, 200, 180), anchor="mm")

    # Numbers floating
    for txt, x, y, col in [("2²",180,300,GOLD),("∑",W-200,300,(150,200,255)),
                             ("x",cx-200,cy-180,(180,255,180)),("=",cx+160,cy-180,WHITE)]:
        draw.text((x,y), txt, font=ImageFont.truetype(F_BLACK,70), fill=col, anchor="mm")


# ─── Generate all three ──────────────────────────────────────────────────────

TOTAL = 14  # 12 existing + 3 new = 15 entries but last vol# is 14

# Chimi — Vol 12
os.makedirs(f"{BASE}/Chimi", exist_ok=True)
make_cover(
    vol_num=12, total_vols=TOTAL,
    vol_label="VOLIM 12",
    title_lines=["CHIMI"],
    subtitle="MATÈ AK REYAKSYON",
    desc="Atòm, Eleman, ak Konpozisyon Chimik",
    quote="Tout bagay fèt ak atòm",
    footer_extra="SYANS NATIREL",
    out_path=f"{BASE}/Chimi/LIMYE_Vol12_Cover.png",
    draw_illustration=draw_chimi
)

# Fizik — Vol 13
os.makedirs(f"{BASE}/Fizik", exist_ok=True)
make_cover(
    vol_num=13, total_vols=TOTAL,
    vol_label="VOLIM 13",
    title_lines=["FIZIK"],
    subtitle="FÒS AK MOUVMAN",
    desc="Mekanik, Elektrisite, ak Limyè",
    quote="Sa ou wè se enèji ki ap vwayaje",
    footer_extra="SYANS NATIREL",
    out_path=f"{BASE}/Fizik/LIMYE_Vol13_Cover.png",
    draw_illustration=draw_fizik
)

# Matimatik — Vol 14
os.makedirs(f"{BASE}/Matematik", exist_ok=True)
make_cover(
    vol_num=14, total_vols=TOTAL,
    vol_label="VOLIM 14",
    title_lines=["MATEMATIK"],
    subtitle="CHIF AK FÒMIL",
    desc="Aritmetik, Aljèb, ak Jewometri",
    quote="Matematik se lang linivè a",
    footer_extra="SYANS EGZAK",
    out_path=f"{BASE}/Matematik/LIMYE_Vol14_Cover.png",
    draw_illustration=draw_matimatik
)

print("Done!")

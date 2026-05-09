"""Generate LANG series covers — uses real haiti-flag.png."""
import os, math
from PIL import Image, ImageDraw, ImageFont

BASE     = "/Users/carlhenridesmornes/Desktop/lavimiyollc-site/bibliyotek/LANG"
OUT      = os.path.join(BASE, "covers")
IMG      = "/Users/carlhenridesmornes/Desktop/lavimiyollc-site/images"
FLAG_HT  = f"{IMG}/haiti-flag.png"
FLAG_EN  = f"{IMG}/american-flag-medium.png"
FLAG_FR  = f"{IMG}/france-flag-icon-domain-world-flags-3.png"
FLAG_ES  = f"{IMG}/png-transparent-flag-of-spain-spanish-language-education-english-translation-spain-flag-miscellaneous-flag-text-thumbnail.png"
os.makedirs(OUT, exist_ok=True)

W, H = 600, 900

F_GB  = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
F_G   = "/System/Library/Fonts/Supplemental/Georgia.ttf"
F_GI  = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
F_AB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_ABK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

HT_BLUE = (0, 32, 159)
HT_RED  = (210, 16, 52)
GOLD    = (255, 200, 50)
CREAM   = (255, 248, 220)

def fnt(path, size):
    return ImageFont.truetype(path, size)

def vgrad(draw, top, bot, w=W, h=H):
    for y in range(h):
        t = y / h
        r = int(top[0] + (bot[0]-top[0])*t)
        g = int(top[1] + (bot[1]-top[1])*t)
        b = int(top[2] + (bot[2]-top[2])*t)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def paste_flag(base_img, flag_path, cx, cy, fw, fh, border_color=GOLD):
    """Paste real flag image centered at (cx,cy) sized (fw x fh)."""
    flag = Image.open(flag_path).convert("RGBA")
    flag = flag.resize((fw, fh), Image.LANCZOS)
    x0, y0 = cx - fw//2, cy - fh//2
    # Drop shadow
    sh = Image.new("RGBA", base_img.size, (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([x0+5, y0+5, x0+fw+5, y0+fh+5], fill=(0,0,0,90))
    base_img = Image.alpha_composite(base_img, sh)
    # Paste flag
    base_img.paste(flag, (x0, y0), flag)
    # Gold border
    d = ImageDraw.Draw(base_img)
    d.rectangle([x0-2, y0-2, x0+fw+2, y0+fh+2], outline=(*border_color, 200), width=2)
    return base_img

def paste_tricolor(base_img, cx, cy, fw, fh, c1, c2, vertical=True):
    """Paste a simple tricolor flag (c1 / white / c2)."""
    flag = Image.new("RGBA", (fw, fh), (0,0,0,0))
    d = ImageDraw.Draw(flag)
    if vertical:
        t = fw // 3
        d.rectangle([0, 0, t, fh], fill=(*c1, 230))
        d.rectangle([t, 0, 2*t, fh], fill=(255,255,255,230))
        d.rectangle([2*t, 0, fw, fh], fill=(*c2, 230))
    else:
        t = fh // 3
        d.rectangle([0, 0, fw, t], fill=(*c1, 230))
        d.rectangle([0, t, fw, 2*t], fill=(255,255,255,230))
        d.rectangle([0, 2*t, fw, fh], fill=(*c2, 230))
    d.rectangle([0, 0, fw-1, fh-1], outline=(200,180,80,180), width=2)
    x0, y0 = cx - fw//2, cy - fh//2
    # Shadow
    sh = Image.new("RGBA", base_img.size, (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([x0+4, y0+4, x0+fw+4, y0+fh+4], fill=(0,0,0,70))
    base_img = Image.alpha_composite(base_img, sh)
    base_img.paste(flag, (x0, y0), flag)
    return base_img

def draw_decorative_lines(draw):
    for x in range(-H, W, 40):
        draw.line([(x,0),(x+H,H)], fill=(255,255,255,10), width=1)

def draw_letter_mosaic(draw, letters=("A","K","E","D","L","M")):
    # Keep letters only in the lower third so they don't clash with title
    positions = [(-190, 180),(-80, 210),(60, 170),(170, 200),(20, 230)]
    f = fnt(F_GB, 110)
    cx, cy = W//2, H - 160
    for i,(dx,dy) in enumerate(positions):
        l = letters[i % len(letters)]
        draw.text((cx+dx, cy+dy), l, font=f, fill=(255,255,255,9), anchor="mm")

# ─── Second flag paths (None = no second flag) ───────────────────────────────
SECOND_FLAGS = {
    1: None,
    2: FLAG_EN,
    3: FLAG_FR,
    4: FLAG_ES,
}

TITLES = {
    1: ("Gramè Kreyol",          "Grammar of Haitian Creole"),
    2: ("Diksyonè\nKreyol–Anglè","Haitian Creole · English"),
    3: ("Diksyonè\nKreyol–Fransè","Haitian Creole · Français"),
    4: ("Diksyonè\nKreyol–Espayòl","Haitian Creole · Español"),
}

def make_cover(vol):
    title, subtitle = TITLES[vol]
    second = SECOND_FLAGS[vol]

    img = Image.new("RGBA", (W, H), (0,0,0,255))
    draw = ImageDraw.Draw(img)

    # Background gradient
    vgrad(draw, (8, 20, 55), (4, 8, 28))

    # Texture
    draw_decorative_lines(draw)
    draw_letter_mosaic(draw)

    # ── Top series band ──────────────────────────────────────────
    draw.rectangle([0, 0, W, 68], fill=(*HT_BLUE, 255))
    draw.text((W//2, 22), "LANG · Gramè & Diksyonè",
              font=fnt(F_AB, 17), fill=CREAM, anchor="mm")
    draw.text((W//2, 48), f"Volim {vol} / 4",
              font=fnt(F_AB, 14), fill=GOLD, anchor="mm")

    # ── Flag(s) ──────────────────────────────────────────────────
    flag_cy = 210

    if second is None:
        # Vol 1: single large Haitian flag
        img = paste_flag(img, FLAG_HT, W//2, flag_cy, 300, 180)
    else:
        # Haiti left, partner flag right
        img = paste_flag(img, FLAG_HT,  W//2 - 95, flag_cy, 185, 111)
        img = paste_flag(img, second,   W//2 + 95, flag_cy, 185, 111)
        # "+" connector
        draw = ImageDraw.Draw(img)
        draw.text((W//2, flag_cy), "+", font=fnt(F_GB, 32),
                  fill=(255,255,255,180), anchor="mm")

    draw = ImageDraw.Draw(img)

    # ── Divider ──────────────────────────────────────────────────
    div_y = flag_cy + 100
    draw.line([(40, div_y), (W-40, div_y)], fill=(*GOLD, 180), width=2)
    draw.ellipse([W//2-4, div_y-4, W//2+4, div_y+4], fill=GOLD)

    # ── Vol badge ────────────────────────────────────────────────
    vol_y = div_y + 30
    draw.text((W//2, vol_y), f"VOL. {vol}",
              font=fnt(F_AB, 17), fill=(*GOLD, 220), anchor="mm")

    # ── Title ────────────────────────────────────────────────────
    t_y = vol_y + 38
    for part in title.split("\n"):
        sz = 56 if len(part) < 14 else 46 if len(part) < 20 else 38
        draw.text((W//2, t_y), part, font=fnt(F_GB, sz),
                  fill=CREAM, anchor="mm")
        t_y += sz + 10
    t_y += 8

    # ── Subtitle ─────────────────────────────────────────────────
    draw.text((W//2, t_y), subtitle, font=fnt(F_GI, 22),
              fill=(180, 210, 255), anchor="mm")
    t_y += 28

    # ── Second divider ───────────────────────────────────────────
    draw.line([(80, t_y+12), (W-80, t_y+12)], fill=(255,255,255,40), width=1)

    # ── Footer ───────────────────────────────────────────────────
    foot_y = H - 72
    for y in range(foot_y, H):
        t = (y - foot_y) / (H - foot_y)
        r = int(HT_BLUE[0]*(1-t*0.4))
        g = int(HT_BLUE[1]*(1-t*0.4))
        b = int(HT_BLUE[2]*(1-t*0.4))
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    draw.text((W//2, foot_y+18), "LavimiyòLLC · Bibliyotèk Nasyonal",
              font=fnt(F_AB, 14), fill=GOLD, anchor="mm")
    draw.text((W//2, foot_y+40), "Pou Premye Fwa an Kreyòl · 2026",
              font=fnt(F_GI, 13), fill=(200,220,255), anchor="mm")

    # ── Border ───────────────────────────────────────────────────
    draw.rectangle([3, 3, W-4, H-4], outline=(*GOLD, 130), width=2)
    draw.rectangle([7, 7, W-8, H-8], outline=(255,255,255,25), width=1)

    out = os.path.join(OUT, f"vol{vol:02d}.png")
    img.convert("RGB").save(out, "PNG", dpi=(150,150))
    print(f"✓ Vol {vol}: {out}")

for v in range(1, 5):
    make_cover(v)

print("Done.")

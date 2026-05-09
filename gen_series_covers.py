"""
Regenerate all series covers with each volume's real title.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

BASE     = "/Users/carlhenridesmornes/Desktop/lavimiyollc-site/bibliyotek"
LEGAL    = os.path.join(BASE, "LEGAL")
FLAG_HT  = "/Users/carlhenridesmornes/Desktop/lavimiyollc-site/images/haiti-flag.png"

F_GB  = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
F_G   = "/System/Library/Fonts/Supplemental/Georgia.ttf"
F_GI  = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
F_AB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_ABK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

W, H = 600, 900
HT_BLUE = (0, 32, 159)
HT_RED  = (210, 16, 52)
GOLD    = (255, 200, 50)
CREAM   = (255, 248, 220)

random.seed(42)

def fnt(path, size):
    return ImageFont.truetype(path, size)

# ── Volume title data ─────────────────────────────────────────────────────────
TI_PRIZ_TITLES = [
    "Fizik Elektrik Fondamantal",
    "Sikit & Komponan Elektronik",
    "Pwoduksyon Termik & Nikleye",
    "Pwoduksyon Idwolik & Maremotris",
    "Pwoduksyon Solè & Eolyen",
    "Rezo & Distribisyon I",
    "Distribisyon & Rezo Elektrik",
    "Enstalasyon Elektrik",
    "Chale & Rezistans Aplike",
    "Mote & Machin Elektrik",
    "Elektronik Aplike & Envertè",
    "Sistèm Entelijan I",
    "Otomatizasyon & Sistèm Entèlijan",
    "Sekirite, Nòm & Pwojè Final",
]

DLO_TITLES = [
    "Fizik Dlo & Idwoloji Fondamantal",
    "Materyel & Zouti Plonbri",
    "Distribisyon Dlo Potab",
    "Evakiyasyon EU & EP",
    "Aparèy Sanite & Saldeben",
    "Plonbri Komèsyal & Endistriyèl",
    "Gaz GPL & Gaz Natirèl",
    "Chofaj & Klimatizasyon HVAC",
    "Ponpe & Sistèm Presyon Avanse",
    "Plonbri Rezidansyèl — Pwojè Konplè",
    "Nòm, Sekirite & Karyè",
    "Pisin, Spa, Fonten & Solèy",
]

DIJITAL_TITLES = [
    "Fizik Elektwonik & Sikit Fondamantal",
    "Komponan Elektwonik",
    "Zouti Tekniyen Pwofesyonèl",
    "Soudure & Reparasyon PCB",
    "Sistèm Odyo Fondamantal",
    "Sono & Live Sound",
    "Estèreo Machin Pwofesyonèl",
    "Emettè FM/AM & Antèn",
    "STL & Chèn Broadcast",
    "Processè Odyo Broadcast",
    "Rezo, Routeur & WiFi/IP",
    "Radyo Kominikasyon VHF/UHF",
    "CONATEL — Règleman & Lisans",
    "Telefòn Selilè & Reparasyon",
    "Televizyon LED / LCD / OLED",
    "Aparèy Menajè I",
    "Aparèy Menajè II & Fou",
    "Klimatizasyon HVAC",
    "Konputè & Laptop",
    "OS & Lojisyèl",
    "Elektwonik Otomobil — ECU/OBD",
    "Estèreo & Multimedia Machin",
    "IoT & Otomatizasyon",
    "Estasyon FM & DAB",
    "Nòm, Sekirite & Etik",
    "Shop Elektwonik & Karyè",
]

KOUPE_TITLES = [
    "Zouti & Sekirite Atelye",
    "Bwa — Tip, Kalite & Chwa",
    "Mezirman, Tras & Plan",
    "Koupe, Rabote & Fòme Bwa",
    "Asanblaj & Jwentaj",
    "Kloure, Vis & Koneksyon",
    "Kabinetri & Mèb",
    "Charpant & Estrikti",
    "Fini, Vèni & Penti",
    "Pòt, Fenèt & Eskalye",
    "Ekipman Elektrik Chapant",
    "Pwojè Final & Karyè",
]

TIWEL_TITLES = [
    "Materyel & Zouti Macon",
    "Motye & Beton",
    "Fòmasyon Blòk & Briks",
    "Fondasyon & Espasман",
    "Masonri Dekoratif",
    "Krepi & Andui",
    "Plas & Sòl Tèren",
    "Espas Eksteryè & Drènaj",
    "Repè Estrikti & Nivo",
    "Nòm Konstriksyon Ayiti",
    "Travay Antisisismik",
    "Pwojè Final & Karyè",
]

LEGAL_VOLS = [
    ("Konstitisyon\nAyiti",  "cover_konstitisyon.png", "Lwa Fondamantal Nasyon an"),
    ("Kòd Sivil",            "kòd sivil/cover.png",    "Relasyon & Kontrak Sivil"),
    ("Kòd Penal",            "kòd penal/cover.png",    "Krim, Ofans & Sanksyon"),
    ("Kòd Travay",           "kòd travay/cover.png",   "Dwa ak Obligasyon Travayè"),
    ("Kòd Komès",            "kòd komès/cover.png",    "Komès, Biznis & Kontra"),
    ("Kòd Dwanye",           "kòd dwanye/cover.png",   "Règleman Fwontyè & Enpòtasyon"),
]

# ── Shared helpers ────────────────────────────────────────────────────────────
def vgrad(draw, top, bot, w=W, h=H):
    for y in range(h):
        t = y / h
        draw.line([(0,y),(w,y)], fill=(
            int(top[0]+(bot[0]-top[0])*t),
            int(top[1]+(bot[1]-top[1])*t),
            int(top[2]+(bot[2]-top[2])*t)))

def centered(draw, text, f, y, fill, shadow=None):
    if shadow:
        draw.text((W//2+2, y+2), text, font=f, fill=shadow, anchor="mm")
    draw.text((W//2, y), text, font=f, fill=fill, anchor="mm")

def wrapped_centered(draw, text, f, cx, y, max_w, fill, line_gap=8):
    """Word-wrap text and draw centered. Returns y after last line."""
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        bb = draw.textbbox((0,0), test, font=f)
        if bb[2]-bb[0] > max_w and cur:
            lines.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(" ".join(cur))
    for line in lines:
        draw.text((cx, y), line, font=f, fill=fill, anchor="mm")
        bb = draw.textbbox((0,0), line, font=f)
        y += (bb[3]-bb[1]) + line_gap
    return y

def title_font_size(text):
    n = len(text)
    if n <= 18: return 36
    if n <= 28: return 30
    if n <= 38: return 25
    return 21

def header_band(draw, series_label, vol_str, accent):
    draw.rectangle([0, 0, W, 68], fill=accent)
    draw.text((W//2, 22), series_label, font=fnt(F_AB, 17), fill=CREAM, anchor="mm")
    draw.text((W//2, 48), vol_str,      font=fnt(F_AB, 15), fill=GOLD,  anchor="mm")

def footer_band(draw, tag_line, foot_color):
    draw.rectangle([0, H-68, W, H], fill=foot_color)
    draw.text((W//2, H-44), "LavimiyòLLC · Bibliyotèk Nasyonal",
              font=fnt(F_AB, 14), fill=GOLD, anchor="mm")
    draw.text((W//2, H-21), tag_line,
              font=fnt(F_GI, 12), fill=(200,220,255), anchor="mm")

def border(draw, c=GOLD):
    draw.rectangle([3,3,W-4,H-4], outline=(*c,150), width=2)
    draw.rectangle([8,8,W-9,H-9], outline=(255,255,255,25), width=1)

def title_block(draw, vol_title, series_name, y_start, title_color=CREAM, sub_color=(160,200,255)):
    """Draw the vol title + series name below graphic. Returns final y."""
    sz = title_font_size(vol_title)
    y = wrapped_centered(draw, vol_title, fnt(F_GB, sz),
                         W//2, y_start, W-60, title_color, line_gap=10)
    y += 10
    draw.line([(70, y),(W-70, y)], fill=(255,255,255,40), width=1)
    y += 16
    draw.text((W//2, y), series_name, font=fnt(F_GI, 17), fill=sub_color, anchor="mm")
    return y

# ═══════════════════════════════════════════════════════════════════════════════
#  TI PRIZ
# ═══════════════════════════════════════════════════════════════════════════════
def draw_ti_priz(vol, n_vols, title, out_path):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (4,8,35), (2,4,18))

    # Hex grid
    hex_r = 28
    for row in range(-1, H//(hex_r*2)+2):
        for col in range(-1, W//(hex_r*2)+2):
            cx = col*hex_r*2 + (row%2)*hex_r
            cy = row*hex_r*2
            for i in range(6):
                a1 = math.radians(60*i+30); a2 = math.radians(60*(i+1)+30)
                draw.line([(cx+hex_r*math.cos(a1), cy+hex_r*math.sin(a1)),
                           (cx+hex_r*math.cos(a2), cy+hex_r*math.sin(a2))],
                          fill=(60,50,0), width=1)

    # Glow
    glow = Image.new("RGB", (W,H), (0,0,0))
    gd   = ImageDraw.Draw(glow)
    for r in range(170,0,-10):
        a = int(55*(1-r/170))
        gd.ellipse([W//2-r,250-r,W//2+r,250+r], fill=(a*3,a*2,0))
    img = Image.blend(img, glow, 0.55)
    draw = ImageDraw.Draw(img)

    # Lightning bolt
    lx, ly = W//2, 110
    bolt = [(lx+20,ly),(lx-10,ly+115),(lx+30,ly+115),
            (lx-30,ly+255),(lx-5,ly+155),(lx-35,ly+155),(lx+20,ly)]
    draw.polygon([(x+5,y+5) for x,y in bolt], fill=(60,40,0))
    for exp,ec in [(8,(170,115,0)),(5,(215,165,0)),(3,(255,215,45))]:
        pts = [(x+exp*math.cos(math.radians(45)),y+exp*math.sin(math.radians(45))) for x,y in bolt]
        try: draw.polygon(pts, fill=ec)
        except: pass
    draw.polygon(bolt, fill=(255,232,45))
    draw.polygon(bolt, outline=(255,255,200), width=2)

    # Sparks
    for ang in range(0,360,28):
        rad=math.radians(ang); r1=random.randint(85,115); r2=r1+random.randint(10,28)
        draw.line([(W//2+r1*math.cos(rad),260+r1*math.sin(rad)),
                   (W//2+r2*math.cos(rad),260+r2*math.sin(rad))], fill=(255,215,70), width=1)

    header_band(draw, "⚡ TI PRIZ · Elektrisite ak Plonbri",
                f"Volim {vol:02d} / {n_vols:02d}", (18,12,75))

    y_title = 395
    centered(draw, f"VOL. {vol}", fnt(F_AB,16), y_title, fill=(*GOLD,210))
    y_title += 28
    y_after = title_block(draw, title, "TI PRIZ", y_title,
                          title_color=(255,232,45), sub_color=(180,200,255))

    footer_band(draw, "Atelye Pratik an Kreyòl · 2026", (18,12,75))
    border(draw, GOLD)
    img.save(out_path, "PNG", dpi=(150,150))

# ═══════════════════════════════════════════════════════════════════════════════
#  DLO
# ═══════════════════════════════════════════════════════════════════════════════
def draw_dlo(vol, n_vols, title, out_path):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (0,20,60), (0,8,30))

    # Waves
    for band in range(6):
        by=330+band*60; amp=18+band*4; spd=0.018+band*0.003
        pts=[(x, by+int(amp*math.sin(spd*x+band*0.8))) for x in range(0,W+1,3)]
        draw.polygon(pts+[(W,H),(0,H)], fill=(0,75+band*12,130+band*8))
        for i in range(len(pts)-1):
            draw.line([pts[i],pts[i+1]], fill=(0,170+band*8,210), width=2)

    # Droplet
    dcx,dcy,dr=W//2,200,85
    draw.ellipse([dcx-dr,dcy-dr,dcx+dr,dcy+dr], fill=(0,95,175), outline=(0,195,240),width=3)
    draw.polygon([(dcx,dcy-dr-55),(dcx-38,dcy-dr+8),(dcx+38,dcy-dr+8)], fill=(0,95,175))
    draw.line([(dcx-38,dcy-dr+8),(dcx,dcy-dr-55)], fill=(0,195,240),width=3)
    draw.line([(dcx+38,dcy-dr+8),(dcx,dcy-dr-55)], fill=(0,195,240),width=3)
    draw.ellipse([dcx-dr//3,dcy-dr//2,dcx-dr//3+dr//3,dcy-dr//2+dr//4], fill=(170,225,255))

    # Bubbles
    random.seed(vol*5+3)
    for _ in range(10):
        bx=random.randint(30,W-30); by=random.randint(80,310); br=random.randint(5,16)
        draw.ellipse([bx-br,by-br,bx+br,by+br], outline=(0,195,235,0), width=2)
        draw.ellipse([bx-br+3,by-br+3,bx-br+7,by-br+7], fill=(195,235,255))

    header_band(draw, "💧 DLO · Plonbri ak Jesyon Dlo",
                f"Volim {vol:02d} / {n_vols:02d}", (0,28,95))

    y_title = 320
    centered(draw, f"VOL. {vol}", fnt(F_AB,16), y_title, fill=(*GOLD,210))
    y_title += 28
    title_block(draw, title, "DLO", y_title, title_color=(0,225,255), sub_color=CREAM)

    footer_band(draw, "Atelye Pratik an Kreyòl · 2026", (0,28,95))
    border(draw, (0,195,255))
    img.save(out_path, "PNG", dpi=(150,150))

# ═══════════════════════════════════════════════════════════════════════════════
#  DIJITAL
# ═══════════════════════════════════════════════════════════════════════════════
def draw_dijital(vol, n_vols, title, out_path):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (4,12,8), (1,4,3))

    # Binary rain
    f_sm = fnt(F_AB, 14)
    random.seed(vol*3+7)
    for cx in range(15, W-15, 22):
        bright=random.randint(18,75); n=random.randint(8,26); sy=random.randint(-200,200)
        for j in range(n):
            cy=sy+j*22
            if 0<cy<H:
                a=max(8,bright-j*3)
                draw.text((cx,cy), str(random.randint(0,1)), font=f_sm, fill=(0,min(255,a*2+35),0))

    # Circuit traces
    random.seed(vol*11+1)
    for _ in range(28):
        sx=random.randint(0,W); sy=random.randint(80,H-80)
        lg=random.randint(30,100); horiz=random.random()>0.5
        ex=sx+(lg if horiz else 0); ey=sy+(0 if horiz else lg)
        draw.line([sx,sy,ex,ey], fill=(0,95,38), width=1)
        draw.ellipse([sx-3,sy-3,sx+3,sy+3], fill=(0,150,55))
        draw.ellipse([ex-3,ey-3,ex+3,ey+3], fill=(0,150,55))

    # Monitor
    mx,my,mw,mh=W//2,235,245,160
    draw.rounded_rectangle([mx-mw//2,my-mh//2,mx+mw//2,my+mh//2],
                           radius=12, fill=(8,24,16), outline=(0,175,75), width=3)
    draw.rounded_rectangle([mx-mw//2+8,my-mh//2+8,mx+mw//2-8,my+mh//2-8],
                           radius=8, fill=(0,38,18))
    short_title = title[:22] + ("…" if len(title)>22 else "")
    draw.text((mx-mw//2+16,my-mh//2+16), f">_ {short_title}", font=fnt(F_AB,13), fill=(0,225,95))
    draw.text((mx-mw//2+16,my-mh//2+46), f"   DIJITAL Vol.{vol:02d}", font=fnt(F_AB,13), fill=(0,175,75))
    draw.text((mx-mw//2+16,my-mh//2+76), "   Bibliyotèk Nasyonal", font=fnt(F_AB,12), fill=(0,130,55))
    draw.polygon([(mx-15,my+mh//2),(mx+15,my+mh//2),(mx+28,my+mh//2+24),(mx-28,my+mh//2+24)],
                 fill=(0,55,28), outline=(0,115,55), width=2)
    draw.rectangle([mx-48,my+mh//2+24,mx+48,my+mh//2+30], fill=(0,115,55))

    header_band(draw, "📱 DIJITAL · Sistèm ak Teknoloji",
                f"Volim {vol:02d} / {n_vols:02d}", (5,32,16))

    y_title = my + mh//2 + 50
    centered(draw, f"VOL. {vol}", fnt(F_AB,16), y_title, fill=(*GOLD,210))
    y_title += 28
    title_block(draw, title, "DIJITAL", y_title, title_color=(0,230,95), sub_color=CREAM)

    footer_band(draw, "Atelye Pratik an Kreyòl · 2026", (5,32,16))
    border(draw, (0,195,75))
    img.save(out_path, "PNG", dpi=(150,150))

# ═══════════════════════════════════════════════════════════════════════════════
#  KOUPE KLOURE
# ═══════════════════════════════════════════════════════════════════════════════
def draw_koupe_kloure(vol, n_vols, title, out_path):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (50,20,8), (25,8,2))

    # Wood grain
    random.seed(vol*7+13)
    for y in range(0, H, 6):
        pts=[]; x=0; cy=y
        while x<=W:
            cy+=random.randint(-2,2); pts.append((x,cy)); x+=8
        for i in range(len(pts)-1):
            sh=random.randint(28,68)
            draw.line([pts[i],pts[i+1]], fill=(sh,int(sh*0.45),int(sh*0.18)), width=1)

    # Saw blade
    scx,scy,sr=W//2,230,95
    draw.ellipse([scx-sr,scy-sr,scx+sr,scy+sr], fill=(58,52,48), outline=(195,158,55),width=4)
    for i in range(24):
        a1=math.radians(i*15); a2=math.radians(i*15+6); a3=math.radians(i*15+7.5)
        r1,r2=sr,sr+17
        draw.polygon([(scx+r1*math.cos(a1),scy+r1*math.sin(a1)),
                      (scx+r2*math.cos(a2),scy+r2*math.sin(a2)),
                      (scx+r1*math.cos(a3),scy+r1*math.sin(a3))], fill=(185,145,48))
    ir=sr-18
    draw.ellipse([scx-ir,scy-ir,scx+ir,scy+ir], fill=(28,22,18), outline=(175,135,38),width=3)
    draw.ellipse([scx-11,scy-11,scx+11,scy+11], fill=(10,8,5), outline=(195,158,55),width=2)
    for i in range(8):
        a=math.radians(i*45)
        draw.line([(scx+ir*0.58*math.cos(a),scy+ir*0.58*math.sin(a)),
                   (scx+ir*0.88*math.cos(a),scy+ir*0.88*math.sin(a))], fill=(75,55,18),width=4)

    for nx,ny in [(75,375),(525,375),(75,415),(525,415)]:
        draw.ellipse([nx-6,ny-6,nx+6,ny+6], fill=(155,135,75), outline=(195,175,95),width=2)
        draw.line([nx,ny-6,nx,ny+6], fill=(115,95,48),width=2)
        draw.line([nx-5,ny,nx+5,ny], fill=(115,95,48),width=1)

    header_band(draw, "🪚 KOUPE KLOURE · Chapant & Menuizri",
                f"Volim {vol:02d} / {n_vols:02d}", (68,28,8))

    y_title = 355
    centered(draw, f"VOL. {vol}", fnt(F_AB,16), y_title, fill=(*GOLD,210))
    y_title += 28
    title_block(draw, title, "KOUPE KLOURE", y_title,
                title_color=(255,198,55), sub_color=CREAM)

    footer_band(draw, "Atelye Pratik an Kreyòl · 2026", (68,28,8))
    border(draw, (208,165,58))
    img.save(out_path, "PNG", dpi=(150,150))

# ═══════════════════════════════════════════════════════════════════════════════
#  TIWÈL
# ═══════════════════════════════════════════════════════════════════════════════
def draw_tiwel(vol, n_vols, title, out_path):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (38,32,28), (18,14,12))

    bw,bh,mt=80,32,4
    random.seed(vol*3+5)
    for row in range(-1, 12):
        y0=row*(bh+mt)+80; off=(bw//2 if row%2==1 else 0)
        for col in range(-1, W//bw+2):
            x0=col*(bw+mt)-off; x1=x0+bw; y1=y0+bh
            if y1<420:
                sh=random.randint(-18,18)
                bc=(min(255,158+sh),min(255,65+sh//2),min(255,36+sh//3))
                draw.rectangle([x0,y0,x1,y1], fill=bc)
                draw.line([x0,y0,x1,y0], fill=(78,70,62),width=mt)
                draw.line([x0,y0,x0,y1], fill=(78,70,62),width=mt)
                if random.random()>0.6:
                    draw.rectangle([x0+5,y0+5,x0+24,y0+9], fill=(min(255,bc[0]+18),bc[1],bc[2]))

    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    od=ImageDraw.Draw(overlay)
    for y in range(220,420):
        t=(y-220)/200
        od.line([(0,y),(W,y)], fill=(0,0,0,int(145*t)))
    img=Image.alpha_composite(img.convert("RGBA"),overlay).convert("RGB")
    draw=ImageDraw.Draw(img)

    tx,ty=W//2,335
    draw.polygon([(tx-8,ty+20),(tx+8,ty+20),(tx+5,ty+90),(tx-5,ty+90)],
                 fill=(118,78,38), outline=(158,108,58),width=2)
    draw.polygon([(tx-50,ty),(tx+50,ty),(tx+30,ty+25),(tx-30,ty+25)],
                 fill=(158,148,138), outline=(198,193,188),width=2)
    draw.rounded_rectangle([tx-7,ty+68,tx+7,ty+98], radius=4,
                            fill=(88,52,22), outline=(128,88,48),width=2)

    header_band(draw, "🧱 TIWÈL · Masonri ak Konstriksyon",
                f"Volim {vol:02d} / {n_vols:02d}", (78,38,26))

    y_title = 445
    centered(draw, f"VOL. {vol}", fnt(F_AB,16), y_title, fill=(*GOLD,210))
    y_title += 28
    title_block(draw, title, "TIWÈL", y_title,
                title_color=(228,178,98), sub_color=CREAM)

    footer_band(draw, "Atelye Pratik an Kreyòl · 2026", (78,38,26))
    border(draw, (218,168,78))
    img.save(out_path, "PNG", dpi=(150,150))

# ═══════════════════════════════════════════════════════════════════════════════
#  LEGAL
# ═══════════════════════════════════════════════════════════════════════════════
def paste_real_flag(img, cx, cy, fw, fh):
    img = img.convert("RGBA")
    flag = Image.open(FLAG_HT).convert("RGBA").resize((fw, fh), Image.LANCZOS)
    x0, y0 = cx-fw//2, cy-fh//2
    sh = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(sh).rectangle([x0+5,y0+5,x0+fw+5,y0+fh+5], fill=(0,0,0,100))
    img = Image.alpha_composite(img, sh)
    img.paste(flag, (x0,y0), flag)
    ImageDraw.Draw(img).rectangle([x0-2,y0-2,x0+fw+2,y0+fh+2], outline=(*GOLD,200), width=2)
    return img.convert("RGB")

def draw_scales(draw, cx, cy, size):
    arm=size
    draw.polygon([(cx-8,cy+arm//2),(cx+8,cy+arm//2),(cx+3,cy-arm//4),(cx-3,cy-arm//4)],
                 fill=(175,145,48), outline=GOLD, width=1)
    draw.rectangle([cx-arm//2,cy+arm//2,cx+arm//2,cy+arm//2+8], fill=(158,128,38), outline=GOLD,width=1)
    draw.line([cx-arm,cy-arm//6,cx+arm,cy-arm//6], fill=GOLD, width=3)
    draw.ellipse([cx-6,cy-arm//6-6,cx+6,cy-arm//6+6], fill=GOLD)
    for side in [-1, 1]:
        px=cx+side*arm; py=cy-arm//6
        off=0 if side==1 else 8
        draw.line([px,py,px-arm//3,py+arm//2-off], fill=GOLD,width=2)
        draw.line([px,py,px+arm//3,py+arm//2-off], fill=GOLD,width=2)
        draw.ellipse([px-arm//3,py+arm//2-off,px+arm//3,py+arm//2-off+arm//5],
                     fill=(28,22,14), outline=GOLD,width=2)

def draw_columns(draw, count=4, col_w=22, col_h=155, y_base=415):
    sp=W//(count+1)
    for i in range(count):
        cx=sp*(i+1)
        draw.rectangle([cx-col_w//2,y_base-col_h,cx+col_w//2,y_base], fill=(28,26,18), outline=(78,68,28),width=1)
        for fl in range(-3,4):
            draw.line([cx+fl*4,y_base-col_h+4,cx+fl*4,y_base-4], fill=(48,43,28),width=1)
        draw.rectangle([cx-col_w//2-5,y_base-col_h-10,cx+col_w//2+5,y_base-col_h], fill=(58,53,33),outline=(98,83,33),width=1)
        draw.rectangle([cx-col_w//2-5,y_base,cx+col_w//2+5,y_base+8], fill=(58,53,33),outline=(98,83,33),width=1)
    draw.rectangle([sp-col_w//2-5,y_base-col_h-22,sp*count+col_w//2+5,y_base-col_h-10],
                   fill=(53,48,28), outline=(98,83,33),width=1)

def draw_legal_cover(title, subtitle, out_path, vol_num):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    vgrad(draw, (8,16,42), (3,7,22))
    for x in range(-H, W, 35):
        draw.line([(x,0),(x+H,H)], fill=(20,28,58),width=1)
    draw_columns(draw)

    img = paste_real_flag(img, W//2, 118, 240, 144)
    draw = ImageDraw.Draw(img)

    arch_cx,arch_cy=W//2,338
    pts=[(arch_cx+108*math.cos(math.radians(a)),arch_cy+108*math.sin(math.radians(a))) for a in range(200,341,3)]
    for i in range(len(pts)-1):
        draw.line([pts[i],pts[i+1]], fill=(175,145,38),width=2)

    draw_scales(draw, W//2, arch_cy+12, 73)

    for sx in range(W//2-80, W//2+81, 40):
        draw.text((sx,455), "★", font=fnt(F_GB,15), fill=GOLD, anchor="mm")

    draw.line([(48,485),(W-48,485)], fill=(*GOLD,100),width=1)

    ty=504
    for part in title.split("\n"):
        sz=42 if len(part)<=12 else 34 if len(part)<=18 else 28
        draw.text((W//2,ty+2), part, font=fnt(F_GB,sz), fill=(0,0,0), anchor="mm")
        draw.text((W//2,ty), part, font=fnt(F_GB,sz), fill=CREAM, anchor="mm")
        ty+=sz+10
    ty+=6
    draw.text((W//2,ty), subtitle, font=fnt(F_GI,19), fill=(158,198,255), anchor="mm")
    ty+=34

    bb=draw.textbbox((W//2,ty+20), f"  Vol. {vol_num}  ", font=fnt(F_AB,16), anchor="mm")
    draw.rounded_rectangle([bb[0]-8,bb[1]-4,bb[2]+8,bb[3]+4], radius=6, fill=(175,138,28))
    draw.text((W//2,ty+20), f"  Vol. {vol_num}  ", font=fnt(F_AB,16), fill=(0,0,0), anchor="mm")

    draw.rectangle([0,H-68,W,H], fill=(10,20,55))
    draw.text((W//2,H-44), "LavimiyòLLC · Bibliyotèk Nasyonal", font=fnt(F_AB,14), fill=GOLD, anchor="mm")
    draw.text((W//2,H-21), "Kòd ak Lwa Ayisyen an Kreyòl · 2026", font=fnt(F_GI,12), fill=(160,198,255), anchor="mm")
    border(draw, GOLD)
    img.save(out_path, "PNG", dpi=(150,150))
    print(f"  ✓ LEGAL Vol {vol_num}: {os.path.basename(out_path)}")

# ═══════════════════════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════════════════════
import unicodedata
def nfd(s): return unicodedata.normalize("NFD", s)

BATCH = [
    ("TI PRIZ",       TI_PRIZ_TITLES, draw_ti_priz),
    ("DLO",           DLO_TITLES,     draw_dlo),
    ("DIJITAL",       DIJITAL_TITLES, draw_dijital),
    ("KOUPE KLOURE",  KOUPE_TITLES,   draw_koupe_kloure),
]

for series_name, titles, fn in BATCH:
    covers_dir = os.path.join(BASE, "TEKNIK", series_name, "covers")
    os.makedirs(covers_dir, exist_ok=True)
    for i, title in enumerate(titles, 1):
        fn(i, len(titles), title, os.path.join(covers_dir, f"vol{i:02d}.png"))
    print(f"✓ {series_name}: {len(titles)} covers")

# TIWÈL (NFD path)
tiwel_dir = os.path.join(BASE, "TEKNIK", nfd("TIWÈL"), "covers")
os.makedirs(tiwel_dir, exist_ok=True)
for i, title in enumerate(TIWEL_TITLES, 1):
    draw_tiwel(i, len(TIWEL_TITLES), title, os.path.join(tiwel_dir, f"vol{i:02d}.png"))
print(f"✓ TIWÈL: {len(TIWEL_TITLES)} covers")

# LEGAL
for i, (title, rel_path, subtitle) in enumerate(LEGAL_VOLS, 1):
    full_path = os.path.join(LEGAL, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    draw_legal_cover(title, subtitle, full_path, i)
print("✓ LEGAL: 6 covers")

print("\nDone.")

"""Claret Atelier Theme - icon candidates.

Code-drawn candidates (no AI images), a light/dark contact sheet and an inline
strip. Re-runnable: every mark is redrawn from scratch.

Run from the project root:  py -3 scripts/generate-icon-candidates.py
"""

import io
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 3
W = 1024

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "logo-candidates")

# palette - winter: navy + ice blue + snow (de-collided from
# oceanic-scale / sapphire-tide / soft-sky / cloudy-canvas / apricot-glow)
NAVY = (26, 46, 68, 255)              # #1A2E44  deep navy
NAVY_D = (18, 32, 48, 255)            # #122030  midnight navy
BLUE = (63, 107, 166, 255)            # #3F6BA6  signal blue
ICE = (217, 234, 253, 255)            # #D9EAFD  pale ice
ICE_D = (182, 196, 214, 255)          # #B6C4D6  steel ice
PERI = (157, 165, 214, 255)           # #9DA5D6  periwinkle
SNOW = (248, 250, 252, 255)           # #F8FAFC  snow white
SNOW_D = (232, 238, 246, 255)         # #E8EEF6  shaded snow
SAND = (227, 217, 198, 255)           # #E3D9C6  driftwood sand
INK = NAVY_D

# No-outline render (flat look used across the set).
OUTLINE = None

# contact sheet backgrounds: a mid ice blue so snow-white, ice and navy
# marks all separate from the sheet
LIGHT_BG = (198, 212, 230, 255)
DARK_BG = (18, 32, 48, 255)
LIGHT_INK = (26, 46, 68, 255)
DARK_INK = (232, 238, 246, 255)

FONT_DIR = r"C:\Windows\Fonts"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


def scr(p):
    return (p[0] * S, p[1] * S)


def wd(v):
    return max(1, int(round(v * S)))


def canvas():
    return Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))


def finish(img):
    return img.resize((W, W), Image.LANCZOS)


def bez(p0, p1, p2, n=64):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1.0 - t
        pts.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return pts


def poly(draw, pts, fill, outline=None, width=0):
    draw.polygon([scr(p) for p in pts], fill=fill,
                 outline=outline, width=wd(width) if width else 0)


def disc(draw, center, r, fill, outline=None, width=0):
    draw.ellipse([center[0] * S - r * S, center[1] * S - r * S,
                  center[0] * S + r * S, center[1] * S + r * S],
                 fill=fill, outline=outline, width=wd(width) if width else 0)


def rrect(draw, box, radius, fill, outline=None, width=0):
    draw.rounded_rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                           radius=radius * S, fill=fill, outline=outline,
                           width=wd(width) if width else 0)


def line(draw, pts, color, width, joint="curve"):
    draw.line([scr(p) for p in pts], fill=color, width=wd(width), joint=joint)


# ---------------------------------------------------------------- candidates

def cand_snowcap():
    """01 - a peak with a snow cap."""
    img = canvas()
    d = ImageDraw.Draw(img)

    # back peak
    poly(d, [(214, 566), (392, 860), (96, 860)], ICE_D)
    # main peak
    poly(d, [(512, 168), (846, 860), (178, 860)], NAVY)

    # jagged snow cap
    poly(d, [(512, 168), (648, 424), (588, 396), (524, 444),
             (462, 398), (378, 424)], SNOW)

    # ground drift
    rrect(d, (110, 860, 914, 916), 26, ICE_D)

    return finish(img)


def cand_snowline():
    """02 - the snow line itself: a bright band cutting two peaks."""
    img = canvas()
    d = ImageDraw.Draw(img)

    # the snow line runs behind the peaks
    rrect(d, (90, 690, 934, 750), 16, SNOW)

    # back peak
    poly(d, [(300, 400), (520, 690), (128, 690)], BLUE)
    # main peak
    poly(d, [(566, 276), (848, 690), (356, 690)], NAVY)
    # snow on the main peak
    poly(d, [(566, 276), (698, 470), (646, 446), (596, 482), (546, 448),
             (468, 470)], SNOW)

    # drifting snow under the line
    rrect(d, (150, 786, 874, 824), 18, ICE_D)

    return finish(img)


def cand_crystal():
    """03 - a six-point ice crystal."""
    img = canvas()
    d = ImageDraw.Draw(img)

    cx, cy = 512, 512
    for i in range(6):
        a = math.radians(i * 60)
        ex = cx + 330 * math.cos(a)
        ey = cy + 330 * math.sin(a)
        line(d, [(cx, cy), (ex, ey)], BLUE, 30)

        # barbs
        for f, length in ((0.55, 120), (0.8, 90)):
            bx = cx + 330 * f * math.cos(a)
            by = cy + 330 * f * math.sin(a)
            for s in (-1, 1):
                b = math.radians(i * 60 + s * 40)
                line(d, [(bx, by), (bx + length * math.cos(b), by + length * math.sin(b))],
                     BLUE, 22)

    disc(d, (cx, cy), 86, SNOW)
    disc(d, (cx, cy), 40, ICE)

    return finish(img)


def cand_pine():
    """04 - a frosted conifer."""
    img = canvas()
    d = ImageDraw.Draw(img)

    # trunk
    rrect(d, (486, 700, 538, 864), 10, NAVY_D)

    # stepped canopy: (half width, base y, apex y)
    tiers = [(210, 742, 496), (160, 566, 330), (108, 402, 198)]
    for half, base, apex in tiers:
        poly(d, [(512 - half, base), (512 + half, base), (512, apex)], NAVY)

    # snow sitting on each tier
    for half, base, apex in tiers:
        h = base - apex
        poly(d, [(512 - half * 0.55, base - h * 0.35),
                 (512 + half * 0.55, base - h * 0.35),
                 (512, apex)], SNOW)

    # ground drift
    rrect(d, (250, 860, 774, 916), 26, ICE_D)

    return finish(img)


def cand_drift():
    """05 - three snowdrifts layered front to back."""
    img = canvas()
    d = ImageDraw.Draw(img)

    def drift(x0, x1, base, crest_x, peak, color):
        top = bez((x0, base), (crest_x, peak), (x1, base))
        poly(d, top + [(x1, base), (x0, base)], color)

    drift(90, 934, 780, 320, 470, (168, 188, 214, 255))
    top = bez((90, 780), (320, 470), (560, 610))
    line(d, top, NAVY, 16)

    # mid drift with a lone pine on its crest
    drift(90, 934, 872, 660, 604, (201, 217, 236, 255))
    poly(d, [(668, 682), (728, 682), (698, 598)], NAVY)

    # near drift
    drift(90, 934, 944, 400, 786, (230, 238, 247, 255))

    return finish(img)


def cand_ridge():
    """06 - layered ridges receding into the snow."""
    img = canvas()
    d = ImageDraw.Draw(img)

    # far ridge
    poly(d, [(90, 720), (300, 470), (520, 720)], PERI)
    # snow on the far ridge
    poly(d, [(266, 508), (334, 508), (300, 470)], SNOW)
    # mid ridge
    poly(d, [(230, 790), (486, 520), (760, 790)], BLUE)
    # snow on the mid ridge
    poly(d, [(452, 558), (520, 558), (486, 520)], SNOW)
    # near ridge
    poly(d, [(400, 860), (640, 610), (900, 860)], NAVY)
    # snow on the near ridge
    poly(d, [(596, 682), (684, 682), (640, 610)], SNOW)

    # snow floor
    rrect(d, (90, 852, 934, 906), 18, SNOW_D)

    return finish(img)


CANDIDATES = [
    ("01", "snowcap", cand_snowcap),
    ("02", "snowline", cand_snowline),
    ("03", "crystal", cand_crystal),
    ("04", "frosted-pine", cand_pine),
    ("05", "drift", cand_drift),
    ("06", "ridge", cand_ridge),
]


# ---------------------------------------------------------------- sheet bits

def centered_text(d, center, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    x = center[0] - (b[2] - b[0]) / 2 - b[0]
    y = center[1] - (b[3] - b[1]) / 2 - b[1]
    d.text((x, y), text, font=fnt, fill=fill)


def contact_sheet(icons, bg, ink, path):
    cell_w, cell_h = 420, 540
    margin, gap = 40, 26
    head = 118
    sheet_w = margin * 2 + cell_w * 3 + gap * 2
    sheet_h = margin + head + cell_h * 2 + gap + margin

    sheet = Image.new("RGBA", (sheet_w, sheet_h), bg)
    d = ImageDraw.Draw(sheet)

    f_title = font("segoeuib.ttf", 40)
    f_num = font("segoeuib.ttf", 30)
    f_name = font("segoeui.ttf", 26)
    f_small = font("segoeui.ttf", 20)

    centered_text(d, (sheet_w / 2, margin + 34), "SNOWLINE THEME", f_title, ink)
    centered_text(d, (sheet_w / 2, margin + 82), "icon candidates", f_small, ink)

    for idx, (num, name, icon) in enumerate(icons):
        row, col = divmod(idx, 3)
        gx = margin + col * (cell_w + gap)
        gy = margin + head + row * (cell_h + gap)

        sheet.alpha_composite(icon.resize((260, 260), Image.LANCZOS),
                              (gx + (cell_w - 260) // 2, gy + 30))

        centered_text(d, (gx + cell_w / 2, gy + 330), num, f_num, ink)
        centered_text(d, (gx + cell_w / 2, gy + 372), name, f_name, ink)
        centered_text(d, (gx + cell_w / 2, gy + 404), "1024 x 1024  PNG", f_small, ink)

        thumb = icon.resize((32, 32), Image.LANCZOS)
        tx, ty = gx + cell_w - 32 - 22, gy + cell_h - 32 - 22
        d.rectangle([tx - 10, ty - 10, tx + 42, ty + 42],
                    outline=(ink[0], ink[1], ink[2], 70), width=1)
        sheet.alpha_composite(thumb, (tx, ty))

    save_png(sheet.convert("RGB"), path)


def inline_strip(icons, path):
    size, gap, margin = 150, 18, 30
    strip_w = margin * 2 + size * len(icons) + gap * (len(icons) - 1)
    strip_h = margin * 2 + size + 34
    strip = Image.new("RGBA", (strip_w, strip_h), LIGHT_BG)
    d = ImageDraw.Draw(strip)
    f_num = font("segoeuib.ttf", 20)

    for idx, (num, _name, icon) in enumerate(icons):
        x = margin + idx * (size + gap)
        strip.alpha_composite(icon.resize((size, size), Image.LANCZOS), (x, margin))
        centered_text(d, (x + size / 2, margin + size + 16), num, f_num, LIGHT_INK)

    save_png(strip.convert("RGB"), path)


def save_png(img, path):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def main():
    os.makedirs(OUT, exist_ok=True)

    icons = []
    for num, name, fn in CANDIDATES:
        icon = fn()
        box = icon.getbbox()
        if box is None:
            raise AssertionError("%s rendered empty" % name)
        left, top, right, bottom = box
        lo, hi = 70, 954
        if left < lo or top < lo or right > hi or bottom > hi:
            raise AssertionError("%s out of safe area: %s" % (name, box))
        path = os.path.join(OUT, "%s-%s.png" % (num, name))
        save_png(icon, path)
        print("wrote", os.path.relpath(path, ROOT), box)
        icons.append((num, name, icon))

    contact_sheet(icons, LIGHT_BG, LIGHT_INK, os.path.join(OUT, "contact-light.png"))
    contact_sheet(icons, DARK_BG, DARK_INK, os.path.join(OUT, "contact-dark.png"))
    inline_strip(icons, os.path.join(OUT, "inline-strip.png"))
    print("wrote contact-light.png / contact-dark.png / inline-strip.png")


if __name__ == "__main__":
    main()

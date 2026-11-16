# -*- coding: utf-8 -*-
"""Render the README banner (icon + wordmark + one colour card per cut).

    py -3 scripts/generate-banner.py

Output:
    docs/banner.png  light banner (snow paper) with a LIGHT and a DARK colour card
"""

import importlib.util
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "docs", "banner.png")

S = 2
W, H = 1600, 420

SNOW = (244, 248, 251, 255)
BORDER = (214, 226, 236, 255)
INK = (23, 41, 61, 255)
MUTED = (104, 124, 142, 255)
RING = (193, 208, 220, 255)

# one colour card per cut: the accent of each variant
CARDS = [
    ("LIGHT", [
        (53, 96, 154, 255),    # glacier
        (124, 130, 102, 255),   # tundra
        (137, 138, 196, 255),   # frostbell
        (151, 163, 176, 255),   # icefall
    ]),
    ("DARK", [
        (148, 180, 193, 255),   # fjord
        (49, 151, 152, 255),    # frostpine
        (23, 41, 61, 255),      # midnight navy
        (248, 250, 252, 255),   # snow
    ]),
]

FONT_DIR = r"C:\Windows\Fonts"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


def load_candidates():
    spec = importlib.util.spec_from_file_location(
        "cands", os.path.join(HERE, "generate-icon-candidates.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    cands = load_candidates()
    icon = [c for c in cands.CANDIDATES if c[0] == "01"][0][2]()
    icon = icon.resize((300 * S, 300 * S), Image.LANCZOS)

    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W * S - 1, H * S - 1], radius=28 * S,
                        fill=SNOW, outline=BORDER, width=2 * S)

    img.alpha_composite(icon, (78 * S, 60 * S))

    f_title = font("segoeuib.ttf", 74 * S)
    f_tag = font("segoeui.ttf", 30 * S)
    f_label = font("segoeuib.ttf", 22 * S)

    tx = 424 * S
    d.text((tx, 84 * S), "Snowline Theme", font=f_title, fill=INK)
    d.text((tx, 172 * S), "one snow line, six winter cuts",
           font=f_tag, fill=MUTED)

    for row, (label, colors) in enumerate(CARDS):
        y = 238 * S + row * 58 * S
        d.text((tx, y + 4 * S), label, font=f_label, fill=MUTED)
        x = tx + 128 * S
        for col in colors:
            d.ellipse([x, y, x + 26 * S, y + 26 * S], fill=col,
                      outline=RING, width=2 * S)
            x += 40 * S

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(OUT)
    print("wrote", os.path.relpath(OUT, BASE))


if __name__ == "__main__":
    main()

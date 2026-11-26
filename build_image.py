#!/usr/bin/env python3
"""Draw the front-page image for news-image-20261125.

A newspaper front page summing up the world news of Wednesday
25 November 2026: a big lead panel (burning tankers in the Strait
of Hormuz) over a grid of smaller story panels, plus a world-in-brief
panel. All facts come from the verified news list in the prose spec.
Drawn with Pillow only; run: python3 build_image.py
Writes entry.png (1024x1024) next to this script.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (10, 26, 51)
NAVY2 = (16, 42, 80)
ORANGE = (255, 140, 40)
AMBER = (255, 190, 70)
CREAM = (244, 238, 224)
INK = (20, 24, 34)
WHITE = (255, 255, 255)
DARK = (8, 12, 22)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def flame(draw, cx, base_y, w, h, seed=0):
    """Layered flame tongues rising from (cx, base_y)."""
    rnd = random.Random(seed)
    for layer, (col, scale) in enumerate(
        [((255, 90, 0), 1.0), ((255, 160, 30), 0.72), ((255, 220, 90), 0.45)]
    ):
        fw = w * scale
        fh = h * scale
        for k in range(3):
            off = rnd.uniform(-fw * 0.28, fw * 0.28)
            x0 = cx + off - fw / 2
            x1 = cx + off + fw / 2
            y0 = base_y - fh * rnd.uniform(0.85, 1.0)
            draw.ellipse([x0, y0, x1, base_y], fill=col)
            draw.polygon(
                [(cx + off - fw * 0.35, base_y - fh * 0.55),
                 (cx + off, base_y - fh),
                 (cx + off + fw * 0.35, base_y - fh * 0.55)],
                fill=col,
            )


def smoke(draw, cx, top_y, base_y, seed=0):
    """Rising black smoke column from base_y up to top_y."""
    rnd = random.Random(seed)
    n = 5
    for i in range(n):
        t = i / (n - 1)
        y = base_y - (base_y - top_y) * t
        r = 10 + t * 20
        drift = math.sin(t * 3.0 + seed) * 12 - t * 26
        col = (28 + int(t * 22), 26 + int(t * 20), 26 + int(t * 20))
        draw.ellipse([cx + drift - r, y - r, cx + drift + r, y + r], fill=col)


def tanker(draw, x, y, scale, hull_col, seed=0):
    """A simple oil tanker silhouette at (x, y) = waterline left."""
    w, h = int(300 * scale), int(52 * scale)
    # hull
    draw.polygon([(x, y), (x + w, y), (x + w - 18 * scale, y + h),
                  (x + 8 * scale, y + h)], fill=hull_col)
    draw.rectangle([x, y - 6 * scale, x + w, y + 2], fill=(60, 30, 20))
    # deck + superstructure
    draw.rectangle([x + w * 0.68, y - 34 * scale, x + w * 0.86, y - 6 * scale],
                   fill=(210, 205, 190))
    draw.rectangle([x + w * 0.70, y - 44 * scale, x + w * 0.84, y - 34 * scale],
                   fill=(230, 226, 214))
    # funnel
    draw.rectangle([x + w * 0.12, y - 30 * scale, x + w * 0.22, y - 6 * scale],
                   fill=(180, 40, 30))
    # masts
    draw.line([(x + w * 0.45, y - 26 * scale), (x + w * 0.45, y - 6 * scale)],
              fill=(40, 40, 40), width=3)
    return w


def caption_band(draw, box, headline, sub, head_size=22, sub_size=16):
    """Dark caption strip at the bottom of a panel box."""
    x0, y0, x1, y1 = box
    band_h = 84
    draw.rectangle([x0, y1 - band_h, x1, y1], fill=(8, 14, 26))
    draw.line([(x0, y1 - band_h), (x1, y1 - band_h)], fill=ORANGE, width=3)
    f_h = font(SANS_B, head_size)
    f_s = font(SANS, sub_size)
    # wrap headline to fit
    words = headline.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if f_h.getlength(trial) <= (x1 - x0 - 16):
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    y = y1 - band_h + 7
    for ln in lines[:2]:
        draw.text((x0 + 8, y), ln, font=f_h, fill=WHITE)
        y += head_size + 3
    if sub:
        draw.text((x0 + 8, y1 - 22), sub, font=f_s, fill=AMBER)


def lead_panel(img, draw):
    x0, y0, x1, y1 = 0, 118, 1024, 580
    # dusk sky: dark navy top to burning orange horizon
    vgrad(draw, (x0, y0, x1, 400), (14, 22, 48), (120, 52, 28))
    vgrad(draw, (x0, 400, x1, 440), (150, 66, 26), (235, 120, 30))
    # low sun glow: concentric discs, brightest at the centre
    for r, col in [(95, (200, 90, 32)), (78, (235, 120, 32))]:
        draw.ellipse([512 - r, 428 - r, 512 + r, 428 + r], fill=col)
    draw.ellipse([512 - 62, 428 - 62, 512 + 62, 428 + 62], fill=(255, 220, 130))
    # cliffs left and right
    draw.polygon([(x0, y0 + 180), (150, y0 + 120), (210, y0 + 260),
                  (120, y0 + 340), (x0, y0 + 320)], fill=(18, 20, 34))
    draw.polygon([(x1, y0 + 150), (880, y0 + 110), (830, y0 + 280),
                  (920, y0 + 340), (x1, y0 + 320)], fill=(16, 18, 32))
    # sea
    vgrad(draw, (x0, 440, x1, y1), (30, 32, 52), (10, 14, 28))
    rnd = random.Random(7)
    for _ in range(60):
        rx = rnd.randint(x0 + 10, x1 - 10)
        ry = rnd.randint(446, y1 - 100)
        ln = rnd.randint(14, 60)
        col = (200, 90, 30) if rnd.random() < 0.45 else (70, 80, 110)
        draw.line([(rx, ry), (rx + ln, ry)], fill=col, width=2)
    # far naval vessel silhouette
    draw.polygon([(700, 452), (760, 452), (752, 442), (712, 442)],
                 fill=(12, 14, 24))
    draw.rectangle([726, 430, 736, 442], fill=(12, 14, 24))
    # tanker 1 (left, burning) — sits in the sea strip above the band
    tanker(draw, 90, 452, 0.62, (120, 78, 62), seed=1)
    flame(draw, 170, 448, 56, 95, seed=11)
    flame(draw, 250, 448, 46, 75, seed=12)
    smoke(draw, 170, 190, 430, seed=21)
    smoke(draw, 250, 220, 430, seed=22)
    # tanker 2 (right, burning)
    tanker(draw, 590, 456, 0.58, (110, 72, 58), seed=2)
    flame(draw, 660, 452, 52, 85, seed=13)
    flame(draw, 740, 452, 42, 65, seed=14)
    smoke(draw, 660, 205, 434, seed=23)
    smoke(draw, 740, 235, 434, seed=24)
    # oil slick glow on water
    draw.ellipse([110, 474, 330, 486], fill=(120, 55, 18))
    draw.ellipse([600, 476, 820, 487], fill=(110, 50, 16))
    # headline band
    draw.rectangle([x0, y1 - 92, x1, y1], fill=(8, 12, 22))
    draw.line([(x0, y1 - 92), (x1, y1 - 92)], fill=ORANGE, width=4)
    f_h = font(SANS_B, 46)
    f_s = font(SANS_B, 24)
    draw.text((28, y1 - 86), "TANKERS ABLAZE IN HORMUZ", font=f_h, fill=WHITE)
    draw.text((28, y1 - 34), "TWO TANKERS HIT BY MINES  •  BRENT CRUDE JUMPS",
              font=f_s, fill=AMBER)


def panel_refinery(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, (x0, y0, x1, y1 - 84), (26, 20, 34), (90, 40, 24))
    # refinery towers
    for tx, th in [(x0 + 30, 70), (x0 + 80, 95), (x0 + 140, 60),
                   (x0 + 200, 88), (x0 + 250, 64)]:
        draw.rectangle([tx, y1 - 84 - th, tx + 26, y1 - 84], fill=(52, 48, 52))
        draw.rectangle([tx + 6, y1 - 84 - th - 12, tx + 20, y1 - 84 - th],
                       fill=(52, 48, 52))
    flame(draw, x0 + 110, y1 - 84, 56, 62, seed=31)
    flame(draw, x0 + 225, y1 - 84, 48, 52, seed=32)
    smoke(draw, x0 + 110, y0 + 14, y1 - 108, seed=33)
    caption_band(draw, box, "HOUTHIS HIT SAUDI REFINERY",
                 "Ras Tanura ablaze; 11 hurt in Riyadh")


def panel_huawei(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, (x0, y0, x1, y1 - 84), NAVY2, (10, 16, 34))
    # microchip
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1 - 84) // 2
    s = 74
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(30, 60, 110), outline=AMBER, width=4)
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                   fill=(200, 40, 40))
    for k in range(-1, 2):
        draw.line([(cx + k * 22, cy - s // 2 - 14), (cx + k * 22, cy - s // 2)],
                  fill=AMBER, width=4)
        draw.line([(cx + k * 22, cy + s // 2), (cx + k * 22, cy + s // 2 + 14)],
                  fill=AMBER, width=4)
        draw.line([(cx - s // 2 - 14, cy + k * 22), (cx - s // 2, cy + k * 22)],
                  fill=AMBER, width=4)
        draw.line([(cx + s // 2, cy + k * 22), (cx + s // 2 + 14, cy + k * 22)],
                  fill=AMBER, width=4)
    # gavel block at right
    draw.rectangle([x1 - 92, y1 - 84 - 46, x1 - 30, y1 - 84 - 34],
                   fill=(120, 82, 40))
    draw.rectangle([x1 - 66, y1 - 84 - 88, x1 - 56, y1 - 84 - 40],
                   fill=(120, 82, 40))
    caption_band(draw, box, "HUAWEI FOUND GUILTY",
                 "Trade secrets, bank fraud — US court")


def panel_space(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1 - 84], fill=(6, 8, 20))
    rnd = random.Random(5)
    for _ in range(46):
        sx = rnd.randint(x0 + 4, x1 - 4)
        sy = rnd.randint(y0 + 4, y1 - 70)
        r = rnd.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    # space station: central module + panels
    cy = (y0 + y1 - 84) // 2
    draw.rectangle([x0 + 60, cy - 14, x1 - 60, cy + 14], fill=(190, 196, 208))
    draw.rectangle([x0 + 130, cy - 8, x0 + 210, cy + 8], fill=(120, 128, 140))
    draw.rectangle([x0 + 60, cy - 34, x0 + 130, cy - 14], fill=(40, 80, 160))
    draw.rectangle([x1 - 130, cy + 14, x1 - 60, cy + 34], fill=(40, 80, 160))
    # capsule docking
    draw.ellipse([x1 - 92, cy - 22, x1 - 52, cy + 22], fill=(230, 120, 40))
    draw.rectangle([x1 - 108, cy - 10, x1 - 88, cy + 10], fill=(230, 120, 40))
    caption_band(draw, box, "CHINA–PAKISTAN IN SPACE",
                 "First foreign astronaut aboard station")


def panel_parade(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, (x0, y0, x1, y1 - 84), (52, 58, 74), (16, 20, 34))
    # storm clouds
    rnd = random.Random(9)
    for _ in range(9):
        cx = rnd.randint(x0 + 20, x1 - 20)
        cy = rnd.randint(y0 + 8, y0 + 52)
        r = rnd.randint(18, 34)
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(70, 74, 88))
    # grounded balloons: full round balloons, tethered low
    draw.ellipse([x0 + 40, y0 + 46, x0 + 150, y0 + 118], fill=(220, 60, 60))
    draw.polygon([(x0 + 88, y0 + 118), (x0 + 98, y0 + 118),
                  (x0 + 93, y0 + 132)], fill=(220, 60, 60))
    draw.line([(x0 + 93, y0 + 132), (x0 + 93, y0 + 142)],
              fill=(200, 200, 200), width=2)
    draw.ellipse([x0 + 190, y0 + 58, x0 + 262, y0 + 116], fill=(60, 140, 220))
    draw.polygon([(x0 + 220, y0 + 116), (x0 + 230, y0 + 116),
                  (x0 + 225, y0 + 128)], fill=(60, 140, 220))
    draw.line([(x0 + 225, y0 + 128), (x0 + 225, y0 + 138)],
              fill=(200, 200, 200), width=2)
    # rain streaks
    for i in range(14):
        rx = x0 + 12 + i * 23
        draw.line([(rx, y0 + 84), (rx - 8, y0 + 108)], fill=(150, 170, 200),
                  width=2)
    caption_band(draw, box, "PARADE POSTPONED",
                 "100th Macy's parade delayed by storm")


def panel_tariffs(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, (x0, y0, x1, y1 - 84), (24, 44, 66), (12, 20, 34))
    # bar chart rising, one bar falling (markets)
    base = y1 - 84
    bars = [(x0 + 34, 46, (60, 160, 90)), (x0 + 84, 62, (60, 160, 90)),
            (x0 + 134, 80, (60, 160, 90)), (x0 + 184, 96, (60, 160, 90))]
    for bx, bh, col in bars:
        draw.rectangle([bx, base - bh, bx + 34, base], fill=col)
    draw.line([(x0 + 30, base - 100), (x0 + 230, base - 108)],
              fill=AMBER, width=3)
    # shipping containers
    draw.rectangle([x0 + 238, base - 44, x0 + 288, base - 22], fill=(200, 70, 40))
    draw.rectangle([x0 + 238, base - 22, x0 + 288, base], fill=(40, 120, 180))
    draw.rectangle([x0 + 292, base - 44, x0 + 318, base], fill=(200, 160, 40))
    caption_band(draw, box, "US TARIFFS RISE",
                 "Brazil, 14 partners; GDP up 4.3%")


def panel_brief(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CREAM)
    draw.rectangle([x0, y0, x1, y0 + 40], fill=(140, 30, 26))
    f_h = font(SANS_B, 22)
    draw.text((x0 + 12, y0 + 7), "WORLD IN BRIEF", font=f_h, fill=WHITE)
    f_b = font(SANS_B, 17)
    f_t = font(SANS, 17)
    items = [
        ("Kraków:", "gunman kills at least six"),
        ("Cartagena:", "25 hostages in siege"),
        ("Sudan:", "19 killed in drone strikes"),
        ("COP31:", "climate talks fail"),
    ]
    y = y0 + 52
    for head, tail in items:
        draw.text((x0 + 12, y), "• " + head, font=f_b, fill=INK)
        tw = f_b.getlength("• " + head + " ")
        draw.text((x0 + 12 + tw, y), tail, font=f_t, fill=INK)
        y += 30
    draw.line([(x0 + 12, y1 - 14), (x1 - 12, y1 - 14)], fill=(140, 30, 26),
              width=2)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # masthead
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.line([(0, 118), (W, 118)], fill=ORANGE, width=4)
    f_title = font(SERIF_B, 88)
    title = "THE WORLD"
    tw = f_title.getlength(title)
    draw.text(((W - tw) / 2, 2), title, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 30)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    dw = f_date.getlength(date)
    draw.text(((W - dw) / 2, 84), date, font=f_date, fill=AMBER)

    lead_panel(img, draw)

    # bottom grid: 3 cols x 2 rows
    gx, gy = 8, 588
    pw, ph = 328, 195
    gap = 8
    panels = [panel_refinery, panel_huawei, panel_space,
              panel_parade, panel_tariffs, panel_brief]
    for i, fn in enumerate(panels):
        col, row = i % 3, i // 3
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        fn(draw, (x0, y0, x0 + pw, y0 + ph))

    # footer with the date again
    draw.rectangle([0, 990, W, H], fill=NAVY)
    f_f = font(SANS_B, 20)
    foot = "WEDNESDAY 25 NOVEMBER 2026  •  THE WORLD"
    fw = f_f.getlength(foot)
    draw.text(((W - fw) / 2, 1001), foot, font=f_f, fill=WHITE)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

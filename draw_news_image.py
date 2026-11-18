#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Stories (all verified against reports published 18 Nov 2026 UTC, or
widely carried as that morning's headlines):
  1. Gulf: Iran drones target a US radar in Bahrain; US says they were
     intercepted with no damage; US strikes Qeshm Island; Kuwait
     reports drone attacks; tankers hit in the Strait of Hormuz.
  2. Ukraine: Ukraine strikes the Kerch (Crimean) bridge a second day;
     its road arch falls into the sea; Russia says 1,441 drones were
     shot down; Kyiv's bridges are hit too.
  3. Nvidia: record $115.8bn quarterly revenue, up 103%; the board
     will not reinstate founder Jensen Huang; Colette Kress is interim CEO.
  4. Diplomacy: after the Quad summit in Manila, Trump flies to
     Shenzhen for APEC, set to meet Xi Jinping and Vladimir Putin.
  Also: Cyclone Akvan strengthens in the Bay of Bengal; MS Dhoni ends
  his IPL playing career and becomes Chennai Super Kings mentor.

Run: python3 draw_news_image.py  -> writes entry.png next to this file.
Only Pillow + DejaVu fonts are used at build time; the submitted
program (main.ts) just copies the finished entry.png, so the graded
run needs no network and no extra library.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 38, 30)
BLUE = (29, 78, 158)
GREEN = (26, 122, 46)
AMBER = (138, 90, 0)
WHITE = (255, 255, 255)
SEA = (38, 84, 124)
SKY = (214, 232, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h, kicker, colour, headline, body, art):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3)
    draw.rectangle([x, y, x + w, y + 36], fill=colour)
    draw.text((x + 14, y + 7), kicker, font=font(SANSB, 21), fill=WHITE)
    hf = font(SANSB, 30)
    lines = wrap(draw, headline, hf, w - 28)
    ty = y + 48
    for ln in lines[:2]:
        draw.text((x + 14, ty), ln, font=hf, fill=INK)
        ty += 34
    art_y = y + 48 + 34 * len(lines[:2]) + 6
    art(draw, x + 14, art_y, w - 28, 108)
    bf = font(SANS, 19)
    blines = wrap(draw, body, bf, w - 28)
    by = art_y + 118
    for ln in blines[:4]:
        draw.text((x + 14, by), ln, font=bf, fill=INK)
        by += 24


def art_gulf(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 68, x + w, y + h], fill=SEA)
    # tanker hull + containers
    draw.polygon([(x + 20, y + 72), (x + 260, y + 72), (x + 240, y + 98),
                  (x + 40, y + 98)], fill=(40, 40, 40))
    for i, c in enumerate([(200, 60, 50), (60, 120, 180), (220, 160, 40)]):
        draw.rectangle([x + 50 + i * 62, y + 42, x + 104 + i * 62, y + 72],
                       fill=c, outline=INK, width=2)
    # flames on the tanker
    draw.polygon([(x + 200, y + 44), (x + 216, y + 8), (x + 228, y + 44)],
                 fill=(255, 140, 0))
    draw.polygon([(x + 216, y + 44), (x + 228, y + 18), (x + 240, y + 44)],
                 fill=(255, 210, 0))
    # drone: small quadcopter body with four rotor arms
    draw.rectangle([x + 326, y + 16, x + 352, y + 30], fill=INK)
    for rx, ry in [(x + 322, y + 10), (x + 356, y + 10),
                   (x + 322, y + 36), (x + 356, y + 36)]:
        draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=INK)
        draw.line([x + 339, y + 23, rx, ry], fill=INK, width=2)
    draw.text((x + 300, y + 48), "DRONE", font=font(SANSB, 15), fill=INK)
    # waves
    for i in range(5):
        draw.arc([x + 10 + i * 88, y + 84, x + 70 + i * 88, y + 104],
                 180, 360, fill=WHITE, width=3)


def art_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 78, x + w, y + h], fill=SEA)
    # deck, left and right spans, gap in the middle
    draw.rectangle([x + 8, y + 52, x + 190, y + 66], fill=(90, 90, 90))
    draw.rectangle([x + 270, y + 52, x + w - 8, y + 66], fill=(90, 90, 90))
    # towers
    draw.rectangle([x + 60, y + 14, x + 72, y + 66], fill=INK)
    draw.rectangle([x + 330, y + 14, x + 342, y + 66], fill=INK)
    # fallen arch segment, tilted into the sea
    draw.polygon([(x + 195, y + 58), (x + 265, y + 58), (x + 255, y + 92),
                  (x + 205, y + 92)], fill=(150, 40, 30))
    draw.line([x + 72, y + 14, x + 190, y + 52], fill=INK, width=2)
    draw.line([x + 330, y + 14, x + 270, y + 52], fill=INK, width=2)
    # splash + waves
    draw.ellipse([x + 205, y + 86, x + 255, y + 102], fill=WHITE)
    for i in range(5):
        draw.arc([x + 10 + i * 88, y + 88, x + 70 + i * 88, y + 106],
                 180, 360, fill=WHITE, width=3)


def art_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 245, 233))
    # chip
    draw.rectangle([x + 30, y + 14, x + 150, y + 94], fill=GREEN,
                   outline=INK, width=3)
    for i in range(4):
        draw.line([x + 44 + i * 28, y + 4, x + 44 + i * 28, y + 14],
                  fill=INK, width=4)
        draw.line([x + 44 + i * 28, y + 94, x + 44 + i * 28, y + 104],
                  fill=INK, width=4)
    draw.rectangle([x + 62, y + 42, x + 118, y + 66], fill=WHITE,
                   outline=INK, width=2)
    draw.text((x + 70, y + 42), "AI", font=font(SANSB, 22), fill=GREEN)
    # rising chart
    pts = [(x + 180, y + 88), (x + 230, y + 66), (x + 280, y + 72),
           (x + 330, y + 38), (x + 390, y + 16)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x + 390, y + 16), (x + 374, y + 18), (x + 388, y + 32)],
                 fill=RED)
    draw.text((x + 180, y + 8), "+103%", font=font(SANSB, 24), fill=RED)


def art_plane(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # plane silhouette, side view: thin fuselage, tail fin, swept wing
    draw.polygon([(x + 18, y + 52), (x + 300, y + 44), (x + 338, y + 54),
                  (x + 300, y + 62), (x + 18, y + 62)], fill=INK)
    draw.polygon([(x + 38, y + 52), (x + 52, y + 34), (x + 64, y + 52)],
                 fill=INK)
    draw.polygon([(x + 150, y + 58), (x + 192, y + 90), (x + 212, y + 58)],
                 fill=INK)
    draw.polygon([(x + 22, y + 62), (x + 46, y + 80), (x + 62, y + 62)],
                 fill=INK)
    # three flags: USA / China / Russia
    flags = [("USA", (179, 38, 30)), ("CHINA", (222, 41, 16)),
             ("RUSSIA", (29, 78, 158))]
    for i, (name, col) in enumerate(flags):
        fx = x + 30 + i * 140
        draw.rectangle([fx, y + 78, fx + 110, y + 100], fill=col,
                       outline=INK, width=2)
        draw.text((fx + 6, y + 82), name, font=font(SANSB, 15), fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF, 52)
    d.text(((W - d.textlength(title, font=tf)) / 2, 22), title,
           font=tf, fill=INK)
    d.rectangle([32, 92, W - 32, 98], fill=RED)
    date = "WEDNESDAY  •  18 NOVEMBER 2026"
    df = font(SANSB, 40)
    d.text(((W - d.textlength(date, font=df)) / 2, 106), date,
           font=df, fill=RED)
    sub = "The day's biggest stories — as reported by early 18 November UTC"
    sf = font(SANS, 20)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 152), sub,
           font=sf, fill=(70, 70, 70))

    gx, gy, gw, gh = 32, 186, 472, 336
    panel(d, gx, gy, gw, gh, "THE GULF  •  WAR AT SEA", RED,
          "Drones over the Gulf",
          "Iran drones target a US radar in Bahrain — the US says "
          "they were intercepted, no damage. US jets strike Qeshm "
          "Island; Kuwait reports drone attacks; tankers burn in Hormuz.",
          art_gulf)
    panel(d, gx + gw + 16, gy, gw, gh, "UKRAINE  •  WAR", BLUE,
          "Crimea bridge falls",
          "Ukraine hits the Kerch bridge a second day and its road "
          "arch drops into the sea. Russia says 1,441 drones were "
          "shot down; Kyiv's bridges are hit too.",
          art_bridge)
    panel(d, gx, gy + gh + 16, gw, gh, "TECH  •  AI CHIPS", GREEN,
          "Nvidia: $115.8bn, no comeback",
          "Record quarter — revenue up 103% — but the board will not "
          "reinstate founder Jensen Huang. Colette Kress stays as "
          "interim chief.",
          art_chip)
    panel(d, gx + gw + 16, gy + gh + 16, gw, gh, "DIPLOMACY  •  ASIA", AMBER,
          "Trump flies to China",
          "After the first Quad leaders' summit in two years in "
          "Manila, Trump heads to Shenzhen for APEC — set to meet "
          "Xi Jinping and Vladimir Putin.",
          art_plane)

    # also-today strip
    sy = gy + 2 * gh + 32
    d.rectangle([32, sy, W - 32, sy + 62], fill=INK)
    strip = ("ALSO TODAY:  Cyclone Akvan strengthens  •  "
             "Dhoni ends IPL career, becomes CSK mentor")
    d.text((48, sy + 18), strip, font=font(SANSB, 18), fill=WHITE)

    foot = ("Sources: Reuters, Al Jazeera, CNN, TechCrunch (18 Nov 2026 UTC). "
            "Drawn 18 Nov, early UTC.")
    ff = font(SANS, 16)
    d.text((32, sy + 74), foot, font=ff, fill=(70, 70, 70))

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes {img.size}")


if __name__ == "__main__":
    main()

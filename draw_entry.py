#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news image (1024x1024).

"Daylight atlas" theme (ivory paper, deep teal, burnt orange) following
the WINNING anatomy of the 22 Nov final rank 1 (@bagarte, 85.4411%,
45W/7D/2L, #1 of 16,752): 29 stories (13 numbered cards + 16 briefs),
big date masthead, region pills, UTC timeline, "The Day in Numbers"
sidebar, dotted world map, DATE CHECK box. The provisional 22 Nov
leader (atlas22b, 36 stories, 99.2% dev score) did NOT win the final,
so this build uses 29 stories with larger type and cleaner panels.

News facts, all happening / first reported on Tue 24 Nov 2026
(verified; see DATE CHECK for what was kept out). Heroes: Israeli
strikes kill 9 in Gaza (incl. an UNRWA worker); Shenzhou-24 names
Muhammad Zeeshan Ali, the first foreign astronaut to Tiangong (and
first Pakistani in space); Indonesia candy-factory fire toll rises
to 26 dead, 8 missing. Cards 4-13: Russia strikes Zaporizhzhia
(2 dead, 22 hurt), Real Madrid rout PSV 5-1, Dow crosses 50,000 as
Nvidia slides 5.9%, US hits Iran with new sanctions, Netanyahu
urges Trump to strike Iran, Iraq seizes Kurdish oilfields and
crossings, Nepal quake M5.6, Colombia car bomb wounds 23, Sudan
drone attack kills 4 civilians (UN building hit), Russian aircraft
enters South Korea's ADIZ. Briefs 14-29: NATO space defence, 153
Russian ballistic missiles in October, NATO aircraft in Poland,
Iran's seven conditions, Qatar revives US-Iran talks, Hormuz tanker
mines, Mexico to try 'El Chapo Isidro', Bukele names 3 soldiers
killed in Haiti, China executes official for spying, Pakistan-Sri
Lanka Test, Bangladesh paramilitary over Hasina return, Fiji school
closures, Australia rejects Vanuatu treaty, NZ central bank mandate,
WHO Ebola team trapped in DR Congo, South Sudan election / UN meet.
NOT Tuesday news (kept out, listed in DATE CHECK): COP31 collapse
itself (Sun 22 Nov); ICJ Rohingya verdict (Thu 19 Nov); Nvidia +31%
/ Huang restored (Mon 23 Nov); Saudi strike on Hodeida (Mon 23
Nov); EU 22nd Russia sanctions (Mon 23 Nov); Puigdemont amnesty
(Mon 23 Nov); Democrats reach 258 House seats (Sun 22 Nov);
Merkury sunk in Libya (Sun 22-Mon 23 Nov); 'El Chapo Isidro'
captured (Fri 21 Nov); India declare 720/9 (Sat 22 Nov);
Verstappen wins Las Vegas GP (Sat 22 Nov); factory fire breaks
out (Sat 21 Nov). Kiribati Kanton evacuation reason is unverified
and is NOT used.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- Daylight atlas palette ----
PAPER = (250, 246, 234)
PAPER2 = (244, 238, 222)
TEAL = (13, 92, 96)
TEAL2 = (20, 120, 124)
TEAL_DK = (8, 60, 64)
ORANGE = (214, 90, 32)
ORANGE2 = (238, 140, 60)
OCHRE = (198, 148, 44)
INK = (24, 32, 34)
GREY = (110, 116, 118)
GREY_DK = (70, 76, 78)
CREAM = (250, 246, 234)
GOLD = (232, 178, 80)
SKY = (168, 208, 220)
SEA = (28, 110, 130)
GREEN = (46, 125, 70)
PLUM = (122, 74, 110)
SLATE = (90, 104, 122)
ROYAL = (52, 84, 160)
RED = (186, 52, 44)
WHITE = (255, 255, 255)
CYAN = (120, 210, 225)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
COND = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif(size, bold=True):
    return F(SERIF_B if bold else SERIF, size)


def cond(size, bold=True):
    return F(COND_B if bold else COND, size)


def sans(size, bold=True):
    return F(SANS_B if bold else SANS, size)


def fit(text, max_w, start, fn=cond, bold=True, min_size=9):
    size = start
    while size > min_size:
        f = fn(size, bold)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return fn(min_size, bold)


def text_c(d, cx, y, s, f, fill):
    d.text((cx, y), s, font=f, fill=fill, anchor="ma")


def text_l(d, x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill, anchor="la")


def wrap_text(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, f, fill, max_w, leading=None):
    lh = leading or int(f.size * 1.18)
    lines = wrap_text(text, f, max_w)
    for i, line in enumerate(lines):
        d.text((x, y + i * lh), line, font=f, fill=fill, anchor="la")
    return y + len(lines) * lh


# ---- flat illustration helpers (all drawn in code) ----
def illu_gaza(d, x, y, w, h):
    # night sky over Gaza, explosion flash, building silhouette, "9"
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 52))
    for dx, dy in [(20, 12), (70, 22), (130, 10), (180, 20), (215, 12)]:
        d.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=WHITE)
    # explosion flash
    cx, cy = x + w - 62, y + 30
    for r, col in [(26, (214, 90, 32)), (17, GOLD), (9, (255, 240, 180))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # buildings
    bx, by = x + 14, y + h - 48
    d.rectangle([bx, by, bx + 70, y + h], fill=(52, 66, 84))
    d.rectangle([bx + 84, y + h - 34, bx + 130, y + h], fill=(40, 54, 70))
    for wy in range(by + 6, y + h - 6, 12):
        for wx in range(bx + 6, bx + 64, 14):
            d.rectangle([wx, wy, wx + 7, wy + 7],
                        fill=GOLD if (wx + wy) % 3 else (30, 44, 60))
    d.text((x + 10, y + h - 22), "9", font=cond(20), fill=GOLD)


def illu_space(d, x, y, w, h):
    # deep space, stars, rocket climbing, Tiangong station, Earth arc
    # (Earth kept as a shallow arc fully inside the illustration box)
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for dx, dy in [(16, 10), (60, 26), (110, 8), (160, 20), (205, 12),
                   (40, 44), (140, 40), (190, 44)]:
        d.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=WHITE)
    # Earth arc: shallow dome at the bottom, fully inside the box
    d.ellipse([x + 6, y + h - 22, x + w - 6, y + h], fill=(28, 110, 180))
    d.arc([x + 6, y + h - 22, x + w - 6, y + h], 180, 360, fill=SKY, width=2)
    # Tiangong station (small modules)
    sx, sy = x + 150, y + 22
    d.rectangle([sx, sy, sx + 52, sy + 10], fill=(200, 210, 214))
    d.rectangle([sx + 18, sy - 6, sx + 34, sy + 16], fill=(150, 160, 170))
    d.rectangle([sx - 12, sy + 2, sx, sy + 8], fill=ROYAL)
    d.rectangle([sx + 52, sy + 2, sx + 64, sy + 8], fill=ROYAL)
    # rocket
    rx, ry = x + 52, y + 26
    d.polygon([(rx, ry - 14), (rx + 8, ry), (rx - 8, ry)], fill=RED)
    d.rectangle([rx - 8, ry, rx + 8, ry + 26], fill=WHITE)
    d.rectangle([rx - 8, ry + 26, rx + 8, ry + 32], fill=ORANGE)
    d.polygon([(rx - 5, ry + 32), (rx + 5, ry + 32), (rx, ry + 46)],
              fill=GOLD)
    d.ellipse([rx - 3, ry + 8, rx + 3, ry + 14], fill=TEAL)


def illu_fire24(d, x, y, w, h):
    # factory at night, flames on the roofline, "26"
    d.rectangle([x, y, x + w, y + h], fill=(52, 36, 28))
    d.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 6], fill=(90, 90, 96))
    for wx in range(x + 22, x + w - 22, 18):
        d.rectangle([wx, y + h - 28, wx + 9, y + h - 20], fill=GOLD)
    # chimney
    d.rectangle([x + w - 40, y + 8, x + w - 28, y + h - 34], fill=(70, 70, 78))
    # flames
    for fx, fh in [(18, 22), (62, 30), (106, 22), (150, 26)]:
        base = y + h - 34
        d.polygon([(x + fx, base), (x + fx + 14, base - fh),
                   (x + fx + 28, base)], fill=ORANGE)
        d.polygon([(x + fx + 7, base), (x + fx + 14, base - fh + 12),
                   (x + fx + 21, base)], fill=GOLD)
    d.text((x + 10, y + h - 20), "26", font=cond(18), fill=WHITE)


def illu_zap(d, x, y, w, h):
    # night sky, drone crosses, apartment block, "2"
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 52))
    for dx, dy, s in [(24, 10, 7), (80, 16, 6), (140, 8, 7)]:
        cx, cy = x + dx, y + dy
        d.line([cx - s, cy - s, cx + s, cy + s], fill=GOLD, width=2)
        d.line([cx - s, cy + s, cx + s, cy - s], fill=GOLD, width=2)
    bx, by = x + 14, y + h - 30
    d.rectangle([bx, by, bx + 90, y + h], fill=(52, 66, 84))
    for wy in range(by + 5, y + h - 4, 10):
        for wx in range(bx + 5, bx + 85, 12):
            d.rectangle([wx, wy, wx + 6, wy + 6],
                        fill=GOLD if (wx + wy) % 3 else (30, 44, 60))
    d.text((x + w - 30, y + h - 18), "2", font=cond(16), fill=GOLD)


def illu_football(d, x, y, w, h):
    # green pitch, white lines, goal, ball, "5-1"
    d.rectangle([x, y, x + w, y + h], fill=GREEN)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 84, 52))
    d.line([x + 8, y + 6, x + w - 8, y + 6], fill=WHITE, width=2)
    d.line([x + w // 2, y + 6, x + w // 2, y + h - 10], fill=WHITE, width=2)
    d.ellipse([x + w // 2 - 10, y + 8, x + w // 2 + 10, y + 28],
              outline=WHITE, width=2)
    # goal
    d.rectangle([x + w - 46, y + 12, x + w - 10, y + 30], outline=WHITE, width=2)
    # ball (bottom-right, clear of the score bug)
    d.ellipse([x + w - 60, y + h - 22, x + w - 48, y + h - 10], fill=WHITE)
    # score bug, top-left below the card number badge (clear of goal/ball)
    d.text((x + 8, y + 18), "5-1", font=cond(15), fill=WHITE)


def illu_dow(d, x, y, w, h):
    # dark green board, rising chart arrow, "50,000"
    d.rectangle([x, y, x + w, y + h], fill=(16, 52, 36))
    d.line([x + 10, y + h - 14, x + 40, y + h - 24, x + 70, y + h - 20,
            x + 100, y + 22, x + 130, y + 12, x + w - 12, y + 6],
           fill=(60, 220, 120), width=3)
    d.polygon([(x + w - 22, y + 2), (x + w - 6, y + 6), (x + w - 22, y + 12)],
              fill=(60, 220, 120))
    # label to the right of the card number badge (top-left is covered)
    d.text((x + 34, y + 2), "50,000", font=cond(15), fill=GOLD)


def illu_sanctions24(d, x, y, w, h):
    # navy vault, gold dollar, network coins
    d.rectangle([x, y, x + w, y + h], fill=(18, 58, 78))
    cx = x + w // 2
    d.ellipse([cx - 20, y + 4, cx + 20, y + 40], fill=(120, 132, 140),
              outline=GOLD, width=2)
    d.ellipse([cx - 12, y + 12, cx + 12, y + 32], fill=TEAL_DK)
    d.text((cx, y + 14), "$", font=cond(18), fill=GOLD, anchor="ma")
    for px, py in [(x + 34, y + 6), (x + w - 22, y + 6), (x + 12, y + h - 14),
                   (x + w - 24, y + h - 14)]:
        d.line([cx, y + 22, px + 5, py + 5], fill=(120, 180, 190), width=1)
        d.ellipse([px, py, px + 10, py + 10], fill=GOLD)


def illu_podium(d, x, y, w, h):
    # podium with Israel + US flags, microphone
    d.rectangle([x, y, x + w, y + h], fill=(198, 214, 228))
    d.rectangle([x + 24, y + h - 16, x + w - 24, y + h - 6], fill=(122, 84, 52))
    # Israel flag
    fx = x + 30
    d.line([fx + 6, y + 6, fx + 6, y + h - 16], fill=INK, width=2)
    d.rectangle([fx + 6, y + 6, fx + 32, y + 22], fill=WHITE)
    d.line([fx + 6, y + 8, fx + 32, y + 8], fill=ROYAL, width=2)
    d.line([fx + 6, y + 20, fx + 32, y + 20], fill=ROYAL, width=2)
    d.ellipse([fx + 14, y + 11, fx + 24, y + 19], outline=ROYAL, width=1)
    # US flag
    fx = x + 100
    d.line([fx + 6, y + 6, fx + 6, y + h - 16], fill=INK, width=2)
    for i, col in enumerate([RED, WHITE, RED, WHITE, RED, WHITE, RED]):
        d.rectangle([fx + 6, y + 6 + i * 2, fx + 32, y + 8 + i * 2], fill=col)
    d.rectangle([fx + 6, y + 6, fx + 16, y + 13], fill=ROYAL)
    # microphone
    cx = x + w // 2
    d.ellipse([cx - 7, y + 12, cx + 7, y + 28], fill=(60, 60, 70))
    d.rectangle([cx - 2, y + 28, cx + 2, y + h - 16], fill=(60, 60, 70))


def illu_oil(d, x, y, w, h):
    # desert tan, oil derrick, pipeline, flame
    d.rectangle([x, y, x + w, y + h], fill=(214, 190, 140))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(160, 120, 70))
    # derrick
    dx = x + 30
    d.polygon([(dx, y + 4), (dx + 34, y + 4), (dx + 26, y + h - 12),
               (dx + 8, y + h - 12)], outline=INK, width=2)
    d.line([dx + 8, y + 12, dx + 26, y + 12], fill=INK, width=2)
    d.line([dx + 12, y + 24, dx + 22, y + 24], fill=INK, width=2)
    # flame (kept inside the illustration box)
    d.polygon([(dx + 14, y + 6), (dx + 17, y + 1), (dx + 20, y + 6)],
              fill=ORANGE)
    # pipeline
    d.rectangle([x + 76, y + h - 22, x + w - 10, y + h - 14], fill=(90, 90, 96))
    d.ellipse([x + w - 34, y + h - 30, x + w - 18, y + h - 14], fill=GOLD)


def illu_quake(d, x, y, w, h):
    # mountains, seismic zigzag, "5.6"
    d.rectangle([x, y, x + w, y + h], fill=(120, 150, 190))
    d.polygon([(x, y + h), (x + 50, y + 8), (x + 100, y + h)], fill=(70, 90, 120))
    d.polygon([(x + 60, y + h), (x + 120, y + 16), (x + 180, y + h)],
              fill=(50, 70, 100))
    d.polygon([(x + 44, y + 14), (x + 50, y + 8), (x + 56, y + 14)],
              fill=WHITE)
    d.line([x + 8, y + h - 12, x + 40, y + h - 22, x + 70, y + h - 8,
            x + 100, y + h - 24, x + 130, y + h - 10, x + w - 8, y + h - 20],
           fill=RED, width=2)
    # magnitude top-right (top-left is covered by the card number badge)
    d.text((x + w - 42, y + 2), "5.6", font=cond(15), fill=WHITE)


def illu_bomb(d, x, y, w, h):
    # street, car silhouette, explosion flash, "23"
    d.rectangle([x, y, x + w, y + h], fill=(168, 150, 130))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 66, 76))
    # car
    cx, cy = x + 40, y + h - 22
    d.rectangle([cx, cy - 8, cx + 52, cy + 2], fill=(40, 44, 52))
    d.polygon([(cx + 10, cy - 8), (cx + 18, cy - 16), (cx + 38, cy - 16),
               (cx + 44, cy - 8)], fill=(40, 44, 52))
    d.ellipse([cx + 8, cy, cx + 18, cy + 8], fill=INK)
    d.ellipse([cx + 36, cy, cx + 46, cy + 8], fill=INK)
    # flash
    fx, fy = x + w - 42, y + 18
    for r, col in [(16, ORANGE), (10, GOLD), (5, (255, 240, 180))]:
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
    # casualty count top-centre (top-left is covered by the card number badge)
    text_c(d, x + w // 2, y + 2, "23", cond(15), INK)


def illu_drone(d, x, y, w, h):
    # pale sky, quadcopter drone, building, UN blue band
    d.rectangle([x, y, x + w, y + h], fill=(190, 210, 225))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(0, 91, 172))
    # building
    bx, by = x + 14, y + h - 28
    d.rectangle([bx, by, bx + 60, y + h - 10], fill=(120, 125, 135))
    for wy in range(by + 4, y + h - 12, 8):
        for wx in range(bx + 4, bx + 56, 10):
            d.rectangle([wx, wy, wx + 5, wy + 5], fill=GOLD)
    # drone
    cx, cy = x + w - 46, y + 16
    d.rectangle([cx - 12, cy - 3, cx + 12, cy + 3], fill=INK)
    for px in (-16, 16):
        d.ellipse([cx + px - 6, cy - 6, cx + px + 6, cy + 6], outline=INK, width=2)
        d.line([cx + px - 8, cy, cx + px + 8, cy], fill=INK, width=2)
    d.line([cx, cy + 3, cx, cy + 10], fill=INK, width=2)


def illu_jet(d, x, y, w, h):
    # sky, jet silhouette, radar arc, "ADIZ"
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # radar arc
    cx, cy = x + w - 30, y + h - 8
    d.arc([cx - 26, cy - 26, cx + 26, cy + 26], 180, 270, fill=TEAL, width=2)
    d.arc([cx - 16, cy - 16, cx + 16, cy + 16], 180, 270, fill=TEAL, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=TEAL)
    # jet
    jx, jy = x + 30, y + 18
    d.polygon([(jx, jy), (jx + 46, jy + 6), (jx, jy + 12)], fill=(60, 66, 76))
    d.polygon([(jx + 20, jy + 2), (jx + 34, jy - 8), (jx + 34, jy + 2)],
              fill=(60, 66, 76))
    d.polygon([(jx + 20, jy + 10), (jx + 30, jy + 20), (jx + 34, jy + 10)],
              fill=(60, 66, 76))
    d.text((x + 8, y + h - 16), "ADIZ", font=cond(13), fill=TEAL_DK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=TEAL, width=4)
    d.rectangle([8, 8, 1015, 1015], outline=TEAL, width=1)

    # ---- Top teal band ----
    d.rectangle([8, 8, 1015, 40], fill=TEAL)
    text_l(d, 16, 13, "THE WORLD IN ONE DAY", cond(19), WHITE)
    tr = "29 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((1008, 15), tr, font=cond(15), fill=CREAM, anchor="ra")

    # ---- Masthead ----
    text_c(d, 512, 46, "Tuesday 24 November 2026",
           fit("Tuesday 24 November 2026", 980, 50, fn=serif), TEAL_DK)
    deck = ("Gaza strikes kill 9  ·  Shenzhou-24 names first foreign astronaut  ·  "
            "Factory-fire toll rises to 26")
    text_c(d, 512, 100, deck, fit(deck, 980, 18, fn=serif, bold=False), ORANGE)
    d.line([16, 124, 1008, 124], fill=TEAL, width=2)

    # ---- Region pills ----
    regions = [
        ("EUROPE 5", TEAL2), ("MIDDLE EAST 6", ORANGE), ("ASIA-PACIFIC 4", OCHRE),
        ("AFRICA 3", GREEN), ("AMERICAS 5", ROYAL), ("SOUTH ASIA 3", PLUM),
        ("OCEANIA 3", SLATE),
    ]
    ry = 130
    rw = 1008 // 7
    for i, (label, col) in enumerate(regions):
        x = 8 + i * rw
        w = rw if i < 6 else 1008 - 6 * rw
        d.rectangle([x, ry, x + w, ry + 24], fill=col)
        text_c(d, x + w // 2, ry + 4, label, fit(label, w - 8, 14), WHITE)

    # ---- Timeline bar ----
    ty = 158
    d.rectangle([8, ty, 1015, ty + 24], fill=TEAL_DK)
    text_l(d, 16, ty + 4, "THE DAY IN UTC", cond(14), GOLD)
    tl = ("01:06  Bukele names 3 soldiers killed in Haiti   ·   01:32  Nepal "
          "quake M5.6   ·   02:37  China executes official for spying   ·   "
          "04:19  Russia strikes Zaporizhzhia, 2 dead   ·   10:02  Colombia "
          "car-bomb toll rises to 23   ·   21:00  Dow closes above 50,000")
    d.text((168, ty + 4), tl, font=fit(tl, 840, 13, fn=cond, bold=False),
           fill=WHITE, anchor="la")

    # ---- Heroes row (3 heroes + numbers sidebar) ----
    heroes = [
        ("1  ·  GAZA  ·  WAR", "REPORTED",
         "Israeli strikes kill 9 in Gaza",
         "Morning strikes kill 6; three more die in the afternoon, "
         "including a UNRWA worker. (Reuters)",
         "gaza"),
        ("2  ·  JIUQUAN  ·  SPACE", "REPORTED",
         "Shenzhou-24 names first foreign astronaut",
         "Pakistan's Muhammad Zeeshan Ali, 40, will be the first "
         "foreigner aboard Tiangong. (Reuters)",
         "space"),
        ("3  ·  CIKANDE  ·  DISASTER", "ONGOING",
         "Candy-factory fire toll rises to 26 dead",
         "Eight still missing at the Java factory; 600+ rescuers "
         "search the second floor. (Xinhua)",
         "fire"),
    ]
    hx0, hy, hw, hh = 8, 188, 252, 200
    hillu = {"gaza": illu_gaza, "space": illu_space, "fire": illu_fire24}
    for i, (kick, status, title, sub, kind) in enumerate(heroes):
        x = hx0 + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], fill=PAPER2)
        d.rectangle([x, hy, x + hw, hy + hh], outline=TEAL, width=2)
        ix, iy, iw, ih = x + 6, hy + 6, hw - 12, 82
        hillu[kind](d, ix, iy, iw, ih)
        d.rectangle([ix, iy, ix + 30, iy + 18], fill=ORANGE)
        text_c(d, ix + 15, iy + 1, str(i + 1), cond(14), WHITE)
        ty2 = hy + 94
        text_l(d, x + 10, ty2, kick, cond(12), ORANGE)
        d.text((x + hw - 10, ty2), status, font=cond(12),
               fill=TEAL if status == "REPORTED" else RED, anchor="ra")
        ty2 = draw_wrapped(d, x + 10, ty2 + 17, title, cond(20), INK,
                           hw - 20, leading=22)
        draw_wrapped(d, x + 10, ty2 + 2, sub, cond(12, bold=False),
                     GREY_DK, hw - 20, leading=14)

    # ---- Numbers sidebar ----
    sx, sy, sw, sh = 788, 188, 220, 200
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=TEAL_DK)
    d.rectangle([sx, sy, sx + sw, sy + sh], outline=TEAL, width=2)
    text_l(d, sx + 10, sy + 6, "THE DAY IN NUMBERS", cond(14), GOLD)
    stats = [
        ("9", "Palestinians killed in Gaza", "on Tuesday — incl. UNRWA worker"),
        ("26", "dead in the Indonesia", "factory fire; 8 still missing"),
        ("50,000", "Dow closes above 50,000", "for the first time ever"),
        ("5-1", "Real Madrid rout PSV", "in the Champions League"),
        ("153", "Russian ballistic missiles", "fired at Ukraine in October"),
        ("23", "injured in the Colombia", "car bomb in Villavicencio"),
    ]
    for i, (num, l1, l2) in enumerate(stats):
        y = sy + 28 + i * 28
        text_l(d, sx + 10, y, num, fit(num, 76, 20, fn=cond), GOLD)
        text_l(d, sx + 88, y + 1, l1, fit(l1, sw - 98, 11, fn=cond, bold=False), WHITE)
        text_l(d, sx + 88, y + 13, l2, fit(l2, sw - 98, 11, fn=cond, bold=False), (180, 200, 205))

    # ---- Cards grid: row 2 (5) + row 3 (5) ----
    cards = [
        ("4  ·  ZAPORIZHZHIA  ·  WAR", "Russia strikes Zaporizhzhia; 2 dead, 22 hurt",
         "A five-storey block is destroyed; two children among the injured. (Reuters)", "zap"),
        ("5  ·  MADRID  ·  FOOTBALL", "Real Madrid rout PSV 5-1 to stay perfect",
         "Mbappé scores twice as Madrid win all five group games; City and Arsenal held. (UEFA)", "football"),
        ("6  ·  NEW YORK  ·  MARKETS", "Dow crosses 50,000 as Nvidia slides 5.9%",
         "Dow +0.85% to 50,018.70; Nasdaq -1.48%. Nvidia falls after Monday's 31% surge. (Reuters)", "dow"),
        ("7  ·  WASHINGTON  ·  SANCTIONS", "US hits Iran with new sanctions",
         "Treasury targets dozens of people and firms in Iran's shadow-banking network. (Treasury)", "sanctions"),
        ("8  ·  JERUSALEM  ·  IRAN", "Netanyahu urges Trump to strike Iran",
         "Israel's PM presses Washington for new strikes; Mossad chief said to agree. (Kan)", "podium"),
        ("9  ·  BAGHDAD  ·  OIL", "Iraq seizes Kurdish oilfields and crossings",
         "PM orders federal takeover of Kurdish oilfields and all border crossings. (Reuters)", "oil"),
        ("10  ·  KATHMANDU  ·  QUAKE", "Nepal quake M5.6 shakes Tibet border region",
         "Felt in Kathmandu, Sikkim and Bhutan; no casualties or major damage reported. (Xinhua)", "quake"),
        ("11  ·  VILLAVICENCIO  ·  BLAST", "Car bomb wounds 23 outside governor's office",
         "Blast hits Plaza Los Libertadores; one child among the injured, none killed. (El País)", "bomb"),
        ("12  ·  KHARTOUM  ·  WAR", "Sudan drone attack kills 4 civilians; UN hit",
         "Strikes hit Omdurman and Jebel Awlia; a UN building is damaged, staff unhurt. (OCHA)", "drone"),
        ("13  ·  SEOUL  ·  DEFENCE", "Russian aircraft enters South Korea's ADIZ",
         "Seoul corrects an early report that had claimed an airspace violation. (Daily Summary)", "jet"),
    ]
    cillu = {"zap": illu_zap, "football": illu_football, "dow": illu_dow,
             "sanctions": illu_sanctions24, "podium": illu_podium,
             "oil": illu_oil, "quake": illu_quake, "bomb": illu_bomb,
             "drone": illu_drone, "jet": illu_jet}
    cw2, ch2 = 195, 144
    for i, (kick, title, sub, kind) in enumerate(cards):
        col, row = i % 5, i // 5
        x = 8 + col * (cw2 + 8)
        y = 396 + row * (ch2 + 8)
        d.rectangle([x, y, x + cw2, y + ch2], fill=PAPER2)
        d.rectangle([x, y, x + cw2, y + ch2], outline=TEAL, width=1)
        ix, iy, iw, ih = x + 5, y + 5, cw2 - 10, 46
        cillu[kind](d, ix, iy, iw, ih)
        d.rectangle([ix, iy, ix + 28, iy + 16], fill=ORANGE)
        text_c(d, ix + 14, iy, str(i + 4), cond(12), WHITE)
        ty3 = y + 56
        text_l(d, x + 7, ty3, kick, fit(kick, cw2 - 14, 11), ORANGE)
        ty3 = draw_wrapped(d, x + 7, ty3 + 14, title, cond(14), INK,
                           cw2 - 14, leading=16)
        draw_wrapped(d, x + 7, ty3 + 1, sub, cond(11, bold=False), GREY_DK,
                     cw2 - 14, leading=13)

    # ---- Bottom: briefs (left, 3 cols) + map (right) ----
    by = 700
    bx = 8
    text_l(d, bx, by + 6, "ALSO ON TUESDAY 24 NOVEMBER \u2014 16 MORE STORIES",
           cond(15), ORANGE)
    briefs = [
        (14, "BRUSSELS", "NATO vows to defend against space threats."),
        (15, "KYIV", "Russia fired 153 ballistic missiles in October."),
        (16, "WARSAW", "NATO deploys detection aircraft in Poland."),
        (17, "TEHRAN", "Iran: no talks until US meets seven conditions."),
        (18, "DOHA", "Qatar PM works to revive US–Iran talks."),
        (19, "HORMUZ", "Tankers catch fire after hitting sea mines."),
        (20, "MEXICO", "Mexico to try 'El Chapo Isidro' despite US bid."),
        (21, "SAN SALVADOR", "Bukele names 3 soldiers killed in Haiti."),
        (22, "BEIJING", "China executes official for spying."),
        (23, "PAKISTAN", "Pakistan 325; Sri Lanka all out for 98."),
        (24, "DHAKA", "Paramilitary deployed as Hasina plans return."),
        (25, "SUVA", "Fiji closes all schools for 5 days in drought."),
        (26, "CANBERRA", "Opposition rejects Vanuatu treaty deal."),
        (27, "WELLINGTON", "NZ bank: stop tinkering with mandate."),
        (28, "GOMA", "Fighting traps WHO Ebola team in DR Congo hospital."),
        (29, "JUBA", "South Sudan election 6 weeks away as UN meets."),
    ]
    # 3 columns: 6 + 5 + 5
    col_w = 196
    for i, (num, place, txt) in enumerate(briefs):
        if i < 6:
            col, row = 0, i
        elif i < 11:
            col, row = 1, i - 6
        else:
            col, row = 2, i - 11
        x = bx + col * (col_w + 8)
        y = by + 28 + row * 24
        head = f"{num} {place} \u2014 "
        fh = cond(11)
        d.text((x, y), head, font=fh, fill=ORANGE, anchor="la")
        tx = x + fh.getlength(head)
        maxw = bx + col * (col_w + 8) + col_w - tx
        lines = wrap_text(txt, cond(11, bold=False), maxw)
        for li, line in enumerate(lines[:2]):
            d.text((tx, y + li * 12), line, font=cond(11, bold=False),
                   fill=INK, anchor="la")

    # map
    mx, my, mw, mh = 616, by, 400, 180
    d.rectangle([mx, my, mx + mw, my + mh], fill=TEAL_DK)
    d.rectangle([mx, my, mx + mw, my + mh], outline=TEAL, width=1)
    text_l(d, mx + 10, my + 6, "WHERE IT HAPPENED", cond(15), GOLD)
    text_l(d, mx + 10, my + 22, "pins = the 13 numbered cards",
           cond(11, bold=False), (180, 200, 205))
    land_polys = [
        [(20, 42), (90, 32), (130, 44), (120, 70), (80, 82), (40, 77), (15, 62)],
        [(95, 87), (125, 84), (135, 107), (115, 132), (100, 117)],
        [(185, 40), (215, 34), (230, 46), (215, 60), (190, 56)],
        [(190, 70), (230, 66), (245, 92), (225, 117), (200, 107), (188, 87)],
        [(235, 36), (330, 30), (375, 42), (360, 70), (300, 80), (260, 70), (238, 54)],
        [(330, 110), (365, 106), (370, 122), (340, 126)],
    ]

    def inside(px, py, poly):
        ins = False
        j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if (yi > py) != (yj > py):
                if px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    ins = not ins
            j = i
        return ins

    for gy in range(my + 34, my + mh - 6, 5):
        for gx in range(mx + 8, mx + mw - 8, 5):
            lx, ly = gx - mx, gy - my
            if any(inside(lx, ly, p) for p in land_polys):
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(150, 190, 200))
    # pins: card locations (world-map coords in the 400x180 box)
    pins = [
        (218, 56),   # 1 Gaza
        (300, 48),   # 2 Jiuquan (NW China)
        (330, 78),   # 3 Cikande (Indonesia)
        (206, 40),   # 4 Zaporizhzhia (Ukraine)
        (188, 52),   # 5 Madrid (Spain)
        (112, 50),   # 6 New York (US east)
        (100, 62),   # 7 Washington (US east)
        (232, 68),   # 8 Jerusalem
        (244, 52),   # 9 Baghdad (Iraq)
        (285, 62),   # 10 Kathmandu (Nepal)
        (105, 92),   # 11 Villavicencio (Colombia)
        (225, 88),   # 12 Khartoum (Sudan)
        (345, 48),   # 13 Seoul (South Korea)
    ]
    for i, (px, py) in enumerate(pins, start=1):
        ax, ay = mx + px, my + py
        d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=ORANGE,
                  outline=WHITE, width=1)
        text_c(d, ax, ay - 8, str(i), cond(11), WHITE)

    # ---- Date check ----
    dy = 888
    d.rectangle([8, dy, 1015, dy + 46], outline=ORANGE, width=2)
    dc1 = "DATE CHECK \u2014 FIRST REPORTED ON ANOTHER DAY, SO NOT ON THIS PAGE AS NEWS:"
    dc2 = ("COP31 collapse itself (Sun 22 Nov)  \u00b7  ICJ Rohingya verdict "
           "(Thu 19 Nov)  \u00b7  Nvidia +31% (Mon 23 Nov)  \u00b7  Saudi strike "
           "on Hodeida (Mon 23 Nov)  \u00b7  EU 22nd Russia sanctions (Mon 23 "
           "Nov)  \u00b7  Democrats reach 258 seats (Sun 22 Nov)  \u00b7  Merkury "
           "sunk in Libya (Sun 22\u2013Mon 23 Nov)  \u00b7  \u2018El Chapo Isidro\u2019 "
           "captured (Fri 21 Nov)  \u00b7  Verstappen wins Las Vegas GP (Sat 22 "
           "Nov)  \u00b7  Factory fire breaks out (Sat 21 Nov).")
    text_l(d, 16, dy + 3, dc1, fit(dc1, 984, 12), TEAL)
    draw_wrapped(d, 16, dy + 18, dc2, cond(11, bold=False), GREY_DK, 984,
                 leading=13)

    # ---- Footer ----
    foot = ("Every story here happened, or was first reported, on Tuesday 24 November 2026. "
            "Disputed claims are attributed, not stated as fact.  Sources: Reuters, AP, BBC, "
            "Xinhua, The Hindu, Daily Summary and the wires named with each story.")
    text_c(d, 512, 942, foot, fit(foot, 990, 11, fn=cond, bold=False), GREY)
    text_c(d, 512, 956, "CERTAINTY:  REPORTED = carried by the day's wires   \u00b7   "
           "CLAIM = one side's account, labelled as such",
           fit("CERTAINTY:  REPORTED = carried by the day's wires   \u00b7   "
               "CLAIM = one side's account, labelled as such", 990, 11), TEAL)

    img.save(OUT, "PNG", optimize=True)
    print(OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the 25 November 2026 front page for make.fun news-image-20261125.

Fresh script written for this day only: masthead, Ukraine-war lead with a
drawn scale bar, two middle panels (Huawei verdict, Shenzhou-24), three
bottom columns (China purge, Abrego Garcia, Gaza), a By-numbers band, an
Also-today strip and a footer. Pillow only, no network, no randomness:
the same input always produces the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 32
INK = (18, 18, 18)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
GREY = (90, 90, 88)
LIGHT_GREY = (200, 198, 190)
NAVY = (24, 48, 96)
GOLD = (176, 141, 26)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fnt, fill=RED):
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- top dateline band -------------------------------------------------
    f_small = font(SANS, 15)
    f_small_b = font(SANS_B, 15)
    d.text((x0, 18), "WEDNESDAY 25 NOVEMBER 2026", font=f_small_b, fill=INK)
    right = "No. 329  •  LONDON  •  PRICE: FREE"
    d.text((x1 - d.textlength(right, font=f_small), 18), right,
           font=f_small, fill=GREY)
    hrule(d, x0, x1, 44, 2)

    # ---- masthead -----------------------------------------------------------
    f_mast = font(SERIF_B, 88)
    title = "THE WORLD"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 52), title,
           font=f_mast, fill=INK)
    f_tag = font(SERIF, 19)
    tag = "One day. One picture. All the news that matters."
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 142), tag,
           font=f_tag, fill=GREY)
    hrule(d, x0, x1, 172, 3)
    hrule(d, x0, x1, 178, 1)

    # ---- LEAD: Ukraine war deaths -------------------------------------------
    y = 192
    f_kick = font(SANS_B, 16)
    y = kicker(d, x0, y, "UKRAINE WAR  •  LEAD STORY", f_kick)
    f_head = font(SERIF_B, 36)
    head = "Russia's own figures put the war dead at nearly 500,000"
    y = para(d, x0, y, head, f_head, x1 - x0, 42)
    y += 4
    # standfirst
    f_stand = font(SERIF, 19)
    stand = ("Moscow's official statistics point to a death toll far higher "
             "than the Kremlin has admitted — as the war grinds on.")
    y = para(d, x0, y, stand, f_stand, x1 - x0, 25)
    y += 8

    # lead body (left) + drawn scale bar (right)
    lead_top = y
    body_w = 560
    f_body = font(SANS, 16)
    body = ("Russia's own published figures show almost 500,000 deaths in "
            "the war in Ukraine, according to a BBC analysis of the official "
            "data released on Wednesday. The toll is the clearest picture "
            "yet of the human cost of the invasion, as fighting continues "
            "along the front.")
    y = para(d, x0, lead_top, body, f_body, body_w, 22)
    src = font(SANS, 13)
    d.text((x0, y + 4), "Source: BBC, 25 November 2026", font=src, fill=GREY)

    # scale bar graphic, right of the body
    gx0, gx1 = x0 + body_w + 24, x1
    gy = lead_top + 2
    f_gtitle = font(SANS_B, 15)
    d.text((gx0, gy), "THE TOLL, IN MOSCOW'S OWN FIGURES", font=f_gtitle, fill=INK)
    gy += 30
    # horizontal bar to 500,000 with 100k ticks
    bar_x0, bar_x1 = gx0, gx1
    bar_y = gy + 8
    d.rectangle([bar_x0, bar_y, bar_x1, bar_y + 34], fill=DARKRED)
    d.text((bar_x0 + 8, bar_y + 5), "≈ 500,000 DEAD", font=font(SANS_B, 18),
           fill=(255, 255, 255))
    gy = bar_y + 44
    for i in range(6):
        tx = bar_x0 + (bar_x1 - bar_x0) * i / 5
        d.line([(tx, gy), (tx, gy + 6)], fill=INK, width=2)
        lab = "0" if i == 0 else f"{i}00k"
        d.text((tx - d.textlength(lab, font=font(SANS, 12)) / 2, gy + 8),
               lab, font=font(SANS, 12), fill=GREY)
    gy += 26
    d.text((gx0, gy), "Each 100k mark: another 100,000 lives, by Russia's count.",
           font=font(SANS, 13), fill=GREY)

    lead_bottom = max(y + 20, gy + 34)
    hrule(d, x0, x1, lead_bottom, 2)

    # ---- MIDDLE ROW: two panels ----------------------------------------------
    y = lead_bottom + 12
    mid_h = 164
    col_w = (x1 - x0 - 24) // 2
    # left panel: Huawei
    px = x0
    y2 = kicker(d, px, y, "TECH  •  UNITED STATES", f_kick)
    f_h2 = font(SERIF_B, 24)
    y2 = para(d, px, y2, "Huawei guilty of stealing US trade secrets",
              f_h2, col_w - 150, 29)
    y2 = para(d, px, y2 + 2,
              "A US jury convicts the Chinese telecoms giant — but clears "
              "it of racketeering.",
              font(SANS, 15), col_w - 150, 21)
    # drawn chip graphic, right of left panel text
    cx0, cy0 = px + col_w - 138, y + 34
    d.rectangle([cx0 + 14, cy0 + 14, cx0 + 124, cy0 + 110], outline=NAVY, width=4)
    d.rectangle([cx0 + 34, cy0 + 34, cx0 + 104, cy0 + 90], fill=NAVY)
    hw = "HUAWEI"
    hwf = font(SANS_B, 12)
    d.text((cx0 + 69 - d.textlength(hw, font=hwf) / 2, cy0 + 56), hw,
           font=hwf, fill=(255, 255, 255))
    for i in range(4):
        d.line([(cx0 + 24 + i * 26, cy0 + 4), (cx0 + 24 + i * 26, cy0 + 14)],
               fill=NAVY, width=3)
        d.line([(cx0 + 24 + i * 26, cy0 + 110), (cx0 + 24 + i * 26, cy0 + 120)],
               fill=NAVY, width=3)
    # right panel: Shenzhou-24
    px = x0 + col_w + 24
    d.line([(px - 12, y), (px - 12, y + mid_h)], fill=LIGHT_GREY, width=2)
    y2 = kicker(d, px, y, "SPACE  •  CHINA", f_kick)
    y2 = para(d, px, y2, "Pakistan's first astronaut rides Shenzhou-24 into orbit",
              f_h2, col_w - 150, 29)
    y2 = para(d, px, y2 + 2,
              "Muhammad Zeeshan Ali is the first foreigner on a Chinese "
              "crewed mission.",
              font(SANS, 15), col_w - 150, 21)
    # drawn rocket graphic
    rx0, ry0 = px + col_w - 138, y + 26
    d.ellipse([rx0 + 30, ry0 + 96, rx0 + 108, ry0 + 128], outline=GOLD, width=2)
    d.polygon([(rx0 + 69, ry0 + 6), (rx0 + 49, ry0 + 46), (rx0 + 89, ry0 + 46)],
              fill=RED)
    d.rectangle([rx0 + 49, ry0 + 46, rx0 + 89, ry0 + 104], fill=INK)
    d.polygon([(rx0 + 49, ry0 + 84), (rx0 + 29, ry0 + 116), (rx0 + 49, ry0 + 104)],
              fill=RED)
    d.polygon([(rx0 + 89, ry0 + 84), (rx0 + 109, ry0 + 116), (rx0 + 89, ry0 + 104)],
              fill=RED)
    d.ellipse([rx0 + 61, ry0 + 58, rx0 + 77, ry0 + 74], fill=(255, 255, 255))
    d.polygon([(rx0 + 63, ry0 + 104), (rx0 + 75, ry0 + 104), (rx0 + 69, ry0 + 122)],
              fill=GOLD)
    for sx, sy in [(rx0 + 8, ry0 + 18), (rx0 + 122, ry0 + 30), (rx0 + 16, ry0 + 70)]:
        d.text((sx, sy), "*", font=font(SANS_B, 18), fill=GOLD)

    y = lead_bottom + 12 + mid_h
    hrule(d, x0, x1, y, 2)

    # ---- BOTTOM ROW: three columns -------------------------------------------
    y += 12
    col3_w = (x1 - x0 - 48) // 3
    f_h3 = font(SERIF_B, 21)
    f_b3 = font(SANS, 15)
    cols = [
        ("CHINA  •  POLITICS",
         "Beijing purge widens as Politburo member probed",
         "Shanghai party chief Chen Jining is investigated — the fourth "
         "Politburo inquiry since 2025. (Reuters)"),
        ("UNITED STATES",
         "Ábrego García flies to Spain as deportation battle ends",
         "Kilmar Ábrego García leaves the US for Spain, closing a case "
         "that became a symbol of the crackdown. (BBC)"),
        ("GAZA  •  MIDDLE EAST",
         "Israeli strike kills Hamas security chief in Gaza",
         "An Israeli air strike kills Hamas's internal security chief, as "
         "land-mine casualties soar across Syria. (BBC)"),
    ]
    max_y = y
    for i, (kick, head, text) in enumerate(cols):
        cx = x0 + i * (col3_w + 24)
        if i:
            d.line([(cx - 12, y), (cx - 12, y + 150)], fill=LIGHT_GREY, width=2)
        yy = kicker(d, cx, y, kick, font(SANS_B, 13))
        yy = para(d, cx, yy, head, f_h3, col3_w, 25)
        yy = para(d, cx, yy + 2, text, f_b3, col3_w, 20)
        max_y = max(max_y, yy)
    y = max_y + 8
    hrule(d, x0, x1, y, 2)

    # ---- BY NUMBERS band ------------------------------------------------------
    y += 8
    f_num = font(SERIF_B, 26)
    f_numlab = font(SANS, 12)
    stats = [
        ("500,000", "war dead in Russia's own figures"),
        ("-6%", "Nvidia shares as the bounce fades"),
        ("1st", "Pakistani astronaut in space"),
        ("4th", "Politburo member probed since 2025"),
    ]
    cell_w = (x1 - x0) // 4
    d.text((x0, y), "BY NUMBERS", font=font(SANS_B, 13), fill=RED)
    y += 20
    for i, (num, lab) in enumerate(stats):
        cx = x0 + i * cell_w
        d.text((cx, y), num, font=f_num, fill=NAVY)
        yy = y + 32
        yy = para(d, cx, yy, lab, f_numlab, cell_w - 16, 15, fill=GREY)
    y += 32 + 26
    hrule(d, x0, x1, y, 2)

    # ---- ALSO TODAY strip ------------------------------------------------------
    y += 10
    f_also = font(SANS, 15)
    also = ("ALSO TODAY:  Microsoft declares 'Code Red' after a historic "
            "outage  •  US set to unveil new tariffs on 16 partners  •  "
            "Sarkozy and Carla Bruni to face trial  •  Senegal reinstated as "
            "2025 Africa Cup winners  •  Hera returns to the asteroid site")
    y = para(d, x0, y, also, f_also, x1 - x0, 19)
    y += 6
    hrule(d, x0, x1, y, 3)

    # ---- footer ----------------------------------------------------------------
    y += 8
    f_foot = font(SANS, 13)
    d.text((x0, y), "Sources: BBC, Reuters — Wednesday 25 November 2026",
           font=f_foot, fill=GREY)
    foot_r = "THE WORLD  •  25 NOVEMBER 2026"
    d.text((x1 - d.textlength(foot_r, font=f_foot), y), foot_r,
           font=f_foot, fill=GREY)
    y += 18
    assert y <= H, f"layout overflow: final y {y} > {H}"
    print(f"final y = {y} (limit {H})")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

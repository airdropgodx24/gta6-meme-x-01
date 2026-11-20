#!/usr/bin/env python3
"""Draw the GTA 6 launch-week meme for the make.fun gta6-meme-x-01 entry.

Everything in the picture is drawn here, in code, from basic shapes:
a Leonida sunset skyline, palm trees, a gamer calling in with a bad case
of "Leonida flu", and make.fun's ghost mascot worked into the scene as
his co-worker, holding its magenta star coin. No image files are loaded.

Output: meme.png (1200 x 1200) next to this script.
"""

from math import cos, pi, sin

from PIL import Image, ImageDraw, ImageFont

W = 1200
H = 1200
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (224, 33, 138)
DARK = (24, 16, 40)
WHITE = (255, 255, 255)
BLACK = (10, 10, 12)


def font(size):
    return ImageFont.truetype(FONT, size)


def fit_font(draw, text, max_width, start):
    """Shrink a bold font until the text fits max_width."""
    size = start
    while size > 18:
        f = font(size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
        size -= 4
    return font(size)


def centred(draw, cx, y, text, f, fill, stroke=0, stroke_fill=BLACK):
    box = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
    draw.text((cx - (box[2] - box[0]) / 2 - box[0], y), text,
              font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def sparkle(draw, cx, cy, r, fill):
    """A four-pointed sparkle / star, the shape of the ghost's eyes."""
    pts = []
    for i in range(8):
        ang = pi / 2 * (i // 2) + (pi / 4 if i % 2 == 0 else 0)
        # alternate long points (cardinal) with short inner corners
        if i % 2 == 0:
            rad, a = r, pi / 4 * i
        else:
            rad, a = r * 0.28, pi / 4 * i
        pts.append((cx + rad * cos(a), cy - rad * sin(a)))
    draw.polygon(pts, fill=fill)


def star(draw, cx, cy, r, fill):
    """A plain five-pointed star, for the coin the ghost holds."""
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -pi / 2 + pi / 5 * i
        pts.append((cx + rad * cos(a), cy + rad * sin(a)))
    draw.polygon(pts, fill=fill)


def sunset(draw):
    top = (255, 138, 76)
    mid = (255, 62, 130)
    low = (96, 44, 150)
    y0, y1 = 148, 1018
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        if t < 0.55:
            s = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * s) for i in range(3))
        else:
            s = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (low[i] - mid[i]) * s) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)
    # the low Leonida sun
    draw.ellipse([812, 268, 1032, 488], fill=(255, 222, 130))
    draw.ellipse([832, 288, 1012, 468], fill=(255, 236, 165))


def skyline(draw):
    base = 872
    buildings = [
        (0, 560, 120), (118, 500, 96), (214, 596, 130), (344, 470, 88),
        (432, 556, 118), (980, 520, 104), (1084, 584, 116),
    ]
    for x, top, w in buildings:
        draw.rectangle([x, top, x + w, base], fill=(43, 24, 74))
        for wy in range(top + 22, base - 26, 42):
            for wx in range(x + 14, x + w - 18, 30):
                if (wx * 7 + wy * 13) % 5 in (0, 2):
                    draw.rectangle([wx, wy, wx + 12, wy + 16],
                                   fill=(255, 205, 92))
    # sand strip the characters stand on
    draw.rectangle([0, base, W, 1018], fill=(238, 196, 118))
    draw.rectangle([0, base, W, base + 10], fill=(255, 226, 155))


def palm(draw, x, base, h, lean):
    pts = []
    steps = 24
    for i in range(steps + 1):
        t = i / steps
        pts.append((x + lean * t * t, base - h * t))
    draw.line(pts, fill=(52, 32, 24), width=17)
    tx, ty = pts[-1]
    # fronds: simple drooping curves out of the crown, drawn point by point
    for dx, dy, droop in ((-120, -34, 58), (-86, -64, 44), (-34, -84, 30),
                          (34, -84, 30), (86, -64, 44), (120, -34, 58)):
        frond = []
        for i in range(17):
            t = i / 16
            fx = tx + dx * t
            fy = ty + dy * t + droop * t * t
            frond.append((fx, fy))
        draw.line(frond, fill=(24, 92, 52), width=11)


def neon_sign(draw):
    # a beachfront club sign that is part of the skyline, not a sticker:
    # a dark board high on the left-hand building, above the gamer's head,
    # carrying the make.fun name where nothing in the scene covers it
    draw.rounded_rectangle([24, 366, 360, 494], radius=18,
                           fill=(18, 10, 34), outline=MAGENTA, width=7)
    f = fit_font(draw, "make.fun", 300, 64)
    centred(draw, 192, 388, "make.fun", f, WHITE)
    f2 = font(25)
    centred(draw, 192, 456, "LEONIDA BEACH CLUB", f2, (255, 205, 92))


def ghost(draw, cx, top):
    """make.fun's mascot: a white ghost, thick black outline, sparkle
    eyes, a round little hand, holding a magenta coin with a white star."""
    w, h = 330, 372
    left, right = cx - w // 2, cx + w // 2
    bottom = top + h
    # body: domed top, straight sides, wavy hem. The dome is filled
    # without an outline first (a pieslice outline would draw a straight
    # chord across the ghost's face), then its arc is stroked on its own.
    draw.pieslice([left, top, right, top + w], start=180, end=0, fill=WHITE)
    draw.rectangle([left, top + w // 2, right, bottom - 34], fill=WHITE)
    draw.arc([left, top, right, top + w], start=180, end=0,
             fill=BLACK, width=10)
    draw.line([(left, top + w // 2), (left, bottom - 34)], fill=BLACK, width=10)
    draw.line([(right, top + w // 2), (right, bottom - 34)], fill=BLACK, width=10)
    bumps = 5
    bw = w / bumps
    for i in range(bumps):
        bx = left + bw * i
        draw.ellipse([bx, bottom - 68, bx + bw, bottom], fill=WHITE)
    draw.arc([left, bottom - 70, left + bw, bottom - 2], 0, 180, fill=BLACK, width=9)
    for i in range(1, bumps):
        bx = left + bw * i
        draw.arc([bx, bottom - 70, bx + bw, bottom - 2], 0, 180, fill=BLACK, width=9)
    draw.line([(left, bottom - 36), (left + 4, bottom - 36)], fill=BLACK, width=9)
    draw.line([(right - 4, bottom - 36), (right, bottom - 36)], fill=BLACK, width=9)
    # sparkle eyes
    sparkle(draw, cx - 62, top + 148, 40, BLACK)
    sparkle(draw, cx + 62, top + 148, 40, BLACK)
    # a small pleased mouth
    draw.arc([cx - 26, top + 176, cx + 26, top + 224], 15, 165,
             fill=BLACK, width=8)
    # the round little hand, out to the side, holding the coin up
    hx, hy = right - 6, top + 252
    draw.ellipse([hx - 6, hy - 30, hx + 54, hy + 30], fill=WHITE,
                 outline=BLACK, width=9)
    # magenta coin with a white star
    coin_cx, coin_cy, coin_r = hx + 88, hy - 6, 62
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r,
                  coin_cx + coin_r, coin_cy + coin_r],
                 fill=MAGENTA, outline=BLACK, width=8)
    star(draw, coin_cx, coin_cy, 34, WHITE)


def gamer(draw):
    # body in a teal hoodie, seated on the sand at the left
    draw.rounded_rectangle([118, 700, 356, 1004], radius=54,
                           fill=(18, 138, 148), outline=BLACK, width=8)
    # head
    draw.ellipse([162, 528, 312, 678], fill=(198, 138, 92),
                 outline=BLACK, width=8)
    # hair cap
    draw.pieslice([162, 514, 312, 640], start=180, end=0, fill=(30, 22, 20))
    # headphones: band and two pads
    draw.arc([150, 500, 324, 660], start=180, end=360, fill=BLACK, width=13)
    draw.rounded_rectangle([140, 586, 176, 656], radius=12, fill=BLACK)
    draw.rounded_rectangle([298, 586, 334, 656], radius=12, fill=BLACK)
    # wide eyes and an unconvincing sick frown
    draw.ellipse([198, 596, 216, 618], fill=BLACK)
    draw.ellipse([256, 596, 274, 618], fill=BLACK)
    draw.arc([208, 636, 266, 676], start=200, end=340, fill=BLACK, width=6)
    # thermometer poking out of the mouth corner, purely for sympathy
    draw.line([(272, 652), (330, 676)], fill=WHITE, width=10)
    draw.line([(272, 652), (330, 676)], fill=BLACK, width=2)
    draw.ellipse([322, 666, 342, 686], fill=(230, 40, 60))
    # arms down to a controller held in both hands
    draw.line([(150, 780), (228, 884)], fill=(18, 138, 148), width=40)
    draw.line([(324, 780), (252, 884)], fill=(18, 138, 148), width=40)
    draw.rounded_rectangle([176, 862, 302, 922], radius=28, fill=(22, 22, 28),
                           outline=BLACK, width=6)
    draw.ellipse([198, 884, 214, 900], fill=MAGENTA)
    draw.ellipse([262, 880, 276, 894], fill=(255, 205, 92))


def speech_bubble(draw):
    box = [352, 452, 842, 622]
    draw.rounded_rectangle(box, radius=30, fill=WHITE, outline=BLACK, width=8)
    draw.polygon([(430, 618), (392, 700), (500, 622)], fill=WHITE)
    draw.line([(430, 618), (392, 700)], fill=BLACK, width=8)
    draw.line([(392, 700), (500, 622)], fill=BLACK, width=8)
    f = fit_font(draw, "Tell my boss I have", 450, 42)
    centred(draw, 597, 478, "Tell my boss I have", f, BLACK)
    f2 = fit_font(draw, "LEONIDA FLU.", 450, 54)
    centred(draw, 597, 534, "LEONIDA FLU.", f2, MAGENTA)


def main():
    img = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    sunset(draw)
    skyline(draw)
    palm(draw, 66, 880, 300, 54)
    palm(draw, 1136, 880, 330, -60)
    neon_sign(draw)
    gamer(draw)
    ghost(draw, 878, 560)
    speech_bubble(draw)
    # caption bars, top and bottom, in the classic meme style
    draw.rectangle([0, 0, W, 148], fill=BLACK)
    f = fit_font(draw, "GTA 6 LAUNCH DAY:", 1120, 84)
    centred(draw, W // 2, 30, "GTA 6 LAUNCH DAY:", f, WHITE)
    draw.rectangle([0, 1018, W, H], fill=BLACK)
    line1 = "WAITED 13 YEARS. SICK IN ONE DAY."
    f = fit_font(draw, line1, 1120, 66)
    centred(draw, W // 2, 1046, line1, f, WHITE)
    line2 = "Symptoms: Leonida flu. Cure: launch week."
    f2 = fit_font(draw, line2, 1120, 48)
    centred(draw, W // 2, 1128, line2, f2, (255, 205, 92))
    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()

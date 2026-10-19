#!/usr/bin/env python3
"""Build the STAR Lab Polaris identity as SVG, PDF, PNG, icons, and favicon.

STAR stands for System Trustworthiness and AI Reliability. The mark is a
tall, faceted Polaris (the North Star: a fixed point people trust to
navigate by), split down the middle. The navy half carries a program graph
of square modules with right-angle wiring (software systems); the sky-blue
half carries a neural network of round neurons with diagonal links (AI).

Usage:  python3 make-logo.py [output-dir]     (default: this directory)

Regeneration needs rsvg-convert and pdftocairo. STAR LAB is drawn as custom
paths; only the full-name line of the signature uses Arial, and it is
converted to outlines, so the outputs need no fonts.
"""
from pathlib import Path
import math
import struct
import subprocess
import sys

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)
WORK = OUT / ".build"
OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(exist_ok=True)

NAVY, SKY, WHITE, INK = "#0A2463", "#82C3F0", "#FFFFFF", "#1A1A1A"
FULL_NAME = "System Trustworthiness and AI Reliability"

# Polaris geometry in a 104-unit box: rays clockwise from north.
CX = CY = 52
RAYS = (50, 20, 38, 20, 50, 20, 38, 20)
VALLEY = 20
GAP = 1.3          # each half moves this far from the center line
SYMBOL_SCALE = .7


def mix(color, other, t):
    a = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def poly(points):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in points) + " Z"


def ray_points():
    points = []
    for k in range(8):
        a = math.radians(-90 + 45 * k)
        points.append((CX + RAYS[k] * math.cos(a), CY + RAYS[k] * math.sin(a)))
        a = math.radians(-90 + 45 * k + 22.5)
        points.append((CX + VALLEY * math.cos(a), CY + VALLEY * math.sin(a)))
    return points


def halves():
    """Split each ray into two facets and sort them into left/right halves."""
    points, left, right = ray_points(), [], []
    for k in range(8):
        tip = points[2 * k]
        for first, valley in ((True, points[2 * k - 1]), (False, points[2 * k + 1])):
            facet = poly([(CX, CY), tip, valley])
            (left if (tip[0] + valley[0] + CX) / 3 < CX else right).append((first, facet))
    return left, right


def emblem(left_dark, left_light, right_dark, right_light,
           left_symbol, right_symbol, symbols=True):
    left, right = halves()
    def paint(facets, dark, light):
        return "".join(f'<path fill="{dark if first else light}" d="{d}"/>' for first, d in facets)
    out = (f'<g transform="translate({-GAP} 0)">{paint(left, left_dark, left_light)}'
           + (program_graph(left_symbol) if symbols else "") + "</g>"
           f'<g transform="translate({GAP} 0)">{paint(right, right_dark, right_light)}'
           + (neural_net(right_symbol) if symbols else "") + "</g>")
    return out


def scaled(content):
    return (f'<g transform="translate({CX} {CY}) scale({SYMBOL_SCALE}) '
            f'translate({-CX} {-CY})">{content}</g>')


def program_graph(color):
    """Software: square modules joined by right-angle wiring (two feed one)."""
    wire = (f'<path d="M{CX-7.5} {CY-8} H{CX-12} V{CY+8} H{CX-7.5} M{CX-12} {CY} H{CX-16}" '
            f'fill="none" stroke="{color}" stroke-width="2.4"/>')
    boxes = "".join(f'<rect x="{CX+x-3.4}" y="{CY+y-3.4}" width="6.8" height="6.8" rx="1.2" fill="{color}"/>'
                    for x, y in [(-7.5, -8), (-7.5, 8), (-16, 0)])
    return scaled(wire + boxes)


def neural_net(color):
    """AI: round neurons joined by diagonal links (two feed one)."""
    links = (f'<path d="M{CX+7.5} {CY-8} L{CX+16} {CY} M{CX+7.5} {CY+8} L{CX+16} {CY}" '
             f'fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')
    neurons = "".join(f'<circle cx="{CX+x}" cy="{CY+y}" r="3.6" fill="{color}"/>'
                      for x, y in [(7.5, -8), (7.5, 8), (16, 0)])
    return scaled(links + neurons)


VARIANTS = {
    # name: (left dark, left light, right dark, right light, left symbol, right symbol, word color)
    "": (NAVY, mix(NAVY, WHITE, .16), mix(SKY, NAVY, .16), SKY, WHITE, NAVY, NAVY),
    "-mono": (INK, INK, INK, INK, WHITE, WHITE, INK),
    "-reverse": (WHITE, mix(WHITE, NAVY, .1), mix(SKY, NAVY, .12), SKY, NAVY, NAVY, WHITE),
}


def lettering(primary, shift=0):
    # Custom geometric letters share a 56-unit cap height and 10-12-unit
    # strokes. Angled S/T terminals give the wordmark its movement; the A
    # carries a small star-shaped counter.
    s = '''M46 4 C39 0 31 -1 24 -1 C9 -1 1 6 1 16
      C1 26 9 30 22 33 L29 35 C34 36 36 38 36 41
      C36 45 32 47 25 47 C17 47 10 44 5 40 L0 49
      C6 54 15 57 24 57 C39 57 48 50 48 39 C48 28 40 24 27 21
      L20 19 C15 18 12 16 12 13 C12 10 16 8 23 8 C30 8 36 10 41 13 Z'''
    t = 'M0 0 H48 L45 10 H30 V56 H18 V10 H0 Z'
    a = '''M0 56 L21 0 H34 L55 56 H42 L37.5 43 H17.5 L13 56 Z
      M27.5 13 L30 21 Q31 24 34 25 L38 27 L34 29 Q31 30 30 33
      L27.5 39 L25 33 Q24 30 21 29 L17 27 L21 25 Q24 24 25 21 Z'''
    r = '''M0 0 H25 C40 0 48 6 48 17 C48 26 43 31 36 33
      L51 56 H37 L24 35 H12 V56 H0 Z
      M12 10 V25 H24 C32 25 36 22 36 17 C36 12 32 10 24 10 Z'''
    lab_l = 'M0 0 H3.7 V25 H18 V28.5 H0 Z'
    lab_a = '''M0 28.5 L11 0 H15 L26 28.5 H22 L18.9 20.5 H7.1 L4 28.5 Z
      M8.5 17 H17.5 L13 4.8 Z'''
    lab_b = '''M0 0 H11 C18 0 21 3.5 21 7.4 C21 10.6 19 12.8 16.5 13.5
      C20.5 14.4 23 16.7 23 20.4 C23 25.5 19.2 28.5 12 28.5 H0 Z
      M3.7 3.4 V12.2 H10.5 C15.2 12.2 17.4 10.7 17.4 7.8
      C17.4 4.9 15.2 3.4 10.5 3.4 Z
      M3.7 15.5 V25.1 H11.7 C16.6 25.1 19.3 23.6 19.3 20.3
      C19.3 17.1 16.6 15.5 11.7 15.5 Z'''
    star = ''.join(f'<path transform="translate({x} 0)" d="{path}"/>'
                   for x, path in [(0, s), (54, t), (100, a), (163, r)])
    lab = ''.join(f'<path transform="translate({x} 0)" d="{path}"/>'
                  for x, path in [(0, lab_l), (23, lab_a), (54, lab_b)])
    return (f'<g fill="{primary}" fill-rule="evenodd" transform="translate({TEXT_X} {shift})">'
            f'<g transform="translate(0 24)">{star}</g>'
            f'<g transform="translate(232 56.06) scale(.84)">{lab}</g></g>')


# The mark spans x 13-91 of its box; lockups shift it flush left.
MARK_SHIFT, TEXT_X = -12.5, 94
LOCKUP_W = 406


def document(contents, width, height, title, description):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" '
            'viewBox="0 0 %s %s" role="img" aria-labelledby="title desc">'
            '<title id="title">%s</title><desc id="desc">%s</desc>%s</svg>' %
            (width, height, width, height, title, description, contents))


def export(name, svg, width, outline=False):
    source = WORK / (name + "-source.svg")
    source.write_text(svg)
    pdf = OUT / (name + ".pdf")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(source)], check=True)
    destination = OUT / (name + ".svg")
    if outline:
        # Cairo converts the full-name line to glyph outlines.
        subprocess.run(["pdftocairo", "-svg", str(pdf), str(destination)], check=True)
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(destination)], check=True)
    else:
        destination.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(width), "-o",
                    str(OUT / (name + ".png")), str(destination)], check=True)


DESC = ("A faceted Polaris split in two: a program graph for software systems "
        "and a neural network for AI. ")

for suffix, (ld, ll, rd, rl, ls, rs, word) in VARIANTS.items():
    mark = emblem(ld, ll, rd, rl, ls, rs)
    export("star-mark" + suffix, document(mark, 104, 104, "STAR Lab Polaris", DESC + FULL_NAME), 1040)
    export("star-mark-small" + suffix,
           document(emblem(ld, ll, rd, rl, ls, rs, symbols=False), 104, 104,
                    "STAR Lab Polaris, small", "Symbol-free variant for 16-32 pixel icons."), 1040)
    placed = f'<g transform="translate({MARK_SHIFT} 0)">{mark}</g>'
    export("star-lockup" + suffix,
           document(placed + lettering(word), LOCKUP_W, 104, "STAR Lab", DESC + FULL_NAME),
           round(2240 * LOCKUP_W / 432))
    signature = (placed + lettering(word, shift=-8) +
                 f'<text x="{TEXT_X}" y="99" fill="{word}" font-family="Arial, sans-serif" '
                 f'font-size="14.5" font-weight="400">{FULL_NAME}</text>')
    export("star-signature" + suffix,
           document(signature, LOCKUP_W, 104, "STAR Lab - " + FULL_NAME,
                    "The full lab signature for larger uses."),
           round(2240 * LOCKUP_W / 432), outline=True)

# Native vector rendering for app icons; the small mark below 48 pixels.
for size in [16, 24, 32, 48, 64, 128, 256]:
    source = OUT / ("star-mark-small.svg" if size <= 32 else "star-mark.svg")
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    "-o", str(OUT / f"star-icon-{size}.png"), str(source)], check=True)
icon_sizes = [16, 32, 48]
icon_data = [(OUT / f"star-icon-{size}.png").read_bytes() for size in icon_sizes]
offset = 6 + 16 * len(icon_sizes)
entries = []
for size, payload in zip(icon_sizes, icon_data):
    entries.append(struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(payload), offset))
    offset += len(payload)
(OUT / "star-favicon.ico").write_bytes(
    struct.pack("<HHH", 0, 1, len(icon_sizes)) + b"".join(entries) + b"".join(icon_data))

# Square avatar for GitHub and social previews; safe inside a circular crop.
avatar = (f'<rect width="104" height="104" fill="{WHITE}"/>'
          f'<g transform="translate(52 52) scale(.8) translate(-52 -52)">'
          + emblem(*VARIANTS[""][:6]) + '</g>')
(WORK / "avatar.svg").write_text(document(avatar, 104, 104, "STAR Lab", FULL_NAME))
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", "-o",
                str(OUT / "star-github-avatar.png"), str(WORK / "avatar.svg")], check=True)

# Review sheet: large mark, signature, small sizes, one color, and on dark.
c = VARIANTS[""]
sheet = ('<rect width="1280" height="700" fill="white"/>'
         '<text x="72" y="56" font-family="Arial, sans-serif" font-size="12" '
         'letter-spacing="1.4" fill="#5C6577">STAR LAB / POLARIS IDENTITY</text>'
         f'<g transform="translate(60 80) scale(2.9)">{emblem(*c[:6])}</g>'
         f'<g transform="translate(420 130) scale(1.9)"><g transform="translate({MARK_SHIFT} 0)">'
         f'{emblem(*c[:6])}</g>{lettering(NAVY, shift=-8)}'
         f'<text x="{TEXT_X}" y="99" fill="{NAVY}" font-family="Arial, sans-serif" '
         f'font-size="14.5">{FULL_NAME}</text></g>'
         '<path d="M72 420 H1208" stroke="#D3DBE7"/>'
         '<text x="72" y="466" font-family="Arial, sans-serif" font-size="11" '
         'letter-spacing="1" fill="#5C6577">SMALL SIZES</text>'
         '<text x="440" y="466" font-family="Arial, sans-serif" font-size="11" '
         'letter-spacing="1" fill="#5C6577">ONE COLOR</text>')
for size, x in [(16, 72), (24, 112), (32, 160), (48, 216), (64, 288)]:
    sheet += (f'<g transform="translate({x} {560-size}) scale({size/104})">'
              + emblem(*c[:6], symbols=size > 32) + '</g>'
              f'<text x="{x}" y="584" font-family="Arial, sans-serif" font-size="12" '
              f'fill="#5C6577">{size}px</text>')
m = VARIANTS["-mono"]
r = VARIANTS["-reverse"]
sheet += (f'<g transform="translate(430 486) scale(.75)"><g transform="translate({MARK_SHIFT} 0)">'
          f'{emblem(*m[:6])}</g>{lettering(INK)}</g>'
          f'<rect x="808" y="446" width="400" height="190" rx="14" fill="{NAVY}"/>'
          '<text x="830" y="474" font-family="Arial, sans-serif" font-size="11" '
          'letter-spacing="1" fill="white">ON DARK</text>'
          f'<g transform="translate(836 500) scale(.82)"><g transform="translate({MARK_SHIFT} 0)">'
          f'{emblem(*r[:6])}</g>{lettering(WHITE)}</g>')
(WORK / "preview.svg").write_text(document(sheet, 1280, 700, "STAR Lab identity", FULL_NAME))
subprocess.run(["rsvg-convert", "-o", str(OUT / "preview.png"), str(WORK / "preview.svg")], check=True)
print(f"Built the STAR Polaris identity in {OUT}")

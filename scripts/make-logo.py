#!/usr/bin/env python3
"""Build STAR's S-and-spark identity as vector SVG/PDF and transparent PNG.

STAR stands for System Trustworthiness and AI Reliability.

Regeneration uses rsvg-convert and pdftocairo. STAR LAB is drawn entirely
with custom paths; only the expanded-name descriptor uses Arial during
regeneration. All final assets contain outlines, so Overleaf and consumers
do not need any fonts or external tools.
"""
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WORK = ROOT / "build" / "identity-polish"
ASSETS.mkdir(exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
MIDNIGHT, CYAN = "#25356B", "#00A8C6"
FULL_NAME = "System Trustworthiness and AI Reliability"


def emblem(primary, accent, small=False):
    """Balanced S strokes rotate around a centered star-shaped opening.

    The small-use drawing opens the narrow channels for 16-32 pixel icons.
    Both versions remain vector paths with real transparent negative space.
    """
    tip, reach, shoulder, tail = (49, 29, 47, 50) if small else (51, 31, 49, 52)
    curve = f'''M44 5 H96 C93 20 82 28 66 28 H34
      C36 32 42 34 {tip} 36 L{shoulder} 45 Q{shoulder-1} 48 45 49 L{reach} 52
      L45 55 Q{shoulder-1} 56 {shoulder} 59 L{tail} 69 L28 63
      C12 60 5 53 5 42 C5 22 25 5 44 5 Z'''
    return (f'<path fill="{primary}" d="{curve}"/>'
            f'<path fill="{accent}" transform="rotate(180 52 52)" d="{curve}"/>')


def lettering(primary, shift=0):
    # Custom geometric letters share a 56-unit cap height and 10-12-unit
    # strokes. Angled S/T terminals echo the emblem; the A repeats its star.
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
    return (f'<g fill="{primary}" fill-rule="evenodd" transform="translate(0 {shift})">'
            f'<g transform="translate(120 24)">{star}</g>'
            f'<g transform="translate(352 56.06) scale(.84)">{lab}</g></g>')


def document(contents, width, height, title, description):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" '
            'viewBox="0 0 %s %s" role="img" aria-labelledby="title desc">'
            '<title id="title">%s</title><desc id="desc">%s</desc>%s</svg>' %
            (width, height, width, height, title, description, contents))


def export(name, svg, width, outline=False):
    source = WORK / (name + "-source.svg")
    source.write_text(svg)
    pdf = ASSETS / (name + ".pdf")
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(source)], check=True)
    destination = ASSETS / (name + ".svg")
    if outline:
        # Cairo converts supporting lettering to reusable glyph paths.
        subprocess.run(["pdftocairo", "-svg", str(pdf), str(destination)], check=True)
        # Re-export the outlined SVG so the PDF also contains no font objects.
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf),
                        str(destination)], check=True)
    else:
        destination.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(width), "-o",
                    str(ASSETS / (name + ".png")), str(destination)], check=True)


for suffix, primary, accent in [("", MIDNIGHT, CYAN),
                                 ("-mono", "#202020", "#202020"),
                                 ("-reverse", "#FFFFFF", CYAN)]:
    mark = emblem(primary, accent)
    export("star-mark" + suffix,
           document(mark, 104, 104, "STAR Lab S monogram",
                    "Sculpted S strokes surround a centered four-point star. " + FULL_NAME), 1040)
    export("star-mark-small" + suffix,
           document(emblem(primary, accent, small=True), 104, 104,
                    "STAR Lab small-use monogram", "Open-channel variant for small icons."), 1040)
    lockup = mark + lettering(primary)
    export("star-lockup" + suffix,
           document(lockup, 432, 104, "STAR Lab",
                    "S-and-star monogram and custom-drawn STAR LAB lettering. " + FULL_NAME),
           2240)
    signature = (mark + lettering(primary, shift=-8) +
                 f'<text x="120" y="99" fill="{primary}" '
                 'font-family="Arial, sans-serif" font-size="14.5" '
                 f'font-weight="400">{FULL_NAME}</text>')
    export("star-signature" + suffix,
           document(signature, 432, 104, "STAR Lab - " + FULL_NAME,
                    "The full lab signature for larger uses."), 2240, outline=True)

# Native vector rendering for small application icons; no bitmap tracing.
for size in [16, 24, 32, 48, 64, 128, 256]:
    source = ASSETS / ("star-mark-small.svg" if size <= 32 else "star-mark.svg")
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    "-o", str(ASSETS / f"star-icon-{size}.png"), str(source)], check=True)
icon_sizes = [16, 32, 48]
icon_data = [(ASSETS / f"star-icon-{size}.png").read_bytes() for size in icon_sizes]
offset = 6 + 16 * len(icon_sizes)
entries = []
for size, payload in zip(icon_sizes, icon_data):
    entries.append(struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(payload), offset))
    offset += len(payload)
(ASSETS / "star-favicon.ico").write_bytes(
    struct.pack("<HHH", 0, 1, len(icon_sizes)) + b"".join(entries) + b"".join(icon_data))

# A presentation preview is intentionally on white; production PNGs remain
# transparent, including the reverse mark for dark backgrounds.
color = (ASSETS / "star-lockup.svg").read_text()
start = color.index(">", color.index("<svg")) + 1
color = color[:start] + '<rect width="100%" height="100%" fill="white"/>' + color[start:]
(WORK / "preview.svg").write_text(color)
(ROOT / "output").mkdir(exist_ok=True)
subprocess.run(["rsvg-convert", "-w", "1792", "-o",
                str(ROOT / "output" / "STAR-logo-preview.png"),
                str(WORK / "preview.svg")], check=True)

# A review sheet shows the actual identity at large, small, and one-ink sizes.
sheet = ('<rect width="1280" height="650" fill="white"/>'
         '<text x="72" y="48" font-family="Arial, sans-serif" font-size="12" '
         'letter-spacing="1.4" fill="#5C6577">STAR LAB / IDENTITY SYSTEM</text>'
         '<g transform="translate(72 90) scale(2.6)">' + emblem(MIDNIGHT, CYAN) +
         lettering(MIDNIGHT, shift=-8) +
         f'<text x="120" y="99" fill="{MIDNIGHT}" font-family="Arial, sans-serif" '
         f'font-size="14.5">{FULL_NAME}</text></g>'
         '<path d="M72 410 H1208" stroke="#D3DBE7"/>'
         '<text x="72" y="460" font-family="Arial, sans-serif" font-size="11" '
         'letter-spacing="1" fill="#5C6577">SMALL-SIZE MARK</text>'
         '<text x="440" y="460" font-family="Arial, sans-serif" font-size="11" '
         'letter-spacing="1" fill="#5C6577">ONE COLOR</text>')
for size, x in [(16, 72), (24, 136), (32, 208), (48, 288)]:
    sheet += (f'<g transform="translate({x} {532-size}) scale({size/104})">' +
              emblem(MIDNIGHT, CYAN, small=size<=32) + '</g>' +
              f'<text x="{x}" y="560" font-family="Arial, sans-serif" '
              f'font-size="12" fill="#5C6577">{size}px</text>')
sheet += ('<g transform="translate(440 486) scale(.72)">' + emblem("#202020", "#202020") +
          lettering("#202020") + '</g>'
          f'<rect x="848" y="438" width="360" height="148" rx="12" fill="{MIDNIGHT}"/>'
          '<text x="866" y="462" font-family="Arial, sans-serif" font-size="11" '
          'letter-spacing="1" fill="white">ON DARK</text>'
          '<g transform="translate(866 485) scale(.75)">' + emblem("#FFFFFF", CYAN) +
          lettering("#FFFFFF") + '</g>')
(WORK / "identity-preview.svg").write_text(document(
    sheet, 1280, 650, "STAR Lab identity", FULL_NAME))
subprocess.run(["rsvg-convert", "-o", str(ROOT / "output" / "STAR-identity-preview.png"),
                str(WORK / "identity-preview.svg")], check=True)
print("Built color, monochrome, and reverse S-and-star monograms and lockups.")

#!/usr/bin/env python3
"""Produce self-contained Overleaf ZIPs; never package the user's examples."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "templates" / "paper"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
SHARED = ["starpaper.cls", "macros.tex", "references.bib", "README.md"]

def add_file(z, source, destination=None):
    p = (ROOT if source.startswith("scripts/") else PAPER) / source
    z.write(p, destination or source)

for layout in ["single", "double", "complete"]:
    name = f"STAR-{layout}-column-Overleaf.zip" if layout != "complete" else "STAR-complete-Overleaf-kit.zip"
    with zipfile.ZipFile(OUTPUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in SHARED:
            add_file(z, f)
        for folder in ["assets", "figures", "scripts"]:
            for p in sorted(((ROOT if folder == "scripts" else PAPER) / folder).rglob("*")):
                if p.is_file() and "__pycache__" not in p.parts and not p.name.startswith("."):
                    if p.name in ["build-demos.py", "new-project.py", "package.py"]:
                        continue
                    add_file(z, p.relative_to(ROOT if folder == "scripts" else PAPER).as_posix())
        layouts = ["single", "double"] if layout == "complete" else [layout]
        for item in layouts:
            add_file(z, f"paper-info-{item}.tex")
            for p in sorted((PAPER / "sections" / item).glob("*.tex")):
                add_file(z, p.relative_to(PAPER).as_posix())
        if layout == "complete":
            add_file(z, "main.tex")
            add_file(z, "main-double.tex")
        else:
            add_file(z, "main.tex" if layout == "single" else "main-double.tex", "main.tex")
    print(OUTPUT / name)

with zipfile.ZipFile(OUTPUT / "STAR-logo-assets.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted((PAPER / "assets").iterdir()):
        if p.is_file() and not p.name.startswith("."):
            z.write(p, p.name)
    for name in ["STAR-logo-preview.png", "STAR-identity-preview.png"]:
        preview = OUTPUT / name
        if preview.is_file():
            z.write(preview, preview.name)
print(OUTPUT / "STAR-logo-assets.zip")

with zipfile.ZipFile(OUTPUT / "STAR-letter-Overleaf.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted((ROOT / "templates" / "letter").rglob("*")):
        if p.is_file() and p.suffix in {".tex", ".sty", ".txt", ".pdf", ".png", ".jpg"} and not p.name.startswith("."):
            z.write(p, p.relative_to(ROOT / "templates" / "letter"))
print(OUTPUT / "STAR-letter-Overleaf.zip")

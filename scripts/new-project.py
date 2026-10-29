#!/usr/bin/env python3
"""Create a self-contained paper or letter in the Git-ignored projects directory."""
import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["paper", "letter"])
    parser.add_argument("name", help="Project folder name (letters, digits, hyphens, underscores)")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.name):
        parser.error("Use letters, digits, hyphens, or underscores; start with a letter or digit.")
    destination = ROOT / "projects" / ("papers" if args.kind == "paper" else "letters") / args.name
    if destination.exists():
        parser.error(f"Project already exists: {destination}")
    shutil.copytree(ROOT / "templates" / args.kind, destination,
                    ignore=shutil.ignore_patterns("*.log", "*.aux", "*.out", ".DS_Store", "__pycache__"))
    if args.kind == "letter":
        (destination / "recommendation-template.tex").rename(destination / "main.tex")
    print(f"Created {destination.relative_to(ROOT)}")
    print(f"Edit and compile main.tex from {destination}")

if __name__ == "__main__":
    main()

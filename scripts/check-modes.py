#!/usr/bin/env python3
"""Smoke-check anonymous metadata, hidden branding, and grayscale logo routing.

Run from any directory. Requires Tectonic, pdfinfo, and pdftotext.
Usage: python3 scripts/check-modes.py --engine tectonic [--bundle PATH]
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = r"""
\documentclass[OPTIONS]{starpaper}
\title{A Neutral Research Manuscript}
\author{IDENTITYTOKEN}
\staraffiliation{AFFILIATIONTOKEN}
\staremails{EMAILTOKEN}
\startrack{TRACKTOKEN}
\starstatus{STATUSTOKEN}
\starversion{VERSIONTOKEN}
\starpartner{PARTNERTOKEN}{}
\starproject[PROJECTTOKEN]{https://example.org/PROJECTTOKEN}
\stargithub{https://example.org/GITHUBTOKEN/repo_name}
\stardataset[DATASETTOKEN]{https://example.org/DATASETTOKEN/data_v1}
\starshorttitle{Neutral Running Title}
\starpaperid{2468}
\starkeywords{learning; systems}
\begin{document}
\maketitle
\begin{abstract}A neutral abstract for mode validation.\end{abstract}
\section{A Neutral Section}
This text checks the first page. \starlogo[20pt]
\ifstaranonymous\stargmumark\starpartnermark\fi
\clearpage
\section{A Second Neutral Section}
This text checks running headers and footers on a subsequent page.
\staracknowledgments{ACKTOKEN}
\end{document}
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default=shutil.which("tectonic"))
    parser.add_argument("--bundle")
    args = parser.parse_args()
    if not args.engine:
        raise SystemExit("Tectonic is required for this optional check.")
    for layout in ["singlecolumn", "twocolumn"]:
        for mode in ["anonymous", "monochrome"]:
            out = ROOT / "build" / "modes" / f"{layout}-{mode}"
            out.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".tex",
                                             prefix=".star-check-", dir=ROOT,
                                             delete=False) as f:
                f.write(FIXTURE.replace("OPTIONS", f"{layout},{mode}"))
                source = Path(f.name)
            try:
                cmd = [args.engine, "--keep-logs", "--outdir", str(out)]
                if args.bundle:
                    cmd += ["--bundle", args.bundle]
                cmd += [str(source)]
                run = subprocess.run(cmd, cwd=ROOT, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                (out / "compile.log").write_text(run.stdout)
                if run.returncode:
                    raise RuntimeError(f"Build failed; inspect {out / 'compile.log'}")
                pdf = out / f"{source.stem}.pdf"
                text = subprocess.check_output(["pdftotext", str(pdf), "-"], text=True)
                metadata = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
                urls = subprocess.check_output(["pdfinfo", "-url", str(pdf)], text=True)
                log = (out / f"{source.stem}.log").read_text(errors="replace")
                if mode == "anonymous":
                    for token in ["IDENTITYTOKEN", "AFFILIATIONTOKEN", "EMAILTOKEN",
                                  "TRACKTOKEN", "STATUSTOKEN", "VERSIONTOKEN",
                                  "ACKTOKEN", "PARTNERTOKEN", "STAR", "George Mason",
                                  "PROJECTTOKEN", "GITHUBTOKEN", "DATASETTOKEN",
                                  "Project page", "GitHub", "Dataset",
                                  "GEORGE MASON", "UNIVERSITY",
                                  "System Trustworthiness", "AI Reliability",
                                  "SYSTEM TRUSTWORTHINESS", "AI RELIABILITY"]:
                        assert token not in text + metadata + urls, f"Identity leak: {token}"
                    assert "Anonymous authors" in text + metadata
                    assert "2468" in text
                    assert "assets/star-mark" not in log
                    assert "assets/star-lockup" not in log
                    assert "assets/institutions/gmu-logo.png" not in log
                else:
                    assert "IDENTITYTOKEN" in text
                    assert "assets/star-mark-mono.pdf" in log
                    assert "assets/star-lockup-mono.pdf" in log
                    assert "assets/star-mark.pdf" not in log
                    assert "assets/star-lockup.pdf" not in log
                    assert "PARTNERTOKEN" in text
                    assert "GEORGE MASON" in text and "UNIVERSITY" in text
                    assert "SYSTEM TRUSTWORTHINESS AND AI RELIABILITY" in text
                    assert "System Trustworthiness and AI Reliability" in metadata
                    assert "assets/institutions/gmu-logo.png" not in log
                    for url in ["https://example.org/PROJECTTOKEN",
                                "https://example.org/GITHUBTOKEN/repo_name",
                                "https://example.org/DATASETTOKEN/data_v1"]:
                        assert url in urls, f"Missing or damaged resource link: {url}"
                    assert "PROJECTTOKEN" in text and "DATASETTOKEN" in text
                assert "??" not in text
                print(f"PASS: {layout}, {mode}", flush=True)
            finally:
                source.unlink()

if __name__ == "__main__":
    main()
